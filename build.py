import os
from datetime import datetime

# 1. Read existing captions from captions.txt
captions_data = {}
if os.path.exists("captions.txt"):
    with open("captions.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                parts = line.strip().split("|")
                img_name = parts[0].strip()
                caption = parts[1].strip()
                date = parts[2].strip() if len(parts) > 2 else datetime.now().strftime("%B %d, %Y")
                captions_data[img_name] = {"caption": caption, "date": date}

# 2. Scan the images folder for photos
img_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
image_files = []
if os.path.exists("images"):
    image_files = [f for f in os.listdir("images") if f.lower().endswith(img_extensions)]
    # Sort files so newest additions or specific patterns group naturally
    image_files.sort()

# 3. Generate the HTML row blocks dynamically
html_rows = ""
for img in image_files:
    # Use caption text if provided, otherwise default to a clean filename title
    data = captions_data.get(img, {
        "caption": os.path.splitext(img)[0].replace("-", " ").replace("_", " "),
        "date": datetime.now().strftime("%B %d, %Y")
    })
    
    html_rows += f"""
            <!-- Entry -->
            <div class="photo-row">
                <div class="photo-box">
                    <img src="images/{img}" alt="{data['caption']}">
                </div>
                <div class="text-box">
                    <div class="photo-date">{data['date']}</div>
                    <p class="photo-caption">{data['caption']}</p>
                </div>
            </div>"""

# 4. Define the HTML Shell template
html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nubian Platform</title>
    <style>
        :root {{ --bg-color: #ffffff; --text-color: #111111; --caption-color: #666666; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: var(--bg-color); color: var(--text-color); line-height: 1.6; margin: 0; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        header {{ text-align: center; padding: 60px 0 40px 0; }}
        h1 {{ margin: 0 0 10px 0; font-size: 2rem; font-weight: 600; }}
        .subtitle {{ color: var(--caption-color); margin: 0; font-size: 1rem; text-transform: lowercase; }}
        .photo-stream {{ display: flex; flex-direction: column; gap: 80px; margin-top: 40px; }}
        .photo-row {{ display: flex; align-items: center; gap: 40px; width: 100%; }}
        .photo-row:nth-child(even) {{ flex-direction: row-reverse; }}
        .photo-box {{ flex: 3; }}
        .photo-box img {{ width: 100%; height: auto; display: block; border-radius: 4px; }}
        .text-box {{ flex: 2; }}
        .photo-date {{ font-size: 0.8rem; color: var(--caption-color); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }}
        .photo-caption {{ font-size: 0.95rem; margin: 0; }}
        @media (max-width: 768px) {{ .photo-row, .photo-row:nth-child(even) {{ flex-direction: column; gap: 16px; }} .photo-stream {{ gap: 50px; }} }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Nubian Platform</h1>
            <p class="subtitle">collection</p>
        </header>
        <main class="photo-stream">{html_rows}
        </main>
    </div>
</body>
</html>"""

# 5. Overwrite index.html with the fresh copy
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Success! Rebuilt index.html with {len(image_files)} photos.")
