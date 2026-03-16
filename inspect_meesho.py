from bs4 import BeautifulSoup
import sys

with open("meesho_debug.html", "r", encoding="utf-8") as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

# Try finding product cards
print("Trying different selectors:")
print(f"div[data-id]: {len(soup.find_all('div', attrs={'data-id': True}))}")
print(f"a[href*=-p-]: {len(soup.find_all('a', href=lambda h: h and '-p-' in h))}")
print(f"div class*=product: {len(soup.find_all('div', class_=lambda c: c and any('product' in x.lower() for x in c)))}")
print(f"div class*=card: {len(soup.find_all('div', class_=lambda c: c and any('card' in x.lower() for x in c)))}")

# Look for unique patterns in page
all_divs = soup.find_all('div', class_=True)
class_freq = {}
for d in all_divs:
    for cls in d.get('class', []):
        class_freq[cls] = class_freq.get(cls, 0) + 1

# Classes appearing 10-50 times are likely product containers or repeated elements
candidates = [(k, v) for k, v in class_freq.items() if 10 <= v <= 50]
candidates.sort(key=lambda x: -x[1])
print("\nFrequent div classes (10-50 occurrences) - likely product grid containers:")
for cls, cnt in candidates[:20]:
    sample = soup.find('div', class_=cls)
    txt = sample.text.strip()[:80].replace('\n', ' ') if sample else ""
    print(f"  .{cls} ({cnt}x): {repr(txt)}")
