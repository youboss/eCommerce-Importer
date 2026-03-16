import asyncio
from bs4 import BeautifulSoup

def analyze_flipkart():
    with open("flipkart_debug.html", "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    items = soup.find_all('div', attrs={'data-id': True})
    print(f"Flipkart found {len(items)} items using data-id")
    if items:
        for idx, item in enumerate(items[:2]):
            link_node = item.find('a', href=True)
            print(f"Item {idx} link: {link_node['href'] if link_node else 'None'}")
            title_node = item.find('div', class_=lambda c: c and 'KzDlHZ' in c) or item.find('a', class_=lambda c: c and 'WKTcLC' in c) or item.find('div', class_='_4rR01T')
            print(f"Item {idx} title: {title_node.text.strip() if title_node else 'None'}")
            price_node = item.find('div', class_=lambda c: c and 'Nx9bqj' in c) or item.find('div', class_='_30jeq3')
            print(f"Item {idx} price: {price_node.text.strip() if price_node else 'None'}")
            img_node = item.find('img', class_=lambda c: c and 'DByuf4' in c) or item.find('img', class_='_396cs4')
            print(f"Item {idx} image: {img_node['src'] if img_node else 'None'}")
            print("---")

def analyze_meesho():
    with open("meesho_debug.html", "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    
    # New Meesho usually uses 'NewProductCard' or similar variants
    items = soup.find_all('div', class_=lambda c: c and ('ProductList__GridCard' in c or 'NewProductCard' in c))
    print(f"Meesho Strategy 1 found {len(items)} items")
    
    # Fallback to general product listing columns
    if not items:
        # Looking for grid column containers
        items = soup.find_all('a', href=lambda h: h and ('-p-' in h))
        print(f"Meesho Strategy 2 (a tags) found len: {len(items)}")

    if items:
        for idx, item in enumerate(items[:2]):
            link = item['href'] if item.name == 'a' else (item.find('a')['href'] if item.find('a') else 'None')
            print(f"Item {idx} link: {link}")
            
            title_node = item.find('p', class_=lambda c: c and 'Name' in c) or item.find('p')
            print(f"Item {idx} title: {title_node.text.strip() if title_node else 'None'}")
            
            price_node = item.find('h5') or item.find('h4')
            print(f"Item {idx} price: {price_node.text.strip() if price_node else 'None'}")
            
            img_node = item.find('img')
            print(f"Item {idx} image: {img_node['src'] if img_node else 'None'}")
            print("---")

print("--- ANALYZING FLIPKART ---")
analyze_flipkart()
print("\n--- ANALYZING MEESHO ---")
analyze_meesho()
