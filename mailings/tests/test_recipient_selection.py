import pytest
from recipients.tests.factories import RecipientFactory
from mailings.tests.factories import MailingFactory


@pytest.mark.django_db
def test_mailing_selects_only_active_recipients():
    mailing = MailingFactory()

    rcp1 = RecipientFactory(user=mailing.user, is_active=True)
    rcp2 = RecipientFactory(user=mailing.user, is_active=True)
    rcp3 = RecipientFactory(user=mailing.user, is_active=False)
    mailing.recipients.set([rcp1, rcp2, rcp3])

    recipients = mailing.get_recipients()

    assert recipients.count() == 2
    assert all(r.is_active for r in recipients)
