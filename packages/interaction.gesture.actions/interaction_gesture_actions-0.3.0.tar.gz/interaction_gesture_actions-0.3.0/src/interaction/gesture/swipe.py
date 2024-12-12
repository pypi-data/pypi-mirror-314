import logging
from typing import TypedDict

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from .calculations import calculate_element_points
from .enums import Direction, SeekDirection, UiSelector

logger = logging.getLogger(__name__)

TIMEOUT = 0.25
SWIPE_ACTION_THRESHOLD = 50
CROP_FACTOR_UPPER = 0.20
CROP_FACTOR_LOWER = 0.90
CROP_FACTOR_LEFT = 0.10
CROP_FACTOR_RIGHT = 0.90


# class AndroidParams(TypedDict, total=False):
#     """Parameters for Android-specific functions."""

#     locator_method_a: AppiumBy
#     ui_selector: UiSelector
#     direction: SeekDirection


# class IOSParams(TypedDict, total=False):
#     """Parameters for iOS-specific functions."""

#     locator_method_i: AppiumBy
#     direction: SeekDirection


# PlatformParams = AndroidParams | IOSParams


class SwipeGestures:
    """Access swipe related gestures."""

    def __init__(self, driver: WebDriver, platform: str) -> None:
        """
        Initialize the SwipeGestures instance.

        Args:
            driver (WebDriver): A WebDriver instance providing access to the app.
            platform (str): The platform type ('Android' or 'iOS').

        """
        self._driver = driver
        self._platform = platform
        self._max_attempts = 5
        self._viewport = self._driver.get_window_size()
        self._viewport_width = self._viewport["width"]
        self._viewport_height = self._viewport["height"]
        self._viewport_x_mid_point = self._viewport_width // 2
        self._viewport_y_mid_point = self._viewport_height // 2
        self._crop_factors = {
            "upper_cf": CROP_FACTOR_UPPER,
            "lower_cf": CROP_FACTOR_LOWER,
            "left_cf": CROP_FACTOR_LEFT,
            "right_cf": CROP_FACTOR_RIGHT,
        }
        self._boundaries = {
            "upper": int(self._viewport_height * self._crop_factors["upper_cf"]),
            "lower": int(self._viewport_height * self._crop_factors["lower_cf"]),
            "left": int(self._viewport_width * self._crop_factors["left_cf"]),
            "right": int(self._viewport_width * self._crop_factors["right_cf"]),
        }
        self._scrollable_area = {
            "x": self._boundaries["right"] - self._boundaries["left"],
            "y": self._boundaries["lower"] - self._boundaries["upper"],
        }

    def _create_action(self) -> ActionChains:
        """
        Create an ActionChains object for the driver.

        Returns:
            ActionChains: The ActionChains object configured for the driver.

        """
        action = ActionChains(self._driver)
        action.w3c_actions = ActionBuilder(
            self._driver,
            mouse=PointerInput(interaction.POINTER_TOUCH, "touch"),
        )
        return action

    def element_into_view(
        self,
        value_a: str | None = None,
        locator_method_a: AppiumBy = None,
        value_i: str | None = None,
        locator_method_i: AppiumBy = None,
        direction: SeekDirection = SeekDirection.DOWN,
    ):
        """
        Swipe to bring an element into view.

        This method performs a swipe gesture to ensure that the specified
        element described by `value` is within the visible area of the app.

        The method if platform agnostic, this means you can include locators for both scenarios
        and the function will use the value of `self._platform` to determine which parameters to use.

        Suffixes `_a` and `_i` are for Android and iOS respectively.

        Args:
            value_a (str): The locator value for the element to swipe to view (e.g., new UiSelector().description("Day planted")).
            locator_method_a (AppiumBy): The method to locate the element (e.g., AppiumBy.ANDROID_UIAUTOMATOR).
            value_i (str): The locator value for the element to swipe to view (e.g., label == 'Flowers').
            locator_method_i (AppiumBy): The method to locate the element (e.g., AppiumBy.IOS_PREDICATE).
            direction (SeekDirection): The direction to scroll (e.g., SeekDirection.DOWN).

        Raises:
            ValueError: If the specified platform is unknown or unspecified.

        Android: Supports all locator methods, however UiSelector is highly preferred.
        iOS: Supports all locator methods, however NSPredicate is highly preferred.

        """
        if self._platform == "Android":
            self._scroll_to_android(value_a, locator_method_a, direction)

        elif self._platform == "iOS":
            self._scroll_to_ios(value_i, locator_method_i, direction)

        else:
            msg = "Unspecified or unknown platform."
            raise ValueError(msg)

    def _scroll_to_android(self, value: str, locator_method: AppiumBy, direction: SeekDirection = None) -> bool | None:
        if locator_method == AppiumBy.ANDROID_UIAUTOMATOR:
            # ui_selector = kwargs.get("ui_selector").value
            query = f"new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView({value})"
            self._driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, query)
            return True
        msg = "Locator was not of type AppiumBy.ANDROID_UIAUTOMATOR or failed to locate element within viewport,"
        "falling back to alternative method."
        logger.info(msg)
        self._fallback_scroll_to_element(value, locator_method, direction)
        return None

    def _scroll_to_ios(self, value: str, locator_method: AppiumBy, direction: SeekDirection) -> bool | None:
        try:
            element = self._driver.find_element(locator_method, value)
            self._driver.execute_script(
                "mobile: scrollToElement",
                {
                    "elementId": element,
                },
            )
        except NoSuchElementException:
            msg = "Failed to locate element within viewport, falling back to alternative method."
            logger.info(msg)
            self._fallback_scroll_to_element(value, locator_method, direction)
            return None
        else:
            return True

    # def _query_builder_uiautomator(self, value: str, locator_method) -> str:
    #     ui_selector = kwargs.get("ui_selector")
    #     return f'(new UiSelector().{ui_selector}("{value}"))'

    def _fallback_scroll_to_element(self, value: str, locator_method: AppiumBy, direction: SeekDirection = None) -> bool:
        action = self._create_action()
        for _ in range(self._max_attempts):
            try:
                element = self._driver.find_element(locator_method, value)
                element_x, element_y = calculate_element_points(element)["mid"]

                if direction in [SeekDirection.UP, SeekDirection.DOWN]:
                    self._swipe_element_into_view_vertical(action, element_y, direction)
                    return True
                elif direction in [SeekDirection.LEFT, SeekDirection.RIGHT]:  # noqa: RET505
                    self._swipe_element_into_view_horizontal(
                        action,
                        element_x,
                        direction,
                    )
                    return True
            except NoSuchElementException:
                swipe_actions = {
                    SeekDirection.UP: lambda: self._perform_navigation_partial_y(
                        action,
                        self._boundaries["upper"],
                        self._boundaries["lower"],
                        self._scrollable_area["y"] * -0.4,
                    ),
                    SeekDirection.DOWN: lambda: self._perform_navigation_partial_y(
                        action,
                        self._boundaries["lower"],
                        self._boundaries["upper"],
                        self._scrollable_area["y"] * 0.4,
                    ),
                    SeekDirection.LEFT: lambda: self._perform_navigation_partial_x(
                        action,
                        self._boundaries["left"],
                        self._boundaries["right"],
                        self._scrollable_area["x"] * -0.2,
                    ),
                    SeekDirection.RIGHT: lambda: self._perform_navigation_partial_x(
                        action,
                        self._boundaries["right"],
                        self._boundaries["left"],
                        self._scrollable_area["x"] * 0.2,
                    ),
                }
                swipe_actions[direction]()

        return False

    def up(self) -> None:
        """Perform a full upward swipe of the calculated viewport."""
        action = self._create_action()
        try:
            self._perform_navigation_full_y(
                action, self._boundaries["lower"], self._boundaries["upper"]
            )
        except (WebDriverException, KeyError, AttributeError) as e:
            self._log_and_raise(f"Failed to swipe up: {e}", e)

    def down(self) -> None:
        """Perform a full downward swipe of the calculated viewport."""
        action = self._create_action()
        try:
            self._perform_navigation_full_y(
                action, self._boundaries["upper"], self._boundaries["lower"]
            )
        except (WebDriverException, KeyError, AttributeError) as e:
            self._log_and_raise(f"Failed to swipe down: {e}", e)

    def left(self) -> None:
        """Perform a full leftward swipe of the calculated viewport."""
        action = self._create_action()
        try:
            self._perform_navigation_full_x(
                action, self._boundaries["right"], self._boundaries["left"]
            )
        except (WebDriverException, KeyError, AttributeError) as e:
            self._log_and_raise(f"Failed to swipe left: {e}", e)

    def right(self) -> None:
        """Perform a full rightward swipe of the calculated viewport."""
        action = self._create_action()
        try:
            self._perform_navigation_full_x(
                action, self._boundaries["left"], self._boundaries["right"]
            )
        except (WebDriverException, KeyError, AttributeError) as e:
            self._log_and_raise(f"Failed to swipe right: {e}", e)

    def previous(self) -> None:
        """Perform a complete swipe from the left-edge of the viewport."""
        action = self._create_action()
        try:
            self._perform_navigation_full_x(action, 0, self._viewport_width)
        except (WebDriverException, AttributeError) as e:
            self._log_and_raise(f"Failed to swipe to previous: {e}", e)

    def next(self) -> None:
        """Perform a complete swipe from the right-edge of the viewport."""
        action = self._create_action()
        try:
            self._perform_navigation_full_x(action, self._viewport_width, 0)
        except (WebDriverException, AttributeError) as e:
            self._log_and_raise(f"Failed to swipe to next: {e}", e)

    def on_element(self, element: WebElement, direction: Direction) -> None:
        """Swipe on a specific element in the given direction."""
        try:
            action = self._create_action()
            element_points = calculate_element_points(element, True)

            points_map = {
                Direction.UP: (element_points["bottom_mid"], element_points["top_mid"]),
                Direction.DOWN: (
                    element_points["top_mid"],
                    element_points["bottom_mid"],
                ),
                Direction.RIGHT: (
                    element_points["left_mid"],
                    element_points["right_mid"],
                ),
                Direction.LEFT: (
                    element_points["right_mid"],
                    element_points["left_mid"],
                ),
            }

            self._perform_navigation_on_element(action, *points_map[direction])
        except (WebDriverException, KeyError, AttributeError, ValueError) as e:
            self._log_and_raise(f"Failed to swipe on element: {e}", e)

    def _swipe_element_into_view_vertical(
        self, action: ActionChains, element_y: int, direction: SeekDirection
    ) -> None:
        """Perform vertical swipes to bring an element into view."""
        try:
            distance_to_element = element_y - self._boundaries["lower"]
            actions_total = distance_to_element / self._scrollable_area["y"]
            actions_complete = int(distance_to_element // self._scrollable_area["y"])
            actions_partial = int(
                self._scrollable_area["y"] * (actions_total - actions_complete)
            )

            start, end = (
                (self._boundaries["upper"], self._boundaries["lower"])
                if direction == SeekDirection.UP
                else (self._boundaries["lower"], self._boundaries["upper"])
            )

            if actions_total > 1:
                self._perform_navigation_full_y(action, start, end, actions_complete)
            if actions_partial > SWIPE_ACTION_THRESHOLD:
                self._perform_navigation_partial_y(action, start, end, actions_partial)
        except (
            WebDriverException,
            KeyError,
            ZeroDivisionError,
            TypeError,
            ValueError,
        ) as e:
            self._log_and_raise(f"Failed to swipe element into view vertically: {e}", e)

    def _swipe_element_into_view_horizontal(
        self, action: ActionChains, element_x: int, direction: SeekDirection
    ) -> None:
        """Perform horizontal swipes to bring an element into view."""
        try:
            distance_to_element = element_x - self._boundaries["left"]
            actions_total = distance_to_element / self._scrollable_area["x"]
            actions_complete = int(distance_to_element // self._scrollable_area["x"])
            actions_partial = int(
                self._scrollable_area["x"] * (actions_total - actions_complete)
            )

            start, end = (
                (self._boundaries["right"], self._boundaries["left"])
                if direction == SeekDirection.LEFT
                else (self._boundaries["left"], self._boundaries["right"])
            )

            if actions_total > 1:
                self._perform_navigation_full_x(action, start, end, actions_complete)
            if actions_partial > SWIPE_ACTION_THRESHOLD:
                self._perform_navigation_partial_x(action, start, end, actions_partial)
        except (
            WebDriverException,
            KeyError,
            ZeroDivisionError,
            TypeError,
            ValueError,
        ) as e:
            self._log_and_raise(
                f"Failed to swipe element into view horizontally: {e}", e
            )

    def _perform_navigation_full_y(
        self,
        action: ActionChains,
        initial_bound: int,
        final_bound: int,
        iterations: int = 1,
    ) -> None:
        """Perform full vertical navigation swipes."""
        try:
            for _ in range(iterations):
                self._perform_swipe(
                    action,
                    (self._viewport_x_mid_point, initial_bound),
                    (self._viewport_x_mid_point, final_bound),
                )
                action.perform()
        except (WebDriverException, AttributeError, ValueError) as e:
            self._log_and_raise(f"Failed to perform full vertical navigation: {e}", e)

    def _perform_navigation_partial_y(
        self,
        action: ActionChains,
        initial_bound: int,
        final_bound: int,
        partial_percentage: int,
    ) -> None:
        """Perform a partial vertical navigation swipe."""
        try:
            self._perform_swipe(
                action,
                (self._viewport_x_mid_point, initial_bound),
                (self._viewport_x_mid_point, final_bound + partial_percentage),
            )
            action.perform()
        except (WebDriverException, AttributeError, ValueError) as e:
            self._log_and_raise(
                f"Failed to perform partial vertical navigation: {e}", e
            )

    def _perform_navigation_full_x(
        self,
        action: ActionChains,
        initial_bound: int,
        final_bound: int,
        iterations: int = 1,
    ) -> None:
        """Perform full horizontal navigation swipes."""
        try:
            for _ in range(iterations):
                self._perform_swipe(
                    action,
                    (initial_bound, self._viewport_y_mid_point),
                    (final_bound, self._viewport_y_mid_point),
                )
                action.perform()
        except (WebDriverException, AttributeError, ValueError) as e:
            self._log_and_raise(f"Failed to perform full horizontal navigation: {e}", e)

    def _perform_navigation_partial_x(
        self,
        action: ActionChains,
        initial_bound: int,
        final_bound: int,
        partial_percentage: int,
    ) -> None:
        """Perform a partial horizontal navigation swipe."""
        try:
            self._perform_swipe(
                action,
                (initial_bound, self._viewport_y_mid_point),
                (final_bound + partial_percentage, self._viewport_y_mid_point),
            )
            action.perform()
        except (WebDriverException, AttributeError, ValueError) as e:
            self._log_and_raise(
                f"Failed to perform partial horizontal navigation: {e}", e
            )

    def _perform_navigation_on_element(
        self,
        action: ActionChains,
        initial_bound: tuple[int, int],
        final_bound: tuple[int, int],
    ) -> None:
        """Perform a navigation swipe on a specific element."""
        try:
            self._perform_swipe(action, initial_bound, final_bound)
            action.perform()
        except (WebDriverException, AttributeError, ValueError) as e:
            self._log_and_raise(f"Failed to perform navigation on element: {e}", e)

    def _perform_swipe(
        self, action: ActionChains, start: tuple[int, int], end: tuple[int, int]
    ) -> None:
        """Perform a swipe action from start to end coordinates."""
        try:
            action.w3c_actions.pointer_action.move_to_location(*start)
            action.w3c_actions.pointer_action.pointer_down()
            action.w3c_actions.pointer_action.move_to_location(*end)
            action.w3c_actions.pointer_action.pause(0.5)
            action.w3c_actions.pointer_action.release()
        except (WebDriverException, AttributeError, ValueError) as e:
            self._log_and_raise(f"Failed to perform swipe action: {e}", e)
