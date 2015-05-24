import bottle

def authenticator(sessions, login_url='/login'):
    '''Create an authenticator decorator.

    :param session: A session manager class to be used for storing
            and retrieving session data.  Probably based on
            :class:`BaseSession`.
    :param login_url: The URL to redirect to if a login is required.
            (default: ``'/login'``).
    '''
    def valid_admin(login_url=login_url):
        def decorator(handler, *a, **ka):
            import functools

            @functools.wraps(handler)
            def check_auth(*a, **ka):
                try:
                    cookie = bottle.request.get_cookie("session")
                    username = sessions.get_username(cookie)
                    admin = sessions.get_admin(cookie)
                    url = None
                    if not username:
                        url = login_url
                        raise KeyError
                    if not admin:
                        url = '/welcome'
                        raise TypeError
                except (KeyError, TypeError):
                    bottle.redirect(url)

                return handler(*a, **ka)
            return check_auth
        return decorator
    return valid_admin


def authenticator_user(sessions, login_url='/login'):
    '''Create an authenticator decorator.

    :param session
    :param login_url: The URL to redirect to if a login is required.
            (default: ``'/login'``).
    '''
    def valid_user(login_url=login_url):
        def decorator(handler, *a, **ka):
            import functools

            @functools.wraps(handler)
            def check_auth(*a, **ka):
                try:
                    cookie = bottle.request.get_cookie("session")
                    username = sessions.get_username(cookie)
                    if not username:
                        raise KeyError
                except (KeyError, TypeError):
                    bottle.redirect(login_url)

                return handler(*a, **ka)
            return check_auth
        return decorator
    return valid_user


