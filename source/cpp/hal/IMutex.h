//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef IMUTEX_H__GLYMPSE__
#define IMUTEX_H__GLYMPSE__

namespace Glympse
{

/*J*public**/ struct IMutex : public ICommon
{
    public: virtual void block() = 0;
    
    public: virtual void unblock() = 0;
};
    
/*C*/typedef O< IMutex > GMutex;/**/
    
}

#endif // !IMUTEX_H__GLYMPSE__
