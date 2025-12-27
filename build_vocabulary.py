#!/usr/bin/env python3
"""
Build master vocabulary.json from individual exercise.json files
Scans all exercise folders and combines them into vocabulary.json
"""

import json
from pathlib import Path

def build_vocabulary():
    # Base directory for exercises
    base_dir = Path(__file__).parent / "data" / "exercises"
    
    # Categories to scan (in preferred order)
    categories = ["Warmup", "Prehab", "Shoulder opener", "Handstand", "Conditioning", "Stretching"]
    
    exercises = []
    
    # Scan each category
    for category in categories:
        category_path = base_dir / category
        if not category_path.exists():
            continue
        
        # Find all exercise.json files in this category
        for exercise_file in sorted(category_path.glob("*/exercise.json")):
            with open(exercise_file, 'r', encoding='utf-8') as f:
                exercise_data = json.load(f)
                exercises.append(exercise_data)
            
            exercise_name = exercise_file.parent.name
            print(f"Added: {category}/{exercise_name}")
    
    # Create the master vocabulary structure
    vocabulary = {
        "exercises": exercises
    }
    
    # Write to vocabulary.json
    output_path = base_dir / "vocabulary.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vocabulary, f, indent=4, ensure_ascii=False)
    
    print(f"\n✅ Done!")
    print(f"📄 Total exercises: {len(exercises)}")
    print(f"💾 Saved to: {output_path}")

if __name__ == "__main__":
    build_vocabulary()
