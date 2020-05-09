import requests
from bs4 import BeautifulSoup
import urllib.request
import nltk
import re
import pandas as pd


# In[25]:


# query = "Budweiser"
def get_url(query):
    page = requests.get("https://www.google.com/search?q="+query+"+alcohol+wikipedia&oq="+query+"+alcohol+wikiped&aqs=chrome.1.69i57j33.11038j1j7&sourceid=chrome&ie=UTF-8")
    soup = BeautifulSoup(page.content)
    urlstr=""
    for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        url = re.split(":(?=http)",link["href"].replace("/url?q=",""))
        urlstr = ' '.join(map(str, url)) 
        urlstr = urlstr.split('&')[0]
        break
    return urlstr


# In[26]:


def list_to_string(s):  
    str1 = " " 
    return (str1.join(s)) 


# In[27]:


def open_url(urlstr):
    page = requests.get(urlstr)
    soup = BeautifulSoup(page.content)

    info= ""
    whitelist = [
      'p','b','a'
    ]

    text_elements = [t for t in soup.find_all(text=True) if t.parent.name in whitelist]

    y=list_to_string(text_elements)
#     print(y)
    return y


# In[28]:


def search(word, sentences):
       return [i for i in sentences if re.search(r'\b%s\b' % word, i)]


# In[29]:


def get_content(y):
    s = re.split(r'[.?!:]+', y)

    a=search('is a', s)
    a+=search('is an ', s)

    content = list_to_string(a)
    return content


# In[37]:


def check_name(query):

    type_list = ['vodka','gin','baijiu','tequila','rum','whisky','brandy','singani','soju','beer','wine','cider']
    query = query.lower()
    flag = 0
    for item in type_list:
        if(query.find(item)!= -1):
            flag = 1
            break
    if flag == 1:
        return item
    else:
        return ""


def get_type(content): 
    type_list = ['vodka','gin','baijiu','tequila','rum','whisky','brandy','singani','soju','beer','wine','cider','scotch','whiskey','scotch whisky','scotch whiskey']
    content_lower = content.lower()
    al_type =""
    for item in type_list:
        if(content_lower.find(item)!= -1):
            al_type = item
    
    return al_type


def get_manu_content_origin(query,al_type,flag):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    switcher = {1: "https://www.google.com/search?biw=1280&bih=610&ei=e8RIXt7HCOK1mgfXy5PwBw&q="+query+al_type+"+manufacturer&oq="+query+al_type+"+manufacturer&gs_l=psy-ab.3..0i71l8.4032.4032..4220...0.2..0.0.0.......0....1..gws-wiz.pkv0d6RvK9Q&ved=0ahUKEwie8b_AndXnAhXimuYKHdflBH4Q4dUDCAs&uact=5",
                2: "https://www.google.com/search?safe=active&sxsrf=ALeKk01tNMV7-s3HnEgklgrrDXTbsTqEOw%3A1585549593397&ei=GZGBXrzqF9qF4-EPq665uAs&q="+query+"+alcohol+content&oq="+query+"+alcohol+content&gs_lcp=CgZwc3ktYWIQAzoECAAQRzoECAAQDToICAAQCBANEB46BQgAEM0CUJxNWIddYNhfaABwA3gAgAGqAYgBuwiSAQMwLjeYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwj82qbCyMHoAhXawjgGHStXDrcQ4dUDCAs&uact=5",
                3: "https://www.google.com/search?safe=active&sxsrf=ALeKk00R9wu9J46c_mWtdLkp5DiNzB4JJw%3A1585556387669&ei=o6uBXtGuKPSZ4-EPqLeg8A0&q="+query+"+alcohol+country+of+origin&oq="+query+"+alcohol+country+of+origin&gs_lcp=CgZwc3ktYWIQAzoECAAQRzoECAAQDVC0S1jDXmDPYGgAcAN4AIABtgGIAf8NkgEEMC4xM5gBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwiRjIjq4cHoAhX0zDgGHagbCN4Q4dUDCAs&uact=5",
               }
    url = switcher.get(flag)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        result = soup.find('div', class_='Z0LcW AZCkJd')
        if(result == None):
            result = soup.find('div', class_='Z0LcW')
            return (result.text)
        else: 
            return (result.text)
    except:
        return ""

def alternate_content(query,al_type):
    import re
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    url = "https://www.google.com/search?safe=active&sxsrf=ALeKk01dKnc0w3NGQk5NpduWqxhNipKXnA%3A1588929288430&ei=CCO1XoH2GZmL4-EP7fSEiA0&q="+query+al_type+"alcohol+percentage&oq="+query+al_type+"alco&gs_lcp=CgZwc3ktYWIQAxgAMggIIRAWEB0QHjIICCEQFhAdEB4yCAghEBYQHRAeOgQIIxAnOgYIABAWEB5QhrgBWOzFAWDn1AFoAHAAeACAAbgBiAGFB5IBAzAuNpgBAKABAaoBB2d3cy13aXo&sclient=psy-ab"
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    
    data = []
    for line in soup.findAll('span', attrs={'class': 'st'}):
        data.append(line.text)
    words = []
    for lines in data:
        words+= lines.split()

    # print(words)
    abv = ""
    index = 0
    try:
        index = words.index("percent")
    except:
        return abv
    for i in range(index-2,index):
        words[i] = words[i].replace("(","")
        words[i] = words[i].replace(")","")
        
        if(words[i].isdigit()):
            abv = words[i]
            break
    return abv
# In[46]:
def check_none(query):
    if(query == None):
        return True

def driver1(query):
    urlstr = get_url(query)
    y = open_url(urlstr)
    content = get_content(y)
    # print("content ",content)
    alcohol_type =""
    manufacturer = ""
    origin = ""
    alco_content = ""

    alco_type = check_name(query)
    if(len(alco_type) == 0):
        alcohol_type = get_type(content)
    else:
        alcohol_type = alco_type
    # print("Alcohol type: "+alcohol_type)
    manufacturer = get_manu_content_origin(query,alcohol_type,1)

    # print("Manufacturer: "+manufacturer)
    alco_content = get_manu_content_origin(query,alcohol_type,2)
    # print("Alcohol content:"+alco_content)
    if(len(alco_content) == 0):
        alco_content = alternate_content(query,alcohol_type)
    
    origin = get_manu_content_origin(query,alcohol_type,3)
    # print("Origin: "+origin)

    params = []
    params.append(query.lower().capitalize())
    params.append(alcohol_type.lower().capitalize())
    params.append(manufacturer.lower().capitalize())
    params.append(origin.lower().capitalize())
    params.append(alco_content.lower().capitalize())

    
    return (params)

def driver(query,options,altype):
    print(options)
    option_list = []
    urlstr = get_url(query)
    y = open_url(urlstr)
    content = get_content(y)
    alcohol_type =""
    manufacturer = ""
    origin = ""
    alco_content = ""
    alco_type = check_name(query)
    if(len(alco_type) == 0):
        alcohol_type = get_type(content)
    else:
        alcohol_type = alco_type
    if len(alcohol_type) == 0 and len(altype)!=0:
        alcohol_type = altype
    print("al tye",alcohol_type)
    if(1 in options):
        option_list.append(alcohol_type.lower().capitalize())
            
    if(2 in options):
        manufacturer = get_manu_content_origin(query,alcohol_type,1)
        option_list.append(manufacturer.lower().capitalize())
    
    if(3 in options):
        origin = get_manu_content_origin(query,alcohol_type,3)
        option_list.append(origin.lower().capitalize())
    
    if(4 in options):
        alco_content = get_manu_content_origin(query,alcohol_type,2)
        if(len(alco_content) == 0):
            alco_content = alternate_content(query,alcohol_type)
        option_list.append(alco_content.lower().capitalize())
    
    return option_list

print(driver("Bacardi",[2,4],"Bacardi rum"))