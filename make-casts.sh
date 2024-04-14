#!/bin/bash


set -ex

# Output Nuitka version or fail if it is't there
export PYTHONPATH=Nuitka-develop:$PYTHONPATH
python -m nuitka --version

rm -f Nuitka-Tests
ln -s Nuitka-develop/tests Nuitka-Tests

for cast in `ls -1 casts`
do
    result_name=doc/casts/${cast%.sh}.cast
    echo "Making $result_name from '$cast' :"

    asciinema-automation --timeout 3600 --asciinema-arguments "--overwrite -c 'env -i PS=\"$ \" PATH=$PATH PYTHONPATH=$PYTHONPATH bash --noprofile --norc" casts/$cast $result_name
done