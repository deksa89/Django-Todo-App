from django.urls import path
#from .views import Register # <= ovo je za class based views
# from django.contrib.auth.views import LogoutView
from . import views  # <= ovo je za function based views


#------------------------- FUNCTION BASED VIEWS -------------------------

urlpatterns = [
    path('', views.errand_list, name="errands"),
    path('detail/<int:pk>/', views.errand_detail, name="detail"), # uvjek stavi slash "/" na kraju path-a
    path('create-task/', views.errand_create, name="create"),  # ako uneses promjene u model, obavezno napravi makemigration i migrate
    path('update-task/<int:pk>', views.errand_update, name="update"),
    path('delete-task/<int:pk>', views.errand_delete, name="delete"),
    path('login/', views.errand_login, name="login"),
    path('logout/', views.errand_logout, name="logout"),
    path('register/', views.errand_register, name="register"),
    path('github/login/', views.github_login, name='github_login'),
    path('callback/', views.github_callback, name='github_callback'),
    path('google/login/', views.google_login, name='google_login'),
    path('accounts/google/login/callback/', views.google_callback, name='google_callback'),
]


#-------------------------- CLASS BASED VIEWS ---------------------------

# urlpatterns = [
#     path('', ErrandList.as_view(), name="errands"),
#     path('detail/<int:pk>/', ErrandDetail.as_view(), name="detail"),
#     path('create-task/', ErrandCreate.as_view(), name="create"),
#     path('update-task/<int:pk>', ErrandUpdate.as_view(), name="update"),
#     path('delete-task/<int:pk>', ErrandDelete.as_view(), name="delete"),
#     path('login/', Login.as_view(), name="login"),
#     path('logout/', LogoutView.as_view(next_page="login"), name="logout"),
#     path('register/', Register.as_view(), name="register"),
# ]