//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef ITHREAD_H__GLYMPSE__
#define ITHREAD_H__GLYMPSE__

namespace Glympse 
{
    
struct IThread : public ICommon
{
    public: virtual void start() = 0;
    
    public: virtual void join() = 0;    
};
    
typedef O< IThread > GThread;
    
}

#endif // !ITHREAD_H__GLYMPSE__
