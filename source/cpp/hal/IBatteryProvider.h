//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef IBATTERYPROVIDER_H__GLYMPSE__
#define IBATTERYPROVIDER_H__GLYMPSE__

namespace Glympse 
{
    
/*J*public**/ struct IBatteryProvider : public ICommon
{    
    public: virtual void setBatteryListener(const GBatteryListener& listener) = 0;
    
    public: virtual void start() = 0;
    
    public: virtual void stop() = 0;    
    
    public: virtual int32 getLevel() = 0;
    
    public: virtual bool isPlugged() = 0;    
    
    public: virtual bool isPresent() = 0;
    
    public: virtual void acquireWakeLock() = 0;
    
    public: virtual void releaseWakeLock() = 0;
};  
    
/*C*/typedef O< IBatteryProvider > GBatteryProvider;/**/
    
}

#endif // !IBATTERYPROVIDER_H__GLYMPSE__
