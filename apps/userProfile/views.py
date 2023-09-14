from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from .serializers import UserProfileSerializer, UserPhotoSerializer
from rest_framework.permissions import IsAuthenticated
from apps.authentication.models import User
class RetrieveUserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self, queryset=None):
        return self.request.user
    
class RetrieveUserPhotoView(RetrieveAPIView):
    serializer_class = UserPhotoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'
    queryset = User.objects.all()

class UpdateUserPhotoView(UpdateAPIView):
    serializer_class = UserPhotoSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self,queryset=None):
        return self.request.user
    
