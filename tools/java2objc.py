#!/usr/bin/env python

#------------------------------------------------------------------------------
#
# Copyright (c) 2016 Glympse Inc.  All rights reserved.
#
#------------------------------------------------------------------------------

import jinja2
import plyj.parser
import plyj.model

import utilities
import translator
import engine
import objc.base
import objc.interface
import objc.cls


class JavaToObjC(translator.BasicTranslator):

    def __init__(self, factory):
        self.factory = factory

    def translate(self, filename_in, filename_out, config, package):
        # Parse input file
        syntax_tree = self.factory.parser.parse_file(str(filename_in))
        if not syntax_tree:
            return

        # Find type declaration
        type = objc.base.BaseTranslator.find_type(syntax_tree)
        if not type:
            return

        # Add to the list of detected types
        package["types"].append(type)

        # Pick proper translator
        if isinstance(type, plyj.model.InterfaceDeclaration):
            translator = objc.interface.InterfaceTranslator(self.factory)
        elif isinstance(type, plyj.model.ClassDeclaration):
            translator = objc.cls.ClassTranslator(self.factory)
        else:
            return

        # Perform translation and generate output file(s)
        translator.translate(config, package, type, filename_out)

    def extension(self):
        # Leave extension blank so that translator can generate both .h and .mm files later.
        return ""


class Factory(translator.BasicFactory):

    def __init__(self):
        self.parser = plyj.parser.Parser()

        self.interface_env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            loader=jinja2.FileSystemLoader("{}/objc/interface".format(utilities.File.local_path())))
        self.interface_header_template = self.interface_env.get_template("header.tpl")
        self.interface_source_template = self.interface_env.get_template("source.tpl")
        self.interface_package_template = self.interface_env.get_template("package.tpl")

        self.class_env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            loader=jinja2.FileSystemLoader("{}/objc/class".format(utilities.File.local_path())))
        self.class_header_template = self.class_env.get_template("header.tpl")
        self.class_source_template = self.class_env.get_template("source.tpl")

    def begin_package(self, config, package):
        package["types"] = []

    def package_completed(self, config, package):
        output = self.interface_package_template.render({"package": package, "config": config.data})
        filepath = "{}/{}.h".format(package["dst"], package["name"])
        utilities.File.write(filepath, output)

    def translator(self):
        return JavaToObjC(self)


if __name__ == '__main__':
    manager = engine.Manager(Factory())
    manager.go()
