"""Shared download helper for all data sources (Ist-Daten, service points, weather).

Why a shared helper: every source is downloaded the same way, by script over
HTTP. Keeping it in one place means the rules apply everywhere:
- skip files that already exist (idempotent: re-running a script is cheap),
- resume a broken download instead of starting again (large files, slow Wi-Fi),
- send a short pause and a clear User-Agent (terms of use of the sources),
- show progress, so a long run in the terminal is not a black box.

Usage:
    from src.download import download_file
    path = download_file(url, RAW_DIR / "stops" / "service_points.csv")
"""
import time
from pathlib import Path

import requests

# Identify ourselves to the data providers (polite and makes support easier)
HEADERS = {"User-Agent": "ZHAW-DA-HS26-group3 student project (github.com/rexheeri/da-projekt-hs26)"}

# Seconds to wait after each request, so we never hammer a server
PAUSE_S = 1.0


def download_file(url, dest, chunk_mb=1, timeout=60):
    """Download url to dest and return dest as a Path.

    - If dest already exists, nothing is downloaded (the file counts as done).
    - The download is written to '<dest>.part' first and only renamed at the end,
      so a half-finished file is never mistaken for a complete one.
    - If a '.part' file exists from an earlier run, the download continues where
      it stopped (HTTP Range request) instead of starting from zero.
    """
    dest = Path(dest)
    if dest.exists():
        print(f"skip (exists): {dest.name}")
        return dest

    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + ".part")

    # Resume: ask the server only for the bytes we do not have yet
    have = part.stat().st_size if part.exists() else 0
    headers = dict(HEADERS)
    if have:
        headers["Range"] = f"bytes={have}-"

    # stream=True reads the file in pieces instead of loading it all into memory
    with requests.get(url, headers=headers, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        # 206 = server sends only the missing part; 200 = server ignored Range, start over
        if have and r.status_code != 206:
            have = 0
        total = have + int(r.headers.get("Content-Length", 0))
        mode = "ab" if have else "wb"
        done = have
        last_print = 0.0
        with open(part, mode) as f:
            for block in r.iter_content(chunk_size=chunk_mb * 1024 * 1024):
                f.write(block)
                done += len(block)
                # Print progress at most every 2 seconds to keep the terminal readable
                if time.time() - last_print > 2:
                    pct = f"{100 * done / total:5.1f} %" if total else ""
                    print(f"  {dest.name}: {done / 1e6:8.1f} MB {pct}", flush=True)
                    last_print = time.time()

    part.rename(dest)
    print(f"done: {dest.name} ({dest.stat().st_size / 1e6:.1f} MB)")
    time.sleep(PAUSE_S)
    return dest
