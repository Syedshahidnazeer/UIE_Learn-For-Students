import pandas as pd
import json

class GamificationSystem:
    def __init__(self):
        self.achievements = {
            'first_quiz': {'name': 'First Quiz', 'coins': 50},
            'perfect_score': {'name': 'Perfect Score', 'coins': 100},
            'streak_3': {'name': '3-Day Streak', 'coins': 150}
        }

    def calculate_level(self, total_score):
        return int(total_score / 1000) + 1

    def check_achievements(self, username, score, user_data):
        earned_achievements = []
        current_achievements = json.loads(user_data['achievements'])

        if score == 100 and 'perfect_score' not in current_achievements:
            earned_achievements.append('perfect_score')

        if len(current_achievements) == 0:
            earned_achievements.append('first_quiz')

        return earned_achievements

    def award_coins(self, achievement):
        return self.achievements[achievement]['coins']
