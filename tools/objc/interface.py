#------------------------------------------------------------------------------
#
# Copyright (c) 2016 Glympse Inc.  All rights reserved.
#
#------------------------------------------------------------------------------

import base


class MethodGroup(object):

    def __init__(self):
        self.overrides = []


class InterfaceTranslator(base.BaseTranslator):

    def translate(self, config, package, type, filename_out):
        # Post process interface declation
        self.__process_type(config, package, type)

        # Type properties
        type.is_protocol = type.name["objc_name"] in config.data["protocols"]
        type.is_sink = type.name["objc_name"] in package["sinks"]
        type.has_private = type.name["objc_name"] in package["private"]

        # Interfaces
        self.__load_interfaces(config, package, type)

        # File name
        filename_out = filename_out.replace(type.original_name, type.name["objc_name"])

        # Generate header file
        self.generate(self.factory.interface_header_template, config, package, type, filename_out, "h")
        # Generate source file
        if not type.is_protocol:
            self.generate(self.factory.interface_source_template, config, package, type, filename_out, "mm")

    def __load_type(self, config, package, filepath):
        # Parse input file
        syntax_tree = self.factory.parser.parse_file(str(filepath))

        # Find type declaration
        type = self.find_type(syntax_tree)

        # Post process interface declation
        self.__process_type(config, package, type)

        return type

    def __process_type(self, config, package, type):
        # Interface type
        type.original_name = type.name
        type.name = self.convert_type(config, package, type.name)

        type.method_index = {}
        for method in type.body:
            # Group methods by name
            if not method.name in type.method_index:
                type.method_index[method.name] = MethodGroup()
            type.method_index[method.name].overrides.append(method)

            # Argument types
            for parameter in method.parameters:
                parameter.type = self.convert_type(config, package, parameter.type)

            # Return type
            method.return_type = self.convert_type(config, package, method.return_type)

        # Mark methods as overridden if they are
        for method_name in type.method_index:
            method_group = type.method_index[method_name]
            for method in method_group.overrides:
                method.is_overridden = len(method_group.overrides) > 1

    def __load_interfaces(self, config, package, type):
        type.interfaces = []
        if not type.name["objc_name"] in package["hierarchy"]:
            return
        type_hierarchy = package["hierarchy"][type.name["objc_name"]]
        if not "interfaces" in type_hierarchy:
            return
        for interface in type_hierarchy["interfaces"]:
            filepath = "{}/{}".format(package["src"], interface["source"])
            interface_type = self.__load_type(config, package, filepath)
            type.interfaces.append(interface_type)

    @staticmethod
    def __base_class(package, type):
        name = type.name["objc_type"]
        if name in package["hierarchy"]:
            return package["hierarchy"][name]
        else:
            return "GlyCommon"
