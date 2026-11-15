#!/bin/bash


set -ex

ROOT=$PWD

# Output Nuitka version or fail if it is't there
export PYTHONPATH=$ROOT/Nuitka-develop:$PYTHONPATH
python -m nuitka --version

rm -f Nuitka-Tests
ln -s Nuitka-develop/tests Nuitka-Tests

for cast in casts/*.sh
do
    name=$(basename ${cast%.sh})
    result_name=$ROOT/site/casts/$name.cast
    echo "Making $result_name from '$cast' :"

    # A folder named like the cast holds the files it works with, the
    # recording runs in a copy of it, so build results are not kept.
    workdir=$ROOT
    if [ -d casts/$name ]
    then
        workdir=$(mktemp -d)
        cp -r casts/$name/. $workdir
    fi

    # The idle time limit is stored in the cast, the "asciinema" directive
    # cannot pass hyphenated options like "idle-time-limit" to the player.
    (cd $workdir && asciinema-automation --timeout 3600 --asciinema-arguments "--overwrite --idle-time-limit 2 -c 'env -i PS=\"$ \" PATH=$PATH PYTHONPATH=$PYTHONPATH bash --noprofile --norc'" $ROOT/$cast $result_name)

    if [ "$workdir" != "$ROOT" ]
    then
        rm -rf $workdir
    fi
done
