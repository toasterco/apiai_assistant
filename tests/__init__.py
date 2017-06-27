def mocked_init_corpus(faked_corpus=None):
    def mocked_init_corpus_closure(self):
        self.corpus = faked_corpus or {}
    return mocked_init_corpus_closure


def get_dummy_request():
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
