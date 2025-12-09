// ---- 1. DEFINE YOUR NODES HERE ----------------------------------
// top/left are in PERCENT of the map image (0–100).

// For now we’re only using Floor 0 images:
const FLOOR0_PATH = "SLFloors/SLFloor0/";

// TODO: Update these image filenames to match the ones
// you actually have in SLFloors/SLFloor0/ (e.g., "SL0_085.jpg").
const nodes = {
  n1: { 
    image: "SL0_084.jpg",
    label: "Image 1",
    description: "Temporary description",
    neighbors: ["n2"],
    mapTop: 50,
    mapLeft: 30
  },
  n2: { 
    image: "SL0_085.jpg",
    label: "Image 2",
    description: "Temporary description",
    neighbors: ["n1", "n3"],
    mapTop: 55,
    mapLeft: 32
  },
  n3: { 
    image: "SL0_086.jpg",
    label: "Image 3",
    description: "Temporary description",
    neighbors: ["n2"],
    mapTop: 60,
    mapLeft: 35
  }
};


// ---- 2. GLOBAL STATE --------------------------------------------

let currentNodeId = null;
let mapPanel, titleEl, descEl, neighborContainer;
let panoViewer = null;   // Pannellum viewer instance


// ---- 3. INITIALIZATION ------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
  mapPanel = document.getElementById("map-panel");
  titleEl = document.getElementById("location-title");
  descEl = document.getElementById("location-description");
  neighborContainer = document.getElementById("neighbor-buttons");

  // Create 360 viewer once, using n1 as the initial scene
  const startNodeId = "n1";
  const startNode = nodes[startNodeId];

  panoViewer = pannellum.viewer("panorama", {
    type: "equirectangular",
    panorama: FLOOR0_PATH + startNode.image,
    autoLoad: true,
    showZoomCtrl: true,
    compass: false
  });

  createMapSpots();

  // Start at default node
  goToNode(startNodeId);
});


// ---- 4. CREATE MAP SPOTS ----------------------------------------

function createMapSpots() {
  Object.entries(nodes).forEach(([id, node]) => {
    const spot = document.createElement("button");
    spot.className = "map-spot";
    spot.style.top = node.mapTop + "%";
    spot.style.left = node.mapLeft + "%";
    spot.title = node.label;
    spot.dataset.nodeId = id;
    spot.addEventListener("click", () => goToNode(id));
    mapPanel.appendChild(spot);
  });
}


// ---- 5. MAIN NAVIGATION FUNCTION -------------------------------
function goToNode(id) {
  const node = nodes[id];
  if (!node) return;

  currentNodeId = id;

  // --- build hotspots for neighbors (arrows / dots inside pano) ---
  const hotSpots = (node.neighbors || []).map((neighborId, idx) => {
    const neighbor = nodes[neighborId];
    if (!neighbor) return null;

    // Basic placement: spread them around horizontally.
    // You can tweak yaw/pitch later for each node if you want.
    const yaw = -60 + idx * 60;  // -60, 0, 60, ... degrees
    const pitch = 0;             // 0 = horizon level

    return {
      pitch: pitch,
      yaw: yaw,
      type: "info",                     // clickable hotspot
      text: "Go to: " + neighbor.label, // hover text
      clickHandlerFunc: () => goToNode(neighborId)
    };
  }).filter(Boolean);

  // destroy old viewer (if any) and create a new one with hotspots
  try {
    if (panoViewer) {
      panoViewer.destroy();
      panoViewer = null;
    }

    panoViewer = pannellum.viewer("panorama", {
      type: "equirectangular",
      panorama: FLOOR0_PATH + node.image,
      autoLoad: true,
      showZoomCtrl: true,
      compass: false,
      hotSpots: hotSpots
    });
  } catch (e) {
    console.error("Error loading panorama for node", id, e);
  }

  // update text
  titleEl.textContent = node.label;
  descEl.textContent = node.description || "";

  // update neighbor buttons under the viewer (keep these too)
  neighborContainer.innerHTML = "";
  (node.neighbors || []).forEach(neighborId => {
    const neighbor = nodes[neighborId];
    if (!neighbor) return;

    const btn = document.createElement("button");
    btn.className = "nav-btn";
    btn.textContent = "Go to: " + neighbor.label;
    btn.addEventListener("click", () => goToNode(neighborId));
    neighborContainer.appendChild(btn);
  });

  // highlight active spot on the map
  highlightActiveSpot(id);
}


function highlightActiveSpot(activeId) {
  const spots = mapPanel.querySelectorAll(".map-spot");
  spots.forEach(spot => {
    if (spot.dataset.nodeId === activeId) {
      spot.classList.add("active");
    } else {
      spot.classList.remove("active");
    }
  });
}
