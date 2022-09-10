from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from api.views import BaseGraphQLView

urlpatterns = [
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path("graphql", csrf_exempt(BaseGraphQLView.as_view(graphiql=True))),
]
