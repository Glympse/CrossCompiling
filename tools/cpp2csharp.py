#!/usr/bin/env python 

#------------------------------------------------------------------------------
#
# Copyright (c) 2014 Glympse Inc.  All rights reserved.
#
#------------------------------------------------------------------------------

import os, re, codecs
import translator, engine

class CppToCSharp(translator.BasicTranslator):
    
    def __init__(self):

        # Initialize regular expressions, so it is globally available
        self.reg_o_wrapper = re.compile(r'O< [\s]* ( [^>]* ) [\s]* >\s', re.VERBOSE)
        self.reg_o_no_sp_wrapper = re.compile(r'O< [\s]* ( [^>]* ) [\s]* >', re.VERBOSE)        
        self.reg_colon_common = re.compile(r':\spublic\sCommon<\s ( [^>]* ) >', re.VERBOSE)        
        self.reg_comma_common = re.compile(r',\spublic\sCommon<\s ( [^>]* ) >', re.VERBOSE)
        self.reg_const_amp_arg = re.compile(r'const\s ( [^&]* ) \&', re.VERBOSE)        
        self.reg_interface_name = re.compile(r'([\s.])I([A-Z][a-z][A-Za-z]*)', re.VERBOSE)            
        self.reg_file_name = re.compile(r'I([A-Z][a-z][A-Za-z]*)', re.VERBOSE)    
        # RegEx. Vector
        self.reg_element_at = re.compile(r'.elementAt\( ( [^)]* ) \)', re.VERBOSE)
        self.reg_insert_element_at = re.compile(r'.insertElementAt\( ( [^,]* ),\s( [^)]* ) \)', re.VERBOSE)
        self.reg_set_element_at = re.compile(r'.setElementAt\( ( [^,]* ),\s( [^)]* ) \)', re.VERBOSE)
        # RegEx. For-each
        self.reg_for_each = re.compile(r'for \s \( \s ([_a-zA-Z\s<>:.-]*) \s : \s ([_a-zA-Z\s()<>:.-]*) \s \)', re.VERBOSE)
        # RegEx. Templates
        self.reg_template_1arg = re.compile(r'template<[\s]*class\s([A-Z_]*)[\s]*>\s(interface|class|struct)\s([A-Za-z]*)', re.VERBOSE)  
        self.reg_template_2args = re.compile(r'template<[\s]*class\s([A-Z_]*)[\s]*,[\s]*class[\s]*([A-Z_]*)[\s]*>\s(interface|class|struct)\s([A-Za-z]*)', re.VERBOSE)      
        # RegEx. Numbers
        self.reg_ll = re.compile(r'( [0-9] )LL', re.VERBOSE)        
        # RegEx. Arrays
        self.reg_array_decl = re.compile(r'\s (?!return)([A-Za-z0-9_]+) \s ([A-Za-z0-9_]+) \[ ([A-Za-z0-9_:.]+) \];', re.VERBOSE)
        self.reg_bytebuffer_decl = re.compile(r'ByteArray \s ([A-Za-z0-9_]+) \( ([A-Za-z0-9_:.]+) \);', re.VERBOSE)                
        self.reg_bytebuffer_assgn = re.compile(r'\s = \s ByteArray \( ([A-Za-z0-9_:.]+) \);', re.VERBOSE)                
        self.reg_bytebuffer_length = re.compile(r'\.length([^\w\(])', re.VERBOSE) 
        # RegEx. Math
        self.reg_math = re.compile(r'\bMath\.([a-z])', re.VERBOSE)

        # Initialize translator's state
        self.multiline_comment = False
        self.remove_lines_count = 0
        self.interface_found = False
    
    def processFragment(self, src_line):   
        # Basic types
        src_line = src_line.replace("int32", "int")
        src_line = src_line.replace("int64", "long")
        # Buffer types
        src_line = src_line.replace("const char*", "String")
        src_line = src_line.replace("char*", "String")
        src_line = src_line.replace("CharBuffer ", "char[] ")
        src_line = src_line.replace("(CharBuffer)", "(char[])")
        src_line = src_line.replace("ByteBuffer ", "byte[] ")                                        
        src_line = src_line.replace("SmartBuffer ", "byte[] ")
        src_line = src_line.replace(".length,", ".Length,") 
        src_line = src_line.replace("unichar", "char")
        src_line = src_line.replace("CharArray ", "char[] ")
        src_line = src_line.replace(".arrayLength()", ".Length")
        # Constants
        src_line = src_line.replace("(NULL", "(null")
        src_line = src_line.replace(" NULL", " null")
        # Smart pointers support
        src_line = src_line.replace("::ptr", "")
        # Templates support
        src_line = src_line.replace("typename ", "")  
        src_line = self.reg_template_1arg.sub(r'\2 \3<\1>', src_line)                
        src_line = self.reg_template_2args.sub(r'\3 \4<\1,\2>', src_line)                        

        if ( self.interface_found ):
            src_line = src_line.replace("public:", "")
            src_line = src_line.replace("private:", "")
            src_line = src_line.replace("protected:", "")
        else:
            src_line = src_line.replace("public:", "public")
            src_line = src_line.replace("private:", "private")
            src_line = src_line.replace("protected:", "protected")                
        if ( -1 != src_line.find("struct I") and -1 == src_line.find(";") ):
            self.interface_found = True
        if ( -1 != src_line.find("};") ):
            self.interface_found = False
        src_line = src_line.replace("struct ", "interface ")            
        src_line = src_line.replace(" inline ", " ")                  
        src_line = src_line.replace("::", ".")
        src_line = src_line.replace("->", ".")
        src_line = src_line.replace("ErrorMessage", "String")

        src_line = self.reg_o_wrapper.sub(r'\1 ', src_line)
        src_line = self.reg_o_no_sp_wrapper.sub(r'\1', src_line)
        src_line = self.reg_colon_common.sub(r': \1', src_line)
        src_line = self.reg_comma_common.sub(r' : \1', src_line)
        src_line = self.reg_const_amp_arg.sub(r'\1', src_line)
        src_line = self.reg_interface_name.sub(r'\1G\2', src_line)        
        src_line = self.reg_for_each.sub(r'foreach ( \1 in \2 )', src_line)
        src_line = self.reg_ll.sub(r'\1L', src_line)
        src_line = self.reg_array_decl.sub(r' \1[] \2 = new \1[\3];', src_line)
        src_line = self.reg_bytebuffer_decl.sub(r'byte[] \1 = new byte[\2];', src_line)                
        src_line = self.reg_bytebuffer_assgn.sub(r' = new byte[\1];', src_line)
        src_line = self.reg_bytebuffer_length.sub(r'.Length\1', src_line)

        # Uppercase first letter of Math functions
        src_line = self.reg_math.sub(lambda pattrn: 'Math.' + pattrn.group(1).upper(), src_line) 

        if ( -1 != src_line.find(") = 0;") ):
            src_line = src_line.replace(") = 0;", ");")   
            src_line = src_line.replace("public ", "public abstract ")   

        if ( self.interface_found or self.override_found_this_line ):
            src_line = src_line.replace(" virtual ", " ")

        if ( 0 == src_line.find("#ifndef") ):
            src_line = self.format_imports()
        if ( 0 == src_line.find("#") ):
            return None     
        # Replace tabs with 4 spaces
        src_line = src_line.expandtabs(4)
        # Post RegEx replacements         
        src_line = src_line.replace(" : public ", " : ")
        src_line = src_line.replace(", public ", ", ")
        src_line = src_line.replace("GThread", "Thread")
        src_line = src_line.replace("GCommonObj", "Object")
        src_line = src_line.replace("new Hashtable", "new GHashtable")
        src_line = src_line.replace(" static const ", " const ")
        src_line = src_line.replace("Object.fromThis(this)", "this")
        # Containers
        src_line = src_line.replace("new Vector", "new GVector")                 
        src_line = src_line.replace("new LinkedList", "new GLinkedList")   
        # Arrays
        src_line = src_line.replace("ByteArray ", "byte[] ")                 
        # Process class statement
        if ( 0 == src_line.find("class ") ):
            src_line = src_line.replace(":", ",")
            src_line = src_line.replace(" , ", " : ", 1)

        # C# classes and method names
        # Object
        src_line = src_line.replace("hashCode(", "GetHashCode(")
        src_line = src_line.replace("equals(", "Equals(")        
        # String
        src_line = src_line.replace("GString", "String")
        src_line = src_line.replace("StaticString", "String")                    
        src_line = src_line.replace("OwnString", "String")
        src_line = src_line.replace(".trim()", ".Trim()")
        src_line = src_line.replace(".compareTo(", ".CompareTo(")
        src_line = src_line.replace(".toCharArray(", ".ToCharArray(")
        src_line = src_line.replace(".indexOf(", ".IndexOf(")
        src_line = src_line.replace(".lastIndexOf(", ".LastIndexOf(")
        src_line = src_line.replace(".startsWith(", ".StartsWith(")
        src_line = src_line.replace(".endsWith(", ".EndsWith(")
        src_line = src_line.replace(".toLowerCase(", ".ToLower(")
        src_line = src_line.replace(".replace(", ".Replace(")
        # StringBuilder
        src_line = src_line.replace(".append(", ".Append(")
        src_line = src_line.replace(" append(", " Append(")
        src_line = src_line.replace(".insert(", ".Insert(")
        # Vector
        src_line = src_line.replace(".contains(", ".Contains(")
        src_line = src_line.replace(".addElement(", ".Add(")
        src_line = src_line.replace(".removeElement(", ".Remove(")
        src_line = src_line.replace(".removeElementAt(", ".RemoveAt(")
        src_line = src_line.replace(".removeAllElements(", ".Clear(")
        src_line = src_line.replace(".sort(", ".Sort(")
        src_line = self.reg_element_at.sub(r'[\1]', src_line)
        src_line = self.reg_insert_element_at.sub(r'.Insert(\2, \1)', src_line)
        src_line = self.reg_set_element_at.sub(r'[\2] = \1;', src_line)
        # LinkedList
        src_line = src_line.replace(".addFirst(", ".AddFirst(")
        src_line = src_line.replace(".addLast(", ".AddLast(")
        src_line = src_line.replace(".removeFirst(", ".RemoveFirst(")
        src_line = src_line.replace(".removeLast(", ".RemoveLast(")
        # Vector.Enumeration
        src_line = src_line.replace("GEnumeration<", "IEnumerator<")
        src_line = src_line.replace(".elements(", ".GetEnumerator(")
        src_line = src_line.replace(".hasMoreElements(", ".MoveNext(")
        src_line = src_line.replace(".nextElement()", ".Current")
        src_line = src_line.replace("GEnumerable", "IEnumerable")
        src_line = src_line.replace("GComparator", "IComparer")
        # IComparer
        src_line = src_line.replace(" compare(", " Compare(")           
        # GHashtable
        src_line = src_line.replace(".containsKey(", ".ContainsKey(")
        src_line = src_line.replace(".containsValue(", ".ContainsValue(")
        src_line = src_line.replace(".clear(", ".Clear(")
        # Exception handling
        src_line = src_line.replace("GThrowable", "Exception")
        src_line = src_line.replace("Debug.ex(true);", "Debug.ex(e, true);")
        src_line = src_line.replace("Debug.ex(false);", "Debug.ex(e, false);")
        src_line = src_line.replace("catch ( ... )", "catch ( Exception e )")
        # Math
        src_line = src_line.replace("Float.", "Single.")
        src_line = src_line.replace(".isNaN(", ".IsNaN(")
        src_line = src_line.replace("MAX_VALUE", "MaxValue")
        src_line = src_line.replace("MIN_VALUE", "MinValue")        
        # TODO: Runnable        
        src_line = src_line.replace("public virtual void run()", "public override void run()")
        # TODO: ErrorReporter
        src_line = src_line.replace("public virtual void handle(String stack)", "public override void handle(String stack)")
        return src_line    

    def format_imports(self):
        imports = ""
        for dependency in self.config.data["dependencies"]:
            imports += "using %s;\n" % dependency
        return imports
    
    def translate(self, filename_in, filename_out, config):
        self.filename_in = filename_in
        self.filename_out = filename_out        
        self.config = config

        # Java/C#. Update output file name
        self.filename_out = self.reg_file_name.sub(r'G\1', self.filename_out)

        # Open files
        src_file = codecs.open(self.filename_in, 'r', encoding='utf-8')
        dst_file = codecs.open(self.filename_out, 'w', encoding='utf-8')

        # Perform the translation
        self.dst_file_contents = ''
        for src_line in src_file:
            
            if ( 0 != self.remove_lines_count ):
                self.remove_lines_count = self.remove_lines_count - 1
                continue

            # Initialize line state
            self.override_found_this_line = ( -1 != src_line.find("override") )
            
            self.processLine(src_line)
        
        # Hide C++/Java statements
        self.dst_file_contents = self.unwrap(self.dst_file_contents, '/*C*/', '/**/', '/*C*', '**/', True)
        self.dst_file_contents = self.unwrap(self.dst_file_contents, '/*J*/', '/**/', '/*J*', '**/', True)
        self.dst_file_contents = self.unwrap(self.dst_file_contents, '/*X*/', '/**/', '/*X*', '**/', True)
        # Show C# statements
        self.dst_file_contents = self.unwrap(self.dst_file_contents, '/*S*', '**/', '/*S*/', '/**/', False)
        self.dst_file_contents = self.unwrap(self.dst_file_contents, '/*O*', '**/', '/*O*/', '/**/', False)
        self.dst_file_contents = self.unwrap(self.dst_file_contents, '/*Z*', '**/', '/*Z*/', '/**/', False)        
        
        # Save result to destination file
        dst_file.write(self.dst_file_contents)
        
        # Close files
        dst_file.close()
        src_file.close()

    def extension(self):
        return "cs"

class CSharpFactory:
    def translator(self):
        return CppToCSharp()

manager = engine.Manager(CSharpFactory())
manager.go()
