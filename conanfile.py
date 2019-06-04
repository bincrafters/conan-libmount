#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
from conans.errors import ConanInvalidConfiguration
import os


class LibmountConan(ConanFile):
    name = "libmount"
    version = "2.33.1"
    description = "The libmount library is used to parse /etc/fstab, /etc/mtab and /proc/self/mountinfo files, manage the mtab file, evaluate mount options, etc"
    topics = ("conan", "mount", "libmount", "linux", "util-linux")
    url = "https://github.com/bincrafters/conan-libmount"
    homepage = "https://git.kernel.org/pub/scm/utils/util-linux/util-linux.git"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GPL-2.0-or-later"
    exports = ["LICENSE.md"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration("only Linux is supported")

    def source(self):
        version_tokens = self.version.split(".")
        major_minor = "%s.%s" % (version_tokens[0], version_tokens[1])
        source_url = "https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/v%s/util-linux-%s.tar.gz" % (major_minor, self.version)
        sha256 = "e15bd3142b3a0c97fffecaed9adfdef8ab1d29211215d7ae614c177ef826e73a"
        tools.get(source_url, sha256=sha256)
        extracted_dir = "util-linux-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            args = ["--disable-all-programs", "--enable-libmount", "--enable-libblkid"]
            if self.options.shared:
                args.extend(["--disable-static", "--enable-shared"])
            else:
                args.extend(["--disable-shared", "--enable-static"])
            env_build = AutoToolsBuildEnvironment(self)
            env_build.configure(args=args)
            env_build.make()
            env_build.install()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = ["mount", "blkid"]
        self.cpp_info.includedirs.append(os.path.join("include", "libmount"))
