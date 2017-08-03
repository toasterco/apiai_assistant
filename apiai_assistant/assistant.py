""" Assistant.

Provides a masterclass for all assistant related needs.
Instantiate Assistant and use it to register intent and process requests """

import logging
import functools

import agent
from .corpus import Corpus


class Assistant(object):
    """ Entrypoint for the apiai_assistant package. The Assistant class
    manages the different intents of the agent and processes the requests

    Args:
        ssml (bool, optional, True): speech is formatted to SSML if True
        corpus (str, optional): path to the corpus json file
        magic_key (str, optional): magic key to verify requests
    """

    def __init__(
            self, ssml=True, corpus=None, magic_key=None, *args, **kwargs):
        self._ssml = ssml
        self.corpus = None
        self.action_map = {}

        if corpus is not None:
            self.corpus = Corpus(corpus)

        self.magic_key = magic_key

    def intent(self, action_id):
        """ Decorator to register actions

        Example:
            @intent('action-id')
            def foo(agent):
                pass

        Args:
            action_id (str): id of the action to register

        Returns:
            a decorator to register the action
        """

        def decorator(f):
            self.action_map[action_id] = f

            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)
            return f

        return decorator

    def validate(self, agent_instance):
        """ Validate an agent instance and update its code and error_message
        if the agent instance is not valid

        Args:
            agent_instance (:obj:`apiai_assistant.agent.Agent`): agent instance

        Returns:
            bool: True if valid, False otherwise.

        """

        if not agent_instance.parser:
            agent_instance.error('Could not instantiate parser',
                                 code=agent.Status.InvalidData)
            return False

        if not agent_instance.parser.is_valid:
            agent_instance.error('Could not validate data',
                                 code=agent.Status.InvalidData)
            return False

        logging.debug("""
        - Actions: {actions}
        - Action: {action}""".format(
            actions=self.action_map.keys(),
            action=agent_instance.parser.action))

        if (not agent_instance.parser.action
           or agent_instance.parser.action not in self.action_map):
            agent_instance.error('Could not understand action',
                                 code=agent.Status.InvalidData)
            return False

        logging.debug("""
        - HTTP Request: {data}
        - API.AI Request: {request}
        - Agent: {code} {message}
        - Valid: {valid}""".format(
            data=agent_instance.parser.data,
            request=agent_instance.parser.request,
            code=agent_instance.code,
            message=agent_instance.error_message,
            valid=agent_instance.code == agent.Status.OK))

        return True

    def process(self, request, headers=None):
        """ Processes the API.ai request and return an agent with the action
        performed in it

        Args:
            request (:obj:`dict`): request received from API.ai
            headers (:obj:`dict`, optional): headers of the HTTP request to verify it

        Returns:
            :obj:`apiai_assistant.agent.Agent`: Agent instance with the action performed in it
        """

        agent_instance = agent.Agent(
            corpus=self.corpus,
            request=request,
            ssml=self._ssml
        )

        if headers and type(headers) is dict:
            h_magic_key = headers.get('magic-key')
            if h_magic_key and self.magic_key and h_magic_key != self.magic_key:
                agent_instance.error('Could not verify request',
                                     code=agent.Status.AccessDenied)
                return agent_instance

        if self.validate(agent_instance):
            action = self.action_map[agent_instance.parser.action]
            action(agent_instance)

        logging.debug('- Response: {}'.format(
            agent_instance.response.to_dict()))

        return agent_instance

