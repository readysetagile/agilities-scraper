# Agilities Scraper

This repository extracts occupation mappings for the **10 Agilities**
from the Tableau-based Occupation Decoder and converts them into
structured JSON aligned with official O\*NET occupation data.

The resulting dataset maps each agility to a list of occupations that
correspond directly to the O\*NET occupation taxonomy.

O\*NET Occupation Reference (v25.1):\
https://www.onetcenter.org/dictionary/25.1/text/occupation_data.html

------------------------------------------------------------------------

## 🎯 Purpose

Agilities.org defines 10 core "Agilities" and maps them to job titles.\
These mappings are not available directly through O\*NET datasets.

This repository:

-   Extracts agility → occupation mappings from Tableau
-   Normalizes them
-   Outputs structured JSON
-   Ensures occupations align with official O\*NET occupation names

------------------------------------------------------------------------

## 📁 Project Structure

    agilities-scraper/
    │
    ├── json/                  # Raw Tableau response payloads (one per agility)
    ├── results.json               # Final compiled dataset
    ├── parse_tableau_agility.py
    └── README.md

------------------------------------------------------------------------

## 🛠 Manual Data Extraction Instructions

Because Tableau does not expose a public API for these mappings, manual
capture is currently required.

### Step 1 --- Navigate to the Occupation Decoder

Go to:

https://public.tableau.com/app/profile/debruce.foundation/viz/OccupationDecoder/OccupationDecoder

------------------------------------------------------------------------

### Step 2 --- Open Developer Tools

In Chrome:

-   Right click → Inspect
-   Go to the **Network** tab
-   Filter by **Fetch/XHR**

------------------------------------------------------------------------

### Step 3 --- Select Agilities

1.  Select the **"Consider #1 Agilities"** dropdown.
2.  For each agility in the list:
    -   Select **only one agility**
    -   In DevTools, locate the request named:

```
    categorical-filter-by-index
```
3.  Click the request.
4.  Copy the full **response payload**.
5.  Paste the response into the corresponding file inside:

```
    /json/<agility_name>.txt
```
Example:
```
    json/developing_others.txt
    json/driving_execution.txt
```
Repeat for all 10 agilities.

------------------------------------------------------------------------

## ▶ Running the Parser

Once all raw response files are saved in `/json`, run:

``` bash
python3 parse_tableau_agility.py json/ -o results.json
```

The script will:

-   Parse each agility file
-   Extract occupation names
-   Match them to O\*NET occupation naming
-   Generate:

```
    results.json
```
------------------------------------------------------------------------

## 📦 Output Format

The final dataset will look like:

```
[
  {
    "agility": "Developing Others",
    "occupations": [
      "Chief Executives",
      "Education Administrators",
      "Human Resources Managers"
    ]
  }
]
```

All occupations match the official O\*NET occupation titles listed here:

https://www.onetcenter.org/dictionary/25.1/text/occupation_data.html

------------------------------------------------------------------------

## 🧠 Long-Term Strategy

This repository intentionally separates:

-   Raw Tableau payloads (source of truth)
-   Parsing logic
-   Final compiled dataset

Future improvements may include:

-   Automating session capture via Playwright
-   Automating categorical-filter payload retrieval
-   CI validation against O\*NET occupation updates

------------------------------------------------------------------------

## ⚖ Notes

-   The 10 Agilities are proprietary mappings.
-   O\*NET occupation titles are public domain.
-   This repository stores derived structural mappings only.

------------------------------------------------------------------------

## 🚀 Maintainer

Ready Set Agile\
https://github.com/readysetagile
