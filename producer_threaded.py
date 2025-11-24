import threading
import time
import random
import os
import logging
from typing import List
from ITStudent import ITStudent
from buffer import BoundedBuffer
from config.settings import PROJECT_CONFIG

logger = logging.getLogger(__name__)

class Producer(threading.Thread):
    def __init__(self, buffer: BoundedBuffer, xml_dir: str, 
                 produce_delay: float = None, max_files: int = None):
        super().__init__(name="ProducerThread")
        self.buffer = buffer
        self.xml_dir = xml_dir
        self.produce_delay = produce_delay or PROJECT_CONFIG['threaded']['produce_delay']
        self.max_files = max_files or PROJECT_CONFIG['max_files']
        
        self.next_file_no = 1
        self.files_produced = 0
        self.running = True
        self.daemon = True
        
        # Ensure XML directory exists
        os.makedirs(self.xml_dir, exist_ok=True)
        
        logger.info(f"Producer initialized with delay {self.produce_delay}s")

    def generate_student(self) -> ITStudent:
        """Generate a random student record"""
        config = PROJECT_CONFIG['student']
        
        name = random.choice(config['names'])
        student_id = f"2024{random.randint(10000, 99999)}"  # More realistic ID
        programme = random.choice(config['programmes'])
        num_courses = random.randint(2, 4)
        courses = random.sample(config['courses'], num_courses)
        marks = [random.randint(40, 95) for _ in range(num_courses)]  # More realistic marks
        
        return ITStudent(name, student_id, programme, courses, marks)

    def save_xml(self, student: ITStudent, file_no: int) -> str:
        """Save student as XML file and return file path"""
        filename = f"student{file_no:03d}.xml"  # Zero-padded filenames
        filepath = os.path.join(self.xml_dir, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(student.to_xml_string())
            logger.debug(f"Saved student XML to {filename}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save {filename}: {e}")
            raise

    def run(self):
        """Main producer loop"""
        logger.info("Producer started")
        
        while self.running and self.files_produced < 100:  # Safety limit
            try:
                # Generate and save student
                student = self.generate_student()
                file_no = self.next_file_no
                filepath = self.save_xml(student, file_no)
                
                # Insert into buffer
                if self.buffer.insert(file_no):
                    logger.info(f"Produced student{file_no:03d}.xml - {student.name} ({student.student_id})")
                    self.files_produced += 1
                    self.next_file_no = (file_no % self.max_files) + 1
                else:
                    logger.warning(f"Failed to insert student{file_no} into buffer")
                
                time.sleep(self.produce_delay)
                
            except Exception as e:
                logger.error(f"Error in producer loop: {e}")
                time.sleep(1)  # Brief pause on error

        logger.info(f"Producer finished. Total files produced: {self.files_produced}")

    def stop(self):
        """Stop the producer thread"""
        logger.info("Stopping producer...")
        self.running = False

if __name__ == "__main__":
    # Test the producer
    import logging
    logging.basicConfig(level=logging.INFO)
    
    from buffer import BoundedBuffer
    buffer = BoundedBuffer(5)
    
    producer = Producer(buffer, "../xml_files", produce_delay=0.5)
    producer.start()
    
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        pass
    finally:
        producer.stop()
        producer.join()
        print("Producer test completed")