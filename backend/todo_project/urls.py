"""
URL configuration for todo_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    """Get CSRF token for frontend"""
    return Response({'detail': 'CSRF cookie set'})

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return Response({
            'detail': 'Login successful',
            'username': user.username,
            'id': user.id
        })
    return Response({'detail': 'Invalid credentials'}, status=400)

@api_view(['POST'])
def logout_view(request):
    """Logout endpoint"""
    logout(request)
    return Response({'detail': 'Logged out'})

@api_view(['GET'])
def check_auth(request):
    """Check authentication status"""
    if request.user.is_authenticated:
        return Response({
            'authenticated': True,
            'username': request.user.username,
            'id': request.user.id
        })
    return Response({'authenticated': False}, status=401)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/csrf/', get_csrf_token),
    path('api/login/', login_view),
    path('api/logout/', logout_view),
    path('api/check/', check_auth),
    path('api/', include('todos.urls')),
]