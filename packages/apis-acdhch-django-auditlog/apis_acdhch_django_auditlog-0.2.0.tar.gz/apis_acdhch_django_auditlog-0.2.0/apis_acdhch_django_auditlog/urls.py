from django.urls import path
from apis_acdhch_django_auditlog.views import AuditLog, UserAuditLog


urlpatterns = [
    path("profile/auditlog", UserAuditLog.as_view()),
    path("auditlog", AuditLog.as_view()),
]
