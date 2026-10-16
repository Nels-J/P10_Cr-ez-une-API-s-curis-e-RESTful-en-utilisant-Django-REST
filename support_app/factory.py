import factory
from django.contrib.auth.hashers import make_password

from . import models


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    birth_date = factory.Faker("date_of_birth", minimum_age=15)
    password = factory.LazyFunction(lambda: make_password("pass1234"))

    class Meta:
        model = models.User
