import streamlit as st
import pandas as pd
import json
from utils.auth import Auth
from utils.data_manager import DataManager
from utils.gamification import GamificationSystem

def show_language_stats(data_manager, username, language):
    progress = data_manager.get_user_progress(username)
    language_progress = progress[progress['language'] == language]
    
    if not language_progress.empty:
        avg_score = language_progress['score'].mean()
        completed_modules = len(language_progress)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Score", f"{avg_score:.1f}%")
        with col2:
            st.metric("Completed Modules", completed_modules)
        
        # Progress bar
        st.markdown(
            f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {avg_score}%"></div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info(f"No progress recorded for {language} yet. Start learning!")

def show_achievements(user_data, gamification):
    st.subheader("Your Achievements")
    achievements = json.loads(user_data['achievements'])
    
    if achievements:
        cols = st.columns(3)
        for idx, achievement in enumerate(achievements):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div class="achievement-badge">
                        🏆 {gamification.achievements[achievement]['name']}
                        <br>
                        +{gamification.achievements[achievement]['coins']} coins
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("Complete quizzes and lessons to earn achievements!")

def show_learning_path(language):
    st.subheader("Learning Path")
    
    paths = {
        "IELTS English": [
            "📖 Reading Comprehension",
            "✍️ Academic Writing",
            "🗣️ Speaking Practice",
            "👂 Listening Skills"
        ],
        "Professional English": [
            "📧 Business Communication",
            "🎯 Presentations",
            "🤝 Negotiations"
        ],
        "Urdu": [
            "📝 Basic Grammar",
            "💬 Conversation",
            "✒️ Script Writing"
        ]
    }
    
    for idx, module in enumerate(paths[language], 1):
        st.markdown(f"**Level {idx}:** {module}")

def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in first")
        st.stop()

    auth = Auth()
    data_manager = DataManager()
    gamification = GamificationSystem()
    
    user_data = auth.get_user_data(st.session_state.username)
    
    # Header section
    st.title("Student Dashboard")
    
    # User stats in the sidebar
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    st.sidebar.write(f"Level: {user_data['level']}")
    st.sidebar.write(f"Coins: {user_data['coins']}")
    
    # Quick actions
    st.sidebar.subheader("Quick Actions")
    if st.sidebar.button("Start New Quiz"):
        st.switch_page("pages/quiz.py")
    if st.sidebar.button("View Leaderboard"):
        st.switch_page("pages/leaderboard.py")
    if st.sidebar.button("Learning Materials"):
        st.switch_page("pages/learn.py")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["IELTS English", "Professional English", "Urdu"])
    
    with tab1:
        show_language_stats(data_manager, st.session_state.username, "IELTS English")
        show_learning_path("IELTS English")
    
    with tab2:
        show_language_stats(data_manager, st.session_state.username, "Professional English")
        show_learning_path("Professional English")
    
    with tab3:
        show_language_stats(data_manager, st.session_state.username, "Urdu")
        show_learning_path("Urdu")
    
    # Achievements section
    st.markdown("---")
    show_achievements(user_data, gamification)
    
    # Recent activity
    st.markdown("---")
    st.subheader("Recent Activity")
    recent_progress = data_manager.get_user_progress(st.session_state.username).tail(5)
    
    if not recent_progress.empty:
        for _, activity in recent_progress.iterrows():
            st.markdown(
                f"""
                <div class="leaderboard-item">
                    {activity['language']} - {activity['module']}: {activity['score']}%
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No recent activity. Start learning to see your progress!")

if __name__ == "__main__":
    main()
