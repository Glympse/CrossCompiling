//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef ILONG_H__GLYMPSE__
#define ILONG_H__GLYMPSE__

namespace Glympse 
{
    
/*C*/
struct ILong;
typedef O< ILong > GLong;
/**/
    
/**
 * The ILong interface wraps a value of the primitive type long (int64) in an object.
 */
/*O*public**/ struct ILong : public ICommon
{
    /**
     * Returns the value of this Long as a long value.
     *
     * @return The numeric value represented by this object after conversion to type long.
     */
    public: virtual int64 longValue() = 0;
};
    
}

#endif // !ILONG_H__GLYMPSE__
