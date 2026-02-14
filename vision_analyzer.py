"""
Vision Analyzer - Uses Ollama's llava model to analyze crochet images
and extract pattern structure information
"""

import ollama
import json
import base64
from pathlib import Path

class VisionAnalyzer:
    def __init__(self, model="llava"):
        self.model = model
        
    def analyze_image(self, image_path):
        """
        Analyze an image and return structured pattern data.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            List of pattern parts in the format:
            [{"type": "sphere", "name": "Body", "color": "Blue", ...}, ...]
        """
        
        # Create the analysis prompt
        prompt = """You are a crochet pattern expert. Analyze this image of a crochet amigurumi and identify its components.

For EACH visible part, describe:
1. Shape type: sphere (round/ball), cylinder (tube/column), cone (pointy/tapered), or flat_leaf (flat/thin)
2. Part name (e.g., "Head", "Body", "Leg", "Ear", "Tail")
3. Color
4. Approximate size (small/medium/large)

Return ONLY a JSON array like this (no other text):
[
  {"type": "sphere", "name": "Head & Body", "color": "Green", "size": "large"},
  {"type": "cone", "name": "Tail", "color": "Green", "size": "medium"},
  {"type": "cylinder", "name": "Arm", "color": "Green", "size": "small"}
]

Be specific and list ALL visible parts."""

        print(f"Analyzing image: {image_path}")
        
        # Call Ollama with the image
        response = ollama.chat(
            model=self.model,
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [str(image_path)]
            }]
        )
        
        # Extract the response
        response_text = response['message']['content']
        print(f"\nLLava Response:\n{response_text}\n")
        
        # Try to parse JSON from the response
        try:
            # Find JSON array in the response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                print("⚠️  No JSON array found in response. Using fallback pattern.")
                return self._create_fallback_pattern(response_text)
            
            json_str = response_text[start_idx:end_idx]
            pattern_data = json.loads(json_str)
            
            # Convert to our internal format
            return self._convert_to_pattern_format(pattern_data)
            
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parsing error: {e}")
            print("Using fallback pattern based on description.")
            return self._create_fallback_pattern(response_text)
    
    def _convert_to_pattern_format(self, vision_data):
        """Convert llava output to pattern engine format"""
        pattern_parts = []
        
        for part in vision_data:
            # Map size to actual stitch counts
            size = part.get('size', 'medium').lower()
            
            if part['type'] == 'sphere':
                max_stitches = {'small': 18, 'medium': 24, 'large': 30}.get(size, 24)
                height = {'small': 3, 'medium': 5, 'large': 8}.get(size, 5)
                pattern_parts.append({
                    "type": "sphere",
                    "name": part['name'],
                    "color": part['color'],
                    "max_stitches": max_stitches,
                    "height": height
                })
            
            elif part['type'] == 'cylinder':
                width = {'small': 6, 'medium': 12, 'large': 18}.get(size, 12)
                height = {'small': 3, 'medium': 6, 'large': 10}.get(size, 6)
                pattern_parts.append({
                    "type": "cylinder",
                    "name": part['name'],
                    "color": part['color'],
                    "width": width,
                    "height": height
                })
            
            elif part['type'] == 'cone':
                base = {'small': 8, 'medium': 12, 'large': 16}.get(size, 12)
                height = {'small': 4, 'medium': 6, 'large': 8}.get(size, 6)
                pattern_parts.append({
                    "type": "cone",
                    "name": part['name'],
                    "color": part['color'],
                    "base": base,
                    "height": height
                })
            
            elif part['type'] == 'flat_leaf':
                length = {'small': 6, 'medium': 10, 'large': 15}.get(size, 10)
                pattern_parts.append({
                    "type": "flat_leaf",
                    "name": part['name'],
                    "color": part['color'],
                    "length": length
                })
        
        return pattern_parts
    
    def _create_fallback_pattern(self, description):
        """Create a simple pattern if JSON parsing fails"""
        print("Creating generic pattern with one body and two arms.")
        return [
            {"type": "sphere", "name": "Body", "color": "Unknown", "max_stitches": 24, "height": 6},
            {"type": "cylinder", "name": "Arm (Make 2)", "color": "Unknown", "width": 6, "height": 4}
        ]


# Test function
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python vision_analyzer.py <image_path>")
        sys.exit(1)
    
    analyzer = VisionAnalyzer()
    image_path = sys.argv[1]
    
    pattern_data = analyzer.analyze_image(image_path)
    
    print("\n=== Generated Pattern Data ===")
    print(json.dumps(pattern_data, indent=2))
