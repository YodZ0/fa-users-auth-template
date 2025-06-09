import logging
import importlib
import json
import os
from pathlib import Path

import sqlalchemy as sa

from src.core.database.db_provider import db_provider, init_db
from src.apps.auth.services.security import SecurityServiceImpl
from src.settings import settings

logger = logging.getLogger(__name__)


def import_from_string(import_str: str):
    package_name, model_name = import_str.rsplit(".", maxsplit=1)
    package = importlib.import_module(package_name)
    return getattr(package, model_name), model_name


async def load_data() -> None:
    """
    Load seed data from json files.
    """
    # Clear DB and create tables
    logger.debug("Init DB")
    await init_db()

    security = SecurityServiceImpl()
    seed_dir = Path(settings.base_dir) / "seed"
    logger.info("Start seed loading")
    for seed_file in os.listdir(seed_dir):
        seed_file_path = seed_dir / seed_file
        logger.debug("Load file %s", seed_file)

        with open(seed_file_path, encoding="utf-8") as f:
            items = json.load(f)
            logger.debug("%s items found", len(items))

        async with db_provider.session_factory() as s, s.begin():
            for item in items:
                model, model_name = import_from_string(item["model"])
                if model_name == "User":
                    item["fields"]["hashed_password"] = security.encode_password(
                        "qwerty"
                    )
                await s.execute(
                    sa.insert(model).values({"id": item["id"], **item["fields"]})
                )
                logger.debug("%s with id:%s created!", model_name, item["id"])
        logger.debug("%s loaded!", seed_file)

    logger.info("Seed loading finished!")
