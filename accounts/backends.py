from django.contrib.auth import backends, get_user_model
from django.db.models import Q
from .models import User



class ModelBackend(backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # print(username, password)
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
            # print(username)
        try:
            # print(username)
            user = User.objects.get(Q(email__iexact=username) | Q(phone_number__iexact=username))
            # print(user, password)
        except User.DoesNotExist:
            User().set_password(password)
        else:
            # print(user.check_password(password))
            if user.check_password(password) and self.user_can_authenticate(user):
                # print(".......",user, password)
                return user
        return super().authenticate(request, username, password, **kwargs)