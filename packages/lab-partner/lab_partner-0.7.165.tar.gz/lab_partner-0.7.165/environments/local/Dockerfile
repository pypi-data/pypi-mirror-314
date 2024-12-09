FROM opensearchproject/data-prepper:1.0.0 as data-prepper
COPY telemetry/pipelines.yaml telemetry/data-prepper-config.yaml telemetry/certs/root-ca.pem /usr/share/data-prepper/


FROM otel/opentelemetry-collector:0.31.0 as opentelemetry-collector
COPY telemetry/otel-collector-config.yml /etc/