from flask import render_template, current_app, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required

from app.weather import weather
from app.weather.forms import CityForm
from utils.weather.city_weather import main as get_weather
from utils.ip.get_current_city import main as get_current_city
from app.weather.models import City, Country, UserCity
from app.auth.models import User


@weather.route('/', methods=['GET', 'POST'])
def index():
    form = CityForm()
    city_weather = None
    city_name = get_current_city()
    country = None

    if form.validate_on_submit():
        api_key = current_app.config['WEATHER_API_KEY']
        city_name = form.city_name.data
        city_weather = get_weather(city_name, api_key)

        if 'message' in city_weather:
            flash(city_weather['message'])
            return redirect(url_for('.index'))

        country = Country.select().where(Country.code == city_weather['country']).first()
        if not country:
            flash('Country not found')
            return redirect('.index')

    return render_template(
        'weather/get_weather.html',
        title='Show weather info',
        form=form,
        city_weather=city_weather,
        city_name=city_name,
        country=country
    )


@weather.route('/city/add', methods=['POST'])
@login_required
def add_city():
    city_name = request.form.get('city').capitalize()

    city = City.select().where(City.name == city_name).first()
    if not city:
        country = request.form.get('country')
        city = City(name=city_name,
                    country=country)
        city.save()

    user_city = UserCity.select().where(UserCity.user == current_user, UserCity.city == city).first()
    if user_city:
        flash(f'City {city_name} already in list of user {current_user.username}')
        return redirect(url_for('.index'))

    user_city = UserCity(user=current_user, city=city)
    user_city.save()

    flash(f'City {city_name} added to user {current_user.username}')
    return redirect(url_for('.index'))


@weather.route('/city/show', methods=['GET'])
@login_required
def show_city():
    user_cities = (
        UserCity
        .select(City)
        .join(User)
        .switch(UserCity)
        .join(City)
        .where(UserCity.user == current_user)
        .order_by(City.name)
    )

    country_name = request.args.get('country')
    if country_name:
        user_cities = [user_city for user_city in user_cities if user_city.city.country.name == country_name]

    return render_template(
        'weather/show_user_cities.html',
        title=f'Cities of {current_user.username}',
        cities=user_cities)


@weather.route('/city/show/<string:city_name>', methods=['GET'])
@login_required
def show_city_detail(city_name: str):
    api_key = current_app.config['WEATHER_API_KEY']
    city_name = city_name.capitalize()

    user_city = (
        UserCity
        .select(City)
        .join(User)
        .where(User.id == current_user.id)
        .switch(UserCity)
        .join(City)
        .where(City.name == city_name).first()
    )

    if not user_city:
        abort(404)

    city_weather = get_weather(user_city.city.name, api_key)
    if 'message' in city_weather:
        flash(city_weather['message'])
        return redirect(url_for('.index'))

    return render_template(
        'weather/show_user_city_detail.html',
        title=f'Weather info about {user_city.city.name}',
        city_weather=city_weather,
        country=user_city.city.country
    )


@weather.route('/city/delete', methods=['POST'])
@login_required
def delete_city():
    selectors = list(map(int, request.form.getlist('selectors')))

    if not selectors:
        flash('Nothing to delete')
        return redirect(url_for('.show_city'))

    (UserCity
     .delete()
     .where(UserCity.user == current_user, UserCity.city.in_(selectors)).execute())

    cities_to_delete = City.select().where(City.id.in_(selectors)).order_by(City.name)
    message = 'Delete: '
    for city in cities_to_delete:
        message += f'{city.name}, '

    flash(message[:-2])
    return redirect(url_for('.show_city'))
