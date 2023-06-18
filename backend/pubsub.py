from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
import time

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-55a82f2f-e70a-4d0f-b88f-e9a3eb3155d7'
pnconfig.publish_key = 'pub-c-2cf48a2f-1dd2-41db-83d3-813b8a5272d2'
pubnub = PubNub(pnconfig)

TEST_CHANNEL = 'TEST_CHANNEL'

pubnub.subscribe().channels([TEST_CHANNEL]).execute()

class Listener(SubscribeCallback):
    def message(self, pubnub, message_object):
        print(f'\n--Incoming Message: {message_object}')


pubnub.add_listener(Listener())


def main():
    print('started main')
    time.sleep(1)
    print('sleep over')
    pubnub.publish().channel([TEST_CHANNEL]).message({'foo': 'bar'}).sync()


if __name__ == '__main__':
    main()
