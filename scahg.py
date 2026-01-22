import json
import os
from pathlib import Path

def merge_json_files(file_paths):
    """
    Merge multiple JSON files into one, prioritizing files starting with 'utpal'.
    Users from the same domain are combined.
    """
    merged = {"domains": {}}
    
    # Sort files: utpal files first, then others
    sorted_files = sorted(file_paths, key=lambda f: not Path(f).name.lower().startswith('utpal'))
    
    for file_path in sorted_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Fix missing commas between closing } and opening "
            import re
            content = re.sub(r'\}\s*\n\s*"', '},\n  "', content)
            
            data = json.loads(content)
                
            print(f"Processing: {Path(file_path).name}")
            
            # Merge domains
            for domain, domain_data in data.items():
                if domain not in merged["domains"]:
                    merged["domains"][domain] = {"users": []}
                
                if "users" in domain_data:
                    merged["domains"][domain]["users"].extend(domain_data["users"])
                    
        except json.JSONDecodeError as e:
            print(f"Error parsing {file_path}: {e}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    
    return merged

def display_stats(merged_data):
    """Display statistics about the merged data."""
    domain_count = len(merged_data["domains"])
    user_count = sum(len(domain["users"]) for domain in merged_data["domains"].values())
    
    print("\n" + "="*50)
    print("MERGE STATISTICS")
    print("="*50)
    print(f"Total Domains: {domain_count}")
    print(f"Total Users: {user_count}")
    print("="*50 + "\n")
    
    print("Domains and User Counts:")
    for domain, data in merged_data["domains"].items():
        print(f"  {domain}: {len(data['users'])} users")

def save_merged_json(merged_data, output_file="merged_domains.json"):
    """Save the merged data to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Merged data saved to: {output_file}")

def main():
    """Main function to run the JSON merger."""
    print("JSON Domain Merger")
    print("=" * 50)
    
    # Option 1: Specify files manually
    # file_paths = ["Ajmat.json", "Shivam.json", "Utpal.json"]
    
    # Option 2: Auto-detect all JSON files in current directory
    file_paths = [str(f) for f in Path('.').glob('*.json') if f.is_file()]
    
    if not file_paths:
        print("No JSON files found in the current directory.")
        print("Please place your JSON files in the same directory as this script.")
        return
    
    print(f"\nFound {len(file_paths)} JSON file(s):")
    for fp in file_paths:
        print(f"  - {Path(fp).name}")
    
    print("\nMerging files...")
    merged_data = merge_json_files(file_paths)
    
    # Display statistics
    display_stats(merged_data)
    
    # Save to output file
    save_merged_json(merged_data)
    
    print("\n✓ Process completed successfully!")

if __name__ == "__main__":
    main()