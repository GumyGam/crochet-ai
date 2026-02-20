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
            "magic loop": "magic loop (or ch 2, and sc 6 times in 2nd ch from hook)",
        }

    # ──────────────────────────────────────────────
    #  PDF OUTPUT
    # ──────────────────────────────────────────────

    def save_to_pdf(self, filename, content):
        """Saves the pattern content to a PDF file."""
        print(f"Generating PDF: {filename}...")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        for clean_line in content.split("\n"):
            clean_line = clean_line.strip()

            if not clean_line:
                pdf.ln(4)
                continue

            if clean_line.startswith("# "):
                pdf.set_font("Helvetica", "B", 16)
                pdf.write(10, clean_line.replace("# ", ""))
                pdf.ln(10)
            elif clean_line.startswith("## "):
                pdf.set_font("Helvetica", "B", 14)
                pdf.ln(4)
                pdf.write(8, clean_line.replace("## ", ""))
                pdf.ln(8)
            elif clean_line.startswith("### "):
                pdf.set_font("Helvetica", "B", 11)
                pdf.write(6, clean_line.replace("### ", ""))
                pdf.ln(6)
            elif clean_line.startswith("**"):
                pdf.set_font("Helvetica", "B", 9)
                pdf.write(5, clean_line.replace("**", ""))
                pdf.ln(5)
            elif clean_line.startswith("- "):
                pdf.set_font("Helvetica", "", 9)
                pdf.write(5, clean_line)
                pdf.ln(5)
            elif clean_line == "---":
                pdf.ln(3)
                pdf.set_font("Helvetica", "", 9)
                pdf.write(2, "_" * 50)
                pdf.ln(5)
            elif clean_line.startswith("*") and clean_line.endswith("*"):
                pdf.set_font("Helvetica", "I", 9)
                pdf.write(5, clean_line.replace("*", ""))
                pdf.ln(5)
            else:
                pdf.set_font("Helvetica", "", 9)
                pdf.write(5, clean_line.replace("**", ""))
                pdf.ln(5)

        pdf.output(filename)
        print(f"PDF saved: {filename}")

    # ──────────────────────────────────────────────
    #  HEADER, MATERIALS, ABBREVIATIONS
    # ──────────────────────────────────────────────

    def add_header(self):
        header = "# YOUR CUSTOM CROCHET PATTERN\n"
        header += "*Terminology: US Standard*\n\n"
        header += "## BEGINNER TIPS\n"
        header += "- **Mark your rounds:** Use a stitch marker (or safety pin) in the first stitch of every round so you don't lose count.\n"
        header += "- **Counting:** The number in (parentheses) at the end of each line is how many stitches you should have. Count them!\n"
        header += "- **Magic Loop:** If the magic loop is too hard, you can 'Chain 2' and make 6 sc into the second chain from the hook.\n\n"
        header += "## ABBREVIATIONS\n"
        for abbr, desc in self.abbreviations.items():
            header += f"- **{abbr}**: {desc}\n"
        header += "\n---\n"
        return header

    def generate_materials(self, pattern_data):
        """Generate a materials/supplies section from the parts list."""
        colors = []
        has_eyes = False

        for part in pattern_data:
            color = part.get("color", "Unknown")
            base_color = color.split(" with ")[0].split("/")[0].strip()
            if base_color not in colors:
                colors.append(base_color)

            name_lower = part.get("name", "").lower()
            if "eye" in name_lower or "head" in name_lower:
                has_eyes = True

        section = "## MATERIALS\n"
        section += "- **Hook:** 3.5mm (E/4) crochet hook\n"
        section += "- **Yarn:** Worsted weight (Medium #4) in the following colors:\n"
        for c in colors:
            section += f"  - {c}\n"
        if has_eyes:
            section += "- **Safety eyes:** 6-9mm (size to your preference)\n"
        section += "- **Stuffing:** Polyester fiberfill\n"
        section += "- **Extras:** Yarn needle, stitch markers, scissors\n"
        section += "\n---\n"
        return section

    # ──────────────────────────────────────────────
    #  UNIFIED PART DISPATCHER
    # ──────────────────────────────────────────────

    def generate_part(self, part):
        """Route a part dict to the correct shape generator."""
        t = part["type"]
        name = part["name"]
        color = part["color"]

        if t == "sphere":
            return self.generate_sphere(name, color, part["max_stitches"], part["height"])
        elif t == "oval":
            return self.generate_oval(name, color, part["max_stitches"], part["height"])
        elif t == "cylinder":
            return self.generate_cylinder(name, color, part["width"], part["height"])
        elif t == "cone":
            return self.generate_cone(name, color, part["base"], part["height"])
        elif t == "dome":
            return self.generate_dome(name, color, part["max_stitches"])
        elif t == "flat_circle":
            return self.generate_flat_circle(name, color, part["max_stitches"])
        elif t == "flat_leaf":
            return self.generate_flat_leaf(name, color, part["length"])
        elif t == "tapered_tube":
            return self.generate_tapered_tube(name, color, part["start_width"], part["end_width"], part["height"])
        elif t == "fan":
            return self.generate_fan(name, color, part.get("size", "medium"))
        elif t == "bird_feet":
            return self.generate_bird_feet(name, color, part.get("size", "medium"))
        elif t == "heart_leaf":
            return self.generate_heart_leaf(name, color, part.get("size", "medium"))
        elif t == "wing":
            return self.generate_wing(name, color, part.get("size", "medium"))
        elif t == "petals":
            return self.generate_petals(name, color, part["num_petals"], part.get("attachment", "edge"))
        elif t == "spikes":
            return self.generate_spikes(name, color, part["num_spikes"])
        elif t == "bobble":
            return self.generate_bobble(name, color, part.get("size", "medium"))
        else:
            return self.generate_sphere(name, color, 18, 3)

    # ──────────────────────────────────────────────
    #  FORMATTING HELPERS
    # ──────────────────────────────────────────────

    def format_round(self, round_num, instruction, count, tip=None):
        """Formats a single round with optional beginner tip."""
        line = f"**Rnd {round_num}:** {instruction} ({count} sts)"
        if tip:
            line += f"\n   *TIP: {tip}*"
        return line

    def format_row(self, row_num, instruction, count=None):
        """Formats a single row for flat pieces."""
        line = f"**Row {row_num}:** {instruction}"
        if count is not None:
            line += f" ({count} sts)"
        return line

    # ──────────────────────────────────────────────
    #  SHAPE GENERATORS — Original shapes
    # ──────────────────────────────────────────────

    def generate_sphere(self, name, color, max_stitches=24, height_rows=5):
        """Symmetric ball: increase → work even → decrease."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("This piece is worked in continuous rounds. Do not join at the end of rounds.\n")

        current_stitches = 6
        pattern.append(self.format_round(1, "Start 6 sc in a magic loop", 6,
                                          "Pull the tail tight to close the hole!"))

        rnd = 2
        while current_stitches < max_stitches:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "inc in every stitch", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(
                    rnd, f"[sc {sc_count}, inc] repeat 6 times", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        pattern.append(self.format_round(
            f"{rnd} to {rnd + height_rows - 1}",
            "sc in every stitch around", current_stitches,
            "Just go round and round!"))
        rnd += height_rows

        if "head" in name.lower():
            eye_rnd = max(rnd - height_rows - 1, 3)
            pattern.append(f"\n**STOP!** If you are using safety eyes, attach them now around Rnd {eye_rnd}.\n")

        while current_stitches > 6:
            sc_count = (current_stitches // 6) - 2
            if sc_count > 0:
                pattern.append(self.format_round(
                    rnd, f"[sc {sc_count}, dec] repeat 6 times", current_stitches - 6))
            else:
                pattern.append(self.format_round(rnd, "dec 6 times", current_stitches - 6))

            if current_stitches == 12:
                pattern.append("   *Stuff the piece firmly with stuffing now!*")

            current_stitches -= 6
            rnd += 1

        pattern.append("\n**Finish:** Cut the yarn, leaving a long tail. Thread a needle and sew the hole closed.\n")
        return "\n".join(pattern)

    def generate_cylinder(self, name, color, width_stitches=12, height_rows=8):
        """Open-ended tube: increase to width, then work even."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")

        current_stitches = 6
        pattern.append(self.format_round(1, "Start 6 sc in a magic loop", 6))

        rnd = 2
        while current_stitches < width_stitches:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "inc in every stitch", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(
                    rnd, f"[sc {sc_count}, inc] repeat 6 times", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        pattern.append(self.format_round(
            f"{rnd} to {rnd + height_rows - 1}",
            "sc in every stitch around", current_stitches))

        pattern.append("\n**Finish:** Fasten off. Leave a long tail for sewing. Stuff lightly.\n")
        return "\n".join(pattern)

    def generate_cone(self, name, color, base_stitches=12, height_rows=6):
        """Tapered cone: gradual increases from a narrow tip."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")

        pattern.append(self.format_round(1, "Start 4 sc in a magic loop", 4))
        current_stitches = 4
        rnd = 2

        target_rounds = height_rows
        inc_interval = max(1, target_rounds // max(1, (base_stitches - 4) // 2))

        while rnd <= target_rounds + 1:
            if current_stitches < base_stitches and (rnd % inc_interval == 0):
                half = current_stitches // 2
                pattern.append(self.format_round(
                    rnd, f"[sc {half - 1}, inc] repeat 2 times", current_stitches + 2))
                current_stitches += 2
            else:
                pattern.append(self.format_round(rnd, "sc in every stitch", current_stitches))
            rnd += 1

        pattern.append("\n**Finish:** Fasten off. Leave a long tail for sewing. Stuff gently.\n")
        return "\n".join(pattern)

    def generate_flat_leaf(self, name, color, length_chains=10):
        """Simple flat strip worked in rows."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*This part is worked in rows, not rounds. Turn your work at the end of each row.*\n")

        pattern.append(self.format_row(1, f"Chain {length_chains}."))
        pattern.append(self.format_row(2, f"Start in 2nd ch from hook. sc {length_chains - 1}. Ch 1, turn.", length_chains - 1))
        pattern.append(self.format_row(3, f"sc {length_chains - 1}. Ch 1, turn.", length_chains - 1))
        pattern.append(self.format_row(4, f"sc {length_chains - 1}.", length_chains - 1))

        pattern.append("\n**Finish:** Fasten off. Leave a long tail for sewing to the body.\n")
        return "\n".join(pattern)

    def generate_heart_leaf(self, name, color, size="medium"):
        """Heart-shaped leaf with chain spaces for the indent."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*This leaf is worked in rows with chain spaces to create the heart shape.*\n")

        base_chains = {"tiny": 2, "small": 2, "medium": 2, "large": 3}.get(size, 2)

        pattern.append(self.format_row(1, f"Chain {base_chains}."))
        pattern.append(self.format_row(2, f"Inc in 2nd ch from hook, ch 1 and turn.", base_chains))
        pattern.append(self.format_row(3, "2 inc, ch 1 and turn.", 4))
        pattern.append(self.format_row(4, "inc, 2 sc, inc, ch 3 and turn.", 6))
        pattern.append(self.format_row(5, "Skip 2 stitches, 2 sc, ch 3, skip 1 st, sl st, ch 1 and turn.", 6))
        pattern.append("   *TIP: The chain-3 spaces create the heart indent at top.*")
        pattern.append(self.format_row(6, "Skip 1 st, 3 sc in ch-3 space, 2 sc, 3 sc in ch-3 space, ch 1 turn.", 8))
        pattern.append(self.format_row(7, "sc, hdc, dc, dc, hdc, sc around the edge."))

        pattern.append("\n**Finish:** Fasten off. Leave long tail for sewing.\n")
        return "\n".join(pattern)

    def generate_wing(self, name, color, size="medium"):
        """Triangular wing with optional jagged edges."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*Wings are worked in rows with increases to create a triangle shape.*\n")

        base_chains = {"tiny": 3, "small": 4, "medium": 5, "large": 6}.get(size, 5)

        pattern.append(self.format_row(1, f"Chain {base_chains}."))
        pattern.append(self.format_row(2, f"sc in 2nd ch from hook, {base_chains - 2} sc, ch 1 and turn.", base_chains - 1))
        pattern.append(self.format_row(3, f"inc, {base_chains - 3} sc, inc, ch 1 and turn.", base_chains + 1))
        pattern.append(self.format_row(4, f"inc, {base_chains - 1} sc, inc, ch 1 and turn.", base_chains + 3))
        pattern.append(self.format_row(5, "inc, 2 sc, 2 inc, 2 sc, inc, ch 1 and turn.", base_chains + 7))
        pattern.append(self.format_row(6, "3 sc, picot, sc, 2 sl st, sc, picot, sc, sl st."))
        pattern.append("   *TIP: Picot stitch = ch 3, sl st into 3rd ch from hook (creates a small point).*")

        pattern.append("\n**Edge:** Work sc evenly along sides of wing for clean edges.")
        pattern.append("**Finish:** Fasten off. Leave long tail for sewing.\n")
        return "\n".join(pattern)

    def generate_petals(self, name, color, num_petals=6, attachment="edge"):
        """Petals worked directly onto an edge."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append(f"*Make {num_petals} petals, worked directly onto the edge.*\n")

        pattern.append("**Step 1:** Sl st join into an edge stitch.")
        pattern.append("**Step 2:** Ch 1, hdc in same stitch.")
        pattern.append("**Step 3:** Hdc in next stitch.")
        pattern.append("**Step 4:** Ch 1, sl st in same stitch as Step 3.")
        pattern.append("   *This creates ONE petal.*")
        pattern.append(f"\n**Step 5:** Skip 1-2 stitches, repeat Steps 1-4 for the next petal.")
        pattern.append(f"**Step 6:** Repeat until you have {num_petals} petals evenly spaced.")

        pattern.append("\n**Finish:** Fasten off and weave in ends.\n")
        return "\n".join(pattern)

    def generate_spikes(self, name, color, num_spikes=5):
        """Small triangular spikes."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn, Make {num_spikes})")
        pattern.append("*Each spike is a tiny triangle.*\n")

        pattern.append(self.format_round(1, "Start 4 sc in magic loop", 4))
        pattern.append(self.format_round(2, "[sc, inc] x 2", 6))

        pattern.append("\n**Finish:** Fasten off with long tail. Sew spikes evenly along the back.\n")
        return "\n".join(pattern)

    # ──────────────────────────────────────────────
    #  SHAPE GENERATORS — New shapes
    # ──────────────────────────────────────────────

    def generate_oval(self, name, color, max_stitches=24, height_rows=7):
        """
        Egg/oval shape: like a sphere but with MORE even rows
        so it stretches taller than it is wide.
        """
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("This piece is worked in continuous rounds (oval/egg shape).\n")

        current_stitches = 6
        pattern.append(self.format_round(1, "Start 6 sc in a magic loop", 6,
                                          "Pull the tail tight to close the hole!"))

        rnd = 2
        while current_stitches < max_stitches:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "inc in every stitch", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(
                    rnd, f"[sc {sc_count}, inc] repeat 6 times", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        # More even rows than a sphere creates the elongated egg shape
        pattern.append(self.format_round(
            f"{rnd} to {rnd + height_rows - 1}",
            "sc in every stitch around", current_stitches,
            "These extra even rounds create the oval/egg shape!"))
        rnd += height_rows

        if "head" in name.lower():
            eye_rnd = max(rnd - height_rows, 3)
            pattern.append(f"\n**STOP!** If you are using safety eyes, attach them now around Rnd {eye_rnd}.\n")

        # Decrease (slightly asymmetric for egg shape — first decrease round has more sc)
        while current_stitches > 6:
            sc_count = (current_stitches // 6) - 2
            if sc_count > 0:
                pattern.append(self.format_round(
                    rnd, f"[sc {sc_count}, dec] repeat 6 times", current_stitches - 6))
            else:
                pattern.append(self.format_round(rnd, "dec 6 times", current_stitches - 6))

            if current_stitches == 12:
                pattern.append("   *Stuff the piece firmly with stuffing now!*")

            current_stitches -= 6
            rnd += 1

        pattern.append("\n**Finish:** Cut the yarn, leaving a long tail. Sew the hole closed.\n")
        return "\n".join(pattern)

    def generate_dome(self, name, color, max_stitches=24):
        """Half-sphere: increase only, no decrease. Flat on the bottom."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("This piece is worked in continuous rounds (dome/half-sphere, flat on the bottom).\n")

        current_stitches = 6
        pattern.append(self.format_round(1, "Start 6 sc in a magic loop", 6))

        rnd = 2
        while current_stitches < max_stitches:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "inc in every stitch", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(
                    rnd, f"[sc {sc_count}, inc] repeat 6 times", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        # A couple of even rounds to give it height
        pattern.append(self.format_round(f"{rnd} to {rnd + 1}", "sc in every stitch around", current_stitches))

        pattern.append("\n**Finish:** Fasten off. Leave a long tail for sewing. Stuff before attaching.\n")
        return "\n".join(pattern)

    def generate_flat_circle(self, name, color, max_stitches=18):
        """Flat disc: increase rounds only, no height. For ears, pads, spots."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*This piece stays flat — do not stuff.*\n")

        current_stitches = 6
        pattern.append(self.format_round(1, "Start 6 sc in a magic loop", 6))

        rnd = 2
        while current_stitches < max_stitches:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "inc in every stitch", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(
                    rnd, f"[sc {sc_count}, inc] repeat 6 times", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        pattern.append("\n**Finish:** Fasten off. Leave a long tail for sewing.\n")
        return "\n".join(pattern)

    def generate_tapered_tube(self, name, color, start_width=12, end_width=6, height_rows=8):
        """Tube that starts wide and gradually narrows (tails, tentacles)."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*This piece starts wide and tapers to a point.*\n")

        # Start with increases to reach start_width
        current_stitches = 6
        pattern.append(self.format_round(1, "Start 6 sc in a magic loop", 6))

        rnd = 2
        while current_stitches < start_width:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "inc in every stitch", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(
                    rnd, f"[sc {sc_count}, inc] repeat 6 times", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        # Work a few even rounds at full width
        even_rows = max(2, height_rows // 3)
        pattern.append(self.format_round(
            f"{rnd} to {rnd + even_rows - 1}",
            "sc in every stitch around", current_stitches))
        rnd += even_rows

        # Gradual decrease
        while current_stitches > end_width:
            sc_count = max(1, (current_stitches // 6) - 2)
            decrease = min(6, current_stitches - end_width)
            repeat = decrease
            sc_per = max(1, (current_stitches // repeat) - 1)
            pattern.append(self.format_round(
                rnd, f"[sc {sc_per}, dec] repeat {repeat} times", current_stitches - repeat))
            current_stitches -= repeat
            rnd += 1

        pattern.append("\n**Finish:** Fasten off. Leave a long tail for sewing. Stuff the wide end lightly.\n")
        return "\n".join(pattern)

    def generate_fan(self, name, color, size="medium"):
        """Fan/spread shape for bird tails, fish tails, ruffles."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*This piece is worked in rows and fans out from narrow to wide.*\n")

        base_ch = {"tiny": 4, "small": 5, "medium": 6, "large": 8}.get(size, 6)

        pattern.append(self.format_row(1, f"Chain {base_ch}."))
        pattern.append(self.format_row(2, f"sc in 2nd ch from hook, sc {base_ch - 2}. Ch 1, turn.", base_ch - 1))
        pattern.append(self.format_row(3, f"inc, sc {base_ch - 3}, inc. Ch 1, turn.", base_ch + 1))
        pattern.append(self.format_row(4, f"inc, sc {base_ch - 1}, inc. Ch 1, turn.", base_ch + 3))
        pattern.append(self.format_row(5, f"inc, sc {base_ch + 1}, inc.", base_ch + 5))
        pattern.append("   *TIP: The increases on both edges create the fan/spread shape.*")

        pattern.append("\n**Finish:** Fasten off. Leave a long tail for sewing.\n")
        return "\n".join(pattern)

    def generate_bird_feet(self, name, color, size="medium"):
        """Simple forked bird feet using chains for toes."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*Each foot has 3 toes made from chains.*\n")

        toe_len = {"tiny": 3, "small": 4, "medium": 5, "large": 6}.get(size, 5)
        leg_len = {"tiny": 3, "small": 4, "medium": 5, "large": 6}.get(size, 5)

        pattern.append(f"**Leg:** Chain {leg_len}. sc in 2nd ch from hook, sc {leg_len - 2}. Do not turn.")
        pattern.append(f"**Toe 1:** Chain {toe_len}. sl st in 2nd ch from hook, sl st {toe_len - 2} back to leg.")
        pattern.append(f"**Toe 2:** Chain {toe_len}. sl st in 2nd ch from hook, sl st {toe_len - 2} back to leg.")
        pattern.append(f"**Toe 3:** Chain {toe_len}. sl st in 2nd ch from hook, sl st {toe_len - 2} back to leg.")
        pattern.append("   *TIP: All 3 toes branch out from the same point at the bottom of the leg.*")

        pattern.append("\n**Finish:** Fasten off. Leave a long tail for sewing to the body.\n")
        return "\n".join(pattern)

    def generate_bobble(self, name, color, size="medium"):
        """Small rounded bump that sticks out (frog eyes, bumps, dots)."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*Small rounded bump — stuff lightly for a 3D effect.*\n")

        stitches = {"tiny": 6, "small": 8, "medium": 10, "large": 12}.get(size, 10)

        pattern.append(self.format_round(1, f"Start {min(stitches, 6)} sc in a magic loop", min(stitches, 6)))
        if stitches > 6:
            pattern.append(self.format_round(2, f"[sc 1, inc] repeat {stitches // 2 - stitches // 4} times, sc remaining", stitches))
        pattern.append(self.format_round(3 if stitches > 6 else 2, "sc in every stitch", stitches))
        pattern.append(self.format_round(4 if stitches > 6 else 3, f"dec {stitches // 2} times", stitches // 2))

        pattern.append("\n**Finish:** Fasten off. Stuff lightly. Leave a long tail for sewing.\n")
        return "\n".join(pattern)

    # ──────────────────────────────────────────────
    #  ASSEMBLY SECTION
    # ──────────────────────────────────────────────

    def generate_assembly(self, pattern_data):
        """
        Generate assembly instructions based on the parts list.
        Uses the 'position' field from each part to explain where to sew things.
        """
        # Filter out parts that are likely the main body (nothing to attach)
        body_names = {"body", "head & body", "head and body", "main body"}
        attachable_parts = []
        for part in pattern_data:
            name_lower = part.get("name", "").lower().split(" (make")[0].strip()
            if name_lower not in body_names:
                attachable_parts.append(part)

        if not attachable_parts:
            return ""

        section = "\n---\n## ASSEMBLY\n"
        section += "*Use a yarn needle and the long tails you left on each piece.*\n\n"

        for i, part in enumerate(attachable_parts, 1):
            name = part.get("name", "Part")
            position = part.get("position", "")

            if position:
                section += f"**Step {i}:** Sew the **{name}** to the {position}.\n"
            else:
                section += f"**Step {i}:** Sew the **{name}** to the body.\n"

        section += f"\n**Step {len(attachable_parts) + 1}:** Weave in all remaining yarn tails.\n"
        section += "\n*TIP: Pin pieces in place with sewing pins before stitching to check the look!*\n"
        return section


if __name__ == "__main__":
    import sys
    engine = BeginnerPatternGenerator()

    test_parts = [
        {"type": "oval", "name": "Body", "color": "White", "position": "center",
         "max_stitches": 24, "height": 7},
        {"type": "sphere", "name": "Head", "color": "White with brown stripes", "position": "top of body",
         "max_stitches": 18, "height": 4},
        {"type": "flat_leaf", "name": "Wing (Make 2)", "color": "White and brown", "position": "sides of body",
         "length": 6},
        {"type": "cone", "name": "Beak", "color": "Orange", "position": "front of head",
         "base": 6, "height": 2},
    ]

    full_pattern = engine.add_header()
    full_pattern += engine.generate_materials(test_parts)
    full_pattern += "## TEST BIRD\n\n"
    for part in test_parts:
        full_pattern += engine.generate_part(part)
    full_pattern += engine.generate_assembly(test_parts)

    engine.save_to_pdf("Test_Bird_Pattern.pdf", full_pattern)
    print("\nDone! Check Test_Bird_Pattern.pdf")
