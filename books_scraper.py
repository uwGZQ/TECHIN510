import requests
from bs4 import BeautifulSoup

base_url = 'http://books.toscrape.com/'

# Mapping textual ratings to numeric values
ratings_mapping = {
    "Zero": 0,  
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

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
    description_text = clean_text(description_text)
    return description_text

def clean_price(price):
    # Replace unwanted characters and strip any leading/trailing whitespace
    cleaned_price = price.replace('Â', '').strip()
    # Remove the '£' sign and convert the price to a float
    cleaned_price = float(cleaned_price.strip('£'))
    return cleaned_price

def clean_text(text):
    import re
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    # Remove any control characters
    text = re.sub(r'[\x00-\x1F\x7F]+', '', text)
    return text

# Function to scrape books from a single page
def scrape_books_from_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    books = []
    # Find all book entries on the page
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        raw_price = book.find('p', class_='price_color').text.strip()
        price = clean_price(raw_price)
        rating = book.find('p', class_='star-rating')['class'][1]  # Assumes class like 'star-rating Three'
        rating = ratings_mapping[rating]
        partial_url = book.h3.a['href']

        full_url = base_url + 'catalogue/' + partial_url.split('/', 2)[2]

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
    page_url = 'http://books.toscrape.com/catalogue/category/books_1/page-1.html'
    response = requests.get(page_url)
    books_on_page = scrape_books_from_page(response.text)

    for book in books_on_page:
        print(book)
