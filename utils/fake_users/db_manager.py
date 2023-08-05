import json

from definitions import PATH_TO_CREDENTIALS
from app.auth.models import User, Role, Profile
from app.weather.models import UserCity
from utils.fake_users.generator import ProfileDTO, generate_profiles


def clear_db():
    UserCity.delete().execute()
    User.delete().execute()
    Role.delete().execute()
    Profile.delete().execute()


def write_to_db(profiles: list[ProfileDTO]):
    role_user = Role(name='user')
    role_user.save()
    role_admin = Role(name='admin')
    role_admin.save()

    for profile in profiles:
        role = Role.get(Role.name == profile.role)
        profile_entity = Profile(avatar=profile.avatar,
                                 info=profile.info)
        profile_entity.save()
        user = User(username=profile.username,
                    email=profile.email,
                    password=profile.password,
                    role=role,
                    profile=profile_entity)
        user.save()


def prepare_user_credentials(users: list[ProfileDTO]):
    users_prepared_to_json = []
    for user in users:
        temp = {
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'role': user.role,
            'id': user.id
        }
        users_prepared_to_json.append(temp)
    return users_prepared_to_json


def write_user_credentials_to_json(users: list[dict[str, str]], json_file: str):
    with open(json_file, 'w') as file:
        json.dump(users, file, indent=4)


def main(qty: int):
    clear_db()
    profiles = generate_profiles(qty)
    write_to_db(profiles)
    users_prepared_to_json = prepare_user_credentials(profiles)
    write_user_credentials_to_json(users_prepared_to_json, PATH_TO_CREDENTIALS)
