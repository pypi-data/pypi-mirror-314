import types
import typing


class Policy:

    algo: types.ModuleType  # algorithm module
    S: int  # surface size

    def __init__(self: "Policy", algo: types.ModuleType, S: int) -> None:
        self.algo = algo
        self.S = S

    def assign_storage_site(self: "Policy", T: int) -> int:
        return self.algo.assign_storage_site(self.S, T)

    def has_ingest_capacity(self: "Policy", T: int) -> bool:
        return self.algo.has_ingest_capacity(self.S, T)

    def lookup_ingest_times(self: "Policy", T: int) -> typing.Iterable[int]:
        return self.algo.lookup_ingest_times(self.S, T)
