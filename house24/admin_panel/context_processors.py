from django.contrib.auth import get_user_model


User = get_user_model()


def add_new_users_to_template(request):
    """
    This function send "new_users_query" and "new_users_count" variables to each template.
    """
    new_users = User.objects.filter(status=1)
    return {
        'new_users_query': new_users,
        'new_users_count': new_users.count()
    }
