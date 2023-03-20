#from django.shortcuts import render


# Models
from django.contrib.auth.models import User
from .models import Cuenta


# imports rest 
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status


# Decorators
from rest_framework.decorators import action

# Serializer
from .serializers import CuentaSerializer


#Other
import random

# Create your views here.
from django.core.exceptions import ObjectDoesNotExist

class CuentaAPIView(viewsets.ModelViewSet):

    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializer
    permission_classes = [permissions.IsAuthenticated]


    def create(self, request):
        data = request.data
        try:
            n_cuenta = random.randint(1000000000, 9999999999)
            user = request.user
            cuenta = Cuenta(n_cuenta = n_cuenta, saldo = data['saldo'], user = user)
            cuenta.save()
            return Response(
                {
                'status': '200',
                'message': 'Cuenta created',
                'data': {
                    'n_cuenta': cuenta.n_cuenta,
                    'user': user.email,
                    'saldo': cuenta.saldo
                    }
                },
                status= status.HTTP_201_CREATED
            )
        except ObjectDoesNotExist:
            return Response(
                {
                'status': '400',
                'message': 'Invalid request, try to send a valid user '
                },
                status= status.HTTP_400_BAD_REQUEST
            )
 
    @action(detail=False, methods=['post'])
    def manipular(self, request):
        user = request.user
        try:
            data = request.data
            cuenta = Cuenta.objects.get(n_cuenta = data['n_cuenta'])
            
            
            # Respuesta default
            respuesta = Response(
                            {
                            'status': '400',
                            'message': 'Oops something went wrong'
                            },
                            status= status.HTTP_400_BAD_REQUEST
                        ) 

            if(data.get('tipo')):
                if(data['tipo'] == 'consignar'):
                    cuenta.saldo += data['valor']
                    cuenta.save()
                    respuesta = Response(
                            {
                            'status': '200',
                            'message': 'Dinero consignado',
                            'data': {
                                'n_cuenta': cuenta.n_cuenta,
                                'user': user.email,
                                'saldo': cuenta.saldo
                                }
                            },
                            status= status.HTTP_200_OK
                        )
                elif( data['tipo'] == 'retirar'):

                    if(cuenta.user != user): 
                        respuesta = Response(
                            {
                            'status': '403',
                            'message': 'No habilitado para retirar de esta cuenta',
                            },
                            status= status.HTTP_403_FORBIDDEN
                        )
                    else:
                        if(data['valor'] <= cuenta.saldo):
                            cuenta.saldo -= data['valor']
                            cuenta.save()
                            respuesta = Response(
                                {
                                'status': '200',
                                'message': 'Cuenta created',
                                'data': {
                                    'n_cuenta': cuenta.n_cuenta,
                                    'user': user.email,
                                    'saldo': cuenta.saldo
                                    }
                                },
                                status= status.HTTP_200_OK
                            )
                        else:
                            respuesta =  Response(
                                {
                                'status': '400',
                                'message': 'Insufficient balance'
                                },
                                status= status.HTTP_400_BAD_REQUEST
                            ) 
                return respuesta
            else:
                return Response(
                    {
                    'status': '400',
                    'message': 'You must send a valid type'
                    },
                    status= status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            return Response(
                    {
                    'status': '400',
                    'message': 'You must send a valid number account'
                    },
                    status= status.HTTP_400_BAD_REQUEST
                )

    def list(self, request):
        
        user = request.user
        data = request.GET
        cuenta = Cuenta.objects.get(n_cuenta = data['n_cuenta'])
        if(user != cuenta.user):
             respuesta = Response(
                            {
                            'status': '401',
                            'message': 'No habilitado para retirar de esta cuenta',
                            },
                            status= status.HTTP_403_FORBIDDEN
                        )
        else:
            respuesta =  Response(
                    {
                    'status': '200',
                    'message': 'Bingo !',
                    'data':{
                        'n_cuenta': cuenta.n_cuenta,
                        'user': user.email,
                        'saldo': cuenta.saldo
                    }
                    },
                    status= status.HTTP_200_OK
                )
        return respuesta
    