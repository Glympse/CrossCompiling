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
    
/**
 * The wrapper for the primitive type long.
 *
 * This class also serves the purpose of being an example of extending and implementing the ICommon interface.
 */
class Long : GLong 
{
    public const long MaxValue/*S*/ = Int64.MaxValue/**/;
    
    private long _value;
    
    public static GLong valueOf(long value)
    {
        return new Long(value);
    }

    public Long()
        /*C*: _value(0)**/
    {
        /*O*/_value = 0;/**/
    }
    
    public Long(long value)
        /*C*: _value(value)**/
    {     
        /*O*/_value = value;/**/
    }    
    
    public virtual long longValue()
    {
        return _value;
    }
    
    /**
     * Returns a hash code for this Long. The result is the exclusive OR of the two halves of the primitive long value 
     * held by this Long object. That is, the hashcode is the value of the expression:
     *     (int)(this.longValue()^(this.longValue()>>>32))
     */
    public /*S*/override/**/ int GetHashCode()
    {
        return (int)(_value ^ (_value>>32));
    }
    
    /**
     * Compares this object to the specified object. The result is true if and only if the argument is not null 
     * and is a Long object that contains the same long value as this object.
     */
    public /*S*/override/**/ bool Equals(Object o)
    {
        Long l = (Long)o;
        return ( ( l != null ) && ( l._value == _value ) );
    }
};
    
}

