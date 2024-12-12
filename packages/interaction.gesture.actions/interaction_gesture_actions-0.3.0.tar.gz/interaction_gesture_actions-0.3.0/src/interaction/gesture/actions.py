import logging

from appium.webdriver.webdriver import WebDriver

from .drag_and_drop import DragAndDropGestures
from .pinch import PinchGestures
from .swipe import SwipeGestures

logger = logging.getLogger(__name__)


class GestureActions:
    """
    A class for enhanced gesture functionality in Appium.
    """

    def __init__(self, driver: WebDriver, platform: str) -> None:
        """
        Initialize the GestureActions object.

        Args:
            driver: The Appium driver instance.
            **kwargs: Optional keyword arguments for customising crop factors, element probe attempts, and probe timeout.
        """
        self._driver = driver
        self._platform = platform
        self._drag_drop: DragAndDropGestures | None = None
        self._pinch: PinchGestures | None = None
        self._swipe: SwipeGestures | None = None

    @property
    def drag_drop(self) -> "DragAndDropGestures":
        """Access drag-and-drop related gestures."""
        if self._drag_drop is None:
            self._drag_drop = DragAndDropGestures(self._driver, self._platform)
        return self._drag_drop

    @property
    def pinch(self) -> "PinchGestures":
        """Access pinch related gestures."""
        if self._pinch is None:
            self._pinch = PinchGestures(self._driver, self._platform)
        return self._pinch

    @property
    def swipe(self) -> "SwipeGestures":
        """Access swipe related gestures."""
        if self._swipe is None:
            self._swipe = SwipeGestures(self._driver, self._platform)
        return self._swipe
