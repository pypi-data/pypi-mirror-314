#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
from tempfile import TemporaryDirectory

from setuptools import setup
from setuptools.extension import Extension

script_dir = os.path.dirname(os.path.abspath(__file__))

otf2lib_sources = [
    os.path.join("src", name)
    for name in os.listdir(os.path.join(script_dir, "src"))
    if name.endswith(".c") and not name.endswith("_inc.c") and "sion" not in name
]

with TemporaryDirectory() as tmp_dir:
    print(tmp_dir)
    subprocess.check_call(
        ["common/utils/src/exception/finalize_error_codes.sh",
         "OTF2",
         "share/otf2/otf2.errors",
         os.path.join(tmp_dir, "otf2/OTF2_ErrorCodes.h"),
         os.path.join(tmp_dir, "otf2_error_decls.gen.h"),
         "common/utils/src/exception/ErrorCodes.tmpl.h",
         ], cwd=script_dir)

    extensions = [
        Extension(
            # this will put the lib in _otf2/_otf2[...].so
            # at the same place autotools puts it
            name="_otf2._otf2",
            sources=otf2lib_sources
                    + [
                        "common/hash/jenkins_hash.c",
                        "common/utils/src/cstr/UTILS_CStr.c",
                        "common/utils/src/exception/UTILS_Error.c",
                        "common/utils/src/io/UTILS_IO_Tools.c",
                        "common/utils/src/io/UTILS_IO_GetExe.c",
                    ],
            include_dirs=[
                "build-config/common/",
                "include",
                "src",
                "common/utils/include",
                "common/hash",
                "src/python/extra",
                tmp_dir,
            ],
            define_macros=[
                ("NOCROSS_BUILD", None),
                ("NDEBUG", None),
            ],
            language="c",
        ),
    ]

    version = subprocess.check_output(
        ["common/generate-package-version.sh", "VERSION"],
        cwd=os.path.join(script_dir, "build-config")).decode().strip()

    setup(
        ext_modules=extensions,
        version=version
    )
