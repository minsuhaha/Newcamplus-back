from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer, CommentCreateSerializer, PostRetrieveSerializer
from .permissions import CustomReadOnly
from users.models import User

# Post 마이페이지 구현 token을 통해 자기가 쓴 글이 보이도록 설정


class MypagelistView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-published_date')
    permission_classes = [CustomReadOnly]
    serializer_class = PostRetrieveSerializer

    # 로그인된 유저가 쓴 게시물만 보도록 filter
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user  # 로그인된 유저
        nickname = user.nickname  # 로그인된 유저의 닉네임
        return queryset.filter(author__nickname=nickname)

# 유저 대학교별 필터링된 게시물 list 보여주는 View


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-published_date')  # 작성시간 기준 최신순으로 배열
    permission_classes = [CustomReadOnly]
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'category']

    # 대학교별 필터
    def get_queryset(self):
        queryset = super().get_queryset()
        # if self.action == 'list' or 'retrieve' or 'update' or 'destory' or 'create': # crud 모든 기능에서 학교별 필터링 적용하기
        user = self.request.user  # 로그인된 유저
        university = user.university  # 로그인된 유저의 대학교
        return queryset.filter(author__university=university)

# Post 상세페이지


class PostRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [CustomReadOnly]
    serializer_class = PostRetrieveSerializer

# 유저 대학교별 필터링된 게시물 작성할수 있도록 만들어주는 View


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all().order_by('-published_date')  # 작성시간 기준 최신순으로 배열
    permission_classes = [CustomReadOnly]
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        # if self.action == 'list' or 'retrieve' or 'update' or 'destory' or 'create': # crud 모든 기능에서 학교별 필터링 적용하기
        user = self.request.user  # 로그인된 유저
        university = user.university  # 로그인된 유저의 대학교
        return queryset.filter(author__university=university)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [CustomReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CommentSerializer
        return CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
