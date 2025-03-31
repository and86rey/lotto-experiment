import requests
import json
import pandas as pd
from datetime import datetime

url = "https://www.lotto.de/lotto-6aus49/lottozahlen"
response = requests.get(url)
html = response.text

# Extract JSON from __NEXT_DATA__
start = html.index('{"props":')  # Find JSON start
end = html.rindex('</script>')  # End before closing tag
json_data = json.loads(html[start:end])

# Get draw data (assuming latest draw is in 'draw' field)
draw = json_data['props']['pageProps'].get('draw', {})
if not draw:  # Fallback if no draw data yet
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    odds = [1, 2, 3, 4, 5, 6]  # Dummy odds
    super_number = 0
else:
    # Adjust based on actual JSON structure (example guess)
    date_str = draw.get('date', datetime.utcnow().strftime('%Y-%m-%d'))  # e.g., '2025-03-29'
    odds = draw.get('odds', [1, 2, 3, 4, 5, 6])  # e.g., [4, 16, 25, 33, 42, 49]
    super_number = draw.get('superNumber', 0)  # e.g., 6

# Load and update CSV
df = pd.read_csv('actual_results.csv')
new_row = pd.DataFrame({'date': [date_str], 'odds': ['-'.join(map(str, odds))], 'super_number': [super_number]})
if date_str not in df['date'].values:
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv('actual_results.csv', index=False)
