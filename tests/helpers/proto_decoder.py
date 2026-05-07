#!/usr/bin/env python3
"""Декодирует OTLP protobuf-байты из файла и выводит JSON.

Использование:
  python3 proto_decoder.py <signal> <input_file>

  signal: traces | logs | metrics
  input_file: файл с бинарными proto-данными

Выход: JSON на stdout, код возврата 0 при успехе.
"""
import sys
import os
import json

# Используем pre-compiled proto stubs из proto_generated/
GENERATED_DIR = os.path.join(os.path.dirname(__file__), 'proto_generated')
if GENERATED_DIR not in sys.path:
    sys.path.insert(0, GENERATED_DIR)

def ensure_compiled():
    pass  # stubs уже скомпилированы и закоммичены в proto_generated/

def decode(signal, data):
    ensure_compiled()
    from google.protobuf import json_format

    if signal == 'traces':
        from opentelemetry.proto.collector.trace.v1 import trace_service_pb2
        msg = trace_service_pb2.ExportTraceServiceRequest()
    elif signal == 'logs':
        from opentelemetry.proto.collector.logs.v1 import logs_service_pb2
        msg = logs_service_pb2.ExportLogsServiceRequest()
    elif signal == 'metrics':
        from opentelemetry.proto.collector.metrics.v1 import metrics_service_pb2
        msg = metrics_service_pb2.ExportMetricsServiceRequest()
    else:
        print(f'ERROR: unknown signal "{signal}". Use traces|logs|metrics', file=sys.stderr)
        sys.exit(1)

    msg.ParseFromString(data)
    result = json_format.MessageToDict(msg, preserving_proto_field_name=True)
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <traces|logs|metrics> <input_file>', file=sys.stderr)
        sys.exit(1)

    signal = sys.argv[1]
    input_file = sys.argv[2]

    with open(input_file, 'rb') as f:
        data = f.read()

    print(decode(signal, data))
