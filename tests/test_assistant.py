import unittest

from apiai_assistant.assistant import Assistant
from apiai_assistant.agent import Agent, Status

from tests import get_dummy_request


class AssistantTestCase(unittest.TestCase):
    def test_intent(self):
        ass = Assistant()

        @ass.intent('foo')
        def bar(agent):
            return 42

        self.assertEqual(ass.action_map['foo'], bar)

    def test_process(self):
        ass = Assistant()

        @ass.intent('foo')
        def bar(agent):
            agent.tell_raw('foobar')

        request = get_dummy_request()
        request['result']['action'] = 'foo'
        agent = ass.process(request)
        self.assertEqual(len(agent.response._messages), 2)
        self.assertEqual(
            agent.response._messages,
            [
                agent.response.initial_message,
                {'platform': 'google',
                 'ssml': '<speak>foobar</speak>',
                 'displayText': 'foobar',
                 'type': 'simple_response'}
            ]
        )

    def test_process_invalid(self):
        ass = Assistant()

        @ass.intent('foo')
        def bar(agent):
            agent.tell_raw('foobar')

        request = get_dummy_request()
        request['result']['action'] = 'foo'
        agent = ass.process(request)
        self.assertEqual(len(agent.response._messages), 2)
        self.assertEqual(
            agent.response._messages,
            [
                agent.response.initial_message,
                {'platform': 'google',
                 'ssml': '<speak>foobar</speak>',
                 'displayText': 'foobar',
                 'type': 'simple_response'}
            ]
        )

    def test_header_check(self):
        magic_key = 'the human eye can only see at 30fps'
        ass = Assistant(magic_key=magic_key)

        @ass.intent('foo')
        def bar(agent):
            agent.tell_raw('foobar')

        request = get_dummy_request()
        request['result']['action'] = 'foo'

        agent = ass.process(request, headers={'magic-key': magic_key[::-1]})
        self.assertEqual(agent.code, Status.AccessDenied)
        self.assertEqual(agent.error_message, 'Could not verify request')

        agent = ass.process(request, headers={'magic-key': magic_key})
        self.assertEqual(agent.code, Status.OK)
        self.assertEqual(len(agent.response._messages), 2)
        self.assertEqual(
            agent.response._messages,
            [
                agent.response.initial_message,
                {'platform': 'google',
                 'ssml': '<speak>foobar</speak>',
                 'displayText': 'foobar',
                 'type': 'simple_response'}
            ]
        )

    def test_validate_parser(self):
        ass = Assistant()
        agent = Agent()
        ass.validate(agent)

        self.assertEqual(agent.code, Status.InvalidData)
        self.assertEqual(agent.error_message, 'Could not instantiate parser')

    def test_validate_request(self):
        ass = Assistant()
        agent = Agent(request={'result': {}, 'originalRequest': {}})
        ass.validate(agent)

        self.assertEqual(agent.code, Status.InvalidData)
        self.assertEqual(agent.error_message, 'Could not validate data')

    def test_validate_action(self):
        ass = Assistant()
        action = 'foo'

        @ass.intent(action)
        def bar(agent):
            return 42

        self.assertEqual(ass.action_map[action], bar)

        request = get_dummy_request()
        request['result']['action'] = action[::-1]
        agent = Agent(request=request)
        ass.validate(agent)
        self.assertEqual(agent.code, Status.InvalidData)
        self.assertEqual(agent.error_message, 'Could not understand action')

if __name__ == '__main__':
    unittest.main()
