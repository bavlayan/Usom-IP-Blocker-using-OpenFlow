import urllib.request
import re
from BlockedUrl import BlockedUrl
from colorama import Fore
import socket

class UsomUrlHelper:   
    def __init__(self):
        self.blocked_url_list = []
        self.usom_url = 'https://www.usom.gov.tr/url-list.txt'

    def get_blocked_urls_from_usom(self):
        response = urllib.request.urlopen(self.usom_url)
        for url in response:
            url_name = url.decode("utf-8").rstrip("\n")
            is_ip = self.check_ip(url_name)
            if is_ip is True:
                continue            
            blocked_url = BlockedUrl(url_name, '')
            self.get_ip_from_url(blocked_url)
            self.blocked_url_list.append(blocked_url)
        return self.blocked_url_list

    def check_ip(self, url):
        ip_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        if(re.search(ip_regex, url)):
            return True
        return False

    def get_ip_from_url(self, blocked_url):
        try:            
            ip_address = socket.gethostbyname(blocked_url.url_name)
            blocked_url.ip = ip_address
            print(Fore.GREEN + "Url: " +blocked_url.url_name + " IP Address: " + blocked_url.ip)
            return ip_address
        except:
            print(Fore.RED + "Url: " +blocked_url.url_name + " IP Address not found")
            return None
        
