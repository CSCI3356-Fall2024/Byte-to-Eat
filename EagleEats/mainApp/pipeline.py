from django.shortcuts import redirect

def check_first_login(backend, user, response, *args, **kwargs):
    # Check if it's the first time the user is logging in
    if user and not user.is_staff and not user.last_login:
        # If it's the first time, store a flag in the session
        backend.strategy.session_set('is_first_login', True)
    else:
        backend.strategy.session_set('is_first_login', False)
