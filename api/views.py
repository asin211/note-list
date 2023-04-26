from django.shortcuts import render
from .models import Note

from rest_framework.response import Response    # using django rest framework
from rest_framework.decorators import api_view
from .serializer import NoteSerializer

# Create your views here.

#  without rest_framework can achieve same results
# from django.http import JsonResponse
# from django.core.serializers import serialize
# import json
# def getRoutes(request):
#     routes = [
#         # /notes GET / POST
#         {
#             'Endpoint': '/notes/',
#             'method': 'GET',
#             'body': None,
#             'description': 'Returns an array of notes'
#         },
#         {
#             'Endpoint': '/notes/',
#             'method': 'POST',
#             'body': {'body': ""},
#             'description': 'Creates new note with data sent in post request'
#         },
#         # /notes/<id> GET / PUT / DELETE
#         {
#             'Endpoint': '/notes/id',
#             'method': 'GET',
#             'body': None,
#             'description': 'Returns a single note object'
#         },
#         {
#             'Endpoint': '/notes/id/',
#             'method': 'PUT',
#             'body': {'body': ""},
#             'description': 'Update an existing note with data sent in put request'
#         },
#         {
#             'Endpoint': '/notes/id/',
#             'method': 'DELETE',
#             'body': None,
#             'description': 'Deletes an exiting note'
#         },
#     ]
#     # return JsonResponse(routes, safe=False, status=200)
#     serialized_notes = json.loads(serialize("json", Note.objects.all()))
#     return JsonResponse(serialized_notes, safe=False, status=200)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        # /notes GET / POST
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        # /notes/<id> GET / PUT / DELETE
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/id/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Update an existing note with data sent in put request'
        },
        {
            'Endpoint': '/notes/id/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes an exiting note'
        },
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
def getNotes(request):
    if request.method == 'GET':
        notes = Note.objects.all().order_by('-updated')
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        data = request.data
        note = Note.objects.create(
        body=data['body']
    )
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def getNote(request, pk):
    if request.method == 'GET':
        notes = Note.objects.get(id=pk)
        # param = request.GET.get('id') #getting get request parameters
        serializer = NoteSerializer(notes, many=False)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        data = request.data
        note = Note.objects.get(id=pk)
        serializer = NoteSerializer(instance=note, data=data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    
    if request.method == 'DELETE':
        note = Note.objects.get(id=pk)
        note.delete()
        return Response('Note was deleted!')
