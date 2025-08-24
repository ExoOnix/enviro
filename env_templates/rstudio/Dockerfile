FROM rocker/tidyverse:latest

ENV USER=rstudio

EXPOSE 23000

CMD ["/usr/lib/rstudio-server/bin/rserver", "--server-daemonize=0", "--auth-none=1", "--www-port=23000"]
