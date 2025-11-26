#!/usr/bin/env python3
import json
import sys

try:
    print("Loading bengaluru_projects.json...")
    with open('bengaluru_projects.json', 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"File size: {len(content)} characters")
        
    print("Parsing JSON...")
    with open('bengaluru_projects.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Successfully loaded {len(data)} projects")
    if len(data) > 0:
        print(f"First project: {data[0]['id']}")
        if len(data) > 76:
            print(f"Project 77: {data[76]['id']}")
        if len(data) > 77:
            print(f"Project 78: {data[77]['id']}")
        else:
            print("Only has 77 or fewer projects")
            
except json.JSONDecodeError as e:
    print(f"JSON Error: {e}")
    print(f"Error at line {e.lineno}, column {e.colno}")
except Exception as e:
    print(f"Other error: {e}")