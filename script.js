// 1. CONSTANTS
const STORAGE_KEY_CURRENT_NODE  = "tourCurrentNode";
const STORAGE_KEY_CURRENT_FLOOR = "tourCurrentFloor";
const DEV_MODE = true;   // turn false to hide dev overlay

// Where the pano images live per floor
const FLOOR_PATHS = {
  "0": "SLFloors/SLFloor0/",
  "1": "SLFloors/SLFloor1/",
  "2": "SLFloors/SLFloor2/",
  "3": "SLFloors/SLFloor3/",
  
};

// Minimap image per floor
const MAP_IMAGES = {
  "0": "floorplan(edited)/floor0.png",
  "1": "floorplan(edited)/floor1.png",
  "2": "floorplan(edited)/floor2.png",
  "3": "floorplan(edited)/floor3.png",
};

const IDLE_DELAY_MS = 4000;

// 2. GLOBAL STATE
let NODES_BY_FLOOR = {};   // filled on load: { "0": window.NODES_F0, "1": window.NODES_F1 }
let currentFloor   = "0";
let nodes          = {};   // shortcut for NODES_BY_FLOOR[currentFloor]
let currentNodeId  = null;

let mapPanel, mapImg, titleEl, descEl, neighborContainer;
let compassNeedleEl = null;
let panoViewer      = null;
let idleTimer       = null;
let isMapExpanded   = false;
let devAwaitMapClick = false;
let lastCursorYaw = null;
let lastCursorPitch = null;
let devIconArmed = false;   // Q + right-click for ICON_YAW


// 3. INITIALIZATION
window.addEventListener("load", () => {
  mapPanel          = document.getElementById("map-panel");
  mapImg            = document.getElementById("map-image");
  titleEl           = document.getElementById("location-title");
  descEl            = document.getElementById("location-description");
  neighborContainer = document.getElementById("neighbor-buttons");
  compassNeedleEl   = document.querySelector(".compass-needle");

  // Floor data from JS files
  NODES_BY_FLOOR = {
    "0": window.NODES_F0,
    "1": window.NODES_F1,
    "2": window.NODES_F2,
    "3": window.NODES_F3,
  };

  // Recover last floor/node if possible
  const savedFloor = window.localStorage.getItem(STORAGE_KEY_CURRENT_FLOOR);
  if (savedFloor && NODES_BY_FLOOR[savedFloor]) {
    currentFloor = savedFloor;
  } else {
    currentFloor = "0";
  }
  nodes = NODES_BY_FLOOR[currentFloor];

  if (!nodes) {
    console.error("No nodes for floor", currentFloor);
    return;
  }

  let startNodeId = window.localStorage.getItem(STORAGE_KEY_CURRENT_NODE);
  if (!startNodeId || !nodes[startNodeId]) {
    // fallback: first key of this floor
    startNodeId = Object.keys(nodes)[0];
  }

  setupIdleMinimap();
  setupCompassClick();
  setupMapInteractions();
  setupFloorButtons();
  setupYawPitchDebug();
  setupDevOverlay();

  updateFloorUI();     // sets map image + active button + dots
  goToNode(startNodeId);

  startCompassTracking();
  setInterval(updateDevPanel, 100);
});

// 4. FLOOR SWITCHING

function updateFloorUI() {
  // activate correct floor button
  const buttons = document.querySelectorAll(".floor-btn");
  buttons.forEach(btn => {
    btn.classList.toggle("active", btn.dataset.floor === currentFloor);
  });

  // swap minimap image
  if (mapImg && MAP_IMAGES[currentFloor]) {
    mapImg.src = MAP_IMAGES[currentFloor];
  }

  // update nodes + rebuild dots
  nodes = NODES_BY_FLOOR[currentFloor];
  createMapSpots();
}

function setupFloorButtons() {
  const buttons = document.querySelectorAll(".floor-btn");
  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const floor = btn.dataset.floor;
      if (!NODES_BY_FLOOR[floor]) return;

      currentFloor = floor;
      window.localStorage.setItem(STORAGE_KEY_CURRENT_FLOOR, floor);

      updateFloorUI();

      // jump to first node on that floor
      const startId = Object.keys(NODES_BY_FLOOR[floor])[0];
      goToNode(startId);
    });
  });
}

// 5. MAP DOTS

function createMapSpots() {
  if (!mapPanel || !nodes) return;

  const oldSpots = mapPanel.querySelectorAll(".map-spot");
  oldSpots.forEach(s => s.remove());

  Object.entries(nodes).forEach(([id, node]) => {
    if (node.hideOnMap === true) return;

    const spot = document.createElement("button");
    spot.className = "map-spot";
    spot.style.top  = node.mapTop + "%";
    spot.style.left = node.mapLeft + "%";
    spot.title = node.label;
    spot.dataset.nodeId = id;

    spot.addEventListener("click", (e) => {
      e.stopPropagation();
      goToNode(id);
    });

    mapPanel.appendChild(spot);
  });
}

function highlightActiveSpot(activeId) {
  if (!mapPanel) return;
  const spots = mapPanel.querySelectorAll(".map-spot");
  spots.forEach(spot => {
    spot.classList.toggle("active", spot.dataset.nodeId === activeId);
  });
}

// 6. MAIN NAVIGATION

// Try to find the node on current floor; if not found, search other floors
function resolveNodeAcrossFloors(id) {
  let node = nodes[id];
  if (node) return node;

  for (const [floorKey, floorNodes] of Object.entries(NODES_BY_FLOOR)) {
    if (floorNodes && floorNodes[id]) {
      currentFloor = floorKey;
      nodes = floorNodes;
      window.localStorage.setItem(STORAGE_KEY_CURRENT_FLOOR, floorKey);
      updateFloorUI();
      return nodes[id];
    }
  }
  return null;
}

function goToNode(id, overrideYaw, overridePitch) {
  const node = resolveNodeAcrossFloors(id);
  if (!node) {
    console.warn("Node not found on any floor:", id);
    return;
  }

  currentNodeId = id;
  try {
    window.localStorage.setItem(STORAGE_KEY_CURRENT_NODE, id);
  } catch (_) {}

  // Build hotspots
  const hotSpots = (node.neighbors || [])
    .map(neighbor => {
      const neighborId   = neighbor.id;
      // We don't know which floor neighbor is on yet; resolve lazily on click
      return {
        pitch: neighbor.pitch ?? 0,
        yaw:   neighbor.yaw   ?? 0,
        type:  "info",
        text:  "Go to: " + neighborId,
        clickHandlerFunc: () =>
          goToNode(
            neighborId,
            (typeof neighbor.viewYaw   === "number") ? neighbor.viewYaw   : undefined,
            (typeof neighbor.viewPitch === "number") ? neighbor.viewPitch : undefined
          )
      };
    })
    .filter(Boolean);

  try {
    if (panoViewer) {
      panoViewer.destroy();
      panoViewer = null;
    }

    const initialYaw =
      (typeof overrideYaw === "number")
        ? overrideYaw
        : (typeof node.defaultYaw === "number" ? node.defaultYaw : 0);

    const initialPitch =
      (typeof overridePitch === "number")
        ? overridePitch
        : (typeof node.defaultPitch === "number" ? node.defaultPitch : 0);

    const panoPath = FLOOR_PATHS[currentFloor] + node.image;

    panoViewer = pannellum.viewer("panorama", {
      type:      "equirectangular",
      panorama:  panoPath,
      autoLoad:  true,
      showZoomCtrl: true,
      compass:   false,
      yaw:   initialYaw,
      pitch: initialPitch,
      hotSpots: hotSpots
    });
  } catch (e) {
    console.error("Error loading panorama for node", id, e);
  }

  titleEl.textContent = node.label;
  descEl.textContent  = node.description || "";

  // Neighbor buttons under viewport
  neighborContainer.innerHTML = "";
  (node.neighbors || []).forEach(neighbor => {
    const btn = document.createElement("button");
    btn.className = "nav-btn";
    btn.textContent = "Go to: " + neighbor.id;
    btn.addEventListener("click", () =>
      goToNode(
        neighbor.id,
        (typeof neighbor.viewYaw   === "number") ? neighbor.viewYaw   : undefined,
        (typeof neighbor.viewPitch === "number") ? neighbor.viewPitch : undefined
      )
    );
    neighborContainer.appendChild(btn);
  });

  highlightActiveSpot(id);
}

// 7. COMPASS

function startCompassTracking() {
  if (!compassNeedleEl) return;
  if (startCompassTracking._intervalId) return;

  startCompassTracking._intervalId = setInterval(() => {
    if (!panoViewer) return;
    const yaw = panoViewer.getYaw();
    compassNeedleEl.style.transform =
      `translate(-50%, -50%) rotate(${-yaw}deg)`;
  }, 60);
}

function setupCompassClick() {
  const compass = document.getElementById("compass-widget");
  if (!compass) return;

  compass.addEventListener("click", () => {
    if (!panoViewer) return;
    panoViewer.setYaw(0);
    panoViewer.setPitch(0);
  });
}

// 8. MINIMAP IDLE / EXPAND

function setupIdleMinimap() {
  if (!mapPanel) return;

  const resetIdle = () => {
    mapPanel.classList.remove("dimmed");
    if (idleTimer) clearTimeout(idleTimer);

    idleTimer = setTimeout(() => {
      if (!isMapExpanded) {
        mapPanel.classList.add("dimmed");
      }
    }, IDLE_DELAY_MS);
  };

  window.__resetMinimapIdle = resetIdle;

  ["mousemove", "mousedown", "wheel", "keydown", "touchstart"].forEach(evt => {
    document.addEventListener(evt, resetIdle, { passive: true });
  });

  resetIdle();
}

function setupMapInteractions() {
  if (!mapPanel) return;

  mapPanel.addEventListener("click", (e) => {
    if (DEV_MODE && devAwaitMapClick && currentNodeId) {
      const rect = mapPanel.getBoundingClientRect();
      const topPct  = ((e.clientY - rect.top)  / rect.height) * 100;
      const leftPct = ((e.clientX - rect.left) / rect.width)  * 100;
      devLog(
        `"${currentNodeId}": (${topPct.toFixed(1)}, ${leftPct.toFixed(1)}),`
      );
      devAwaitMapClick = false;
      return;
    }

    if (e.target.classList.contains("map-spot")) return;
    toggleMapExpanded();
  });
}

function toggleMapExpanded() {
  if (!mapPanel) return;

  isMapExpanded = !isMapExpanded;
  if (isMapExpanded) {
    mapPanel.classList.add("expanded");
    mapPanel.classList.remove("dimmed");
  } else {
    mapPanel.classList.remove("expanded");
    if (typeof window.__resetMinimapIdle === "function") {
      window.__resetMinimapIdle();
    }
  }
}

// 9. YAW/PITCH DEBUG

function setupYawPitchDebug() {
  const dbg     = document.getElementById("debug-orient");
  const panoDiv = document.getElementById("panorama");
  if (!dbg || !panoDiv) return;

  panoDiv.addEventListener("mousemove", (e) => {
    if (!panoViewer) return;

    const coords = panoViewer.mouseEventToCoords(e);
    if (!coords) return;

    const [pitch, yaw] = coords;
    const viewYaw   = panoViewer.getYaw();
    const viewPitch = panoViewer.getPitch();

    // remember last cursor coords for the Q + right-click shortcut
    lastCursorYaw = yaw;
    lastCursorPitch = pitch;

    dbg.textContent =
      `View Yaw: ${viewYaw.toFixed(1)}, Pitch: ${viewPitch.toFixed(1)} ` +
      `| Cursor Yaw: ${yaw.toFixed(1)}, Pitch: ${pitch.toFixed(1)}`;
  });
}

// 10. DEV OVERLAY

function logNeighborYaw(fromId, toId, yaw, pitch) {
  if (!fromId || !toId) return;

  const yawStr   = yaw.toFixed(1);
  const pitchStr = pitch.toFixed(1);

  devLog(
    `# NEIGHBOR_YAWS\n("${fromId}", "${toId}"): (${yawStr}, ${pitchStr}),`
  );
}

function setupDevOverlay() {
  if (!DEV_MODE) {
    const box = document.getElementById("onscreen-dev");
    if (box) box.style.display = "none";
    return;
  }

  const btnDefault   = document.getElementById("dev-btn-default");
  const btnEdge      = document.getElementById("dev-btn-edge");
  const btnIcon      = document.getElementById("dev-btn-icon");
  const btnExtra     = document.getElementById("dev-btn-extra");
  const btnMap       = document.getElementById("dev-btn-map");
  const neighborSel  = document.getElementById("dev-neighbor-select");
  const extraDirSel  = document.getElementById("dev-extra-dir");
  const panoDiv      = document.getElementById("panorama");

  // DEFAULT_ORIENTATIONS
  if (btnDefault) {
    btnDefault.onclick = () => {
      if (!panoViewer || !currentNodeId) return;
      const yaw   = panoViewer.getYaw().toFixed(1);
      const pitch = panoViewer.getPitch().toFixed(1);
      devLog(`# DEFAULT_ORIENTATIONS\n"${currentNodeId}": (${yaw}, ${pitch}),`);
    };
  }

  // EDGE_VIEW_ORIENTATIONS (arrival camera orientation)
  if (btnEdge) {
    btnEdge.onclick = () => {
      if (!panoViewer || !currentNodeId || !neighborSel) return;
      const toNode = neighborSel.value;
      if (!toNode) return;

      const yaw   = panoViewer.getYaw();
      const pitch = panoViewer.getPitch();
      devLog(
        `# EDGE_VIEW_ORIENTATIONS\n("${currentNodeId}", "${toNode}"): (${yaw.toFixed(1)}, ${pitch.toFixed(1)}),`
      );
    };
  }

  // NEIGHBOR_YAWS (icon yaw/pitch hotspot) – uses VIEW yaw/pitch
  if (btnIcon) {
    btnIcon.onclick = () => {
      if (!panoViewer || !currentNodeId || !neighborSel) return;
      const toNode = neighborSel.value;
      if (!toNode) return;

      const yaw   = panoViewer.getYaw();
      const pitch = panoViewer.getPitch();
      logNeighborYaw(currentNodeId, toNode, yaw, pitch);
    };
  }

  // EXTRA_LINKS (third directions / shortcuts)
  if (btnExtra) {
    btnExtra.onclick = () => {
      if (!panoViewer || !currentNodeId || !neighborSel || !extraDirSel) return;
      const toNode    = neighborSel.value;
      const direction = extraDirSel.value;
      if (!toNode || !direction) return;

      const yaw   = panoViewer.getYaw().toFixed(1);
      const pitch = panoViewer.getPitch().toFixed(1);

      devLog(
        `# EXTRA_LINKS\n("${currentNodeId}", "${toNode}", "${direction}", ${yaw}, ${pitch}),`
      );
    };
  }

  // MAP_POSITIONS (mapTop/mapLeft)
  if (btnMap) {
    btnMap.onclick = () => {
      if (!mapPanel || !currentNodeId) return;
      devAwaitMapClick = true;
      devLog("# MAP_POSITIONS\nClick on the minimap to record mapTop/mapLeft.");
    };
  }

  // Q + right-click on pano → ICON yaw/pitch from CURSOR
  document.addEventListener("keydown", (e) => {
    if (e.key === "q" || e.key === "Q") {
      devIconArmed = true;
    }
  });

  if (panoDiv) {
    panoDiv.addEventListener("contextmenu", (e) => {
      if (!DEV_MODE || !devIconArmed) return;
      if (!currentNodeId || !neighborSel || !neighborSel.value) return;
      if (lastCursorYaw == null || lastCursorPitch == null) return;

      e.preventDefault(); // don't open browser context menu

      const toNode = neighborSel.value;
      logNeighborYaw(currentNodeId, toNode, lastCursorYaw, lastCursorPitch);

      // disarm so you don't accidentally spam
      devIconArmed = false;
    });
  }
}


function devLog(text) {
  const box = document.getElementById("dev-output-box");
  if (!box) return;
  box.value = text;
}

function updateDevPanel() {
  if (!DEV_MODE || !panoViewer || !currentNodeId) return;

  const yaw   = panoViewer.getYaw().toFixed(1);
  const pitch = panoViewer.getPitch().toFixed(1);

  const nodeLabel = document.getElementById("dev-current-node");
  const viewLabel = document.getElementById("dev-view");
  const select    = document.getElementById("dev-neighbor-select");

  if (nodeLabel) nodeLabel.textContent = `Node: ${currentNodeId}`;
  if (viewLabel) viewLabel.textContent = `Yaw: ${yaw} | Pitch: ${pitch}`;

  if (select) {
    const previous = select.value;
    select.innerHTML = "";

    const node = nodes[currentNodeId];
    (node.neighbors || []).forEach(n => {
      const opt = document.createElement("option");
      opt.value = n.id;
      opt.textContent = n.id;
      select.appendChild(opt);
    });

    if (previous && Array.from(select.options).some(o => o.value === previous)) {
      select.value = previous;
    } else if (select.options.length > 0) {
      select.value = select.options[0].value;
    }
  }
}
