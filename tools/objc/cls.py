#------------------------------------------------------------------------------
#
# Copyright (c) 2016 Glympse Inc.  All rights reserved.
#
#------------------------------------------------------------------------------

import base


class ClassTranslator(base.BaseTranslator):

    def translate(self, config, package, type, filename_out):
        # Post process interface declation
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
        objc_name = "Gly{}".format(type.name)
        type.name = {
            "java_name": type.name,
            "objc_name": objc_name
        }

        # Update types
        for item in type.body:
            if hasattr(item, "type"):
                item.type = self.convert_type(config, package, item.type)
            elif hasattr(item, "return_type"):
                item.return_type = self.convert_type(config, package, item.return_type)
