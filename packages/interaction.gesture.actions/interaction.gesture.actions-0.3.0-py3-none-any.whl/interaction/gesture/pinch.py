import logging
from dataclasses import dataclass

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement

from .exceptions import ZoomError

logger = logging.getLogger(__name__)


@dataclass
class PinchParameters:
    """Encapsulates the parameters needed to perform pinch gestures."""

    element: WebElement
    _percent: float = 0.75
    speed: float = 1.0

    @property
    def percent(self) -> float:
        """Get the scale factor for the pinch gesture."""
        return self._percent

    @percent.setter
    def percent(self, value: float) -> None:
        if not 0.0 <= value <= 1.0:
            msg = f"Percent must be between 0.0 and 1.0, got {value}"
            raise ValueError(msg)
        self._percent = value


class PinchGestures:
    """Access pinch/zoom related gestures."""

    def __init__(self, driver: WebDriver, platform: str) -> None:
        self._driver = driver
        self._platform = platform

    def open(
        self,
        element: WebElement,
        percent: float = 0.75,
        speed: float = 1.0,
    ) -> bool:
        """
        Performs a pinch-open (zoom in) gesture on the specified element.

        This function executes a pinch gesture that spreads two fingers apart, commonly used
        for zooming in on images, maps, or other content. The implementation differs
        between Android and iOS platforms.

        Args:
            element (WebElement): The target element to perform the pinch gesture on.
            percent (float, optional): The scale factor of the pinch as a percentage (0.0-1.0).
                Higher values create a larger pinch spread.
                Defaults to 0.75.
            speed (float, optional): The velocity of the pinch gesture as a percentage.
                For Android, this is multiplied by the device's DPI to calculate the final velocity.
                For iOS, this value is used directly.
                Defaults to 1.0 (100%).

        Returns:
            bool: True if the pinch gesture was successfully executed.

        Raises:
            ZoomError: If the pinch gesture fails to execute, wrapping the underlying
                platform-specific exception.

        """
        p = PinchParameters(element, percent, speed)
        try:
            return (
                self._pinch_open_android(p.element, p.percent, p.speed)
                if self._platform == "Android"
                else self._pinch_open_ios(p.element, p.percent, p.speed)
            )
        except Exception as e:
            msg = f"Failed to perform pinch open: {str(e)}"
            logger.error(msg)
            raise ZoomError(msg) from e

    def _pinch_open_android(self, element: WebElement, percent: float, speed: float) -> bool:
        """Execute Android-specific pinch-open gesture."""
        dpi = self._driver.get_display_density()
        velocity = (2500 * dpi) * speed
        return self._driver.execute_script(
            "mobile: pinchOpenGesture",
            {
                "elementId": element,
                "percent": percent,
                "speed": velocity,
            },
        )

    def _pinch_open_ios(self, element: WebElement, percent: float, speed: float) -> bool:
        """Execute iOS-specific pinch gesture."""
        return self._driver.execute_script(
            "mobile: pinch",
            {
                "elementId": element,
                "scale": percent,
                "velocity": speed,
            },
        )

    def close(
        self,
        element: WebElement,
        percent: float = 0.75,
        speed: float = 1.0,
    ) -> bool:
        """
        Performs a pinch-close (zoom out) gesture on the specified element.

        This function executes a pinch gesture that pulls two fingers inward, commonly used
        for zooming out on images, maps, or other content. The implementation differs
        between Android and iOS platforms.

        Args:
            element (WebElement): The target element to perform the pinch gesture on.
            percent (float, optional): The scale factor of the pinch as a percentage (0.0-1.0).
                Higher values create a larger pinch pull.
                On iOS a value > 1 inverts the pinch gesture, therefore the value is * 2.
                Defaults to 0.75.
            speed (float, optional): The velocity of the pinch gesture as a percentage.
                For Android, this is multiplied by the device's DPI to calculate the final velocity.
                For iOS, this value is used directly.
                Defaults to 1.0.

        Returns:
            bool: True if the pinch gesture was successfully executed.

        Raises:
            ZoomError: If the pinch gesture fails to execute, wrapping the underlying
                platform-specific exception.

        """
        p = PinchParameters(element, percent, speed)
        try:
            return (
                self._pinch_close_android(p.element, p.percent, p.speed)
                if self._platform == "Android"
                else self._pinch_close_ios(p.element, p.percent, p.speed)
            )
        except Exception as e:
            msg = f"Failed to perform pinch close: {str(e)}"
            logger.error(msg)
            raise ZoomError(msg) from e

    def _pinch_close_android(self, element: WebElement, percent: float, speed: float) -> bool:
        """Execute Android-specific pinch-close gesture."""
        dpi = self._driver.get_display_density()
        velocity = (2500 * dpi) * speed
        return self._driver.execute_script(
            "mobile: pinchCloseGesture",
            {
                "elementId": element,
                "percent": percent,
                "speed": velocity,
            },
        )

    def _pinch_close_ios(self, element: WebElement, percent: float, speed: float) -> bool:
        """Execute iOS-specific pinch gesture."""
        return self._driver.execute_script(
            "mobile: pinch",
            {
                "elementId": element,
                "scale": percent * 2,
                "velocity": speed,
            },
        )
