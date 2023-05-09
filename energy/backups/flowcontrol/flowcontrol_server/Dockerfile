FROM ubuntu:20.04
RUN apt-get update && apt-get install -y --no-install-recommends socat r-base-core jq
COPY bin/* bin/
CMD ["/usr/bin/socat", "tcp4-listen:23,reuseaddr,fork,crnl", "exec:/bin/flowcontrol.sh,stderr,pty,su=nobody,echo=0"]
