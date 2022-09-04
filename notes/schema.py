import graphene
from django.db.models import QuerySet


class BaseQuery(graphene.ObjectType):
    def resolve(self, info, user_uid, **kwargs) -> QuerySet:
        pass


class BaseMutation(graphene.Mutation):
    class Arguments:
        pass

    def mutate(self, info) -> graphene.Mutation:
        pass


schema = graphene.Schema(query=BaseQuery, mutation=BaseMutation)
