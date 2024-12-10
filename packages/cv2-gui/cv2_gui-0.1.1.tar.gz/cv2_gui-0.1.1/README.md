# cv2_gui

`cv2_gui` is a Python library for creating GUI elements using OpenCV.

## Installation

```bash
pip install cv2_gui
```

## Usage

```python
from cv2_gui import create_button_manager, create_toggle_button, create_cycle_button, create_eyedropper,create_slider,create_dpad
import cv2

def aaa(default):
    pass

a = create_toggle_button("on","off",aaa,aaa)
b = create_cycle_button(["a","b"],[aaa,aaa])
c=create_slider("slider",0,100,100)
d=create_slider("slider2",0,100,100,ranged=True)

e=create_eyedropper()
f=create_dpad()



img=cv2.imread("sample.png")
while 1:
    a.update()
    arg = b.update()
    create_button_manager.update(img)
```


