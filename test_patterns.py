"""
Test script: Runs 4 different creature patterns through the pattern engine
and validates that the stitch math is correct.

Tests:
  1. Cat   - sphere head, oval body, cone ears, cylinder legs, tapered_tube tail
  2. Flower - flat_circle center, petals, cylinder stem, flat_leaf leaves
  3. Dinosaur - sphere head, oval body, cylinder legs, spikes, tapered_tube tail
  4. Jellyfish - dome head, cylinder tentacles, bobble eyes

For each pattern, we:
  - Generate the full pattern text
  - Parse out every round/row and its stitch count
  - Simulate the actual stitches mathematically
  - Compare expected vs actual counts
  - Report any mismatches
"""

import re
from pattern_engine import BeginnerPatternGenerator
from vision_analyzer import VisionAnalyzer

# ── TEST DATA: 4 creatures with realistic AI-like part lists ──

# ── BATCH 3: Tests for the NEW round of 3 fixes ──
#
# Frog:     Tests Fix 3 (oversized oval eyes → should become flat_circle/small)
#           Tests Fix 2 (garbled color descriptions with narrative phrases)
# Owl:      Tests Fix 1 (assembly list bug — position as Python list)
#           Tests Fix 3 (medium sphere eyes → should downsize)
# Penguin:  Tests Fix 2 (colors with "details", "tuft", "at the" phrases)
#           Clean structure otherwise
# Dragon:   Tests ALL fixes together — missing body, list positions,
#           oversized eyes, and messy colors

TEST_CREATURES = {
    "Frog (oversized eyes + garbled colors)": [
        {"type": "sphere", "name": "Body", "color": "Bright green with darker green details along the back and sides of the body", "size": "medium",
         "count": 1, "position": "center"},
        {"type": "sphere", "name": "Head", "color": "Green with a small lighter patch near the mouth area", "size": "medium",
         "count": 1, "position": "top of body"},
        # These oval/medium eyes should be auto-fixed to flat_circle/small
        {"type": "oval", "name": "Eye", "color": "White with black pupil and a small highlight on the surface", "size": "medium",
         "count": 2, "position": "top of head"},
        {"type": "cylinder", "name": "Front Leg", "color": "Green matching the body color", "size": "small",
         "count": 2, "position": "front sides of body"},
        {"type": "cylinder", "name": "Back Leg", "color": "Green similar to the front legs", "size": "small",
         "count": 2, "position": "back sides of body"},
    ],

    "Owl (list positions + sphere eyes)": [
        {"type": "oval", "name": "Body", "color": "Brown", "size": "medium",
         "count": 1, "position": "center"},
        {"type": "sphere", "name": "Head", "color": "Brown with tan face disc", "size": "medium",
         "count": 1, "position": "top of body"},
        # sphere/medium eyes — should be auto-fixed to flat_circle/small
        {"type": "sphere", "name": "Eye", "color": "Yellow with black center", "size": "medium",
         "count": 2, "position": ["left side of face", "right side of face"]},
        {"type": "cone", "name": "Beak", "color": "Orange", "size": "tiny",
         "count": 1, "position": "center of face"},
        # position as a list — should be joined properly in assembly
        {"type": "cone", "name": "Ear Tuft", "color": "Dark brown", "size": "small",
         "count": 2, "position": ["top left of head", "top right of head"]},
        {"type": "flat_leaf", "name": "Wing", "color": "Brown with tan edges", "size": "medium",
         "count": 2, "position": "sides of body"},
        {"type": "fan", "name": "Tail", "color": "Brown", "size": "small",
         "count": 1, "position": "back of body"},
    ],

    "Penguin (narrative color descriptions)": [
        {"type": "oval", "name": "Body", "color": "Black with white belly details on the front half of the torso", "size": "large",
         "count": 1, "position": "center"},
        {"type": "sphere", "name": "Head", "color": "Black with white patches near the eye area on both sides", "size": "medium",
         "count": 1, "position": "top of body"},
        # large sphere eyes — should get capped to flat_circle/small
        {"type": "sphere", "name": "Eye", "color": "White with a small black dot at the center", "size": "large",
         "count": 2, "position": "sides of head"},
        {"type": "cone", "name": "Beak", "color": "Orange with yellow tips at the end of the beak", "size": "small",
         "count": 1, "position": "front of head"},
        {"type": "flat_leaf", "name": "Wing", "color": "Black, same as the body sides", "size": "medium",
         "count": 2, "position": "sides of body"},
        {"type": "flat_circle", "name": "Foot", "color": "Orange with small tuft details around the edges", "size": "small",
         "count": 2, "position": "bottom of body"},
    ],

    "Dragon (all fixes combined)": [
        # NO body — should auto-add one (Fix 1 from earlier)
        {"type": "sphere", "name": "Head", "color": "Dark green with lighter green details along the jaw and near the nose", "size": "large",
         "count": 1, "position": "front of body"},
        # sphere/large eyes — should become flat_circle/small
        {"type": "sphere", "name": "Eye", "color": "Yellow with a small black slit in the middle of the surface", "size": "large",
         "count": 2, "position": ["left side of head", "right side of head"]},
        {"type": "cone", "name": "Horn", "color": "Dark gold matching the head color somewhat", "size": "small",
         "count": 2, "position": ["top left of head", "top right of head"]},
        {"type": "wing", "name": "Wing", "color": "Dark green with lighter green membrane details on the wing surface", "size": "large",
         "count": 2, "position": "sides of body"},
        {"type": "tapered_tube", "name": "Tail", "color": "Dark green, same as body and head colors", "size": "large",
         "count": 1, "position": "back of body"},
        {"type": "spikes", "name": "Back Spike", "color": "Gold", "size": "small",
         "count": 6, "position": "along the back from head to tail"},
        {"type": "cylinder", "name": "Leg", "color": "Dark green similar to the body", "size": "small",
         "count": 4, "position": "bottom of body"},
    ],
}


def simulate_stitch_math(instruction, current_stitches):
    """
    Given a pattern instruction string and the current stitch count,
    simulate what the new stitch count should be.
    Returns (new_count, explanation) or (None, reason) if can't parse.
    """
    text = instruction.strip()

    # "6 sc in a magic ring"
    m = re.match(r"(\d+)\s+sc\s+in\s+a\s+magic\s+ring", text)
    if m:
        return int(m.group(1)), "magic ring"

    # "N inc" (all increases)
    m = re.match(r"(\d+)\s+inc$", text)
    if m:
        num_inc = int(m.group(1))
        return num_inc * 2, f"{num_inc} inc = {num_inc}*2"

    # "[N sc, inc] x M"
    m = re.match(r"\[.*?inc\]\s*x\s*(\d+)", text)
    if m:
        repeats = int(m.group(1))
        sc_match = re.search(r"(\d+)\s+sc", text)
        sc_count = int(sc_match.group(1)) if sc_match else 1
        if "sc," in text and "inc" in text and "dec" not in text:
            new = (sc_count + 2) * repeats
            return new, f"[{sc_count} sc, inc] x {repeats} = ({sc_count}+2)*{repeats}"

    # "[N sc, dec] x M"
    m = re.match(r"\[.*?dec\]\s*x\s*(\d+)", text)
    if m:
        repeats = int(m.group(1))
        sc_match = re.search(r"(\d+)\s+sc", text)
        sc_count = int(sc_match.group(1)) if sc_match else 1
        if "dec" in text:
            new = (sc_count + 1) * repeats
            return new, f"[{sc_count} sc, dec] x {repeats} = ({sc_count}+1)*{repeats}"

    # "[sc, inc] x M (without number before sc)
    m = re.match(r"\[sc,\s*inc\]\s*x\s*(\d+)", text)
    if m:
        repeats = int(m.group(1))
        return 3 * repeats, f"[sc, inc] x {repeats} = 3*{repeats}"

    # "[sc, dec] x M (without number before sc)
    m = re.match(r"\[sc,\s*dec\]\s*x\s*(\d+)", text)
    if m:
        repeats = int(m.group(1))
        return 2 * repeats, f"[sc, dec] x {repeats} = 2*{repeats}"

    # "N dec"
    m = re.match(r"(\d+)\s+dec$", text)
    if m:
        num_dec = int(m.group(1))
        return num_dec, f"{num_dec} dec = {num_dec}*1"

    # "N sc" (even round, no change)
    m = re.match(r"(\d+)\s+sc$", text)
    if m:
        return int(m.group(1)), "even round"

    # "[sc, inc] x 2, N sc" (bobble pattern)
    m = re.match(r"\[sc,\s*inc\]\s*x\s*(\d+),\s*(\d+)\s+sc", text)
    if m:
        repeats = int(m.group(1))
        extra_sc = int(m.group(2))
        return (3 * repeats) + extra_sc, f"[sc, inc] x {repeats} + {extra_sc} sc"

    # "[sc, dec] x N" (bobble decrease)
    m = re.match(r"\[sc,\s*dec\]\s*x\s*(\d+)$", text)
    if m:
        repeats = int(m.group(1))
        return 2 * repeats, f"[sc, dec] x {repeats}"

    # "N inc, M sc" (cone pattern)
    m = re.match(r"(\d+)\s+inc,\s*(\d+)\s+sc", text)
    if m:
        num_inc = int(m.group(1))
        num_sc = int(m.group(2))
        return (num_inc * 2) + num_sc, f"{num_inc} inc + {num_sc} sc"

    # "[N sc, inc] x 2" (cone pattern)
    m = re.match(r"\[(\d+\s+)?sc,\s*inc\]\s*x\s*(\d+)", text)
    if m:
        sc_part = m.group(1)
        repeats = int(m.group(2))
        sc_count = int(sc_part.strip()) if sc_part else 1
        return (sc_count + 2) * repeats, f"[{sc_count} sc, inc] x {repeats}"

    # "4 sc in a magic ring"
    m = re.match(r"(\d+)\s+sc\s+in\s+a\s+magic\s+ring", text)
    if m:
        return int(m.group(1)), "magic ring"

    return None, f"Could not parse: '{text}'"


def validate_round_based_pattern(pattern_text, part_name):
    """
    Extract all rounds from a pattern, simulate the stitch math,
    and check if the stated counts match the simulated counts.
    """
    issues = []
    rounds_checked = 0

    lines = pattern_text.split("\n")

    current_stitches = 0

    for line in lines:
        # Match "Rnd N:" or "Rnds N-M:" patterns
        rnd_match = re.match(r"\*\*Rnds?\s+([\d-]+):\*\*\s+(.+?)\s+\((\d+)\)", line)
        if not rnd_match:
            continue

        rnd_label = rnd_match.group(1)
        instruction = rnd_match.group(2).strip()
        stated_count = int(rnd_match.group(3))

        simulated, explanation = simulate_stitch_math(instruction, current_stitches)

        if simulated is not None:
            rounds_checked += 1
            if simulated != stated_count:
                issues.append(
                    f"  MISMATCH Rnd {rnd_label}: instruction '{instruction}' "
                    f"should give {simulated} stitches but pattern says ({stated_count}). "
                    f"[{explanation}]"
                )
            current_stitches = stated_count
        else:
            current_stitches = stated_count

    return rounds_checked, issues


def validate_row_based_pattern(pattern_text, part_name):
    """
    Validate row-based (flat) pieces. These are harder to simulate
    because they use chains, turns, and increases on edges.
    We check what we can.
    """
    issues = []
    rows_checked = 0

    lines = pattern_text.split("\n")
    current_stitches = 0

    for line in lines:
        row_match = re.match(r"\*\*Row\s+(\d+):\*\*\s+(.+?)(?:\s+\((\d+)\))?$", line)
        if not row_match:
            continue

        row_num = int(row_match.group(1))
        instruction = row_match.group(2).strip()
        stated_count = int(row_match.group(3)) if row_match.group(3) else None

        if stated_count is None:
            continue

        rows_checked += 1

        # Row 2 of chain-start pieces: "Sc in 2nd ch from hook, N sc" = chain - 1
        ch_start = re.match(r"Sc in 2nd ch from hook,\s*(\d+)\s+sc", instruction)
        if ch_start:
            sc_after = int(ch_start.group(1))
            expected = sc_after + 1
            if expected != stated_count:
                issues.append(
                    f"  MISMATCH Row {row_num}: 'Sc in 2nd ch from hook, {sc_after} sc' "
                    f"= {expected} stitches but says ({stated_count})"
                )
            current_stitches = stated_count
            continue

        # "Inc, N sc, inc" rows (fan shape)
        fan_match = re.match(r"Inc,\s*(\d+)\s+sc,\s*inc", instruction)
        if fan_match:
            middle_sc = int(fan_match.group(1))
            expected = 2 + middle_sc + 2
            if expected != stated_count:
                issues.append(
                    f"  MISMATCH Row {row_num}: 'Inc, {middle_sc} sc, inc' "
                    f"= {expected} stitches but says ({stated_count})"
                )
            current_stitches = stated_count
            continue

        # "Dec, N sc, dec" rows (wing triangle)
        dec_match = re.match(r"Dec,\s*(\d+)\s+sc,\s*dec", instruction)
        if dec_match:
            middle_sc = int(dec_match.group(1))
            expected = 1 + middle_sc + 1
            if expected != stated_count:
                issues.append(
                    f"  MISMATCH Row {row_num}: 'Dec, {middle_sc} sc, dec' "
                    f"= {expected} stitches but says ({stated_count})"
                )
            current_stitches = stated_count
            continue

        # "N sc" even rows
        even_match = re.match(r"(\d+)\s+sc", instruction)
        if even_match:
            expected = int(even_match.group(1))
            if expected != stated_count:
                issues.append(
                    f"  MISMATCH Row {row_num}: '{expected} sc' but says ({stated_count})"
                )
            current_stitches = stated_count
            continue

        current_stitches = stated_count

    return rows_checked, issues


def check_has_body(pattern_data):
    """Check if the pattern has a body or main piece."""
    body_keywords = ["body", "main", "torso", "center"]
    for part in pattern_data:
        name_lower = part.get("name", "").lower()
        if any(kw in name_lower for kw in body_keywords):
            return True
    return False


def check_assembly_references(assembly_text, pattern_data):
    """Check that assembly instructions reference parts that exist,
    and that no raw Python lists leaked into the text."""
    issues = []
    for part in pattern_data:
        name = part.get("name", "")
        if name.lower() in ("body", "head & body", "main body"):
            continue
        if name not in assembly_text:
            issues.append(f"  Assembly is missing reference to '{name}'")

    # Check for raw Python list syntax leaking into assembly text
    if "['" in assembly_text or "[''" in assembly_text:
        issues.append("  Assembly contains raw Python list syntax (e.g. ['left', 'right'])")

    return issues


def run_test(creature_name, raw_parts):
    """Run one full test: convert parts, generate pattern, validate math."""
    print(f"\n{'='*60}")
    print(f"  TEST: {creature_name}")
    print(f"{'='*60}")

    # Step 1: Run through the FULL pipeline (validate + convert)
    # This is the same path the real app uses.
    analyzer = VisionAnalyzer()
    validated_parts = analyzer._validate_parts(list(raw_parts))
    pattern_data = analyzer._convert_to_pattern_format(validated_parts)

    print(f"\n  Parts from AI: {len(raw_parts)}")
    for p in raw_parts:
        count_str = f" (x{p['count']})" if p.get("count", 1) > 1 else ""
        print(f"    - {p['name']}{count_str}: {p['type']} / {p['size']}")

    print(f"  Parts after validation+conversion: {len(pattern_data)}")

    # Step 2: Verify the 3 fixes
    fix_results = []

    # Fix 1 check: Was a body auto-added if it was missing?
    original_has_body = check_has_body(raw_parts)
    final_has_body = check_has_body(pattern_data)
    if not original_has_body and final_has_body:
        print(f"\n  [Fix 1] BODY AUTO-ADDED: AI had no body, validator added one")
        fix_results.append(("Fix 1 - body auto-add", True))
    elif not original_has_body and not final_has_body:
        print(f"\n  [Fix 1] FAILED: Body was missing and NOT auto-added!")
        fix_results.append(("Fix 1 - body auto-add", False))
    else:
        print(f"\n  [Fix 1] N/A: AI already included a body part")

    # Fix 2 check: Were bad eyes corrected to flat_circle/small?
    bad_eyes_in = [
        p for p in raw_parts
        if "eye" in p.get("name", "").lower()
        and (p.get("type") == "cylinder"
             or (p.get("type") in ("sphere", "oval") and p.get("size") in ("medium", "large")))
    ]
    bad_eyes_out = [
        p for p in pattern_data
        if "eye" in p.get("name", "").lower()
        and p.get("type") != "flat_circle"
    ]
    if bad_eyes_in:
        if not bad_eyes_out:
            types_fixed = [f"{p['type']}/{p['size']}" for p in bad_eyes_in]
            print(f"  [Fix - eyes] CORRECTED: {', '.join(types_fixed)} → flat_circle/small")
            fix_results.append(("Eye size/type correction", True))
        else:
            print(f"  [Fix - eyes] FAILED: Bad eyes were NOT corrected!")
            fix_results.append(("Eye size/type correction", False))
    else:
        print(f"  [Fix - eyes] N/A: No oversized/wrong-type eyes in input")

    # Fix check: Were messy colors cleaned up?
    for i, (orig, conv) in enumerate(zip(validated_parts, pattern_data)):
        orig_color = orig.get("color", "")
        conv_color = conv.get("color", "")
        if orig_color != conv_color and len(orig_color) > len(conv_color):
            print(f"  [Fix - color] CLEANED: '{orig.get('name', '')}': '{orig_color}' → '{conv_color}'")

    # Fix check: Were list positions handled properly?
    list_positions = [p for p in raw_parts if isinstance(p.get("position"), list)]
    if list_positions:
        print(f"  [Fix - assembly] {len(list_positions)} part(s) had list positions — checking assembly output...")

    has_body = check_has_body(pattern_data)
    if not has_body:
        print(f"\n  !! STRUCTURAL ISSUE: No body/main piece found!")

    # Step 3: Generate the full pattern
    engine = BeginnerPatternGenerator()
    full_pattern = engine.add_header()
    full_pattern += f"## {creature_name.upper()}\n\n"
    full_pattern += engine.generate_materials(pattern_data)

    for part in pattern_data:
        full_pattern += engine.generate_part(part)

    assembly = engine.generate_assembly(pattern_data)
    full_pattern += assembly

    # Step 4: Validate stitch math for each part
    total_issues = []
    total_rounds_checked = 0

    for part in pattern_data:
        part_pattern = engine.generate_part(part)
        part_name = part["name"]
        part_type = part["type"]

        if part_type in ("flat_leaf", "fan", "wing", "heart_leaf"):
            checked, issues = validate_row_based_pattern(part_pattern, part_name)
        elif part_type in ("petals", "bird_feet"):
            print(f"\n  [{part_name}] ({part_type}) - Skipping: procedural instructions, no stitch counts to validate")
            continue
        else:
            checked, issues = validate_round_based_pattern(part_pattern, part_name)

        total_rounds_checked += checked

        if issues:
            print(f"\n  [{part_name}] ({part_type}) - {len(issues)} ISSUE(S):")
            for issue in issues:
                print(f"    {issue}")
            total_issues.extend(issues)
        else:
            print(f"\n  [{part_name}] ({part_type}) - {checked} rounds/rows checked, ALL CORRECT")

    # Step 5: Check assembly
    if assembly:
        asm_issues = check_assembly_references(assembly, pattern_data)
        if asm_issues:
            print(f"\n  ASSEMBLY ISSUES:")
            for issue in asm_issues:
                print(f"    {issue}")
            total_issues.extend(asm_issues)
        else:
            print(f"\n  Assembly: All parts referenced correctly")

    # Step 6: Save pattern for manual review
    safe_name = creature_name.replace(" ", "_")
    engine.save_to_pdf(f"generated_patterns/Test_{safe_name}_Pattern.pdf", full_pattern)

    # Summary
    print(f"\n  --- SUMMARY for {creature_name} ---")
    print(f"  Rounds/rows validated: {total_rounds_checked}")
    print(f"  Issues found: {len(total_issues)}")
    if not total_issues:
        print(f"  RESULT: PASS")
    else:
        print(f"  RESULT: FAIL")

    return len(total_issues) == 0


# ── MAIN ──

if __name__ == "__main__":
    print("\n" + "#"*60)
    print("  CROCHET PATTERN ENGINE - MATH VALIDATION TESTS")
    print("#"*60)

    results = {}
    for creature_name, raw_parts in TEST_CREATURES.items():
        passed = run_test(creature_name, raw_parts)
        results[creature_name] = passed

    print("\n\n" + "="*60)
    print("  FINAL RESULTS")
    print("="*60)
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status}")

    total_pass = sum(1 for v in results.values() if v)
    total_fail = sum(1 for v in results.values() if not v)
    print(f"\n  Total: {total_pass} passed, {total_fail} failed")
    print("="*60)
