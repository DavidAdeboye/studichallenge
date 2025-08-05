import google.generativeai as genai
import os
import json
import re

class AIProcessor:
    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_study_materials(self, lecture_text, exam_text):
        """
        Generate study materials using Gemini AI based on lecture notes and past exams
        """
        prompt = self._create_study_prompt(lecture_text, exam_text)
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            raise Exception(f"Error generating study materials: {str(e)}")
    
    def _create_study_prompt(self, lecture_text, exam_text):
        """
        Create a comprehensive prompt for generating study materials
        """
        prompt = f"""
        You are an expert academic tutor and exam preparation specialist. Based on the provided lecture notes and past exam questions, generate comprehensive study materials.

        LECTURE NOTES:
        {lecture_text}

        PAST EXAM QUESTIONS:
        {exam_text}

        Please analyze both documents and provide the following in a structured format:

        1. PREDICTED EXAM QUESTIONS (exactly 50 questions):
        Generate 50 high-quality exam questions based on patterns from past exams and content from lecture notes. Include:
        - Multiple choice questions
        - Short answer questions
        - Essay questions
        - Problem-solving questions (if applicable)
        - Make sure questions cover all major topics and follow the style/difficulty of past exams.
        - Take a look at the exaam text, the PAST EXAM QUESTIONS section, and the lecture notes, the LECTURE NOTES section, and give questions that are relevant to the content, and that corrolate with the past exam questions.

        2. AREAS OF CONCENTRATION:
        Identify 8-12 key topic areas that students should focus on based on:
        - Frequency of topics in past exams
        - Emphasis in lecture notes
        - Complexity and importance of concepts
        - Include both broad topics and specific subtopics.
        - Include references to specific pages or sections in the lecture notes where these topics are covered.

        3. STUDY TIPS:
        Provide 10-15 specific, actionable study tips including:
        - How to approach different question types
        - Key concepts to memorize vs understand
        - Study techniques for this specific subject
        - Time management strategies
        - Common mistakes to avoid

        Format your response EXACTLY as follows:

        PREDICTED_QUESTIONS_START
        1. [Question 1]
        2. [Question 2]
        ...
        50. [Question 50]
        PREDICTED_QUESTIONS_END

        AREAS_OF_CONCENTRATION_START
        • [Area 1]
        • [Area 2]
        ...
        AREAS_OF_CONCENTRATION_END

        STUDY_TIPS_START
        • [Tip 1]
        • [Tip 2]
        ...
        STUDY_TIPS_END

        Make sure all content is relevant, specific, and actionable for exam preparation.
        """
        return prompt
    
    def _parse_response(self, response_text):
        """
        Parse the AI response into structured data
        """
        result = {
            "predicted_questions": [],
            "areas_of_concentration": [],
            "study_tips": []
        }
        
        try:
            # Extract predicted questions
            questions_match = re.search(
                r'PREDICTED_QUESTIONS_START(.*?)PREDICTED_QUESTIONS_END',
                response_text,
                re.DOTALL
            )
            if questions_match:
                questions_text = questions_match.group(1).strip()
                # Split by lines and find numbered questions
                lines = questions_text.split('\n')
                questions = []
                for line in lines:
                    line = line.strip()
                    if re.match(r'\d+\.', line):
                        question = re.sub(r'^\d+\.\s*', '', line)
                        if question:
                            questions.append(question)
                result["predicted_questions"] = questions
            
            # Extract areas of concentration
            areas_match = re.search(
                r'AREAS_OF_CONCENTRATION_START(.*?)AREAS_OF_CONCENTRATION_END',
                response_text,
                re.DOTALL
            )
            if areas_match:
                areas_text = areas_match.group(1).strip()
                # Split by lines and find bulleted areas
                lines = areas_text.split('\n')
                areas = []
                for line in lines:
                    line = line.strip()
                    if line.startswith('•') or line.startswith('-'):
                        area = re.sub(r'^[•-]\s*', '', line)
                        if area:
                            areas.append(area)
                result["areas_of_concentration"] = areas
            
            # Extract study tips
            tips_match = re.search(
                r'STUDY_TIPS_START(.*?)STUDY_TIPS_END',
                response_text,
                re.DOTALL
            )
            if tips_match:
                tips_text = tips_match.group(1).strip()
                # Split by lines and find bulleted tips
                lines = tips_text.split('\n')
                tips = []
                for line in lines:
                    line = line.strip()
                    if line.startswith('•') or line.startswith('-'):
                        tip = re.sub(r'^[•-]\s*', '', line)
                        if tip:
                            tips.append(tip)
                result["study_tips"] = tips
            
        except Exception as e:
            print(f"Error parsing response: {str(e)}")
            # Fallback: try to extract any numbered/bulleted items
            result = self._fallback_parse(response_text)
        
        return result
    
    def _fallback_parse(self, response_text):
        """
        Fallback parsing method if structured parsing fails
        """
        lines = response_text.split('\n')
        result = {
            "predicted_questions": [],
            "areas_of_concentration": [],
            "study_tips": []
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Try to identify sections
            if 'question' in line.lower() and ('predict' in line.lower() or 'exam' in line.lower()):
                current_section = 'questions'
                continue
            elif 'area' in line.lower() and 'concentration' in line.lower():
                current_section = 'areas'
                continue
            elif 'tip' in line.lower() or 'study' in line.lower():
                current_section = 'tips'
                continue
            
            # Extract content based on current section
            if current_section == 'questions' and re.match(r'\d+\.', line):
                question = re.sub(r'^\d+\.\s*', '', line)
                if question:
                    result["predicted_questions"].append(question)
            elif current_section == 'areas' and (line.startswith('•') or line.startswith('-')):
                area = re.sub(r'^[•-]\s*', '', line)
                if area:
                    result["areas_of_concentration"].append(area)
            elif current_section == 'tips' and (line.startswith('•') or line.startswith('-')):
                tip = re.sub(r'^[•-]\s*', '', line)
                if tip:
                    result["study_tips"].append(tip)
        
        return result
