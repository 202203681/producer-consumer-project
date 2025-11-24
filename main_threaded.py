import time, os, sys
from buffer import BoundedBuffer
from producer_threaded import Producer
from consumer_threaded import Consumer

XML_DIR = os.path.join(os.path.dirname(__file__), "../xml_files")

def main():
    # Ensure xml directory exists
    os.makedirs(XML_DIR, exist_ok=True)

    buffer = BoundedBuffer(10)
    producer = Producer(buffer, XML_DIR, produce_delay=0.8)
    consumer = Consumer(buffer, XML_DIR, consume_delay=1.2)

    producer.start()
    consumer.start()

    try:
        # run for a short demo period; in real assignment run indefinitely or until condition
        time.sleep(12)
    except KeyboardInterrupt:
        pass
    finally:
        producer.stop()
        consumer.stop()
        producer.join()
        consumer.join()
        print("Demo finished.")

if __name__ == "__main__":
    main()
