from .models import User


class OpenBackend(object):

    def authenticate(self, request, username=None, password=None):
        return User.objects.get(username=username)

    def get_user(self, user_id):
        return User.objects.filter(pk=user_id).first()
