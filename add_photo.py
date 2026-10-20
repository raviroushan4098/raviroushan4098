"""Put your photo inside the circular frame of assets/hero.svg.

Usage:   python3 add_photo.py my_photo.jpg
Needs:   Python 3 (Pillow is optional; it crops and shrinks the photo for you:  pip install pillow)
"""
import base64, io, re, sys, os

if len(sys.argv) < 2:
    sys.exit("Usage: python3 add_photo.py my_photo.jpg")

src = sys.argv[1]
data = None
try:
    from PIL import Image
    im = Image.open(src).convert("RGB")
    s = min(im.size)
    l, t = (im.width - s) // 2, (im.height - s) // 2
    im = im.crop((l, t, l + s, t + s)).resize((600, 600))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=85); data = buf.getvalue()
except ImportError:
    data = open(src, "rb").read()
    if len(data) > 600_000:
        sys.exit("Photo is too big. Install Pillow (pip install pillow) or use a photo under 400 KB.")

b64 = base64.b64encode(data).decode()
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "hero.svg")
svg = open(path, encoding="utf-8").read()
cx, cy = 1010, 272
img = (f'<!--PHOTO_START--><g clip-path="url(#pc)"><image href="data:image/jpeg;base64,{b64}" '
       f'x="{cx-152}" y="{cy-152}" width="304" height="304" preserveAspectRatio="xMidYMid slice"/></g><!--PHOTO_END-->')
new, n = re.subn(r"<!--PHOTO_START-->.*?<!--PHOTO_END-->", lambda m: img, svg, flags=re.S)
if n == 0:
    sys.exit("Could not find the photo slot in hero.svg")
open(path, "w", encoding="utf-8").write(new)
print("Done. Commit assets/hero.svg to GitHub.")
