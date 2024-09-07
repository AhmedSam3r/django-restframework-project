from rest_framework import permissions

class IsStaffEdtiorPermssion(permissions.DjangoModelPermissions):
    #To solve the problem of having custom permission per each view like get and post (list and create)
    # to work update the permissions of the user to staff and then
    # add permissions such as view, add ...etc.
    perms_map = {
        # 'GET': [],
        #%(app_label)s.view_%(model_name)s ==> must change the name manually to work
        #NOOOOOOOOOOOO WRONG 
        #def get_required_permissions(self, method, model_cls): map them through perm % kwargs
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],  # appname.action_modelname
        'PUT': ['%(app_label)s.change_%(model_name)s'], 
        # 'PATCH': ['%(app_label)s.change_%(model_name)s'],
        # 'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        if not request.user.is_staff:
            return False
        return super().has_permission(request, view)
    # def has_permission(self, request, view):
    #     user = request.user
    #     # return super().has_permission(request, view) #returns True
    #     print("IsStaffEdtiorPermssion\n")
    #     print(user.get_all_permissions())
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #     if request.user.is_staff:
    #         '''
    #             this part is kind of ruined as if the staff user has one of the permissions
    #             in the listcreate api the staff user will bypass any permission 
    #                 ==> due to the existence of another one
    #         '''
    #         if user.has_perm("product.view_product"): #appname.action_modelname
    #             return True
    #         if user.has_perm("product.add_product"):
    #             return True
    #         if user.has_perm("product.delete_product"):
    #             return True
    #         if user.has_perm("product.change_product"):
    #             return True
    #     return False
    
    # def has_object_permission(self, request, view, obj):
    #     return super().has_object_permission(request, view, obj)