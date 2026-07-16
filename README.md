# SL Building Virtual Tour

Demo Site: https://dinhanh0.github.io/SL-Building-Virtual-Tour/

A browser-based indoor navigation experience for the Purdue Science Building that combines **360° panoramas**, **graph based scene navigation**, and a **minimap** to help users explore the building virtually.

Built with HTML, CSS, JavaScript, and Python, the project organizes panorama scenes as connected nodes across multiple floors and generates reusable floor datasets for scalable tour maintenance.

This was a final project for course CSCI 435 Multimedia Information Systems

## Features

- 360° panorama viewer using **Pannellum**
- Multi-floor navigation for floors **0–3**
- Interactive **minimap** with floor-specific map images
- Node-based navigation between connected panorama locations
- Floor switching with persistent state
- Compass widget and navigation controls
- Developer/debug tools for tuning:
  - default scene orientation
  - edge view orientation
  - hotspot icon yaw/pitch
  - extra links between nodes
  - map positioning

## Project Structure

```bash
SL-Building-Virtual-Tour/
│
├── index.html                  # Main app layout
├── style.css                   # Styling for viewer, controls, minimap, and panels
├── script.js                   # Main app logic and navigation behavior
│
├── nodes_floor0.js             # Auto-generated node data for floor 0
├── nodes_floor1.js             # Auto-generated node data for floor 1
├── nodes_floor2.js             # Auto-generated node data for floor 2
├── nodes_floor3.js             # Auto-generated node data for floor 3
│
├── generate_nodes_floor0.py    # Generates nodes_floor0.js
├── generate_nodes_floor1.py    # Generates nodes_floor1.js
├── generate_nodes_floor2.py    # Generates nodes_floor2.js
├── generate_nodes_floor3.py    # Generates nodes_floor3.js
│
├── SLFloors/                   # Panorama image folders by floor
│   ├── SLFloor0/
│   ├── SLFloor1/
│   ├── SLFloor2/
│   └── SLFloor3/
│
└── floorplan(edited)/          # Edited floor map images used by minimap
