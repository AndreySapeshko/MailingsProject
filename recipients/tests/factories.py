import factory
from recipients.models import Recipient
from mailings.tests.factories import UserFactory

class RecipientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipient

    user = factory.SubFactory(UserFactory)
    email = factory.Faker("email")
    name = factory.Faker("name")
    is_active = True
    comment = factory.Faker("sentence")
