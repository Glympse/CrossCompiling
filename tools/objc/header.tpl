//------------------------------------------------------------------------------
//
//  Copyright (c) 2016 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------
{% macro base_class(type) -%}
{{ type.base }}
{%- if type.is_sink %}
< GlyEventSink >
{%- endif %}
{%- endmacro %}

{% for type in syntax_tree.type_declarations %}
{% if type.name %}
{% if type.is_protocol %}
@protocol {{ type.name.name }}< NSObject >
{% else %}
@interface {{ type.name.name }} : {{ base_class(type=type) }}
{% endif %}
{% for method in type.body %}

- ({{ method.return_type.name }}){{ method.name -}}
{% for parameter in method.parameters %}
{% if loop.first %}
:({{ parameter.type.name }}){{ parameter.variable.name }}
{%- else %}
 {{ parameter.variable.name }}:({{ parameter.type.name }}){{ parameter.variable.name }}
{%- endif %}
{% endfor %}; {# Parameters #}

{% endfor %} {# Methods #}

@end

{% endif %} {# Type name specified #}
{% endfor %} {# Types #}