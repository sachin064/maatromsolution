import json
from dateutil.parser import parse
from flask import request, make_response
import requests
from .models import News_Data, Category
from sqlalchemy import and_
from app import app, db


@app.route('/api/fetch_news', methods=['GET'])
def query_test():
    try:
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
    except Exception as e:
        return make_response({'message': str(e)})


@app.route('/api/category_post', methods=['POST'])
def category_post():
    try:
        category = request.json
        category1 = ({
            'name': category.get('category')
        })
        result = Category(**category1)
        db.session.add(result)
        db.session.commit()
        return make_response({'message': "category added succesfully"})
    except Exception as e:
        return make_response({'message': str(e)})


@app.route('/api/category_list', methods=['GET'])
def category_list():
    try:
        category = Category.query.all()
        l = []
        for i in category:
            content = {
                'category': i.name
            }
            l.append(content)
        return make_response({'category': l})
    except Exception as e:
        return make_response({'message': str(e)})


@app.route('/api/list-news', methods=['POST'])
def new_list():
    try:
        categories = (request.args.get('category').split(','))
        date_from = request.args.get('from_date')
        to_date = request.args.get('to_date')
        data = []
        for catego in list(categories):
            new_data = db.session.query(News_Data).filter(
                and_(News_Data.published_at.between(date_from, to_date), News_Data.category.like(catego)))
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
        return make_response({'news_data': data})
    except Exception as e:
        return make_response({'message': str(e)})
