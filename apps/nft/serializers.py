from rest_framework import serializers

from .models import Faction, MintTransaction, Snailz


class FactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faction
        fields = ["id", "name", "color", "description", "tag"]


class SnailzSerializer(serializers.ModelSerializer):
    faction = FactionSerializer(read_only=True)

    class Meta:
        model = Snailz
        fields = [
            "id", "token_id", "faction", "rarity", "rarity_score",
            "is_major", "metadata", "image", "created_at",
        ]


class MintTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MintTransaction
        fields = ["id", "snailz", "tx_hash", "amount_eth", "status", "created_at"]
        read_only_fields = ["id", "created_at"]
