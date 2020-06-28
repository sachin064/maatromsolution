from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)


class News_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))
    category = db.Column(db.String, db.ForeignKey(Category.name), nullable=False)
    published_at = db.Column(db.DateTime, nullable=False)
    url_image = db.Column(db.String(400))
