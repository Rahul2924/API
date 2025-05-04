from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def show_gold_price():
    url = "https://www.livechennai.com/gold_silverrate.asp"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "<h2>Failed to fetch gold price data</h2>"

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 5 and 'Gold' not in cols[0].text:
            date = cols[0].text.strip()
            g24_1g = cols[1].text.strip()
            g24_8g = cols[2].text.strip()
            g22_1g = cols[3].text.strip()
            g22_8g = cols[4].text.strip()

            html = f"""
            <html>
                <head>
                    <title>Gold Price in India</title>
                    <style>
                        body {{
                            background: #f9f5f0;
                            font-family: Arial, sans-serif;
                            text-align: center;
                            padding-top: 50px;
                        }}
                        h1 {{
                            font-size: 3em;
                            margin-bottom: 10px;
                        }}
                        h2 {{
                            font-size: 2em;
                            margin-bottom: 30px;
                        }}
                        .price {{
                            font-size: 1.8em;
                            margin: 10px;
                        }}
                        .source {{
                            margin-top: 40px;
                            font-size: 0.9em;
                            color: #888;
                        }}
                    </style>
                </head>
                <body>
                    <h1>Gold Price in India</h1>
                    <h2>{date}</h2>
                    <div class="price">24K Gold (1g): <strong>{g24_1g}</strong></div>
                    <div class="price">24K Gold (8g): <strong>{g24_8g}</strong></div>
                    <div class="price">22K Gold (1g): <strong>{g22_1g}</strong></div>
                    <div class="price">22K Gold (8g): <strong>{g22_8g}</strong></div>
                    <div class="source">Source: <a href="{url}" target="_blank">Live Chennai</a></div>
                </body>
            </html>
            """
            return HTMLResponse(content=html)

    return "<h2>No gold price data found</h2>"
