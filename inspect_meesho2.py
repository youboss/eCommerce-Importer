from bs4 import BeautifulSoup

with open("meesho_debug2.html", "r", encoding="utf-8") as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')
print(f"Total HTML length: {len(content)}")
print(f"Total tags: {len(soup.find_all())}")

# Check all 'a' tags
all_a = soup.find_all('a', href=True)
print(f"\nTotal <a> tags: {len(all_a)}")
for a in all_a[:10]:
    print(f"  href={a['href']!r} text={repr(a.text.strip()[:50])}")

# Get all unique class names
all_classes = set()
for tag in soup.find_all(class_=True):
    for cls in tag.get('class', []):
        all_classes.add(cls)
with open("meesho_classes.txt", "w", encoding="utf-8") as f:
    f.write('\n'.join(sorted(all_classes)))
print(f"\nWritten {len(all_classes)} unique classes to meesho_classes.txt")

# Check page title/body text snippet
body = soup.find('body')
if body:
    print(f"\nBody text snippet (first 500 chars): {repr(body.text.strip()[:500])}")
