#set default count
MAX_COUNT=100
#initialize failure count
FAILURE_COUNT=0

#parse parameters
while getopts "c:" opt; do
 case $opt in
   c) MAX_COUNT=$OPTARG ;;  #set the maximum count
   *)
     echo "Usage: $0 [-c count]"
     exit 1
     ;;
 esac
done

#confirm MAX_COUNT a positive integer
if ! [[ "$MAX_COUNT" =~ ^[0-9]+$ ]]; then
 echo "Error: Count must be a positive integer."
 exit 1
fi

#execute loop
for ((i = 1; i <= MAX_COUNT; i++)); do
 echo "Running iteration $i..."
 
 #run gst-launch-1.0 command and capture its exit status
 sudo gst-launch-1.0 icamerasrc ! autovideosink &
 sleep 10
 sudo killall gst-launch-1.0
 GST_EXIT_STATUS=$?  #capture the exit status of the previous command
 
 if [ $GST_EXIT_STATUS -ne 0 ]; then
   echo "Error occurred in iteration $i, exit status: $GST_EXIT_STATUS"
   FAILURE_COUNT=$((FAILURE_COUNT + 1))  #failure count
 fi
 
 sleep 2
done

#print the summary
echo "Execution completed."
echo "Total failures: $FAILURE_COUNT"