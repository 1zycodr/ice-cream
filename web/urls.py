from django.urls import path
from web import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.UserLoginView.as_view(), name='login'),
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path(
        'success_register',
        views.SuccessRegisterView.as_view(),
        name='register-success',
    ),

    path('cart/<int:pk>/', views.CartView.as_view(), name='cart',),
    path('cart/add/', views.AddToCartView.as_view(), name='add-to-cart',),
    path(
        'cart/remove/',
        views.RemoveFromCartView.as_view(),
        name='remove-from-cart',
    ),

    path('orders', views.OrderView.as_view(), name='orders'),
    path(
        'order/create',
        TemplateView.as_view(template_name='create-order.html'),
        name='create-order',
    ),
    path(
        'order/save',
        views.SaveOrderView.as_view(),
        name='save-order',
    ),
    path(
        'order/<int:pk>',
        views.OrderDetailsView.as_view(),
        name='order-details',
    ),
    path(
        'about',
        TemplateView.as_view(template_name='about.html'),
        name='about',
    ),
    path(
        'contacts',
        TemplateView.as_view(template_name='contact.html'),
        name='contacts',
    ),

    path('products', views.ProductView.as_view(), name='products'),
    path(
        'products/create',
        views.ProductCreateView.as_view(),
        name='create-product',
    ),
    path(
        'products/<int:pk>',
        views.ProductDetailView.as_view(),
        name='product-detail',
    ),
    path(
        'products/<int:pk>/update',
        views.ProductUpdateView.as_view(),
        name='update-product',
    ),
    path(
        'products/<int:pk>/delete',
        views.ProductDeleteView.as_view(),
        name='delete-product',
    ),
]
