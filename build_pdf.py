"""يبني NOVA_Atelier_Catalogue.pdf من products.json.
لو في صورة محلية باسم images/<الكود>.jpg بيستخدمها، وإلا بيستخدم رابط الصورة من products.json (محتاج إنترنت).
التشغيل: pip install playwright && playwright install chromium && python build_pdf.py"""
import json, os, html
from pathlib import Path
R=Path(__file__).parent.resolve(); WHATSAPP_NUMBER=""
P=json.load(open(R/"products.json",encoding="utf-8"))
CATS=[("Shoes","أحذية","Shoes"),("Bags","حقائب","Bags"),("Accessories","إكسسوارات","Accessories")]
AR={"Espresso":"إسبريسو","White":"أبيض","Black":"أسود","Sand":"رملي","Tan":"بني فاتح","Charcoal":"فحمي","Camel":"جملي","Stone":"رمادي حجري","Cognac":"كونياك","Mocha":"موكا","Olive":"زيتي","Ivory":"عاجي","Black / Gold":"أسود / ذهبي","Sand print":"طبعة رملية","Bronze":"برونزي"}
def src(p):
    f=R/"images"/f'{p["id"]}.jpg'
    return f.as_uri() if f.exists() else p["image"]
def card(p):
    s=p["sizes"].replace("One size","مقاس واحد · One size")
    return f'''<div class="c"><div class="ph"><img src="{src(p)}" onerror="this.remove()"></div>
<div class="row"><div><h3>{html.escape(p["name_en"])}</h3><div class="ar">{html.escape(p["name_ar"])}</div></div><div class="pr">{p["price"]:,} <small>EGP</small></div></div>
<div class="meta"><span>{p["id"]}</span><span>{html.escape(p["color"])} · {AR.get(p["color"],"")}</span><span>{html.escape(s)}</span></div></div>'''
pages=[];toc=[]
n=3  # cover=1, contents=2
for k,ar,en in CATS:
    L=[p for p in P if p["category"]==k]
    toc.append((en,ar,n,len(L)))
    for i in range(0,len(L),4):
        pages.append((en,ar,L[i:i+4],n)); n+=1
wa="https://wa.me/"+WHATSAPP_NUMBER
body=f'''<section class="pg cover"><div class="tiny">ACCESSORIES • EST. 2026</div><div><h1>NOVA<br>ATELIER</h1><p class="tag">Timeless style, thoughtfully chosen.</p><p class="big">Elegance in every detail.</p><p class="arb">أحذية • حقائب • إكسسوارات</p></div>
</section>
<section class="pg"><div class="eb">CONTENTS · المحتويات</div><h2>The collection</h2><div class="toc">{"".join(f'<div><span>{e} · {a}</span><b>{c} pieces</b><em>{pg}</em></div>' for e,a,pg,c in toc)}<div><span>Contact · تواصل معنا</span><b></b><em>{n}</em></div></div>
<p class="note">Codes and prices are fictional demo data.<br>الأكواد والأسعار بيانات تجريبية افتراضية.</p><div class="ft"><span>NOVA ATELIER</span><span>2</span></div></section>'''
for en,ar,L,pg in pages:
    body+=f'<section class="pg"><div class="hd"><h2>{en}</h2><span class="arh">{ar}</span></div><div class="gr">{"".join(card(p) for p in L)}</div><div class="ft"><span>NOVA ATELIER</span><span>{pg}</span></div></section>'
body+=f'''<section class="pg end"><div class="tiny">NEED A HAND? · هل تحتاج للمساعدة؟</div><div><h1>Find your next favourite.</h1><p class="arb">اعثر على اختيارك القادم.</p><p class="tag">Message us on WhatsApp with the product name and code.<br>ابعتلنا على واتساب اسم المنتج وكوده.</p><a href="{wa}" class="btn">WhatsApp ↗</a></div><div class="tiny">© 2026 NOVA ATELIER · Independent concept project. All products and prices are fictional.</div><div class="ft dk"><span>NOVA ATELIER</span><span>{n}</span></div></section>'''
css='''@font-face{font-family:Cairo;src:url(fonts/Cairo.ttf);font-weight:200 1000}@font-face{font-family:PF;src:url(fonts/Playfair.ttf);font-weight:400 900}
@page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;font-family:Cairo,sans-serif;color:#29251F}
.pg{width:210mm;height:297mm;padding:18mm 16mm;position:relative;page-break-after:always;overflow:hidden;background:#FFFDFA}
h1,h2,h3{font-family:PF,Cairo,serif;font-weight:500;margin:0}.tiny,.eb{font-size:8pt;letter-spacing:.2em;color:#876C4D;font-weight:600}
.cover,.end{background:#29251F;color:#F4F0E8;display:flex;flex-direction:column;justify-content:space-between;padding:22mm 20mm}.cover .tiny,.end .tiny{color:#B9A58A}
.cover h1{font-size:74pt;line-height:1;letter-spacing:.04em}.end h1{font-size:44pt;line-height:1.1}.tag{font-size:12pt;color:#B9A58A;margin:6mm 0}.big{font-family:PF;font-size:20pt;margin:14mm 0 2mm}.arb{font-size:15pt;margin:0}
.cover>div:nth-child(2){margin:auto 0}.btn{display:inline-block;margin-top:8mm;background:#F4F0E8;color:#29251F;padding:4mm 9mm;text-decoration:none;font-size:11pt}
h2{font-size:30pt}.toc{margin-top:14mm}.toc div{display:flex;align-items:baseline;gap:6mm;border-bottom:1px solid #E5DED3;padding:5mm 0;font-size:14pt}.toc span{flex:1}.toc b{font-weight:400;color:#766C60;font-size:10pt}.toc em{font-style:normal;color:#876C4D;font-weight:700}
.note{position:absolute;bottom:30mm;font-size:9pt;color:#766C60;line-height:1.7}
.hd{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid #B9A58A;padding-bottom:4mm;margin-bottom:7mm}.arh{font-size:20pt;color:#876C4D}
.gr{display:grid;grid-template-columns:1fr 1fr;gap:8mm 7mm}.c{height:106mm}.ph{height:72mm;background:#F4F0E8;position:relative;overflow:hidden;border-radius:7mm;box-shadow:0 0 8mm 1mm rgba(135,108,77,.32)}.ph:after{content:"N";position:absolute;inset:0;display:grid;place-items:center;font:64pt PF;color:#B9A58A;z-index:0}
.ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:1}
.row{display:flex;justify-content:space-between;gap:4mm;padding-top:3mm}h3{font-size:12.5pt}.ar{font-size:10.5pt;color:#766C60}.pr{font-weight:700;font-size:12pt;white-space:nowrap}.pr small{font-weight:400;font-size:8pt;color:#766C60}
.meta{display:flex;flex-wrap:wrap;gap:1mm 4mm;font-size:8pt;color:#766C60;margin-top:2mm}.meta span:first-child{color:#876C4D;font-weight:700}
.ft{position:absolute;bottom:9mm;left:16mm;right:16mm;display:flex;justify-content:space-between;font-size:8pt;letter-spacing:.15em;color:#766C60}.ft.dk{color:#B9A58A}'''
out=R/"catalogue.html"; out.write_text(f'<!doctype html><meta charset="utf-8"><style>{css}</style>{body}',encoding="utf-8")
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.goto(out.as_uri())
    try: pg.wait_for_load_state("networkidle",timeout=20000)
    except Exception: pass
    pg.pdf(path=str(R/"NOVA_Atelier_Catalogue.pdf"),prefer_css_page_size=True,print_background=True);b.close()
print("done")
