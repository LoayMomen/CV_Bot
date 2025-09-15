import httpx
from typing import Dict, Any, List
from app.core.config import settings


class LLMService:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = settings.DEEPSEEK_BASE_URL

    async def _call_api(self, messages: List[Dict[str, str]], max_tokens: int = 1000) -> str:
        """Make API call to DeepSeek"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.1
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"LLM API error: {e}")
                # Return fallback response
                return self._get_fallback_response()

    def _get_fallback_response(self) -> str:
        """Fallback response when API fails"""
        return '{"skills_required": [], "skills_preferred": [], "min_experience_years": 0, "education_level": "Any", "certifications": []}'

    async def extract_requirements(self, job_description: str) -> Dict[str, Any]:
        """Extract structured requirements from job description"""
        prompt = f"""
        Analyze the following job description and extract structured requirements as JSON:

        Job Description:
        {job_description}

        Extract and return ONLY a JSON object with these fields:
        - skills_required: List of must-have technical skills
        - skills_preferred: List of nice-to-have skills
        - min_experience_years: Minimum years of experience required (number)
        - education_level: Required education level (e.g., "Bachelor's", "Master's", "High School", "Any")
        - certifications: List of required or preferred certifications
        - location: Work location if specified

        Return only valid JSON, no explanations.
        """

        messages = [
            {"role": "system", "content": "You are an HR assistant that extracts structured data from job descriptions. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ]

        response = await self._call_api(messages)

        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            # Return default structure if parsing fails
            return {
                "skills_required": [],
                "skills_preferred": [],
                "min_experience_years": 0,
                "education_level": "Any",
                "certifications": [],
                "location": None
            }

    async def generate_questionnaire(self, job_description: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate interview questionnaire based on job requirements"""
        prompt = f"""
        Create an interview questionnaire based on this job description and requirements:

        Job Description: {job_description}

        Requirements: {requirements}

        Generate a JSON questionnaire with these sections:
        - technical_questions: 5-7 technical questions about required skills
        - experience_questions: 3-5 questions about relevant experience
        - behavioral_questions: 3-5 behavioral/situational questions
        - education_questions: 2-3 questions about education and certifications

        Each question should have:
        - question: The question text
        - type: "text", "number", "boolean", or "scale"
        - category: The skill/area being assessed
        - weight: Importance weight (1-5)

        Return only valid JSON.
        """

        messages = [
            {"role": "system", "content": "You are an HR assistant that creates interview questionnaires. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ]

        response = await self._call_api(messages, max_tokens=1500)

        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            # Return default questionnaire if parsing fails
            return {
                "technical_questions": [
                    {
                        "question": "Describe your experience with the main technologies required for this role.",
                        "type": "text",
                        "category": "technical_skills",
                        "weight": 5
                    }
                ],
                "experience_questions": [
                    {
                        "question": "How many years of relevant experience do you have?",
                        "type": "number",
                        "category": "experience",
                        "weight": 4
                    }
                ],
                "behavioral_questions": [
                    {
                        "question": "Describe a challenging project you worked on and how you overcame obstacles.",
                        "type": "text",
                        "category": "problem_solving",
                        "weight": 3
                    }
                ],
                "education_questions": [
                    {
                        "question": "What is your highest level of education?",
                        "type": "text",
                        "category": "education",
                        "weight": 2
                    }
                ]
            }

    async def explain_candidate_match(self, job_description: str, resume_text: str, score_breakdown: Dict[str, float]) -> str:
        """Generate explanation for candidate match"""
        prompt = f"""
        Explain why this candidate matches (or doesn't match) the job requirements:

        Job Description: {job_description}

        Resume: {resume_text}

        Scores: {score_breakdown}

        Provide a clear, concise explanation (2-3 paragraphs) covering:
        1. Key strengths and relevant experience
        2. Areas where the candidate excels or falls short
        3. Overall recommendation

        Keep it professional and specific.
        """

        messages = [
            {"role": "system", "content": "You are an HR assistant providing candidate match explanations. Be concise and professional."},
            {"role": "user", "content": prompt}
        ]

        response = await self._call_api(messages, max_tokens=500)
        return response.strip()