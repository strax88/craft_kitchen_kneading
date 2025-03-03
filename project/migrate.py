import os.path
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config


def run_migrations():
    # Загружаем конфигурацию Alembic
    alembic_cfg = Config(os.path.join(Path(__file__).parent.parent / "project", "alembic.ini"))

    # Указываем, что хотим выполнить все миграции до последней
    command.upgrade(alembic_cfg, "head")

def downgrade_migration(revision):
    # Загружаем конфигурацию Alembic
    alembic_cfg = Config("alembic.ini")

    # Выполняем даунгрейд до указанной ревизии

    command.downgrade(alembic_cfg, revision)
def main(params):
    """"""
    revision = None
    if "-d" in params:
        revision = params[params.index("-d") + 1]
    elif "-drop" in params:
        revision = params[params.index("-drop") + 1]
    if revision is not None:
        downgrade_migration(revision)
    else:
        run_migrations()
if __name__ == "__main__":
    main(sys.argv[1:])
