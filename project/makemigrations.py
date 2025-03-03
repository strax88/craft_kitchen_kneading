import os.path
import sys
from datetime import datetime
from pathlib import Path

from alembic import command
from alembic.config import Config


def create_migration(message):
    alembic_cfg = Config(os.path.join(Path(__file__).parent.parent / "project", "alembic.ini"))

    # Создаем новую миграцию
    command.revision(alembic_cfg, message, autogenerate=True)


def create_revision(message):
    alembic_cfg = Config(os.path.join(Path(__file__).parent.parent / "project", "alembic.ini"))

    # Создаем новую миграцию
    command.revision(alembic_cfg, message, autogenerate=False)


if __name__ == "__main__":
    params = sys.argv[1:]
    name_index = None
    name = "new_migration"
    if "-n" in params:
        name_index = params.index("-n") + 1
    elif "--name" in params:
        name_index = params.index("--name") + 1
    if name_index is not None:
        name = params[name_index]
    timestamped_name = "_".join([datetime.now().isoformat(), name])
    if "-r" in params:
        create_revision(timestamped_name)
    else:
        create_migration(timestamped_name)
