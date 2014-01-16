//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

package com.glympse.java.hal;

import java.util.*;
import com.glympse.java.core.*;
import com.glympse.java.hal.*;
    
/*J*/public/**/ interface GBatteryListener extends GCommon
{    
    public void updateStatus(int level, boolean plugged, boolean present);

    public void memoryWarningReceived();
};
    
/*C*typedef GBatteryListener  GBatteryListener;**/
    


