# Package Assets Action

Package release artifacts and generate checksums for GitHub releases with
optional dockerized execution.

## Features

- ✅ Packages artifacts in the given directory and emits JSON metadata
- ✅ Generates sha256 checksum list suitable for `sha256sum -c`
- ✅ Safe defaults when artifacts are missing (empty outputs)
- ✅ Optional docker execution via GHCR image

## Usage

````yaml
- name: Build artifacts
  run: make dist

- name: Package assets
  id: package
  uses: jdfalk/package-assets-action@v1
  with:
    artifacts-dir: dist

- name: Create release
  uses: softprops/action-gh-release@v1
  with:
    files: dist/*
    body: |
      ## Checksums
      ```
      ${{ steps.package.outputs.checksums }}
      ```
````

### Force Docker Execution

```yaml
- uses: jdfalk/package-assets-action@v1
  id: package
  with:
    use-docker: true
    docker-image: ghcr.io/jdfalk/package-assets-action:main
```

## Inputs

| Input           | Description                                                      | Default                                     |
| --------------- | ---------------------------------------------------------------- | ------------------------------------------- |
| `artifacts-dir` | Directory containing build artifacts                             | `dist`                                      |
| `use-docker`    | Run the action inside the published container image              | `false`                                     |
| `docker-image`  | Docker image reference (tag or digest) when `use-docker` is true | `ghcr.io/jdfalk/package-assets-action:main` |

## Outputs

| Output      | Description                                 |
| ----------- | ------------------------------------------- |
| `assets`    | Packaged assets as JSON array with metadata |
| `checksums` | SHA256 checksums in standard format         |

## Asset JSON Format

```json
[
  {
    "filename": "app-linux-amd64",
    "size": 12345678,
    "sha256": "abc123def456..."
  },
  {
    "filename": "app.tar.gz",
    "size": 987654,
    "sha256": "xyz789uvw012..."
  }
]
```

## Checksum Format

Compatible with `sha256sum` command:

```text
abc123def456...  app-linux-amd64
xyz789uvw012...  app.tar.gz
```

Verify with:

```bash
sha256sum -c checksums.txt
```

## Examples

### Include checksums in release

```yaml
- name: Package and create release
  id: release
  run: |
    make dist

- name: Package assets
  id: package
  uses: jdfalk/package-assets-action@v1
  with:
    artifacts-dir: dist

- name: Create release
  uses: softprops/action-gh-release@v1
  with:
    files: |
      dist/*
    body: |
      ## Release Assets

      | File                                                      | Size                                                  | SHA256                                                    |
      | --------------------------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------- |
      | ${{ fromJson(steps.package.outputs.assets)[0].filename }} | ${{ fromJson(steps.package.outputs.assets)[0].size }} | `${{ fromJson(steps.package.outputs.assets)[0].sha256 }}` |

      ## Verify Checksums
      \`\`\`bash
      ${{ steps.package.outputs.checksums }}
      \`\`\`
```

### Multi-artifact build

```yaml
- name: Build all artifacts
  run: |
    make build-go
    make build-python
    make build-docker

- name: Package
  id: package
  uses: jdfalk/package-assets-action@v1
  with:
    artifacts-dir: dist

- name: Release
  uses: softprops/action-gh-release@v1
  with:
    files: dist/**/*
    body: '${{ steps.package.outputs.checksums }}'
```

## Features

✅ **SHA256 Hashing** - Industry-standard checksums ✅ **Recursive Discovery** -
Finds artifacts in subdirectories ✅ **File Metadata** - Includes size in JSON
output ✅ **Standard Formats** - Compatible with sha256sum ✅ **Release
Integration** - Easy GitHub release body insertion

## Checksum Verification

Users can verify artifacts:

```bash
# Download checksums.txt from release
wget https://github.com/user/repo/releases/download/v1.0.0/checksums.txt

# Verify downloads
sha256sum -c checksums.txt
```

## Related Actions

- [generate-version-action](https://github.com/jdfalk/generate-version-action) -
  Generate semantic versions
- [release-strategy-action](https://github.com/jdfalk/release-strategy-action) -
  Determine release strategy
