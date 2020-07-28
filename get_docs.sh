#!/usr/bin/env bash

mkdir -p ./docs

git clone https://github.com/cakephp/docs.git ./docs_src

cd ./docs_src

versions=( 2 3 4 )

for ver in "${versions[@]}"; do
    git checkout ${ver}.x
    make html-en
    mv ./build/html/en ../docs/${ver}
    rm -rf ./build
done

rm -rf ./docs_src