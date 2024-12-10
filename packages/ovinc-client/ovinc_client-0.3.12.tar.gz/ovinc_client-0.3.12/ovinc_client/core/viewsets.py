import abc

from adrf.viewsets import ViewSet
from rest_framework.viewsets import GenericViewSet

from ovinc_client.core.cache import CacheMixin


class MainViewSet(CacheMixin, ViewSet, GenericViewSet):
    """
    Base ViewSet
    """

    ...


class CreateMixin(abc.ABC):
    @abc.abstractmethod
    async def create(self, request, *args, **kwargs):
        raise NotImplementedError()


class ListMixin(abc.ABC):
    @abc.abstractmethod
    async def list(self, request, *args, **kwargs):
        raise NotImplementedError()


class RetrieveMixin(abc.ABC):
    @abc.abstractmethod
    async def retrieve(self, request, *args, **kwargs):
        raise NotImplementedError()


class UpdateMixin(abc.ABC):
    @abc.abstractmethod
    async def update(self, request, *args, **kwargs):
        raise NotImplementedError()


class DestroyMixin(abc.ABC):
    @abc.abstractmethod
    async def destroy(self, request, *args, **kwargs):
        raise NotImplementedError()
