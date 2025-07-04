# Portfolio + IoT Project

This project consists of creating my personal portfolio, to which I decided to integrate a side project I had previously developed: a temperature and humidity monitoring system.

![image](https://github.com/user-attachments/assets/3a9a7f8d-d3ef-4c9f-8a17-f6de8c30a70f)

## Temperature and Humidity Monitoring Project

This system was developed using an Arduino UNO and programmed in C++ through the Arduino IDE. The goal is to measure and record ambient temperature and humidity values, storing them in a database.

### Components Used

* 6 LEDs
* RGB LED
* Resistors (220 ohm and another of unknown value)
* DHT11 Sensor (temperature and humidity)
* Photoresistor
* Jumper wires
* Breadboard
* Arduino UNO

### Circuit Diagram

![Smashing Wolt-Juttuli](https://github.com/user-attachments/assets/5caba5e6-d516-4e61-9aa7-f21521d68777)

The data is read via the serial port (in this case, COM5). These values are processed by a Python application that connects directly to the MongoDB database, where the measurements are automatically stored.

**Note:** The COM port may vary depending on the device and operating system.

### Future Improvements

The system is expected to be upgraded in the future by adding a Wi-Fi module to the Arduino (e.g., ESP8266 or ESP32), allowing direct network communication without the need for a physical connection to a computer.

## Website Project

For the web part of the project, a simple application was developed that displays my portfolio and integrates the data collected by the IoT system.

### Technologies Used

#### Backend:

* Java with Spring Boot
* MongoDB (NoSQL database)

#### Frontend:

* HTML
* Tailwind CSS

**Note:** The website is not mobile-responsive at the moment.

#### Prototyping:

* Figma

### Architecture

The architecture of the project follows this flow:

![ARCH drawio](https://github.com/user-attachments/assets/28e6c3e4-c0f0-4593-9787-a55a33f9ebff)
