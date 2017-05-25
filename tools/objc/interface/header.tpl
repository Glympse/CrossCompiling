//------------------------------------------------------------------------------
//
//  Copyright (c) 2017 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------
{% import 'macros.tpl' as macros %}

{% if type.is_protocol %}
@protocol {{ type.name.objc_name }}{{ macros.protocol_heirarchy(package=package, type=type) }}
{% else %}
@interface {{ type.name.objc_name }} : {{ macros.class_heirarchy(package=package, type=type) }}
{% endif %}

{% for method in type.body -%}

{{ macros.method_signature(method=method) }};

{% endfor %}
@end