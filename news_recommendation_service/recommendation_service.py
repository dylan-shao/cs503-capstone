import os
import pyjsonrpc
import sys
import operator
import datetime

# Import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from metrics_client import metrics_client
from config import SERVICE_HOST, SERVICE_PORT, PREFERENCE_MODEL_TABLE_NAME

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """ Get user's preference in an ordered class list """
    @pyjsonrpc.rpcmethod
    def getPreferenceForUser(self, user_id):
        start_time = datetime.datetime.now()

        db = mongodb_client.get_db()
        model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({ 'userId':user_id })
        if model is None:
            return []

        sorted_tuples = sorted(model['preference'].items(), key=operator.itemgetter(1), reverse=True)
        sorted_list = [x[0] for x in sorted_tuples]
        sorted_value_list = [x[1] for x in sorted_tuples]

        # If the first preference is same as the last one, the preference makes
        # no sense.
        if isclose(float(sorted_value_list[0]), float(sorted_value_list[-1])):
            return []

        end_time = datetime.datetime.now()
        # Measure the time of the RPC in milliseconds
        rpc_time_in_milliseconds = int((end_time - start_time).total_seconds() * 1000)

        # Send the metrics
        metrics_client.timing('coconut_news.recommendation_service.getPreferenceForUser',
                              rpc_time_in_milliseconds)
        metrics_client.increment('coconut_news.recommendation_service.getPreferenceForUser')

        return sorted_list


# Threading HTTP Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVICE_HOST, SERVICE_PORT),
    RequestHandlerClass = RequestHandler
)

print 'Starting HTTP server on %s:%d' % (SERVICE_HOST, SERVICE_PORT)

http_server.serve_forever()
