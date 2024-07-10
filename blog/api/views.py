from blog.models import Post, Comment

from blog.api.serializers import BlogSerializer 

from rest_framework.decorators import api_view 



from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
def blog(request, id = None):
    if request.method == 'GET':
        # id = request.GET.get('id', None)
        if id is not None:
            blog = Post.objects.get(id=id)
            serializer = BlogSerializer(blog)
            return Response(serializer.data)
        
        blog = Post.objects.all()
        serializer = BlogSerializer(blog, many=True)
        return Response(serializer.data)
        
    if request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        # id = request.data.get('id', None)
        blog = Post.objects.get(id=id)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'msg':'data updated'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PATCH':
        # id = request.data.get('id', None)
        blog = Post.objects.get(id=id)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'msg':'data patch updated'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        # id = request.data.get('id', None)
        blog = Post.objects.get(id=id)
        blog.delete()
        return Response({
            'msg':'data deleted'
        })