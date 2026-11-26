# Module 1

## Learning Goals

By the end of this module, I can:

1. Explain how the class works, including its challenge- and project-based approach, portfolio assessment, and moving draft boundary.
2. Set up a personal portfolio from the course template and use a `.gitignore` that keeps databases and secrets out of Git.
3. Set up and verify the course toolchain reproducibly with `uv`, Python, SQLite, DuckDB, Datasette, and related tools.
4. Use a measurement to explain the difference between embedded and client/server databases, and why a local application may not need a separate server.
5. Load real rows into SQLite and query them from Python using bound parameters.
6. Run an LLM-generated query and verify its result and behavior before trusting it.

**Planned focus:** Use the machine telemetry data to practice SQL and verify query results before relying on them.

These goals follow the [official Module 1 specification](../Course_Materials/01-introduction-and-local-first.md).

## Task Inspirations

- Inspiration 1
     I am motivated to deepen my understanding of database design and development. I want to improve my SQL skills and learn how to create efficient, reliable, and well-structured databases. I am particularly interested in applying theoretical knowledge to practical projects. My goal is to develop the technical skills needed to solve real-world data management challenges.

- Inspiration 2
    I am interested in understanding how databases store, organize, and process information efficiently. I want to explore database optimization, data security, and performance improvement. Through practical exercises and projects, I aim to strengthen my analytical and problem-solving skills. My goal is to build a solid foundation for applying database technologies in my future career.

## Task Personal Profile

    My name is Myo Min Lin, and I am originally from Myanmar (Burma). I am currently in my third semester of the undergraduate Mechatronics and Automation program, taught in English, at Hochschule Bielefeld (HSBI), Germany. During my previous semesters, I gained foundational knowledge of C and C++ programming, which helped me develop my logical thinking and problem-solving skills.I am particularly interested in the connection between programming, automation, and engineering applications. I enjoy learning how technical systems work and how software can be used to control, improve, and optimize them. As I continue my studies, I aim to expand my technical knowledge, strengthen my practical programming abilities, and gain experience in applying theoretical concepts to real-world engineering problems. I am motivated to learn new technologies, take on challenging projects, and continuously improve my skills to prepare myself for a successful future career in mechatronics and automation.

## Task What is IoT

Domains and included areas:
    -Industrial IoT: Factory automation, machine monitoring, predictive maintenance, and smart manufacturing.

    -Smart Homes and Buildings: Smart lighting, temperature control, security systems, and energy management.

    -Healthcare and Agriculture: Remote patient monitoring, wearable devices, soil sensors, and automated irrigation.

    -Smart Cities and Transportation: Traffic management, smart parking, vehicle tracking, and environmental monitoring.

Commonly used (data) protocols:
    -MQTT (Message Queuing Telemetry Transport): A lightweight protocol used to send data between IoT devices and servers. It is ideal for sensors and devices with limited bandwidth.

    -HTTP/HTTPS (Hypertext Transfer Protocol): Used for communication between IoT devices and web servers through request-and-response messages. HTTPS provides encryption for secure data transmission.

    -CoAP (Constrained Application Protocol): A lightweight protocol designed for small IoT devices with limited memory and processing power. It is commonly used in low-power sensor networks.

Typical devices (appliance or micro controller):
    -ESP32 Microcontroller: A low-cost microcontroller with built-in Wi-Fi and Bluetooth, commonly used for sensor monitoring, smart home systems, and automation projects.

    -Arduino: A microcontroller platform used to read sensor data and control actuators such as motors, LEDs, and relays.

    -Raspberry Pi: A small single-board computer used for IoT gateways, data processing, and connecting devices to databases or cloud services.

Challenges:
    -security and Privacy: Connected devices can be vulnerable to cyberattacks and unauthorized access to personal or sensitive data.

    -Connectivity and Compatibility: Unstable internet connections and different communication standards can make it difficult for devices to communicate reliably.

    -Power and Data Management: Many IoT devices have limited battery life and storage capacity, making efficient energy use and data processing important.

## Reflection 1
[Reflection 1](../Reflections/ref01.md)
I found .schema most useful because it shows a table's structure, including its column names and data types.

### Task 8: Publish Data with Datasette

- **Table view screenshot:** `datasette-filtered-view.png`
- **Filtered CSV export:** `datasette-cnc-01.csv`
- **Single-row URL:** `http://127.0.0.1:8001/telemetry/readings/1`
- **Total readings:** 172,800
- **Filtered readings for `cnc-01`:** 57,600

**Result:** Datasette successfully displayed the telemetry database, filtered readings by machine, and exported the filtered results as CSV.
