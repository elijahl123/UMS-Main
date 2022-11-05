import graphene
from graphene_django import DjangoObjectType

from notes.models import Note


class NoteType(DjangoObjectType):
    class Meta:
        model = Note
        fields = (
            'uid',
            'uploaded',
            'modified',
            'course',
            'user',
            'title',
            'content'
        )
        filter_fields = [
            'uid',
            'uploaded',
            'modified',
            'course',
            'user',
            'title',
            'content'
        ]
        interfaces = (graphene.relay.Node,)

