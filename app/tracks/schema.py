import graphene
from graphene_django import DjangoObjectType
from .models import Track

class TrackType(DjangoObjectType):
    class Meta:
        model = Track

class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType)

    def resolve_tracks(self, info):
        return Track.objects.all()

class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        artist = graphene.String()
        album = graphene.String()
        url = graphene.String()
    # def mutate(self, info, title, album, artist, description, url):
    def mutate(self, info, **kwargs):
        track = Track(
            title=kwargs.get('title'),
            description=kwargs.get('description'),
            artist=kwargs.get('artist'),
            album=kwargs.get('album'),
            url=kwargs.get('url')
        )
        track.save()
        return CreateTrack(track=track)

class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()