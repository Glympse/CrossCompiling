//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

package com.glympse.java.hal;

import java.util.*;
import com.glympse.java.core.*;
import com.glympse.java.hal.*;
    
/*J*/public/**/ interface GBatteryProvider extends GCommon
{    
    public void setBatteryListener(GBatteryListener listener);
    
    public void start();
    
    public void stop();    
    
    public int getLevel();
    
    public boolean isPlugged();    
    
    public boolean isPresent();
    
    public void acquireWakeLock();
    
    public void releaseWakeLock();
};  
    
/*C*typedef GBatteryProvider  GBatteryProvider;**/
    


