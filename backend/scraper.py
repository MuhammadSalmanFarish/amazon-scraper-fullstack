from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Firefox(options=options)

def get_url(search_term):
    search_term = search_term.replace(" ", "+")
    return f"https://www.amazon.in/s?k={search_term}"

def extract_record(item):
    title_tag = item.find("h2")
    title = title_tag.text.strip() if title_tag else "No title"

    try:
        price_tag = item.find("span", class_="a-price-whole")
        price = price_tag.text.strip()
    except:
        price = "Not Available"

    link_tag = item.find("a", class_="a-link-normal")
    link = "https://www.amazon.in" + link_tag.get("href", " ") if link_tag else "No link found"

    try:
        rating_tag = item.find("i")
        rating = rating_tag.text.strip() if rating_tag.text.strip()!="" else "No Rating available"
    except:
        rating = "No Ratings available"

    try:
        rating_count_tag = item.find("span", class_="a-size-mini puis-normal-weight-text s-underline-text")
        rating_count = rating_count_tag.text.strip()
    except:
        rating_count = "No ratings available"

    rec = (title, price, link, rating, rating_count)
    return rec

def scrape(product):
    driver = get_driver()
    url = get_url(product)
    driver.get(url)
    time.sleep(10)

    records = []
    next_page_available = True

    while next_page_available:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        results = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in results:
            records.append(extract_record(item))

        next_button = soup.find("a", class_="s-pagination-next")

        if next_button and "s-pagination-disabled" not in next_button.get("class", []):
            next_page_url = "https://www.amazon.in" + next_button["href"]
            driver.get(next_page_url)
            time.sleep(10)
        else:
            next_page_available = False

    driver.quit()
    return records
