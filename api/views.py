import random
import re

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from api.models import Reme

class RemeSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Reme
        fields = '__all__'

    def get_tags(self, obj):
        return obj.tags.names()


def paginate(page):
    per_page = 20
    start = per_page * page
    end = start + per_page
    return start, end


@api_view(['GET'])
def popular(request):
    page = int(request.GET.get('page', '0'))
    start, end = paginate(page)

    remes = Reme.objects.order_by("-downloads")[start:end]
    data = RemeSerializer(remes, many=True).data

    return Response(data)


@api_view(['GET'])
def recent(request):
    page = int(request.GET.get('page', '0'))
    start, end = paginate(page)

    remes = Reme.objects.order_by("-created")[start:end]
    data = RemeSerializer(remes, many=True).data

    return Response(data)


@api_view(['GET'])
def similar(request, reme_id):
    try:
        reme = Reme.objects.get(pk=reme_id)
        similar_remes = list(Reme.objects.filter(tags__name__in=reme.tags.names()).distinct())

        random_sample = random.sample(similar_remes, k=min(len(similar_remes), 10))

        data = RemeSerializer(random_sample, many=True).data
        return Response(data)
    
    except Reme.DoesNotExist:
        raise NotFound()


@api_view(['POST'])
def upload(request):
    media = request.data.get("media")
    tags = request.data.get("tags")

    if not media or not tags:
        raise ValidationError()

    reme = Reme.objects.create(media=media)
    reme.tags.add(*tags)

    data = RemeSerializer(reme).data

    return Response(data)


@api_view(['GET'])
def search(request):
    keys = request.GET.get('q', '')
    page = int(request.GET.get('page', '0'))

    if not keys:
        raise ValidationError()

    tags = [re.sub(r'\s+', ' ', a) for a in keys.split(",")]
    found_remes = Reme.objects.filter(tags__name__in=tags).distinct()

    start, end = paginate(page)
    data = RemeSerializer(found_remes[start:end], many=True).data

    return Response(data)


@api_view(['GET'])
def download(request, reme_id):
    try:
        reme = Reme.objects.get(pk=reme_id)
        reme.downloads += 1
        reme.save()

        data = RemeSerializer(reme).data

        return Response(data)
    
    except Reme.DoesNotExist:
        raise NotFound()