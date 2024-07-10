from blog.models import Post, Comment

from blog.api.serializers import BlogSerializer 

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response




from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
# from rest_framework.permissions import IsAuthenticatedOrReadOnly 

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    
    throttle_classes = [AnonRateThrottle, UserRateThrottle, ScopedRateThrottle]


# update retrieve and destroy
class URDBlog(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogSerializer


# List and create
class LCBlogList(GenericAPIView, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = BlogSerializer 

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([])
def blog(request, id=None):
    queryset = Post.objects.all()  # Define your queryset here

    if request.method == 'GET':
        if id is not None:
            try:
                blog = queryset.get(id=id)
                serializer = BlogSerializer(blog)
                return Response(serializer.data)
            except Post.DoesNotExist:
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method in ['PUT', 'PATCH', 'DELETE']:
        try:
            blog = queryset.get(id=id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'PUT':
            serializer = BlogSerializer(blog, data=request.data)
        elif request.method == 'PATCH':
            serializer = BlogSerializer(blog, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)