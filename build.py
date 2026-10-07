#!/usr/bin/env python3
"""Builds index.html for pittner/2027-vision-board-template.

A single-purpose page for the seasonal "2027 vision board template" intent. The sheet
itself is not redrawn here: it is imported from ../vision-board-templates/build.py
(sheet_2027), so the printable is byte-for-byte the one already published there.
"""
import html as _html
import importlib.util
import os
import pathlib
import sys
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("tpl", HERE.parent / "vision-board-templates" / "build.py")
tpl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tpl)

URL = "https://pittner.github.io/2027-vision-board-template/"
SRC = "ghpages_2027"
CAMPAIGN = "template_2027"
PAYPAL_CID = os.environ.get("VB_PAYPAL_CID", "").strip()

# (slug, goal, first step before 1 January, proof by 31 March)
EXAMPLES = [
    ("run10k", "Run a 10K without stopping", "Three 20-minute runs a week, starting in November", "A timed 5K by 31 March"),
    ("fund", "Three months of expenses saved", "An automatic transfer on every payday", "One month saved by 31 March"),
    ("ship", "My side project gets its first paying customer", "Write the one-page offer this weekend", "Landing page live by 31 March"),
    ("read", "Read 24 books in 2027", "Put the first two books on the nightstand tonight", "6 books finished by 31 March"),
    ("job", "A job I chose, not one I drifted into", "Update the CV and message 3 people this month", "10 applications sent by 31 March"),
    ("spanish", "Hold a real conversation in Spanish", "15 minutes a day, starting in November", "A 10-minute call in Spanish by 31 March"),
    ("sleep", "Seven hours of sleep on weeknights", "Phone charges outside the bedroom from tonight", "4 of 5 weeknights in March"),
    ("trip", "The trip I keep postponing, actually taken", "Pick the dates and book the flight before New Year", "Flights booked by 31 March"),
]


def tool(_slug, goal=None, step=None):
    # utm_content is appended in the browser from data-cta, so _slug only documents the caller
    q = {"goal": goal, "step": step, "mode": "wallpaper", "layout": "text"} if goal else {"mode": "wallpaper"}
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com/free-vision-board-maker/?" + urlencode(q)


WALL_2027 = ("https://visionboard.bemooore.com/2027-vision-board-wallpaper/?utm_source=" + SRC
             + "&utm_medium=referral&utm_campaign=" + CAMPAIGN)
HOME = "https://visionboard.bemooore.com/?utm_source=" + SRC + "&utm_medium=referral&utm_campaign=" + CAMPAIGN

FAQ = [
    ("Is there a free printable 2027 vision board template?",
     "Yes, this one. It is a single A4 sheet that also prints on US Letter: 2027 in one word, what has to be true by 31 December 2027, "
     "four quarter boxes with one picture and one proof each, what you leave in 2026, and a first step before 1 January. Free and MIT licensed."),
    ("Can I get the 2027 template as a PDF?",
     "Press Print and choose Save as PDF in the print dialog. That gives a vector PDF at the exact paper size, sharper than a hosted PDF."),
    ("When should I make my 2027 vision board?",
     "Before January, ideally in October or November. A board made in autumn has a first step that is already done on 1 January, "
     "a board made on 31 December usually has none."),
    ("Can I use the 2027 vision board as a phone wallpaper?",
     "Yes. The free browser maker turns a goal and a first step into a 1080x1920 lock-screen wallpaper, no signup and no e-mail. "
     "Each example on this page opens it already filled in."),
]


def main():
    if not PAYPAL_CID:
        sys.exit("VB_PAYPAL_CID is empty: grep -o 'client-id=...' checkout.php on the server")
    W, H = tpl.W, tpl.H
    svg = (f'<svg id="svg-year-2027" class="sheet" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
           f'role="img" aria-label="2027 vision board template, quarter by quarter, printable">'
           f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>{tpl.sheet_2027()}</svg>')
    ex = []
    for slug, goal, step, proof in EXAMPLES:
        ex.append(f'''<li class="ex">
  <b>{_html.escape(goal)}</b>
  <span>First step before 1 January: {_html.escape(step)}.</span>
  <span>Q1 proof: {_html.escape(proof)}.</span>
  <a class="btn" href="{_html.escape(tool(slug, goal, step))}" data-cta="ex_{slug}">Make this my lock screen</a>
</li>''')
    faq_html = "\n".join(f"  <h3>{_html.escape(q)}</h3>\n  <p>{_html.escape(a)}</p>" for q, a in FAQ)
    faq_ld = ",\n".join(
        '{"@type":"Question","name":' + _json(q) + ',"acceptedAnswer":{"@type":"Answer","text":' + _json(a) + '}}'
        for q, a in FAQ)

    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Free Printable 2027 Vision Board Template (A4 &amp; US Letter, no signup)</title>
<meta name="description" content="A free printable 2027 vision board template: one picture and one proof per quarter, what you leave in 2026, and a first step before 1 January. Print from the browser on A4 or US Letter, or download SVG/PNG. No signup, MIT licensed.">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:title" content="Free Printable 2027 Vision Board Template - quarter by quarter">
<meta property="og:description" content="Print-ready 2027 vision board sheet with a proof per quarter. A4 or US Letter, SVG/PNG, no signup, MIT licensed.">
<meta property="og:url" content="{URL}">
<style>
:root{{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#6D28D9;--bg:#FBFAF9}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
a{{color:var(--acc)}}
.wrap{{max-width:1000px;margin:0 auto;padding:0 20px}}
header.hero{{padding:48px 0 18px}}
h1{{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}}
.lede{{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}}
.meta{{font-size:14px;color:var(--muted);margin:0}}
.btn{{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}}
.btn:hover{{border-color:var(--acc);color:var(--acc)}}
.btn.primary{{background:var(--acc);border-color:var(--acc);color:#fff}}
.btn.primary:hover{{background:#5B21B6;color:#fff}}
.main{{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:28px;align-items:start;padding:12px 0 36px}}
@media (max-width:760px){{.main{{grid-template-columns:1fr}}}}
.card{{background:#fff;border:1px solid var(--rule);border-radius:16px;overflow:hidden}}
.preview{{padding:16px}}
.preview svg{{width:100%;height:auto;display:block;border:1px solid var(--rule);border-radius:6px}}
.actions{{padding:0 16px 16px;display:flex;gap:8px;flex-wrap:wrap}}
.side h2{{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}}
.side ol{{padding-left:20px;margin:0 0 18px;color:#374151}}
.side li{{margin:6px 0}}
.bar{{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 14px}}
section.block{{padding:30px 0;border-top:1px solid var(--rule)}}
section.block h2{{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}}
section.block>p{{max-width:70ch;color:#374151}}
ul.exs{{list-style:none;padding:0;margin:16px 0 0;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}}
.ex{{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 16px;display:flex;flex-direction:column;gap:4px}}
.ex b{{font:600 16px/1.35 Georgia,serif}}
.ex span{{font-size:14px;color:#4B5563}}
.ex .btn{{align-self:flex-start;margin-top:8px}}
.after{{margin:0 16px 16px;padding:16px 18px;border:1px solid var(--rule);border-left:4px solid var(--acc);border-radius:12px;background:#FAF7FF;font-size:15px;color:#374151}}
.after[hidden]{{display:none}}
.after p{{margin:0 0 10px}}
.after .lbl{{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:14px 0 6px}}
.tip-amts{{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 10px}}
.tip-amt.on{{background:var(--acc);border-color:var(--acc);color:#fff}}
#tip-go:disabled{{opacity:.7;cursor:default}}
#tip-msg{{margin-top:8px;font-size:13px;color:var(--muted)}}
.faq h3{{font:600 16px/1.4 inherit;margin:18px 0 4px}}
.faq p{{margin:0;color:#374151;max-width:70ch}}
footer{{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}}
@media print{{
  body{{background:#fff}}
  .wrap>*:not(.printzone){{display:none!important}}
  .printzone{{display:block!important}}
  .printzone svg{{width:100%;height:auto;display:block;border:0}}
}}
@page{{size:A4 portrait;margin:0}}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Free printable 2027 vision board template</h1>
  <p class="lede">One page for the whole of 2027: a word for the year, what has to be true by 31 December, and four quarters with one picture and one proof each, so you can check it on 31 March instead of hoping in December. Print it from this page. No signup, no e-mail, no watermark.</p>
  <p class="meta">A4 and US Letter &middot; browser print or Save as PDF &middot; SVG and PNG download &middot; MIT licensed</p>
</header>

<div class="main">
  <article class="card" id="year-2027">
    <div class="preview">{svg}</div>
    <div class="actions">
      <button class="btn primary" data-print="year-2027">Print this sheet</button>
      <button class="btn" data-svg="year-2027">Download SVG</button>
      <button class="btn" data-png="year-2027">Download PNG</button>
    </div>
    <div class="after" id="afterDl" hidden>
      <p><strong>Saved.</strong> Want the same 2027 goal on your phone? The free maker turns it into a 1080&times;1920 lock-screen wallpaper you see every time you unlock. No signup, no e-mail.</p>
      <a class="btn primary" href="{_html.escape(tool('after_dl'))}" data-cta="after_dl_tool">Make it my lock screen</a>
      <div class="lbl">Or just say thanks</div>
      <p>This template is free and MIT licensed, and it stays that way. If it saved you time, you can send a one-off thank you. You get nothing extra for it.</p>
      <div class="tip-amts" role="group" aria-label="Amount">
        <button type="button" class="btn tip-amt" data-amt="3">&euro;3</button>
        <button type="button" class="btn tip-amt on" data-amt="5">&euro;5</button>
        <button type="button" class="btn tip-amt" data-amt="10">&euro;10</button>
      </div>
      <button type="button" class="btn" id="tip-go">Say thanks with PayPal</button>
      <div id="tip-pp" style="max-width:360px;margin-top:10px"></div>
      <div id="tip-msg">PayPal handles the payment. Nothing is loaded from PayPal until you press the button.</div>
    </div>
  </article>

  <div class="side">
    <h2>Fill it in 30 minutes</h2>
    <div class="bar">
      <button class="btn primary" id="pageA4" aria-pressed="true">Paper: A4</button>
      <button class="btn" id="pageLetter" aria-pressed="false">Paper: US Letter</button>
    </div>
    <ol>
      <li>Write 2027 in one word first. If you cannot, the rest of the sheet will be a wish list.</li>
      <li>Write the one sentence that must be true by 31 December 2027.</li>
      <li>Give each quarter one picture and one proof you can check on its date: 31 March, 30 June, 30 September, 31 December.</li>
      <li>Name what you leave in 2026 and what you keep doing. Both lines matter.</li>
      <li>Do the first step before 1 January and write the date next to it.</li>
      <li>Tick a review box on each quarter date. Change the picture if the goal changed, not the date.</li>
    </ol>
    <p class="meta">On a phone? Printing is awkward there. <a href="{_html.escape(WALL_2027)}" data-cta="side_wallpaper_2027">Pick a ready 2027 goal as a lock-screen wallpaper</a> instead.</p>
  </div>
</div>

<section class="block">
  <h2>Stuck on what to write? Eight 2027 goals with a proof</h2>
  <p>Each example has the two things most boards are missing: a first step you take before New Year and a proof you can check on 31 March. Copy one onto the sheet, or tap it to open the free maker already filled in and save it as your lock screen.</p>
  <ul class="exs">
{chr(10).join(ex)}
  </ul>
</section>

<section class="block faq">
  <h2>Questions</h2>
{faq_html}
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="{_html.escape(HOME)}" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/vision-board-templates/">all 7 printable vision board templates</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">AI vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/2027-vision-board-template">source</a>
</footer>

<div class="printzone" id="printzone" style="display:none"></div>
</div>

<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{faq_ld}
]}}
</script>

<script>
(function(){{
  var EP='https://visionboard.bemooore.com/api/event.php',P='{SRC}',engaged=false;
  function beacon(ev,label){{
    try{{
      var b=JSON.stringify({{event:ev,utm:P+' | '+label+' | '+location.search}});
      if(navigator.sendBeacon){{navigator.sendBeacon(EP,new Blob([b],{{type:'text/plain'}}));}}
      else{{fetch(EP,{{method:'POST',body:b,keepalive:true,mode:'no-cors'}});}}
    }}catch(e){{}}
  }}
  // Every link to our site carries the button and where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){{
    a.href+='&utm_content='+encodeURIComponent(a.getAttribute('data-cta'))+'&utm_term='+encodeURIComponent('via_'+src);
  }});
  function engage(how){{ if(engaged)return; engaged=true; beacon('page_engaged',how); }}
  setTimeout(function(){{engage('dwell6s');}},6000);
  window.addEventListener('scroll',function(){{
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  }},{{passive:true}});
  document.addEventListener('click',function(e){{
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  }});

  var ps=document.createElement('style'); document.head.appendChild(ps);
  function paper(size){{
    ps.textContent='@page{{size:'+size+' portrait;margin:'+(size==='A4'?'0':'6mm')+'}}';
    document.getElementById('pageA4').classList.toggle('primary',size==='A4');
    document.getElementById('pageLetter').classList.toggle('primary',size!=='A4');
    document.getElementById('pageA4').setAttribute('aria-pressed',String(size==='A4'));
    document.getElementById('pageLetter').setAttribute('aria-pressed',String(size!=='A4'));
  }}
  paper('A4');
  document.getElementById('pageA4').onclick=function(){{paper('A4');beacon('cta_click','paper_a4');}};
  document.getElementById('pageLetter').onclick=function(){{paper('Letter');beacon('cta_click','paper_letter');}};

  var after=document.getElementById('afterDl');
  function showAfter(){{ after.hidden=false; }}

  // Voluntary thank-you, same flow as T-095/T-105: PayPal SDK loads only on click.
  var amt='5',tipLoading=false,amts=document.querySelector('.tip-amts'),go=document.getElementById('tip-go'),msg=document.getElementById('tip-msg');
  amts.addEventListener('click',function(e){{
    var b=e.target.closest('.tip-amt'); if(!b)return;
    amt=b.getAttribute('data-amt');
    Array.prototype.forEach.call(amts.querySelectorAll('.tip-amt'),function(x){{x.classList.toggle('on',x===b);}});
  }});
  go.addEventListener('click',function(){{
    if(tipLoading)return; tipLoading=true; go.disabled=true; go.textContent='Loading PayPal...';
    beacon('cta_click','tip_open_'+amt);
    var s=document.createElement('script');
    s.src='https://www.paypal.com/sdk/js?client-id={PAYPAL_CID}&currency=EUR&intent=capture&components=buttons';
    s.onerror=function(){{ tipLoading=false; go.disabled=false; go.textContent='Say thanks with PayPal'; msg.textContent='PayPal could not be loaded. Please try again in a moment.'; }};
    s.onload=function(){{
      go.style.display='none';
      window.paypal.Buttons({{
        style:{{layout:'vertical',label:'paypal'}},
        createOrder:function(d,actions){{
          return actions.order.create({{
            purchase_units:[{{amount:{{value:amt,currency_code:'EUR'}},custom_id:'tip-vb-2027',description:'Printable 2027 vision board template, voluntary thank you'}}],
            application_context:{{brand_name:'VisionBoard',user_action:'PAY_NOW',shipping_preference:'NO_SHIPPING'}}
          }});
        }},
        onApprove:function(d,actions){{
          return actions.order.capture().then(function(){{
            beacon('cta_click','tip_paid_'+amt);
            document.getElementById('tip-pp').innerHTML='<p><strong>Thank you.</strong> The payment went through.</p>';
            msg.textContent='PayPal has emailed you the receipt.';
          }});
        }},
        onError:function(){{ msg.textContent='Something went wrong at PayPal and no money was taken. You can try again.'; }}
      }}).render('#tip-pp');
    }};
    document.head.appendChild(s);
  }});

  function svgEl(){{ return document.getElementById('svg-year-2027'); }}
  function serialize(){{
    var s=svgEl().cloneNode(true); s.removeAttribute('class'); s.removeAttribute('id');
    s.setAttribute('xmlns','http://www.w3.org/2000/svg');
    s.setAttribute('width','210mm'); s.setAttribute('height','297mm');
    return '<?xml version="1.0" encoding="UTF-8"?>\\n'+new XMLSerializer().serializeToString(s);
  }}
  function save(blob,name){{
    var u=URL.createObjectURL(blob),a=document.createElement('a');
    a.href=u;a.download=name;document.body.appendChild(a);a.click();
    setTimeout(function(){{URL.revokeObjectURL(u);a.remove();}},1500);
  }}
  document.addEventListener('click',function(e){{
    var b=e.target.closest('button'); if(!b)return;
    if(b.hasAttribute('data-print')){{
      var z=document.getElementById('printzone');
      z.innerHTML=''; z.appendChild(svgEl().cloneNode(true)); z.style.display='block';
      beacon('template_print','year-2027');
      window.print();
      setTimeout(function(){{z.style.display='none';z.innerHTML='';showAfter();}},800);
    }} else if(b.hasAttribute('data-svg')){{
      save(new Blob([serialize()],{{type:'image/svg+xml'}}),'2027-vision-board-template.svg');
      beacon('template_download','year-2027|svg');
      showAfter();
    }} else if(b.hasAttribute('data-png')){{
      var img=new Image(), src='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(serialize())));
      img.onload=function(){{
        var c=document.createElement('canvas'); c.width=1654; c.height=2339; // A4 @ 200dpi
        var x=c.getContext('2d'); x.fillStyle='#fff'; x.fillRect(0,0,c.width,c.height);
        x.drawImage(img,0,0,c.width,c.height);
        c.toBlob(function(bl){{ save(bl,'2027-vision-board-template.png'); }},'image/png');
      }};
      img.src=src;
      beacon('template_download','year-2027|png');
      showAfter();
    }}
  }});
}})();
</script>
</body>
</html>
'''
    (HERE / "index.html").write_text(page, encoding="utf-8")
    (HERE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'  <url><loc>{URL}</loc><lastmod>2026-10-07</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>\n'
        '</urlset>\n', encoding="utf-8")
    print("wrote", HERE / "index.html", len(page), "bytes,", len(EXAMPLES), "examples")


def _json(s):
    import json
    return json.dumps(s, ensure_ascii=False)


if __name__ == "__main__":
    main()
