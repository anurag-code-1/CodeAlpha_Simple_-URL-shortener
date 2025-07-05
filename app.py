from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import string
import random
import os
from urllib.parse import urlparse

# Flask app setup
app = Flask(__name__)
# Use the instance folder for the database for better portability
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'urls.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # Add secret key for flash messages

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Initialize DB
db = SQLAlchemy(app)

# Database model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)

# Generate a unique short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if not URL.query.filter_by(short_code=code).first():
            return code

# Home page: form and result
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        custom_code = request.form.get('custom_code')

        # Validate URL
        if not original_url:
            return render_template('index.html', error="Please enter a URL")
        
        # Add http:// if not present
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url

        if not is_valid_url(original_url):
            return render_template('index.html', error="Please enter a valid URL")

        try:
            if custom_code:
                if len(custom_code) > 10:
                    return render_template('index.html', error="Custom code must be 10 characters or less")
                if URL.query.filter_by(short_code=custom_code).first():
                    return render_template('index.html', error="Custom short code already in use.")
                short_code = custom_code
            else:
                short_code = generate_short_code()

            # Save to database
            new_url = URL(original_url=original_url, short_code=short_code)
            db.session.add(new_url)
            db.session.commit()

            short_url = request.host_url + short_code
            # The 'click_count' variable is not used in the template, so it can be removed.
            return render_template('index.html', short_url=short_url)
        except Exception as e:
            db.session.rollback()
            import traceback
            traceback.print_exc()  # This will print the full error in your terminal
            return render_template('index.html', error=f"An error occurred: {e}")

    return render_template('index.html')

@app.route('/<short_code>')
def redirect_to_url(short_code):
    try:
        url = URL.query.filter_by(short_code=short_code).first_or_404()
        url.clicks += 1
        db.session.commit()
        return redirect(url.original_url)
    except Exception as e:
        db.session.rollback()
        print("ERROR:", str(e))
        return render_template('index.html', error="URL not found")


# Create database if not exists
if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database successfully initialized")
        except Exception as e:
            print("Database Error:", str(e))
    app.run(host='0.0.0.0', debug=True)
