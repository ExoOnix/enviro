#!/bin/bash

# Start the first process
sudo dockerd &

# Start the second process
code-server /home/coder/project --bind-addr 0.0.0.0:8080 --disable-getting-started-override=true --auth=none &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?