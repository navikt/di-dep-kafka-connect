FROM confluentinc/cp-kafka-connect:5.0.3

# See https://superuser.com/questions/1423486/issue-with-fetching-http-deb-debian-org-debian-dists-jessie-updates-inrelease
RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list

RUN echo "deb http://nginx.org/packages/debian/ jessie nginx" | tee /etc/apt/sources.list.d/nginx.list
RUN curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add -

RUN apt-get update && apt-get install -y nginx gettext-base

COPY nginx.conf /etc/nginx/conf.d/connect.conf
COPY run.sh /usr/local/bin/run-kafka-connect.sh

CMD ["/usr/local/bin/run-kafka-connect.sh"]