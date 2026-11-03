"""Shared download helper for all data sources (Ist-Daten, service points, weather).

Why a shared helper: every source is downloaded the same way, by script over
HTTP. Keeping it in one place means the rules apply everywhere:
- skip files that already exist (idempotent: re-running a script is cheap),
- for files that change (e.g. MeteoSwiss 'recent'), ask the server with the
  file's ETag whether there is a new version (HTTP If-None-Match -> 304 = unchanged),
- resume a broken download instead of starting again (large files, slow Wi-Fi),
- retry failed requests with "truncated exponential backoff with jitter",
  as recommended by MeteoSwiss/swisstopo (opendatadocs.meteoswiss.ch/general/download);
  this also covers the 502/503 errors seen on data.opentransportdata.swiss,
- send a short pause and a clear User-Agent (terms of use of the sources),
- show progress, so a long run in the terminal is not a black box.

Usage:
    from src.download import download_file
    path = download_file(url, RAW_DIR / "stops" / "service_points.csv")
    path = download_file(url, dest, refresh=True)   # re-check with ETag
"""
import random
import time
from pathlib import Path

import requests

# Identify ourselves to the data providers (polite and makes support easier)
HEADERS = {"User-Agent": "ZHAW-DA-HS26-group3 student project (github.com/rexheeri/da-projekt-hs26)"}

# Seconds to wait after each download, so we never hammer a server
PAUSE_S = 1.0

# Retry settings: wait at most CAP_S seconds between tries, give up after MAX_TRIES
MAX_TRIES = 6
BASE_S = 2.0
CAP_S = 60.0
RETRY_STATUS = {429, 500, 502, 503, 504}  # server busy or temporarily broken


def backoff_wait(attempt):
    """Seconds to wait before retry number `attempt` (0, 1, 2, ...).

    Truncated exponential backoff with jitter: the upper limit doubles with
    every try (2, 4, 8 ... s) but never exceeds CAP_S ("truncated"), and the
    actual wait is a random value below that limit ("jitter"), so many clients
    do not all retry at the same moment.
    """
    return random.uniform(0, min(CAP_S, BASE_S * 2 ** attempt))


def get_with_retry(url, headers=None, timeout=60, stream=False):
    """HTTP GET that retries on network errors and on 429/5xx answers.

    Returns the requests.Response (status 200, 206 or 304). Raises after MAX_TRIES.
    """
    headers = {**HEADERS, **(headers or {})}
    for attempt in range(MAX_TRIES):
        try:
            r = requests.get(url, headers=headers, timeout=timeout, stream=stream)
            if r.status_code not in RETRY_STATUS:
                r.raise_for_status()  # other errors (e.g. 404) are not worth retrying
                return r
            reason = f"HTTP {r.status_code}"
            r.close()
        except (requests.ConnectionError, requests.Timeout) as e:
            reason = type(e).__name__
        wait = backoff_wait(attempt)
        print(f"  retry {attempt + 1}/{MAX_TRIES - 1} in {wait:.1f} s ({reason}): {url.rsplit('/', 1)[-1]}")
        time.sleep(wait)
    raise RuntimeError(f"giving up after {MAX_TRIES} tries: {url}")


def download_file(url, dest, refresh=False, chunk_mb=1, timeout=60):
    """Download url to dest and return dest as a Path.

    - refresh=False: if dest exists, nothing is requested (for files that never
      change, e.g. archive ZIPs or MeteoSwiss 'historical').
    - refresh=True: if dest exists, the server is asked with the stored ETag
      (file '<dest>.etag'); 304 = unchanged -> keep, otherwise download again.
    - The download goes to '<dest>.part' first and is renamed at the end, so a
      half-finished file is never mistaken for a complete one. If a '.part'
      file exists from an earlier run, the download continues where it stopped
      (HTTP Range request).
    """
    dest = Path(dest)
    etag_file = dest.with_name(dest.name + ".etag")
    if dest.exists() and not refresh:
        print(f"skip (exists): {dest.name}")
        return dest

    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + ".part")
    headers = {}
    if dest.exists() and etag_file.exists():
        headers["If-None-Match"] = etag_file.read_text().strip()

    # Resume: ask only for the bytes we do not have yet
    have = part.stat().st_size if part.exists() else 0
    if have:
        headers["Range"] = f"bytes={have}-"

    with get_with_retry(url, headers=headers, timeout=timeout, stream=True) as r:
        if r.status_code == 304:
            print(f"unchanged (ETag): {dest.name}")
            return dest
        # 206 = server sends only the missing part; 200 = full file, start over
        if have and r.status_code != 206:
            have = 0
        total = have + int(r.headers.get("Content-Length", 0))
        done, last_print = have, 0.0
        with open(part, "ab" if have else "wb") as f:
            for block in r.iter_content(chunk_size=chunk_mb * 1024 * 1024):
                f.write(block)
                done += len(block)
                # Print progress at most every 5 seconds to keep the terminal readable
                if time.time() - last_print > 5:
                    pct = f"{100 * done / total:5.1f} %" if total else ""
                    print(f"  {dest.name}: {done / 1e6:8.1f} MB {pct}", flush=True)
                    last_print = time.time()
        etag = r.headers.get("ETag")

    part.replace(dest)  # replace() also overwrites an older version of dest
    if etag:
        etag_file.write_text(etag)
    print(f"done: {dest.name} ({dest.stat().st_size / 1e6:.1f} MB)")
    time.sleep(PAUSE_S)
    return dest
