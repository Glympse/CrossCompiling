//------------------------------------------------------------------------------
//
//  Copyright (c) 2017 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------
{% import 'macros.tpl' as macros %}

@interface {{ type.name.objc_name }} : NSObject
{
}

{% for item in type.body %}
{% if item.return_type %}
{{ macros.method_signature(method=item) }};
{% else %}
+ ({{ item.type.objc_type }}){{ item.variable_declarators[0].variable.name }};
{% endif %}

{% endfor %}
@end
