from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from .serializers import UserProfileSerializer, UserPhotoSerializer
from rest_framework.permissions import IsAuthenticated
class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self, queryset=None):
        return self.request.user
    

class UserPhotoView(UpdateAPIView):
    serializer_class = UserPhotoSerializer
    permission_classes = (IsAuthenticated,)
    def get_object(self,queryset=None):
        return self.request.user