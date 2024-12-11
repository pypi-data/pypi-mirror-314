class Dialog:
    def __init__(self, title, uri, label="", hint_width="", hint_height="", resource_types=None, usages=None):
        self.title = title
        self.uri = uri
        self.label = label
        self.hint_width = hint_width
        self.hint_height = hint_height
        self.resource_types = resource_types if resource_types is not None else []
        self.usages = usages if usages is not None else []