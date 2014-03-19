#!/usr/bin/env python 

#------------------------------------------------------------------------------
#
# Copyright (c) 2014 Glympse Inc.  All rights reserved.
#
#------------------------------------------------------------------------------

import os, re, codecs
import translator, engine

class CppToJava(translator.BasicTranslator):
    
    def __init__(self):
    
        # Initialize regular expressions, so it is globally available
        self.reg_o_wrapper = re.compile(r'O< [\s]* ( [^>]* ) [\s]* >\s', re.VERBOSE)        
        self.reg_o_no_sp_wrapper = re.compile(r'O< [\s]* ( [^>]* ) [\s]* >', re.VERBOSE)        
        self.reg_colon_common = re.compile(r':\spublic\sCommon<\s ( [^>]* ) >', re.VERBOSE)        
        self.reg_comma_common = re.compile(r',\spublic\sCommon<\s ( [^>]* ) >', re.VERBOSE)        
        self.reg_const_amp_arg = re.compile(r'const\s ( [^&]* ) \&', re.VERBOSE)            
        self.reg_interface_name = re.compile(r'([\s.])I([A-Z][a-z][A-Za-z]*)', re.VERBOSE)    
        self.reg_file_name = re.compile(r'I([A-Z][a-z][A-Za-z]*)', re.VERBOSE)    
        # RegEx. Templates        
        self.reg_template_1arg = re.compile(r'template<[\s]*class\s([A-Z_]*)[\s]*>\s(interface|class|struct)\s([A-Za-z]*)', re.VERBOSE)  
        self.reg_template_2args = re.compile(r'template<[\s]*class\s([A-Z_]*)[\s]*,[\s]*class[\s]*([A-Z_]*)[\s]*>\s(interface|class|struct)\s([A-Za-z]*)', re.VERBOSE)    
        # RegEx. Numbers        
        self.reg_ll = re.compile(r'( [0-9] )LL', re.VERBOSE) 
        # RegEx. Arrays
        self.reg_array_decl = re.compile(r'\s (?!return)([A-Za-z0-9_]+) \s ([A-Za-z0-9_]+) \[ ([A-Za-z0-9_:.]+) \];', re.VERBOSE)
        self.reg_bytebuffer_decl = re.compile(r'ByteArray \s ([A-Za-z0-9_]+) \( ([A-Za-z0-9_:.]+) \);', re.VERBOSE)        
        self.reg_bytebuffer_assgn = re.compile(r'\s = \s ByteArray \( ([A-Za-z0-9_:.]+) \);', re.VERBOSE)        

        # Initialize translator's state
        self.imports_added = False
        self.namespaces_found = 0
        self.multiline_comment = False
        self.remove_lines_count = 0             

    def processFragment(self, src_line):    
        
        # Basic types
        src_line = src_line.replace("int32", "int")
        src_line = src_line.replace("int64", "long")
        src_line = src_line.replace(" bool ", " boolean ")
        src_line = src_line.replace("(bool ", "(boolean ")
        src_line = src_line.replace("(bool)", "(boolean)")           
        # Buffer types
        src_line = src_line.replace("const char*", "String")
        src_line = src_line.replace("char*", "String")
        src_line = src_line.replace("CharBuffer ", "char[] ")
        src_line = src_line.replace("(CharBuffer)", "(char[])")
        src_line = src_line.replace("ByteBuffer ", "byte[] ")
        src_line = src_line.replace("(ByteBuffer)", "(byte[])")
        src_line = src_line.replace("SmartBuffer ", "byte[] ")               
        src_line = src_line.replace("ErrorMessage", "String") 
        src_line = src_line.replace("unichar", "char")
        src_line = src_line.replace("CharArray ", "char[] ")
        src_line = src_line.replace(".arrayLength()", ".length")
        # Constants
        src_line = src_line.replace("(NULL", "(null")
        src_line = src_line.replace(" NULL", " null")
        # Smart pointers support
        src_line = src_line.replace("::ptr", "")        
        # Templates support
        src_line = src_line.replace("typename ", "")   
        src_line = self.reg_template_1arg.sub(r'\2 \3<\1>', src_line)
        src_line = self.reg_template_2args.sub(r'\3 \4<\1,\2>', src_line)                

        src_line = src_line.replace("struct ", "interface ")
        src_line = src_line.replace("public:", "public")        
        src_line = src_line.replace("private:", "private")
        src_line = src_line.replace("protected:", "protected")
        src_line = src_line.replace(" inline ", " ")                  
        src_line = src_line.replace("virtual ", "")
        src_line = src_line.replace(") = 0;", ");")        
        src_line = src_line.replace("::", ".")
        src_line = src_line.replace("->", ".")                
            
        src_line = self.reg_o_wrapper.sub(r'\1 ', src_line)
        src_line = self.reg_o_no_sp_wrapper.sub(r'\1', src_line)
        src_line = self.reg_colon_common.sub(r'implements \1', src_line)
        src_line = self.reg_comma_common.sub(r' implements \1', src_line)
        src_line = self.reg_const_amp_arg.sub(r'\1', src_line)
        src_line = self.reg_interface_name.sub(r'\1G\2', src_line)
        src_line = self.reg_ll.sub(r'\1L', src_line)
        src_line = self.reg_array_decl.sub(r' \1[] \2 = new \1[\3];', src_line)
        src_line = self.reg_bytebuffer_decl.sub(r'byte[] \1 = new byte[\2];', src_line)   
        src_line = self.reg_bytebuffer_assgn.sub(r' = new byte[\1];', src_line)

        # Replace second "implements" keyword with comma (","). 
        if ( -1 != src_line.find("class ") ):
            src_line = src_line.replace(" implements ", "##IMPLEMENTS##")
            src_line = src_line.replace("##IMPLEMENTS##", " implements ", 1)
            src_line = src_line.replace("##IMPLEMENTS##", ", ")
        
        if ( 0 == src_line.find("#ifndef") ):
            src_line = 'package ' + self.package + ';' + os.linesep
        if ( 0 == src_line.find("#") ):
            return None      
        if ( 0 == src_line.find("namespace") ):
            self.namespaces_found = self.namespaces_found + 1
            self.remove_lines_count = 1            
            if ( not self.imports_added ):
                src_line = self.format_imports()
                self.imports_added = True  
            else:
                return None
        
        # Post RegEx replacements         
        src_line = src_line.replace(" : public ", " extends ")
        src_line = src_line.replace(", public ", ", ")                          
        src_line = src_line.replace(" const ", " final ")
        if ( src_line.endswith("const") ):
            src_line = src_line.replace(" const", " final")    
        src_line = src_line.replace("GCommonObj", "Object")   
        src_line = src_line.replace("Object.fromThis(this)", "this")
        src_line = src_line.replace("GLong", "Long")        
        src_line = src_line.replace("GString", "String")
        src_line = src_line.replace("GThread", "Thread")
        src_line = src_line.replace("GRunnable", "Runnable")                    
        src_line = src_line.replace("StaticString", "String")                    
        src_line = src_line.replace("OwnString", "String")                    
        src_line = src_line.replace("GHashtable", "Hashtable") 
        src_line = src_line.replace("GEnumeration", "Enumeration") 
        src_line = src_line.replace("GComparator", "Comparator")       
        # Containers
        src_line = src_line.replace("new Vector", "new GVector")                 
        src_line = src_line.replace("new LinkedList", "new GLinkedList")                  
        # Exception handling
        src_line = src_line.replace("GThrowable", "Throwable")        
        src_line = src_line.replace("Debug.ex(true);", "Debug.ex(e, true);")
        src_line = src_line.replace("Debug.ex(false);", "Debug.ex(e, false);")    
        src_line = src_line.replace("catch ( ... )", "catch ( Exception e )")
        # Arrays
        src_line = src_line.replace("ByteArray ", "byte[] ")                        

        return src_line

    def format_imports(self):
        imports = ""
        for dependency in self.config.data["dependencies"]:
            imports += "import {0};{1}".format(dependency, os.linesep)
        return imports
    
    def translate(self, filename_in, filename_out, config):
        self.filename_in = filename_in
        self.filename_out = filename_out        
        self.config = config
        
        # Java. Format package name
        self.package = self.filename_out[self.filename_out.find('com'):self.filename_out.rfind('/')]
        self.package = self.package.replace('/', '.')
        
        # Java/C#. Update output file name
        self.filename_out = self.reg_file_name.sub(r'G\1', self.filename_out)

        # Verify existence of destination directory
        dst_dir = os.path.dirname(self.filename_out)
        if ( False == os.path.exists(dst_dir) ):
            os.makedirs(dst_dir)

        # Open files
        src_file = codecs.open(self.filename_in, 'r', encoding='utf-8')
        dst_file = codecs.open(self.filename_out, 'w', encoding='utf-8')
               
        # Perform the translation
        self.dst_file_contents = ""   
        for src_line in src_file:            

            if ( 0 != self.remove_lines_count ):
                self.remove_lines_count = self.remove_lines_count - 1
                continue            

            self.processLine(src_line)
                    
        # Hide C++/C# statements
        self.dst_file_contents = self.unwrap(self.dst_file_contents, '/*C*/', '/**/', '/*C*', '**/', True)
        self.dst_file_contents = self.unwrap(self.dst_file_contents, '/*S*/', '/**/', '/*S*', '**/', True)
        self.dst_file_contents = self.unwrap(self.dst_file_contents, '/*Z*/', '/**/', '/*Z*', '**/', True)
        # Show Java statements
        self.dst_file_contents = self.unwrap(self.dst_file_contents, '/*J*', '**/', '/*J*/', '/**/', False)
        self.dst_file_contents = self.unwrap(self.dst_file_contents, '/*O*', '**/', '/*O*/', '/**/', False)
        self.dst_file_contents = self.unwrap(self.dst_file_contents, '/*X*', '**/', '/*X*/', '/**/', False)    

        # Remove trailing curly brackets left by namespace statements
        while ( self.namespaces_found > 0 ):
            bracket_pos = self.dst_file_contents.rfind('}')
            self.dst_file_contents = self.dst_file_contents[0:bracket_pos] + self.dst_file_contents[bracket_pos + 1:len(self.dst_file_contents)]
            self.namespaces_found = self.namespaces_found - 1
                
        # Save result to destination file
        dst_file.write(self.dst_file_contents)
        
        # Close files
        dst_file.close()
        src_file.close()

    def extension(self):
        return "java"

class CppFactory:
    def translator(self):
        return CppToJava()

manager = engine.Manager(CppFactory())
manager.go()

