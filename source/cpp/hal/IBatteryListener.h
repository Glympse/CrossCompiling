//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef IBATTERYLISTENER_H__GLYMPSE__
#define IBATTERYLISTENER_H__GLYMPSE__

namespace Glympse 
{
    
/*J*public**/ struct IBatteryListener : public ICommon
{    
    public: virtual void updateStatus(int32 level, bool plugged, bool present) = 0;

    public: virtual void memoryWarningReceived() = 0;
};
    
/*C*/typedef O< IBatteryListener > GBatteryListener;/**/
    
}

#endif // !IBATTERYLISTENER_H__GLYMPSE__
