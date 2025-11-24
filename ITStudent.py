import xml.etree.ElementTree as ET
import logging
from typing import List, Dict, Any
from config.settings import PROJECT_CONFIG

logger = logging.getLogger(__name__)

class ITStudent:
    def __init__(self, name: str, student_id: str, programme: str, 
                 courses: List[str], marks: List[int]):
        self.name = name
        self.student_id = student_id
        self.programme = programme
        self.courses = courses
        self.marks = marks
        
        self._validate_data()

    def _validate_data(self):
        """Validate student data"""
        if not self.name or not self.name.strip():
            raise ValueError("Student name cannot be empty")
        
        if not self.student_id or not self.student_id.strip():
            raise ValueError("Student ID cannot be empty")
            
        if len(self.courses) != len(self.marks):
            raise ValueError("Courses and marks lists must have same length")
            
        for mark in self.marks:
            if not (0 <= mark <= 100):
                raise ValueError(f"Mark {mark} is not between 0 and 100")

    def to_xml_string(self) -> str:
        """Convert student to XML string with proper formatting"""
        root = ET.Element("Student")
        
        name_el = ET.SubElement(root, "Name")
        name_el.text = self.name.strip()
        
        id_el = ET.SubElement(root, "ID")
        id_el.text = self.student_id.strip()
        
        prog_el = ET.SubElement(root, "Programme")
        prog_el.text = self.programme.strip()

        courses_el = ET.SubElement(root, "Courses")
        for course_name, mark in zip(self.courses, self.marks):
            course_el = ET.SubElement(courses_el, "Course")
            
            cname = ET.SubElement(course_el, "CourseName")
            cname.text = course_name.strip()
            
            mark_el = ET.SubElement(course_el, "Mark")
            mark_el.text = str(mark)

        # Pretty print XML
        self._indent_xml(root)
        return ET.tostring(root, encoding='utf-8').decode('utf-8')

    def _indent_xml(self, elem, level=0):
        """Helper method to format XML with indentation"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent_xml(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    @classmethod
    def from_xml_file(cls, path: str):
        """Create ITStudent from XML file with error handling"""
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            
            name = root.findtext("Name", "").strip()
            student_id = root.findtext("ID", "").strip()
            programme = root.findtext("Programme", "").strip()
            
            courses = []
            marks = []
            
            for course_el in root.findall("./Courses/Course"):
                course_name = course_el.findtext("CourseName", "").strip()
                mark_text = course_el.findtext("Mark", "0").strip()
                
                if course_name:  # Only add if course name exists
                    courses.append(course_name)
                    marks.append(int(mark_text))
            
            logger.debug(f"Parsed student from {path}: {name} ({student_id})")
            return cls(name, student_id, programme, courses, marks)
            
        except ET.ParseError as e:
            logger.error(f"XML parsing error in {path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error reading student from {path}: {e}")
            raise

    def to_dict(self) -> Dict[str, Any]:
        """Convert student to dictionary"""
        return {
            'name': self.name,
            'student_id': self.student_id,
            'programme': self.programme,
            'courses': self.courses,
            'marks': self.marks,
            'average': self.average(),
            'passed': self.passed()
        }

    def average(self) -> float:
        """Calculate average mark"""
        if not self.marks:
            return 0.0
        return sum(self.marks) / len(self.marks)

    def passed(self, threshold: float = None) -> bool:
        """Check if student passed"""
        if threshold is None:
            threshold = PROJECT_CONFIG['student']['pass_threshold']
        return self.average() >= threshold

    def __str__(self) -> str:
        return f"{self.name} ({self.student_id}) - {self.programme}"

    def __repr__(self) -> str:
        return f"ITStudent(name='{self.name}', id='{self.student_id}')"

if __name__ == "__main__":
   
    try:
        student = ITStudent(
            "Musa Dlamini", 
            "12345678", 
            "BSc IT", 
            ["CS101", "MATH101"], 
            [60, 70]
        )
        print("Student created successfully:")
        print(student.to_xml_string())
        print(f"Average: {student.average():.2f}")
        print(f"Passed: {student.passed()}")
        
    except Exception as e:
        print(f"Error creating student: {e}")