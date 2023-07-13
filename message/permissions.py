from django.contrib.auth.models import Permission
class CanViewOwnGroup(Permission):
       """
       Custom permission class to allow users to view only their own groups
       """
       def has_object_permission(self, request, view, obj):
           if request.user.is_authenticated and obj.created_by == request.user:
               return True
           return False