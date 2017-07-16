import pyjsonrpc
import operations
from config import SERVICE_HOST, SERVICE_PORT

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    # Test Method
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print 'add is called with %d and %d' % (a, b)
        return a + b

    """ Get news summaries for a user """
    @pyjsonrpc.rpcmethod
    def getNewsSummariesForUser(self, user_id, page_num):
        return operations.get_news_summaries_for_user(user_id, page_num)

    """ Log user news clicks """
    @pyjsonrpc.rpcmethod
    def logNewsClickForUser(self, user_id, news_id):
        return operations.log_news_click_for_user(user_id, news_id)

# HTTP Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVICE_HOST, SERVICE_PORT),
    RequestHandlerClass = RequestHandler
)

print 'Starting HTTP server on %s:%d' % (SERVICE_HOST, SERVICE_PORT)
http_server.serve_forever()
