//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef LONG_H__GLYMPSE__
#define LONG_H__GLYMPSE__

namespace Glympse 
{
    
/**
 * The wrapper for the primitive type long.
 *
 * This class also serves the purpose of being an example of extending and implementing the ICommon interface.
 */
class Long : public Common< ILong >
{
    public: static const int64 MAX_VALUE/*S* = Int64.MaxValue**/;
    
    private: int64 _value;
    
    public: static inline GLong valueOf(int64 value)
    {
        return new Long(value);
    }

    public: Long()
        /*C*/: _value(0)/**/
    {
        /*O*/_value = 0;/**/
    }
    
    public: Long(int64 value)
        /*C*/: _value(value)/**/
    {     
        /*O*/_value = value;/**/
    }    
    
    public: virtual int64 longValue()
    {
        return _value;
    }
    
    /**
     * Returns a hash code for this Long. The result is the exclusive OR of the two halves of the primitive long value 
     * held by this Long object. That is, the hashcode is the value of the expression:
     *     (int)(this.longValue()^(this.longValue()>>>32))
     */
    public: virtual /*S*override**/ int32 hashCode()
    {
        return (int32)(_value ^ (_value>>32));
    }
    
    /**
     * Compares this object to the specified object. The result is true if and only if the argument is not null 
     * and is a Long object that contains the same long value as this object.
     */
    public: virtual /*S*override**/ bool equals(const GCommonObj& o)
    {
        O<Long> l = (O<Long>)o;
        return ( ( l != NULL ) && ( l->_value == _value ) );
    }
};
    
}

#endif // !LONG_H__GLYMPSE__
