//------------------------------------------------------------------------------
//
//  Copyright (c) 2016 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------
{% import 'macros.tpl' as macros %}

{% if type.is_protocol %}
@protocol {{ type.name.objc_name }}< NSObject >
{% else %}
@interface {{ type.name.objc_name }} : {{ macros.base_class(package=package, type=type) }}
{% endif %}

{% for method in type.body -%}

{{ macros.method_signature(method=method) }};

{% endfor %} {# Methods #}
@end