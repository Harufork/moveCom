from django.contrib import admin
from django.urls import path, include
from moving_company.views import HomePageView, FaqView, NavigationView
from users.views import Registration
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
    new_request_move, ThankForOrder

# TODO: Разбить урлки по приложениям, а не как сечас в одной куче
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('navigation/', NavigationView.as_view(), name='navigation'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('registration/', Registration.as_view(), name='registration'),
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

    path('moveorder/<int:pk>', MoveOrderView.as_view(), name='moveorder'),
    path('moveorder/<int:pk>/change/', MoveOrderChange.as_view(), name='change_moveorder'),
    path('moveorder/<int:pk>/delete/', MoveOrderDelete.as_view(), name='delete_moveorder'),
    path('moveorder-list/', MoveOrderViewList.as_view(), name='moveorder_list'),
    path('moveorder/add/', MoveOrderCreate.as_view(), name='add_moveorder'),

    path('accounts/', include('django.contrib.auth.urls')),
]
