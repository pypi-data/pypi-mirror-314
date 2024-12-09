#!/usr/bin/env bash

codedir=$(dirname $0)

markdownDoc=$1
shift
block=$1
shift

destTmpfile=$(mktemp /tmp/replace-markdown-block.XXXXXX)

replacementTmpfile=$(mktemp /tmp/replace-markdown-block.XXXXXX)
echo '```' > $replacementTmpfile
gallerator --help  >> $replacementTmpfile
echo '```' >> $replacementTmpfile


cat $markdownDoc | \
  python3 $codedir/replace-section.py $block \
  "$(cat $replacementTmpfile)" > $destTmpfile
mv $destTmpfile $markdownDoc
rm "$replacementTmpfile"
