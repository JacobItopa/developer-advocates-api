from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Advocate, Company
from .serializers import AdvocateSerializer, CompanySerializer
from django.db.models import Q
# Create your views here.
@api_view(['GET'])
def endpoint(request):
    data = ['advocates/', 'advocates/:username/']
    return Response(data)

@api_view(['GET', 'POST'])
def advocate_list(request):
    #data = ['Jay', 'Dennis', 'John']
    if request.method == 'GET':
        query = request.GET.get('query')
        if query == None:
            query = ''
        advocate = Advocate.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))
        serializer = AdvocateSerializer(advocate, many=True)
        return Response(serializer.data)
        
    if request.method=='POST':
        advocate=Advocate.objects.create(username=request.data['username'], bio=request.data['bio'])
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def advocate_detail(request, username):
    advocate = Advocate.objects.get(username=username)
    if request.method=='GET':
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    if request.method == 'PUT':
        advocate.username = request.data['username']
        advocate.bio = request.data['bio']
        advocate.save()
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    if request.method == 'DELETE':
        advocate.delete()
        return Response('user was deleted')

@api_view(['GET'])
def company_list(request):
    company = Company.objects.all()
    serializer = CompanySerializer(company, many=True)
    return Response(serializer.data)