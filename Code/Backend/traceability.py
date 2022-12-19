name: Action To Run traceability.py
run-name: ${{ github.actor }} run of traceability.py Action Demo
on: [pull_request]

jobs:
  Example-Action:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - uses: tj-actions/changed-files@v33
        id: changed-files

      - uses: actions/setup-python@v4
        with:
          python-version: "3.8"
      - name: "PR commits + 1"
        run: echo "PR_FETCH_DEPTH=$(( ${{ github.event.pull_request.commits }} + 1 ))" >> "${GITHUB_ENV}"
      - uses: actions/checkout@v3
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: ${{ env.PR_FETCH_DEPTH }}
      - name: Install dependencies
        run: python -m pip install -r requirements.txt

      - name: Get Variables
        run: |
          for line in $(cat config.conf); do
            echo $line >> $GITHUB_ENV
          done
      - run: |
          cd ./Code/Backend
          touch changed-file-list.txt
          for file in ${{ steps.changed-files.outputs.all_changed_files }}; do
            echo "$file"
            echo "$file" >> changed-file-list.txt
          done
          touch Traceability_Report.html
          echo "<!DOCTYPE html><html><head><title>T-Miner Traceability Report</title></head><body><p>Commit Details: " >> Traceability_Report.html
          git log >> Traceability_Report.html
          echo "</p><ol>" >> Traceability_Report.html
          python traceability.py $sourcePath $targetList $outputFile $targetThreshold $targetSourceString $targetString $targetSourceValue ${{ github.repository }}
          echo "</ol></body></html>" >> Traceability_Report.html
      - name: Upload changed files list
        uses: actions/upload-artifact@v3
        with:
          name: Traceability Report
          path: Code/Backend/Traceability_Report.html
