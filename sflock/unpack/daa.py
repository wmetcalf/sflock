# Copyright (C) 2016 Jurriaan Bremer.
# Copyright (C) 2018-2019 Hatching B.V.
# This file is part of SFlock - http://www.sflock.org/.
# See the file 'docs/LICENSE.txt' for copying permission.

import os
import subprocess
import tempfile

from sflock.abstracts import Unpacker

"""
wget http://www.poweriso.com/poweriso-1.3.tar.gz
tar xf poweriso-1.3.tar.gz
sudo mv poweriso /usr/bin
"""

class DaaFile(Unpacker):
    name = "daafile"
    exe = "/usr/bin/poweriso"
    exts = b".daa"
    magic = "PowerISO Direct-Access-Archive"

    def unpack(self, password=None, duplicates=None):
        dirpath = tempfile.mkdtemp()

        if self.f.filepath:
            filepath = os.path.abspath(self.f.filepath)
            temporary = False
        else:
            filepath = self.f.temp_path(".daa")
            temporary = True

        #ret = self.zipjail(
        #    filepath, dirpath, "extract",  filepath, "/", "-od", dirpath
        #)
        p = subprocess.check_output([self.exe, "extract",  filepath, "/", "-od", dirpath])
        #p = subprocess.check_output(["/usr/bin/poweriso", "extract",  "test.daa", "/", "-od", "/tmp"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if "Extracting to" not in p:
        #if not ret:
            return []

        if temporary:
            os.unlink(filepath)

        return self.process_directory(dirpath, duplicates)
