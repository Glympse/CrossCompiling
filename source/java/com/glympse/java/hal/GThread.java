//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

package com.glympse.java.hal;

import java.util.*;
import com.glympse.java.core.*;
import com.glympse.java.hal.*;
    
interface Thread extends GCommon
{
    public void start();
    
    public void join();    
};
    
typedef Thread  Thread;
    


