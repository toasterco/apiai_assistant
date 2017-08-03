from . import GoogleAssistantWidget


class SelectItem(GoogleAssistantWidget):
    def __init__(self, title, option_info,
                 text=None, image=None):
        self.title = title
        self.option_info = option_info

        self.text = text
        self.image = image

        super(SelectItem, self).__init__()

    def render(self):
        return {
            'title': self.title,
            'description': self.text,
            'optionInfo': self.option_info.render(),
            'image': self.image.render() if self.image else None
        }
