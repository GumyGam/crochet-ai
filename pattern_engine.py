import math
from fpdf import FPDF

class BeginnerPatternGenerator:
    def __init__(self):
        self.abbreviations = {
            "sc": "single crochet (US term)",
            "inc": "increase (2 sc in one stitch)",
            "dec": "decrease (sc 2 stitches together)",
            "ch": "chain",
            "sl st": "slip stitch",
            "hdc": "half double crochet (US term)",
            "dc": "double crochet (US term)",
            "magic loop": "magic loop (or ch 2, and sc 6 times in 2nd ch from hook)"
        }

    def save_to_pdf(self, filename, content):
        """Saves the pattern content to a PDF file using fpdf2 (lightweight)."""
        print(f"Generating PDF: {filename}...")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        lines = content.split('\n')
        for clean_line in lines:
            # Clean the line
            clean_line = clean_line.strip()
            
            # Skip empty lines
            if not clean_line:
                pdf.ln(4)
                continue
            
            if clean_line.startswith("# "): # H1
                pdf.set_font("Helvetica", 'B', 16)
                pdf.write(10, clean_line.replace("# ", ""))
                pdf.ln(10)
            elif clean_line.startswith("## "): # H2
                pdf.set_font("Helvetica", 'B', 14)
                pdf.ln(4)
                pdf.write(8, clean_line.replace("## ", ""))
                pdf.ln(8)
            elif clean_line.startswith("### "): # H3
                pdf.set_font("Helvetica", 'B', 11)
                pdf.write(6, clean_line.replace("### ", ""))
                pdf.ln(6)
            elif clean_line.startswith("**"): # Bold line
                pdf.set_font("Helvetica", 'B', 9)
                text = clean_line.replace("**", "")
                pdf.write(5, text)
                pdf.ln(5)
            elif clean_line.startswith("-"): # List item
                pdf.set_font("Helvetica", '', 9)
                pdf.write(5, clean_line)
                pdf.ln(5)
            elif clean_line == "---": # Separator
                pdf.ln(3)
                pdf.set_font("Helvetica", '', 9)
                pdf.write(2, "_" * 50)
                pdf.ln(5)
            elif clean_line.startswith("*") and clean_line.endswith("*"): # Italic
                pdf.set_font("Helvetica", 'I', 9)
                pdf.write(5, clean_line.replace("*", ""))
                pdf.ln(5)
            else:
                # Regular text
                pdf.set_font("Helvetica", '', 9)
                final_text = clean_line.replace("**", "")
                pdf.write(5, final_text)
                pdf.ln(5)
        
        pdf.output(filename)
        print(f"PDF saved: {filename}")

    def add_header(self):
        header = "# YOUR CUSTOM CROCHET PATTERN\n"
        header += "*Terminlogy: US Standard*\n\n"
        header += "## BEGINNER TIPS\n"
        header += "- **Mark your rounds:** Use a stitch marker (or safety pin) in the first stitch of every round so you don't lose count.\n"
        header += "- **Counting:** The number in (parentheses) at the end of each line is how many stitches you should have. Count them!\n"
        header += "- **Magic Loop:** If the magic loop is too hard, you can 'Chain 2' and make 6 sc into the second chain from the hook.\n\n"
        header += "## ABBREVIATIONS\n"
        for abbr, desc in self.abbreviations.items():
            header += f"- **{abbr}**: {desc}\n"
        header += "\n---\n"
        return header

    def format_round(self, round_num, instruction, count, tip=None):
        """Formats a single round with beginner tips."""
        line = f"**Rnd {round_num}:** {instruction} ({count} sts)"
        if tip:
            line += f"\n   *TIP: {tip}*"
        return line

    def generate_sphere(self, name, color, max_stitches=24, height_rows=5):
        """Generates a beginner-friendly sphere pattern."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("This piece is worked in continuous rounds. Do not join at the end of rounds.\n")
        
        # 1. Increase Phase
        current_stitches = 6
        pattern.append(self.format_round(1, "Start 6 sc in a magic loop", 6, "Pull the tail tight to close the hole!"))
        
        rnd = 2
        while current_stitches < max_stitches:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "inc in every stitch", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(rnd, f"[sc {sc_count}, inc] repeat 6 times", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        # 2. Work Even Phase
        pattern.append(self.format_round(f"{rnd} to {rnd + height_rows - 1}", "sc in every stitch around", current_stitches, "Just go round and round!"))
        rnd += height_rows

        # SAFETY EYES CHECKPOINT
        if "Head" in name:
            pattern.append("\n**STOP!** If you are using safety eyes, attach them now between Rnds 8 and 9.\n")

        # 3. Decrease Phase
        while current_stitches > 6:
            sc_count = (current_stitches // 6) - 2
            if sc_count > 0:
                pattern.append(self.format_round(rnd, f"[sc {sc_count}, dec] repeat 6 times", current_stitches - 6))
            else:
                pattern.append(self.format_round(rnd, "dec 6 times", current_stitches - 6))
            
            if current_stitches == 12:
                 pattern.append("   *Stuff the piece firmly with stuffing now!*")
            
            current_stitches -= 6
            rnd += 1

        pattern.append("\n**Finish:** Cut the yarn, leaving a long tail. Thread a needle and sew the hole closed.\n")
        return "\n".join(pattern)

    def generate_cylinder(self, name, color, width_stitches=12, height_rows=8):
        """Generates a tube pattern."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        
        # 1. Start with magic loop
        current_stitches = 6
        pattern.append(self.format_round(1, "Start 6 sc in a magic loop", 6))
        
        # 2. Increase to desired width
        rnd = 2
        while current_stitches < width_stitches:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "inc in every stitch", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(rnd, f"[sc {sc_count}, inc] repeat 6 times", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        # 3. Work even for height
        pattern.append(self.format_round(f"{rnd} to {rnd + height_rows - 1}", "sc in every stitch around", current_stitches))
        
        pattern.append("\n**Finish:** Fasten off. Leave a long tail for sewing it to the body. Stuff lightly.\n")
        return "\n".join(pattern)

    def generate_cone(self, name, color, base_stitches=12, height_rows=6):
        """Generates a cone pattern."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        
        pattern.append(self.format_round(1, "Start 4 sc in a magic loop", 4))
        current_stitches = 4
        rnd = 2

        target_rounds = height_rows
        inc_interval = max(1, target_rounds // ((base_stitches - 4) // 2))

        while rnd <= target_rounds + 1:
            if current_stitches < base_stitches and (rnd % inc_interval == 0):
                half = current_stitches // 2
                pattern.append(self.format_round(rnd, f"[sc {half-1}, inc] repeat 2 times", current_stitches + 2))
                current_stitches += 2
            else:
                pattern.append(self.format_round(rnd, "sc in every stitch", current_stitches))
            rnd += 1

        pattern.append("\n**Finish:** Fasten off. Leave a long tail. Stuff gently.\n")
        return "\n".join(pattern)

    def generate_flat_leaf(self, name, color, length_chains):
        """Generates a simple flat leaf (Otis style)."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*This part is worked in rows, not rounds. You will turn your work at the end of each row.*")
        
        pattern.append(f"**Row 1:** Chain {length_chains}.")
        pattern.append(f"**Row 2:** Start in 2nd chain from hook. sc {length_chains-1} down the chain. Chain 1, Turn.")
        pattern.append(f"**Row 3:** sc {length_chains-1} back up. Chain 1, Turn.")
        pattern.append(f"**Row 4:** sc {length_chains-1} back down.")
        
        pattern.append("\n**Finish:** Fasten off. Leave a tail to sew it into the pot.\n")
        return "\n".join(pattern)

    def generate_heart_leaf(self, name, color, size="medium"):
        """Generates a heart-shaped leaf (Monstera style) with increases for width."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*This leaf is worked in rows with chain spaces to create the heart shape.*\n")
        
        # Size mapping
        base_chains = {"small": 2, "medium": 2, "large": 3}.get(size, 2)
        
        pattern.append(f"**Row 1:** Chain {base_chains}.")
        pattern.append(f"**Row 2:** Inc in 2nd ch from hook, ch 1 and turn. ({base_chains} sts)")
        pattern.append(f"**Row 3:** 2 inc, ch 1 and turn. (4 sts)")
        pattern.append(f"**Row 4:** inc, 2 sc, inc, ch 3 and turn. (6 sts)")
        pattern.append(f"**Row 5:** Skip 2 stitches, 2 sc, ch 3, skip 1 st, sl st, ch 1 and turn. (6 sts)")
        pattern.append(f"   *TIP: The chain-3 spaces create the heart indent at top.*")
        pattern.append(f"**Row 6:** Skip 1 st, 3 sc in ch-3 space, 2 sc, 3 sc in ch-3 space, ch 1 turn. (8 sts)")
        pattern.append(f"**Row 7:** sc, hdc, dc, dc, hdc, sc around the edge.")
        
        pattern.append("\n**Finish:** Fasten off. Leave long tail for sewing.\n")
        return "\n".join(pattern)

    def generate_wing(self, name, color, size="medium"):
        """Generates a triangular wing with jagged edges (Balrog style)."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*Wings are worked in rows with increases to create a triangle shape.*\n")
        
        # Size determines base chain length
        base_chains = {"small": 4, "medium": 5, "large": 6}.get(size, 5)
        
        pattern.append(f"**Row 1:** Chain {base_chains}.")
        pattern.append(f"**Row 2:** sc in 2nd ch from hook, {base_chains-2} sc, ch 1 and turn. ({base_chains-1} sts)")
        pattern.append(f"**Row 3:** inc, {base_chains-3} sc, inc, ch 1 and turn. ({base_chains+1} sts)")
        pattern.append(f"**Row 4:** inc, {base_chains-1} sc, inc, ch 1 and turn. ({base_chains+3} sts)")
        pattern.append(f"**Row 5:** inc, 2 sc, 2 inc, 2 sc, inc, ch 1 and turn. ({base_chains+7} sts)")
        pattern.append(f"**Row 6:** 3 sc, picot, sc, 2 sl st, sc, picot, sc, sl st.")
        pattern.append(f"   *TIP: Picot stitch = ch 3, sl st into 3rd ch from hook (creates spike).*")
        
        pattern.append("\n**Edge:** Work sc along sides of wing to create clean edges.")
        pattern.append("**Finish:** Fasten off. Leave long tail for sewing to back.\n")
        return "\n".join(pattern)

    def generate_petals(self, name, color, num_petals=6, attachment="edge"):
        """Generates petals that attach to an edge (Sunflower style)."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append(f"*Petals are worked directly onto the edge. Make {num_petals} petals total.*\n")
        
        pattern.append(f"**Step 1:** Position your flower piece. Sl st join into edge stitch.")
        pattern.append(f"**Step 2:** Ch 1, hdc in same stitch.")
        pattern.append(f"**Step 3:** Hdc in next stitch.")
        pattern.append(f"**Step 4:** Ch 1, sl st in same stitch as step 3.")
        pattern.append(f"   *This creates ONE petal.*")
        pattern.append(f"\n**Step 5:** Skip 1 or 2 stitches, then repeat Steps 1-4 for the next petal.")
        pattern.append(f"**Step 6:** Repeat until you have {num_petals} petals evenly spaced around.")
        
        pattern.append("\n**Finish:** Fasten off and weave in ends.\n")
        return "\n".join(pattern)

    def generate_spikes(self, name, color, num_spikes=5):
        """Generates small triangle spikes (like dinosaur back spikes)."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn, Make {num_spikes})")
        pattern.append("*Each spike is a tiny triangle.*\n")
        
        pattern.append(f"**Rnd 1:** Start 4 sc in magic loop. (4 sts)")
        pattern.append(f"**Rnd 2:** [sc, inc] x 2. (6 sts)")
        
        pattern.append("\n**Finish:** Fasten off with long tail. Sew spikes along back, spacing evenly.\n")
        return "\n".join(pattern)


# --- SIMULATION 1: Fred the Dino ---
fred_vision_output = [
    {"type": "sphere", "name": "Head & Body", "color": "Green", "max_stitches": 30, "height": 8},
    {"type": "cone", "name": "Tail", "color": "Green", "base": 14, "height": 8},
    {"type": "cylinder", "name": "Arm (Make 2)", "color": "Green", "width": 6, "height": 3},
]

# --- SIMULATION 2: Otis the Snake Plant ---
otis_vision_output = [
    {"type": "cylinder", "name": "Pot", "color": "Red", "width": 24, "height": 8},
    {"type": "sphere", "name": "Dirt (Inside Pot)", "color": "Dark Brown", "max_stitches": 24, "height": 2},
    {"type": "flat_leaf", "name": "Tall Leaf", "color": "Green/Dark Green", "length": 15},
    {"type": "flat_leaf", "name": "Short Leaf", "color": "Green", "length": 10}
]

# --- SIMULATION 3: Ana the Sunflower (Simplified for now) ---
ana_vision_output = [
    {"type": "sphere", "name": "Flower Face (Make 2)", "color": "Brown", "max_stitches": 24, "height": 2},
    {"type": "cylinder", "name": "Stem", "color": "Green", "width": 6, "height": 10},
    {"type": "cylinder", "name": "Pot", "color": "Tan", "width": 24, "height": 6},
    # Note: Petals are still tricky, represented as small leaves for now
    {"type": "flat_leaf", "name": "Leaf (Make 2)", "color": "Green", "length": 8} 
]

# --- MAIN GENERATOR LOGIC ---
if __name__ == "__main__":
    import sys
    engine = BeginnerPatternGenerator()
    
    # Check if a specific pattern was requested
    if len(sys.argv) > 1:
        pattern_name = sys.argv[1].lower()
    else:
        pattern_name = "all"
    
    print(f"Generating patterns: {pattern_name}")

    if pattern_name in ["fred", "all"]:
        print("\n=== Generating Fred the Dino ===")
        full_pattern = engine.add_header()
        full_pattern += "## FRED THE DINO\n\n"
        for part in fred_vision_output:
            if part["type"] == "sphere":
                full_pattern += engine.generate_sphere(part["name"], part["color"], part["max_stitches"], part["height"])
            elif part["type"] == "cylinder":
                full_pattern += engine.generate_cylinder(part["name"], part["color"], part["width"], part["height"])
            elif part["type"] == "cone":
                full_pattern += engine.generate_cone(part["name"], part["color"], part["base"], part["height"])
        engine.save_to_pdf("Fred_The_Dino_Pattern.pdf", full_pattern)
        del full_pattern  # Free memory

    if pattern_name in ["otis", "all"]:
        print("\n=== Generating Otis the Snake Plant ===")
        full_pattern = engine.add_header()
        full_pattern += "## OTIS THE SNAKE PLANT\n\n"
        for part in otis_vision_output:
            if part["type"] == "sphere":
                full_pattern += engine.generate_sphere(part["name"], part["color"], part["max_stitches"], part["height"])
            elif part["type"] == "cylinder":
                full_pattern += engine.generate_cylinder(part["name"], part["color"], part["width"], part["height"])
            elif part["type"] == "cone":
                full_pattern += engine.generate_cone(part["name"], part["color"], part["base"], part["height"])
            elif part["type"] == "flat_leaf":
                 full_pattern += engine.generate_flat_leaf(part["name"], part["color"], part["length"])
        engine.save_to_pdf("Otis_The_Snake_Plant_Pattern.pdf", full_pattern)
        del full_pattern  # Free memory

    if pattern_name in ["ana", "all"]:
        print("\n=== Generating Ana the Sunflower ===")
        full_pattern = engine.add_header()
        full_pattern += "## ANA THE SUNFLOWER\n\n"
        for part in ana_vision_output:
            if part["type"] == "sphere":
                full_pattern += engine.generate_sphere(part["name"], part["color"], part["max_stitches"], part["height"])
            elif part["type"] == "cylinder":
                full_pattern += engine.generate_cylinder(part["name"], part["color"], part["width"], part["height"])
            elif part["type"] == "cone":
                full_pattern += engine.generate_cone(part["name"], part["color"], part["base"], part["height"])
            elif part["type"] == "flat_leaf":
                 full_pattern += engine.generate_flat_leaf(part["name"], part["color"], part["length"])
        engine.save_to_pdf("Ana_The_Sunflower_Pattern.pdf", full_pattern)
        del full_pattern  # Free memory

    print("\n✅ Done! PDF files created.")
