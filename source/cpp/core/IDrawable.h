//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef IDRAWABLE_H__GLYMPSE__
#define IDRAWABLE_H__GLYMPSE__

namespace Glympse 
{

/**
 * Represents bitmap objects on the system. Provides minimal cross-platform
 * interface to access image properties. 
 */
/*O*public**/ struct IDrawable : public ICommon
{
};
    
/*C*/typedef O< IDrawable > GDrawable;/**/
    
}

#endif // !IDRAWABLE_H__GLYMPSE__
