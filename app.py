"""
Flask Web App for Crochet Pattern Generator
Provides a simple web interface for image upload and pattern generation
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import json
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
    """Analyze image or text prompt and return pattern data"""
    try:
        pattern_data = []
        
        # Check if it's an image upload or text prompt
        if 'image' in request.files and request.files['image'].filename:
            # Image upload path
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Analyze with vision AI
                analyzer = VisionAnalyzer()
                pattern_data = analyzer.analyze_image(filepath)
        
        elif 'prompt' in request.form and request.form['prompt'].strip():
            # Text prompt path
            prompt = request.form['prompt'].strip()
            
            # Use Ollama to generate pattern from text description
            system_prompt = """You are a crochet pattern expert. Based on the user's description, identify the components needed.

Return ONLY a JSON array like this (no other text):
[
  {"type": "sphere", "name": "Body", "color": "Blue", "size": "large"},
  {"type": "cylinder", "name": "Leg", "color": "Blue", "size": "small"}
]

Available types: sphere (round/ball), cylinder (tube/column), cone (pointy/tapered), flat_leaf (flat/thin)
Sizes: small, medium, large"""
            
            response = ollama.chat(
                model='llava',
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': f"Create a crochet pattern for: {prompt}"}
                ]
            )
            
            response_text = response['message']['content']
            
            # Parse JSON from response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx != -1 and end_idx > 0:
                json_str = response_text[start_idx:end_idx]
                vision_data = json.loads(json_str)
                
                analyzer = VisionAnalyzer()
                pattern_data = analyzer._convert_to_pattern_format(vision_data)
        
        else:
            return jsonify({'error': 'Please provide either an image or a text description'}), 400
        
        if not pattern_data:
            return jsonify({'error': 'Could not analyze the input. Please try again.'}), 400
        
        return jsonify({'pattern_data': pattern_data})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate pattern preview and PDF from pattern data"""
    try:
        data = request.json
        pattern_data = data.get('pattern_data', [])
        pattern_name = data.get('name', 'Custom_Pattern')
        
        if not pattern_data:
            return jsonify({'error': 'No pattern data provided'}), 400
        
        # Generate pattern text
        engine = BeginnerPatternGenerator()
        full_pattern = engine.add_header()
        full_pattern += f"## {pattern_name.replace('_', ' ').upper()}\n\n"
        
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
