from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import  NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet, UserCreateView

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

auth_router = routers.DefaultRouter()
auth_router.register(r'users', UserCreateView, basename='users')

main_api_urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]

auth_api_urlpatterns = [
    path('', include(auth_router.urls)), 
]
