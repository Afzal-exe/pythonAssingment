from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import pandas as pd
URL = "https://www.amazon.in/s?k=bags&ref=sr_pg_1"
HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

def get_page_data(URL, HEADERS):
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    linksList = []
    nameList = []
    priceList = []
    ratingList = []
    part1 = {}

    links = soup.find_all("a", attrs={'class': 'a-size-base a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal'})
    prices = soup.find_all("span", attrs={'class': 'a-price-whole'})
    names = soup.find_all("span", attrs={'class': 'a-size-medium a-color-base a-text-normal'})
    ratings = soup.find_all("span", attrs={'class': 'a-size-base puis-normal-weight-text'})

    # getting product urls
    for link in links:
        href = link.get('href')
        if "picassoRedirect" not in href:
            href = urljoin('https://www.amazon.in/', href)
            linksList.append(href)

    # getting names
    for name in names:
        name = str(name).split(">")[1].split("<")[0]
        nameList.append(name)

    # getting Prices
    for price in prices:
        price = str(price).split(">")[1].split("<")[0]
        priceList.append(price)

    # getting ratings
    for rating in ratings:
        rating = str(rating).split(">")[1].split("<")[0]
        ratingList.append(rating)

    part1["product url"] = linksList
    part1["Name"] = nameList
    part1["price"] = priceList
    part1["rating"] = ratingList

    return part1

part1 = get_page_data(URL, HEADERS)
final_data = []
for i in range(21):
    dict = {}
    dict["Name"] = part1["Name"][i]
    dict["price"] = part1["price"][i]
    dict["product url"] = part1["product url"][i]
    dict["rating"] = part1["rating"][i]
    final_data.append(dict)

df = pd.DataFrame(final_data)
df.to_csv("part1Out.csv")







