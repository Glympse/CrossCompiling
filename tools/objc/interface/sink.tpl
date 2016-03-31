#pragma mark - {{ config.params.sink.source }}

- (BOOL)addListener:(id<{{ config.params.sink.listener }}>)listener
{
    return [_commonSink addListener:listener];
}

- (BOOL)removeListener:(id<{{ config.params.sink.listener }}>)listener
{
    return [_commonSink removeListener:listener];
}
