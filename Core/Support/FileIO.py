# ORIGINAL CREATOR: Luca Garofalo (Lucksi)
# AUTHOR: Luca Garofalo (Lucksi)
# Copyright (C) 2024 Lucksi <lukege287@gmail.com>
# License: GNU General Public License v3.0

import json
import os
import tempfile


class Json:

    @staticmethod
    def write_atomic(path, payload):
        directory = os.path.dirname(path)
        if directory == "":
            directory = "."
        fd, temp_path = tempfile.mkstemp(prefix=".tmp_json_", dir=directory)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=4)
            os.replace(temp_path, path)
        except Exception:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise
