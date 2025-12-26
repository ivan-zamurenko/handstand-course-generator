#!/usr/bin/env python3
"""
Interactive script to update exercise descriptions in vocabulary.json
Allows systematic review and updating of all exercise information
"""

import json
import os
from pathlib import Path

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_exercise(exercise, index, total):
    """Display exercise information clearly"""
    print(f"{Colors.CYAN}[{index}/{total}] Exercise: {Colors.BOLD}{exercise['name']}{Colors.ENDC}")
    print(f"{Colors.BLUE}ID:{Colors.ENDC} {exercise['id']}")
    print(f"{Colors.BLUE}Category:{Colors.ENDC} {exercise['category']}")
    print(f"{Colors.BLUE}Difficulty:{Colors.ENDC} {exercise['difficulty']}")
    print(f"{Colors.BLUE}Equipment:{Colors.ENDC} {exercise['equipment']}")
    print(f"{Colors.BLUE}Sets/Reps:{Colors.ENDC} {exercise['default_sets']} sets x {exercise['default_reps']}")
    print(f"{Colors.BLUE}Muscles:{Colors.ENDC} {', '.join(exercise['primary_muscle_groups'])}")
    print(f"\n{Colors.GREEN}Current Description:{Colors.ENDC}")
    print(f"  {exercise['description']}")
    print()

def get_exercise_suggestion(exercise):
    """Generate improved description suggestions based on exercise name and category"""
    name = exercise['name'].lower()
    category = exercise['category'].lower()
    
    # This is a knowledge base that could be expanded
    suggestions = {
        'wrist': 'Focus on gentle mobility, prevent injury, prepare for weight-bearing.',
        'plank': 'Maintain neutral spine, shoulders over wrists/elbows, squeeze glutes, brace core.',
        'hollow body': 'Press lower back to floor, lift shoulders and legs, arms extended by ears.',
        'bridge': 'Drive through heels, squeeze glutes at top, maintain neutral neck.',
        'handstand': 'Active shoulders (push away from ground), hollow body, tight core, pointed toes.',
        'crow': 'Knees high on triceps, lean forward, gaze forward, lift one foot at a time.',
        'l-sit': 'Depress shoulders, protract scapula, externally rotate arms, compress pike.',
        'pike push': 'Hips high, elbows track back, lower crown of head toward ground.',
        'shoulder': 'Move through full range of motion, focus on controlled movement.',
        'cat-cow': 'Inhale on cow (arch), exhale on cat (round), move with breath.',
        'downward dog': 'Push hips back and up, press palms down, lengthen spine, pedal feet.',
    }
    
    for key, suggestion in suggestions.items():
        if key in name:
            return f"💡 Suggestion: {suggestion}"
    
    if category in ['warmup']:
        return "💡 Include: Purpose (warm-up specific areas), tempo, and cardio benefits."
    elif category in ['prehab']:
        return "💡 Include: Injury prevention focus, which joints/tissues are protected, proper form."
    elif category in ['shoulder opener']:
        return "💡 Include: Range of motion goals, breathing cues, how it helps handstands."
    elif category in ['handstand']:
        return "💡 Include: Body alignment cues, where to look, common mistakes to avoid."
    elif category in ['conditioning']:
        return "💡 Include: Muscle engagement cues, tempo, how to scale difficulty."
    elif category in ['stretching']:
        return "💡 Include: Breathing instructions, target muscles, how deep to go."
    
    return "💡 Include: Detailed form cues, benefits, common mistakes, and modifications."

def update_description(exercise):
    """Interactive description update"""
    print(get_exercise_suggestion(exercise))
    print(f"\n{Colors.WARNING}Options:{Colors.ENDC}")
    print("  1. Enter new description")
    print("  2. Add ⚠️ (needs research)")
    print("  3. Keep current description")
    print("  4. Skip to next category")
    print("  5. Save and exit")
    
    choice = input(f"\n{Colors.BOLD}Choose option (1-5): {Colors.ENDC}").strip()
    
    if choice == '1':
        print(f"\n{Colors.GREEN}Enter new description (press Enter twice when done):{Colors.ENDC}")
        lines = []
        while True:
            line = input()
            if line == '' and lines and lines[-1] == '':
                lines.pop()  # Remove last empty line
                break
            lines.append(line)
        
        new_desc = ' '.join(lines).strip()
        if new_desc:
            exercise['description'] = new_desc
            return 'updated'
    
    elif choice == '2':
        if '⚠️' not in exercise['description']:
            exercise['description'] = '⚠️ ' + exercise['description']
        return 'marked'
    
    elif choice == '3':
        return 'kept'
    
    elif choice == '4':
        return 'skip_category'
    
    elif choice == '5':
        return 'exit'
    
    return 'kept'

def update_equipment(exercise):
    """Quick equipment check"""
    print(f"\n{Colors.BLUE}Update equipment? Current: {exercise['equipment']}{Colors.ENDC}")
    print("Press Enter to keep, or type new equipment:")
    new_equipment = input().strip()
    if new_equipment:
        exercise['equipment'] = new_equipment
        return True
    return False

# Update amount of sets/reps based on progression
def update_sets(exercise):
    """Offer to update default sets/reps"""
    print(f"\n{Colors.BLUE}Current sets/reps: {exercise['default_sets']} sets x {exercise['default_reps']}{Colors.ENDC}")
    print("Press Enter to keep, or type new sets (number) and reps (e.g., '3 10-15'):")
    inp = input().strip()
    if inp:
        parts = inp.split()
        if len(parts) == 2:
            try:
                new_sets = int(parts[0])
                new_reps = parts[1]
                exercise['default_sets'] = new_sets
                exercise['default_reps'] = new_reps
                return True
            except ValueError:
                print(f"{Colors.FAIL}Invalid input. Keeping current sets/reps.{Colors.ENDC}")
    return False

def main():
    # Load vocabulary
    vocab_path = Path(__file__).parent / 'data' / 'exercises' / 'vocabulary.json'
    
    if not vocab_path.exists():
        print(f"{Colors.FAIL}Error: vocabulary.json not found at {vocab_path}{Colors.ENDC}")
        return
    
    with open(vocab_path, 'r') as f:
        data = json.load(f)
    
    exercises = data['exercises']
    total = len(exercises)
    
    print_header("Exercise Description Update Tool")
    print(f"{Colors.GREEN}Total exercises: {total}{Colors.ENDC}")
    print(f"{Colors.WARNING}Review and update exercise descriptions systematically{Colors.ENDC}\n")
    
    # Option to filter by category
    categories = sorted(set(ex['category'] for ex in exercises))
    print(f"{Colors.CYAN}Categories:{Colors.ENDC} {', '.join(categories)}")
    print("\nFilter by category? (press Enter for all, or type category name):")
    filter_cat = input().strip()
    
    if filter_cat:
        exercises = [ex for ex in exercises if ex['category'].lower() == filter_cat.lower()]
        print(f"\n{Colors.GREEN}Filtered to {len(exercises)} exercises in '{filter_cat}'{Colors.ENDC}")
    
    # Track statistics
    stats = {
        'reviewed': 0,
        'updated': 0,
        'marked': 0,
        'kept': 0,
        'equipment_updated': 0
    }
    
    # Process exercises
    current_category = None
    for i, exercise in enumerate(exercises, 1):
        # Category header
        if exercise['category'] != current_category:
            current_category = exercise['category']
            print_header(f"Category: {current_category}")
        
        print_exercise(exercise, i, len(exercises))
        
        # Update description
        result = update_description(exercise)
        
        if result == 'exit':
            print(f"\n{Colors.WARNING}Saving and exiting...{Colors.ENDC}")
            break
        elif result == 'skip_category':
            # Skip to next category
            next_cat = None
            for ex in exercises[i:]:
                if ex['category'] != current_category:
                    next_cat = ex['category']
                    break
            if next_cat:
                print(f"\n{Colors.CYAN}Skipping to category: {next_cat}{Colors.ENDC}")
                continue
            else:
                print(f"\n{Colors.WARNING}No more categories. Saving...{Colors.ENDC}")
                break
        
        stats['reviewed'] += 1
        if result == 'updated':
            stats['updated'] += 1
            # Also offer equipment update
            if update_equipment(exercise):
                stats['equipment_updated'] += 1
        elif result == 'marked':
            stats['marked'] += 1
        elif result == 'kept':
            stats['kept'] += 1
    
    # Save updated data
    print(f"\n{Colors.GREEN}Saving changes...{Colors.ENDC}")
    with open(vocab_path, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    # Print statistics
    print_header("Update Summary")
    print(f"{Colors.CYAN}Exercises reviewed:{Colors.ENDC} {stats['reviewed']}")
    print(f"{Colors.GREEN}Descriptions updated:{Colors.ENDC} {stats['updated']}")
    print(f"{Colors.WARNING}Marked for research (⚠️):{Colors.ENDC} {stats['marked']}")
    print(f"{Colors.BLUE}Kept unchanged:{Colors.ENDC} {stats['kept']}")
    print(f"{Colors.CYAN}Equipment updated:{Colors.ENDC} {stats['equipment_updated']}")
    print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Changes saved to vocabulary.json{Colors.ENDC}\n")
    
    # Show exercises marked with warning
    marked_exercises = [ex for ex in exercises if '⚠️' in ex['description']]
    if marked_exercises:
        print(f"\n{Colors.WARNING}Exercises marked for research (⚠️):{Colors.ENDC}")
        for ex in marked_exercises:
            print(f"  • {ex['name']} ({ex['category']})")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Interrupted by user. Changes may not be saved.{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
