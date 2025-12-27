# Exercise Database Management

This project uses a **hybrid system** for managing exercise data:

- **Individual files**: Each exercise has its own `exercise.json` in its folder
- **Master file**: `vocabulary.json` is auto-generated for fast querying
- **Images**: Auto-detected and linked to exercises

## 📁 Folder Structure

```
data/exercises/
├── vocabulary.json          # Master file (auto-generated)
├── Warmup/
│   ├── Jumping Jacks/
│   │   ├── exercise.json   # Individual exercise data
│   │   ├── image1.jpg      # Exercise images
│   │   └── image2.jpg
│   └── ...
├── Prehab/
├── Shoulder opener/
├── Handstand/
├── Conditioning/
└── Stretching/
```

## 🔧 Management Scripts

### 1. **split_vocabulary.py**
Splits master `vocabulary.json` into individual `exercise.json` files.

```bash
python split_vocabulary.py
```

**When to use:** First time setup, or to distribute updates from master file.

---

### 2. **build_vocabulary.py**
Builds master `vocabulary.json` from all individual `exercise.json` files.

```bash
python build_vocabulary.py
```

**When to use:** After editing individual exercise files to update the master.

---

### 3. **update_images.py**
Scans exercise folders for images and updates `exercise.json` with image paths.

```bash
python update_images.py
```

**When to use:** After adding images to exercise folders.

---

### 4. **create_exercise_folders.py**
Creates folder structure from vocabulary.json.

```bash
python create_exercise_folders.py
```

**When to use:** Initial setup or adding new exercises.

---

## 📋 Common Workflows

### **Adding a New Exercise**

1. Add exercise data to `vocabulary.json`
2. Run `python create_exercise_folders.py` to create the folder
3. Run `python split_vocabulary.py` to create `exercise.json`

### **Editing an Exercise**

1. Edit `data/exercises/[Category]/[Exercise Name]/exercise.json`
2. Run `python build_vocabulary.py` to update master file

### **Adding Images**

1. Copy images to `data/exercises/[Category]/[Exercise Name]/`
2. Run `python update_images.py` to link images
3. Run `python build_vocabulary.py` to update master file

### **Bulk Update from Master**

1. Edit `vocabulary.json`
2. Run `python split_vocabulary.py` to update all individual files

---

## 🎯 Best Practices

✅ **Edit individual files** for single exercise updates  
✅ **Run build_vocabulary.py** after any individual file changes  
✅ **Run update_images.py** after adding images  
✅ **Commit both individual files and vocabulary.json** to git  
✅ **Use vocabulary.json** in your application for fast access  

❌ **Don't** manually edit vocabulary.json after splitting (edit individual files instead)  
❌ **Don't** forget to rebuild after changes  

---

## 📊 Current Database

- **Categories**: 6 (Warmup, Prehab, Shoulder opener, Handstand, Conditioning, Stretching)
- **Exercises**: 232
- **Format**: JSON with UTF-8 encoding

---

## 🔄 Complete Workflow Example

```bash
# 1. Edit an exercise
vim "data/exercises/Warmup/Jumping Jacks/exercise.json"

# 2. Add some images
cp ~/images/*.jpg "data/exercises/Warmup/Jumping Jacks/"

# 3. Update image links
python update_images.py

# 4. Rebuild master file
python build_vocabulary.py

# 5. Commit changes
git add .
git commit -m "Updated Jumping Jacks exercise with new images"
```

---

## 💡 Tips

- **JSON validation**: Your editor should validate JSON syntax automatically
- **Image formats**: Supports .jpg, .jpeg, .png, .gif, .webp, .svg
- **Multiple images**: Will store as array if multiple images found
- **Relative paths**: Image paths are relative to `data/exercises/`
