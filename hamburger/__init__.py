from authomatic import Authomatic

from authomatic.providers import oauth2

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.config import Configurator
from pyramid_zodbconn import get_connection

from zope.component import getGlobalSiteManager

from hamburger.dataserver import appmaker

from hamburger.dataserver.dataserver.interfaces import IOAuthSettings


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())


def configure_oauth(settings):
    key = settings['facebook.key']
    secret = settings['facebook.secret']
    CONFIG = {
        'fb': {
            'class_': oauth2.Facebook,
            'consumer_key': key,
            'consumer_secret': secret,
            'scope': ['email']
        }
    }
    authomatic = Authomatic(config=CONFIG, secret="giftpacito")
    return authomatic


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'
    config.include('pyramid_chameleon')
    config.include('pyramid_zcml')
    config.set_root_factory(root_factory)
    config.load_zcml('configure.zcml')
    authn_policy = AuthTktAuthenticationPolicy(
        settings['tutorial.secret'], hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    # Configure oauth
    oauth = configure_oauth(settings)
    sm = getGlobalSiteManager()
    sm.registerUtility(oauth, IOAuthSettings)

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.scan()
    return config.make_wsgi_app()
