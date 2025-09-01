import os
import random
import string
from flask import Flask, request, redirect, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# Create a Flask application instance
app = Flask(__name__)

# Database configuration: prefer DATABASE_URL (Postgres) otherwise use local sqlite
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    # local fallback for development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)


class URLMapping(db.Model):
    __tablename__ = 'url_mappings'
    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    long_url = db.Column(db.Text, nullable=False)

    def as_dict(self):
        return {'short_code': self.short_code, 'long_url': self.long_url}


def generate_short_code(length=6):
    """Generate a unique random short code."""
    characters = string.ascii_letters + string.digits
    while True:
        short_code = ''.join(random.choice(characters) for _ in range(length))
        if not URLMapping.query.filter_by(short_code=short_code).first():
            return short_code


# Create tables at startup (compatible with Flask 3 lifecycle)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """Serve the index.html file for the homepage."""
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    """API endpoint to shorten a URL."""
    data = request.get_json() or {}
    long_url = data.get('url')

    if not long_url:
        return jsonify({'error': 'URL is required'}), 400

    # Generate a new short code
    short_code = generate_short_code()

    # Store the mapping in the database
    mapping = URLMapping(short_code=short_code, long_url=long_url)
    db.session.add(mapping)
    db.session.commit()

    # Construct the full shortened URL
    short_url = f"{request.host_url.rstrip('/')}/{short_code}"

    return jsonify({'short_url': short_url, 'code': short_code})


@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to the original URL based on the short code."""
    mapping = URLMapping.query.filter_by(short_code=short_code).first()

    if mapping:
        return redirect(mapping.long_url)
    else:
        # If the short code is not found, return a 404 error
        return "URL not found", 404


if __name__ == '__main__':
    # Running the Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', port=port, debug=debug)
