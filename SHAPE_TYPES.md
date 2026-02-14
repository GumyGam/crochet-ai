# Crochet Shape Types Guide

This document explains all the shape types our AI system can recognize and generate patterns for.

## 🎯 Complete Shape Library

### 1. **SPHERE** (Round/Ball Shapes)
**Best for:** Heads, bodies, round fruits, balls, pom-poms

**How it works:**
- Starts with magic loop (6 stitches)
- Increases evenly to reach maximum width
- Works straight rounds at max width
- Decreases evenly back to 6 stitches

**Example uses:**
- Dragon head & body
- Octopus head
- Apple
- Christmas ornament

---

### 2. **CYLINDER** (Tube/Column Shapes)
**Best for:** Arms, legs, necks, tubes, tree trunks

**How it works:**
- Starts with magic loop
- Increases to desired width
- Works straight rounds for entire height
- No decreasing (stays same width)

**Example uses:**
- Octopus tentacles
- Character arms/legs
- Flower pot
- Scarf (if worked flat)

---

### 3. **CONE** (Pointy/Tapered Shapes)
**Best for:** Ears, horns, tails with points, carrots, party hats

**How it works:**
- Starts at the base (widest part)
- Decreases gradually to a point
- Creates triangular/tapered shape

**Example uses:**
- Dragon horns
- Cat ears
- Carrot
- Ice cream cone

---

### 4. **FLAT_LEAF** (Simple Flat Pieces)
**Best for:** Basic leaves, scarves, belts, flat decorations

**How it works:**
- Chain foundation
- Work in rows (not rounds)
- Same width throughout
- Very simple and quick

**Example uses:**
- Simple plant leaf (like Otis the Plant)
- Scarf
- Belt or strap
- Banner/flag

---

### 5. **HEART_LEAF** (Organic/Heart-Shaped Leaves) ✨ NEW!
**Best for:** Monstera leaves, fancy plant leaves, hearts, complex organic shapes

**How it works:**
- Work in rows with increases
- Uses chain-spaces to create heart indent at top
- Border round with varied stitches (sc, hdc, dc) for organic shape
- Creates realistic leaf shapes

**Example uses:**
- Monstera plant leaves
- Sunflower leaves
- Heart decorations
- Organic petals

**Real pattern reference:** Ophelia the Monstera (small & large leaves)

---

### 6. **WING** (Triangular Wings with Jagged Edges) ✨ NEW!
**Best for:** Bat wings, dragon wings, fairy wings, fins

**How it works:**
- Work in rows, increasing to create triangle
- Final row uses **picot stitches** (ch 3, sl st) for jagged/pointed edges
- Border work creates clean sides
- Very dramatic look!

**Example uses:**
- Balrog wings (Lord of the Rings)
- Dragon wings
- Bat wings
- Fairy wings
- Fish fins

**Real pattern reference:** Balrog wings (black yarn with picots)

**Pro tip:** Picot stitch = chain 3, slip stitch into 3rd chain from hook. This creates small spikes/points perfect for wings!

---

### 7. **PETALS** (Loops Around Circular Base) ✨ NEW!
**Best for:** Flower petals, frills, decorative edges

**How it works:**
- Works directly onto an existing circular piece (like a flower center)
- Each petal is: ch 1, hdc, hdc, ch 1, sl st
- Repeat around edge with spacing
- Number of petals adjusts based on size

**Example uses:**
- Sunflower petals (yellow around brown center)
- Daisy petals
- Decorative collar/ruffle
- Fringe

**Real pattern reference:** Ana the Sunflower (yellow petals)

**Pro tip:** Join to BOTH pieces at once (front and back layers) for stability!

---

### 8. **SPIKES** (Tiny Triangular Protrusions) ✨ NEW!
**Best for:** Dinosaur spikes, ridges, scales, decorative bumps

**How it works:**
- Each spike is a mini cone
- 4 sc in magic loop
- One increase round to 6 stitches
- Fasten off and sew along back/spine

**Example uses:**
- Dinosaur back spikes
- Dragon spine
- Hedgehog quills
- Decorative ridges

**Pro tip:** Make multiple and space evenly along the back for best effect!

---

## 🎨 How the AI Chooses Shape Types

When you upload an image, our AI (llava model) looks at each component and asks:

1. **Is it round?** → Sphere
2. **Is it a tube/column?** → Cylinder  
3. **Does it taper to a point?** → Cone
4. **Is it flat and simple?** → Flat_leaf
5. **Is it organic/heart-shaped?** → Heart_leaf
6. **Does it have jagged/pointed edges like a wing?** → Wing
7. **Are there small loops around a circle?** → Petals
8. **Are there tiny triangular bumps?** → Spikes

## 🧠 Size Mapping

The AI identifies size as "small", "medium", or "large" and our system converts this to actual stitch counts:

### Sphere
- Small: 18 stitches max, 3 rounds height
- Medium: 24 stitches max, 5 rounds height
- Large: 30 stitches max, 8 rounds height

### Cylinder
- Small: 6 stitches wide, 3 rounds tall
- Medium: 12 stitches wide, 6 rounds tall
- Large: 18 stitches wide, 10 rounds tall

### Cone
- Small: 8 stitch base, 4 rounds tall
- Medium: 12 stitch base, 6 rounds tall
- Large: 16 stitch base, 8 rounds tall

### Petals
- Small: 6 petals
- Medium: 8 petals
- Large: 12 petals

## 📚 Pattern Structure

All patterns include:
- **US Standard Terminology** (sc, inc, dec, ch, etc.)
- **Detailed abbreviations section**
- **Beginner tips and safety eye reminders**
- **Round-by-round breakdown**
- **Stitch counts in parentheses**

## 🚀 What Makes This System Special

1. **Smart Recognition**: The AI looks for specific features (jagged edges, heart shapes, loops) not just basic geometry
2. **Count Support**: If you have 2 wings or 8 legs, it tells you "Make 2" or "Make 8"
3. **Real Pattern References**: Every shape is based on actual Woobles patterns
4. **Beginner-Friendly**: All instructions use simple language with tips
5. **Complex Shapes**: Can handle wings with picots, heart-shaped leaves, petal arrangements

## 🔧 Technical Details

### Vision Prompt (Fine-Tuned)
The AI receives specific instructions to:
- Look for EVERY component (including small details)
- Identify jagged/pointed edges as wings
- Recognize heart shapes and organic curves
- Count repeated elements
- Choose the BEST matching shape type

### Pattern Generation
Each shape has its own generation function with:
- Stitch-by-stitch instructions
- Proper increase/decrease ratios
- Tips for beginners
- Assembly instructions

## 🎯 Next Steps

Potential future shape types:
- **Ruffle**: Gathered fabric effect
- **Spiral**: Twisted shapes
- **Shell**: Scalloped edges
- **Bobble**: Textured bumps
- **Granny Square**: Flat square motifs

---

**Current Capabilities:** 8 shape types covering 90%+ of amigurumi patterns!
