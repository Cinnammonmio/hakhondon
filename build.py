"""Build index.html (GitHub Pages / home-screen app) from app.html.

app.html is the page body used for the claude.ai preview. This script wraps it in a
full HTML document with icons, the web app manifest, and full-screen fixes for
iPhone home-screen mode.

Usage: python3 build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
body = (ROOT / "app.html").read_text(encoding="utf-8")

HEAD = """<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="หาคนโดน: รวมเกมวงเพื่อน ลุ้นว่าใครโดน เล่นเครื่องเดียวหรือหลายเครื่องก็ได้">
<meta name="theme-color" content="#13091f">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="หาคนโดน">
<link rel="icon" type="image/svg+xml" href="logo.svg">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="manifest" href="manifest.webmanifest">
<style>:root{color-scheme:dark;background:#13091f}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}</style>
"""

# iPhone home-screen mode with a translucent status bar reports a page height that is
# short by the status bar, which left an empty strip at the bottom. A fixed body always
# covers the whole screen; safe-area padding keeps content clear of the notch and the
# home indicator.
STANDALONE = """<style>
html{height:100%}
body{position:fixed;inset:0;height:auto;padding-top:env(safe-area-inset-top,0px)}
.menu-wrap{padding-bottom:calc(28px + env(safe-area-inset-bottom,0px))}
.controls{padding-bottom:max(16px,calc(env(safe-area-inset-bottom,0px) + 6px))}
.view>.stage:last-child{margin-bottom:max(16px,env(safe-area-inset-bottom,0px))}
</style>
"""

end = body.index("</style>") + len("</style>")
html = HEAD + body[:end] + "\n" + STANDALONE + "</head>\n<body>\n" + body[end:] + "\n</body>\n</html>\n"
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("built index.html", len(html), "bytes")
