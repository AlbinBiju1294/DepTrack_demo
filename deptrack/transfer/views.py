# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Transfer, TransferDetails
from .serializer import TransferSerializer, TransferDetailsSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Transfer, TransferDetails
from .serializer import TransferSerializer, TransferDetailsSerializer
from user.rbac import IsManagerOrDuhead;

class CreateTransferAPIView(APIView):
    permission_classes = [IsManagerOrDuhead,]

    def post(self, request):
        transfer_serializer = TransferSerializer(data=request.data)
        details_serializer = TransferDetailsSerializer(data=request.data)
        
        if transfer_serializer.is_valid() and details_serializer.is_valid():
            # Determine status based on user role
            if request.user.role_id == 2 :
                status_value = 1
            else:
                status_value = 2

            # Save the transfer with the determined status
            transfer = transfer_serializer.save(status=status_value)
            details_serializer.save(transfer=transfer)
            return Response({"message": "Transfer created successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(transfer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ListTransfersByStatusAPIView(APIView):
    permission_classes = [IsDuhead]


    def get(self, request):
        employee_id = request.user.employee_id
        employee = Employee.objects.get(id=employee_id)
        du_id = employee.department_id
        filter_value = request.query_params.get('filter_value')  # Get status value from query parameters

        if filter_value is not None:
            transfers = Transfer.objects.filter(status=filter_value,targetdu_id = du_id )
            transfer_serializer = TransferSerializer(transfers, many=True)
            return Response(transfer_serializer.data)
        else:
            return Response({"error": "Status value not provided in the query parameters"}, status=status.HTTP_400_BAD_REQUEST)
