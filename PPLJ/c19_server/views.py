from c19_server.models import Form, UserID, UserPhone
from c19_server.serializers import FormSerializer, UserIDSerializer, UserSerializer, UserPhoneSerializer
from c19_server.permissions import IsOwnerOrReadOnly, IsOwner
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, mixins
from rest_framework_extensions.mixins import NestedViewSetMixin


class ListOnlyModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


# Create your views here.
class FormViewSet(viewsets.ModelViewSet, NestedViewSetMixin):
    """
    Menyediakan fungsi 'Create', 'Retrieve', 'Update', dan 'Destroy'
    untuk form pendataan
    """
    serializer_class = FormSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Form.objects.filter(userid=self.kwargs['parent_lookup_userid'])

    def perform_create(self, serializer):
        (param1, param2, param3, param4) = self.request.POST.get('gejala_demam', False), \
                                           self.request.POST.get('usia', False), \
                                           self.request.POST.get('kontak', False), \
                                           self.request.POST.get('aktivitas', False)
        score = 0
        if param1:
            score += 3
        if param2:
            score += 1
        if param3:
            score += 2
        if param4:
            score += 1
        if score >= 5:
            return serializer.save(kategori=3, userid_id=self.kwargs['parent_lookup_userid'])
        elif score >= 3:
            return serializer.save(kategori=2, userid_id=self.kwargs['parent_lookup_userid'])
        elif score < 3:
            return serializer.save(kategori=1, userid_id=self.kwargs['parent_lookup_userid'])


class UserIDViewSet(viewsets.ModelViewSet, NestedViewSetMixin):
    """
    Menyediakan fungsi 'Create', 'Retrieve', 'Update', dan 'Destroy'
    untuk form identitas pengguna
    """
    serializer_class = UserIDSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserID.objects.filter(no_HP=self.kwargs['parent_lookup_userphone'])

    def perform_create(self, serializer):
        return serializer.save(no_HP_id=self.kwargs['parent_lookup_userphone'])


class UserPhoneViewSet(viewsets.ModelViewSet, NestedViewSetMixin):
    """
    Menyediakan fungsi 'Create', 'Retrieve', 'Update', dan 'Destroy'
    untuk nomor HP pengguna
    """
    serializer_class = UserPhoneSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return UserPhone.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Menyediakan fungsi 'list' dan 'detail' untuk user (device)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

