from pathlib import Path
import sys

def verify_structure():
    """Verify the project directory structure"""
    base_dir = Path(__file__).parent
    
    required_dirs = [
        base_dir / 'data',
        base_dir / 'data' / 'images',
        base_dir / 'data' / 'drone',
        base_dir / 'models',
        base_dir / '.cache'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not dir_path.exists():
            missing_dirs.append(dir_path)
            
    if missing_dirs:
        print("Error: Missing directories:")
        for dir_path in missing_dirs:
            print(f"  - {dir_path}")
        return False
        
    print("Success: All required directories exist!")
    return True

if __name__ == "__main__":
    sys.exit(0 if verify_structure() else 1)