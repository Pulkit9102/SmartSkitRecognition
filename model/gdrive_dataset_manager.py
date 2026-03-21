"""
Google Drive features removed.

This repository previously contained scripts and docs for an extended
Google Drive team-collaboration workflow. Those files were removed or
disabled. If you need Google Drive dataset downloads, re-add a simple
`gdown`-based downloader or follow the instructions in `HOW_TO_RUN.md`.

This file is a placeholder to avoid runtime errors if something imports
`gdrive_dataset_manager`. It intentionally does nothing.
"""

def notify_removed():
    print("Google Drive integration has been removed from this repository.")

if __name__ == '__main__':
    notify_removed()
