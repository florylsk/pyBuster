import requests
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import timeit
import sys

if len(sys.argv) != 4:
    print("Execution example: pybuster.py {URL} {File path/name} {Num of Threads}")
    sys.exit()

start = timeit.default_timer()
URL = sys.argv[1]

directories = []
with open(sys.argv[2], 'r') as f:
    for line in f.readlines():
        line = line.rstrip("\n")
        directories.append(line)

print("Scanning host", URL + "...")

URIS = []
session = requests.Session()
for directory in directories:
    URI = URL + "/" + directory
    URIS.append(URI)

numThreads = int(sys.argv[3])
threads = min(numThreads, len(directories))
with FuturesSession(max_workers=numThreads) as session:
    futures = [session.get(URI) for URI in URIS]
    for future in as_completed(futures):
        if (future.result().status_code != 404):
            print("[+] " + future.result().url.replace(URL, "") + " - " + str(future.result().status_code))

stop = timeit.default_timer()
print('Total runtime: ', stop - start, 'seconds')
