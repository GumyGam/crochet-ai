"""
Flask Web App for Crochet Pattern Generator
Provides a simple web interface for image upload and pattern generation
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
import traceback
from pathlib import Path
from vision_analyzer import VisionAnalyzer
from pattern_engine import BeginnerPatternGenerator
import ollama

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('generated_patterns', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze image and/or text prompt and return pattern data"""
    try:
        pattern_data = []
        has_image = 'image' in request.files and request.files['image'].filename
        has_prompt = 'prompt' in request.form and request.form['prompt'].strip()
        
        if not has_image and not has_prompt:
            return jsonify({'error': 'Please provide either an image, text description, or both'}), 400
        
        # Build the AI prompt
        if has_image:
            # Image upload path
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Create enhanced prompt if text is also provided
                additional_context = ""
                if has_prompt:
                    additional_context = f"\n\nAdditional context from user: {request.form['prompt'].strip()}"
                
                analyzer = VisionAnalyzer()
                
                # Enhanced analysis with both image and text
                base_prompt = """You are a crochet pattern expert. Analyze this image of a crochet amigurumi and identify its components.

For EACH visible part, describe:
1. Shape type: sphere (round/ball), cylinder (tube/column), cone (pointy/tapered), or flat_leaf (flat/thin)
2. Part name (e.g., "Head", "Body", "Leg", "Ear", "Tail")
3. Color
4. Approximate size (small/medium/large)"""
                
                if has_prompt:
                    base_prompt += additional_context
                
                base_prompt += """

Return ONLY a JSON array like this (no other text):
[
  {"type": "sphere", "name": "Head & Body", "color": "Green", "size": "large"},
  {"type": "cone", "name": "Tail", "color": "Green", "size": "medium"}
]

Be specific and list ALL visible parts."""
                
                try:
                    response = ollama.chat(
                        model='llava',
                        messages=[{
                            'role': 'user',
                            'content': base_prompt,
                            'images': [filepath]
                        }]
                    )
                    response_text = response['message']['content']
                except Exception as ollama_err:
                    print("[ANALYZE] Ollama error:", str(ollama_err))
                    traceback.print_exc()
                    return jsonify({
                        'error': 'Could not reach Ollama. Is it running? Run "ollama serve" and ensure "llava" is installed (ollama pull llava).'
                    }), 503
                
                # Parse JSON
                start_idx = response_text.find('[')
                end_idx = response_text.rfind(']') + 1
                if start_idx == -1 or end_idx <= 0:
                    print("[ANALYZE] No JSON array in response. First 500 chars:", response_text[:500])
                    return jsonify({
                        'error': 'AI did not return valid part list. Try a clearer image or different description.'
                    }), 400
                try:
                    json_str = response_text[start_idx:end_idx]
                    vision_data = json.loads(json_str)
                    pattern_data = analyzer._convert_to_pattern_format(vision_data)
                except json.JSONDecodeError as je:
                    print("[ANALYZE] JSON parse error:", je)
                    traceback.print_exc()
                    return jsonify({
                        'error': f'Invalid response from AI (JSON error). Try again or simplify the image/description.'
                    }), 400
                except (KeyError, TypeError) as ke:
                    print("[ANALYZE] Convert error:", ke)
                    traceback.print_exc()
                    return jsonify({
                        'error': f'AI returned an unsupported shape or missing field: {ke}. Try a simpler image or description.'
                    }), 400
        
        elif has_prompt:
            # Text-only path
            prompt = request.form['prompt'].strip()
            
            system_prompt = """You are a crochet pattern expert. Based on the user's description, identify the components needed.

Return ONLY a JSON array like this (no other text):
[
  {"type": "sphere", "name": "Body", "color": "Blue", "size": "large"},
  {"type": "cylinder", "name": "Leg", "color": "Blue", "size": "small"}
]

Available types: sphere (round/ball), cylinder (tube/column), cone (pointy/tapered), flat_leaf (flat/thin)
Sizes: small, medium, large"""
            
            try:
                response = ollama.chat(
                    model='llava',
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': f"Create a crochet pattern for: {prompt}"}
                    ]
                )
                response_text = response['message']['content']
            except Exception as ollama_err:
                print("[ANALYZE] Ollama error (text-only):", str(ollama_err))
                traceback.print_exc()
                return jsonify({
                    'error': 'Could not reach Ollama. Is it running? Run "ollama serve" and ensure "llava" is installed (ollama pull llava).'
                }), 503
            
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx == -1 or end_idx <= 0:
                print("[ANALYZE] No JSON array (text-only). First 500 chars:", response_text[:500])
                return jsonify({
                    'error': 'AI did not return valid part list. Try a different or more specific description.'
                }), 400
            try:
                json_str = response_text[start_idx:end_idx]
                vision_data = json.loads(json_str)
                analyzer = VisionAnalyzer()
                pattern_data = analyzer._convert_to_pattern_format(vision_data)
            except json.JSONDecodeError as je:
                print("[ANALYZE] JSON parse error (text-only):", je)
                traceback.print_exc()
                return jsonify({'error': 'Invalid response from AI. Try a different description.'}), 400
            except (KeyError, TypeError) as ke:
                print("[ANALYZE] Convert error (text-only):", ke)
                traceback.print_exc()
                return jsonify({'error': f'AI returned unsupported shape or missing field: {ke}'}), 400
        
        if not pattern_data:
            return jsonify({'error': 'Could not analyze the input. Please try again.'}), 400
        
        return jsonify({'pattern_data': pattern_data})
    
    except Exception as e:
        print("[ANALYZE] Unexpected error:", str(e))
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate pattern preview and PDF from pattern data"""
    try:
        data = request.json
        pattern_data = data.get('pattern_data', [])
        pattern_name = data.get('name', 'Custom_Pattern')
        
        if not pattern_data:
            return jsonify({'error': 'No pattern data provided. Re-run analysis (upload image or enter description) and try again.'}), 400
        
        # Generate pattern text
        engine = BeginnerPatternGenerator()
        full_pattern = engine.add_header()
        full_pattern += f"## {pattern_name.replace('_', ' ').upper()}\n\n"
        
        try:
            for part in pattern_data:
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
                else:
                    return jsonify({
                        'error': f'Unknown part type "{part.get("type", "?")}" for "{part.get("name", "?")}". The AI may have returned a shape we don\'t support yet.'
                    }), 400
        except KeyError as ke:
            part_name = part.get('name', 'unknown')
            print("[GENERATE] Missing key:", ke, "for part:", part)
            traceback.print_exc()
            return jsonify({
                'error': f'Pattern data incomplete: missing "{ke}" for part "{part_name}". Try a simpler image or description.'
            }), 400
        
        # Convert markdown to HTML for preview
        html_pattern = markdown_to_html(full_pattern)
        
        # Generate PDF
        pdf_filename = f"{pattern_name}_Pattern.pdf"
        pdf_path = os.path.join('generated_patterns', pdf_filename)
        engine.save_to_pdf(pdf_path, full_pattern)
        
        return jsonify({
            'preview': html_pattern,
            'pdf_url': f'/download/{pdf_filename}'
        })
    
    except Exception as e:
        print("[GENERATE] Unexpected error:", str(e))
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download(filename):
    """Download generated PDF"""
    try:
        pdf_path = os.path.join('generated_patterns', filename)
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

def markdown_to_html(markdown_text):
    """Convert simple markdown to HTML for preview"""
    html = markdown_text
    
    # Headers
    html = html.replace('# ', '<h1>').replace('\n\n', '</h1>\n\n')
    lines = html.split('\n')
    result = []
    
    for line in lines:
        if line.startswith('## '):
            result.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            result.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('**') and '**' in line[2:]:
            # Bold text
            line = line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
            result.append(f'<p>{line}</p>')
        elif line.startswith('- '):
            result.append(f'<li>{line[2:]}</li>')
        elif line.startswith('*') and line.endswith('*'):
            result.append(f'<p><em>{line[1:-1]}</em></p>')
        elif line.strip() == '---':
            result.append('<hr>')
        elif line.strip():
            result.append(f'<p>{line}</p>')
        else:
            result.append('<br>')
    
    return '\n'.join(result)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🧶 CROCHET PATTERN GENERATOR - Web Interface")
    print("="*60)
    print("\n✅ Server starting...")
    print("📱 Open your browser to: http://localhost:5001")
    print("\nPress Ctrl+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5001)
