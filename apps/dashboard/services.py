def env_key(group, request):
    match = getattr(request, 'resolver_match', None)
    env_id = match.kwargs.get('env_id') if match else None
    if env_id is None:
        # No env_id -> disallow this endpoint
        raise ValueError("env_id is required for rate limiting key")
    return f"env:{env_id}"
