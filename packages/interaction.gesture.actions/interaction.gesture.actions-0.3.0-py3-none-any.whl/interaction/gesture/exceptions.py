from selenium.common.exceptions import WebDriverException


class GestureError(WebDriverException):
    """Base exception for all gesture-related errors."""


class ViewportError(GestureError):
    """Raised when there are issues with viewport dimensions or calculations."""


class ElementInteractionError(GestureError):
    """Raised when interaction with an element fails."""


class SwipeError(GestureError):
    """Raised when a swipe action fails."""


class ElementNotInViewError(GestureError):
    """Raised when an element cannot be brought into view after maximum attempts."""


class InvalidGestureError(GestureError):
    """Raised when an invalid gesture is attempted."""


class ZoomError(GestureError):
    """Raised when a zoom operation fails."""


class DragDropError(GestureError):
    """Raised when a drag and drop operation fails."""
