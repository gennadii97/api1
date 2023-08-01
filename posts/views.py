from django.db.models import Count
from rest_framework import generics
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from datetime import datetime
from .models import Posts, Like
from .serializers import PostsSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class PostAPIList(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PostAPIDestroy(generics.DestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = (IsAuthenticated,)



class PostLikeView(APIView):

    def get(self, request, pk):
        if request.user.is_authenticated:
            post = get_object_or_404(Posts, id=pk)
            if request.user in post.liked_by.all():
                post.liked_by.remove(request.user)
            else:
                post.liked_by.add(request.user)
            post.save()
            return Response({'success': True})
        else:
            return Response({'success': False})


class AnalyticView(GenericAPIView):
    queryset = Like.objects.all()

    def get_queryset(self, date_from, date_to):
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
            date_to = datetime.strptime(date_to, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        queryset = Like.objects.filter(created_time__gte=date_from, created_time__lte=date_to).order_by('created_time')
        return queryset

    def get(self, request):
        queryset = self.get_queryset(request.query_params['date_from'], request.query_params['date_to'])
        grouped_by = self.filter_queryset(queryset).values('created_time__date').annotate(
            total_likes=Count('id')).values('post_id', 'created_time__date', 'total_likes').order_by(
            'created_time__date')

        return Response(grouped_by)


class LastLogin(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            last_login = user.last_login.strftime('%y-%m-%d %a %H:%M:%S')
            return Response({'last_login': last_login})
        else:
            return Response({'success': False})
