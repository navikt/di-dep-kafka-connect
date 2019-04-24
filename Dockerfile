FROM confluentinc/cp-kafka-connect:5.0.3

COPY run.sh /usr/local/bin/run-kafka-connect.sh

CMD ["/usr/local/bin/run-kafka-connect.sh"]