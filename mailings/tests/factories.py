import factory
from django.utils import timezone
from mailings.models import Mailing, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    user = factory.SubFactory(UserFactory)
    subject = factory.Faker("sentence")
    body = factory.Faker("paragraph")


class MailingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mailing

    user = factory.SubFactory(UserFactory)
    message = factory.SubFactory(MessageFactory)
    name = factory.Faker("sentence")
    date_first_dispatch = factory.LazyFunction(timezone.now)
    dispatch_end_date = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=1))
    status = "started"
