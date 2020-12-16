from django.urls import path

from . import views

app_name = 'dating'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/self/', views.QuestionSelfView.as_view(), name='detail_self'),
    path('<int:pk>/other/', views.QuestionOtherView.as_view(), name='detail_other'),    
    path('<int:question_id>/vote_self/', views.vote_self, name='vote_self'),
    path('<int:question_id>/vote_other/', views.vote_other, name='vote_other'),
    path('profile/me', views.ProfileViewSelf.as_view(), name='profile_self'),
    path('profile/testuser', views.ProfileViewOther.as_view(), name='profile_other'),
]
