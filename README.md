# Crochet

Turn a photo — or a short description — into a beginner crochet pattern.

Local vision model, local engine, PDF out. No cloud API. Product page: **[gumygam.github.io/crochet-ai](https://gumygam.github.io/crochet-ai/)**

The generator itself is not hosted. Clone this repo and run it on your machine.

## What you get

- Image and/or text in
- Review UI so you can edit detected parts before writing
- Eight+ shape families (sphere, cylinder, cone, leaves, wings, petals, spikes, …)
- Beginner PDF with US terms, stitch counts, and assembly
- CLI for batch use

## Quick start

### 1. Ollama (the local model)

```bash
# https://ollama.com  or:
brew install ollama
ollama pull llava
```

Keep `ollama serve` running in the background if it is not already.

### 2. Install this repo

```bash
git clone https://github.com/GumyGam/crochet-ai.git
cd crochet-ai
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Python 3.10+ is enough.

### 3. Web app (recommended)

```bash
source venv/bin/activate
python3 app.py
```

Open **http://localhost:5001**

1. Drop a photo, or type what you want (or both)
2. Click **Analyze** (15–30s typical)
3. Review parts — edit / remove / add
4. **Generate pattern**
5. Download the PDF

### 4. Command line

```bash
source venv/bin/activate
python3 image_to_pattern.py path/to/image.jpg "Cute Dragon"
```

## How it is put together

```
photo and/or text
        │
        ▼
 Ollama (llava) — names parts and colors
        │
        ▼
 review UI — you correct the list
        │
        ▼
 pattern engine — rounds, counts, assembly
        │
        ▼
 PDF
```

Shape notes: [SHAPE_TYPES.md](SHAPE_TYPES.md)

## Project layout

```
app.py                 Flask app (localhost:5001)
pattern_engine.py      Round-by-round writing
vision_analyzer.py     Ollama vision
image_to_pattern.py    CLI
templates/index.html   Desk UI
static/studio.css      Shared look
docs/                  GitHub Pages product page
requirements.txt
```

## Tips

Good photos: clear light, simple background, shapes readable from the front.

Useful notes: “blue octopus, eight legs”, “ignore the branch”, “small ears”.

## Troubleshooting

**Ollama not found** — install from [ollama.com](https://ollama.com) or `brew install ollama`.

**llava missing** — `ollama pull llava`.

**Port 5001 busy** — change `port=` at the bottom of `app.py`.

**Pattern is off** — try another angle, or add notes, then edit parts in the review step.

## License

MIT. Generated patterns are yours.

Pattern style is inspired by public beginner amigurumi teaching (including [The Woobles](https://thewoobles.com/)). This project is not affiliated with them.

Powered locally by [Ollama](https://ollama.com/) and llava.
