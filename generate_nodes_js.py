import os

# ------------ CONFIG -------------------------------------------------

IMAGE_DIR = "SLFloors/SLFloor0"
OUTPUT_JS = "nodes.js"

YAW_FORWARD = 20
YAW_BACK = -120
YAW_LEFT = -90
YAW_RIGHT = 90
PITCH_DEFAULT = 0

MAP_TOP_START = 40
MAP_LEFT_START = 30
MAP_STEP = 1

# ------------ EXTRA NEIGHBOR LINKS (third directions, shortcuts) ----
# Format: (from_node, to_node, direction[, view_yaw, view_pitch])
# direction ∈ {"forward", "back", "left", "right"}
EXTRA_LINKS = [
    # examples:
    # ("n2", "n25", "left"),
    # ("n25", "n2", "right", 0.0, 0.0),
]

DIR_TO_YAW = {
    "forward": YAW_FORWARD,
    "back": YAW_BACK,
    "left": YAW_LEFT,
    "right": YAW_RIGHT,
}

# ------------ DEFAULT ORIENTATIONS ----------------------------------
# Add entries like:
#   "n2": (yaw, pitch)
DEFAULT_ORIENTATIONS = {
    # "n2": (178.1, 22.8),
}

# ------------ EDGE VIEW ORIENTATIONS (arrival view per edge) -------
# Entries like:
#   ("n3", "n2"): (yaw, pitch)
EDGE_VIEW_ORIENTATIONS = {
    # ("n2", "n1"): (-10.6, 11.1),
    # ("n2", "n3"): (178.1, 22.8),
}

# ------------ ICON YAW / PITCH PER EDGE -----------------------------
# This controls the hotspot position (icon) for a specific edge.
# Entries like:
#   ("n2", "n3"): (yaw, pitch)
NEIGHBOR_YAWS = {
    # ("n2", "n3"): (175.0, 0.0),
}


# ====================================================================
def main():
    # 1. Collect images
    files = sorted([
        f for f in os.listdir(IMAGE_DIR)
        if os.path.splitext(f)[1].lower() in {".jpg", ".jpeg", ".png"}
    ])

    if not files:
        raise SystemExit(f"No images found in: {IMAGE_DIR}")

    print(f"Found {len(files)} images.")

    # 2. Build base node list (linear prev/next)
    nodes = {}

    for i, filename in enumerate(files, start=1):
        node_id = f"n{i}"

        neighbors = []

        # back neighbor (i-1)
        if i > 1:
            back_id = f"n{i-1}"
            yaw_back = YAW_BACK
            pitch_back = PITCH_DEFAULT
            pair_back = (node_id, back_id)
            if pair_back in NEIGHBOR_YAWS:
                yaw_back, pitch_back = NEIGHBOR_YAWS[pair_back]
            neighbors.append({"id": back_id, "yaw": yaw_back, "pitch": pitch_back})

        # forward neighbor (i+1)
        if i < len(files):
            fwd_id = f"n{i+1}"
            yaw_fwd = YAW_FORWARD
            pitch_fwd = PITCH_DEFAULT
            pair_fwd = (node_id, fwd_id)
            if pair_fwd in NEIGHBOR_YAWS:
                yaw_fwd, pitch_fwd = NEIGHBOR_YAWS[pair_fwd]
            neighbors.append({"id": fwd_id, "yaw": yaw_fwd, "pitch": pitch_fwd})

        map_top = min(100, MAP_TOP_START + (i - 1) * MAP_STEP)
        map_left = min(100, MAP_LEFT_START + (i - 1) * MAP_STEP)

        # Default camera orientation
        default_yaw, default_pitch = DEFAULT_ORIENTATIONS.get(node_id, (0, 0))

        nodes[node_id] = {
            "image": filename,
            "label": f"Image {i}",
            "description": "",
            "defaultYaw": default_yaw,
            "defaultPitch": default_pitch,
            "neighbors": neighbors,
            "mapTop": map_top,
            "mapLeft": map_left
        }

    # 3. Apply EXTRA_LINKS (including optional view overrides)
    for entry in EXTRA_LINKS:
        if len(entry) not in (3, 5):
            print(f"WARNING: EXTRA_LINK invalid format: {entry}")
            continue

        if len(entry) == 3:
            from_id, to_id, direction = entry
            view_yaw = None
            view_pitch = None
        else:
            from_id, to_id, direction, view_yaw, view_pitch = entry

        if from_id not in nodes or to_id not in nodes:
            print(f"WARNING: invalid EXTRA_LINK: {from_id} -> {to_id}")
            continue
        if direction not in DIR_TO_YAW:
            print(f"WARNING: invalid direction '{direction}' in EXTRA_LINK: {entry}")
            continue

        base_yaw = DIR_TO_YAW[direction]

        # allow NEIGHBOR_YAWS to override icon yaw/pitch for this extra link
        icon_yaw, icon_pitch = base_yaw, PITCH_DEFAULT
        pair = (from_id, to_id)
        if pair in NEIGHBOR_YAWS:
            icon_yaw, icon_pitch = NEIGHBOR_YAWS[pair]

        neighbor_dict = {
            "id": to_id,
            "yaw": icon_yaw,
            "pitch": icon_pitch,
        }
        if view_yaw is not None:
            neighbor_dict["viewYaw"] = view_yaw
        if view_pitch is not None:
            neighbor_dict["viewPitch"] = view_pitch

        nodes[from_id]["neighbors"].append(neighbor_dict)
        print(f"Added extra link: {from_id} -> {to_id} ({direction}, yaw={base_yaw})")

    # 4. Apply EDGE_VIEW_ORIENTATIONS to existing neighbors
    for (from_id, to_id), (view_yaw, view_pitch) in EDGE_VIEW_ORIENTATIONS.items():
        if from_id not in nodes:
            print(f"WARNING: EDGE_VIEW_ORIENTATIONS from_id {from_id} not in nodes")
            continue

        neighbor_list = nodes[from_id]["neighbors"]
        found = False
        for n in neighbor_list:
            if n["id"] == to_id:
                n["viewYaw"] = view_yaw
                n["viewPitch"] = view_pitch
                found = True
                break
        if not found:
            print(f"WARNING: EDGE_VIEW_ORIENTATIONS pair {from_id}->{to_id} not found among neighbors")

    # 5. Write nodes.js
    print("\nWriting nodes.js...")

    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write("// Auto-generated by generate_nodes_js.py\n")
        f.write("window.NODES = {\n\n")

        for i in range(1, len(files) + 1):
            node_id = f"n{i}"
            node = nodes[node_id]

            neighbor_lines = []
            for n in node["neighbors"]:
                parts = [
                    f'id: "{n["id"]}"',
                    f"yaw: {n['yaw']}",
                    f"pitch: {n['pitch']}",
                ]
                if "viewYaw" in n:
                    parts.append(f"viewYaw: {n['viewYaw']}")
                if "viewPitch" in n:
                    parts.append(f"viewPitch: {n['viewPitch']}")
                neighbor_lines.append("      { " + ", ".join(parts) + " }")

            neighbors_block = ",\n".join(neighbor_lines)

            block = f"""  {node_id}: {{
    image: "{node["image"]}",
    label: "{node["label"]}",
    description: "",
    defaultYaw: {node["defaultYaw"]},
    defaultPitch: {node["defaultPitch"]},
    neighbors: [
{neighbors_block}
    ],
    mapTop: {node["mapTop"]},
    mapLeft: {node["mapLeft"]}
  }}"""

            if i < len(files):
                block += ","

            f.write(block + "\n\n")

        f.write("};\n")

    print("nodes.js generated successfully.")


if __name__ == "__main__":
    main()
