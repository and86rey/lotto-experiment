import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

url = "https://www.lotto.de/lotto-6aus49/lottozahlen"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract draw date (e.g., "Samstag, 29.03.2025" or similar)
date_elem = soup.select_one('.drawing-result__date')  # Adjust selector
date_str = datetime.strptime(date_elem.text.split(', ')[1], '%d.%m.%Y').strftime('%Y-%m-%d')  # e.g., '2025-03-29'

# Extract numbers
draw_section = soup.select_one('.drawing-result__numbers')
numbers = draw_section.find_all('span', class_='lotto-ball')
odds = [int(n.text) for n in numbers[:6]]
super_number = int(numbers[-1].text)

# Load and update CSV
df = pd.read_csv('actual_results.csv')
new_row = pd.DataFrame({'date': [date_str], 'odds': ['-'.join(map(str, odds))], 'super_number': [super_number]})
if date_str not in df['date'].values:
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('actual_results.csv', index=False)
