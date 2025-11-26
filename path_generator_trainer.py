import json
import random
import time
from datetime import datetime
import math
from shapely.geometry import Point, LineString, mapping
from shapely.ops import nearest_points

def get_current_timestamp():
    """Returns the current time as a formatted string."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def load_specialized_layers(filepath='specialized_map_layers.json'):
    """Loads the canonical transport model from the specified file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f"[{get_current_timestamp()}] Loading canonical transport model from {filepath}...")
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"[{get_current_timestamp()}] CRITICAL ERROR: Canonical model file '{filepath}' not found or invalid. Cannot proceed.")
        return None

def find_closest_canonical_line(project_point, canonical_lines):
    """
    Finds the closest canonical line to a project's location using geospatial analysis.
    Returns the line object and the minimum distance.
    """
    min_dist = float('inf')
    closest_line_info = None
    
    for line_data in canonical_lines:
        try:
            line_geom = LineString(line_data['geometry']['coordinates'])
            dist = project_point.distance(line_geom)
            if dist < min_dist:
                min_dist = dist
                closest_line_info = (line_data, line_geom)
        except Exception as e:
            print(f"[{get_current_timestamp()}] WARNING: Could not process a line geometry. Skipping. Error: {e}")
            continue
            
    return closest_line_info, min_dist

def project_point_onto_line(point, line_geom):
    """Projects a Shapely Point onto a Shapely LineString, returning a new Point."""
    return line_geom.interpolate(line_geom.project(point))

def generate_extension_geometry(project_point, canonical_line_geom, length_km=2.5):
    """
    Generates a LineString extending from the nearest end of a canonical line,
    in the general direction of the project's original location.
    """
    start_node = Point(canonical_line_geom.coords[0])
    end_node = Point(canonical_line_geom.coords[-1])
    
    dist_to_start = project_point.distance(start_node)
    dist_to_end = project_point.distance(end_node)
    
    # Determine the extension point and the direction
    if dist_to_start < dist_to_end:
        extension_start_point = start_node
        # Direction from start of line towards the project
        direction_vector = (project_point.x - start_node.x, project_point.y - start_node.y)
    else:
        extension_start_point = end_node
        # Direction from end of line towards the project
        direction_vector = (project_point.x - end_node.x, project_point.y - end_node.y)

    # Normalize the direction vector
    norm = math.sqrt(direction_vector[0]**2 + direction_vector[1]**2)
    if norm == 0: return canonical_line_geom # Cannot extend if vector is zero

    # Calculate the end point of the extension
    # Conversion: 1 degree of latitude is approx 111 km
    extension_end_x = extension_start_point.x + (direction_vector[0] / norm) * (length_km / 111.0)
    extension_end_y = extension_start_point.y + (direction_vector[1] / norm) * (length_km / 111.0)
    
    return LineString([extension_start_point, (extension_end_x, extension_end_y)])

def generate_plausible_line_path(start_lat, start_lon, project_name):
    """Generates a plausible, multi-segment LineString for generic linear projects."""
    num_points = random.randint(8, 15)
    total_length_km = random.uniform(2.0, 7.0)
    path = [[start_lon, start_lat]]
    current_lat, current_lon = start_lat, start_lon
    angle = random.uniform(0, 2 * math.pi)
    
    for _ in range(num_points - 1):
        segment_length_km = total_length_km / (num_points - 1)
        angle += random.uniform(-math.pi / 4, math.pi / 4)
        lat_change = (segment_length_km / 111.0) * math.sin(angle)
        lon_change = (segment_length_km / (111.0 * abs(math.cos(math.radians(current_lat))))) * math.cos(angle)
        current_lat += lat_change
        current_lon += lon_change
        path.append([current_lon, current_lat])
        
    return {"type": "LineString", "coordinates": path}

def train_path_generator_model(output_file='bengaluru_projects_with_paths.json'):
    """
    Applies a high-precision, geospatial model to generate project geometries.
    """
    input_file = 'bengaluru_projects.json'
    print(f"[{get_current_timestamp()}] Starting Ultra-Precision Pathfinding AI...")
    
    canonical_model = load_specialized_layers()
    if not canonical_model: return

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            projects = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[{get_current_timestamp()}] ERROR: Could not read or parse {input_file}. Error: {e}")
        return

    # --- Counters for statistics ---
    stats = {
        "total": len(projects), "processed": 0, "skipped": 0,
        "metro_station": 0, "metro_extension": 0, "metro_other": 0,
        "road_aligned": 0, "generative_fallback": 0, "point_default": 0
    }
    start_time = time.time()

    for project in projects:
        try:
            project_name = project.get('projectName', '').lower()
            project_name_raw = project.get('projectName', '')
            lat = project.get('geoPoint', {}).get('latitude') or project.get('latitude')
            lon = project.get('geoPoint', {}).get('longitude') or project.get('longitude')

            if not lat or not lon:
                stats['skipped'] += 1
                continue

            project_point = Point(lon, lat)
            geom = None

            # --- Tier 1: Metro Project High-Precision Alignment ---
            if 'metro' in project_name:
                closest_line_info, dist = find_closest_canonical_line(project_point, canonical_model.get('metro_lines', []))
                
                if closest_line_info and dist < 0.1: # 0.1 degrees is ~11km, a generous threshold
                    line_data, line_geom = closest_line_info
                    
                    # Sanitize strings for printing to avoid UnicodeEncodeError on Windows
                    safe_project_name = project_name_raw.encode('ascii', 'ignore').decode('ascii')
                    safe_line_name = line_data['name'].encode('ascii', 'ignore').decode('ascii')
                    print(f"[{get_current_timestamp()}] Aligning '{safe_project_name}' with canonical '{safe_line_name}'.")

                    if 'station' in project_name:
                        geom = mapping(project_point_onto_line(project_point, line_geom))
                        stats['metro_station'] += 1
                    elif 'extension' in project_name:
                        geom = mapping(generate_extension_geometry(project_point, line_geom))
                        stats['metro_extension'] += 1
                    else: # Default for other metro projects (e.g., "commercial development")
                        geom = mapping(project_point_onto_line(project_point, line_geom))
                        stats['metro_other'] += 1
            
            # --- Tier 2: Road Project Alignment ---
            if not geom and any(kw in project_name for kw in ['road', 'flyover', 'expressway', 'underpass']):
                closest_line_info, dist = find_closest_canonical_line(project_point, canonical_model.get('major_roads', []))
                if closest_line_info and dist < 0.05: # Tighter threshold for roads
                    line_data, line_geom = closest_line_info
                    geom = line_data['geometry'] # Use the whole road segment for now
                    stats['road_aligned'] += 1

            # --- Tier 3: Generative Fallback for other Linear Projects ---
            if not geom and any(kw in project_name for kw in ['corridor', 'pipeline']):
                geom = generate_plausible_line_path(lat, lon, project_name_raw)
                stats['generative_fallback'] += 1

            # --- Tier 4: Default to Point Geometry ---
            if not geom:
                geom = mapping(project_point)
                stats['point_default'] += 1
            
            project['geometry'] = geom
            stats['processed'] += 1

        except Exception as e:
            safe_project_name = project.get('projectName', 'Unknown').encode('ascii', 'ignore').decode('ascii')
            print(f"[{get_current_timestamp()}] ERROR: Failed to process project {safe_project_name}. Error: {e}")
            stats['skipped'] += 1
            project['geometry'] = mapping(Point(project.get('longitude', 0), project.get('latitude', 0)))


    # --- Finalization ---
    end_time = time.time()
    print(f"\n[{get_current_timestamp()}] Pathfinding AI Run Complete in {end_time - start_time:.2f}s.")
    print("-" * 50)
    print(f"  Total Projects: {stats['total']}")
    print(f"  - Processed: {stats['processed']} | Skipped: {stats['skipped']}")
    print(f"  Geometries Generated:")
    print(f"    - Metro Stations (Snapped): {stats['metro_station']}")
    print(f"    - Metro Extensions (Generated): {stats['metro_extension']}")
    print(f"    - Other Metro (Snapped): {stats['metro_other']}")
    print(f"    - Roads (Aligned): {stats['road_aligned']}")
    print(f"    - Generative Fallback: {stats['generative_fallback']}")
    print(f"    - Default Points: {stats['point_default']}")
    print("-" * 50)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(projects, f, indent=4)
        print(f"[{get_current_timestamp()}] Successfully saved ultra-precision geometries to {output_file}")
    except IOError as e:
        print(f"[{get_current_timestamp()}] ERROR: Could not write to output file {output_file}. Error: {e}")

if __name__ == '__main__':
    train_path_generator_model()

