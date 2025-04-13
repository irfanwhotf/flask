"""
Utility functions for interacting with Google's Gemini AI API.
Handles prompt construction, API calls, and response processing.
"""
import os
import json
import requests
from typing import Dict, Any, Optional, List, Union

class GeminiAIClient:
    """Client for interacting with Google's Gemini AI API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash"):
        """
        Initialize the Gemini AI client.
        
        Args:
            api_key: The API key for Gemini. If None, will try to get from environment.
            model: The model to use for generation.
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable.")
        
        self.model = model
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}"
    
    def generate_resume_content(self, 
                               personal_info: Dict[str, str],
                               experience: List[Dict[str, str]],
                               education: List[Dict[str, str]],
                               skills: List[str],
                               job_target: str) -> Dict[str, str]:
        """
        Generate resume content based on user inputs.
        
        Args:
            personal_info: Dictionary containing name, email, phone, etc.
            experience: List of work experiences with company, title, dates, description
            education: List of education entries with institution, degree, dates
            skills: List of skills
            job_target: Target job or industry
            
        Returns:
            Dictionary with resume sections (summary, experience, etc.)
        """
        # Construct a detailed prompt for the AI
        prompt = self._construct_resume_prompt(
            personal_info, experience, education, skills, job_target
        )
        
        # Call the API and process the response
        response = self._call_gemini_api(prompt)
        
        # Parse and structure the response
        return self._parse_resume_response(response)
    
    def generate_cover_letter(self,
                             personal_info: Dict[str, str],
                             job_details: Dict[str, str],
                             experience_highlights: List[str],
                             skills_highlights: List[str],
                             tone: str = "professional") -> str:
        """
        Generate a cover letter based on user inputs.
        
        Args:
            personal_info: Dictionary with name, contact info
            job_details: Dictionary with job title, company, requirements
            experience_highlights: Key experiences to highlight
            skills_highlights: Key skills to highlight
            tone: Desired tone (professional, enthusiastic, etc.)
            
        Returns:
            Formatted cover letter text
        """
        # Construct the prompt
        prompt = self._construct_cover_letter_prompt(
            personal_info, job_details, experience_highlights, skills_highlights, tone
        )
        
        # Call the API
        response = self._call_gemini_api(prompt)
        
        # Process and return the cover letter text
        return self._parse_cover_letter_response(response)
    
    def _construct_resume_prompt(self,
                               personal_info: Dict[str, str],
                               experience: List[Dict[str, str]],
                               education: List[Dict[str, str]],
                               skills: List[str],
                               job_target: str) -> str:
        """Construct a detailed prompt for resume generation."""
        # Format the experience and education entries
        experience_text = "\n".join([
            f"- {exp.get('title')} at {exp.get('company')} ({exp.get('dates', '')}): {exp.get('description', '')}"
            for exp in experience
        ])
        
        education_text = "\n".join([
            f"- {edu.get('degree')} from {edu.get('institution')} ({edu.get('dates', '')})"
            for edu in education
        ])
        
        skills_text = ", ".join(skills)
        
        # Construct the full prompt with clear instructions
        prompt = f"""
        Generate a professional resume for {personal_info.get('name')} targeting a position as {job_target}.
        
        Personal Information:
        - Name: {personal_info.get('name')}
        - Email: {personal_info.get('email')}
        - Phone: {personal_info.get('phone')}
        - Location: {personal_info.get('location', '')}
        - LinkedIn: {personal_info.get('linkedin', '')}
        
        Work Experience:
        {experience_text}
        
        Education:
        {education_text}
        
        Skills:
        {skills_text}
        
        Please create a complete resume with the following sections:
        1. A concise, impactful professional summary (3-4 sentences)
        2. Work experience with bullet points highlighting achievements and responsibilities
        3. Education section
        4. Skills section organized by category
        5. Any additional relevant sections
        
        Make the content ATS-friendly with relevant keywords for {job_target}.
        Focus on quantifiable achievements and results where possible.
        Keep the language professional and impactful.
        Format the response as a JSON object with sections as keys.
        """
        
        return prompt
    
    def _construct_cover_letter_prompt(self,
                                     personal_info: Dict[str, str],
                                     job_details: Dict[str, str],
                                     experience_highlights: List[str],
                                     skills_highlights: List[str],
                                     tone: str) -> str:
        """Construct a detailed prompt for cover letter generation."""
        experience_text = "\n".join([f"- {exp}" for exp in experience_highlights])
        skills_text = "\n".join([f"- {skill}" for skill in skills_highlights])
        
        prompt = f"""
        Generate a professional cover letter for {personal_info.get('name')} applying for the position of 
        {job_details.get('title')} at {job_details.get('company')}.
        
        Personal Information:
        - Name: {personal_info.get('name')}
        - Email: {personal_info.get('email')}
        - Phone: {personal_info.get('phone')}
        
        Job Details:
        - Position: {job_details.get('title')}
        - Company: {job_details.get('company')}
        - Job Requirements: {job_details.get('requirements', '')}
        
        Key Experience to Highlight:
        {experience_text}
        
        Key Skills to Highlight:
        {skills_text}
        
        Tone: {tone}
        
        Please create a well-structured cover letter with:
        1. Professional greeting and strong opening paragraph
        2. Body paragraphs that connect experience to job requirements
        3. A closing paragraph with call to action
        4. Professional sign-off
        
        The letter should be approximately 300-400 words, demonstrate enthusiasm for the role,
        and highlight the candidate's fit for the position. Avoid generic language and focus on
        specific qualifications that match the job.
        """
        
        return prompt
    
    def _call_gemini_api(self, prompt: str) -> Dict[str, Any]:
        """
        Call the Gemini API with the given prompt.
        
        Args:
            prompt: The text prompt to send to the API
            
        Returns:
            The API response as a dictionary
        """
        url = f"{self.base_url}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.4,
                "topK": 32,
                "topP": 0.95,
                "maxOutputTokens": 2048,
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            # Log the error and raise a more user-friendly exception
            print(f"Error calling Gemini API: {str(e)}")
            raise Exception(f"Failed to generate content: {str(e)}")
    
    def _parse_resume_response(self, response: Dict[str, Any]) -> Dict[str, str]:
        """
        Parse the Gemini API response for resume content.
        
        Args:
            response: The raw API response
            
        Returns:
            Dictionary with structured resume sections
        """
        try:
            # Extract the text from the response
            text = response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            
            # Try to parse as JSON if the model returned JSON
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                # If not JSON, parse the text into sections
                sections = {}
                current_section = None
                current_content = []
                
                for line in text.split("\n"):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Check if this is a section header
                    if line.endswith(":") or any(line.startswith(h) for h in ["#", "##", "###"]):
                        # Save the previous section if it exists
                        if current_section and current_content:
                            sections[current_section] = "\n".join(current_content)
                            current_content = []
                        
                        # Set the new section
                        current_section = line.strip("#: ")
                    else:
                        # Add to the current section content
                        if current_section:
                            current_content.append(line)
                
                # Add the last section
                if current_section and current_content:
                    sections[current_section] = "\n".join(current_content)
                
                return sections
        except Exception as e:
            # Fallback for any parsing errors
            print(f"Error parsing Gemini response: {str(e)}")
            return {"error": "Failed to parse the generated content. Please try again."}
    
    def _parse_cover_letter_response(self, response: Dict[str, Any]) -> str:
        """
        Parse the Gemini API response for cover letter content.
        
        Args:
            response: The raw API response
            
        Returns:
            Formatted cover letter text
        """
        try:
            # Extract the text from the response
            text = response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            
            # Clean up the text (remove extra whitespace, etc.)
            lines = [line.strip() for line in text.split("\n")]
            cleaned_text = "\n\n".join([line for line in lines if line])
            
            return cleaned_text
        except Exception as e:
            # Fallback for any parsing errors
            print(f"Error parsing Gemini response: {str(e)}")
            return "Failed to generate cover letter. Please try again."
