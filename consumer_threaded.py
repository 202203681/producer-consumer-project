import threading
import time
import os
import logging
from ITStudent import ITStudent
from buffer import BoundedBuffer
from config.settings import PROJECT_CONFIG

logger = logging.getLogger(__name__)

class Consumer(threading.Thread):
    def __init__(self, buffer: BoundedBuffer, xml_dir: str, 
                 consume_delay: float = None):
        super().__init__(name="ConsumerThread")
        self.buffer = buffer
        self.xml_dir = xml_dir
        self.consume_delay = consume_delay or PROJECT_CONFIG['threaded']['consume_delay']
        self.running = True
        self.daemon = True
        self.students_processed = 0
        
        logger.info(f"Consumer initialized with delay {self.consume_delay}s")

    def process_file(self, file_no: int) -> bool:
        """Process a student XML file and return success status"""
        filename = f"student{file_no:03d}.xml"
        filepath = os.path.join(self.xml_dir, filename)
        
        if not os.path.exists(filepath):
            logger.warning(f"File {filename} does not exist")
            return False

        try:
            # Parse student from XML
            student = ITStudent.from_xml_file(filepath)
            
            # Display student information
            self._display_student_info(student, file_no)
            
            # Delete the file after processing
            try:
                os.remove(filepath)
                logger.debug(f"Deleted processed file: {filename}")
            except Exception as e:
                logger.warning(f"Could not delete {filename}: {e}")
            
            self.students_processed += 1
            return True
            
        except Exception as e:
            logger.error(f"Failed to process {filename}: {e}")
            return False

    def _display_student_info(self, student: ITStudent, file_no: int):
        """Display formatted student information"""
        print(f"\n{'='*50}")
        print(f"PROCESSED: student{file_no:03d}.xml")
        print(f"{'='*50}")
        print(f"Name: {student.name}")
        print(f"Student ID: {student.student_id}")
        print(f"Programme: {student.programme}")
        print("\nCourses and Marks:")
        for course, mark in zip(student.courses, student.marks):
            status = "PASS" if mark >= 50 else "FAIL"
            print(f"  {course}: {mark:3d} [{status}]")
        print(f"\nAverage: {student.average():.2f}")
        print(f"Overall Result: {'PASS' if student.passed() else 'FAIL'}")
        print(f"{'='*50}\n")

    def run(self):
        """Main consumer loop"""
        logger.info("Consumer started")
        
        while self.running:
            try:
                # Remove item from buffer
                file_no = self.buffer.remove(timeout=2.0)  # Add timeout
                
                if file_no is not None:
                    self.process_file(file_no)
                else:
                    # Timeout occurred, check if we should continue
                    if not self.running:
                        break
                    continue
                
                time.sleep(self.consume_delay)
                
            except Exception as e:
                logger.error(f"Error in consumer loop: {e}")
                time.sleep(1)  # Brief pause on error

        logger.info(f"Consumer finished. Total students processed: {self.students_processed}")

    def stop(self):
        """Stop the consumer thread"""
        logger.info("Stopping consumer...")
        self.running = False

if __name__ == "__main__":
    # Test the consumer
    import logging
    logging.basicConfig(level=logging.INFO)
    
    from buffer import BoundedBuffer
    from producer_threaded import Producer
    
    buffer = BoundedBuffer(5)
    consumer = Consumer(buffer, "../xml_files", consume_delay=0.5)
    
    # Create a test file
    os.makedirs("../xml_files", exist_ok=True)
    test_student = ITStudent("Test Student", "20240001", "BSc IT", ["CSC101", "MAT101"], [85, 92])
    with open("../xml_files/student001.xml", "w") as f:
        f.write(test_student.to_xml_string())
    
    buffer.insert(1)
    consumer.start()
    
    try:
        time.sleep(3)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.stop()
        consumer.join()
        print("Consumer test completed")