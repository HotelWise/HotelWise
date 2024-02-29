FROM apache/beam_python3.11_sdk:2.54.0

WORKDIR /app

RUN pip install --no-cache-dir apache-beam[gcp]==2.54.0

RUN pip install --no-cache-dir -U googlemaps

RUN pip install --no-cache-dir polars

COPY . /app/

ENTRYPOINT ["/opt/apache/beam/boot"]

