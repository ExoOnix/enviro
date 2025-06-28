#!/bin/bash

start_dockerd() {
    # Clean up stale PID file if necessary
    if [ -f /var/run/docker.pid ]; then
        pid=$(cat /var/run/docker.pid)
        if ! ps -p "$pid" > /dev/null 2>&1; then
            echo "Removing stale Docker PID file"
            sudo rm -f /var/run/docker.pid
        else
            echo "dockerd already running with PID $pid"
            return
        fi
    fi

    echo "Starting dockerd..."
    sudo dockerd > /tmp/dockerd.log 2>&1 &
}


# Start the first process
start_dockerd &

# Start the second process
code-server /home/coder/project --bind-addr 0.0.0.0:8080 --disable-getting-started-override=true --auth=none &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?