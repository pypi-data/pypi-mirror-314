def get_classes(module):
    # Get a list of all attributes in the module
    attributes = dir(module)
    # Filter out classes
    return [getattr(module, attr) for attr in attributes if isinstance(getattr(module, attr), type)]
