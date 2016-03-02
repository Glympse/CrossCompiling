#------------------------------------------------------------------------------
#
# Copyright (c) 2014 Glympse Inc.  All rights reserved.
#
#------------------------------------------------------------------------------

class BasicTranslator(object):

    def processLine(self, src_line):              	
        # Handle '/* */' comments
        if ( self.multiline_comment ):
            # Look for multiline comment end statement '*/'
            c_comment_end_pos = src_line.find("*/")
            if ( -1 == c_comment_end_pos ):
                # Comment is not ending this line. Just add it to destination without processing
                self.dst_file_contents = self.dst_file_contents + src_line
                return
            else:
                # Split line            
                comment = src_line[0:c_comment_end_pos + 2]
                after_comment = src_line[c_comment_end_pos + 2:len(src_line)]  
        
                # Add remaining comment to destination
                self.dst_file_contents = self.dst_file_contents + comment
        
                # End multiline comment
                self.multiline_comment = False
                
                # Process remaining part of the line
                self.processLine(after_comment)
                return
        else:
            # Handle '// ' comments. Avoid '*//' cases.
            cpp_comment_pos = src_line.find("//")
            if ( ( -1 != cpp_comment_pos ) and ( '*' != src_line[cpp_comment_pos - 1] ) ):
                # Split line            
                before_comment = src_line[0:cpp_comment_pos]
                comment = src_line[cpp_comment_pos:len(src_line)]            
            
                # Process the first part of the line
                if ( not self.processLine(before_comment) ):
                    return
                
                # Append comment to destination
                self.dst_file_contents = self.dst_file_contents + comment        
                return

            # Look for multiline comment begin statement '/*'
            c_comment_begin_pos = src_line.find("/*")
            if ( -1 != c_comment_begin_pos ):
                # Split line            
                before_comment = src_line[0:c_comment_begin_pos]
                comment = src_line[c_comment_begin_pos:len(src_line)]  
                
                # Start multiline comment
                self.multiline_comment = True                
                
                # Process the first part of the line
                before_comment = self.processFragment(before_comment)
                if ( before_comment is not None ):
                    self.dst_file_contents = self.dst_file_contents + before_comment
                
                # Append comment begin statement to destination
                self.dst_file_contents = self.dst_file_contents + "/*"
                
                # Process comment (what if it ends right at the same line)
                comment_content = comment[2:len(comment)]  
                self.processLine(comment_content)
                return
        
        src_line = self.processFragment(src_line)
        if ( src_line is None ):
            return False
        
        self.dst_file_contents = self.dst_file_contents + src_line
        return True

    def unwrap(self, content, begin, end, new_begin, new_end, wrap):
        begin_pos = content.find(begin)
        while ( -1 != begin_pos ):
            end_pos = content.find(end, begin_pos)
            if ( -1 != end_pos ):
                already_wrapped = False
                if ( not wrap ):
                    next_ch = content[begin_pos + len(begin):begin_pos + len(begin) + 1]
                    if ( next_ch == "/" ):
                        already_wrapped = True
                if ( not already_wrapped ):
                    content = content[0:begin_pos] + new_begin + content[begin_pos + len(begin):end_pos] + new_end + content[end_pos + len(end):len(content)] 
            else:
                end_pos = begin_pos + 1
            begin_pos = content.find(begin, end_pos + 1)
        return content


class BasicFactory(object):

    def begin_package(self, config, package):
        pass

    def package_completed(self, config, package):
        pass