import os
import requests
from pprint import pprint
from collections import defaultdict
import json
import sys
from base64 import b64decode

sys.stdout.reconfigure(encoding='utf-8')

username = "smty2018"

token = "github_token"

url = f"https://api.github.com/users/{username}/repos"

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

proj_list=[]

response = requests.get(url, headers=headers)

if response.status_code == 200:
    repos = response.json()
    # pprint(repos)


    for repo in repos:
        if not repo['fork']: 
            
            # proj_list.append({})
        
            # proj_list.append({})
            # proj_list.append({})

            
            # print(f"Stars: {repo['stargazers_count']}")
            # print(f"URL: {repo['html_url']}")

           
            readme_url = f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/readme"
            readme_response = requests.get(readme_url, headers=headers)

            if readme_response.status_code == 200:
                readme = readme_response.json()
                readme_content = b64decode(readme['content']).decode('utf-8')

                proj_list.append({"name":repo['name'],"url":repo['html_url'],"stars":repo['stargazers_count'],"des":repo["description"],"readme":readme_content})
                # proj_list.append({})
                # print(f"{readme_content}")
            else:
                print(f" Status Code: {readme_response.status_code},{repo['name']}")
                proj_list.append({"name":repo['name'],"url":repo['html_url'],"stars":repo['stargazers_count'],"des":repo["description"],"readme":None})

           

   
   
else:
    print(f" Status Code: {response.status_code}")

proj_list_sorted = sorted(proj_list, key=lambda x: x['stars'], reverse=True)
proj_list_sorted=proj_list_sorted[0:2]

# pprint(proj_list)