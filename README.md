# HERBWISE - Plant monitoring system

## REPORT

### Team:

- Paul O’Brien
- Oleksandr Shostak
- Oleksandr Budonnyi
- Ewan Paul Fane

## Overview

The plant monitoring system is a web application for manage the health of plants by monitoring soil moisture, temperature, light level and humidity with implemented alert system.
Main goal was to provide real-time data visualization and user-friendly interface. The system collects data from multiple sensors  and displays real-time information on a website. 
The backend was built using Django framework and the frontend through HTML, CSS, and JavaScript. The system is hosted on an Apache web server on Linode ensuring secure access via HTTPS and a custom domain with SQLite as the database.

## Architecture

The system is built by the following components:

- •	Sensors & Raspberry Pi: Collects data from sensors (temperature, humidity, light levels, and soil moisture) and sending it to the server.
- •	Backend: Processes incoming data from PI, manages authentication, and serves the web application using Django framework.
- •	Frontend: Displays sensor data in a proper and intuitive interface.
- •	Database: Stores historical data of the plant health in SQLite format. Also stores for different plants properties information. 
- •	Server: Hosting on an Apache web server and ensures reliable and secure access to it.

![High Level Diagram Photo]("/imaged-forreadme/highlevelarchitecture-diagram.jpg")
Caption: The Herb Wise architecture.

## Main Components

### (Hardware)

Sensors collect data from plants and send it to a Pi. The Raspberry Pi acts as a mediator, between sensor data readings and web server via HTTP POST requests.
Raspberry PI also shows information from sensors to it’s LCD screen with all needed information.	

### (Backend)

Django is one of the major components of the HerbWise. We integrated a RESTful APIs to enable smooth data sending from the Raspberry Pi to the frontend, with focus on a scalability. We made a lot of code refactoring which resolved bottlenecks. Codebase was restructured.
The authentication system was implemented by using Django’s built-in feature which includes password hashing, protect from vulnerabilities such as CSRF, XSS and SQL injection attacks. SQLite database stores user’s sessions, plant records and sensor data. Oriented relational mapper for managing. 

### (Frontend)

Built with Django templates using HTML for structure, CSS for responsive design and user-friendly interface, and JavaScript for user interactions. Implemented dashboard for streaming data in a human readable format. To keep user engagement, we have a streak system to reward daily logins. 
![Dashboard]("/imaged-forreadme/dashboard.jpg")
![Item]("/imaged-forreadme/item0.jpg")
![Data records]("/imaged-forreadme/screen01.jpg")
Caption: Website elements.

### (Server)

We provided a server on Linode. Apache was deployed with virtual hosts, SSL certificates (via HTTPS), and settings for Django. A custom domain was acquired (https://herbwise.site/). DNS records were configured ensuring seamless and secure user access.

### (Data Flow)

Data flows from sensors to the Raspberry PI, then to the Django backend via RESTful APIs over HTTPS. The backend processes stores in SQLite, retrieving data to the frontend.
![Data Flow diagram]("/imaged-forreadme/dataflow-diagram.jpg")

## Challenges and Lessons Learned

1.	Frontend-Backend API Integration: We found challenging connecting the frontend to the backend via RESTful APIs. We resolved some issues by correcting API responses and adding error handling. It taught us the importance of clear communication protocols.

2.	SSL/DNS Issues: Misconfigured SSL certificates and DNS delays wrecked access. Verifying propagation fixed this.

3.	CSS Design: Creating a responsive and visually consistent frontend with CSS was harder than expected, with layouts breaking across devices. With appropriate delegations between team members, it was solved. 

4.	Raspberry PI Stability: Network issues disrupted data from the PI to the server. Implementing a retry mechanism on the PI ensured reliability.  

5.	Security Tuning: Early authentication lacked CSRF protection. Implementing Django’s built-in middleware fixed this. 
Adopting Kanban approach helped with our collaboration, ensuring challenges were solved systematically and met deadlines for certain tasks. It increased our productivity with challenges we’ve faced by dividing them into a small parts.

## Team Contributions

- Team Member 1 (Ewan Paul Fane): Set up the Linode server with Apache and developed the RESTful APIs for efficient backend communication. Implemented the warnings if thresholds arent met.
- Team Member 2 (Paul O’Brien): Configured the Raspberry Pi and sensor readings and managed data transmission to the server, bridging hardware and software.
Implemented fetch latest sensor readings so users can see real time readings.
Developed the plant dashboard page, using graphs to display historical sensor data.
Implemented a database to store plant thresholds and display thresholds on dashbaord graphs.
Linked sensor values, individual plants, gardens, and users, ensuring data was correctly associated with the right user and garden.
- Team Member 3 (Oleksandr Shostak): Focused on the frontend, designing the HTML, CSS, and JavaScript.
- Team Member 4 (Oleksandr Budonnyi): Worked alongside Team Member 3 on the frontend, implementing the streak system and refining the user interface.
In the final days, all team members worked together to fix bugs and resolve integration issues, ensuring a functional system through debugging and testing.
