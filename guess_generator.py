import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime, timedelta

# Load CSVs from repo
def load_csv(url):
    df = pd.read_csv(url)
    df['odds'] = df['odds'].apply(lambda x: list(map(int, x.split('-'))))
    return df

# Prepare features and targets
def prepare_data(df_human, df_ai, df_actual):
    df_all = pd.concat([df_human, df_ai, df_actual], ignore_index=True)
    X = []
    y_odds = []
    y_super = []
    for i in range(len(df_all)):
        odds_binary = [1 if j in df_all.iloc[i]['odds'] else 0 for j in range(1, 50)]
        X.append(odds_binary + [df_all.iloc[i]['super_number']])
        if i > 0:
            y_odds.append(df_all.iloc[i-1]['odds'])
            y_super.append(df_all.iloc[i-1]['super_number'])
    return np.array(X[:-1]), np.array(y_odds), np.array(y_super)

# Train and predict
def generate_guess(X, y_odds, y_super, latest_features):
    clf_odds = RandomForestClassifier(n_estimators=50, random_state=42)
    clf_odds.fit(X, [[1 if i in odds else 0 for i in range(1, 50)] for odds in y_odds])
    clf_super = RandomForestClassifier(n_estimators=50, random_state=42)
    clf_super.fit(X, y_super)
    odds_probs = clf_odds.predict_proba([latest_features])[0]
    odds = sorted(np.argsort([p[1] for p in odds_probs])[-6:] + 1)
    super_number = clf_super.predict([latest_features])[0]
    return odds, super_number

# Main
if __name__ == "__main__":
    repo = "and86rey/lotto-experiment"  # Your repo
    human_url = f"https://raw.githubusercontent.com/{repo}/main/human_guess.csv"
    ai_url = f"https://raw.githubusercontent.com/{repo}/main/ai_guess.csv"
    actual_url = f"https://raw.githubusercontent.com/{repo}/main/actual_results.csv"

    df_human = load_csv(human_url)
    df_ai = load_csv(ai_url)
    df_actual = load_csv(actual_url)

    # Next draw date (Wednesday or Saturday)
    today = datetime(2025, 3, 31)
    next_draw = today + timedelta(days=(2 - today.weekday() + 7) % 7 if today.weekday() <= 2 else (5 - today.weekday() + 7) % 7)
    next_date = next_draw.strftime("%Y-%m-%d")

    X, y_odds, y_super = prepare_data(df_human, df_ai, df_actual)
    if len(X) > 0:
        latest_features = X[-1]
        odds, super_number = generate_guess(X, y_odds, y_super, latest_features)
    else:
        odds = sorted(np.random.choice(range(1, 50), 6, replace=False))
        super_number = np.random.randint(0, 10)

    # Output for Actions to update ai_guess.csv
    print(f"{next_date},{'-'.join(map(str, odds))},{super_number}")
