#------------------------------------------------------------------------------
#
# Copyright (c) 2014 Glympse Inc.  All rights reserved.
#
#------------------------------------------------------------------------------

import os, sys
import utilities


class DirectoryWalker:

    def __init__(self, package, factory, config):
        self.package = package
        self.src_dir = package["src"]
        self.dest_dir = package["dst"]
        self.include = package.get("include", [])
        self.exclude = package.get("exclude", [])
        self.factory = factory
        self.config = config

    def process(self):
        self.factory.begin_package(self.config, self.package)

        dir = os.listdir(self.src_dir)
        dir = dir[:]
        
        for file in dir:
            src_file = self.src_dir + '/' + file

            # Check exclude filder
            if self.include and ( not file in self.include ):
                continue
            if ( file in self.exclude ) or os.path.isdir(src_file):
                continue

            # Instantiate translator
            translator = self.factory.translator()

            # Generate destination file name
            dest_file = file
            dest_file = dest_file.replace(".h", "." + translator.extension())
            dest_file = dest_file.replace(".java", "." + translator.extension())
            dest_file = self.dest_dir + '/' + dest_file

            # Perform translation
            translator.translate(src_file, dest_file, self.config, self.package)

        self.factory.package_completed(self.config, self.package)


class Config:

    def __init__(self):
        # Check input
        if ( len(sys.argv) < 2 ):
            print("usage: cpp2[lang].py config")
            exit(1)

        # Load config data    
        filename = sys.argv[1]
        self.data = utilities.File.read_json(filename)


class Manager:

    def __init__(self, factory):        
        self.factory = factory
        self.config = Config()

    def __translate_package(self, package):
        walker = DirectoryWalker(package, self.factory, self.config)
        walker.process()

    def go(self):
        # Walk through the list of packages
        for package in self.config.data["packages"]:
            self.__translate_package(package)

