from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("flipkart_debug.html", "r", encoding="utf-8") as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')
items = soup.find_all('div', attrs={'data-id': True})
print(f"Found {len(items)} items with data-id")

if items:
    item = items[0]
    lines = []
    lines.append("\n--- ALL ELEMENTS with class in first item ---")
    for tag in item.find_all(['div', 'a', 'p', 'span', 'img']):
        cls = tag.get('class')
        if cls:
            txt = tag.text.strip()[:80].replace('\n',' ')
            lines.append(f"<{tag.name}> class={cls} text={repr(txt)}")
    
    with open("flipkart_inspect.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(lines))
    print("Written to flipkart_inspect.txt")
