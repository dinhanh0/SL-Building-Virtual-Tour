// ---- 1. CONSTANTS -----------------------------------------------
const FLOOR0_PATH = "SLFloors/SLFloor0/"; // base path for floor-0 images
const IDLE_DELAY_MS = 4000;              // minimap dim delay (ms)
const STORAGE_KEY_CURRENT_NODE = "tourCurrentNode";
const DEV_MODE = true;                   // set false to hide overlay later

// ---- 2. GLOBAL STATE --------------------------------------------
let nodes = {};
let currentNodeId = null;

let mapPanel, titleEl, descEl, neighborContainer;
let compassNeedleEl = null;
let panoViewer = null;
let idleTimer = null;
let isMapExpanded = false;

// for dev overlay "click map" mode
let devAwaitMapClick = false;

// ---- 3. INITIALIZATION ------------------------------------------
window.addEventListener("load", () => {
  mapPanel          = document.getElementById("map-panel");
  titleEl           = document.getElementById("location-title");
  descEl            = document.getElementById("location-description");
  neighborContainer = document.getElementById("neighbor-buttons");
  compassNeedleEl   = document.querySelector(".compass-needle");

  setupIdleMinimap();
  setupCompassClick();
  setupMapInteractions();

  // nodes loaded from nodes.js
  nodes = window.NODES || {};
  console.log("nodes after assignment:", nodes);

  if (!nodes || Object.keys(nodes).length === 0) {
    console.error("No nodes found. Check nodes.js");
    return;
  }

  // restore last node from localStorage
  let startNodeId = window.localStorage.getItem(STORAGE_KEY_CURRENT_NODE);
  if (!startNodeId || !nodes[startNodeId]) {
    startNodeId = "n1";  // fallback
  }

  if (!nodes[startNodeId]) {
    console.error("Start node not found in nodes.js");
    return;
  }

  createMapSpots();
  goToNode(startNodeId);   // no override → uses node.defaultYaw/defaultPitch
  startCompassTracking();
  setupYawPitchDebug();
  setupDevOverlay();

  // start live overlay updates
  setInterval(updateDevPanel, 100);
});


// ---- 4. CREATE MAP SPOTS ----------------------------------------
function createMapSpots() {
  if (!mapPanel) return;

  const oldSpots = mapPanel.querySelectorAll(".map-spot");
  oldSpots.forEach(s => s.remove());

  Object.entries(nodes).forEach(([id, node]) => {
    // 👈 NEW: if this node is marked hidden, don't make a dot
    if (node.hideOnMap === true) return;

    const spot = document.createElement("button");
    spot.className = "map-spot";
    spot.style.top = node.mapTop + "%";
    spot.style.left = node.mapLeft + "%";
    spot.title = node.label;
    spot.dataset.nodeId = id;

    // clicking a dot should move to that node, not toggle map expand
    spot.addEventListener("click", (e) => {
      e.stopPropagation();
      goToNode(id);  // map uses defaultYaw/defaultPitch
    });

    mapPanel.appendChild(spot);
  });
}


// ---- 5. MAIN NAVIGATION FUNCTION -------------------------------
// overrideYaw / overridePitch are optional; used for direction-specific views.
function goToNode(id, overrideYaw, overridePitch) {
  const node = nodes[id];
  if (!node) return;

  currentNodeId = id;

  // Remember this node across reloads
  try {
    window.localStorage.setItem(STORAGE_KEY_CURRENT_NODE, id);
  } catch (e) {
    // ignore if storage not available
  }

  // Build hotspots to neighbors for this pano
  const hotSpots = (node.neighbors || [])
    .map(neighbor => {
      const neighborId   = neighbor.id;
      const neighborNode = nodes[neighborId];
      if (!neighborNode) return null;

      return {
        pitch: neighbor.pitch ?? 0,
        yaw:   neighbor.yaw   ?? 0,
        type:  "info",
        text:  "Go to: " + neighborNode.label,

        // If neighbor has viewYaw/viewPitch, use them as overrides when clicked
        clickHandlerFunc: () =>
          goToNode(
            neighborId,
            (typeof neighbor.viewYaw  === "number") ? neighbor.viewYaw  : undefined,
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

    panoViewer = pannellum.viewer("panorama", {
      type: "equirectangular",
      panorama: FLOOR0_PATH + node.image,
      autoLoad: true,
      showZoomCtrl: true,
      compass: false,
      yaw: initialYaw,        // uses override first, then defaultYaw
      pitch: initialPitch,    // uses override first, then defaultPitch
      hotSpots: hotSpots
    });
  } catch (e) {
    console.error("Error loading panorama for node", id, e);
  }

  titleEl.textContent = node.label;
  descEl.textContent  = node.description || "";

  // Neighbor buttons under the viewer
  neighborContainer.innerHTML = "";
  (node.neighbors || []).forEach(neighbor => {
    const neighborId   = neighbor.id;
    const neighborNode = nodes[neighborId];
    if (!neighborNode) return;

    const btn = document.createElement("button");
    btn.className = "nav-btn";
    btn.textContent = "Go to: " + neighborNode.label;

    btn.addEventListener("click", () =>
      goToNode(
        neighborId,
        (typeof neighbor.viewYaw  === "number") ? neighbor.viewYaw  : undefined,
        (typeof neighbor.viewPitch === "number") ? neighbor.viewPitch : undefined
      )
    );

    neighborContainer.appendChild(btn);
  });

  highlightActiveSpot(id);
}


// ---- 6. MAP SPOT HIGHLIGHTING ----------------------------------
function highlightActiveSpot(activeId) {
  if (!mapPanel) return;
  const spots = mapPanel.querySelectorAll(".map-spot");
  spots.forEach(spot => {
    if (spot.dataset.nodeId === activeId) {
      spot.classList.add("active");
    } else {
      spot.classList.remove("active");
    }
  });
}


// ---- 7. COMPASS TRACKING & CLICK TO RECENTER -------------------
function startCompassTracking() {
  if (!compassNeedleEl || !panoViewer) return;

  if (startCompassTracking._intervalId) return; // prevent multiple intervals

  startCompassTracking._intervalId = setInterval(() => {
    if (!panoViewer) return;
    const yaw = panoViewer.getYaw(); // degrees

    // rotate in opposite direction so red tip points north-ish
    compassNeedleEl.style.transform =
      `translate(-50%, -50%) rotate(${-yaw}deg)`;
  }, 60); // ~16 FPS
}

function setupCompassClick() {
  const compass = document.getElementById("compass-widget");
  if (!compass) return;

  compass.addEventListener("click", () => {
    if (!panoViewer) return;
    // recenters the view: yaw 0, pitch 0
    panoViewer.setYaw(0);
    panoViewer.setPitch(0);
  });
}


// ---- 8. MINIMAP IDLE DIMMING + EXPAND/SHRINK -------------------
function setupIdleMinimap() {
  if (!mapPanel) return;

  const resetIdle = () => {
    if (!mapPanel) return;
    mapPanel.classList.remove("dimmed");
    if (idleTimer) clearTimeout(idleTimer);

    idleTimer = setTimeout(() => {
      if (!isMapExpanded) {
        mapPanel.classList.add("dimmed");
      }
    }, IDLE_DELAY_MS);
  };

  // Save ref so other functions can rearm it
  window.__resetMinimapIdle = resetIdle;

  // Reset on user activity
  ["mousemove", "mousedown", "wheel", "keydown", "touchstart"].forEach(evt => {
    document.addEventListener(evt, resetIdle, { passive: true });
  });

  resetIdle();
}

function setupMapInteractions() {
  if (!mapPanel) return;

  mapPanel.addEventListener("click", (e) => {
    // if dev "waiting for map click", capture mapTop/mapLeft instead
    if (DEV_MODE && devAwaitMapClick && currentNodeId) {
      const rect   = mapPanel.getBoundingClientRect();
      const topPct = ((e.clientY - rect.top)  / rect.height) * 100;
      const leftPct = ((e.clientX - rect.left) / rect.width)  * 100;

      // Python-ready snippet for MAP_POSITIONS
      devLog(
        `"${currentNodeId}": (${topPct.toFixed(1)}, ${leftPct.toFixed(1)}),`
      );
      devAwaitMapClick = false;
      return; // don't toggle expand
    }

    // Clicking background or map image toggles expanded mode.
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


// ---- 9. YAW / PITCH DEBUG (cursor-based) ------------------------
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

    dbg.textContent =
      `View Yaw: ${viewYaw.toFixed(1)}, Pitch: ${viewPitch.toFixed(1)} ` +
      `| Cursor Yaw: ${yaw.toFixed(1)}, Pitch: ${pitch.toFixed(1)}`;
  });
}


// ---- 10. ON-SCREEN DEV OVERLAY ---------------------------------
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

      const yaw   = panoViewer.getYaw().toFixed(1);
      const pitch = panoViewer.getPitch().toFixed(1);
      devLog(
        `# EDGE_VIEW_ORIENTATIONS\n("${currentNodeId}", "${toNode}"): (${yaw}, ${pitch}),`
      );
    };
  }

  // NEIGHBOR_YAWS (icon yaw/pitch hotspot)
  if (btnIcon) {
    btnIcon.onclick = () => {
      if (!panoViewer || !currentNodeId || !neighborSel) return;
      const toNode = neighborSel.value;
      if (!toNode) return;

      const yaw   = panoViewer.getYaw().toFixed(1);
      const pitch = panoViewer.getPitch().toFixed(1);
      devLog(
        `# NEIGHBOR_YAWS\n("${currentNodeId}", "${toNode}"): (${yaw}, ${pitch}),`
      );
    };
  }

  // EXTRA_LINKS (third directions / shortcuts) with viewYaw/viewPitch
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
}

// Dev output helper
function devLog(text) {
  const box = document.getElementById("dev-output-box");
  if (!box) return;
  box.value = text;
}

// Live dev panel info (node, yaw/pitch, neighbor list)
function updateDevPanel() {
  if (!DEV_MODE) return;
  if (!panoViewer || !currentNodeId) return;

  const yaw   = panoViewer.getYaw().toFixed(1);
  const pitch = panoViewer.getPitch().toFixed(1);

  const nodeLabel = document.getElementById("dev-current-node");
  const viewLabel = document.getElementById("dev-view");
  const select    = document.getElementById("dev-neighbor-select");

  if (nodeLabel) {
    nodeLabel.textContent = `Node: ${currentNodeId}`;
  }
  if (viewLabel) {
    viewLabel.textContent = `Yaw: ${yaw} | Pitch: ${pitch}`;
  }

  if (select) {
    const previous = select.value; // remember current choice

    select.innerHTML = "";
    const node = nodes[currentNodeId];

    (node.neighbors || []).forEach(n => {
      const opt = document.createElement("option");
      opt.value = n.id;
      opt.textContent = n.id;
      select.appendChild(opt);
    });

    // try to restore previous selection if it still exists
    if (previous) {
      const options = Array.from(select.options).map(o => o.value);
      if (options.includes(previous)) {
        select.value = previous;
      }
    }

    // if nothing selected, default to first option
    if (!select.value && select.options.length > 0) {
      select.value = select.options[0].value;
    }
  }
}
