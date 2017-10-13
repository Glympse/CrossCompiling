//------------------------------------------------------------------------------
//
//  Copyright (c) 2016 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------

{% for type in package.additional_types %}
@class {{ type }};
{% endfor %}
{% for type in package.types %}
{% if type.is_protocol %}
@protocol
{%- else %}
@class
{%- endif %}
 {{ type.name.objc_name }};
{% endfor %}

{% for type in package.additional_types %}
#import "{{ type }}.h"
{% endfor %}
{% for type in package.types %}
#import "{{ type.name.objc_name }}.h"
{% endfor %}
