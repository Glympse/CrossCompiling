//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef COMMONIMPL_H__GLYMPSE__
#define COMMONIMPL_H__GLYMPSE__

namespace Glympse 
{

template< class T > GString Common<T>::toString()
{
    return CoreFactory::createString(typeid(*this).name());
}
    
}

#endif // !COMMONIMPL_H__GLYMPSE__
