//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef OBJECT_H__GLYMPSE__
#define OBJECT_H__GLYMPSE__

namespace Glympse
{

/**
 * Smart pointer designed to maintain lifetime of objects with internal reference counting 
 * (ICommon degived classes).
 *
 * The following rules are applied to incrementing and decrementing reference counter:
 * - Reference counter is not incremented, when O<T> is initialized with raw pointer
 *   (neither constructed nor assigned to).
 * - Reference counter is incremented, when O<T> is initialized with another object of O<T> type
 *   (both constructed and assigned to).
 * - Reference counter is incremented, when O<T> is initialized with another object of O<Y> type,
 *   if Y can be casted dynamically to T (using dynamic_cast).
 * - Reference counter is decremented unconditionally, when instance of O<T> is destroyed.
 */
template< class T > class O
{
    /**
     * A pointer to the object we are referencing.
     */
    private: T* _object;

    /**
     * There are several cases below where we have templatized methods below that
     * need access to _object between types of O. We can allow this by friending our main type.
     */
    template< class U > friend class O;
    template< class V > friend class Common;
    
    /**
     * @name Constructors
     */

    /**
     * This constructor just creates an empty "null reference" that can be assinged later.
     */
    public: O() 
        : _object(NULL)
    {
    }
    public: O(T* address)
        : _object(address)
    {
    }
    public: O(const O<T>& rO)
        : _object(rO._object)
    {
        retain();
    }
    public: template< class T2 > O(const O<T2>& rO)
        : _object(dynamic_cast<T*>(rO._object))
    {
        retain();
    }
    
    /**
     * @name Assignment Operators
     */
    
    public: O<T>& operator=(T* address)
    {
        release();
        _object = address;
        return *this;
    }    
    public: O<T>& operator=(const O<T>& rO)
    {
        if ( this != &rO )
        {
            release();
            _object = rO._object;
            retain();
        }
        return *this;
    }
    public: template< class T2 > O<T>& operator=(const O<T2>& rO)
    {
        release();
        _object = dynamic_cast<T*>(rO._object);
        retain();
        return *this;
    }
    
    /**
     * @name Destructor
     */
    
    /**
     * Regardless of how we obtained the object we are pointing to, we release it when we destuct.
     */
    public: virtual ~O()
    {
        release();
    }

    /**
     * @name Equality Checks
     * These equality checks are for use when two smart pointers are being compared.
     */
    
    public: template<class T2> bool operator==(const O<T2> &rO)
    {
        return _object == rO._object;
    }
    public: template<class T2> bool operator==(const O<T2> &rO) const
    {
        return _object == rO._object;
    }    
    public: template<class T2> bool operator!=(const O<T2> &rO)
    {
        return _object != rO._object;
    }
    public: template<class T2> bool operator!=(const O<T2> &rO) const
    {
        return _object != rO._object;
    }    
    public: template<class T2> bool operator<(const O<T2> &rO)
    {
        return _object < rO._object;
    }    
    public: template<class T2> bool operator<(const O<T2> &rO) const
    {
        return _object < rO._object;
    }
    
    /**
     * @name Testing for NULL
     * These equality checks are for use when comapring a smart pointer to raw pointer
     * (this also handles comparing to NULL).
     */
        
    public: bool operator==(T* address)
    {
        return (_object == address);
    }
    public: bool operator==(T* address) const
    {
        return (_object == address);
    }
    public: bool operator!=(T* address)
    {
        return (_object != address);
    }
    public: bool operator!=(T* address) const
    {
        return (_object != address);
    }
    
    /**
     * @name Member Access
     * This is how we allow access to the members of the object we are referencing.
     */
        
    T* operator->()
    {
        return _object;
    }
    T* operator->() const
    {
        return _object;
    }
        
    /**
     * @name Internals 
     */

    /**
     * Internal helper function to safely add a reference.
     */
    private: inline void retain()
    {
        if ( _object )
        {
            _object->retain();
        }
    }

    /**
     * Internal helper function to safely release a reference.
     */
    private: inline void release()
    {
        if ( _object )
        {
            _object->release();
            _object = NULL;
        }
    }
};

/**
 * Global equality operator to enable the followng syntax:
 * <code>if ( NULL == ptr )</code>
 */
template< class T > inline bool operator==(void* lhs, const O<T>& rhs)
{
    return ( lhs == rhs.operator->() );
}

/**
 * Global equality operator to enable the followng syntax:
 * <code>if ( NULL != ptr )</code>
 */
template< class T > inline bool operator!=(void* lhs, const O<T>& rhs)
{
    return ( lhs != rhs.operator->() );
}

/**
 * The Object class provides some helpers for dealing with O<T> objects. 
 */
class Object
{
    /**
     * fromThis() allows an object t to safely generate additional O<T> instances that
     * all manipulate the lifetime of t (through its internal reference counter).
     * <pre>
     * void someMethod()
     * {
     *     Glympse::GSomeEventSink sink = ...;
     *     sink->addListener(Glympse::Object::fromThis(this));
     * }
     * </pre>
     *
     * @note fromThis() method should NOT be used when object is instantiated.
     * Newly created objects have internal reference counter already initialized with 1.
     * <pre>
     * Glympse::GLong number = new Glympse::Long(10LL);
     * </pre>
     *
     * @param Pointer to the object of class that implements ICommon.
     * @return Instance of O<T> that wraps raw pointer and participates in its
     * lifetime management.
     */
    public: template<typename T> static inline O<T> fromThis(T* t)
    {
        const O<T>& o(t);
        o->retain();
        return o;
    }
};
        
}

#endif // !OBJECT_H__GLYMPSE__
