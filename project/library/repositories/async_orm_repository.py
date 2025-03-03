from library.repositories.mixins import (
    AsyncCreateRepositoryMixin,
    AsyncReadRepositoryMixin,
    AsyncUpdateRepositoryMixin,
    AsyncDeleteRepositoryMixin,
)


class AsyncORMRepository(
    AsyncCreateRepositoryMixin, AsyncReadRepositoryMixin, AsyncUpdateRepositoryMixin, AsyncDeleteRepositoryMixin
):
    """"""