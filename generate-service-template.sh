#!/bin/bash

# Check if service name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <service-name>"
  exit 1
fi

SERVICE_NAME=$1

# Define the directory structure
DIRS=(
  "$SERVICE_NAME"
  "$SERVICE_NAME/src"
  "$SERVICE_NAME/src/${SERVICE_NAME//-/_}"
  "$SERVICE_NAME/src/${SERVICE_NAME//-/_}/lib"
  "$SERVICE_NAME/src/${SERVICE_NAME//-/_}/routes"
  "$SERVICE_NAME/tests"
)

# Define the files to be created
FILES=(
  "$SERVICE_NAME/Dockerfile"
  "$SERVICE_NAME/requirements.txt"
  "$SERVICE_NAME/src/${SERVICE_NAME//-/_}/main.py"
  "$SERVICE_NAME/src/${SERVICE_NAME//-/_}/const.py"
)

# Create the directories
for DIR in "${DIRS[@]}"; do
  mkdir -p "$DIR"
done

# Create the files
for FILE in "${FILES[@]}"; do
  touch "$FILE"
done

echo "Creating service template for $SERVICE_NAME..."
echo "Directory structure:"
for DIR in "${DIRS[@]}"; do
  echo "$DIR/"
done
echo "Files:"
for FILE in "${FILES[@]}"; do
  echo "$FILE"
done
echo "Service template generated successfully!"