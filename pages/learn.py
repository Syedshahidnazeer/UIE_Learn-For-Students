import streamlit as st
from utils.data_manager import DataManager

def show_content(language, module):
    content = {
        "IELTS English": {
            "Reading": "Practice reading comprehension with academic texts...",
            "Writing": "Learn essay structures and academic writing...",
            "Speaking": "Improve your speaking skills with practice exercises...",
            "Listening": "Enhance your listening skills with audio exercises..."
        },
        "Professional English": {
            "Business Communication": "Learn professional email writing...",
            "Presentations": "Master the art of business presentations...",
            "Negotiations": "Develop negotiation skills in English..."
        },
        "Urdu": {
            "Basic Grammar": "Learn fundamental Urdu grammar...",
            "Conversation": "Practice everyday Urdu conversations...",
            "Writing": "Learn Urdu script and writing..."
        }
    }
    
    st.write(content[language][module])
    
    # Practice exercise
    st.subheader("Practice Exercise")
    user_input = st.text_area("Complete the exercise:")
    if st.button("Submit"):
        st.success("Exercise submitted! Great job!")

def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in first")
        st.stop()

    st.title("Learning Materials")
    
    language = st.selectbox("Select Language", ["IELTS English", "Professional English", "Urdu"])
    
    modules = {
        "IELTS English": ["Reading", "Writing", "Speaking", "Listening"],
        "Professional English": ["Business Communication", "Presentations", "Negotiations"],
        "Urdu": ["Basic Grammar", "Conversation", "Writing"]
    }
    
    module = st.selectbox("Select Module", modules[language])
    
    show_content(language, module)

if __name__ == "__main__":
    main()

