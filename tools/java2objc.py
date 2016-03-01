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


class JavaToObjC(translator.BasicTranslator):

    def __init__(self, factory):
        self.factory = factory

    def translate(self, filename_in, filename_out, config, package):
        # Parse input file
        syntax_tree = self.factory.parser.parse_file(str(filename_in))

        for type in syntax_tree.type_declarations:
            if not hasattr(type, "body"):
                continue

            # Interface type
            type.original_name = type.name
            type.name = self.__convert_type(config, type.name, ptr=False)

            # Base class
            type.base = self.__base_class(package, type)

            # Global properties
            type.is_protocol = type.name["name"] in package["protocols"]
            type.is_sync = type.name["name"] in package["sinks"]

            # File name
            filename_out = filename_out.replace(type.original_name, type.name["name"])

            for method in type.body:
                # Argument types
                for parameter in method.parameters:
                    parameter.type = self.__convert_type(config, parameter.type)

                # Return type
                method.return_type = self.__convert_type(config, method.return_type)

            # Generate header file
            self.__generate(self.factory.header_template, syntax_tree, config, filename_out, "h")
            # Generate source file
            if not type.is_protocol:
                self.__generate(self.factory.source_template, syntax_tree, config, filename_out, "mm")

            break

    @staticmethod
    def __generate(template, syntax_tree, config, filename, extension):
        output = template.render({"syntax_tree": syntax_tree, "config": config.data})
        filepath = "{}{}".format(filename, extension)
        utilities.File.write(filepath, output)

    @staticmethod
    def __convert_type(config, type, ptr=True):
        if isinstance(type, plyj.model.Type):
            type = type.name.value
        if type in config.data["types"]:
            return config.data["types"][type]
        if type.startswith("G"):
            interface_name = type[1:]
            return {
                "name": "Gly{}{}".format(interface_name, "*" if ptr else ""),
                "native": False
            }

    @staticmethod
    def __base_class(package, type):
        name = type.name["name"]
        if name in package["hierarchy"]:
            return package["hierarchy"][name]
        else:
            return "GlyCommon"

    def extension(self):
        # Leave extension blank so that translator can generate both .h and .mm files later.
        return ""


class Factory:

    def __init__(self):
        self.parser = plyj.parser.Parser()
        self.jinja_env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
        self.header_template = self.jinja_env.from_string(utilities.File.read_relative("./objc/header.tpl"))
        self.source_template = self.jinja_env.from_string(utilities.File.read_relative("./objc/source.tpl"))

    def translator(self):
        return JavaToObjC(self)


if __name__ == '__main__':
    manager = engine.Manager(Factory())
    manager.go()
