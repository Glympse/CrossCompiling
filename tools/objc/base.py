#------------------------------------------------------------------------------
#
# Copyright (c) 2016 Glympse Inc.  All rights reserved.
#
#------------------------------------------------------------------------------

import utilities


class MethodGroup(object):

    def __init__(self):
        self.overrides = []


class BaseTranslator(object):

    def __init__(self, factory):
        self.factory = factory

    @staticmethod
    def find_type(syntax_tree):
        for type in syntax_tree.type_declarations:
            if not hasattr(type, "body"):
                continue
            return type

    @staticmethod
    def generate(template, config, package, type, filename, extension):
        output = template.render({"type": type, "config": config.data, "package": package})
        filepath = "{}{}".format(filename, extension)
        utilities.File.write(filepath, output)

    @staticmethod
    def convert_types(config, package, type):
        type.method_index = {}
        for item in type.body:
            if hasattr(item, "type"):
                item.type = BaseTranslator.convert_type(config, package, item.type)
            elif hasattr(item, "return_type"):
                # Group methods by name
                if not item.name in type.method_index:
                    type.method_index[item.name] = MethodGroup()
                type.method_index[item.name].overrides.append(item)

                # Parameter types
                invalid_params = []
                for parameter in item.parameters:
                    parameter.type = BaseTranslator.convert_type(config, package, parameter.type)
                    if not parameter.type:
                        invalid_params.append(parameter)
                for parameter in invalid_params:
                    item.parameters.remove(parameter)

                # Return type
                item.return_type = BaseTranslator.convert_type(config, package, item.return_type)

        # Mark methods as overridden if they are
        for method_name in type.method_index:
            method_group = type.method_index[method_name]
            for method in method_group.overrides:
                method.is_overridden = len(method_group.overrides) > 1

    @staticmethod
    def convert_type(config, package, type):
        if hasattr(type, "name"):
            type = type.name.value
        if type in config.data["types"]:
            return config.data["types"][type]
        if type.startswith("G"):
            interface_name = type[1:]
            objc_type_name = "Gly{}".format(interface_name)
            if objc_type_name in config.data["undefined"]:
                return {
                    "objc_name": "GlyCommon",
                    "objc_type": "GlyCommon*",
                    "objc_arg_name": objc_type_name,
                    "cpp_type": "Glympse::GCommon",
                    "cpp_arg_type": "const Glympse::GCommon&",
                    "native": False
                }
            elif objc_type_name in config.data["protocols"]:
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
