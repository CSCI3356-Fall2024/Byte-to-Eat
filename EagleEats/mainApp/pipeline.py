def check_first_login(backend, user, response, *args, **kwargs):
    if user and not user.is_staff and not user.last_login:
        backend.strategy.session_set('is_first_login', True)
    else:
        backend.strategy.session_set('is_first_login', False)
