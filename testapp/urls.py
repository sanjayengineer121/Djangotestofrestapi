
from django.urls import path,include
from .views import create
from .views import update
from .views import invoices
from .views import reciept
from . import views


urlpatterns = [
    
    path('invoices/',invoices,name='invoices'),
    path('create/',create,name='create'), 
    path('update/',update,name='update'),
    path('createinvce/', views.create_invoice, name='create_invoice'),
    path('modifyinvoice/<int:invoice_id>/', views.modify_invoice, name='modify_invoice'),
    path('invoices/<int:pk>/',reciept,name='reciept')

]
