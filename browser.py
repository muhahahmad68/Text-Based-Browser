import os
import sys
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
# write your code here
args = sys.argv  # works with cmd
dir_name = args[1]

try:
    os.makedirs(f'{dir_name}')  #Check if directory if available 
except FileExistsError:
    print("Directory already available")

my_stack = deque()  # Creating a deque
while True:
    site = input()

    if site.startswith('http'):
        site = site.replace("https://", '')
    file_name = site.rsplit('.', 1)[0]  # Removes the extension e.g .org, .com

    if site == 'exit':
        break

    elif site == 'back':
        my_stack.pop()
        print(my_stack[-1].pop())  # Back takes us back to previous tab, deleting recent tab

    elif '.' not in site:
        if os.path.exists(f'{dir_name}/{file_name}'):
            with open(f'{dir_name}/{file_name}') as f:
                print(f.read())
            my_stack.append(f)
        else:
            print('Error')
            
    else:
        if 'https://' not in site:
            site = 'https://' + site
        web = requests.get(site)
        soup = BeautifulSoup(web.content, 'html.parser')
        ans = soup.find_all(['title', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'p', 'a'])
        for tag in ans:
            if tag.string:
                if tag.name == 'a':
                    r = Fore.BLUE + tag.string  # Paint links blue

                else:
                    r = Style.RESET_ALL + tag.string  # other text remain normal

                with open(f'{dir_name}/{file_name}', 'w') as file:
                    file.write(r)
                my_stack.append(r)
