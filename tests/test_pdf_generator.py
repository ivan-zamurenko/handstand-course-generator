import unittest
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.course_generator.generator import CourseGenerator
from src.pdf_generator.generator import PDFGenerator

class TestPDFGenerator(unittest.TestCase):
    def setUp(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.vocabulary_path = os.path.join(project_root, "data", "exercises", "vocabulary.json")
        self.templates_path = os.path.join(project_root, "data", "exercises", "program_templates.json")
        self.output_path = os.path.join(project_root, "test_course.pdf")

    def test_generate_pdf(self):
        """Test that a PDF is generated successfully."""
        # Generate a course
        generator = CourseGenerator(self.vocabulary_path, self.templates_path)
        course = generator.generate_course("Test Course", 3, "beginner_handstand")
        
        # Generate PDF
        pdf_generator = PDFGenerator(self.output_path)
        pdf_generator.generate_pdf(course)
        
        # Check that the file was created
        self.assertTrue(os.path.exists(self.output_path))
        
        # Check that the file is not empty
        self.assertGreater(os.path.getsize(self.output_path), 0)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

if __name__ == '__main__':
    unittest.main()
