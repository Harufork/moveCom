from django.contrib import admin
from django.urls import path, include
from moving_company.views import HomePageView, FaqView, NavigationView
from users.views import registration, NotifictionViewList, EmployeeRoleViewList, EmployeeRoleView, EmployeeRoleCreate,\
    EmployeeRoleChange, EmployeeRoleDelete, \
    ProfileViewList, ProfileView, ProfileCreate, ProfileChange, ProfileDelete,\
    EmployeeView, EmployeeChange, EmployeeDelete, EmployeeViewList, EmployeeCreate, \
    GroupView, GroupChange, GroupDelete, GroupViewList, GroupCreate, \
    UserView, UserChange, UserDelete, UserViewList, UserCreate
from packing.views import \
    TypePackingViewList, TypePackingView, TypePackingCreate, TypePackingChange, TypePackingDelete,\
    MeasurementViewList, MeasurementView, MeasurementCreate, MeasurementChange, MeasurementDelete,\
    PackingViewList, PackingView, PackingCreate, PackingChange, PackingDelete
from transport.views import \
    ModeTransportChange, ModeTransportView, ModeTransportCreate, ModeTransportDelete, ModeTransportViewList, \
    TransportView, TransportChange, TransportCreate, TransportDelete, TransportViewList
from pricelist.views import \
    PriceModeTDistanceChange, PriceModeTDistanceCreate, PriceModeTDistanceDelete, PriceModeTDistanceView, PriceModeTDistanceViewList,\
    PriceModeTransportChange, PriceModeTransportCreate, PriceModeTransportDelete, PriceModeTransportView, PriceModeTransportViewList, \
    PricePackingView, PricePackingChange, PricePackingCreate, PricePackingDelete, PricePackingViewList, \
    PriceRoleView, PriceRoleChange, PriceRoleCreate, PriceRoleDelete, PriceRoleViewList
from orders.views import \
    MoveAssistanceRequestViewList, MoveAssistanceRequestView, MoveAssistanceRequestCreate, MoveAssistanceRequestChange, MoveAssistanceRequestDelete,\
    MoveRequestViewList, MoveRequestView, MoveRequestCreate, MoveRequestChange, MoveRequestDelete, \
    MoveOrderViewList, MoveOrderView, MoveOrderCreate, MoveOrderChange, MoveOrderDelete,\
    new_request_move,\
    get_move_order_from_request, ThankForOrder, confirm_move_order, rejection_move_request,\
    cancel_move_order, calc_total_cost_of_move_order, in_progress_move_order,\
    completed_move_order, \
    EmployeeForMoveView, EmployeeForMoveChange, EmployeeForMoveDelete, EmployeeForMoveViewList, EmployeeForMoveCreate,\
    TransportForMoveViewList, TransportForMoveView, TransportForMoveCreate, TransportForMoveChange, TransportForMoveDelete,\
    PackingForMoveViewList, PackingForMoveView, PackingForMoveCreate, PackingForMoveChange, PackingForMoveDelete,\
    RouteMoveViewList, RouteMoveView, RouteMoveCreate, RouteMoveChange, RouteMoveDelete,\
    EmployeeForMoveRequestViewList, EmployeeForMoveRequestView, EmployeeForMoveRequestCreate, EmployeeForMoveRequestChange, EmployeeForMoveRequestDelete,\
    TransportForMoveRequestViewList, TransportForMoveRequestView, TransportForMoveRequestCreate, TransportForMoveRequestChange, TransportForMoveRequestDelete, \
    MoveOrderViewListForExecution, MoveOrderViewForExecution, MoveRequestViewListForConfirm

# TODO: Разбить урлки по приложениям, а не как сечас в одной куче
urlpatterns = [
    path('notification_list/', NotifictionViewList.as_view(), name='notification_list'),

    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('navigation/', NavigationView.as_view(), name='navigation'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('registration/', registration, name='registration'),
    path('new-request-move/', new_request_move, name='newrequestmove'),
    path('thank/', ThankForOrder.as_view(), name='thank_for_order'),

    # packing
    path('type-packing/<int:pk>/', TypePackingView.as_view(), name='typepacking'),
    path('type-packing/<int:pk>/change/', TypePackingChange.as_view(), name='change_typepacking'),
    path('type-packing/<int:pk>/delete/', TypePackingDelete.as_view(), name='delete_typepacking'),
    path('type-packing-list/', TypePackingViewList.as_view(), name='typepacking_list'),
    path('type-packing/add/', TypePackingCreate.as_view(), name='add_typepacking'),

    path('measurement/<int:pk>', MeasurementView.as_view(), name='measurement'),
    path('measurement/<int:pk>/change/', MeasurementChange.as_view(), name='change_measurement'),
    path('measurement/<int:pk>/delete/', MeasurementDelete.as_view(), name='delete_measurement'),
    path('measurement-list/', MeasurementViewList.as_view(), name='measurement_list'),
    path('measurement/add/', MeasurementCreate.as_view(), name='add_measurement'),

    path('packing/<int:pk>', PackingView.as_view(), name='packing'),
    path('packing/<int:pk>/change/', PackingChange.as_view(), name='change_packing'),
    path('packing/<int:pk>/delete/', PackingDelete.as_view(), name='delete_packing'),
    path('packing-list/', PackingViewList.as_view(), name='packing_list'),
    path('packing/add/', PackingCreate.as_view(), name='add_packing'),

    # transport
    path('modetransport/<int:pk>', ModeTransportView.as_view(), name='modetransport'),
    path('modetransport/<int:pk>/change/', ModeTransportChange.as_view(), name='change_modetransport'),
    path('modetransport/<int:pk>/delete/', ModeTransportDelete.as_view(), name='delete_modetransport'),
    path('modetransport-list/', ModeTransportViewList.as_view(), name='modetransport_list'),
    path('modetransport/add/', ModeTransportCreate.as_view(), name='add_modetransport'),

    path('transport/<int:pk>', TransportView.as_view(), name='transport'),
    path('transport/<int:pk>/change/', TransportChange.as_view(), name='change_transport'),
    path('transport/<int:pk>/delete/', TransportDelete.as_view(), name='delete_transport'),
    path('transport-list/', TransportViewList.as_view(), name='transport_list'),
    path('transport/add/', TransportCreate.as_view(), name='add_transport'),

    # price-list
    path('pricerole/<int:pk>', PriceRoleView.as_view(), name='pricerole'),
    path('pricerole/<int:pk>/change/', PriceRoleChange.as_view(), name='change_pricerole'),
    path('pricerole/<int:pk>/delete/', PriceRoleDelete.as_view(), name='delete_pricerole'),
    path('pricerole-list/', PriceRoleViewList.as_view(), name='pricerole_list'),
    path('pricerole/add/', PriceRoleCreate.as_view(), name='add_pricerole'),

    path('pricemodetransport/<int:pk>', PriceModeTransportView.as_view(), name='pricemodetransport'),
    path('pricemodetransport/<int:pk>/change/', PriceModeTransportChange.as_view(), name='change_pricemodetransport'),
    path('pricemodetransport/<int:pk>/delete/', PriceModeTransportDelete.as_view(), name='delete_pricemodetransport'),
    path('pricemodetransport-list/', PriceModeTransportViewList.as_view(), name='pricemodetransport_list'),
    path('pricemodetransport/add/', PriceModeTransportCreate.as_view(), name='add_pricemodetransport'),

    path('pricemodetdistance/<int:pk>', PriceModeTDistanceView.as_view(), name='pricemodetdistance'),
    path('pricemodetdistance/<int:pk>/change/', PriceModeTDistanceChange.as_view(), name='change_pricemodetdistance'),
    path('pricemodetdistance/<int:pk>/delete/', PriceModeTDistanceDelete.as_view(), name='delete_pricemodetdistance'),
    path('pricemodetdistance-list/', PriceModeTDistanceViewList.as_view(), name='pricemodetdistance_list'),
    path('pricemodetdistance/add/', PriceModeTDistanceCreate.as_view(), name='add_pricemodetdistance'),

    path('pricepacking/<int:pk>', PricePackingView.as_view(), name='pricepacking'),
    path('pricepacking/<int:pk>/change/', PricePackingChange.as_view(), name='change_pricepacking'),
    path('pricepacking/<int:pk>/delete/', PricePackingDelete.as_view(), name='delete_pricepacking'),
    path('pricepacking-list/', PricePackingViewList.as_view(), name='pricepacking_list'),
    path('pricepacking/add/', PricePackingCreate.as_view(), name='add_pricepacking'),

    # orders
    path('moveassistancerequest/<int:pk>', MoveAssistanceRequestView.as_view(), name='moveassistancerequest'),
    path('moveassistancerequest/<int:pk>/change/', MoveAssistanceRequestChange.as_view(), name='change_moveassistancerequest'),
    path('moveassistancerequest/<int:pk>/delete/', MoveAssistanceRequestDelete.as_view(), name='delete_moveassistancerequest'),
    path('moveassistancerequest-list/', MoveAssistanceRequestViewList.as_view(), name='moveassistancerequest_list'),
    path('moveassistancerequest/add/', MoveAssistanceRequestCreate.as_view(), name='add_moveassistancerequest'),

    path('moverequest/<int:pk>', MoveRequestView.as_view(), name='moverequest'),
    path('moverequest/<int:pk>/change/', MoveRequestChange.as_view(), name='change_moverequest'),
    path('moverequest/<int:pk>/delete/', MoveRequestDelete.as_view(), name='delete_moverequest'),
    path('moverequest-list/', MoveRequestViewList.as_view(), name='moverequest_list'),
    path('moverequest/add/', MoveRequestCreate.as_view(), name='add_moverequest'),

    path('moverequest/create_move_order/', get_move_order_from_request, name='get_move_order_from_request'),
    path('moverequest/rejection_move_request/', rejection_move_request, name='rejection_move_request'),

    path('moverequest-list-for-confirm/', MoveRequestViewListForConfirm.as_view(), name='moverequest_list_for_confirm'),

    path('moveorder/<int:pk>', MoveOrderView.as_view(), name='moveorder'),
    path('moveorder/<int:pk>/change/', MoveOrderChange.as_view(), name='change_moveorder'),
    path('moveorder/<int:pk>/delete/', MoveOrderDelete.as_view(), name='delete_moveorder'),
    path('moveorder-list/', MoveOrderViewList.as_view(), name='moveorder_list'),
    path('moveorder/add/', MoveOrderCreate.as_view(), name='add_moveorder'),

    path('moveorder_executor_list/', MoveOrderViewListForExecution.as_view(), name='moveorder_executor_list'),
    path('moveorder_executor_view/<int:pk>', MoveOrderViewForExecution.as_view(), name='moveorder_executor_view'),

    path('moveorder/completed_move_order/', completed_move_order, name='completed_move_order'),
    path('moveorder/in_progress_move_order/', in_progress_move_order, name='in_progress_move_order'),
    path('moveorder/confirm_move_order/', confirm_move_order, name='confirm_move_order'),
    path('moveorder/cancel_move_order/', cancel_move_order, name='cancel_move_order'),
    path('moveorder/calc_total_cost_of_move_order/', calc_total_cost_of_move_order, name='calc_total_cost_of_move_order'),

    path('employeeformove/<int:pk>', EmployeeForMoveView.as_view(), name='employeeformove'),
    path('employeeformove/<int:pk>/change/', EmployeeForMoveChange.as_view(), name='change_employeeformove'),
    path('employeeformove/<int:pk>/delete/', EmployeeForMoveDelete.as_view(), name='delete_employeeformove'),
    path('employeeformove-list/', EmployeeForMoveViewList.as_view(), name='employeeformove_list'),
    path('employeeformove/add/', EmployeeForMoveCreate.as_view(), name='add_employeeformove'),

    path('transportformove/<int:pk>', TransportForMoveView.as_view(), name='transportformove'),
    path('transportformove/<int:pk>/change/', TransportForMoveChange.as_view(), name='change_transportformove'),
    path('transportformove/<int:pk>/delete/', TransportForMoveDelete.as_view(), name='delete_transportformove'),
    path('transportformove-list/', TransportForMoveViewList.as_view(), name='transportformove_list'),
    path('transportformove/add/', TransportForMoveCreate.as_view(), name='add_transportformove'),

    path('packingformove/<int:pk>', PackingForMoveView.as_view(), name='packingformove'),
    path('packingformove/<int:pk>/change/', PackingForMoveChange.as_view(), name='change_packingformove'),
    path('packingformove/<int:pk>/delete/', PackingForMoveDelete.as_view(), name='delete_packingformove'),
    path('packingformove-list/', PackingForMoveViewList.as_view(), name='packingformove_list'),
    path('packingformove/add/', PackingForMoveCreate.as_view(), name='add_packingformove'),

    path('routemove/<int:pk>', RouteMoveView.as_view(), name='routemove'),
    path('routemove/<int:pk>/change/', RouteMoveChange.as_view(), name='change_routemove'),
    path('routemove/<int:pk>/delete/', RouteMoveDelete.as_view(), name='delete_routemove'),
    path('routemove-list/', RouteMoveViewList.as_view(), name='routemove_list'),
    path('routemove/add/', RouteMoveCreate.as_view(), name='add_routemove'),

    path('employeeformoverequest/<int:pk>', EmployeeForMoveRequestView.as_view(), name='employeeformoverequest'),
    path('employeeformoverequest/<int:pk>/change/', EmployeeForMoveRequestChange.as_view(), name='change_employeeformoverequest'),
    path('employeeformoverequest/<int:pk>/delete/', EmployeeForMoveRequestDelete.as_view(), name='delete_employeeformoverequest'),
    path('employeeformoverequest-list/', EmployeeForMoveRequestViewList.as_view(), name='employeeformoverequest_list'),
    path('employeeformoverequest/add/', EmployeeForMoveRequestCreate.as_view(), name='add_employeeformoverequest'),

    path('transportformoverequest/<int:pk>', TransportForMoveRequestView.as_view(), name='transportformoverequest'),
    path('transportformoverequest/<int:pk>/change/', TransportForMoveRequestChange.as_view(), name='change_transportformoverequest'),
    path('transportformoverequest/<int:pk>/delete/', TransportForMoveRequestDelete.as_view(), name='delete_transportformoverequest'),
    path('transportformoverequest-list/', TransportForMoveRequestViewList.as_view(), name='transportformoverequest_list'),
    path('transportformoverequest/add/', TransportForMoveRequestCreate.as_view(), name='add_transportformoverequest'),

    #personal
    path('employeerole/<int:pk>', EmployeeRoleView.as_view(), name='employeerole'),
    path('employeerole/<int:pk>/change/', EmployeeRoleChange.as_view(), name='change_employeerole'),
    path('employeerole/<int:pk>/delete/', EmployeeRoleDelete.as_view(), name='delete_employeerole'),
    path('employeerole-list/', EmployeeRoleViewList.as_view(), name='employeerole_list'),
    path('employeerole/add/', EmployeeRoleCreate.as_view(), name='add_employeerole'),

    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/change/', ProfileChange.as_view(), name='change_profile'),
    path('profile/<int:pk>/delete/', ProfileDelete.as_view(), name='delete_profile'),
    path('profile-list/', ProfileViewList.as_view(), name='profile_list'),
    path('profile/add/', ProfileCreate.as_view(), name='add_profile'),

    path('employee/<int:pk>', EmployeeView.as_view(), name='employee'),
    path('employee/<int:pk>/change/', EmployeeChange.as_view(), name='change_employee'),
    path('employee/<int:pk>/delete/', EmployeeDelete.as_view(), name='delete_employee'),
    path('employee-list/', EmployeeViewList.as_view(), name='employee_list'),
    path('employee/add/', EmployeeCreate.as_view(), name='add_employee'),

    path('group/<int:pk>', GroupView.as_view(), name='group'),
    path('group/<int:pk>/change/', GroupChange.as_view(), name='change_group'),
    path('group/<int:pk>/delete/', GroupDelete.as_view(), name='delete_group'),
    path('group-list/', GroupViewList.as_view(), name='group_list'),
    path('group/add/', GroupCreate.as_view(), name='add_group'),

    path('user/<int:pk>', UserView.as_view(), name='user'),
    path('user/<int:pk>/change/', UserChange.as_view(), name='change_user'),
    path('user/<int:pk>/delete/', UserDelete.as_view(), name='delete_user'),
    path('user-list/', UserViewList.as_view(), name='user_list'),
    path('user/add/', UserCreate.as_view(), name='add_user'),

    path('accounts/', include('django.contrib.auth.urls')),
]
