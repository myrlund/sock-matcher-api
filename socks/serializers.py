from rest_framework import serializers

from .models import Sock, SockMatch, SockPreference


class SockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sock
        fields = (
            'id',
            'owner',
            'name',
            'size_description',
            'image',
            'is_rental',
            'has_match',
        )


class SockPreferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = SockPreference
        fields = (
            'source_sock',
            'target_sock',
            'preference',
            'is_match',
        )


class SockMatchSerializer(serializers.HyperlinkedModelSerializer):

    winner_sock = SockSerializer()
    loser_sock = SockSerializer()

    class Meta:
        model = SockMatch
        fields = (
            'winner_sock',
            'loser_sock',
        )
