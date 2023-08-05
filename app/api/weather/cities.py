from flask import jsonify, abort, request, url_for, g, current_app


from app.api import api
from app.weather.models import City, Country, UserCity
from app.api.errors import forbidden
from utils.weather.city_weather import main as check_city_name


@api.route('/cities/', methods=['GET'])
def get_cities():
    cities = City.select()
    response = [city.to_json() for city in cities]
    return jsonify(response), 200


@api.route('/cities/<int:city_id>', methods=['GET'])
def get_city(city_id):
    city = City.select().where(City.id == city_id).first()
    if not city:
        abort(404)
    return jsonify(city.to_json()), 200


@api.route('/cities/', methods=['POST'])
def add_city():
    if not g.current_user.is_admin():
        return forbidden('you don\'t have access to add new city')

    new_city = City.from_json(request.json)
    api_key = current_app.config['WEATHER_API_KEY']

    check_city = check_city_name(new_city.name, api_key)
    if 'message' in check_city:
        return jsonify(check_city), 404

    country = Country.select().where(Country.code == check_city['country']).first()
    new_city.country = country
    new_city.save()
    return jsonify({
        'city': new_city.to_json(),
        'location': url_for('api.get_city', city_id=new_city.id)
    })


@api.route('/cities/<int:city_id>', methods=['PUT'])
def edit_city(city_id):
    if not g.current_user.is_admin():
        return forbidden('you don\'t have access to add new city')

    city_to_edit = City.select().where(City.id == city_id).first()
    if not city_to_edit:
        abort(404)

    new_city = City.from_json(request.json)
    api_key = current_app.config['WEATHER_API_KEY']

    check_city = check_city_name(new_city.name, api_key)
    if 'message' in check_city:
        return jsonify(check_city), 404

    country = Country.select().where(Country.code == check_city['country']).first()

    city_to_edit.name = new_city.name
    city_to_edit.country = country
    city_to_edit.save()
    return jsonify(city_to_edit.to_json())


@api.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_city(city_id):
    if not g.current_user.is_admin():
        return forbidden('you don\'t have access to add new city')

    city = City.select().where(City.id == city_id).first()
    if not city:
        abort(404)

    City.delete().where(City.id == city_id).execute()
    return jsonify(''), 204


@api.route('/cities/', methods=['DELETE'])
def delete_cities():
    if not g.current_user.is_admin():
        return forbidden('you don\'t have access to add new city')
    UserCity.delete().execute()
    City.delete().execute()
    return jsonify(''), 204


