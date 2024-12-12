import logging
from dataclasses import dataclass

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement

from .calculations import calculate_element_points
from .exceptions import DragDropError

logger = logging.getLogger(__name__)


@dataclass
class DragAndDropParameters:
    """Encapsulates the parameters needed to perform the drag and drop gestures."""

    element_source: WebElement
    element_target: WebElement
    _speed: float = 1.0

    @property
    def speed(self) -> float:
        """Get the velocity factor for the drag and drop gesture."""
        return self._speed

    @speed.setter
    def speed(self, value: float) -> None:
        if not 0.0 <= value <= 10.0:
            msg = f"Speed must be between 0.0 and 10.0, got {value}"
            raise ValueError(msg)
        self._speed = value


class DragAndDropGestures:
    """Access pinch/zoom related gestures."""

    def __init__(self, driver: WebDriver, platform: str) -> None:
        self._driver = driver
        self._platform = platform

    def drag_and_drop(
        self,
        element_source: WebElement,
        element_target: WebElement,
        speed: float = 1.0,
    ) -> None:
        """
        Perform a drag and drop action from the source element to the target element.

        This function only supports initial and final elements which are both visible within the viewport.

        Args:
            element_source (WebElement): The source element to begin the drag and drop gesture on.
            element_target (WebElement): The target element to finish the drag and drop gesture on.
            speed (float, optional): The velocity of the drag-and-drop gesture as a percentage.
                For Android, this is multiplied by the device's DPI to calculate the final velocity.
                For iOS, this value is multiplied by the default value of 400.
                Defaults to 1.0 (100%).
        """
        p = DragAndDropParameters(element_source, element_target, speed)
        try:
            init_element = calculate_element_points(p.element_source)
            init_x, init_y = init_element["mid"]
            final_element = calculate_element_points(p.element_target)
            final_x, final_y = final_element["mid"]

            return (
                self._drag_drop_android(init_x, init_y, final_x, final_y, p.speed)
                if self._platform == "Android"
                else self._drag_drop_ios(init_x, init_y, final_x, final_y, p.speed)
            )
        except Exception as e:
            msg = f"Failed to perform drag and drop: {str(e)}"
            logger.error(msg)
            raise DragDropError(msg) from e

    def _drag_drop_android(
        self, init_x: int, init_y: int, final_x: int, final_y: int, speed: float
    ) -> bool:
        """Execute Android-specific drag-and-drop gesture."""
        dpi = self._driver.get_display_density()
        velocity = (2500 * dpi) * speed
        return self._driver.execute_script(
            "mobile: dragGesture",
            {
                "startX": init_x,
                "startY": init_y,
                "endX": final_x,
                "endY": final_y,
                "speed": velocity,
            },
        )

    def _drag_drop_ios(
        self, init_x: int, init_y: int, final_x: int, final_y: int, speed: float
    ) -> bool:
        """Execute iOS-specific drag-and-drop gesture."""
        velocity = 400 * speed
        press_duration = 0.5
        hold_duration = 0.1
        return self._driver.execute_script(
            "mobile: dragFromToWithVelocity",
            {
                "pressDuration": press_duration,
                "holdDuration": hold_duration,
                "fromX": init_x,
                "fromY": init_y,
                "toX": final_x,
                "toY": final_y,
                "velocity": velocity,
            },
        )
