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
    ("n4", "n17","forward"),

    ("n17", "n4","left"),

    ("n5", "n7", "forward"),

    ("n7", "n5", "forward"),

    ("n10", "n21","forward"),
    ("n21", "n10", "forward"),

    ("n21", "n12", "forward"),
    ("n12", "n21", "forward"),

    ("n12", "n24", "forward"),
    ("n24", "n12", "forward"),

    ("n13", "n18", "forward"),
    ("n18", "n13", "forward"),

    ("n14", "n16", "forward"),
    ("n16", "n14", "forward"),

    ("n7", "n18", "forward"),
    ("n18", "n7", "forward"),

    ("n21", "n23", "forward"),
    ("n23", "n21", "forward"),

    ("n24", "n20", "forward"),
    ("n20", "n24", "forward"),



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
    "n1": (180, 0),
    #"n2": (-180.0, 0.0),
    "n3": (180.0, 0.0)
    
}

# ------------ EDGE VIEW ORIENTATIONS (arrival view per edge) -------
# Entries like:
#   ("n3", "n2"): (yaw, pitch)
EDGE_VIEW_ORIENTATIONS = {
    # ("n2", "n1"): (-10.6, 11.1),
    # ("n2", "n3"): (178.1, 22.8),
    ("n1", "n2"): (180, 0),

    ("n2", "n1"): (0, 0),
    ("n2", "n3"): (180.0, 0),

    ("n3", "n2"): (0, 0),
    ("n3", "n4"): (-180, 0),

    ("n4", "n3"): (0, 0),
    ("n4", "n5"): (180, 0),
    ("n4", "n17"): (-10, 7.6),

    ("n5", "n7"): (180, 0),

    ("n6", "n5"): (86, -7.6),

    ("n7", "n5"): (-6, -7.6),
    ("n7", "n8"): (180, 0),
    ("n7", "n18"): (175, 2),

    ("n8", "n9"): (178, 0),

    ("n9", "n10"): (180, 0),

    ("n10", "n9"): (-100, 0),
    ("n10", "n21"): (-2, 10),
    


    ("n12", "n24"): (130, 0),
    ("n12", "n13"): (180, 0),
    ("n12", "n21"): (180, 0),

    ("n13", "n14"): (180, 0),


    ("n14", "n15"): (-180, 0),

    ("n14", "n16"): (-90, 0),
    ("n15", "n14"): (88, 0),

    ("n16", "n17"): (180, 0),

    ("n17", "n16"): (0, 0),
    ("n17", "n4"): (-90, 4),

    ("n18", "n7"): (-97, 6),
    ("n18", "n13"): (-90, 0), 

    ("n20", "n24"): (40, 2),


    ("n21", "n12"): (-90, 4),
    ("n21", "n23"): (-40, -2),

    ("n22", "n23"): (143, 9),
    ("n23", "n22"): (90, 5),

    ("n24", "n12"): (180,0),
    ("n24", "n20"): (180,0),








    
}

# ------------ ICON YAW / PITCH PER EDGE -----------------------------
# This controls the hotspot position (icon) for a specific edge.
# Entries like:
#   ("n2", "n3"): (yaw, pitch)
NEIGHBOR_YAWS = {
    # ("n2", "n3"): (175.0, 0.0),
    ("n1", "n2"): (-178, -22),

    ("n2", "n1"): (-12, 26.9),
    ("n2", "n3"): (-180, 0),

    ("n3", "n2"): (-1.0, 4),
    ("n3", "n4"): (178,-8),

    ("n4", "n3"): (-4,-4),
    ("n4", "n5"): (177,-8),
    ("n4", "n17"): (88, -5),

    ("n5", "n6"): (-65, -2),
    ("n5", "n4"): (-1, -5),
    ("n5", "n7"): (180, -8),

    ("n6", "n5"): (-78, -8),

    ("n7", "n5"): (-5, -6),
    ("n7", "n8"): (175, -4),
    ("n7", "n18"): (86, -1),


    ("n8", "n7"): (-3, 0),
    ("n8", "n9"): (178, -6),

    ("n9", "n8"): (-6, -8),
    ("n9", "n10"): (86, 0),

    ("n10", "n9"): (-4, 0),
    ("n10", "n21"): (180, -5),
     
    ("n21", "n10"): (180, -2),
    ("n21", "n12"): (-2, 3),
    ("n21", "n23"): (-78, 2),


    ("n12", "n21"): (90, -4),
    ("n12", "n24"): (0.4,0.9),
    ("n12", "n13"): (180, -4),
    ("n12", "n14"): (180, -4),

    ("n13", "n14"): (176, -4),
    ("n13", "n12"): (-6, 3),
    ("n13", "n18"): (84,0),


    ("n14", "n15"): (-90, 0),
    ("n14", "n13"): (-4, 3),
    ("n14", "n16"): (180,-4),


    ("n15", "n14"): (-2, 5),

    ("n16", "n14"): (82, -5),
    ("n16", "n17"): (173, -3),

    ("n17", "n4"): (175, -5), 
    ("n17", "n16"): (-11, 4), 

    ("n18", "n7"): (-8, 2), 
    ("n18", "n19"): (-8, 2), 
    ("n18", "n13"): (175, -3), 

    ("n19", "n18"): (-8, 2), 
    ("n20", "n24"): (-100, -25), 


    ("n22", "n23"): (-58, -7),

    ("n23", "n22"): (-43, 2),
    ("n23", "n21"): (106, -3),


    ("n24", "n12"): (-51,-2),
    ("n24", "n20"): (-156,-27),

}
BLOCKED_EDGES = {
    # ("n7", "n6"),
    ("n6", "n7"),
    ("n7", "n6"),

    ("n10", "n11"),
    ("n11", "n10"),
    ("n12", "n11"),
    ("n11", "n12"),

    ("n21", "n20"),
    ("n20", "n21"),
    
    ("n24", "n20"),
    ("n20", "n24"),
    ("n20", "n19"),
    ("n19", "n20"),

    ("n24", "n23"),
    ("n23", "n24"),

    ("n22", "n21"),
    ("n21", "n22"),

    ("n15", "n16"),
    ("n16", "n15"),
    ("n17", "n18"),
    ("n18", "n17"),

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

        # ---- back neighbor (i-1) ----
        if i > 1:
            back_id = f"n{i-1}"
            # skip if blocked
            if (node_id, back_id) not in BLOCKED_EDGES:
                yaw_back = YAW_BACK
                pitch_back = PITCH_DEFAULT
                pair_back = (node_id, back_id)
                if pair_back in NEIGHBOR_YAWS:
                    yaw_back, pitch_back = NEIGHBOR_YAWS[pair_back]
                neighbors.append({"id": back_id, "yaw": yaw_back, "pitch": pitch_back})

        # ---- forward neighbor (i+1) ----
        if i < len(files):
            fwd_id = f"n{i+1}"
            # skip if blocked
            if (node_id, fwd_id) not in BLOCKED_EDGES:
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