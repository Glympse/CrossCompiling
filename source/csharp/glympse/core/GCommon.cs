//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using System.Threading;

namespace Glympse 
{

/*C*
// 64bit int definition.
    typedef int int;    
    typedef __long long;
    typedef int int;
    typedef long long int long;
**/
    
/*C*
// Typedefs for character arrays and buffers.
typedef char byte;
typedef String CharBuffer;    
typedef String ByteBuffer;
        
// Preliminary GCommon declaration.    
interface GCommon;
typedef GCommon  GCommon;
typedef GCommon Object;

// Preliminary IString declaration.
interface String;    
typedef String  String;   
**/
    
/**
 * The foundtation for the Glympse API object model. 
 */
/*O*/public/**/ interface GCommon
{
    /** 
     * Add a reference to our object in a COM-like way. 
     */
    /*C* int retain();**/
        
    /**
     * Release a reference to our object in a COM-like way.
     */
    /*C* int release();**/
    
    /**
     * Returns an integer hash code for this object.
     */     
    /*C* int GetHashCode();**/
    
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
    /*C* bool Equals(Object o);**/
    
    /**
     * Returns a string containing a concise, human-readable description of this object.
     *
     * This method is not designed for efficiency, so it should only be used for 
     * debugging purposes. Avoid using it in production code. 
     * 
     * The implementation is platform specific. You should not rely on the value returned
     * by this method. 
     */     
    /*C* String toString();**/
              
    /**
     * Destructor is protected to deny explicit object deallocation.
     * It is virtual to prevent incorrect behavior, when the object is destroyed.
     * It is implemented to prevent linker issues.
     */
    /*C* ~ICommon() 
    {            
    }**/        
};
    
}

