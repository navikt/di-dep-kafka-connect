FROM confluentinc/cp-kafka-connect:5.0.3

# See https://superuser.com/questions/1423486/issue-with-fetching-http-deb-debian-org-debian-dists-jessie-updates-inrelease
RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list

COPY run.sh /usr/local/bin/run-kafka-connect.sh

CMD ["/usr/local/bin/run-kafka-connect.sh"]