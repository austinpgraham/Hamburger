from authomatic import Authomatic

from authomatic.providers import oauth2

from pyramid.events import NewResponse

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.config import Configurator
from pyramid_zodbconn import get_connection

from zope.component import getGlobalSiteManager

from hamburger.dataserver import appmaker

from hamburger.dataserver.dataserver.interfaces import IOAuthSettings

from hamburger.app.cors import CorsPreflightPredicate
from hamburger.app.cors import add_cors_to_response


def cors_options_view(context, request):
    response = request.response
    if 'Access-Control-Request-Headers' in request.headers:
        response.headers['Access-Control-Allow-Methods'] = ', '.join({
            'POST',
            'PUT',
            'DELETE',
        })
    response.headers['Access-Control-Allow-Headers'] = ', '.join({
        'Content-Type',
        'Accept',
        'X-Requested-With',
    })
    request.response.headers['Access-Control-Max-Age'] = '3600'

    return response

def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())


def configure_oauth(settings):
    CONFIG = {
        'fb': {
            'class_': oauth2.Facebook,
            'consumer_key': settings['facebook.key'],
            'consumer_secret': settings['facebook.secret'],
            'scope': ['email']
        },
        'google': {
            'class_': oauth2.Google,
            'consumer_key': settings['google.key'],
            'consumer_secret': settings['google.secret'],
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
    config.add_subscriber(add_cors_to_response, 'pyramid.events.NewResponse')
    config.add_route_predicate('cors_preflight', CorsPreflightPredicate)
    config.add_route(
        'cors-options-preflight', '/{catch_all:.*}',
        cors_preflight=True,
    )
    config.add_view(
        cors_options_view,
        route_name='cors-options-preflight',
    )
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
