from django.contrib.auth.mixins import AccessMixin

class AdminRequiredMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.user_role=='auth':
            return self.handle_no_permission()

        return super().dispatch(request,*args,**kwargs)

class celertRequiredMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.user_role=='dashboard':
            return self.handle_no_permission()

        return super().dispatch(request,*args,**kwargs)

class clientRequiredMixin(AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.user_role=='front':
            return self.handle_no_permission()

        return super().dispatch(request,*args,**kwargs)