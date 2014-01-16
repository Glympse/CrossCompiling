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
    
/*J*public**/ interface GBatteryListener : GCommon
{    
     void updateStatus(int level, bool plugged, bool present);

     void memoryWarningReceived();
};
    
/*C*typedef GBatteryListener  GBatteryListener;**/
    
}

