"""
Vision Analyzer - Uses Ollama's llava model to analyze images
and extract structured pattern data for crochet pattern generation.

Pipeline:
  Round 1: AI looks at image + user text → identifies parts
  Round 2: AI reviews its own work → catches mistakes
  User text filtering is built into both rounds (user text always wins)
"""

import ollama
import json
from pathlib import Path

# Every shape type the pattern engine can generate.
# This list is passed to the AI so it knows what options it has.
SUPPORTED_SHAPES = {
    "sphere": "Round/ball shapes (heads, round bodies, balls, eyes)",
    "oval": "Egg or oval shapes (bird bodies, elongated heads, beans)",
    "cylinder": "Tube/column shapes (legs, arms, necks, stems, pots)",
    "cone": "Pointy/tapered shapes (ears, horns, beaks, small noses, carrots)",
    "dome": "Half-sphere, flat on bottom (mushroom caps, turtle shells, hats)",
    "flat_circle": "Small flat round shapes (round ears, paw pads, spots, eye patches)",
    "flat_leaf": "Simple flat rectangle/strip (simple leaves, scarves, flat wings)",
    "tapered_tube": "Tube that gradually gets thinner (tails, tentacles, snakes)",
    "fan": "Fan or spread-out shape (bird tails, fish tails, ruffles)",
    "bird_feet": "Small forked/branching feet (bird or chicken feet)",
    "heart_leaf": "Heart-shaped or organic curvy leaves (Monstera, fancy leaves)",
    "wing": "Triangular bat/dragon wings with jagged edges",
    "petals": "Small loops attached around a circular center (flower petals)",
    "spikes": "Tiny triangular protrusions (dinosaur spikes, hedgehog spines)",
    "bobble": "Round bumps that stick out (frog/bug eyes, textured dots)",
}


class VisionAnalyzer:
    def __init__(self, model="llava"):
        self.model = model

    def _build_shapes_list(self):
        """Format the supported shapes into a readable list for the AI prompt."""
        lines = []
        for shape_name, description in SUPPORTED_SHAPES.items():
            lines.append(f"  - {shape_name}: {description}")
        return "\n".join(lines)

    def _build_analysis_prompt(self, user_text=None):
        """
        Build the Round 1 prompt. This is the main prompt that asks the AI
        to analyze the image and identify all parts.
        """
        shapes_list = self._build_shapes_list()

        prompt = f"""You are an expert crochet amigurumi pattern designer.
Analyze this image carefully and identify every visible part.

AVAILABLE SHAPE TYPES (pick the best match for each part):
{shapes_list}

For EACH visible part, identify:
1. shape type (from the list above)
2. part name (be specific: "Body", "Head", "Left Wing", "Beak", "Eye", etc.)
3. color (be precise: "White with brown stripes on top" not just "White")
4. size: tiny, small, medium, or large (relative to the whole figure)
5. count: how many of this part (e.g., 2 wings, 4 legs, 2 eyes)
6. position: where this attaches on the figure (e.g., "top of body", "sides of body", "front of head", "bottom center")

CRITICAL RULES:
- You MUST list at least 3-5 parts. Most figures have a body, head, AND additional features.
- Include ALL visible parts, even tiny details (eyes, nose, beak, feet, wings, tail, markings)
- Do NOT invent parts you cannot see — only describe what is visible
- Be precise about colors, noting stripes, patterns, or gradients
- If head and body are one continuous piece, combine them as one part
- "position" describes where this part connects for assembly
- Do NOT just say "Body" and "Head" — look carefully for wings, limbs, facial features, and details"""

        if user_text:
            prompt += f"""

USER INSTRUCTIONS (these override what you see):
\"{user_text}\"
- Only include parts that match the user's description
- If the user says to ignore something, DO NOT include it
- If the user specifies colors or features, use those instead of what you see"""

        prompt += """

IMPORTANT: The example below is ONLY to show the JSON format.
Do NOT copy the example values — analyze the ACTUAL image and describe what YOU see.
Include ALL parts you can identify (body, head, eyes, beak, wings, tail, feet, accessories, etc.).

Return ONLY valid JSON (no markdown, no explanation):
{
  "creature_type": "<what this is>",
  "parts": [
    {"type": "<shape>", "name": "<part name>", "color": "<exact color>", "size": "<tiny|small|medium|large>", "count": <number>, "position": "<where it attaches>"},
    {"type": "<shape>", "name": "<another part>", "color": "<exact color>", "size": "<size>", "count": <number>, "position": "<position>"}
  ]
}"""

        return prompt

    def _build_validation_prompt(self, analysis_json, user_text=None):
        """
        Build the Round 2 prompt. This sends the AI's own analysis back
        and asks it to review for mistakes.
        """
        parts_summary = json.dumps(analysis_json, indent=2)

        prompt = f"""Look at this image again carefully.

I previously analyzed it and found these parts:
{parts_summary}

Please check:
1. Are there VISIBLE parts I missed? (eyes, nose, beak, feet, tail, color markings, accessories?)
2. Are the colors accurate? Look for stripes, patterns, or color changes I missed.
3. Are the shape types correct? (Would "oval" fit better than "sphere"? Is a "tapered_tube" better than "cylinder"?)
4. Are any parts listed that AREN'T actually in the image? Remove those.
5. Are the positions/attachments correct for assembly?"""

        if user_text:
            prompt += f"""

Remember the user said: \"{user_text}\"
Only keep parts that match what the user wants."""

        prompt += """

Return the CORRECTED full JSON in the same format.
If everything looks correct, return it unchanged.
Return ONLY valid JSON, no other text:
{
  "creature_type": "...",
  "parts": [...]
}"""

        return prompt

    def analyze(self, image_path=None, user_text=None):
        """
        Main entry point. Runs the full analysis pipeline:
          Round 1: Initial analysis
          Round 2: Self-check (only when we have an image to re-examine)

        Args:
            image_path: Path to image file (optional)
            user_text:  User's text description (optional)

        Returns:
            dict with:
              - creature_type (str): what kind of thing this is
              - raw_parts (list): the AI's part descriptions
              - pattern_data (list): converted for the pattern engine
            or None if analysis fails
        """
        if not image_path and not user_text:
            raise ValueError("Need at least an image or text description")

        # ── ROUND 1: Initial analysis ──
        prompt = self._build_analysis_prompt(user_text)

        messages = [{"role": "user", "content": prompt}]
        if image_path:
            messages[0]["images"] = [str(image_path)]

        print(f"[Round 1] Analyzing {'image' if image_path else 'text only'}...")

        response = ollama.chat(model=self.model, messages=messages)
        response_text = response["message"]["content"]
        print(f"[Round 1] Response:\n{response_text}\n")

        analysis = self._parse_json_response(response_text)
        if not analysis:
            print("[Round 1] Failed to parse AI response, using fallback")
            return {
                "creature_type": "unknown",
                "raw_parts": [],
                "pattern_data": self._create_fallback_pattern(),
            }

        # ── ROUND 2: Self-check (only with images — we need something to look at again) ──
        if image_path:
            print("[Round 2] AI self-check...")
            validation_prompt = self._build_validation_prompt(analysis, user_text)

            try:
                val_response = ollama.chat(
                    model=self.model,
                    messages=[{
                        "role": "user",
                        "content": validation_prompt,
                        "images": [str(image_path)],
                    }],
                )
                val_text = val_response["message"]["content"]
                print(f"[Round 2] Response:\n{val_text}\n")

                validated = self._parse_json_response(val_text)
                if validated:
                    analysis = validated
                    print("[Round 2] Self-check complete, using corrected analysis")
                else:
                    print("[Round 2] Could not parse validation response, keeping Round 1 result")
            except Exception as e:
                print(f"[Round 2] Validation failed ({e}), keeping Round 1 result")

        # ── Validate and convert to pattern engine format ──
        parts = analysis.get("parts", [])
        parts = self._validate_parts(parts)
        pattern_data = self._convert_to_pattern_format(parts)

        return {
            "creature_type": analysis.get("creature_type", "unknown"),
            "raw_parts": parts,
            "pattern_data": pattern_data,
        }

    def _parse_json_response(self, response_text):
        """
        Extract a JSON object from the AI's response text.
        Handles both the new format {"creature_type":..., "parts":[...]}
        and the old format (plain array [...]).
        """
        # Try to find a JSON object first (new format)
        obj_start = response_text.find("{")
        obj_end = response_text.rfind("}") + 1
        if obj_start != -1 and obj_end > 0:
            try:
                result = json.loads(response_text[obj_start:obj_end])
                if "parts" in result:
                    return result
            except json.JSONDecodeError:
                pass

        # Fall back to finding a JSON array (old format / simpler AI response)
        arr_start = response_text.find("[")
        arr_end = response_text.rfind("]") + 1
        if arr_start != -1 and arr_end > 0:
            try:
                parts = json.loads(response_text[arr_start:arr_end])
                return {"creature_type": "unknown", "parts": parts}
            except json.JSONDecodeError:
                pass

        return None

    def _clean_color(self, color, part_name):
        """
        Clean up AI color descriptions into usable yarn color names.

        Handles two problems:
        1. References to other body parts:
           "Blue, with white on wings" → "Blue" (for a non-wing piece)
        2. Narrative/descriptive phrases that aren't color names:
           "White with black details and a small tuft at the tip" → "White with black"
        """
        if not color:
            return "Unknown"

        # Step 1: Remove references to OTHER body parts
        other_parts = ["wing", "tail", "head", "body", "leg", "arm",
                       "beak", "ear", "foot", "feet", "eye", "nose"]
        part_name_lower = part_name.lower()
        other_parts = [p for p in other_parts if p not in part_name_lower]

        segments = [s.strip() for s in color.replace(";", ",").split(",")]
        cleaned = []
        for segment in segments:
            mentions_other = any(part in segment.lower() for part in other_parts)
            if not mentions_other:
                cleaned.append(segment)

        result = ", ".join(cleaned) if cleaned else color.split(",")[0].strip()

        # Step 2: Cut off narrative/descriptive phrases that aren't color info.
        # These are phrases the AI adds that describe texture, position, or shape
        # rather than actual yarn color.
        cutoff_phrases = [
            " details", " and a small", " at the ", " on the ",
            " matching ", " same as ", " similar to ",
            " around the ", " along the ", " near the ",
            " of the ", " from the ", " tuft",
        ]
        result_lower = result.lower()
        earliest_cut = len(result)
        for phrase in cutoff_phrases:
            pos = result_lower.find(phrase)
            if pos != -1 and pos < earliest_cut:
                earliest_cut = pos

        if earliest_cut < len(result):
            result = result[:earliest_cut].strip().rstrip(",")

        # Step 3: Remove dangling filler words left after cutting.
        # E.g. "Orange with small" → "Orange" (the "with small" is incomplete)
        dangling = ["with", "and", "a", "an", "the", "small", "large",
                     "on", "in", "at", "for", "from", "to", "near"]
        words = result.split()
        while len(words) > 1 and words[-1].lower().rstrip(",") in dangling:
            words.pop()
        result = " ".join(words)

        # Step 4: If still too long, truncate at last full word before 50 chars
        if len(result) > 50:
            result = result[:50].rsplit(" ", 1)[0]

        return result if result else "Unknown"

    def _convert_to_pattern_format(self, parts):
        """
        Convert AI-detected parts into the format the pattern engine expects.
        Maps size labels (tiny/small/medium/large) to actual stitch counts.
        Also auto-corrects common AI mistakes (e.g. eyes as cylinders).
        """
        pattern_parts = []

        for part in parts:
            size = part.get("size", "medium").lower()
            if size not in ("tiny", "small", "medium", "large"):
                size = "medium"

            count = part.get("count", 1)
            part_type = part.get("type", "sphere")
            position = part.get("position", "")
            color = self._clean_color(part.get("color", "Unknown"), part.get("name", "Part"))

            # Auto-correct eyes: the AI often picks oversized or wrong shapes.
            #  - cylinder eyes → flat_circle (tubes don't look like eyes)
            #  - sphere/oval eyes → flat_circle (3D balls are way too big)
            #  - medium/large eyes → capped to small (eyes should be tiny/small)
            name_lower = part.get("name", "").lower()
            if "eye" in name_lower:
                oversized_3d = part_type in ("sphere", "oval") and size in ("medium", "large")
                wrong_shape = part_type == "cylinder"

                if oversized_3d or wrong_shape:
                    old_desc = f"{part_type}/{size}"
                    part_type = "flat_circle"
                    size = "small"
                    print(f"[Auto-fix] Eye '{part.get('name')}': {old_desc} → flat_circle/small")

            part_name = part.get("name", "Part")
            if count > 1:
                part_name = f"{part_name} (Make {count})"

            base = {
                "name": part_name,
                "color": color,
                "position": position,
            }

            if part_type == "sphere":
                base.update({
                    "type": "sphere",
                    "max_stitches": {"tiny": 12, "small": 18, "medium": 24, "large": 30}[size],
                    "height": {"tiny": 2, "small": 3, "medium": 5, "large": 8}[size],
                })

            elif part_type == "oval":
                base.update({
                    "type": "oval",
                    "max_stitches": {"tiny": 12, "small": 18, "medium": 24, "large": 30}[size],
                    "height": {"tiny": 3, "small": 5, "medium": 7, "large": 10}[size],
                })

            elif part_type == "cylinder":
                base.update({
                    "type": "cylinder",
                    "width": {"tiny": 6, "small": 6, "medium": 12, "large": 18}[size],
                    "height": {"tiny": 2, "small": 3, "medium": 6, "large": 10}[size],
                })

            elif part_type == "cone":
                base.update({
                    "type": "cone",
                    "base": {"tiny": 6, "small": 8, "medium": 12, "large": 16}[size],
                    "height": {"tiny": 2, "small": 4, "medium": 6, "large": 8}[size],
                })

            elif part_type == "dome":
                base.update({
                    "type": "dome",
                    "max_stitches": {"tiny": 12, "small": 18, "medium": 24, "large": 36}[size],
                })

            elif part_type == "flat_circle":
                base.update({
                    "type": "flat_circle",
                    "max_stitches": {"tiny": 12, "small": 18, "medium": 24, "large": 30}[size],
                })

            elif part_type == "flat_leaf":
                base.update({
                    "type": "flat_leaf",
                    "length": {"tiny": 4, "small": 6, "medium": 10, "large": 15}[size],
                })

            elif part_type == "tapered_tube":
                base.update({
                    "type": "tapered_tube",
                    "start_width": {"tiny": 8, "small": 12, "medium": 16, "large": 24}[size],
                    "end_width": 6,
                    "height": {"tiny": 3, "small": 5, "medium": 8, "large": 12}[size],
                })

            elif part_type == "fan":
                base.update({"type": "fan", "size": size})

            elif part_type == "bird_feet":
                base.update({"type": "bird_feet", "size": size})

            elif part_type == "heart_leaf":
                base.update({"type": "heart_leaf", "size": size})

            elif part_type == "wing":
                base.update({"type": "wing", "size": size})

            elif part_type == "petals":
                base.update({
                    "type": "petals",
                    "num_petals": {"tiny": 4, "small": 6, "medium": 8, "large": 12}[size],
                    "attachment": "edge",
                })

            elif part_type == "spikes":
                base.update({
                    "type": "spikes",
                    "num_spikes": count if count > 1 else 5,
                })

            elif part_type == "bobble":
                base.update({"type": "bobble", "size": size})

            else:
                print(f"[Warning] Unknown shape '{part_type}' for '{part_name}', defaulting to sphere")
                base.update({
                    "type": "sphere",
                    "max_stitches": 18,
                    "height": 3,
                })

            pattern_parts.append(base)

        return pattern_parts

    def _validate_parts(self, parts):
        """
        Safety net: checks that essential parts exist.
        If the AI forgot to include a body, we add a sensible default
        so the pattern isn't missing its biggest piece.
        """
        body_keywords = {"body", "torso", "main body", "head & body", "head and body"}
        has_body = any(
            p.get("name", "").lower().split(" (make")[0].strip() in body_keywords
            for p in parts
        )

        if not has_body and len(parts) > 0:
            print("[Validate] No body part found — adding a default body")

            biggest_size = "medium"
            for p in parts:
                if p.get("size") == "large":
                    biggest_size = "large"
                    break

            default_body = {
                "type": "oval",
                "name": "Body",
                "color": parts[0].get("color", "Unknown").split(" with ")[0],
                "size": biggest_size,
                "count": 1,
                "position": "center",
            }
            parts.insert(0, default_body)

        return parts

    def _create_fallback_pattern(self):
        """Last resort if AI analysis fails completely."""
        return [{
            "type": "sphere",
            "name": "Body",
            "color": "Unknown",
            "position": "center",
            "max_stitches": 24,
            "height": 6,
        }]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python vision_analyzer.py <image_path> [optional text]")
        sys.exit(1)

    analyzer = VisionAnalyzer()
    image_path = sys.argv[1]
    user_text = sys.argv[2] if len(sys.argv) > 2 else None

    result = analyzer.analyze(image_path, user_text)

    if result:
        print("\n=== Analysis Result ===")
        print(f"Creature type: {result['creature_type']}")
        print(f"Raw parts:\n{json.dumps(result['raw_parts'], indent=2)}")
        print(f"Pattern data:\n{json.dumps(result['pattern_data'], indent=2)}")
    else:
        print("Analysis failed.")
