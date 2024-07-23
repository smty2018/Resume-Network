import os
import requests
from pprint import pprint
from collections import defaultdict
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

username = "smty2018"

token = "github_token"

url_git = f"https://api.github.com/users/{username}/repos"

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

lst=[]


response = requests.get(url_git, headers=headers)

if response.status_code == 200:

    repos = response.json()

    overall_stats = defaultdict(int)
    total_bytes = 0

    for repo in repos:


        lang_stats = defaultdict(int)

        bytes_total = 0
        
        lang_url = f"https://api.github.com/repos/{username}/{repo['name']}/languages"
        lang_response = requests.get(lang_url, headers=headers)
        
        if lang_response.status_code == 200:

            languages = lang_response.json()

            for lang, bytes_code in languages.items():
                lang_stats[lang] += bytes_code
                bytes_total += bytes_code
            
            for lang, bytes_code in lang_stats.items():
                overall_stats[lang] += bytes_code
                total_bytes += bytes_code
    
    for lang, bytes_code in overall_stats.items():

        percentage = (bytes_code / total_bytes) * 100
        lst.append({lang: f"{percentage:.2f}%"})



else:
    print(f"Status Code: {response.status_code}")
lst=sorted(lst, key=lambda x: float(list(x.values())[0][:-1]), reverse=True)
lst=lst[0:6]
skill_bar=json.dumps(lst)

with open('./templatesskills.json', 'w') as f:
    json.dump(lst, f, ensure_ascii=False, indent=4)

print(lst)