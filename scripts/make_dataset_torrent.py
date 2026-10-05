#!/usr/bin/env python3
"""
scripts/make_dataset_torrent.py - Zero-Dependency BitTorrent Dataset Packager

Generates BitTorrent v1 .torrent files and Magnet URIs for single files or
multi-file dataset directories. Includes multi-tier public tracker pools,
DHT bootstrap nodes, automatic piece-size calibration, and BEP 0019 web-seeding.
"""

import argparse
import hashlib
import math
import os
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

# High-reliability Tier-1 public tracker announce URLs
DEFAULT_TRACKERS: List[List[str]] = [
    ["udp://tracker.opentrackr.org:1337/announce"],
    ["udp://open.stealth.si:80/announce"],
    ["udp://tracker.torrent.eu.org:451/announce"],
    ["udp://explodie.org:6969/announce"],
    ["http://tracker.academictorrents.com:8080/announce"],
]

DEFAULT_DHT_NODES: List[List[Union[str, int]]] = [
    ["router.bittorrent.com", 6881],
    ["dht.transmissionbt.com", 6881],
    ["router.utorrent.com", 6881],
]


# ============================================================================
# Pure-Python Bencode Encoder & Decoder (BEP 0003)
# ============================================================================

def bencode(data: Any) -> bytes:
    """Encode Python objects into BitTorrent bencoded bytes."""
    if isinstance(data, int):
        return f"i{data}e".encode("ascii")
    elif isinstance(data, bytes):
        return f"{len(data)}:".encode("ascii") + data
    elif isinstance(data, str):
        encoded = data.encode("utf-8")
        return f"{len(encoded)}:".encode("ascii") + encoded
    elif isinstance(data, (list, tuple)):
        return b"l" + b"".join(bencode(item) for item in data) + b"e"
    elif isinstance(data, dict):
        # Keys must be sorted by raw byte representation per BEP 0003
        items = []
        for k, v in data.items():
            key_bytes = k.encode("utf-8") if isinstance(k, str) else k
            items.append((key_bytes, v))
        items.sort(key=lambda x: x[0])
        encoded_dict = b"d"
        for k_bytes, val in items:
            encoded_dict += f"{len(k_bytes)}:".encode("ascii") + k_bytes + bencode(val)
        return encoded_dict + b"e"
    else:
        raise TypeError(f"Unsupported type for bencoding: {type(data)}")


def bdecode(data: bytes) -> Tuple[Any, int]:
    """Decode bencoded bytes into Python objects. Returns (object, bytes_read)."""
    if not data:
        raise ValueError("Cannot bdecode empty buffer")
    char = data[:1]
    if char == b"i":
        end = data.index(b"e", 1)
        return int(data[1:end]), end + 1
    elif char.isdigit():
        colon = data.index(b":")
        length = int(data[:colon])
        start = colon + 1
        return data[start : start + length], start + length
    elif char == b"l":
        items = []
        idx = 1
        while data[idx : idx + 1] != b"e":
            item, read = bdecode(data[idx:])
            items.append(item)
            idx += read
        return items, idx + 1
    elif char == b"d":
        res = {}
        idx = 1
        while data[idx : idx + 1] != b"e":
            k, k_read = bdecode(data[idx:])
            idx += k_read
            v, v_read = bdecode(data[idx:])
            idx += v_read
            if isinstance(k, bytes):
                k = k.decode("utf-8", errors="replace")
            res[k] = v
        return res, idx + 1
    else:
        raise ValueError(f"Invalid bencode token: {char}")


# ============================================================================
# Piece Size Optimization & Piece Hashing
# ============================================================================

def calculate_optimal_piece_length(total_size: int, explicit_piece_size_kb: int = 0) -> int:
    """
    Computes an optimal power-of-2 piece size in bytes.
    Target: between 1,000 and 2,500 pieces to balance metadata size and overhead.
    """
    if explicit_piece_size_kb > 0:
        return explicit_piece_size_kb * 1024

    if total_size <= 50 * 1024 * 1024:         # <= 50 MB
        return 256 * 1024                       # 256 KB
    elif total_size <= 500 * 1024 * 1024:      # <= 500 MB
        return 512 * 1024                       # 512 KB
    elif total_size <= 2 * 1024 * 1024 * 1024: # <= 2 GB
        return 1024 * 1024                      # 1 MB
    elif total_size <= 8 * 1024 * 1024 * 1024: # <= 8 GB
        return 2 * 1024 * 1024                  # 2 MB
    elif total_size <= 32 * 1024 * 1024 * 1024:# <= 32 GB
        return 4 * 1024 * 1024                  # 4 MB
    else:
        return 8 * 1024 * 1024                  # 8 MB


def collect_dataset_files(target_path: Path) -> Tuple[bool, int, List[Tuple[Path, int, List[str]]]]:
    """
    Discovers target files and returns:
    (is_single_file, total_size, [(absolute_path, file_size, relative_path_parts)])
    """
    if target_path.is_file():
        size = target_path.stat().st_size
        return True, size, [(target_path, size, [target_path.name])]

    if not target_path.is_dir():
        raise FileNotFoundError(f"Path does not exist: {target_path}")

    files: List[Tuple[Path, int, List[str]]] = []
    total_size = 0

    # Sort files deterministically for reproducible piece ordering
    all_paths = sorted(target_path.rglob("*"))
    for p in all_paths:
        if p.is_file() and not p.name.startswith("."):
            size = p.stat().st_size
            rel_parts = list(p.relative_to(target_path).parts)
            files.append((p, size, rel_parts))
            total_size += size

    if not files:
        raise ValueError(f"Target directory contains no valid data files: {target_path}")

    return False, total_size, files


def hash_dataset_pieces(
    file_list: List[Tuple[Path, int, List[str]]],
    total_size: int,
    piece_length: int,
    progress_callback=None,
) -> bytes:
    """
    Sequentially streams and hashes all data chunks across single or multiple files.
    Returns concatenated 20-byte SHA-1 digests.
    """
    pieces = bytearray()
    current_piece = bytearray()
    processed_bytes = 0
    start_time = time.time()

    for file_path, file_size, _ in file_list:
        with open(file_path, "rb") as f:
            while True:
                needed = piece_length - len(current_piece)
                chunk = f.read(needed)
                if not chunk:
                    break
                current_piece.extend(chunk)
                processed_bytes += len(chunk)

                if len(current_piece) == piece_length:
                    pieces.extend(hashlib.sha1(current_piece).digest())
                    current_piece.clear()
                    if progress_callback:
                        progress_callback(processed_bytes, total_size, start_time)

    # Final partial piece
    if len(current_piece) > 0:
        pieces.extend(hashlib.sha1(current_piece).digest())
        if progress_callback:
            progress_callback(processed_bytes, total_size, start_time)

    return bytes(pieces)


def format_bytes(num_bytes: int) -> str:
    """Formats bytes into human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if num_bytes < 1024.0 or unit == "TB":
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.2f} TB"


def print_progress(processed: int, total: int, start_time: float):
    """Prints a lightweight CLI progress line."""
    elapsed = max(time.time() - start_time, 0.001)
    rate = processed / elapsed / (1024 * 1024)
    pct = (processed / total) * 100 if total > 0 else 100
    sys.stdout.write(
        f"\r  Hashing: [{pct:6.2f}%] {format_bytes(processed)} / {format_bytes(total)} ({rate:.1f} MB/s)"
    )
    sys.stdout.flush()


# ============================================================================
# Main Torrent & Magnet Generation Pipeline
# ============================================================================

def create_dataset_torrent(
    target_path: Path,
    output_torrent: Path = None,
    piece_size_kb: int = 0,
    trackers: List[List[str]] = None,
    web_seeds: List[str] = None,
    comment: str = "Aaradhya Research & Engineering Dataset",
) -> Dict[str, Any]:
    """Builds and writes a .torrent file and constructs the Magnet link."""
    target_path = target_path.resolve()
    is_single, total_size, file_list = collect_dataset_files(target_path)
    piece_length = calculate_optimal_piece_length(total_size, piece_size_kb)
    total_pieces = math.ceil(total_size / piece_length)

    print(f"Target: {target_path}")
    print(f"Structure: {'Single File' if is_single else f'Directory ({len(file_list)} files)'}")
    print(f"Total Size: {format_bytes(total_size)} ({total_size:,} bytes)")
    print(f"Piece Length: {format_bytes(piece_length)} | Total Pieces: {total_pieces:,}\n")

    # Hash pieces
    pieces_digest = hash_dataset_pieces(file_list, total_size, piece_length, progress_callback=print_progress)
    print("\n  Hashing complete!\n")

    # Construct the 'info' dictionary
    name = target_path.name
    info_dict: Dict[str, Any] = {
        "name": name,
        "piece length": piece_length,
        "pieces": pieces_digest,
    }

    if is_single:
        info_dict["length"] = total_size
    else:
        info_files = []
        for _, f_size, rel_parts in file_list:
            info_files.append({"length": f_size, "path": rel_parts})
        info_dict["files"] = info_files

    # Calculate infohash (SHA-1 of bencoded info_dict)
    info_bencoded = bencode(info_dict)
    info_hash_bytes = hashlib.sha1(info_bencoded).digest()
    info_hash_hex = hashlib.sha1(info_bencoded).hexdigest()

    # Trackers
    active_trackers = trackers if trackers is not None else DEFAULT_TRACKERS
    primary_tracker = active_trackers[0][0] if active_trackers and active_trackers[0] else ""

    # Construct master torrent dictionary
    torrent_dict: Dict[str, Any] = {
        "info": info_dict,
        "announce": primary_tracker,
        "announce-list": active_trackers,
        "creation date": int(time.time()),
        "created by": "make_dataset_torrent.py (Aaradhya Dev Tamrakar)",
        "comment": comment,
        "nodes": DEFAULT_DHT_NODES,
    }

    if web_seeds:
        torrent_dict["url-list"] = web_seeds

    # Write output file
    if output_torrent is None:
        output_torrent = target_path.parent / f"{target_path.name}.torrent"
    output_torrent = output_torrent.resolve()

    bencoded_torrent = bencode(torrent_dict)
    with open(output_torrent, "wb") as f:
        f.write(bencoded_torrent)

    # Build Magnet Link
    magnet_params = [
        ("xt", f"urn:btih:{info_hash_hex}"),
        ("dn", name),
    ]
    for tier in active_trackers:
        for tr in tier:
            magnet_params.append(("tr", tr))
    if web_seeds:
        for ws in web_seeds:
            magnet_params.append(("ws", ws))

    magnet_uri = "magnet:?" + urllib.parse.urlencode(magnet_params)

    return {
        "torrent_file": str(output_torrent),
        "info_hash": info_hash_hex,
        "magnet_uri": magnet_uri,
        "name": name,
        "total_size": total_size,
        "piece_length": piece_length,
        "total_pieces": total_pieces,
        "trackers": active_trackers,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Zero-dependency BitTorrent dataset packager and magnet link generator."
    )
    parser.add_argument("target", help="Path to file or folder to package into a torrent")
    parser.add_argument(
        "-o", "--output", help="Output .torrent path (default: <target>.torrent)", default=None
    )
    parser.add_argument(
        "--piece-size-kb",
        type=int,
        default=0,
        help="Explicit piece length in KB (e.g. 1024, 2048, 4096). Default auto-calibrates.",
    )
    parser.add_argument(
        "--web-seed",
        action="append",
        dest="web_seeds",
        help="BEP 0019 HTTP Web-Seed URL (fallback mirror). Can be specified multiple times.",
    )
    parser.add_argument(
        "--comment",
        default="Aaradhya Research & Engineering Dataset",
        help="Metadata comment string.",
    )

    args = parser.parse_args()
    target_path = Path(args.target)
    if not target_path.exists():
        print(f"Error: Target path '{target_path}' does not exist.", file=sys.stderr)
        return 1

    out_path = Path(args.output) if args.output else None
    res = create_dataset_torrent(
        target_path=target_path,
        output_torrent=out_path,
        piece_size_kb=args.piece_size_kb,
        web_seeds=args.web_seeds,
        comment=args.comment,
    )

    print("=" * 60)
    print("TORRENT GENERATION SUCCESSFUL")
    print("=" * 60)
    print(f"Dataset Name : {res['name']}")
    print(f"File Size    : {format_bytes(res['total_size'])} ({res['total_size']:,} bytes)")
    print(f"Infohash     : {res['info_hash']}")
    print(f"Torrent Path : {res['torrent_file']}")
    print("\nMagnet Link (Copy & Share):")
    print("-" * 60)
    print(res["magnet_uri"])
    print("-" * 60)
    print("\nTo seed this immediately with aria2c, run:")
    parent_dir = target_path.parent
    print(
        f'aria2c --enable-dht=true --enable-peer-exchange=true --seed-ratio=0.0 --dir="{parent_dir}" "{res["torrent_file"]}"\n'
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
