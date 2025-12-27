#!/bin/bash

python3 -m invoke --help 2>/dev/null >/dev/null || python3 -m pip install invoke
python3 -m invoke virtualenv

while true
do
    set -ex

    # Remove old output
    rm -rf output

    # Trigger updates from Changelog documents and update downloads page
    # python3 -m invoke update-docs

    if ! python3 -m invoke site
    then
        echo ""
        echo "Error detected, sleeping somewhat to allow you to see it."

        sleep 5
        continue
    fi
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
