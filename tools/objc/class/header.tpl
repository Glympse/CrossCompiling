//------------------------------------------------------------------------------
//
//  Copyright (c) 2016 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------

@interface {{ type.name.objc_name }} : NSObject
{
}

{% for item in type.body %}
{% if item.return_type %}
+ ({{ item.return_type.objc_type }}){{ item.name }};
{% else %}
+ ({{ item.type.objc_type }}){{ item.variable_declarators[0].variable.name }};
{% endif %}

{% endfor %}
@end
