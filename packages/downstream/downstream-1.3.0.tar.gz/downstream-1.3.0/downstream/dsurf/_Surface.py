import typing

from ._Policy import Policy


class Surface:

    _storage: list  # storage sites
    T: int  # current logical time
    policy: Policy  # policy

    def __init__(self: "Surface", policy: Policy) -> None:
        self.T = 0
        self._storage = [None] * policy.S
        self.policy = policy

    def __iter__(self: "Surface") -> typing.Iterable[object]:
        return iter(self._storage)

    def __getitem__(self: "Surface", site: int) -> object:
        return self._storage[site]

    def enumerate(
        self: "Surface",
    ) -> typing.Iterable[typing.Tuple[int, object]]:
        """Iterate over ingest times and values of retained data items."""
        return zip(self.lookup(), self._storage)

    def ingest(self: "Surface", item: object) -> typing.Optional[int]:
        """Ingest data item.

        Returns the storage site of the data item, or None if the data item is
        not retained.
        """
        assert self.policy.has_ingest_capacity(self.T)
        site = self.policy.assign_storage_site(self.T)
        if site is not None:
            self._storage[site] = item
        self.T += 1
        return site

    def lookup(self: "Surface") -> typing.Iterable[int]:
        """Iterate over ingest times of retained data items."""
        return self.policy.lookup_ingest_times(self.T)
