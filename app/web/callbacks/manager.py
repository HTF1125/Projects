import os
from dash import Dash, DiskcacheManager, CeleryManager, Input, Output, html, callback


from typing import Union


def get_background_manager() -> Union[CeleryManager, DiskcacheManager]:
    if "REDIS_URL" in os.environ:
        # Use Redis & Celery if REDIS_URL set as an env variable
        from celery import Celery

        celery_app = Celery(
            __name__,
            broker=os.environ["REDIS_URL"],
            backend=os.environ["REDIS_URL"],
        )
        return CeleryManager(celery_app)

    # Diskcache for non-production apps when developing locally
    import diskcache

    folderpath = "./cache/web/background"
    cache = diskcache.Cache(folderpath)
    return DiskcacheManager(cache)


manager = get_background_manager()
