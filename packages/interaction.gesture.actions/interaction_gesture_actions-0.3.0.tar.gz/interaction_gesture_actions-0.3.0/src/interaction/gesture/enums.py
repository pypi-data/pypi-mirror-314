from enum import Enum


class Direction(Enum):
    """Direction of the swipe action."""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    IN = "in"
    OUT = "out"


class SeekDirection(Enum):
    """
    Direction in which to seek for an element.
    """

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class UiSelector(Enum):
    """
    Android UiSelector method to locate an element.
    """

    DESC = "description"
    DESC_CONTAINS = "descriptionContains"
    DESC_MATCHES = "descriptionMatches"
    CLASS = "className"
    CLASS_MATCH = "classNameMatches"
    TEXT = "text"
    TEXT_CONTAINS = "textContains"
    TEXT_MATCHES = "textMatches"
    TEXT_STARTS_WITH = "textStartsWith"
