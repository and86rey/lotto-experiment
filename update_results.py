import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Fetch latest draw from lotto.de
url = "https://www.lotto.de/lotto-6aus49/lottozahlen"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract numbers (assumes latest draw is first in table)
draw_section = soup.select_one('.drawing-result__numbers')  # Adjust selector if needed
numbers = draw_section.find_all('span', class_='lotto-ball')  # Class for odds
odds = [int(n.text) for n in numbers[:6]]  # First 6 numbers
super_number = int(numbers[-1].text)  # Last is Superzahl

# Date (today’s draw—Wed or Sat)
today = datetime.utcnow()
date_str = today.strftime("%Y-%m-%d")  # e.g., 2025-04-02

# Load existing CSV
df = pd.read_csv('actual_results.csv')
new_row = pd.DataFrame({'date': [date_str], 'odds': ['-'.join(map(str, odds))], 'super_number': [super_number]})

# Append and save (avoid duplicates)
if date_str not in df['date'].values:
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('actual_results.csv', index=False)  
