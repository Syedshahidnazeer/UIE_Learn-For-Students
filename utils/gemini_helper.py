# utils/gemini_helper.py
import google.generativeai as genai
from typing import List, Dict, Any
import json

class GeminiQuizSystem:
    def __init__(self):
        # Initialize Gemini API (make sure you have your API key configured)
        genai.configure(api_key='YOUR_GEMINI_API_KEY')
        self.model = genai.GenerativeModel('Gemini 2.0 Flash')

    def generate_reading_questions(self, passage: str) -> List[Dict[str, Any]]:
        """
        Generate IELTS-style reading comprehension questions based on the given passage.
        
        Args:
            passage (str): The reading passage text
            
        Returns:
            List[Dict]: A list of question dictionaries with format:
                {
                    "question": str,
                    "options": List[str],
                    "correct": str
                }
        """
        try:
            # Prompt engineering for Gemini to generate IELTS-style questions
            prompt = f"""
            Generate 5 IELTS reading comprehension questions based on this passage:

            {passage}

            Create questions that test different reading skills like:
            - Main idea comprehension
            - Detail identification
            - Inference
            - Vocabulary in context
            - Purpose/tone understanding

            For each question:
            - Include 4 plausible multiple choice options
            - Ensure only one correct answer
            - Make questions progressively more challenging
            
            Format the response as a JSON array with this structure:
            [
                {{
                    "question": "The question text",
                    "options": ["option1", "option2", "option3", "option4"],
                    "correct": "correct option text"
                }}
            ]
            
            Only return the JSON array, no other text.
            """

            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the response as JSON
            questions = json.loads(response.text)
            
            # Validate the response format
            validated_questions = []
            for q in questions:
                if self._validate_question_format(q):
                    validated_questions.append(q)
            
            # Ensure we have at least some valid questions
            if not validated_questions:
                return self._get_fallback_questions(passage)
                
            return validated_questions

        except Exception as e:
            print(f"Error generating reading questions: {str(e)}")
            # Return fallback questions if there's an error
            return self._get_fallback_questions(passage)

    def _validate_question_format(self, question: Dict) -> bool:
        """Validate that a question dictionary has the correct format."""
        required_keys = {"question", "options", "correct"}
        
        if not all(key in question for key in required_keys):
            return False
            
        if not isinstance(question["options"], list):
            return False
            
        if len(question["options"]) != 4:
            return False
            
        if question["correct"] not in question["options"]:
            return False
            
        return True

    def _get_fallback_questions(self, passage: str) -> List[Dict[str, Any]]:
        """Generate basic fallback questions if the API fails."""
        return [
            {
                "question": "What is the main idea of this passage?",
                "options": [
                    "Cannot be determined from the passage",
                    self._extract_first_sentence(passage),
                    "The passage does not have a main idea",
                    "The topic is too complex to summarize"
                ],
                "correct": self._extract_first_sentence(passage)
            },
            {
                "question": "Which of the following best describes the purpose of this passage?",
                "options": [
                    "To inform",
                    "To entertain",
                    "To persuade",
                    "To criticize"
                ],
                "correct": "To inform"
            }
        ]

    def _extract_first_sentence(self, passage: str) -> str:
        """Extract the first sentence from a passage."""
        sentences = passage.split('.')
        if sentences:
            return sentences[0].strip() + '.'
        return "Main idea of the passage"

    def evaluate_answer(self, question: str, user_answer: str, correct_answer: str) -> Dict[str, Any]:
        """
        Evaluate a user's answer and provide feedback using Gemini.
        
        Args:
            question (str): The question text
            user_answer (str): The user's selected answer
            correct_answer (str): The correct answer
            
        Returns:
            Dict: Evaluation results with feedback
        """
        is_correct = user_answer == correct_answer
        
        try:
            prompt = f"""
            Question: {question}
            User's answer: {user_answer}
            Correct answer: {correct_answer}
            
            Provide constructive feedback in JSON format:
            {{
                "is_correct": boolean,
                "feedback": "brief explanation why the answer is correct/incorrect",
                "improvement_tips": "specific suggestion for improvement if incorrect",
                "score": "1 if correct, 0 if incorrect"
            }}
            
            Only return the JSON object, no other text.
            """
            
            response = self.model.generate_content(prompt)
            feedback = json.loads(response.text)
            
            # Ensure the feedback has the correct format
            return {
                "is_correct": is_correct,
                "feedback": feedback.get("feedback", "Your answer is " + ("correct!" if is_correct else "incorrect.")),
                "improvement_tips": feedback.get("improvement_tips", "Review the passage carefully."),
                "score": 1 if is_correct else 0
            }
            
        except Exception as e:
            print(f"Error generating feedback: {str(e)}")
            return {
                "is_correct": is_correct,
                "feedback": "Your answer is " + ("correct!" if is_correct else "incorrect."),
                "improvement_tips": "Review the passage carefully and try again.",
                "score": 1 if is_correct else 0
            }