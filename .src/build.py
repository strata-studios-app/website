#!/usr/bin/env python3
"""Builds the static stratastudios.app site into the website repo. Markdown in, HTML out."""
import html, os, re, shutil, sys
import markdown

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
FONTS = sys.argv[2]

ADDRESS = "2524 N Broadway, Ste 554 #108357, Edmond, OK 73034"
PHONE = "(405) 237-9026"

CLIMB = ('<svg class="climb" viewBox="14 6 92 104" aria-hidden="true" focusable="false">'
         '<path class="lo" d="M26 96 L60 64 L94 96"/><path class="up" d="M26 70 L60 38 L94 70"/>'
         '<circle class="pt" cx="60" cy="19" r="9"/></svg>')

CSP = ("default-src 'none'; style-src 'self'; font-src 'self'; img-src 'self'; "
       "base-uri 'none'; form-action 'none'")

FOOT_LINKS = [("Support", "/strata/support"), ("Privacy Policy", "/strata/privacy"),
              ("Consumer Health Data", "/strata/consumer-health-data"),
              ("Terms of Use", "/strata/terms"), ("Security", "/security")]


def page(path, title, eyebrow, h1, body, desc):
    links = "".join(f'<a href="{u}">{html.escape(t)}</a>' for t, u in FOOT_LINKS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="no-referrer">
<meta name="author" content="Joshua Antonious">
<meta name="description" content="{html.escape(desc)}">
<meta name="color-scheme" content="light dark">
<title>{html.escape(title)}</title>
<link rel="canonical" href="https://stratastudios.app{path}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/site.css">
</head>
<body>
<header class="top"><a class="brand" href="/" aria-label="Strata Studios home">{CLIMB}<span class="word">strata<span class="dot">.</span></span></a></header>
<main>
<p class="eyebrow">{html.escape(eyebrow)}</p>
<h1>{html.escape(h1)}</h1>
<div class="rule"></div>
{body}
</main>
<footer><nav>{links}</nav><p class="mono">STRATA STUDIOS LLC · {html.escape(ADDRESS.upper())}</p></footer>
</body>
</html>
"""


def md(name):
    text = open(os.path.join(SRC, name), encoding="utf-8").read()
    out = markdown.markdown(text, extensions=["tables", "toc"], output_format="html5")
    return out.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")


def write(rel, content):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)


# Clean everything but .git
for e in os.listdir(OUT):
    if e != ".git":
        fp = os.path.join(OUT, e)
        shutil.rmtree(fp) if os.path.isdir(fp) else os.remove(fp)

os.makedirs(os.path.join(OUT, "fonts"))
for f in ["archivo-latin-400-normal.woff2", "archivo-latin-600-normal.woff2", "archivo-latin-800-normal.woff2",
          "archivo-latin-900-normal.woff2", "ibm-plex-mono-latin-400-normal.woff2", "ibm-plex-mono-latin-500-normal.woff2"]:
    src = os.path.join(FONTS, "archivo" if f.startswith("archivo") else "ibm-plex-mono", "files", f)
    shutil.copy(src, os.path.join(OUT, "fonts", f))
shutil.copy(os.path.join(SRC, "site.css"), os.path.join(OUT, "site.css"))
shutil.copy(os.path.join(SRC, "favicon.svg"), os.path.join(OUT, "favicon.svg"))

write("CNAME", "stratastudios.app\n")
write(".nojekyll", "")

legal = [("terms", "Terms of Use", "STRATA · LEGAL", "Terms of Use",
          "Strata Terms of Use: the agreement between you and Strata Studios LLC."),
         ("privacy", "Privacy Policy", "STRATA · LEGAL", "Privacy Policy",
          "How Strata handles information. Your workout, body and health information stays on your phone."),
         ("consumer-health-data", "Consumer Health Data Privacy Policy", "STRATA · LEGAL",
          "Consumer Health Data Privacy Policy",
          "Strata's consumer health data policy for Washington, Nevada, Connecticut and everyone else.")]
for slug, title, eb, h1, desc in legal:
    write(f"strata/{slug}.html", page(f"/strata/{slug}", f"{title} · Strata", eb, h1, md(f"{slug}.md"), desc))

support = f"""
<p class="lead">Email us about anything in Strata. We reply within one business day.</p>
<h2>Help with the app</h2>
<p>Email <a href="mailto:support@stratastudios.app">support@stratastudios.app</a>. In Strata, More › Help &amp; feedback opens an email with your app version filled in.</p>
<h2>Membership and billing</h2>
<p>Apple bills every Strata membership. To cancel, open Settings › your name › Subscriptions on your iPhone, or More › Membership in Strata, which opens that screen. Cancel at least 24 hours before a renewal or the end of a free trial to avoid the next charge. Deleting the app does not cancel a membership.</p>
<p>Apple handles refunds. Start one from More › Membership in Strata, or at <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.</p>
<h2>Your data</h2>
<p>Your workouts, body and health information stay on your iPhone. Export or delete everything in More › Privacy &amp; security. Privacy questions and requests: <a href="mailto:privacy@stratastudios.app">privacy@stratastudios.app</a>. Read the <a href="/strata/privacy">Privacy Policy</a> and the <a href="/strata/consumer-health-data">Consumer Health Data Privacy Policy</a>.</p>
<h2>Legal notices</h2>
<p>Notices of disputes and arbitration opt-outs go to <a href="mailto:legal@stratastudios.app">legal@stratastudios.app</a>. See the <a href="/strata/terms">Terms of Use</a>.</p>
<h2>Security</h2>
<p>Found a security problem? See our <a href="/security">security policy</a>.</p>
<h2>Important</h2>
<p>Strata is for adults 18 and older. It is fitness guidance, not medical advice. In an emergency, call 911. If you're in crisis, call or text 988.</p>
<div class="card"><p class="mono">CONTACT</p><p>Strata Studios LLC<br>{html.escape(ADDRESS)}<br>{html.escape(PHONE)}<br><a href="mailto:support@stratastudios.app">support@stratastudios.app</a></p></div>
"""
write("strata/support.html", page("/strata/support", "Support · Strata", "STRATA · SUPPORT", "Support", support,
                                  "Help with Strata: support, membership and billing, privacy and legal contacts."))

security = """
<p>Found a security problem in Strata or on stratastudios.app? Email <a href="mailto:security@stratastudios.app">security@stratastudios.app</a> with the details. We reply within 2 business days. Please give us 90 days to fix it before you publish anything. We don't offer a bounty. If you act in good faith, follow this policy, and don't access, keep or share anyone else's data, we won't pursue legal action against you for your research.</p>
"""
write("security.html", page("/security", "Security · Strata Studios", "STRATA STUDIOS · SECURITY", "Security", security,
                            "How to report a security problem in Strata or on stratastudios.app."))

write(".well-known/security.txt", "Contact: mailto:security@stratastudios.app\nExpires: 2027-10-31T00:00:00.000Z\n"
      "Preferred-Languages: en\nCanonical: https://stratastudios.app/.well-known/security.txt\n"
      "Policy: https://stratastudios.app/security\n")

home_links = "".join(f'<li><a href="{u}">{html.escape(t)}</a></li>' for t, u in [
    ("About Strata", "/strata/"), ("Strata support", "/strata/support"), ("Privacy Policy", "/strata/privacy"),
    ("Consumer Health Data Privacy Policy", "/strata/consumer-health-data"),
    ("Terms of Use", "/strata/terms")])
home = f"""
<p class="lead">We make Strata, a strength-training app for iPhone.</p>
<p class="tag">Train with a purpose.</p>
<ul class="links">{home_links}</ul>
"""
write("index.html", page("/", "Strata Studios", "STRATA STUDIOS LLC", "Strata Studios", home,
                         "Strata Studios makes Strata, a strength-training app for iPhone."))
product = """
<p class="lead">A strength-training app for iPhone. Log every set, follow a plan, and get coaching that changes when your plans do.</p>
<p class="tag">Train with a purpose.</p>
<p>Coming to the App Store on Tuesday, December 8, 2026.</p>
<h2>What Strata does</h2>
<ul>
<li>Logs sets, reps and weight fast, with what you did last time beside every set.</li>
<li>Builds a plan around your goal and the days you can train.</li>
<li>Checks in before you train. Short on time or sore, Coach reshapes today's workout and tells you why.</li>
<li>Shows the muscles you've trained this week on a body map.</li>
<li>Travels with you. Pick a hotel gym or no equipment, and Strata swaps in exercises that train the same muscles.</li>
<li>Keeps your rest timer on the Lock Screen.</li>
<li>Explains how to do every exercise in the library.</li>
<li>Reports your results at the end of every plan.</li>
</ul>
<h2>Your data stays yours</h2>
<p>No account required. Your workouts, body and health information stay on your iPhone. We don't collect them and we can't see them. There are no ads. Export everything at any time, as a full backup or as a spreadsheet (CSV).</p>
<h2>Works with the Apple Health app</h2>
<p>Optional. With your permission, Strata reads sleep, heart rate variability, resting heart rate, steps, workouts and body weight from the Health app to shape Coach's call, and saves the workouts you finish to the Health app.</p>
<h2>Price</h2>
<p>14 days free. Then $39.99 a year for the first 1,000 yearly members, kept for as long as you renew, or $9.99 a month. After the first 1,000, the yearly price is $59.99. Apple handles billing, and you can cancel at any time in your iPhone settings.</p>
<h2>Questions</h2>
<h3>Do I need an account?</h3>
<p>No. Strata works without an account, an email or a password.</p>
<h3>Where is my data stored?</h3>
<p>On your iPhone. Strata has no servers for your workout, body or health information.</p>
<h3>How does Coach decide what to change?</h3>
<p>Coach follows training rules that run on your iPhone. It looks at your check-in, your recent training and, if you allow it, your Health app data. Every call comes with the reason.</p>
<h3>Can I train without a gym?</h3>
<p>Yes. Choose no equipment or a travel gym when you start, and Strata adjusts the workout.</p>
<h3>Is there a free version?</h3>
<p>There's a 14-day free trial. After that, Strata is a paid membership.</p>
<h3>Can I move to a new iPhone?</h3>
<p>Yes. Your iPhone backup brings Strata with it, and you can restore from a Strata export file.</p>
<h3>Is Strata on Android?</h3>
<p>Not yet. Strata is for iPhone.</p>
<h3>Who is Strata for?</h3>
<p>Adults 18 and older who lift or want to start. Strata is fitness guidance, not medical advice.</p>
<h2>Who makes Strata</h2>
<p>Strata Studios LLC in Edmond, Oklahoma. Founded by Joshua Antonious. Questions go to <a href="mailto:hello@stratastudios.app">hello@stratastudios.app</a>; help with the app goes to <a href="/strata/support">Strata support</a>.</p>
"""
write("strata/index.html", page("/strata/", "Strata: strength-training app for iPhone", "STRATA", "Strata", product,
    "Strata is a strength-training app for iPhone. No account required, your data stays on your phone, 14 days free. On the App Store December 8, 2026."))

write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: https://stratastudios.app/sitemap.xml\n")
urls = ["/", "/strata/", "/strata/support", "/strata/privacy", "/strata/consumer-health-data", "/strata/terms", "/security"]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      + "".join(f"<url><loc>https://stratastudios.app{u}</loc></url>\n" for u in urls) + "</urlset>\n")

nf = '<p class="lead">That page isn\'t here.</p><p><a href="/">Go to the home page</a> or <a href="/strata/support">get support</a>.</p>'
write("404.html", page("/404", "Page not found · Strata Studios", "STRATA STUDIOS · 404", "Page not found", nf,
                       "Page not found."))
print("built", OUT)
