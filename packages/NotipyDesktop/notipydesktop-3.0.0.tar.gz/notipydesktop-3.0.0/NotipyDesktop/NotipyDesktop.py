#!/usr/bin/env python3
import sys
import gi
gi.require_version('Notify', '0.7')  # Version festlegen
from gi.repository import Notify

def notify(app_name, title, message):
    Notify.init(app_name)
    notification = Notify.Notification.new(title, message)
    notification.show()

if __name__ == "__main__":
    if len(sys.argv) != 4:  # sys.argv[0] (Skriptname) + 3 Argumente
        print("Usage: python3 PyNotifier.py <app_name> <title> <message>")
    else:
        app_name = sys.argv[1]
        title = sys.argv[2]
        message = sys.argv[3]
        notify(app_name, title, message)
