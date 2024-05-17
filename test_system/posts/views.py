import httpx
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status, serializers
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist

from posts.models import Post
from posts.serializers import PostSerializer
from users_actions.models import User


class AllPostsView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get(self, request):
        all_posts_from_db = Post.objects.select_related('user').all().order_by('id')

        if not all_posts_from_db.exists():
            with httpx.Client() as client:
                response = client.get('https://jsonplaceholder.typicode.com/posts')
                return JsonResponse(response.json(), safe=False)

        posts_serializer = PostSerializer(all_posts_from_db, many=True)
        return JsonResponse(posts_serializer.data, safe=False)

    def post(self, request):
        with httpx.Client() as client:
            response = client.get('https://jsonplaceholder.typicode.com/posts')
            try:
                for row in response.json():
                    user = User.objects.get(pk=row['userId'])
                    posts = Post(user=user, title=row['title'], body=row['body'])
                    posts.save()
                return JsonResponse({'status': status.HTTP_200_OK})
            except ObjectDoesNotExist:
                res = serializers.ValidationError({'message': 'Post does not exist'})
                res.status_code = status.HTTP_404_NOT_FOUND
                raise res


class PostView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, post_id: int):
        try:
            post = Post.objects.select_related('user').get(pk=post_id)
            post_serializer = PostSerializer(post)
            return JsonResponse(post_serializer.data, safe=True)
        except ObjectDoesNotExist:
            res = serializers.ValidationError({'message': 'Post does not exist'})
            res.status_code = status.HTTP_404_NOT_FOUND
            raise res

    def delete(self, request, post_id: int):
        try:
            Post.objects.get(pk=post_id).delete()
            return JsonResponse({'status': status.HTTP_200_OK})
        except ObjectDoesNotExist:
            res = serializers.ValidationError({'message': 'Post does not exist'})
            res.status_code = status.HTTP_404_NOT_FOUND
            raise res
