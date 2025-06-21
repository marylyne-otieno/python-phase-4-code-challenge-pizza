from flask import request
from flask_restful import Resource
from models import db, Restaurant, Pizza, RestaurantPizza

class Restaurants(Resource):
    def get(self):
        return [r.to_dict(only=("id", "name", "address")) for r in Restaurant.query.all()], 200

class RestaurantByID(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        return restaurant.to_dict(), 200

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204

class Pizzas(Resource):
    def get(self):
        return [p.to_dict(only=("id", "name", "ingredients")) for p in Pizza.query.all()], 200

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()

        try:
            price = int(data.get("price"))
            pizza_id = int(data.get("pizza_id"))
            restaurant_id = int(data.get("restaurant_id"))

            if price < 1 or price > 30:
                return {"errors": ["validation errors"]}, 400

            pizza = Pizza.query.get(pizza_id)
            restaurant = Restaurant.query.get(restaurant_id)

            if not pizza or not restaurant:
                return {"errors": ["validation errors"]}, 400

            rp = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
            db.session.add(rp)
            db.session.commit()

            return rp.to_dict(), 201

        except Exception as e:
            return {"errors": ["validation errors"]}, 400

