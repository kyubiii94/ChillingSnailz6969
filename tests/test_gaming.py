import pytest
from django.urls import reverse

from apps.gaming.models import GameScore


@pytest.mark.django_db
class TestGamingViews:
    def test_invaders_page_loads(self, anon_client):
        resp = anon_client.get(reverse("gaming:invaders"))
        assert resp.status_code == 200
        assert b"Snailz Invaders" in resp.content


@pytest.mark.django_db
class TestGameScore:
    def test_create_score(self, user):
        score = GameScore.objects.create(
            user=user, game="invaders", score=4200, wave=5,
        )
        assert score.score == 4200
        assert "invaders" in str(score)

    def test_ordering_by_score_desc(self, user):
        GameScore.objects.create(user=user, game="invaders", score=100)
        GameScore.objects.create(user=user, game="invaders", score=500)
        GameScore.objects.create(user=user, game="invaders", score=300)
        scores = list(GameScore.objects.values_list("score", flat=True))
        assert scores == [500, 300, 100]
