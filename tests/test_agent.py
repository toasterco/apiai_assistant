import mock
import unittest

from tests import mocked_init_corpus

from apiai_assistant import Platforms
from apiai_assistant.agent import Agent
from apiai_assistant.agent import get_origin
from apiai_assistant.agent import Status
from apiai_assistant.corpus import Corpus
from apiai_assistant.widgets import GoogleAssistantLinkOutChipWidget


FAKE_CORPUS = {
    "corpus": {'foo': ['bar']},
    "suggestions": {'confirmation': [['Yes', 'No']]}
}

FAKE_GOOGLE_ASSISTANT_REQUEST = {
    'result': {},
    'originalRequest': {}
}

FAKE_FACEBOOK_MESSENGER_REQUEST = {
    'result': {},
    'originalRequest': {'source': 'facebook'}
}

FAKE_AMAZON_ALEXA_REQUEST = {
    'session': {},
    'context': {},
    'request': {}
}


@mock.patch('apiai_assistant.corpus.Corpus.init_corpus', mocked_init_corpus(FAKE_CORPUS))
class AgentTestCase(unittest.TestCase):
    def test_get_origin(self):
        self.assertEqual(Platforms.GOOGLE_ASSISTANT, get_origin(FAKE_GOOGLE_ASSISTANT_REQUEST))
        self.assertEqual(Platforms.AMAZON_ALEXA, get_origin(FAKE_AMAZON_ALEXA_REQUEST))
        self.assertEqual(Platforms.API_AI, get_origin({'foo': 'bar'}))

    def test_repr(self):
        agent = Agent(request=FAKE_GOOGLE_ASSISTANT_REQUEST)
        self.assertEqual(
            str(agent), '<Agent: (OK)>')

        agent.code = Status.GenericError
        agent.error_message = 'foo'
        self.assertEqual(
            str(agent), '<Agent: (GenericError - foo)>')

    def test_error(self):
        agent = Agent(request=FAKE_GOOGLE_ASSISTANT_REQUEST)
        agent.error('foo')

        self.assertEqual(agent.response.to_dict(), {'error': '400'})
        self.assertEqual(agent.code, Status.GenericError)
        self.assertEqual(agent.error_message, 'foo')

        self.assertEqual(agent.response.code, Status.GenericError)
        self.assertEqual(agent.response.error_message, 'foo')

    def test_abort(self):
        agent = Agent(request=FAKE_GOOGLE_ASSISTANT_REQUEST)
        agent.abort('foo')

        self.assertEqual(agent.response.to_dict(), {'error': '400'})
        self.assertEqual(agent.code, Status.Aborted)
        self.assertEqual(agent.error_message, 'foo')

        self.assertEqual(agent.response.code, Status.Aborted)
        self.assertEqual(agent.response.error_message, 'foo')

    def test_tell(self):
        agent = Agent(
            request=FAKE_GOOGLE_ASSISTANT_REQUEST, corpus=Corpus('foo.json'))
        key = 'foo'
        context = {'name': 'bar'}
        agent.tell(key, context=context)
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

    def test_tell_no_context(self):
        agent = Agent(
            request=FAKE_GOOGLE_ASSISTANT_REQUEST, corpus=Corpus('foo.json'))
        key = 'foo'
        agent.tell(key)
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
                        FAKE_CORPUS['corpus'][key][0]),
                    'platform': 'google',
                    'type': 'simple_response'
                }
            ]
        )

    def test_ask(self):
        agent = Agent(
            request=FAKE_GOOGLE_ASSISTANT_REQUEST, corpus=Corpus('foo.json'))
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
        agent = Agent(request=FAKE_GOOGLE_ASSISTANT_REQUEST)
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
        agent = Agent(request=FAKE_GOOGLE_ASSISTANT_REQUEST)
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
        agent = Agent(
            request=FAKE_GOOGLE_ASSISTANT_REQUEST, corpus=Corpus('foo.json'))
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

    def test_suggest_notfound(self):
        agent = Agent(
            request=FAKE_GOOGLE_ASSISTANT_REQUEST, corpus=Corpus('foo.json'))
        key = 'confirmation'[::-1]
        self.assertTrue(key not in agent.corpus)

        agent.suggest(key)
        payload = agent.response.to_dict()
        self.assertEqual(len(payload['messages']), 1)
        self.assertEqual(
            payload['messages'],
            [
                agent.response.initial_message
            ]
        )

    def test_suggest_raw(self):
        agent = Agent(request=FAKE_GOOGLE_ASSISTANT_REQUEST)
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
        agent = Agent(
            request=FAKE_GOOGLE_ASSISTANT_REQUEST, corpus=Corpus('foo.json'))
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
        agent = Agent(
            request=FAKE_GOOGLE_ASSISTANT_REQUEST, corpus=Corpus('foo.json'))
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
        agent = Agent(request=FAKE_GOOGLE_ASSISTANT_REQUEST)
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
        agent = Agent(request=FAKE_GOOGLE_ASSISTANT_REQUEST)
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
        widget = GoogleAssistantLinkOutChipWidget(title, url)
        agent = Agent(request=FAKE_GOOGLE_ASSISTANT_REQUEST)
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

    def test_show_no_message(self):
        title = "foo"
        url = "bar.com"
        widget = GoogleAssistantLinkOutChipWidget(title, url)
        agent = Agent(request=FAKE_FACEBOOK_MESSENGER_REQUEST)
        agent.show(widget)
        payload = agent.response.to_dict()
        self.assertEqual(payload['messages'], [])

    def test_ask_for_permissions(self):
        agent = Agent(request=FAKE_GOOGLE_ASSISTANT_REQUEST)
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
