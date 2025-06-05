# Bulgarian Elections OpenData

This repository contains election data and tools for processing Bulgarian elections data.

## Data Structure

The `/data` directory contains structured election data organized in a standardized format:

### Directory Structure

- **YYYYMMDD folders** (e.g., `20210404`, `20210711`): Contain standardized open data for elections that took place on the particular date
- **common**: Contains files with common reference data
- **processed**: Contains derived CSV data produced based on data from all supported elections


### Elections Folders

The files in each election folder are organized into the following groups based on their prefix number (N):

#### File Format and Naming Convention
All data files are in CSV format using ';' as separator and UTF-8 encoding. File naming follows the pattern: `NM_<type_of_data>.csv` where:
- N: Number denoting a particular group of data
- M: Type indicator (0 for source data, 1+ for derived data)

#### Group 10 - Security and Verification
- `10_certificate_chain.crt` - Certificate chain used for cryptographic verification of electronic voting data, specifically for validating digital signatures of vote data exported from each voting machine

#### Group 20 - Party and Registration Information
- `20_local_candidates.csv` - Information about local individual candidates
  - `code` - Unique candidate identifier
  - `name` - Candidate's full name
  - `registration_code` - Official registration code
  - `registration_sub_code` - The regional election commission code where the candidate is registered
  - `registration_name` - Official registered name

- `20_parties.csv` - List of registered parties and coalitions
  - `code` - Unique party/coalition identifier
  - `name` - Short party/coalition name
  - `registration_code` - The number assigned to the party/coalition that voters use to mark their choice on the ballot
  - `registration_name` - The name registered to the party/coalition that voters use to mark their choice on the ballot

- `21_participants.csv` - Unified list of election participants (parties, coalitions and individuals)
  - `code` - Unique participant identifier
  - `name` - Short name used for reporting
  - `registration_code` - Official registration code
  - `registration_sub_code` - Applicable for individual candidates
  - `registration_name` - Official participant name

#### Group 30 - Section Information
- `30_pre_processed_sections.csv` - Section data before processing
  - `section_id` - Unique section identifier
  - `rik_code` - Regional election commission code
  - `administration_code` - Administrative district code and name
  - `ekatte` - EKATTE (location) code
  - `city` - City/village name
  - `address` - Section address
  - `is_mobile` - Mobile section indicator (0/1)
  - `is_on_ship` - Ship section indicator (0/1)
  - `machines_count` - Number of voting machines assigned to the section

- `30_sections_with_failed_machine.csv` - List of sections with machine voting issues
  - `section_id` - Section identifier
  - `failed_machines_count` - Number of failed machines

- `31_sections.csv` - Final processed section data with geographical information
  - `section_id` - Unique section identifier
  - `rik_code` - Regional election commission code
  - `rik_name` - Regional election commission name
  - `municipality_code` - Municipality code
  - `municipality` - Municipality name
  - `ekatte` - EKATTE (location) code
  - `postal_code` - Postal code
  - `city` - City/village name
  - `address` - Section address
  - `is_mobile` - Mobile section indicator (0/1)
  - `is_on_ship` - Ship section indicator (0/1)
  - `machines_count` - Number of voting machines assigned to the section
  - `failed_machines_count` - Number of failed machines
  - `longitude` - Geographic longitude
  - `latitude` - Geographic latitude

#### Group 40 - Electoral Lists and Protocols
- `40_elections_lists.csv` - Latest list of registred voters 
  - `section_id` - Section identifier
  - `registered_voters` - Number of registered voters in the section

- `41_protocols.csv` - Official voting protocols data
  - `section_id` - Section identifier
  - `distributed_ballots` - Number of paper ballots distributed to the section
  - `pre_registered_voters` - Initially announced number of voters registered
  - `registered_voters` - Latest officially announced number of registered voters
  - `onsite_listed_voters` - Additional voters registered on-site
  - `voted_voters` - Total number of voters who voted
  - `unused_paper_ballots` - Number of unused paper ballots
  - `destroyed_paper_ballots` - Number of destroyed/invalid paper ballots
  - `urn_paper_ballots` - Number of paper ballots in the ballot box
  - `invalid_paper_ballots` - Number of invalid paper ballots in the ballot box
  - `support_noone_paper_ballots` - Number of paper ballots marked "I don't support anyone"
  - `valid_paper_votes_for_parties` - Number of valid paper votes for participants
  - `urn_machine_ballots` - Number of machine votes cast
  - `support_noone_machine_ballots` - Number of machine "I don't support anyone" votes
  - `valid_machine_votes_for_parties` - Number of valid machine votes for participants

#### Group 50 - Voting Results
- `50_votes_machine_from_machine_data.csv` - Data for machine votes extracted from raw machine voting data
  - `section_id` - Section identifier
  - `party` - Participant identifier
  - `votes` - Number of votes from machine

- `50_votes_machine.csv` - Machine voting results from paper protocols
  - `section_id` - Section identifier
  - `party` - Participant identifier
  - `votes` - Number of votes from machine voting

- `50_votes_paper.csv` - Paper ballot voting results from paper protocols
  - `section_id` - Section identifier
  - `party` - Participant identifier
  - `votes` - Number of votes from paper ballots

- `51_votes_combined.csv` - Combined voting results
  - `section_id` - Section identifier
  - `municipality_code` - Municipality code
  - `rik_code` - Regional election commission code
  - `paper_votes` - Number of paper ballot votes
  - `machine_votes` - Number of machine votes
  - `machine_data_votes` - Number of machine votes according raw machine voting data
  - `registration_code` - Participant registration code
  - `registration_sub_code` - Participant registration sub-code
  - `participant_code` - Unified participant code
  - `participant_name` - Participant name

### Common Reference Files

Files in the `common` folder provide reference data used across all elections:

- `ekkate.csv` - EKATTE (Unified classifier of administrative-territorial and territorial units)
  - `ekatte` - Unique EKATTE code
  - `postal_code` - Postal code
  - `type` - Type of settlement (city, village, etc.)
  - `name` - Settlement name in Bulgarian
  - `name_latin` - Settlement name in Latin script
  - `municipality` - Municipality name in Bulgarian
  - `municipality_latin` - Municipality name in Latin script
  - `district` - District name in Bulgarian
  - `district_latin` - District name in Latin script

- `elections.csv` - List of elections included in the dataset
  - `id` - Election date in YYYYMMDD format
  - `label` - Short identifier for the election

- `municipalities.csv` - Reference data for municipalities in Bulgaria
  - `municipality_code` - Unique municipality code
  - `municipality` - Municipality name in Bulgarian
  - `municipality_latin` - Municipality name in Latin script
  - `rik_code` - Regional election commission code
  - `rik_name` - Regional election commission name

- `participants.csv` - Reference mapping of parties and coalitions across different elections
  - `code` - Unified participant identifier
  - `name` - Standardized name used for the participant
  - `mapping` - Name mapping used to match participant names across different elections

- `riks.csv` - Regional election commission (РИК) reference data
  - `rik_code` - Regional election commission code
  - `rik_name` - Regional election commission name in Bulgarian
  - `district` - District name in Bulgarian
  - `district_latin` - District name in Latin script

### Processed Data Files

Files in the `processed` folder contain aggregated and analyzed data across all elections:

- `parties_total_votes.csv` - Aggregated voting results for each party across all elections
  - `party_name` - Name of the party
  - For each election (E{YYYYMMDD}):
    - `E{YYYYMMDD}_machine_votes` - Number of machine votes
    - `E{YYYYMMDD}_paper_votes` - Number of paper votes
    - `E{YYYYMMDD}_total_votes` - Total number of votes

- `sections_total_votes.csv` - Statistical analysis of voter turnout by section
  - `section_id` - Unique section identifier
  - For each election (E{YYYYMMDD}):
    - `E{YYYYMMDD}` - Total votes in the section
  - `row_mean` - Mean votes across all elections
  - `row_std` - Standard deviation of votes
  - `1std_lower` - Lower bound (1 standard deviation)
  - `1std_upper` - Upper bound (1 standard deviation)
  - `2std_lower` - Lower bound (2 standard deviations)
  - `2std_upper` - Upper bound (2 standard deviations)

- `sections_with_addresses.csv` - Section locations across all elections
  - `section_id` - Unique section identifier
  - For each election (E{YYYYMMDD}):
    - `E{YYYYMMDD}_ekatte` - EKATTE code for the section location
    - `E{YYYYMMDD}_address` - Physical address of the section

## API Data Structure

The repository provides JSON-formatted election data through an API. The data is available at different geographical levels, from individual voting sections up to country-wide totals. The JSON structure uses abbreviated keys derived from the CSV column names, where each key typically uses the first letter of each word in the original column name.

### API Organization

The API provides data through two main paths:
1. Election-specific data: `/YYYYMMDD/` - Contains data for a specific election (e.g., `/20210404/`)
2. Combined data: `/combined/` - Contains aggregated data across all supported elections

Each path provides data at four hierarchical levels:

```
/api/{base_path}/
├── total/             # Country-level aggregated data
├── riks/              # Regional election commission level
│   └── {code}/        # Individual RIK data
├── municipalities/    # Municipality level
│   └── {code}/        # Individual municipality data
└── sections/          # Section level
    └── {id}/          # Individual section data
```

All endpoints return data in the same JSON format with an `index.json` file.

### Common JSON Structure

All hierarchical levels (total, RIK, municipality, section) share the same JSON structure:

```json
{
    "id": "Identifier (varies by level - see details below)",
    "e": "Election date (YYYYMMDD)",
    "prv": "Pre-registered voters",
    "rv": "Registered voters",
    "olv": "On-site listed voters",
    "v": "Total voters who voted",
    "db": "Distributed ballots",
    "uupb": "Unused paper ballots",
    "dpb": "Destroyed paper ballots",
    "ub": "Used ballots",
    "upb": "Used paper ballots",
    "umb": "Used machine ballots",
    "ipb": "Invalid paper ballots",
    "vv": "Valid votes",
    "vvp": "Valid votes for parties",
    "vvsn": "Valid votes for 'support none'",
    "vd": [
        {
            "id": "Party/candidate registration code",
            "n": "Party/candidate name",
            "p": "Paper votes",
            "m": "Machine votes",
            "md": "Machine data votes",
            "t": "Total votes"
        }
    ]
}
```

### Identifier Format by Level

Each level uses a specific format for the `id` field:

- **Total** (`/total/index.json`)
  - No ID field (country-level data)
  - Example: `/20210404/total/index.json`

- **RIK** (`/riks/{code}/index.json`)
  - Two-digit Regional Commission code
  - Example: `/20210404/riks/01/index.json`

- **Municipality** (`/municipalities/{code}/index.json`)
  - Four-digit Municipality code
  - Example: `/20210404/municipalities/0101/index.json`

- **Section** (`/sections/{id}/index.json`)
  - Nine-digit Section identifier
  - Example: `/20210404/sections/010100001/index.json`

### Combined Data Structure (`/combined/`)

The combined data path provides aggregated data across all supported elections. While it follows the same hierarchical organization as election-specific data, the JSON structure is modified to accommodate multiple elections:

```json
{
    "id": "Identifier (varies by level - same as election-specific)",
    "prv": [
        {
            "e": "Election date (YYYYMMDD)",
            "v": "Number of pre-registered voters"
        }
    ],
    "rv": [
        {
            "e": "Election date (YYYYMMDD)",
            "v": "Number of registered voters"
        }
    ],
    "olv": [
        {
            "e": "Election date (YYYYMMDD)",
            "v": "Number of on-site listed voters"
        }
    ],
    // ... similar arrays for v, db, uupb, dpb, ub, upb, umb, ipb, vv, vvp, vvsn
    "vd": [
        {
            "id": "Party/candidate registration code",
            "n": "Party/candidate name",
            "p": [
                {
                    "e": "Election date (YYYYMMDD)",
                    "v": "Number of paper votes"
                }
            ],
            "m": [
                {
                    "e": "Election date (YYYYMMDD)",
                    "v": "Number of machine votes"
                }
            ],
            "md": [
                {
                    "e": "Election date (YYYYMMDD)",
                    "v": "Number of machine data votes"
                }
            ],
            "t": [
                {
                    "e": "Election date (YYYYMMDD)",
                    "v": "Total number of votes"
                }
            ]
        }
    ]
}
```

Key differences from election-specific data:
1. All numeric values are wrapped in arrays of objects with election date (`e`) and value (`v`)
2. Party/candidate voting details (`vd`) contain arrays of votes per election
3. Data is available for all supported elections at each level
4. Results can be compared across elections within the same JSON response

The combined structure makes it easy to:
- Track changes in voter registration and turnout over time
- Compare party performance across multiple elections
- Analyze voting method trends (paper vs. machine)
- Study geographical voting patterns over time

### Common Reference Data

Static reference data available at `/common/`:
- `/elections/` - Election metadata
- `/municipalities/` - Municipality reference data
- `/participants/` - Party and coalition information
- `/riks/` - Regional election commission details

### Custom Analytics

Specialized analytical views available at `/custom/`:
- `/sections_total_votes/` - Statistical analysis of voting patterns

## License

This repository uses dual licensing:

- **Source Data**: All data files in the `/data` directory are licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

- **API Data**: All data served through our GitHub Pages API (not present in the repository but generated during build) is also licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). This applies to all JSON data accessible through our API endpoints.

Both data licenses allow for both personal and commercial use, with the requirements of attribution and sharing any derivative works under the same license.

- **Code**: All code in this repository (including the converter tools) is licensed under the [MIT License](LICENSE). This provides very broad permissions to use, modify, and distribute the code, requiring only that the original copyright and license notices are preserved.

Please see the individual LICENSE files in the root directory and the `/data` directory for the full license texts.
