//------------------------------------------------------------------------------
//
//  Copyright (c) 2016 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------
{% import 'macros.tpl' as macros %}

{% for dependency in config.dependencies %}
#import "{{ dependency }}"
{% endfor %}

@implementation {{ type.name.objc_name }}
{
}

{% for item in type.body %}
{% if item.return_type %}
{{ macros.method_signature(method=item) }}
{
{% if item.return_type.native %}
    return {{ type.name.cpp_type }}::{{ item.name }}({{ macros.method_call_args(method=item) }});
{% else %}
    return Glympse::ClassBinder::bind({{ type.name.cpp_type }}::{{ item.name }}({{ macros.method_call_args(method=item) }}));
{% endif %}
}
{% else %}
+ ({{ item.type.objc_type }}){{ item.variable_declarators[0].variable.name }}
{
    return {{ type.name.cpp_type }}::{{ item.variable_declarators[0].variable.name }};
}
{% endif %}

{% endfor %}
@end
