#!/usr/bin/env bash
# really basic test driver
# copy the rubber source, and the test case data to a temporary
# directory, and run rubber on the file.

set -e                          # Stop at first failure.

VERBOSE=
while [ 1 -le $# ]; do
    case $1 in
		-d)
			set -x
			;;
        -v|-vv|-vvv)
            VERBOSE="$VERBOSE $1"
            ;;
        --debchroot)
            # Dependencies inside Debian.
            apt install -y \
                debhelper dh-python python3 texlive-latex-base asymptote \
                biber cwebx imagemagick \
                python3-prompt-toolkit python3-pygments r-cran-knitr \
                texlive-bibtex-extra texlive-binaries texlive-extra-utils \
                texlive-latex-extra texlive-latex-recommended \
                texlive-metapost texlive-pictures transfig
            # combine is not packaged for Debian.
            touch combine/disable
            ;;
        *)
            break
    esac
    shift
done

SOURCE_DIR="$(cd ..; pwd)"
printf -v DATE '%(%Y%m%d)T' -1
tmpdir=$(mktemp --tmpdir="/var/tmp" --directory "rubber-${DATE}-XXXXXX")
readonly PYTHON="python3 -W error -X dev"

echo "When a test fails, please remove the $tmpdir directory manually."

# Copy source directory, because python
# will attempt to write precompiled *.pyc sources.  For efficiency,
# we share these temporary files among tests.
cp -a "$SOURCE_DIR/rubber" $tmpdir/rubber
# Also rename rubber to rubber.py to avoid a clash with rubber/.
for exe in rubber rubber-info rubber-pipe; do
    cp "$SOURCE_DIR/bin/$exe" $tmpdir/$exe.py
done

for main; do
    case "$main" in
        run.sh | shared)
            continue;;
    esac

    [ -d $main ] || {
        echo "$main must be a directory"
        exit 1
    }

    [ -e $main/disable ] && {
        echo "Skipping test $main"
        continue
    }

    echo "Test: $main"

    mkdir $tmpdir/$main
    cp $main/* shared/* $tmpdir/$main
    cd $tmpdir/$main

    if test -r document; then
        read doc < document
    else
        doc=doc
    fi
    if test -r arguments; then
        read arguments < arguments
    fi

    if [ -e fragment ]; then
        # test brings their own code
        . ./fragment
    else
        # default test code:  try to build two times, clean up.
        echo "Running $PYTHON ../rubber.py $VERBOSE $arguments $doc ..."
        $PYTHON ../rubber.py $VERBOSE $arguments "$doc"
    fi

    ([ -r expected ] && cat expected ) | while read f; do
        [ -e "$f" ] || {
            echo "Expected file $f was not produced."
            exit 1
        }
    done

    if ! [ -e fragment ]; then
        # default test code:  try to build two times, clean up.
        $PYTHON ../rubber.py $VERBOSE $arguments         "$doc"
        $PYTHON ../rubber.py $VERBOSE $arguments --clean "$doc"
    fi

    unset doc arguments

    cd "${SOURCE_DIR}/tests"

    for before in $main/* shared/*; do
        after=$tmpdir/$main/${before##*/}
        diff $before $after || {
            echo "File $after missing or changed"
            exit 1
        }
        rm $after
    done

    rmdir $tmpdir/$main || {
        echo "Directory $tmpdir/$main is not left clean:"
        ls $tmpdir/$main
        exit 1
    }
done

rm -fr $tmpdir

echo OK
