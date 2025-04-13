# AI Resume & Cover Letter Generator

A web-based SaaS tool that allows users to generate professional resumes and cover letters using Google's Gemini 2.0 Flash AI model. The tool is aimed at job seekers, students, and professionals who want to create high-quality application materials with ease.

## Features

- AI-generated resume builder with step-by-step form
- AI-generated cover letter with customizable options
- Real-time preview of resume/letter
- Multiple templates and export to PDF
- Mobile-first, responsive design
- SEO-optimized structure

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **AI Integration**: Google Gemini 2.0 Flash model
- **PDF Generation**: WeasyPrint
- **Deployment**: Render

## Local Development

1. Clone the repository:
   ```
   git clone https://github.com/irfanwhotf/flask.git
   cd flask
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Then edit the `.env` file with your actual configuration values.

5. Run the application:
   ```
   python app.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000`

## Project Structure

```
/
├── app.py              # Main application entry point
├── config.py           # Configuration management
├── requirements.txt    # Dependencies
├── static/             # Static assets
│   ├── css/            # Stylesheets
│   ├── js/             # Client-side scripts
│   └── images/         # Image assets
├── templates/          # Jinja2 templates
│   ├── index.html      # Landing page
│   ├── resume_builder.html # Resume builder
│   └── cover_letter_builder.html # Cover letter builder
└── utils/              # Utility functions
    ├── ai_helpers.py   # Gemini API interaction
    └── pdf_generator.py # PDF generation utilities
```

## Deployment

This application is configured for deployment on Render:

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Configure the service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add environment variables in the Render dashboard

## License

MIT
