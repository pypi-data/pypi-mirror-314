# Appium Gestures Library

This library is to provide a number gesture/interaction functions for Appium mobile automation.  
The gestures are platform agnostic, which allows the user to provide a WebElement - or locators for both Android and iOS in the same function call.  

## Available Functions

### Swipe Gestures

- [x] up()
- [x] down()
- [x] left()
- [x] right()
- [x] next()
- [x] previous()
- [x] on_element()
- [x] element_into_view()

### Drag and Drop Gestures

- [x] drag_and_drop()

### Pinch Gestures

- [x] open()
- [x] close()

-----

[Documentation](https://tanakrit-d.github.io/appium-gesture-actions/index.html)

-----

## Compatibility

- [x] Android  
  Requires: `appium driver install uiautomator2`
- [x] iOS (unverified)  
  Requires: `appium driver install xcuitest`

## Install

```bash
pip install interaction-gesture-actions
# or
uv add interaction-gesture-actions
```

### Changelog

```md
## 0.3.0 (2024-12-12) 🎄

- Renamed package to resolve namespace collisions
  - This also resolved the workaround required when building docs

    ```python
    from interaction.gestures.actions import GestureActions
    ```

- Updated dependencies
- Change build backend from `hatchling` to `build`
- Migrating back from TypedDict allows for better Type Hinting/Intellisense
- Updated demo
```

See full list of changes: [CHANGES.md](https://github.com/tanakrit-d/appium-gesture-actions/raw/main/CHANGES.md)

## To-do

- [x] Expand functionality to include gestures
- [x] Add cross-platform functionality
- [x] Robust error handling
- [x] Add documentation
- [x] Add examples for other gestures
- [x] Return bool for most functions
- [ ] Return WebElement on `element_into_view()`
- [ ] Completely rewrite the tests
- [ ] Allow for the specifying of values in sub-classes (such as `_max_attempts` or `CROP_FACTOR_` in `SwipeGestures`)
- [ ] Reduce minimum Python version
- [ ] Remove direct accessing of `ActionBuilder` - or not..
- [ ] Handling of different orientations
- [ ] Allow for re-initialisation of viewport calculations

## Demo and Example Usage

### Demonstration

This demo shows the following actions being executed:

```python
element_a = self.driver.find_element(AppiumBy.XPATH, "//android.widget.ImageView")
action.pinch.open(element_a)
action.pinch.close(element_a)
element_b = self.driver.find_element(
    AppiumBy.XPATH,
    "//android.widget.ScrollView/android.view.View[1]/android.widget.EditText[3]",
)
action.drag_drop.drag_and_drop(element_a, element_b)
action.swipe.element_into_view(
    value_a='new UiSelector().descriptionContains("Day planted")',
    locator_method_a=AppiumBy.ANDROID_UIAUTOMATOR,
)
action.swipe.element_into_view(
    value_a="//android.widget.ImageView",
    locator_method_a=AppiumBy.XPATH,
    direction=SeekDirection.UP,
)
```

![Library Demo](https://github.com/tanakrit-d/appium-gesture-actions/raw/main/demo/example.gif)

### Example Implementation

```python
from interaction.gestures.actions import GestureActions
from interaction.gestures.enums import Direction, SeekDirection, UiSelector

class TestDemo(TestCore):
    def test_cool_stuff(self):
        # Initialise class object
        action = GestureActions(self.driver, self.options["platformName"])

        # Drag and Drop
        image_element = driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.widget.ImageView[0]',
        )
        delete_element = driver.find_element(
            by=AppiumBy.XPATH,
            value='//android.widget.ImageView[1]',
        )
        action.drag_drop.drag_and_drop(image_element, delete_element)

        # Swipe
        action.swipe.up()
        action.swipe.next()

        # Pinch
        action.pinch.open(image_element)

        # Swipe on Element
        action.swipe.on_element(
            image_element,
            Direction.LEFT,
        )

        # Scroll to Element (Android - UiAutomator)
        action.swipe.element_into_view(
            value_a='new UiSelector().description("Save")',
            locator_method_a=AppiumBy.ANDROID_UIAUTOMATOR,
        )

        # Scroll to Element (Android - XPATH)
        action.swipe.element_into_view(
            value_a="//android.widget.ImageView",
            locator_method_a=AppiumBy.XPATH,
            direction=SeekDirection.UP,
        )

        # Scroll to Element (Multi-platform, single code base)
        action.swipe.element_into_view(
            value_a='//android.widget.Button[@content-desc="Save"]',
            value_i="label == 'Save'"
            locator_method_a=AppiumBy.XPATH,
            locator_method_i=AppiumBy.IOS_PREDICATE,
            direction=SeekDirection.DOWN,
        )
```

## An Explainer on Swipe Element Into View

This function (part of the [SwipeGestures](https://github.com/tanakrit-d/appium-gesture-actions/blob/5fbda3fa02cc07474dfe532fe5ac0f43fb6928a7/src/interaction/gesture/swipe.py#L44) class) has cross-platform support.  
It is achieved by using parameters with different suffixes (`_a` and `_i` for Android and iOS respectively).  

This will allow you to use a single function call for use on both platforms.

Additionally, it includes a fallback method (which is less efficient) if the element cannot be located initially.  
This is achieved by scrolling the viewport until the element is located, or the maximum number of swipes is achieved (default: 5).  
An example situation would be if an element is not yet present in the viewport and is loaded after scrolling.  
If this situation applies to you, the `direction` parameter will need to be specified.  

### A Quick Word on Perform Navigation (Full and Partial)

The fallback method will calculate the viewport size, and then define a scrollable region based on crop factors to avoid triggering the notification shade/center or multi-tasking view.  
If it cannot locate the element, it will call `_perform_navigation_partial_` until it does - or it exceeds the max attempts.  
In the event that the element *is* present but *not* in the viewport, it will calculate the distance to the element.  
Then, it will determine the correct number of full (and if necessary) partial swipes to bring the element into the center of the viewport.  

Additionally, the `if actions_partial > SWIPE_ACTION_THRESHOLD` check ensures the pixel distance is large enough to warrant an action.  
When this value is less than 50px, the swipe action will be interpreted by the OS as a double-tap.

Please look at `_fallback_scroll_to_element` if you would like to learn more.  
<https://github.com/tanakrit-d/appium-gesture-actions/blob/5fbda3fa02cc07474dfe532fe5ac0f43fb6928a7/src/interaction/gesture/swipe.py#L172>

## Defining a Scrollable Region

This library divides the viewport into four bounds: upper, lower, left, and right. The default values cannot be overwritten (this will change in a future release).  
Using these bounds, we then define a 'scrollable region'. We can then perform our scroll/swipe actions within this space.  
The impetus for this is to recreate scrolling/swiping behaviour more similar to a user and avoid hardcoding coordinates.  
Additionally, it avoids the automation attempting to perform actions on top of elements (such as headers or footers).  
![Viewport Diagram](https://github.com/tanakrit-d/appium-gesture-actions/raw/main/resources/viewport_scrollable_bounds.png)

## Defining Element Points

The importance of dynamically generating 'points' of an element to interact with allows us to account for re-sizing under a number of conditions (such as different devices/resolutions).

For the purpose of this library, we are only concerned with two attributes of an element: position and size.  
The element's coordinates within the viewport is considered the top-left-point.

We can then use the element size to determine where it occupies relative to the view-port position.
![Element Diagram](https://github.com/tanakrit-d/appium-gesture-actions/raw/main/resources/understanding_element_position-dimension.png)

```python
top_left_point      = element.location["x"], element.location["y"]
top_mid_point       = element.location["x"] + (element.size["width"] // 2), element.location["y"]
top_right_point     = element.location["x"] + element.size["width"], element.location["y"]

left_mid_point      = element.location["x"], element.location["y"] + (element.size["height"] // 2)
mid_point           = element.location["x"] + (element.size["width"] // 2), element.location["y"] + (element.size["height"] // 2)
right_mid_point     = element.location["x"] + element.size["width"], element.location["y"] + (element.size["height"] // 2)

bottom_left_point   = element.location["x"], element.location["y"] + element.size["height"]
bottom_mid_point    = element.location["x"] + (element.size["width"] // 2), element.location["y"] + element.size["height"]
bottom_right_point  = element.location["x"] + element.size["width"], element.location["y"] + element.size["height"]
```

Using the example element from the image, the above calculations would output as follows:  

```console
Top-Left-Point:  (20, 20)  
Top-Mid-Point:  (40, 20)  
Top-Right-Point:  (60, 20)
  
Left-Mid-Point:  (20, 30)  
Mid-Point:  (40, 30)  
Right-Mid-Point:  (60, 30)
  
Bottom-Left-Point:  (20, 40)  
Bottom-Mid-Point:  (40, 40)  
Bottom-Right-Point:  (60, 40)
```

An example of this is available here: [demo/calc_coordinates.py](https://github.com/tanakrit-d/appium-gesture-actions/raw/main/demo/calc_coordinates.py)

## Notes

### Gesture Execution, Design Decisions, and Documentation

I wrote this library based on issues I had with automating scroll-to-element functionality in my testing.  
The majority of the tutorials or documentation I have found on the subject is either sparse, low quality and SEO orientated, or relies on hardcoding coordinates for the scroll actions.  
Additionally, I did not find these to be robust enough or support different screen sizes when using the same code for different devices.  

-----

The [Appium Python Client](https://github.com/appium/python-client/blob/master/appium/webdriver/extensions/action_helpers.py) implementation relies on `ActionChains`, and the `.swipe()` and `.scroll()` functions require either both elements to be directly provided - or the x and y coordinates to be specified.

In this library, `Drag and Drop` and `Pinch` call the Selenium JavaScript `.execute_script()` function - which is more reliable and robust than using `ActionChains`.  

Initially, a prototype implementation using `ActionChains` was attempted, however the performance was poor and buggy since Selenium implements a number of logical checks when executing it.  
I found it threw numerous exceptions due to some form of built-in element detection.  

`Swipe` contains a combination of `.execute_script()` and `ActionChains`.  

For Android, the preferred method is `AppiumBy.ANDROID_UIAUTOMATOR` which uses `new UiScrollable()` as it is incredibly quick and reliable.  
It will use `ActionChains` if any other locator method is called.  

For iOS, it will initially attempt to use `.execute_script()`, and then fallback to `ActionChains` if the element cannot be located.

I would recommend reading the following documentation which helped inform the design and implementation.  

- [Appium XCUITest Driver](https://appium.github.io/appium-xcuitest-driver/latest/reference/execute-methods/)
  - [NSPredicate Cheatsheet](http://realm.io.s3-website-us-east-1.amazonaws.com/assets/downloads/NSPredicateCheatsheet.pdf)
- [Appium UiAutomator2 Driver](https://github.com/appium/appium-uiautomator2-driver/blob/master/docs/android-mobile-gestures.md)
  - [Android Developer Reference: UiScrollable](https://developer.android.com/reference/androidx/test/uiautomator/UiScrollable)
  - [Android Developer Reference: UiSelector](https://developer.android.com/reference/androidx/test/uiautomator/UiSelector)
- [Appium Swipe Tutorial](https://appium.github.io/appium.io/docs/en/writing-running-appium/tutorial/swipe-tutorial/)

### Android

If you would like to see the pointer interactions and coordinates, this can be enabled on a device level in `Settings > Developer Options > Pointer location`

## Contributing

Contributions or feedback is welcome! Please feel free to submit a Pull Request.  
As this is my first Python package I am open to any and all suggestions :^)

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository.
