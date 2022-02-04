import urllib.request
import re
import socket
import threading
import sys

from BlockedUrl import BlockedUrl
from colorama import Fore

class UsomUrlHelper:   
    def __init__(self):
        self.thread_count = 8
        self.blocked_url_list = []
        self.usom_url = 'https://www.usom.gov.tr/url-list.txt'

    def get_blocked_urls_from_usom(self):
        try:
            response = urllib.request.urlopen(self.usom_url, timeout=3)
            for url in response:
                url_name = url.decode("utf-8").rstrip("\n")
                is_ip = self.check_ip(url_name)
                if is_ip is True:
                    continue            
                blocked_url = BlockedUrl(url_name, '')
                self.blocked_url_list.append(blocked_url)
        except:
            print("Url not open")
            sys.exit()


    def check_ip(self, url):
        ip_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        if(re.search(ip_regex, url)):
            return True
        return False
    
    def set_ip(self):
        try:
            thread_arr = []
            last_index = 0
            self.blocked_url_list = self.blocked_url_list[:80]
            loop_last_index = int(len(self.blocked_url_list) / self.thread_count)
            for i in range(loop_last_index):
                last_index = last_index + self.thread_count
                first_index = int(i * self.thread_count)
                partial_blocked_list = self.blocked_url_list[first_index:last_index]
                t = threading.Thread(target=self.get_ip_from_url, args=(partial_blocked_list,))
                thread_arr.append(t)

            for t in thread_arr:
                t.start()

            for t in thread_arr:
                t.join()
        except:
            print("Getting error in set ip function")

    def get_ip_from_url(self, blocked_url_list):               
        for blocked_url in blocked_url_list:
            try:
                ip_address = socket.gethostbyname(blocked_url.url_name)
                if not ip_address:
                    print(Fore.YELLOW + "bu ne aq " + blocked_url.url_name)
                blocked_url.ip = ip_address                    
                print(Fore.GREEN + "Url:" + blocked_url.url_name + " Ip:" + blocked_url.ip)                             
            except:
                print(Fore.RED + "Url: " +blocked_url.url_name + " IP Address not found")
                continue
                            
        
