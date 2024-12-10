class Element:
    __slots__ = ("_frame", "_module", "_element", "_props", "_children", 
                 "_is_context_parent", "_registered", "_is_prop", "_parent")

    def __init__(self, frame, module, element):
        self._frame = frame
        self._module = module
        self._element = element
        self._props = {}
        self._children = []
        self._is_context_parent = False
        self._registered = False
        self._is_prop = False
        self._parent = None

    def __enter__(self):
        """Enter a new context for this element."""
        self._is_context_parent = True
        self._frame.capture_children()
        return self

    def __exit__(self, *_):
        """Exit the context and finalize this element."""
        self._frame.save_children(self)

    def __call__(self, *children, **props):
        """Add children and props to this element."""
        for key, value in props.items():
            cleaned_key = key.rstrip("_")
            if isinstance(value, Element):
                value._is_prop = True
                value._parent = self
                value._registered = True  # Prevent prop elements from being registered as children
            self._props[cleaned_key] = value

        for child in children:
            if isinstance(child, Element):
                child._parent = self
            self._children.append(child)

        if (self._frame.is_capturing_children() and 
            not self._is_context_parent and 
            not self._registered and 
            not self._is_prop and 
            not self._parent):  # Only register if truly a root-level element
            self._frame._children.append(self)
            self._registered = True

        return self

    def to_dict(self):
        def convert_value(value):
            if isinstance(value, Element):
                return value.to_dict()
            elif isinstance(value, dict):
                return {k: convert_value(v) for k, v in value.items()}
            elif isinstance(value, (list, tuple)):
                return [convert_value(v) for v in value]
            elif callable(value):  # Handle functions
                return f"function {value.__name__}" if hasattr(value, "__name__") else "function"
            else:
                return value

        result = {
            "type": self._element,
            "module": self._module,
            "props": convert_value(self._props),
            "children": convert_value(self._children),
        }
        # print(f"Element to_dict: {result}")  # Debugging
        return result
