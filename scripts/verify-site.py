from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import re
root=Path(__file__).resolve().parents[1] / 'dist'
class Page(HTMLParser):
 def __init__(self): super().__init__(); self.refs=[];self.ids=set();self.text=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for attr in ['href','src']:
   if attr in a:self.refs.append(a[attr])
 def handle_data(self,data):self.text.append(data)
parsed={}
for file in root.glob('*.html'):
 p=Page();p.feed(file.read_text());parsed[file]=p
errors=[];refs=0
for file,p in parsed.items():
 for ref in p.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  path=unquote(u.path)
  if path.startswith('/website/'): target=root/path.removeprefix('/website/')
  elif path.startswith('/'):target=root/path.lstrip('/')
  elif not path:target=file
  else:target=file.parent/path
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{file.name}: missing {ref}')
  if u.fragment and target in parsed and u.fragment not in parsed[target].ids:errors.append(f'{file.name}: missing fragment {ref}')
  refs+=1
 text=' '.join(p.text)
 for needle in ['§','**','Voice note','deliberately vague','Pull quote','Hero body','EDIT THIS','__FOOTNOTE__','Links (visible before login','interface only','Sample:','Section headline']:
  if needle in text:errors.append(f'{file.name}: editorial artifact {needle}')
print(f'Checked {len(parsed)} built pages and {refs} local links/assets.')
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print('All link, asset, fragment, and editorial checks passed.')
