from bs4 import BeautifulSoup
import re

def clean_html_description(description):
    result = ""
    for p in description.find_all('p', class_=True):
        result += (p.get_text()+" \n ")
    return result

def extract_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    p_sqr_land = soup.find('span', attrs={'data-aut-id': 'value_p_sqr_land'})
    item_location = soup.find('div', attrs={'data-aut-id': 'itemLocation'})
    item_description_content = soup.find('div', attrs={'data-aut-id': 'itemDescriptionContent'})
    return {"size": p_sqr_land.text, "location": item_location.text, "description": clean_html_description(item_description_content)}

# Function to extract listings from the HTML content
def extract_listings(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Finding 'li' elements with the specified attribute
    listings_li = soup.find_all('li', attrs={'data-aut-category-id': '4827'})

    # Extracting 'a' tags within these 'li' elements that have href starting with '/item'
    listings = []
    for li in listings_li:
        a_tag = li.find('a', href=lambda href: href and href.startswith('/item'))
        if a_tag:
            listings.append(a_tag)

    # Extracting details from the listings
    extracted_listings = []
    for listing in listings:
        # Extracting the URL
        url = listing.get('href')
        full_url = f"https://www.olx.co.id{url}" if url else None

        # Extracting the title
        title = None
        if listing.find('img'):
            title = listing.find('img').get('alt')
        elif listing.text:
            title = listing.text.strip()

        # Extracting the price if available
        price = None
        price_pattern = re.compile(r'Rp\s*\d+[\d.,]*')  # Regex pattern for price in Indonesian format
        if price_pattern.search(str(listing)):
            price = price_pattern.search(str(listing)).group()

        # Adding the extracted details to the list
        extracted_listings.append({'url': full_url, 'title': title, 'price': price})

    return extracted_listings
