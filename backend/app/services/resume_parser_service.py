import os
import re
from typing import Dict, Any, List, Tuple
from pathlib import Path
import json

# Document parsing
from pdfminer.high_level import extract_text as pdf_extract_text
from docx import Document
import pytesseract
from PIL import Image

# NLP for text processing
import numpy as np


class ResumeParserService:
    def __init__(self):
        self.skills_database = self._load_skills_database()

    def _load_skills_database(self) -> Dict[str, List[str]]:
        """Load predefined skills database with synonyms"""
        return {
            "programming": [
                "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
                "php", "ruby", "swift", "kotlin", "scala", "r", "matlab", "sql"
            ],
            "web_development": [
                "html", "css", "react", "angular", "vue", "nodejs", "express", "django",
                "flask", "spring", "laravel", "rails", "nextjs", "nuxtjs"
            ],
            "databases": [
                "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "cassandra",
                "oracle", "sqlite", "dynamodb", "firebase"
            ],
            "cloud": [
                "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
                "jenkins", "gitlab", "github actions"
            ],
            "data_science": [
                "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
                "spark", "hadoop", "tableau", "powerbi", "jupyter"
            ],
            "mobile": [
                "android", "ios", "react native", "flutter", "xamarin", "ionic",
                "swift", "kotlin", "objective-c"
            ]
        }

    async def parse_resume(self, file_path: str) -> Tuple[str, Dict[str, Any]]:
        """Parse resume and extract text and structured data"""
        # Extract text from file
        text = await self._extract_text(file_path)

        # Parse structured data
        structured_data = await self._parse_structured_data(text)

        return text, structured_data

    async def _extract_text(self, file_path: str) -> str:
        """Extract text from PDF or DOCX file"""
        file_extension = Path(file_path).suffix.lower()

        try:
            if file_extension == '.pdf':
                text = pdf_extract_text(file_path)
                # If text extraction failed (scanned PDF), use OCR
                if not text.strip():
                    text = await self._ocr_extract_text(file_path)
            elif file_extension in ['.docx', '.doc']:
                doc = Document(file_path)
                text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")

            return text.strip()

        except Exception as e:
            # Fallback to OCR if parsing fails
            print(f"Text extraction failed, trying OCR: {e}")
            return await self._ocr_extract_text(file_path)

    async def _ocr_extract_text(self, file_path: str) -> str:
        """Extract text using OCR (for scanned documents)"""
        try:
            # Convert PDF to images if needed
            if file_path.endswith('.pdf'):
                # This would require pdf2image library
                # For now, return empty string as fallback
                return ""

            # OCR for image files
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text.strip()

        except Exception as e:
            print(f"OCR extraction failed: {e}")
            return ""

    async def _parse_structured_data(self, text: str) -> Dict[str, Any]:
        """Parse structured data from resume text"""
        structured_data = {
            "skills": await self._extract_skills(text),
            "experience_years": await self._extract_experience_years(text),
            "education": await self._extract_education(text),
            "certifications": await self._extract_certifications(text),
            "previous_roles": await self._extract_previous_roles(text),
            "summary": await self._extract_summary(text)
        }

        return structured_data

    async def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        text_lower = text.lower()
        found_skills = []

        # Search for skills from database
        for category, skills in self.skills_database.items():
            for skill in skills:
                # Use regex to find whole words
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.append(skill)

        # Remove duplicates and return
        return list(set(found_skills))

    async def _extract_experience_years(self, text: str) -> int:
        """Extract years of experience from text"""
        # Look for patterns like "5 years of experience", "3+ years", etc.
        patterns = [
            r'(\d+)\+?\s*years?\s*of\s*experience',
            r'(\d+)\+?\s*years?\s*experience',
            r'experience\s*:?\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s*exp',
        ]

        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(match) for match in matches])

        # Return the maximum years found, or 0 if none
        return max(years) if years else 0

    async def _extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education_keywords = [
            "bachelor", "master", "phd", "doctorate", "mba", "bsc", "msc",
            "bachelor's", "master's", "university", "college", "degree"
        ]

        education = []
        lines = text.split('\n')

        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                # Clean and add the education line
                clean_line = line.strip()
                if clean_line and len(clean_line) > 10:  # Filter out short matches
                    education.append(clean_line)

        return education[:3]  # Return top 3 education entries

    async def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        cert_patterns = [
            r'certified\s+(.+?)(?:\n|$)',
            r'certification\s*:?\s*(.+?)(?:\n|$)',
            r'cert\.\s*(.+?)(?:\n|$)',
        ]

        certifications = []
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            certifications.extend([match.strip() for match in matches])

        return certifications[:5]  # Return top 5 certifications

    async def _extract_previous_roles(self, text: str) -> List[str]:
        """Extract previous job roles/titles"""
        # Common job title patterns
        role_patterns = [
            r'(software engineer|developer|programmer|analyst|manager|director|lead|senior|junior|intern)',
            r'(data scientist|product manager|project manager|tech lead|architect|consultant)',
            r'(designer|researcher|specialist|coordinator|administrator|executive)'
        ]

        roles = []
        for pattern in role_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            roles.extend(matches)

        # Remove duplicates and return
        return list(set(roles))[:5]

    async def _extract_summary(self, text: str) -> str:
        """Extract summary/objective section"""
        summary_keywords = ["summary", "objective", "profile", "about"]

        lines = text.split('\n')
        summary_lines = []
        capturing = False

        for i, line in enumerate(lines):
            line_lower = line.lower().strip()

            # Check if this line starts a summary section
            if any(keyword in line_lower for keyword in summary_keywords):
                capturing = True
                # Skip the header line itself
                continue

            if capturing:
                # Stop capturing if we hit another section
                if line.strip() and (
                    line_lower.startswith(('experience', 'education', 'skills', 'work'))
                    or line.isupper()
                ):
                    break

                # Add non-empty lines to summary
                if line.strip():
                    summary_lines.append(line.strip())

        summary_text = ' '.join(summary_lines)
        # Return first 300 characters
        return summary_text[:300] + "..." if len(summary_text) > 300 else summary_text

    async def create_chunks(self, text: str, chunk_size: int = 400, overlap: int = 50) -> List[Dict[str, Any]]:
        """Split resume text into chunks for embeddings"""
        # Split text into sections first
        sections = await self._split_into_sections(text)

        chunks = []
        for section_name, section_text in sections.items():
            # Split each section into smaller chunks
            words = section_text.split()
            for i in range(0, len(words), chunk_size - overlap):
                chunk_words = words[i:i + chunk_size]
                chunk_text = ' '.join(chunk_words)

                if len(chunk_text.strip()) > 50:  # Only include meaningful chunks
                    chunks.append({
                        "text": chunk_text,
                        "type": section_name,
                        "word_count": len(chunk_words)
                    })

        return chunks

    async def _split_into_sections(self, text: str) -> Dict[str, str]:
        """Split resume into logical sections"""
        sections = {
            "summary": "",
            "experience": "",
            "education": "",
            "skills": "",
            "other": ""
        }

        lines = text.split('\n')
        current_section = "other"

        section_keywords = {
            "summary": ["summary", "objective", "profile", "about"],
            "experience": ["experience", "work", "employment", "career", "professional"],
            "education": ["education", "academic", "degree", "university", "college"],
            "skills": ["skills", "technical", "competencies", "technologies", "tools"]
        }

        for line in lines:
            line_clean = line.strip()
            if not line_clean:
                continue

            line_lower = line_clean.lower()

            # Check if this line indicates a new section
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    current_section = section
                    break

            # Add line to current section
            sections[current_section] += line_clean + " "

        # Clean up sections
        for section in sections:
            sections[section] = sections[section].strip()

        return sections