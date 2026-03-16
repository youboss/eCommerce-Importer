from bs4 import BeautifulSoup

with open("amazon_debug.html", "r", encoding="utf-8") as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')
items = soup.find_all('div', {'data-component-type': 's-search-result'})
print(f"Found {len(items)} items")

for idx, item in enumerate(items[:2]):
    title_elem = item.find('h2')
    print(f"Item {idx} title elem: {title_elem}")
