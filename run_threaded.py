#!/usr/bin/env python3
"""
Main entry point for threaded producer-consumer demo
"""

import os
import time
import logging
import logging.config
from src.buffer import BoundedBuffer
from src.producer_threaded import Producer
from src.consumer_threaded import Consumer
from config.settings import PROJECT_CONFIG, LOGGING_CONFIG

def setup_environment():
    """Setup project environment"""
    # Create necessary directories
    os.makedirs(PROJECT_CONFIG['xml_directory'], exist_ok=True)
    os.makedirs(PROJECT_CONFIG['log_directory'], exist_ok=True)
    
    # Configure logging
    logging.config.dictConfig(LOGGING_CONFIG)

def main():
    """Main threaded demo"""
    setup_environment()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Producer-Consumer Demo (Threaded Version)")
    
    # Initialize components
    buffer = BoundedBuffer(PROJECT_CONFIG['buffer_capacity'])
    producer = Producer(
        buffer, 
        PROJECT_CONFIG['xml_directory'],
        PROJECT_CONFIG['threaded']['produce_delay'],
        PROJECT_CONFIG['max_files']
    )
    consumer = Consumer(
        buffer,
        PROJECT_CONFIG['xml_directory'], 
        PROJECT_CONFIG['threaded']['consume_delay']
    )
    
    # Start threads
    producer.start()
    consumer.start()
    
    logger.info("Producer and Consumer threads started")
    print("\n" + "="*60)
    print("PRODUCER-CONSUMER DEMO RUNNING (Threaded Version)")
    print("Press Ctrl+C to stop the demo")
    print("="*60 + "\n")
    
    try:
        # Run for specified duration
        runtime = PROJECT_CONFIG['threaded']['runtime_duration']
        logger.info(f"Demo will run for {runtime} seconds")
        time.sleep(runtime)
        
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
        print("\nStopping demo...")
    finally:
        # Stop threads
        producer.stop()
        consumer.stop()
        
        # Wait for threads to finish
        producer.join(timeout=5)
        consumer.join(timeout=5)
        
        # Summary
        print("\n" + "="*60)
        print("DEMO SUMMARY")
        print(f"Files produced: {producer.files_produced}")
        print(f"Students processed: {consumer.students_processed}")
        print("Demo finished successfully!")
        print("="*60)

if __name__ == "__main__":
    main()