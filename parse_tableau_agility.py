import json
import os
import argparse

def extract_workbook_hierarchy(input_directory, output_file):
    """
    Reads Tableau JSON files and structures data into: Agility -> List of Titles.
    Preserves duplicates if a title appears under different Agilities.
    """
    hierarchy = {}

    if not os.path.exists(input_directory):
        print(f"Error: Directory '{input_directory}' does not exist.")
        return

    # 1. Process all .json and .txt files in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".json") or filename.endswith(".txt"):
            file_path = os.path.join(input_directory, filename)
            print(f"processing: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    
                    # Navigate the Tableau workbook structure
                    zones = data.get("vqlCmdResponse", {}).get("layoutStatus", {}).get("applicationPresModel", {}).get("workbookPresModel", {}).get("dashboardPresModel", {}).get("zones", {})
                    
                    file_agility = "Unknown Agility"
                    file_occupations = []

                    # Scan all zones in the file to find filters and the occupation list
                    for zone_id, zone_data in zones.items():
                        pres_model = zone_data.get("presModelHolder", {}).get("visual", {})
                        filters_json_str = pres_model.get("filtersJson", "[]")
                        filters = json.loads(filters_json_str)
                        
                        for f_item in filters:
                            # Capture the Agility (Top Level)
                            if f_item.get("caption") == "Agilities":
                                summary = f_item.get("summary")
                                if summary and summary != "Unknown Agility":
                                    file_agility = summary
                            
                            # Capture the Job Titles
                            if f_item.get("caption") == "Occupation . Full":
                                tuples = f_item.get("table", {}).get("tuples", [])
                                for t in tuples:
                                    title = t.get("t", [{}])[0].get("v")
                                    if title and title not in file_occupations:
                                        file_occupations.append(title)

                    # 2. Add to hierarchy (Agility -> [Titles])
                    if file_agility not in hierarchy:
                        hierarchy[file_agility] = []
                    
                    for job in file_occupations:
                        if job not in hierarchy[file_agility]:
                            hierarchy[file_agility].append(job)

                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    print(f"Skipping {filename} due to error: {e}")

    # 3. Save the simplified hierarchy
    with open(output_file, 'w', encoding='utf-8') as out_f:
        json.dump(hierarchy, out_f, indent=4)
    
    print(f"Successfully created 2-level hierarchy in {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Extract a 2-level hierarchy (Agility -> Title) from Tableau JSON.")
    parser.add_argument("input_dir", help="Directory containing Tableau .json or .txt response files")
    parser.add_argument("-o", "--output", default="agility_titles.json", help="Output JSON file name")

    args = parser.parse_args()
    extract_workbook_hierarchy(args.input_dir, args.output)

if __name__ == "__main__":
    main()
