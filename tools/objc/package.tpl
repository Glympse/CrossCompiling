//------------------------------------------------------------------------------
//
//  Copyright (c) 2016 Glympse Inc. All rights reserved.
//
//------------------------------------------------------------------------------

{% for type in package.types %}
@class {{ type.name.name }};
{% endfor %}

{% for type in package.types %}
#import "{{ type.name.name }}.h"
{% endfor %}