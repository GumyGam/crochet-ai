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

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('generated_patterns', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Analyze image and/or text. Returns:
      - creature_type: what the AI thinks this is
      - raw_parts: what the AI detected (for the review UI)
      - pattern_data: converted for the pattern engine
    """
    try:
        has_image = 'image' in request.files and request.files['image'].filename
        has_prompt = 'prompt' in request.form and request.form['prompt'].strip()

        if not has_image and not has_prompt:
            return jsonify({'error': 'Please provide either an image, text description, or both'}), 400

        filepath = None
        user_text = request.form.get('prompt', '').strip() if has_prompt else None

        if has_image:
            file = request.files['image']
            if not file or not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type. Use PNG, JPG, JPEG, or GIF.'}), 400
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

        analyzer = VisionAnalyzer()

        try:
            result = analyzer.analyze(image_path=filepath, user_text=user_text)
        except Exception as ollama_err:
            print("[ANALYZE] Ollama/analysis error:", str(ollama_err))
            traceback.print_exc()
            return jsonify({
                'error': 'Could not reach Ollama. Is it running? '
                         'Run "ollama serve" and ensure "llava" is installed (ollama pull llava).'
            }), 503

        if not result or not result.get('pattern_data'):
            return jsonify({
                'error': 'AI could not identify any parts. Try a clearer image or more detailed description.'
            }), 400

        return jsonify({
            'creature_type': result['creature_type'],
            'raw_parts': result['raw_parts'],
            'pattern_data': result['pattern_data'],
        })

    except Exception as e:
        print("[ANALYZE] Unexpected error:", str(e))
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate():
    """Generate pattern preview and PDF from pattern data or raw_parts"""
    try:
        data = request.json
        pattern_data = data.get('pattern_data', [])
        raw_parts = data.get('raw_parts', [])
        pattern_name = data.get('name', 'Custom_Pattern')

        # If raw_parts came from the review UI, convert them to engine format
        if raw_parts and not pattern_data:
            analyzer = VisionAnalyzer()
            pattern_data = analyzer._convert_to_pattern_format(raw_parts)

        if not pattern_data:
            return jsonify({'error': 'No pattern data provided. Run analysis first.'}), 400
        
        # Generate pattern text
        engine = BeginnerPatternGenerator()
        full_pattern = engine.add_header()
        full_pattern += f"## {pattern_name.replace('_', ' ').upper()}\n\n"
        full_pattern += engine.generate_materials(pattern_data)
        
        try:
            for part in pattern_data:
                full_pattern += engine.generate_part(part)
        except KeyError as ke:
            part_name = part.get('name', 'unknown')
            print("[GENERATE] Missing key:", ke, "for part:", part)
            traceback.print_exc()
            return jsonify({
                'error': f'Pattern data incomplete: missing "{ke}" for part "{part_name}". Try a simpler image or description.'
            }), 400
        
        # Add assembly instructions based on part positions
        full_pattern += engine.generate_assembly(pattern_data)

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
    print("\nCrochet pattern desk")
    print("Open http://localhost:5001")
    print("Ctrl+C to stop\n")
    app.run(debug=False, host='127.0.0.1', port=5001)
