
#!/bin/bash

VERSION_FILE="version.txt"

# Function to get current version
get_version() {
    if [ -f "$VERSION_FILE" ]; then
        cat "$VERSION_FILE"
    else
        echo "1.0.0"
    fi
}

# Function to bump version
bump_version() {
    local version=$(get_version)
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)
    local patch=$(echo $version | cut -d. -f3)
    
    case "$1" in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch|*)
            patch=$((patch + 1))
            ;;
    esac
    
    echo "${major}.${minor}.${patch}"
}

# Main script
case "$1" in
    get)
        get_version
        ;;
    bump)
        bump_version "$2"
        ;;
    *)
        echo "Usage: $0 {get|bump [major|minor|patch]}"
        exit 1
        ;;
esac
