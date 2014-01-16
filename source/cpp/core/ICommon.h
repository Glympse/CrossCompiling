//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef ICOMMON_H__GLYMPSE__
#define ICOMMON_H__GLYMPSE__

namespace Glympse 
{

/*C*/
// 64bit int definition.
#if defined(WIN32) || defined(__MINGW32__) // Windows environment
    typedef int int32;    
    typedef __int64 int64;
#else // Everyone else
    typedef int int32;
    typedef long long int int64;
#endif    
/**/
    
/*C*/
// Typedefs for character arrays and buffers.
typedef char byte;
typedef char* CharBuffer;    
typedef char* ByteBuffer;
        
// Preliminary GCommon declaration.    
struct ICommon;
typedef O< ICommon > GCommon;
typedef GCommon GCommonObj;

// Preliminary IString declaration.
struct IString;    
typedef O< IString > GString;   
/**/
    
/**
 * The foundtation for the Glympse API object model. 
 */
/*O*public**/ struct ICommon
{
    /** 
     * Add a reference to our object in a COM-like way. 
     */
    /*C*/public: virtual int32 retain() = 0;/**/
        
    /**
     * Release a reference to our object in a COM-like way.
     */
    /*C*/public: virtual int32 release() = 0;/**/
    
    /**
     * Returns an integer hash code for this object.
     */     
    /*C*/public: virtual int32 hashCode() = 0;/**/
    
    /**
     * Compares this instance with the specified object and indicates if they are equal. 
     * In order to be equal, o must represent the same object as this instance using a class-specific comparison. 
     * The general contract is that this comparison should be reflexive, symmetric, and transitive. 
     * Also, no object reference other than NULL is equal to NULL.
     *
     * The default implementation returns true only if this == o. 
     * 
     * @param o The object to compare this instance with.
     * @return Returns true if the specified object is equal to this object; false otherwise.
     */     
    /*C*/public: virtual bool equals(const GCommonObj& o) = 0;/**/
    
    /**
     * Returns a string containing a concise, human-readable description of this object.
     *
     * This method is not designed for efficiency, so it should only be used for 
     * debugging purposes. Avoid using it in production code. 
     * 
     * The implementation is platform specific. You should not rely on the value returned
     * by this method. 
     */     
    /*C*/public: virtual GString toString() = 0;/**/
              
    /**
     * Destructor is protected to deny explicit object deallocation.
     * It is virtual to prevent incorrect behavior, when the object is destroyed.
     * It is implemented to prevent linker issues.
     */
    /*C*/protected: virtual ~ICommon() 
    {            
    }/**/        
};
    
}

#endif // !ICOMMON_H__GLYMPSE__
