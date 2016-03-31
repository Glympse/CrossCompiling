#------------------------------------------------------------------------------
#
# Copyright (c) 2016 Glympse Inc.  All rights reserved.
#
#------------------------------------------------------------------------------

import base


class ClassTranslator(base.BaseTranslator):

    def translate(self, config, package, type, filename_out):
        # Post process interface declaration
        self.__process_type(config, package, type)

        # File name
        filename_out = filename_out.replace(type.name["java_name"], type.name["objc_name"])

        # Generate header file
        self.generate(
            self.factory.class_header_template, config, package, type, filename_out, "h")
        # Generate source file
        self.generate(
            self.factory.class_source_template, config, package, type, filename_out, "mm")

    def __process_type(self, config, package, type):
        # Format new type name
        cpp_namespace = config.data["params"]["cpp_namespace"]
        objc_name = "Gly{}".format(type.name)
        type.name = {
            "java_name": type.name,
            "cpp_type": "{}::{}".format(cpp_namespace, type.name),
            "objc_name": objc_name
        }

        # Method parameter and return types
        base.BaseTranslator.convert_types(config, package, type)
