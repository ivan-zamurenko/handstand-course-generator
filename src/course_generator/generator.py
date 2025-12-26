import json
import random
import os
from typing import List, Dict
from .models import Exercise, Session, Course

class CourseGenerator:
    def __init__(self, vocabulary_path: str, templates_path: str):
        self.vocabulary_path = vocabulary_path
        self.templates_path = templates_path
        self.exercise_vocabulary = self.load_vocabulary()
        self.program_templates = self.load_templates()

    def load_vocabulary(self) -> Dict[str, Exercise]:
        """Load the exercise vocabulary from a JSON file."""
        with open(self.vocabulary_path, 'r') as f:
            data = json.load(f)

        vocabulary = {}
        for ex in data['exercises']:
            exercise = Exercise(
                exercise_id=ex['id'],
                name=ex['name'],
                description=ex['description'],
                sets=ex['default_sets'],
                reps=ex['default_reps'],
                difficulty=ex.get('difficulty'),
                equipment=ex.get('equipment'),
                primary_muscle_groups=ex.get('primary_muscle_groups', []),
                image=ex.get('image')
            )
            vocabulary[ex['id']] = exercise
        
        return vocabulary

    def load_templates(self) -> Dict:
        """Load the program templates from a JSON file."""
        with open(self.templates_path, 'r') as f:
            data = json.load(f)
        return data['program_templates']

    def generate_course(self, name: str, days: int, template_name: str = "beginner_handstand") -> Course:
        """Generate a course with progressive overload."""
        course = Course(name, days)
        
        # Get the template
        if template_name not in self.program_templates:
            raise ValueError(f"Template '{template_name}' not found. Available: {list(self.program_templates.keys())}")
        
        template = self.program_templates[template_name]
        sections_config = template['sections']
        
        # Define the sections in the order they should appear in each session
        sections = ["Warmup", "Prehab", "Shoulder Opener", "Handstand", "Conditioning", "Stretching"]
        
        for day in range(1, days + 1):
            session_sections = {}
            
            for section in sections:
                if section in sections_config:
                    config = sections_config[section]
                    exercise_ids = config['exercise_ids']
                    min_ex = config.get('min_exercises', 1)
                    max_ex = config.get('max_exercises', 2)
                    
                    # Select random number of exercises
                    num_exercises = min(len(exercise_ids), random.randint(min_ex, max_ex))
                    selected_ids = random.sample(exercise_ids, num_exercises)
                    
                    # Apply progressive overload: increase sets and reps as the course progresses
                    modified_exercises = []
                    for ex_id in selected_ids:
                        if ex_id not in self.exercise_vocabulary:
                            continue
                        
                        base_ex = self.exercise_vocabulary[ex_id]
                        
                        # Calculate the progression factor
                        progression = 1 + (day - 1) / days * 0.5  # Up to 50% increase by the end
                        
                        # Create a new exercise with modified sets
                        new_sets = max(1, int(base_ex.sets * progression))
                        
                        modified_ex = Exercise(
                            exercise_id=base_ex.exercise_id,
                            name=base_ex.name,
                            description=base_ex.description,
                            sets=new_sets,
                            reps=base_ex.reps,
                            difficulty=base_ex.difficulty,
                            equipment=base_ex.equipment,
                            primary_muscle_groups=base_ex.primary_muscle_groups,
                            image=base_ex.image
                        )
                        modified_exercises.append(modified_ex)
                    
                    session_sections[section] = modified_exercises
            
            session = Session(f"Day {day}", session_sections)
            course.add_session(session)
        
        return course

    def save_course_to_json(self, course: Course, output_path: str):
        """Save the course to a JSON file."""
        course.to_json(output_path)
