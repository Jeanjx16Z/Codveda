# HANDLE DYNAMIC CONTENT
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd


# url = "https://en.wikipedia.org/wiki/Max_Verstappen"

# # Send HTTP request and parse with BeautifulSoup
# response = requests.get(url)
# soup = BeautifulSoup(response.content, "html.parser")

# # Locate the infobox
# infobox = soup.find("table", class_="infobox")

# # Extract desired rows
# data = []
# for row in infobox.find_all("tr"):
#     header = row.find("th")
#     cell = row.find("td")
#     if header and cell:
#         label = header.get_text(" ", strip=True)
#         value = cell.get_text(" ", strip=True)
#         data.append((label, value))

# # Convert to DataFrame and filter for specific fields
# df = pd.DataFrame(data, columns=["Attribute", "Value"])
# fields_to_include = [
#     "Born", "Partner", "Children", "Parents", "Relatives",
#     "Awards", "Nationality", "2025 team(s)", "Car number" ,"Entries", "Championships",
#     "Wins", "Podiums", "Career points", "Pole positions", "Fastest laps"
# ]
# df = df[df["Attribute"].isin(fields_to_include)].reset_index(drop=True)

# # Output the result
# print(df)

# # Optionally save to CSV
# df.to_csv("max_verstappen_info.csv", index=False)
#  HANDLED PAGINATION
import requests
from bs4 import BeautifulSoup
import json

base_url = "https://www.crash.net/id/motogp/news?page={}"
all_articles = []

for page in range(1, 4):
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    articles = soup.find_all("article")
    
    for article in articles:
        link_tag = article.find("a", href=True)
        article_url = "https://www.crash.net" + link_tag["href"] if link_tag else None

        if article_url:
            article_response = requests.get(article_url)
            article_soup = BeautifulSoup(article_response.text, "html.parser")

            # Extract title
            title_tag = article_soup.find("h1")
            title = title_tag.text.strip() if title_tag else "N/A"

            # Extract journalist
            journalist_tag = article_soup.find("a", href=lambda x: x and "/id/about-us/authors/" in x)
            journalist = journalist_tag.text.strip() if journalist_tag else None

            # Extract publication date
            time_tag = article_soup.find("time")
            date = time_tag["datetime"] if time_tag and "datetime" in time_tag.attrs else None

            # Extract article text
            paragraphs = article_soup.find_all("p")
            article_text = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())

            article_data = {
                "title": title,
                "url": article_url,
                "date": date,
                "journalist": journalist,
                "article": article_text
            }

            all_articles.append(article_data)
# print(article_data)
# Save to JSON
with open("motogp_articles_full.json", "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)

print("Scraping complete. Data saved to motogp_articles_full.json")


