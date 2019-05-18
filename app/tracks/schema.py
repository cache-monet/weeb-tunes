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
    def mutate(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Please log in to add track")
        track = Track (
            title=kwargs.get('title'),
            description=kwargs.get('description'),
            artist=kwargs.get('artist'),
            album=kwargs.get('album'),
            url=kwargs.get('url'),
            posted_by=user,
        )
        track.save()
        return CreateTrack(track=track)

class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        artist = graphene.String()
        album = graphene.String()
        url = graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user
        track = Track.objects.get(id=kwargs.get('track_id'))

        if user.is_anonymous:
            raise Exception("You must be logged in to update tracks")

        if kwargs.get('title'): track.title = kwargs.get('title')
        if kwargs.get('description'): track.description = kwargs.get('description')
        if kwargs.get('artist'): track.artist = kwargs.get('artist')
        if kwargs.get('album'): track.album = kwargs.get('album')
        if kwargs.get('url'): track.url = kwargs.get('url')

        track.save()
        return UpdateTrack(track=track)

class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()