class CreationFactory:
    def __init__(self, label, resource_shapes=None, resource_types=None, usages=None):
        self.label = label
        self.resource_shapes = resource_shapes if resource_shapes is not None else []
        self.resource_types = resource_types if resource_types is not None else []
        self.usages = usages if usages is not None else []