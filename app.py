from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_dance.contrib.google import make_google_blueprint, google
import os
import pdfplumber
import random
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Upload folder setup
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Google OAuth settings
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.config['GOOGLE_OAUTH_CLIENT_ID'] = 
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = 

google_bp = make_google_blueprint(
    client_id=app.config['GOOGLE_OAUTH_CLIENT_ID'],
    client_secret=app.config['GOOGLE_OAUTH_CLIENT_SECRET'],
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ],
    redirect_to="main"
)
app.register_blueprint(google_bp, url_prefix="/login")

# Skill Keywords
SKILL_KEYWORDS = [
    'python', 'java', 'html', 'css', 'flask', 'django', 'sql',
    'machine learning', 'data analysis', 'communication', 'teamwork',
    'web development', 'api design', 'data analyst', 'javascript',
    'react', 'angular', 'node.js', 'restful api', 'graphql',
    'cloud computing', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
    'devops', 'linux', 'git', 'c++', 'c#', 'php', 'ruby', 'go',
    'typescript', 'scala', 'swift', 'objective-c', 'r', 'matlab',
    'sas', 'spark', 'hadoop', 'tableau', 'power bi', 'excel',
    'project management', 'agile', 'scrum', 'kanban', 'jira',
    'business analysis', 'product management', 'seo', 'sem',
    'content writing', 'digital marketing', 'graphic design',
    'ui/ux design', 'adobe photoshop', 'adobe illustrator',
    'figma', 'sketch', 'blender', '3d modeling', 'animation',
    'video editing', 'after effects', 'premiere pro', 'salesforce',
    'sap', 'oracle', 'erp', 'crm', 'blockchain', 'cybersecurity',
    'penetration testing', 'network security', 'ethical hacking',
    'data engineering', 'etl', 'data warehousing', 'big data',
    'nlp', 'computer vision', 'deep learning', 'tensorflow',
    'pytorch', 'keras', 'open cv', 'natural language processing',
    'reinforcement learning', 'time series analysis', 'statistics',
    'probability', 'linear algebra', 'calculus', 'data visualization',
    'business intelligence', 'market research', 'financial analysis',
    'accounting', 'auditing', 'taxation', 'law', 'legal research',
    'human resources', 'recruitment', 'training and development',
    'customer service', 'technical support', 'supply chain management',
    'logistics', 'procurement', 'inventory management', 'quality assurance',
    'quality control', 'manufacturing', 'production planning',
    'mechanical engineering', 'electrical engineering', 'civil engineering',
    'chemical engineering', 'biotechnology', 'pharmaceuticals',
    'medical devices', 'healthcare', 'nursing', 'clinical research',
    'public health', 'education', 'teaching', 'e-learning',
    'language translation', 'interpretation', 'writing', 'editing',
    'proofreading', 'publishing', 'journalism', 'photography',
    'videography', 'music production', 'sound engineering',
    'event management', 'hospitality', 'travel and tourism',
    'real estate', 'construction', 'architecture', 'interior design',
    'fashion design', 'textile design', 'retail', 'e-commerce',
    'customer relationship management', 'business development',
    'sales', 'marketing', 'advertising', 'public relations',
    'social media management', 'influencer marketing', 'brand management',
    'strategic planning', 'consulting', 'entrepreneurship',
    'startups', 'venture capital', 'private equity', 'investment banking',
    'financial modeling', 'risk management', 'compliance', 'legal compliance',
    'data privacy', 'gdpr', 'information security', 'it governance',
    'business continuity planning', 'disaster recovery', 'change management',
    'organizational development', 'performance management',
    'talent management', 'employee engagement', 'compensation and benefits',
    'labor laws', 'industrial relations', 'negotiation', 'conflict resolution',
    'coaching', 'mentoring', 'leadership', 'emotional intelligence',
    'decision making', 'problem solving', 'critical thinking',
    'analytical skills', 'creativity', 'innovation', 'adaptability',
    'resilience', 'time management', 'stress management',
    'work-life balance', 'remote work', 'virtual collaboration',
    'cross-cultural communication', 'diversity and inclusion',
    'sustainability', 'corporate social responsibility',
    'environmental management', 'energy management', 'carbon footprint',
    'green building', 'renewable energy', 'climate change',
    'urban planning', 'geographic information systems', 'remote sensing',
    'aerospace engineering', 'automotive engineering', 'marine engineering',
    'nanotechnology', 'robotics', 'mechatronics', 'embedded systems',
    'internet of things', 'wearable technology', '3d printing',
    'augmented reality', 'virtual reality', 'mixed reality',
    'game development', 'game design', 'game programming',
    'esports', 'gamification', 'human-computer interaction',
    'user research', 'usability testing', 'accessibility',
    'information architecture', 'content strategy', 'copywriting',
    'storytelling', 'scriptwriting', 'screenwriting', 'film production',
    'cinematography', 'directing', 'acting', 'theatre', 'performing arts',
    'dance', 'music', 'singing', 'instrumental music', 'composition',
    'music theory', 'music education', 'sound design', 'audio engineering',
    'broadcasting', 'radio', 'television', 'podcasting', 'voice-over',
    'animation', '2d animation', '3d animation', 'stop motion',
    'motion graphics', 'visual effects', 'post-production',
    'color grading', 'video production', 'video editing',
    'film editing', 'photo editing', 'graphic design', 'illustration',
    'typography', 'branding', 'logo design', 'package design',
    'print design', 'web design', 'mobile app design', 'responsive design',
    'user interface design', 'user experience design', 'interaction design',
    'information design', 'data visualization', 'infographics',
    'presentation design', 'exhibition design', 'environmental design',
    'interior architecture', 'landscape architecture', 'urban design',
    'product design', 'industrial design', 'furniture design',
    'automotive design', 'transportation design', 'aerospace design',
    'fashion design', 'textile design', 'costume design', 'jewelry design',
    'accessory design', 'footwear design', 'set design', 'scenic design',
    'lighting design', 'sound design', 'stage management',
    'production management', 'arts administration', 'arts management',
    'cultural management', 'museum studies', 'art history',
    'conservation', 'restoration', 'curation', 'art criticism',
    'art education', 'art therapy', 'creative writing', 'poetry',
    'fiction writing', 'non-fiction writing', 'playwriting',
    'screenwriting', 'journalism', 'photojournalism', 'investigative journalism',
    'broadcast journalism', 'digital journalism', 'data journalism',
    'science communication', 'technical writing', 'grant writing',
    'proposal writing', 'business writing', 'academic writing',
    'editing', 'proofreading', 'publishing', 'book publishing',
    'magazine publishing', 'newspaper publishing', 'digital publishing',
    'self-publishing', 'e-books', 'audiobooks', 'literary agents',
    'book marketing', 'book design', 'bookbinding', 'typography',
    'calligraphy', 'printmaking', 'illustration', 'comic art',
    'graphic novels', 'cartooning', 'animation', 'storyboarding',
    'character design', 'concept art', 'environment design',
    'game art', '3d modeling', 'texturing', 'rigging', 'lighting',
    'rendering', 'compositing', 'visual effects', 'motion capture',
    'virtual production', 'film production', 'cinematography',
    'directing', 'producing', 'screenwriting', 'editing', 'sound design',
    'music composition', 'film scoring', 'post-production',
    'color grading', 'distribution', 'film marketing', 'film festivals',
    'film criticism', 'film studies', 'media studies', 'communication studies',
    'mass communication', 'public relations', 'advertising',
    'marketing', 'branding', 'digital marketing', 'social media marketing',
    'content marketing', 'email marketing', 'search engine optimization',
    'search engine marketing', 'pay-per-click advertising',
    'affiliate marketing', 'influencer marketing', 'video marketing',
    'mobile marketing', 'event marketing', 'experiential marketing',
    'guerrilla marketing', 'viral marketing', 'word-of-mouth marketing',
    'customer relationship management', 'customer experience',
    'customer service', 'sales', 'retail', 'e-commerce', 'merchandising',
    'inventory management', 'supply chain management', 'logistics',
    'procurement', 'warehouse management', 'transportation management',
    'fleet management', 'distribution', 'reverse logistics',
    'demand planning', 'forecasting', 'production planning',
    'manufacturing', 'lean manufacturing', 'six sigma',
    'total quality management', 'quality assurance', 'quality control',
    'process improvement', 'operations management', 'project management',
    'program management', 'portfolio management', 'risk management',
    'change management', 'organizational development', 'human resources',
    'talent acquisition', 'employee engagement', 'performance management',
    'compensation and benefits', 'training and development',
    'succession planning', 'labor relations', 'employment law',
    'diversity and inclusion', 'workplace safety', 'occupational health',
    'wellness programs', 'employee assistance programs',
    'corporate social responsibility', 'sustainability', 'environmental management',
    'energy management', 'carbon footprint', 'green building',
    'renewable energy', 'climate change', 'environmental policy',
    'environmental law', 'environmental science', 'ecology',
    'conservation', 'natural resource management', 'wildlife management',
    'forestry', 'agriculture', 'horticulture', 'landscape architecture',
    'urban planning', 'geographic information systems', 'remote sensing',
]






TAMIL_NADU_LOCATIONS = ["Chennai", "Coimbatore", "Madurai", "Trichy", "Salem"]

# Companies and Links
company_names = [
    "Infosys", "TCS", "Wipro", "Cognizant", "Accenture", "HCL", "Tech Mahindra",
    "L&T", "Mindtree", "Capgemini", "Amazon", "Google", "Microsoft", "IBM", "Zoho",
    "Mu Sigma", "Oracle", "SAP", "DXC Technology", "Genpact", "Deloitte", "KPMG", "EY",
    "PwC", "Mphasis", "CureMetrix", "Exl Service", "Atos", "CGI", "UBS", "Virtusa",
    "Siemens", "Syntel", "Tata Elxsi", "Persistent Systems", "Hexaware", "Bain & Co",
    "American Express", "Dell Technologies", "Verizon", "Sprint", "Visa", "Citi",
    "BlackRock", "Adobe", "Intuit", "LinkedIn", "Hewlett-Packard", "SAP Labs", "Flipkart",
    "Byju's", "Swiggy", "Zomato", "Ola", "Airtel", "Paytm", "PhonePe", "InMobi",
    "Freshworks", "Razorpay", "UrbanClap", "Bigbasket", "Myntra", "Snapdeal", "RedBus",
    "Indigo", "MakeMyTrip", "MGM Healthcare", "Sundaram Finance", "Ashok Leyland",
    "Tamilnad Mercantile Bank", "TVS Motors", "Bharat Heavy Electricals Limited",
    "Madurai Meenakshi Medical College", "Kovai Medical Center", "Mannai Group",
    "Zoho Corp", "Sutherland", "Temenos", "Ramco Systems", "BankBazaar", "Chargebee",
    "FreshToHome", "CaratLane", "Zifo RnD Solutions", "LatentView Analytics",
    "ThoughtWorks", "GlobalLogic", "CloudCherry", "Lemoxo", "WayCool", "GoFrugal",
    "Testleaf", "Plintron", "Soliton", "Uniphore", "iNautix", "Vuram", "Kimberly-Clark"
]

company_links = {}
for name in company_names:
    link = name.lower().replace(' ', '').replace('&', 'and').replace("'", "").replace('.', '')
    company_links[name] = f"https://www.{link}.com"

# Generate random job data
def generate_jobs():
    jobs = []
    for i in range(100):
        location = random.choice(TAMIL_NADU_LOCATIONS)
        job = {
            'role': random.choice(['Python Developer', 'Frontend Developer', 'Data Analyst', 'ML Engineer']),
            'company': company_names[i % len(company_names)],
            'skills': random.sample(SKILL_KEYWORDS, k=3),
            'description': f"{company_names[i % len(company_names)]} is hiring in {location}.",
            'type': random.choice(['Full-time', 'Part-time', 'Internship']),
            'location': location + ", Tamil Nadu",
            'experience_level': random.choice(['Junior', 'Mid', 'Senior']),
            'salary': random.randint(500000, 2000000),
            'date_posted': datetime.now() - timedelta(days=random.randint(0, 30))
        }
        jobs.append(job)
    return jobs

JOB_DATABASE = generate_jobs()

# ------------------ ROUTES -------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/main')
def main():
    if not google.authorized:
        return redirect(url_for('google.login'))

    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return f"Failed to fetch user info: {resp.text}"

    user_info = resp.json()
    email = user_info.get('email', '')

    if not email.endswith('@gmail.com'):
        return "Sorry, only Gmail accounts are allowed."

    session['user'] = email
    return render_template('main.html', user=email)

@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    if 'user' not in session:
        return redirect(url_for('home'))

    skills_found = []
    if request.method == 'POST':
        file = request.files['resume']
        if file and file.filename.endswith('.pdf'):
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)

            with pdfplumber.open(path) as pdf:
                text = ''.join([page.extract_text() or '' for page in pdf.pages]).lower()
                skills_found = [skill for skill in SKILL_KEYWORDS if skill in text]

            session['skills'] = skills_found
            return redirect(url_for('show_recommendations'))

    return render_template('upload_resume.html', user=session['user'], skills=skills_found)

@app.route('/recommendations', methods=['GET', 'POST'])
def show_recommendations():
    if 'skills' not in session:
        return redirect(url_for('upload_resume'))

    user = session.get('user')
    user_skills = session['skills']

    job_type = request.args.get('job_type', '')
    location = request.args.get('location', '')
    experience = request.args.get('experience', '')
    sort_by = request.args.get('sort_by', 'date_posted')

    matched_jobs = [job for job in JOB_DATABASE if any(skill in job['skills'] for skill in user_skills)]

    if job_type:
        matched_jobs = [job for job in matched_jobs if job['type'] == job_type]
    if location:
        matched_jobs = [job for job in matched_jobs if location.lower() in job['location'].lower()]
    if experience:
        matched_jobs = [job for job in matched_jobs if job['experience_level'] == experience]

    if sort_by == 'salary':
        matched_jobs.sort(key=lambda x: x['salary'], reverse=True)
    else:
        matched_jobs.sort(key=lambda x: x['date_posted'], reverse=True)

    for job in matched_jobs:
        job['salary_inr'] = f"₹{job['salary']:,}"

    return render_template('recommendations.html', user=user, jobs=matched_jobs, company_links=company_links)

@app.route('/resume_builder', methods=['GET', 'POST'])
def resume_builder():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        skills = request.form.get('skills')
        experience = request.form.get('experience')
        education = request.form.get('education')

        safe_name = name.replace(" ", "_")
        pdf_filename = f"{safe_name}_resume.pdf"
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)

        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica", 12)

        c.drawString(100, 750, f"Name: {name}")
        c.drawString(100, 730, f"Email: {email}")
        c.drawString(100, 710, f"Phone: {phone}")
        c.drawString(100, 690, f"Skills: {skills}")
        c.drawString(100, 670, f"Experience: {experience}")
        c.drawString(100, 650, f"Education: {education}")

        c.save()

        return redirect(url_for('download_resume', filename=pdf_filename))

    return render_template('resume_builder.html')

@app.route('/download_resume/<filename>')
def download_resume(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ----------------- MAIN -------------------
if __name__ == '__main__':
    app.run(debug=True)
