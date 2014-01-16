//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef ISTRING_H__GLYMPSE__
#define ISTRING_H__GLYMPSE__

namespace Glympse 
{
    
/**
 * Type for Unicode characters.
 */
typedef unsigned short unichar;
    
/**
 * An immutable sequence of characters/code units. A string is represented by array of UTF-8 values.
 */
struct IString : public ICommon
{
    /**
     * Returns the size of this string.
     * 
     * For strings having unicode characters, it returns a number of bytes occupied by a string 
     * representation in UTF-8 encoding. 
     *
     * @return the number of characters in this string.
     */
    public: virtual int32 length() = 0;
    
    /**
     * Copies this string removing white space characters from the beginning and end of the string.
     *
     * @return a new string with characters <= \\u0020 removed from the beginning and the end.
     */ 
    public: virtual GString trim() = 0;
    
    /**
     * Returns the character at the specified offset in this string.
     *
     * @param index the zero-based index in this string.
     * @return Returns the character at the index.
     */
    public: virtual unichar charAt(int32 index) = 0;
    
    /**
     * Searches in this string for the first index of the specified character. 
     * The search for the character starts at the beginning and moves towards the end of this string.
     *
     * @param seperator the character to find.
     *     
     * @return the index in this string of the specified character, -1 if the character isn't found.
     */
    public: virtual int32 indexOf(char seperator) = 0;    
    
    /**
     * Searches in this string for the first index of the specified character. 
     * The search for the character starts at the beginning and moves towards the end of this string.
     *
     * @param seperator the character to find.
     * @param start the starting offset.
     *     
     * @return the index in this string of the specified character, -1 if the character isn't found.
     */
    public: virtual int32 indexOf(char seperator, int32 start) = 0;
    
    /**
     * Searches in this string for the index of the specified string. 
     * The search for the string starts at the beginning and moves towards the end of this string.
     * 
     * @param str the string to find.
     * @return Returns the index of the first character of the specified string in this string, 
     * -1 if the specified string is not a substring.
     */ 
    public: virtual int32 indexOf(const GString& str) = 0;       
    
    /**
     * Searches in this string for the index of the specified string. 
     * The search for the string starts at the specified offset and moves towards the end of this string.
     * 
     * @param str the string to find.
     * @param start the starting offset.
     * @return Returns the index of the first character of the specified string in this string, 
     * -1 if the specified string is not a substring.
     */ 
    public: virtual int32 indexOf(const char* str, int32 start) = 0;    
    
    /**
     * Returns the last index of the code point c, or -1. 
     * The search for the character starts at the end and moves towards the beginning of this string.
     * 
     * @param seperator the character to find.
     *
     * @return the index in this string of the specified character, -1 if the character isn't found.
     */    
    public: virtual int32 lastIndexOf(char seperator) = 0;    
    
    /**
     * Returns a string containing a subsequence of characters from this string. 
     * The returned string shares this string's backing array.
     *
     * @param start the offset of the first character.
     * @param end the offset one past the last character.
     * 
     * @return a new string containing the characters from start to end - 1.
     */
    public: virtual GString substring(int32 start, int32 end) = 0;

    /**
     * Appends the string to current string and returns new string. 
     *
     * @param str the string to append to current string. 
     * 
     * @return a new string containing a concatenation of current string and the argument.
     */     
    public: virtual GString append(const char* str) = 0;
    
    /**
     * This method is provided for convenience. 
     * See append(const char*) for more details. 
     */ 
    public: virtual GString append(const GString& str) = 0;
    
    /**
     * Compares the specified string to this string to determine if the specified string is a prefix.
     *
     * @param prefix the prefix to look for.
     *
     * @return true if the specified string is a prefix of this string, false otherwise.
     */
    public: virtual bool startsWith(const char* prefix) = 0;       
    
    /**
     * Compares the specified string to this string to determine if the specified string is a prefix.
     *
     * @param prefix the prefix to look for.
     *
     * @return true if the specified string is a prefix of this string, false otherwise.
     */
    public: virtual bool startsWith(const GString& prefix) = 0;          
    
    /**
     * Compares the specified string to this string to determine if the specified string is a suffix.
     *
     * @param suffix the suffix to look for.
     *
     * @return true if the specified string is a suffix of this string, false otherwise.
     */
    public: virtual bool endsWith(const char* suffix) = 0;        
    
    /**
     * This method is provided for convenience. 
     * See endsWith(const char*) for more details. 
     */ 
    public: virtual bool endsWith(const GString& suffix) = 0;    

    /**
     * Splits this string using the supplied str. 
     *
     * @return an array of substrings if this instance is delimited by one or more of the characters in separator.
     * an array consisting of a single element containing this instance, if this instance contains none of the characters in separator.     
     */
    public: virtual GArray<GString>::ptr split(const char* separator) = 0;
    
    /**
     * This method is provided for convenience. 
     * See split(const char*) for more details. 
     */     
    public: virtual GArray<GString>::ptr split(const GString& str) = 0;    
    
    /**
     * Copies this string replacing occurrences of the specified target sequence with another sequence. 
     * The string is processed from the beginning to the end.
     *
     * @param target the sequence to replace.
     * @param replacement the replacement sequence.
     * @return Returns the resulting string.
     */
    public: virtual GString replace(const char* target, const char* replacement) = 0;     
        
    /**
     * Converts this string to lower case, using the rules of the user's default locale.
     *
     * @return Returns a new lower case string, or this if it's already all lower case.
     */
    public: virtual GString toLowerCase() = 0;
    
    /**
     * Compares the specified string to this string and returns true if they are equal. 
     * 
     * @param str the string to compare.
     * 
     * @return true if the specified string is equal to this string, false otherwise.
     */ 
    public: virtual bool equals(const char* str) = 0;
    
    /**
     * This method is provided for convenience. 
     * See equals(const char*) for more details. 
     */   
    public: virtual bool equals(const GString& str) = 0;
    
    /**
     * Compares the specified string to this string ignoring the case of the characters and returns true if they are equal.
     * 
     * @param str the string to compare.
     * 
     * @return true if the specified string is equal to this string, false otherwise.
     */     
    public: virtual bool equalsIgnoreCase(const char* str) = 0;
    
    /**
     * This method is provided for convenience. 
     * See equalsIgnoreCase(const char*) for more details. 
     */       
    public: virtual bool equalsIgnoreCase(const GString& str) = 0;
    
    /**
     * Compares the specified string to this string using the Unicode values of the characters. 
     * Returns 0 if the strings contain the same characters in the same order. 
     * Returns a negative integer if the first non-equal character in this string has a Unicode value 
     * which is less than the Unicode value of the character at the same position in the specified string, 
     * or if this string is a prefix of the specified string. Returns a positive integer 
     * if the first non-equal character in this string has a Unicode value which is greater
     * than the Unicode value of the character at the same position in the specified string, 
     * or if the specified string is a prefix of this string.
     * 
     * @param str the string to compare.
     * 
     * @return 0 if the strings are equal, a negative integer if this string is before the specified string, 
     * or a positive integer if this string is after the specified string.
     */ 
    public: virtual int32 compareTo(const GString& str) = 0;    
    
    /**
     * Provides access to the array containing the characters of this string.
     * The array contains string representation in UTF-8 encoding. 
     *
     * You should never modify contents of the returned array. 
     * 
     * @return a character array containing the characters of this string.
     */
    public: virtual const char* getBytes() = 0;
    
    /**
     * This method is provided for convenience. 
     * See getBytes() for more details. 
     */     
    public: virtual const char* toCharArray() = 0;    
};
        
}

#endif // !ISTRING_H__GLYMPSE__
