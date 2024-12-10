import argparse
import subprocess
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Debug a downstream implementation against selected reference "
            "test cases."
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
pv=$(which pv && echo "--size $((17*512))" || echo "cat")

EXITCODE=0
for algo in "steady_algo" "stretched_algo" "tilted_algo"; do
    for func in \
        "assign_storage_site" \
        "has_ingest_capacity" \
        "lookup_ingest_times" \
    ; do
        target="${algo}.${func}"
        echo "target=${target}"
        python3 -m downstream.testing.debug_one "$2" "${target}" --reference "$1" | ${pv} | grep -v "OK"
        status=${PIPESTATUS[0]}

        if [ ${status} != 0 ]; then
            ((EXITCODE+=status))
        else
            echo "ALL OK"
        fi

        echo
    done
done
exit $EXITCODE
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
