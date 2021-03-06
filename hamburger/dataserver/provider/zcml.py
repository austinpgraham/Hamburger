from functools import partial

from zope import interface
from zope import component

from zope.schema import Text

from zope.configuration.fields import GlobalObject

from hamburger.dataserver.provider.interfaces import IProvider
from hamburger.dataserver.provider.interfaces import IProductParser
from hamburger.dataserver.provider.interfaces import IProductFetcher


class IRegisterProvider(interface.Interface):
    """
    Registration of a new product provider.
    """
    name = Text(title="Name of provider",
                required=True)

    provider = GlobalObject(title="Provider class",
                            required=True)

    fetcher = GlobalObject(title="Product fetcher for this provider.",
                           required=True)

    parser = GlobalObject(title="Product parser for this provider.",
                          required=True)

    appID = Text(title="Provider AppID",
                 required=False,
                 default=None)


def registerProvider(_context, name, provider, fetcher, parser, **kwargs):
    pfetcher = fetcher()
    if not IProductFetcher.providedBy(pfetcher):
        raise TypeError("Fetcher must provide IProductFetcher") # pragma: no cover
    pparser = parser()
    if not IProductParser.providedBy(pparser):
        raise TypeError("Parser must provide IProductParser") # pragma: no cover
    provider_factory = partial(provider, fetcher=pfetcher, parser=pparser, **kwargs)
    component.zcml.utility(_context, provides=IProvider,
                           component=provider_factory, name=name)
