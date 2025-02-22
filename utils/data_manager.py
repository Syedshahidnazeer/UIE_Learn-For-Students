import pandas as pd
import json
from pathlib import Path

class DataManager:
    def __init__(self):
        self.progress_file = "data/progress.xlsx"
        Path("data").mkdir(exist_ok=True)
        
        if not Path(self.progress_file).exists():
            df = pd.DataFrame(columns=['username', 'language', 'module', 'score', 'completed'])
            df.to_excel(self.progress_file, index=False)

    def save_progress(self, username, language, module, score):
        df = pd.read_excel(self.progress_file)
        new_progress = {
            'username': username,
            'language': language,
            'module': module,
            'score': score,
            'completed': True
        }
        df = df.append(new_progress, ignore_index=True)
        df.to_excel(self.progress_file, index=False)

    def get_user_progress(self, username):
        df = pd.read_excel(self.progress_file)
        return df[df['username'] == username]

    def get_leaderboard(self):
        df = pd.read_excel(self.progress_file)
        return df.groupby('username')['score'].mean().sort_values(ascending=False).head(10)
