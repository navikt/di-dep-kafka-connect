FROM adoptopenjdk/openjdk11:slim AS jmxexporter

WORKDIR /usr/local/
ENV EXPORTER_VERSION=76cf1bf03c4cd4a050eb089f37af6a8af15abf0a
ENV EXPORTER_REPO=github.com/prometheus/jmx_exporter

RUN set -ex; \
    DEBIAN_FRONTEND=noninteractive; \
    runDeps=''; \
    buildDeps='curl ca-certificates' \
    apt-get update && apt-get install -y $runDeps $buildeps --no-install-recommends; \
    MAVEN_VERSION=3.6.2 PATH=$PATH:$(pwd)/maven/bin; \
    mkdir ./maven; \
    curl -SLs https://archive.apache.org/dist/maven/maven-3/$MAVEN_VERSION/binaries/apache-maven-$MAVEN_VERSION-bin.tar.gz | tar -xzf - --strip-components=1 -C ./maven; \
    mvn --version; \
    mkdir ./jmx_exporter; \
    curl -SLs https://$EXPORTER_REPO/archive/$EXPORTER_VERSION.tar.gz | tar -xzf - --strip-components=1 -C ./jmx_exporter; \
    cd ./jmx_exporter; \
    mvn package; \
    find jmx_prometheus_httpserver/ -name *-jar-with-dependencies.jar -exec mv -v '{}' ../jmx_prometheus_httpserver.jar \;; \
    mv example_configs ../; \
    cd ..; \
    rm -Rf ./jmx_exporter ./maven /root/.m2; \
    apt-get purge -y --auto-remove $buildDeps; \
    rm -rf /var/lib/apt/lists/*; \
    rm -rf /var/log/dpkg.log /var/log/alternatives.log /var/log/apt


FROM confluentinc/cp-kafka-connect:5.4.1 AS main

# See https://superuser.com/questions/1423486/issue-with-fetching-http-deb-debian-org-debian-dists-jessie-updates-inrelease
RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list

RUN echo "deb http://nginx.org/packages/debian/ jessie nginx" | tee /etc/apt/sources.list.d/nginx.list
RUN curl -fsSL https://nginx.org/keys/nginx_signing.key | apt-key add -

RUN apt-get update && apt-get install -y nginx gettext-base

COPY nginx.conf /etc/nginx/conf.d/connect.conf
RUN mkdir -p /usr/share/java/vault-provider
COPY kafka-connect-vault-provider.jar /usr/share/java/vault-provider/
COPY vault-java-driver.jar /usr/share/java/vault-provider/

### Setup JMX exporter

RUN mkdir -p /usr/local/jmx_prometheus
COPY --from=jmxexporter /usr/local/jmx_prometheus_httpserver.jar /usr/local/jmx_prometheus
COPY jmx-kafka-connect-prometheus.yml /usr/local/jmx_prometheus/

### Setup Oracle JDBC driver
COPY ojdbc8-12.2.0.1.jar /usr/share/java/kafka-connect-jdbc/jars/

### ADD custom Oracle dialect
COPY complex-types-oracle-dialect.jar /usr/share/java/kafka-connect-jdbc/

### ADD Kafa Connect util lib (used to convert STRUCT fields to JSON)
COPY kafka-connect-common-1.1.9.jar /usr/share/java/kafka-connect-jdbc/jars/

# Install and configure s6 supervisor
ADD https://github.com/just-containers/s6-overlay/releases/download/v1.22.1.0/s6-overlay-amd64.tar.gz /tmp/
RUN tar xzf /tmp/s6-overlay-amd64.tar.gz -C /
COPY ./s6/ /etc/services.d/
ENV S6_KEEP_ENV=1

ENTRYPOINT ["/init"]
