# cv2_gui

`cv2_gui` is a Python library for creating GUI elements using OpenCV.

# Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Button Types](#button-types)
    1. [Toggle Button](#toggle-button)
    2. [Cycle Button](#cycle-button)
    3. [Slider](#slider)
    4. [Eyedropper](#eyedropper)
    5. [D-Pad](#d-pad)



## Introduction

`cv2_gui` simplifies creating GUI elements, such as buttons, sliders, and more, with OpenCV.

## Installation

```bash
pip install cv2_gui
```
This will also install dependencies such as `cv2` and `numpy`.

## Button Types

| Button Type        | Description                          | Example Usage           |
|--------------------|--------------------------------------|-------------------------|
| [Toggle Button](#toggle-button)      | Switch between two states.          | `create_toggle_button`  |
| [Cycle Button](#cycle-button)       | Cycle through a list of options.    | `create_cycle_button`   |
| [Slider](#slider)             | Adjust a value within a range.      | `create_slider`         |
| [Eyedropper](#eyedropper)         | Select a color from an image.       | `create_eyedropper`     |
| [D-Pad](#d-pad)              | Control directional movements.      | `create_dpad`           |


### Toggle Button
Toggle button can switch between on and off state performing 1 of 2 actions based on current state.
#### Parameters for `create_toggle_button`

| Parameter Name   | Description                                                                 | Type                |
|------------------|-----------------------------------------------------------------------------|---------------------|
| `on_text`        | The text displayed on the button when it is in the "on" state.                | `str`               |
| `off_text`       | The text displayed on the button when it is in the "off" state.               | `str`               |
| `on_callback`    | The function that will run when the button is in the "on" state.              | `function`          |
| `off_callback`   | The function that will run when the button is in the "off" state.             | `function` or `None`|
| `toggle_once`    | If `True`, will run the callback function every update; otherwise, it runs the callback only when the state changes. | `bool`              |
| `on_color`       | The color of the button in the "on" state, represented as a list of RGB values. | `List[float, float, float]` |
| `off_color`      | The color of the button in the "off" state, represented as a list of RGB values. | `List[float, float, float]` |
| `tooltip`        | The text displayed when you hover over the button, providing additional information about the button's state. | `str`               |

#### example
a basic function that will be executed based on button state
```python
def display_image(img):
    return img[0]
```


import toggle button, button manager and dependecies from library.
```python
from cv2_gui import create_button_manager, create_toggle_button
import cv2
import numpy as np

toggle=create_toggle_button('ON','OFF',display_image,display_image,tooltip="A simple on-off button")

```
this will create a button which when pressed will display the passed image.
```python
sample = cv2.imread('sample.png')
while 1:
    output = toggle.update([sample],[None])
    output = create_button_manager.update(output)
```
first argument of `update` is `argument_on` which will be passed to `on_callabck` and second argument is `argument_off` passed to `off_callback` these are run when the corresponding state is active.

You can press `q` to close the window and stop execution,
Hovering over the button will display the tooltip.

<div align="center">
  <div style="display: inline-block; margin-right: 20px;">
    <img src="media/toggle_video.gif" width="600" />
    <p><em>Toggle Button Demo</em></p>
  </div>
</div>

### Cycle Button
Cycle button can switch between multiple states performing various actions based on current state.
#### Parameters for `create_cycle_button`
| Parameter   | Description                                                                 | Type                        |
|-------------|-----------------------------------------------------------------------------|-----------------------------|
| `modes`     | The text that will be displayed on the button when in a particular mode.     | List of Strings             |
| `callbacks` | The functions that will run when the button is in a selected mode.          | List of Functions           |
| `toggle_once` | If `True`, the callback function runs every update; if `False`, runs once per state change. | Boolean                    |
| `tooltip`   | Text displayed when you hover the mouse on the button, providing further information. | String                      |

#### example
a basic function that will be executed based on button state
```python
def convert_img(arguments):
    type,frame=arguments

    if type.lower()=="hsv":
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    elif type.lower()=="rgb":
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    elif type.lower()=="bw":
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frame=cv2.merge([frame, frame, frame])

    return frame
```


import cycle button, button manager and dependecies from library.
```python
from cv2_gui import create_button_manager, create_cycle_button
import cv2
import numpy as np

cycle=cycle=create_cycle_button(["BGR","RGB","BW"],[convert_img,convert_img,convert_img],tooltip="convert image color format")
```
this will create a button which when cycled will convert image formats of the passed image.
```python
sample = cv2.imread('sample.png')
while 1:
    output = cycle.update([["BGR",output],["RGB",output],["BW",output]])
    output = create_button_manager.update(output)
```
first argument of `update` is `arguments` the first element of argument will be passed to first callback function and so on.

You can press `q` to close the window and stop execution,
Hovering over the button will display the tooltip.

<div align="center">
  <div style="display: inline-block; margin-right: 20px;">
    <img src="media/cycle_video.gif" width="600" />
    <p><em>Cycle Button Demo</em></p>
  </div>
</div>

### Slider

A slider allows users to adjust a value by dragging a handle along a track, with the value returned for use in other actions or settings.

#### Parameters for `create_slider`
| **Parameter**     | **Type**      | **Description**                                                                                                                                  |
|-------------------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| `text`            | String        | The text that will be displayed on the slider.                                                                                                   |
| `lower_range`     | int / float  | The lower threshold or minimum value of the slider.                                                                                             |
| `upper_range`     | int / float  | The upper threshold or maximum value of the slider.                                                                                             |
| `steps`           | int           | The number of steps on the slider between minimum and maximum.                                                                                  |
| `return_int`      | Boolean       | If true, will store the integer value of the slider. If false, will store the float value of the slider.                                        |
| `return_odd_int`  | Boolean       | If true, will store an odd integer value of the slider (used for blur where odd integers are needed). If false, will store the float value.    |
| `on_color`        | List(1x3)      | The color of the button border (RGB color value).                                                                                              |
| `toggle_once`     | Boolean       | If true, will run the callback function on every update. If false, will run the callback function once every time the state changes.            |
| `tooltip`         | String        | The text displayed when you hover the mouse over the button, providing further information about the button's states.                           |

#### example with `ranged = False`

import slider, button manager and dependecies from library.
```python
from cv2_gui import create_button_manager, create_slider
import cv2
import numpy as np

slider = create_slider("Blur",0,100,100,return_odd_int=True,tooltip="define values for blur amount")
```
this will create a slider which will store the current value and when we drag the slider update the value.
```python
while 1:
    sample = cv2.imread('sample.png')
    slider_val=slider.value
    sample = cv2.blur(sample, (slider_val,slider_val))
    create_button_manager.update(sample)
```
The value of the slider is stored in `slider.value` and is updated everytime `button_manager.update()` is called.

You can press `q` to close the window and stop execution,
Hovering over the button will display the tooltip.

<div align="center">
  <div style="display: inline-block; margin-right: 20px;">
    <img src="media/slider_video.gif" width="600" />
    <p><em>Slider Demo</em></p>
  </div>
</div>

#### example with `ranged = True`
a basic function that will be executed with slider value.
```python
def brightness_filter(frame,bounds):
    lower=bounds[0]
    upper=bounds[1]

    gray=cv2.cvtColor(frame.copy(),cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(gray, lower, upper)
    mask_3channel = cv2.merge([mask, mask, mask])
    filtered_image = cv2.bitwise_and(frame, mask_3channel)

    return filtered_image
```


import slider, button manager and dependecies from library.
```python
from cv2_gui import create_button_manager, create_slider
import cv2
import numpy as np

slider = create_slider("Light Filter",0,255,200,ranged=True,return_odd_int=True,tooltip="define values for blur amount")
```
this will create a slider which will store the lower and upper value and when we drag the slider update the value.
```python
while 1:
    sample = cv2.imread('sample.png')
    lower=int(slider.value[0])
    upper=int(slider.value[1])
    output=brightness_filter(sample,[lower,upper])
    create_button_manager.update(output)
```
The value of the slider is stored in `slider.value` as a list where `slider.value[0]` is lower value, `slider.value[1]` is upper value and it is updated everytime `button_manager.update()` is called.

You can press `q` to close the window and stop execution,
Hovering over the button will display the tooltip.

<div align="center">
  <div style="display: inline-block; margin-right: 20px;">
    <img src="media/slider_ranged_video.gif" width="600" />
    <p><em>Slider Ranged Demo</em></p>
  </div>
</div>


### Eyedropper

An eyedropper tool allows users to select a color from an image by clicking on the required pixel, displaying the selected color value.

#### Parameters for `create_eyedropper`

| **Parameter**       | **Type**       | **Description**                                                                                      |
|----------------------|----------------|------------------------------------------------------------------------------------------------------|
| `text`              | String         | The text displayed on the button.                                                                   |
| `toggle_duration`   | Float          | The duration (in seconds) for which the commanded function will execute before resetting. Overrides and resets if another key is pressed. |
| `toggle_once`       | Boolean        | If true, the callback function will run on every update. If false, it will run once when the state changes. |
| `on_color`          | List(1x3)      | The color of the button when it is pressed (RGB values).                                            |
| `off_color`         | List(1x3)      | The color of the button when it is released (RGB values).                                           |
| `tooltip`           | String         | The text displayed when hovering over the button, providing additional information about its states. |


#### example

import eyedropper, button manager and dependecies from library.
```python
from cv2_gui import create_button_manager, create_eyedropper
import cv2
import numpy as np

dropper=create_eyedropper()
```
this will create an eyedropper tool which will show the pixel values in BGR and HSV of the clicked pixel.
```python
while 1:
    sample = cv2.imread('sample.png')
    create_button_manager.update(sample)
```
You can press `q` to close the window and stop execution,
Hovering over the button will display the tooltip.

<div align="center">
  <div style="display: inline-block; margin-right: 20px;">
    <img src="media/eyedropper_video.gif" width="600" />
    <p><em>Eyedropper Demo</em></p>
  </div>
</div>

### D-pad
A D-pad (Directional pad) allows users to provide directional input (e.g., up, down, left, right) for navigation or control, with the selected direction respective action will be performed.

#### Parameters for `create_dpad`

| **Parameter**       | **Type**       | **Description**                                                                                      |
|----------------------|----------------|------------------------------------------------------------------------------------------------------|
| `text`              | String         | The text displayed on the button.                                                                   |
| `toggle_duration`   | Float          | The duration (in seconds) for which the commanded function will execute before resetting. Overrides and resets if another key is pressed. |
| `toggle_once`       | Boolean        | If true, the callback function will run on every update. If false, it will run once when the state changes. |
| `on_color`          | List(1x3)      | The color of the button when it is pressed (RGB values).                                            |
| `off_color`         | List(1x3)      | The color of the button when it is released (RGB values).                                           |
| `tooltip`           | String         | The text displayed when hovering over the button, providing additional information about its states. |


#### example

Basic functions which will be executed when corresponding button in pressed.
```python

```

import Dpad, button manager and dependecies from library.
```python
from cv2_gui import create_button_manager, create_dpad
import cv2
import numpy as np

dropper=create_eyedropper()
```
this will create a Dpad which perfoms an action when corresponding button is pressed.
```python
while 1:
    sample = cv2.imread('sample.png')
    create_button_manager.update(sample)
```
It will continously run the function for `toggle_duration` seconds

You can press `q` to close the window and stop execution,
Hovering over the button will display the tooltip.

<div align="center">
  <div style="display: inline-block; margin-right: 20px;">
    <img src="media/eyedropper_video.gif" width="600" />
    <p><em>Eyedropper Demo</em></p>
  </div>
</div>