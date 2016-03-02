//------------------------------------------------------------------------------
//
//  Copyright (c) 2016 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------
{% import 'macros.tpl' as macros %}

{% for dependency in config.dependencies %}
#import "{{ dependency }}"
{% endfor %}

@interface {{ type.name.objc_name }}()
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

#pragma mark - {{ type.name.cpp_type }}

{% for method in type.body %}
{{ macros.method_signature(method=method) }}
{
{% if "void" != method.return_type.objc_type %}
{% if method.return_type.native %}
    return {{ macros.method_call(method=method) }};
{% else %}
    return Glympse::ClassBinder::bind({{ macros.method_call(method=method) }});
{% endif %}
{% else %}
    {{ macros.method_call(method=method) }};
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