import streamlit as st
import pandas as pd
from utils.auth import Auth
from utils.data_manager import DataManager
from utils.gamification import GamificationSystem
from utils.virtual_economy import VirtualEconomy
from utils.motivation import show_motivation
import os
import json

# Initialize systems
auth = Auth()
data_manager = DataManager()
gamification = GamificationSystem()
economy = VirtualEconomy()

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("Language Learning Platform")

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")

                if submit:
                    success, message = auth.login(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.rerun()  # Updated from experimental_rerun
                    else:
                        st.error(message)

        with tab2:
            with st.form("signup_form"):
                new_username = st.text_input("Choose Username")
                new_password = st.text_input("Choose Password", type="password")
                submit = st.form_submit_button("Sign Up")

                if submit:
                    success, message = auth.signup(new_username, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

    else:
        user_data = auth.get_user_data(st.session_state.username)

        # Sidebar with user info and virtual economy stats
        st.sidebar.title(f"Welcome, {st.session_state.username}")

        # Check and display streak
        streak = economy.check_daily_streak(st.session_state.username)
        if streak > 0:
            st.sidebar.success(f"🔥 {streak} Day Streak!")

        # Display user stats
        col1, col2, col3 = st.sidebar.columns(3)
        col1.metric("Level", user_data['level'])
        col2.metric("Coins", user_data['coins'])
        col3.metric("Streak", streak)

        # Quick actions
        st.sidebar.subheader("Quick Actions")
        if st.sidebar.button("Visit Shop"):
            st.switch_page("pages/shop.py")
        if st.sidebar.button("Start New Quiz"):
            st.switch_page("pages/quiz.py")
        if st.sidebar.button("View Leaderboard"):
            st.switch_page("pages/leaderboard.py")
        if st.sidebar.button("Learning Materials"):
            st.switch_page("pages/learn.py")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        st.title("Dashboard")

        # Language selection
        language = st.selectbox("Select Language", ["IELTS English", "Professional English", "Urdu"])

        # Main content area
        col1, col2 = st.columns(2)

        with col1:
            st.header("Quick Start")
            if st.button("Start Learning"):
                st.switch_page("pages/learn.py")
            if st.button("Take a Quiz"):
                st.switch_page("pages/quiz.py")

        with col2:
            st.header("Your Progress")
            progress = data_manager.get_user_progress(st.session_state.username)
            if not progress.empty:
                avg_score = progress['score'].mean()
                st.metric("Average Score", f"{avg_score:.1f}%")

                # Progress bar
                st.markdown(
                    f"""
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {avg_score}%"></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Recent achievements and inventory
        col1, col2 = st.columns(2)

        with col1:
            st.header("Recent Achievements")
            if user_data and 'achievements' in user_data:
                achievements = json.loads(user_data['achievements'])
                if achievements:
                    for achievement in achievements[-3:]:
                        st.markdown(
                            f"""
                            <div class="achievement-badge">
                                🏆 {gamification.achievements[achievement]['name']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.info("Complete quizzes to earn achievements!")
            else:
                st.info("Complete quizzes to earn achievements!")

        with col2:
            st.header("Your Items")
            inventory = economy.get_user_inventory(st.session_state.username)
            if inventory:
                for item in inventory:
                    st.markdown(
                        f"""
                        <div class="achievement-badge">
                            🎁 {item['item_id']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("Visit the shop to get some items!")

if __name__ == "__main__":
    main()