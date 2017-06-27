import functools

from .corpus import Corpus
import agent


class Assistant(object):

    def __init__(
            self, ssml=True, corpus=None, magic_key=None, *args, **kwargs):
        self._ssml = ssml
        self.corpus = None
        self.action_map = {}

        if corpus is not None:
            self.corpus = Corpus(corpus)

        self.magic_key = magic_key

    def intent(self, action_id):
        def decorator(f):
            self.action_map[action_id] = f

            @functools.wraps(f)
            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)
            return f

        return decorator

    def validate(self, agent_instance):
        if not agent_instance.parser:
            agent_instance.code = agent.Status.KO
            agent_instance.error_message = 'Could not instantiate parser'
            return False

        if not agent_instance.parser.is_valid:
            agent_instance.code = agent.Status.KO
            agent_instance.error_message = 'Could not validate data'
            return False

        print '\n - Actions: {}'.format(self.action_map.keys())
        print '\n - Action: {}'.format(agent_instance.parser.action)

        if not agent_instance.parser.action or agent_instance.parser.action not in self.action_map:
            agent_instance.code = agent.Status.KO
            agent_instance.error_message = 'Could not understand action'
            return False
        print '\n - HTTP Request: {}'.format(agent_instance.parser.data)
        print '\n - API.AI Request: {}'.format(agent_instance.parser.request)
        print '\n - Agent: {} {}'.format(agent_instance.code, agent_instance.error_message)
        print '\n - Valid: {}'.format(agent_instance.code == agent.Status.OK)

        return True

    def process(self, request, headers=None):
        agent_instance = agent.Agent(
            corpus=self.corpus,
            request=request,
            ssml=self._ssml
        )

        if headers:
            h_magic_key = headers.get('magic-key')
            if h_magic_key and self.magic_key and h_magic_key != self.magic_key:
                agent_instance.code = agent.Status.KO
                agent_instance.error_message = 'Could not verify request'
                return agent_instance

        if self.validate(agent_instance):
            action = self.action_map[agent_instance.parser.action]
            action(agent_instance)

        print '\n - Response: {}'.format(agent_instance.response.to_dict())
        return agent_instance

