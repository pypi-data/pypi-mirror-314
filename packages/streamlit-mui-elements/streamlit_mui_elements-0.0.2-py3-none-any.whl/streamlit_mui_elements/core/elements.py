import json
from contextlib import contextmanager
import time
from streamlit import session_state

from streamlit_mui_elements.core.exceptions import ElementsFrameError
from streamlit_mui_elements.core.element import Element
from streamlit_mui_elements.core.render import render_component

ELEMENTS_FRAME_KEY = f"{__name__}.elements_frame"


def get_elements_frame():
    if ELEMENTS_FRAME_KEY not in session_state:
        raise ElementsFrameError("Frame was not created.")
    return session_state[ELEMENTS_FRAME_KEY]


@contextmanager
def new_frame(key):
    key = f"{ELEMENTS_FRAME_KEY}.{key}"  # Unique key for each frame
    frame = ElementsFrame(key)
    session_state[ELEMENTS_FRAME_KEY] = frame

    frame.capture_children()

    try:
        yield
        ui_tree = frame.to_dict()
        # print("Final UI Tree:", json.dumps(ui_tree, indent=2))  # Debug print for tree

        if ui_tree:
            ui_description = json.dumps(ui_tree)
            _component = render_component(data=ui_description, key=key, default=0)
            if _component != 0:
                event_key = _component.get('key', '')
                value = _component.get('value', '')
                timestamp = _component.get('timestamp', 0)

                if event_key == '':
                    event_key = 'undefined'

                session_state["events"] = session_state.get("events", {})
                session_state["events"][event_key] = {"value": value, "timestamp": timestamp}
    finally:
        del session_state[ELEMENTS_FRAME_KEY]


def new_element(module, element):
    if ELEMENTS_FRAME_KEY not in session_state:
        raise ElementsFrameError("Cannot create element outside a frame.")
    return Element(session_state[ELEMENTS_FRAME_KEY], module, element)


class ElementsFrame:
    __slots__ = ('_children', '_parents', '_key', '_is_saving')

    def __init__(self, key):
        self._children = []
        self._parents = []
        self._key = key
        self._is_saving = False

    def capture_children(self):
        # print(f"Start capturing children. Current children: {self._children}")  # Debugging
        self._parents.append(self._children)
        self._children = []
        # print(f"New context started. Parents stack: {self._parents}")  # Debugging

    def save_children(self, element):
        if self._is_saving:
            raise RuntimeError("Reentrant save_children call detected.")

        if not self._parents:
            raise RuntimeError("save_children called without active context.")

        self._is_saving = True
        captured_children = self._children
        self._children = self._parents.pop()

        # Only add non-prop children
        filtered_children = [
            child for child in captured_children 
            if not child._is_prop and not child._parent
        ]
        element(*filtered_children)

        if not element._is_prop and element not in self._children:
            self._children.append(element)

        captured_children.clear()
        self._is_saving = False

    def is_capturing_children(self):
        return len(self._parents) > 0

    def to_dict(self):
        result = [child.to_dict() for child in self._children]
        # print("UI Tree to_dict:", result)  # Debugging
        return result
