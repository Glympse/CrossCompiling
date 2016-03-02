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


class MethodGroup(object):

    def __init__(self):
        self.overrides = []


class JavaToObjC(translator.BasicTranslator):

    def __init__(self, factory):
        self.factory = factory

    def translate(self, filename_in, filename_out, config, package):
        # Load global type
        type = self.__load_type(config, package, filename_in)

        # Add to the list of detected types
        package["types"].append(type)

        # Global properties
        type.is_protocol = type.name["objc_name"] in config.data["protocols"]
        type.is_sink = type.name["objc_name"] in package["sinks"]
        type.has_private = type.name["objc_name"] in package["private"]

        # File name
        filename_out = filename_out.replace(type.original_name, type.name["objc_name"])

        # Generate header file
        self.__generate(self.factory.header_template, type, config, package, filename_out, "h")
        # Generate source file
        if not type.is_protocol:
            self.__generate(self.factory.source_template, type, config, package, filename_out, "mm")

    def __load_type(self, config, package, filepath):
        # Parse input file
        syntax_tree = self.factory.parser.parse_file(str(filepath))

        for type in syntax_tree.type_declarations:
            if not hasattr(type, "body"):
                continue

            # Interface type
            type.original_name = type.name
            type.name = self.__convert_type(config, package, type.name)

            type.method_index = {}
            for method in type.body:
                # Group methods by name
                if not method.name in type.method_index:
                    type.method_index[method.name] = MethodGroup()
                type.method_index[method.name].overrides.append(method)

                # Argument types
                for parameter in method.parameters:
                    parameter.type = self.__convert_type(config, package, parameter.type)

                # Return type
                method.return_type = self.__convert_type(config, package, method.return_type)

            # Mark methods as overridden if they are
            for method_name in type.method_index:
                method_group = type.method_index[method_name]
                for method in method_group.overrides:
                    method.is_overridden = len(method_group.overrides) > 1

            return type

    @staticmethod
    def __generate(template, type, config, package, filename, extension):
        output = template.render({"type": type, "config": config.data, "package": package})
        filepath = "{}{}".format(filename, extension)
        utilities.File.write(filepath, output)

    @staticmethod
    def __convert_type(config, package, type):
        if isinstance(type, plyj.model.Type):
            type = type.name.value
        if type in config.data["types"]:
            return config.data["types"][type]
        if type.startswith("G"):
            interface_name = type[1:]
            objc_type_name = "Gly{}".format(interface_name)
            is_protocol = objc_type_name in config.data["protocols"]
            if is_protocol:
                return {
                    "objc_name": objc_type_name,
                    "objc_type": "id<{}>".format(objc_type_name),
                    "objc_arg_name": objc_type_name,
                    "cpp_type": "Glympse::{}".format(type),
                    "cpp_arg_type": "const Glympse::{}&".format(type),
                    "native": False
                }
            else:
                return {
                    "objc_name": objc_type_name,
                    "objc_type": "{}*".format(objc_type_name),
                    "objc_arg_name": objc_type_name,
                    "cpp_type": "Glympse::{}".format(type),
                    "cpp_arg_type": "const Glympse::{}&".format(type),
                    "native": False
                }

    @staticmethod
    def __base_class(package, type):
        name = type.name["objc_type"]
        if name in package["hierarchy"]:
            return package["hierarchy"][name]
        else:
            return "GlyCommon"

    def extension(self):
        # Leave extension blank so that translator can generate both .h and .mm files later.
        return ""


class Factory(translator.BasicFactory):

    def __init__(self):
        self.parser = plyj.parser.Parser()
        self.jinja_env = jinja2.Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            loader=jinja2.FileSystemLoader("{}/objc".format(utilities.File.local_path())))
        self.header_template = self.jinja_env.get_template("header.tpl")
        self.source_template = self.jinja_env.get_template("source.tpl")
        self.package_template = self.jinja_env.get_template("package.tpl")

    def translator(self):
        return JavaToObjC(self)

    def begin_package(self, config, package):
        package["types"] = []

    def package_completed(self, config, package):
        output = self.package_template.render({"package": package, "config": config.data})
        filepath = "{}/{}.h".format(package["dst"], package["name"])
        utilities.File.write(filepath, output)

if __name__ == '__main__':
    manager = engine.Manager(Factory())
    manager.go()
