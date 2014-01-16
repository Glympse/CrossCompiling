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

/*C*interface GPrimitive;
typedef GPrimitive  GPrimitive;**/

/**
 * The IPrimitive interface is designed to operate with free form data structures.
 * The model behind IPrimitive conforms to JavaScript Object Notation (JSON)
 * (see http://www.ietf.org/rfc/rfc4627 for details).
 *
 * Supported primitive types are (see CC):
 * - array (PRIMITIVE_TYPE_ARRAY) - represents array of IPrimitive objects;
 * - object (PRIMITIVE_TYPE_OBJECT) - represents string hastable with value of IPrimitive type;
 * - double (PRIMITIVE_TYPE_DOUBLE) - represents value of primitive double type;
 * - long (PRIMITIVE_TYPE_LONG) - represents value of primitive long type (Glympse::int64);
 * - boolean (PRIMITIVE_TYPE_BOOL) - represents value of primitive boolean type;
 * - string (PRIMITIVE_TYPE_STRING) - represents value of primitive string type (Glympse::IString);
 * - null (PRIMITIVE_TYPE_BOOL) - indicates that object does not contain any value associated with it.
 */
/*O*/public/**/ interface GPrimitive : GComparable
{
    /**
     * Common properties.
     */

     int type();

     bool isArray();

     bool isObject();

     bool isDouble();

     bool isLong();

     bool isBool();

     bool isString();

     bool isNull();

     int size();
    
     GPrimitive clone();

    /**
     * Value getters.
     */

     double getDouble();

     long getLong();

     bool getBool();

     String getString();

    /**
     * Object getters.
     */

     GPrimitive get(String key);

     double getDouble(String key);

     long getLong(String key);

     bool getBool(String key);

     String getString(String key);

     IEnumerator<String> getKeys();

     bool hasKey(String key);

    /**
     * Array getters.
     */

     GArray<GPrimitive> getArray();

     GPrimitive get(int index);

     double getDouble(int index);

     long getLong(int index);

     bool getBool(int index);

     String getString(int index);

    /**
     * Value modifiers.
     */

     void set(double value);

     void set(long value);

     void set(bool value);

     void set(String value);

     void setNull();

    /**
     * Object modifiers.
     */

     void put(String key, GPrimitive value);

     void put(String key, double value);

     void put(String key, long value);

     void put(String key, bool value);

     void put(String key, String value);

     void putNull(String key);

     void remove(String key);

    /**
     * Array modifiers.
     */

     void put(GPrimitive value);

     void put(double value);

     void put(long value);

     void put(bool value);

     void put(String value);

     void insert(int index, GPrimitive value);

     void put(int index, GPrimitive value);

     void put(int index, double value);

     void put(int index, long value);

     void put(int index, bool value);

     void put(int index, String value);

     void putNull(int index);

     void remove(int index);

     void remove(GPrimitive value);
    
};

}

