from UsomUrlHelper import UsomUrlHelper
import socket

if __name__ == "__main__":
    usomurlhelper = UsomUrlHelper()
    blocked_url_list = usomurlhelper.get_blocked_urls_from_usom()
    