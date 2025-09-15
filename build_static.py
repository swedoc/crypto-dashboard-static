import os
import datetime

# Skapa katalogen public om den inte finns
os.makedirs("public", exist_ok=True)

# Skapa en tidsstämpel
now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# HTML-innehåll
html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Crypto Dashboard (Static)</title>
</head>
<body>
  <h1>Crypto Dashboard (Static)</h1>
  <p>Senast uppdaterad: {now}</p>
</body>
</html>
"""

# Skriv filen till public/index.html
with open("public/index.html", "w") as f:
    f.write(html_content)
