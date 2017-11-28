from django.core.serializers.json import DjangoJSONEncoder
from bson import objectid
class MongoAwareEncoder(DjangoJSONEncoder): """JSON encoder class that adds support for Mongo objectids."""
def default(self, o):
    if isinstance(o, objectid.ObjectId):
        return str(o)
    else:
        return super(MongoAwareEncoder, self).default(o)
        