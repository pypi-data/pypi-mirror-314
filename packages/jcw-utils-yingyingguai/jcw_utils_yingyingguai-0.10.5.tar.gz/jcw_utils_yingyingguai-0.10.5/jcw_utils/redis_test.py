import time
import redis
import multiprocessing

# Publisher function
def publisher():
    r = redis.Redis(host='localhost', port=6379, db=0)
    while True:
        message = "Hello from publisher!"
        r.publish('my_channel', message)
        print(f"Published: {message}")
        time.sleep(2)  # Publish every 2 seconds

# Subscriber function
def subscriber():
    r = redis.Redis(host='localhost', port=6379, db=0)
    pubsub = r.pubsub()
    pubsub.subscribe('my_channel')

    print("Subscriber started, waiting for messages...")
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received: {message['data'].decode('utf-8')}")

if __name__ == '__main__':
    # Create processes for publisher and subscriber
    pub_process = multiprocessing.Process(target=publisher)
    sub_process = multiprocessing.Process(target=subscriber)

    # Start the processes
    sub_process.start()
    pub_process.start()

    # Wait for the processes to finish (they won't, so we can run indefinitely)
    pub_process.join()
    sub_process.join()

