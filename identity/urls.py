from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("inicio/", views.dashboard, name="dashboard"),
    path("salir/", views.logout_view, name="logout"),
    path("productos/nuevo/", views.product_entry, name="product-entry"),
    path("inventario/carga-inicial/", views.inventory_load, name="inventory-load"),
    path("caja/abrir/", views.cash_open, name="cash-open"),
    path("ventas/", views.sales_counter, name="sales-counter"),
]

