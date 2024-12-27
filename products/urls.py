from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.ProductCreateView.as_view(), name='create'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('messages/', views.message_list, name='message_list'),
    path('get-unread-count/', views.get_unread_count, name='get_unread_count'),
    
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('<int:pk>/cart/', views.toggle_cart, name='toggle_cart'),
    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete'),
    path('<int:pk>/mark-as-sold/', views.mark_as_sold, name='mark_as_sold'),
    
    path('seller/<int:seller_id>/', views.seller_profile_view, name='seller_profile'),
    
    path('products/<int:pk>/messages/', views.message_list_create, name='messages'),
    path('<int:pk>/messages/read/', views.mark_messages_read, name='mark_messages_read'),
    
    path('<int:pk>/inquiry/', views.create_inquiry, name='create_inquiry'),
    path('<int:pk>/inquiries/', views.get_inquiries, name='get_inquiries'),
    path('<int:pk>/inquiry/<int:inquiry_id>/answer/', views.answer_inquiry, name='answer_inquiry'),
    
    path('<int:pk>/review/', views.create_review, name='create_review'),
    path('<int:pk>/review/<int:review_id>/', views.update_review, name='update_review'),
] 