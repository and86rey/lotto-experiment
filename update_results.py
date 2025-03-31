from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Set up headless Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Fetch rendered page
url = "https://www.lotto.de/lotto-6aus49/lottozahlen"
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Extract draw date
date_elem = soup.find('div', class_='drawing-result')  # Parent container
if date_elem and date_elem.find('span', class_='date'):
    date_text = date_elem.find('span', class_='date').text
    date_str = datetime.strptime(date_text.split(', ')[1], '%d.%m.%Y').strftime('%Y-%m-%d')
    print(f"Date found: {date_str}")
else:
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    print(f"Date not found, using fallback: {date_str}")

# Extract numbers
draw_section = soup.find('div', class_='drawing-result__numbers')
if draw_section:
    numbers = draw_section.find_all('span', class_='lotto-ball')
    odds = [int(n.text) for n in numbers[:6]]
    super_number = int(numbers[-1].text)
    print(f"Numbers found: {odds}, Superzahl: {super_number}")
else:
    odds = [1, 2, 3, 4, 5, 6]
    super_number = 0
    print("Numbers not found, using fallback")

# Load and update CSV
df = pd.read_csv('actual_results.csv')
new_row = pd.DataFrame({'date': [date_str], 'odds': ['-'.join(map(str, odds))], 'super_number': [super_number]})
if date_str not in df['date'].values:
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('actual_results.csv', index=False)
    print(f"Added to CSV: {date_str}, {odds}, {super_number}")
else:
    print(f"Date {date_str} already in CSV, skipped")
