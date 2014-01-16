//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

package com.glympse.java.hal;

import java.util.*;
import com.glympse.java.core.*;
import com.glympse.java.hal.*;

/*J*/public/**/ interface GMutex extends GCommon
{
    public void block();
    
    public void unblock();
};
    
/*C*typedef GMutex  GMutex;**/
    


