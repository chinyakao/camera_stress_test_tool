#set default count
MAX_COUNT=100

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
 sudo gst-launch-1.0 icamerasrc ! autovideosink &
 sleep 10
 sudo killall gst-launch-1.0
 sleep 2
done