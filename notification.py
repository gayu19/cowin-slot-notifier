from plyer import notification

def send_notification(title, message, timeout):
    
    notification.notify(title= title,
                        message= message,
                        app_icon = None,
                        timeout= 15,
                        toast=False)

    return (f"{title}, {message}")