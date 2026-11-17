---
date: 2016-01-08
categories:
  - Archive
---

# Migrating git repo to new server

Simple script to copy all branches and code from one repo to another.

<!-- more -->

Use at your own risk! =)

## migrate.sh

```bash
#!/bin/sh
set -e

if [[ $# != 2 ]] ; then
    echo "Usage: $0 <source-repo> <destination-repo>"
    exit 1
fi

tmpdir=`mktemp -d 2>/dev/null || mktemp -d -t 'tmpdir'`

git clone --mirror $1 $tmpdir
cd $tmpdir
git remote rm origin
git remote add stash $2
git push --all stash
git push --tags stash
rm -rf $tmpdir
```
