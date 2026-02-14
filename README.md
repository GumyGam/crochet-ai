# 🧶 AI Crochet Pattern Generator

Transform any image into a complete, beginner-friendly crochet pattern using local AI. No API costs, no internet required (after setup).

## ✨ Features

- **🖼️ Image Analysis**: Upload any crochet amigurumi photo
- **✍️ Text Prompts**: Add details or generate from description alone
- **🤖 8 Shape Types**: Sphere, Cylinder, Cone, Flat Leaf, Heart Leaf, Wings, Petals, Spikes
- **📄 PDF Output**: Professional patterns with US terminology
- **🌐 Web Interface**: Beautiful drag-and-drop UI with live preview
- **💻 Command Line**: For automation and batch processing
- **🚀 100% Local**: Runs on your Mac M4 using Ollama
- **👶 Beginner-Friendly**: Detailed tips, stitch counts, abbreviations

## 🎯 What Can It Make?

✅ **Animals** (cats, dogs, octopuses, dragons)  
✅ **Fantasy Creatures** (with wings and spikes)  
✅ **Plants** (with heart-shaped leaves and petals)  
✅ **Flowers** (with petal arrangements)  
✅ **Characters** (heads, bodies, arms, legs)  
✅ **Simple to Complex** (90%+ amigurumi pattern coverage)

## 🚀 Quick Start

### 1. Prerequisites

**Install Ollama** (for local AI):
```bash
# Download from: https://ollama.com
# Or via Homebrew:
brew install ollama

# Pull the vision model:
ollama pull llava
```

### 2. Setup

```bash
# Clone the repository
git clone https://github.com/GumyGam/crochet-ai.git
cd crochet-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Web Interface (Recommended)

```bash
source venv/bin/activate
python3 app.py
```

Open your browser to: **http://localhost:5001**

**How to use:**
1. Upload an image OR type a description
2. Optionally add text details ("make it blue", "bigger ears")
3. Enter a pattern name
4. Click "Generate Pattern"
5. Preview the pattern (15-30 seconds)
6. Download your PDF!

### 4. Command Line Usage

```bash
source venv/bin/activate
python3 image_to_pattern.py path/to/image.jpg [optional_name]
```

**Example:**
```bash
python3 image_to_pattern.py my_dragon.png "Cute Dragon"
```

## 📚 Documentation

- **[SHAPE_TYPES.md](SHAPE_TYPES.md)**: Complete guide to all 8 shape types with examples and techniques

## 🏗️ System Architecture

```
┌─────────────┐
│   Image     │
│     OR      │ ──┐
│  Text Input │   │
└─────────────┘   │
                  ▼
         ┌─────────────────┐
         │  Ollama (llava)  │ ◄─── Local AI Vision Model
         │  Vision Analysis │
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Pattern Data     │ ◄─── JSON: shapes, colors, sizes
         │ (8 shape types)  │
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Pattern Engine   │ ◄─── Generates crochet instructions
         │ (pattern_engine) │
         └─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │   PDF Output    │ ◄─── Clean, printable pattern
         └─────────────────┘
```

## 🎨 Shape Types Explained

The system recognizes **8 different shape types** based on real Woobles patterns:

| Shape Type | Best For | Example |
|------------|----------|---------|
| **Sphere** | Round/ball shapes | Heads, bodies, balls |
| **Cylinder** | Tubes/columns | Arms, legs, necks |
| **Cone** | Pointy/tapered | Ears, horns, tails |
| **Flat Leaf** | Simple flat pieces | Basic leaves, scarves |
| **Heart Leaf** | Organic shapes | Monstera leaves, fancy leaves |
| **Wing** | Triangular with jagged edges | Dragon wings, bat wings |
| **Petals** | Loops around center | Sunflower petals, ruffles |
| **Spikes** | Tiny triangles | Dinosaur spikes, ridges |

See [SHAPE_TYPES.md](SHAPE_TYPES.md) for detailed explanations and techniques.

## 📊 Technical Details

### Performance (Mac M4)
- **Image analysis**: 15-30 seconds
- **Pattern generation**: <1 second
- **PDF creation**: <1 second
- **Total**: ~20-35 seconds per pattern

### Memory Usage
- ~2-3GB during AI analysis
- Safe for continuous use
- Optimized for Mac M4
- No memory leaks

### Technologies
- **Backend**: Python 3.14 + Flask
- **AI**: Ollama with llava vision model
- **PDF**: fpdf2 (lightweight)
- **Frontend**: HTML + CSS + Vanilla JavaScript

## 📁 Project Structure

```
crochet-ai/
├── app.py                  # Flask web server
├── pattern_engine.py       # Core pattern generation (8 shapes)
├── vision_analyzer.py      # AI image analysis (Ollama)
├── image_to_pattern.py     # CLI interface
├── templates/
│   └── index.html         # Web UI (green theme)
├── requirements.txt        # Python dependencies
├── SHAPE_TYPES.md         # Shape type documentation
└── README.md              # This file
```

## 💡 Tips for Best Results

### Good Images:
✅ Clear, well-lit photos  
✅ Front-facing angle  
✅ Simple backgrounds  
✅ Visible shapes and colors  

### AI Prompt Tips:
✅ Be specific: "blue octopus with 8 legs"  
✅ Mention colors: "make the body green"  
✅ Indicate sizes: "small ears, large head"  
✅ Combine with image for best accuracy  

## 🔧 Troubleshooting

### "Ollama not found"
```bash
# Install from: https://ollama.com
brew install ollama
```

### "llava model not found"
```bash
ollama pull llava
```

### Server won't start (port 5001 in use)
```bash
# Change port in app.py:
app.run(host='0.0.0.0', port=5002, debug=True)  # Use different port
```

### Pattern doesn't match image
- Try a different angle/photo
- Add text details to clarify
- The AI is learning and may need guidance for very complex designs

### High memory usage
- This is normal during AI analysis
- Memory is released after pattern generation
- Close other memory-intensive apps if needed

## 🎓 For Beginners

**New to coding?** Here's what you need to know:

1. **Virtual Environment (`venv/`)**: Keeps your project dependencies separate from other Python projects
2. **Requirements.txt**: Lists all the Python packages needed
3. **Flask**: Makes the web interface work
4. **Ollama**: Runs the AI vision model on your computer
5. **fpdf2**: Creates the PDF files

**New to crochet?** The generated patterns include:
- Detailed abbreviations (sc = single crochet, inc = increase, etc.)
- Beginner tips throughout
- Step-by-step instructions
- Stitch counts to verify you're on track

## 🌟 Examples

Generated patterns include:
- Materials list (yarn colors, hook size, safety eyes)
- Abbreviations section with full explanations
- Row-by-round instructions with stitch counts
- Special techniques (magic loop, picot stitches, chain-spaces)
- Assembly guidance

**Example output structure:**
```
# My Cute Dragon Pattern

## Materials Needed
- Green yarn (body)
- Black yarn (wings)
- 3.5mm crochet hook
- Safety eyes
- Stuffing

## Abbreviations
[Full list of stitches]

## BODY & HEAD (Green yarn)
Rnd 1: Start 6 sc in magic loop (6)
Rnd 2: [inc] x 6 (12)
...

## WING (Make 2, Black yarn)
Row 1: Chain 5
Row 2: sc in 2nd ch from hook...
[Instructions with picot stitches]

## ASSEMBLY
Sew wings to back between rounds 10-11...
```

## 🚀 What Makes This Special?

1. **Smart Recognition**: Detects jagged edges (wings), heart shapes (leaves), loop patterns (petals)
2. **Count Support**: Automatically tells you "Make 2" for wings, "Make 8" for octopus legs
3. **Real Patterns**: Based on actual Woobles patterns (Balrog, Sunflower, Monstera)
4. **Learning Mode**: Detailed explanations for each step
5. **Local & Free**: No API costs, no internet needed after setup
6. **Mac Optimized**: Runs smoothly on Mac M4

## 📈 Version History

- **v1.0** (Feb 2026): Initial release with 4 basic shapes
- **v2.0** (Feb 2026): Added 4 complex shapes (wings, petals, heart leaves, spikes)
- **v2.1** (Feb 2026): Fine-tuned AI prompts, improved recognition accuracy

## 🤝 Contributing

This is a personal project, but suggestions are welcome! If you find bugs or have ideas for improvement, feel free to open an issue.

## 📝 License

This project is for personal use. Generated patterns are yours to use as you wish!

## 🙏 Acknowledgments

- Pattern style inspired by [The Woobles](https://thewoobles.com/)
- Uses US crochet terminology throughout
- Powered by [Ollama](https://ollama.com/) and the llava vision model

---

**Ready to create your own crochet patterns?** 🧶

```bash
source venv/bin/activate
python3 app.py
# Open http://localhost:5001 and start creating!
```
