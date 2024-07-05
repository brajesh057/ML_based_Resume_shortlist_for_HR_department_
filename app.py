from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from models import db, Candidate, init_db
from authentication import authenticate_user
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.decomposition import TruncatedSVD
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hr.db'
app.config['SECRET_KEY'] = 'your_secret_key'
init_db(app)

# Load dataset
data_path = 'data/eng_data.csv'
data = pd.read_csv(data_path)

# Preprocess and Train SVM Model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['resume'])
y = data['category']

# Dimensionality Reduction with LSA
lsa = TruncatedSVD(n_components=100)
X_lsa = lsa.fit_transform(X)

# Train SVM
svm_model = SVC(kernel='linear', C=1, gamma=0.1)
svm_model.fit(X_lsa, y)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        candidates = Candidate.query.all()
        return render_template('dashboard.html', candidates=candidates)
    else:
        return redirect(url_for('index'))


@app.route('/classify', methods=['POST'])
def classify_resume():
    if 'username' in session:
        if request.method == 'POST':
            resume_text = request.form['resume']
            candidate_name = request.form['name']
            candidate_email = request.form['email']
            candidate_phone = request.form['phone']
            candidate_skills = request.form['skills']

            # Preprocess the resume
            X_new = vectorizer.transform([resume_text])
            X_new_lsa = lsa.transform(X_new)
            prediction = svm_model.predict(X_new_lsa)

            # Save candidate to the database
            new_candidate = Candidate(
                name=candidate_name,
                email=candidate_email,
                phone=candidate_phone,
                skills=candidate_skills,
                resume=resume_text,
                category=prediction[0]
            )
            db.session.add(new_candidate)
            db.session.commit()

            return jsonify({'category': prediction[0]})
    else:
        return "Unauthorized", 401


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    auth_message = authenticate_user(username, password)

    if "Authentication successful" in auth_message:
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return auth_message, 401


if __name__ == '__main__':
    app.run(debug=True)
