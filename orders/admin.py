from django.contrib import admin
from .models import MoveAssistanceRequest, AssistantForMARequest, \
    MoveRequest, MoveOrder, EmployeeForMove, TransportForMove, \
    PackingForMove, RouteMove, EmployeeForMoveRequest, TransportForMoveRequest


admin.site.register(MoveAssistanceRequest)
admin.site.register(AssistantForMARequest)

admin.site.register(MoveRequest)
admin.site.register(MoveOrder)
admin.site.register(EmployeeForMove)
admin.site.register(TransportForMove)
admin.site.register(EmployeeForMoveRequest)
admin.site.register(TransportForMoveRequest)
admin.site.register(PackingForMove)
admin.site.register(RouteMove)