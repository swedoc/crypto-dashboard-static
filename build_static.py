import datetime

# Här skulle vi annars hämta och räkna, men nu testar vi bara grunden
now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Crypto Dashboard (Static)</title>
</head>
<body>
    <h1>Crypto Dashboard</h1>
    <p>Senast uppdaterad: {now}</p>
    <p>Det här är en testversion av den statiska dashboarden.</p>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
