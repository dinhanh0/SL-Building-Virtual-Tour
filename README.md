# SL Building Virtual Tour

Final project for course CSCI 435 Multimedia Information Systems
An interactive indoor virtual tour of the Purdue Science Building 
This project lets users explore the building through **360° panorama scenes**, switch between floors, use a **minimap**, and navigate between connected locations through hotspots and buttons.

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
