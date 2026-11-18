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
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
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

# iPhone home-screen mode (iOS 26) with a translucent status bar reports a viewport
# that is short by the status-bar height, which leaves an empty strip at the bottom.
# iOS 26 also refuses to draw position:fixed content below that short viewport, so
# the page uses normal flow instead: the script measures the missing height (iOS
# home-screen mode only) and <html> grows by that much. Safe-area padding keeps
# content clear of the notch and is kept tight above the home bar.
STANDALONE = """<script>
(function(){
  function fix(){
    var g=0;
    if(window.navigator.standalone===true){
      var land=window.matchMedia&&matchMedia('(orientation: landscape)').matches;
      var full=land?Math.min(screen.width,screen.height):Math.max(screen.width,screen.height);
      g=Math.round(full-window.innerHeight);if(g<0||g>120)g=0;
    }
    document.documentElement.style.setProperty('--vfix',g+'px');
  }
  fix();window.addEventListener('resize',fix);window.addEventListener('orientationchange',function(){setTimeout(fix,300)});window.addEventListener('pageshow',fix);
})();
</script>
<style>
html{height:calc(100% + var(--vfix,0px));overflow:hidden}
body{position:relative;height:100%;overflow:hidden;padding-top:env(safe-area-inset-top,0px)}
.menu-wrap{padding-bottom:calc(12px + env(safe-area-inset-bottom,0px) / 2)}
.controls{padding-bottom:max(10px,calc(env(safe-area-inset-bottom,0px) - 18px))}
.view>.stage:last-child{margin-bottom:max(10px,calc(env(safe-area-inset-bottom,0px) - 18px))}
</style>
"""

end = body.index("</style>") + len("</style>")
html = HEAD + body[:end] + "\n" + STANDALONE + "</head>\n<body>\n" + body[end:] + "\n</body>\n</html>\n"
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("built index.html", len(html), "bytes")
