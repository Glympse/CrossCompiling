//------------------------------------------------------------------------------
//
// Copyright (c) 2014 Glympse Inc.  All rights reserved.
//
//------------------------------------------------------------------------------

#ifndef ICOMPARABLE_H__GLYMPSE__
#define ICOMPARABLE_H__GLYMPSE__

namespace Glympse
{
    
/**
 * The IComparable interface is introduced to provide additional mechanizm
 * of content-oriented objects comparison, which does not conflict with
 * language-specific one (Object.equals in Java and Object.Equals in C#).
 */
/*O*public**/ struct IComparable : public virtual ICommon
{
    /**
     * Compares this instance with the specified object and indicates if they are equal.
     * In order to be equal, o must represent the same object as this instance using a class-specific comparison.
     * The general contract is that this comparison should be reflexive, symmetric, and transitive.
     * Also, no object reference other than NULL is equal to NULL.
     *
     * @param o The object to compare this instance with.
     * @return Returns true if the specified object is equal to this object; false otherwise.
     */
    public: virtual bool isEqual(const GCommon& o) = 0;
};
    
/*C*/typedef O< IComparable > GComparable;/**/
    
}

#endif // !ICOMPARABLE_H__GLYMPSE__
