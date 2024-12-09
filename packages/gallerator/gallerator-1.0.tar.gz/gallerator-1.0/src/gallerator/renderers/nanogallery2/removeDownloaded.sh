#!/usr/bin/env bash
set -e

echo "Removing downloaded nanogallery2 distribution files"

dst=$(dirname $0)/static

rm -f $dst/jquery.nanogallery2.min.js
rm -f $dst/nanogallery2.min.css
rm -f $dst/font/ngy2_icon_font.woff
