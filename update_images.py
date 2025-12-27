#!/usr/bin/env python3
"""
Update exercise images by scanning exercise folders
Automatically detects images and updates exercise.json files with image paths
"""

import json
from pathlib import Path

def update_images():
    # Base directory for exercises
    base_dir = Path(__file__).parent / "data" / "exercises"
    
    # Image extensions to look for
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
    
    # Track statistics
    exercises_updated = 0
    images_found = 0
    
    # Scan all categories
    for category_path in base_dir.iterdir():
        if not category_path.is_dir() or category_path.name.startswith('.'):
            continue
        
        # Scan exercises in this category
        for exercise_path in category_path.iterdir():
            if not exercise_path.is_dir():
                continue
            
            exercise_file = exercise_path / "exercise.json"
            if not exercise_file.exists():
                continue
            
            # Find all images in this folder
            images = []
            for file in exercise_path.iterdir():
                if file.suffix.lower() in image_extensions:
                    # Store relative path from data/exercises/
                    relative_path = file.relative_to(base_dir)
                    images.append(str(relative_path))
                    images_found += 1
            
            # Read exercise data
            with open(exercise_file, 'r', encoding='utf-8') as f:
                exercise_data = json.load(f)
            
            # Update image field
            if images:
                # If multiple images, store as array, otherwise as string
                exercise_data['image'] = images if len(images) > 1 else images[0]
                exercises_updated += 1
                print(f"✓ {category_path.name}/{exercise_path.name}: {len(images)} image(s)")
            else:
                # No images found, set to null
                if exercise_data.get('image') is not None:
                    exercise_data['image'] = None
            
            # Write back
            with open(exercise_file, 'w', encoding='utf-8') as f:
                json.dump(exercise_data, f, indent=4, ensure_ascii=False)
    
    print(f"\n✅ Done!")
    print(f"🖼️  Images found: {images_found}")
    print(f"📄 Exercises updated: {exercises_updated}")
    print(f"\n💡 Tip: Run 'python build_vocabulary.py' to update the master file")

if __name__ == "__main__":
    update_images()
