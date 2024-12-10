import types

import pytest

from downstream.dstream import steady_algo, stretched_algo, tilted_algo
from downstream.dsurf import Policy, Surface


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32])
def test_Surface(algo: types.ModuleType, S: int) -> None:
    policy = Policy(algo, S)
    surface = Surface(policy)
    assert surface.T == 0
    assert surface.policy.S == S
    assert surface.policy.algo is algo
    assert [*surface] == [None] * S
    assert [*surface.lookup()] == [None] * S

    for T in range(min(2**S, 100)):
        site = surface.ingest(T)
        if site is not None:
            assert surface[site] == T
        assert [*surface] == [*surface.lookup()]
        assert [*zip(surface.lookup(), surface)] == [*surface.enumerate()]
