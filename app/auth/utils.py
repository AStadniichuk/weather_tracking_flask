import hashlib
from flask_login import LoginManager

from app.auth.models import User


def create_login_manager():
    manager = LoginManager()
    manager.login_view = 'auth.login'
    return manager


login_manager = create_login_manager()


@login_manager.user_loader
def load_user(user_id):
    return User.select().where(User.id == user_id).first()


def is_admin(user_to_check):
    user = User.select().where(User.id == user_to_check.id).first()
    if user.role.name != 'admin':
        return False
    return True


def get_gravatar(email: str, size: int = 100):
    md5_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    gravatar_url = f'https://www.gravatar.com/avatar/{md5_hash}?d=identicon&s={size}'
    return gravatar_url


