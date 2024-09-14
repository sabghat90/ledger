from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('orders/', views.orders, name='orders'),
    path('accounts/', views.accounts, name='accounts'),
    path('add-order/', views.add_order, name='add-order'),
    path('add-account/', views.add_account, name='add-account'),
    path('view-account/<int:pk>/', views.view_account, name='view-account'),
    path('view-order/<int:pk>/', views.view_order, name='view-order'),
    path('update-order/<int:pk>/', views.update_order, name='update-order'),
    path('update-account/<int:pk>/', views.update_account, name='update-account'),
    path('delete-order/<int:pk>/', views.delete_order, name='delete-order'),
    path('expense/', views.expense, name='expense'),
    path('add-expense/', views.add_expense, name='add-expense'),
    path('view-expense/<int:pk>/', views.view_expense, name='view-expense'),
    path('update-expense/<int:pk>/', views.update_expense, name='update-expense'),
    path('delete-expense/<int:pk>/', views.delete_expense, name='delete-expense'),
    path('agents/', views.agents, name='agents'),
    path('<int:pk>/view-agent/', views.view_agent, name='view-agent')
]
