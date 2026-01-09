class CredentialsException(Exception):
    pass


class InactiveUser(Exception):
    pass


class UserUnauthorized(Exception):
    pass


class AccessDenied(Exception):
    pass