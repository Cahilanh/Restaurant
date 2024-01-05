from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
)
import certifi
from pymongo import MongoClient

app = Flask(__name__)

password = 'sparta'
cxn_str = f'mongodb+srv://test:{password}@cluster1.z20fjyy.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(cxn_str)
db = client.db_SMK_UKK2024


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/restaurants', methods=["GET"])
def get_restaurants():
    # This api endpoint should fetch a list of restaurants
    restaurants = list(db.restaurants.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'restaurants': restaurants})

@app.route('/restaurant/create', methods=['POST'])
def create_restaurant():
    name = request.form.get('name')
    categories = request.form.get('categories')
    location = request.form.get('location')
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')
    doc = {
        'name': name,
        'categories': categories,
        'location': location,
        'center': [longitude, latitude]
    }
    db.restaurants.insert_one(doc)
    return jsonify({
        'result': 'success',
        'msg': 'successfully created a restaurant'
    })
    
@app.route('/restaurant/delete', methods=['POST'])
def delete_restaurant():
    name = request.form.get('name')
    db.restaurants.delete_one({'name': name})
    return jsonify({
        'result': 'success',
        'msg': 'successfully deleted a restaurant'
    })
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)