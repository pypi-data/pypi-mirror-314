class Link:
    def __init__(self, value: str = None, label: str = None):
        """
        Initialize the Link object.
        
        :param value: URI or resource the link points to.
        :param label: An optional label for the link.
        """
        self.value = value if value else None
        self.label = label if label else None