import subprocess
import sys
import os

def main():
    """
    Initializes the project data by running the scraper and path generator.
    This script ensures that the necessary project JSON files exist before starting the server.
    """
    print("🚀 Initializing project data...")

    # Define paths to the scripts
    scraper_script = 'bengaluru_scraper.py'
    path_generator_script = 'path_generator_trainer.py'
    
    # --- Step 1: Run the scraper to generate initial raw project data ---
    print(f"\n[1/2] Running scraper: {scraper_script}")
    try:
        scraper_result = subprocess.run(
            ['py', scraper_script],
            capture_output=True, text=True, check=True, encoding='utf-8'
        )
        print("✅ Scraper finished successfully.")
        print(scraper_result.stdout)
    except FileNotFoundError:
        print(f"❌ FATAL: Scraper script '{scraper_script}' not found.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ FATAL: Scraper script failed with exit code {e.returncode}.")
        print("--- stdout ---")
        print(e.stdout)
        print("--- stderr ---")
        print(e.stderr)
        sys.exit(1)

    # --- Step 2: Run the path generator to create the final, geometry-rich data file ---
    print(f"\n[2/2] Running path generator: {path_generator_script}")
    try:
        path_gen_result = subprocess.run(
            ['py', path_generator_script],
            capture_output=True, text=True, check=True, encoding='utf-8'
        )
        print("✅ Path generator finished successfully.")
        print(path_gen_result.stdout)
    except FileNotFoundError:
        print(f"❌ FATAL: Path generator script '{path_generator_script}' not found.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ FATAL: Path generator script failed with exit code {e.returncode}.")
        print("--- stdout ---")
        print(e.stdout)
        print("--- stderr ---")
        print(e.stderr)
        sys.exit(1)

    print("\n🎉 Project data initialization complete!")
    print("The file 'bengaluru_projects_with_paths.json' should now be ready.")

if __name__ == "__main__":
    main()
