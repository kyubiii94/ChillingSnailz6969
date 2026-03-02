from django.shortcuts import render

from .models import Snailz


def collection(request):
    rarity_filter = request.GET.get("rarity", "all")
    snailz_list = Snailz.objects.select_related("faction").all()
    if rarity_filter != "all":
        snailz_list = snailz_list.filter(rarity=rarity_filter)
    return render(request, "nft/collection.html", {
        "snailz_list": snailz_list[:24],
        "current_filter": rarity_filter,
    })
