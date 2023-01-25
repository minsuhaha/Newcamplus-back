from django.urls import path, include
from rest_framework import routers
from .views import CommentViewSet, MypagelistView, PostRetrieveView, PostListView, PostCreateView

router = routers.SimpleRouter()
# router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('mypage/', MypagelistView.as_view()),
    path('post/', PostListView.as_view()),
    path('post/<int:pk>', PostRetrieveView.as_view()),
    path('post/create/', PostCreateView.as_view()),
]
