
python3 -m pip install -U invoke
python3 -m invoke virtualenv

while true
do
    set -ex

    # Remove old output
    rm -rf output

    # python3 -m invoke run -t update-docs
    python3 -m invoke site
    # python3 -m invoke intl -l zh_CN
    # python3 -m invoke intl -l de_DE
    python3 -m invoke run -t post-process

    set +e
    python3 -m invoke run -t serve-site

    if [ $? -eq 27 ]
    then
        continue
    fi

    break
done
