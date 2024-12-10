# SPDX-FileCopyrightText: 2024-present Oori Data <info@oori.dev>
#
# SPDX-License-Identifier: Apache-2.0
# toolio.client
'''
Encapsulate HTTP query of LLMs for structured response, as hosted by MLXStructuredLMServer

Modeled on ogbujipt.llm_wrapper.openai_api & ogbujipt.llm_wrapper.openai_chat_api

'''
# import logging
import json
import warnings
import logging
from enum import Flag, auto

import httpx
# import asyncio

from amara3 import iri

from ogbujipt import config
from ogbujipt.llm_wrapper import llm_response, response_type

from toolio.common import TOOLIO_MODEL_TYPE_FIELD, TOOL_CHOICE_AUTO, TOOL_CHOICE_NONE, FLAGS_LOOKUP
from toolio.common import DEFAULT_JSON_SCHEMA_CUTOUT, DEFAULT_FLAGS as DEFAULT_MODEL_FLAGS
from toolio.common import model_client_mixin
from toolio.prompt_helper import set_tool_response


class tool_flag(Flag):
    REMOVE_USED_TOOLS = auto()  # Remove tools which the LLM has already used from subsequent trips


DEFAULT_FLAGS = tool_flag.REMOVE_USED_TOOLS
# Tool choice feels like it could be an enum, but it's not clear that the valus are fixed across conventions

HTTP_SUCCESS = 200


class struct_mlx_chat_api(model_client_mixin):
    '''
    Wrapper for OpenAI chat-style LLM API endpoint, with support for structured responses
    via schema specifiation in query

    Note: Only supports chat-style completions

    >>> import asyncio; from toolio.client import struct_mlx_chat_api
    >>> llm = struct_mlx_chat_api(base_url='http://localhost:8000')
    >>> resp = asyncio.run(llm_api(prompt_to_chat('Knock knock!')))
    >>> resp.first_choice_text
    '''
    def __init__(self, base_url=None, default_schema=None, flags=DEFAULT_FLAGS, tool_reg=None, logger=logging,
                 json_schema_cutout=DEFAULT_JSON_SCHEMA_CUTOUT, **kwargs):
        '''
        Args:
            base_url (str, optional): Base URL of the API endpoint
                (should be a MLXStructuredLMServer host, or equiv)

            flags (int, optional): bitwise flags to control tool flow

            tool_reg (list) - Tools with available implementations, in registry format, i.e. each item is one of:
                * Python import path for a callable annotated (i.e. using toolio.tool.tool decorator)
                * actual callable, annotated (i.e. using toolio.tool.tool decorator)
                * tuple of (callable, schema), with separately specified schema
                * tuple of (None, schema), in which case a tool is declared (with schema) but with no implementation

            logger - logger object, handy for tracing operations

            json_schema_cutout - Prompt text which should be replaced by actual JSON schema

            kwargs (dict, optional): Extra parameters for the API or for the model host
        '''
        self.parameters = config.attr_dict(kwargs)
        self.default_schema = default_schema
        self.json_schema_cutout = json_schema_cutout
        self.base_url = base_url
        if self.base_url:
            # If the user includes the API version in the base, don't add it again
            scheme, authority, path, query, fragment = iri.split_uri_ref(base_url)
            path = path or kwargs.get('api_version', '/v1')
            self.base_url = iri.unsplit_uri_ref((scheme, authority, path, query, fragment))
            # self.base_url = self.base_url.rstrip('/')  # SHould already e free of trailing /
        if not self.base_url:
            # FIXME: i18n
            warnings.warn('base_url not provided, so each invocation will require one', stacklevel=2)
        # OpenAI-style tool-calling LLMs give IDs to tool requests by the LLM
        # Internal structure to manage these. Key is tool_call_id; value is tuple of callable, kwargs
        # self._pending_tool_calls = {}
        self._flags = flags
        super().__init__(tool_reg=tool_reg, logger=logger)

    async def __call__(self, messages, req='chat/completions', json_schema=None, toolset=None, sysprompt=None,
                       tool_choice=TOOL_CHOICE_AUTO, apikey=None, max_trips=3, trip_timeout=90.0, json_schema_cutout=None, **kwargs):
        '''
        Invoke the LLM with a completion request

        Args:
            messages (str) - Prompt in the form of list of messages to send ot the LLM for completion.
                If you have a system prompt, and you are setting up to call tools, it will be updated with
                the tool spec

            req (str) - API endpoint to invoke

            json_schema - JSON schema to be used to guide the final generation step (after all tool-calling, if any)

            sysprompt (str) - System prompt to use in the chat messages

            toolset (list) - tools specified for this request, presumably a subset of overall tool registry.
                Each entry is either a tool name, in which the invocation schema is as registered, or a full
                tool-calling format stanza, in which case, for this request, only the implementaton is used
                from the initial registry

            trip_timeout (float) - timeout (in seconds) per LLM API request trip; defaults to 90s

            json_schema_cutout (str) - Prompt text which should be replaced by actual JSON schema;
                overrides instance default

            kwargs (dict, optional): Extra parameters to pass to the model via API.
                See Completions.create in OpenAI API, but in short, these:
                temperature, max_tokens, best_of, echo, frequency_penalty, logit_bias, logprobs,
                presence_penalty, seed, stop, stream, suffix, top_p, userq
        Returns:
            dict: JSON response from the LLM
        '''
        # Uncomment for test case construction
        # print('MESSAGES', messages, '\n', 'json_schema', json_schema, '\n', 'TOOLS', toolset)
        toolset = toolset or self.toolset
        json_schema_cutout = json_schema_cutout or self.json_schema_cutout
        req = req.strip('/')
        req_tools = self._resolve_tools(toolset)
        req_tool_spec = [ s for f, s in req_tools.values() ]

        if max_trips < 1:
            raise ValueError(f'At least one trip must be permitted, but {max_trips=}')
        schema = json_schema or self.default_schema  # Remember: default, default schema (😂) is None
        schema_str = None
        if schema:
            schema_str = json.dumps(schema)

            # Replace JSON schema cutout references with the actual schema
            cutout_replaced = False
            for m in messages:
                # XXX: content should always be in m, though. Validate?
                if 'content' in m and json_schema_cutout in m['content']:
                    m['content'] = m['content'].replace(json_schema_cutout, schema_str)
                    cutout_replaced = True

            if not cutout_replaced:
                warnings.warn('JSON Schema provided, but no place found to replace it.'
                            ' Will be tacked on the end of the first user message', stacklevel=2)
                target_msg = next(m for m in messages if m['role'] == 'user')
                target_msg['content'] += '\nRespond in JSON according to this schema: ' + schema_str

        req_data = {'messages': messages, **kwargs}
        if toolset:
            req_data['tool_choice'] = tool_choice
            if req_tools and tool_choice == TOOL_CHOICE_NONE:
                warnings.warn('Tools were provided, but tool_choice was set to `none`, so they\'ll never be used')
            # if tool_options: req_data['tool_options'] = tool_options
            # for t in tools_list:
            #     self.register_tool(t['function']['name'], t['function'].get('pyfunc'))
            req_data['tools'] = [ {'type': 'function', 'function': t} for t in req_tool_spec ]

            # Enter tool-calling sequence
            llm_call_needed = True
            while max_trips > 0 and llm_call_needed:
                # If the tools list is empty (perhaps we removed the last one in a prev loop), omit it entirely
                if 'tools' in req_data and not req_data['tools']:
                    del req_data['tools']
                    # XXX: Interplay between tool use & schema is actually much trickier than it seems, at first
                    if schema:
                        req_data['response_format'] = {'type': 'json_object', 'schema': schema_str}
                resp = await self._http_trip(req, req_data, trip_timeout, apikey, **kwargs)
                max_trips -= 1
                # If LLM has asked for tool calls, prepare to loop back
                if resp['response_type'] == response_type.TOOL_CALL:
                    bypass_response = self._check_tool_handling_bypass(resp)
                    if bypass_response:
                        # LLM refused to call a tool, and provided an alternative response
                         return llm_response.from_openai_chat(bypass_response)

                    if not max_trips:
                        # If there are no more available trips, don't bother calling the tools
                        self.logger.debug('Maximum trips exhausted')
                        return resp

                    tool_responses = await self._execute_tool_calls(resp, req_tools)
                    for call_id, callee_name, callee_args, result in tool_responses:
                        model_type = resp.get(TOOLIO_MODEL_TYPE_FIELD)
                        model_flags = FLAGS_LOOKUP.get(model_type, DEFAULT_MODEL_FLAGS)
                        # print(model_type, model_flags, model_flags and model_flag.TOOL_RESPONSE in model_flags)
                        if not model_flags:
                            warnings.warn(f'Unknown model type {model_type} specified by server. Likely client/server version skew')
                        # logging.info(f'{messages=}')
                        set_tool_response(messages, call_id, callee_name, callee_args, str(result), model_flags=model_flags)
                        # logging.info(f'{messages=}')
                        if tool_flag.REMOVE_USED_TOOLS in self._flags:
                            # Many FLOSS LLMs get confused if they see a tool definition still in the response back
                            # And loop back with a new tool request. Remove it to avoid this.
                            remove_list = [
                                i for (i, t) in enumerate(req_data.get('tools', []))
                                if t.get('function', {}).get('name') == callee_name]
                            # print(f'removing tools with index {remove_list} from request structure')
                            for i in remove_list:
                                req_data['tools'].pop(i)
                else:
                    llm_call_needed = False

            # Loop exited. We have a final response, or exhausted allowed trips
            if max_trips <= 0:
                # FIXME: i18n
                warnings.warn('Maximum LLM trips exhausted without a final answer')

        elif schema:
            req_data['response_format'] = {'type': 'json_object', 'schema': schema_str}
            resp = await self._http_trip(req, req_data, trip_timeout, apikey, **kwargs)

        else:
            resp = await self._http_trip(req, req_data, trip_timeout, apikey, **kwargs)

        return resp

    async def _http_trip(self, req, req_data, timeout, apikey, **kwargs):
        '''
        Single call/response to toolio_server. Multiple might be involved in a single tool-calling round

        req must not end with '/'
        '''
        header = {'Content-Type': 'application/json'}
        # if apikey is None:
        #     apikey = self.apikey
        # if apikey:
        #     header['Authorization'] = f'Bearer {apikey}'
        async with httpx.AsyncClient() as client:
            result = await client.post(
                f'{self.base_url}/{req}', json=req_data, headers=header, timeout=timeout)
            if result.status_code == HTTP_SUCCESS:
                res_json = result.json()
                # print('RESULT_JSON', res_json)
                resp_msg = res_json['choices'][0]['message']
                assert resp_msg['role'] == 'assistant'
                resp = llm_response.from_openai_chat(res_json)
                return resp
            else:
                raise RuntimeError(f'Unexpected response from {self.base_url}/{req}:\n{repr(result)}')

    def lookup_tool(self, name):
        '''
        Given a function/tool name, return the callable which implements it
        '''
        # print('lookup_tool', name)
        if name in self._tool_registry:
            return self._tool_registry[name]
        else:
            # FIXME: i18n
            raise LookupError(f'Unknown tool: {name}')

    # def update_tool_calls(self, response):
    #     # print('update_tool_calls', response)
    #     for tc in response['choices'][0].get('message', {}).get('tool_calls'):
    #         callee_name = tc['function']['name']
    #         callee_args = tc['function']['arguments_obj']
    #         tool = self.lookup_tool(callee_name)
    #         self._pending_tool_calls[tc['id']] = (tool, callee_args)


def cmdline_tools_struct(tools_obj):
    'Specifying a function on the command line calls for its own format. Processes it for model managers'
    if isinstance(tools_obj, dict):
        tools_list = tools_obj['tools']
    elif isinstance(tools_obj, str):
        tools_list = [tools_obj]
    else:
        tools_list = tools_obj or []
    new_tools_list = []
    for t in tools_list:
        if isinstance(t, dict):
            tf = t['function']
            new_tools_list.append((tf.get('pyfunc'), tf))
            if 'pyfunc' in tf: del tf['pyfunc']   # noqa: E701
        else:
            new_tools_list.append(t)
    return new_tools_list
