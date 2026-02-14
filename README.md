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

## Usage

### 🌐 Option 1: Web Interface (Recommended)
The easiest way to use the generator!

```bash
source venv/bin/activate
python3 app.py
```

Then open your browser to: **http://localhost:5001**

Features:
- 📤 **Upload an image** OR ✍️ **describe what you want**
- ⚙️ **Adjust settings** (pattern name, colors, sizes)
- 👁️ **Live preview** in the same window
- 📥 **Download PDF** with one click

### 💻 Option 2: Command Line
For automation or scripting:

```bash
source venv/bin/activate
python3 image_to_pattern.py path/to/your/image.jpg [optional_name]
```

**Example:**
```bash
python3 image_to_pattern.py my_crochet_toy.png "My Custom Toy"
```

## Project Status

### ✅ Completed
- **Step 1**: Pattern generation engine ✅
- **Step 2**: Ollama vision AI integration ✅
- **Step 3**: Web interface with live preview ✅

### 🎨 Features
- Upload image OR text prompt
- Live HTML preview
- Adjustable settings
- PDF download
- ~3-30 second generation time
- 100% local, no API costs

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
