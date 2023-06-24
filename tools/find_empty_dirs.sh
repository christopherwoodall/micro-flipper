#!/bin/bash

empty_folders_file="empty_folders.txt"

# Check if a folder is empty
is_empty_folder() {
    folder_path=$1
    if [ -z "$(ls -A "$folder_path")" ]; then
        return 0
    else
        return 1
    fi
}

# Append folder path to the text file
append_to_file() {
    folder_path=$1
    echo "$folder_path" >> "$empty_folders_file"
}

# DSelete the empty directory
delete_folder() {
    folder_path=$1
    rm -rf "$folder_path"
    echo "Deleted folder: $folder_path"
}

# Traverse through the directory and find empty folders
find_empty_folders() {
    directory=$1
    for item in "$directory"/*; do
        if [ -d "$item" ]; then
            if is_empty_folder "$item"; then
                append_to_file "$item"
                delete_folder "$item"
            else
                find_empty_folders "$item"
            fi
        fi
    done
}

# Start from the current directory
current_directory=$(pwd)

# Run the script
find_empty_folders "$current_directory"
