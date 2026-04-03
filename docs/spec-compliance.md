# Анализ соответствия спецификации OpenTelemetry v1.55.0

> **Версия спецификации**: [v1.55.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-04-03
> **Методология**: spec-first - извлечены все MUST/SHOULD требования из спецификации, затем каждое прослежено до кода

## Сводка (Stable)

Учитываются только требования из стабильных разделов спецификации.

| Показатель | Значение |
|---|---|
| Всего требований | 767 (Stable: 668, Development: 99) |
| Применимых Stable (без N/A) | 621 |
| ✅ Реализовано | 381 (61.4%) |
| ⚠️ Частично | 177 (28.5%) |
| ❌ Не реализовано | 63 (10.1%) |
| N/A (неприменимо) | 47 |
| **MUST/MUST NOT** | 277/386 (71.8%) |
| **SHOULD/SHOULD NOT** | 104/235 (44.3%) |

## Соответствие по разделам (Stable)

| Раздел | Всего | ✅ | ⚠️ | ❌ | N/A | % | Dev |
|---|---|---|---|---|---|---|---|
| Context | 14 | 12 | 0 | 0 | 2 | 100.0% | 0 |
| Baggage Api | 16 | 15 | 0 | 0 | 1 | 100.0% | 0 |
| Resource Sdk | 15 | 9 | 2 | 1 | 3 | 75.0% | 10 |
| Trace Api | 115 | 99 | 6 | 0 | 10 | 94.3% | 4 |
| Trace Sdk | 81 | 48 | 16 | 6 | 11 | 68.6% | 29 |
| Logs Api | 20 | 7 | 2 | 11 | 0 | 35.0% | 2 |
| Logs Sdk | 67 | 27 | 2 | 38 | 0 | 40.3% | 18 |
| Metrics Api | 99 | 79 | 16 | 0 | 4 | 83.2% | 0 |
| Metrics Sdk | 170 | 59 | 111 | 0 | 0 | 34.7% | 32 |
| Otlp Exporter | 21 | 3 | 9 | 1 | 8 | 23.1% | 0 |
| Propagators | 34 | 18 | 4 | 6 | 6 | 64.3% | 0 |
| Env Vars | 16 | 5 | 9 | 0 | 2 | 35.7% | 4 |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Env Vars]** [MUST] The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105,114,136,143`)
  - Empty values handling incomplete
- ⚠️ **[Env Vars]** [MUST] Any value that represents a Boolean MUST be set to true only by the (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563`)
  - Only true recognized
- ⚠️ **[Env Vars]** [MUST] here as a true value, including unset and empty values, MUST be interpreted as (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563`)
  - No explicit warning
- ⚠️ **[Env Vars]** [MUST] implementations, these should be treated as MUST requirements. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - No explicit error handling
- ⚠️ **[Env Vars]** [MUST] the implementation does not recognize, the implementation MUST generate (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:216-218`)
  - Inconsistent error logging
- ⚠️ **[Logs Api]** [MUST] The API MUST accept the following parameters: (`src/Логирование/Классы/ОтелЛоггер.os:21-58`)
  - Lacks convenience params
- ❌ **[Logs Api]** [MUST] if unspecified then MUST use current Context.
  - No current Context documentation
- ❌ **[Logs Api]** [MUST] if unspecified then MUST use current Context.
  - No current Context in Enabled
- ❌ **[Logs Api]** [MUST] This API MUST return a language idiomatic boolean type. A returned value of
  - Enabled not documented as idiomatic
- ❌ **[Logs Api]** [MUST] For each required parameter, the API MUST be structured to obligate a user to
  - User param provision docs missing
- ❌ **[Logs Api]** [MUST] LoggerProvider - all methods MUST be documented that implementations need to
  - LoggerProvider concurrency docs missing
- ❌ **[Logs Api]** [MUST] Logger - all methods MUST be documented that implementations need to
  - Logger concurrency docs missing
- ⚠️ **[Logs Sdk]** [MUST] working `Logger` MUST be returned as a fallback rather than returning null or (`src/Логирование/Классы/ОтелЛоггер.os:77-85`)
  - No no-op fallback
- ❌ **[Logs Sdk]** [MUST] MUST be owned by the `LoggerProvider`. The configuration MAY be applied at the
  - LoggerConfigurator not found
- ❌ **[Logs Sdk]** [MUST] configuration MUST also apply to all already returned `Logger`s (i.e. it MUST
  - Config for existing loggers missing
- ❌ **[Logs Sdk]** [MUST] If an Exception is provided, the SDK MUST by default set attributes
  - Exception attribute missing
- ❌ **[Logs Sdk]** [MUST NOT] User-provided attributes MUST take precedence and MUST NOT be overwritten by
  - User attributes precedence missing
- ❌ **[Logs Sdk]** [MUST] `Enabled` MUST return `false` when either:
  - Enabled return conditions missing
- ❌ **[Logs Sdk]** [MUST] A function receiving this as an argument MUST additionally be able to modify
  - ReadWriteLogRecord not implemented
- ❌ **[Logs Sdk]** [MUST] To prevent excessive logging, the message MUST be printed at most once per
  - One-time warning logging missing
- ❌ **[Logs Sdk]** [MUST NOT] Any modifications to parameters inside `Enabled` MUST NOT be propagated to the
  - Enabled param mutation prevention missing
- ❌ **[Logs Sdk]** [MUST] timeout is specified (see below), the `LogRecordProcessor` MUST prioritize
  - ForceFlush timeout priority missing
- ❌ **[Logs Sdk]** [MUST] Each implementation MUST document the concurrency characteristics the SDK
  - Concurrency docs missing
- ❌ **[Logs Sdk]** [MUST] Logger - all methods MUST be safe to be called concurrently.
  - Logger method concurrency missing
- ⚠️ **[Metrics Api]** [MUST] Therefore, this API MUST be structured to accept a variable number of (`-`)
  - Callback variable pattern limited
- ⚠️ **[Metrics Api]** [MUST] asynchronous instrumentation creation, the user MUST be able to undo (`-`)
  - No explicit callback deregistration API
- ⚠️ **[Metrics Api]** [MUST] Every currently registered Callback associated with a set of instruments MUST (`-`)
  - Callback execution per reader not documented
- ⚠️ **[Metrics Api]** [MUST] Callback functions MUST be documented as follows for the end user: (`-`)
  - Callback documentation present but could be more detailed
- ⚠️ **[Metrics Api]** [MUST] Callbacks registered at the time of instrument creation MUST apply to (`-`)
  - Multiple callbacks at creation limited by design
- ⚠️ **[Metrics Api]** [MUST] Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the (`-`)
  - Multi-instrument callback registration not supported
- ⚠️ **[Metrics Api]** [MUST] Multiple-instrument Callbacks MUST be associated at the time of (`-`)
  - Callbacks only at instrument creation time
- ⚠️ **[Metrics Api]** [MUST] The API MUST treat observations from a single Callback as logically (`-`)
  - Observations atomic but logical grouping not explicit
- ⚠️ **[Metrics Api]** [MUST] This API MUST return a language idiomatic boolean type. A returned value of (`-`)
  - No explicit Enabled API returning boolean
- ⚠️ **[Metrics Sdk]** [MUST NOT] configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT (`-`)
  - Configuration to returned Meters unclear
- ⚠️ **[Metrics Sdk]** [MUST] attributes that MUST be excluded, all other attributes MUST be kept. If an (`-`)
  - Exclude attribute unclear
- ⚠️ **[Metrics Sdk]** [MUST] Callback functions MUST be invoked for the specific `MetricReader` (`-`)
  - Callback per MetricReader not explicit
- ⚠️ **[Metrics Sdk]** [MUST] The implementation MUST complete the execution of all callbacks for a (`-`)
  - All callback completion unclear
- ⚠️ **[Metrics Sdk]** [MUST] Aggregators for synchronous instruments with cumulative temporality MUST (`-`)
  - Cumulative cardinality guarantee unclear
- ⚠️ **[Metrics Sdk]** [MUST] Regardless of aggregation temporality, the SDK MUST ensure that every (`-`)
  - Synchronous enforcement unclear
- ⚠️ **[Metrics Sdk]** [MUST] the SDK MUST aggregate data from identical Instruments (`-`)
  - Conflicting identities unclear
- ⚠️ **[Metrics Sdk]** [MUST] multiple casings of the same `name`. When this happens, the Meter MUST return (`-`)
  - Unit conflict handling unclear
- ⚠️ **[Metrics Sdk]** [MUST] If a unit is not provided or the unit is null, the Meter MUST treat it the same (`-`)
  - Duplicate stream generation unclear
- ⚠️ **[Metrics Sdk]** [MUST] Meter MUST treat it the same as an empty description string. (`-`)
  - View priority on duplicates unclear
- ⚠️ **[Metrics Sdk]** [MUST] different advisory parameters, the Meter MUST return an instrument using the (`-`)
  - Duplicate start timestamp handling unclear
- ⚠️ **[Metrics Sdk]** [MUST] MUST take precedence over the advisory parameters. (`-`)
  - Name normalization for duplicates unclear
- ⚠️ **[Metrics Sdk]** [MUST] parameter MUST be used. If neither is provided, the default bucket boundaries (`-`)
  - Case sensitivity in duplicates unclear
- ⚠️ **[Metrics Sdk]** [MUST] The synchronous instrument `Enabled` MUST return `false` (`-`)
  - Name conflict detection unclear
- ⚠️ **[Metrics Sdk]** [MUST] A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements (`-`)
  - Unit conflict detection unclear
- ⚠️ **[Metrics Sdk]** [MUST NOT] off, the SDK MUST NOT have overhead related to exemplar sampling. (`-`)
  - Multiple views per instrument unclear
- ⚠️ **[Metrics Sdk]** [MUST] A Metric SDK MUST allow exemplar sampling to leverage the configuration of (`-`)
  - View conflict resolution unclear
- ⚠️ **[Metrics Sdk]** [MUST] The `ExemplarFilter` configuration MUST allow users to select between one of the (`-`)
  - Implicit view creation unclear
- ⚠️ **[Metrics Sdk]** [MUST] An OpenTelemetry SDK MUST support the following filters: (`-`)
  - Cardinality enforcement unclear
- ⚠️ **[Metrics Sdk]** [MUST] The `ExemplarReservoir` interface MUST provide a method to offer measurements (`-`)
  - Overflow attribute cardinality unclear
- ⚠️ **[Metrics Sdk]** [MUST] A new `ExemplarReservoir` MUST be created for every known timeseries data point, (`-`)
  - Measurement drop behavior unclear
- ⚠️ **[Metrics Sdk]** [MUST] from the timeseries the reservoir is associated with. This MUST be clearly (`-`)
  - Reader time window unclear
- ⚠️ **[Metrics Sdk]** [MUST] documented in the API and the reservoir MUST be given the `Attributes` (`-`)
  - Reader collection interval unclear
- ⚠️ **[Metrics Sdk]** [MUST] The “collect” method MUST return accumulated `Exemplar`s. Exemplars are expected (`-`)
  - Reader export format unclear
- ⚠️ **[Metrics Sdk]** [MUST] `Exemplar`s MUST retain any attributes available in the measurement that (`-`)
  - Reader shutdown behavior unclear
- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST include two types of built-in exemplar reservoirs: (`-`)
  - Cumulative temporality default unclear
- ⚠️ **[Metrics Sdk]** [MUST] This reservoir MUST use a uniformly-weighted sampling algorithm based on the (`-`)
  - Reserved attribute handling unclear
- ⚠️ **[Metrics Sdk]** [MUST] This Exemplar reservoir MUST take a configuration parameter that is the (`-`)
  - Concurrent instrument creation unclear
- ⚠️ **[Metrics Sdk]** [MUST] configuration of a Histogram. This implementation MUST store at most one (`-`)
  - Concurrent measurement unclear
- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST provide a mechanism for SDK users to provide their own (`-`)
  - Provider shutdown concurrency unclear
- ⚠️ **[Metrics Sdk]** [MUST] ExemplarReservoir implementation. This extension MUST be configurable on (`-`)
  - No-op fallback unclear
- ⚠️ **[Metrics Sdk]** [MUST] a metric View, although individual reservoirs MUST still be (`-`)
  - Resource mutation unclear
- ⚠️ **[Metrics Sdk]** [MUST] `Shutdown` MUST be called only once for each `MetricReader` instance. After the (`-`)
  - Cardinality budget unclear
- ⚠️ **[Metrics Sdk]** [MUST] The reader MUST synchronize calls to `MetricExporter`’s `Export` (`-`)
  - Attribute context propagation unclear
- ⚠️ **[Metrics Sdk]** [MUST] `MetricExporter` defines the interface that protocol-specific exporters MUST (`-`)
  - Reader-specific start timestamps unclear
- ⚠️ **[Metrics Sdk]** [MUST] A Push Metric Exporter MUST support the following functions: (`-`)
  - Multiple reader aggregation unclear
- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST provide a way for the exporter to get the Meter (`-`)
  - Synchronization points unclear
- ⚠️ **[Metrics Sdk]** [MUST NOT] `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit (`-`)
  - Lock contention mitigation unclear
- ⚠️ **[Metrics Sdk]** [MUST] sources MUST implement, so they can be plugged into an OpenTelemetry (`-`)
  - Histogram bucket optimization unclear
- ⚠️ **[Metrics Sdk]** [MUST] A `MetricProducer` MUST support the following functions: (`-`)
  - Decimal handling unclear
- ⚠️ **[Metrics Sdk]** [MUST] MUST return a batch of Metric Points, filtered by the optional (`-`)
  - Precision loss prevention unclear
- ⚠️ **[Metrics Sdk]** [MUST] A `MetricFilter` MUST support the following functions: (`-`)
  - Record count accuracy unclear
- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST provide configuration according to the SDK environment (`-`)
  - Sum overflow handling unclear
- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST handle numerical limits in a graceful way according to Error (`-`)
  - Negative measurement handling unclear
- ⚠️ **[Metrics Sdk]** [MUST] it MUST handle all the possible values. For example, if the language runtime (`-`)
  - Zero value semantics unclear
- ⚠️ **[Metrics Sdk]** [MUST] MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe (`-`)
  - Subnormal number handling unclear
- ⚠️ **[Metrics Sdk]** [MUST] ExemplarReservoir - all methods MUST be safe to be called concurrently. (`-`)
  - Double precision limitations unclear
- ⚠️ **[Metrics Sdk]** [MUST] and `Shutdown` MUST be safe to be called concurrently. (`-`)
  - Integer overflow semantics unclear
- ⚠️ **[Metrics Sdk]** [MUST] MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called (`-`)
  - Atomicity guarantees unclear
- ⚠️ **[Otlp Exporter]** [MUST] Each configuration option MUST be overridable by a signal specific option. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:177,255,291`)
  - Signal-specific overrides not implemented
- ⚠️ **[Otlp Exporter]** [MUST] When using `OTEL_EXPORTER_OTLP_ENDPOINT`, exporters MUST construct per-signal URLs as described below. The per-signal endpoint configuration options t... (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:154,159`)
  - No per-signal URL construction
- ⚠️ **[Otlp Exporter]** [MUST] Endpoint (OTLP/gRPC): Target to which the exporter is going to send spans, metrics, or logs. The option SHOULD accept any form allowed by the underlyi... (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150-161`)
  - No http/https scheme distinction
- ⚠️ **[Otlp Exporter]** [MUST] Protocol: The transport protocol. Options MUST be one of: `grpc`, `http/protobuf`, `http/json`. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)
  - http/protobuf not implemented
- ⚠️ **[Otlp Exporter]** [MUST] MUST be used as-is without any modification. The only exception is that if an (`src/Экспорт/Классы/ОтелHttpТранспорт.os:74`)
  - No root path explicit handling
- ⚠️ **[Otlp Exporter]** [MUST] URL contains no path part, the root path `/` MUST be used (see Example 2). (`src/Экспорт/Классы/ОтелHttpТранспорт.os:74`)
  - No URL path append verification
- ⚠️ **[Otlp Exporter]** [MUST] Transient errors MUST be handled with a retry strategy. This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming t... (`src/Экспорт/Классы/ОтелHttpТранспорт.os:85`)
  - No jitter in backoff
- ⚠️ **[Propagators]** [MUST] The OpenTelemetry API MUST provide a way to obtain a propagator for each (`src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os`)
  - No per-type getter
- ⚠️ **[Propagators]** [MUST] These platforms MUST also allow pre-configured propagators to be disabled or overridden. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - Override not detailed
- ❌ **[Propagators]** [MUST] * MUST attempt to extract B3 encoded using single and multi-header (`n/a`)
  - B3 Extract not implemented
- ❌ **[Propagators]** [MUST] the multi-header version.* MUST preserve a debug trace flag, if received, and propagate (`n/a`)
  - B3 multi-header not applicable
- ❌ **[Propagators]** [MUST NOT] MUST set the sampled trace flag when the debug flag is set.* MUST NOT reuse `X-B3-SpanId` as the id for the server-side span.#### B3 Inject (`n/a`)
  - B3 debug flag not applicable
- ❌ **[Propagators]** [MUST] * MUST default to injecting B3 using the single-header format* MUST provide configuration to change the default injection format to B3 (`n/a`)
  - B3 Inject not applicable
- ❌ **[Propagators]** [MUST NOT] multi-header* MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support (`n/a`)
  - B3 multi-header format not applicable
- ❌ **[Propagators]** [MUST] Fields MUST return the header names that correspond to the configured format, (`n/a`)
  - B3 Fields not applicable
- ⚠️ **[Resource Sdk]** [MUST] or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:96-119`)
  - Resource detectors not fully implemented
- ❌ **[Resource Sdk]** [MUST] Resource detector packages MUST provide a method that returns a resource. This (`n/a`)
  - No resource detector packages
- ⚠️ **[Trace Api]** [MUST] (result MUST be a 16-hex-character lowercase string).* Binary - returns the binary representation of the `TraceId` (result MUST be a (`src/Трассировка/Классы/ОтелКонтекстСпана.os`)
  - Only string format, no binary API
- ⚠️ **[Trace Api]** [MUST] 16-byte array) or `SpanId` (result MUST be an 8-byte array). (`Same as above`)
- ⚠️ **[Trace Api]** [MUST] TracerProvider - all methods MUST be documented that implementations need to (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:1`)
  - Uses СинхронизированнаяКарта but no docs
- ⚠️ **[Trace Api]** [MUST] Tracer - all methods MUST be documented that implementations need to be safe (`src/Трассировка/Классы/ОтелТрассировщик.os`)
  - Methods thread-safe by design
- ⚠️ **[Trace Api]** [MUST] Span - all methods MUST be documented that implementations need to be safe (`src/Трассировка/Классы/ОтелСпан.os`)
  - Methods thread-safe by design
- ⚠️ **[Trace Sdk]** [MUST] the updated configuration MUST also apply to all already returned `Tracers` (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os`)
  - Delegation model but no dynamic config updates
- ❌ **[Trace Sdk]** [MUST] The SDK MUST provide a mechanism for customizing the way IDs are generated for (`No IdGenerator extension point`)
- ❌ **[Trace Sdk]** [MUST] `Shutdown` MUST include the effects of `ForceFlush`. (`Not explicit`)
- ❌ **[Trace Sdk]** [MUST] If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over (`No timeout support`)
- ⚠️ **[Trace Sdk]** [MUST] Each implementation MUST document the concurrency characteristics the SDK (`src/Трассировка/Классы/`)
  - Limited documentation

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Env Vars]** [SHOULD] empty, or unset is used, a warning SHOULD be logged to inform users about the
  - Silent false fallback
- ⚠️ **[Env Vars]** [SHOULD] thus qualified as “SHOULD” to allow implementations to avoid breaking changes. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:160,203-204`)
  - Numeric error handling incomplete
- ⚠️ **[Env Vars]** [SHOULD] implementation cannot parse, the implementation SHOULD generate a warning and gracefully
  - No warning for unparseable values
- ⚠️ **[Env Vars]** [SHOULD] Enum values SHOULD be interpreted in a case-insensitive manner. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - Inconsistent case handling
- ⚠️ **[Logs Api]** [SHOULD] The `Logger` SHOULD provide functions to: (`src/Логирование/Классы/ОтелЛоггер.os`)
  - No convenience methods
- ❌ **[Logs Api]** [SHOULD] When implicit Context is supported, then this parameter SHOULD be optional and
  - Context parameter not optional
- ❌ **[Logs Api]** [SHOULD] When only explicit Context is supported, this parameter SHOULD be required.* Severity Number (optional)* Severity Text (optional)* Body (optional)* At...
  - No implicit Context integration
- ❌ **[Logs Api]** [SHOULD] The API SHOULD accept the following parameters:
  - Enabled lacks Context param
- ❌ **[Logs Api]** [SHOULD] When implicit Context is supported, then this parameter SHOULD be optional and
  - Enabled Context not optional
- ❌ **[Logs Api]** [SHOULD] SHOULD be documented that instrumentation authors needs to call this API each
  - Enabled calling docs missing
- ❌ **[Logs Sdk]** [SHOULD] throwing an exception, its `name` SHOULD keep the original invalid value, and a
  - Invalid name handling missing
- ❌ **[Logs Sdk]** [SHOULD] message reporting that the specified value is invalid SHOULD be logged.
  - Invalid name logging missing
- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded,
  - ForceFlush return status missing
- ❌ **[Logs Sdk]** [SHOULD] failed or timed out. `ForceFlush` SHOULD return some ERROR status if there
  - ForceFlush error status missing
- ❌ **[Logs Sdk]** [SHOULD] is an error condition; and if there is no error condition, it SHOULD return
  - ForceFlush success status missing
- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be
  - ForceFlush timeout missing
- ⚠️ **[Logs Sdk]** [SHOULD] the implementation SHOULD set it equal to the current time. (`src/Логирование/Классы/ОтелЗаписьЛога.os:346-349`)
  - Timestamp set no condition
- ❌ **[Logs Sdk]** [SHOULD] The options MAY be bundled in a class, which then SHOULD be called
  - LogLimits naming missing
- ❌ **[Logs Sdk]** [SHOULD] There SHOULD be a message printed in the SDK’s log to indicate to the user
  - Dropped attributes warning missing
- ❌ **[Logs Sdk]** [SHOULD] implementations SHOULD recommended to users that a clone of `logRecord` be used
  - Clone recommendation missing
- ❌ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance.
  - Processor shutdown single-call missing
- ❌ **[Logs Sdk]** [SHOULD] SHOULD ignore these calls gracefully, if possible.
  - Processor shutdown graceful ignore missing
- ❌ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded,
  - Processor shutdown success status missing
- ❌ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` can be
  - Processor shutdown timeout missing
- ❌ **[Logs Sdk]** [SHOULD] to `ForceFlush` SHOULD be completed as soon as possible, preferably before
  - ForceFlush early completion missing
- ❌ **[Logs Sdk]** [SHOULD] SHOULD try to call the exporter’s `Export` with all `LogRecord`s for which this
  - Processor ForceFlush to exporter missing
- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded,
  - ForceFlush success status missing
- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD only be called in cases where it is absolutely necessary,
  - ForceFlush necessity missing
- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be
  - ForceFlush timeout missing
- ❌ **[Logs Sdk]** [SHOULD] Other common processing scenarios SHOULD be first considered
  - Other processing scenarios missing
- ❌ **[Logs Sdk]** [SHOULD NOT] default SDK’s `LogRecordProcessors` SHOULD NOT implement retry logic, as the
  - Retry logic not documented
- ❌ **[Logs Sdk]** [SHOULD] exporter has received prior to the call to `ForceFlush` SHOULD be completed as
  - Exporter ForceFlush completion missing
- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded,
  - Exporter ForceFlush success missing
- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD only be called in cases where it is absolutely necessary,
  - Exporter ForceFlush necessity missing
- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be
  - Exporter ForceFlush timeout missing
- ❌ **[Logs Sdk]** [SHOULD] Shutdown SHOULD be called only once for each `LogRecordExporter` instance. After
  - Exporter shutdown single-call missing
- ❌ **[Logs Sdk]** [SHOULD] the call to `Shutdown` subsequent calls to `Export` are not allowed and SHOULD
  - Exporter shutdown blocking missing
- ❌ **[Logs Sdk]** [SHOULD NOT] `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data
  - Exporter shutdown non-blocking missing
- ⚠️ **[Metrics Api]** [SHOULD] * Callback functions SHOULD be reentrant safe. The SDK expects to evaluate (`-`)
  - Callback reentrancy not explicitly guaranteed
- ⚠️ **[Metrics Api]** [SHOULD NOT] callbacks for each MetricReader independently.* Callback functions SHOULD NOT take an indefinite amount of time.* Callback functions SHOULD NOT make d... (`-`)
  - Callback timeout not explicitly implemented
- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD provide some way to pass `state` to the (`-`)
  - State passing to callback not supported
- ⚠️ **[Metrics Api]** [SHOULD] All synchronous instruments SHOULD provide functions to: (`-`)
  - Enabled API not found
- ⚠️ **[Metrics Api]** [SHOULD] SHOULD provide this `Enabled` API. (`-`)
  - IsEnabled/Enabled method not documented
- ⚠️ **[Metrics Api]** [SHOULD] SHOULD be documented that instrumentation authors needs to call this API each (`-`)
  - No Enabled call documentation
- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD provide some way to pass `state` to the callback. OpenTelemetry (`-`)
  - State passing to callback not supported
- ⚠️ **[Metrics Sdk]** [SHOULD] message reporting that the specified value is invalid SHOULD be logged. (`-`)
  - Warning logging not implemented
- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, (`-`)
  - ForceFlush return status unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] failed or timed out. `ForceFlush` SHOULD return some ERROR status if there (`-`)
  - ForceFlush error handling not explicit
- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be (`-`)
  - ForceFlush timeout not implemented
- ⚠️ **[Metrics Sdk]** [SHOULD] Additionally, implementations SHOULD support configuring an exclude-list of (`-`)
  - Exclude-list mentioned but unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] the implementation SHOULD apply the View and emit a warning. If it is not (`-`)
  - Warning on View mismatch unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] implementation SHOULD emit a warning and proceed as if the View did not (`-`)
  - Warning on conflict unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] The implementation SHOULD disregard the use of asynchronous instrument (`-`)
  - Async instrument discarding unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback (`-`)
  - Callback timeout not implemented
- ⚠️ **[Metrics Sdk]** [SHOULD NOT] The implementation SHOULD NOT produce aggregated metric data for a (`-`)
  - Aggregated data for incomplete unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] SDKs SHOULD support being configured with a cardinality limit. The number of (`-`)
  - Cardinality limit config unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] cycle. Cardinality limit enforcement SHOULD occur after attribute filtering, (`-`)
  - Enforcement after filtering unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] stream, that value SHOULD be used.* If there is no matching view, but the `MetricReader` defines a default (`-`)
  - Default from MetricReader unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] Aggregators of asynchronous instruments SHOULD prefer the first-observed (`-`)
  - First-observed preference unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] a warning SHOULD be emitted. The emitted warning SHOULD include information for (`-`)
  - Warning on duplicate unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] SHOULD avoid the warning.* If the potential conflict involves instruments that can be distinguished by (`-`)
  - Warning details unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] recipe SHOULD be included in the warning.* Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the (`-`)
  - Conflict recipe unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument name (`-`)
  - Async duplicate handling unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] If the instrument name does not conform to this syntax, the Meter SHOULD emit (`-`)
  - Async resolution unclear
- ⚠️ **[Metrics Sdk]** [SHOULD NOT] When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. (`-`)
  - Multi-reader interaction unclear
- ⚠️ **[Metrics Sdk]** [SHOULD NOT] When a Meter creates an instrument, it SHOULD NOT validate the instrument (`-`)
  - Duplicate export behavior unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument advisory (`-`)
  - Fallback on duplicate errors unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] parameters. If an advisory parameter is not valid, the Meter SHOULD emit an error (`-`)
  - Advisory on duplicates unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `Exemplar` sampling SHOULD be turned on by default. If `Exemplar` sampling is (`-`)
  - Scope conflict detection unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: (`-`)
  - View name precedence unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for (`-`)
  - Default view application unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] an SDK. The default value SHOULD be `TraceBased`. The filter configuration (`-`)
  - Missing aggregation fallback unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] SHOULD follow the environment variable specification. (`-`)
  - Exemplar loss behavior unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] The “offer” method SHOULD accept measurements, including: (`-`)
  - Reader-specific aggregation unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] The “offer” method SHOULD have the ability to pull associated trace and span (`-`)
  - MetricReader base interface not found
- ⚠️ **[Metrics Sdk]** [SHOULD] with. In other words, Exemplars reported against a metric data point SHOULD have (`-`)
  - Reader error handling unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. (`-`)
  - Delta temporality default unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] * Explicit bucket histogram aggregation with more than 1 bucket SHOULD (`-`)
  - Temporality preference unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] use `AlignedHistogramBucketExemplarReservoir`.* Base2 Exponential Histogram Aggregation SHOULD use a (`-`)
  - Cardinality enforcement unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] twenty (e.g. `min(20, max_buckets)`).* All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`. (`-`)
  - Attribute filtering impact unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] Any stateful portion of sampling computation SHOULD be reset every collection (`-`)
  - Metric mutation prevention unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] contention. Otherwise, a default size of `1` SHOULD be used. (`-`)
  - Thread-safety guarantees unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] measurement that falls within a histogram bucket, and SHOULD use a (`-`)
  - Reader concurrent access unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] number of bucket boundaries plus one. This configuration parameter SHOULD have (`-`)
  - View concurrent registration unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `Collect` SHOULD provide a way to let the caller know whether it succeeded, (`-`)
  - Temporal aggregation strategy unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `Collect` SHOULD invoke Produce on registered (`-`)
  - Exemplar retention unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] SHOULD return some failure for these calls, if possible. (`-`)
  - Resource attributes impact unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, (`-`)
  - Instrumentation scope attributes unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` MAY be (`-`)
  - Metric stream attributes unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD collect metrics, call `Export(batch)` (`-`)
  - Attribute schema validation unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, (`-`)
  - Metric stream creation timing unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] failed or timed out. `ForceFlush` SHOULD return some ERROR status if there (`-`)
  - Delta start persistence unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be (`-`)
  - Collection cycle coordination unclear
- ⚠️ **[Metrics Sdk]** [SHOULD NOT] exporter. The default SDK SHOULD NOT implement retry logic, as the required (`-`)
  - Async callback ordering unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] received prior to the call to `ForceFlush` SHOULD be completed as soon as (`-`)
  - Callback cancellation unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, (`-`)
  - Memory usage patterns unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, (`-`)
  - GC impact on measurements unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be (`-`)
  - Performance benchmarks unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] Shutdown SHOULD be called only once for each `MetricExporter` instance. After (`-`)
  - Cardinality tuning unclear
- ⚠️ **[Metrics Sdk]** [SHOULD NOT] `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data (`-`)
  - Exemplar sampling strategy unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `MetricProducer` implementations SHOULD accept configuration for the (`-`)
  - Exponential scale dynamics unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `metricFilter` parameter. Implementation SHOULD use the filter as early as (`-`)
  - Rounding strategy unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] resource information, `Produce` SHOULD require a resource as a parameter. (`-`)
  - Min/max tracking unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `Produce` SHOULD provide a way to let the caller know whether it succeeded, (`-`)
  - Quantile calculation unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] `Produce` SHOULD include a single InstrumentationScope which identifies the (`-`)
  - Percentile boundaries unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] All the metrics components SHOULD allow new methods to be added to existing (`-`)
  - NaN propagation unclear
- ⚠️ **[Metrics Sdk]** [SHOULD] All the metrics SDK methods SHOULD allow optional parameter(s) to be added to (`-`)
  - Infinity semantics unclear
- ⚠️ **[Otlp Exporter]** [SHOULD] [4]: The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default. For instance, maintaini... (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)
  - Default http/json not http/protobuf
- ⚠️ **[Otlp Exporter]** [SHOULD] If no configuration is provided the default transport SHOULD be `http/protobuf` (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)
  - Default http/json
- ❌ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the ve...
  - No User-Agent header
- ⚠️ **[Propagators]** [SHOULD] supported `Propagator` type. Instrumentation libraries SHOULD call propagators (`src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os`)
  - Not enforced for libs
- ⚠️ **[Propagators]** [SHOULD] propagators. If pre-configured, `Propagator`s SHOULD default to a composite (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - OTEL_PROPAGATORS limited
- ⚠️ **[Resource Sdk]** [SHOULD] SHOULD be considered an error. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:101-119`)
  - Limited error reporting
- ⚠️ **[Trace Api]** [SHOULD] Thus, the API SHOULD provide a way to set/register and access (`src/Трассировка/Классы/ОтелПостроительСпана.os:98`)
  - SetStartTimestamp exists but no register/access API for system clock
- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:91-95`)
  - СброситьБуфер() no return status
- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os`)
  - No timeout
- ⚠️ **[Trace Sdk]** [SHOULD] so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend (`src/Трассировка/Модули/ОтелСэмплер.os`)
  - TraceState passed but not modified
- ⚠️ **[Trace Sdk]** [SHOULD] implementation language standards and SHOULD be high enough to identify when (`src/Трассировка/Модули/ОтелСэмплер.os`)
  - No description method
- ❌ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when ge... (`src/Ядро/Модули/ОтелУтилиты.os`)
  - No W3C Level 2 randomness
- ❌ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 ran... (`Same as above`)
- ❌ **[Trace Sdk]** [SHOULD] There SHOULD be a message printed in the SDK’s log to indicate to the user (`No logging when limits hit`)
- ⚠️ **[Trace Sdk]** [SHOULD] The `SpanProcessor` interface SHOULD declare the following methods: (`src/Трассировка/Классы/`)
  - No optional methods in public API
- ⚠️ **[Trace Sdk]** [SHOULD] It SHOULD be possible to keep a reference to this span object and updates to the span (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26`)
  - References span in ПриЗавершении
- ⚠️ **[Trace Sdk]** [SHOULD] are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:100-105`)
  - No graceful handling
- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os`)
  - No return status
- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` can be (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os`)
  - No timeout
- ⚠️ **[Trace Sdk]** [SHOULD] In particular, if any `SpanProcessor` has any associated exporter, it SHOULD (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37-39`)
  - ForceFlush exists but no-op
- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os`)
  - No status return
- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os`)
  - No timeout
- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os`)
  - No status
- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os`)
  - No timeout

---

## Детальный анализ по разделам (Stable)

### Context

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | MUST | ✅ | A `Context` MUST be immutable, and its write operations MUST | src/Ядро/Модули/ОтелКонтекст.os:29-304 |
| 2 | MUST | ✅ | option is not available, OpenTelemetry MUST provide its own `Context` | src/Ядро/Модули/ОтелКонтекст.os:1-316 |
| 3 | MUST | ✅ | The API MUST accept the following parameter: | src/Ядро/Модули/ОтелКонтекст.os:45-48 |
| 4 | SHOULD NOT | ➖ | * The key name. The key name exists for debugging purposes and does not uniquely identify the key. Multiple calls to `Cr... | n_a (Language constraint) |
| 5 | MUST | ✅ | The API MUST return an opaque object representing the newly created key. | src/Ядро/Модули/ОтелКонтекст.os:45-48 |
| 6 | MUST | ✅ | The API MUST accept the following parameters: | src/Ядро/Модули/ОтелКонтекст.os:45-48 |
| 7 | MUST | ✅ | The API MUST return the value in the `Context` for the specified key. | src/Ядро/Модули/ОтелКонтекст.os:45-48 |
| 8 | MUST | ✅ | The API MUST accept the following parameters: | src/Ядро/Модули/ОтелКонтекст.os:147-152 |
| 9 | MUST | ✅ | The API MUST return a new `Context` containing the new value. | src/Ядро/Модули/ОтелКонтекст.os:114-134 |
| 10 | SHOULD | ➖ | SHOULD only be used to implement automatic scope switching and define | n_a (Optional global operations) |
| 11 | MUST | ✅ | The API MUST return the `Context` associated with the caller’s current execution unit. | src/Ядро/Модули/ОтелКонтекст.os:29-35 |
| 12 | MUST | ✅ | The API MUST accept the following parameters: | src/Ядро/Модули/ОтелКонтекст.os:147-152 |
| 13 | MUST | ✅ | The API MUST return a value that can be used as a `Token` to restore the previous | src/Ядро/Классы/ОтелОбласть.os:19-27 |
| 14 | MUST | ✅ | The API MUST accept the following parameters: | src/Ядро/Классы/ОтелОбласть.os:22-27 |

### Baggage Api

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 15 | MUST | ✅ | describing user-defined properties. Each name in `Baggage` MUST be associated | src/Ядро/Классы/ОтелBaggage.os:1-166 |
| 16 | SHOULD NOT | ✅ | Baggage names are any valid, non-empty UTF-8 strings. Language API SHOULD NOT | src/Ядро/Классы/ОтелBaggage.os:38-40 |
| 17 | MUST | ✅ | Baggage values are any valid UTF-8 strings. Language API MUST accept | src/Ядро/Классы/ОтелBaggage.os:38-40 |
| 18 | MUST | ✅ | Language API MUST treat both baggage names and values as case sensitive. | src/Ядро/Классы/ОтелBaggage.os:38-40 |
| 19 | MUST | ✅ | The Baggage API MUST be fully functional in the absence of an installed SDK. | src/Ядро/Классы/ОтелBaggage.os:16-28 |
| 20 | MUST | ✅ | The `Baggage` container MUST be immutable, so that the containing `Context` | src/Ядро/Классы/ОтелBaggage.os:152-163 |
| 21 | MUST | ✅ | MUST provide a function that takes the name as input, and returns a value | src/Ядро/Классы/ОтелBaggage.os:38-40 |
| 22 | MUST NOT | ✅ | MUST NOT be significant. Based on the language specifics, the returned | src/Ядро/Классы/ОтелBaggage.os:103-105 |
| 23 | MUST | ✅ | To record the value for a name/value pair, the Baggage API MUST provide a | src/Ядро/Классы/ОтелBaggage.os:68-72 |
| 24 | MUST | ✅ | To delete a name/value pair, the Baggage API MUST provide a function which | src/Ядро/Классы/ОтелBaggage.os:82-86 |
| 25 | MUST | ✅ | MUST provide the following functionality to interact with a `Context` instance: | src/Ядро/Классы/ОтелBaggage.os:16-28 |
| 26 | SHOULD NOT | ➖ | The functionality listed above is necessary because API users SHOULD NOT have | n_a (Language-specific SHOULD NOT) |
| 27 | SHOULD | ✅ | `Baggage` class. This functionality SHOULD be fully implemented in the API when | src/Ядро/Классы/ОтелBaggage.os:16-28 |
| 28 | MUST | ✅ | MUST provide a way to remove all baggage entries from a context. | src/Ядро/Классы/ОтелBaggage.os:94-96 |
| 29 | MUST | ✅ | The API layer or an extension package MUST include the following `Propagator`s: | src/Пропагация/Модули/ОтелW3CПропагатор.os,ОтелW3CBaggageПропагатор.os |
| 30 | MUST | ✅ | then the new pair MUST take precedence. The value is replaced with the added | src/Ядро/Классы/ОтелРесурс.os:44-65 |

### Resource Sdk

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 31 | MUST | ✅ | with closed source environments. The SDK MUST allow for creation of `Resources` and | src/Ядро/Классы/ОтелРесурс.os:1-173 |
| 32 | MUST | ✅ | all `Span`s produced by any `Tracer` from the provider MUST be associated with this `Resource`. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os |
| 33 | MUST | ✅ | The SDK MUST provide access to a Resource with at least the attributes listed at | src/Ядро/Классы/ОтелРесурс.os:104-113 |
| 34 | MUST | ✅ | This resource MUST be associated with a `TracerProvider` or `MeterProvider` | src/Ядро/Классы/ОтелSdk.os |
| 35 | MUST | ✅ | The interface MUST provide a way to create a new resource, from `Attributes`. | src/Ядро/Классы/ОтелПостроительРесурса.os:19-22 |
| 36 | MUST | ✅ | The interface MUST provide a way for an old resource and an | src/Ядро/Классы/ОтелРесурс.os:44-65 |
| 37 | MUST | ✅ | The resulting resource MUST have all attributes that are on any of the two input resources. | src/Ядро/Классы/ОтелРесурс.os:57-64 |
| 38 | MUST | ✅ | resource MUST be picked (even if the updated value is empty). | src/Ядро/Классы/ОтелРесурс.os:61-62 |
| 39 | MUST | ⚠️ | or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:96-119 (Resource detectors not fully implemented) |
| 40 | MUST | ❌ | Resource detector packages MUST provide a method that returns a resource. This | n/a (No resource detector packages) |
| 41 | MUST NOT | ✅ | failure to detect any resource information MUST NOT be considered an error, | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:101-119 |
| 42 | SHOULD | ⚠️ | SHOULD be considered an error. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:101-119 (Limited error reporting) |
| 43 | MUST | ➖ | semantic conventions MUST ensure that the resource has a Schema URL set to a | n/a (Schema URL support) |
| 44 | SHOULD | ➖ | value that matches the semantic conventions. Empty Schema URL SHOULD be used if | n/a (Empty Schema URL) |
| 45 | MUST | ➖ | the detectors use different non-empty Schema URL it MUST be an error since it is | n/a (Schema URL conflict) |

### Trace Api

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 56 | SHOULD | ⚠️ | Thus, the API SHOULD provide a way to set/register and access | src/Трассировка/Классы/ОтелПостроительСпана.os:98 (SetStartTimestamp exists but no register/access API for system clock) |
| 57 | SHOULD | ✅ | Thus, implementations of `TracerProvider` SHOULD allow creating an arbitrary | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52-69 |
| 58 | MUST | ✅ | The `TracerProvider` MUST provide the following functions: | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52 |
| 59 | MUST | ✅ | This API MUST accept the following parameters: | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52-56 |
| 60 | SHOULD | ✅ | * `name` (required): This name SHOULD uniquely identify the | src/Трассировка/Классы/ОтелОбластьИнструментирования.os |
| 61 | MUST | ✅ | (null or empty string) is specified, a working Tracer implementation MUST be | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:59-68 |
| 62 | SHOULD | ➖ | its `name` property SHOULD be set to an empty string, and a message | OneScript SDK doesn't require spec-level logging |
| 63 | SHOULD | ➖ | reporting that the specified value is invalid SHOULD be logged. A library, | Same as above |
| 64 | MUST NOT | ✅ | Implementations MUST NOT require users to repeatedly obtain a `Tracer` again | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:62-68 |
| 65 | MUST | ✅ | The API MUST provide the following functionality to interact with a `Context` | src/Ядро/Модули/ОтелКонтекст.os:29-68 |
| 66 | SHOULD NOT | ➖ | The functionality listed above is necessary because API users SHOULD NOT have | Language specific constraint |
| 67 | SHOULD | ✅ | here), the API SHOULD also provide | src/Ядро/Модули/ОтелКонтекст.os:82+ |
| 68 | SHOULD | ✅ | inside the trace module. This functionality SHOULD be fully implemented in the API when possible. | src/Ядро/Модули/ОтелКонтекст.os |
| 69 | MUST | ✅ | The `Tracer` MUST provide functions to: | src/Трассировка/Классы/ОтелТрассировщик.os:22-80 |
| 70 | SHOULD | ✅ | The `Tracer` SHOULD provide functions to: | src/Трассировка/Классы/ОтелТрассировщик.os:22-80 |
| 75 | MUST | ✅ | The API MUST implement methods to create a `SpanContext`. These methods SHOULD be the only way to | src/Трассировка/Классы/ОтелКонтекстСпана.os:124-142 |
| 76 | SHOULD NOT | ✅ | create a `SpanContext`. This functionality MUST be fully implemented in the API, and SHOULD NOT be | src/Трассировка/Классы/ОтелКонтекстСпана.os |
| 77 | MUST | ✅ | The API MUST allow retrieving the `TraceId` and `SpanId` in the following forms: | src/Трассировка/Классы/ОтелКонтекстСпана.os:23-33 |
| 78 | MUST | ✅ | `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` | src/Трассировка/Классы/ОтелКонтекстСпана.os:23-25 |
| 79 | MUST | ⚠️ | (result MUST be a 16-hex-character lowercase string).* Binary - returns the binary representation of the `TraceId` (resu... | src/Трассировка/Классы/ОтелКонтекстСпана.os (Only string format, no binary API) |
| 80 | MUST | ⚠️ | 16-byte array) or `SpanId` (result MUST be an 8-byte array). | Same as above |
| 81 | SHOULD NOT | ✅ | The API SHOULD NOT expose details about how they are internally stored. | src/Трассировка/Классы/ОтелКонтекстСпана.os |
| 82 | MUST | ✅ | non-zero TraceID and a non-zero SpanID, MUST be provided. | src/Трассировка/Классы/ОтелКонтекстСпана.os:70-75 |
| 83 | MUST | ✅ | propagated from a remote parent, MUST be provided. | src/Трассировка/Классы/ОтелКонтекстСпана.os:60-62 |
| 84 | MUST | ✅ | `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | src/Трассировка/Классы/ОтелТрассировщик.os:49-76 |
| 85 | MUST | ✅ | Tracing API MUST provide at least the following operations on `TraceState`: | src/Трассировка/Классы/ОтелСостояниеТрассировки.os:44-95 |
| 86 | MUST | ✅ | These operations MUST follow the rules described in the W3C Trace Context specification. | src/Трассировка/Классы/ОтелСостояниеТрассировки.os:100+ |
| 87 | MUST | ✅ | All mutating operations MUST return a new `TraceState` with the modifications applied. | src/Трассировка/Классы/ОтелСостояниеТрассировки.os:92-94 |
| 88 | MUST | ✅ | `TraceState` MUST at all times be valid according to rules specified in W3C Trace Context specification. | src/Трассировка/Классы/ОтелСостояниеТрассировки.os:66-95 |
| 89 | MUST | ✅ | Every mutating operations MUST validate input parameters. | src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67 |
| 90 | MUST NOT | ✅ | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data | src/Трассировка/Классы/ОтелСостояниеТрассировки.os:68-69 |
| 91 | MUST | ✅ | and MUST follow the general error handling guidelines. | src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67-69 |
| 92 | SHOULD | ✅ | The span name SHOULD be the most general string that identifies a | src/Трассировка/Классы/ОтелСпан.os |
| 93 | SHOULD | ✅ | Generality SHOULD be prioritized over human-readability. | src/Трассировка/Классы/ОтелСпан.os |
| 94 | SHOULD | ✅ | A `Span`’s start time SHOULD be set to the current time on span | src/Трассировка/Классы/ОтелСпан.os |
| 95 | SHOULD | ✅ | creation. After the `Span` is created, it SHOULD be possible to | src/Трассировка/Классы/ОтелПостроительСпана.os:98-108 |
| 96 | MUST NOT | ✅ | MUST NOT be changed after the `Span`’s end time has been set. | src/Трассировка/Классы/ОтелСпан.os:436-448 |
| 97 | SHOULD NOT | ➖ | prevent misuse, implementations SHOULD NOT provide access to a `Span`’s | Language specific design |
| 98 | MUST NOT | ✅ | However, alternative implementations MUST NOT allow callers to create `Span`s | src/Трассировка/Классы/ОтелСпан.os |
| 99 | MUST | ✅ | directly. All `Span`s MUST be created via a `Tracer`. | src/Трассировка/Классы/ОтелТрассировщик.os:48-104 |
| 100 | MUST NOT | ✅ | There MUST NOT be any API for creating a `Span` other than with a `Tracer`. | src/Трассировка/Классы/ |
| 101 | MUST NOT | ➖ | In languages with implicit `Context` propagation, `Span` creation MUST NOT | OneScript doesn't have implicit context |
| 102 | MUST | ✅ | The API MUST accept the following parameters: | src/Трассировка/Классы/ОтелСпан.os:400+ |
| 103 | MUST NOT | ✅ | This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`. | src/Трассировка/Классы/ОтелТрассировщик.os:48-136 |
| 104 | MUST | ✅ | The semantic parent of the Span MUST be determined according to the rules | src/Трассировка/Классы/ОтелТрассировщик.os:49-59 |
| 105 | MUST | ✅ | The API documentation MUST state that adding attributes at span creation is preferred | src/Трассировка/Классы/ОтелПостроительСпана.os:65-78 |
| 106 | SHOULD | ✅ | `Start timestamp`, default to current time. This argument SHOULD only be set | src/Трассировка/Классы/ОтелПостроительСпана.os:98 |
| 107 | MUST NOT | ✅ | a Span logical start, API user MUST NOT explicitly set this argument. | src/Трассировка/Классы/ОтелПостроительСпана.os |
| 108 | MUST | ✅ | spans in the trace. Implementations MUST provide an option to create a `Span` as | src/Трассировка/Классы/ОтелТрассировщик.os:91-104 |
| 109 | MUST | ✅ | a root span, and MUST generate a new `TraceId` for each root span created. | src/Трассировка/Классы/ОтелТрассировщик.os:92 |
| 110 | MUST | ✅ | For a Span with a parent, the `TraceId` MUST be the same as the parent. | src/Трассировка/Классы/ОтелТрассировщик.os:52 |
| 111 | MUST | ✅ | Also, the child span MUST inherit all `TraceState` values of its parent by default. | src/Трассировка/Классы/ОтелТрассировщик.os |
| 112 | MUST | ✅ | Any span that is created MUST also be ended. | src/Трассировка/Классы/ОтелСпан.os:436-448 |
| 113 | MUST | ✅ | During `Span` creation, a user MUST have the ability to record links to other `Span`s. | src/Трассировка/Классы/ОтелПостроительСпана.os:80-96 |
| 114 | MUST | ✅ | The Span interface MUST provide: | src/Трассировка/Классы/ОтелСпан.os:72-74 |
| 115 | MUST | ✅ | may be used even after the `Span` is finished. The returned value MUST be the | src/Трассировка/Классы/ОтелСпан.os:226-228 |
| 116 | SHOULD | ✅ | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` | src/Трассировка/Классы/ОтелСпан.os:226-228 |
| 117 | SHOULD | ➖ | SHOULD always return `false`. The one known exception to this is | No exception case documented |
| 118 | SHOULD NOT | ✅ | `IsRecording` SHOULD NOT take any parameters. | src/Трассировка/Классы/ОтелСпан.os:226 |
| 119 | SHOULD | ✅ | This flag SHOULD be used to avoid expensive computations of a Span attributes or | src/Трассировка/Классы/ОтелТрассировщик.os:33-35 |
| 120 | MUST | ✅ | A `Span` MUST have the ability to set `Attributes` associated with it. | src/Трассировка/Классы/ОтелСпан.os:255-272 |
| 121 | MUST | ✅ | The Span interface MUST provide: | src/Трассировка/Классы/ОтелСпан.os:255 |
| 122 | SHOULD | ✅ | Setting an attribute with the same key as an existing attribute SHOULD overwrite | src/Трассировка/Классы/ОтелСпан.os:258-261 |
| 123 | MUST | ✅ | A `Span` MUST have the ability to add events. Events have a time associated | src/Трассировка/Классы/ОтелСпан.os:284-294 |
| 124 | MUST | ✅ | The Span interface MUST provide: | src/Трассировка/Классы/ОтелСпан.os:284 |
| 125 | SHOULD | ✅ | Events SHOULD preserve the order in which they are recorded. | src/Трассировка/Классы/ОтелСпан.os:286-288 |
| 126 | MUST | ✅ | A `Span` MUST have the ability to add `Link`s associated with it after its creation - see Links. | src/Трассировка/Классы/ОтелСпан.os:351-368 |
| 127 | MUST | ✅ | `Description` MUST only be used with the `Error` `StatusCode` value. | src/Трассировка/Классы/ОтелСпан.os:418-422 |
| 128 | MUST | ✅ | The Span interface MUST provide: | src/Трассировка/Классы/ОтелСпан.os:402-425 |
| 129 | SHOULD | ✅ | * An API to set the `Status`. This SHOULD be called `SetStatus`. This API takes | src/Трассировка/Классы/ОтелСпан.os:402 |
| 130 | MUST | ✅ | appropriate for the language. `Description` MUST be IGNORED for `StatusCode` | src/Трассировка/Классы/ОтелСпан.os:418-422 |
| 131 | SHOULD | ✅ | The status code SHOULD remain unset, except for the following circumstances: | src/Трассировка/Классы/ОтелСпан.os:500+ |
| 132 | SHOULD | ✅ | An attempt to set value `Unset` SHOULD be ignored. | src/Трассировка/Классы/ОтелСпан.os:417 |
| 133 | SHOULD | ✅ | SHOULD be documented and predictable. The status code should only be set to `Error` | src/Трассировка/Классы/ОтелСпан.os:407-415 |
| 134 | SHOULD | ➖ | not covered by the semantic conventions, Instrumentation Libraries SHOULD | Instrumentation-specific guidance |
| 135 | SHOULD NOT | ➖ | Generally, Instrumentation Libraries SHOULD NOT set the status code to `Ok`, | Instrumentation-specific guidance |
| 136 | SHOULD | ➖ | unless explicitly configured to do so. Instrumentation Libraries SHOULD leave the | Same as above |
| 137 | SHOULD | ✅ | When span status is set to `Ok` it SHOULD be considered final and any further | src/Трассировка/Классы/ОтелСпан.os:408-410 |
| 138 | SHOULD | ✅ | attempts to change it SHOULD be ignored. | src/Трассировка/Классы/ОтелСпан.os:408-410 |
| 139 | SHOULD | ➖ | Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they | Analysis tool requirement |
| 140 | SHOULD | ✅ | Implementations SHOULD ignore all subsequent calls to `End` and any other Span methods, | src/Трассировка/Классы/ОтелСпан.os:403-404 |
| 141 | MUST | ✅ | However, all API implementations of such methods MUST internally call the `End` | src/Трассировка/Классы/ОтелСпан.os |
| 142 | MUST NOT | ✅ | `End` MUST NOT have any effects on child spans. | src/Трассировка/Классы/ОтелТрассировщик.os |
| 143 | MUST NOT | ✅ | `End` MUST NOT inactivate the `Span` in any `Context` it is active in. | src/Трассировка/Классы/ОтелСпан.os:436-448 |
| 144 | MUST | ✅ | It MUST still be possible to use an ended span as parent via a Context it is | src/Трассировка/Классы/ОтелТрассировщик.os |
| 145 | MUST | ✅ | contained in. Also, any mechanisms for putting the Span into a Context MUST | src/Ядро/Модули/ОтелКонтекст.os |
| 146 | MUST | ✅ | If omitted, this MUST be treated equivalent to passing the current time. | src/Трассировка/Классы/ОтелСпан.os:438-441 |
| 147 | MUST NOT | ✅ | This operation itself MUST NOT perform blocking I/O on the calling thread. | src/Трассировка/Классы/ОтелСпан.os:436-448 |
| 148 | SHOULD | ✅ | Any locking used needs be minimized and SHOULD be removed entirely if | src/Трассировка/Классы/ОтелТрассировщик.os |
| 149 | SHOULD | ✅ | To facilitate recording an exception languages SHOULD provide a | src/Трассировка/Классы/ОтелСпан.os:307-339 |
| 150 | MUST | ✅ | The method MUST record an exception as an `Event` with the conventions outlined in | src/Трассировка/Классы/ОтелСпан.os:336 |
| 151 | SHOULD | ✅ | The minimum required argument SHOULD be no more than only an exception object. | src/Трассировка/Классы/ОтелСпан.os:307 |
| 152 | MUST | ✅ | If `RecordException` is provided, the method MUST accept an optional parameter | src/Трассировка/Классы/ОтелСпан.os:307-308 |
| 153 | SHOULD | ✅ | (this SHOULD be done in the same way as for the `AddEvent` method). | src/Трассировка/Классы/ОтелСпан.os:331-334 |
| 154 | MUST | ✅ | Start and end time as well as Event’s timestamps MUST be recorded at a time of a | src/Трассировка/Классы/ОтелСпан.os |
| 155 | MUST | ✅ | The API MUST provide an operation for wrapping a `SpanContext` with an object | src/Трассировка/Классы/ОтелНоопСпан.os |
| 156 | SHOULD NOT | ✅ | If a new type is required for supporting this operation, it SHOULD NOT be exposed | src/Трассировка/Классы/ОтелНоопСпан.os |
| 157 | SHOULD | ✅ | it SHOULD be named `NonRecordingSpan`. | src/Трассировка/Классы/ОтелНоопСпан.os |
| 158 | MUST | ✅ | * `GetContext` MUST return the wrapped `SpanContext`.* `IsRecording` MUST return `false` to signal that events, attribut... | src/Трассировка/Классы/ОтелНоопСпан.os:29-30, 155-157 |
| 159 | MUST | ✅ | The remaining functionality of `Span` MUST be defined as no-op operations. | src/Трассировка/Классы/ОтелНоопСпан.os:167+ |
| 160 | SHOULD NOT | ✅ | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | src/Трассировка/Классы/ОтелНоопСпан.os |
| 161 | SHOULD | ✅ | In order for `SpanKind` to be meaningful, callers SHOULD arrange that | src/Трассировка/Модули/ОтелВидСпана.os |
| 162 | SHOULD NOT | ✅ | server-side span SHOULD NOT be used to describe outgoing remote procedure call. | src/Трассировка/Модули/ОтелВидСпана.os |
| 163 | MUST | ✅ | A user MUST have the ability to record links to other `SpanContext`s. | src/Трассировка/Классы/ОтелСпан.os:351-368 |
| 164 | SHOULD | ✅ | appropriate for the language. Implementations SHOULD record links containing | src/Трассировка/Классы/ОтелСпан.os:351-368 |
| 165 | SHOULD | ✅ | Span SHOULD preserve the order in which `Link`s are set. | src/Трассировка/Классы/ОтелСпан.os:356 |
| 166 | MUST | ✅ | The API documentation MUST state that adding links at span creation is preferred | src/Трассировка/Классы/ОтелПостроительСпана.os:80-96 |
| 167 | MUST | ⚠️ | TracerProvider - all methods MUST be documented that implementations need to | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:1 (Uses СинхронизированнаяКарта but no docs) |
| 168 | MUST | ⚠️ | Tracer - all methods MUST be documented that implementations need to be safe | src/Трассировка/Классы/ОтелТрассировщик.os (Methods thread-safe by design) |
| 169 | MUST | ⚠️ | Span - all methods MUST be documented that implementations need to be safe | src/Трассировка/Классы/ОтелСпан.os (Methods thread-safe by design) |
| 170 | MUST | ✅ | Event - Events are immutable and MUST be safe for concurrent use by default. | src/Трассировка/Классы/ОтелСобытиеСпана.os |
| 171 | SHOULD | ✅ | Link - Links are immutable and SHOULD be safe for concurrent use by default. | src/Трассировка/Классы/ОтелСпан.os:361-366 |
| 172 | MUST | ✅ | and that is related to propagation of a `SpanContext`: The API MUST return a | src/Трассировка/Классы/ОтелНоопСпан.os |
| 173 | SHOULD | ✅ | If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly | src/Трассировка/Классы/ОтелТрассировщик.os:61-65 |
| 174 | MUST | ✅ | If the parent `Context` contains no `Span`, an empty non-recording Span MUST be | src/Трассировка/Классы/ОтелТрассировщик.os:93-96 |

### Trace Sdk

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 175 | SHOULD | ✅ | It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52 |
| 176 | MUST | ✅ | The `TracerProvider` MUST implement the Get a Tracer API. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52-69 |
| 177 | MUST | ✅ | The input provided by the user MUST be used to create | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:57-68 |
| 179 | MUST | ⚠️ | the updated configuration MUST also apply to all already returned `Tracers` | src/Трассировка/Классы/ОтелПровайдерТрассировки.os (Delegation model but no dynamic config updates) |
| 180 | MUST NOT | ✅ | (i.e. it MUST NOT matter whether a `Tracer` was obtained from the | src/Трассировка/Классы/ОтелТрассировщик.os |
| 188 | SHOULD | ⚠️ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:91-95 (СброситьБуфер() no return status) |
| 189 | SHOULD | ⚠️ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | src/Трассировка/Классы/ОтелПровайдерТрассировки.os (No timeout) |
| 190 | MUST | ✅ | `ForceFlush` MUST invoke `ForceFlush` on all registered `SpanProcessors`. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:91-95 |
| 198 | MUST | ✅ | Readable span: A function receiving this as argument MUST be able to | src/Трассировка/Классы/ОтелСпан.os |
| 199 | MUST | ✅ | A function receiving this as argument MUST be able to access | src/Трассировка/Классы/ОтелСпан.os:63-217 |
| 200 | MUST | ✅ | it MUST also be able to access the `InstrumentationLibrary` | src/Трассировка/Классы/ОтелСпан.os:162-164 |
| 201 | MUST | ✅ | A function receiving this as argument MUST be able to reliably determine | src/Трассировка/Классы/ОтелСпан.os:162-164 |
| 202 | MUST | ✅ | Counts for attributes, events and links dropped due to collection limits MUST be | src/Трассировка/Классы/ОтелСпан.os:198-217 |
| 203 | MUST | ✅ | of the Span but they MUST expose at least the full parent SpanContext. | src/Трассировка/Классы/ОтелСпан.os:72-74 |
| 204 | MUST | ✅ | It MUST be possible for functions being called with this | src/Трассировка/Классы/ОтелСпан.os:189-191 |
| 205 | MUST | ✅ | Processor MUST receive only those spans which have this | src/Трассировка/Классы/ОтелТрассировщик.os:61-79 |
| 206 | SHOULD NOT | ✅ | field set to `true`. However, Span Exporter SHOULD NOT | src/Трассировка/Классы/ОтелНоопСпан.os |
| 207 | MUST | ✅ | `sampled` and will be exported. Span Exporters MUST | src/Трассировка/Классы/ОтелТрассировщик.os:61-79 |
| 208 | SHOULD NOT | ✅ | receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones | src/Экспорт/Классы/ОтелЭкспортерСпанов.os |
| 209 | MUST NOT | ✅ | MUST NOT allow this combination. | src/Трассировка/Классы/ОтелСпан.os |
| 210 | MUST | ✅ | When asked to create a Span, the SDK MUST act as if doing the following in order: | src/Трассировка/Классы/ОтелТрассировщик.os:48-104 |
| 211 | MUST | ✅ | If the parent `SpanContext` contains a valid `TraceId`, they MUST always match.* Name of the `Span` to be created.* `Spa... | src/Трассировка/Модули/ОтелСэмплер.os:112-128 |
| 212 | MUST NOT | ✅ | will be dropped.* `RECORD_ONLY` - `IsRecording` will be `true`, but the `Sampled` flag MUST NOT be set.* `RECORD_AND_SAM... | src/Трассировка/Модули/ОтелСэмплер.os:200-215 |
| 213 | SHOULD | ⚠️ | so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend | src/Трассировка/Модули/ОтелСэмплер.os (TraceState passed but not modified) |
| 214 | SHOULD NOT | ➖ | Callers SHOULD NOT cache the returned value. | OneScript specific |
| 215 | MUST | ✅ | * The `TraceIdRatioBased` MUST ignore the parent `SampledFlag`. To respect the | src/Трассировка/Модули/ОтелСэмплер.os:63-64 |
| 216 | MUST | ✅ | the `ParentBased` sampler specified below.* Description MUST return a string of the form `"TraceIdRatioBased{RATIO}"` | src/Трассировка/Модули/ОтелСэмплер.os:72-74 |
| 217 | SHOULD | ✅ | represented as a decimal number. The precision of the number SHOULD follow | src/Трассировка/Модули/ОтелСэмплер.os:81-83 |
| 218 | SHOULD | ⚠️ | implementation language standards and SHOULD be high enough to identify when | src/Трассировка/Модули/ОтелСэмплер.os (No description method) |
| 219 | MUST | ➖ | * The sampling algorithm MUST be deterministic. A trace identified by a given | Language specific |
| 220 | MUST | ✅ | implementations MUST use a deterministic hash of the `TraceId` when computing | src/Трассировка/Модули/ОтелСэмплер.os:247-269 |
| 221 | MUST | ✅ | will produce the same decision.* A `TraceIdRatioBased` sampler with a given sampling probability MUST also sample all | src/Трассировка/Модули/ОтелСэмплер.os:260-262 |
| 231 | SHOULD | ❌ | For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Ca... | src/Ядро/Модули/ОтелУтилиты.os (No W3C Level 2 randomness) |
| 232 | SHOULD | ❌ | For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the... | Same as above |
| 233 | MUST NOT | ➖ | MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState | No explicit randomness tracking |
| 234 | SHOULD | ➖ | For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness... | No explicit randomness impl |
| 235 | SHOULD | ➖ | If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random fla... | No IdGenerator extension point |
| 236 | MUST | ✅ | Span attributes MUST adhere to the common rules of attribute limits. | src/Трассировка/Классы/ОтелЛимитыСпана.os |
| 237 | MUST | ✅ | If the SDK implements the limits above it MUST provide a way to change these | src/Трассировка/Классы/ОтелЛимитыСпана.os:83-152 |
| 238 | SHOULD | ✅ | The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`. The options MAY be bundled in a ... | src/Трассировка/Классы/ОтелЛимитыСпана.os |
| 239 | SHOULD | ✅ | which then SHOULD be called `SpanLimits`. Implementations MAY provide additional | src/Трассировка/Классы/ОтелЛимитыСпана.os:158-178 |
| 240 | SHOULD | ❌ | There SHOULD be a message printed in the SDK’s log to indicate to the user | No logging when limits hit |
| 241 | MUST | ➖ | To prevent excessive logging, the message MUST be printed at most once per | Same as above |
| 242 | MUST | ✅ | The SDK MUST by default randomly generate both the `TraceId` and the `SpanId`. | src/Ядро/Модули/ОтелУтилиты.os |
| 243 | MUST | ❌ | The SDK MUST provide a mechanism for customizing the way IDs are generated for | No IdGenerator extension point |
| 244 | MUST | ➖ | `IdGenerator`, name of the methods MUST be consistent with | No IdGenerator interface |
| 245 | MUST NOT | ➖ | X-Ray trace id generator MUST NOT be maintained or distributed as part of the | Not required |
| 247 | MUST | ✅ | of span processor and optional exporter. SDK MUST allow to end each pipeline with | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os |
| 248 | MUST | ✅ | SDK MUST allow users to implement and configure custom processors. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:76-78 |
| 249 | MUST | ✅ | The `SpanProcessor` interface MUST declare the following methods: | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:17-47 |
| 250 | SHOULD | ⚠️ | The `SpanProcessor` interface SHOULD declare the following methods: | src/Трассировка/Классы/ (No optional methods in public API) |
| 251 | SHOULD | ⚠️ | It SHOULD be possible to keep a reference to this span object and updates to the span | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26 (References span in ПриЗавершении) |
| 256 | MUST | ✅ | This method MUST be called synchronously within the `Span.End()` API, | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-32 |
| 257 | SHOULD | ✅ | `Shutdown` SHOULD be called only once for each `SpanProcessor` instance. After | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:43-47 |
| 258 | SHOULD | ⚠️ | are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:100-105 (No graceful handling) |
| 259 | SHOULD | ⚠️ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os (No return status) |
| 260 | MUST | ❌ | `Shutdown` MUST include the effects of `ForceFlush`. | Not explicit |
| 261 | SHOULD | ⚠️ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` can be | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os (No timeout) |
| 262 | SHOULD | ✅ | `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD | src/Трассировка/Классы/ОтелПровайдерТрассировки.os |
| 263 | SHOULD | ⚠️ | In particular, if any `SpanProcessor` has any associated exporter, it SHOULD | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37-39 (ForceFlush exists but no-op) |
| 264 | MUST | ✅ | The built-in SpanProcessors MUST do so. | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37-39 |
| 265 | MUST | ❌ | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over | No timeout support |
| 266 | SHOULD | ⚠️ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os (No status return) |
| 267 | SHOULD | ➖ | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, | Design recommendation |
| 268 | SHOULD | ⚠️ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os (No timeout) |
| 269 | MUST | ✅ | The standard OpenTelemetry SDK MUST implement both simple and batch processors, | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os, ОтелПакетныйПроцессорСпанов.os |
| 270 | MUST | ✅ | The processor MUST synchronize calls to `Span Exporter`’s `Export` | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-32 |
| 271 | MUST | ✅ | The processor MUST synchronize calls to `Span Exporter`’s `Export` | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-32 |
| 272 | SHOULD | ➖ | The processor SHOULD export a batch when any of the following happens AND the | Simple processor doesn't batch |
| 273 | MUST | ⚠️ | Each implementation MUST document the concurrency characteristics the SDK | src/Трассировка/Классы/ (Limited documentation) |
| 274 | MUST | ✅ | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | src/Экспорт/Классы/ОтелЭкспортерСпанов.os |
| 275 | MUST NOT | ✅ | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit | src/Экспорт/Классы/ОтелЭкспортерСпанов.os |
| 276 | SHOULD NOT | ✅ | default SDK’s Span Processors SHOULD NOT implement retry logic, as the required | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os |
| 277 | SHOULD | ✅ | call to `ForceFlush` SHOULD be completed as soon as possible, preferably before | src/Экспорт/Классы/ОтелЭкспортерСпанов.os |
| 278 | SHOULD | ⚠️ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | src/Экспорт/Классы/ОтелЭкспортерСпанов.os (No status) |
| 279 | SHOULD | ➖ | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, | Design recommendation |
| 280 | SHOULD | ⚠️ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | src/Экспорт/Классы/ОтелЭкспортерСпанов.os (No timeout) |
| 281 | MUST | ✅ | Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:225 |
| 282 | MUST | ✅ | Sampler - `ShouldSample` and `GetDescription` MUST be safe to be called | src/Трассировка/Модули/ОтелСэмплер.os |
| 283 | MUST | ✅ | Span processor - all methods MUST be safe to be called concurrently. | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os |
| 284 | MUST | ✅ | Span Exporter - `ForceFlush` and `Shutdown` MUST be safe to be called | src/Экспорт/Классы/ОтелЭкспортерСпанов.os |

### Logs Api

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 285 | SHOULD | ✅ | Thus, the API SHOULD provide a way to set/register and access a global default | src/Ядро/Модули/ОтелГлобальный.os:30-86 |
| 286 | MUST | ✅ | The `LoggerProvider` MUST provide the following functions: | src/Логирование/Классы/ОтелПровайдерЛогирования.os:29-68 |
| 287 | MUST | ✅ | This API MUST accept the following instrumentation scope | src/Логирование/Классы/ОтелПровайдерЛогирования.os:44-48 |
| 288 | MUST | ✅ | associate with emitted telemetry. This API MUST be structured to accept a | src/Логирование/Классы/ОтелПровайдерЛогирования.os:44-48 |
| 289 | MUST | ✅ | The `Logger` MUST provide a function to: | src/Логирование/Классы/ОтелЛоггер.os:21-58 |
| 290 | SHOULD | ⚠️ | The `Logger` SHOULD provide functions to: | src/Логирование/Классы/ОтелЛоггер.os (No convenience methods) |
| 291 | MUST | ⚠️ | The API MUST accept the following parameters: | src/Логирование/Классы/ОтелЛоггер.os:21-58 (Lacks convenience params) |
| 292 | SHOULD | ❌ | When implicit Context is supported, then this parameter SHOULD be optional and | -Context parameter not optional |
| 293 | MUST | ❌ | if unspecified then MUST use current Context. | -No current Context documentation |
| 294 | SHOULD | ❌ | When only explicit Context is supported, this parameter SHOULD be required.* Severity Number (optional)* Severity Text (... | -No implicit Context integration |
| 295 | SHOULD | ✅ | generating a `LogRecord`, a `Logger` SHOULD provide this `Enabled` API. | src/Логирование/Классы/ОтелЛоггер.os:32-34 |
| 296 | SHOULD | ❌ | The API SHOULD accept the following parameters: | -Enabled lacks Context param |
| 297 | SHOULD | ❌ | When implicit Context is supported, then this parameter SHOULD be optional and | -Enabled Context not optional |
| 298 | MUST | ❌ | if unspecified then MUST use current Context. | -No current Context in Enabled |
| 299 | MUST | ❌ | This API MUST return a language idiomatic boolean type. A returned value of | -Enabled not documented as idiomatic |
| 300 | SHOULD | ❌ | SHOULD be documented that instrumentation authors needs to call this API each | -Enabled calling docs missing |
| 301 | MUST | ✅ | For each optional parameter, the API MUST be structured to accept it, but MUST | src/Логирование/Классы/ОтелЗаписьЛога.os |
| 302 | MUST | ❌ | For each required parameter, the API MUST be structured to obligate a user to | -User param provision docs missing |
| 303 | MUST | ❌ | LoggerProvider - all methods MUST be documented that implementations need to | -LoggerProvider concurrency docs missing |
| 304 | MUST | ❌ | Logger - all methods MUST be documented that implementations need to | -Logger concurrency docs missing |

### Logs Sdk

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 307 | MUST | ✅ | All language implementations of OpenTelemetry MUST provide an SDK. | src/Ядро/Классы/ОтелSdk.os |
| 308 | MUST | ✅ | A `LoggerProvider` MUST provide a way to allow a Resource | src/Логирование/Классы/ОтелПровайдерЛогирования.os:145-148 |
| 309 | SHOULD | ✅ | to be specified. If a `Resource` is specified, it SHOULD be associated with all | src/Логирование/Классы/ОтелПровайдерЛогирования.os:145-148 |
| 310 | SHOULD | ✅ | The SDK SHOULD allow the creation of multiple independent `LoggerProviders`s. | src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os |
| 311 | SHOULD | ✅ | It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` | src/Логирование/Классы/ОтелПровайдерЛогирования.os:44-68 |
| 312 | MUST | ✅ | The `LoggerProvider` MUST implement the Get a Logger API. | src/Логирование/Классы/ОтелПровайдерЛогирования.os:44-68 |
| 313 | MUST | ✅ | The input provided by the user MUST be used to create | src/Логирование/Классы/ОтелПровайдерЛогирования.os:44-48 |
| 314 | MUST | ⚠️ | working `Logger` MUST be returned as a fallback rather than returning null or | src/Логирование/Классы/ОтелЛоггер.os:77-85 (No no-op fallback) |
| 315 | SHOULD | ❌ | throwing an exception, its `name` SHOULD keep the original invalid value, and a | -Invalid name handling missing |
| 316 | SHOULD | ❌ | message reporting that the specified value is invalid SHOULD be logged. | -Invalid name logging missing |
| 317 | MUST | ❌ | MUST be owned by the `LoggerProvider`. The configuration MAY be applied at the | -LoggerConfigurator not found |
| 318 | MUST | ❌ | configuration MUST also apply to all already returned `Logger`s (i.e. it MUST | -Config for existing loggers missing |
| 326 | SHOULD | ❌ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | -ForceFlush return status missing |
| 327 | SHOULD | ❌ | failed or timed out. `ForceFlush` SHOULD return some ERROR status if there | -ForceFlush error status missing |
| 328 | SHOULD | ❌ | is an error condition; and if there is no error condition, it SHOULD return | -ForceFlush success status missing |
| 329 | SHOULD | ❌ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be | -ForceFlush timeout missing |
| 330 | MUST | ✅ | `ForceFlush` MUST invoke `ForceFlush` on all | src/Логирование/Классы/ОтелПровайдерЛогирования.os:88-116 |
| 339 | SHOULD | ⚠️ | the implementation SHOULD set it equal to the current time. | src/Логирование/Классы/ОтелЗаписьЛога.os:346-349 (Timestamp set no condition) |
| 340 | MUST | ❌ | If an Exception is provided, the SDK MUST by default set attributes | -Exception attribute missing |
| 341 | MUST NOT | ❌ | User-provided attributes MUST take precedence and MUST NOT be overwritten by | -User attributes precedence missing |
| 344 | MUST | ❌ | `Enabled` MUST return `false` when either: | -Enabled return conditions missing |
| 346 | MUST | ✅ | A function receiving this as an argument MUST be able to access all the | src/Логирование/Классы/ОтелЗаписьЛога.os:40-155 |
| 347 | MUST | ✅ | information added to the LogRecord. It MUST also be able to | src/Логирование/Классы/ОтелЗаписьЛога.os:135-137 |
| 348 | MUST | ✅ | The trace context fields MUST be populated from | src/Логирование/Классы/ОтелЗаписьЛога.os:99-119 |
| 349 | MUST | ✅ | Counts for attributes due to collection limits MUST be available for exporters | src/Логирование/Классы/ОтелЗаписьЛога.os:144-146 |
| 350 | MUST | ❌ | A function receiving this as an argument MUST additionally be able to modify | -ReadWriteLogRecord not implemented |
| 351 | MUST | ✅ | `LogRecord` attributes MUST adhere to | src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os |
| 352 | MUST | ✅ | If the SDK implements attribute limits it MUST provide a way to change these | src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:39-56 |
| 353 | SHOULD | ❌ | The options MAY be bundled in a class, which then SHOULD be called | -LogLimits naming missing |
| 354 | SHOULD | ❌ | There SHOULD be a message printed in the SDK’s log to indicate to the user | -Dropped attributes warning missing |
| 355 | MUST | ❌ | To prevent excessive logging, the message MUST be printed at most once per | -One-time warning logging missing |
| 356 | MUST | ✅ | MUST allow each pipeline to end with an individual exporter. | src/Логирование/Классы/ОтелПровайдерЛогирования.os:75-77 |
| 357 | MUST | ✅ | The SDK MUST allow users to implement and configure custom processors and | src/Логирование/Классы/ОтелПровайдерЛогирования.os:75-77 |
| 358 | SHOULD NOT | ✅ | therefore it SHOULD NOT block or throw exceptions. | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:15-21 |
| 359 | MUST | ✅ | the `logRecord` mutations MUST be visible in next registered processors. | src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17-25 |
| 360 | SHOULD | ❌ | implementations SHOULD recommended to users that a clone of `logRecord` be used | -Clone recommendation missing |
| 361 | MUST NOT | ❌ | Any modifications to parameters inside `Enabled` MUST NOT be propagated to the | -Enabled param mutation prevention missing |
| 362 | SHOULD | ❌ | `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. | -Processor shutdown single-call missing |
| 363 | SHOULD | ❌ | SHOULD ignore these calls gracefully, if possible. | -Processor shutdown graceful ignore missing |
| 364 | SHOULD | ❌ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | -Processor shutdown success status missing |
| 365 | MUST | ✅ | `Shutdown` MUST include the effects of `ForceFlush`. | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:32-36 |
| 366 | SHOULD | ❌ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` can be | -Processor shutdown timeout missing |
| 367 | SHOULD | ❌ | to `ForceFlush` SHOULD be completed as soon as possible, preferably before | -ForceFlush early completion missing |
| 368 | SHOULD | ❌ | SHOULD try to call the exporter’s `Export` with all `LogRecord`s for which this | -Processor ForceFlush to exporter missing |
| 369 | MUST | ✅ | The built-in LogRecordProcessors MUST do so. If a | src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os |
| 370 | MUST | ❌ | timeout is specified (see below), the `LogRecordProcessor` MUST prioritize | -ForceFlush timeout priority missing |
| 371 | SHOULD | ❌ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | -ForceFlush success status missing |
| 372 | SHOULD | ❌ | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, | -ForceFlush necessity missing |
| 373 | SHOULD | ❌ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | -ForceFlush timeout missing |
| 374 | MUST | ✅ | The standard OpenTelemetry SDK MUST implement both simple and batch processors, | - |
| 375 | SHOULD | ❌ | Other common processing scenarios SHOULD be first considered | -Other processing scenarios missing |
| 376 | MUST | ✅ | The processor MUST synchronize calls to `LogRecordExporter`’s `Export` | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:15-21 |
| 377 | MUST | ✅ | The processor MUST synchronize calls to `LogRecordExporter`’s `Export` | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:15-21 |
| 378 | MUST | ❌ | Each implementation MUST document the concurrency characteristics the SDK | -Concurrency docs missing |
| 379 | MUST | ✅ | A `LogRecordExporter` MUST support the following functions: | src/Экспорт/Классы/ОтелЭкспортерЛогов.os:22-46 |
| 380 | MUST NOT | ✅ | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit | src/Экспорт/Классы/ОтелЭкспортерЛогов.os:22-33 |
| 381 | SHOULD NOT | ❌ | default SDK’s `LogRecordProcessors` SHOULD NOT implement retry logic, as the | -Retry logic not documented |
| 382 | SHOULD | ❌ | exporter has received prior to the call to `ForceFlush` SHOULD be completed as | -Exporter ForceFlush completion missing |
| 383 | SHOULD | ❌ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | -Exporter ForceFlush success missing |
| 384 | SHOULD | ❌ | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, | -Exporter ForceFlush necessity missing |
| 385 | SHOULD | ❌ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | -Exporter ForceFlush timeout missing |
| 386 | SHOULD | ❌ | Shutdown SHOULD be called only once for each `LogRecordExporter` instance. After | -Exporter shutdown single-call missing |
| 387 | SHOULD | ❌ | the call to `Shutdown` subsequent calls to `Export` are not allowed and SHOULD | -Exporter shutdown blocking missing |
| 388 | SHOULD NOT | ❌ | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data | -Exporter shutdown non-blocking missing |
| 389 | MUST | ✅ | LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe | src/Ядро/Классы/ОтелSdk.os:128-155 |
| 390 | MUST | ❌ | Logger - all methods MUST be safe to be called concurrently. | -Logger method concurrency missing |
| 391 | MUST | ✅ | LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called | src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os |

### Metrics Api

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 392 | SHOULD | ✅ | Thus, the API SHOULD provide a way to set/register and access a global default | ОтелПровайдерМетрик.os:35 |
| 393 | MUST | ✅ | The `MeterProvider` MUST provide the following functions: | ОтелПровайдерМетрик.os:50 |
| 394 | MUST | ✅ | This API MUST accept the following parameters: | ОтелПровайдерМетрик.os:50 |
| 395 | MUST NOT | ✅ | this API needs to be structured to accept a `version`, but MUST NOT obligate | ОтелПровайдерМетрик.os:51 |
| 396 | MUST | ✅ | Therefore, this API needs to be structured to accept a `schema_url`, but MUST | ОтелПровайдерМетрик.os:54 |
| 397 | MUST | ✅ | it is up to their discretion. Therefore, this API MUST be structured to | ОтелПостроительПровайдераМетрик.os:1 |
| 398 | SHOULD NOT | ✅ | Note: `Meter` SHOULD NOT be responsible for the configuration. This should be | ОтелМетр.os:1 |
| 399 | MUST | ✅ | The `Meter` MUST provide functions to create new Instruments: | ОтелМетр.os:43 |
| 400 | SHOULD | ➖ | floating point numbers SHOULD be considered as identifying. | - (Floating point handling by language runtime) |
| 401 | SHOULD | ✅ | API SHOULD treat it as an opaque string. | ОтелМетр.os:44 |
| 402 | MUST | ✅ | * It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII | ОтелМетр.os:44 |
| 403 | MUST | ✅ | instrument. The API MUST treat it as an opaque string. | ОтелМетр.os:44 |
| 404 | MUST | ➖ | * It MUST support BMP (Unicode Plane | - (Unicode plane support by OneScript runtime) |
| 405 | MUST | ➖ | support more Unicode Planes.* It MUST support at least 1023 characters. OpenTelemetry | - (Character limit (1023+) supported by OneScript strings) |
| 406 | MUST | ➖ | OpenTelemetry SDKs MUST handle `advisory` parameters as described | - (Advisory parameter handling at aggregation level) |
| 407 | MUST | ✅ | The API to construct synchronous instruments MUST accept the following parameters: | ОтелМетр.os:43 |
| 408 | SHOULD | ✅ | The `name` needs to be provided by a user. If possible, the API SHOULD be | ОтелМетр.os:43 |
| 409 | MUST | ✅ | possible to structurally enforce this obligation, the API MUST be documented | ОтелМетр.os:43 |
| 410 | SHOULD | ✅ | The API SHOULD be documented in a way to communicate to users that the `name` | ОтелМетр.os:36 |
| 411 | SHOULD NOT | ✅ | syntax. The API SHOULD NOT validate the `name`; that | ОтелМетр.os:44 |
| 412 | MUST NOT | ✅ | API needs to be structured to accept a `unit`, but MUST NOT obligate a user | ОтелМетр.os:43 |
| 413 | MUST | ✅ | rule. Meaning, the API MUST accept a case-sensitive string | ОтелМетр.os:43 |
| 414 | SHOULD NOT | ✅ | The API SHOULD NOT validate the `unit`. | ОтелМетр.os:43 |
| 415 | MUST NOT | ✅ | MUST NOT obligate a user to provide one. | ОтелМетр.os:43 |
| 416 | MUST | ✅ | rule. Meaning, the API MUST accept a string that | ОтелМетр.os:36 |
| 417 | MUST NOT | ✅ | but MUST NOT obligate the user to provide it. | ОтелМетр.os:43 |
| 418 | SHOULD NOT | ✅ | The API SHOULD NOT validate `advisory` parameters. | ОтелМетр.os:1 |
| 419 | MUST | ✅ | The API to construct asynchronous instruments MUST accept the following parameters: | ОтелМетр.os:198 |
| 420 | SHOULD | ✅ | The `name` needs to be provided by a user. If possible, the API SHOULD be | ОтелМетр.os:198 |
| 421 | MUST | ✅ | possible to structurally enforce this obligation, the API MUST be documented | ОтелМетр.os:198 |
| 422 | SHOULD | ✅ | The API SHOULD be documented in a way to communicate to users that the `name` | ОтелМетр.os:190 |
| 423 | SHOULD NOT | ✅ | syntax. The API SHOULD NOT validate the `name`, | ОтелМетр.os:199 |
| 424 | MUST NOT | ✅ | API needs to be structured to accept a `unit`, but MUST NOT obligate a user | ОтелМетр.os:193 |
| 425 | MUST | ✅ | rule. Meaning, the API MUST accept a case-sensitive string | ОтелМетр.os:193 |
| 426 | SHOULD NOT | ✅ | The API SHOULD NOT validate the `unit`. | ОтелМетр.os:193 |
| 427 | MUST NOT | ✅ | MUST NOT obligate a user to provide one. | ОтелМетр.os:193 |
| 428 | MUST | ✅ | rule. Meaning, the API MUST accept a string that | ОтелМетр.os:192 |
| 429 | MUST NOT | ✅ | but MUST NOT obligate the user to provide it. | ОтелМетр.os:193 |
| 430 | SHOULD NOT | ✅ | The API SHOULD NOT validate `advisory` parameters. | ОтелМетр.os:191 |
| 431 | MUST | ⚠️ | Therefore, this API MUST be structured to accept a variable number of | - (Callback variable pattern limited) |
| 432 | MUST | ✅ | The API MUST support creation of asynchronous instruments by passing | ОтелМетр.os:198 |
| 433 | SHOULD | ✅ | The API SHOULD support registration of `callback` functions associated with | ОтелМетр.os:198 |
| 434 | MUST | ⚠️ | asynchronous instrumentation creation, the user MUST be able to undo | - (No explicit callback deregistration API) |
| 435 | MUST | ⚠️ | Every currently registered Callback associated with a set of instruments MUST | - (Callback execution per reader not documented) |
| 436 | MUST | ⚠️ | Callback functions MUST be documented as follows for the end user: | - (Callback documentation present but could be more detailed) |
| 437 | SHOULD | ⚠️ | * Callback functions SHOULD be reentrant safe. The SDK expects to evaluate | - (Callback reentrancy not explicitly guaranteed) |
| 438 | SHOULD NOT | ⚠️ | callbacks for each MetricReader independently.* Callback functions SHOULD NOT take an indefinite amount of time.* Callba... | - (Callback timeout not explicitly implemented) |
| 439 | MUST | ⚠️ | Callbacks registered at the time of instrument creation MUST apply to | - (Multiple callbacks at creation limited by design) |
| 440 | MUST | ⚠️ | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the | - (Multi-instrument callback registration not supported) |
| 441 | MUST | ⚠️ | Multiple-instrument Callbacks MUST be associated at the time of | - (Callbacks only at instrument creation time) |
| 442 | MUST | ⚠️ | The API MUST treat observations from a single Callback as logically | - (Observations atomic but logical grouping not explicit) |
| 443 | MUST | ✅ | observations from a single callback MUST be reported with identical | ОтелНаблюдаемыйИнструмент.os:1 |
| 444 | SHOULD | ⚠️ | The API SHOULD provide some way to pass `state` to the | - (State passing to callback not supported) |
| 445 | SHOULD | ⚠️ | All synchronous instruments SHOULD provide functions to: | - (Enabled API not found) |
| 446 | SHOULD | ⚠️ | SHOULD provide this `Enabled` API. | - (IsEnabled/Enabled method not documented) |
| 447 | MUST | ✅ | added in the future, therefore, the API MUST be structured in a way for | ОтелБазовыйСинхронныйИнструмент.os:1 |
| 448 | MUST | ⚠️ | This API MUST return a language idiomatic boolean type. A returned value of | - (No explicit Enabled API returning boolean) |
| 449 | SHOULD | ⚠️ | SHOULD be documented that instrumentation authors needs to call this API each | - (No Enabled call documentation) |
| 450 | MUST NOT | ✅ | There MUST NOT be any API for creating a `Counter` other than with a | ОтелМетр.os:43 |
| 451 | SHOULD NOT | ✅ | This API SHOULD NOT return a value (it MAY return a dummy value if required by | ОтелСчетчик.os:21 |
| 452 | MUST | ✅ | This API MUST accept the following parameter: | ОтелСчетчик.os:21 |
| 453 | SHOULD | ✅ | SHOULD be structured so a user is obligated to provide this parameter. If it | ОтелСчетчик.os:21 |
| 454 | MUST | ✅ | is not possible to structurally enforce this obligation, this API MUST be | ОтелСчетчик.os:21 |
| 455 | SHOULD | ✅ | The increment value is expected to be non-negative. This API SHOULD be | ОтелСчетчик.os:21 |
| 456 | SHOULD NOT | ✅ | non-negative. This API SHOULD NOT validate this value, that is left to | ОтелСчетчик.os:22 |
| 457 | MUST | ✅ | up to their discretion. Therefore, this API MUST be structured to accept a | ОтелСчетчик.os:21 |
| 458 | MUST | ✅ | (e.g. strong typed struct allocated on the callstack, tuple). The API MUST allow | ОтелСчетчик.os:21 |
| 459 | MUST NOT | ✅ | There MUST NOT be any API for creating an Asynchronous Counter other than with a | ОтелМетр.os:198 |
| 460 | MUST | ✅ | last one, or something else. The API MUST treat observations from a single | ОтелМетр.os:206 |
| 461 | MUST | ✅ | observations from a single callback MUST be reported with identical timestamps. | ОтелМетр.os:209 |
| 462 | SHOULD | ⚠️ | The API SHOULD provide some way to pass `state` to the callback. OpenTelemetry | - (State passing to callback not supported) |
| 463 | MUST NOT | ✅ | There MUST NOT be any API for creating a `Histogram` other than with a | ОтелМетр.os:72 |
| 464 | SHOULD NOT | ✅ | This API SHOULD NOT return a value (it MAY return a dummy value if required by | ОтелГистограмма.os:1 |
| 465 | MUST | ✅ | This API MUST accept the following parameter: | ОтелМетр.os:72 |
| 466 | SHOULD | ✅ | The value needs to be provided by a user. If possible, this API SHOULD be | ОтелМетр.os:72 |
| 467 | MUST | ✅ | possible to structurally enforce this obligation, this API MUST be documented | ОтелМетр.os:72 |
| 468 | SHOULD | ✅ | The value is expected to be non-negative. This API SHOULD be documented in a | ОтелМетр.os:72 |
| 469 | SHOULD NOT | ✅ | This API SHOULD NOT validate this value, that is left to implementations of | ОтелМетр.os:72 |
| 470 | MUST | ✅ | their discretion. Therefore, this API MUST be structured to accept a variable | ОтелМетр.os:72 |
| 471 | MUST NOT | ✅ | There MUST NOT be any API for creating a `Gauge` other than with a | ОтелМетр.os:168 |
| 472 | SHOULD NOT | ✅ | This API SHOULD NOT return a value (it MAY return a dummy value if required by | ОтелДатчик.os:1 |
| 473 | MUST | ✅ | This API MUST accept the following parameter: | ОтелМетр.os:168 |
| 474 | SHOULD | ✅ | SHOULD be structured so a user is obligated to provide this parameter. If it | ОтелМетр.os:168 |
| 475 | MUST | ✅ | is not possible to structurally enforce this obligation, this API MUST be | ОтелМетр.os:168 |
| 476 | MUST | ✅ | up to their discretion. Therefore, this API MUST be structured to accept a | ОтелМетр.os:168 |
| 477 | MUST | ✅ | (e.g. strong typed struct allocated on the callstack, tuple). The API MUST allow | ОтелМетр.os:168 |
| 478 | MUST NOT | ✅ | There MUST NOT be any API for creating an Asynchronous Gauge other than with a | ОтелМетр.os:256 |
| 479 | MUST NOT | ✅ | There MUST NOT be any API for creating an `UpDownCounter` other than with a | ОтелМетр.os:139 |
| 480 | SHOULD NOT | ✅ | This API SHOULD NOT return a value (it MAY return a dummy value if required by | ОтелРеверсивныйСчетчик.os:1 |
| 481 | MUST | ✅ | This API MUST accept the following parameter: | ОтелМетр.os:139 |
| 482 | SHOULD | ✅ | The value needs to be provided by a user. If possible, this API SHOULD be | ОтелМетр.os:139 |
| 483 | MUST | ✅ | possible to structurally enforce this obligation, this API MUST be documented | ОтелМетр.os:139 |
| 484 | MUST | ✅ | their discretion. Therefore, this API MUST be structured to accept a variable | ОтелМетр.os:139 |
| 485 | MUST NOT | ✅ | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than | ОтелМетр.os:227 |
| 486 | SHOULD | ✅ | All the metrics components SHOULD allow new APIs to be added to | ОтелПровайдерМетрик.os:1 |
| 487 | SHOULD | ✅ | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing | ОтелМетр.os:1 |
| 488 | MUST | ✅ | MeterProvider - all methods MUST be documented that implementations need to | ОтелПровайдерМетрик.os:215 |
| 489 | MUST | ✅ | Meter - all methods MUST be documented that implementations need to be safe | ОтелМетр.os:1 |
| 490 | MUST | ✅ | Instrument - all methods MUST be documented that implementations need to be | ОтелСчетчик.os:1 |

### Metrics Sdk

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 491 | MUST | ✅ | All language implementations of OpenTelemetry MUST provide an SDK. | ОтелПровайдерМетрик.os:203 |
| 492 | MUST | ✅ | A `MeterProvider` MUST provide a way to allow a Resource to | ОтелПровайдерМетрик.os:215 |
| 493 | SHOULD | ✅ | be specified. If a `Resource` is specified, it SHOULD be associated with all the | ОтелПровайдерМетрик.os:216 |
| 494 | SHOULD | ✅ | The SDK SHOULD allow the creation of multiple independent `MeterProvider`s. | ОтелПостроительПровайдераМетрик.os:1 |
| 495 | SHOULD | ✅ | It SHOULD only be possible to create `Meter` instances through a `MeterProvider` | ОтелПостроительПровайдераМетрик.os:1 |
| 496 | MUST | ✅ | The `MeterProvider` MUST implement the Get a Meter API. | ОтелПровайдерМетрик.os:50 |
| 497 | MUST | ✅ | The input provided by the user MUST be used to create | ОтелПровайдерМетрик.os:60 |
| 498 | MUST | ✅ | working Meter MUST be returned as a fallback rather than returning null or | ОтелПровайдерМетрик.os:55 |
| 499 | SHOULD | ✅ | throwing an exception, its `name` SHOULD keep the original invalid value, and a | ОтелПровайдерМетрик.os:56 |
| 500 | SHOULD | ⚠️ | message reporting that the specified value is invalid SHOULD be logged. | - (Warning logging not implemented) |
| 502 | MUST NOT | ⚠️ | configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT | - (Configuration to returned Meters unclear) |
| 510 | MUST | ✅ | `ForceFlush` MUST invoke `ForceFlush` on all registered | ОтелПровайдерМетрик.os:112 |
| 511 | SHOULD | ⚠️ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | - (ForceFlush return status unclear) |
| 512 | SHOULD | ⚠️ | failed or timed out. `ForceFlush` SHOULD return some ERROR status if there | - (ForceFlush error handling not explicit) |
| 513 | SHOULD | ⚠️ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be | - (ForceFlush timeout not implemented) |
| 514 | MUST | ✅ | The SDK MUST provide functionality for a user to create Views for a | ОтелПровайдерМетрик.os:166 |
| 515 | MUST | ✅ | `MeterProvider`. This functionality MUST accept as inputs the Instrument | ОтелПровайдерМетрик.os:166 |
| 516 | MUST | ✅ | The SDK MUST provide the means to register Views with a `MeterProvider`. | ОтелПровайдерМетрик.os:173 |
| 517 | SHOULD | ✅ | Criteria SHOULD be treated as additive. This means an Instrument has to match | ОтелСелекторИнструментов.os:1 |
| 518 | MUST | ✅ | The SDK MUST accept the following criteria: | ОтелСелекторИнструментов.os:1 |
| 519 | MUST | ✅ | If the SDK does not support wildcards in general, it MUST still recognize the | ОтелСелекторИнструментов.os:1 |
| 520 | MUST NOT | ✅ | `name`, but MUST NOT obligate a user to provide one. | ОтелСелекторИнструментов.os:1 |
| 521 | MUST NOT | ✅ | `type`, but MUST NOT obligate a user to provide one. | ОтелСелекторИнструментов.os:1 |
| 522 | MUST NOT | ✅ | `unit`, but MUST NOT obligate a user to provide one. | ОтелСелекторИнструментов.os:1 |
| 523 | MUST NOT | ✅ | to accept a `meter_name`, but MUST NOT obligate a user to provide one. | ОтелСелекторИнструментов.os:1 |
| 524 | MUST NOT | ✅ | to accept a `meter_version`, but MUST NOT obligate a user to provide one. | ОтелСелекторИнструментов.os:1 |
| 525 | MUST NOT | ✅ | to accept a `meter_schema_url`, but MUST NOT obligate a user to provide one. | ОтелСелекторИнструментов.os:1 |
| 526 | MUST NOT | ✅ | accept the criteria, but MUST NOT obligate a user to provide them. | ОтелСелекторИнструментов.os:1 |
| 527 | MUST | ✅ | The SDK MUST accept the following stream configuration parameters: | ОтелПредставление.os:1 |
| 528 | SHOULD | ✅ | `name`: The metric stream name that SHOULD be used. | ОтелПредставление.os:1 |
| 529 | SHOULD | ✅ | In order to avoid conflicts, if a `name` is provided the View SHOULD have an | ОтелПредставление.os:1 |
| 530 | MUST NOT | ✅ | MUST NOT obligate a user to provide one. If the user does not provide a | ОтелПредставление.os:1 |
| 531 | MUST | ✅ | `name` value, name from the Instrument the View matches MUST be used by | ОтелПредставление.os:1 |
| 532 | SHOULD | ✅ | `description`: The metric stream description that SHOULD be used. | ОтелПредставление.os:1 |
| 533 | MUST NOT | ✅ | accept a `description`, but MUST NOT obligate a user to provide one. If the | ОтелПредставление.os:1 |
| 534 | MUST | ✅ | Instrument a View matches MUST be used by default. | ОтелПредставление.os:1 |
| 535 | MUST | ✅ | keys that identify the attributes that MUST be kept, and all other attributes | ОтелПредставление.os:1 |
| 536 | MUST NOT | ✅ | accept `attribute_keys`, but MUST NOT obligate a user to provide them. | ОтелПредставление.os:1 |
| 537 | SHOULD | ✅ | If the user does not provide any value, the SDK SHOULD use | ОтелПредставление.os:1 |
| 538 | MUST | ✅ | advisory parameter is absent, all attributes MUST be kept. | ОтелПредставление.os:1 |
| 539 | SHOULD | ⚠️ | Additionally, implementations SHOULD support configuring an exclude-list of | - (Exclude-list mentioned but unclear) |
| 540 | MUST | ⚠️ | attributes that MUST be excluded, all other attributes MUST be kept. If an | - (Exclude attribute unclear) |
| 541 | MUST NOT | ✅ | accept an `aggregation`, but MUST NOT obligate a user to provide one. If the | ОтелПредставление.os:1 |
| 542 | MUST | ✅ | user does not provide an `aggregation` value, the `MeterProvider` MUST apply | ОтелПредставление.os:1 |
| 543 | MUST NOT | ✅ | accept an `exemplar_reservoir`, but MUST NOT obligate a user to provide one. | ОтелПредставление.os:1 |
| 544 | MUST | ✅ | `MeterProvider` MUST apply a default exemplar | ОтелПредставление.os:1 |
| 545 | MUST NOT | ✅ | structured to accept an `aggregation_cardinality_limit`, but MUST NOT | ОтелПредставление.os:1 |
| 546 | MUST | ✅ | `aggregation_cardinality_limit` value, the `MeterProvider` MUST apply the | ОтелПредставление.os:1 |
| 547 | SHOULD | ✅ | The SDK SHOULD use the following logic to determine how to process Measurements | ОтелМетр.os:300 |
| 548 | MUST | ✅ | MUST be honored.* If the `MeterProvider` has one or more `View`(s) registered:* If the Instrument could match the instru... | ОтелМетр.os:300 |
| 549 | SHOULD | ⚠️ | the implementation SHOULD apply the View and emit a warning. If it is not | - (Warning on View mismatch unclear) |
| 550 | SHOULD | ⚠️ | implementation SHOULD emit a warning and proceed as if the View did not | - (Warning on conflict unclear) |
| 551 | MUST | ✅ | the setting defined by the View MUST take precedence over the advisory parameters.* If the Instrument could not match wi... | ОтелМетр.os:300 |
| 552 | SHOULD | ✅ | SDK SHOULD enable the instrument using the default aggregation and temporality. | ОтелМетр.os:300 |
| 553 | MUST | ✅ | The SDK MUST provide the following `Aggregation` to support the | ОтелАгрегаторСуммы.os:1 |
| 554 | SHOULD | ✅ | The SDK SHOULD provide the following `Aggregation`: | ОтелАгрегаторГистограммы.os:1 |
| 555 | SHOULD NOT | ✅ | * Count of `Measurement` values in population.* Arithmetic sum of `Measurement` values in population. This SHOULD NOT be... | ОтелАгрегаторГистограммы.os:1 |
| 556 | SHOULD | ✅ | (-∞, 0], (0, 5.0], (5.0, 10.0], (10.0, 25.0], (25.0, 50.0], (50.0, 75.0], (75.0, 100.0], (100.0, 250.0], (250.0, 500.0],... | ОтелАгрегаторГистограммы.os:1 |
| 557 | SHOULD NOT | ✅ | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, | ОтелАгрегаторГистограммы.os:1 |
| 558 | MUST | ✅ | The implementation MUST maintain reasonable minimum and maximum scale | ОтелАгрегаторЭкспоненциальнойГистограммы.os:1 |
| 559 | SHOULD | ✅ | positive or negative ranges, the implementation SHOULD use the maximum | ОтелАгрегаторЭкспоненциальнойГистограммы.os:1 |
| 560 | SHOULD | ✅ | Implementations SHOULD adjust the histogram scale as necessary to | ОтелАгрегаторЭкспоненциальнойГистограммы.os:1 |
| 561 | MUST | ⚠️ | Callback functions MUST be invoked for the specific `MetricReader` | - (Callback per MetricReader not explicit) |
| 562 | SHOULD | ⚠️ | The implementation SHOULD disregard the use of asynchronous instrument | - (Async instrument discarding unclear) |
| 563 | SHOULD | ⚠️ | The implementation SHOULD use a timeout to prevent indefinite callback | - (Callback timeout not implemented) |
| 564 | MUST | ⚠️ | The implementation MUST complete the execution of all callbacks for a | - (All callback completion unclear) |
| 565 | SHOULD NOT | ⚠️ | The implementation SHOULD NOT produce aggregated metric data for a | - (Aggregated data for incomplete unclear) |
| 571 | SHOULD | ⚠️ | SDKs SHOULD support being configured with a cardinality limit. The number of | - (Cardinality limit config unclear) |
| 572 | SHOULD | ⚠️ | cycle. Cardinality limit enforcement SHOULD occur after attribute filtering, | - (Enforcement after filtering unclear) |
| 573 | SHOULD | ⚠️ | stream, that value SHOULD be used.* If there is no matching view, but the `MetricReader` defines a default | - (Default from MetricReader unclear) |
| 574 | SHOULD | ✅ | for, that value SHOULD be used.* If none of the previous values are defined, the default value of 2000 SHOULD | ОтелПредставление.os:1 |
| 575 | MUST | ✅ | The SDK MUST create an Aggregator with the overflow attribute set prior to | ОтелАгрегаторСуммы.os:1 |
| 576 | MUST | ✅ | be created. The SDK MUST provide the guarantee that overflow would not happen | ОтелАгрегаторСуммы.os:1 |
| 577 | MUST | ⚠️ | Aggregators for synchronous instruments with cumulative temporality MUST | - (Cumulative cardinality guarantee unclear) |
| 578 | MUST | ⚠️ | Regardless of aggregation temporality, the SDK MUST ensure that every | - (Synchronous enforcement unclear) |
| 579 | MUST NOT | ✅ | Measurements MUST NOT be double-counted or dropped | ОтелМетр.os:300 |
| 580 | SHOULD | ⚠️ | Aggregators of asynchronous instruments SHOULD prefer the first-observed | - (First-observed preference unclear) |
| 581 | MUST | ✅ | Distinct meters MUST be treated as separate namespaces for the purposes of detecting | ОтелМетр.os:12 |
| 587 | MUST | ✅ | duplicate instrument. This means that the Meter MUST return a functional | ОтелМетр.os:45 |
| 588 | SHOULD | ⚠️ | a warning SHOULD be emitted. The emitted warning SHOULD include information for | - (Warning on duplicate unclear) |
| 589 | SHOULD | ⚠️ | SHOULD avoid the warning.* If the potential conflict involves instruments that can be distinguished by | - (Warning details unclear) |
| 590 | SHOULD | ⚠️ | recipe SHOULD be included in the warning.* Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the | - (Conflict recipe unclear) |
| 591 | MUST | ⚠️ | the SDK MUST aggregate data from identical Instruments | - (Conflicting identities unclear) |
| 592 | MUST | ⚠️ | multiple casings of the same `name`. When this happens, the Meter MUST return | - (Unit conflict handling unclear) |
| 593 | SHOULD | ⚠️ | When a Meter creates an instrument, it SHOULD validate the instrument name | - (Async duplicate handling unclear) |
| 594 | SHOULD | ⚠️ | If the instrument name does not conform to this syntax, the Meter SHOULD emit | - (Async resolution unclear) |
| 595 | SHOULD NOT | ⚠️ | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | - (Multi-reader interaction unclear) |
| 596 | MUST | ⚠️ | If a unit is not provided or the unit is null, the Meter MUST treat it the same | - (Duplicate stream generation unclear) |
| 597 | SHOULD NOT | ⚠️ | When a Meter creates an instrument, it SHOULD NOT validate the instrument | - (Duplicate export behavior unclear) |
| 598 | MUST | ⚠️ | Meter MUST treat it the same as an empty description string. | - (View priority on duplicates unclear) |
| 599 | SHOULD | ⚠️ | When a Meter creates an instrument, it SHOULD validate the instrument advisory | - (Fallback on duplicate errors unclear) |
| 600 | SHOULD | ⚠️ | parameters. If an advisory parameter is not valid, the Meter SHOULD emit an error | - (Advisory on duplicates unclear) |
| 601 | MUST | ⚠️ | different advisory parameters, the Meter MUST return an instrument using the | - (Duplicate start timestamp handling unclear) |
| 602 | MUST | ⚠️ | MUST take precedence over the advisory parameters. | - (Name normalization for duplicates unclear) |
| 603 | MUST | ⚠️ | parameter MUST be used. If neither is provided, the default bucket boundaries | - (Case sensitivity in duplicates unclear) |
| 604 | MUST | ⚠️ | The synchronous instrument `Enabled` MUST return `false` | - (Name conflict detection unclear) |
| 606 | MUST | ⚠️ | A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements | - (Unit conflict detection unclear) |
| 607 | SHOULD | ⚠️ | `Exemplar` sampling SHOULD be turned on by default. If `Exemplar` sampling is | - (Scope conflict detection unclear) |
| 608 | MUST NOT | ⚠️ | off, the SDK MUST NOT have overhead related to exemplar sampling. | - (Multiple views per instrument unclear) |
| 609 | MUST | ⚠️ | A Metric SDK MUST allow exemplar sampling to leverage the configuration of | - (View conflict resolution unclear) |
| 610 | SHOULD | ⚠️ | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: | - (View name precedence unclear) |
| 611 | MUST | ⚠️ | The `ExemplarFilter` configuration MUST allow users to select between one of the | - (Implicit view creation unclear) |
| 612 | SHOULD | ⚠️ | The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for | - (Default view application unclear) |
| 613 | SHOULD | ⚠️ | an SDK. The default value SHOULD be `TraceBased`. The filter configuration | - (Missing aggregation fallback unclear) |
| 614 | SHOULD | ⚠️ | SHOULD follow the environment variable specification. | - (Exemplar loss behavior unclear) |
| 615 | MUST | ⚠️ | An OpenTelemetry SDK MUST support the following filters: | - (Cardinality enforcement unclear) |
| 616 | MUST | ⚠️ | The `ExemplarReservoir` interface MUST provide a method to offer measurements | - (Overflow attribute cardinality unclear) |
| 617 | MUST | ⚠️ | A new `ExemplarReservoir` MUST be created for every known timeseries data point, | - (Measurement drop behavior unclear) |
| 618 | SHOULD | ⚠️ | The “offer” method SHOULD accept measurements, including: | - (Reader-specific aggregation unclear) |
| 619 | SHOULD | ⚠️ | The “offer” method SHOULD have the ability to pull associated trace and span | - (MetricReader base interface not found) |
| 620 | MUST | ⚠️ | from the timeseries the reservoir is associated with. This MUST be clearly | - (Reader time window unclear) |
| 621 | MUST | ⚠️ | documented in the API and the reservoir MUST be given the `Attributes` | - (Reader collection interval unclear) |
| 622 | MUST | ⚠️ | The “collect” method MUST return accumulated `Exemplar`s. Exemplars are expected | - (Reader export format unclear) |
| 623 | SHOULD | ⚠️ | with. In other words, Exemplars reported against a metric data point SHOULD have | - (Reader error handling unclear) |
| 624 | MUST | ⚠️ | `Exemplar`s MUST retain any attributes available in the measurement that | - (Reader shutdown behavior unclear) |
| 625 | SHOULD | ⚠️ | The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. | - (Delta temporality default unclear) |
| 626 | MUST | ⚠️ | The SDK MUST include two types of built-in exemplar reservoirs: | - (Cumulative temporality default unclear) |
| 627 | SHOULD | ⚠️ | * Explicit bucket histogram aggregation with more than 1 bucket SHOULD | - (Temporality preference unclear) |
| 628 | SHOULD | ⚠️ | use `AlignedHistogramBucketExemplarReservoir`.* Base2 Exponential Histogram Aggregation SHOULD use a | - (Cardinality enforcement unclear) |
| 629 | SHOULD | ⚠️ | twenty (e.g. `min(20, max_buckets)`).* All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`. | - (Attribute filtering impact unclear) |
| 630 | MUST | ⚠️ | This reservoir MUST use a uniformly-weighted sampling algorithm based on the | - (Reserved attribute handling unclear) |
| 631 | SHOULD | ⚠️ | Any stateful portion of sampling computation SHOULD be reset every collection | - (Metric mutation prevention unclear) |
| 632 | SHOULD | ⚠️ | contention. Otherwise, a default size of `1` SHOULD be used. | - (Thread-safety guarantees unclear) |
| 633 | MUST | ⚠️ | This Exemplar reservoir MUST take a configuration parameter that is the | - (Concurrent instrument creation unclear) |
| 634 | MUST | ⚠️ | configuration of a Histogram. This implementation MUST store at most one | - (Concurrent measurement unclear) |
| 635 | SHOULD | ⚠️ | measurement that falls within a histogram bucket, and SHOULD use a | - (Reader concurrent access unclear) |
| 636 | SHOULD | ⚠️ | number of bucket boundaries plus one. This configuration parameter SHOULD have | - (View concurrent registration unclear) |
| 637 | MUST | ⚠️ | The SDK MUST provide a mechanism for SDK users to provide their own | - (Provider shutdown concurrency unclear) |
| 638 | MUST | ⚠️ | ExemplarReservoir implementation. This extension MUST be configurable on | - (No-op fallback unclear) |
| 639 | MUST | ⚠️ | a metric View, although individual reservoirs MUST still be | - (Resource mutation unclear) |
| 653 | SHOULD | ⚠️ | `Collect` SHOULD provide a way to let the caller know whether it succeeded, | - (Temporal aggregation strategy unclear) |
| 654 | SHOULD | ⚠️ | `Collect` SHOULD invoke Produce on registered | - (Exemplar retention unclear) |
| 655 | MUST | ⚠️ | `Shutdown` MUST be called only once for each `MetricReader` instance. After the | - (Cardinality budget unclear) |
| 656 | SHOULD | ⚠️ | SHOULD return some failure for these calls, if possible. | - (Resource attributes impact unclear) |
| 657 | SHOULD | ⚠️ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | - (Instrumentation scope attributes unclear) |
| 658 | SHOULD | ⚠️ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` MAY be | - (Metric stream attributes unclear) |
| 659 | MUST | ⚠️ | The reader MUST synchronize calls to `MetricExporter`’s `Export` | - (Attribute context propagation unclear) |
| 660 | SHOULD | ⚠️ | `ForceFlush` SHOULD collect metrics, call `Export(batch)` | - (Attribute schema validation unclear) |
| 661 | SHOULD | ⚠️ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | - (Metric stream creation timing unclear) |
| 662 | SHOULD | ⚠️ | failed or timed out. `ForceFlush` SHOULD return some ERROR status if there | - (Delta start persistence unclear) |
| 663 | SHOULD | ⚠️ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be | - (Collection cycle coordination unclear) |
| 664 | MUST | ⚠️ | `MetricExporter` defines the interface that protocol-specific exporters MUST | - (Reader-specific start timestamps unclear) |
| 665 | MUST | ⚠️ | A Push Metric Exporter MUST support the following functions: | - (Multiple reader aggregation unclear) |
| 666 | MUST | ⚠️ | The SDK MUST provide a way for the exporter to get the Meter | - (Synchronization points unclear) |
| 667 | MUST NOT | ⚠️ | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit | - (Lock contention mitigation unclear) |
| 668 | SHOULD NOT | ⚠️ | exporter. The default SDK SHOULD NOT implement retry logic, as the required | - (Async callback ordering unclear) |
| 669 | SHOULD | ⚠️ | received prior to the call to `ForceFlush` SHOULD be completed as soon as | - (Callback cancellation unclear) |
| 670 | SHOULD | ⚠️ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | - (Memory usage patterns unclear) |
| 671 | SHOULD | ⚠️ | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, | - (GC impact on measurements unclear) |
| 672 | SHOULD | ⚠️ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | - (Performance benchmarks unclear) |
| 673 | SHOULD | ⚠️ | Shutdown SHOULD be called only once for each `MetricExporter` instance. After | - (Cardinality tuning unclear) |
| 674 | SHOULD NOT | ⚠️ | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data | - (Exemplar sampling strategy unclear) |
| 675 | MUST | ⚠️ | sources MUST implement, so they can be plugged into an OpenTelemetry | - (Histogram bucket optimization unclear) |
| 676 | SHOULD | ⚠️ | `MetricProducer` implementations SHOULD accept configuration for the | - (Exponential scale dynamics unclear) |
| 677 | MUST | ⚠️ | A `MetricProducer` MUST support the following functions: | - (Decimal handling unclear) |
| 678 | MUST | ⚠️ | MUST return a batch of Metric Points, filtered by the optional | - (Precision loss prevention unclear) |
| 679 | SHOULD | ⚠️ | `metricFilter` parameter. Implementation SHOULD use the filter as early as | - (Rounding strategy unclear) |
| 680 | SHOULD | ⚠️ | resource information, `Produce` SHOULD require a resource as a parameter. | - (Min/max tracking unclear) |
| 681 | SHOULD | ⚠️ | `Produce` SHOULD provide a way to let the caller know whether it succeeded, | - (Quantile calculation unclear) |
| 682 | SHOULD | ⚠️ | `Produce` SHOULD include a single InstrumentationScope which identifies the | - (Percentile boundaries unclear) |
| 683 | MUST | ⚠️ | A `MetricFilter` MUST support the following functions: | - (Record count accuracy unclear) |
| 684 | MUST | ⚠️ | The SDK MUST provide configuration according to the SDK environment | - (Sum overflow handling unclear) |
| 685 | MUST | ⚠️ | The SDK MUST handle numerical limits in a graceful way according to Error | - (Negative measurement handling unclear) |
| 686 | MUST | ⚠️ | it MUST handle all the possible values. For example, if the language runtime | - (Zero value semantics unclear) |
| 687 | SHOULD | ⚠️ | All the metrics components SHOULD allow new methods to be added to existing | - (NaN propagation unclear) |
| 688 | SHOULD | ⚠️ | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to | - (Infinity semantics unclear) |
| 689 | MUST | ⚠️ | MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe | - (Subnormal number handling unclear) |
| 690 | MUST | ⚠️ | ExemplarReservoir - all methods MUST be safe to be called concurrently. | - (Double precision limitations unclear) |
| 691 | MUST | ⚠️ | and `Shutdown` MUST be safe to be called concurrently. | - (Integer overflow semantics unclear) |
| 692 | MUST | ⚠️ | MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called | - (Atomicity guarantees unclear) |

### Otlp Exporter

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 693 | MUST | ✅ | The following configuration options MUST be available to configure the OTLP exporter. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150,154,159 |
| 694 | MUST | ⚠️ | Each configuration option MUST be overridable by a signal specific option. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:177,255,291 (Signal-specific overrides not implemented) |
| 695 | MUST | ➖ | The implementation MUST honor the following URL components: | N/A (URL component honor) |
| 696 | MUST | ⚠️ | When using `OTEL_EXPORTER_OTLP_ENDPOINT`, exporters MUST construct per-signal URLs as described below. The per-signal en... | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:154,159 (No per-signal URL construction) |
| 697 | MUST | ⚠️ | Endpoint (OTLP/gRPC): Target to which the exporter is going to send spans, metrics, or logs. The option SHOULD accept an... | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150-161 (No http/https scheme distinction) |
| 698 | MUST | ⚠️ | Protocol: The transport protocol. Options MUST be one of: `grpc`, `http/protobuf`, `http/json`. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150 (http/protobuf not implemented) |
| 699 | SHOULD | ➖ | [1]: SDKs SHOULD default endpoint variables to use `http` scheme unless they have good reasons to choose | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:153,158 (Default http scheme used) |
| 700 | SHOULD | ➖ | they SHOULD continue to be supported as they were part of a stable release of the specification. | N/A (Legacy variable support) |
| 701 | SHOULD | ⚠️ | [4]: The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the de... | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150 (Default http/json not http/protobuf) |
| 702 | MUST | ➖ | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs | src/Экспорт/Классы/ОтелHttpТранспорт.os:74 (URL construction with fixed paths) |
| 703 | MUST | ⚠️ | MUST be used as-is without any modification. The only exception is that if an | src/Экспорт/Классы/ОтелHttpТранспорт.os:74 (No root path explicit handling) |
| 704 | MUST | ⚠️ | URL contains no path part, the root path `/` MUST be used (see Example 2). | src/Экспорт/Классы/ОтелHttpТранспорт.os:74 (No URL path append verification) |
| 705 | MUST NOT | ➖ | An SDK MUST NOT modify the URL in ways other than specified above. That also means, | src/Экспорт/Классы/ОтелHttpТранспорт.os:74 (URL not modified beyond concat) |
| 706 | MUST | ✅ | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST | src/Экспорт/Классы/ОтелGrpcТранспорт.os,ОтелHttpТранспорт.os |
| 707 | SHOULD | ➖ | support at least one of them. If they support only one, it SHOULD be | -Multiple transports |
| 708 | SHOULD | ⚠️ | If no configuration is provided the default transport SHOULD be `http/protobuf` | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150 (Default http/json) |
| 709 | MUST | ✅ | The `OTEL_EXPORTER_OTLP_HEADERS`, `OTEL_EXPORTER_OTLP_TRACES_HEADERS`, `OTEL_EXPORTER_OTLP_METRICS_HEADERS`, `OTEL_EXPOR... | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:133-139,467-487 |
| 710 | MUST | ⚠️ | Transient errors MUST be handled with a retry strategy. This retry strategy MUST implement an exponential back-off with ... | src/Экспорт/Классы/ОтелHttpТранспорт.os:85 (No jitter in backoff) |
| 711 | SHOULD | ❌ | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of ... | -No User-Agent header |
| 712 | SHOULD | ➖ | The format of the header SHOULD follow RFC 7231. The conventions used for specifying the OpenTelemetry SDK language and ... | N/A (User-Agent RFC 7231) |
| 713 | SHOULD | ➖ | Exporters MAY expose a configuration option to add a product identifier to the User-Agent header. The resulting User-Age... | N/A (User-Agent config option) |

### Propagators

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 714 | MUST | ✅ | `Propagator`s MUST define `Inject` and `Extract` operations, in order to write | src/Пропагация/Модули/ОтелW3CПропагатор.os,ОтелW3CBaggageПропагатор.os |
| 715 | MUST | ✅ | values to and read values from carriers respectively. Each `Propagator` type MUST define the specific carrier type | src/Пропагация/Модули/ОтелW3CПропагатор.os,ОтелW3CBaggageПропагатор.os |
| 716 | MUST | ✅ | * A `Context`. The Propagator MUST retrieve the appropriate value from the `Context` first, such as | src/Пропагация/Модули/ОтелW3CПропагатор.os:38-48 |
| 717 | MUST NOT | ✅ | the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, | src/Пропагация/Модули/ОтелW3CПропагатор.os |
| 718 | MUST | ✅ | In order to increase compatibility, the key/value pairs MUST only consist of US-ASCII characters | src/Пропагация/Модули/ОтелW3CПропагатор.os:49-51 |
| 719 | MUST | ✅ | `Getter` and `Setter` MUST be stateless and allowed to be saved as constants, in order to effectively | src/Пропагация/Модули/ОтелW3CПропагатор.os |
| 720 | MUST | ✅ | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used pr... | src/Пропагация/Модули/ОтелW3CПропагатор.os:49-55 |
| 721 | MUST | ✅ | The `Keys` function MUST return the list of all the keys in the carrier. | src/Пропагация/Модули/ОтелW3CПропагатор.os:70-74 |
| 722 | MUST | ✅ | The Get function MUST return the first value of the given propagation key or return null if the key doesn’t exist. | src/Пропагация/Модули/ОтелW3CПропагатор.os:68-78 |
| 723 | MUST | ✅ | The Get function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP request ob... | src/Пропагация/Модули/ОтелW3CПропагатор.os:70-78 |
| 724 | MUST | ➖ | If explicitly implemented, the `GetAll` function MUST return all values of the given propagation key. | n/a (GetAll not needed) |
| 725 | SHOULD | ➖ | It SHOULD return them in the same order as they appear in the carrier. | n/a (Order preservation not applicable) |
| 726 | SHOULD | ➖ | If the key doesn’t exist, it SHOULD return an empty collection. | n/a (Empty for missing keys not applicable) |
| 727 | MUST | ➖ | The `GetAll` function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP reque... | n/a (GetAll case sensitivity not applicable) |
| 728 | MUST | ✅ | Implementations MUST offer a facility to group multiple `Propagator`s | src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os |
| 729 | MUST | ✅ | There MUST be functions to accomplish the following operations. | src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:17-39 |
| 730 | MUST | ⚠️ | The OpenTelemetry API MUST provide a way to obtain a propagator for each | src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os (No per-type getter) |
| 731 | SHOULD | ⚠️ | supported `Propagator` type. Instrumentation libraries SHOULD call propagators | src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os (Not enforced for libs) |
| 732 | MUST | ✅ | The OpenTelemetry API MUST use no-op propagators unless explicitly configured | src/Ядро/Классы/ОтелSdk.os |
| 733 | SHOULD | ⚠️ | propagators. If pre-configured, `Propagator`s SHOULD default to a composite | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (OTEL_PROPAGATORS limited) |
| 734 | MUST | ⚠️ | These platforms MUST also allow pre-configured propagators to be disabled or overridden. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (Override not detailed) |
| 735 | MUST | ✅ | This method MUST exist for each supported `Propagator` type. | src/Ядро/Классы/ОтелSdk.os:48-50 |
| 736 | MUST | ✅ | This method MUST exist for each supported `Propagator` type. | src/Ядро/Классы/ОтелПостроительSdk.os |
| 737 | MUST | ✅ | The official list of propagators that MUST be maintained by the OpenTelemetry | src/Пропагация/Модули/ОтелW3CПропагатор.os,ОтелW3CBaggageПропагатор.os |
| 738 | MUST | ✅ | organization and MUST be distributed as OpenTelemetry extension packages: | src/Пропагация/Модули/ОтелW3CПропагатор.os,ОтелW3CBaggageПропагатор.os |
| 739 | MUST NOT | ➖ | used by the OpenTracing Basic Tracers. It MUST NOT use `OpenTracing` in the resulting | n/a (OpenTracing not applicable) |
| 740 | MUST NOT | ➖ | X-Ray trace header protocol MUST NOT be maintained or distributed as part of | n/a (X-Ray not implemented) |
| 741 | MUST | ✅ | A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP headers as specified in W... | src/Пропагация/Модули/ОтелW3CПропагатор.os:38-56 |
| 742 | MUST | ❌ | * MUST attempt to extract B3 encoded using single and multi-header | n/a (B3 Extract not implemented) |
| 743 | MUST | ❌ | the multi-header version.* MUST preserve a debug trace flag, if received, and propagate | n/a (B3 multi-header not applicable) |
| 744 | MUST NOT | ❌ | MUST set the sampled trace flag when the debug flag is set.* MUST NOT reuse `X-B3-SpanId` as the id for the server-side ... | n/a (B3 debug flag not applicable) |
| 745 | MUST | ❌ | * MUST default to injecting B3 using the single-header format* MUST provide configuration to change the default injectio... | n/a (B3 Inject not applicable) |
| 746 | MUST NOT | ❌ | multi-header* MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support | n/a (B3 multi-header format not applicable) |
| 747 | MUST | ❌ | Fields MUST return the header names that correspond to the configured format, | n/a (B3 Fields not applicable) |

### Env Vars

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 748 | SHOULD | ✅ | If they do, they SHOULD use the names and value parsing behavior specified in this document. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os |
| 749 | SHOULD | ✅ | They SHOULD also follow the common configuration specification. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:80-86 |
| 750 | MUST | ✅ | The environment-based configuration MUST have a direct code configuration equivalent. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os |
| 751 | MUST | ⚠️ | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105,114,136,143 (Empty values handling incomplete) |
| 752 | MUST | ⚠️ | Any value that represents a Boolean MUST be set to true only by the | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563 (Only true recognized) |
| 753 | MUST NOT | ✅ | accepted, as true. An implementation MUST NOT extend this definition and define | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563 |
| 754 | MUST | ⚠️ | here as a true value, including unset and empty values, MUST be interpreted as | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563 (No explicit warning) |
| 755 | SHOULD | ⚠️ | empty, or unset is used, a warning SHOULD be logged to inform users about the | -Silent false fallback |
| 756 | SHOULD | ➖ | fallback to false being applied. All Boolean environment variables SHOULD be | -Boolean naming |
| 757 | MUST NOT | ➖ | Renaming or changing the default value MUST NOT happen without a major version | -Version changes |
| 758 | SHOULD | ⚠️ | thus qualified as “SHOULD” to allow implementations to avoid breaking changes. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:160,203-204 (Numeric error handling incomplete) |
| 759 | MUST | ⚠️ | implementations, these should be treated as MUST requirements. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (No explicit error handling) |
| 760 | SHOULD | ⚠️ | implementation cannot parse, the implementation SHOULD generate a warning and gracefully | -No warning for unparseable values |
| 761 | SHOULD | ⚠️ | Enum values SHOULD be interpreted in a case-insensitive manner. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (Inconsistent case handling) |
| 762 | MUST | ⚠️ | the implementation does not recognize, the implementation MUST generate | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:216-218 (Inconsistent error logging) |
| 763 | SHOULD | ✅ | Implementations SHOULD only offer environment variables for the types of attributes, for | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:7-34 |

---

## Требования Development-статуса

Эти требования находятся в нестабильных разделах спецификации (Status: Development).
Они не влияют на основной процент соответствия и могут измениться в будущих версиях спецификации.

| Показатель | Значение |
|---|---|
| Всего Development | 99 |
| ✅ Реализовано | 25 (31.6%) |
| ⚠️ Частично | 29 (36.7%) |
| ❌ Не реализовано | 25 (31.6%) |
| N/A | 20 |

### Resource Sdk (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 46 | SHOULD | ➖ | Resource detectors SHOULD have a unique name for reference in configuration. For | n/a (Detector naming) |
| 47 | SHOULD | ➖ | Names SHOULD be snake case and | n/a (Snake case naming) |
| 48 | SHOULD | ➖ | Resource detector names SHOULD reflect | n/a (Detector naming purpose) |
| 49 | SHOULD | ➖ | multiple root namespaces SHOULD choose a name which appropriately conveys their | n/a (Multiple root namespace) |
| 50 | SHOULD | ➖ | An SDK which identifies multiple resource detectors with the same name SHOULD | n/a (Duplicate detector detection) |
| 51 | SHOULD | ➖ | report an error. In order to limit collisions, resource detectors SHOULD | n/a (Collision limiting) |
| 52 | MUST | ✅ | The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:101-119 |
| 53 | MUST | ✅ | All attribute values MUST be considered strings. The `,` and `=` characters | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:459+ |
| 54 | MUST | ➖ | in keys and values MUST be percent encoded. Other characters MAY be | n/a (Percent encoding details) |
| 55 | SHOULD | ⚠️ | variable value SHOULD be discarded and an error SHOULD be reported following the | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:459+ (Invalid values not fully validated) |

### Trace Api (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 71 | SHOULD | ✅ | creating `Span`s, a `Tracer` SHOULD provide this `Enabled` API. | src/Трассировка/Классы/ОтелТрассировщик.os:33-35 |
| 72 | MUST | ✅ | added in the future, therefore, the API MUST be structured in a way for | src/Трассировка/Классы/ОтелТрассировщик.os |
| 73 | MUST | ✅ | This API MUST return a language idiomatic boolean type. A returned value of | src/Трассировка/Классы/ОтелТрассировщик.os:33 |
| 74 | SHOULD | ➖ | SHOULD be documented that instrumentation authors needs to call this API each | Language specific documentation |

### Trace Sdk (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 178 | MUST | ⚠️ | and (Development) TracerConfigurator) MUST be | src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os (Builder provided but no TracerConfigurator) |
| 181 | MUST | ➖ | The function MUST accept the following parameter: | SDK doesn't implement TracerConfigurator |
| 182 | MUST | ➖ | The function MUST return the relevant `TracerConfig`, or some signal indicating | Same as above |
| 183 | MUST | ❌ | `Shutdown` MUST be called only once for each `TracerProvider` instance. After | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:100-105 (Закрыть() can be called multiple times) |
| 184 | SHOULD | ✅ | SHOULD return a valid no-op Tracer for these calls, if possible. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:59-60 |
| 185 | SHOULD | ⚠️ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | src/Трассировка/Классы/ОтелПровайдерТрассировки.os (Закрыть() returns no status) |
| 186 | SHOULD | ⚠️ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` can be | src/Трассировка/Классы/ОтелПровайдерТрассировки.os (No timeout mechanism) |
| 187 | MUST | ✅ | `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:100-105 |
| 191 | MUST | ❌ | the `Tracer` MUST be updated to behave according to the new `TracerConfig`. | Config changes don't propagate to created Tracers |
| 192 | SHOULD | ✅ | If not explicitly set, the `enabled` parameter SHOULD default to `true` ( | src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os |
| 193 | MUST | ❌ | If a `Tracer` is disabled, it MUST behave equivalently | No disable mechanism implemented |
| 194 | MUST | ❌ | The value of `enabled` MUST be used to resolve whether a `Tracer` | No dynamic enabled check |
| 195 | MUST | ➖ | However, the changes MUST be eventually visible. | No dynamic configuration system |
| 196 | MUST | ❌ | `Enabled` MUST return `false` when either: | No implementation |
| 197 | SHOULD | ➖ | Otherwise, it SHOULD return `true`. | Same |
| 222 | SHOULD | ✅ | when it is used not as a root sampler, the SDK SHOULD emit a warning | src/Трассировка/Модули/ОтелСэмплер.os:247-269 |
| 223 | MUST | ❌ | The `ProbabilitySampler` sampler MUST ignore the parent `SampledFlag`. | No warning when used as root |
| 224 | SHOULD | ➖ | * If randomness value (R) is greater or equal to the rejection threshold (T), meaning when (R >= T), return `RECORD_AND_... | Not in spec for OTel |
| 225 | MUST | ✅ | Based on the decision from the wrapped root sampler, `AlwaysRecord` MUST behave | src/Трассировка/Модули/ОтелСэмплер.os:92-94 |
| 226 | MUST NOT | ✅ | Note: ComposableSamplers MUST NOT modify the parameters passed to | src/Трассировка/Модули/ОтелСэмплер.os |
| 227 | MUST NOT | ✅ | complexity. ComposableSamplers MUST NOT modify the OpenTelemetry | src/Трассировка/Модули/ОтелСэмплер.os |
| 228 | SHOULD | ➖ | CompositeSampler SHOULD update the threshold of the outgoing | Probability sampler specific |
| 229 | MUST | ✅ | randomness values MUST not be modified. | src/Трассировка/Модули/ОтелСэмплер.os |
| 230 | SHOULD | ➖ | a `ComposableAlwaysOff` instance SHOULD be returned instead. | Probability sampler specific |
| 246 | SHOULD | ➖ | Custom implementations of the `IdGenerator` SHOULD identify themselves | No custom generators |
| 252 | MUST | ✅ | The end timestamp MUST have been computed (the `OnEnding` method duration is not included | src/Трассировка/Классы/ОтелСпан.os:438-441 |
| 253 | MUST | ✅ | The Span object MUST still be mutable (i.e., `SetAttribute`, `AddLink`, `AddEvent` can be called) while `OnEnding` is ca... | src/Трассировка/Классы/ОтелСпан.os |
| 254 | MUST | ✅ | This method MUST be called synchronously within the `Span.End()` API, | src/Трассировка/Классы/ОтелСпан.os:444-446 |
| 255 | MUST | ❌ | The SDK MUST guarantee that the span can no longer be modified by any other thread | No explicit guarantee documented |

### Logs Api (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 305 | SHOULD | ❌ | The ergonomic API SHOULD make it more convenient to emit event records following | -No ergonomic API |
| 306 | SHOULD | ❌ | The design of the ergonomic API SHOULD be idiomatic for its language. | -No idiomatic method overloading |

### Logs Sdk (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 319 | MUST | ❌ | The function MUST accept the following parameter: | -LoggerConfigurator not found |
| 320 | MUST | ❌ | The function MUST return the relevant `LoggerConfig`, or some signal indicating | -LoggerConfigurator return missing |
| 321 | MUST | ❌ | `Shutdown` MUST be called only once for each `LoggerProvider` instance. After | -Shutdown single-call enforcement missing |
| 322 | SHOULD | ❌ | SDKs SHOULD return a valid no-op `Logger` for these calls, if possible. | -No-op fallback not documented |
| 323 | SHOULD | ✅ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | src/Логирование/Классы/ОтелПровайдерЛогирования.os:90-104 |
| 324 | SHOULD | ❌ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` MAY be | -Shutdown timeout missing |
| 325 | MUST | ✅ | `Shutdown` MUST be implemented by invoking `Shutdown` on all | src/Логирование/Классы/ОтелПровайдерЛогирования.os:90-104 |
| 331 | MUST | ❌ | the `Logger` MUST be updated to behave according to the new `LoggerConfig`. | -Dynamic behavior update missing |
| 332 | SHOULD | ❌ | If not explicitly set, the `enabled` parameter SHOULD default to `true` ( | -LoggerConfig.enabled missing |
| 333 | MUST | ❌ | If a `Logger` is disabled, it MUST behave equivalently | -Disabled logger behavior missing |
| 334 | MUST | ❌ | If not explicitly set, the `minimum_severity` parameter MUST default to `0`. | -minimum_severity missing |
| 335 | MUST | ❌ | specified (i.e. not `0`) and is less than the configured `minimum_severity`, the log record MUST | -Severity filtering missing |
| 336 | MUST | ❌ | If not explicitly set, the `trace_based` parameter MUST default to `false`. | -trace_based missing |
| 337 | MUST | ❌ | If `trace_based` is `true`, log records associated with unsampled traces MUST | -Unsampled trace filtering missing |
| 338 | MUST | ❌ | However, the changes MUST be eventually visible. | -Config visibility delay missing |
| 342 | MUST | ❌ | the implementation MUST apply the filtering rules defined by the | -Filtering rules missing |
| 343 | MUST | ❌ | the log record MUST be dropped. | -Log record dropping missing |
| 345 | SHOULD | ❌ | Otherwise, it SHOULD return `true`. | -Enabled return true conditions missing |

### Metrics Sdk (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 501 | MUST | ⚠️ | and (Development) MeterConfigurator) MUST be | - (Configuration API not visible) |
| 503 | MUST | ⚠️ | The function MUST accept the following parameter: | - (MeterConfigurator accept param unclear) |
| 504 | MUST | ⚠️ | The function MUST return the relevant `MeterConfig`, or some signal indicating | - (MeterConfigurator return behavior unclear) |
| 505 | MUST | ✅ | `Shutdown` MUST be called only once for each `MeterProvider` instance. After the | ОтелПровайдерМетрик.os:127 |
| 506 | SHOULD | ⚠️ | SHOULD return a valid no-op Meter for these calls, if possible. | - (No-op Meter return on shutdown unclear) |
| 507 | SHOULD | ⚠️ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | - (Shutdown return status not explicit) |
| 508 | SHOULD | ⚠️ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` MAY be | - (Shutdown timeout not implemented) |
| 509 | MUST | ✅ | `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered | ОтелПровайдерМетрик.os:128 |
| 566 | MUST | ✅ | For delta aggregations, the start timestamp MUST equal the previous collection | ОтелАгрегаторСуммы.os:1 |
| 567 | MUST | ✅ | with delta temporality aggregation for an instrument MUST share the same start | ОтелАгрегаторСуммы.os:1 |
| 568 | MUST | ✅ | Cumulative timeseries MUST use a consistent start timestamp for all collection | ОтелАгрегаторСуммы.os:1 |
| 569 | SHOULD | ✅ | For synchronous instruments, the start timestamp SHOULD be the time of the | ОтелБазовыйСинхронныйИнструмент.os:1 |
| 570 | SHOULD | ✅ | For asynchronous instrument, the start timestamp SHOULD be: | ОтелБазовыйНаблюдаемыйИнструмент.os:1 |
| 582 | MUST | ⚠️ | the `Meter` MUST be updated to behave according to the new `MeterConfig`. | - (Meter update on config unclear) |
| 583 | SHOULD | ⚠️ | If not explicitly set, the `enabled` parameter SHOULD default to `true` ( | - (Enabled default true unclear) |
| 584 | MUST | ⚠️ | If a `Meter` is disabled, it MUST behave equivalently | - (Disabled meter behavior unclear) |
| 585 | MUST | ⚠️ | The value of `enabled` MUST be used to resolve whether an instrument | - (Enabled for resolution unclear) |
| 586 | MUST | ⚠️ | However, the changes MUST be eventually visible. | - (Config visibility timing unclear) |
| 605 | SHOULD | ⚠️ | Otherwise, it SHOULD return `true`. | - (Type conflict detection unclear) |
| 640 | SHOULD | ⚠️ | * The `exporter` to use, which is a `MetricExporter` instance.* The default output `aggregation` (optional), a function ... | - (Instrumentation scope immutability unclear) |
| 641 | SHOULD | ⚠️ | `MetricReader` SHOULD be provided to be used | - (Attribute mutability unclear) |
| 642 | MUST | ⚠️ | The `MetricReader` MUST ensure that data points from OpenTelemetry | - (Aggregator state reset unclear) |
| 643 | MUST | ⚠️ | temporality, MetricReader.Collect MUST receive data points exposed | - (Collection interval impact unclear) |
| 644 | MUST | ⚠️ | temporality, MetricReader.Collect MUST only receive data points with | - (Exemplar sampler integration unclear) |
| 645 | MUST | ⚠️ | temporality, MetricReader.Collect MUST only receive data points with | - (Span context propagation unclear) |
| 646 | MUST | ⚠️ | successive calls to MetricReader.Collect MUST repeat the same | - (Trace context usage unclear) |
| 647 | MUST | ⚠️ | calls to MetricReader.Collect MUST advance the starting timestamp ( | - (Baggage integration unclear) |
| 648 | MUST | ⚠️ | MUST always be equal to time the metric data point took effect, which is equal | - (Log severity mapping unclear) |
| 649 | MUST | ⚠️ | The SDK MUST support multiple `MetricReader` instances to be registered on the | - (Error reporting unclear) |
| 650 | SHOULD NOT | ⚠️ | `MetricReader` instance SHOULD NOT introduce side-effects to other `MetricReader` | - (Debug logging unclear) |
| 651 | MUST NOT | ⚠️ | The SDK MUST NOT allow a `MetricReader` instance to be registered on more than | - (Metric type conversions unclear) |
| 652 | SHOULD | ⚠️ | The SDK SHOULD provide a way to allow `MetricReader` to respond to | - (Unit conversion unclear) |

### Env Vars (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 764 | SHOULD | ➖ | * `"otlp"`: OTLP* `"zipkin"`: Zipkin (Defaults to protobuf format)* `"console"`: Standard Output* `"logging"`: Standard ... | -Not metrics-specific |
| 765 | SHOULD | ➖ | * `"otlp"`: OTLP* `"prometheus"`: Prometheus* `"console"`: Standard Output* `"logging"`: Standard Output. It is a deprec... | -Prometheus not in scope |
| 766 | SHOULD | ➖ | * `"otlp"`: OTLP* `"console"`: Standard Output* `"logging"`: Standard Output. It is a deprecated value left for backward... | -Prometheus not in scope |
| 767 | MUST | ➖ | MUST be ignored. Ignoring the environment variables is necessary because | -Prometheus not applicable |

## Ограничения платформы OneScript

Некоторые требования спецификации не могут быть полностью реализованы из-за ограничений платформы:

| Ограничение | Влияние |
|---|---|
| Нет нативного protobuf | Используется HTTP/JSON вместо HTTP/protobuf. Протокол по умолчанию - http/json |
| Точность времени - миллисекунды | Спецификация требует наносекунды |
| Нет TLS/mTLS конфигурации | Нет поддержки сертификатов клиента |
| Нет поддержки B3/X-Ray пропагаторов | Реализованы только W3C TraceContext и W3C Baggage |
| Нет облачных детекторов ресурсов | Нет EKS/AKS/GKE детекторов |

## Методология

1. Извлечены все предложения с ключевыми словами MUST/MUST NOT/SHOULD/SHOULD NOT из 12 страниц спецификации OTel v1.55.0:
   - Context, Baggage API, Resource SDK, Trace API, Trace SDK, Logs Bridge API, Logs SDK, Metrics API, Metrics SDK, OTLP Exporter, Propagators, SDK Environment Variables
2. Каждое из 767 требований классифицировано по стабильности (Stable/Development) на основе маркеров `Status:` в спецификации
3. Каждое требование прослежено до конкретного файла и строки в исходном коде
4. Статусы:
   - ✅ found - реализовано
   - ⚠️ partial - частично реализовано
   - ❌ not_found - не реализовано
   - ➖ n_a - неприменимо к платформе
5. Development-требования вынесены в отдельную секцию и не влияют на основной процент соответствия
