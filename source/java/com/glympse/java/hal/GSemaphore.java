//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

package com.glympse.java.hal;

import java.util.*;
import com.glympse.java.core.*;
import com.glympse.java.hal.*;
    
/*J*/public/**/ interface GSemaphore extends GCommon
{
    public void acquire();
        
    public void notify(int count);    
};  
    
/*C*typedef GSemaphore  GSemaphore;**/
    


