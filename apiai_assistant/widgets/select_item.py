from . import GoogleAssistantWidget


class GoogleAssistantSelectItem(GoogleAssistantWidget):
    def __init__(self, title, option_info,
                 text=None, image=None):
        self.title = title
        self.option_info = option_info

        self.text = text
        self.image = image

        super(GoogleAssistantSelectItem, self).__init__()

    def render_google_assistant(self, origin):
        return {
            'title': self.title,
            'description': self.text,
            'optionInfo': self.option_info.render(origin),
            'image': self.image.render(origin) if self.image else None
        }
