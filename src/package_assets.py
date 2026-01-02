#!/usr/bin/env python3
# file: src/package_assets.py
# version: 1.0.0
# guid: 9c0d1e2f-3a4b-5c6d-7e8f-9a0b1c2d3e4f

"""Package release artifacts and generate checksums"""

import hashlib
import json
import os
from pathlib import Path


def write_output(name, value):
    """Write to GITHUB_OUTPUT."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as f:
            if "\n" in str(value):
                delimiter = "EOF"
                f.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")
            else:
                f.write(f"{name}={value}\n")


def write_summary(text):
    """Write to GITHUB_STEP_SUMMARY."""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(text + "\n")


def compute_sha256(file_path):
    """Compute SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def main():
    artifacts_dir = Path(os.environ.get("ARTIFACTS_DIR", "dist"))

    assets = []
    checksums = {}

    if not artifacts_dir.exists():
        print(f"⚠️ Artifacts directory not found: {artifacts_dir}")
        write_output("assets", json.dumps([], separators=(",", ":")))
        write_output("checksums", "")
        return

    # Find all artifacts
    for artifact in sorted(artifacts_dir.glob("**/*")):
        if artifact.is_file():
            rel_path = artifact.relative_to(artifacts_dir)
            sha256 = compute_sha256(artifact)

            assets.append(
                {
                    "filename": str(rel_path),
                    "size": artifact.stat().st_size,
                    "sha256": sha256,
                }
            )

            checksums[str(rel_path)] = sha256

    # Generate checksums file
    checksums_content = "\n".join(f"{sha}  {filename}" for filename, sha in checksums.items())

    write_output("assets", json.dumps(assets, separators=(",", ":")))
    write_output("checksums", checksums_content)

    # Summary
    write_summary("## 📦 Packaged Assets")
    write_summary(f"- **Total artifacts:** {len(assets)}")
    if assets:
        write_summary("\n### Files:")
        for asset in assets:
            size_mb = asset["size"] / (1024 * 1024)
            write_summary(f"- `{asset['filename']}` ({size_mb:.2f} MB)")
            write_summary(f"  SHA256: `{asset['sha256']}`")

    print(f"✅ Packaged {len(assets)} artifacts")


if __name__ == "__main__":
    main()
