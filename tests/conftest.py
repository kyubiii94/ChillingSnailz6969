import pytest
from django.test import Client

from apps.accounts.models import CustomUser
from apps.nft.models import Faction, Snailz


@pytest.fixture
def user_password():
    return "TestP@ssw0rd!2024"


@pytest.fixture
def user(db, user_password):
    return CustomUser.objects.create_user(
        email="test@chillingsnailz.com",
        username="testsnailz",
        password=user_password,
        gdpr_consent=True,
    )


@pytest.fixture
def admin_user(db, user_password):
    return CustomUser.objects.create_superuser(
        email="admin@chillingsnailz.com",
        username="admin",
        password=user_password,
    )


@pytest.fixture
def auth_client(user, user_password):
    client = Client()
    client.login(email=user.email, password=user_password)
    return client


@pytest.fixture
def anon_client():
    return Client()


@pytest.fixture
def faction(db):
    return Faction.objects.create(name="Aqua", color="#00d4ff", tag="STRATEGIE")


@pytest.fixture
def snailz(db, faction, user):
    return Snailz.objects.create(
        token_id=1, owner=user, faction=faction,
        rarity="common", rarity_score=42.0,
    )
