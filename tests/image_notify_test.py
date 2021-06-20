import os
import sys

# from winpynotify import win_notify as notifier

scriptpath = "src/winpynotify"
sys.path.append(os.path.abspath(scriptpath))
import win_notify as notifier

def image_notify_test():
    notifier.notify_win_image_link(
        "App Name Title",
        "Title Name", 
        "Text Inside", 
        "https://picsum.photos/364/180?image=1043", 
        "https://www.google.com/",
        4
    )

def notify_test():
    notifier.notify_win("App Name Title", "Title Name", "Text Inside")

def clean_env():
    notifier.clean_temp()

if __name__ == "__main__":
    clean_env()
    image_notify_test()
    notify_test()