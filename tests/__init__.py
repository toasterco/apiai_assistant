from apiai_assistant import corpus


def mocked_init_corpus(faked_corpus=None):
    def mocked_init_corpus_closure(self):
        self.corpus = {}
        if faked_corpus:
            self.corpus = faked_corpus['corpus']
            self.suggestions = faked_corpus.get('suggestions')
            self.confirmations = faked_corpus.get('confirmations', corpus.Corpus.DEFAULT_CONFIRMATIONS)
    return mocked_init_corpus_closure


def get_dummy_google_request():
    return {
        'result': {
            'parameters': {},
            'contexts': [],
            'action': 'action',
        },
        'originalRequest': {
            'data': {
                'surface': {
                    'capabilities': [
                        {'name': 'actions.capability.AUDIO_OUTPUT'},
                        {'name': 'actions.capability.SCREEN_OUTPUT'}
                    ]
                },
                'user': {
                    'locale': 'en-US',
                    'userId': '7w8ZsrFnALTj1fLiI9474qFAlJIVkSixmXjI8BrUEIs'
                },
            }
        }
    }


def get_dummy_amazon_request():
    return {
        'request': {
            'type': '',
            'intent': {
                'name': None,
                'slots': {}
            },
        },
        'session': {},
        'context': {
            'System': {
                'device': {
                    'deviceId': None,
                    'supportedInterfaces': {}
                },
                'user': {
                    'userId': None
                }
            }
        }
    }
