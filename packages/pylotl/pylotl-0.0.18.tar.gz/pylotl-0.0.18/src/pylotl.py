import datetime
import json
import os
import re
import requests
import threading
import time
import urllib.parse
import warnings
from bs4 import BeautifulSoup
from clear import clear
from flask import *

app = Flask(__name__)

fake_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
                "UPGRADE-INSECURE-REQUESTS": "1"}

my_session = requests.Session()

def automatic_index():
    yesterday = datetime.date.today()
    while True:
        time.sleep(60)
        today = datetime.date.today()
        if today != yesterday:
            print("Starting automatic indexing!")
            index()
            print("Automatic indexing done!")

        yesterday = datetime.date.today()
        
def crawl(website):
    website = website.rstrip("/")
    warnings.filterwarnings("ignore")
 
    banned = []
    visited = [website]

    for visit_now in range(10000):
        try:
            visited = list(dict.fromkeys(visited[:]))
            time.sleep(1)

            if ".7z" not in visited[visit_now] and ".gz" not in visited[visit_now] and ".iso" not in visited[visit_now] and ".tar" not in visited[visit_now] and ".zip" not in visited[visit_now]:
                my_request = my_session.get(visited[visit_now], verify = False, headers = fake_headers, timeout = 10, stream = True)
                data = my_request.text
                if len(data) < 100000000:
                    links = []
                   
                    soup = BeautifulSoup(data, "html.parser")

                    try:
                        new_links = soup.find_all("a")
                        for link in new_links:
                            if link.get("href") is not None:
                                links.append(link.get("href"))

                    except:
                        pass

                    try:
                        soup.findAll("img")
                        images = soup.find_all("img")
                        for image in images:
                            if image["src"] is not None:
                                links.append(image["src"])

                    except:
                        pass

                    try:
                        new_links = soup.find_all("link")
                        for link in new_links:
                            if link.get("href") is not None:
                                links.append(link.get("href"))
                           
                            if link.get("imagesrcset") is not None:
                                for i in link.get("imagesrcset").split(","):
                                    links.append(i.strip())

                    except:
                        pass
                   
                    links = list(dict.fromkeys(links[:]))
                   
                    for path in links:
                        if re.search("^[a-zA-Z0-9]", path.lstrip("/")) and not re.search("script|data:", path):
                            if path.startswith("/"):
                                visited.append(website + path)

                            elif path.startswith("http://") or path.startswith("https://"):
                                if urllib.parse.urlparse(website).netloc in urllib.parse.urlparse(path).netloc:
                                    visited.append(path)

                            else:
                                visited.append(website + "/" + path)

                    scripts = soup.find_all("script")
                    for script in scripts:
                        if script.get("src") is not None:
                            path = script.get("src")
                            if re.search("^[a-zA-Z0-9]", path.lstrip("/")) and not re.search("script|data:", path):
                                if path.startswith("/"):
                                    visited.append(website + path)
         
                                elif path.startswith("http://") or path.startswith("https://") or path.startswith("ftp://"):
                                    visited.append(path)
         
                                else:
                                    visited.append(website + "/" + path)
 
        except IndexError:
            break
 
        except:
            pass

    with open("links.txt", "a") as file:
        for link in visited:
            if urllib.parse.urlparse(website).netloc in link:
                file.write(f"{link}\n")
                
def index():
    urls = []
    with open("links.txt", "r") as file:
        for line in file:
            new_line = line.rstrip("\n")
            urls.append(new_line.rstrip("/"))

    delay = 1

    hits = {}

    count = -1
    while True:
        try:
            count += 1
            time.sleep(1)
            my_request = my_session.get(urls[count], headers = fake_headers, timeout = 10, stream = True)

            if my_request.status_code == 200 and re.search(r"<\s*html", my_request.text) and len(my_request.text) < 100000000:
                soup = BeautifulSoup(my_request.text, "html.parser")
                [s.extract() for s in soup(["style", "script", "[document]", "head", "title"])]
                readable_text = soup.getText().split("\n")
                new_text = []
                for i in readable_text:
                    i = re.sub(r"\s+", " ", i)
                    if len(i) > 0 and i != " ":
                        new_text.append(i)

                new_text = list(dict.fromkeys(new_text[:]))
                new_text.sort()
                hits.update({urls[count]: new_text})

        except IndexError:
            break

        except:
            pass

    hits = json.dumps(hits, indent = 4, sort_keys = True)
    with open("index.json", "w") as file:
        file.write(hits)

def search(query):
    hits = []
    with open("index.json", "r") as file:
        json_data = json.loads(file.read())

    for key, value in json_data.items():
        for _ in value:
            if re.search(query, _):
                hits.append(key)

    hits = list(dict.fromkeys(hits[:]))
    hits.sort()

    if len(hits) > 0:
        return hits

    else:
        return None

@app.route("/crawl", methods=["GET", "POST"])
def crawl_html():
    if os.path.exists("links.txt"):
        if request.method == "GET":
            html = '''<html>
                      <head>
                      <title>pylotl</title>
                      </head>
                      <body>
                      <form method="POST">
                      <label for="crawl">Crawl:</label><br>
                      <input type="text" id="crawl" name="crawl"><br>
                      <input type="submit" id="GO" name="GO" value="GO">
                      </form>
                      </body>
                      </html>
                    '''
            
            return render_template_string(html)

        if request.method == "POST":
            urls = []
            with open("links.txt", "r") as file:
                for line in file:
                    new_line = line.rstrip("\n")
                    urls.append(new_line.rstrip("/"))

            if request.form["crawl"].rstrip("/") not in urls:
                crawl(request.form["crawl"])
                index()
                html = '''<html>
                          <head>
                          <title>pylotl</title>
                          </head>
                          <body>
                          <form method="POST">
                          <label for="crawl">Crawl:</label><br>
                          <input type="text" id="crawl" name="crawl"><br>
                          <input type="submit" id="GO" name="GO" value="GO">''' + f'<br><strong>Done crawling and indexing {request.form["crawl"]}</strong><br><a href="/search">Search</a></form></body></html>'

            else:
                html = '''<html>
                          <head>
                          <title>pylotl</title>
                          </head>
                          <body>
                          <form method="POST">
                          <label for="crawl">Crawl:</label><br>
                          <input type="text" id="crawl" name="crawl"><br>
                          <input type="submit" id="GO" name="GO" value="GO">
                          </form>
                          <strong>We already have that indexed!</strong>
                          </body>
                          </html>'''

        return  render_template_string(html)

    else:
        crawl("https://www.example.com")
        index()
        html = '''<html>
                      <head>
                      <title>pylotl</title>
                      </head>
                      <body>
                      <strong>We are currently setting up. Please Try Again!</strong>
                      </body>
                      </html>
                    '''

        return  render_template_string(html)

@app.route("/search", methods=["GET", "POST"])
def search_html():
    if os.path.exists("index.json"):
        if request.method == "GET":
            html = '''<html>
                      <head>
                      <title>pylotl</title>
                      </head>
                      <body>
                      <form method="POST">
                      <label for="query">Query:</label><br>
                      <input type="text" id="query" name="query"><br>
                      <input type="submit" id="GO" name="GO" value="GO">
                      </strong><br><a href="/crawl">Crawl</a>
                      </form>
                      </body>
                      </html>
                    '''
            
            return render_template_string(html)

        if request.method == "POST":
            html = '''<html>
                      <head>
                      <title>pylotl</title>
                      </head>
                      <body>
                      <form method="POST">
                      <label for="query">Query:</label><br>
                      <input type="text" id="query" name="query"><br>
                      <input type="submit" id="GO" name="GO" value="GO">
                      </strong><br><a href="/crawl">Crawl</a>
                      </form>
                      <br>
                    '''
            
            query = request.form["query"]
            hits = search(query)
            html += f'<strong>You searched for: {query}</strong><br>'
            if hits is not None:
                for hit in hits:
                    html += f'<a href="{hit}">{hit}</a><br>'

                html += '''</body>
                           </html>
                           '''

            else:
                html += '''No hits found!
                           </body>
                           </html>
                           '''
            
            return render_template_string(html)

    else:
        crawl("https://www.example.com")
        index()
        html = '''<html>
                      <head>
                      <title>pylotl</title>
                      </head>
                      <body>
                      <strong>We are currently setting up. Please Try Again!</strong>
                      </body>
                      </html>
                    '''

        return  render_template_string(html)
        

@app.route("/", methods=["GET"])
def main_html():
    if request.method == "GET":
            html = '''<html>
                      <head>
                      <title>pylotl</title>
                      </head>
                      <body>
                      <a href="/crawl">Crawl</a>
                      <br>
                      <a href="/search">Search</a>
                      </body>
                      </html>
                    '''
            
            return render_template_string(html)

if __name__ == "__main__":
    clear()
    my_thread = threading.Thread(target = automatic_index).start()
    app.run(debug=False, port=5000)
