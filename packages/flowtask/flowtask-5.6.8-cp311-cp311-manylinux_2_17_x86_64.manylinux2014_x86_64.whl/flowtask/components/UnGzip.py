import os
import logging
import asyncio
from typing import List
from collections.abc import Callable
from pathlib import PosixPath, Path, PurePath
import tarfile
from ..exceptions import FileError, ComponentError, FileNotFound
from .FileCopy import FileCopy
from ..interfaces.compress import CompressSupport


class UnGzip(CompressSupport, FileCopy):
    """
    UnGzip

        Overview

            The UnGzip class is a component for decompressing Gzip (.gz) files, including compressed tarballs (e.g., .tar.gz, .tar.bz2, .tar.xz).
            This component extracts the specified Gzip or tarball file into a target directory and supports optional source file deletion
            after extraction.

        .. table:: Properties
        :widths: auto

            +----------------+----------+-----------+---------------------------------------------------------------+
            | Name           | Required | Summary                                                                   |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | filename       |   Yes    | The path to the Gzip file to uncompress.                                  |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | directory      |   Yes    | The target directory where files will be extracted.                       |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | delete_source  |   No     | Boolean indicating if the source file should be deleted post-extraction.  |
            +----------------+----------+-----------+---------------------------------------------------------------+
            | extract        |   No     | Dictionary specifying filenames to extract and/or output directory.       |
            +----------------+----------+-----------+---------------------------------------------------------------+

        Returns

            This component extracts files from a specified Gzip or tarball archive into the designated directory
            and returns a list of paths to the extracted files. It tracks metrics for the output directory and the source
            Gzip file. If configured, the original compressed file is deleted after extraction. Errors encountered during
            extraction or directory creation are logged and raised as exceptions.
    """  # noqa

    _namelist = []
    _directory = ""

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self._output: PurePath = None
        self._filenames: List = []
        self.delete_source: bool = False
        super(UnGzip, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        await super().start(**kwargs)
        # Handle extraction settings
        if hasattr(self, "extract"):
            for _, filename in enumerate(self.extract["filenames"]):
                filename = self.mask_replacement(filename)
                self._filenames.append(filename)
            if "directory" in self.extract:
                self._output = Path(self.extract["directory"]).resolve()
                # Create directory if not exists
                try:
                    self._output.mkdir(parents=True, exist_ok=True)
                except Exception as err:
                    logging.error(f"Error creating directory {self._output}: {err}")
                    raise ComponentError(
                        f"Error creating directory {self._output}: {err}"
                    ) from err
            else:
                # same directory:
                self._output = Path(self.directory)
        return True

    async def close(self):
        pass

    async def run(self):
        # Check if file exists
        self._result = {}
        for file in self._sources:
            if not file.exists() or not file.is_file():
                raise FileNotFound(
                    f"Compressed File doesn't exist: {file}"
                )
            # Uncompress the gzip/tar.gz file
            try:
                files = await self.uncompress_gzip(
                    source=file,
                    destination=self._destination,
                    remove_source=self.delete_source,
                )
                print('List files ', files)
            except (FileNotFoundError, ComponentError) as err:
                raise FileError(f"UnGzip failed: {err}")
            except RuntimeError as err:
                raise FileError(f"UnGzip failed: {err}")

            if self.delete_source:
                file.unlink(missing_ok=True)

            filenames = []
            for filename in files:
                filenames.append(filename)
            self._result[str(file)] = filenames

        return self._result
