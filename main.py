from UsomUrlHelper import UsomUrlHelper
import socket
import threading

def create_blocked_url_list():
    usomurlhelper = UsomUrlHelper()
    usomurlhelper.get_blocked_urls_from_usom()
    usomurlhelper.set_ip()

if __name__ == "__main__":
    create_blocked_url_list()

    