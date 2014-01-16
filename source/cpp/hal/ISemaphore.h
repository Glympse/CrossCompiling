//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef ISEMAPHORE_H__GLYMPSE__
#define ISEMAPHORE_H__GLYMPSE__

namespace Glympse 
{
    
/*J*public**/ struct ISemaphore : public ICommon
{
    public: virtual void acquire() = 0;
        
    public: virtual void notify(int32 count) = 0;    
};  
    
/*C*/typedef O< ISemaphore > GSemaphore;/**/
    
}

#endif // !ISEMAPHORE_H__GLYMPSE__
