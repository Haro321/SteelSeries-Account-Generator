import requests
import json
from typing import Tuple
import string
from random import choice
from uuid import uuid4
from colorama import Fore
import threading

class STEELSERIES:
    def __init__(self , proxies : dict):
        self.proxies = proxies
    
    def register(self,email : str = None,password : str = None) -> json:
        """
            email : you can use fake one
            proxies : to avoid rate limit 
        """
        try:
            if email == None:
                email , password = self.random_data()
                
            url = "https://127.0.0.1:6327/user"

            payload = {
            "email": email,
            "password1": password,
            "password2": password,
            "acceptedPrivacyPolicy": True,
            "subscribeToNewsletter": [
                "on"
            ]
            }

            headers = {
            'Host': "127.0.0.1:6327",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) steelseries-gg-client/3.0.0 Chrome/126.0.6478.185 Electron/31.3.1 Safari/537.36",
            'Accept': "application/json, text/plain, */*",
            'Content-Type': "application/json",
            'Authorization': f"Bearer {uuid4}"
            }

            response = requests.post(url, data=json.dumps(payload), verify=False, headers=headers , proxies=self.proxies)
            jsonRes = response.json()
            
            if "{'error': '429'}" in jsonRes:
                return {
                    "success" : False,
                    "data" : "rate limit"
                }
            elif "error" not in jsonRes:
                self.save_data(jsonRes , password)
                return {
                    "success" : True,
                    "data" : jsonRes
                }
            else:
                return  {
                    "success" : False,
                    "data" : jsonRes
                }
                
        except Exception as e:
            print(Fore.RED , "error in register :", e , Fore.RESET)
                
    def random_data(self) -> Tuple[str,str]:
        email = "".join(choice(string.ascii_letters + string.digits) for i in range(9)) + "@gmail.com"
        password =  "".join(choice(string.ascii_letters + string.digits) for i in range(9))
        return email , password
    
    def save_data(self, data : json , password : str) -> bool:
        try:
            data['user']['password'] = password
            with open("accounts.json" ,"r") as file:
                oldData = json.load(file)
                oldData.append(data)
            with open("accounts.json","w") as file:
                json.dump(oldData, file , indent=4)
        except Exception as e:
            print("error in save_data :", e)
            
    def run(self):
        try:
            result = self.register()
            if result['success'] == True:
                print(Fore.GREEN , "account generated with email : ",result['data']['user']['email'] , Fore.RESET)
            else:
                print(Fore.RED , result , Fore.RESET)
        except Exception as e:
            print(Fore.RED + "error in run :", e , Fore.RESET)
                
    def generate_accounts(self, accountsNumber : int = 10) -> None:
        for i in range(accountsNumber):
            threading.Thread(target=self.run).start()

print(STEELSERIES(None).generate_accounts(10))