import unittest
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.course_generator.generator import CourseGenerator
from src.course_generator.models import Course

class TestCourseGenerator(unittest.TestCase):
    def setUp(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.vocabulary_path = os.path.join(project_root, "data", "exercises", "vocabulary.json")
        self.templates_path = os.path.join(project_root, "data", "exercises", "program_templates.json")
        self.generator = CourseGenerator(self.vocabulary_path, self.templates_path)

    def test_load_vocabulary(self):
        """Test that the vocabulary loads correctly."""
        self.assertIsNotNone(self.generator.exercise_vocabulary)
        self.assertIn("warmup_001", self.generator.exercise_vocabulary)
        self.assertIn("handstand_001", self.generator.exercise_vocabulary)
    
    def test_load_templates(self):
        """Test that templates load correctly."""
        self.assertIsNotNone(self.generator.program_templates)
        self.assertIn("beginner_handstand", self.generator.program_templates)
        self.assertIn("intermediate_handstand", self.generator.program_templates)

    def test_generate_course(self):
        """Test that a course is generated correctly."""
        course = self.generator.generate_course("Test Course", 7)
        
        self.assertIsInstance(course, Course)
        self.assertEqual(course.name, "Test Course")
        self.assertEqual(course.days, 7)
        self.assertEqual(len(course.sessions), 7)

    def test_progressive_overload(self):
        """Test that progressive overload is applied."""
        course = self.generator.generate_course("Progressive Test", 10)
        
        # Check that later sessions have more sets than earlier ones
        first_session = course.sessions[0]
        last_session = course.sessions[-1]
        
        # Get the first exercise from the first section of each session
        first_section_name = list(first_session.sections.keys())[0]
        first_exercise_day1 = first_session.sections[first_section_name][0]
        
        last_section_name = list(last_session.sections.keys())[0]
        last_exercise_day10 = last_session.sections[last_section_name][0]
        
        # The last session should have more or equal sets than the first
        self.assertGreaterEqual(last_exercise_day10.sets, first_exercise_day1.sets)

if __name__ == '__main__':
    unittest.main()
