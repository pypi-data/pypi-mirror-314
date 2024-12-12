import typing

from ..._auxlib._bit_floor import bit_floor
from ..._auxlib._ctz import ctz


def steady_assign_storage_site(S: int, T: int) -> typing.Optional[int]:
    """Site selection algorithm for steady curation.

    Parameters
    ----------
    S : int
        Buffer size. Must be a power of two.
    T : int
        Current logical time.

    Returns
    -------
    typing.Optional[int]
        Selected site, if any.
    """
    s = S.bit_length() - 1
    t = T.bit_length() - s  # Current epoch (or negative)
    h = ctz(T + 1)  # Current hanoi value
    if h < t:  # If not a top n(T) hanoi value...
        return None  # ...discard without storing

    i = T >> (h + 1)  # Hanoi value incidence (i.e., num seen)
    if i == 0:  # Special case the 0th bunch
        k_b = 0  # Bunch position
        o = 0  # Within-bunch offset
        w = s + 1  # Segment width
    else:
        j = bit_floor(i) - 1  # Num full-bunch segments
        B = j.bit_length()  # Num full bunches
        k_b = (1 << B) * (s - B + 1)  # Bunch position
        w = h - t + 1  # Segment width
        assert w > 0
        o = w * (i - j - 1)  # Within-bunch offset

    p = h % w  # Within-segment offset
    return k_b + o + p  # Calculate placement site


assign_storage_site = steady_assign_storage_site  # lazy loader workaround
