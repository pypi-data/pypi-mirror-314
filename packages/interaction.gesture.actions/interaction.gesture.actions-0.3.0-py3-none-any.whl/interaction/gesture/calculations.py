import logging

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)

from .exceptions import ViewportError

logger = logging.getLogger(__name__)


def calculate_boundaries_and_scrollable_area(
    driver: WebDriver, **kwargs: any
) -> tuple[dict, dict]:
    """
    Calculate and return scrolling boundaries and scrollable area based on crop factors.

    Returns:
        tuple: A tuple containing two dictionaries:
            - boundaries: Dictionary with upper, lower, left, and right bounds
            - scrollable_area: Dictionary with x and y dimensions

    """
    viewport_width, viewport_height = retrieve_viewport_dimensions(driver)
    crop_factors = {
        "upper_cf": kwargs.get("upper_cf", 0.20),
        "lower_cf": kwargs.get("lower_cf", 0.90),
        "left_cf": kwargs.get("left_cf", 0.10),
        "right_cf": kwargs.get("right_cf", 0.90),
    }
    boundaries = {
        "upper": int(viewport_height * crop_factors["upper_cf"]),
        "lower": int(viewport_height * crop_factors["lower_cf"]),
        "left": int(viewport_width * crop_factors["left_cf"]),
        "right": int(viewport_width * crop_factors["right_cf"]),
    }
    scrollable_area = {
        "x": boundaries["right"] - boundaries["left"],
        "y": boundaries["lower"] - boundaries["upper"],
    }

    return crop_factors, boundaries, scrollable_area


def _get_element_coordinates(element: WebElement) -> tuple[int, int, int, int]:
    """
    Get the location and size of an element.

    Args:
        element: The WebElement to calculate points for.

    Returns:
        A tuple containing x, y, width, and height of the element.

    Raises:
        ValueError: If the element dimensions are invalid.
    """
    x, y = element.location["x"], element.location["y"]
    width, height = element.size["width"], element.size["height"]

    if width <= 0 or height <= 0:
        msg = "Invalid element dimensions"
        raise ValueError(msg)

    return x, y, width, height


def calculate_element_points(
    element: WebElement, safe_inset: bool = False
) -> dict[str, tuple[int, int]]:
    """
    Calculate various points on an element with optional safety insets.

    Args:
        element: The WebElement to calculate points for.
        safe_inset: If True, applies a 10% inset to all edge points for safer interaction.
                    Default is False.

    Returns:
        A dictionary containing coordinates of nine points on the element:
        - Corners: top_left, top_right, bottom_left, bottom_right
        - Edge midpoints: top_mid, right_mid, bottom_mid, left_mid
        - Center: mid

    Raises:
        ValueError: If the element dimensions are invalid.
    """
    try:
        x, y, width, height = _get_element_coordinates(element)

        mid_x = x + width // 2
        mid_y = y + height // 2
        right_x = x + width
        bottom_y = y + height

        if safe_inset:
            inset = 0.1  # 10% inset
            inset_x = int(width * inset)
            inset_y = int(height * inset)

            return {
                # Corners
                "top_left": (x + inset_x, y + inset_y),
                "top_right": (right_x - inset_x, y + inset_y),
                "bottom_left": (x + inset_x, bottom_y - inset_y),
                "bottom_right": (right_x - inset_x, bottom_y - inset_y),
                # Edge midpoints
                "top_mid": (mid_x, y + inset_y),
                "right_mid": (right_x - inset_x, mid_y),
                "bottom_mid": (mid_x, bottom_y - inset_y),
                "left_mid": (x + inset_x, mid_y),
                # Center point
                "mid": (mid_x, mid_y),
            }

        return {
            # Corners
            "top_left": (x, y),
            "top_right": (right_x, y),
            "bottom_left": (x, bottom_y),
            "bottom_right": (right_x, bottom_y),
            # Edge midpoints
            "top_mid": (mid_x, y),
            "right_mid": (right_x, mid_y),
            "bottom_mid": (mid_x, bottom_y),
            "left_mid": (x, mid_y),
            # Center point
            "mid": (mid_x, mid_y),
        }

    except ValueError as e:
        msg = f"Failed to calculate element points: {str(e)}"
        logger.error(msg)
        raise


def retrieve_element_location(element: WebElement) -> tuple[int, int]:
    """
    Retrieve the location of an element.

    Args:
        locator_method: The method to locate the element (e.g., AppiumBy.XPATH).
        locator_value: The value to use with the locator method.

    Returns:
        A tuple containing the x and y coordinates of the element.
    """
    try:
        return element.location["x"], element.location["y"]
    except TimeoutException as e:
        msg = f"Element not found: {str(e)}"
        logger.error(msg)
        raise NoSuchElementException(msg) from e


def retrieve_viewport_dimensions(driver: WebDriver) -> tuple[int, int] | None:
    """
    Retrieve the viewport dimensions from the driver.

    Returns:
        A tuple of (width, height) or None if dimensions couldn't be retrieved.
    """
    try:
        viewport = driver.get_window_size()
        if viewport is None:
            msg = "Failed to retrieve viewport dimensions"
            raise ViewportError(msg)
        return viewport["width"], viewport["height"]
    except WebDriverException as e:
        msg = f"Failed to get viewport dimensions: {str(e)}"
        logger.error(msg)
        raise ViewportError(msg) from e
