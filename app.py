"""
Main application file for the Resume & Cover Letter Generator.
Defines routes, views, and application logic.
"""
import os
import json
from datetime import datetime
from flask import (
    Flask, render_template, request, jsonify,
    send_file, redirect, url_for, flash, session
)
from werkzeug.utils import secure_filename
from config import config
from utils.ai_helpers import GeminiAIClient
# PDF generation will be implemented in a future update
# from utils.pdf_generator import PDFGenerator

# Initialize Flask application
app = Flask(__name__)

# Load configuration based on environment
config_name = os.environ.get('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])

# Set secret key for session
app.secret_key = app.config.get('SECRET_KEY', 'dev-key-for-development-only')

# Initialize services
ai_client = None  # Will be initialized when API key is available
# PDF generation will be implemented in a future update
# pdf_generator = PDFGenerator()

# Routes
@app.route('/')
def index():
    """Render the landing page."""
    return render_template('index.html')

@app.route('/resume-builder')
def resume_builder():
    """Render the resume builder page."""
    return render_template('resume_builder.html')

@app.route('/cover-letter-builder')
def cover_letter_builder():
    """Render the cover letter builder page."""
    return render_template('cover_letter_builder.html')

@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    """API endpoint to generate resume content."""
    try:
        # For demo purposes, return mock data
        mock_resume = {
            "summary": "Dedicated software engineer with experience in web development and AI integration. Skilled in Python, JavaScript, and modern frameworks. Passionate about creating user-friendly applications with clean, maintainable code.",
            "experience": "<p><strong>Software Engineer, Tech Solutions Inc.</strong> (2020-Present)</p><ul><li>Developed responsive web applications using modern JavaScript frameworks</li><li>Implemented RESTful APIs with Python Flask</li><li>Improved application performance by 40%</li></ul>",
            "education": "<p><strong>Bachelor of Science in Computer Science</strong></p><p>University of Technology, 2016-2020</p>",
            "skills": "<ul><li>Programming: Python, JavaScript, HTML/CSS</li><li>Frameworks: Flask, React, Bootstrap</li><li>Tools: Git, Docker, AWS</li></ul>"
        }

        # Store in session for PDF generation
        session['resume_data'] = {
            'content': mock_resume,
            'personal_info': request.json.get('personal_info', {'name': 'John Doe'}),
            'template': request.json.get('template', 'modern')
        }

        return jsonify({'success': True, 'resume': mock_resume})

    except Exception as e:
        app.logger.error(f"Error generating resume: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    """API endpoint to generate cover letter content."""
    try:
        # For demo purposes, return mock data
        mock_letter = """Dear Hiring Manager,

I am writing to express my interest in the Software Engineer position at Tech Innovations Inc. With my background in web development and experience with Python and JavaScript frameworks, I believe I would be a valuable addition to your team.

In my previous role at Tech Solutions, I developed responsive web applications and implemented RESTful APIs that improved system performance by 40%. My experience aligns perfectly with the requirements outlined in your job posting.

I am particularly excited about the opportunity to work on innovative projects that leverage AI technologies, as mentioned in your company profile. My recent work integrating machine learning models into web applications has prepared me well for this challenge.

Thank you for considering my application. I look forward to the possibility of discussing how my skills and experience can contribute to Tech Innovations Inc.'s continued success.

Sincerely,
John Doe"""

        # Store in session for PDF generation
        session['cover_letter_data'] = {
            'text': mock_letter,
            'personal_info': request.json.get('personal_info', {'name': 'John Doe'}),
            'job_info': request.json.get('job_details', {'title': 'Software Engineer', 'company': 'Tech Innovations Inc.'}),
            'template': request.json.get('template', 'modern')
        }

        return jsonify({'success': True, 'cover_letter': mock_letter})

    except Exception as e:
        app.logger.error(f"Error generating cover letter: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download-resume-pdf')
def download_resume_pdf():
    """Generate and download the resume as a text file (PDF generation to be implemented later)."""
    try:
        # Check if resume data exists in session
        if 'resume_data' not in session:
            flash('No resume data found. Please generate a resume first.')
            return redirect(url_for('resume_builder'))

        resume_data = session['resume_data']
        content = resume_data['content']
        personal_info = resume_data['personal_info']

        # Create a simple text version of the resume
        # Process HTML tags to plain text
        experience_text = content['experience']
        experience_text = experience_text.replace('<p>', '')
        experience_text = experience_text.replace('</p>', '\n')
        experience_text = experience_text.replace('<ul>', '')
        experience_text = experience_text.replace('</ul>', '')
        experience_text = experience_text.replace('<li>', '- ')
        experience_text = experience_text.replace('</li>', '\n')
        experience_text = experience_text.replace('<strong>', '')
        experience_text = experience_text.replace('</strong>', '')

        education_text = content['education']
        education_text = education_text.replace('<p>', '')
        education_text = education_text.replace('</p>', '\n')
        education_text = education_text.replace('<strong>', '')
        education_text = education_text.replace('</strong>', '')

        skills_text = content['skills']
        skills_text = skills_text.replace('<ul>', '')
        skills_text = skills_text.replace('</ul>', '')
        skills_text = skills_text.replace('<li>', '- ')
        skills_text = skills_text.replace('</li>', '\n')

        resume_text = f"""RESUME

Name: {personal_info.get('name', 'User')}
Email: {personal_info.get('email', '')}
Phone: {personal_info.get('phone', '')}
Location: {personal_info.get('location', '')}

PROFESSIONAL SUMMARY
{content['summary']}

EXPERIENCE
{experience_text}

EDUCATION
{education_text}

SKILLS
{skills_text}
"""

        # Create a temporary file
        temp_file_path = os.path.join(os.getcwd(), 'temp_resume.txt')
        with open(temp_file_path, 'w') as f:
            f.write(resume_text)

        # Generate a filename
        filename = f"Resume_{secure_filename(personal_info.get('name', 'User'))}_{datetime.now().strftime('%Y%m%d')}.txt"

        # Send the file
        return send_file(
            temp_file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )

    except Exception as e:
        app.logger.error(f"Error generating text file: {str(e)}")
        flash(f"Error generating file: {str(e)}")
        return redirect(url_for('resume_builder'))

@app.route('/download-cover-letter-pdf')
def download_cover_letter_pdf():
    """Generate and download the cover letter as a text file (PDF generation to be implemented later)."""
    try:
        # Check if cover letter data exists in session
        if 'cover_letter_data' not in session:
            flash('No cover letter data found. Please generate a cover letter first.')
            return redirect(url_for('cover_letter_builder'))

        cover_letter_data = session['cover_letter_data']
        text = cover_letter_data['text']
        personal_info = cover_letter_data['personal_info']
        job_info = cover_letter_data['job_info']

        # Create a simple text version of the cover letter
        cover_letter_text = f"""{personal_info.get('name', 'User')}
{personal_info.get('email', '')}
{personal_info.get('phone', '')}
{personal_info.get('location', '')}

Date: {datetime.now().strftime('%B %d, %Y')}

{job_info.get('company', 'Company Name')}
Re: Application for {job_info.get('title', 'Position')}

{text}
"""

        # Create a temporary file
        temp_file_path = os.path.join(os.getcwd(), 'temp_cover_letter.txt')
        with open(temp_file_path, 'w') as f:
            f.write(cover_letter_text)

        # Generate a filename
        filename = f"CoverLetter_{secure_filename(personal_info.get('name', 'User'))}_{datetime.now().strftime('%Y%m%d')}.txt"

        # Send the file
        return send_file(
            temp_file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )

    except Exception as e:
        app.logger.error(f"Error generating text file: {str(e)}")
        flash(f"Error generating file: {str(e)}")
        return redirect(url_for('cover_letter_builder'))

@app.route('/api/hello')
def hello():
    """Simple API test endpoint."""
    return jsonify({"message": "Hello from the Resume & Cover Letter Generator!"})

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')

@app.route('/privacy-policy')
def privacy_policy():
    """Render the privacy policy page."""
    return render_template('privacy_policy.html')

@app.route('/terms-of-service')
def terms_of_service():
    """Render the terms of service page."""
    return render_template('terms_of_service.html')

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
