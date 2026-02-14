# Quick Start Guide

## 🎯 Generate a Pattern from ANY Image

### The Simple Way:
```bash
source venv/bin/activate
python3 image_to_pattern.py path/to/your/crochet_image.jpg
```

That's it! You'll get a PDF pattern in seconds.

---

## 📖 Detailed Instructions

### 1. **Prepare Your Image**
- Take a clear photo of a crochet amigurumi
- Works best with simple, visible shapes
- Front-facing angle recommended

### 2. **Run the Generator**
```bash
python3 image_to_pattern.py "my_photo.jpg" "Custom Name"
```

The system will:
1. Analyze the image with AI (15-30 seconds)
2. Identify all visible parts
3. Generate crochet instructions
4. Create a PDF pattern (~1 second)

### 3. **What You Get**
A complete PDF pattern with:
- Materials list
- Beginner tips & abbreviations  
- Step-by-step instructions for each part
- Stitch counts and assembly guidance

---

## 🔧 How It Works

```
Image → Ollama (llava) → Pattern Data → Pattern Engine → PDF
```

1. **Vision AI** looks at your image and identifies:
   - Shape types (sphere, cylinder, cone, leaf)
   - Colors
   - Relative sizes

2. **Pattern Engine** converts this to crochet:
   - Calculates stitch counts
   - Generates round-by-round instructions
   - Formats as beginner-friendly text

3. **PDF Generator** creates a printable pattern

---

## 💡 Tips for Best Results

### Good Images:
✅ Clear, well-lit photos
✅ Simple shapes (balls, tubes, cones)
✅ Solid colors
✅ Front-facing angle

### Tricky Images:
⚠️ Very complex details (lots of small parts)
⚠️ Multiple overlapping colors
⚠️ Side/back angles

The AI does its best, but you may need to adjust the generated pattern for very complex designs.

---

## 🐛 Troubleshooting

### "Ollama not found"
Install from: https://ollama.com

### "llava model not found"
Run: `ollama pull llava`

### Pattern doesn't match image
The AI is still learning! You can:
- Try a different angle/photo
- Manually edit the pattern
- Adjust the size parameters in `vision_analyzer.py`

---

## 🎨 Examples

Try these test commands:
```bash
# Generate from any image in Patterns folder
python3 image_to_pattern.py "Patterns/Woobles/Code Files (random)/F74e_SpXwAAKJWs.png" "Test1"

# Or use the pre-made examples
python3 pattern_engine.py fred
python3 pattern_engine.py otis
python3 pattern_engine.py ana
```
