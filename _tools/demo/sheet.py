import sys, os, glob
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sc, lang, fmt = sys.argv[1:4]
fs = sorted(glob.glob(os.path.join(HERE, "preview", f"{sc}-{lang}-{fmt}-*.png")), key=lambda f: int(f.rsplit("-", 1)[1][:-4]))
ims = [Image.open(f) for f in fs]
w, h = ims[0].size; cols = 4 if fmt == "land" else 4; s = 0.5 if fmt == "land" else 0.5
tw, th = int(w * s), int(h * s); rows = (len(ims) + cols - 1) // cols
out = Image.new("RGB", (cols * tw + (cols - 1) * 6, rows * th + (rows - 1) * 6), "white")
for i, im in enumerate(ims): out.paste(im.resize((tw, th), Image.LANCZOS), ((i % cols) * (tw + 6), (i // cols) * (th + 6)))
out.save(os.path.join(HERE, "preview", f"_sheet-{sc}-{lang}-{fmt}.png"))
