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
            "magic ring": "adjustable ring to start rounds (or ch 2, sc 6 in 2nd ch from hook)",
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
            clean_line = clean_line.replace("\u2014", "-").replace("\u2013", "-").replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')

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
        header += "- **Magic ring:** If the magic ring is too hard, you can 'Chain 2' and make 6 sc into the second chain from the hook.\n\n"
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

    def _fmt_sc(self, count):
        """
        Format sc (single crochet) notation the standard way:
          1  → 'sc'        (real patterns never write 'sc 1')
          5  → '5 sc'      (number BEFORE stitch name)
        """
        if count == 1:
            return "sc"
        return f"{count} sc"

    def format_round(self, round_num, instruction, count, tip=None):
        """
        Formats a single round with optional beginner tip.
        Uses standard pattern notation:
          - Single round:  **Rnd 5:** ...
          - Range:         **Rnds 5-9:** ...
          - Stitch count:  (24) — no 'sts' suffix
        """
        rnd_str = str(round_num)
        if "-" in rnd_str or "to" in rnd_str.lower():
            label = f"Rnds {rnd_str}"
        else:
            label = f"Rnd {rnd_str}"
        line = f"**{label}:** {instruction} ({count})"
        if tip:
            line += f"\n   *TIP: {tip}*"
        return line

    def format_row(self, row_num, instruction, count=None):
        """Formats a single row for flat pieces."""
        line = f"**Row {row_num}:** {instruction}"
        if count is not None:
            line += f" ({count})"
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
        pattern.append(self.format_round(1, "6 sc in a magic ring", 6,
                                          "Pull the tail tight to close the hole!"))

        rnd = 2
        while current_stitches < max_stitches:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "6 inc", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(
                    rnd, f"[{self._fmt_sc(sc_count)}, inc] x 6", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        even_end = rnd + height_rows - 1
        pattern.append(self.format_round(
            f"{rnd}-{even_end}",
            f"{current_stitches} sc", current_stitches,
            "Just go round and round!"))
        rnd += height_rows

        if "head" in name.lower():
            eye_rnd = max(rnd - height_rows - 1, 3)
            pattern.append(f"\n**STOP!** If you are using safety eyes, attach them now between Rnds {eye_rnd} and {eye_rnd + 1}.\n")

        while current_stitches > 6:
            sc_count = (current_stitches // 6) - 2
            if sc_count > 0:
                pattern.append(self.format_round(
                    rnd, f"[{self._fmt_sc(sc_count)}, dec] x 6", current_stitches - 6))
            else:
                pattern.append(self.format_round(rnd, "6 dec", current_stitches - 6))

            if current_stitches - 6 <= 12 and current_stitches > 12:
                pattern.append("   *Stuff the piece firmly with stuffing now!*")

            current_stitches -= 6
            rnd += 1

        pattern.append("\n**Finish:** Fasten off leaving a long tail. Thread a needle with the tail, then pull the yarn through the front loops of each remaining stitch. Pull tight to close.\n")
        return "\n".join(pattern)

    def generate_cylinder(self, name, color, width_stitches=12, height_rows=8):
        """Open-ended tube: increase to width, then work even."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("This piece is worked in continuous rounds.\n")

        current_stitches = 6
        pattern.append(self.format_round(1, "6 sc in a magic ring", 6))

        rnd = 2
        while current_stitches < width_stitches:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "6 inc", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(
                    rnd, f"[{self._fmt_sc(sc_count)}, inc] x 6", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        even_end = rnd + height_rows - 1
        pattern.append(self.format_round(
            f"{rnd}-{even_end}",
            f"{current_stitches} sc", current_stitches))

        pattern.append("\n**Finish:** Fasten off leaving a long tail for sewing. Stuff lightly.\n")
        return "\n".join(pattern)

    def generate_cone(self, name, color, base_stitches=12, height_rows=6):
        """
        Tapered cone: gradual increases from a narrow tip.
        Based on real patterns (like Luna the Bat ears, Mandrake leaves):
        Start at 4 sc, increase by 2 each increase round using [N sc, inc] x 2.
        Even rounds are spread between increases when height allows.
        """
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("This piece is worked in continuous rounds from the tip down.\n")

        start_stitches = 4
        pattern.append(self.format_round(1, f"{start_stitches} sc in a magic ring", start_stitches))
        current_stitches = start_stitches
        rnd = 2

        inc_rounds_needed = (base_stitches - start_stitches) // 2
        total_rounds = height_rows
        even_rounds_available = max(0, total_rounds - inc_rounds_needed)

        if inc_rounds_needed > 0:
            even_spacing = even_rounds_available / inc_rounds_needed
        else:
            even_spacing = total_rounds

        inc_done = 0
        even_budget = 0.0

        while rnd <= total_rounds + 1:
            if current_stitches < base_stitches:
                sc_before = (current_stitches // 2) - 1
                if sc_before > 0:
                    pattern.append(self.format_round(
                        rnd, f"[{self._fmt_sc(sc_before)}, inc] x 2", current_stitches + 2))
                else:
                    pattern.append(self.format_round(rnd, "2 inc, 2 sc", current_stitches + 2))
                current_stitches += 2
                inc_done += 1
                even_budget += even_spacing
                rnd += 1

                even_now = int(even_budget)
                if even_now > 0 and rnd <= total_rounds + 1:
                    if even_now == 1:
                        pattern.append(self.format_round(rnd, f"{current_stitches} sc", current_stitches))
                    else:
                        end_rnd = min(rnd + even_now - 1, total_rounds + 1)
                        if end_rnd > rnd:
                            pattern.append(self.format_round(f"{rnd}-{end_rnd}", f"{current_stitches} sc", current_stitches))
                        else:
                            pattern.append(self.format_round(rnd, f"{current_stitches} sc", current_stitches))
                        even_now = end_rnd - rnd + 1
                    rnd += even_now
                    even_budget -= even_now
            else:
                remaining = total_rounds + 1 - rnd + 1
                if remaining == 1:
                    pattern.append(self.format_round(rnd, f"{current_stitches} sc", current_stitches))
                elif remaining > 1:
                    pattern.append(self.format_round(f"{rnd}-{rnd + remaining - 1}", f"{current_stitches} sc", current_stitches))
                break

        pattern.append("\n**Finish:** Fasten off leaving a long tail for sewing. Stuff gently.\n")
        return "\n".join(pattern)

    def generate_flat_leaf(self, name, color, length_chains=10):
        """Simple flat strip worked in rows."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*This part is worked in rows, not rounds. Turn your work at the end of each row.*\n")

        sc_count = length_chains - 1
        pattern.append(self.format_row(1, f"Ch {length_chains}"))
        pattern.append(self.format_row(2, f"Sc in 2nd ch from hook, {self._fmt_sc(sc_count - 1)}, ch 1 and turn", sc_count))
        pattern.append(self.format_row(3, f"{self._fmt_sc(sc_count)}, ch 1 and turn", sc_count))
        pattern.append(self.format_row(4, f"{self._fmt_sc(sc_count)}", sc_count))

        pattern.append("\n**Finish:** Fasten off leaving a long tail for sewing.\n")
        return "\n".join(pattern)

    def generate_heart_leaf(self, name, color, size="medium"):
        """Heart-shaped leaf with chain spaces for the indent."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*This leaf is worked in rows with chain spaces to create the heart shape.*\n")

        base_chains = {"tiny": 2, "small": 2, "medium": 2, "large": 3}.get(size, 2)

        pattern.append(self.format_row(1, f"Ch {base_chains}"))
        pattern.append(self.format_row(2, "Inc in 2nd ch from hook, ch 1 and turn", base_chains))
        pattern.append(self.format_row(3, "2 inc, ch 1 and turn", 4))
        pattern.append(self.format_row(4, "Inc, 2 sc, inc, ch 3 and turn", 6))
        pattern.append(self.format_row(5, "Sk 2 sts, 2 sc, ch 3, sk 1 st, sl st, ch 1 and turn", 6))
        pattern.append("   *TIP: The chain-3 spaces create the heart indent at top.*")
        pattern.append(self.format_row(6, "Sk 1 st, 3 sc in ch-3 space, 2 sc, 3 sc in ch-3 space, ch 1 and turn", 8))
        pattern.append(self.format_row(7, "Sc, hdc, dc, dc, hdc, sc around the edge"))

        pattern.append("\n**Finish:** Fasten off leaving a long tail for sewing.\n")
        return "\n".join(pattern)

    def generate_wing(self, name, color, size="medium"):
        """
        Triangular wing that tapers from wide base to narrow tip.
        Each row decreases by 2 stitches (dec on both edges)
        to create the wing/triangle shape.
        """
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*Wings are worked in rows. Ch 1 and turn at the end of each row.*\n")

        base_chains = {"tiny": 6, "small": 8, "medium": 11, "large": 14}.get(size, 11)

        pattern.append(self.format_row(1, f"Ch {base_chains}"))
        width = base_chains - 1
        pattern.append(self.format_row(
            2, f"Sc in 2nd ch from hook, {self._fmt_sc(width - 1)}, ch 1 and turn", width))

        row_num = 3
        while width > 4:
            new_width = width - 2
            inner = new_width - 2
            pattern.append(self.format_row(
                row_num, f"Dec, {self._fmt_sc(inner)}, dec, ch 1 and turn", new_width))
            width = new_width
            row_num += 1

        pattern.append(self.format_row(row_num, f"{self._fmt_sc(width)}", width))

        pattern.append("\n**Finish:** Fasten off leaving a long tail for sewing.\n")
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
        pattern.append(f"\n**Step 5:** Sk 1-2 sts, repeat Steps 1-4 for the next petal.")
        pattern.append(f"**Step 6:** Repeat until you have {num_petals} petals evenly spaced.")

        pattern.append("\n**Finish:** Fasten off and weave in ends.\n")
        return "\n".join(pattern)

    def generate_spikes(self, name, color, num_spikes=5):
        """Small triangular spikes."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn, make {num_spikes})")
        pattern.append("*Each spike is a tiny triangle.*\n")

        pattern.append(self.format_round(1, "4 sc in a magic ring", 4))
        pattern.append(self.format_round(2, "[sc, inc] x 2", 6))

        pattern.append("\n**Finish:** Fasten off leaving a long tail. Sew spikes evenly along the back.\n")
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
        pattern.append(self.format_round(1, "6 sc in a magic ring", 6,
                                          "Pull the tail tight to close the hole!"))

        rnd = 2
        while current_stitches < max_stitches:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "6 inc", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(
                    rnd, f"[{self._fmt_sc(sc_count)}, inc] x 6", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        even_end = rnd + height_rows - 1
        pattern.append(self.format_round(
            f"{rnd}-{even_end}",
            f"{current_stitches} sc", current_stitches,
            "These extra even rounds create the oval/egg shape!"))
        rnd += height_rows

        if "head" in name.lower():
            eye_rnd = max(rnd - height_rows, 3)
            pattern.append(f"\n**STOP!** If you are using safety eyes, attach them now between Rnds {eye_rnd} and {eye_rnd + 1}.\n")

        while current_stitches > 6:
            sc_count = (current_stitches // 6) - 2
            if sc_count > 0:
                pattern.append(self.format_round(
                    rnd, f"[{self._fmt_sc(sc_count)}, dec] x 6", current_stitches - 6))
            else:
                pattern.append(self.format_round(rnd, "6 dec", current_stitches - 6))

            if current_stitches - 6 <= 12 and current_stitches > 12:
                pattern.append("   *Stuff the piece firmly with stuffing now!*")

            current_stitches -= 6
            rnd += 1

        pattern.append("\n**Finish:** Fasten off leaving a long tail. Thread a needle with the tail, then pull the yarn through the front loops of each remaining stitch. Pull tight to close.\n")
        return "\n".join(pattern)

    def generate_dome(self, name, color, max_stitches=24):
        """Half-sphere: increase only, no decrease. Flat on the bottom."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("This piece is worked in continuous rounds (dome/half-sphere, flat on the bottom).\n")

        current_stitches = 6
        pattern.append(self.format_round(1, "6 sc in a magic ring", 6))

        rnd = 2
        while current_stitches < max_stitches:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "6 inc", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(
                    rnd, f"[{self._fmt_sc(sc_count)}, inc] x 6", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        pattern.append(self.format_round(f"{rnd}-{rnd + 1}", f"{current_stitches} sc", current_stitches))

        pattern.append("\n**Finish:** Fasten off leaving a long tail for sewing. Stuff before attaching.\n")
        return "\n".join(pattern)

    def generate_flat_circle(self, name, color, max_stitches=18):
        """Flat disc: increase rounds only, no height. For ears, pads, spots."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*This piece stays flat — do not stuff.*\n")

        current_stitches = 6
        pattern.append(self.format_round(1, "6 sc in a magic ring", 6))

        rnd = 2
        while current_stitches < max_stitches:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "6 inc", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(
                    rnd, f"[{self._fmt_sc(sc_count)}, inc] x 6", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        pattern.append("\n**Finish:** Fasten off leaving a long tail for sewing.\n")
        return "\n".join(pattern)

    def generate_tapered_tube(self, name, color, start_width=12, end_width=6, height_rows=8):
        """Tube that starts wide and gradually narrows (tails, tentacles)."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*This piece starts wide and tapers to a point.*\n")

        current_stitches = 6
        pattern.append(self.format_round(1, "6 sc in a magic ring", 6))

        rnd = 2
        while current_stitches < start_width:
            if rnd == 2:
                pattern.append(self.format_round(rnd, "6 inc", 12))
                current_stitches = 12
            else:
                sc_count = (current_stitches // 6) - 1
                pattern.append(self.format_round(
                    rnd, f"[{self._fmt_sc(sc_count)}, inc] x 6", current_stitches + 6))
                current_stitches += 6
            rnd += 1

        even_rows = max(2, height_rows // 3)
        even_end = rnd + even_rows - 1
        pattern.append(self.format_round(
            f"{rnd}-{even_end}",
            f"{current_stitches} sc", current_stitches))
        rnd += even_rows

        while current_stitches > end_width:
            decrease = min(6, current_stitches - end_width)
            repeat = decrease
            # -2 because each dec consumes 2 stitches from the previous round
            # (same formula the sphere uses for its decrease rounds)
            sc_per = (current_stitches // repeat) - 2
            if sc_per > 0:
                pattern.append(self.format_round(
                    rnd, f"[{self._fmt_sc(sc_per)}, dec] x {repeat}", current_stitches - repeat))
            else:
                # Not enough room for sc between decreases — use plain decs
                pattern.append(self.format_round(
                    rnd, f"{repeat} dec", current_stitches - repeat))
            current_stitches -= repeat
            rnd += 1

        pattern.append("\n**Finish:** Fasten off leaving a long tail for sewing. Stuff the wide end lightly.\n")
        return "\n".join(pattern)

    def generate_fan(self, name, color, size="medium"):
        """Fan/spread shape for bird tails, fish tails, ruffles."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*This piece is worked in rows and fans out from narrow to wide.*\n")

        base_ch = {"tiny": 4, "small": 5, "medium": 6, "large": 8}.get(size, 6)

        pattern.append(self.format_row(1, f"Ch {base_ch}"))
        pattern.append(self.format_row(2, f"Sc in 2nd ch from hook, {self._fmt_sc(base_ch - 2)}, ch 1 and turn", base_ch - 1))
        pattern.append(self.format_row(3, f"Inc, {self._fmt_sc(base_ch - 3)}, inc, ch 1 and turn", base_ch + 1))
        pattern.append(self.format_row(4, f"Inc, {self._fmt_sc(base_ch - 1)}, inc, ch 1 and turn", base_ch + 3))
        pattern.append(self.format_row(5, f"Inc, {self._fmt_sc(base_ch + 1)}, inc", base_ch + 5))
        pattern.append("   *TIP: The increases on both edges create the fan/spread shape.*")

        pattern.append("\n**Finish:** Fasten off leaving a long tail for sewing.\n")
        return "\n".join(pattern)

    def generate_bird_feet(self, name, color, size="medium"):
        """Simple forked bird feet using chains for toes."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*Each foot has 3 toes made from chains.*\n")

        toe_len = {"tiny": 3, "small": 4, "medium": 5, "large": 6}.get(size, 5)
        leg_len = {"tiny": 3, "small": 4, "medium": 5, "large": 6}.get(size, 5)

        pattern.append(f"**Leg:** Ch {leg_len}, sc in 2nd ch from hook, {self._fmt_sc(leg_len - 2)}. Do not turn.")
        pattern.append(f"**Toe 1:** Ch {toe_len}, sl st in 2nd ch from hook, {toe_len - 2} sl st back to leg.")
        pattern.append(f"**Toe 2:** Ch {toe_len}, sl st in 2nd ch from hook, {toe_len - 2} sl st back to leg.")
        pattern.append(f"**Toe 3:** Ch {toe_len}, sl st in 2nd ch from hook, {toe_len - 2} sl st back to leg.")
        pattern.append("   *TIP: All 3 toes branch out from the same point at the bottom of the leg.*")

        pattern.append("\n**Finish:** Fasten off leaving a long tail for sewing.\n")
        return "\n".join(pattern)

    def generate_bobble(self, name, color, size="medium"):
        """Small rounded bump that sticks out (frog eyes, bumps, dots)."""
        pattern = []
        pattern.append(f"### {name.upper()} (Use {color} yarn)")
        pattern.append("*Small rounded bump — stuff lightly for a 3D effect.*\n")

        if size == "tiny":
            pattern.append(self.format_round(1, "6 sc in a magic ring", 6))
            pattern.append(self.format_round(2, "6 sc", 6))
            pattern.append(self.format_round(3, "3 dec", 3))
        elif size == "small":
            pattern.append(self.format_round(1, "6 sc in a magic ring", 6))
            pattern.append(self.format_round(2, "[sc, inc] x 2, 2 sc", 8))
            pattern.append(self.format_round(3, "8 sc", 8))
            pattern.append(self.format_round(4, "4 dec", 4))
        elif size == "large":
            pattern.append(self.format_round(1, "6 sc in a magic ring", 6))
            pattern.append(self.format_round(2, "6 inc", 12))
            pattern.append(self.format_round(3, "12 sc", 12))
            pattern.append(self.format_round(4, "6 dec", 6))
        else:
            pattern.append(self.format_round(1, "6 sc in a magic ring", 6))
            pattern.append(self.format_round(2, "[sc, inc] x 3", 9))
            pattern.append(self.format_round(3, "9 sc", 9))
            pattern.append(self.format_round(4, "[sc, dec] x 3", 6))

        pattern.append("\n**Finish:** Fasten off leaving a long tail. Stuff lightly before sewing.\n")
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

            # The AI sometimes returns position as a list instead of a string
            # (e.g. ['left side of head', 'right side of head']).
            # Convert lists into a readable sentence.
            if isinstance(position, list):
                position = " and ".join(str(p) for p in position)

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
