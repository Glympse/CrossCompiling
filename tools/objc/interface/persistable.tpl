#pragma mark - {{ config.params.persistable }}

- (void)decode:(GlyPrimitive *)decoder
{
    _common->decode(Glympse::ClassBinder::unwrap(decoder));
}

- (void)encode:(GlyPrimitive *)encoder mode:(int)mode
{
    _common->encode(Glympse::ClassBinder::unwrap(encoder), mode);
}
