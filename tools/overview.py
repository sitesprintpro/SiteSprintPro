"""Turn a tall full-page screenshot into side-by-side columns so the whole page can be reviewed in one image."""
import sys
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
colw = int(sys.argv[3]) if len(sys.argv) > 3 else 330
im = Image.open(src).convert("RGB")
scale = colw / im.width
im = im.resize((colw, int(im.height * scale)))
colh = 1500
cols = [im.crop((0, y, colw, min(y + colh, im.height))) for y in range(0, im.height, colh)]
sheet = Image.new("RGB", (len(cols) * (colw + 16) + 16, colh + 32), (30, 30, 34))
for i, c in enumerate(cols):
    sheet.paste(c, (16 + i * (colw + 16), 16))
sheet.save(out, quality=85)
print(out, len(cols), "columns")
