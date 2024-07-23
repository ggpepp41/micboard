#!/bin/bash

# Website URL to check
URL="http://localhost:8058/#tvmode=elinfo00&bgmode=IMG" # Launches the website in big image mode

echo "Starting website check..."

# Loop until the website is online
while true; do
    echo "Checking $URL..."
    
    # Use GET method
    RESPONSE=$(curl -s --write-out "%{http_code}" --output /dev/null "$URL")
    echo "Response Code: $RESPONSE"

    if [ "$RESPONSE" -eq 200 ]; then
        echo "$URL is online."
        DISPLAY=:0 chromium-browser "$URL" --kiosk &
        break
    else
        echo "$URL is not reachable. Checking again in 10 seconds..."
        sleep 10
    fi
done
