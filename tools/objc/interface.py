#------------------------------------------------------------------------------
#
# Copyright (c) 2016 Glympse Inc.  All rights reserved.
#
#------------------------------------------------------------------------------

from . import base


class InterfaceTranslator(base.BaseTranslator):

    def translate(self, config, package, type, filename_out):
        # Post process interface declaration
        self.__process_type(config, package, type)

        # Type properties
        type.is_protocol = type.name["objc_name"] in config.data["protocols"]
        type.base_class, type.protocols = InterfaceTranslator.__find_class_hierarchy(config, package, type)
        type.is_sink = config.data["params"]["sink"]["source"] in type.protocols
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

        # Method parameter and return types
        base.BaseTranslator.convert_types(config, package, type)

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
    def __find_class_hierarchy(config, package, type):
        base = "GlyCommon"
        name = type.name["objc_name"]
        info = package["types_info"]
        protocols = config.data["protocols"]

        if not name in info:
            return base, []

        type = info[name]
        if not type.extends:
            return base, []

        first = type.extends[0]["objc_name"]
        if first not in protocols:
            base = first
        interfaces = [ x["objc_name"] for x in type.extends if x["objc_name"] in protocols ]

        return base, interfaces
