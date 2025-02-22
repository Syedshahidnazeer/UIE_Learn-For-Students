import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

class Auth:
    def __init__(self):
        self.users_file = "data/users.xlsx"
        Path("data").mkdir(exist_ok=True)

        if not Path(self.users_file).exists():
            df = pd.DataFrame(columns=[
                'username', 'password', 'coins', 'level', 'achievements',
                'inventory', 'streak', 'last_login'  # New columns
            ])
            df.to_excel(self.users_file, index=False)
            print(f"Created new users file at {self.users_file}")

    def signup(self, username, password):
        try:
            if not username or not password:
                return False, "Username and password are required"

            df = pd.read_excel(self.users_file)
            if username in df['username'].values:
                return False, "Username already exists"

            # Ensure password is stored as string
            new_user = pd.DataFrame({
                'username': [username],
                'password': [str(password)],  # Convert password to string
                'coins': [100],  # Welcome bonus
                'level': [1],
                'achievements': [json.dumps([])],
                'inventory': [json.dumps([])],  # Initialize empty inventory
                'streak': [0],  # Initialize streak
                'last_login': [datetime.now().date().isoformat()]  # Set initial login date
            })

            df = pd.concat([df, new_user], ignore_index=True)
            df['password'] = df['password'].astype(str)  # Ensure all passwords are strings
            df.to_excel(self.users_file, index=False)
            print(f"Successfully created new user: {username}")
            print(f"Current users in database: {df['username'].tolist()}")
            return True, "Signup successful! Welcome bonus: 100 coins"
        except Exception as e:
            print(f"Error during signup: {str(e)}")
            return False, f"Signup failed: {str(e)}"

    def login(self, username, password):
        try:
            if not username or not password:
                return False, "Username and password are required"

            df = pd.read_excel(self.users_file)
            df['password'] = df['password'].astype(str)  # Convert all passwords to strings
            print(f"All users in database: {df['username'].tolist()}")

            user = df[df['username'] == username]
            print(f"Attempting login for user: {username}")
            print(f"Found user data: {not user.empty}")

            if user.empty:
                return False, "User not found"

            stored_password = str(user.iloc[0]['password'])  # Convert stored password to string
            input_password = str(password)  # Convert input password to string
            print(f"Password match: {stored_password == input_password}")

            if stored_password == input_password:
                print("Login successful")
                return True, "Login successful"
            return False, "Invalid password"
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False, f"Login failed: {str(e)}"

    def get_user_data(self, username):
        try:
            df = pd.read_excel(self.users_file)
            user = df[df['username'] == username]
            if not user.empty:
                return user.iloc[0].to_dict()
            print(f"No data found for user: {username}")
            return None
        except Exception as e:
            print(f"Error getting user data: {str(e)}")
            return None