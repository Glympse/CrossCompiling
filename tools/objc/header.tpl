//------------------------------------------------------------------------------
//
//  Copyright (c) 2016 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------
{% import 'macros.tpl' as macros %}

{% for type in syntax_tree.type_declarations %}
{% if type.name %}
{% if type.is_protocol %}
@protocol {{ type.name.objc_name }}< NSObject >
{% else %}
@interface {{ type.name.objc_name }} : {{ macros.base_class(type=type) }}
{% endif %}
{% for method in type.body %}

{{ macros.method_signature(method=method) }}; {# Parameters #}

{% endfor %} {# Methods #}

@end

{% endif %} {# Type name specified #}
{% endfor %} {# Types #}