# from django.http import JsonResponse
# from .models import Order

# VALID_PIZZA_TYPES = ['Burger','Pizza','Maggi','Coffee']

# def home(request):
#     return JsonResponse({
#         'message': 'Welcome to the Pizza Ordering App!',
#         'available_pizzas': VALID_PIZZA_TYPES
#     })


# def place_order(request):
#     if request.method == 'POST':
#         customer_name = request.POST.get('customer_name')
#         pizza_type = request.POST.get('pizza_type')
#         quantity = request.POST.get('quantity')
        

#         if not (customer_name and pizza_type and quantity):
#             return JsonResponse({'error': 'All fields are required.'}, status=400)

#         try:
#             quantity = int(quantity)
#             if quantity <= 0:
#                 return JsonResponse({'error': 'Quantity must be a positive number.'}, status=400)
#             if quantity > 50:  # This line should catch quantity=60
#                 return JsonResponse({'error': 'Quantity cannot exceed 50.'}, status=400)
#         except ValueError:
#             return JsonResponse({'error': 'Quantity must be a number.'}, status=400)

#         if pizza_type not in VALID_PIZZA_TYPES:
#             return JsonResponse({
#                 'error': 'Order not available yet.',
#                 'message': f"'{pizza_type}' is not available. Available options are: {', '.join(VALID_PIZZA_TYPES)}.",
#                 'retry': True,
#             }, status=400)

#         order = Order.objects.create(
#             customer_name=customer_name,
#             pizza_type=pizza_type,
#             quantity=quantity
#         )
#         return JsonResponse({
#             'message': 'Order placed successfully!',
#             'order_id': order.id
#         }, status=201)

#     return JsonResponse({'error': 'Invalid request method.'}, status=405)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer
from .serializers import UserLoginSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token  


# Define valid pizza types
VALID_PIZZA_TYPES = ['Margherita', 'Pepperoni', 'BBQ Chicken', 'Veggie', 'Cheese']

class PlaceOrderAPIView(APIView):
    def post(self, request):
        customer_name = request.data.get('customer_name')
        pizza_type = request.data.get('pizza_type')
        quantity = request.data.get('quantity')

        if not (customer_name and pizza_type and quantity):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                return Response({'error': 'Quantity must be a positive number.'}, status=status.HTTP_400_BAD_REQUEST)
            if quantity > 50:
                return Response({'error': 'Quantity cannot exceed 50.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Quantity must be a number.'}, status=status.HTTP_400_BAD_REQUEST)

        if pizza_type not in VALID_PIZZA_TYPES:
            return Response({
                'error': 'Order not available yet.',
                'message': f"'{pizza_type}' is not available. Available options are: {', '.join(VALID_PIZZA_TYPES)}.",
                'retry': True,
            }, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            customer_name=customer_name,
            pizza_type=pizza_type,
            quantity=quantity
        )

        return Response({
            'message': 'Order placed successfully!',
            'order_id': order.id
        }, status=status.HTTP_201_CREATED)                                                 



class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # role = request.data.get('role')

        # if role not in ['admin', 'librarian']:
        #     return Response({"error": "Invalid role"}, status=400)

        # user = User.objects.create_user(username=username, password=password, role=role)
        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully"}, status=201)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {"token": token.key, "message": "Login successful!"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        try:
            token = Token.objects.get(key=request.auth.key)
            token.delete() 
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)