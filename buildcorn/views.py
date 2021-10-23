
"""
forms handling
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import *
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from rest_framework.permissions import IsAdminUser

User = get_user_model()


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return User.SUPER_ADMIN==request.user.user_type
class CheckListFCreateFormView(LoginRequiredMixin,generic.CreateView):
    permission_classes = (IsSuperUser,)
    template_name = "buildcron/checklist_create.html"
    form_class = CheckListCreateForm
    # context_object_name = "checklists"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.user_type=='SA':
            # return HttpResponse({"error":"You dont have permissions"})
            raise PermissionDenied()
        return super(CheckListFCreateFormView, self).dispatch(request, *args, **kwargs)
    def get_success_url(self):
        return reverse("checklist-list")

class CheckListFormView(LoginRequiredMixin,generic.ListView):
    
    template_name = "buildcron/check_list.html"
    context_object_name = "checklists"
    queryset = CheckList.objects.all()

    def get_success_url(self):
        return reverse("checklist-list")

class ChecklistDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "buildcron/checklist_detail.html"
    context_object_name = "checklist"
    queryset = CheckList.objects.all()

    def get_success_url(self):
        return reverse("buildcron:checklist-list")