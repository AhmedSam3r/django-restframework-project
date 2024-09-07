from rest_framework import permissions

from .permissions import IsStaffEdtiorPermssion
from product.validators import unique_product_title
'''
MOST PROBABLY we will need to use the staff editor permission across all our website
    so we need to move it in the api app to set ourselves for sucess
    in order to use it without issues    
'''

'''
    Mixins are really useful, they help in code maintainability
    so we can use it in different things like queryset, permissions ...etc.
'''


class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, IsStaffEdtiorPermssion]


class UserQuerySetMixing(IsStaffEdtiorPermssion):
    '''
    class UserQuerySetMixing()
        the biggest flaw here is that the class isn't in sync with the IsStaffEdtiorPermssion
        as the staff created a product even though it shouldn't be allowed class ProductCreateAPIView (UserQuerySetMixing,StaffEditorPermissionMixin, generics.CreateAPIView):
        since it doesn't have the perms_map object
    '''
    user_field = 'user'
    #we can override it in the view
    allow_staff_view = False

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args, **kwargs)
        # we won't  be able to make this check
        # Cannot apply IsStaffEdtiorPermssion on a view that does not set `.queryset` or have a `.get_queryset()` method.
        # if user.is_staff and IsStaffEdtiorPermssion().has_permission(self.request,
        #                                                              self.request.resolver_match.view_name):
        #     return qs

        if user.is_staff and self.allow_staff_view:
            return qs.filter(**lookup_data) # to make it return his items only or i can make it return qs to return all products so the staff can see it
        return qs.filter(**lookup_data)
