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

PROTO_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'proto')

# Добавляем скомпилированные proto в sys.path
# (генерируем при первом запуске в /tmp/otlp_proto_gen)
GENERATED_DIR = '/tmp/otlp_proto_gen'

def compile_protos():
    from grpc_tools import protoc
    os.makedirs(GENERATED_DIR, exist_ok=True)
    proto_files = [
        'opentelemetry/proto/common/v1/common.proto',
        'opentelemetry/proto/resource/v1/resource.proto',
        'opentelemetry/proto/trace/v1/trace.proto',
        'opentelemetry/proto/logs/v1/logs.proto',
        'opentelemetry/proto/metrics/v1/metrics.proto',
        'opentelemetry/proto/collector/trace/v1/trace_service.proto',
        'opentelemetry/proto/collector/logs/v1/logs_service.proto',
        'opentelemetry/proto/collector/metrics/v1/metrics_service.proto',
    ]
    args = [
        'grpc_tools.protoc',
        f'-I{PROTO_DIR}',
        f'--python_out={GENERATED_DIR}',
    ] + proto_files
    result = protoc.main(args)
    if result != 0:
        print(f'ERROR: proto compilation failed (code {result})', file=sys.stderr)
        sys.exit(1)

def ensure_compiled():
    marker = os.path.join(GENERATED_DIR, 'opentelemetry', 'proto', 'collector', 'trace', 'v1', 'trace_service_pb2.py')
    if not os.path.exists(marker):
        compile_protos()
    if GENERATED_DIR not in sys.path:
        sys.path.insert(0, GENERATED_DIR)

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
