"""
CLI tool for managing media files.
"""

# pylint: disable=logging-fstring-interpolation,broad-exception-raised

import importlib.metadata
import json
import logging
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from enum import Enum
from pathlib import Path

import typer
from typing_extensions import Annotated, List, Optional

# root logger configuration
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s: %(message)s",
    stream=sys.stdout,
)

# package metadata handling
dist = importlib.metadata.distribution(__package__)


# enumerations
class MediaTypeEnum(str, Enum):
    """
    Supported media types enumeration
    """

    VIDEO = "video"
    IMAGE = "image"


# utils
def duration(start, decimals=2):
    """
    Calculates duration from given time `start` to current time.
    """
    return round(time.perf_counter() - start, decimals)


def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# typer
app = typer.Typer(
    help=f"{dist.metadata['summary']} (Version {dist.version})", no_args_is_help=True
)


@app.command()
def info():
    """
    Provides more information about media repository
    """


@app.command("import", no_args_is_help=True)
def import_media(
    # arguments
    import_path: Annotated[
        List[Path], typer.Argument(exists=True, dir_okay=True, readable=True)
    ],
    # options
    verbose: Annotated[
        Optional[int],
        typer.Option("--verbose", "-v", help="Increase command verbosity", count=True),
    ] = 0,
    recurse: Annotated[
        Optional[bool],
        typer.Option(
            "--recurse",
            "-r",
            help="Import media files recursively",
        ),
    ] = False,
    mediatype: Annotated[
        Optional[List[MediaTypeEnum]],
        typer.Option(
            "--mediatype",
            "-m",
            help="Media type to import",
        ),
    ] = [MediaTypeEnum.IMAGE.value, MediaTypeEnum.VIDEO.value],
    symlinks: Annotated[
        Optional[bool],
        typer.Option(
            "--symlinks",
            "-s",
            help="Do not copy media files and create symlinks instead",
        ),
    ] = False,
    delete: Annotated[
        Optional[bool],
        typer.Option(
            "--delete",
            help="Delete source file upon sucessfull import. Ignored if --symlinks is active.",
        ),
    ] = False,
    dryrun: Annotated[
        Optional[bool],
        typer.Option(
            "--dry-run",
            help="Run import without actual importing files (simulation)",
        ),
    ] = False,
    repo: Annotated[
        Optional[Path],
        typer.Option(
            help="Media repository (directory)",
            dir_okay=True,
            writable=True,
        ),
    ] = "./",
):
    """
    Import media from <IMPORT_PATH> into media repository
    """

    if verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)
    elif verbose == 1:
        logging.getLogger().setLevel(logging.INFO)

    logging.debug(f"Import command run with these options and arguments: {locals()}")

    exif_datetime_fmt = "%Y:%m:%d %H:%M:%S"

    scanned_files = []

    start = time.perf_counter()

    # scan files and parse exif data
    try:
        # use json output (-j) in exiftool
        import_abs_paths = [str(p.absolute()) for p in import_path]
        exiftool_cmd = ["exiftool", "-j"] + import_abs_paths

        if recurse:
            exiftool_cmd.insert(1, "-r")

        logging.info(
            f"Searching / parsing media files in {' '.join(import_abs_paths)} started"
        )

        logging.debug(f"Running external command: {' '.join(exiftool_cmd)}")

        p = subprocess.run(exiftool_cmd, capture_output=True)

        if len(p.stdout) > 0:
            # parse list of dictionaries from exiftool json output
            scanned_files = json.loads(p.stdout)
        else:
            if p.returncode == 0:
                raise Warning("No files have been found")
            # sometimes exiftool exits with 1 without apparent reason, so only warning
            # is raised and processing continues
            else:
                raise Warning(f"exiftool exit code: {p.returncode}, stderr: {p.stderr}")
    except Warning as e:
        logging.warning(e)
    except FileNotFoundError:
        # logging.error("exiftool command not available on system PATH")
        print_err("FATAL: exiftool command not available on system PATH")
        raise typer.Abort()
    except json.decoder.JSONDecodeError:
        print_err("FATAL: parsing json exiftool json output failed")
    except Exception as e:
        print_err(e)
        raise typer.Abort()

    # further processing only on media files (image/video)
    media_files = [
        f
        for f in scanned_files
        if f.get("MIMEType") and f["MIMEType"].split("/")[0] in mediatype
    ]

    logging.info(
        f"Found {len(media_files)} media files "
        f"(out of {len(scanned_files)}) "
        f"in {duration(start)}s"
    )

    import_stats = {"ok": 0, "failed": 0, "deleted": 0}

    # import individual media files
    for f in media_files:
        file_start = time.perf_counter()
        src_file_path = Path(f["Directory"]).absolute() / Path(f["FileName"])

        try:
            # parsing EXIF yelded warning/error
            if f.get("Warning") is not None:
                raise Exception(f["Warning"])

            datetime_original = f.get("DateTimeOriginal") or f.get("CreateDate")

            if datetime_original:
                datetime_original = datetime.strptime(
                    datetime_original, exif_datetime_fmt
                )
                dst_dir = Path(datetime_original.strftime("%Y/%m"))
                dst_file_path = (
                    repo
                    / dst_dir
                    / Path(
                        datetime_original.strftime("%Y-%m-%dT%H:%M:%S")
                        + "_"
                        + f["FileName"]
                    )
                )
            else:
                dst_dir = Path("unknown")
                dst_file_path = repo / dst_dir / Path(f["FileName"])

            if not dst_file_path.is_file():
                if not dryrun:
                    # create destination dir
                    os.makedirs(repo / dst_dir, exist_ok=True)
                    # copy or create symlink
                    if symlinks:
                        dst_file_path.symlink_to(src_file_path)
                    else:
                        # shutil.copy2 tries to preserve file metadata
                        shutil.copy2(src_file_path, dst_file_path)
            else:
                raise Exception(f"File/symlink <{dst_file_path}> already exists")

        except Exception as e:
            # failed import
            import_stats["failed"] += 1
            logging.error(f"File <{src_file_path}> not imported, reason: {e}")
        else:
            # sucessfull import
            import_stats["ok"] += 1

            file_type = "symlink" if symlinks else "file"

            logging.info(
                f"File <{src_file_path}> successfuly imported "
                f"as {file_type} <{dst_file_path}> "
                f"in {duration(file_start, 3)}s"
            )

            # delete source file
            if not dryrun and delete:
                try:
                    if symlinks:
                        raise Exception("--symlink option active")
                    src_file_path.unlink()
                    import_stats["deleted"] += 1
                except Exception as e:
                    logging.warning(
                        f"File <{src_file_path}> was not deleted, reason: {e}"
                    )
                else:
                    logging.info(f"File <{src_file_path}> was deleted")

    logging.info(
        "Importing files finished: "
        f"{import_stats['ok']} (Imported), "
        f"{import_stats['failed']} (Failed), "
        f"{import_stats['deleted']} (Source deleted), "
        f"{len(media_files)} (Total media), "
        f"{len(scanned_files)} (Total scanned) "
        f"in {duration(start)}s"
    )


if __name__ == "__main__":
    app()
