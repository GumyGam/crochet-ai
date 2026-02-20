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
- Include ALL visible parts, even tiny details (eyes, nose, beak, feet, markings)
- Do NOT invent parts you cannot see — only describe what is visible
- Be precise about colors, noting stripes, patterns, or gradients
- If head and body are one continuous piece, combine them as one part
- "position" describes where this part connects for assembly"""

        if user_text:
            prompt += f"""

USER INSTRUCTIONS (these override what you see):
\"{user_text}\"
- Only include parts that match the user's description
- If the user says to ignore something, DO NOT include it
- If the user specifies colors or features, use those instead of what you see"""

        prompt += """

Return ONLY valid JSON in this exact format (no markdown, no explanation):
{
  "creature_type": "bird",
  "parts": [
    {"type": "oval", "name": "Body", "color": "White", "size": "large", "count": 1, "position": "center"},
    {"type": "sphere", "name": "Head", "color": "White with brown stripes", "size": "medium", "count": 1, "position": "top of body"}
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

        # ── Convert to pattern engine format ──
        parts = analysis.get("parts", [])
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

    def _convert_to_pattern_format(self, parts):
        """
        Convert AI-detected parts into the format the pattern engine expects.
        Maps size labels (tiny/small/medium/large) to actual stitch counts.
        """
        pattern_parts = []

        for part in parts:
            size = part.get("size", "medium").lower()
            if size not in ("tiny", "small", "medium", "large"):
                size = "medium"

            count = part.get("count", 1)
            part_type = part.get("type", "sphere")
            position = part.get("position", "")
            color = part.get("color", "Unknown")

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
