import streamlit as st
import random
from utils.data_manager import DataManager
from utils.gamification import GamificationSystem
from utils.auth import Auth
from utils.motivation import MotivationSystem
from utils.gemini_helper import GeminiQuizSystem

def get_ielts_reading_passage(topic):
    # Sample IELTS reading passages - In production, these should come from a database
    passages = {
        "Academic": {
            "Science": """
            The Human Brain
            
            The human brain is the command center for the human nervous system. It receives signals from the body's sensory organs and outputs information to the muscles. The human brain has the same basic structure as other mammal brains but is larger in relation to body size than any other brains.
            
            The brain contains approximately 86 billion nerve cells (neurons) — the "gray matter." These neurons are connected by trillions of connections, or synapses. The brain has three main parts: the cerebrum, cerebellum, and brainstem. The cerebrum is the largest part of the brain. It is associated with higher order functioning, including thinking, perceiving, planning, and understanding language.
            """,
            "Environment": """
            Climate Change Impact
            
            Climate change poses one of the most serious threats to the world's environments and human societies. Rising global temperatures have been linked to changes in weather patterns, leading to more frequent extreme weather events and shifting precipitation patterns.
            
            These changes affect agriculture, water resources, and ecosystems worldwide. Scientists have observed numerous effects of climate change, including rising sea levels, melting glaciers, and changes in the timing of seasonal events. The impact on biodiversity has been particularly severe.
            """
        },
        "General": {
            "Society": """
            The Evolution of Social Media
            
            Social media has transformed how people communicate and share information in the 21st century. What started as simple platforms for connecting with friends has evolved into complex networks that influence everything from personal relationships to global politics.
            
            The first social media platforms emerged in the late 1990s, but the real revolution began with the launch of Facebook in 2004. Today, billions of people use social media daily, sharing content, connecting with others, and consuming news and entertainment.
            """
        }
    }
    return passages.get(topic, {}).get(random.choice(list(passages[topic].keys())))

def get_quiz_questions(language, reading_passage=None):
    if language == "IELTS English" and reading_passage:
        # Generate questions based on the reading passage using Gemini API
        quiz_system = GeminiQuizSystem()
        return quiz_system.generate_reading_questions(reading_passage)
    
    # Your existing questions dictionary for other types
    questions = {
        "IELTS English": [
            {
                "question": "Which word is a synonym for 'ubiquitous'?",
                "options": ["rare", "widespread", "unique", "special"],
                "correct": "widespread"
            },
            {
                "question": "What is the correct past participle of 'write'?",
                "options": ["wrote", "written", "writed", "writing"],
                "correct": "written"
            }
        ],
        "Professional English": [
            {
                "question": "Which is the most appropriate way to start a formal email?",
                "options": ["Hey!", "Dear Sir/Madam,", "Hi there,", "Hello!"],
                "correct": "Dear Sir/Madam,"
            }
        ],
        "Urdu": [
            {
                "question": "What is the Urdu word for 'Hello'?",
                "options": ["Khuda Hafiz", "Shukriya", "Assalam o Alaikum", "Namaste"],
                "correct": "Assalam o Alaikum"
            }
        ]
    }
    return questions[language]

def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in first")
        st.stop()

    # Initialize systems
    data_manager = DataManager()
    gamification = GamificationSystem()
    auth = Auth()
    quiz_system = GeminiQuizSystem()

    st.title("Quiz")

    # Language and topic selection
    language = st.selectbox("Select Language", ["IELTS English", "Professional English", "Urdu"])

    topics = {
        "IELTS English": {
            "Reading": ["Academic", "General"],
            "Writing": ["Task 1", "Task 2"],
            "Speaking": ["Part 1", "Part 2", "Part 3"],
            "Listening": ["Section 1", "Section 2", "Section 3", "Section 4"]
        },
        "Professional English": ["Business Communication", "Presentations", "Negotiations"],
        "Urdu": ["Basic Grammar", "Conversation", "Writing"]
    }

    # Handle nested topics for IELTS
    if language == "IELTS English":
        skill = st.selectbox("Select Skill", list(topics[language].keys()))
        if skill == "Reading":
            topic_type = st.selectbox("Select Type", topics[language][skill])
            reading_passage = get_ielts_reading_passage(topic_type)
        else:
            topic_type = st.selectbox("Select Type", topics[language][skill])
    else:
        skill = st.selectbox("Select Topic", topics[language])
        reading_passage = None
        topic_type = skill

    # Initialize session state
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
        st.session_state.questions = []
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.submitted = False
        st.session_state.feedback = []

    # Display reading passage for IELTS Reading
    if language == "IELTS English" and skill == "Reading" and reading_passage:
        st.markdown("""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
                <h3>Reading Passage</h3>
                <div style='height: 300px; overflow-y: auto;'>
                    {}
                </div>
            </div>
        """.format(reading_passage.replace('\n', '<br>')), unsafe_allow_html=True)

    # Start Quiz button
    if not st.session_state.quiz_started:
        if st.button("Start Quiz"):
            with st.spinner("Generating quiz questions..."):
                if language == "IELTS English" and skill == "Reading":
                    st.session_state.questions = get_quiz_questions(language, reading_passage)
                else:
                    st.session_state.questions = get_quiz_questions(language)
                st.session_state.quiz_started = True
                st.rerun()
    # Quiz in progress
    if st.session_state.quiz_started and not st.session_state.submitted:
        try:
            question_data = st.session_state.questions[st.session_state.current_question]

            # Display progress
            progress = (st.session_state.current_question + 1) / len(st.session_state.questions)
            st.progress(progress)

            # Display question
            st.write(f"Question {st.session_state.current_question + 1}/{len(st.session_state.questions)}:")
            st.write(question_data["question"])

            # Create unique key for radio button
            radio_key = f"answer_{st.session_state.current_question}"
            answer = st.radio("Select your answer:", question_data["options"], key=radio_key)

            # Submit button
            if st.button("Submit Answer", key=f"submit_{st.session_state.current_question}"):
                # Get evaluation from Gemini
                evaluation = quiz_system.evaluate_answer(
                    question_data["question"],
                    answer,
                    question_data["correct"]
                )

                # Store feedback
                st.session_state.feedback.append(evaluation)

                # Update score
                if evaluation["is_correct"]:
                    st.success(evaluation["feedback"])
                    st.session_state.score += evaluation["score"]
                else:
                    st.error(evaluation["feedback"])
                    st.info(f"Improvement tip: {evaluation['improvement_tips']}")

                # Move to next question or finish quiz
                if st.session_state.current_question < len(st.session_state.questions) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.session_state.submitted = True
                    st.rerun()

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            if st.button("Reset Quiz"):
                st.session_state.quiz_started = False
                st.rerun()

    # Quiz completed
    if st.session_state.submitted:
        final_score = (st.session_state.score / len(st.session_state.questions)) * 100

        # Show motivation
        show_motivation(final_score)

        # Save progress
        data_manager.save_progress(
            st.session_state.username,
            language,
            topic,
            final_score
        )

        # Check achievements
        user_data = auth.get_user_data(st.session_state.username)
        earned_achievements = gamification.check_achievements(
            st.session_state.username,
            final_score,
            user_data
        )

        if earned_achievements:
            for achievement in earned_achievements:
                st.balloons()
                st.success(f"New Achievement: {gamification.achievements[achievement]['name']}!")

        st.write(f"Final Score: {final_score:.1f}%")

        # Review answers
        if st.button("Review Answers"):
            for i, (question, feedback) in enumerate(zip(st.session_state.questions, st.session_state.feedback)):
                with st.expander(f"Question {i+1}"):
                    st.write(question["question"])
                    st.write(f"Your answer was {'correct' if feedback['is_correct'] else 'incorrect'}")
                    st.write(f"Feedback: {feedback['feedback']}")
                    if not feedback['is_correct']:
                        st.write(f"Tip: {feedback['improvement_tips']}")

        if st.button("Try Another Quiz"):
            st.session_state.quiz_started = False
            st.session_state.questions = []
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.submitted = False
            st.session_state.feedback = []
            st.rerun()

if __name__ == "__main__":
    main()