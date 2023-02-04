from rest_framework import serializers
from .models import Post, Comment
from users.serializers import UserInfoSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    # author = UserInfoSerializer()

    class Meta:
        model = Comment
        fields = ("pk", "author", "post", "text")

    def get_author(self, obj):
        return UserInfoSerializer(obj.author).data


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post", "text")

# Post 전체목록 댓글이 보이지 않도록 설정


class PostSerializer(serializers.ModelSerializer):
    # 작성한 유저 닉네임이 함께 보이도록 설정
    author = serializers.SerializerMethodField()
    # author = UserInfoSerializer()

    class Meta:
        model = Post
        fields = ("pk", "author", "title", "category",
                  "body", "location",  "published_date")

    def get_author(self, obj):
        return UserInfoSerializer(obj.author).data

    # def get_univ(self, obj):
    #     return obj.university.university


# Post 세부목록(상세페이지) 이때만 댓글이 같이 보이도록 설정
class PostRetrieveSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("pk", "author", "title", "category", "body",
                  "location", "published_date", "comments")

    def get_author(self, obj):
        return UserInfoSerializer(obj.author).data


# Post 작성
class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("title", "category", "location", "body")
