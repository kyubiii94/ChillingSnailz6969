from django.conf import settings
from django.db import models


class GameScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_scores")
    game = models.CharField(max_length=50, db_index=True)
    score = models.IntegerField(default=0)
    wave = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-score"]

    def __str__(self):
        return f"{self.user} — {self.game}: {self.score}"
