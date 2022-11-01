#------------------------------------------------------------------------------
#
# Copyright (c) 2016 Glympse Inc.  All rights reserved.
#
#------------------------------------------------------------------------------

import sys

import plyj.model

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
        invalid_methods = []
        method_index = {}
        for item in type.body:
            if hasattr(item, "type"):
                item.type = BaseTranslator.convert_type(config, package, item.type)
            elif hasattr(item, "return_type"):
                # Group methods by name
                if not item.name in method_index:
                    method_index[item.name] = MethodGroup()
                method_index[item.name].overrides.append(item)

                # Parameter types
                invalid_params = []
                for parameter in item.parameters:
                    parameter.type = BaseTranslator.convert_type(config, package, parameter.type)
                    if not parameter.type:
                        invalid_params.append(parameter)

                # Remove parameters of unknown types
                for parameter in invalid_params:
                    item.parameters.remove(parameter)

                # Return type
                item.return_type = BaseTranslator.convert_type(config, package, item.return_type)
                if not item.return_type:
                    invalid_methods.append(item)
            else:
                invalid_methods.append(item)

        # Remove methods marked invalid
        for method in invalid_methods:
            type.body.remove(method)

        # Mark methods as overridden if they are
        for method_name in method_index:
            method_group = method_index[method_name]
            for method in method_group.overrides:
                method.is_overridden = len(method_group.overrides) > 1

    @staticmethod
    def convert_type(config, package, type):
        type_info = type
        if hasattr(type, "name"):
            type = type.name.value
        if type in config.data["types"]:
            return config.data["types"][type]
        if type.startswith("G"):
            cpp_namespace = config.data["params"]["cpp_namespace"]
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
                    "cpp_type": "{}::{}".format(cpp_namespace, type),
                    "cpp_arg_type": "const {}::{}&".format(cpp_namespace, type),
                    "native": False
                }
            else:
                specializations = []
                if objc_type_name in config.data["generics"]:
                    for generic_type in type_info.type_arguments:
                        spec_type = BaseTranslator.convert_type(config, package, generic_type)
                        specializations.append(spec_type["objc_type"])

                if 0 < len(specializations):
                    objc_type = "{}<{}>*".format(objc_type_name, ",".join(specializations))
                else:
                    objc_type = "{}*".format(objc_type_name)

                return {
                    "objc_name": objc_type_name,
                    "objc_type": objc_type,
                    "objc_arg_name": objc_type_name,
                    "cpp_type": "{}::{}".format(cpp_namespace, type),
                    "cpp_holder_type": "Glympse::Holder<{}::I{}>".format(cpp_namespace, interface_name),
                    "cpp_holder_private_type": "Glympse::Holder<{}::I{}Private>".format(cpp_namespace, interface_name),
                    "cpp_arg_type": "const Glympse::{}&".format(type),
                    "native": False
                }

    @staticmethod
    def convert_extends(config, package, type):
        converted = []
        extends = type.extends
        if isinstance(extends, list):
            for extend in extends:
                converted.append(BaseTranslator.convert_type(config, package, extend))
        elif isinstance(extends, plyj.model.Type):
            converted.append(BaseTranslator.convert_type(config, package, extends))
        return converted

    @staticmethod
    def dependency_sort(package):
        types = package["types"]
        info = package["types_info"]
        sorted = []

        last_length = sys.maxsize
        while len(types) < last_length and 0 < len(types):
            last_length = len(types)
            next_types = list(types)
            for type in types:
                satisfied = True
                for dependency in type.extends:
                    if not dependency:
                        continue
                    name = dependency["objc_name"]
                    if name in info:
                        # We only care about types that are imported as part of the same package. If the dependency is
                        # being satisfied in another way, then it is not relevant to this sort. So we simply check if
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
