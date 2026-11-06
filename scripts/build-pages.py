from pathlib import Path
import re, html, json
ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'content/editorial-copy.md').read_text()
OLD = (ROOT / 'content/layout-source.html').read_text()
def esc(s): return html.escape(str(s), quote=True)
def plain(s):
    s = html.unescape(s).replace('\\[','[').replace('\\] ','] ').replace('\\] ','] ').replace('\\_', '_').replace('\\*','__FOOTNOTE__').replace('\\]',']')
    s = s.replace('*','').replace('__FOOTNOTE__','*')
    return s.strip().strip('*').strip()
def inline(s):
    s = plain(s)
    s = re.sub(r'\s*\(§\d+\)', '', s)
    s = re.sub(r'\s*per §\d+', '', s)
    s = s.replace('See §12.', 'See Correspondence.').replace('See §6.', 'See Corporate Governance.')
    s = re.sub(r'→ §\d+', '', s)
    return esc(s)
def md(s):
    out=[]; paragraph=[]; in_list=False
    def flush():
        if paragraph:
            out.append('<p>'+inline(' '.join(paragraph))+'</p>'); paragraph.clear()
    def close():
        nonlocal in_list
        if in_list: out.append('</ul>'); in_list=False
    for raw in s.strip().splitlines():
        line=raw.strip()
        if not line or line=='---': flush(); close(); continue
        if line.startswith('#'):
            flush(); close(); out.append('<h2>'+inline(re.sub(r'^#+\s*','',line))+'</h2>'); continue
        if re.match(r'^[-\d][.\s]',line):
            flush()
            if not in_list: out.append('<ul>'); in_list=True
            out.append('<li>'+inline(re.sub(r'^(?:- |\d+\. )','',line))+'</li>'); continue
        if line.startswith('>'):
            flush(); close(); out.append('<blockquote>'+inline(line.lstrip('> '))+'</blockquote>'); continue
        if re.match(r'^\*\*[^*]+:\*\*',line):
            flush(); close()
            label, rest = re.match(r'^\*\*([^*]+):\*\*\s*(.*)',line).groups()
            if label == 'Pull quote':
                out.append('<blockquote>'+inline(rest)+'</blockquote>'); continue
            label = re.sub(r'\s*\(deliberately vague about origins\)', '', label)
            if label not in ['Body','Intro','Hero body','Manifesto','Section intro']:
                out.append('<h2>'+inline(label)+'</h2>')
            if rest: paragraph.append(rest)
            continue
        paragraph.append(line)
    flush(); close(); return '\n'.join(out)
sections={}
for m in re.finditer(r'^## (.+)\n([\s\S]*?)(?=^## |\Z)',SOURCE,re.M): sections[m.group(1)]=m.group(2).strip()
def sec(prefix): return next(v for k,v in sections.items() if k.startswith(prefix))
def field(text,label):
    m=re.search(r'\*\*'+re.escape(label)+r':\*\*\s*([\s\S]*?)(?=\n\n\*\*|\n###|\Z)',text)
    return m.group(1).strip().rstrip('-').strip() if m else ''
def link(url,label,cls='section-link micro'): return f'<a class="{cls}" href="{esc(url)}">{esc(label)} <span aria-hidden="true">→</span></a>'
def heading(kicker,title,summary='',image=None):
    cls = 'with-image' if image else ''
    lede = '<p class="lede">'+esc(summary)+'</p>' if summary else ''
    art = '<img src="assets/'+esc(image)+'" alt="'+esc(title)+' — image detail" />' if image else ''
    return '<section class="page-heading '+cls+'"><div><p class="micro">'+esc(kicker)+'</p><h1>'+esc(title)+'</h1>'+lede+'</div>'+art+'</section>'

def prose(body): return '<div class="reading">'+body+'</div>'
nav=[('our-legacy.html','Our Legacy'),('portfolio.html','Portfolio'),('impact.html','Impact'),('foundation.html','Foundation')]
footer_groups={
'Company':[('our-legacy.html','Our Legacy'),('leadership.html','Leadership'),('governance.html','Governance'),('careers.html','Careers'),('where-we-operate.html','Where We Operate'),('employees.html','Employees')],
'Portfolio':[('mind-control-press.html','Mind Control Press'),('special-purpose-vehicles.html','SPV'),('liquidity-events.html','Liquidity Events'),('front-running.html','Front Running'),('just-vitamins.html','“Just” Vitamins'),('ic9000.html','IC9000')],
'Investors':[('investors.html','Investor Portal'),('annual-reports.html','Annual Reports'),('capital-allocation.html','Capital Allocation'),('founders-letter.html','Shareholder Letters')],
'Legal':[('forward-looking-statements.html','Forward-Looking Statements'),('terms.html','Terms'),('privacy.html','Privacy (Ours)'),('cookies.html','Cookie Policy (Non-Negotiable)')],
'Contact':[('contact.html','PO Box 1000')]}
legal=plain(field(sec('16.'),'Legal microcopy')).replace("The world's best global holding company", "The world's primary holding corporation")
header='<header class="site-header"></header>'
footer='<footer class="site-footer"><div class="footer-grid">'+''.join('<div><h2 class="micro">'+title+'</h2>'+''.join(f'<a href="{u}">{l}</a>' for u,l in items)+'</div>' for title,items in footer_groups.items())+'</div><div class="footer-bottom"><p>'+esc(legal)+'</p><a class="system-link" href="operating-system.html">› Access the operating system</a></div></footer>'
pages={}
def page(slug,title,body,kind='',description=None):
    text=re.sub('<[^>]+>',' ',body)
    desc=description or re.sub(r'\s+',' ',html.unescape(text)).strip()[:160]
    pages[slug]=f'<!doctype html>\n<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><meta name="description" content="{esc(desc)}"/><meta name="theme-color" content="#f6f4f0"/><title>{esc(title)} — Legacy Systems</title><link rel="icon" href="/favicon.svg"/><link rel="stylesheet" href="/src/site.css"/></head><body class="{kind}"><a class="skip-link" href="#main">Skip to content</a>{header}<main id="main">{body}</main>{footer}<script type="module" src="/src/site.js"></script></body></html>'
# Source layout CSS is retained, shared, and extended for long-form pages.
css=re.search(r'<style>([\s\S]*?)</style>',OLD).group(1)
css=css.replace("url('assets/hero-architecture.jpg')", "url('/assets/hero-architecture.jpg')")
(ROOT/'src/site.css').write_text(css+'\n'+(ROOT/'content/extensions.css').read_text()+'\n'+(ROOT/'content/experiences.css').read_text())
style_path = ROOT / 'src/site.css'
style_path.write_text('\n'.join(line.rstrip() for line in style_path.read_text().splitlines())+'\n')
# Subsidiaries: full supplied copy, with one detail page each.
port=sec('4.')
entries=re.split(r'\n### ',port)[1:]
slugs=['mind-control-press','special-purpose-vehicles','liquidity-events','front-running','just-vitamins','ic9000']
images=['mind-control-press.jpg','special-purpose-vehicles.jpg','liquidity-events.jpg','front-running.jpg','just-vitamins.jpg','ic1000.jpg']
companies=[]
for entry,slug,img in zip(entries,slugs,images):
    lines=entry.splitlines(); name=plain(lines[0]).replace(' — spv.racing','').replace('"JUST"','“JUST”')
    body='\n'.join(lines[1:]).strip().strip('-').strip()
    category=plain(body.split('\n')[0]); body=body.split('\n',1)[1].strip()
    tagline=plain(field(body,'Tagline'))
    body=re.sub(r'\*\*Tagline:\*\*[\s\S]*','',body).strip().rstrip('-').strip()
    # Correct markup artifacts in the supplied category name.
    category=category.replace('*','')
    company={'slug':slug,'name':name.title() if slug!='ic9000' else 'IC9000','category':category,'image':img,'tagline':tagline,'body':body}
    if slug=='special-purpose-vehicles': company['name']='Special Purpose Vehicles'
    if slug=='just-vitamins': company['name']='“Just” Vitamins'
    companies.append(company)
    page(slug,company['name'],heading('Our businesses / '+category,company['name'],tagline,img)+prose(md(body)+f'<blockquote>{esc(tagline)}</blockquote>'+link('portfolio.html','All businesses')+link('contact.html','Correspondence')))
def cards():
    return '<div class="holdings-grid">'+''.join(f'<article class="holding" data-name="{esc(c["name"])}" data-description="{esc(c["category"])}"><a class="card-image" href="{c["slug"]}.html" aria-label="Explore {esc(c["name"])}"><img src="assets/{c["image"]}" alt="{esc(c["category"])}" width="394" height="284"/></a><h3 class="holding-title"><a href="{c["slug"]}.html">{esc(c["name"])}</a></h3><p class="holding-desc">{esc(c["category"])}</p><a class="holding-link" href="{c["slug"]}.html" aria-label="More about {esc(c["name"])}">→</a></article>' for c in companies)+'</div>'
# Public V2 retains the architecture-led hero, holding grid, and split lower section.
home=sec('1A. PUBLIC HOMEPAGE — V2')
hero_body=field(home,'Hero body')
hero_body = hero_body.replace('The answer? Relentlessly creative discovery, applied patiently,', 'We apply relentlessly creative discovery, patiently,')
hero_paras=[plain(p) for p in hero_body.split('\n\n') if p.strip()]
hero=re.search(r'<section class="hero"[\s\S]*?</section>',OLD).group(0)
hero=hero.replace('id="about"','id="about"')
hero=re.sub(r'<p class="hero-description">[\s\S]*?</p>', '<p class="hero-description">'+esc(plain(field(home,'Hero subhead')))+'</p>',hero)
hero=hero.replace('href="#principles"','href="our-legacy.html"').replace('Our Approach <span','Our Legacy <span')
hero=hero.replace('<!-- EDIT THIS HEADLINE -->','').replace('<!-- EDITABLE HERO IMAGE TEXT: change the words or <br> line breaks below. -->','')
intro='<section class="home-intro"><p class="micro">Discovery. Potential. Adaptation. Continuity.</p><div>'+''.join('<p>'+esc(p)+'</p>' for p in hero_paras)+'</div></section>'
stats='<section class="stats" aria-label="Legacy Systems at a glance">'+''.join(f'<div><strong>{n}</strong><p class="micro">{t}</p></div>' for n,t in [('400M+','people reached daily'),('1 in 3','households served by an LSG company'),('7–10','generation holding period')])+'</section>'
portfolio='<section class="holdings" id="holdings"><div class="section-heading"><h2 class="micro">Selected holdings</h2>'+link('portfolio.html','View all')+'</div>'+cards()+'</section>'
belief=plain(field(home,'"What we believe" block'))
lower='<section class="lower"><div class="letter"><div><p class="micro">A letter from our founders</p><h2>Continuity<br/>is forever.</h2></div><div class="letter-info"><p>To our shareholders, our neighbors, and the many people who did not choose us.</p>'+link('founders-letter.html','Read the letter')+'</div></div><div class="principles"><p class="micro">What we believe</p><p class="belief">'+esc(belief)+'</p></div></section>'
page('index',"The world’s primary holding corporation",hero+intro+stats+portfolio+lower+'<section class="correspondence-strip"><p>We welcome correspondence by mail.</p>'+link('contact.html','Contact')+'</section>','home')
page('portfolio','Our businesses',heading('Portfolio','Our businesses.',plain(field(port,'Section intro')))+ '<section class="holdings portfolio-list">'+cards()+'</section>')
# Long-form corporate pages.
for prefix,slug,kicker in [('3.','our-legacy','Our Legacy'),('6.','governance','Corporate Governance'),('9.','capital-allocation','Capital Allocation'),('10.','leadership','Leadership & Board'),('11.','impact','Impact'),('12.','contact','Correspondence'),('13.','foundation','Foundation'),('14.','careers','Careers'),('15.','where-we-operate','Where We Operate')]:
    text=sec(prefix); title=plain(field(text,'Headline')); text=re.sub(r'^\*\*Headline:\*\*[^\n]*\n*','',text)
    text=text.replace('See §6. It\'s fine.', 'Our governance framework documents our commitment to oversight and continuity.')
    text=text.replace('and is illustrated on the map at right, minus the parts we\'ve asked the mapmaker to leave blank.', '. The parts we have asked the mapmaker to leave blank remain outside this account.')
    text=text.replace('**Legacy Systems** **Office of Correspondence** **PO Box 1000** **\\[Jurisdiction Withheld\\]**','Legacy Systems · Office of Correspondence · PO Box 1000 · [Jurisdiction Withheld]')
    text=text.replace('*comprehensive* .', '*comprehensive*.')
    text=text.replace('Corporate Governance (see attached, unsigned)','Corporate Governance')
    content=md(text)
    if slug=='careers': content += '<div class="action-row">'+link('legacy-match.html','Begin LegacyMatch™')+'</div>'
    if slug=='impact': content += '<div class="action-row">'+link('foundation.html','The Foundation')+link('governance.html','Corporate Governance')+'</div>'
    if slug=='contact': content=content.replace('→ Contact','')
    page(slug,kicker,heading(kicker,title)+prose(content), 'contact-page' if slug=='contact' else '')
letter=sec('5.').strip().rstrip('-').strip()
page('founders-letter','A Letter from Our Founders',heading('Shareholder letters','A letter from our founders.')+prose(md(letter)))
# Investor portal, status gate, and dedicated white-space-led visual treatment.
invest=sec('1B.')
pathways=[('founders-letter.html','A Letter from Our Founders'),('annual-reports.html','Annual Reports'),('capital-allocation.html','Capital Allocation Philosophy'),('governance.html','Corporate Governance'),('leadership.html','Leadership & Board'),('investor-relations.html','Investor Relations')]
invcontent=heading('Investors','Capital, allocated perfectly, forever.',image='hero-architecture.jpg')+prose(md(field(invest,'Hero body')))+'<section class="pathways">'+''.join(link(u,t,'pathway') for u,t in pathways)+'</section><section class="correspondence-strip"><p>Investor inquiries are accepted by mail.</p>'+link('investor-relations.html','Contact IR')+'</section>'
gate='<section id="investor-gate" class="gate" aria-labelledby="gate-title"><p class="micro">Investor access</p><h1 id="gate-title">Please confirm your status before continuing.</h1><div class="action-row"><button class="button" data-investor-status="accredited">I am an accredited investor</button><button class="button secondary" data-investor-status="intending">I intend to become one</button></div><p class="demo-note">Demonstration only. Your selection is kept in this tab for this visit; it is not submitted.</p></section><div id="investor-content" hidden>'+invcontent+'</div>'
page('investors','Investors',gate,'investor')
ir=sec('7.')
page('investor-relations','Investor Relations',heading('Investor Relations',plain(field(ir,'Headline')))+prose(md(field(ir,'Intro'))+'<h2>We do not pay a dividend.</h2><p>A dividend is capital admitting defeat. We reinvest everything into businesses, or into the acquisition of businesses, or into the structures that hold the businesses that acquire businesses.</p>')+'<section class="pathways">'+''.join(link(u,t,'pathway') for u,t in [('annual-report.html','Annual report — reading edition'),('annual-reports.html','Annual Report Archive'),('capital-allocation.html','Capital Allocation Philosophy'),('founders-letter.html','Shareholder Letters'),('contact.html','Contact IR — by mail')])+'</section>','investor')
report=sec('8.')
forward=report.split('**Sample: Forward-Looking Statements (the fine-print playground):**')[1].split('**Sample: Risk Factors (opening lines):**')[0].strip()
risks=report.split('**Sample: Risk Factors (opening lines):**')[1].strip().rstrip('-').strip()
page('forward-looking-statements','Forward-Looking Statements',heading('Disclosures','Forward-looking statements.')+prose(md(forward)+'<h2>Risk factors</h2>'+md(risks)))
page('annual-reports','Annual Reports',heading('Investor publications','The annual record.')+prose('<p>We report annually, in writing, at length, and with candor calibrated precisely to our legal exposure.</p><h2>Current reading edition</h2><p>The founders’ letter, our businesses, and forward-looking statements.</p>'+link('annual-report.html','Read the report')+'<h2>Archive</h2><p class="availability">Prior-year reports are not available in this edition.</p>'),'investor')
page('annual-report','Annual Report — Reading Edition',heading('Annual report / reading edition','Continuity, in writing.')+prose('<p class="edition-note">Reading edition. Financial statements and historical reports have not been supplied.</p><button class="button secondary" id="print-report">Print / Save as PDF</button><h2>A letter from our founders</h2>'+md(letter)+'<h2>Our businesses</h2>'+''.join('<h3>'+esc(c['name'])+'</h3>'+md(c['body']) for c in companies)+'<h2>Forward-looking statements</h2>'+md(forward)+'<h2>Risk factors</h2>'+md(risks)),'investor report')
# Legal pages use supplied microcopy rather than invented policy claims.
for slug,title,text in [('terms','Terms','Nothing herein is an offer, a guarantee, an admission, or, in most jurisdictions, evidence.'),('privacy','Privacy (Ours)','All rights reserved, retroactively.'),('cookies','Cookie Policy (Non-Negotiable)','Reading this website constitutes acceptance of terms you were not shown.')]:
    body='<p>'+esc(text)+'</p><p>'+esc(legal)+'</p><aside class="edition-note">This is a fictional corporate website. The employee forms and store are browser-only demonstrations. Form contents are not submitted or retained. The investor access selection is stored only for this tab’s session; no tracking cookies are set by this implementation.</aside>'+link('contact.html','Correspondence')
    page(slug,title,heading('Legal',title+'.')+prose(body))
# Employee pages: finite browser-local flows, no credentials, submissions, or payment integrations.
emp=sec('1C.')
landing=emp.split('### Landing')[1].split('### Sign in')[0]
features=[('Family Spotlight','Celebrating 30 years with Doris in Correspondence. Doris has not missed a day.'),('From the Handbook','“A family that logs together stays together.” (Ch. 4, Hours)'),('Wellness Week is every week.','Your modules are waiting.')]
page('employees','Employees',heading('The Legacy family',plain(field(landing,'Hero headline')),plain(field(landing,'Hero body')))+'<section class="employee-actions">'+link('employee-sign-in.html','Sign in — returning family members','button')+link('legacy-match.html','Apply for a role — LegacyMatch™','button secondary')+'</section><section class="feature-grid">'+''.join('<article><p class="micro">'+esc(t)+'</p><p>'+esc(b)+'</p></article>' for t,b in features)+'</section><div class="quiet-link">'+link('employee-create.html','New employee account creation')+'</div>','employee warm')
signin=emp.split('### Sign in')[1].split('### Apply for a role')[0]
page('employee-sign-in','Employee Sign In',heading('Employee access','Welcome back. You were missed.')+prose(md(field(signin,'Body').split('\n\nForgot your password?')[0])+'<p class="demo-note">Local demonstration. No credentials are requested and no authentication occurs.</p><form data-demo-form="signin"><label>Employee ID<input name="employee" autocomplete="off" placeholder="Demonstration ID" required /></label><button class="button" type="submit">Enter demonstration dashboard</button></form><p>Forgot your password? You have not forgotten your password.</p><div class="disabled-links" aria-label="Available after sign-in">Log Hours · Wellness (Mandatory) · Report a Colleague · Benefits · The Handbook (Read-Only)</div>'),'employee')
match=emp.split('### Apply for a role — LegacyMatch™')[1].split('### New employee account creation')[0]
items=['Your loyalty','Your discretion','Your need for sleep','Your memory of previous employers','Your attachment to your current life','Your opinions, generally','Your sense of where you end and the company begins','Your will']
scale=['Strong','Somewhat strong','Neutral','Somewhat weak','Weak']
assessment='<form id="assessment"><p>Rate each of the following on a scale from Strong to Weak. Answer quickly and honestly. Hesitation is also recorded.</p><p class="demo-note">Local demonstration. Responses and response times are not collected or retained.</p>'+''.join('<fieldset><legend>'+str(i+1)+'. '+esc(item)+'</legend><div class="rating-row">'+''.join(f'<label><input type="radio" name="item-{i}" value="{j}" required />{s}</label>' for j,s in enumerate(scale))+'</div></fieldset>' for i,item in enumerate(items))+'<button class="button" type="submit">Complete assessment</button></form><section id="assessment-processing" hidden aria-live="polite"><h2>Analyzing your strengths…</h2><p id="processing-line">Analyzing your weaknesses…</p></section><section id="assessment-result" hidden aria-labelledby="result-title"><p class="micro">LegacyMatch™ / Placement</p><h2 id="result-title">Congratulations. You are a Perpetuity Associate (IC2).</h2><dl class="results"><dt>Ideal placement</dt><dd>Correspondent, PO Box (on-site)</dd><dt>Strongest trait</dt><dd>Availability</dd><dt>Area for growth</dt><dd>Everything else. IC9000 coaching has been scheduled on your behalf.</dd></dl><p>Your results have been shared with your future manager, and your current one.</p><p class="demo-note">Demonstration result. Nothing has been shared or scheduled.</p><div class="action-row">'+link('employee-dashboard.html','Accept placement','button')+link('careers.html','Accept placement later','button secondary')+'</div></section>'
page('legacy-match','LegacyMatch™',heading('Careers / LegacyMatch™','Find where you fit.')+prose(md(field(match,'Intro'))+assessment),'employee')
create='<p class="micro">new_employee_acct_create (DRAFT — do not publish)</p><p class="demo-note">Local demonstration. These fields are not submitted or stored. Use sample information.</p><form data-demo-form="create"><label>Full legal name<input name="name" required autocomplete="off" /></label><label>Employee ID (assigned)<input name="id" value="LSG-IC2" readonly /></label><label>Start date<input name="start" id="start-date" type="date" readonly /></label><label>Department<input name="department" value="Office of Correspondence" readonly /></label><label>Emergency contact (optional; we have one on file)<input name="emergency" autocomplete="off" /></label><button class="button" type="submit">Create account</button></form><section id="account-confirmation" hidden role="status"><h2>Account created. Welcome to the Legacy family!</h2><p>We weren’t expecting you, but we were prepared. Your onboarding has begun, your badge is being printed, and your desk has been assigned.</p><p>There is no need to contact HR. HR will contact you.</p><p class="demo-note">Demonstration complete. No account was created.</p>'+link('employee-dashboard.html','Continue to your dashboard','button')+'</section>'
page('employee-create','New Employee Account',heading('Employee onboarding','Welcome to the family.')+prose(create),'employee')
tiles=[('hours-ledger','Hours Ledger'),('wellness','Wellness Modules (3 overdue)'),('peer-observations','Peer Observations (1 about you)'),('handbook','The Handbook'),('legacy-store','The Legacy Store')]
page('employee-dashboard','Employee Dashboard',heading('Employee dashboard','Good morning. You are on time.')+'<section class="pathways">'+''.join(link(s+'.html',t,'pathway') for s,t in tiles)+'</section><div class="quiet-link"><p class="demo-note">Demonstration dashboard. No employee account or private records are connected.</p></div>','employee cold')
for slug,title,copy in [('hours-ledger','Hours Ledger','Pre-numbered pages. Please do not remove pages.'),('wellness','Wellness Modules','Wellness Week is every week. Your modules are waiting.'),('peer-observations','Peer Observations','Morale is a shared responsibility.')]:
    page(slug,title,heading('Employee dashboard',title+'.')+prose('<p>'+copy+'</p><p class="edition-note">No employee records are connected to this demonstration.</p>'+link('employee-dashboard.html','Return to your dashboard')),'employee cold')
page('handbook','The Employee Handbook',heading('The Legacy family','The Handbook.')+prose('<p class="micro">Chapter 4 / Hours</p><blockquote>A family that logs together stays together.</blockquote><p>Every member receives, reads, and carries the Legacy Systems Employee Handbook.</p><p class="edition-note">The complete handbook has not been supplied in this edition.</p><hr/><p class="micro">Last page</p>'+link('legacy-store.html','The Legacy Store')+link('employee-dashboard.html','Return to your dashboard')),'employee cold')
# Store catalog parsed from the supplied product table.
store=sec('2.')
products=[]
for line in store.splitlines():
    if line.startswith('|') and not line.startswith('| ---') and not line.startswith('| Item'):
        cols=[plain(c.strip()) for c in line.strip('|').split('|')]
        if len(cols)==4: products.append(dict(zip(['name','category','price','description'],cols)))
(ROOT/'src/products.json').write_text(json.dumps(products,ensure_ascii=False,indent=2)+'\n')
categories=list(dict.fromkeys(p['category'] for p in products))
shop=heading('For the Legacy family','The Legacy Store.','Everything the Legacy family needs. Some of it required.')+'<section class="store-body"><div class="policy-banner"><p>Payment by payroll deduction only. Free delivery to your desk. Uniform items are issued, not sold, and therefore cannot be returned.</p><p class="demo-note">Demonstration store. No payment or payroll deduction occurs.</p></div><div class="store-toolbar"><label>Category<select id="store-category"><option value="all">All categories</option>'+''.join('<option>'+esc(c)+'</option>' for c in categories)+'</select></label><a class="button secondary" href="#cart">Your cart (<span id="cart-count">0</span>)</a></div><div class="product-grid">'+''.join(f'<article class="product" data-category="{esc(p["category"])}"><p class="micro">{esc(p["category"])}</p><h2>{esc(p["name"])}</h2><p>{esc(p["description"])}</p><p class="product-price">{esc(p["price"])}</p><button class="button secondary" data-add="{i}" {"disabled" if p["price"]=="—" else ""}>{"Unavailable" if p["price"]=="—" else "Add to cart"}</button></article>' for i,p in enumerate(products))+'</div><section id="cart" class="cart" aria-labelledby="cart-heading"><h2 id="cart-heading">Your cart.</h2><div id="cart-items" aria-live="polite"><p>Your cart is empty. Your uniform order is not.</p></div><p id="cart-total"></p><button class="button" id="checkout" disabled>Place demonstration order</button><div id="order-confirmation" hidden role="status"><h3>Thank you. Your order has been placed and deducted.</h3><p>It will be waiting at your desk, as will you.</p><p class="demo-note">Demonstration complete. No order or deduction was made.</p></div></section>'+link('employee-dashboard.html','Return to your dashboard')+'</section>'
page('legacy-store','The Legacy Store',shop,'store')
# Raw back-office page intentionally excludes the polished shared shell.
(ROOT/'public/founders-letter.txt').write_text('LEGACY SYSTEMS — A LETTER FROM OUR FOUNDERS\n\n'+plain(letter).replace('**','')+'\n')
oslinks=[('founders-letter.txt','A Message from the Founders (plain text)'),('system-ledger.html','Ledger (do not modify)'),('system-subsidiaries.html','Subsidiaries [list]'),('system-intake.html','PO Box Intake Queue [restricted]'),('system-ic9000.html','IC9000 [access denied]'),('system-1987.html','1987 [file not found]'),('governance.html','Corporate Governance (see attached, unsigned)')]
pages['operating-system']='<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>LEGACY SYSTEMS — INTERNAL</title></head><body bgcolor="#f6f4f0"><h1>LEGACY SYSTEMS — INTERNAL</h1><hr/><table cellpadding="10">'+''.join('<tr><td><a href="'+u+'">'+esc(t)+'</a></td></tr>' for u,t in oslinks)+'</table><p>Warning: this page is monitored.</p><hr/><p>Last updated: unknown. Uptime: continuous.</p><p><a href="index.html">Public website</a></p></body></html>'
pages['system-subsidiaries']='<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>Subsidiaries — Internal</title></head><body bgcolor="#f6f4f0"><h1>Subsidiaries [list]</h1><table cellpadding="10">'+''.join('<tr><td><a href="'+c['slug']+'.html">'+esc(c['name'])+'</a></td></tr>' for c in companies)+'</table><p><a href="operating-system.html">Return to internal index</a></p></body></html>'
for slug,title in [('system-ledger','Ledger (do not modify)'),('system-intake','PO Box Intake Queue — restricted'),('system-ic9000','IC9000 — access denied'),('system-1987','1987 — file not found')]:
    pages[slug]=f'<!doctype html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>{esc(title)}</title></head><body bgcolor="#f6f4f0"><h1>{esc(title)}</h1><p>Warning: this page is monitored.</p><p><a href="operating-system.html">Return to internal index</a></p></body></html>'
from experiences import enhance
enhance(pages)
from terminal import terminal_pages
terminal_pages(pages)
for slug,document in pages.items(): (ROOT/(slug+'.html')).write_text('\n'.join(line.rstrip() for line in document.replace('><', '>\n<').splitlines())+'\n')
print(f'Generated {len(pages)} pages and {len(products)} store products.')
