import requests, time, re, os
from pathlib import Path
from bs4 import BeautifulSoup
from config import DOCX_DIR

HEADERS = {'User-Agent': 'Mozilla/5.0 Chrome/120.0.0.0'}

def clean_name(name):
    return re.sub(r'[\\/*?:"<>|]', '', name).strip()[:60]

def get_docx_url(item_id):
    url = f'https://vbpl.vn/TW/Pages/vbpq-van-ban-goc.aspx?ItemID={item_id}'
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200: return None, None
        soup = BeautifulSoup(r.text, 'html.parser')
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else str(item_id)
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '.docx' in href.lower():
                full = href if href.startswith('http') else 'https://vbpl.vn'+href
                return full, clean_name(title)
        return None, None
    except: return None, None

def download_one(item_id, group_name):
    grp_dir = Path(DOCX_DIR) / clean_name(group_name)
    grp_dir.mkdir(parents=True, exist_ok=True)
    docx_url, title = get_docx_url(item_id)
    if not docx_url: return 'no_docx'
    save_path = grp_dir / f'{item_id}_{title}.docx'
    if save_path.exists(): return 'exists'   # KHONG GHI DE
    try:
        resp = requests.get(docx_url, headers=HEADERS, timeout=30)
        if resp.status_code==200 and len(resp.content)>1000:
            save_path.write_bytes(resp.content)
            return 'downloaded'
        return 'error'
    except: return 'error'

def batch_download(group_name, id_start, id_end, target=300,
                   delay=0.5, progress_cb=None, status_cb=None):
    results = {'downloaded':0, 'exists':0, 'error':0, 'no_docx':0}
    scanned = 0
    for item_id in range(id_start, id_end):
        if results['downloaded'] >= target: break
        status = download_one(item_id, group_name)
        results[status] = results.get(status,0) + 1
        scanned += 1
        if progress_cb: progress_cb(results['downloaded'] / target)
        if status_cb: status_cb(f'ID {item_id}: {status} | Da tai: {results["downloaded"]}/{target}')
        time.sleep(delay)
    return results
