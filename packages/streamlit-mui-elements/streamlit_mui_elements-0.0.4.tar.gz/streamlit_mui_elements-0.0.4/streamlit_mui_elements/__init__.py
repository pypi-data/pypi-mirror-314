from streamlit_mui_elements.core.elements import new_frame as _new_frame
from streamlit_mui_elements.core.exceptions import *
from streamlit_mui_elements.modules import *
from streamlit_mui_elements.version import __version__


def elements(key: str) -> None:
    """Create a Streamlit Elements frame."""
    return _new_frame(key)

