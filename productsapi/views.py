
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer, MedicineSerializer
from django.shortcuts import get_object_or_404
from  store .models import Medicine
from .serializers import MedicineSerializer


# API for user signup
@api_view(['POST'])
@permission_classes((AllowAny,))
def signup_view(request):
   
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create and return token for the new user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"message": "User registered successfully.", "token": token.key},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API for user login
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_view(request):
  
    try:
        data = request.data
        username = data.get("username")
        password = data.get("password")
    except Exception as e:
        return Response({'error': 'Invalid request format.'}, status=HTTP_400_BAD_REQUEST)

    if not username or not password:
        return Response({'error': 'Both username and password are required'}, status=HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Generate or retrieve the token for the authenticated user
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"message": "Login successful.", "token": token.key, "username": username},
            status=HTTP_200_OK
        )
    else:
        return Response({"error": "Invalid credentials."}, status=HTTP_401_UNAUTHORIZED)



#API FOR ADD_BOOKMARK
@api_view(['POST'])
@permission_classes([AllowAny])
def add_medicine(request):
    """
    API to add a new bookmark.
    """
    if request.method == 'POST':
        # Create a serializer with the data from the request
        serializer = MedicineSerializer(data=request.data)

        # Validate and save the data
        if serializer.is_valid():
            # Save the bookmark and return the created data
            serializer.save()
            return Response(
                {
                    "message": "Medicine added successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        # If the data is invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#api for update 
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_medicine_api(request, pk):
   
    medicine = get_object_or_404(Medicine, pk=pk)
    serializer = MedicineSerializer(Medicine, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#api for delete
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # Ensures only authenticated users can delete bookmarks
def delete_medicine_api(request, pk):
    """
    Delete a specific medicine by ID without user ownership check.
    """
    medicine = get_object_or_404(Medicine, pk=pk)
    
    # Delete the bookmark
    medicine.delete()
    
    return Response(
        {"message": f"Medicine with ID {pk} has been deleted."},
        status=status.HTTP_200_OK,
    )


#api for logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only authenticated users can log out
def logout_api(request):
    """
    API endpoint for logging out the user.
    """
    try:
        # Delete the user's authentication token
        request.user.auth_token.delete()
        # Log the user out
        logout(request)
        return Response(
            {"message": "Logout successful."},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": "Something went wrong during logout."},
            status=status.HTTP_400_BAD_REQUEST
        )
