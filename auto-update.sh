#!/bin/bash

while [[ $# -gt 0 ]]; do
    case "$1" in
        --development)
            DEVELOPMENT_MODE=1
            echo "Overriding to DEVELOPMENT mode (from flag)" | tee -a auto-update.log
            shift
            ;;
        --production)
            DEVELOPMENT_MODE=0
            echo "Overriding to PRODUCTION mode (from flag)" | tee -a auto-update.log
            shift
            ;;
        *)
            echo "Unknown argument: $1"
            shift
            ;;
    esac
done

if [ "${DEVELOPMENT_MODE:-0}" -eq 1 ]; then
    echo "Running in DEVELOPMENT mode" | tee -a auto-update.log
else
    echo "Running in PRODUCTION mode" | tee -a auto-update.log
fi
python3 -m invoke --help 2>/dev/null >/dev/null || python3 -m pip install invoke
python3 -m invoke virtualenv

while true
do
    set -ex

    # Remove old output
    rm -rf output

    # Trigger updates from Changelog documents and update downloads page
    # python3 -m invoke update-docs

    python3 -m invoke site
    # python3 -m invoke intl -l zh_CN
    # python3 -m invoke intl -l de_DE

    python3 -m invoke post-process

    set +e
    python3 -m invoke serve

    if [ $? -eq 27 ]
    then
        continue
    fi

    break
done
