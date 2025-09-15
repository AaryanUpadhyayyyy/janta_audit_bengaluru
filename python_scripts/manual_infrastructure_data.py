#!/usr/bin/env python3
"""
Manual Infrastructure Data for Bengaluru Projects
Contains detailed project information from comprehensive infrastructure report
"""

from datetime import datetime
import random

def get_random_bengaluru_coords():
    """Generate random coordinates within Bengaluru bounds"""
    lat_min, lat_max = 12.8, 13.2
    lon_min, lon_max = 77.4, 77.8
    return {
        "latitude": round(random.uniform(lat_min, lat_max), 6),
        "longitude": round(random.uniform(lon_min, lon_max), 6)
    }

def get_manual_infrastructure_projects():
    """Get manually curated infrastructure projects from detailed report"""
    manual_projects = [
        # Namma Metro Projects
        {
            'id': "MANUAL_METRO_1",
            'projectName': 'Namma Metro Blue Line Phase 2A & 2B (ORR-Airport Corridor)',
            'description': '58.19 km metro line connecting Central Silk Board to Krishnarajapura (K.R. Pura) and extending to Kempegowda International Airport (KIA) with driverless trains and luggage racks',
            'budget': 1478800000000,  # ₹14,788 crore
            'status': 'In Progress',
            'location': 'Central Silk Board to K.R. Pura to Kempegowda International Airport, Bengaluru, Karnataka',
            'startDate': '2020-01-01',
            'endDate': '2027-12-31',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://www.thehindu.com/news/cities/bangalore/bengalurus-blue-line-of-namma-metro-scheduled-for-completion-by-dec-2027/article70013051.ece',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'BMRCL',
            'physicalProgress': 52.5,
            'totalLength': 58.19,
            'stations': 30,
            'contractor': 'Multiple contractors including Jakson Limited, MR Constructions, Godrej & Boyce',
            'wardNumber': 15,
            'geoPoint': get_random_bengaluru_coords()
        },
        {
            'id': "MANUAL_METRO_2",
            'projectName': 'Namma Metro Orange Line Phase 3 (Double-Decker Viaduct)',
            'description': '44+ km metro line with 31 elevated stations featuring integrated double-decker flyover beneath metro line. Corridor 1: J.P. Nagar 4th Phase to Kempapura, Corridor 2: Hosahalli to Kadabagere',
            'budget': 1561100000000,  # >₹15,611 crore
            'status': 'Approved',
            'location': 'Western Bengaluru - J.P. Nagar 4th Phase to Kempapura & Hosahalli to Kadabagere, Karnataka',
            'startDate': '2025-01-01',
            'endDate': '2031-05-31',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://www.thehindu.com/news/cities/bangalore/orange-line-may-be-delayed-by-a-year-as-double-decker-flyovers-planned/article70009112.ece',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'BMRCL',
            'physicalProgress': 0,
            'totalLength': 44,
            'stations': 31,
            'contractor': 'To be awarded',
            'wardNumber': 20,
            'geoPoint': get_random_bengaluru_coords()
        },
        {
            'id': "MANUAL_METRO_3",
            'projectName': 'Namma Metro Yellow Line (RV Road to Bommasandra)',
            'description': '18 km driverless metro line connecting RV Road to Bommasandra, delayed due to rolling-stock supply crisis',
            'budget': 800000000000,  # Estimated ₹8,000 crore
            'status': 'Delayed',
            'location': 'RV Road to Bommasandra, Bengaluru, Karnataka',
            'startDate': '2019-01-01',
            'endDate': '2025-12-31',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://en.wikipedia.org/wiki/Namma_Metro',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'BMRCL',
            'physicalProgress': 85,
            'totalLength': 18,
            'stations': 19,
            'contractor': 'CRRC Nanjing Puzhen Co Ltd (Rolling Stock)',
            'wardNumber': 25,
            'geoPoint': get_random_bengaluru_coords()
        },
        # Bengaluru Suburban Rail Project
        {
            'id': "MANUAL_RAIL_1",
            'projectName': 'Bengaluru Suburban Rail Project - Mallige Line (Line 2)',
            'description': '25.07 km suburban rail corridor from Benniganahalli to Chikkabanavara with 14 stations',
            'budget': 500000000000,  # Estimated ₹5,000 crore
            'status': 'In Progress',
            'location': 'Benniganahalli to Chikkabanavara, Bengaluru, Karnataka',
            'startDate': '2020-01-01',
            'endDate': '2026-12-31',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://www.newindianexpress.com/cities/bengaluru/2025/Aug/30/only-185-of-work-done-on-suburban-rail-project-in-bengaluru',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'K-RIDE',
            'physicalProgress': 28,
            'totalLength': 25.07,
            'stations': 14,
            'contractor': 'Multiple contractors (some terminated)',
            'wardNumber': 10,
            'geoPoint': get_random_bengaluru_coords()
        },
        {
            'id': "MANUAL_RAIL_2",
            'projectName': 'Bengaluru Suburban Rail Project - Kanaka Line (Line 4)',
            'description': '46.24 km suburban rail corridor from Heelalige to Rajanukunte with 19 stations, facing land acquisition challenges. Part of four-corridor network with terminals at KSR Bengaluru, Devanahalli, Kengeri, and Whitefield',
            'budget': 700000000000,  # ₹7,000 crore (escalated)
            'status': 'In Progress',
            'location': 'Heelalige to Rajanukunte via KSR Bengaluru, Devanahalli, Kengeri, Whitefield, Bengaluru, Karnataka',
            'startDate': '2020-01-01',
            'endDate': '2027-12-31',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://www.newindianexpress.com/cities/bengaluru/2025/Aug/30/only-185-of-work-done-on-suburban-rail-project-in-bengaluru',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'K-RIDE',
            'physicalProgress': 6,
            'totalLength': 46.24,
            'stations': 19,
            'contractor': 'Larsen & Toubro (terminated), new contractors being sought',
            'wardNumber': 18,
            'geoPoint': get_random_bengaluru_coords()
        },
        # Highway Projects
        {
            'id': "MANUAL_HIGHWAY_1",
            'projectName': 'Bengaluru-Chennai Expressway (NE-7)',
            'description': '258 km greenfield expressway reducing travel time between Bengaluru and Chennai to 2-3 hours. Karnataka section (71 km) opened in December 2024',
            'budget': 1793000000000,  # ₹17,930 crore
            'status': 'In Progress',
            'location': 'Bengaluru to Chennai via Hoskote, Malur, Bangarapet, Bethamangala, Karnataka',
            'startDate': '2019-01-01',
            'endDate': '2026-07-31',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://en.wikipedia.org/wiki/Bengaluru%E2%80%93Chennai_Expressway',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'NHAI',
            'physicalProgress': 65,
            'totalLength': 258,
            'contractor': 'Multiple contractors including Dilip Buildcon, KCC Buildcon, Montecarlo Construction',
            'wardNumber': 1,
            'geoPoint': get_random_bengaluru_coords()
        },
        {
            'id': "MANUAL_HIGHWAY_2",
            'projectName': 'Peripheral Ring Road (PRR) - Bangalore Business Corridor',
            'description': '73.04 km ring road encircling Bengaluru to divert heavy vehicle traffic and decongest city center. Affects 77 villages. Stalled due to land acquisition disputes over compensation framework',
            'budget': 2700000000000,  # ₹27,000 crore
            'status': 'Stalled',
            'location': '73.04 km corridor encircling Bengaluru affecting 77 villages, Karnataka',
            'startDate': '2005-01-01',
            'endDate': 'TBD',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://bangaloremirror.indiatimes.com/bangalore/others/compensation-row-stalls-bengaluru-prr-land-acquisition/articleshow/123350819.cms',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'BDA',
            'physicalProgress': 0,
            'totalLength': 73.04,
            'contractor': 'Not awarded due to land acquisition issues',
            'wardNumber': 30,
            'geoPoint': get_random_bengaluru_coords()
        },
        # Urban Tunnel Project
        {
            'id': "MANUAL_TUNNEL_1",
            'projectName': 'Hebbal-Silk Board Twin Tunnel Road',
            'description': '16.74 km twin-tube underground tunnel road with Build-Own-Operate-Transfer model. Facing legal challenges from NGT over environmental concerns',
            'budget': 1900000000000,  # ₹19,000 crore
            'status': 'Tendering',
            'location': 'Hebbal to Silk Board (16.74 km twin-tube tunnel), Bengaluru, Karnataka',
            'startDate': '2025-01-01',
            'endDate': '2029-12-31',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://www.thehindu.com/news/national/karnataka/tenders-invited-for-167-km-twin-tunnel-project-linking-hebbal-and-silk-board/article69815904.ece',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'B-SMILE',
            'physicalProgress': 0,
            'totalLength': 16.74,
            'contractor': 'Global tenders floated',
            'wardNumber': 5,
            'geoPoint': get_random_bengaluru_coords()
        },
        # BBMP Urban Projects
        {
            'id': "MANUAL_BBMP_1",
            'projectName': 'IT-BT Corridor (Silk Board to K.R. Puram)',
            'description': '22.7 km IT-BT corridor development for improved connectivity in tech corridors',
            'budget': 40000000000,  # ₹400 crore
            'status': 'Approved',
            'location': 'Bengaluru, Karnataka',
            'startDate': '2025-04-01',
            'endDate': '2027-03-31',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://bangaloremirror.indiatimes.com/bangalore/others/bbmp-budget-2025-26-plans-big-on-roads-white-topping-for-seamless-flow/articleshow/119727561.cms',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'BBMP',
            'physicalProgress': 0,
            'totalLength': 22.7,
            'contractor': 'To be awarded',
            'wardNumber': 12,
            'geoPoint': get_random_bengaluru_coords()
        },
        {
            'id': "MANUAL_BBMP_2",
            'projectName': 'BBMP Urban Flyovers - Signal Free Corridors',
            'description': '110 km of urban flyovers across Bengaluru to create signal-free corridors',
            'budget': 1320000000000,  # ₹13,200 crore
            'status': 'Planning',
            'location': 'Bengaluru, Karnataka',
            'startDate': '2025-06-01',
            'endDate': '2030-12-31',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://bangaloremirror.indiatimes.com/bangalore/others/bbmp-budget-2025-26-plans-big-on-roads-white-topping-for-seamless-flow/articleshow/119727561.cms',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'BBMP',
            'physicalProgress': 0,
            'totalLength': 110,
            'contractor': 'Multiple contractors to be awarded',
            'wardNumber': 8,
            'geoPoint': get_random_bengaluru_coords()
        },
        {
            'id': "MANUAL_BBMP_3",
            'projectName': 'Double-Decker Flyover Integration Project',
            'description': '40 km double-decker flyover integrating road and metro infrastructure',
            'budget': 900000000000,  # ₹9,000 crore
            'status': 'Planning',
            'location': 'Bengaluru, Karnataka',
            'startDate': '2025-01-01',
            'endDate': '2030-12-31',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://bangaloremirror.indiatimes.com/bangalore/others/bbmp-budget-2025-26-plans-big-on-roads-white-topping-for-seamless-flow/articleshow/119727561.cms',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'BBMP',
            'physicalProgress': 0,
            'totalLength': 40,
            'contractor': 'To be integrated with metro contractors',
            'wardNumber': 16,
            'geoPoint': get_random_bengaluru_coords()
        },
        {
            'id': "MANUAL_BBMP_4",
            'projectName': 'White-Topping of Major Roads',
            'description': 'White-topping of major roads across Bengaluru to improve durability and reduce potholes',
            'budget': 600000000000,  # ₹6,000 crore
            'status': 'Planning',
            'location': 'Bengaluru, Karnataka',
            'startDate': '2025-04-01',
            'endDate': '2028-03-31',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://bangaloremirror.indiatimes.com/bangalore/others/bbmp-budget-2025-26-plans-big-on-roads-white-topping-for-seamless-flow/articleshow/119727561.cms',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'BBMP',
            'physicalProgress': 0,
            'contractor': 'Multiple contractors to be awarded',
            'wardNumber': 22,
            'geoPoint': get_random_bengaluru_coords()
        },
        {
            'id': "MANUAL_BBMP_5",
            'projectName': 'Hebbal Flyover Second Loop Construction',
            'description': 'Second loop construction at Hebbal flyover for direct passage from northern suburbs to Mekhri Circle',
            'budget': 5000000000,  # ₹50 crore (estimated)
            'status': 'In Progress',
            'location': 'Hebbal, Bengaluru',
            'startDate': '2024-06-01',
            'endDate': '2026-01-01',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://www.thehindu.com/news/national/karnataka/bengalurus-mekhri-circle-to-face-heavier-congestion-as-second-hebbal-loop-construction-continues/article70042416.ece',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'BBMP',
            'physicalProgress': 75,
            'contractor': 'Local construction contractor',
            'wardNumber': 3,
            'geoPoint': get_random_bengaluru_coords()
        },
        # High-Speed Rail Future Project
        {
            'id': "MANUAL_HSR_1",
            'projectName': 'Bengaluru-Hyderabad High-Speed Rail Corridor',
            'description': '626 km elevated high-speed rail route with design speed of 350 kmph, reducing journey time from 19 hours to 2 hours',
            'budget': 5000000000000,  # Estimated ₹50,000 crore
            'status': 'Planning',
            'location': 'Bengaluru to Hyderabad',
            'startDate': '2026-01-01',
            'endDate': '2035-12-31',
            'source': 'Manual Infrastructure Report',
            'sourceUrl': 'https://timesofindia.indiatimes.com/city/bengaluru/detailed-project-report-for-bengaluru-hyderabad-high-speed-rail-by-march-2026/articleshow/123873809.cms',
            'scrapedAt': datetime.now().isoformat(),
            'department': 'SCR',
            'physicalProgress': 0,
            'totalLength': 626,
            'contractor': 'DPR scheduled for March 2026',
            'wardNumber': 1,
            'geoPoint': get_random_bengaluru_coords()
        }
    ]
    
    return manual_projects

if __name__ == "__main__":
    projects = get_manual_infrastructure_projects()
    print(f"Generated {len(projects)} manual infrastructure projects")
    for project in projects:
        print(f"- {project['projectName']} ({project['department']}) - ₹{project['budget']:,}")
