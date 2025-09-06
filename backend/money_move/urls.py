from django.contrib import admin
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    # При переходе на главную страницу проекта происходит перенаправление
    # на страницу панели администратора с записями о движении денежных средств.
    path(
        '',
        RedirectView.as_view(
            url=reverse_lazy('admin:records_record_changelist')
        ),
        name='index',
    ),
    path('admin/', admin.site.urls),
]
