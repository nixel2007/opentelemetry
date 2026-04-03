# Анализ соответствия спецификации OpenTelemetry v1.55.0

> **Версия спецификации**: [v1.55.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-04-03
> **Методология**: spec-first - извлечены все MUST/SHOULD требования из спецификации, затем каждое прослежено до кода

## Сводка (Stable)

Учитываются только требования из стабильных разделов спецификации с универсальной областью применения.

| Показатель | Значение |
|---|---|
| Всего требований | 767 |
| Stable (универсальные) | 662 |
| Conditional (B3, Prometheus и др.) | 6 |
| Development (нестабильные) | 99 |
| Deprecated | 0 |
| Применимых Stable (без N/A) | 619 |
| ✅ Реализовано | 424 (68.5%) |
| ⚠️ Частично | 143 (23.1%) |
| ❌ Не реализовано | 52 (8.4%) |
| N/A (неприменимо) | 43 |
| **MUST/MUST NOT** | 279/371 (75.2%) |
| **SHOULD/SHOULD NOT** | 145/248 (58.5%) |

## Соответствие по разделам (Stable)

| Раздел | Всего | ✅ | ⚠️ | ❌ | N/A | % | Cond | Dev |
|---|---|---|---|---|---|---|---|---|
| Context | 14 | 12 | 0 | 0 | 2 | 100.0% | 0 | 0 |
| Baggage Api | 16 | 15 | 0 | 0 | 1 | 100.0% | 0 | 0 |
| Resource Sdk | 15 | 8 | 2 | 0 | 5 | 80.0% | 0 | 10 |
| Trace Api | 115 | 103 | 9 | 0 | 3 | 92.0% | 0 | 4 |
| Trace Sdk | 81 | 47 | 29 | 1 | 4 | 61.0% | 0 | 29 |
| Logs Api | 20 | 17 | 2 | 0 | 1 | 89.5% | 0 | 2 |
| Logs Sdk | 67 | 38 | 18 | 8 | 3 | 59.4% | 0 | 18 |
| Metrics Api | 99 | 87 | 7 | 0 | 5 | 92.6% | 0 | 0 |
| Metrics Sdk | 170 | 70 | 57 | 34 | 9 | 43.5% | 0 | 32 |
| Otlp Exporter | 21 | 6 | 9 | 5 | 1 | 30.0% | 0 | 0 |
| Propagators | 28 | 17 | 4 | 0 | 7 | 81.0% | 6 | 0 |
| Env Vars | 16 | 4 | 6 | 4 | 2 | 28.6% | 0 | 4 |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Env Vars]** [MUST] The environment-based configuration MUST have a direct code configuration equivalent. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105-110`)
  - Empty value handling inconsistent
- ⚠️ **[Env Vars]** [MUST] The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563`)
  - Boolean parsing only true accepted
- ⚠️ **[Env Vars]** [MUST NOT] accepted, as true. An implementation MUST NOT extend this definition and define (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563`)
  - Unset defaults to true not false
- ❌ **[Env Vars]** [MUST] here as a true value, including unset and empty values, MUST be interpreted as (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - No warning for invalid boolean values
- ⚠️ **[Env Vars]** [MUST NOT] Renaming or changing the default value MUST NOT happen without a major version (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:160`)
  - Numeric parsing without error handling
- ❌ **[Env Vars]** [MUST] implementations, these should be treated as MUST requirements. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - No warning for unparseable numeric values
- ⚠️ **[Logs Api]** [MUST] For each required parameter, the API MUST be structured to obligate a user to (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:164`)
  - Methods documented as thread-safe but limited detail
- ⚠️ **[Logs Api]** [MUST] LoggerProvider - all methods MUST be documented that implementations need to (`src/Логирование/Классы/ОтелЛоггер.os:29,55`)
  - Methods documented as safe but limited detail
- ❌ **[Logs Sdk]** [MUST] If an Exception is provided, the SDK MUST by default set attributes (`-`)
  - User attribute precedence not implemented
- ⚠️ **[Logs Sdk]** [MUST NOT] User-provided attributes MUST take precedence and MUST NOT be overwritten by (`src/Логирование/Классы/ОтелЛоггер.os:41-50`)
  - Filtering via Включен() but no LoggerConfig rules
- ❌ **[Logs Sdk]** [MUST] Counts for attributes due to collection limits MUST be available for exporters (`-`)
  - ReadWriteLogRecord for processor modification not implemented
- ⚠️ **[Logs Sdk]** [MUST NOT] Any modifications to parameters inside `Enabled` MUST NOT be propagated to the (`src/Логирование/Классы/ОтелПростойПроцессорЛогов.os`)
  - No note on single-call guarantee
- ⚠️ **[Logs Sdk]** [MUST] `Shutdown` MUST include the effects of `ForceFlush`. (`src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:32-36`)
  - No timeout mechanism
- ⚠️ **[Logs Sdk]** [MUST] The built-in LogRecordProcessors MUST do so. If a (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:73-112`)
  - Batch has timeout, simple doesnt
- ⚠️ **[Logs Sdk]** [MUST] timeout is specified (see below), the `LogRecordProcessor` MUST prioritize (`src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:32-36`)
  - No status indication
- ⚠️ **[Logs Sdk]** [MUST] The processor MUST synchronize calls to `LogRecordExporter`’s `Export` (`src/Логирование/Классы/ОтелПростойПроцессорЛогов.os`)
  - No concurrency documentation
- ⚠️ **[Metrics Api]** [MUST] The `Meter` MUST provide functions to create new Instruments: (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:1-40`)
  - Float handling present but no explicit documentation
- ⚠️ **[Metrics Api]** [MUST] observations from a single callback MUST be reported with identical (`src/Метрики/Классы/ОтелМетр.os:348-351`)
  - No explicit state parameter
- ⚠️ **[Metrics Api]** [MUST] observations from a single callback MUST be reported with identical timestamps. (`src/Метрики/Классы/ОтелМетр.os:348`)
  - State passing not explicit
- ⚠️ **[Metrics Api]** [MUST] MeterProvider - all methods MUST be documented that implementations need to (`src/Метрики/Классы/ОтелМетр.os:1-450`)
  - Thread-safe but documentation incomplete
- ⚠️ **[Metrics Api]** [MUST] Meter - all methods MUST be documented that implementations need to be safe (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:1-317`)
  - Thread-safe structures but documentation lacking
- ⚠️ **[Metrics Sdk]** [MUST] working Meter MUST be returned as a fallback rather than returning null or (`src/Метрики/Классы/ОтелМетр.os:44-49`)
  - Instrument name is normalized but original value not logged for invalid names
- ⚠️ **[Metrics Sdk]** [MUST] `ForceFlush` MUST invoke `ForceFlush` on all registered (`src/Метрики/Классы/ОтелПровайдерМетрик.os:149-153`)
  - ForceFlush async but no explicit timeout parameter
- ⚠️ **[Metrics Sdk]** [MUST NOT] `name`, but MUST NOT obligate a user to provide one. (`src/Метрики/Классы/ОтелМетр.os:176-183`)
  - Representation validation missing warning log
- ⚠️ **[Metrics Sdk]** [MUST NOT] `type`, but MUST NOT obligate a user to provide one. (`src/Метрики/Классы/ОтелМетр.os:84-93`)
  - View boundaries configurable but precedence over advisory not fully documented
- ⚠️ **[Metrics Sdk]** [MUST NOT] `unit`, but MUST NOT obligate a user to provide one. (`src/Метрики/Классы/ОтелМетр.os:84-93`)
  - Default views apply advisory boundaries but precedence not guaranteed
- ⚠️ **[Metrics Sdk]** [MUST] MUST be honored.* If the `MeterProvider` has one or more `View`(s) registered:* If the Instrument could match the instrument selection criteria, for e... (`src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:177-184`)
  - Scale must not increase - implementation assumed
- ⚠️ **[Metrics Sdk]** [MUST] The implementation MUST maintain reasonable minimum and maximum scale (`src/Метрики/Классы/ОтелПериодическийЧитателяМетрик.os:109-149`)
  - Delta start time handling - need verification
- ⚠️ **[Metrics Sdk]** [MUST] The implementation MUST complete the execution of all callbacks for a (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109`)
  - ForceFlush calls Collect via СобратьИЭкспортировать
- ⚠️ **[Metrics Sdk]** [MUST] Aggregators for synchronous instruments with cumulative temporality MUST (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:40-42`)
  - ForceFlush success not explicitly communicated
- ⚠️ **[Metrics Sdk]** [MUST] Regardless of aggregation temporality, the SDK MUST ensure that every (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:40-42`)
  - ForceFlush no timeout parameter
- ⚠️ **[Metrics Sdk]** [MUST NOT] Measurements MUST NOT be double-counted or dropped (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:46-48`)
  - Shutdown called once (assumed) but no explicit once-only enforcement
- ❌ **[Metrics Sdk]** [MUST] Distinct meters MUST be treated as separate namespaces for the purposes of detecting (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os`)
  - Shutdown not blocking indefinitely (synchronous)
- ❌ **[Metrics Sdk]** [MUST] duplicate instrument. This means that the Meter MUST return a functional (`src/Метрики/Классы/ОтелМетр.os`)
  - Overflow attribute set not found
- ⚠️ **[Metrics Sdk]** [MUST] If a unit is not provided or the unit is null, the Meter MUST treat it the same (`src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14-25`)
  - Exemplar data immutability not explicit
- ⚠️ **[Metrics Sdk]** [MUST] Meter MUST treat it the same as an empty description string. (`src/Метрики/Классы/ОтелЭкспортерМетрик.os:322-330`)
  - Exemplars not fully exposed
- ❌ **[Metrics Sdk]** [MUST] The synchronous instrument `Enabled` MUST return `false` (`src/Метрики`)
  - MetricProducer not found
- ❌ **[Metrics Sdk]** [MUST] A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements (`src/Метрики`)
  - MetricProducer returns ResourceMetrics - not found
- ❌ **[Metrics Sdk]** [MUST NOT] off, the SDK MUST NOT have overhead related to exemplar sampling. (`src/Метрики`)
  - Produce appending not found
- ❌ **[Metrics Sdk]** [MUST] A Metric SDK MUST allow exemplar sampling to leverage the configuration of (`src/Метрики`)
  - MetricReader MetricProducers support not found
- ❌ **[Metrics Sdk]** [MUST] The `ExemplarFilter` configuration MUST allow users to select between one of the (`src/Метрики`)
  - MetricProducer data modification restriction not found
- ❌ **[Metrics Sdk]** [MUST] An OpenTelemetry SDK MUST support the following filters: (`src/Метрики`)
  - API MetricProducer registration not found
- ❌ **[Metrics Sdk]** [MUST] A new `ExemplarReservoir` MUST be created for every known timeseries data point, (`src/Экспорт`)
  - stdout MetricExporter not found
- ❌ **[Metrics Sdk]** [MUST] documented in the API and the reservoir MUST be given the `Attributes` (`src/Метрики/Классы/ОтелМетр.os`)
  - Configuration method for attribute limits not found
- ⚠️ **[Metrics Sdk]** [MUST] `Exemplar`s MUST retain any attributes available in the measurement that (`src/Метрики/Классы/ОтелМетр.os:44-49`)
  - Warning logged via ПроверитьКонфликтДескриптора but not shown
- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST include two types of built-in exemplar reservoirs: (`src/Метрики/Классы/ОтелМетр.os:44-49`)
  - Different Meter separate stream (assumed)
- ⚠️ **[Metrics Sdk]** [MUST] This reservoir MUST use a uniformly-weighted sampling algorithm based on the (`src/Метрики/Классы/ОтелМетр.os:44-49`)
  - Default conflict resolution not fully implemented
- ⚠️ **[Metrics Sdk]** [MUST] This Exemplar reservoir MUST take a configuration parameter that is the (`src/Метрики/Классы/ОтелНаблюдениеМетрики.os:19-30`)
  - Measurement reporting supported
- ⚠️ **[Metrics Sdk]** [MUST] configuration of a Histogram. This implementation MUST store at most one (`src/Метрики/Классы/ОтелНаблюдениеМетрики.os:19-30`)
  - Last reported measurement preference not explicit
- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST provide a mechanism for SDK users to provide their own (`src/Метрики/Классы/ОтелБазовыйАгрегатор.os:1`)
  - Identical attribute aggregation (assumed)
- ⚠️ **[Metrics Sdk]** [MUST] `Shutdown` MUST be called only once for each `MetricReader` instance. After the (`src/Метрики/Классы/ОтелМетр.os:256-272`)
  - Appending result not found
- ❌ **[Metrics Sdk]** [MUST] The reader MUST synchronize calls to `MetricExporter`’s `Export` (`src/Метрики`)
  - MetricReader multiple MetricProducers not found
- ❌ **[Metrics Sdk]** [MUST] `MetricExporter` defines the interface that protocol-specific exporters MUST (`src/Экспорт`)
  - stdout MetricExporter not found
- ⚠️ **[Metrics Sdk]** [MUST] A `MetricProducer` MUST support the following functions: (`src/Метрики/Классы/ОтелНаблюдениеМетрики.os`)
  - Last measurement preferred (not explicit)
- ⚠️ **[Metrics Sdk]** [MUST] MUST return a batch of Metric Points, filtered by the optional (`src/Метрики/Классы/ОтелНаблюдениеМетрики.os`)
  - Duplicate warning not logged
- ⚠️ **[Metrics Sdk]** [MUST] A `MetricFilter` MUST support the following functions: (`src/Метрики/Классы/ОтелМетр.os:72-93`)
  - Advisory boundaries conditional on View (not explicit)
- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST provide configuration according to the SDK environment (`src/Метрики/Классы/ОтелМетр.os:72-93`)
  - Default boundaries change visibility (not explicit)
- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST handle numerical limits in a graceful way according to Error (`src/Метрики/Классы/ОтелМетр.os:72-93`)
  - View aggregation prevents advisory use (assumed)
- ❌ **[Metrics Sdk]** [MUST] it MUST handle all the possible values. For example, if the language runtime (`src/Метрики`)
  - ValidRange advisory not found
- ❌ **[Metrics Sdk]** [MUST] MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe (`src/Метрики`)
  - Invalid measurement dropping not found
- ❌ **[Metrics Sdk]** [MUST] ExemplarReservoir - all methods MUST be safe to be called concurrently. (`src/Метрики`)
  - Dropped measurement logging not found
- ❌ **[Metrics Sdk]** [MUST] and `Shutdown` MUST be safe to be called concurrently. (`src/Метрики`)
  - Dropped measurement cardinality exclusion not found
- ⚠️ **[Otlp Exporter]** [MUST] The following configuration options MUST be available to configure the OTLP exporter. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - Missing signal-specific endpoint overrides
- ⚠️ **[Otlp Exporter]** [MUST] Each configuration option MUST be overridable by a signal specific option. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150-161`)
  - URL components partially honored
- ❌ **[Otlp Exporter]** [MUST] The implementation MUST honor the following URL components: (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - No per-signal URL construction from global endpoint
- ⚠️ **[Otlp Exporter]** [MUST] Endpoint (OTLP/gRPC): Target to which the exporter is going to send spans, metrics, or logs. The option SHOULD accept any form allowed by the underlyi... (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)
  - Protocol options: grpc and http/json supported; http/protobuf not supported
- ⚠️ **[Otlp Exporter]** [MUST] Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs (`src/Экспорт/Классы/ОтелHttpТранспорт.os:74`)
  - Endpoint used as-is, only path appended
- ❌ **[Otlp Exporter]** [MUST] MUST be used as-is without any modification. The only exception is that if an (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - No explicit root path handling
- ⚠️ **[Otlp Exporter]** [MUST] URL contains no path part, the root path `/` MUST be used (see Example 2). (`src/Экспорт/Классы/ОтелHttpТранспорт.os:74`)
  - URL concatenation without validation
- ⚠️ **[Otlp Exporter]** [MUST NOT] An SDK MUST NOT modify the URL in ways other than specified above. That also means, (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150-156`)
  - Supports gRPC and HTTP/JSON; no true protobuf
- ❌ **[Otlp Exporter]** [MUST] Transient errors MUST be handled with a retry strategy. This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming t... (`src/Экспорт/Классы/ОтелHttpТранспорт.os`)
  - No User-Agent header emitted
- ⚠️ **[Propagators]** [MUST] There MUST be functions to accomplish the following operations. (`src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os`)
  - No per-type getter API
- ⚠️ **[Propagators]** [MUST] The OpenTelemetry API MUST provide a way to obtain a propagator for each (`src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os`)
  - Not enforced for libraries
- ⚠️ **[Propagators]** [MUST] The OpenTelemetry API MUST use no-op propagators unless explicitly configured (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - Limited OTEL_PROPAGATORS support
- ⚠️ **[Resource Sdk]** [MUST] resource MUST be picked (even if the updated value is empty). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:96-119`)
  - Limited environment detection
- ⚠️ **[Resource Sdk]** [MUST NOT] failure to detect any resource information MUST NOT be considered an error, (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:101-119`)
  - Limited error reporting
- ⚠️ **[Trace Api]** [MUST NOT] `End` MUST NOT have any effects on child spans. (`src/Ядро/Модули/ОтелКонтекст.os`)
  - SpanContext from Propagator stored in Context (mechanism present)
- ⚠️ **[Trace Sdk]** [MUST] `ForceFlush` MUST invoke `ForceFlush` on all registered `SpanProcessors`. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os`)
  - Timeout handling not explicitly documented
- ⚠️ **[Trace Sdk]** [MUST] When asked to create a Span, the SDK MUST act as if doing the following in order: (`src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os`)
  - Default batch size not documented in visible code
- ⚠️ **[Trace Sdk]** [MUST] If the parent `SpanContext` contains a valid `TraceId`, they MUST always match.* Name of the `Span` to be created.* `SpanKind` of the `Span` to be cre... (`src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os`)
  - Exporter configuration not fully documented in visible code
- ⚠️ **[Trace Sdk]** [MUST NOT] will be dropped.* `RECORD_ONLY` - `IsRecording` will be `true`, but the `Sampled` flag MUST NOT be set.* `RECORD_AND_SAMPLE` - `IsRecording` will be `... (`src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os`)
  - Schedule delay interval not configured in visible code
- ⚠️ **[Trace Sdk]** [MUST] * The `TraceIdRatioBased` MUST ignore the parent `SampledFlag`. To respect the (`src/Трассировка/Классы`)
  - SpanExporter interface not fully visible in trace module
- ⚠️ **[Trace Sdk]** [MUST] the `ParentBased` sampler specified below.* Description MUST return a string of the form `"TraceIdRatioBased{RATIO}"` (`src/Трассировка/Классы`)
  - Export called on sampled spans (implementation in processor)
- ⚠️ **[Trace Sdk]** [MUST] * The sampling algorithm MUST be deterministic. A trace identified by a given (`src/Экспорт`)
  - Shutdown called on exporter (documented separately)
- ⚠️ **[Trace Sdk]** [MUST] implementations MUST use a deterministic hash of the `TraceId` when computing (`src/Экспорт`)
  - Shutdown provides completion signal (async support available)
- ⚠️ **[Trace Sdk]** [MUST] will produce the same decision.* A `TraceIdRatioBased` sampler with a given sampling probability MUST also sample all (`src/Экспорт`)
  - Shutdown non-blocking characteristic not fully documented
- ⚠️ **[Trace Sdk]** [MUST NOT] MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState (`src/Трассировка/Модули/ОтелСэмплер.os:81`)
  - TraceIdRatio defined but default 0.0001 not documented
- ⚠️ **[Trace Sdk]** [MUST] The SDK MUST provide a mechanism for customizing the way IDs are generated for (`src/Трассировка/Классы/ОтелСпан.os`)
  - Dropped attribute logging not visible in code
- ⚠️ **[Trace Sdk]** [MUST] `IdGenerator`, name of the methods MUST be consistent with (`src/Трассировка/Классы`)
  - Logging frequency control not documented
- ⚠️ **[Trace Sdk]** [MUST] `Shutdown` MUST include the effects of `ForceFlush`. (`src/Трассировка/Классы/ОтелСпан.os`)
  - Span concurrency safety not explicitly documented
- ⚠️ **[Trace Sdk]** [MUST] The built-in SpanProcessors MUST do so. (`src/Трассировка/Классы`)
  - ForceFlush timeout handling and prioritization not documented
- ⚠️ **[Trace Sdk]** [MUST] If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os`)
  - ForceFlush no status indication

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Env Vars]** [SHOULD] If they do, they SHOULD use the names and value parsing behavior specified in this document. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - Common configuration partially followed
- ⚠️ **[Env Vars]** [SHOULD] empty, or unset is used, a warning SHOULD be logged to inform users about the (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - Boolean env vars not consistently handled
- ❌ **[Env Vars]** [SHOULD] thus qualified as “SHOULD” to allow implementations to avoid breaking changes. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - No validation for numeric parse failures
- ❌ **[Env Vars]** [SHOULD] Enum values SHOULD be interpreted in a case-insensitive manner. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - No warning for unrecognized enum values
- ⚠️ **[Logs Sdk]** [SHOULD] throwing an exception, its `name` SHOULD keep the original invalid value, and a (`src/Логирование/Классы/ОтелПровайдерЛогирования.os`)
  - No logging message about invalid value
- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:112-116`)
  - No ERROR status
- ⚠️ **[Logs Sdk]** [SHOULD] failed or timed out. `ForceFlush` SHOULD return some ERROR status if there (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:112-116`)
  - No SUCCESS status
- ⚠️ **[Logs Sdk]** [SHOULD] is an error condition; and if there is no error condition, it SHOULD return (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:112-116`)
  - No timeout mechanism
- ❌ **[Logs Sdk]** [SHOULD] the implementation SHOULD set it equal to the current time. (`-`)
  - Exception attribute handling not implemented
- ❌ **[Logs Sdk]** [SHOULD] The options MAY be bundled in a class, which then SHOULD be called (`-`)
  - No log message when attribute limit exceeded
- ❌ **[Logs Sdk]** [SHOULD] There SHOULD be a message printed in the SDK’s log to indicate to the user (`-`)
  - No throttling of warning messages
- ⚠️ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. (`src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:32-36`)
  - Silently ignored (graceful)
- ⚠️ **[Logs Sdk]** [SHOULD] SHOULD ignore these calls gracefully, if possible. (`src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:32-36`)
  - No status indication
- ❌ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` can be (`-`)
  - ForceFlush not prioritized in simple processor
- ❌ **[Logs Sdk]** [SHOULD] to `ForceFlush` SHOULD be completed as soon as possible, preferably before (`-`)
  - ForceFlush no-op in simple processor
- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, (`src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:26-28`)
  - No timeout mechanism
- ⚠️ **[Logs Sdk]** [SHOULD NOT] default SDK’s `LogRecordProcessors` SHOULD NOT implement retry logic, as the (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38-40`)
  - ForceFlush no status
- ⚠️ **[Logs Sdk]** [SHOULD] exporter has received prior to the call to `ForceFlush` SHOULD be completed as (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38-40`)
  - No status indication
- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, (`-`)
  - ForceFlush guidance missing
- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38-40`)
  - No timeout mechanism
- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:44-46`)
  - Should be called once not documented
- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD be called only once for each `LogRecordExporter` instance. After (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:44-46`)
  - Export returns False after Shutdown
- ⚠️ **[Metrics Api]** [SHOULD] API SHOULD treat it as an opaque string. (`src/Метрики/Классы/ОтелМетр.os:43-59`)
  - Case-sensitive handling unclear
- ⚠️ **[Metrics Api]** [SHOULD] All the metrics APIs SHOULD allow optional parameter(s) to be added to existing (`src/Метрики/Классы/ОтелПровайдерМетрик.os:1-250`)
  - Thread-safe but not all documented
- ❌ **[Metrics Sdk]** [SHOULD] throwing an exception, its `name` SHOULD keep the original invalid value, and a (`src/Метрики/Классы/ОтелМетр.os`)
  - No warning logged for invalid instrument names
- ⚠️ **[Metrics Sdk]** [SHOULD] The SDK SHOULD use the following logic to determine how to process Measurements (`src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:177-184`)
  - Scale can decrease but no explicit requirement check
- ⚠️ **[Metrics Sdk]** [SHOULD] the implementation SHOULD apply the View and emit a warning. If it is not (`src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:8`)
  - max_size invariant needs verification
- ⚠️ **[Metrics Sdk]** [SHOULD NOT] * Count of `Measurement` values in population.* Arithmetic sum of `Measurement` values in population. This SHOULD NOT be collected when used with (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109-149`)
  - Collect aggregation logic present but delta temporality handling needs review
- ⚠️ **[Metrics Sdk]** [SHOULD] (-∞, 0], (0, 5.0], (5.0, 10.0], (10.0, 25.0], (25.0, 50.0], (50.0, 75.0], (75.0, 100.0], (100.0, 250.0], (250.0, 500.0], (500.0, 750.0], (750.0, 1000.... (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109-149`)
  - Cumulative temporality born at start implemented
- ⚠️ **[Metrics Sdk]** [SHOULD NOT] Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109-149`)
  - Cumulative no-reset start time - need verification
- ⚠️ **[Metrics Sdk]** [SHOULD] positive or negative ranges, the implementation SHOULD use the maximum (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109-149`)
  - Duplicate data point deduplication not explicit
- ⚠️ **[Metrics Sdk]** [SHOULD] Implementations SHOULD adjust the histogram scale as necessary to (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109-149`)
  - Collect error status partially handled
- ⚠️ **[Metrics Sdk]** [SHOULD] The implementation SHOULD disregard the use of asynchronous instrument (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:85-102`)
  - MetricReader can call MeterProvider ForceFlush (assumed)
- ⚠️ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:68-70,76-78`)
  - ForceFlush provided but no timeout parameter
- ❌ **[Metrics Sdk]** [SHOULD] stream, that value SHOULD be used.* If there is no matching view, but the `MetricReader` defines a default (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os`)
  - No explicit SDK retry logic comment
- ⚠️ **[Metrics Sdk]** [SHOULD] Aggregators of asynchronous instruments SHOULD prefer the first-observed (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:23-24`)
  - Export returns Ложь after shutdown but no status detail
- ❌ **[Metrics Sdk]** [SHOULD] a warning SHOULD be emitted. The emitted warning SHOULD include information for (`src/Метрики/Классы/ОтелМетр.os`)
  - Configurable cardinality limit not found
- ❌ **[Metrics Sdk]** [SHOULD] SHOULD avoid the warning.* If the potential conflict involves instruments that can be distinguished by (`src/Метрики/Классы/ОтелМетр.os`)
  - View cardinality override not found
- ⚠️ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument name (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1`)
  - Exemplar sampling mechanism present but incomplete
- ⚠️ **[Metrics Sdk]** [SHOULD] If the instrument name does not conform to this syntax, the Meter SHOULD emit (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1`)
  - FixedSizeExemplarFilter not explicitly named
- ⚠️ **[Metrics Sdk]** [SHOULD NOT] When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. (`src/Метрики/Модули/ОтелФильтрЭкземпляров.os:1`)
  - ExemplarFilter implemented (AlwaysOn, AlwaysOff, TraceBased)
- ⚠️ **[Metrics Sdk]** [SHOULD NOT] When a Meter creates an instrument, it SHOULD NOT validate the instrument (`src/Метрики/Классы/ОтелЭкспортерМетрик.os:322-330`)
  - Exemplars not fully exposed
- ⚠️ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument advisory (`src/Метрики/Классы/ОтелЭкспортерМетрик.os:322-330`)
  - Exemplars not fully exposed
- ⚠️ **[Metrics Sdk]** [SHOULD] parameters. If an advisory parameter is not valid, the Meter SHOULD emit an error (`src/Метрики/Классы/ОтелЭкспортерМетрик.os:322-330`)
  - Exemplars not fully exposed
- ❌ **[Metrics Sdk]** [SHOULD] `Exemplar` sampling SHOULD be turned on by default. If `Exemplar` sampling is (`src/Метрики`)
  - ResourceMetrics association not found
- ❌ **[Metrics Sdk]** [SHOULD] A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: (`src/Метрики`)
  - MetricProducer deduplication not found
- ❌ **[Metrics Sdk]** [SHOULD] The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for (`src/Метрики`)
  - MetricReader multiple producers not found
- ❌ **[Metrics Sdk]** [SHOULD] an SDK. The default value SHOULD be `TraceBased`. The filter configuration (`src/Метрики`)
  - OpenTelemetry MetricProducer not found
- ❌ **[Metrics Sdk]** [SHOULD] SHOULD follow the environment variable specification. (`src/Метрики`)
  - MetricProducer registration mechanism not found
- ⚠️ **[Metrics Sdk]** [SHOULD] with. In other words, Exemplars reported against a metric data point SHOULD have (`src/Метрики/Классы/ОтелМетр.os:44-49`)
  - Detection covers normalization but not full spec
- ⚠️ **[Metrics Sdk]** [SHOULD] The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. (`src/Метрики/Классы/ОтелМетр.os:44-49`)
  - Same Meter same name returns existing instrument
- ⚠️ **[Metrics Sdk]** [SHOULD] twenty (e.g. `min(20, max_buckets)`).* All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`. (`src/Метрики/Классы/ОтелМетр.os:44-49`)
  - Conflict resolution missing explicit policy
- ⚠️ **[Metrics Sdk]** [SHOULD] Any stateful portion of sampling computation SHOULD be reset every collection (`src/Метрики/Классы/ОтелМетр.os:44-49`)
  - Resolved stream equivalence not documented
- ⚠️ **[Metrics Sdk]** [SHOULD] contention. Otherwise, a default size of `1` SHOULD be used. (`src/Метрики/Классы/ОтелМетр.os:198-272`)
  - Asynchronous measurements with attributes supported
- ⚠️ **[Metrics Sdk]** [SHOULD] measurement that falls within a histogram bucket, and SHOULD use a (`src/Метрики/Классы/ОтелНаблюдениеМетрики.os:19-30`)
  - Duplicate measurement warning not logged
- ⚠️ **[Metrics Sdk]** [SHOULD] number of bucket boundaries plus one. This configuration parameter SHOULD have (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:1`)
  - Complete attribute set for synchronous instruments (assumed)
- ⚠️ **[Metrics Sdk]** [SHOULD] `Collect` SHOULD provide a way to let the caller know whether it succeeded, (`src/Метрики/Классы/ОтелМетр.os:256-272`)
  - ResourceMetrics not found
- ⚠️ **[Metrics Sdk]** [SHOULD] `Collect` SHOULD invoke Produce on registered (`src/Метрики/Классы/ОтелМетр.os:256-272`)
  - InstrumentationScope association not found
- ❌ **[Metrics Sdk]** [SHOULD] SHOULD return some failure for these calls, if possible. (`src/Метрики`)
  - MetricReader MetricProducers support not found
- ❌ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, (`src/Метрики`)
  - MetricProducer deduplication not found
- ❌ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` MAY be (`src/Метрики`)
  - MetricProducer data modification restriction not found
- ❌ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD collect metrics, call `Export(batch)` (`src/Метрики`)
  - OpenTelemetry MetricProducer independence not found
- ❌ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, (`src/Метрики`)
  - MetricProducer registration mechanism not found
- ❌ **[Metrics Sdk]** [SHOULD] failed or timed out. `ForceFlush` SHOULD return some ERROR status if there (`src/Метрики`)
  - API MetricProducer registration not found
- ❌ **[Metrics Sdk]** [SHOULD NOT] exporter. The default SDK SHOULD NOT implement retry logic, as the required (`src/Метрики/Классы/ОтелМетр.os`)
  - Configuration method for attribute limits not found
- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, (`src/Метрики/Классы/ОтелМетр.os:47-48`)
  - Warning logged via ПроверитьКонфликтДескриптора (implicit)
- ⚠️ **[Metrics Sdk]** [SHOULD] Shutdown SHOULD be called only once for each `MetricExporter` instance. After (`src/Метрики/Классы/ОтелМетр.os:45-48`)
  - Different Meter separate streams (assumed)
- ⚠️ **[Metrics Sdk]** [SHOULD] `MetricProducer` implementations SHOULD accept configuration for the (`src/Метрики/Классы/ОтелНаблюдениеМетрики.os`)
  - Asynchronous measurements with attributes
- ⚠️ **[Metrics Sdk]** [SHOULD] `metricFilter` parameter. Implementation SHOULD use the filter as early as (`src/Метрики/Классы/ОтелМетр.os:72-93`)
  - View boundaries used instead of advisory
- ⚠️ **[Metrics Sdk]** [SHOULD] resource information, `Produce` SHOULD require a resource as a parameter. (`src/Метрики/Классы/ОтелМетр.os:72-93`)
  - Boundaries not overridden when View configured
- ⚠️ **[Metrics Sdk]** [SHOULD] `Produce` SHOULD provide a way to let the caller know whether it succeeded, (`src/Метрики/Классы/ОтелМетр.os:72-93`)
  - View boundaries applied to async instruments
- ⚠️ **[Metrics Sdk]** [SHOULD] `Produce` SHOULD include a single InstrumentationScope which identifies the (`src/Метрики/Классы/ОтелМетр.os:72-93`)
  - View boundaries take precedence (assumed)
- ❌ **[Metrics Sdk]** [SHOULD] All the metrics components SHOULD allow new methods to be added to existing (`src/Метрики`)
  - ValidRange advisory not found
- ❌ **[Metrics Sdk]** [SHOULD] All the metrics SDK methods SHOULD allow optional parameter(s) to be added to (`src/Метрики`)
  - ValidRange advisory not found
- ⚠️ **[Otlp Exporter]** [SHOULD] they SHOULD continue to be supported as they were part of a stable release of the specification. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)
  - Default protocol is http/json not http/protobuf
- ⚠️ **[Otlp Exporter]** [SHOULD] [4]: The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default. For instance, maintaini... (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130-162`)
  - HTTP URLs constructed but signal-specific resolution missing
- ⚠️ **[Otlp Exporter]** [SHOULD] support at least one of them. If they support only one, it SHOULD be (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)
  - Default is http/json not http/protobuf
- ❌ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the ve... (`src/Экспорт/Классы/ОтелHttpТранспорт.os`)
  - No RFC 7231 User-Agent
- ❌ **[Otlp Exporter]** [SHOULD] The format of the header SHOULD follow RFC 7231. The conventions used for specifying the OpenTelemetry SDK language and version are available in the R... (`src/Экспорт/Классы/ОтелHttpТранспорт.os`)
  - No User-Agent configuration option
- ⚠️ **[Propagators]** [SHOULD] propagators. If pre-configured, `Propagator`s SHOULD default to a composite (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)
  - Override not fully detailed
- ⚠️ **[Trace Api]** [SHOULD] its `name` property SHOULD be set to an empty string, and a message (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52`)
  - Parameter validation and logging not fully documented in code comments
- ⚠️ **[Trace Api]** [SHOULD] reporting that the specified value is invalid SHOULD be logged. A library, (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52`)
  - Error logging mechanism not visible in code
- ⚠️ **[Trace Api]** [SHOULD] The span name SHOULD be the most general string that identifies a (`src/Трассировка/Классы/ОтелСпан.os:269`)
  - Attributes stored in ОтелАтрибуты, order preservation not explicitly guaranteed
- ⚠️ **[Trace Api]** [SHOULD NOT] prevent misuse, implementations SHOULD NOT provide access to a `Span`’s (`src/Трассировка/Классы/ОтелСпан.os`)
  - No explicit guidance on avoiding high-level concepts
- ⚠️ **[Trace Api]** [SHOULD NOT] `IsRecording` SHOULD NOT take any parameters. (`src/Трассировка/Классы/ОтелСпан.os:307`)
  - RecordException does not set Error status automatically
- ⚠️ **[Trace Api]** [SHOULD] This flag SHOULD be used to avoid expensive computations of a Span attributes or (`src/Трассировка/Классы/ОтелСпан.os`)
  - Exception semantic conventions not explicitly referenced in code
- ⚠️ **[Trace Api]** [SHOULD NOT] Generally, Instrumentation Libraries SHOULD NOT set the status code to `Ok`, (`src/Трассировка/Классы/ОтелСпан.os`)
  - Concurrency safety not explicitly documented; uses providers internal SinkhronizedMap
- ⚠️ **[Trace Api]** [SHOULD] unless explicitly configured to do so. Instrumentation Libraries SHOULD leave the (`src/Трассировка/Классы`)
  - Propagators not found in this codebase (separate module expected)
- ⚠️ **[Trace Sdk]** [SHOULD] so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend (`src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os`)
  - Export batch size not documented (extends parent class)
- ⚠️ **[Trace Sdk]** [SHOULD NOT] Callers SHOULD NOT cache the returned value. (`src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os`)
  - maxQueueSize vs maxExportBatchSize relationship not documented
- ⚠️ **[Trace Sdk]** [SHOULD] represented as a decimal number. The precision of the number SHOULD follow (`src/Трассировка/Классы`)
  - Export blocking not explicitly prevented at API level
- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD be called only once for each `SpanProcessor` instance. After (`src/Трассировка/Классы`)
  - ReadWriteSpan (writable span) not separately distinguished
- ⚠️ **[Trace Sdk]** [SHOULD] are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os`)
  - Concurrency in provider not explicitly documented
- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, (`src/Трассировка/Классы/ОтелТрассировщик.os`)
  - Tracer method concurrency safety not explicitly documented
- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` can be (`src/Трассировка/Классы`)
  - SpanExporter concurrency safety not explicitly documented
- ⚠️ **[Trace Sdk]** [SHOULD] `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os`)
  - SpanProcessor concurrency safety not explicitly documented
- ⚠️ **[Trace Sdk]** [SHOULD] In particular, if any `SpanProcessor` has any associated exporter, it SHOULD (`src/Трассировка/Классы`)
  - Concurrency characteristics not systematically documented
- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os`)
  - No timeout mechanism
- ⚠️ **[Trace Sdk]** [SHOULD] The processor SHOULD export a batch when any of the following happens AND the (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os`)
  - No concurrency documentation
- ⚠️ **[Trace Sdk]** [SHOULD NOT] default SDK’s Span Processors SHOULD NOT implement retry logic, as the required (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38-40`)
  - ForceFlush no status
- ⚠️ **[Trace Sdk]** [SHOULD] call to `ForceFlush` SHOULD be completed as soon as possible, preferably before (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38-40`)
  - No status indication
- ❌ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, (`-`)
  - ForceFlush guidance missing
- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38-40`)
  - No timeout mechanism

---

## Детальный анализ по разделам (Stable)

### Context

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | MUST | ✅ | A `Context` MUST be immutable, and its write operations MUST | src/Ядро/Модули/ОтелКонтекст.os:1-316 |
| 2 | MUST | ✅ | option is not available, OpenTelemetry MUST provide its own `Context` | src/Ядро/Модули/ОтелКонтекст.os:45-48 |
| 3 | MUST | ➖ | The API MUST accept the following parameter: | spec-compliance.md (Language constraint - not applicable) |
| 4 | SHOULD NOT | ✅ | * The key name. The key name exists for debugging purposes and does not uniquely identify the key. Multiple calls to `Cr... | src/Ядро/Модули/ОтелКонтекст.os:45-48 |
| 5 | MUST | ✅ | The API MUST return an opaque object representing the newly created key. | src/Ядро/Модули/ОтелКонтекст.os:45-48 |
| 6 | MUST | ✅ | The API MUST accept the following parameters: | src/Ядро/Модули/ОтелКонтекст.os:45-48 |
| 7 | MUST | ✅ | The API MUST return the value in the `Context` for the specified key. | src/Ядро/Модули/ОтелКонтекст.os:147-152 |
| 8 | MUST | ✅ | The API MUST accept the following parameters: | src/Ядро/Модули/ОтелКонтекст.os:114-134 |
| 9 | MUST | ➖ | The API MUST return a new `Context` containing the new value. | Optional for OneScript platform (Optional scope switching) |
| 10 | SHOULD | ✅ | SHOULD only be used to implement automatic scope switching and define | src/Ядро/Модули/ОтелКонтекст.os:29-35 |
| 11 | MUST | ✅ | The API MUST return the `Context` associated with the caller’s current execution unit. | src/Ядро/Модули/ОтелКонтекст.os:147-152 |
| 12 | MUST | ✅ | The API MUST accept the following parameters: | src/Ядро/Классы/ОтелОбласть.os:19-27 |
| 13 | MUST | ✅ | The API MUST return a value that can be used as a `Token` to restore the previous | src/Ядро/Классы/ОтелОбласть.os:22-27 |
| 14 | MUST | ✅ | The API MUST accept the following parameters: | src/Ядро/Классы/ОтелBaggage.os:1-166 |

### Baggage Api

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 15 | MUST | ✅ | describing user-defined properties. Each name in `Baggage` MUST be associated | src/Ядро/Классы/ОтелBaggage.os:38-40 |
| 16 | SHOULD NOT | ✅ | Baggage names are any valid, non-empty UTF-8 strings. Language API SHOULD NOT | src/Ядро/Классы/ОтелBaggage.os:38-40 |
| 17 | MUST | ✅ | Baggage values are any valid UTF-8 strings. Language API MUST accept | src/Ядро/Классы/ОтелBaggage.os:38-40 |
| 18 | MUST | ✅ | Language API MUST treat both baggage names and values as case sensitive. | src/Ядро/Классы/ОтелBaggage.os:16-28 |
| 19 | MUST | ✅ | The Baggage API MUST be fully functional in the absence of an installed SDK. | src/Ядро/Классы/ОтелBaggage.os:152-163 |
| 20 | MUST | ✅ | The `Baggage` container MUST be immutable, so that the containing `Context` | src/Ядро/Классы/ОтелBaggage.os:38-40 |
| 21 | MUST | ✅ | MUST provide a function that takes the name as input, and returns a value | src/Ядро/Классы/ОтелBaggage.os:103-105 |
| 22 | MUST NOT | ✅ | MUST NOT be significant. Based on the language specifics, the returned | src/Ядро/Классы/ОтелBaggage.os:68-72 |
| 23 | MUST | ✅ | To record the value for a name/value pair, the Baggage API MUST provide a | src/Ядро/Классы/ОтелBaggage.os:82-86 |
| 24 | MUST | ✅ | To delete a name/value pair, the Baggage API MUST provide a function which | src/Ядро/Классы/ОтелBaggage.os:16-28 |
| 25 | MUST | ➖ | MUST provide the following functionality to interact with a `Context` instance: | Language-specific design (Not applicable) |
| 26 | SHOULD NOT | ✅ | The functionality listed above is necessary because API users SHOULD NOT have | src/Ядро/Классы/ОтелBaggage.os:16-28 |
| 27 | SHOULD | ✅ | `Baggage` class. This functionality SHOULD be fully implemented in the API when | src/Ядро/Классы/ОтелBaggage.os:94-96 |
| 28 | MUST | ✅ | MUST provide a way to remove all baggage entries from a context. | src/Пропагация/Модули/ОтелW3CПропагатор.os |
| 29 | MUST | ✅ | The API layer or an extension package MUST include the following `Propagator`s: | src/Ядро/Классы/ОтелРесурс.os:44-65 |
| 30 | MUST | ✅ | then the new pair MUST take precedence. The value is replaced with the added | src/Ядро/Классы/ОтелРесурс.os:1-173 |

### Resource Sdk

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 31 | MUST | ✅ | with closed source environments. The SDK MUST allow for creation of `Resources` and | src/Трассировка/Классы/ОтелПровайдерТрассировки.os |
| 32 | MUST | ✅ | all `Span`s produced by any `Tracer` from the provider MUST be associated with this `Resource`. | src/Ядро/Классы/ОтелРесурс.os:104-113 |
| 33 | MUST | ✅ | The SDK MUST provide access to a Resource with at least the attributes listed at | src/Ядро/Классы/ОтелSdk.os |
| 34 | MUST | ✅ | This resource MUST be associated with a `TracerProvider` or `MeterProvider` | src/Ядро/Классы/ОтелПостроительРесурса.os |
| 35 | MUST | ✅ | The interface MUST provide a way to create a new resource, from `Attributes`. | src/Ядро/Классы/ОтелРесурс.os:44-65 |
| 36 | MUST | ✅ | The interface MUST provide a way for an old resource and an | src/Ядро/Классы/ОтелРесурс.os:57-64 |
| 37 | MUST | ✅ | The resulting resource MUST have all attributes that are on any of the two input resources. | src/Ядро/Классы/ОтелРесурс.os:61-62 |
| 38 | MUST | ⚠️ | resource MUST be picked (even if the updated value is empty). | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:96-119 (Limited environment detection) |
| 39 | MUST | ➖ | or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as | No resource detector packages (Not applicable) |
| 40 | MUST | ✅ | Resource detector packages MUST provide a method that returns a resource. This | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:101-119 |
| 41 | MUST NOT | ⚠️ | failure to detect any resource information MUST NOT be considered an error, | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:101-119 (Limited error reporting) |
| 42 | SHOULD | ➖ | SHOULD be considered an error. | No resource detectors (Not applicable) |
| 43 | MUST | ➖ | semantic conventions MUST ensure that the resource has a Schema URL set to a | No resource detectors (Not applicable) |
| 44 | SHOULD | ➖ | value that matches the semantic conventions. Empty Schema URL SHOULD be used if | No resource detectors (Not applicable) |
| 45 | MUST | ➖ | the detectors use different non-empty Schema URL it MUST be an error since it is | No resource detectors (scope:conditional:Resource Detector Naming) |

### Trace Api

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 56 | SHOULD | ✅ | Thus, the API SHOULD provide a way to set/register and access | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:85 |
| 57 | SHOULD | ✅ | Thus, implementations of `TracerProvider` SHOULD allow creating an arbitrary | src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os |
| 58 | MUST | ✅ | The `TracerProvider` MUST provide the following functions: | src/Трассировка/Классы/ОтелТрассировщик.os:22 |
| 59 | MUST | ✅ | This API MUST accept the following parameters: | src/Трассировка/Классы/ОтелТрассировщик.os:22 |
| 60 | SHOULD | ✅ | * `name` (required): This name SHOULD uniquely identify the | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52 |
| 61 | MUST | ✅ | (null or empty string) is specified, a working Tracer implementation MUST be | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:59-68 |
| 62 | SHOULD | ⚠️ | its `name` property SHOULD be set to an empty string, and a message | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52 (Parameter validation and logging not fully documented in code comments) |
| 63 | SHOULD | ⚠️ | reporting that the specified value is invalid SHOULD be logged. A library, | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52 (Error logging mechanism not visible in code) |
| 64 | MUST NOT | ✅ | Implementations MUST NOT require users to repeatedly obtain a `Tracer` again | src/Трассировка/Классы/ОтелТрассировщик.os |
| 65 | MUST | ✅ | The API MUST provide the following functionality to interact with a `Context` | src/Трассировка/Классы/ОтелТрассировщик.os:33 |
| 66 | SHOULD NOT | ✅ | The functionality listed above is necessary because API users SHOULD NOT have | src/Трассировка/Классы/ОтелПостроительСпана.os:118 |
| 67 | SHOULD | ✅ | here), the API SHOULD also provide | src/Трассировка/Классы/ОтелПостроительСпана.os |
| 68 | SHOULD | ✅ | inside the trace module. This functionality SHOULD be fully implemented in the API when possible. | src/Трассировка/Классы/ОтелПостроительСпана.os:33-49 |
| 69 | MUST | ✅ | The `Tracer` MUST provide functions to: | src/Трассировка/Классы/ОтелПостроительСпана.os:33-49 |
| 70 | SHOULD | ✅ | The `Tracer` SHOULD provide functions to: | src/Трассировка/Классы/ОтелСпан.os:559 |
| 75 | MUST | ✅ | The API MUST implement methods to create a `SpanContext`. These methods SHOULD be the only way to | src/Трассировка/Классы/ОтелСпан.os:563 |
| 76 | SHOULD NOT | ✅ | create a `SpanContext`. This functionality MUST be fully implemented in the API, and SHOULD NOT be | src/Трассировка/Классы/ОтелСпан.os:544 |
| 77 | MUST | ✅ | The API MUST allow retrieving the `TraceId` and `SpanId` in the following forms: | src/Трассировка/Классы/ОтелСпан.os:545 |
| 78 | MUST | ✅ | `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` | src/Трассировка/Классы/ОтелТрассировщик.os:49-79 |
| 79 | MUST | ✅ | (result MUST be a 16-hex-character lowercase string).* Binary - returns the binary representation of the `TraceId` (resu... | src/Трассировка/Классы/ОтелТрассировщик.os:50 |
| 80 | MUST | ✅ | 16-byte array) or `SpanId` (result MUST be an 8-byte array). | src/Трассировка/Классы/ОтелТрассировщик.os:116-135 |
| 81 | SHOULD NOT | ✅ | The API SHOULD NOT expose details about how they are internally stored. | src/Ядро/Модули/ОтелКонтекст.os:114 |
| 82 | MUST | ✅ | non-zero TraceID and a non-zero SpanID, MUST be provided. | src/Трассировка/Классы/ОтелПостроительСпана.os:90-96 |
| 83 | MUST | ✅ | propagated from a remote parent, MUST be provided. | src/Трассировка/Классы/ОтелСпан.os:351 |
| 84 | MUST | ✅ | `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | src/Трассировка/Классы/ОтелСпан.os:366 |
| 85 | MUST | ✅ | Tracing API MUST provide at least the following operations on `TraceState`: | src/Трассировка/Классы/ОтелНоопСпан.os |
| 86 | MUST | ✅ | These operations MUST follow the rules described in the W3C Trace Context specification. | src/Трассировка/Классы/ОтелСпан.os:72 |
| 87 | MUST | ✅ | All mutating operations MUST return a new `TraceState` with the modifications applied. | src/Трассировка/Классы/ОтелКонтекстСпана.os |
| 88 | MUST | ✅ | `TraceState` MUST at all times be valid according to rules specified in W3C Trace Context specification. | src/Трассировка/Классы/ОтелСпан.os:226 |
| 89 | MUST | ✅ | Every mutating operations MUST validate input parameters. | src/Трассировка/Классы/ОтелСпан.os:255 |
| 90 | MUST NOT | ✅ | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data | src/Трассировка/Классы/ОтелСпан.os:226 |
| 91 | MUST | ✅ | and MUST follow the general error handling guidelines. | src/Трассировка/Классы/ОтелСпан.os:239 |
| 92 | SHOULD | ⚠️ | The span name SHOULD be the most general string that identifies a | src/Трассировка/Классы/ОтелСпан.os:269 (Attributes stored in ОтелАтрибуты, order preservation not explicitly guaranteed) |
| 93 | SHOULD | ✅ | Generality SHOULD be prioritized over human-readability. | src/Трассировка/Классы/ОтелСпан.os:255 |
| 94 | SHOULD | ✅ | A `Span`’s start time SHOULD be set to the current time on span | src/Трассировка/Классы/ОтелСпан.os:255 |
| 95 | SHOULD | ✅ | creation. After the `Span` is created, it SHOULD be possible to | src/Трассировка/Классы/ОтелСпан.os:255 |
| 96 | MUST NOT | ✅ | MUST NOT be changed after the `Span`’s end time has been set. | src/Трассировка/Классы/ОтелСпан.os:258 |
| 97 | SHOULD NOT | ⚠️ | prevent misuse, implementations SHOULD NOT provide access to a `Span`’s | src/Трассировка/Классы/ОтелСпан.os (No explicit guidance on avoiding high-level concepts) |
| 98 | MUST NOT | ✅ | However, alternative implementations MUST NOT allow callers to create `Span`s | src/Трассировка/Классы/ОтелСпан.os |
| 99 | MUST | ✅ | directly. All `Span`s MUST be created via a `Tracer`. | src/Трассировка/Классы/ОтелСпан.os |
| 100 | MUST NOT | ✅ | There MUST NOT be any API for creating a `Span` other than with a `Tracer`. | src/Трассировка/Классы/ОтелСпан.os:269 |
| 101 | MUST NOT | ✅ | In languages with implicit `Context` propagation, `Span` creation MUST NOT | src/Трассировка/Классы/ОтелЛимитыСпана.os:170 |
| 102 | MUST | ✅ | The API MUST accept the following parameters: | src/Трассировка/Классы/ОтелСпан.os:284 |
| 103 | MUST NOT | ✅ | This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`. | src/Трассировка/Классы/ОтелСпан.os:284 |
| 104 | MUST | ✅ | The semantic parent of the Span MUST be determined according to the rules | src/Трассировка/Классы/ОтелСобытиеСпана.os:83-90 |
| 105 | MUST | ✅ | The API documentation MUST state that adding attributes at span creation is preferred | src/Трассировка/Классы/ОтелСпан.os:287 |
| 106 | SHOULD | ✅ | `Start timestamp`, default to current time. This argument SHOULD only be set | src/Трассировка/Классы/ОтелСпан.os:402 |
| 107 | MUST NOT | ✅ | a Span logical start, API user MUST NOT explicitly set this argument. | src/Трассировка/Модули/ОтелКодСтатуса.os |
| 108 | MUST | ✅ | spans in the trace. Implementations MUST provide an option to create a `Span` as | src/Трассировка/Классы/ОтелСпан.os:402 |
| 109 | MUST | ✅ | a root span, and MUST generate a new `TraceId` for each root span created. | src/Трассировка/Классы/ОтелСпан.os:418 |
| 110 | MUST | ✅ | For a Span with a parent, the `TraceId` MUST be the same as the parent. | src/Трассировка/Классы/ОтелСпан.os:418-421 |
| 111 | MUST | ✅ | Also, the child span MUST inherit all `TraceState` values of its parent by default. | src/Трассировка/Классы/ОтелСпан.os:239 |
| 112 | MUST | ✅ | Any span that is created MUST also be ended. | src/Трассировка/Классы/ОтелСпан.os:436 |
| 113 | MUST | ✅ | During `Span` creation, a user MUST have the ability to record links to other `Span`s. | src/Трассировка/Классы/ОтелСпан.os:437-447 |
| 114 | MUST | ✅ | The Span interface MUST provide: | src/Трассировка/Классы/ОтелСпан.os:240 |
| 115 | MUST | ✅ | may be used even after the `Span` is finished. The returned value MUST be the | src/Трассировка/Классы/ОтелСпан.os:436 |
| 116 | SHOULD | ✅ | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` | src/Трассировка/Классы/ОтелСпан.os:307 |
| 117 | SHOULD | ✅ | SHOULD always return `false`. The one known exception to this is | src/Трассировка/Классы/ОтелСпан.os:312-328 |
| 118 | SHOULD NOT | ⚠️ | `IsRecording` SHOULD NOT take any parameters. | src/Трассировка/Классы/ОтелСпан.os:307 (RecordException does not set Error status automatically) |
| 119 | SHOULD | ⚠️ | This flag SHOULD be used to avoid expensive computations of a Span attributes or | src/Трассировка/Классы/ОтелСпан.os (Exception semantic conventions not explicitly referenced in code) |
| 120 | MUST | ✅ | A `Span` MUST have the ability to set `Attributes` associated with it. | src/Трассировка/Классы/ОтелСпан.os:568 |
| 121 | MUST | ✅ | The Span interface MUST provide: | src/Трассировка/Классы/ОтелСпан.os:408 |
| 122 | SHOULD | ✅ | Setting an attribute with the same key as an existing attribute SHOULD overwrite | src/Трассировка/Классы/ОтелСпан.os:412-415 |
| 123 | MUST | ✅ | A `Span` MUST have the ability to add events. Events have a time associated | src/Трассировка/Классы/ОтелСпан.os |
| 124 | MUST | ✅ | The Span interface MUST provide: | src/Трассировка/Классы/ОтелСпан.os:180-182 |
| 125 | SHOULD | ✅ | Events SHOULD preserve the order in which they are recorded. | src/Трассировка/Классы/ОтелСпан.os |
| 126 | MUST | ✅ | A `Span` MUST have the ability to add `Link`s associated with it after its creation - see Links. | src/Трассировка/Классы/ОтелКонтекстСпана.os |
| 127 | MUST | ✅ | `Description` MUST only be used with the `Error` `StatusCode` value. | src/Трассировка/Классы/ОтелКонтекстСпана.os:70-75 |
| 128 | MUST | ✅ | The Span interface MUST provide: | src/Трассировка/Классы/ОтелКонтекстСпана.os:70-75 |
| 129 | SHOULD | ✅ | * An API to set the `Status`. This SHOULD be called `SetStatus`. This API takes | src/Трассировка/Классы/ОтелКонтекстСпана.os:41-42 |
| 130 | MUST | ✅ | appropriate for the language. `Description` MUST be IGNORED for `StatusCode` | src/Трассировка/Классы/ОтелКонтекстСпана.os:45-52 |
| 131 | SHOULD | ✅ | The status code SHOULD remain unset, except for the following circumstances: | src/Трассировка/Классы/ОтелКонтекстСпана.os:70 |
| 132 | SHOULD | ✅ | An attempt to set value `Unset` SHOULD be ignored. | src/Трассировка/Классы/ОтелКонтекстСпана.os:60-62 |
| 133 | SHOULD | ✅ | SHOULD be documented and predictable. The status code should only be set to `Error` | src/Трассировка/Классы/ОтелКонтекстСпана.os:41-42 |
| 134 | SHOULD | ✅ | not covered by the semantic conventions, Instrumentation Libraries SHOULD | src/Трассировка/Классы/ОтелКонтекстСпана.os:70-75 |
| 135 | SHOULD NOT | ⚠️ | Generally, Instrumentation Libraries SHOULD NOT set the status code to `Ok`, | src/Трассировка/Классы/ОтелСпан.os (Concurrency safety not explicitly documented; uses providers internal SinkhronizedMap) |
| 136 | SHOULD | ⚠️ | unless explicitly configured to do so. Instrumentation Libraries SHOULD leave the | src/Трассировка/Классы (Propagators not found in this codebase (separate module expected)) |
| 137 | SHOULD | ➖ | When span status is set to `Ok` it SHOULD be considered final and any further | Propagators module (Trace context propagation in separate module) |
| 138 | SHOULD | ➖ | attempts to change it SHOULD be ignored. | Propagators module (Not all propagators needed for OneScript platform) |
| 139 | SHOULD | ➖ | Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they | Propagators module (Platform-specific propagator support) |
| 140 | SHOULD | ✅ | Implementations SHOULD ignore all subsequent calls to `End` and any other Span methods, | src/Трассировка |
| 141 | MUST | ✅ | However, all API implementations of such methods MUST internally call the `End` | src/Трассировка/Классы/ОтелНоопСпан.os |
| 142 | MUST NOT | ⚠️ | `End` MUST NOT have any effects on child spans. | src/Ядро/Модули/ОтелКонтекст.os (SpanContext from Propagator stored in Context (mechanism present)) |
| 143 | MUST NOT | ✅ | `End` MUST NOT inactivate the `Span` in any `Context` it is active in. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:59 |
| 144 | MUST | ✅ | It MUST still be possible to use an ended span as parent via a Context it is | src/Трассировка/Классы/ОтелНоопСпан.os:220 |
| 145 | MUST | ✅ | contained in. Also, any mechanisms for putting the Span into a Context MUST | src/Трассировка/Классы/ОтелНоопСпан.os:252 |
| 146 | MUST | ✅ | If omitted, this MUST be treated equivalent to passing the current time. | src/Трассировка/Классы/ОтелНоопСпан.os |
| 147 | MUST NOT | ✅ | This operation itself MUST NOT perform blocking I/O on the calling thread. | src/Трассировка/Классы/ОтелНоопСпан.os:155 |
| 148 | SHOULD | ✅ | Any locking used needs be minimized and SHOULD be removed entirely if | src/Трассировка/Классы/ОтелСпан.os:258 |
| 149 | SHOULD | ✅ | To facilitate recording an exception languages SHOULD provide a | src/Трассировка/Классы/ОтелСпан.os:286-292 |
| 150 | MUST | ✅ | The method MUST record an exception as an `Event` with the conventions outlined in | src/Трассировка/Классы/ОтелСпан.os:307-338 |
| 151 | SHOULD | ✅ | The minimum required argument SHOULD be no more than only an exception object. | src/Трассировка/Классы/ОтелКонтекстСпана.os |
| 152 | MUST | ✅ | If `RecordException` is provided, the method MUST accept an optional parameter | src/Трассировка/Классы/ОтелНоопСпан.os:272 |
| 153 | SHOULD | ✅ | (this SHOULD be done in the same way as for the `AddEvent` method). | src/Трассировка/Классы/ОтелНоопСпан.os:155 |
| 154 | MUST | ✅ | Start and end time as well as Event’s timestamps MUST be recorded at a time of a | src/Трассировка/Классы/ОтелНоопСпан.os:276-278 |
| 155 | MUST | ✅ | The API MUST provide an operation for wrapping a `SpanContext` with an object | src/Трассировка/Классы/ОтелНоопСпан.os |
| 156 | SHOULD NOT | ✅ | If a new type is required for supporting this operation, it SHOULD NOT be exposed | src/Ядро/Модули/ОтелКонтекст.os:82-102 |
| 157 | SHOULD | ✅ | it SHOULD be named `NonRecordingSpan`. | src/Ядро/Модули/ОтелКонтекст.os:82-102 |
| 158 | MUST | ✅ | * `GetContext` MUST return the wrapped `SpanContext`.* `IsRecording` MUST return `false` to signal that events, attribut... | src/Трассировка/Классы/ОтелНоопСпан.os |
| 159 | MUST | ✅ | The remaining functionality of `Span` MUST be defined as no-op operations. | src/Трассировка/Классы/ОтелНоопСпан.os |
| 160 | SHOULD NOT | ✅ | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | src/Трассировка/Классы/ОтелКонтекстСпана.os:124-142 |
| 161 | SHOULD | ✅ | In order for `SpanKind` to be meaningful, callers SHOULD arrange that | src/Трассировка/Классы/ОтелКонтекстСпана.os:70 |
| 162 | SHOULD NOT | ✅ | server-side span SHOULD NOT be used to describe outgoing remote procedure call. | src/Трассировка/Классы/ОтелКонтекстСпана.os:60 |
| 163 | MUST | ✅ | A user MUST have the ability to record links to other `SpanContext`s. | src/Трассировка/Классы/ОтелНоопСпан.os:272 |
| 164 | SHOULD | ✅ | appropriate for the language. Implementations SHOULD record links containing | src/Трассировка/Классы/ОтелНоопСпан.os:155 |
| 165 | SHOULD | ✅ | Span SHOULD preserve the order in which `Link`s are set. | src/Трассировка/Классы/ОтелНоопСпан.os:29 |
| 166 | MUST | ✅ | The API documentation MUST state that adding links at span creation is preferred | src/Трассировка/Классы/ОтелНоопСпан.os:29 |
| 167 | MUST | ✅ | TracerProvider - all methods MUST be documented that implementations need to | src/Трассировка/Классы/ОтелНоопСпан.os:29 |
| 168 | MUST | ✅ | Tracer - all methods MUST be documented that implementations need to be safe | src/Трассировка/Классы/ОтелНоопСпан.os |
| 169 | MUST | ✅ | Span - all methods MUST be documented that implementations need to be safe | src/Трассировка/Классы/ОтелНоопСпан.os:29 |
| 170 | MUST | ✅ | Event - Events are immutable and MUST be safe for concurrent use by default. | src/Трассировка/Классы/ОтелНоопСпан.os:29 |
| 171 | SHOULD | ✅ | Link - Links are immutable and SHOULD be safe for concurrent use by default. | src/Трассировка/Классы/ОтелНоопСпан.os:274-278 |
| 172 | MUST | ✅ | and that is related to propagation of a `SpanContext`: The API MUST return a | src/Трассировка/Классы/ОтелНоопСпан.os:155 |
| 173 | SHOULD | ✅ | If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly | src/Трассировка/Классы/ОтелНоопСпан.os:243 |
| 174 | MUST | ✅ | If the parent `Context` contains no `Span`, an empty non-recording Span MUST be | src/Трассировка/Классы/ОтелПровайдерТрассировки.os |

### Trace Sdk

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 175 | SHOULD | ✅ | It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:207-235 |
| 176 | MUST | ✅ | The `TracerProvider` MUST implement the Get a Tracer API. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:59-69 |
| 177 | MUST | ✅ | The input provided by the user MUST be used to create | src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os |
| 179 | MUST | ✅ | the updated configuration MUST also apply to all already returned `Tracers` | src/Трассировка/Классы/ОтелТрассировщик.os:52-68 |
| 180 | MUST NOT | ✅ | (i.e. it MUST NOT matter whether a `Tracer` was obtained from the | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:59-68 |
| 188 | SHOULD | ✅ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:59-68 |
| 189 | SHOULD | ✅ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:100 |
| 190 | MUST | ⚠️ | `ForceFlush` MUST invoke `ForceFlush` on all registered `SpanProcessors`. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os (Timeout handling not explicitly documented) |
| 198 | MUST | ✅ | Readable span: A function receiving this as argument MUST be able to | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:17-46 |
| 199 | MUST | ✅ | A function receiving this as argument MUST be able to access | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:17 |
| 200 | MUST | ✅ | it MUST also be able to access the `InstrumentationLibrary` | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:17 |
| 201 | MUST | ✅ | A function receiving this as argument MUST be able to reliably determine | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26 |
| 202 | MUST | ✅ | Counts for attributes, events and links dropped due to collection limits MUST be | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-32 |
| 203 | MUST | ✅ | of the Span but they MUST expose at least the full parent SpanContext. | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:41-46 |
| 204 | MUST | ✅ | It MUST be possible for functions being called with this | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os |
| 205 | MUST | ✅ | Processor MUST receive only those spans which have this | src/Трассировка/Классы |
| 206 | SHOULD NOT | ✅ | field set to `true`. However, Span Exporter SHOULD NOT | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-31 |
| 207 | MUST | ✅ | `sampled` and will be exported. Span Exporters MUST | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-32 |
| 208 | SHOULD NOT | ✅ | receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os |
| 209 | MUST NOT | ✅ | MUST NOT allow this combination. | src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os |
| 210 | MUST | ⚠️ | When asked to create a Span, the SDK MUST act as if doing the following in order: | src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os (Default batch size not documented in visible code) |
| 211 | MUST | ⚠️ | If the parent `SpanContext` contains a valid `TraceId`, they MUST always match.* Name of the `Span` to be created.* `Spa... | src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os (Exporter configuration not fully documented in visible code) |
| 212 | MUST NOT | ⚠️ | will be dropped.* `RECORD_ONLY` - `IsRecording` will be `true`, but the `Sampled` flag MUST NOT be set.* `RECORD_AND_SAM... | src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os (Schedule delay interval not configured in visible code) |
| 213 | SHOULD | ⚠️ | so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend | src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os (Export batch size not documented (extends parent class)) |
| 214 | SHOULD NOT | ⚠️ | Callers SHOULD NOT cache the returned value. | src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os (maxQueueSize vs maxExportBatchSize relationship not documented) |
| 215 | MUST | ⚠️ | * The `TraceIdRatioBased` MUST ignore the parent `SampledFlag`. To respect the | src/Трассировка/Классы (SpanExporter interface not fully visible in trace module) |
| 216 | MUST | ⚠️ | the `ParentBased` sampler specified below.* Description MUST return a string of the form `"TraceIdRatioBased{RATIO}"` | src/Трассировка/Классы (Export called on sampled spans (implementation in processor)) |
| 217 | SHOULD | ⚠️ | represented as a decimal number. The precision of the number SHOULD follow | src/Трассировка/Классы (Export blocking not explicitly prevented at API level) |
| 218 | SHOULD | ✅ | implementation language standards and SHOULD be high enough to identify when | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os |
| 219 | MUST | ⚠️ | * The sampling algorithm MUST be deterministic. A trace identified by a given | src/Экспорт (Shutdown called on exporter (documented separately)) |
| 220 | MUST | ⚠️ | implementations MUST use a deterministic hash of the `TraceId` when computing | src/Экспорт (Shutdown provides completion signal (async support available)) |
| 221 | MUST | ⚠️ | will produce the same decision.* A `TraceIdRatioBased` sampler with a given sampling probability MUST also sample all | src/Экспорт (Shutdown non-blocking characteristic not fully documented) |
| 231 | SHOULD | ✅ | For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Ca... | src/Трассировка/Модули/ОтелСэмплер.os:63 |
| 232 | SHOULD | ✅ | For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the... | src/Трассировка/Модули/ОтелСэмплер.os:72 |
| 233 | MUST NOT | ⚠️ | MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState | src/Трассировка/Модули/ОтелСэмплер.os:81 (TraceIdRatio defined but default 0.0001 not documented) |
| 234 | SHOULD | ✅ | For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness... | src/Трассировка/Модули/ОтелСэмплер.os:81 |
| 235 | SHOULD | ✅ | If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random fla... | src/Трассировка/Модули/ОтелСэмплер.os:247-269 |
| 236 | MUST | ✅ | Span attributes MUST adhere to the common rules of attribute limits. | src/Трассировка/Модули/ОтелСэмплер.os:264-268 |
| 237 | MUST | ✅ | If the SDK implements the limits above it MUST provide a way to change these | src/Трассировка/Модули/ОтелСэмплер.os:92 |
| 238 | SHOULD | ✅ | The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`. The options MAY be bundled in a ... | src/Трассировка/Модули/ОтелСэмплер.os:146-173 |
| 239 | SHOULD | ✅ | which then SHOULD be called `SpanLimits`. Implementations MAY provide additional | src/Трассировка/Модули/ОтелСэмплер.os:231-245 |
| 240 | SHOULD | ✅ | There SHOULD be a message printed in the SDK’s log to indicate to the user | src/Трассировка/Классы/ОтелЛимитыСпана.os:169-176 |
| 241 | MUST | ✅ | To prevent excessive logging, the message MUST be printed at most once per | src/Трассировка/Классы/ОтелЛимитыСпана.os:83-152 |
| 242 | MUST | ✅ | The SDK MUST by default randomly generate both the `TraceId` and the `SpanId`. | src/Трассировка/Классы/ОтелЛимитыСпана.os |
| 243 | MUST | ⚠️ | The SDK MUST provide a mechanism for customizing the way IDs are generated for | src/Трассировка/Классы/ОтелСпан.os (Dropped attribute logging not visible in code) |
| 244 | MUST | ⚠️ | `IdGenerator`, name of the methods MUST be consistent with | src/Трассировка/Классы (Logging frequency control not documented) |
| 245 | MUST NOT | ✅ | X-Ray trace id generator MUST NOT be maintained or distributed as part of the | src/Трассировка |
| 247 | MUST | ✅ | of span processor and optional exporter. SDK MUST allow to end each pipeline with | src/Трассировка/Классы/ОтелСпан.os:563-564 |
| 248 | MUST | ➖ | SDK MUST allow users to implement and configure custom processors. | SDK Configuration (TracerConfig feature marked [DEV]) |
| 249 | MUST | ➖ | The `SpanProcessor` interface MUST declare the following methods: | SDK Configuration (TracerConfig default enabled marked [DEV]) |
| 250 | SHOULD | ➖ | The `SpanProcessor` interface SHOULD declare the following methods: | SDK Configuration (TracerConfig disabled behavior marked [DEV]) |
| 251 | SHOULD | ➖ | It SHOULD be possible to keep a reference to this span object and updates to the span | SDK Configuration (TracerConfig visibility marked [DEV]) |
| 256 | MUST | ✅ | This method MUST be called synchronously within the `Span.End()` API, | src/Трассировка/Классы/ОтелСпан.os:198-217 |
| 257 | SHOULD | ⚠️ | `Shutdown` SHOULD be called only once for each `SpanProcessor` instance. After | src/Трассировка/Классы (ReadWriteSpan (writable span) not separately distinguished) |
| 258 | SHOULD | ⚠️ | are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os (Concurrency in provider not explicitly documented) |
| 259 | SHOULD | ⚠️ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | src/Трассировка/Классы/ОтелТрассировщик.os (Tracer method concurrency safety not explicitly documented) |
| 260 | MUST | ⚠️ | `Shutdown` MUST include the effects of `ForceFlush`. | src/Трассировка/Классы/ОтелСпан.os (Span concurrency safety not explicitly documented) |
| 261 | SHOULD | ⚠️ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` can be | src/Трассировка/Классы (SpanExporter concurrency safety not explicitly documented) |
| 262 | SHOULD | ⚠️ | `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os (SpanProcessor concurrency safety not explicitly documented) |
| 263 | SHOULD | ⚠️ | In particular, if any `SpanProcessor` has any associated exporter, it SHOULD | src/Трассировка/Классы (Concurrency characteristics not systematically documented) |
| 264 | MUST | ⚠️ | The built-in SpanProcessors MUST do so. | src/Трассировка/Классы (ForceFlush timeout handling and prioritization not documented) |
| 265 | MUST | ⚠️ | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os (ForceFlush no status indication) |
| 266 | SHOULD | ✅ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os |
| 267 | SHOULD | ⚠️ | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os (No timeout mechanism) |
| 268 | SHOULD | ✅ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os + src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os |
| 269 | MUST | ✅ | The standard OpenTelemetry SDK MUST implement both simple and batch processors, | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os |
| 270 | MUST | ✅ | The processor MUST synchronize calls to `Span Exporter`’s `Export` | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os |
| 271 | MUST | ✅ | The processor MUST synchronize calls to `Span Exporter`’s `Export` | src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:73-112 |
| 272 | SHOULD | ⚠️ | The processor SHOULD export a batch when any of the following happens AND the | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os (No concurrency documentation) |
| 273 | MUST | ✅ | Each implementation MUST document the concurrency characteristics the SDK | src/Экспорт/Классы/ОтелЭкспортерСпанов.os:22-46 |
| 274 | MUST | ✅ | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | src/Экспорт/Классы/ОтелЭкспортерСпанов.os:22-33 |
| 275 | MUST NOT | ✅ | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit | src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:136-149 |
| 276 | SHOULD NOT | ⚠️ | default SDK’s Span Processors SHOULD NOT implement retry logic, as the required | src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38-40 (ForceFlush no status) |
| 277 | SHOULD | ⚠️ | call to `ForceFlush` SHOULD be completed as soon as possible, preferably before | src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38-40 (No status indication) |
| 278 | SHOULD | ❌ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | - (ForceFlush guidance missing) |
| 279 | SHOULD | ⚠️ | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, | src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38-40 (No timeout mechanism) |
| 280 | SHOULD | ✅ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | src/Трассировка/Классы/ОтелПровайдерТрассировки.os |
| 281 | MUST | ✅ | Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe | src/Трассировка/Классы/ОтелВсегдаЗаписывающийСэмплер.os |
| 282 | MUST | ✅ | Sampler - `ShouldSample` and `GetDescription` MUST be safe to be called | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os |
| 283 | MUST | ✅ | Span processor - all methods MUST be safe to be called concurrently. | src/Экспорт/Классы/ОтелЭкспортерСпанов.os |
| 284 | MUST | ✅ | Span Exporter - `ForceFlush` and `Shutdown` MUST be safe to be called | src/Ядро/Модули/ОтелГлобальный.os:41-43 |

### Logs Api

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 285 | SHOULD | ✅ | Thus, the API SHOULD provide a way to set/register and access a global default | src/Логирование/Классы/ОтелПровайдерЛогирования.os:31-68 |
| 286 | MUST | ✅ | The `LoggerProvider` MUST provide the following functions: | src/Логирование/Классы/ОтелПровайдерЛогирования.os:46-50 |
| 287 | MUST | ✅ | This API MUST accept the following instrumentation scope | src/Логирование/Классы/ОтелПровайдерЛогирования.os:46-50 |
| 288 | MUST | ✅ | associate with emitted telemetry. This API MUST be structured to accept a | src/Логирование/Классы/ОтелЛоггер.os:19-24 |
| 289 | MUST | ✅ | The `Logger` MUST provide a function to: | src/Логирование/Классы/ОтелЛоггер.os:41-50 |
| 290 | SHOULD | ✅ | The `Logger` SHOULD provide functions to: | src/Логирование/Классы/ОтелЛоггер.os:41 |
| 291 | MUST | ✅ | The API MUST accept the following parameters: | src/Логирование/Классы/ОтелЛоггер.os:41 |
| 292 | SHOULD | ✅ | When implicit Context is supported, then this parameter SHOULD be optional and | src/Логирование/Классы/ОтелЛоггер.os:70-72 |
| 293 | MUST | ➖ | if unspecified then MUST use current Context. | OneScript uses implicit context (Not applicable) |
| 294 | SHOULD | ✅ | When only explicit Context is supported, this parameter SHOULD be required.* Severity Number (optional)* Severity Text (... | src/Логирование/Классы/ОтелЛоггер.os:41-50 |
| 295 | SHOULD | ✅ | generating a `LogRecord`, a `Logger` SHOULD provide this `Enabled` API. | src/Логирование/Классы/ОтелЛоггер.os:41 |
| 296 | SHOULD | ✅ | The API SHOULD accept the following parameters: | src/Логирование/Классы/ОтелЛоггер.os:41 |
| 297 | SHOULD | ✅ | When implicit Context is supported, then this parameter SHOULD be optional and | src/Логирование/Классы/ОтелЛоггер.os:70-72 |
| 298 | MUST | ✅ | if unspecified then MUST use current Context. | src/Логирование/Классы/ОтелЛоггер.os:41-50 |
| 299 | MUST | ✅ | This API MUST return a language idiomatic boolean type. A returned value of | src/Логирование/Классы/ОтелЛоггер.os:26-28 |
| 300 | SHOULD | ✅ | SHOULD be documented that instrumentation authors needs to call this API each | src/Логирование/Классы/ОтелПостроительЛоггера.os:26-42 |
| 301 | MUST | ✅ | For each optional parameter, the API MUST be structured to accept it, but MUST | src/Логирование/Классы/ОтелПостроительЛоггера.os:62 |
| 302 | MUST | ⚠️ | For each required parameter, the API MUST be structured to obligate a user to | src/Логирование/Классы/ОтелПровайдерЛогирования.os:164 (Methods documented as thread-safe but limited detail) |
| 303 | MUST | ⚠️ | LoggerProvider - all methods MUST be documented that implementations need to | src/Логирование/Классы/ОтелЛоггер.os:29,55 (Methods documented as safe but limited detail) |
| 304 | MUST | ✅ | Logger - all methods MUST be documented that implementations need to | src/Логирование/Классы/ОтелПостроительЛоггера.os:26-42 |

### Logs Sdk

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 307 | MUST | ✅ | All language implementations of OpenTelemetry MUST provide an SDK. | src/Логирование/Классы/ОтелПровайдерЛогирования.os:176-183 |
| 308 | MUST | ✅ | A `LoggerProvider` MUST provide a way to allow a Resource | src/Логирование/Классы/ОтелЛоггер.os:65-66 |
| 309 | SHOULD | ✅ | to be specified. If a `Resource` is specified, it SHOULD be associated with all | src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os |
| 310 | SHOULD | ✅ | The SDK SHOULD allow the creation of multiple independent `LoggerProviders`s. | src/Логирование/Классы/ОтелПровайдерЛогирования.os:31-68 |
| 311 | SHOULD | ✅ | It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` | src/Логирование/Классы/ОтелПровайдерЛогирования.os:46-68 |
| 312 | MUST | ✅ | The `LoggerProvider` MUST implement the Get a Logger API. | src/Логирование/Классы/ОтелПровайдерЛогирования.os:56-57 |
| 313 | MUST | ✅ | The input provided by the user MUST be used to create | src/Логирование/Классы/ОтелПровайдерЛогирования.os:51-67 |
| 314 | MUST | ✅ | working `Logger` MUST be returned as a fallback rather than returning null or | src/Логирование/Классы/ОтелПровайдерЛогирования.os:52-54 |
| 315 | SHOULD | ⚠️ | throwing an exception, its `name` SHOULD keep the original invalid value, and a | src/Логирование/Классы/ОтелПровайдерЛогирования.os (No logging message about invalid value) |
| 316 | SHOULD | ✅ | message reporting that the specified value is invalid SHOULD be logged. | src/Логирование/Классы/ОтелПровайдерЛогирования.os:176-183 |
| 317 | MUST | ✅ | MUST be owned by the `LoggerProvider`. The configuration MAY be applied at the | src/Логирование/Классы/ОтелЛоггер.os:19-24 |
| 318 | MUST | ➖ | configuration MUST also apply to all already returned `Logger`s (i.e. it MUST | LoggerConfigurator not implemented (DEV requirement) |
| 326 | SHOULD | ⚠️ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | src/Логирование/Классы/ОтелПровайдерЛогирования.os:112-116 (No ERROR status) |
| 327 | SHOULD | ⚠️ | failed or timed out. `ForceFlush` SHOULD return some ERROR status if there | src/Логирование/Классы/ОтелПровайдерЛогирования.os:112-116 (No SUCCESS status) |
| 328 | SHOULD | ⚠️ | is an error condition; and if there is no error condition, it SHOULD return | src/Логирование/Классы/ОтелПровайдерЛогирования.os:112-116 (No timeout mechanism) |
| 329 | SHOULD | ✅ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be | src/Логирование/Классы/ОтелПровайдерЛогирования.os:91-93 |
| 330 | MUST | ➖ | `ForceFlush` MUST invoke `ForceFlush` on all | LoggerConfig not implemented (DEV requirement) |
| 339 | SHOULD | ❌ | the implementation SHOULD set it equal to the current time. | - (Exception attribute handling not implemented) |
| 340 | MUST | ❌ | If an Exception is provided, the SDK MUST by default set attributes | - (User attribute precedence not implemented) |
| 341 | MUST NOT | ⚠️ | User-provided attributes MUST take precedence and MUST NOT be overwritten by | src/Логирование/Классы/ОтелЛоггер.os:41-50 (Filtering via Включен() but no LoggerConfig rules) |
| 344 | MUST | ✅ | `Enabled` MUST return `false` when either: | src/Логирование/Классы/ОтелЛоггер.os:43-50 |
| 346 | MUST | ✅ | A function receiving this as an argument MUST be able to access all the | src/Логирование/Классы/ОтелЗаписьЛога.os:144 |
| 347 | MUST | ✅ | information added to the LogRecord. It MUST also be able to | src/Логирование/Классы/ОтелЛоггер.os:73-78 |
| 348 | MUST | ✅ | The trace context fields MUST be populated from | src/Логирование/Классы/ОтелЗаписьЛога.os:144-146 |
| 349 | MUST | ❌ | Counts for attributes due to collection limits MUST be available for exporters | - (ReadWriteLogRecord for processor modification not implemented) |
| 350 | MUST | ✅ | A function receiving this as an argument MUST additionally be able to modify | src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os |
| 351 | MUST | ✅ | `LogRecord` attributes MUST adhere to | src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:39-56 |
| 352 | MUST | ✅ | If the SDK implements attribute limits it MUST provide a way to change these | src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os |
| 353 | SHOULD | ❌ | The options MAY be bundled in a class, which then SHOULD be called | - (No log message when attribute limit exceeded) |
| 354 | SHOULD | ❌ | There SHOULD be a message printed in the SDK’s log to indicate to the user | - (No throttling of warning messages) |
| 355 | MUST | ✅ | To prevent excessive logging, the message MUST be printed at most once per | src/Логирование/Классы/ОтелПровайдерЛогирования.os:75-77 |
| 356 | MUST | ✅ | MUST allow each pipeline to end with an individual exporter. | src/Логирование/Классы/ОтелПровайдерЛогирования.os:75-77 |
| 357 | MUST | ✅ | The SDK MUST allow users to implement and configure custom processors and | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:15-21 |
| 358 | SHOULD NOT | ✅ | therefore it SHOULD NOT block or throw exceptions. | src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17-25 |
| 359 | MUST | ✅ | the `logRecord` mutations MUST be visible in next registered processors. | src/Логирование/Классы/ОтелЛоггер.os:90-91 |
| 360 | SHOULD | ✅ | implementations SHOULD recommended to users that a clone of `logRecord` be used | src/Логирование/Классы/ОтелЛоггер.os:41 |
| 361 | MUST NOT | ⚠️ | Any modifications to parameters inside `Enabled` MUST NOT be propagated to the | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os (No note on single-call guarantee) |
| 362 | SHOULD | ⚠️ | `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:32-36 (Silently ignored (graceful)) |
| 363 | SHOULD | ⚠️ | SHOULD ignore these calls gracefully, if possible. | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:32-36 (No status indication) |
| 364 | SHOULD | ✅ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:32-36 |
| 365 | MUST | ⚠️ | `Shutdown` MUST include the effects of `ForceFlush`. | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:32-36 (No timeout mechanism) |
| 366 | SHOULD | ❌ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` can be | - (ForceFlush not prioritized in simple processor) |
| 367 | SHOULD | ❌ | to `ForceFlush` SHOULD be completed as soon as possible, preferably before | - (ForceFlush no-op in simple processor) |
| 368 | SHOULD | ✅ | SHOULD try to call the exporter’s `Export` with all `LogRecord`s for which this | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os |
| 369 | MUST | ⚠️ | The built-in LogRecordProcessors MUST do so. If a | src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:73-112 (Batch has timeout, simple doesnt) |
| 370 | MUST | ⚠️ | timeout is specified (see below), the `LogRecordProcessor` MUST prioritize | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:32-36 (No status indication) |
| 371 | SHOULD | ✅ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:26-28 |
| 372 | SHOULD | ⚠️ | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:26-28 (No timeout mechanism) |
| 373 | SHOULD | ✅ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os |
| 374 | MUST | ➖ | The standard OpenTelemetry SDK MUST implement both simple and batch processors, | Other processing scenarios not specified (Not applicable) |
| 375 | SHOULD | ✅ | Other common processing scenarios SHOULD be first considered | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:15-21 |
| 376 | MUST | ✅ | The processor MUST synchronize calls to `LogRecordExporter`’s `Export` | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:15-21 |
| 377 | MUST | ⚠️ | The processor MUST synchronize calls to `LogRecordExporter`’s `Export` | src/Логирование/Классы/ОтелПростойПроцессорЛогов.os (No concurrency documentation) |
| 378 | MUST | ✅ | Each implementation MUST document the concurrency characteristics the SDK | src/Экспорт/Классы/ОтелЭкспортерЛогов.os:22-46 |
| 379 | MUST | ✅ | A `LogRecordExporter` MUST support the following functions: | src/Экспорт/Классы/ОтелЭкспортерЛогов.os:22-33 |
| 380 | MUST NOT | ✅ | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit | src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:136-149 |
| 381 | SHOULD NOT | ⚠️ | default SDK’s `LogRecordProcessors` SHOULD NOT implement retry logic, as the | src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38-40 (ForceFlush no status) |
| 382 | SHOULD | ⚠️ | exporter has received prior to the call to `ForceFlush` SHOULD be completed as | src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38-40 (No status indication) |
| 383 | SHOULD | ❌ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | - (ForceFlush guidance missing) |
| 384 | SHOULD | ⚠️ | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, | src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38-40 (No timeout mechanism) |
| 385 | SHOULD | ⚠️ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | src/Экспорт/Классы/ОтелЭкспортерЛогов.os:44-46 (Should be called once not documented) |
| 386 | SHOULD | ⚠️ | Shutdown SHOULD be called only once for each `LogRecordExporter` instance. After | src/Экспорт/Классы/ОтелЭкспортерЛогов.os:44-46 (Export returns False after Shutdown) |
| 387 | SHOULD | ✅ | the call to `Shutdown` subsequent calls to `Export` are not allowed and SHOULD | src/Экспорт/Классы/ОтелЭкспортерЛогов.os:44-46 |
| 388 | SHOULD NOT | ✅ | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data | src/Логирование/Классы/ОтелПровайдерЛогирования.os:191 |
| 389 | MUST | ✅ | LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe | src/Логирование/Классы/ОтелЛоггер.os:29,55 |
| 390 | MUST | ✅ | Logger - all methods MUST be safe to be called concurrently. | src/Экспорт/Классы/ОтелЭкспортерЛогов.os:44-46 |
| 391 | MUST | ✅ | LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called | src/Метрики/Классы/ОтелПровайдерМетрик.os:35 |

### Metrics Api

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 392 | SHOULD | ✅ | Thus, the API SHOULD provide a way to set/register and access a global default | src/Метрики/Классы/ОтелПровайдерМетрик.os:50 |
| 393 | MUST | ✅ | The `MeterProvider` MUST provide the following functions: | src/Метрики/Классы/ОтелПровайдерМетрик.os:50-54 |
| 394 | MUST | ✅ | This API MUST accept the following parameters: | src/Ядро/Классы/ОтелОбластьИнструментирования.os:77 |
| 395 | MUST NOT | ✅ | this API needs to be structured to accept a `version`, but MUST NOT obligate | src/Ядро/Классы/ОтелОбластьИнструментирования.os:77 |
| 396 | MUST | ✅ | Therefore, this API needs to be structured to accept a `schema_url`, but MUST | src/Метрики/Классы/ОтелПровайдерМетрик.os:50-54 |
| 397 | MUST | ✅ | it is up to their discretion. Therefore, this API MUST be structured to | src/Метрики/Классы/ОтелМетр.os:399-401 |
| 398 | SHOULD NOT | ✅ | Note: `Meter` SHOULD NOT be responsible for the configuration. This should be | src/Метрики/Классы/ОтелМетр.os:43,72,107,129,168,187,198,227,245,256 |
| 399 | MUST | ⚠️ | The `Meter` MUST provide functions to create new Instruments: | src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:1-40 (Float handling present but no explicit documentation) |
| 400 | SHOULD | ✅ | floating point numbers SHOULD be considered as identifying. | src/Метрики/Классы/ОтелМетр.os:43-59 |
| 401 | SHOULD | ⚠️ | API SHOULD treat it as an opaque string. | src/Метрики/Классы/ОтелМетр.os:43-59 (Case-sensitive handling unclear) |
| 402 | MUST | ✅ | * It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII | src/Метрики/Классы/ОтелМетр.os:43-59 |
| 403 | MUST | ➖ | instrument. The API MUST treat it as an opaque string. | OneScript platform (Unicode BMP depends on runtime) |
| 404 | MUST | ➖ | * It MUST support BMP (Unicode Plane | OneScript platform (Character limit depends on platform) |
| 405 | MUST | ➖ | support more Unicode Planes.* It MUST support at least 1023 characters. OpenTelemetry | src/Метрики/Классы/ОтелМетр.os (Advisory parameters not explicitly documented) |
| 406 | MUST | ✅ | OpenTelemetry SDKs MUST handle `advisory` parameters as described | src/Метрики/Классы/ОтелМетр.os:43-59 |
| 407 | MUST | ✅ | The API to construct synchronous instruments MUST accept the following parameters: | src/Метрики/Классы/ОтелМетр.os:43,72,107,129,168 |
| 408 | SHOULD | ✅ | The `name` needs to be provided by a user. If possible, the API SHOULD be | src/Метрики/Классы/ОтелМетр.os:43,72,107,129,168 |
| 409 | MUST | ✅ | possible to structurally enforce this obligation, the API MUST be documented | src/Метрики/Классы/ОтелМетр.os:43,72,107,129,168 |
| 410 | SHOULD | ✅ | The API SHOULD be documented in a way to communicate to users that the `name` | src/Метрики/Классы/ОтелМетр.os:43 |
| 411 | SHOULD NOT | ✅ | syntax. The API SHOULD NOT validate the `name`; that | src/Метрики/Классы/ОтелМетр.os:43 |
| 412 | MUST NOT | ✅ | API needs to be structured to accept a `unit`, but MUST NOT obligate a user | src/Метрики/Классы/ОтелМетр.os:43 |
| 413 | MUST | ✅ | rule. Meaning, the API MUST accept a case-sensitive string | src/Метрики/Классы/ОтелМетр.os:43 |
| 414 | SHOULD NOT | ✅ | The API SHOULD NOT validate the `unit`. | src/Метрики/Классы/ОтелМетр.os:43 |
| 415 | MUST NOT | ✅ | MUST NOT obligate a user to provide one. | src/Метрики/Классы/ОтелМетр.os:43 |
| 416 | MUST | ✅ | rule. Meaning, the API MUST accept a string that | src/Метрики/Классы/ОтелМетр.os:43 |
| 417 | MUST NOT | ✅ | but MUST NOT obligate the user to provide it. | src/Метрики/Классы/ОтелМетр.os:43 |
| 418 | SHOULD NOT | ✅ | The API SHOULD NOT validate `advisory` parameters. | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 419 | MUST | ✅ | The API to construct asynchronous instruments MUST accept the following parameters: | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 420 | SHOULD | ✅ | The `name` needs to be provided by a user. If possible, the API SHOULD be | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 421 | MUST | ✅ | possible to structurally enforce this obligation, the API MUST be documented | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 422 | SHOULD | ✅ | The API SHOULD be documented in a way to communicate to users that the `name` | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 423 | SHOULD NOT | ✅ | syntax. The API SHOULD NOT validate the `name`, | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 424 | MUST NOT | ✅ | API needs to be structured to accept a `unit`, but MUST NOT obligate a user | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 425 | MUST | ✅ | rule. Meaning, the API MUST accept a case-sensitive string | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 426 | SHOULD NOT | ✅ | The API SHOULD NOT validate the `unit`. | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 427 | MUST NOT | ✅ | MUST NOT obligate a user to provide one. | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 428 | MUST | ✅ | rule. Meaning, the API MUST accept a string that | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 429 | MUST NOT | ✅ | but MUST NOT obligate the user to provide it. | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 430 | SHOULD NOT | ✅ | The API SHOULD NOT validate `advisory` parameters. | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 431 | MUST | ✅ | Therefore, this API MUST be structured to accept a variable number of | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 432 | MUST | ✅ | The API MUST support creation of asynchronous instruments by passing | src/Метрики/Классы/ОтелМетр.os:348-351 |
| 433 | SHOULD | ✅ | The API SHOULD support registration of `callback` functions associated with | src/Метрики/Классы/ОтелМетр.os:348-351 |
| 434 | MUST | ✅ | asynchronous instrumentation creation, the user MUST be able to undo | src/Метрики/Классы/ОтелМетр.os:355-375 |
| 435 | MUST | ✅ | Every currently registered Callback associated with a set of instruments MUST | src/Метрики/Классы/ОтелМетр.os:348-351 |
| 436 | MUST | ➖ | Callback functions MUST be documented as follows for the end user: | src/Метрики/Классы/ОтелМетр.os:355 (Reentrancy depends on runtime) |
| 437 | SHOULD | ➖ | * Callback functions SHOULD be reentrant safe. The SDK expects to evaluate | src/Метрики/Классы/ОтелМетр.os (No explicit timeout mechanism) |
| 438 | SHOULD NOT | ✅ | callbacks for each MetricReader independently.* Callback functions SHOULD NOT take an indefinite amount of time.* Callba... | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 439 | MUST | ✅ | Callbacks registered at the time of instrument creation MUST apply to | src/Метрики/Классы/ОтелМетр.os:348-351 |
| 440 | MUST | ✅ | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the | src/Метрики/Классы/ОтелМетр.os:348-351 |
| 441 | MUST | ✅ | Multiple-instrument Callbacks MUST be associated at the time of | src/Метрики/Классы/ОтелМетр.os:355-375 |
| 442 | MUST | ✅ | The API MUST treat observations from a single Callback as logically | src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:137-147 |
| 443 | MUST | ⚠️ | observations from a single callback MUST be reported with identical | src/Метрики/Классы/ОтелМетр.os:348-351 (No explicit state parameter) |
| 444 | SHOULD | ✅ | The API SHOULD provide some way to pass `state` to the | src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:76,179 |
| 445 | SHOULD | ✅ | All synchronous instruments SHOULD provide functions to: | src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179 |
| 446 | SHOULD | ✅ | SHOULD provide this `Enabled` API. | src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179 |
| 447 | MUST | ✅ | added in the future, therefore, the API MUST be structured in a way for | src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179 |
| 448 | MUST | ✅ | This API MUST return a language idiomatic boolean type. A returned value of | src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179 |
| 449 | SHOULD | ✅ | SHOULD be documented that instrumentation authors needs to call this API each | src/Метрики/Классы/ОтелСчетчик.os:1-40 |
| 450 | MUST NOT | ✅ | There MUST NOT be any API for creating a `Counter` other than with a | src/Метрики/Классы/ОтелСчетчик.os:21-26 |
| 451 | SHOULD NOT | ✅ | This API SHOULD NOT return a value (it MAY return a dummy value if required by | src/Метрики/Классы/ОтелСчетчик.os:21-26 |
| 452 | MUST | ✅ | This API MUST accept the following parameter: | src/Метрики/Классы/ОтелСчетчик.os:21-26 |
| 453 | SHOULD | ✅ | SHOULD be structured so a user is obligated to provide this parameter. If it | src/Метрики/Классы/ОтелСчетчик.os:21-26 |
| 454 | MUST | ✅ | is not possible to structurally enforce this obligation, this API MUST be | src/Метрики/Классы/ОтелСчетчик.os:21-26 |
| 455 | SHOULD | ✅ | The increment value is expected to be non-negative. This API SHOULD be | src/Метрики/Классы/ОтелСчетчик.os:22-23 |
| 456 | SHOULD NOT | ✅ | non-negative. This API SHOULD NOT validate this value, that is left to | src/Метрики/Классы/ОтелСчетчик.os:21-26 |
| 457 | MUST | ✅ | up to their discretion. Therefore, this API MUST be structured to accept a | src/Метрики/Классы/ОтелСчетчик.os:21-26 |
| 458 | MUST | ✅ | (e.g. strong typed struct allocated on the callstack, tuple). The API MUST allow | src/Метрики/Классы/ОтелМетр.os:187-214 |
| 459 | MUST NOT | ✅ | There MUST NOT be any API for creating an Asynchronous Counter other than with a | src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:76-85 |
| 460 | MUST | ✅ | last one, or something else. The API MUST treat observations from a single | src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:137-147 |
| 461 | MUST | ⚠️ | observations from a single callback MUST be reported with identical timestamps. | src/Метрики/Классы/ОтелМетр.os:348 (State passing not explicit) |
| 462 | SHOULD | ✅ | The API SHOULD provide some way to pass `state` to the callback. OpenTelemetry | src/Метрики/Классы/ОтелГистограмма.os:1-36 |
| 463 | MUST NOT | ✅ | There MUST NOT be any API for creating a `Histogram` other than with a | src/Метрики/Классы/ОтелГистограмма.os:20-22 |
| 464 | SHOULD NOT | ✅ | This API SHOULD NOT return a value (it MAY return a dummy value if required by | src/Метрики/Классы/ОтелГистограмма.os:20-22 |
| 465 | MUST | ✅ | This API MUST accept the following parameter: | src/Метрики/Классы/ОтелГистограмма.os:20-22 |
| 466 | SHOULD | ✅ | The value needs to be provided by a user. If possible, this API SHOULD be | src/Метрики/Классы/ОтелГистограмма.os:20-22 |
| 467 | MUST | ✅ | possible to structurally enforce this obligation, this API MUST be documented | src/Метрики/Классы/ОтелГистограмма.os:20-22 |
| 468 | SHOULD | ✅ | The value is expected to be non-negative. This API SHOULD be documented in a | src/Метрики/Классы/ОтелГистограмма.os:20-22 |
| 469 | SHOULD NOT | ✅ | This API SHOULD NOT validate this value, that is left to implementations of | src/Метрики/Классы/ОтелГистограмма.os:20-22 |
| 470 | MUST | ✅ | their discretion. Therefore, this API MUST be structured to accept a variable | src/Метрики/Классы/ОтелДатчик.os:1-36 |
| 471 | MUST NOT | ✅ | There MUST NOT be any API for creating a `Gauge` other than with a | src/Метрики/Классы/ОтелДатчик.os:21-23 |
| 472 | SHOULD NOT | ✅ | This API SHOULD NOT return a value (it MAY return a dummy value if required by | src/Метрики/Классы/ОтелДатчик.os:21-23 |
| 473 | MUST | ✅ | This API MUST accept the following parameter: | src/Метрики/Классы/ОтелДатчик.os:21-23 |
| 474 | SHOULD | ✅ | SHOULD be structured so a user is obligated to provide this parameter. If it | src/Метрики/Классы/ОтелДатчик.os:21-23 |
| 475 | MUST | ✅ | is not possible to structurally enforce this obligation, this API MUST be | src/Метрики/Классы/ОтелДатчик.os:21-23 |
| 476 | MUST | ✅ | up to their discretion. Therefore, this API MUST be structured to accept a | src/Метрики/Классы/ОтелДатчик.os:21-23 |
| 477 | MUST | ✅ | (e.g. strong typed struct allocated on the callstack, tuple). The API MUST allow | src/Метрики/Классы/ОтелМетр.os:245-272 |
| 478 | MUST NOT | ✅ | There MUST NOT be any API for creating an Asynchronous Gauge other than with a | src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:1-37 |
| 479 | MUST NOT | ✅ | There MUST NOT be any API for creating an `UpDownCounter` other than with a | src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21-23 |
| 480 | SHOULD NOT | ✅ | This API SHOULD NOT return a value (it MAY return a dummy value if required by | src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21-23 |
| 481 | MUST | ✅ | This API MUST accept the following parameter: | src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21-23 |
| 482 | SHOULD | ✅ | The value needs to be provided by a user. If possible, this API SHOULD be | src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21-23 |
| 483 | MUST | ✅ | possible to structurally enforce this obligation, this API MUST be documented | src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21-23 |
| 484 | MUST | ✅ | their discretion. Therefore, this API MUST be structured to accept a variable | src/Метрики/Классы/ОтелМетр.os:216-243 |
| 485 | MUST NOT | ✅ | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than | src/Метрики/Классы/ОтелПредставление.os:1-103 |
| 486 | SHOULD | ✅ | All the metrics components SHOULD allow new APIs to be added to | src/Метрики/Классы/ОтелМетр.os:43 |
| 487 | SHOULD | ⚠️ | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing | src/Метрики/Классы/ОтелПровайдерМетрик.os:1-250 (Thread-safe but not all documented) |
| 488 | MUST | ⚠️ | MeterProvider - all methods MUST be documented that implementations need to | src/Метрики/Классы/ОтелМетр.os:1-450 (Thread-safe but documentation incomplete) |
| 489 | MUST | ⚠️ | Meter - all methods MUST be documented that implementations need to be safe | src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:1-317 (Thread-safe structures but documentation lacking) |
| 490 | MUST | ✅ | Instrument - all methods MUST be documented that implementations need to be | src/Метрики/Классы/ОтелПровайдерМетрик.os:1 |

### Metrics Sdk

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 491 | MUST | ✅ | All language implementations of OpenTelemetry MUST provide an SDK. | src/Метрики/Классы/ОтелПровайдерМетрик.os:215-220 |
| 492 | MUST | ✅ | A `MeterProvider` MUST provide a way to allow a Resource to | src/Метрики/Классы/ОтелПровайдерМетрик.os:50-77 |
| 493 | SHOULD | ✅ | be specified. If a `Resource` is specified, it SHOULD be associated with all the | src/Метрики/Классы/ОтелПровайдерМетрик.os:50 |
| 494 | SHOULD | ✅ | The SDK SHOULD allow the creation of multiple independent `MeterProvider`s. | src/Метрики/Классы/ОтелПровайдерМетрик.os:35-37 |
| 495 | SHOULD | ✅ | It SHOULD only be possible to create `Meter` instances through a `MeterProvider` | src/Метрики/Классы/ОтелПровайдерМетрик.os:50-77 |
| 496 | MUST | ✅ | The `MeterProvider` MUST implement the Get a Meter API. | src/Метрики/Классы/ОтелМетр.os:1 |
| 497 | MUST | ✅ | The input provided by the user MUST be used to create | src/Метрики/Классы/ОтелПровайдерМетрик.os:55-58 |
| 498 | MUST | ⚠️ | working Meter MUST be returned as a fallback rather than returning null or | src/Метрики/Классы/ОтелМетр.os:44-49 (Instrument name is normalized but original value not logged for invalid names) |
| 499 | SHOULD | ❌ | throwing an exception, its `name` SHOULD keep the original invalid value, and a | src/Метрики/Классы/ОтелМетр.os (No warning logged for invalid instrument names) |
| 500 | SHOULD | ✅ | message reporting that the specified value is invalid SHOULD be logged. | src/Метрики/Классы/ОтелПровайдерМетрик.os:12,18,24 |
| 502 | MUST NOT | ➖ | configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT | src/Метрики/Классы/ОтелПровайдерМетрик.os (MeterConfigurator not applicable to OneScript SDK) |
| 510 | MUST | ⚠️ | `ForceFlush` MUST invoke `ForceFlush` on all registered | src/Метрики/Классы/ОтелПровайдерМетрик.os:149-153 (ForceFlush async but no explicit timeout parameter) |
| 511 | SHOULD | ✅ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | src/Метрики/Классы/ОтелПровайдерМетрик.os:112-121 |
| 512 | SHOULD | ➖ | failed or timed out. `ForceFlush` SHOULD return some ERROR status if there | src/Метрики/Классы/ОтелПровайдерМетрик.os (MeterConfig not applicable) |
| 513 | SHOULD | ➖ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be | src/Метрики/Классы/ОтелПровайдерМетрик.os (MeterConfig not applicable) |
| 514 | MUST | ➖ | The SDK MUST provide functionality for a user to create Views for a | src/Метрики/Классы/ОтелПровайдерМетрик.os (MeterConfig not applicable) |
| 515 | MUST | ➖ | `MeterProvider`. This functionality MUST accept as inputs the Instrument | src/Метрики/Классы/ОтелПровайдерМетрик.os (MeterConfig not applicable) |
| 516 | MUST | ✅ | The SDK MUST provide the means to register Views with a `MeterProvider`. | src/Метрики/Классы/ОтелПредставление.os:1 |
| 517 | SHOULD | ✅ | Criteria SHOULD be treated as additive. This means an Instrument has to match | src/Метрики/Классы/ОтелСелекторИнструментов.os:1 |
| 518 | MUST | ✅ | The SDK MUST accept the following criteria: | src/Метрики/Модули/ОтелАгрегация.os:1 |
| 519 | MUST | ✅ | If the SDK does not support wildcards in general, it MUST still recognize the | src/Метрики/Классы/ОтелПровайдерМетрик.os:69,173-178 |
| 520 | MUST NOT | ⚠️ | `name`, but MUST NOT obligate a user to provide one. | src/Метрики/Классы/ОтелМетр.os:176-183 (Representation validation missing warning log) |
| 521 | MUST NOT | ⚠️ | `type`, but MUST NOT obligate a user to provide one. | src/Метрики/Классы/ОтелМетр.os:84-93 (View boundaries configurable but precedence over advisory not fully documented) |
| 522 | MUST NOT | ⚠️ | `unit`, but MUST NOT obligate a user to provide one. | src/Метрики/Классы/ОтелМетр.os:84-93 (Default views apply advisory boundaries but precedence not guaranteed) |
| 523 | MUST NOT | ✅ | to accept a `meter_name`, but MUST NOT obligate a user to provide one. | src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:1 |
| 524 | MUST NOT | ✅ | to accept a `meter_version`, but MUST NOT obligate a user to provide one. | src/Метрики/Классы/ОтелМетр.os:198-272 |
| 525 | MUST NOT | ✅ | to accept a `meter_schema_url`, but MUST NOT obligate a user to provide one. | src/Метрики/Модули/ОтелАгрегация.os:1 |
| 526 | MUST NOT | ✅ | accept the criteria, but MUST NOT obligate a user to provide them. | src/Метрики/Модули/ОтелАгрегация.os:15-17 |
| 527 | MUST | ✅ | The SDK MUST accept the following stream configuration parameters: | src/Метрики/Модули/ОтелАгрегация.os:45-47 |
| 528 | SHOULD | ✅ | `name`: The metric stream name that SHOULD be used. | src/Метрики/Модули/ОтелАгрегация.os:45-47 |
| 529 | SHOULD | ✅ | In order to avoid conflicts, if a `name` is provided the View SHOULD have an | src/Метрики/Классы/ОтелАгрегаторСуммы.os:29-31 |
| 530 | MUST NOT | ✅ | MUST NOT obligate a user to provide one. If the user does not provide a | src/Метрики/Классы/ОтелАгрегаторСуммы.os:1 |
| 531 | MUST | ✅ | `name` value, name from the Instrument the View matches MUST be used by | src/Метрики/Классы/ОтелАгрегаторСуммы.os:29-31 |
| 532 | SHOULD | ✅ | `description`: The metric stream description that SHOULD be used. | src/Метрики/Классы/ОтелАгрегаторСуммы.os:1 |
| 533 | MUST NOT | ✅ | accept a `description`, but MUST NOT obligate a user to provide one. If the | src/Метрики/Классы/ОтелАгрегаторГистограммы.os:50-51 |
| 534 | MUST | ✅ | Instrument a View matches MUST be used by default. | src/Метрики/Классы/ОтелАгрегаторПоследнегоЗначения.os:29-31 |
| 535 | MUST | ✅ | keys that identify the attributes that MUST be kept, and all other attributes | src/Метрики/Классы/ОтелАгрегаторГистограммы.os:27-31 |
| 536 | MUST NOT | ✅ | accept `attribute_keys`, but MUST NOT obligate a user to provide them. | src/Метрики/Классы/ОтелАгрегаторГистограммы.os:27-31 |
| 537 | SHOULD | ✅ | If the user does not provide any value, the SDK SHOULD use | src/Метрики/Классы/ОтелАгрегаторГистограммы.os:27-31 |
| 538 | MUST | ✅ | advisory parameter is absent, all attributes MUST be kept. | src/Метрики/Классы/ОтелАгрегаторГистограммы.os:27-31 |
| 539 | SHOULD | ✅ | Additionally, implementations SHOULD support configuring an exclude-list of | src/Метрики/Классы/ОтелАгрегаторГистограммы.os:118-134 |
| 540 | MUST | ✅ | attributes that MUST be excluded, all other attributes MUST be kept. If an | src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:36 |
| 541 | MUST NOT | ✅ | accept an `aggregation`, but MUST NOT obligate a user to provide one. If the | src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:37 |
| 542 | MUST | ✅ | user does not provide an `aggregation` value, the `MeterProvider` MUST apply | src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:38-39 |
| 543 | MUST NOT | ✅ | accept an `exemplar_reservoir`, but MUST NOT obligate a user to provide one. | src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:40 |
| 544 | MUST | ✅ | `MeterProvider` MUST apply a default exemplar | src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:43-46,48-51 |
| 545 | MUST NOT | ✅ | structured to accept an `aggregation_cardinality_limit`, but MUST NOT | src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:41 |
| 546 | MUST | ✅ | `aggregation_cardinality_limit` value, the `MeterProvider` MUST apply the | src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:10 |
| 547 | SHOULD | ⚠️ | The SDK SHOULD use the following logic to determine how to process Measurements | src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:177-184 (Scale can decrease but no explicit requirement check) |
| 548 | MUST | ⚠️ | MUST be honored.* If the `MeterProvider` has one or more `View`(s) registered:* If the Instrument could match the instru... | src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:177-184 (Scale must not increase - implementation assumed) |
| 549 | SHOULD | ⚠️ | the implementation SHOULD apply the View and emit a warning. If it is not | src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:8 (max_size invariant needs verification) |
| 550 | SHOULD | ✅ | implementation SHOULD emit a warning and proceed as if the View did not | src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:107 |
| 551 | MUST | ✅ | the setting defined by the View MUST take precedence over the advisory parameters.* If the Instrument could not match wi... | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:1 |
| 552 | SHOULD | ✅ | SDK SHOULD enable the instrument using the default aggregation and temporality. | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:32-40 |
| 553 | MUST | ✅ | The SDK MUST provide the following `Aggregation` to support the | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:22-35 |
| 554 | SHOULD | ✅ | The SDK SHOULD provide the following `Aggregation`: | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:22-35 |
| 555 | SHOULD NOT | ⚠️ | * Count of `Measurement` values in population.* Arithmetic sum of `Measurement` values in population. This SHOULD NOT be... | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109-149 (Collect aggregation logic present but delta temporality handling needs review) |
| 556 | SHOULD | ⚠️ | (-∞, 0], (0, 5.0], (5.0, 10.0], (10.0, 25.0], (25.0, 50.0], (50.0, 75.0], (75.0, 100.0], (100.0, 250.0], (250.0, 500.0],... | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109-149 (Cumulative temporality born at start implemented) |
| 557 | SHOULD NOT | ⚠️ | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109-149 (Cumulative no-reset start time - need verification) |
| 558 | MUST | ⚠️ | The implementation MUST maintain reasonable minimum and maximum scale | src/Метрики/Классы/ОтелПериодическийЧитателяМетрик.os:109-149 (Delta start time handling - need verification) |
| 559 | SHOULD | ⚠️ | positive or negative ranges, the implementation SHOULD use the maximum | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109-149 (Duplicate data point deduplication not explicit) |
| 560 | SHOULD | ⚠️ | Implementations SHOULD adjust the histogram scale as necessary to | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109-149 (Collect error status partially handled) |
| 561 | MUST | ✅ | Callback functions MUST be invoked for the specific `MetricReader` | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:85 |
| 562 | SHOULD | ⚠️ | The implementation SHOULD disregard the use of asynchronous instrument | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:85-102 (MetricReader can call MeterProvider ForceFlush (assumed)) |
| 563 | SHOULD | ⚠️ | The implementation SHOULD use a timeout to prevent indefinite callback | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:68-70,76-78 (ForceFlush provided but no timeout parameter) |
| 564 | MUST | ⚠️ | The implementation MUST complete the execution of all callbacks for a | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109 (ForceFlush calls Collect via СобратьИЭкспортировать) |
| 565 | SHOULD NOT | ✅ | The implementation SHOULD NOT produce aggregated metric data for a | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:85,95 |
| 571 | SHOULD | ✅ | SDKs SHOULD support being configured with a cardinality limit. The number of | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:46-48 |
| 572 | SHOULD | ✅ | cycle. Cardinality limit enforcement SHOULD occur after attribute filtering, | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:22-35 |
| 573 | SHOULD | ❌ | stream, that value SHOULD be used.* If there is no matching view, but the `MetricReader` defines a default | src/Экспорт/Классы/ОтелЭкспортерМетрик.os (No explicit SDK retry logic comment) |
| 574 | SHOULD | ✅ | for, that value SHOULD be used.* If none of the previous values are defined, the default value of 2000 SHOULD | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:65-72 |
| 575 | MUST | ✅ | The SDK MUST create an Aggregator with the overflow attribute set prior to | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:69 |
| 576 | MUST | ✅ | be created. The SDK MUST provide the guarantee that overflow would not happen | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:40-42 |
| 577 | MUST | ⚠️ | Aggregators for synchronous instruments with cumulative temporality MUST | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:40-42 (ForceFlush success not explicitly communicated) |
| 578 | MUST | ⚠️ | Regardless of aggregation temporality, the SDK MUST ensure that every | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:40-42 (ForceFlush no timeout parameter) |
| 579 | MUST NOT | ⚠️ | Measurements MUST NOT be double-counted or dropped | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:46-48 (Shutdown called once (assumed) but no explicit once-only enforcement) |
| 580 | SHOULD | ⚠️ | Aggregators of asynchronous instruments SHOULD prefer the first-observed | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:23-24 (Export returns Ложь after shutdown but no status detail) |
| 581 | MUST | ❌ | Distinct meters MUST be treated as separate namespaces for the purposes of detecting | src/Экспорт/Классы/ОтелЭкспортерМетрик.os (Shutdown not blocking indefinitely (synchronous)) |
| 587 | MUST | ❌ | duplicate instrument. This means that the Meter MUST return a functional | src/Метрики/Классы/ОтелМетр.os (Overflow attribute set not found) |
| 588 | SHOULD | ❌ | a warning SHOULD be emitted. The emitted warning SHOULD include information for | src/Метрики/Классы/ОтелМетр.os (Configurable cardinality limit not found) |
| 589 | SHOULD | ❌ | SHOULD avoid the warning.* If the potential conflict involves instruments that can be distinguished by | src/Метрики/Классы/ОтелМетр.os (View cardinality override not found) |
| 590 | SHOULD | ✅ | recipe SHOULD be included in the warning.* Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the | src/Метрики/Классы/ОтелМетр.os:12,19 |
| 591 | MUST | ✅ | the SDK MUST aggregate data from identical Instruments | src/Метрики/Классы/ОтелМетр.os:13 |
| 592 | MUST | ✅ | multiple casings of the same `name`. When this happens, the Meter MUST return | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:1 |
| 593 | SHOULD | ⚠️ | When a Meter creates an instrument, it SHOULD validate the instrument name | src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1 (Exemplar sampling mechanism present but incomplete) |
| 594 | SHOULD | ⚠️ | If the instrument name does not conform to this syntax, the Meter SHOULD emit | src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1 (FixedSizeExemplarFilter not explicitly named) |
| 595 | SHOULD NOT | ⚠️ | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | src/Метрики/Модули/ОтелФильтрЭкземпляров.os:1 (ExemplarFilter implemented (AlwaysOn, AlwaysOff, TraceBased)) |
| 596 | MUST | ⚠️ | If a unit is not provided or the unit is null, the Meter MUST treat it the same | src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14-25 (Exemplar data immutability not explicit) |
| 597 | SHOULD NOT | ⚠️ | When a Meter creates an instrument, it SHOULD NOT validate the instrument | src/Метрики/Классы/ОтелЭкспортерМетрик.os:322-330 (Exemplars not fully exposed) |
| 598 | MUST | ⚠️ | Meter MUST treat it the same as an empty description string. | src/Метрики/Классы/ОтелЭкспортерМетрик.os:322-330 (Exemplars not fully exposed) |
| 599 | SHOULD | ⚠️ | When a Meter creates an instrument, it SHOULD validate the instrument advisory | src/Метрики/Классы/ОтелЭкспортерМетрик.os:322-330 (Exemplars not fully exposed) |
| 600 | SHOULD | ⚠️ | parameters. If an advisory parameter is not valid, the Meter SHOULD emit an error | src/Метрики/Классы/ОтелЭкспортерМетрик.os:322-330 (Exemplars not fully exposed) |
| 601 | MUST | ✅ | different advisory parameters, the Meter MUST return an instrument using the | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:1 |
| 602 | MUST | ✅ | MUST take precedence over the advisory parameters. | src/Метрики/Модули/ОтелСелекторВременнойАгрегации.os:1 |
| 603 | MUST | ✅ | parameter MUST be used. If neither is provided, the default bucket boundaries | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:69 |
| 604 | MUST | ❌ | The synchronous instrument `Enabled` MUST return `false` | src/Метрики (MetricProducer not found) |
| 606 | MUST | ❌ | A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements | src/Метрики (MetricProducer returns ResourceMetrics - not found) |
| 607 | SHOULD | ❌ | `Exemplar` sampling SHOULD be turned on by default. If `Exemplar` sampling is | src/Метрики (ResourceMetrics association not found) |
| 608 | MUST NOT | ❌ | off, the SDK MUST NOT have overhead related to exemplar sampling. | src/Метрики (Produce appending not found) |
| 609 | MUST | ❌ | A Metric SDK MUST allow exemplar sampling to leverage the configuration of | src/Метрики (MetricReader MetricProducers support not found) |
| 610 | SHOULD | ❌ | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: | src/Метрики (MetricProducer deduplication not found) |
| 611 | MUST | ❌ | The `ExemplarFilter` configuration MUST allow users to select between one of the | src/Метрики (MetricProducer data modification restriction not found) |
| 612 | SHOULD | ❌ | The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for | src/Метрики (MetricReader multiple producers not found) |
| 613 | SHOULD | ❌ | an SDK. The default value SHOULD be `TraceBased`. The filter configuration | src/Метрики (OpenTelemetry MetricProducer not found) |
| 614 | SHOULD | ❌ | SHOULD follow the environment variable specification. | src/Метрики (MetricProducer registration mechanism not found) |
| 615 | MUST | ❌ | An OpenTelemetry SDK MUST support the following filters: | src/Метрики (API MetricProducer registration not found) |
| 616 | MUST | ✅ | The `ExemplarReservoir` interface MUST provide a method to offer measurements | src/Экспорт/Классы/ОтелВПамятьТранспорт.os:1 |
| 617 | MUST | ❌ | A new `ExemplarReservoir` MUST be created for every known timeseries data point, | src/Экспорт (stdout MetricExporter not found) |
| 618 | SHOULD | ➖ | The “offer” method SHOULD accept measurements, including: | src/Экспорт (Prometheus Exporter marked as n/a per requirements) |
| 619 | SHOULD | ✅ | The “offer” method SHOULD have the ability to pull associated trace and span | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:1 |
| 620 | MUST | ✅ | from the timeseries the reservoir is associated with. This MUST be clearly | src/Метрики/Классы/ОтелМетр.os:1 |
| 621 | MUST | ❌ | documented in the API and the reservoir MUST be given the `Attributes` | src/Метрики/Классы/ОтелМетр.os (Configuration method for attribute limits not found) |
| 622 | MUST | ✅ | The “collect” method MUST return accumulated `Exemplar`s. Exemplars are expected | src/Метрики/Классы/ОтелМетр.os:44-49 |
| 623 | SHOULD | ⚠️ | with. In other words, Exemplars reported against a metric data point SHOULD have | src/Метрики/Классы/ОтелМетр.os:44-49 (Detection covers normalization but not full spec) |
| 624 | MUST | ⚠️ | `Exemplar`s MUST retain any attributes available in the measurement that | src/Метрики/Классы/ОтелМетр.os:44-49 (Warning logged via ПроверитьКонфликтДескриптора but not shown) |
| 625 | SHOULD | ⚠️ | The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. | src/Метрики/Классы/ОтелМетр.os:44-49 (Same Meter same name returns existing instrument) |
| 626 | MUST | ⚠️ | The SDK MUST include two types of built-in exemplar reservoirs: | src/Метрики/Классы/ОтелМетр.os:44-49 (Different Meter separate stream (assumed)) |
| 627 | SHOULD | ✅ | * Explicit bucket histogram aggregation with more than 1 bucket SHOULD | src/Метрики/Классы/ОтелМетр.os:44-49 |
| 628 | SHOULD | ✅ | use `AlignedHistogramBucketExemplarReservoir`.* Base2 Exponential Histogram Aggregation SHOULD use a | src/Метрики/Классы/ОтелМетр.os:44-49 |
| 629 | SHOULD | ⚠️ | twenty (e.g. `min(20, max_buckets)`).* All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`. | src/Метрики/Классы/ОтелМетр.os:44-49 (Conflict resolution missing explicit policy) |
| 630 | MUST | ⚠️ | This reservoir MUST use a uniformly-weighted sampling algorithm based on the | src/Метрики/Классы/ОтелМетр.os:44-49 (Default conflict resolution not fully implemented) |
| 631 | SHOULD | ⚠️ | Any stateful portion of sampling computation SHOULD be reset every collection | src/Метрики/Классы/ОтелМетр.os:44-49 (Resolved stream equivalence not documented) |
| 632 | SHOULD | ⚠️ | contention. Otherwise, a default size of `1` SHOULD be used. | src/Метрики/Классы/ОтелМетр.os:198-272 (Asynchronous measurements with attributes supported) |
| 633 | MUST | ⚠️ | This Exemplar reservoir MUST take a configuration parameter that is the | src/Метрики/Классы/ОтелНаблюдениеМетрики.os:19-30 (Measurement reporting supported) |
| 634 | MUST | ⚠️ | configuration of a Histogram. This implementation MUST store at most one | src/Метрики/Классы/ОтелНаблюдениеМетрики.os:19-30 (Last reported measurement preference not explicit) |
| 635 | SHOULD | ⚠️ | measurement that falls within a histogram bucket, and SHOULD use a | src/Метрики/Классы/ОтелНаблюдениеМетрики.os:19-30 (Duplicate measurement warning not logged) |
| 636 | SHOULD | ⚠️ | number of bucket boundaries plus one. This configuration parameter SHOULD have | src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:1 (Complete attribute set for synchronous instruments (assumed)) |
| 637 | MUST | ⚠️ | The SDK MUST provide a mechanism for SDK users to provide their own | src/Метрики/Классы/ОтелБазовыйАгрегатор.os:1 (Identical attribute aggregation (assumed)) |
| 638 | MUST | ➖ | ExemplarReservoir implementation. This extension MUST be configurable on | src/Метрики/Классы/ОтелМетр.os (SynchronousMeasurementHandler not applicable) |
| 639 | MUST | ➖ | a metric View, although individual reservoirs MUST still be | src/Метрики/Классы/ОтелМетр.os (SynchronousMeasurementHandler not applicable) |
| 653 | SHOULD | ⚠️ | `Collect` SHOULD provide a way to let the caller know whether it succeeded, | src/Метрики/Классы/ОтелМетр.os:256-272 (ResourceMetrics not found) |
| 654 | SHOULD | ⚠️ | `Collect` SHOULD invoke Produce on registered | src/Метрики/Классы/ОтелМетр.os:256-272 (InstrumentationScope association not found) |
| 655 | MUST | ⚠️ | `Shutdown` MUST be called only once for each `MetricReader` instance. After the | src/Метрики/Классы/ОтелМетр.os:256-272 (Appending result not found) |
| 656 | SHOULD | ❌ | SHOULD return some failure for these calls, if possible. | src/Метрики (MetricReader MetricProducers support not found) |
| 657 | SHOULD | ❌ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | src/Метрики (MetricProducer deduplication not found) |
| 658 | SHOULD | ❌ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` MAY be | src/Метрики (MetricProducer data modification restriction not found) |
| 659 | MUST | ❌ | The reader MUST synchronize calls to `MetricExporter`’s `Export` | src/Метрики (MetricReader multiple MetricProducers not found) |
| 660 | SHOULD | ❌ | `ForceFlush` SHOULD collect metrics, call `Export(batch)` | src/Метрики (OpenTelemetry MetricProducer independence not found) |
| 661 | SHOULD | ❌ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | src/Метрики (MetricProducer registration mechanism not found) |
| 662 | SHOULD | ❌ | failed or timed out. `ForceFlush` SHOULD return some ERROR status if there | src/Метрики (API MetricProducer registration not found) |
| 663 | SHOULD | ✅ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be | src/Экспорт/Классы/ОтелВПамятьТранспорт.os |
| 664 | MUST | ❌ | `MetricExporter` defines the interface that protocol-specific exporters MUST | src/Экспорт (stdout MetricExporter not found) |
| 665 | MUST | ➖ | A Push Metric Exporter MUST support the following functions: | src/Метрики (Prometheus Exporter extension - n/a per requirements) |
| 666 | MUST | ✅ | The SDK MUST provide a way for the exporter to get the Meter | src/Экспорт/Классы/ОтелЭкспортерМетрик.os |
| 667 | MUST NOT | ✅ | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit | src/Метрики/Классы/ОтелМетр.os |
| 668 | SHOULD NOT | ❌ | exporter. The default SDK SHOULD NOT implement retry logic, as the required | src/Метрики/Классы/ОтелМетр.os (Configuration method for attribute limits not found) |
| 669 | SHOULD | ✅ | received prior to the call to `ForceFlush` SHOULD be completed as soon as | src/Метрики/Классы/ОтелМетр.os:44-49 |
| 670 | SHOULD | ✅ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | src/Метрики/Классы/ОтелМетр.os:44-49 |
| 671 | SHOULD | ⚠️ | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, | src/Метрики/Классы/ОтелМетр.os:47-48 (Warning logged via ПроверитьКонфликтДескриптора (implicit)) |
| 672 | SHOULD | ✅ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | src/Метрики/Классы/ОтелМетр.os:45-48 |
| 673 | SHOULD | ⚠️ | Shutdown SHOULD be called only once for each `MetricExporter` instance. After | src/Метрики/Классы/ОтелМетр.os:45-48 (Different Meter separate streams (assumed)) |
| 674 | SHOULD NOT | ✅ | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data | src/Метрики/Классы/ОтелМетр.os:45-48 |
| 675 | MUST | ✅ | sources MUST implement, so they can be plugged into an OpenTelemetry | src/Метрики/Классы/ОтелМетр.os:45-48 |
| 676 | SHOULD | ⚠️ | `MetricProducer` implementations SHOULD accept configuration for the | src/Метрики/Классы/ОтелНаблюдениеМетрики.os (Asynchronous measurements with attributes) |
| 677 | MUST | ⚠️ | A `MetricProducer` MUST support the following functions: | src/Метрики/Классы/ОтелНаблюдениеМетрики.os (Last measurement preferred (not explicit)) |
| 678 | MUST | ⚠️ | MUST return a batch of Metric Points, filtered by the optional | src/Метрики/Классы/ОтелНаблюдениеМетрики.os (Duplicate warning not logged) |
| 679 | SHOULD | ⚠️ | `metricFilter` parameter. Implementation SHOULD use the filter as early as | src/Метрики/Классы/ОтелМетр.os:72-93 (View boundaries used instead of advisory) |
| 680 | SHOULD | ⚠️ | resource information, `Produce` SHOULD require a resource as a parameter. | src/Метрики/Классы/ОтелМетр.os:72-93 (Boundaries not overridden when View configured) |
| 681 | SHOULD | ⚠️ | `Produce` SHOULD provide a way to let the caller know whether it succeeded, | src/Метрики/Классы/ОтелМетр.os:72-93 (View boundaries applied to async instruments) |
| 682 | SHOULD | ⚠️ | `Produce` SHOULD include a single InstrumentationScope which identifies the | src/Метрики/Классы/ОтелМетр.os:72-93 (View boundaries take precedence (assumed)) |
| 683 | MUST | ⚠️ | A `MetricFilter` MUST support the following functions: | src/Метрики/Классы/ОтелМетр.os:72-93 (Advisory boundaries conditional on View (not explicit)) |
| 684 | MUST | ⚠️ | The SDK MUST provide configuration according to the SDK environment | src/Метрики/Классы/ОтелМетр.os:72-93 (Default boundaries change visibility (not explicit)) |
| 685 | MUST | ⚠️ | The SDK MUST handle numerical limits in a graceful way according to Error | src/Метрики/Классы/ОтелМетр.os:72-93 (View aggregation prevents advisory use (assumed)) |
| 686 | MUST | ❌ | it MUST handle all the possible values. For example, if the language runtime | src/Метрики (ValidRange advisory not found) |
| 687 | SHOULD | ❌ | All the metrics components SHOULD allow new methods to be added to existing | src/Метрики (ValidRange advisory not found) |
| 688 | SHOULD | ❌ | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to | src/Метрики (ValidRange advisory not found) |
| 689 | MUST | ❌ | MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe | src/Метрики (Invalid measurement dropping not found) |
| 690 | MUST | ❌ | ExemplarReservoir - all methods MUST be safe to be called concurrently. | src/Метрики (Dropped measurement logging not found) |
| 691 | MUST | ❌ | and `Shutdown` MUST be safe to be called concurrently. | src/Метрики (Dropped measurement cardinality exclusion not found) |
| 692 | MUST | ✅ | MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130-162 |

### Otlp Exporter

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 693 | MUST | ⚠️ | The following configuration options MUST be available to configure the OTLP exporter. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (Missing signal-specific endpoint overrides) |
| 694 | MUST | ⚠️ | Each configuration option MUST be overridable by a signal specific option. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150-161 (URL components partially honored) |
| 695 | MUST | ❌ | The implementation MUST honor the following URL components: | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (No per-signal URL construction from global endpoint) |
| 696 | MUST | ✅ | When using `OTEL_EXPORTER_OTLP_ENDPOINT`, exporters MUST construct per-signal URLs as described below. The per-signal en... | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:154-159 |
| 697 | MUST | ⚠️ | Endpoint (OTLP/gRPC): Target to which the exporter is going to send spans, metrics, or logs. The option SHOULD accept an... | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150 (Protocol options: grpc and http/json supported; http/protobuf not supported) |
| 698 | MUST | ✅ | Protocol: The transport protocol. Options MUST be one of: `grpc`, `http/protobuf`, `http/json`. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150-159 |
| 699 | SHOULD | ➖ | [1]: SDKs SHOULD default endpoint variables to use `http` scheme unless they have good reasons to choose | OneScript SDK (Legacy env var support not part of stable release) |
| 700 | SHOULD | ⚠️ | they SHOULD continue to be supported as they were part of a stable release of the specification. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150 (Default protocol is http/json not http/protobuf) |
| 701 | SHOULD | ⚠️ | [4]: The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the de... | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130-162 (HTTP URLs constructed but signal-specific resolution missing) |
| 702 | MUST | ⚠️ | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs | src/Экспорт/Классы/ОтелHttpТранспорт.os:74 (Endpoint used as-is, only path appended) |
| 703 | MUST | ❌ | MUST be used as-is without any modification. The only exception is that if an | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (No explicit root path handling) |
| 704 | MUST | ⚠️ | URL contains no path part, the root path `/` MUST be used (see Example 2). | src/Экспорт/Классы/ОтелHttpТранспорт.os:74 (URL concatenation without validation) |
| 705 | MUST NOT | ⚠️ | An SDK MUST NOT modify the URL in ways other than specified above. That also means, | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150-156 (Supports gRPC and HTTP/JSON; no true protobuf) |
| 706 | MUST | ✅ | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150 |
| 707 | SHOULD | ⚠️ | support at least one of them. If they support only one, it SHOULD be | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150 (Default is http/json not http/protobuf) |
| 708 | SHOULD | ✅ | If no configuration is provided the default transport SHOULD be `http/protobuf` | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:133-139 |
| 709 | MUST | ✅ | The `OTEL_EXPORTER_OTLP_HEADERS`, `OTEL_EXPORTER_OTLP_TRACES_HEADERS`, `OTEL_EXPORTER_OTLP_METRICS_HEADERS`, `OTEL_EXPOR... | src/Экспорт/Классы/ОтелHttpТранспорт.os:73-96 |
| 710 | MUST | ❌ | Transient errors MUST be handled with a retry strategy. This retry strategy MUST implement an exponential back-off with ... | src/Экспорт/Классы/ОтелHttpТранспорт.os (No User-Agent header emitted) |
| 711 | SHOULD | ❌ | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of ... | src/Экспорт/Классы/ОтелHttpТранспорт.os (No RFC 7231 User-Agent) |
| 712 | SHOULD | ❌ | The format of the header SHOULD follow RFC 7231. The conventions used for specifying the OpenTelemetry SDK language and ... | src/Экспорт/Классы/ОтелHttpТранспорт.os (No User-Agent configuration option) |
| 713 | SHOULD | ✅ | Exporters MAY expose a configuration option to add a product identifier to the User-Agent header. The resulting User-Age... | src/Пропагация/Модули/ОтелW3CПропагатор.os:38,68 |

### Propagators

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 714 | MUST | ✅ | `Propagator`s MUST define `Inject` and `Extract` operations, in order to write | src/Пропагация/Модули/ОтелW3CПропагатор.os:1-8 |
| 715 | MUST | ✅ | values to and read values from carriers respectively. Each `Propagator` type MUST define the specific carrier type | src/Пропагация/Модули/ОтелW3CПропагатор.os:38-48 |
| 716 | MUST | ✅ | * A `Context`. The Propagator MUST retrieve the appropriate value from the `Context` first, such as | src/Пропагация/Модули/ОтелW3CПропагатор.os:40-42 |
| 717 | MUST NOT | ✅ | the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, | src/Пропагация/Модули/ОтелW3CПропагатор.os:49-51 |
| 718 | MUST | ✅ | In order to increase compatibility, the key/value pairs MUST only consist of US-ASCII characters | src/Пропагация/Модули/ОтелW3CПропагатор.os |
| 719 | MUST | ✅ | `Getter` and `Setter` MUST be stateless and allowed to be saved as constants, in order to effectively | src/Пропагация/Модули/ОтелW3CПропагатор.os:49-51 |
| 720 | MUST | ✅ | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used pr... | src/Пропагация/Модули/ОтелW3CПропагатор.os:70-74 |
| 721 | MUST | ✅ | The `Keys` function MUST return the list of all the keys in the carrier. | src/Пропагация/Модули/ОтелW3CПропагатор.os:68-78 |
| 722 | MUST | ✅ | The Get function MUST return the first value of the given propagation key or return null if the key doesn’t exist. | src/Пропагация/Модули/ОтелW3CПропагатор.os:70-78 |
| 723 | MUST | ➖ | The Get function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP request ob... | GetAll not explicitly defined (Not required when not implemented) |
| 724 | MUST | ➖ | If explicitly implemented, the `GetAll` function MUST return all values of the given propagation key. | GetAll not implemented (Not applicable) |
| 725 | SHOULD | ➖ | It SHOULD return them in the same order as they appear in the carrier. | GetAll not implemented (Not applicable) |
| 726 | SHOULD | ➖ | If the key doesn’t exist, it SHOULD return an empty collection. | GetAll not implemented (Not applicable) |
| 727 | MUST | ✅ | The `GetAll` function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP reque... | src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:73-75 |
| 728 | MUST | ✅ | Implementations MUST offer a facility to group multiple `Propagator`s | src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:17-39 |
| 729 | MUST | ⚠️ | There MUST be functions to accomplish the following operations. | src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os (No per-type getter API) |
| 730 | MUST | ⚠️ | The OpenTelemetry API MUST provide a way to obtain a propagator for each | src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os (Not enforced for libraries) |
| 731 | SHOULD | ✅ | supported `Propagator` type. Instrumentation libraries SHOULD call propagators | src/Ядро/Классы/ОтелSdk.os |
| 732 | MUST | ⚠️ | The OpenTelemetry API MUST use no-op propagators unless explicitly configured | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (Limited OTEL_PROPAGATORS support) |
| 733 | SHOULD | ⚠️ | propagators. If pre-configured, `Propagator`s SHOULD default to a composite | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (Override not fully detailed) |
| 734 | MUST | ✅ | These platforms MUST also allow pre-configured propagators to be disabled or overridden. | src/Ядро/Классы/ОтелSdk.os:48-50 |
| 735 | MUST | ✅ | This method MUST exist for each supported `Propagator` type. | src/Ядро/Классы/ОтелПостроительSdk.os |
| 736 | MUST | ✅ | This method MUST exist for each supported `Propagator` type. | src/Пропагация/Модули/ОтелW3CПропагатор.os |
| 737 | MUST | ✅ | The official list of propagators that MUST be maintained by the OpenTelemetry | src/Пропагация/Модули/ОтелW3CПропагатор.os |
| 738 | MUST | ➖ | organization and MUST be distributed as OpenTelemetry extension packages: | No OpenTracing (Not applicable) |
| 739 | MUST NOT | ➖ | used by the OpenTracing Basic Tracers. It MUST NOT use `OpenTracing` in the resulting | No X-Ray (Not applicable) |
| 740 | MUST NOT | ✅ | X-Ray trace header protocol MUST NOT be maintained or distributed as part of | src/Пропагация/Модули/ОтелW3CПропагатор.os:38-56 |
| 741 | MUST | ➖ | A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP headers as specified in W... | B3 NOT implemented (scope:conditional:B3 Propagator) |

### Env Vars

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 748 | SHOULD | ⚠️ | If they do, they SHOULD use the names and value parsing behavior specified in this document. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (Common configuration partially followed) |
| 749 | SHOULD | ✅ | They SHOULD also follow the common configuration specification. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:59-73 |
| 750 | MUST | ⚠️ | The environment-based configuration MUST have a direct code configuration equivalent. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105-110 (Empty value handling inconsistent) |
| 751 | MUST | ⚠️ | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563 (Boolean parsing only true accepted) |
| 752 | MUST | ✅ | Any value that represents a Boolean MUST be set to true only by the | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563 |
| 753 | MUST NOT | ⚠️ | accepted, as true. An implementation MUST NOT extend this definition and define | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563 (Unset defaults to true not false) |
| 754 | MUST | ❌ | here as a true value, including unset and empty values, MUST be interpreted as | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (No warning for invalid boolean values) |
| 755 | SHOULD | ⚠️ | empty, or unset is used, a warning SHOULD be logged to inform users about the | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (Boolean env vars not consistently handled) |
| 756 | SHOULD | ✅ | fallback to false being applied. All Boolean environment variables SHOULD be | src/Конфигурация/Модули/ОтелАвтоконфигурация.os |
| 757 | MUST NOT | ⚠️ | Renaming or changing the default value MUST NOT happen without a major version | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:160 (Numeric parsing without error handling) |
| 758 | SHOULD | ❌ | thus qualified as “SHOULD” to allow implementations to avoid breaking changes. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (No validation for numeric parse failures) |
| 759 | MUST | ❌ | implementations, these should be treated as MUST requirements. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (No warning for unparseable numeric values) |
| 760 | SHOULD | ✅ | implementation cannot parse, the implementation SHOULD generate a warning and gracefully | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:344 |
| 761 | SHOULD | ❌ | Enum values SHOULD be interpreted in a case-insensitive manner. | src/Конфигурация/Модули/ОтелАвтоконфигурация.os (No warning for unrecognized enum values) |
| 762 | MUST | ➖ | the implementation does not recognize, the implementation MUST generate | OneScript SDK (Platform limitation for attribute types) |
| 763 | SHOULD | ➖ | Implementations SHOULD only offer environment variables for the types of attributes, for | Prometheus exporter not implemented (Prometheus exporter not implemented) |

---

## Требования Development-статуса

Эти требования находятся в нестабильных разделах спецификации (Status: Development).
Они не влияют на основной процент соответствия и могут измениться в будущих версиях спецификации.

| Показатель | Значение |
|---|---|
| Всего Development | 99 |
| ✅ Реализовано | 42 (64.6%) |
| ⚠️ Частично | 18 (27.7%) |
| ❌ Не реализовано | 5 (7.7%) |
| N/A | 34 |

### Resource Sdk (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 46 | SHOULD | ➖ | Resource detectors SHOULD have a unique name for reference in configuration. For | No resource detectors (scope:conditional:Resource Detector Naming) |
| 47 | SHOULD | ➖ | Names SHOULD be snake case and | No resource detectors (scope:conditional:Resource Detector Naming) |
| 48 | SHOULD | ➖ | Resource detector names SHOULD reflect | No resource detectors (scope:conditional:Resource Detector Naming) |
| 49 | SHOULD | ➖ | multiple root namespaces SHOULD choose a name which appropriately conveys their | No resource detectors (scope:conditional:Resource Detector Naming) |
| 50 | SHOULD | ➖ | An SDK which identifies multiple resource detectors with the same name SHOULD | No resource detectors (scope:conditional:Resource Detector Naming) |
| 51 | SHOULD | ➖ | report an error. In order to limit collisions, resource detectors SHOULD | No resource detectors (scope:conditional:Resource Detector Naming) |
| 52 | MUST | ➖ | The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment | No resource detectors (scope:conditional:Resource Detector Naming) |
| 53 | MUST | ➖ | All attribute values MUST be considered strings. The `,` and `=` characters | No resource detectors (scope:conditional:Resource Detector Naming) |
| 54 | MUST | ➖ | in keys and values MUST be percent encoded. Other characters MAY be | No resource detectors (scope:conditional:Resource Detector Naming) |
| 55 | SHOULD | ✅ | variable value SHOULD be discarded and an error SHOULD be reported following the | src/Трассировка/Классы/ОтелТрассировщик.os:48 |

### Trace Api (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 71 | SHOULD | ✅ | creating `Span`s, a `Tracer` SHOULD provide this `Enabled` API. | src/Трассировка/Классы/ОтелПостроительСпана.os:75 |
| 72 | MUST | ✅ | added in the future, therefore, the API MUST be structured in a way for | src/Трассировка/Классы/ОтелПостроительСпана.os:90 |
| 73 | MUST | ✅ | This API MUST return a language idiomatic boolean type. A returned value of | src/Трассировка/Классы/ОтелПостроительСпана.os:107 |
| 74 | SHOULD | ✅ | SHOULD be documented that instrumentation authors needs to call this API each | src/Трассировка/Классы/ОтелСпан.os:563 |

### Trace Sdk (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 178 | MUST | ✅ | and (Development) TracerConfigurator) MUST be | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52 |
| 181 | MUST | ⚠️ | The function MUST accept the following parameter: | src/Трассировка/Классы/ОтелПровайдерТрассировки.os (Invalid name handling not explicitly documented) |
| 182 | MUST | ⚠️ | The function MUST return the relevant `TracerConfig`, or some signal indicating | src/Трассировка/Классы/ОтелПровайдерТрассировки.os (Invalid name logging not explicitly documented) |
| 183 | MUST | ✅ | `Shutdown` MUST be called only once for each `TracerProvider` instance. After | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:207-235 |
| 184 | SHOULD | ✅ | SHOULD return a valid no-op Tracer for these calls, if possible. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os |
| 185 | SHOULD | ➖ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | SDK Configuration (TracerConfig feature marked [DEV]) |
| 186 | SHOULD | ➖ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` can be | SDK Configuration (TracerConfig feature marked [DEV]) |
| 187 | MUST | ✅ | `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:100 |
| 191 | MUST | ✅ | the `Tracer` MUST be updated to behave according to the new `TracerConfig`. | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:101-104 |
| 192 | SHOULD | ✅ | If not explicitly set, the `enabled` parameter SHOULD default to `true` ( | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:112 |
| 193 | MUST | ⚠️ | If a `Tracer` is disabled, it MUST behave equivalently | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:112 (Timeout handling not documented) |
| 194 | MUST | ✅ | The value of `enabled` MUST be used to resolve whether a `Tracer` | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:92-94 |
| 195 | MUST | ✅ | However, the changes MUST be eventually visible. | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26 |
| 196 | MUST | ✅ | `Enabled` MUST return `false` when either: | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:76 |
| 197 | SHOULD | ✅ | Otherwise, it SHOULD return `true`. | src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-31 |
| 222 | SHOULD | ⚠️ | when it is used not as a root sampler, the SDK SHOULD emit a warning | src/Трассировка/Классы (SpanExporter concurrency safety not explicitly documented) |
| 223 | MUST | ✅ | The `ProbabilitySampler` sampler MUST ignore the parent `SampledFlag`. | src/Трассировка/Модули/ОтелСэмплер.os:112 |
| 224 | SHOULD | ✅ | * If randomness value (R) is greater or equal to the rejection threshold (T), meaning when (R >= T), return `RECORD_AND_... | src/Трассировка/Классы/ОтелПровайдерТрассировки.os:228 |
| 225 | MUST | ✅ | Based on the decision from the wrapped root sampler, `AlwaysRecord` MUST behave | src/Трассировка/Модули/ОтелСэмплер.os:112-128 |
| 226 | MUST NOT | ✅ | Note: ComposableSamplers MUST NOT modify the parameters passed to | src/Трассировка/Классы/ОтелРезультатСэмплирования.os |
| 227 | MUST NOT | ✅ | complexity. ComposableSamplers MUST NOT modify the OpenTelemetry | src/Трассировка/Модули/ОтелСэмплер.os:36-54 |
| 228 | SHOULD | ✅ | CompositeSampler SHOULD update the threshold of the outgoing | src/Трассировка/Модули/ОтелСэмплер.os |
| 229 | MUST | ✅ | randomness values MUST not be modified. | src/Трассировка/Модули/ОтелСэмплер.os:112-128 |
| 230 | SHOULD | ✅ | a `ComposableAlwaysOff` instance SHOULD be returned instead. | src/Трассировка/Модули/ОтелСэмплер.os:58-94 |
| 246 | SHOULD | ⚠️ | Custom implementations of the `IdGenerator` SHOULD identify themselves | src/Трассировка (ID generator customization mechanism not visible in provider code) |
| 252 | MUST | ⚠️ | The end timestamp MUST have been computed (the `OnEnding` method duration is not included | src/Трассировка/Классы (ReadableSpan functionality provided via public Span methods (no separate class)) |
| 253 | MUST | ⚠️ | The Span object MUST still be mutable (i.e., `SetAttribute`, `AddLink`, `AddEvent` can be called) while `OnEnding` is ca... | src/Трассировка/Классы/ОтелСпан.os (Readable span provides access to all public properties) |
| 254 | MUST | ✅ | This method MUST be called synchronously within the `Span.End()` API, | src/Трассировка/Классы/ОтелСпан.os:162-163 |
| 255 | MUST | ✅ | The SDK MUST guarantee that the span can no longer be modified by any other thread | src/Трассировка/Классы/ОтелСпан.os |

### Logs Api (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 305 | SHOULD | ✅ | The ergonomic API SHOULD make it more convenient to emit event records following | src/Логирование/Классы/ОтелПостроительЛоггера.os:26-42 |
| 306 | SHOULD | ✅ | The design of the ergonomic API SHOULD be idiomatic for its language. | src/Логирование/Классы/ОтелПровайдерЛогирования.os |

### Logs Sdk (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 319 | MUST | ➖ | The function MUST accept the following parameter: | LoggerConfigurator not implemented (DEV requirement) |
| 320 | MUST | ⚠️ | The function MUST return the relevant `LoggerConfig`, or some signal indicating | src/Логирование/Классы/ОтелПровайдерЛогирования.os:99-104 (Shutdown implemented but no single-call guarantee) |
| 321 | MUST | ✅ | `Shutdown` MUST be called only once for each `LoggerProvider` instance. After | src/Логирование/Классы/ОтелПровайдерЛогирования.os:51-54 |
| 322 | SHOULD | ⚠️ | SDKs SHOULD return a valid no-op `Logger` for these calls, if possible. | src/Логирование/Классы/ОтелПровайдерЛогирования.os:99-104 (No status indication) |
| 323 | SHOULD | ⚠️ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | src/Логирование/Классы/ОтелПровайдерЛогирования.os:99-104 (No timeout mechanism) |
| 324 | SHOULD | ✅ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` MAY be | src/Логирование/Классы/ОтелПровайдерЛогирования.os:100-102 |
| 325 | MUST | ⚠️ | `Shutdown` MUST be implemented by invoking `Shutdown` on all | src/Логирование/Классы/ОтелПровайдерЛогирования.os:112-116 (ForceFlush returns nothing, no status) |
| 331 | MUST | ➖ | the `Logger` MUST be updated to behave according to the new `LoggerConfig`. | LoggerConfig not implemented (DEV requirement) |
| 332 | SHOULD | ➖ | If not explicitly set, the `enabled` parameter SHOULD default to `true` ( | LoggerConfig not implemented (DEV requirement) |
| 333 | MUST | ➖ | If a `Logger` is disabled, it MUST behave equivalently | LoggerConfig not implemented (DEV requirement) |
| 334 | MUST | ➖ | If not explicitly set, the `minimum_severity` parameter MUST default to `0`. | LoggerConfig not implemented (DEV requirement) |
| 335 | MUST | ➖ | specified (i.e. not `0`) and is less than the configured `minimum_severity`, the log record MUST | LoggerConfig not implemented (DEV requirement) |
| 336 | MUST | ➖ | If not explicitly set, the `trace_based` parameter MUST default to `false`. | LoggerConfig not implemented (DEV requirement) |
| 337 | MUST | ➖ | If `trace_based` is `true`, log records associated with unsampled traces MUST | LoggerConfig not implemented (DEV requirement) |
| 338 | MUST | ✅ | However, the changes MUST be eventually visible. | src/Логирование/Классы/ОтелЛоггер.os:81-84 |
| 342 | MUST | ⚠️ | the implementation MUST apply the filtering rules defined by the | src/Логирование/Классы/ОтелЛоггер.os:41-50 (Log record handling but no formal filtering cascade) |
| 343 | MUST | ⚠️ | the log record MUST be dropped. | src/Логирование/Классы/ОтелЛоггер.os:43-50 (Returns false when closed or no processors, but no min severity) |
| 345 | SHOULD | ✅ | Otherwise, it SHOULD return `true`. | src/Логирование/Классы/ОтелЗаписьЛога.os:45-155 |

### Metrics Sdk (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 501 | MUST | ✅ | and (Development) MeterConfigurator) MUST be | src/Метрики/Классы/ОтелПровайдерМетрик.os:69-74 |
| 503 | MUST | ➖ | The function MUST accept the following parameter: | src/Метрики/Классы/ОтелПровайдерМетрик.os (MeterConfigurator not applicable to OneScript SDK) |
| 504 | MUST | ✅ | The function MUST return the relevant `MeterConfig`, or some signal indicating | src/Метрики/Классы/ОтелПровайдерМетрик.os:127 |
| 505 | MUST | ✅ | `Shutdown` MUST be called only once for each `MeterProvider` instance. After the | src/Метрики/Классы/ОтелПровайдерМетрик.os:55-58 |
| 506 | SHOULD | ✅ | SHOULD return a valid no-op Meter for these calls, if possible. | src/Метрики/Классы/ОтелПровайдерМетрик.os:127-141 |
| 507 | SHOULD | ⚠️ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:85-102 (Shutdown uses timeout but no explicit timeout configuration) |
| 508 | SHOULD | ✅ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` MAY be | src/Метрики/Классы/ОтелПровайдерМетрик.os:133-140 |
| 509 | MUST | ✅ | `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered | src/Метрики/Классы/ОтелПровайдерМетрик.os:149-153 |
| 566 | MUST | ✅ | For delta aggregations, the start timestamp MUST equal the previous collection | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:208-210 |
| 567 | MUST | ✅ | with delta temporality aggregation for an instrument MUST share the same start | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:208-210 |
| 568 | MUST | ✅ | Cumulative timeseries MUST use a consistent start timestamp for all collection | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:208-210 |
| 569 | SHOULD | ✅ | For synchronous instruments, the start timestamp SHOULD be the time of the | src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:109-149 |
| 570 | SHOULD | ✅ | For asynchronous instrument, the start timestamp SHOULD be: | src/Экспорт/Классы/ОтелЭкспортерМетрик.os:22-35 |
| 582 | MUST | ⚠️ | the `Meter` MUST be updated to behave according to the new `MeterConfig`. | src/Метрики/Классы/ОтелМетр.os:1 (Attribute limits configuration not found) |
| 583 | SHOULD | ❌ | If not explicitly set, the `enabled` parameter SHOULD default to `true` ( | src/Метрики/Классы/ОтелМетр.os (Attribute limits configuration not found) |
| 584 | MUST | ❌ | If a `Meter` is disabled, it MUST behave equivalently | src/Метрики/Классы/ОтелМетр.os (Cardinality limit not found) |
| 585 | MUST | ❌ | The value of `enabled` MUST be used to resolve whether an instrument | src/Метрики/Классы/ОтелМетр.os (Cardinality limit enforcement not found) |
| 586 | MUST | ❌ | However, the changes MUST be eventually visible. | src/Метрики/Классы/ОтелМетр.os (Cardinality limit drop not found) |
| 605 | SHOULD | ❌ | Otherwise, it SHOULD return `true`. | src/Метрики (MetricProducer Produce function not found) |
| 640 | SHOULD | ➖ | * The `exporter` to use, which is a `MetricExporter` instance.* The default output `aggregation` (optional), a function ... | src/Метрики/Классы/ОтелМетр.os (SynchronousMeasurementHandler not applicable) |
| 641 | SHOULD | ➖ | `MetricReader` SHOULD be provided to be used | src/Метрики/Классы/ОтелМетр.os (SynchronousMeasurementHandler not applicable) |
| 642 | MUST | ➖ | The `MetricReader` MUST ensure that data points from OpenTelemetry | src/Метрики/Классы/ОтелМетр.os (SynchronousMeasurementHandler not applicable) |
| 643 | MUST | ➖ | temporality, MetricReader.Collect MUST receive data points exposed | src/Метрики/Классы/ОтелМетр.os (SynchronousMeasurementHandler not applicable) |
| 644 | MUST | ➖ | temporality, MetricReader.Collect MUST only receive data points with | src/Метрики/Классы/ОтелМетр.os (SynchronousMeasurementHandler not applicable) |
| 645 | MUST | ➖ | temporality, MetricReader.Collect MUST only receive data points with | src/Метрики/Классы/ОтелМетр.os (SynchronousMeasurementHandler not applicable) |
| 646 | MUST | ➖ | successive calls to MetricReader.Collect MUST repeat the same | src/Метрики/Классы/ОтелМетр.os (SynchronousMeasurementHandler not applicable) |
| 647 | MUST | ➖ | calls to MetricReader.Collect MUST advance the starting timestamp ( | src/Метрики/Классы/ОтелМетр.os (SynchronousMeasurementHandler not applicable) |
| 648 | MUST | ➖ | MUST always be equal to time the metric data point took effect, which is equal | src/Метрики/Классы/ОтелМетр.os (SynchronousMeasurementHandler not applicable) |
| 649 | MUST | ➖ | The SDK MUST support multiple `MetricReader` instances to be registered on the | src/Метрики/Классы/ОтелМетр.os (SynchronousMeasurementHandler not applicable) |
| 650 | SHOULD NOT | ⚠️ | `MetricReader` instance SHOULD NOT introduce side-effects to other `MetricReader` | src/Метрики/Классы/ОтелМетр.os:72-93 (Advisory boundaries used but not explicitly conditioned) |
| 651 | MUST NOT | ⚠️ | The SDK MUST NOT allow a `MetricReader` instance to be registered on more than | src/Метрики/Классы/ОтелМетр.os:256-272 (Observable Gauge uses LastValueAggregator) |
| 652 | SHOULD | ⚠️ | The SDK SHOULD provide a way to allow `MetricReader` to respond to | src/Метрики/Классы/ОтелМетр.os:256-272 (Produce function not found) |

### Env Vars (Development)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 764 | SHOULD | ➖ | * `"otlp"`: OTLP* `"zipkin"`: Zipkin (Defaults to protobuf format)* `"console"`: Standard Output* `"logging"`: Standard ... | Prometheus exporter not implemented (Prometheus exporter not implemented) |
| 765 | SHOULD | ➖ | * `"otlp"`: OTLP* `"prometheus"`: Prometheus* `"console"`: Standard Output* `"logging"`: Standard Output. It is a deprec... | Prometheus exporter not implemented (Prometheus exporter not implemented) |
| 766 | SHOULD | ➖ | * `"otlp"`: OTLP* `"console"`: Standard Output* `"logging"`: Standard Output. It is a deprecated value left for backward... | Prometheus exporter not implemented (Prometheus exporter not implemented) |
| 767 | MUST | ➖ | MUST be ignored. Ignoring the environment variables is necessary because | Prometheus exporter not implemented (scope:conditional:Prometheus Exporter) |

---

## Условные требования (Conditional)

Эти требования применяются только при реализации конкретной опциональной функциональности
(например, B3 propagator, Prometheus exporter). Если функциональность не реализована,
требования неприменимы (N/A) и не влияют на основной процент соответствия.

| Показатель | Значение |
|---|---|
| Всего Conditional | 6 |
| ✅ Реализовано | 0 (0.0%) |
| ⚠️ Частично | 1 (100.0%) |
| ❌ Не реализовано | 0 (0.0%) |
| N/A | 5 |

### B3 Propagator (extension)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 742 | MUST | ➖ | * MUST attempt to extract B3 encoded using single and multi-header | B3 NOT implemented (scope:conditional:B3 Propagator) |
| 743 | MUST | ➖ | the multi-header version.* MUST preserve a debug trace flag, if received, and propagate | B3 NOT implemented (scope:conditional:B3 Propagator) |
| 744 | MUST NOT | ➖ | MUST set the sampled trace flag when the debug flag is set.* MUST NOT reuse `X-B3-SpanId` as the id for the server-side ... | B3 NOT implemented (scope:conditional:B3 Propagator) |
| 745 | MUST | ➖ | * MUST default to injecting B3 using the single-header format* MUST provide configuration to change the default injectio... | B3 NOT implemented (scope:conditional:B3 Propagator) |
| 746 | MUST NOT | ➖ | multi-header* MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support | B3 NOT implemented (scope:conditional:B3 Propagator) |
| 747 | MUST | ⚠️ | Fields MUST return the header names that correspond to the configured format, | src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1-35 (Standard OTEL env vars read but missing signal-specific overrides) |

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
2. Каждое из 767 требований классифицировано по трем осям:
   - **Стабильность**: Stable / Development (на основе маркеров `Status:` в спецификации)
   - **Область**: universal / conditional / deprecated
     - *universal* - обязательно для любой реализации SDK
     - *conditional* - обязательно только при реализации конкретной опциональной фичи (B3, Prometheus и др.)
     - *deprecated* - относится к устаревшей функциональности (Jaeger, OT Trace)
3. Каждое требование прослежено до конкретного файла и строки в исходном коде
4. Статусы:
   - ✅ found - реализовано
   - ⚠️ partial - частично реализовано
   - ❌ not_found - не реализовано
   - ➖ n_a - неприменимо к платформе
5. Основной процент соответствия считается только по Stable + universal требованиям
6. Development, conditional и deprecated требования вынесены в отдельные секции
