# Crochet Pattern AI Generator

An AI-powered system that generates beginner-friendly crochet patterns from images.

## Features
- ✅ **Pattern Engine**: Generates patterns for basic shapes (Sphere, Cylinder, Cone, Flat Leaf)
- ✅ **PDF Output**: Clean, formatted PDF patterns with US terminology
- ✅ **Beginner-Friendly**: Includes tips, stitch counts, and clear instructions

## Setup

### 1. Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install fpdf2
```

### 2. Download Ollama Vision Model
```bash
ollama pull llava
```

### 3. Generate a Pattern from an Image
```bash
source venv/bin/activate
python3 image_to_pattern.py path/to/your/image.jpg [optional_name]
```

**Example:**
```bash
python3 image_to_pattern.py my_crochet_toy.png "My Custom Toy"
```

### 4. Or Use Pre-Made Examples
```bash
python3 pattern_engine.py fred    # Generates Fred the Dino
python3 pattern_engine.py otis    # Generates Otis the Snake Plant  
python3 pattern_engine.py ana     # Generates Ana the Sunflower
```

## Project Status

### ✅ Completed
- **Step 1**: Pattern generation engine with 4 shape types ✅
- **Step 2**: Ollama vision AI integration (llava model) ✅
  - Analyzes images and identifies components
  - Generates patterns in ~3-30 seconds depending on complexity
  - Runs 100% locally on your Mac M4

### 🚧 Next Steps
- **Step 3**: Build simple web interface
- **Step 4**: Add more shape types (petals, wings, complex leaves)
- **Step 5**: Fine-tune prompts for better accuracy

## Example Output
Generated PDFs are ~3KB each and include:
- Materials list
- Beginner tips and abbreviations
- Row-by-row instructions with stitch counts
- Assembly guidance

## Notes
- All patterns use **US crochet terminology**
- Patterns are optimized for Mac M4 (low memory usage)
- Each pattern generates in ~1 second
