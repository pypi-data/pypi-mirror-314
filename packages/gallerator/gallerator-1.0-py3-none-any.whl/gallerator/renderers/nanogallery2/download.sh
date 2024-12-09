#!/usr/bin/env bash
set -e

echo "Downloading nanogallery2 distribution files"

src='https://cdn.jsdelivr.net/npm/nanogallery2/dist'

dst=$(dirname $0)/static

mkdir -p $dst/font

wget -O $dst/jquery.nanogallery2.min.js $src/jquery.nanogallery2.min.js
wget -O $dst/nanogallery2.min.css $src/css/nanogallery2.min.css
wget -O $dst/font/ngy2_icon_font.woff $src/css/font/ngy2_icon_font.woff
