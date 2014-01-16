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
interface GLong;
typedef GLong  GLong;
**/
    
/**
 * The ILong interface wraps a value of the primitive type long (int64) in an object.
 */
/*O*/public/**/ interface GLong : GCommon
{
    /**
     * Returns the value of this Long as a long value.
     *
     * @return The numeric value represented by this object after conversion to type long.
     */
     long longValue();
};
    
}

