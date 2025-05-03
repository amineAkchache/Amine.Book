import os
from datetime import datetime
from app import db
from markupsafe import Markup
from werkzeug.utils import secure_filename

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    avg_rating = db.Column(db.Float, nullable=True)
    cover_image = db.Column(db.Text, nullable=True)
    published_date = db.Column(db.String(20), nullable=True)
    categories = db.Column(db.Text, nullable=True)
    page_count = db.Column(db.Integer, nullable=True)
    google_books_id = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    pdf_file = db.Column(db.Text, nullable=False)  # Path to uploaded PDF
    pdf_filename = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    reading_progress = db.relationship('ReadingProgress', backref='book', lazy=True)
    reviews = db.relationship('Review', backref='book', lazy=True)
    
    def __repr__(self):
        return f"Book('{self.title}', '{self.authors}')"
        
    def get_avg_user_rating(self):
        """Calculate the average rating from user reviews"""
        reviews = Review.query.filter_by(book_id=self.id).all()
        if not reviews:
            return 0
        
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / len(reviews), 1)
    
    def get_formatted_description(self):
        """Safely render HTML content from book description"""
        if not self.description:
            return ""
        return Markup(self.description)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'description': self.description,
            'avg_rating': self.avg_rating,
            'cover_image': self.cover_image,
            'published_date': self.published_date,
            'categories': self.categories,
            'page_count': self.page_count,
            'pdf_file': self.pdf_file  # Include PDF file path in the dictionary
        }

    @staticmethod
    def save_pdf_file(form_file):
        if not form_file:
            return None
        # Ensure the upload folder exists
        upload_folder = os.path.join('static', 'uploads')
        full_upload_path = os.path.join(current_app.root_path, upload_folder)

        os.makedirs(full_upload_path, exist_ok=True)
    
        filename = secure_filename(form_file.filename)
        file_path = os.path.join(full_upload_path, filename)
        form_file.save(file_path)
    
    # Return relative path for database storage
        return os.path.join('uploads', filename)
