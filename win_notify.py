from winrt.windows.ui.notifications import ToastNotificationManager, ToastNotification, ToastTemplateType
import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom

def toast_notification(AppID, title, text):
    XML = ToastNotificationManager.get_template_content(ToastTemplateType.TOAST_IMAGE_AND_TEXT02)

    texts = XML.get_elements_by_tag_name("text")
    texts[0].append_child(XML.create_text_node(title))
    texts[1].append_child(XML.create_text_node(text))

    images = XML.get_elements_by_tag_name("image")
    # images[0].attributes.get_named_item("src").node_value = "https://picsum.photos/364/180?image=1043"
    
    # src = images[0].attributes.get_named_item("src")
    # tp = src.node_type
    # tp1 = src.node_value
    # tp2 = src.node_name
    # src.node_value = "C:\\Projects\\Python\\WinPyNotify\\img.jpg"

    # img = XML.create_element("IMG")
    # img.set_attribute("src", "https://picsum.photos/364/180?image=1043")
    # images[0].append_child(img)
    
    # images[0].set_attribute("src", "https://picsum.photos/364/180?image=1043")

    notifier = ToastNotificationManager.create_toast_notifier(AppID)
    notifier.show(ToastNotification(XML))

def main():
    toast_notification("hey", "test", "test")

if __name__ == "__main__":
    main()