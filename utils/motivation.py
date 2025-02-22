# utils/motivation.py
import random
import streamlit as st

class MotivationSystem:
    def __init__(self):
        self.high_score_quotes = [
            "🌟 Absolutely brilliant! You're mastering this!",
            "🏆 Outstanding performance! Keep shining!",
            "🎉 Incredible work! You're on fire!",
            "⭐ Excellence is your trademark! Amazing job!",
            "🌈 Phenomenal score! You're unstoppable!"
        ]
        
        self.medium_score_quotes = [
            "👍 Good effort! You're making solid progress!",
            "💪 Well done! Keep pushing forward!",
            "🌱 You're growing stronger with each attempt!",
            "✨ Solid performance! Keep up the good work!",
            "🎯 You're on the right track! Keep going!"
        ]
        
        self.low_score_quotes = [
            "🌅 Every master was once a beginner. Keep going!",
            "🚀 The only way is up from here!",
            "💡 Each attempt makes you stronger!",
            "🌱 Growth comes from challenges. You've got this!",
            "⭐ Don't give up! Progress takes time!"
        ]

        # ASCII art for different score ranges
        self.high_score_art = """
        🌟 🎉 🌟 🎉 🌟
        ╔═══════════╗
        ║ EXCELLENT ║
        ╚═══════════╝
        🌟 🎉 🌟 🎉 🌟
        """

        self.medium_score_art = """
        💪 ✨ 💪 ✨ 💪
        ╔════════╗
        ║  GOOD  ║
        ╚════════╝
        💪 ✨ 💪 ✨ 💪
        """

        self.low_score_art = """
        🌱 💡 🌱 💡 🌱
        ╔═══════════╗
        ║ KEEP GOING ║
        ╚═══════════╝
        🌱 💡 🌱 💡 🌱
        """

    def get_motivation_content(self, score):
        """
        Get motivational content based on the score.
        
        Args:
            score (float): Score percentage (0-100)
            
        Returns:
            dict: Dictionary containing motivational content
        """
        if score >= 80:
            quote = random.choice(self.high_score_quotes)
            art = self.high_score_art
            color = "#28a745"  # green
        elif score >= 60:
            quote = random.choice(self.medium_score_quotes)
            art = self.medium_score_art
            color = "#ffc107"  # yellow
        else:
            quote = random.choice(self.low_score_quotes)
            art = self.low_score_art
            color = "#17a2b8"  # blue

        return {
            "quote": quote,
            "art": art,
            "color": color
        }

def show_motivation(score):
    """
    Display motivational content in Streamlit based on the score.
    
    Args:
        score (float): Score percentage (0-100)
    """
    motivation = MotivationSystem()
    content = motivation.get_motivation_content(score)

    # Create a visually appealing container
    st.markdown(f"""
        <div style='
            background-color: {content["color"]}22;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
            border: 2px solid {content["color"]};
        '>
            <h2 style='color: {content["color"]};'>{content["quote"]}</h2>
            <pre style='
                background-color: transparent;
                border: none;
                font-family: monospace;
                color: {content["color"]};
                margin-top: 15px;
            '>{content["art"]}</pre>
        </div>
    """, unsafe_allow_html=True)

    # Add some animations based on score
    if score >= 80:
        st.balloons()
    elif score >= 60:
        st.success("Keep up the great work! 🌟")
    else:
        st.info("Remember: Every attempt makes you stronger! 💪")

    # Add specific tips based on score
    if score < 60:
        st.markdown("""
        ### Tips for Improvement:
        1. Review the questions you found challenging
        2. Take notes on areas that need more focus
        3. Try practicing similar questions
        4. Consider shorter study sessions with more frequency
        """)