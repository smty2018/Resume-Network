import requests
from pprint import pprint
import json
import sys
import openai
sys.stdout.reconfigure(encoding='utf-8')

api_key = 'linkedinscraper_api_key'
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
params = {
    'linkedin_profile_url': 'https://www.linkedin.com/in/sheetali-maity-1a0724210/',
    'extra': 'include',
    'github_profile_id': 'include',
    'facebook_profile_id': 'exclude',
    'twitter_profile_id': 'include',
    'personal_contact_number': 'exclude',
    'personal_email': 'include',
    'inferred_salary': 'exclude',
    'skills': 'include',
    'use_cache': 'if-present',
    'fallback_to_cache': 'on-error',
}
response = requests.get(api_endpoint,
                        params=params,
                        headers=headers)

res=response.content.decode('utf-8')
json_data = json.loads(res) 
pprint(json_data)



#profile_pic_url

#headline
#country full name ,city,state

name=json_data['full_name']
pic_url=json_data['profile_pic_url']
exp=json_data['experiences']

sorted_exp = sorted(exp, key=lambda x: (x['starts_at']['year'], x['starts_at']['month'], x['starts_at']['day']), reverse=True)

# for item in sorted_data:
#     print(f"Company: {item['company']}, Title: {item['title']}, Start Date: {item['starts_at']['day']}/{item['starts_at']['month']}/{item['starts_at']['year']}")

occupation=sorted_exp[0]['title']
occupation=json_data['occupation']

# print(occupation)

cert_list=json_data['certifications']


#summary
#gpt from headline + description
import google.generativeai as genai

genai.configure(api_key="gemini_api")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

data_to_summarize = json_data["headline"]+json_data["description"]


summary = model.summarize(data=data_to_summarize)

print(summary)








education_list=json_data['education'][0]
deg_name=education_list["degree_name"]
field=education_list["field_of_study"]
school=education_list["school"]
school_logo=education_list["logo_url"]
from_date=education_list["starts_at"]
to_date=education_list["ends_at"]
school_url=education_list["school_linkedin_profile_url"]

education_data = {
    'degree_name': deg_name,
    'field_of_study': field,
    'school': school,
    'school_logo': school_logo,
    'from_date': from_date,
    'to_date': to_date,
    'school_url': school_url
}

location=json_data['city']+json_data['state']+json_data['country']

##SKILL BAR

import os
import requests
from pprint import pprint
from collections import defaultdict
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

username = "smty2018"

git_token = ""

url_git = f"https://api.github.com/users/{username}/repos"

headers = {
    'Authorization': f'token {git_token}',
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
        lst.append({lang: int(percentage)})




else:
    print(f"Status Code: {response.status_code}")
lst_sorted = sorted(lst, key=lambda x: x[next(iter(x))], reverse=True)
lst_sorted=lst_sorted[0:6]


# with open('./templatesskills.json', 'w') as f:
#     json.dump(lst, f, ensure_ascii=False, indent=4)

print(lst)


#PROJECT
import os
import requests
from pprint import pprint
from collections import defaultdict
import json
import sys
from base64 import b64decode

sys.stdout.reconfigure(encoding='utf-8')

username = "smty2018"

token = ""

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




#Flask Server


from flask import Flask, render_template

app = Flask(__name__)

@app.template_filter('colorize')
def colorize(index):
    colors = ["#e74c3c", "#8e44ad", "#3498db", "#2ecc71", "#f1c40f", "#e67e22"]
    return colors[index % len(colors)]

@app.route('/input')
def func():
   
    return render_template('index.html')

@app.route('/')
def index():
    #mone kore change them to vars
    username = name  
    profile_pic_url=pic_url
    occ=occupation
    # sk1=skill_bar[0][]
    return render_template('resume_template1.html', username=username,profile_pic_url=profile_pic_url,occupation=occ,proj_list=proj_list_sorted,skills=lst_sorted,education=education_data)






if __name__ == "__main__":
    app.run(debug=True)

