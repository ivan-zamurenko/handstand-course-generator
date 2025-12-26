import json
from typing import List, Dict, Optional

class Exercise:
    def __init__(self, name: str, description: str, sets: int, reps: str, 
                 exercise_id: str = None, category: str = None, difficulty: str = None, 
                 equipment: str = None, primary_muscle_groups: List[str] = None, 
                 image: str = None):
        self.exercise_id = exercise_id
        self.name = name
        self.description = description
        self.sets = sets
        self.reps = reps
        self.category = category
        self.difficulty = difficulty
        self.equipment = equipment
        self.primary_muscle_groups = primary_muscle_groups or []
        self.image = image

    def to_dict(self):
        return {
            "exercise_id": self.exercise_id,
            "name": self.name,
            "description": self.description,
            "sets": self.sets,
            "reps": self.reps,
            "category": self.category,
            "difficulty": self.difficulty,
            "equipment": self.equipment,
            "primary_muscle_groups": self.primary_muscle_groups,
            "image": self.image
        }

class Session:
    def __init__(self, name: str, sections: Dict[str, List[Exercise]]):
        self.name = name
        self.sections = sections

    def to_dict(self):
        return {
            "name": self.name,
            "sections": {section: [ex.to_dict() for ex in exercises] for section, exercises in self.sections.items()}
        }

class Course:
    def __init__(self, name: str, days: int):
        self.name = name
        self.days = days
        self.sessions: List[Session] = []

    def add_session(self, session: Session):
        self.sessions.append(session)

    def to_dict(self):
        return {
            "name": self.name,
            "days": self.days,
            "sessions": [session.to_dict() for session in self.sessions]
        }

    def to_json(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

