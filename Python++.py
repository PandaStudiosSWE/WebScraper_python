import os
import datetime
import requests as r
from colorama import init, Fore
from bs4 import BeautifulSoup

def session_req(a):
    s = r.Session()
    page = s.get(a)
    return page
    
def soupy(b):
    soup = BeautifulSoup(b.content, 'html.parser')
    for element in soup.select('title'):
        result = element.text.split()[0]
        return result
        
def soup_scripts(c, ur):
    js_data = ""
    js_http = ["http", "https"]
    soup = BeautifulSoup(c.content, 'html.parser')
    for i in soup.find_all('script'):
        if 'src' in i.attrs:
            js_data += "\n" + i['src']
            js_name = i['src']
            js_name = js_name.replace("/", "_")
            js_name = js_name.replace(":", "-")
            js_name = js_name.replace("?", "_")
            js_name = js_name.replace("=", "_")
            js_name = js_name.replace(",", "-")
            site = session_req(i['src'])
            if js_http in site:
                with open(f"{myjs}/{js_name}", "w", encoding='utf-8') as f:
                    f.write(site.text)
            else:
                site = session_req(ur+"/"+i['src'])
                with open(f"{myjs}/{js_name}", "w", encoding='utf-8') as f:
                    f.write(site.text)
    return js_data
    
def soup_css(a, b):
    css_data = ""
    css_http = ["http", "https"]
    soup = BeautifulSoup(a.content, 'html.parser')
    for i in soup.find_all('link'):
        if 'href' in i.attrs:
            css_data += "\n" + i['href']
            css_name = i['href']
            css_name = css_name.replace("/", "_")
            css_name = css_name.replace(":", "-")
            css_name = css_name.replace(",", "-")
            css_name = css_name.replace("=", "_")
            css_name = css_name.replace("?", "_")
            site = session_req(i['href'])
            if css_http in site:
                with open(f"{mycss}/{css_name}", "w", encoding='utf-8') as f:
                    f.write(site.text)
            else:
                site2 = session_req(b+i['href'])
                with open(f"{mycss}/{css_name}", "w", encoding='utf-8') as f:
                    f.write(site2.text)
    return css_data

mydir = "Python++_output"
if not os.path.exists(mydir):
    os.makedirs(mydir)

myjs = "js_output" 
if not os.path.exists(myjs):
    os.makedirs(myjs)
    
mycss = "css_output" 
if not os.path.exists(mycss):
    os.makedirs(mycss)

init(convert=True) 
print(f"{Fore.GREEN}[BETA] Welcome to Pandas Web Scraper! [BETA] {Fore.RED} [BETA] Expect Errors [BETA]{Fore.CYAN}\n\n")

choice = int(input("[1] Single URL, [2] List Of URLs: "))

if choice == 1:
    url = input("\nURL: ")
    site = session_req(url)
    final = soupy(site)
    css_site = soup_css(site, url)
    js_site = soup_scripts(site, url)
    with open(f"{mydir}/{final}_HTML_output.html", "w", encoding='utf-8') as f:
        f.write(site.text)
    
elif choice == 2:
    print("\nMake sure that you place a .txt file with the url list in script directory!\n")
    fName = input("\nFile Name, don't include .txt: ")
    with open(f"{fName}.txt", encoding='utf-8') as g:
        lines = g.readlines()
        for i in lines:
            site = session_req(i)
            css_site = soup_css(site, url)
            js_site = soup_scripts(site)
            final = soupy(site)
            with open(f"{mydir}/{final}_HTML_output.html", "w", encoding='utf-8') as f:
                f.write(site.text)
                
print("\n\nDone!\n")
input("Press Enter To Exit")