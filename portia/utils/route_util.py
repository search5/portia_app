def is_authenticated(user):
    if callable(user.is_authenticated):
        return user.is_authenticated()
    else:
        return user.is_authenticated


def associations(user, strategy):
    user_associations = strategy.storage.user.get_social_auth_for_user(user)
    if hasattr(user_associations, 'all'):
        user_associations = user_associations.all()
    return list(user_associations)


def common_context(authentication_backends, strategy, user=None, **extra):
    """Common view context"""
    context = {
        'user': user,
        'associated': {}
    }

    print(user)

    if user and is_authenticated(user):
        context['associated'] = dict((association.provider, association)
                                     for association in associations(user, strategy))

    print('-' * 80)
    print(extra)
    print('-' * 80)
    return dict(context, **extra)
