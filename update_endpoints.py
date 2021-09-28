#!/usr/bin/env python

import time
from find_endpoints import find_endpoints
from pathlib import Path

# filename for the sentinel file
SENTINEL_FILE_NAME = "endpoints"

# number of seconds to wait until
# we query again GOCDB
SENTINEL_FILE_CHANGE_SECONDS = 600

# sentinel file descriptor
sentinel_file = Path(SENTINEL_FILE_NAME)


def update_endpoints():
    """
    Update the file containing the list of GOCDB endpoints
    of type "org.openstack.horizon"
    """
    # Recreate sentinel file    
    sentinel_file.unlink(missing_ok=True)

    with open(sentinel_file, 'w') as f:
        endpoints = find_endpoints("org.openstack.horizon")
        for site, service_type, endpoint in endpoints:
            f.write(f'{site},{endpoint}\n')
        

def read_endpoints():
    """
    Read the list of GOCDB endpoints of type "org.openstack.horizon".
    Instead of querying GOCDB every time, we save the result of
    the query in a local file with SENTINEL_FILE_NAME. The file is
    updated with GOCDB data only after SENTINEL_FILE_CHANGE_SECONDS.
    """
    if not sentinel_file.exists():
        update_endpoints()
    else:
        # When was the sentinel file last modified?
        time_sentinel_modified = round(sentinel_file.stat().st_ctime)
        # What's the time now?
        time_now_in_seconds = round(time.time())
        # How long has it passed?
        difference = time_now_in_seconds - time_sentinel_modified
    
        if difference > SENTINEL_FILE_CHANGE_SECONDS:
            update_endpoints()

    endpoints = []
    # see ideas from
    # https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list
    with open(sentinel_file) as f:
        for line in f:
            endpoints.append(line.rstrip().split(','))

    return endpoints


def main():
    endpoints = read_endpoints()
    for site, endpoint in endpoints:
        print(site, endpoint)


if __name__ == "__main__":
    main()
