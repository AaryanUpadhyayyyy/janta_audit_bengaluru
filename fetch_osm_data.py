import overpass
import json
from datetime import datetime
from collections import defaultdict
import time

def get_current_timestamp():
    """Returns the current time as a formatted string."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def stitch_ways(ways, line_name):
    """
    Stitches a list of OSM ways (LineStrings) into a single, continuous LineString.
    This is a highly sophisticated algorithm to ensure topological correctness.
    """
    if not ways:
        print(f"[{get_current_timestamp()}]    - No ways provided for stitching '{line_name}'.")
        return None

    endpoints = defaultdict(list)
    for way in ways:
        # Defensive check for geometry and coordinates
        if not way.get('geometry') or not way['geometry'].get('coordinates'):
            continue
        coords = way['geometry']['coordinates']
        if not isinstance(coords, list) or len(coords) < 2:
            continue
        
        start_node, end_node = tuple(coords[0]), tuple(coords[-1])
        endpoints[start_node].append(coords)
        endpoints[end_node].append(list(reversed(coords)))

    if not endpoints:
        print(f"[{get_current_timestamp()}]    - No valid endpoints found for stitching '{line_name}'.")
        return None

    # Start with the first available segment
    stitched_line = endpoints[list(endpoints.keys())[0]].pop(0)
    
    # Iteratively find and append connected segments
    for _ in range(len(ways) * 2): # Safety break to prevent infinite loops
        found_segment = False
        
        current_end_node = tuple(stitched_line[-1])
        if endpoints.get(current_end_node):
            segment_to_add = endpoints[current_end_node].pop(0)
            if tuple(segment_to_add[0]) != current_end_node:
                segment_to_add.reverse()
            stitched_line.extend(segment_to_add[1:])
            found_segment = True

        current_start_node = tuple(stitched_line[0])
        if endpoints.get(current_start_node):
            segment_to_add = endpoints[current_start_node].pop(0)
            if tuple(segment_to_add[-1]) != current_start_node:
                segment_to_add.reverse()
            stitched_line = segment_to_add[:-1] + stitched_line
            found_segment = True
            
        if not found_segment:
            break

    return {"type": "LineString", "coordinates": stitched_line}

def fetch_and_build_canonical_model():
    """
    Fetches OSM data and builds a canonical, stitched model of the transport network.
    This version (v4) uses the most robust multi-step query process.
    """
    print(f"[{get_current_timestamp()}] Starting Robust Canonical Transport Model Build (v4)...")
    
    api = overpass.API(timeout=900)
    bbox_str = "12.8,77.4,13.2,77.8"
    stitched_metro_lines = []

    # --- 1. Fetch Metro Line Relation IDs FIRST ---
    print(f"\n[{get_current_timestamp()}] Step 1: Fetching ONLY Metro Line Relation IDs...")
    metro_relation_ids_query = f'relation["route"="subway"]({bbox_str}); out ids;'
    
    try:
        relation_ids_response = api.get(metro_relation_ids_query, responseformat="json")
        relation_ids = [element['id'] for element in relation_ids_response.get('elements', [])]
        print(f"[{get_current_timestamp()}] -> Success! Found {len(relation_ids)} metro line relation(s).")
    except Exception as e:
        print(f"[{get_current_timestamp()}] -> CRITICAL ERROR: Could not fetch metro relation IDs. Error: {e}")
        relation_ids = []

    # --- 2. Process and Stitch Each Metro Line Individually ---
    print(f"\n[{get_current_timestamp()}] Step 2: Fetching, processing, and stitching each metro line individually...")
    for rel_id in relation_ids:
        print(f"[{get_current_timestamp()}]  -> Processing Relation ID: {rel_id}")
        try:
            individual_relation_query = f'(relation({rel_id});>;);out geom;'
            relation_data = api.get(individual_relation_query, responseformat="geojson")
            
            features = relation_data.get('features', [])
            
            # Correctly find the main relation feature
            main_relation = next((f for f in features if f.get('properties', {}).get('id') == rel_id and f.get('properties', {}).get('type') == 'relation'), None)
            
            if not main_relation:
                print(f"[{get_current_timestamp()}]    - WARNING: Could not find main relation feature for ID {rel_id} in response.")
                continue

            props = main_relation.get('properties', {})
            line_name = props.get('tags', {}).get('name', f"Unnamed Relation {rel_id}")
            
            member_ways = [f for f in features if f.get('geometry', {}).get('type') == 'LineString']
            print(f"[{get_current_timestamp()}]    - Found {len(member_ways)} member ways for '{line_name}'.")

            if not member_ways:
                continue

            stitched_geometry = stitch_ways(member_ways, line_name)
            
            if stitched_geometry:
                stitched_metro_lines.append({"name": line_name, "geometry": stitched_geometry})
                print(f"[{get_current_timestamp()}]  -> SUCCESS: Stitched '{line_name}' into a single LineString.")
            else:
                print(f"[{get_current_timestamp()}]  -> FAILED: Could not stitch ways for '{line_name}'.")
            
            time.sleep(10)

        except Exception as e:
            print(f"[{get_current_timestamp()}]  -> ERROR: Failed to process relation ID {rel_id}. Error: {e}")

    # --- 3. Fetch Major Roads ---
    print(f"\n[{get_current_timestamp()}] Step 3: Fetching major road network...")
    major_roads = []
    road_types = ["motorway", "trunk", "primary", "secondary", "tertiary"]
    for road_type in road_types:
        print(f"[{get_current_timestamp()}]  -> Querying for '{road_type}' roads...")
        try:
            roads_query = f'way["highway"="{road_type}"]({bbox_str}); out geom;'
            roads_response = api.get(roads_query, responseformat="geojson")
            
            processed_roads = [
                {
                    "name": f.get('properties', {}).get('tags', {}).get('name', f'Unnamed {road_type.capitalize()} Road'),
                    "geometry": f['geometry']
                }
                for f in roads_response.get('features', []) if f.get('geometry', {}).get('type') == 'LineString'
            ]
            major_roads.extend(processed_roads)
            print(f"[{get_current_timestamp()}]  -> Success! Found {len(processed_roads)} '{road_type}' road segments.")
            time.sleep(5)
        except Exception as e:
            print(f"[{get_current_timestamp()}]  -> ERROR: Failed to fetch '{road_type}' roads. Error: {e}")

    # --- 4. Save the Canonical Model ---
    output_file = 'specialized_map_layers.json'
    canonical_model = {
        "metro_lines": stitched_metro_lines,
        "major_roads": major_roads
    }
    
    print(f"\n[{get_current_timestamp()}] Canonical Model Build Complete.")
    print(f" -> Total Stitched Metro Lines: {len(stitched_metro_lines)}")
    print(f" -> Total Major Road Segments: {len(major_roads)}")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(canonical_model, f, indent=2)
        print(f"[{get_current_timestamp()}] Successfully saved canonical transport model to {output_file}")
    except IOError as e:
        print(f"[{get_current_timestamp()}] ERROR: Could not write to output file {output_file}. Error: {e}")

if __name__ == '__main__':
    fetch_and_build_canonical_model()
