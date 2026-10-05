#!/usr/bin/env python3
"""gRPC server for the OTLP collector services that answers every Export with an error status.

The status of the answer is chosen by the call metadata x-otel-test-status, for example
UNAVAILABLE;retry=1500 (code UNAVAILABLE with RetryInfo, retry_delay 1500 ms),
RESOURCE_EXHAUSTED;quota (QuotaFailure in the status details, no RetryInfo) or
RESOURCE_EXHAUSTED (no status details).

For every call one line is appended to the log file: the scenario and the time of the call
in milliseconds (monotonic clock), separated by a tab.

Arguments: port, log file. Requires grpcio and grpcio-status.
"""
import sys
import threading
import time
from concurrent import futures

import grpc
from google.protobuf import any_pb2, duration_pb2
from google.rpc import code_pb2, error_details_pb2, status_pb2
from grpc_status import rpc_status

SERVICES = (
    'opentelemetry.proto.collector.trace.v1.TraceService',
    'opentelemetry.proto.collector.logs.v1.LogsService',
    'opentelemetry.proto.collector.metrics.v1.MetricsService',
)


def status_details(options):
    details = []
    for option in options:
        if option.startswith('retry='):
            delay_ms = int(option[len('retry='):])
            delay = duration_pb2.Duration(seconds=delay_ms // 1000, nanos=(delay_ms % 1000) * 1000000)
            detail = any_pb2.Any()
            detail.Pack(error_details_pb2.RetryInfo(retry_delay=delay))
            details.append(detail)
        elif option == 'quota':
            violation = error_details_pb2.QuotaFailure.Violation(subject='client', description='quota')
            detail = any_pb2.Any()
            detail.Pack(error_details_pb2.QuotaFailure(violations=[violation]))
            details.append(detail)
    return details


def main():
    port, log_path = int(sys.argv[1]), sys.argv[2]
    lock = threading.Lock()

    def export(request, context):
        scenario = dict(context.invocation_metadata()).get('x-otel-test-status', 'UNAVAILABLE')
        with lock:
            with open(log_path, 'a', encoding='utf-8') as log:
                log.write(f'{scenario}\t{int(time.monotonic() * 1000)}\n')
        code_name, *options = scenario.split(';')
        status = status_pb2.Status(
            code=getattr(code_pb2, code_name), message='test error', details=status_details(options))
        context.abort_with_status(rpc_status.to_status(status))

    handlers = [
        grpc.method_handlers_generic_handler(service, {'Export': grpc.unary_unary_rpc_method_handler(export)})
        for service in SERVICES
    ]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    server.add_generic_rpc_handlers(handlers)
    server.add_insecure_port(f'127.0.0.1:{port}')
    server.start()
    print(f'gRPC status server on port {port}', flush=True)
    server.wait_for_termination()


if __name__ == '__main__':
    main()
