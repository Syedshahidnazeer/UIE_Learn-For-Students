import streamlit as st
from utils.data_manager import DataManager

def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in first")
        st.stop()

    st.title("Leaderboard")
    
    data_manager = DataManager()
    leaderboard = data_manager.get_leaderboard()
    
    st.write("Top Performers")
    
    for idx, (username, score) in enumerate(leaderboard.items(), 1):
        st.markdown(
            f"""
            <div class="leaderboard-item">
                <b>#{idx}</b> {username} - Score: {score:.1f}%
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()

