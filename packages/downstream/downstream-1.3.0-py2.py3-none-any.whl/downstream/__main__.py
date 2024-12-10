import argparse
import itertools as it
from signal import SIG_BLOCK, SIGPIPE, signal
import sys

import opytional as opyt

from downstream.dstream import steady_algo  # noqa: F401
from downstream.dstream import stretched_algo  # noqa: F401
from downstream.dstream import tilted_algo  # noqa: F401

if __name__ == "__main__":
    signal(SIGPIPE, SIG_BLOCK)  # prevent broken pipe errors from head, tail

    parser = argparse.ArgumentParser(
        description="""
        Run site selection tests with the specified algorithm function on
        provided input data.

        The script reads pairs of integers S and T from standard input. For
        each pair, it checks if the algorithm has ingest capacity for S and T.
        If so, it runs the specified algorithm function and prints the result
        to standard output.

        Iterable results are space-separated, and output is limited to the
        specified maximum number of words. Null values in the results are
        represented as 'None'.

        If the algorithm does not have ingest capacity for the given S and T, a
        blank line is printed.
        """,
        epilog="""
        Example usage:
        $ python3 -m downstream.testing.generate_test_cases \
            | python3 -m downstream 'steady_algo.assign_storage_site'

        Additional available commands:
        $ python3 -m downstream.dataframe.explode_lookup_packed
        $ python3 -m downstream.dataframe.explode_lookup_unpacked
        $ python3 -m downstream.dataframe.unpack_data_packed
        $ python3 -m downstream.testing.debug_all
        $ python3 -m downstream.testing.debug_one
        $ python3 -m downstream.testing.generate_test_cases
        $ python3 -m downstream.testing.validate_all
        $ python3 -m downstream.testing.validate_one

        For information on a command, invoke it with the --help flag.
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "target",
        help=(
            "The algorithm function to test. "
            "Example: 'steady_algo.assign_storage_site'."
        ),
    )
    parser.add_argument(
        "--max-words",
        default=100,
        type=int,
        help="Maximum number of words to output from the result.",
    )
    args = parser.parse_args()

    algo = eval(args.target.split(".")[0])
    target = eval(args.target)
    for line in sys.stdin:
        S, T = map(int, line.rstrip().split())
        if algo.has_ingest_capacity(S, T):
            res = target(S, T)
            try:
                print(*it.islice(res, 100))
            except TypeError:
                print(opyt.apply_if(res, int))
        else:
            print()
