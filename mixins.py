""" ViewSet mixins """


# Create your mixins here.
class OwnerMixin:
    """Filter queryset by owner and add owner of the object when creating"""

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
