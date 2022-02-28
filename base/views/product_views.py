
from itertools import product
from math import prod
from urllib.request import Request
from wsgiref.util import request_uri


from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Product, Review
from base.serializers import ProductSerializer
from rest_framework import status

@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    # many flag means we are serializing multiple objects
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(request):

    product = Product.objects.create(
        user=request.user,
        name='Sample Name',
        price=0,
        brand='Sample Srand',
        countInStock=0,
        category='Sample Category',
        description=''
    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_product(request, pk):
    # take data from form
    data = request.data

    # find product by Id
    product = Product.objects.get(_id=pk)

    # modify product data
    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']
    
    product.save()
    
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Product Deleted')

# add image to product
@api_view(['POST'])
def upload_image(request):
    data = request.data

    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()
    return Response('Image was uploaded')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_review(request, pk):
    product = Product.objects.get(_id=pk)
    user = request.user
    data = request.data

    # if review already exists for a user, do not allow duplicate
    alreadyExists = product.review_set.filter(user=user).exists()

    if alreadyExists:
        content = {'detail': 'You already reviewed this product.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # if customer submit a review without a rating / or zero rating
    elif data['rating'] == 0:
        content = {'detail': 'Please select a valid rating.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment'],
        )

        # update number of reviews
        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        totalRating = 0
        for i in reviews:
            totalRating += i.rating
        
        product.rating = totalRating / product.numReviews
        product.save()

        return Response('Review added')