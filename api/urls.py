from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from api.views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
