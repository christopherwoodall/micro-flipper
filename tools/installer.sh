#!/bin/bash
# Simple installer for the `micro-flipper` repository. The installer can be run
# by executing the following command:
#  $ curl -s https://raw.githubusercontent.com/christopherwoodall/micro-flipper/main/tools/installer.sh | bash


repo_url="https://github.com/christopherwoodall/micro-flipper.git"

# Create a temporary directory for cloning the repository
tmp_dir=$(mktemp -d)

git clone "$repo_url" "$tmp_dir"

cd "$tmp_dir"

git remote add upstream "$repo_url"

git fetch upstream

git reset upstream/main

git checkout -t upstream/main

rm -rf "$tmp_dir"

echo "Installation completed successfully."