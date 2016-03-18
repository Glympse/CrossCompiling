#!/usr/bin/env python

#------------------------------------------------------------------------------
#
# Copyright (c) 2016 Glympse Inc.  All rights reserved.
#
#------------------------------------------------------------------------------

import sys
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

        # Transform and gather information on generated types for later transforms.
        type.extends = objc.base.BaseTranslator.convert_extends(config, package, type)
        type_info = objc.base.BaseTranslator.convert_type(config, package, type.name)
        if type_info is not None:
            package["types_info"][type_info["objc_name"]] = type

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

        # We want to gather type info through all our generated
        # packages; so initialize here and accumulate during
        # translation.
        self.types_info = {}

    def begin_package(self, config, package):
        package["types"] = []
        package["types_info"] = self.types_info

    def package_completed(self, config, package):
        package["types"] = Factory.dependency_sort(package)
        output = self.interface_package_template.render({"package": package, "config": config.data})
        filepath = "{}/{}.h".format(package["dst"], package["name"])
        utilities.File.write(filepath, output)

    def translator(self):
        return JavaToObjC(self)

    @staticmethod
    def dependency_sort(package):
        types = package["types"]
        info = package["types_info"]
        sorted = []

        last_length = sys.maxint
        while len(types) < last_length and 0 < len(types):
            last_length = len(types)
            next_types = list(types)
            for type in types:
                satisfied = True
                for dependency in type.extends:
                    name = dependency["objc_name"]
                    if name in info:
                        # We only care about types that are imported as
                        # part of the same package. If the dependency is
                        # being satisfied in another way, then it is not
                        # relevant to this sort. So we simply check if
                        # there is a dependency still in the type list.
                        if info[name] in types:
                            satisfied = False
                            break
                if satisfied:
                    sorted.append(type)
                    next_types.remove(type)
            types = next_types

        if 0 != len(types):
            raise Exception('Unable to satisfy dependencies: ', types)
        return sorted

if __name__ == '__main__':
    manager = engine.Manager(Factory())
    manager.go()
