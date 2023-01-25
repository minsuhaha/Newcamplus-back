from django.urls import path
from .views import RegisterView, LoginView, UserActivate,  RegisterView  # ,SignUpView

app_name = 'user'

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('activate/<str:uidb64>/<str:token>',
         UserActivate.as_view(), name='activate')
]
