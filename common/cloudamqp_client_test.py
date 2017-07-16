from cloudamqp_client import CloudAMQPClient

CLOUDAMQP_URL = 'amqp://elkeiyay:toRc-yZ3LuVtM3F7fh8YuCSGOSm9FQjc@fish.rmq.cloudamqp.com/elkeiyay'
QUEUE_NAME = 'test'

def test():
    client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

    sent_message = {'test_key':'test_value'}
    client.send_message(sent_message)
    client.sleep(5)
    received_message = client.get_message()
    assert sent_message == received_message
    print 'test_basic passed.'

if __name__ == '__main__':
    test() 
