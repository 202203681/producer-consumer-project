# ProducerConsumerProject

**Course:** CSC411 - Integrative Programming Technologies  
**Project:** Producer–Consumer Problem (Mini Project)  
**Source:** The uploaded assignment specification included at: /mnt/data/The ProducerConsumerProblem.pdf

## Project Overview
This project implements the Producer–Consumer concurrency problem. The producer generates IT student records, wraps them into XML files (`student1.xml` ... `student10.xml`), and inserts an identifier into a bounded buffer. The consumer reads identifiers from the buffer, parses the corresponding XML, computes the average and pass/fail, prints output, and deletes the processed XML file. A socket-based version is also provided for networked communication.

## Folder Structure
```
/ProducerConsumerProject
├── src/
│   ├── ITStudent.py
│   ├── buffer.py
│   ├── producer_threaded.py
│   ├── consumer_threaded.py
│   ├── main_threaded.py
│   ├── socket_producer.py
│   └── socket_consumer.py
├── xml_files/
│   ├── student1.xml
│   ├── student2.xml
│   └── student3.xml
├── docs/
│   └── final_report.pdf
└── README.md
```

## Requirements
- Python 3.8+
- No external dependencies required for threaded/socket demo (uses standard library)
- If running in restricted environment, ensure read/write permissions for xml_files directory

## Setup Instructions
1. Clone the repository (or copy the project folder).
2. Ensure Python 3.8+ is installed.
3. From the project root, run commands below to execute the threaded or socket versions.

## How to run threaded version (local, using shared buffer)
1. Open a terminal in `ProducerConsumerProject/src`
2. Run:
```
python main_threaded.py
```
This will start a Producer and Consumer for a short demo period (12 seconds). To run indefinitely, edit `main_threaded.py` and remove the timed sleep, or call with longer duration.

## How to run socket version
1. Open two terminals.
2. In terminal A (producer/server):
```
python socket_producer.py
```
3. In terminal B (consumer/client):
```
python socket_consumer.py
```
The producer will listen on `127.0.0.1:9009` by default and send periodic XML messages; the consumer will connect and process them.

## Group Members (placeholders - replace with your actual names & IDs)
- Member 1: Lungelo Dlamini - 2025XXXXX
- Member 2: Michael Mamba - 2025YYYYY

## Demo Video
Include a 5–10 minute demo video explaining the implementation, showing the code running, and demonstrating both threaded and socket versions. Add the video file to the repository root as `demo_video.mp4` or provide a link to YouTube/GitHub release.

## Final Report
A 4-page PDF report has been included in `docs/final_report.pdf`. The original assignment spec is included at `/mnt/data/The ProducerConsumerProblem.pdf`.

## Notes
- The sample XML files are provided in `xml_files/` to test the consumer independently.
- After running threaded version, produced XML files will appear in `xml_files/` and will be deleted by the consumer after processing.
