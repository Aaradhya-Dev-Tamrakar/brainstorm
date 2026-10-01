from bs4 import BeautifulSoup
import json
import re

with open(r'F:\AaradhyaDT\AaradhyaDT.github.io\projects.html', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

cards = soup.find_all('details', class_='project-card')
projects = []
for c in cards:
    pid = c.get('id', 'N/A')
    summary = c.find('summary')
    title_el = summary.find('h3', class_='project-title') if summary else None
    title = title_el.get_text(strip=True) if title_el else ''
    date_el = summary.find('span', class_='project-date') if summary else None
    date_str = date_el.get_text(strip=True) if date_el else ''
    repo = c.get('data-evidence-repo', '')
    category = c.get('data-category', '')
    
    # Check payload link id or links
    payload_btn = c.find(attrs={'data-payload-link-id': True})
    payload_id = payload_btn.get('data-payload-link-id') if payload_btn else ''
    
    # Check tags
    tags = [t.get_text(strip=True) for t in c.find_all('span', class_='tag')]
    
    # bullets
    bullets = [li.get_text(strip=True) for li in c.find_all('li')]
    
    # Slug logic
    if payload_id:
        slug = payload_id.replace('proj-', '')
    elif repo:
        slug = repo.split('/')[-1].lower()
    else:
        # derive from title
        clean = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        slug = re.sub(r'[\s_]+', '-', clean).strip('-')

    projects.append({
        'id': pid,
        'slug': slug,
        'title': title,
        'date': date_str,
        'category': category,
        'repo': repo,
        'payload_id': payload_id,
        'tags': tags,
        'bullets': bullets
    })

with open('research/portfolio_39_projects.json', 'w', encoding='utf-8') as out:
    json.dump(projects, out, indent=2)

print(f"Exported {len(projects)} projects to research/portfolio_39_projects.json")
