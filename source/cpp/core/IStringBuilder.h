//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef ISTRINGBUILDER_H__GLYMPSE__
#define ISTRINGBUILDER_H__GLYMPSE__

namespace Glympse 
{
    
struct IStringBuilder;    
typedef O< IStringBuilder > GStringBuilder;        
    
/**
 * A modifiable sequence of characters for use in creating strings.
 */
struct IStringBuilder : public ICommon
{
    public: virtual void append(const char* str) = 0;
    
    public: virtual void append(const GString& str) = 0;
    
    public: virtual void append(const GStringBuilder& sb) = 0;
    
    public: virtual void append(char c) = 0;
    
    public: virtual void append(unichar c) = 0;
    
    public: virtual void append(int32 i) = 0;            
    
    public: virtual void append(int64 ll) = 0;         
    
    public: virtual void append(double d) = 0;                
    
    public: virtual void insert(int32 offset, char c) = 0;
    
    public: virtual int32 capacity() = 0;
    
    public: virtual void ensureCapacity(int32 capacity) = 0;    

    public: virtual void setLength(int32 length) = 0;
    
    public: virtual int32 length() = 0;

    public: virtual GString toString() = 0;
};

}

#endif // !ISTRINGBUILDER_H__GLYMPSE__
