from drf_spectacular.utils import OpenApiResponse, extend_schema
from product_app.models import Product, Review
from product_app.serializers.review import ReviewSerializer
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import get_or_none


class ProductReviewsView(APIView):
    """
    Класс APIView для отзыва на продукт.
    """

    queryset = Product.objects.all()
    review_serializer = ReviewSerializer

    @extend_schema(
        request=ReviewSerializer,
        responses={
            200: ReviewSerializer(many=True),
            400: OpenApiResponse(description="Неверный запрос."),
        },
        description="Сохранение отзыва.",
        tags=("Product",),
    )
    def post(self, request: Request, product_id: int) -> Response:
        """
        Создаём отзыв на продукт.

        :param request: Request.
        :param product_id: ID продукта.
        :return: Response.
        """

        product = get_or_none(self.queryset, id=product_id)
        if not product:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.review_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Review.objects.create(product=product, **serializer.validated_data)
        reviews = Review.objects.filter(product=product)
        return Response(self.review_serializer(reviews, many=True).data)
