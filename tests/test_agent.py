import mock
import unittest

from tests import mocked_init_corpus

from apiai_assistant.agent import Response
from apiai_assistant.agent import Agent
from apiai_assistant.agent import Status
from apiai_assistant.corpus import Corpus
from apiai_assistant.widgets import LinkOutChipWidget


FAKE_CORPUS = {
    "corpus": {'foo': ['bar']},
    "suggestions": {'confirmation': [['Yes', 'No']]}
}


class ResponseTestCase(unittest.TestCase):
    def test_open_mic(self):
        r = Response()
        self.assertFalse(r.to_dict()['data']['google']['expectUserResponse'])
        r.open_mic()
        self.assertTrue(r.to_dict()['data']['google']['expectUserResponse'])

    def test_close_mic(self):
        r = Response()
        r.open_mic()
        self.assertTrue(r.to_dict()['data']['google']['expectUserResponse'])
        r.close_mic()
        self.assertFalse(r.to_dict()['data']['google']['expectUserResponse'])

    def test_to_dict(self):
        r = Response()
        payload = r.to_dict()
        self.assertTrue('messages' in payload)
        self.assertTrue('data' in payload)
        self.assertTrue('contextOut' not in payload)

        r.add_context({'foo': 'bar'})
        payload = r.to_dict()
        self.assertTrue('messages' in payload)
        self.assertTrue('data' in payload)
        self.assertTrue('contextOut' in payload)

    def test_add_message(self):
        r = Response()
        self.assertEqual(r._messages, [r.initial_message])

        r.add_message({'foo': 'bar'})
        self.assertEqual(
            r._messages,
            [r.initial_message, {'foo': 'bar'}]
        )

        r.add_message({'bar': 'foo'}, 0)
        self.assertEqual(
            r._messages,
            [{'bar': 'foo'}, r.initial_message, {'foo': 'bar'}]
        )

    def test_add_context(self):
        r = Response()
        self.assertEqual(r._contexts, [])

        r.add_context({'foo': 'bar'})
        self.assertEqual(
            r._contexts,
            [{'foo': 'bar'}]
        )

        r.add_context({'bar': 'foo'}, 0)
        self.assertEqual(
            r._contexts,
            [{'bar': 'foo'}, {'foo': 'bar'}]
        )

    def test_add_permission(self):
        r = Response()
        self.assertEqual(r._permissions, [])

        r.add_permission('because', [Agent.SupportedPermissions.NAME])
        self.assertEqual(
            r._permissions,
            [('because', [r.PERMISSIONS[Agent.SupportedPermissions.NAME]])]
        )

        r.add_permission('cause', [Agent.SupportedPermissions.NAME])
        self.assertEqual(
            r._permissions,
            [('because', [r.PERMISSIONS[Agent.SupportedPermissions.NAME]]),
             ('cause', [r.PERMISSIONS[Agent.SupportedPermissions.NAME]])]
        )

    def test_to_dict_permissions(self):
        r = Response()
        r.add_permission('because', [Agent.SupportedPermissions.NAME])
        r.add_permission('cause', [Agent.SupportedPermissions.NAME])

        data = r.to_dict()['data']['google']['systemIntent']['data']
        self.assertEqual(
            data['permissions'],
            [r.PERMISSIONS[Agent.SupportedPermissions.NAME]])

        r.add_permission('because', [Agent.SupportedPermissions.COARSE_LOCATION,
                                     Agent.SupportedPermissions.PRECISE_LOCATION])
        data = r.to_dict()['data']['google']['systemIntent']['data']
        self.assertEqual(
            set(data['permissions']),
            {r.PERMISSIONS[Agent.SupportedPermissions.NAME],
             r.PERMISSIONS[Agent.SupportedPermissions.COARSE_LOCATION],
             r.PERMISSIONS[Agent.SupportedPermissions.PRECISE_LOCATION]})


@mock.patch('apiai_assistant.corpus.Corpus.init_corpus', mocked_init_corpus(FAKE_CORPUS))
class AgentTestCase(unittest.TestCase):
    def test_repr(self):
        agent = Agent()
        self.assertEqual(
            str(agent), '<Agent: (OK)>')

        agent.code = Status.GenericError
        agent.error_message = 'foo'
        self.assertEqual(
            str(agent), '<Agent: (GenericError - foo)>')

    def test_error(self):
        agent = Agent()
        agent.error('foo')

        self.assertEqual(agent.response.to_dict(), {'error': '400'})
        self.assertEqual(agent.code, Status.GenericError)
        self.assertEqual(agent.error_message, 'foo')

        self.assertEqual(agent.response.code, Status.GenericError)
        self.assertEqual(agent.response.error_message, 'foo')

    def test_abort(self):
        agent = Agent()
        agent.abort('foo')

        self.assertEqual(agent.response.to_dict(), {'error': '400'})
        self.assertEqual(agent.code, Status.Aborted)
        self.assertEqual(agent.error_message, 'foo')

        self.assertEqual(agent.response.code, Status.Aborted)
        self.assertEqual(agent.response.error_message, 'foo')

    def test_tell(self):
        agent = Agent(corpus=Corpus('foo.json'))
        key = 'foo'
        context = {'name': 'bar'}
        agent.tell(key, context)
        payload = agent.response.to_dict()
        self.assertFalse(payload['data']['google']['expectUserResponse'])
        self.assertEqual(len(payload['messages']), 2)
        self.assertEqual(
            payload['messages'],
            [
                agent.response.initial_message,
                {
                    'displayText': FAKE_CORPUS['corpus'][key][0],
                    'ssml': '<speak>{}</speak>'.format(
                        FAKE_CORPUS['corpus'][key][0].format(context)),
                    'platform': 'google',
                    'type': 'simple_response'
                }
            ]
        )

    def test_ask(self):
        agent = Agent(corpus=Corpus('foo.json'))
        key = 'foo'
        context = {'name': 'bar'}
        agent.ask(key, context)
        payload = agent.response.to_dict()
        self.assertTrue(payload['data']['google']['expectUserResponse'])
        self.assertEqual(len(payload['messages']), 2)
        self.assertEqual(
            payload['messages'],
            [
                agent.response.initial_message,
                {
                    'displayText': FAKE_CORPUS['corpus'][key][0],
                    'ssml': '<speak>{}</speak>'.format(
                        FAKE_CORPUS['corpus'][key][0].format(context)),
                    'platform': 'google',
                    'type': 'simple_response'
                }
            ]
        )

    def test_tell_raw(self):
        agent = Agent()
        text = 'foo'
        agent.tell_raw(text)
        payload = agent.response.to_dict()
        self.assertFalse(payload['data']['google']['expectUserResponse'])
        self.assertEqual(len(payload['messages']), 2)
        self.assertEqual(
            payload['messages'],
            [
                agent.response.initial_message,
                {
                    'displayText': text,
                    'ssml': '<speak>{}</speak>'.format(text),
                    'platform': 'google',
                    'type': 'simple_response'
                }
            ]
        )

    def test_ask_raw(self):
        agent = Agent()
        text = 'foo'
        agent.ask_raw(text)
        payload = agent.response.to_dict()
        self.assertTrue(payload['data']['google']['expectUserResponse'])
        self.assertEqual(len(payload['messages']), 2)
        self.assertEqual(
            payload['messages'],
            [
                agent.response.initial_message,
                {
                    'displayText': text,
                    'ssml': '<speak>{}</speak>'.format(text),
                    'platform': 'google',
                    'type': 'simple_response'
                }
            ]
        )

    def test_suggest(self):
        agent = Agent(corpus=Corpus('foo.json'))
        key = 'confirmation'
        agent.suggest(key)
        payload = agent.response.to_dict()
        self.assertEqual(len(payload['messages']), 2)
        self.assertEqual(
            payload['messages'],
            [
                agent.response.initial_message,
                {
                    'suggestions': [
                        {'title': 'Yes'},
                        {'title': 'No'},
                    ],
                    'platform': 'google',
                    'type': 'suggestion_chips'
                }
            ]
        )

    def test_suggest_raw(self):
        agent = Agent()
        suggestions = ['Yes', 'No']
        agent.suggest_raw(suggestions)
        payload = agent.response.to_dict()
        self.assertEqual(len(payload['messages']), 2)
        self.assertEqual(
            payload['messages'],
            [
                agent.response.initial_message,
                {
                    'suggestions': [
                        {'title': 'Yes'},
                        {'title': 'No'},
                    ],
                    'platform': 'google',
                    'type': 'suggestion_chips'
                }
            ]
        )

    def test_ask_for_confirmation(self):
        agent = Agent(corpus=Corpus('foo.json'))
        key = 'foo'
        agent.ask_for_confirmation(key)

        payload = agent.response.to_dict()
        self.assertEqual(len(payload['messages']), 3)
        self.assertTrue(payload['data']['google']['expectUserResponse'])
        self.assertEqual(
            payload['messages'],
            [
                agent.response.initial_message,
                {
                    'displayText': FAKE_CORPUS['corpus'][key][0],
                    'ssml': '<speak>{}</speak>'.format(
                        FAKE_CORPUS['corpus'][key][0]),
                    'platform': 'google',
                    'type': 'simple_response'
                },
                {
                    'suggestions': [
                        {'title': 'Yes'},
                        {'title': 'No'},
                    ],
                    'platform': 'google',
                    'type': 'suggestion_chips'
                }
            ]
        )

    def test_ask_for_confirmation_raw(self):
        agent = Agent(corpus=Corpus('foo.json'))
        question = 'Annie are you OK?'
        agent.ask_for_confirmation_raw(question)

        payload = agent.response.to_dict()
        self.assertEqual(len(payload['messages']), 3)
        self.assertTrue(payload['data']['google']['expectUserResponse'])
        self.assertEqual(
            payload['messages'],
            [
                agent.response.initial_message,
                {
                    'displayText': question,
                    'ssml': '<speak>{}</speak>'.format(
                        question),
                    'platform': 'google',
                    'type': 'simple_response'
                },
                {
                    'suggestions': [
                        {'title': 'Yes'},
                        {'title': 'No'},
                    ],
                    'platform': 'google',
                    'type': 'suggestion_chips'
                }
            ]
        )

    def test_suggest_raw_one_suggestion(self):
        agent = Agent()
        suggestion = 'Sure'
        agent.suggest_raw(suggestion)
        payload = agent.response.to_dict()
        self.assertEqual(len(payload['messages']), 2)
        self.assertEqual(
            payload['messages'],
            [
                agent.response.initial_message,
                {
                    'suggestions': [
                        {'title': 'Sure'},
                    ],
                    'platform': 'google',
                    'type': 'suggestion_chips'
                }
            ]
        )

    def test_add_context(self):
        agent = Agent()
        context_name = 'foobar'
        agent.add_context(context_name)
        payload = agent.response.to_dict()
        self.assertEqual(len(payload['messages']), 1)
        self.assertEqual(payload['messages'], [agent.response.initial_message])
        self.assertTrue('contextOut' in payload)
        self.assertEqual(
            payload['contextOut'],
            [{
                'name': context_name,
                'lifespan': 5,
                'parameters': {}
            }]
        )

    def test_show(self):
        title = "foo"
        url = "bar.com"
        widget = LinkOutChipWidget(title, url)
        agent = Agent()
        agent.show(widget)
        payload = agent.response.to_dict()
        self.assertEqual(len(payload['messages']), 2)
        self.assertEqual(
            payload['messages'],
            [
                agent.response.initial_message,
                {
                    "platform": "google",
                    "type": "link_out_chip",
                    "title": title,
                    "url": url
                }
            ]
        )


    def test_ask_for_permissions(self):
        agent = Agent()
        reason = 'Just because'
        agent.ask_for_permissions(reason, [agent.SupportedPermissions.NAME])
        payload = agent.response.to_dict()
        self.assertEqual(len(payload['messages']), 1)
        self.assertEqual(payload['messages'], [agent.response.initial_message])
        self.assertTrue('systemIntent' in payload['data']['google'])
        self.assertEqual(
            payload['data']['google']['systemIntent']['data']['optContext'],
            reason
        )
        self.assertEqual(
            payload['data']['google']['systemIntent']['data']['permissions'],
            [agent.response.PERMISSIONS[agent.SupportedPermissions.NAME]]
        )

if __name__ == '__main__':
    unittest.main()
