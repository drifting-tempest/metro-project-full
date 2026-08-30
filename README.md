# Tokyo Metro Route Finder

A lightweight, browser-based route planning tool for Tokyo's subway and tram networks. It calculates the top 3 shortest paths between stations, estimates travel time, and determines official fares across different ticket types.

## Features

* **Shortest Path Calculation:** Finds the fastest route and alternative paths using Dijkstra's algorithm.
* **Accurate Fares:** Calculates fare prices for Adult IC, Adult Ticket, Child IC, and Child Ticket, taking into account split-fare transfer rules and flat-fare lines.
* **Interactive Map & UI:** Visualizes route lines on an interactive Leaflet map with step-by-step itinerary breakdowns.

## Repository Structure

* `index.html` – The main user interface and layout.
* `styles.css` – UI styling, dark theme design, and responsive layout rules.
* `app.js` – Core logic, pathfinding algorithms (Dijkstra/Yen's $K$-shortest paths), fare calculation engine, and Leaflet map rendering.
* `data.js` – Station coordinate datasets, network line connections, edge distances, and special transfer hub rules.

## Getting Started

1. Clone or download this repository.
2. Open `index.html` directly in any web browser—no web server or build step required.
3. Select your **From** and **To** stations and click **Find fastest routes**.
