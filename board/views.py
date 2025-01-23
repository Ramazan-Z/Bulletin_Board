from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from board import filters, models, paginators, serializers
from board.permissions import IsAuthorUser
from users.permissions import IsAdminUser


@extend_schema_view(get=extend_schema(operation_id="List of ads"))
class ListAdsView(generics.ListAPIView):
    """
    Просмотр списка объявлений. Принимает параметры фильтрации  по диапазону цен,
    минимальной дате создания и авторам. А также параметры сортировки, пагинации и
    поисковый запрос. Доступно неавторизованным пользователям.
    """

    queryset = models.Advertisement.objects.all()
    serializer_class = serializers.AdsListSerializer
    permission_classes = [AllowAny]
    pagination_class = paginators.ListPagination
    filterset_class = filters.AdvertisementFilter
    ordering_fields = ("create_at", "price")
    search_fields = ("title", "description")


@extend_schema_view(post=extend_schema(operation_id="Create an ad"))
class CreateAdView(generics.CreateAPIView):
    """Создание объявления. Доступно только авторизованным пользователям."""

    queryset = models.Advertisement.objects.all()
    serializer_class = serializers.AdSerializer

    def perform_create(self, serializer):
        """Присвоение авторства при создании."""
        serializer.save(author=self.request.user)


@extend_schema_view(get=extend_schema(operation_id="Viewing an ad"))
class RetrieveAdView(generics.RetrieveAPIView):
    """Просмотр деталей объявления. Доступно только авторизованным пользователям."""

    queryset = models.Advertisement.objects.all()
    serializer_class = serializers.AdRetrieveSerializer


@extend_schema_view(put=extend_schema(operation_id="Update the ad"), patch=extend_schema(operation_id="Edit the ad"))
class UpdateAdView(generics.UpdateAPIView):
    """Редактирование объявления. Доступно только владельцу или администратору."""

    queryset = models.Advertisement.objects.all()
    serializer_class = serializers.AdSerializer
    permission_classes = [IsAuthenticated, IsAuthorUser | IsAdminUser]


@extend_schema_view(delete=extend_schema(operation_id="Delete an ad"))
class DestroyAdView(generics.DestroyAPIView):
    """Удаление объявления. Доступно только владельцу или администратору."""

    queryset = models.Advertisement.objects.all()
    serializer_class = serializers.AdSerializer
    permission_classes = [IsAuthenticated, IsAuthorUser | IsAdminUser]


@extend_schema_view(get=extend_schema(operation_id="List of reviews"))
class ListComments(generics.ListAPIView):
    """
    Просмотр списка отзывов. Принимает параметры фильтрации  по объявлениям и авторам.
    А также параметры сортировки по дате, пагинации и поисковый запрос.
    Доступно только авторизованным пользователям.
    """

    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    filterset_fields = ("author", "ad")
    ordering_fields = ("create_at",)
    search_fields = ("text", "description")


@extend_schema_view(post=extend_schema(operation_id="Leave a review"))
class CreateComment(generics.CreateAPIView):
    """Создание отзыва. Доступно только авторизованным пользователям."""

    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        """Присвоение авторства при создании."""
        serializer.save(author=self.request.user)


@extend_schema_view(get=extend_schema(operation_id="View the review"))
class RetrieveComment(generics.RetrieveAPIView):
    """Просмотр деталей отзыва. Доступно только авторизованным пользователям."""

    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer


@extend_schema_view(
    put=extend_schema(operation_id="Update the review"), patch=extend_schema(operation_id="Edit a review")
)
class UpdateComment(generics.UpdateAPIView):
    """Редактирование отзыва. Доступно только владельцу или администратору."""

    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorUser | IsAdminUser]


@extend_schema_view(delete=extend_schema(operation_id="Delete a review"))
class DestroyComment(generics.DestroyAPIView):
    """Удаление отзыва. Доступно только владельцу или администратору."""

    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorUser | IsAdminUser]
