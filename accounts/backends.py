from django.contrib.auth import backends, get_user_model
from django.db.models import Q
User = get_user_model()


class ModelBackend(backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(username, password)
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
            print(username)
        try:
            print(username)
            user = User.objects.get(Q(email__iexact=username))
        except User.DoesNotExist:
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return super().authenticate(request, username, password, **kwargs)