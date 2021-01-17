# Hydronizer
An intelligent addition to any water bottle to increase daily water intake

https://youtu.be/uOv5yZM5v3Y

![physical](https://i.imgur.com/3hPBUsF.png "Physical Layout")
![website](https://i.imgur.com/ThGmNJd.jpg "Website")
![extension](https://i.imgur.com/4SULhLe.png "Extension")
![hardware](https://i.imgur.com/bifZerP.jpg "Hardware")

## Inspiration
What inspired us to create Hydronizer was the growing importance for individuals to be conscious of their health. Especially during COVID-19, most people spend the majority of their day sitting in front of a computer screen. As a result, individuals have become much less conscious about their physical wellbeing, often forgetting about the importance of taking care of your body, and staying hydrated.

## What it does
Hydronizer provides users with a seamless experience that allows individuals to set regular water drinking reminders and goals as they go about their day. Hydronizer comes with a Smart coaster that users should use with their mug or water bottle, which is used to keep track of their water consumption throughout the day. Through an easy to install Google Chrome Extension that pairs with the Smart coaster, users can toggle Hydronizer on and off and customize their water break times throughout the day. When the timer goes off, the user’s chrome browser will freeze until they have taken a sip of water. For more metrics on the individual’s liquid consumption, users can view their water metrics on the Hydronizer website which provides details such as the total amount of water the user has consumed that day, the number of sips they’ve taken, and the amount of water they have yet to drink before reaching the daily recommended liquid consumption.

## How we built it
Hydronizer’s hardware component is built with an ESP32 and various sensors such as an RFID sensor for reading the water bottle. An OLED display is also included to view details such as when you should take your next sip of water.

The backend component is built with Python and Flask, and uses MQTT protocol to send messages between the Smart coaster and the backend service whenever the user takes a sip of water. The information received from the Smart Coaster is then stored in a database using CockroachDB. Through the use of REST APIs, both the Google Chrome extension and website retrieve the necessary metrics and information needed through API calls.

The frontend (Google Chrome extension and website) are developed using Javascript, React, HTML, and CSS, and pull information from our backend service.

## Tech Stack
ESP32 for Embedded Hardware Implementation
MQTT for facilitating hardware and server communications
CockroachDB for the database
Flask to host our backend API endpoints
React.js for the frontend website
Pure HTML/CSS/JS for Chrome Extension
Google Cloud for hosting the services above (except CockroachDB)

## Challenges we ran into
One notable challenge that we encountered was integrating the hardware component (Smart coaster) with the backend service through the use of MQTT protocol. This was the first time most of the team was working on a hardware project, so there was definitely a learning curve at first.

## What's next for Hydronizer
Adding more metrics to the Hydronizer dashboard to provide users with a detailed description of their water drinking habits. This could include more personalized recommendations based on an individual’s gender, weight, etc.