#!/usr/bin/env sh

BROWSER=none yarn start &
until $(curl --output /dev/null --silent --head --fail http://localhost:3000); do
    printf '.'
    sleep 5
done

electron .

