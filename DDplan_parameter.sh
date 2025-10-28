#!/bin/bash

# File check
FILTERBANK_FILE="$1"

if [ -z "$FILTERBANK_FILE" ]; then
  echo "Error: Please provide the filterbank file path."
  exit 1
fi

if [ ! -f "$FILTERBANK_FILE" ]; then
  echo "Error: File not found at '$FILTERBANK_FILE'."
  exit 1
fi

# Parameter extraction from readfile

echo "Running readfile"

# Run readfile and store the output in a variable
READFILE_OUTPUT=$(readfile "$FILTERBANK_FILE" 2>&1)

# Function to safely extract a value using AWK
extract_value() {
  # Use the READFILE_OUTPUT variable as input
  echo "$READFILE_OUTPUT" | \
  grep -iF "$1" | \
  awk -F= '{print $2}' | \
  tr -d '[:space:]' | \
  # Remove the trailing unit (e.g., 'MHz', 'us') if it exists
  sed 's/[[:alpha:]].*//g'
}

# Extract required parameters for DDplan.py

CENTRAL_FREQ=$(extract_value "Central freq (MHz)")
BANDWIDTH=$(extract_value "Total Bandwidth (MHz)")
NUM_CHANNELS=$(extract_value "Number of channels")
SAMPLE_TIME_US=$(extract_value "Sample time (us)")

# DEFINE DDplan.py PARAMETERS

# Extract the base filename (e.g., 'data.fil' -> 'data')
BASENAME=$(basename "$FILTERBANK_FILE" .fil)

# Convert microseconds (us) to seconds (s) for DDplan.py's -t flag
SAMPLE_TIME_S=$(echo "scale=8; $SAMPLE_TIME_US / 1000000" | bc)


#====== change parameters as needed ==========

DDPLAN_ARGS=(
  #change the values as needed
  # Set output filename without .fil extension
  "-o" "${BASENAME}"
  # Low DM (0) and High DM (500)
  "-l" "0.0"
  "-d" "500.0"
  # Extracted values
  "-f" "${CENTRAL_FREQ}"
  "-b" "${BANDWIDTH}"
  "-n" "${NUM_CHANNELS}"
  # Fixed parameters
  "-s" "32" #number of subbands
  # Other required parameters
  "-t" "${SAMPLE_TIME_S}"
)

#run DDplan.py and make parameter file

echo "Running DDplan.py"
echo "Parameters used: ${DDPLAN_ARGS[*]}"

# Run DDplan.py and store its output for later extraction
DDPLAN_OUTPUT=$(DDplan.py "${DDPLAN_ARGS[@]}" 2>&1)
DDPLAN_STATUS=$?

if [ $DDPLAN_STATUS -ne 0 ]; then
  echo "Error: DDplan.py failed with exit code $DDPLAN_STATUS."
  echo "$DDPLAN_OUTPUT" # Output the error messages
  exit 1
fi

# EXTRACT AND SAVE DDplan OUTPUT

OUTPUT_FILE="${BASENAME}_parameters.txt"
echo "Saving output to ${OUTPUT_FILE}"

echo "$DDPLAN_OUTPUT" | \
awk '
  /Low DM/ { 
    print_mode=1; 
	gsub(/Low DM/, "Low_DM", $0);
	gsub(/High DM/, "High_DM", $0);
	gsub(/#/, "", $0);
	gsub(/\//, "", $0);
	gsub(/DMscall/, "DM_call", $0);
	print $0;
 } 
  
  /Optimal/ { 
    print_mode=0; 
    next 
  }
  
  print_mode == 1 { 
    # Check if the line starts with a number (Low DM value) to capture only data rows
    if ($1 ~ /^[0-9]/) {
        print $0 
    }
  }
' > "$OUTPUT_FILE"

echo "Dedispersion parameters saved to $OUTPUT_FILE"
