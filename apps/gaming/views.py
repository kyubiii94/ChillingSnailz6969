from django.shortcuts import render

GAMES = [
    {
        "name": "Snailz Invaders",
        "slug": "invaders",
        "url_name": "gaming:invaders",
        "tag": "ARCADE · SHOOT'EM UP",
        "desc": "Defend Lettuce Island contre les envahisseurs. Bats les highscores et gagne des $NAILZ.",
        "available": True,
    },
    {
        "name": "Shell Racer",
        "slug": "racer",
        "tag": "RACING · VITESSE",
        "desc": "Course de coquilles en pixel art sur les pistes de Lettuce Island. Bientot disponible.",
        "available": False,
    },
    {
        "name": "Lettuce Rumble",
        "slug": "rumble",
        "tag": "COMBAT · PVP",
        "desc": "Affronte d'autres Snailz dans l'arene 1v1. Bientot disponible.",
        "available": False,
    },
    {
        "name": "Clan Wars",
        "slug": "clanwars",
        "tag": "STRATEGIE · FACTIONS",
        "desc": "Guerres de factions en temps reel. Coordonne ton clan pour dominer l'ile. Bientot disponible.",
        "available": False,
    },
]


def index(request):
    return render(request, "gaming/index.html", {"games": GAMES})


def invaders(request):
    return render(request, "gaming/invaders.html")
