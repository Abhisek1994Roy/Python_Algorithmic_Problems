import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import json
import unicodedata
import re
import sys
import warnings
import io
if not sys.warnoptions:
    warnings.simplefilter("ignore")

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

#For ignoring SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# url = input('Enter url - ' )
url = "https://www.tripadvisor.in/Hotel_Review-g1162480-d12081701-Reviews-WelcomHotel_Kences_Palm_Beach-Mahabalipuram_Kanchipuram_District_Tamil_Nadu.html"
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

html = soup.prettify("utf-8")
hotel_json = {}

for line in soup.find_all('script',attrs={"type" : "application/ld+json"}):
    details = line.text.strip()
    details = json.loads(details)
    hotel_json["name"] = details["name"]
    hotel_json["url"] = "https://www.tripadvisor.in"+details["url"]
    hotel_json["image"] = details["image"]
    details["priceRange"] = details["priceRange"].replace("₹ ","Rs ")
    details["priceRange"] = details["priceRange"].replace("₹","Rs ")
    print(details["priceRange"])
    hotel_json["priceRange"] = details["priceRange"]
    hotel_json["aggregateRating"]={}
    hotel_json["aggregateRating"]["ratingValue"]=details["aggregateRating"]["ratingValue"]
    hotel_json["aggregateRating"]["reviewCount"]=details["aggregateRating"]["reviewCount"]
    hotel_json["address"]={}
    hotel_json["address"]["Street"]=details["address"]["streetAddress"]
    hotel_json["address"]["Locality"]=details["address"]["addressLocality"]
    hotel_json["address"]["Region"]=details["address"]["addressRegion"]
    hotel_json["address"]["Zip"]=details["address"]["postalCode"]
    hotel_json["address"]["Country"]=details["address"]["addressCountry"]["name"]
    break
hotel_json["reviews"]=[]
for line in soup.find_all('p',attrs={"class" : "partial_entry"}):
    review = line.text.strip()
    if review != "":
        review = line.text.strip()
        if review.endswith("More"):
            review = review[:-4]
        if review.startswith("Dear"):
            continue
        review = review.replace('\r', ' ').replace('\n', ' ')
        review = ' '.join(review.split())
        hotel_json["reviews"].append(review)


with open(hotel_json["name"]+".html", "wb") as file:
    file.write(html)
print("-------------------------------------------------")
with open(hotel_json["name"]+".json", 'w') as outfile:
    json.dump(hotel_json, outfile, indent=4)
print(hotel_json)
