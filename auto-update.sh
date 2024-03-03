set -ex

# Remove old output
rm -rf output

python3 -m pip install -U invoke
python3 -m invoke virtualenv
# python3 -m invoke run -t update-docs
python3 -m invoke doc
# python3 -m invoke intl -l zh_CN
# python3 -m invoke intl -l de_DE
python3 -m invoke run -t post-process
python3 -m invoke run -t serve-site
