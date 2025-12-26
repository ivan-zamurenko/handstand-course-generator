from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import sys
import os

# Add parent directory to path to import from course_generator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from course_generator.models import Course

class PDFGenerator:
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.doc = SimpleDocTemplate(output_path, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.story = []
        
        # Create custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        self.section_style = ParagraphStyle(
            'SectionHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#16A085'),
            spaceAfter=8,
            spaceBefore=8
        )

    def generate_pdf(self, course: Course):
        """Generate a PDF from the course."""
        
        # Title page
        self.story.append(Paragraph(course.name, self.title_style))
        self.story.append(Spacer(1, 0.5 * inch))
        self.story.append(Paragraph(f"{course.days}-Day Program", self.styles['Normal']))
        self.story.append(PageBreak())
        
        # Add each session
        for session in course.sessions:
            self.add_session(session)
            self.story.append(PageBreak())
        
        # Build the PDF
        self.doc.build(self.story)

    def add_session(self, session):
        """Add a session to the PDF."""
        # Session title
        self.story.append(Paragraph(session.name, self.heading_style))
        self.story.append(Spacer(1, 0.2 * inch))
        
        # Add each section
        for section_name, exercises in session.sections.items():
            self.story.append(Paragraph(section_name, self.section_style))
            
            # Create a table for exercises
            table_data = []
            table_data.append(['Exercise', 'Description', 'Sets', 'Reps'])
            
            for exercise in exercises:
                table_data.append([
                    exercise.name,
                    exercise.description[:50] + '...' if len(exercise.description) > 50 else exercise.description,
                    str(exercise.sets),
                    exercise.reps
                ])
            
            # Create and style the table
            table = Table(table_data, colWidths=[2*inch, 3*inch, 0.7*inch, 1.3*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            self.story.append(table)
            self.story.append(Spacer(1, 0.3 * inch))
