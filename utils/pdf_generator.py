"""
Utility functions for generating PDF documents from resume and cover letter content.
Uses WeasyPrint for HTML to PDF conversion with customizable templates.
"""
import os
import tempfile
from typing import Dict, Any, Optional
import jinja2
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

class PDFGenerator:
    """Generate PDF documents from HTML templates."""
    
    def __init__(self, templates_dir: str = "templates"):
        """
        Initialize the PDF generator.
        
        Args:
            templates_dir: Directory containing the HTML templates
        """
        self.templates_dir = templates_dir
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
    
    def generate_resume_pdf(self, 
                          resume_data: Dict[str, Any], 
                          template_name: str = "resume_template.html",
                          output_path: Optional[str] = None) -> str:
        """
        Generate a PDF resume from the provided data.
        
        Args:
            resume_data: Dictionary containing resume sections
            template_name: Name of the HTML template to use
            output_path: Path to save the PDF (if None, uses a temp file)
            
        Returns:
            Path to the generated PDF file
        """
        # Render the HTML template with the resume data
        template = self.env.get_template(template_name)
        html_content = template.render(resume=resume_data)
        
        # Create a temporary file if no output path is provided
        if output_path is None:
            fd, output_path = tempfile.mkstemp(suffix='.pdf')
            os.close(fd)
        
        # Generate the PDF
        font_config = FontConfiguration()
        html = HTML(string=html_content)
        css = CSS(string=self._get_default_css(), font_config=font_config)
        
        html.write_pdf(output_path, stylesheets=[css], font_config=font_config)
        
        return output_path
    
    def generate_cover_letter_pdf(self,
                                cover_letter_text: str,
                                personal_info: Dict[str, str],
                                job_info: Dict[str, str],
                                template_name: str = "cover_letter_template.html",
                                output_path: Optional[str] = None) -> str:
        """
        Generate a PDF cover letter from the provided text.
        
        Args:
            cover_letter_text: The body text of the cover letter
            personal_info: Dictionary with name, contact info
            job_info: Dictionary with job title, company
            template_name: Name of the HTML template to use
            output_path: Path to save the PDF (if None, uses a temp file)
            
        Returns:
            Path to the generated PDF file
        """
        # Render the HTML template
        template = self.env.get_template(template_name)
        html_content = template.render(
            letter_text=cover_letter_text,
            personal_info=personal_info,
            job_info=job_info
        )
        
        # Create a temporary file if no output path is provided
        if output_path is None:
            fd, output_path = tempfile.mkstemp(suffix='.pdf')
            os.close(fd)
        
        # Generate the PDF
        font_config = FontConfiguration()
        html = HTML(string=html_content)
        css = CSS(string=self._get_default_css(), font_config=font_config)
        
        html.write_pdf(output_path, stylesheets=[css], font_config=font_config)
        
        return output_path
    
    def _get_default_css(self) -> str:
        """
        Get default CSS for PDF styling.
        
        Returns:
            CSS string for PDF styling
        """
        return """
            @page {
                size: letter;
                margin: 1cm;
            }
            body {
                font-family: 'Helvetica', 'Arial', sans-serif;
                font-size: 11pt;
                line-height: 1.4;
                color: #333;
            }
            h1 {
                font-size: 18pt;
                margin-bottom: 0.5cm;
                color: #2c3e50;
            }
            h2 {
                font-size: 14pt;
                margin-top: 0.5cm;
                margin-bottom: 0.3cm;
                color: #3498db;
                border-bottom: 1pt solid #eee;
                padding-bottom: 0.2cm;
            }
            .contact-info {
                font-size: 10pt;
                color: #555;
                margin-bottom: 0.5cm;
            }
            .section {
                margin-bottom: 0.5cm;
            }
            .watermark {
                position: fixed;
                bottom: 0.5cm;
                right: 0.5cm;
                font-size: 8pt;
                color: #aaa;
                opacity: 0.7;
            }
            .experience-item {
                margin-bottom: 0.3cm;
            }
            .experience-header {
                font-weight: bold;
            }
            .experience-date {
                float: right;
                color: #777;
            }
            ul {
                margin-top: 0.2cm;
                margin-bottom: 0.2cm;
                padding-left: 0.5cm;
            }
            li {
                margin-bottom: 0.1cm;
            }
        """
