import os
def install():
    # Install all from requirements.txt
    os.system("pip install -r requirements.txt")

install()

from encodings.utf_8 import encode
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from bs4 import BeautifulSoup

def fixTitle(tit: str) -> str:
    """Remove aphostrophes and replace spaces with dashes, lower case the return value"""
    tit = tit.replace(" ", "-")
    tit = tit.replace("'", "")
    return tit.lower()

def getTotalChapters(title: str) -> BeautifulSoup:
    """Fetch LightNovel's (title) number of chapters"""
    title = fixTitle(title)

    # Get to the website
    browser.get("https://www.lightnovelpub.com/novel/{0}".format(title))
    soup = BeautifulSoup(browser.page_source, features="html.parser")

    # Narrow down the results
    results = soup.find("div", {"class": "header-stats"})

    # Find the Chapters number
    for x in results:
        if "Chapters" in str(x):
            chapters = (str(x.text).split())[0]
    return soup, chapters

def findFirstChapter(soup: BeautifulSoup, tit: str, totalChapters: str):
    chaptersURLs = []
    results = soup.find_all("a", {"id": "readchapterbtn"})
    for x in results:
        if "Chapter" in str(x.text):
            url = str(x.get("href"))
    
    # String operations to find the last unconstant part
    start = url.find(fixTitle(tit))
    start = url[start:].find("-chapter-") + start
    for x in range(0, int(totalChapters)):
        chaptersURLs.append(url.replace("-chapter-1", "-chapter-" + str(x + 1)))
    return chaptersURLs

def FetchAll(tit: str, urls: list):
    x = "https://www.lightnovelpub.com" + urls[0]
    for n in range(0, len(urls)):
        if x not in done:
            browser.get(x)
            sourceSouped = BeautifulSoup(browser.page_source, features="html.parser")
            try:
                rawText = ""
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/main/article/section[1]/div[3]")))
                for x in sourceSouped.find_all("div", {"id": "chapter-container"}):
                    for y in x.find_all("p"):
                        rawText = rawText + y.text + "\n\n"
                        done.append(x)
                for y in sourceSouped.find_all("span", {"class":"chapter-title"}):
                    if "Chapter" in y.text:
                        rawText = y.text + "\n" + rawText
                        print("Progress: {0}/{1}".format(n, len(urls)))
                        break
                x = prepare4PDF(rawText, "CHAPTER_" + str(n + 1))
            except Exception as e:
                print(e)
                FetchAll(tit, urls)

def prepare4PDF(raw: str, chapterText):
    try:
        os.mkdir(os.getcwd() + "\\" + title)
    except:
        pass
    with open(os.getcwd() + "\\" + title + "\\" + chapterText + ".txt", "wb") as f:
        f.write(raw.encode())
        return str(browser.find_element_by_xpath("/html/body/main/article/section[1]/div[4]/a[3]").get_attribute("href"))

def createAIO():
    files = len(os.listdir(os.getcwd() + "\\" + title))
    AIO = open(os.getcwd() + "\\" + title +".txt", "a", encoding="utf-8")
    for file in range(1, files + 1):
        with open(os.getcwd() + "\\" + title + "\\CHAPTER_" + str(file) + ".txt", "r", encoding="utf-8") as f:
            AIO.write(f.read())

if __name__ == "__main__":
    install()
    # Instantiate the Chrome Webdriver
    browser = uc.Chrome(executable_path="chromedriver.exe")
    title = "im-a-spider-so-what-lnw-03052141"
    soup, chapters = getTotalChapters(title)
    URLs = findFirstChapter(soup, title, chapters)
    done = []
    FetchAll(title, URLs)
    createAIO()