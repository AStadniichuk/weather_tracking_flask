from faker import Faker
from faker.providers import BaseProvider
from password_generator import PasswordGenerator
from random import choice
from typing import NamedTuple

from app.auth.utils import get_gravatar


class ProfileDTO(NamedTuple):
    username: str
    email: str
    password: str
    info: str
    avatar: str
    role: str
    id: str


class RoleProvider(BaseProvider):
    roles = ('user', 'admin')

    def role(self) -> str:
        return choice(self.roles)


def generate_password(min_len: int = 10, max_len: int = 15):
    generator = PasswordGenerator()
    generator.minlen = min_len
    generator.maxlen = max_len
    return generator.generate()


def generate_profiles(qty: int) -> list[ProfileDTO]:
    profiles = []
    id_count = 0

    for _ in range(qty):
        profile = fake.profile()
        role = fake.role()
        username = profile['username']
        email = profile['mail']
        info = profile['job']
        password = generate_password()
        avatar = get_gravatar(email)
        id_count += 1
        id = str(id_count)
        profiles.append(
            ProfileDTO(username, email, password, info, avatar, role, id))
    return profiles


fake = Faker()
fake.add_provider(RoleProvider)
