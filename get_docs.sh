#!/usr/bin/env bash
mkdir docs
git clone https://github.com/cakephp/docs.git docs_src
cd docs_src
git checkout 2.x
make html-en
mv build/html/en ../docs/2
rm -rf build
git checkout 3.x
make html-en
mv build/html/en ../docs/3
rm -rf build
git checkout 4.x
make html-en
mv build/html/en ../docs/4
rm -rf build