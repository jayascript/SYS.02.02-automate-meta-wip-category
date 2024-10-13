#!/usr/bin/env sh

# Check if the prefixed README exists
if [ -f "SYS.02.02-README.org" ]; then
    # Copy the contents of SYS.02.00-README.org to README.org
    cp SYS.02.02-README.org README.org
    echo "README.org has been generated from SYS.02.02-README.org."
else
    echo "SYS.02.02-README.org not found."
fi
