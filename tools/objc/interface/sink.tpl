#pragma mark - GlyEventSink

- (BOOL)addListener:(id<GlyEventListener>)listener
{
    return [_commonSink addListener:listener];
}

- (BOOL)removeListener:(id<GlyEventListener>)listener
{
    return [_commonSink removeListener:listener];
}
