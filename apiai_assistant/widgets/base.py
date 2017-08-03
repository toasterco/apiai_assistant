class InvalidGoogleAssistantWidget(Exception):
    pass


class GoogleAssistantWidget(object):
    def __init__(self):
        self.platform = 'google'

    def render(self):
        return {
            'platform': self.platform
        }
