#!/usr/bin/env python3
"""
Simple script to create folder structure for exercises based on vocabulary.json
Creates: data/exercises/<Category>/<Exercise Name>/
"""

import json
import os
from pathlib import Path

def create_exercise_folders():
    # Load the vocabulary.json file
    json_path = Path(__file__).parent / "data" / "exercises" / "vocabulary.json"
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Base directory for exercises
    base_dir = Path(__file__).parent / "data" / "exercises"
    
    # Track statistics
    categories_created = set()
    exercises_created = 0
    
    # Create folders for each exercise
    for exercise in data['exercises']:
        category = exercise['category']
        name = exercise['name']
        
        # Create category folder if it doesn't exist
        category_path = base_dir / category
        category_path.mkdir(parents=True, exist_ok=True)
        categories_created.add(category)
        
        # Create exercise folder
        exercise_path = category_path / name
        exercise_path.mkdir(parents=True, exist_ok=True)
        exercises_created += 1
        
        print(f"Created: {category}/{name}")
    
    print(f"\n✅ Done!")
    print(f"📁 Categories created: {len(categories_created)}")
    print(f"🏋️  Exercise folders created: {exercises_created}")
    print(f"\nCategories: {', '.join(sorted(categories_created))}")

if __name__ == "__main__":
    create_exercise_folders()
