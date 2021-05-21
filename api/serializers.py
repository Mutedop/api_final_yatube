from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Post, Comment, Group, User, Follow


class PostSerializer(serializers.ModelSerializer):
    """Serializer class for Posts."""
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Serializer class for Comments."""
    author = serializers.SlugRelatedField(
        many=False,
        slug_field='username',
    )
    post = serializers.SlugRelatedField(
        slug_field='id',
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post', )


class GroupSerializer(serializers.ModelSerializer):
    """Serializer class for Group."""
    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """
    Serializer class for Follow.

    We use UniqueTogetherValidator.
    The class always imposes an implicit constraint that all fields it applies
    to are always treated as required. Fields with default values are an
    exception because they always provide a value, even if they are
    omitted from user input.

    The user field cannot be set directly by the user,
    the views of the current user are set,
    but will be used in the output view of the serializer.
    """
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    def validate_following(self, following):
        """Field level validation - "following"."""
        if self.context.get('request').method == 'POST':
            if following is None:
                raise serializers.ValidationError(
                    'ERROR: Ошибка при оформлении подписки'
                )
            if self.context.get('request').user == following:
                raise serializers.ValidationError(
                    'ERROR: попытка подписаться на самого себя'
                )
        return following

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
            )
        ]
