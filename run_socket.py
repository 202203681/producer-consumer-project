#!/usr/bin/env python3
"""
Main entry point for socket-based producer-consumer demo
"""

import os
import logging
import logging.config
import threading
import time
from config.settings import PROJECT_CONFIG, LOGGING_CONFIG

def setup_environment():
    """Setup project environment"""
    os.makedirs(PROJECT_CONFIG['xml_directory'], exist_ok=True)
    os.makedirs(PROJECT_CONFIG['log_directory'], exist_ok=True)
    logging.config.dictConfig(LOGGING_CONFIG)

def run_socket_demo():
    """Run socket-based producer-consumer demo"""
    setup_environment()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Socket-based Producer-Consumer Demo")
    
    try:
        # Import here to avoid circular imports
        from src.socket_producer import run_server
        from src.socket_consumer import run_client
        
        # Start producer in a separate thread
        producer_thread = threading.Thread(
            target=run_server,
            daemon=True,
            name="SocketProducer"
        )
        producer_thread.start()
        
        logger.info("Socket producer started, waiting for initialization...")
        time.sleep(2)  # Give producer time to start
        
        # Run consumer in main thread
        print("\n" + "="*60)
        print("SOCKET PRODUCER-CONSUMER DEMO RUNNING")
        print("Producer: Running on background thread")
        print("Consumer: Starting in main thread")
        print("Press Ctrl+C to stop the demo")
        print("="*60 + "\n")
        
        run_client()
        
    except KeyboardInterrupt:
        logger.info("Socket demo interrupted by user")
        print("\nStopping socket demo...")
    except Exception as e:
        logger.error(f"Error in socket demo: {e}")
        raise
    finally:
        logger.info("Socket demo finished")

if __name__ == "__main__":
    run_socket_demo()