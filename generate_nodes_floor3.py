import os

#CONFIG (FLOOR 3) 

IMAGE_DIR = "SLFloors/SLFloor3"
OUTPUT_JS = "nodes_floor3.js"

YAW_FORWARD = 20
YAW_BACK    = -120
YAW_LEFT    = -90
YAW_RIGHT   = 90
PITCH_DEFAULT = 0

MAP_TOP_START  = 40
MAP_LEFT_START = 30
MAP_STEP       = 1



DIR_TO_YAW = {
    "forward": YAW_FORWARD,
    "back":    YAW_BACK,
    "left":    YAW_LEFT,
    "right":   YAW_RIGHT,
}

DEFAULT_ORIENTATIONS = {}
EDGE_VIEW_ORIENTATIONS = {
    ("SL3_003", "SL3_004"): (180, 0),
    ("SL3_020", "SL3_005"): (177.9, -4.2),
    ("SL3_005", "SL3_021"): (177.9, -4.2),
    ("SL3_006", "SL3_007"): (-180,0),
    ("SL3_007", "SL3_006"): (90,0),
    ("SL3_007", "SL3_008"): (180,0),
    ("SL3_008", "SL3_009"): (180,0),
    ("SL3_009", "SL3_010"): (180,0),
    ("SL3_010", "SL3_011"): (180,0),
    ("SL3_010", "SL3_009"): (90,0),
    ("SL3_011", "SL3_010"): (0,0),
    ("SL3_011", "SL3_012"): (180,0),
    ("SL3_012", "SL3_013"): (180,0),
    ("SL3_013", "SL3_012"): (90, -3.9),
    ("SL3_013", "SL3_014"): (180,0),
    ("SL3_014", "SL3_005"): (90,0),
    ("SL3_012", "SL3_015"): (180,0),
    ("SL3_015", "SL3_016"): (180,0),
    ("SL3_016", "SL3_017"): (180,0),
    ("SL3_018", "SL3_017"): (-90,0),
    ("SL3_017", "SL3_019"): (-180,0),
    ("SL3_019", "SL3_004"): (90,0),
    ("SL3_004", "SL3_020"): (180,0),
    ("SL3_021", "SL3_006"): (180,0),
    ("SL3_106", "SL3_011"): (-90,0),
    ("SL3_003","SL3_107"): (-180,0),
    ("SL3_107", "SL3_003"): (180,0),
    ("SL3_107", "SL3_108"): (180,0),
    ("SL3_006", "SL3_109"): (180,0),
    ("SL3_109", "SL3_110"): (-150,0),
    ("SL3_110", "SL2_047"): (180,0),
    ("SL3_111", "SL3_106"): (90,0),
    ("SL3_106", "SL3_111"): (180,0),




}
NEIGHBOR_YAWS = {
    ("SL3_003", "SL3_004"): (-177.2, -6.5),
    ("SL3_004", "SL3_003"): (-2.9, -5.6),
    ("SL3_004", "SL3_005"): (177.9, -4.2),
    ("SL3_005", "SL3_004"): (-2.4, -0.0),
    ("SL3_005", "SL3_006"): (177.4, -3.5),
    ("SL3_006", "SL3_005"): (1.6, 0.2),
    ("SL3_006", "SL3_007"): (-89.3, -1.5),
    ("SL3_007", "SL3_006"): (-0.2, -3.8),
    ("SL3_007", "SL3_008"): (179.5, -6.0),
    ("SL3_008", "SL3_007"): (-2.7, -0.5),
    ("SL3_008", "SL3_009"): (179.0, -5.0),
    ("SL3_009", "SL3_008"): (6.9, -6.2),
    ("SL3_009", "SL3_010"): (-90.6, -4.7),
    ("SL3_010", "SL3_009"): (-2.4, -1.7),
    ("SL3_010", "SL3_011"): (176.1, -8.2),
    ("SL3_011", "SL3_010"): (-3.2, 0.1),
    ("SL3_012", "SL3_011"): (9.2, -5.4),
    ("SL3_011", "SL3_012"): (175.6, -4.4),
    ("SL3_012", "SL3_013"): (-83.5, -5.0),
    ("SL3_013", "SL3_012"): (1.4, -3.9),
    ("SL3_013", "SL3_014"): (-177.1, -3.6),
    ("SL3_014", "SL3_013"): (3.0, 1.0),
    ("SL3_014", "SL3_005"): (-175.7, -10.4),
    ("SL3_005", "SL3_014"): (-92.7, -7.3),
    ("SL3_012", "SL3_015"): (-172.6, -6.0),
    ("SL3_015", "SL3_012"): (7.6, -1.9),
    ("SL3_015", "SL3_016"): (-171.2, -5.4),
    ("SL3_016", "SL3_015"): (4.5, -0.4),
    ("SL3_016", "SL3_017"): (-86.1, -10.4),
    ("SL3_017", "SL3_018"): (45.5, -17.1),
    ("SL3_018", "SL3_017"): (-40.8, -8.9),
    ("SL3_017", "SL3_016"): (0.2, -4.8),
    ("SL3_017", "SL3_019"): (-178.3, -5.1),
    ("SL3_019", "SL3_017"): (-3.2, -3.5),
    ("SL3_019", "SL3_004"): (177.1, -8.2),
    ("SL3_004", "SL3_019"): (-92.3, -5.0),
    ("SL3_004", "SL3_020"): (177.5, -6.7),
    ("SL3_020", "SL3_004"): (-4.1, -2.0),
    ("SL3_020", "SL3_005"): (175.6, -4.2),
    ("SL3_005", "SL3_020"): (-3.5, -0.0),
    ("SL3_005", "SL3_021"): (177.3, -6.7),
    ("SL3_021", "SL3_006"): (175.8, -4.7),
    ("SL3_021", "SL3_005"): (-5.2, -4.5),
    ("SL3_006", "SL3_021"): (1.7, -2.8),
    ("SL3_011", "SL3_106"): (88.4, -1.4),
    ("SL3_106", "SL3_011"): (74.6, -0.5),
    ("SL3_107", "SL3_108"): (166.6, -25.0),
    ("SL3_107", "SL3_003"): (-6.1, 0.4),
    ("SL3_108", "SL3_107"): (1.1, 18.8),
    ("SL3_006", "SL3_109"): (-177.6, -4.8),
    ("SL3_109", "SL3_006"): (2.0, -0.1),
    ("SL3_109", "SL3_110"): (-178.9, -23.2),
    ("SL3_110", "SL3_109"): (10.3, 18.2),
    ("SL3_108", "SL2_049"): (-7.5, -21.6),
    ("SL3_110", "SL2_047"): (23.8, -21.6),
    ("SL3_106", "SL3_111"): (-115.5, -2.1),
    ("SL3_111", "SL3_106"): (97.2, -1.3),
    ("SL3_111", "SL2_052"): (-175.8, -24.2),

}

EXTRA_LINKS = [
    # e.g. ("SL3_010", "SL2_030", "forward"),
    ("SL3_005", "SL3_014", "forward"),
    ("SL3_014", "SL3_005", "forward"),
    ("SL3_012", "SL3_015", "forward"),
    ("SL3_015", "SL3_012", "forward"),
    ("SL3_017","SL3_019", "forward"),
    ("SL3_019","SL3_017", "forward"),
    ("SL3_004","SL3_019", "forward"),
    ("SL3_019","SL3_004", "forward"),
    ("SL3_004","SL3_020", "forward"),
    ("SL3_020","SL3_004", "forward"),
    ("SL3_005","SL3_020", "forward"),
    ("SL3_020","SL3_005", "forward"),
    ("SL3_005","SL3_021", "forward"),
    ("SL3_021","SL3_005", "forward"),
    ("SL3_006","SL3_021", "forward"),
    ("SL3_021","SL3_006", "forward"),
    ("SL3_011","SL3_106", "forward"),
    ("SL3_106","SL3_011", "forward"),
    ("SL3_003","SL3_107", "forward"),
    ("SL3_107","SL3_003", "forward"),
    ("SL3_006","SL3_109", "forward"),
    ("SL3_109","SL3_006", "forward"),
    ("SL3_108","SL2_049", "forward"),
    ("SL3_110","SL2_047", "forward"),
    ("SL3_106","SL3_111", "forward"),
    ("SL3_111","SL3_106", "forward"),
    ("SL3_111", "SL2_052", "forward"),
]

BLOCKED_EDGES = {
    ("SL3_014","SL3_015"),
    ("SL3_015","SL3_014"),
    ("SL3_018","SL3_019"),
    ("SL3_019","SL3_018"),
    ("SL3_019","SL3_020"),
    ("SL3_020","SL3_019"),
    ("SL3_004","SL3_005"),
    ("SL3_005","SL3_004"),
    ("SL3_020","SL3_021"),
    ("SL3_021","SL3_020"),
    ("SL3_005","SL3_006"),
    ("SL3_006","SL3_005"),
    ("SL3_021","SL3_022"),
    ("SL3_022","SL3_021"),
    ("SL3_021","SL3_106"),
    ("SL3_106","SL3_021"),
    ("SL3_106","SL3_107"),
    ("SL3_107","SL3_106"),
    ("SL3_108","SL3_109"),
    ("SL3_109","SL3_108"),
    ("SL3_110","SL3_111"),
    ("SL3_111","SL3_110"),
}
MAP_POSITIONS = {
    "SL3_003": (19.9, 15.7),
    "SL3_004": (19.6, 23.9),
    "SL3_020": (20.4, 35.2),
    "SL3_005": (20.1, 49.8),
    "SL3_021": (20.1, 62.4),
    "SL3_006": (20.1, 75.4),
    "SL3_007": (31.6, 75.9),
    "SL3_008": (48.1, 75.6),
    "SL3_009": (62.8, 75.4),
    "SL3_010": (63.7, 62.8),
    "SL3_011": (63.7, 55.9),
    "SL3_106": (79.6, 58.5),
    "SL3_012": (63.4, 49.3),
    "SL3_015": (63.1, 37.2),
    "SL3_016": (62.5, 23.5),
    "SL3_017": (57.5, 23.0),
    "SL3_018": (56.3, 18.3),
    "SL3_019": (36.0, 23.5),
    "SL3_005": (20.4, 49.6),    
    "SL3_013": (50.4, 49.4),
    "SL3_014": (33.7, 49.4),
    "SL3_107": (19.9, 11.5),
    "SL3_108": (18.7, 3.3),
    "SL3_109": (21.3, 88.5),
    "SL3_110": (20.2, 95.1),
    "SL3_111": (89.0, 61.2),
    
}
HIDDEN_NODES = {}


def main():
    files = sorted([
        f for f in os.listdir(IMAGE_DIR)
        if os.path.splitext(f)[1].lower() in {".jpg", ".jpeg", ".png"}
    ])

    if not files:
        raise SystemExit(f"No images found in: {IMAGE_DIR}")

    print(f"[Floor3] Found {len(files)} images.")
    nodes = {}

    for idx, filename in enumerate(files):
        base = os.path.splitext(filename)[0]
        node_id = base

        neighbors = []

        if idx > 0:
            prev_base = os.path.splitext(files[idx - 1])[0]
            back_id = prev_base
            if (node_id, back_id) not in BLOCKED_EDGES:
                yaw_back   = YAW_BACK
                pitch_back = PITCH_DEFAULT
                pair_back  = (node_id, back_id)
                if pair_back in NEIGHBOR_YAWS:
                    yaw_back, pitch_back = NEIGHBOR_YAWS[pair_back]
                neighbors.append({
                    "id": back_id,
                    "yaw": yaw_back,
                    "pitch": pitch_back,
                })

        if idx < len(files) - 1:
            next_base = os.path.splitext(files[idx + 1])[0]
            fwd_id = next_base
            if (node_id, fwd_id) not in BLOCKED_EDGES:
                yaw_fwd   = YAW_FORWARD
                pitch_fwd = PITCH_DEFAULT
                pair_fwd  = (node_id, fwd_id)
                if pair_fwd in NEIGHBOR_YAWS:
                    yaw_fwd, pitch_fwd = NEIGHBOR_YAWS[pair_fwd]
                neighbors.append({
                    "id": fwd_id,
                    "yaw": yaw_fwd,
                    "pitch": pitch_fwd,
                })

        auto_top  = min(100, MAP_TOP_START  + idx * MAP_STEP)
        auto_left = min(100, MAP_LEFT_START + idx * MAP_STEP)

        if node_id in MAP_POSITIONS:
            map_top, map_left = MAP_POSITIONS[node_id]
        else:
            map_top, map_left = auto_top, auto_left

        default_yaw, default_pitch = DEFAULT_ORIENTATIONS.get(node_id, (0, 0))

        nodes[node_id] = {
            "image": filename,
            "label": node_id,
            "description": "",
            "defaultYaw": default_yaw,
            "defaultPitch": default_pitch,
            "neighbors": neighbors,
            "mapTop": map_top,
            "mapLeft": map_left,
            "hideOnMap": (node_id in HIDDEN_NODES),
        }

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

        if from_id not in nodes:
            print(f"WARNING: EXTRA_LINK from_id {from_id} not in nodes (skipping)")
            continue

        if to_id not in nodes:
            print(f"NOTE: EXTRA_LINK to_id {to_id} not in this floor's nodes (probably cross-floor)")

        if direction not in DIR_TO_YAW:
            print(f"WARNING: invalid direction '{direction}' in EXTRA_LINK: {entry}")
            continue

        base_yaw = DIR_TO_YAW[direction]

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
        print(f"Added extra link (F3): {from_id} -> {to_id} ({direction}, yaw={base_yaw})")

    for (from_id, to_id), (view_yaw, view_pitch) in EDGE_VIEW_ORIENTATIONS.items():
        if from_id not in nodes:
            print(f"WARNING: EDGE_VIEW from_id {from_id} not in nodes")
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
            print(f"WARNING: EDGE_VIEW pair {from_id}->{to_id} not found among neighbors")

    print("\nWriting nodes_floor3.js...")

    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write("// Auto-generated by generate_nodes_floor3.py\n")
        f.write("window.NODES_F3 = {\n\n")

        first = True
        for node_id in nodes:
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

            block = f"""  "{node_id}": {{
    image: "{node["image"]}",
    label: "{node["label"]}",
    description: "",
    defaultYaw: {node["defaultYaw"]},
    defaultPitch: {node["defaultPitch"]},
    neighbors: [
{neighbors_block}
    ],
    mapTop: {node["mapTop"]},
    mapLeft: {node["mapLeft"]},
    hideOnMap: {str(node["hideOnMap"]).lower()}
  }}"""

            if not first:
                f.write(",\n\n")
            first = False
            f.write(block)

        f.write("\n\n};\n")

    print("nodes_floor3.js generated successfully.")


if __name__ == "__main__":
    main()
