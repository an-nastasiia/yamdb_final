from django.shortcuts import get_object_or_404

from reviews.models import Review, Title


class CurrentTitleDefault:
    """Defoult class for curent Title."""

    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['request'].parser_context.get(
            'kwargs').get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title


class CurrentReviewDefault:
    """Defoult class for curent Review."""

    requires_context = True

    def __call__(self, serializer_field):
        review_id = serializer_field.context['request'].parser_context.get(
            'kwargs').get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review
