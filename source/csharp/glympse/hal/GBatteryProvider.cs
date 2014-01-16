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
    
/*J*public**/ interface GBatteryProvider : GCommon
{    
     void setBatteryListener(GBatteryListener listener);
    
     void start();
    
     void stop();    
    
     int getLevel();
    
     bool isPlugged();    
    
     bool isPresent();
    
     void acquireWakeLock();
    
     void releaseWakeLock();
};  
    
/*C*typedef GBatteryProvider  GBatteryProvider;**/
    
}

