import json
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from utils.motivation import show_motivation

class VirtualEconomy:
    def __init__(self):
        self.shop_items = {
            'profile_themes': {
                'dark_theme': {'name': 'Dark Theme', 'price': 200, 'type': 'theme'},
                'premium_theme': {'name': 'Premium Theme', 'price': 500, 'type': 'theme'}
            },
            'boosters': {
                'double_coins': {'name': 'Double Coins (24h)', 'price': 300, 'type': 'booster'},
                'extra_hints': {'name': 'Extra Hints (10)', 'price': 150, 'type': 'booster'}
            },
            'badges': {
                'language_master': {'name': 'Language Master Badge', 'price': 1000, 'type': 'badge'},
                'quiz_champion': {'name': 'Quiz Champion Badge', 'price': 800, 'type': 'badge'}
            }
        }
        
        self.users_file = "data/users.xlsx"
        
    def get_shop_items(self):
        """Return all available shop items"""
        return self.shop_items
        
    def purchase_item(self, username, item_id):
        """Process item purchase for a user"""
        try:
            df = pd.read_excel(self.users_file)
            user_row = df[df['username'] == username].index[0]
            user_data = df.loc[user_row]
            
            # Find item in shop
            for category in self.shop_items.values():
                if item_id in category:
                    item = category[item_id]
                    break
            else:
                return False, "Item not found"
            
            # Check if user has enough coins
            if user_data['coins'] < item['price']:
                return False, "Not enough coins"
            
            # Update user's inventory and coins
            inventory = json.loads(user_data['inventory']) if 'inventory' in user_data else []
            inventory.append({
                'item_id': item_id,
                'purchased_at': datetime.now().isoformat(),
                'type': item['type']
            })
            
            # Deduct coins and update inventory
            df.at[user_row, 'coins'] = user_data['coins'] - item['price']
            df.at[user_row, 'inventory'] = json.dumps(inventory)
            df.to_excel(self.users_file, index=False)
            
            return True, f"Successfully purchased {item['name']}"
        except Exception as e:
            print(f"Error during purchase: {str(e)}")
            return False, f"Purchase failed: {str(e)}"
    
    def get_user_inventory(self, username):
        """Get user's purchased items"""
        try:
            df = pd.read_excel(self.users_file)
            user_data = df[df['username'] == username].iloc[0]
            if 'inventory' in user_data:
                return json.loads(user_data['inventory'])
            return []
        except Exception as e:
            print(f"Error getting inventory: {str(e)}")
            return []
    
    def check_daily_streak(self, username):
        """Check and update user's daily streak"""
        try:
            df = pd.read_excel(self.users_file)
            user_row = df[df['username'] == username].index[0]
            user_data = df.loc[user_row]
            
            last_login = user_data.get('last_login')
            current_streak = user_data.get('streak', 0)
            
            today = datetime.now().date()
            if last_login:
                last_login_date = datetime.fromisoformat(last_login).date()
                if today - last_login_date == timedelta(days=1):
                    current_streak += 1
                    bonus_coins = min(current_streak * 10, 100)  # Cap at 100 coins
                    df.at[user_row, 'coins'] = user_data['coins'] + bonus_coins
                    df.at[user_row, 'streak'] = current_streak
                elif today - last_login_date > timedelta(days=1):
                    current_streak = 1
                    df.at[user_row, 'streak'] = current_streak
            
            df.at[user_row, 'last_login'] = today.isoformat()
            df.to_excel(self.users_file, index=False)
            
            return current_streak
        except Exception as e:
            print(f"Error checking streak: {str(e)}")
            return 0
