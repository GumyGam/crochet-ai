"""
Full Pipeline: Image to Crochet Pattern PDF
Combines vision analysis with pattern generation
"""

import sys
import json
from pathlib import Path
from vision_analyzer import VisionAnalyzer
from pattern_engine import BeginnerPatternGenerator

def generate_pattern_from_image(image_path, output_name=None):
    """
    Complete pipeline: Image → Analysis → Pattern → PDF
    
    Args:
        image_path: Path to the crochet image
        output_name: Optional custom name for the PDF (without .pdf extension)
    
    Returns:
        Path to the generated PDF
    """
    
    print("=" * 60)
    print("🧶 CROCHET PATTERN GENERATOR")
    print("=" * 60)
    
    # Step 1: Analyze the image with vision AI
    print("\n📸 Step 1: Analyzing image with AI...")
    analyzer = VisionAnalyzer()
    vision_data = analyzer.analyze_image(image_path)
    
    print(f"\n✅ Identified {len(vision_data)} parts:")
    for part in vision_data:
        print(f"   - {part['name']} ({part['type']}) - {part['color']}")
    
    # Step 2: Generate the pattern
    print("\n✏️  Step 2: Generating crochet pattern...")
    engine = BeginnerPatternGenerator()
    
    # Create pattern name from image filename if not provided
    if output_name is None:
        output_name = Path(image_path).stem.replace(" ", "_")
    
    full_pattern = engine.add_header()
    full_pattern += f"## {output_name.replace('_', ' ').upper()}\n\n"
    
    # Generate each part
    for part in vision_data:
        if part["type"] == "sphere":
            full_pattern += engine.generate_sphere(
                part["name"], part["color"], 
                part["max_stitches"], part["height"]
            )
        elif part["type"] == "cylinder":
            full_pattern += engine.generate_cylinder(
                part["name"], part["color"],
                part["width"], part["height"]
            )
        elif part["type"] == "cone":
            full_pattern += engine.generate_cone(
                part["name"], part["color"],
                part["base"], part["height"]
            )
        elif part["type"] == "flat_leaf":
            full_pattern += engine.generate_flat_leaf(
                part["name"], part["color"],
                part["length"]
            )
        elif part["type"] == "heart_leaf":
            full_pattern += engine.generate_heart_leaf(
                part["name"], part["color"],
                part["size"]
            )
        elif part["type"] == "wing":
            full_pattern += engine.generate_wing(
                part["name"], part["color"],
                part["size"]
            )
        elif part["type"] == "petals":
            full_pattern += engine.generate_petals(
                part["name"], part["color"],
                part["num_petals"], part["attachment"]
            )
        elif part["type"] == "spikes":
            full_pattern += engine.generate_spikes(
                part["name"], part["color"],
                part["num_spikes"]
            )
    
    # Step 3: Save to PDF
    print("\n📄 Step 3: Generating PDF...")
    pdf_filename = f"{output_name}_Pattern.pdf"
    engine.save_to_pdf(pdf_filename, full_pattern)
    
    print("\n" + "=" * 60)
    print(f"✅ SUCCESS! Pattern saved as: {pdf_filename}")
    print("=" * 60)
    
    return pdf_filename


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python image_to_pattern.py <image_path> [output_name]")
        print("\nExample:")
        print("  python image_to_pattern.py my_crochet.jpg")
        print("  python image_to_pattern.py my_crochet.jpg CustomName")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(image_path).exists():
        print(f"❌ Error: Image not found: {image_path}")
        sys.exit(1)
    
    generate_pattern_from_image(image_path, output_name)
