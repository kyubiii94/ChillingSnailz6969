from django.contrib import admin

from .models import Faction, MintTransaction, Snailz


@admin.register(Faction)
class FactionAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "tag")


@admin.register(Snailz)
class SnailzAdmin(admin.ModelAdmin):
    list_display = ("token_id", "faction", "rarity", "is_major", "owner")
    list_filter = ("faction", "rarity", "is_major")
    search_fields = ("token_id",)


@admin.register(MintTransaction)
class MintTransactionAdmin(admin.ModelAdmin):
    list_display = ("snailz", "user", "status", "amount_eth", "created_at")
    list_filter = ("status",)
    readonly_fields = ("tx_hash", "created_at")
