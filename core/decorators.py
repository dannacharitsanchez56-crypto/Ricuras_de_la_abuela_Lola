from django.contrib.auth.decorators import user_passes_test


def solo_staff(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.is_staff,
        login_url='login'
    )(view_func)