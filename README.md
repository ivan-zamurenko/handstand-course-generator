# Handstand Course Generator

This project is a Python application that dynamically generates personalized handstand training programs. It creates PDF workout plans based on a library of exercises, allowing for progressive overload and customization.

## Features

- **Dynamic Course Generation**: Create courses of varying lengths (e.g., 21-day, 30-day).
- **Exercise Vocabulary System**: Centralized exercise library with unique IDs, difficulty levels, equipment requirements, and muscle group targeting.
- **Multiple Difficulty Levels**: Choose from Beginner, Intermediate, or Advanced templates.
- **Progressive Overload**: The program automatically increases the difficulty and volume of workouts over time (up to 50% by the end).
- **PDF Output**: Generates a professional-looking PDF of the course for easy printing and use.
- **Customizable Sessions**: Each training session is structured into sections like Warmup, Pre-hab, Shoulder Opener, Handstand, Conditioning, and Stretching.
- **Scalable Architecture**: Easy to add new exercises and create custom program templates.

## Project Structure
```
course_creater/
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   └── exercises/
│       ├── vocabulary.json          # All exercises with metadata
│       └── program_templates.json   # Program templates by difficulty
├── src/
│   ├── main.py
│   ├── course_generator/
│   │   ├── __init__.py
│   │   ├── models.py                # Exercise, Session, Course classes
│   │   └── generator.py             # Course generation logic
│   └── pdf_generator/
│       ├── __init__.py
│       └── generator.py             # PDF creation logic
└── tests/
    ├── __init__.py
    ├── test_course_generator.py
    └── test_pdf_generator.py
```

## Architecture

### Exercise Vocabulary
All exercises are defined in `data/exercises/vocabulary.json` with the following attributes:
- **ID**: Unique identifier (e.g., `handstand_001`)
- **Name**: Exercise name
- **Description**: Detailed instructions
- **Default sets/reps**: Starting point for progression
- **Difficulty**: beginner, intermediate, or advanced
- **Equipment**: Required equipment
- **Muscle groups**: Primary muscles targeted

### Program Templates
Templates in `data/exercises/program_templates.json` define which exercises belong to each section and difficulty level. This allows:
- ✅ **Reusability**: Same exercise can appear in multiple programs
- ✅ **Easy maintenance**: Update exercises in one place
- ✅ **Scalability**: Add hundreds of exercises without duplication

## How to Use

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Program**:
    ```bash
    python src/main.py
    ```
    You'll be prompted to:
    - Enter course name (or use default)
    - Choose number of days
    - Select difficulty level (1=Beginner, 2=Intermediate, 3=Advanced)

3.  **Output**: A PDF file will be generated in the root directory.

## Adding New Exercises

1. Add exercise definition to `data/exercises/vocabulary.json`
2. Reference the exercise ID in `data/exercises/program_templates.json` under the appropriate section
3. The exercise is now available for course generation!

## Running Tests

```bash
python -m pytest tests/ -v
```
