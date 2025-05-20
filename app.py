from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from resume_parser.parser import parse_resume
from job_scraper.scraper import search_jobs_serpapi
# from ai_engine.tailor import generate_resume_cover_letter
# from db.models import save_job, get_all_jobs

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['resume']
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        resume_text, keywords = parse_resume(filepath)
        print(keywords)
        jobs = search_jobs_serpapi(keywords)
        print(jobs)
        return render_template('dashboard.html', jobs=jobs, resume_text=resume_text)
    return redirect(url_for('home'))

# @app.route('/download/<filename>')
# def download_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# @app.route('/dashboard')
# def dashboard():
#     jobs = get_all_jobs()
#     return render_template('dashboard.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=False)
