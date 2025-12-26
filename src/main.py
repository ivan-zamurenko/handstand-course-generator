import os
from course_generator.generator import CourseGenerator
from pdf_generator.generator import PDFGenerator

def main():
    print("🤸 Handstand Course Generator 🤸")
    print("=" * 50)
    
    # Get user input
    course_name = input("Enter course name (default: '21-Day Handstand Challenge'): ").strip()
    if not course_name:
        course_name = "21-Day Handstand Challenge"
    
    try:
        days = int(input("Enter number of days (default: 21): ").strip() or "21")
    except ValueError:
        print("Invalid input. Using default: 21 days")
        days = 21
    
    # Select difficulty level
    print("\nSelect difficulty level:")
    print("1. Beginner (beginner_handstand)")
    print("2. Intermediate (intermediate_handstand)")
    print("3. Advanced (advanced_handstand)")
    difficulty_choice = input("Enter choice (default: 1): ").strip() or "1"
    
    difficulty_map = {
        "1": "beginner_handstand",
        "2": "intermediate_handstand",
        "3": "advanced_handstand"
    }
    template_name = difficulty_map.get(difficulty_choice, "beginner_handstand")
    
    print(f"\nGenerating {days}-day course: '{course_name}' (Level: {template_name})...")
    
    # Get the absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    vocabulary_path = os.path.join(project_root, "data", "exercises", "vocabulary.json")
    templates_path = os.path.join(project_root, "data", "exercises", "program_templates.json")
    
    # Generate the course
    generator = CourseGenerator(vocabulary_path, templates_path)
    course = generator.generate_course(course_name, days, template_name)
    
    print(f"✓ Course generated with {len(course.sessions)} sessions")
    
    # Generate PDF
    output_path = os.path.join(project_root, "handstand_course.pdf")
    pdf_generator = PDFGenerator(output_path)
    pdf_generator.generate_pdf(course)
    
    print(f"✓ PDF generated: {output_path}")
    print("\n✨ Course generation complete! ✨")

if __name__ == "__main__":
    main()
