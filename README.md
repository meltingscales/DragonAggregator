# DragonAggregator

This tool aggregates vulnerability data from SAST, DAST, SCA, and Secrets scanning into a unified format and saves it to an SQLite database. 

It is intended to be a standalone component, data analysis CLI tool, or used as a backend for a vulnerability management tool.

## Usage

### Running locally
    
```sh
poetry install
poetry shell

python -m dragonaggregator pull   veracode  sast  --config config.yaml
python -m dragonaggregator pull   veracode  dast  --config config.yaml
python -m dragonaggregator pull   snyk      sca   --config config.yaml
# then, view db.sqlite3 with a SQLite browser

python -m dragonaggregator export all       all --output output_all.json
# or, view output.json
```

## Future Goals

- Normalize data into standardized formats like SPDX, SARIF, and CycloneDX
  - This avoids the need for custom parsers or the use of whatever custom "VulnFinding" models I come up with
- Add more scanners
  - Checkmarx
  - SonarQube
  - GitLab
  - GitHub
  - Container scanners
  - Fortify
  - ShiftLeft
- Add a modular architecture for adding scanners
- Add more export formats

# Other ideas

## Standards/frameworks

- CVRF
  - https://www.first.org/cvrf/
- OVAL
  - https://oval.mitre.org/
- CVSS
  - https://www.first.org/cvss/
- CWE
  - https://cwe.mitre.org/
- NVD
  - https://nvd.nist.gov/
- SCAP
  - https://scap.nist.gov/
- CycloneDX
  - https://cyclonedx.org/
- SPDX
  - https://spdx.dev/
- SARIF
  - https://sarifweb.azurewebsites.net/