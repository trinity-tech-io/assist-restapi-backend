#!/usr/bin/env bash
echo "Install required packages"

case `uname` in
    Linux )
        sudo apt-get update -y 
        sudo apt-get install build-essential python3.7 python3-dev libleveldb-dev libpython3.7-dev -y
        ;;
    Darwin )
        brew update
        brew install leveldb python@3.7
        ;;
    *)
    exit 1
    ;;
esac

pip3 install virtualenv 

type virtualenv >/dev/null 2>&1 || { echo >&2 "No suitable python virtual env tool found, aborting"; exit 1; }

rm -rf .venv
virtualenv -p `which python3.7` .venv
source .venv/bin/activate
pip install --upgrade pip

case `uname` in
    Linux )
        pip install -r requirements.txt
        ;;
    Darwin )
        pip install --global-option=build_ext \
                    --global-option="-I/usr/local/include" --global-option="-L/usr/local/lib" \
                    --global-option="-I/usr/local/opt/zlib/include" --global-option="-L/usr/local/opt/zlib/lib" -r requirements.txt
        ;;
    *)
    exit 1
    ;;
esac

