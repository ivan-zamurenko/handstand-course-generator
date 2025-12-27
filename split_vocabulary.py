#!/usr/bin/env python3
"""
Split master vocabulary.json into individual exercise.json files
Creates exercise.json in each exercise's folder
"""

import json
from pathlib import Path

def split_vocabulary():
    # Load the master vocabulary.json file
    json_path = Path(__file__).parent / "data" / "exercises" / "vocabulary.json"
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Base directory for exercises
    base_dir = Path(__file__).parent / "data" / "exercises"
    
    # Track statistics
    files_created = 0
    
    # Create individual exercise.json files
    for exercise in data['exercises']:
        category = exercise['category']
        name = exercise['name']
        
        # Create path to exercise folder
        exercise_path = base_dir / category / name
        exercise_file = exercise_path / "exercise.json"
        
        # Write individual exercise.json
        with open(exercise_file, 'w', encoding='utf-8') as f:
            json.dump(exercise, f, indent=4, ensure_ascii=False)
        
        files_created += 1
        print(f"Created: {category}/{name}/exercise.json")
    
    print(f"\n✅ Done!")
    print(f"📄 Exercise files created: {files_created}")

if __name__ == "__main__":
    split_vocabulary()
