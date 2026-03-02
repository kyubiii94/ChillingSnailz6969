from django.conf import settings
from django.db import models


class Faction(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, help_text="Hex color code, e.g. #00d4ff")
    description = models.TextField(blank=True, default="")
    tag = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Snailz(models.Model):
    class Rarity(models.TextChoices):
        COMMON = "common", "Common"
        UNCOMMON = "uncommon", "Uncommon"
        RARE = "rare", "Rare"
        LEGENDARY = "legendary", "Legendary"

    token_id = models.IntegerField(unique=True, db_index=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="snailz",
    )
    faction = models.ForeignKey(Faction, on_delete=models.PROTECT, related_name="snailz")
    rarity = models.CharField(max_length=20, choices=Rarity.choices, default=Rarity.COMMON)
    rarity_score = models.FloatField(default=0.0)
    is_major = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    image = models.ImageField(upload_to="snailz/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "snailz"
        ordering = ["token_id"]

    def __str__(self):
        return f"SNAILZ #{self.token_id:04d}"


class MintTransaction(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mint_transactions")
    snailz = models.ForeignKey(Snailz, on_delete=models.CASCADE, related_name="mint_transactions")
    tx_hash = models.CharField(max_length=255)
    amount_eth = models.DecimalField(max_digits=18, decimal_places=8)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Mint {self.snailz} by {self.user} — {self.status}"
