import requests


def getMods(modsPerPage: int = 25, pageNum: int = 1):
    return requests.get(
        f"https://mods.factorio.com/api/mods?page_size={modsPerPage}&page={pageNum}"
    ).json()


def getModInfo(modName: str, full=False):
    return requests.get(
        f"https://mods.factorio.com/api/mods/{modName}{"/full" if full else ""}"
    ).json()
