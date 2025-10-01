from pathlib import Path
from PIL import Image, ImageOps

SRC = Path("assets/honors")
OUT = SRC                 # write outputs next to originals
MAX_W = 1600             # clamp width for the web
BG = (17, 17, 17)        # dark letterbox to match your theme

def to_web_sizes(p: Path):
    im = Image.open(p).convert("RGB")
    w, h = im.size

    # scale down if too wide
    if w > MAX_W:
        im = im.resize((MAX_W, round(h * MAX_W / w)), Image.Resampling.LANCZOS)
        w, h = im.size

    # letterbox to exact 16:9 (no face cutoffs)
    target = ImageOps.pad(
        im,
        size=(MAX_W, round(MAX_W * 9 / 16)),
        method=Image.Resampling.LANCZOS,
        color=BG,
        centering=(0.5, 0.35)  # bias a bit upward to keep faces in frame
    )

    jpg_path  = OUT / f"{p.stem}-web.jpg"
    webp_path = OUT / f"{p.stem}-web.webp"

    target.save(jpg_path,  quality=88, optimize=True, progressive=True)
    target.save(webp_path, format="WEBP", quality=82, method=6)

def main():
    for ext in ("*.jpg","*.jpeg","*.png"):
        for p in SRC.glob(ext):
            # skip already-processed outputs
            if p.name.endswith(("-web.jpg", "-web.webp")):
                continue
            to_web_sizes(p)

if __name__ == "__main__":
    main()
