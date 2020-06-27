import json
from dateutil.parser import parse
from flask import Flask, request, make_response, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from newsapi import NewsApiClient
import requests
from sqlalchemy import and_

app = Flask(__name__)
news_api = NewsApiClient(api_key="25e1b68d930346689d93ca5c9d6498e1")
app.config['SECRET_KEY'] = "JUSTFORDOING"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Royal@1a@localhost:5432/news"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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


@app.route('/api/fetch_news', methods=['GET'])
def query_test():
    category = request.args['q']
    date = request.args['date']
    data = requests.get(
        f"http://newsapi.org/v2/everything?q={category}&date={date}&apiKey=25e1b68d930346689d93ca5c9d6498e1")
    r = json.loads(data.content)
    if isinstance(r['articles'], list):
        data = {}
        for i in r['articles']:
            date = i.get('publishedAt')
            dt = parse(date)
            data.update({
                'author': i.get('author'),
                'title': i.get('title'),
                'description': i.get('description'),
                'published_at': dt.date(),
                'url_image': i.get('url'),
                'category': category
            })
            news = News_Data(**data)
            db.session.add(news)
            db.session.commit()
    return make_response({'message': " data saved succesfully"})


@app.route('/api/category_post', methods=['POST'])
def category_post():
    category = request.json
    category1 = ({
        'name': category.get('category')
    })
    result = Category(**category1)
    db.session.add(result)
    db.session.commit()
    return make_response({'message': "category added succesfully"})


@app.route('/api/list-news', methods=['POST'])
def new_list():
    categories = (request.args.get('category').split(','))
    date_from = request.args.get('from_date')
    to_date = request.args.get('to_date')
    data = []
    for catego in list(categories):
        new_data = db.session.query(News_Data).filter(and_(News_Data.published_at.between(date_from,to_date),News_Data.category.like(catego)))
        for i in new_data:
            l = ({
                'author': i.author,
                'title': i.title,
                'description': i.description,
                'published_at': i.published_at,
                'url_image': i.url_image,
                'category': i.category
            })
            data.append(l)
    return make_response({'message': data})


if __name__ == '__main__':
    app.run(debug=True)
