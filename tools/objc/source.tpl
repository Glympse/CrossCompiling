//------------------------------------------------------------------------------
//
//  Copyright (c) 2016 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------
{% macro method_args(method) -%}
{% for parameter in method.parameters %}
{% if parameter.type.native %}
{{ parameter.variable.name }}
{%- else %}
Glympse::ClassBinder::unwrap({{ parameter.variable.name }})
{%- endif %}
{% if not loop.last %}, {% endif %}
{% endfor %}
{%- endmacro %}
{% macro method_call(method) -%}
    _common->{{ method.name }}({{ method_args(method=method) }})
{%- endmacro %}

{% for dependency in config.dependencies %}
#import "{{ dependency }}"
{% endfor %}

{% for type in syntax_tree.type_declarations %}
{% if type.name %}
@interface {{ type.name.name }}()
{
    Glympse::{{ type.original_name }} _common;
{% if type.is_sink %}
    GlyCommonSink* _commonSink;
{% endif %}
}
@end

@implementation {{ type.name.name }}

#pragma mark - Internals

- (id)initWithCommon:(const Glympse::GCommon &)object
{
    self = [super initWithCommon:object];
    if ( self != nil )
    {
        _common = object;
{% if type.is_sink %}
        _commonSink = [[GlyCommonSink alloc] initWithSink:_common];
{% endif %}
    }
    return self;
}

#pragma mark - {{ type.original_name }}

{% for method in type.body %}
- ({{ method.return_type.name }}){{ method.name -}}
{% for parameter in method.parameters %}
{% if loop.first %}
:({{ parameter.type.name }}){{ parameter.variable.name }}
{%- else %}
 {{ parameter.variable.name }}:({{ parameter.type.name }}){{ parameter.variable.name }}
{%- endif %}
{% endfor %}

{
{% if "void" != method.return_type %}
{% if method.return_type.native %}
    return {{ method_call(method=method) }};
{% else %}
    return Glympse::ClassBinder::bind({{ method_call(method=method) }});
{% endif %}
{% else %}
    {{ method_call(method=method) }};
{% endif %}
}

{% endfor %} {#- Methods #}
{% if type.is_sink %}
#pragma mark - GlyEventSink

- (BOOL)addListener:(id<GlyEventListener>)listener
{
    return [_commonSink addListener:listener];
}

- (BOOL)removeListener:(id<GlyEventListener>)listener
{
    return [_commonSink removeListener:listener];
}

{% endif %}
@end

{% endif %} {# Type name specified #}
{% endfor %} {# Types #}
