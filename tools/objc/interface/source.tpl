//------------------------------------------------------------------------------
//
//  Copyright (c) 2016 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------
{% import 'macros.tpl' as macros %}

{% for dependency in config.dependencies %}
#import "{{ dependency }}"
{% endfor %}

@interface {{ type.name.objc_name }}(){{ macros.interfaces_list(type=type) }}
{
{% if type.has_private %}
    {{ type.name.cpp_type }}Private _common;
{% else %}
    {{ type.name.cpp_type }} _common;
{% endif %}
{% if type.is_sink %}
    GlyCommonSink* _commonSink;
{% endif %}
}
@end

@implementation {{ type.name.objc_name }}

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

{{ macros.methods_impl(type=type) -}}

{% for interface in type.interfaces %}
{{ macros.methods_impl(type=interface) -}}
{%- endfor %}
{% if type.is_sink %}
{% include "sink.tpl" %}


{% endif %}
@end