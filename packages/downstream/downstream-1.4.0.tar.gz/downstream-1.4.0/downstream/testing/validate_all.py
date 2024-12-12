import argparse
import subprocess
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Test a downstream implementation against reference implementation "
            "over a large battery of test cases."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "command",
        help="The command to test. Example: 'python3 ./my_program'",
    )
    parser.add_argument(
        "--reference",
        default="python3 -O -m downstream",
        help="Reference command to validate against.",
    )
    args = parser.parse_args()

    script = r"""
set -e

rm -rf /tmp/dstream
mkdir -p /tmp/dstream

for algo in "steady_algo" "stretched_algo" "tilted_algo"; do
    for func in \
        "assign_storage_site" \
        "has_ingest_capacity" \
        "lookup_ingest_times" \
    ; do
        target="${algo}.${func}"
        echo "target=${target}"
        (\
            python3 -m downstream.testing.validate_one "$2" "${target}" --reference "$1" >/dev/null \
            || touch "/tmp/dstream/${target}" \
        ) &
    done
done

wait

if ls /tmp/dstream/* 1> /dev/null 2>&1; then
    echo "Tests failed!"
    (cd /tmp/dstream && ls *)
    exit 1
else
    echo "All tests passed!"
    exit 0
fi

rm -f /tmp/dstream
"""

if __name__ == "__main__":
    result = subprocess.run(
        [
            "bash",
            "-c",
            script,
            sys.argv[0],
            args.reference,
            args.command,
        ],
    )
    sys.exit(result.returncode)
