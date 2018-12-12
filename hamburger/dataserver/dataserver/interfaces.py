from zope import interface

from zope.schema import List


class IDataserver(interface.Interface):
    """
    Interface mapping the root object of the
    server application.
    """


class IExternalPersistent(interface.Interface):
    """
    Interface marking a class that is persistent
    and externalizable.
    """

    KEYS = List(title="Keys",
                required=True)

    EXCLUDE = List(title="Exclusions",
                   required=True)

    def to_json():
        """
        Convert object to json via KEYS
        """

    def from_json(json):
        """
        Convert JSON object to Python object
        """

    def is_complete():
        """
        Check all fields listed in keys are present.
        """


class ICollection(interface.Interface):
    """
    Interface that defines a base collection object.
    """

    def insert(new_obj, check_member=False):
        """
        Insert a new item into the collection,
        returning an error if it cannot be inserted
        for any reason.
        """


class IContained(interface.Interface):
    """
    Interface that defines an object contained in a container.
    """

    def get_key():
        """
        Return attribute implementing __key__
        """


class IOAuthSettings(interface.Interface):
    """
    Interace for oauth settings access
    """
