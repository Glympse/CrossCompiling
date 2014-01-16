//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef COMMON_H__GLYMPSE__
#define COMMON_H__GLYMPSE__

namespace Glympse 
{

/**
 * The purpose of this storage helper is to avoid the need in virtual inheritance
 * in client side code. This allows multiple inheritance from Common<T> without the
 * need to specify "virtual" keyword, as Common is already derived from CommonStorage
 * virtually.
 */ 
class CommonStorage
{
    /**
     * Our private ref count.
     */
    protected: int32 _ref;        
    
    protected: CommonStorage()
        : _ref(1)
    {        
    }    
};
    
/**
 * Implements all methods of ICommon interface. All interfaces on the system extend ICommon.
 * Every class on the system should use this helper to avoid implementing all ICommon methods on its own.
 * Some classes will still decide to override hashCode() and equals(). 
 */
template< class T > 
class Common 
    : public T
    , public virtual CommonStorage
{
    /**
     * Our constructor. Protected for now since I don't think anyone should
     * ever need to create an Object by itself. It is intended to be used only
     * as a base class.
     */
    protected: Common() 
        : CommonStorage()
    {
    }
    
    /**
     * Our destructor is here simply to create an entry in the vtable to ensure
     * derived classes destruct correctly.
     */
    protected: virtual ~Common()
    {
    }
        
    /**
     * Add a reference to our object in a COM-like way. 
     */
    public: virtual int32 retain()
    {
        return Concurrent::increment((int32*)&_ref);
    }
    
    /**
     * Release a reference to our object in a COM-like way. 
     */ 
    public: virtual int32 release()
    {
        int32 result = Concurrent::decrement((int32*)&_ref);
        if ( 0 == result )
        {
            delete this;
        }
        return result;
    }
    
    /**
     * Returns an integer hash code for this object.
     */
    public: virtual int32 hashCode()
    {
        return hashCode((int64)this);
    }
    
    /**
     * Compares this instance with the specified object and indicates if they are equal.
     */
    public: virtual bool equals(const GCommonObj& o)
    {
        return ( this == o._object );
    }
    
    /**
     * Returns a string containing a concise, human-readable description of this object.
     */
    public: virtual GString toString();
    
    /**
     * Calculates hash code (32-bit value) of 64-bit value.
     */
    public: static inline int32 hashCode(int64 value)
    {
        return ((int32)(value ^ (value >> 32)));
    }
};

}

#endif // !COMMON_H__GLYMPSE__
