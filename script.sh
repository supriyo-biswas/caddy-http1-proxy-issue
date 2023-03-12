#!/bin/bash

set -eu

expected_data='#done.test.1234567890'

for i in {1..1000}; do
    curl -sS "https://$1/api/run/test" \
        --http1.1 \
        --data-urlencode 'id=1234567890' > out.txt
    if ! grep -Fq "$expected_data" out.txt; then
        echo "Failed after $i requests"
        exit 1
    fi
done
