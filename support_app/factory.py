import factory
from . import models


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    birth_date = factory.Faker("date_of_birth")
    username = factory.Faker("user_name")

    class Meta:
        model = models.User
