# WinPyNotify

A Python framework to throw notifications to Windows Toaster.

## Usage

```python
from winpynotify import win_notify as notifier

# Simple notification:
notifier.notify_win("App Name Title", "Title Name", "Text Inside")
# Notification with image and open path(local or web) callback
notifier.notify_win_image_link(
    "App Name Title",
    "Title Name", 
    "Text Inside", 
    "https://picsum.photos/364/180?image=1043",  # notification picture
    "https://www.google.com/",                   # site you want to open on "Open" callback
    4                                            # priortiy (changes background color)
)
```

To test notifications:
```bash
python .\tests\image_notify_test.py
```

## Installation

All dependencies should be resolved by .toml file.

From root folder:
```bash
pip install .
```
