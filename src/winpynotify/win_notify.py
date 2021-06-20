import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom
import sys
import requests
import os
import os.path as path
import shutil
from PIL import Image

color_red = (255,0,0,255)
color_yellow = (255,255,0,255)
color_white = (255,255,255,255)

def resize_image_keep_aspect(image_raw, width, height, background_color):
    '''
    Resize PIL image keeping ratio and using white background.
    '''
    image_pil = Image.open(image_raw)
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height
    image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGBA', (width, height), background_color)
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    return background.convert('RGB')

def clamp(n, smallest, largest): 
    return max(smallest, min(n, largest))

def get_priority_color(priority):
    result_priority = clamp(priority, 0, 2)
    if result_priority == 0:
        return color_white
    if result_priority == 1:
        return color_yellow
    if result_priority == 2:
        return color_red
    return color_red

def resize_image(raw_image, width, height):
    return Image.open(raw_image).resize((width, height), Image.ANTIALIAS)

def get_available_file_id(temp_dir):
    max_id = 0
    for file in os.listdir(temp_dir):
        if file.endswith(".jpg"):
            filename = file.replace(".jpg", "")
            if filename.isnumeric():
                file_id = int(filename)
                max_id = file_id if file_id > max_id else max_id
    return int(max_id) + int(1)

def get_available_filename(temp_dir):
    return str(get_available_file_id(temp_dir)) + ".jpg"

def get_image_local_path(image):
    # create temp image folder
    working_dir = os.getcwd()
    temp_dir = path.join(working_dir, "temp")
    if (False == path.isdir(temp_dir)):
        os.mkdir(temp_dir)

    # if 'image' is online link we need to save file first
    is_web_image = "http" in image
    image_path = image
    if is_web_image:
        image_path = path.join(temp_dir, get_available_filename(temp_dir))

    return image_path

def get_notify_xml(app_id, title, text, image_path, url):
    #define notification as string
    xml_string = f"""
    <toast launch="{app_id}">
    <visual>
      <binding template="ToastGeneric">
        <image placement="hero" src="{image_path}"/>
            <text hint-maxLines="1">{title}</text>
            <text>{text}</text>
      </binding>
    </visual>
    <actions>
        <action content="Open" activationType="protocol" arguments="{url}" />
    </actions>
  </toast>
"""
    return xml_string

def notify_win(app_id, title, text):
    notify_win_common(app_id, title, text, "", "", 0)

def notify_win_image(app_id, title, text, image):
    notify_win_common(app_id, title, text, image, "", 0)

def notify_win_link(app_id, title, text, link):
    notify_win_common(app_id, title, text, "", link, 0)

def notify_win_image_link(app_id, title, text, image, link, priority):
    notify_win_common(app_id, title, text, image, link, priority)

def notify_win_common(app_id, title, text, image, url, priority):
    # initialize notifier
    nManager = notifications.ToastNotificationManager
    notifier = nManager.create_toast_notifier(sys.executable)

    image_path = get_image_local_path(image)

    is_web_image = "http" in image
    # download image file
    if is_web_image:
        img_data = resize_image_keep_aspect(requests.get(image, stream=True).raw, 640, 360, get_priority_color(priority))
        img_data.save(image_path, format='JPEG')

    xml_string = get_notify_xml(app_id, title, text, image_path, url)

    # Convert notification to an XmlDocument
    xDoc = dom.XmlDocument()
    xDoc.load_xml(xml_string)

    # Display notification
    notifier.show(notifications.ToastNotification(xDoc))

def clean_temp():
    working_dir = os.getcwd()
    temp_dir = path.join(working_dir, "temp")
    if (True == path.isdir(temp_dir)):
        shutil.rmtree(temp_dir)