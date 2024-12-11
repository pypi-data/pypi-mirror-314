from rest_framework_nested import routers

from zs_utils.base_support import views


app_name = "zs_utils.base_support"

router = routers.SimpleRouter()
router.register("ticket/file", views.BaseSupportTicketMessageFileView, basename="ticket_file")
router.register("ticket", views.BaseSupportTicketView, basename="ticket")
ticket_router = routers.NestedDefaultRouter(router, "ticket", lookup="ticket")
ticket_router.register("message", views.BaseSupportTicketMessageView, basename="ticket-message")

urlpatterns = []
urlpatterns += router.urls
urlpatterns += ticket_router.urls
