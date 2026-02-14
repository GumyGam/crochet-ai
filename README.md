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

### 2. Generate a Pattern
Currently, the system uses simulated vision data. To generate the example patterns:

```bash
source venv/bin/activate
python3 pattern_engine.py fred    # Generates Fred the Dino
python3 pattern_engine.py otis    # Generates Otis the Snake Plant
python3 pattern_engine.py ana     # Generates Ana the Sunflower
python3 pattern_engine.py all     # Generates all three
```

## Project Status

### ✅ Completed (Step 1)
- Pattern generation engine with 4 shape types
- PDF export using fpdf2 (lightweight, fast)
- Fixed infinite loops and memory issues
- All emojis removed for proper PDF rendering

### 🚧 Next Steps
- **Step 2**: Connect Ollama vision AI (llava model)
- **Step 3**: Build simple web interface
- **Step 4**: Add more shape types (petals, wings, complex leaves)

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
