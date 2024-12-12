import io
import re
from datetime import datetime
from io import BytesIO
from typing import Generator, Optional

import pysftp
from django.conf import settings

from ..models import ImportCredential
from .abstract import AbstractDataBackend
from .utils import register


@register("SFTP", save_data_in_import_source=True, passive_only=True)
class DataBackend(AbstractDataBackend):
    def __init__(
        self,
        import_credential: Optional[ImportCredential] = None,
        **kwargs,
    ):
        if not import_credential:
            raise ValueError("The sftp backend needs an import credential")

        self.username = import_credential.username
        self.password = import_credential.password
        self.host = import_credential.additional_resources.get("host", "")
        self.port = import_credential.additional_resources.get("port", "")

    def get_files(
        self,
        execution_time: datetime,
        sftp_folder,
        file_name_regex: Optional[str] = None,
        cleanup_files: Optional[bool] = getattr(settings, "WBIMPORT_EXPORT_SFTPBACKEND_CLEAN_FILES", False),
        **kwargs,
    ) -> Generator[tuple[str, BytesIO], None, None]:
        # Create CnOpts for Paramiko
        cnopts = pysftp.CnOpts()
        setattr(cnopts, "hostkeys", None)

        # Create Connection to the SFTP Server
        with pysftp.Connection(
            self.host, port=self.port, username=self.username, password=self.password, cnopts=cnopts
        ) as sftp:
            # Change working directory
            sftp.cwd(sftp_folder)

            # Filter all the files we need
            file_names = sftp.listdir()
            if file_name_regex:
                # Compile the regex for later filtering the files
                file_names = filter(lambda x: re.match(file_name_regex, x), file_names)

            for file_name in file_names:
                # Create a Buffer where we write the file to
                sftp_file = io.BytesIO()
                sftp.getfo(file_name, sftp_file)
                yield file_name, sftp_file

                if cleanup_files:
                    # Delete the file from the server
                    sftp.remove(file_name)
