# import os

# import requests
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv

# from db import Database

# load_dotenv()

# BASE_URL = 'https://quotes.toscrape.com/page/{page}/'
# mydb = Database(os.getenv('DATABASE_URL'))
# mydb.create_table()

# # TODO: use argparse to enable truncating table
# mydb.truncate_table()

# quotes = []
# page = 1
# while True:
#     url = BASE_URL.format(page=page)
#     print(f"Scraping {url}")
#     response = requests.get(url)

#     # if outside of valid page range
#     if 'No quotes found!' in response.text:
#         break

#     soup = BeautifulSoup(response.text, 'html.parser')
#     # select all quote divs
#     quote_divs = soup.select('div.quote')

#     for quote_div in quote_divs:
#         # parse individual quote
#         quote = {}
#         quote['content'] = quote_div.select_one('span.text').text
#         quote['author'] = quote_div.select_one('small.author').text
#         #quote['author_link'] = quote_div.select('span')[1].select('a')[0]
#         quote['tags'] = ','.join([tag.text for tag in quote_div.select('a.tag')])
#         #quote['tag_links'] = [tag['href'] for tag in quote_div.select('a.tag')]
        
#         # insert into database
#         mydb.insert_quote(quote)
#         quotes.append(quote)
#     page += 1

# print(quotes)


# Scraper
import requests
from bs4 import BeautifulSoup

# # Base URL for 'Books to Scrape'
# base_url = 'http://books.toscrape.com/'

# Function to fetch and parse a single book page
def fetch_book_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the product description; it is usually contained within a paragraph or div element
    description_block = soup.find('div', id='product_description')
    description_text = ''
    if description_block:
        next_sibling = description_block.find_next_sibling('p')
        description_text = next_sibling.text.strip() if next_sibling else "No description available"
    return description_text

# Function to scrape books from a single page
def scrape_books_from_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    books = []

    # Find all book entries on the page
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text.strip()
        rating = book.find('p', class_='star-rating')['class'][1]  # Assumes class like 'star-rating Three'
        partial_url = book.h3.a['href']

        full_url = base_url + 'catalogue/' + partial_url.split('/', 2)[2]
        # raise Exception('Stop here')

        # Fetch the book description by visiting the book's detail page
        description = fetch_book_details(full_url)
        
        # Append a dictionary with the details
        books.append({
            'title': title,
            'price': price,
            'rating': rating,
            'description': description,
            'url': full_url
        })

    return books

if __name__ == '__main__':
    # Example: scrape a single page (adjust URL as needed)
    page_url = 'http://books.toscrape.com/catalogue/category/books_1/page-1.html'
    response = requests.get(page_url)
    books_on_page = scrape_books_from_page(response.text)

    # Print out the list of books
    for book in books_on_page:
        print(book)
