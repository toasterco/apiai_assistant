import mock
import unittest

from tests import mocked_init_corpus

from apiaiassistant.agent import Response
from apiaiassistant.agent import Agent
from apiaiassistant import corpus
from apiaiassistant.widgets import LinkOutChipWidget


FAKE_CORPUS = {
    'foo': ['bar']
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


# @mock.patch('apiaiassistant.corpus.Corpus.init_corpus', mocked_init_corpus(FAKE_CORPUS))
# class AgentTestCase(unittest.TestCase):
#     def test_repr(self):
#         agent = Agent()
#         self.assertEqual(
#             str(agent), '<Agent: (OK)>')

#     def test_tell(self):
#         agent = Agent()
#         text = 'foo'
#         agent.tell_raw(text)
#         payload = agent.response.to_dict()
#         self.assertFalse(payload['data']['google']['expectUserResponse'])
#         self.assertEqual(len(payload['messages']), 2)
#         self.assertEqual(
#             payload['messages'],
#             [
#                 agent.response.initial_message,
#                 {
#                     'displayText': text,
#                     'speech': '<speak>{}</speak>'.format(text),
#                     'platform': 'google',
#                     'type': 'simple_response'

#                 }
#             ]
#         )

#     def test_ask(self):
#         agent = Agent()
#         text = 'foo'
#         agent.ask(text)
#         payload = agent.response.to_dict()
#         self.assertTrue(payload['data']['google']['expectUserResponse'])
#         self.assertEqual(len(payload['messages']), 2)
#         self.assertEqual(
#             payload['messages'],
#             [
#                 agent.response.initial_message,
#                 {
#                     'displayText': text,
#                     'speech': '<speak>{}</speak>'.format(text),
#                     'platform': 'google',
#                     'type': 'simple_response'

#                 }
#             ]
#         )

#     def test_tell_raw(self):
#         agent = Agent()
#         text = 'foo'
#         agent.tell_raw(text)
#         payload = agent.response.to_dict()
#         self.assertFalse(payload['data']['google']['expectUserResponse'])
#         self.assertEqual(len(payload['messages']), 2)
#         self.assertEqual(
#             payload['messages'],
#             [
#                 agent.response.initial_message,
#                 {
#                     'displayText': text,
#                     'speech': '<speak>{}</speak>'.format(text),
#                     'platform': 'google',
#                     'type': 'simple_response'

#                 }
#             ]
#         )

#     def test_ask_raw(self):
#         agent = Agent()
#         text = 'foo'
#         agent.ask_raw(text)
#         payload = agent.response.to_dict()
#         self.assertTrue(payload['data']['google']['expectUserResponse'])
#         self.assertEqual(len(payload['messages']), 2)
#         self.assertEqual(
#             payload['messages'],
#             [
#                 agent.response.initial_message,
#                 {
#                     'displayText': text,
#                     'speech': '<speak>{}</speak>'.format(text),
#                     'platform': 'google',
#                     'type': 'simple_response'

#                 }
#             ]
#         )

#     def test_suggest(self):
#         agent = Agent()
#         suggestions = ['Yes', 'No']
#         agent.suggest(suggestions)
#         payload = agent.response.to_dict()
#         self.assertEqual(len(payload['messages']), 2)
#         self.assertEqual(
#             payload['messages'],
#             [
#                 agent.response.initial_message,
#                 {
#                     'suggestions': [
#                         {'title': 'Yes'},
#                         {'title': 'No'},
#                     ],
#                     'platform': 'google',
#                     'type': 'suggestion_chips'

#                 }
#             ]
#         )

#     def test_suggest_raw(self):
#         agent = Agent()
#         suggestions = ['Yes', 'No']
#         agent.suggest_raw(suggestions)
#         payload = agent.response.to_dict()
#         self.assertEqual(len(payload['messages']), 2)
#         self.assertEqual(
#             payload['messages'],
#             [
#                 agent.response.initial_message,
#                 {
#                     'suggestions': [
#                         {'title': 'Yes'},
#                         {'title': 'No'},
#                     ],
#                     'platform': 'google',
#                     'type': 'suggestion_chips'

#                 }
#             ]
#         )

#     def test_add_context(self):
#         agent = Agent()
#         context_name = 'foobar'
#         agent.add_context(context_name)
#         payload = agent.response.to_dict()
#         self.assertEqual(len(payload['messages']), 1)
#         self.assertEqual(payload['messages'], [agent.response.initial_message])
#         self.assertTrue('contextOut' in payload)
#         self.assertEqual(
#             payload['contextOut'],
#             [{
#                 'name': context_name,
#                 'lifespan': 5,
#                 'parameters': {}
#             }]
#         )

#     def test_show(self):
#         title = "foo"
#         url = "bar.com"
#         widget = LinkOutChipWidget(title, url)
#         agent = Agent()
#         agent.show(widget)
#         payload = agent.response.to_dict()
#         self.assertEqual(len(payload['messages']), 2)
#         self.assertEqual(
#             payload['messages'],
#             [
#                 agent.response.initial_message,
#                 {
#                     "platform": "google",
#                     "type": "link_out_chip",
#                     "title": title,
#                     "url": url
#                 }
#             ]
#         )


# if __name__ == '__main__':
#     unittest.main()
