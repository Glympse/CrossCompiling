//------------------------------------------------------------------------------
//
//  Copyright (c) 2016 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------

{% for dependency in config.dependencies %}
#import "{{ dependency }}"
{% endfor %}

@implementation {{ type.name.objc_name }}
{
}

{% for item in type.body %}
{% if item.return_type %}
+ ({{ item.return_type.objc_type }}){{ item.name }}
{
{% if item.return_type.native %}
    return Glympse::{{ type.name.java_name }}::{{ item.name }}();
{% else %}
    return Glympse::ClassBinder::bind(Glympse::{{ type.name.java_name }}::{{ item.name }}());
{% endif %}
}
{% else %}
+ ({{ item.type.objc_type }}){{ item.variable_declarators[0].variable.name }}
{
    return Glympse::{{ type.name.java_name }}::{{ item.variable_declarators[0].variable.name }};
}
{% endif %}

{% endfor %}
@end
