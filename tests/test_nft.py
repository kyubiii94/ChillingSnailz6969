import pytest
from django.urls import reverse

from apps.nft.models import Faction, MintTransaction, Snailz


@pytest.mark.django_db
class TestFactionModel:
    def test_str(self, faction):
        assert str(faction) == "Aqua"


@pytest.mark.django_db
class TestSnailzModel:
    def test_str_format(self, snailz):
        assert str(snailz) == "SNAILZ #0001"

    def test_rarity_choices(self, faction):
        s = Snailz.objects.create(
            token_id=99, faction=faction, rarity="legendary",
            rarity_score=99.5, is_major=True,
        )
        assert s.get_rarity_display() == "Legendary"
        assert s.is_major is True


@pytest.mark.django_db
class TestMintTransaction:
    def test_create_transaction(self, user, snailz):
        tx = MintTransaction.objects.create(
            user=user, snailz=snailz,
            tx_hash="0x" + "a" * 64,
            amount_eth="0.05000000",
            status="confirmed",
        )
        assert tx.status == "confirmed"
        assert "0xaaa" in str(tx)


@pytest.mark.django_db
class TestCollectionView:
    def test_collection_page_loads(self, anon_client):
        resp = anon_client.get(reverse("nft:collection"))
        assert resp.status_code == 200

    def test_collection_filter(self, anon_client, snailz):
        resp = anon_client.get(reverse("nft:collection") + "?rarity=common")
        assert resp.status_code == 200

    def test_collection_filter_empty(self, anon_client, snailz):
        resp = anon_client.get(reverse("nft:collection") + "?rarity=legendary")
        assert resp.status_code == 200
        assert b"AUCUN SNAILZ" in resp.content


@pytest.mark.django_db
class TestSnailzAPI:
    def test_list_snailz(self, anon_client, snailz):
        resp = anon_client.get("/api/v1/snailz/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1

    def test_retrieve_snailz(self, anon_client, snailz):
        resp = anon_client.get(f"/api/v1/snailz/{snailz.id}/")
        assert resp.status_code == 200
        assert resp.json()["token_id"] == 1


@pytest.mark.django_db
class TestMintAPI:
    def test_mint_requires_auth(self, anon_client):
        resp = anon_client.get("/api/v1/mint/")
        assert resp.status_code == 403

    def test_mint_list_authenticated(self, auth_client):
        resp = auth_client.get("/api/v1/mint/")
        assert resp.status_code == 200
