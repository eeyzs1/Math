from playwright.sync_api import sync_playwright
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json
root=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
 def handle_starttag(self,t,attrs):
  for key,v in attrs:
   if key in ('href','src') and v and not urlparse(v).scheme and not v.startswith('#'):
    target=(self.file.parent/unquote(v.split('#')[0])).resolve()
    assert target.exists(),(self.file,v)
for f in root.rglob('*.html'):
 p=Links();p.file=f;p.feed(f.read_text(encoding='utf-8'))
with sync_playwright() as p:
 try: # 优先使用 Playwright 自带/已安装的浏览器，失败时回退本机 Chrome。
  browser=p.chromium.launch(headless=True)
 except Exception:
  browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 page=browser.new_page(viewport={'width':1280,'height':900});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((root/'index.html').as_uri());page.screenshot(path=str(root/'assets/home-preview.png'),full_page=True)
 page.goto((root/'reference/labs.html').as_uri());page.screenshot(path=str(root/'assets/labs-preview.png'),full_page=True)
 for id,value in [('h','0.01'),('a','0'),('a','-2'),('p','0'),('p','1'),('step','1.2'),('n','1'),('n','50'),('x0','0'),('x0','-2.5'),('x0','2.5')]:
  page.locator('#'+id).evaluate('(el,v)=>{el.value=v;el.dispatchEvent(new Event("input"))}',value)
  assert 'NaN' not in page.locator('main').inner_text()
 assert '1.000000' in page.locator('#p-out').inner_text()
 page.goto((root/'06-analysis/lessons/01.html').as_uri());page.locator('summary').click();assert page.locator('details').get_attribute('open') is not None
 page.set_viewport_size({'width':390,'height':844});page.goto((root/'reference/labs.html').as_uri())
 assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
 page.goto((root/'reference/classification.html').as_uri())
 audit=json.loads((root/'assets/classification-audit.json').read_text(encoding='utf-8'))
 assert page.locator('.major').count()==audit['major']
 assert page.locator('.entry').count()==audit['subject_leaf']+audit['general_leaf']
 page.locator('#search').fill('11A05')
 page.wait_for_function("document.querySelectorAll('.entry:not([hidden])').length===1")
 assert page.locator('[id="11A05"]').is_visible()
 page.locator('#search').fill('zzzz-no-match')
 page.wait_for_function("document.querySelectorAll('.major:not([hidden])').length===0")
 page.locator('#search').fill('')
 page.wait_for_function("document.querySelectorAll('.major:not([hidden])').length===63")
 assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
 page.set_viewport_size({'width':1280,'height':900})
 page.screenshot(path=str(root/'assets/classification-preview.png'))
 page.goto((root/'reference/classification.html').as_uri()+'#60G44')
 assert page.locator('[id="60G44"]').is_visible()
 for folder in root.glob('[0-9][0-9]-*'):
  page.goto((folder/'curriculum.html').as_uri())
  assert page.locator('article').count()==5
 page.goto((root/'reference/concepts.html').as_uri())
 concepts=json.loads((root/'assets/concepts.json').read_text(encoding='utf-8'))
 assert page.locator('[data-module]').count()==len(concepts)
 assert page.locator('.concept input').count()==sum(len(c['items']) for v in concepts.values() for c in v)
 page.on('dialog',lambda d:d.accept())
 page.locator('.concept input').first.check()
 assert page.locator('#total').inner_text().startswith('总进度：1 /')
 page.locator('#reset').click()
 assert page.locator('#total').inner_text().startswith('总进度：0 /')
 assert not errors,errors
 browser.close()
print('PASS: local links, browser JS, sliders including endpoints, answer reveal, mobile overflow, concept checklist')
