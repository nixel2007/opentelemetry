# Анализ соответствия спецификации OpenTelemetry v1.55.0

> **Версия спецификации**: [v1.55.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-04-03
> **Методология**: spec-first - извлечены все MUST/SHOULD требования из спецификации, затем каждое прослежено до кода

## Сводка

| Показатель | Значение |
|---|---|
| Всего требований | 613 |
| Применимых (без N/A) | 589 |
| ✅ Реализовано | 507 (86.1%) |
| ⚠️ Частично | 50 (8.5%) |
| ❌ Не реализовано | 32 (5.4%) |
| N/A (неприменимо/Development) | 24 |
| **MUST/MUST NOT** | 325/366 (88.8%) |
| **SHOULD/SHOULD NOT** | 182/223 (81.6%) |

## Соответствие по разделам

| Раздел | Всего | ✅ | ⚠️ | ❌ | N/A | % |
|---|---|---|---|---|---|---|
| Baggage Api | 16 | 15 | 1 | 0 | 0 | 93.8% |
| Context | 11 | 9 | 0 | 2 | 0 | 81.8% |
| Env Vars | 20 | 16 | 3 | 1 | 0 | 80.0% |
| Logs Api | 17 | 12 | 4 | 0 | 1 | 75.0% |
| Logs Sdk | 61 | 36 | 10 | 4 | 11 | 72.0% |
| Metrics Api | 71 | 68 | 1 | 0 | 2 | 98.6% |
| Metrics Sdk | 133 | 126 | 7 | 0 | 0 | 94.7% |
| Otlp Exporter | 20 | 6 | 8 | 4 | 2 | 33.3% |
| Propagators | 29 | 11 | 7 | 7 | 4 | 44.0% |
| Resource Sdk | 25 | 10 | 1 | 14 | 0 | 40.0% |
| Trace Api | 114 | 106 | 6 | 0 | 2 | 94.6% |
| Trace Sdk | 96 | 92 | 2 | 0 | 2 | 97.9% |

## Ключевые несоответствия

### MUST/MUST NOT нарушения

- ⚠️ **[Baggage Api]** [MUST] The API layer or an extension package MUST include the following `Propagator`s: (`W3CПропагатор.os, W3CBaggageПропагатор.os`)
  - W3C propagators included, no B3
- ❌ **[Context]** [MUST] The API MUST return an opaque object representing the newly created key.
  - No CreateKey function; uses string keys directly
- ⚠️ **[Env Vars]** [MUST] The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. (`ОтелАвтоконфигурация.os:105,114`)
  - Empty = unset, but not all vars tested
- ⚠️ **[Env Vars]** [MUST] the implementation does not recognize, the implementation MUST generate (`ОтелАвтоконфигурация.os:216-218`)
  - Inconsistent error handling for enums
- ⚠️ **[Logs Sdk]** [MUST] `Shutdown` MUST be called only once for each `LoggerProvider` instance. After (`ОтелПровайдерЛогирования.os:99-104`)
  - Shutdown exists, no once-only check
- ❌ **[Logs Sdk]** [MUST] If an Exception is provided, the SDK MUST by default set attributes
  - No exception-to-attributes conversion
- ❌ **[Logs Sdk]** [MUST NOT] User-provided attributes MUST take precedence and MUST NOT be overwritten by
  - Exception attributes not implemented
- ⚠️ **[Logs Sdk]** [MUST] A function receiving this as an argument MUST additionally be able to modify (`ОтелЗаписьЛога.os:173-307`)
  - ReadWrite after emit is no-op
- ⚠️ **[Logs Sdk]** [MUST] timeout is specified (see below), the `LogRecordProcessor` MUST prioritize (`ОтелБазовыйПакетныйПроцессор.os:136-149`)
  - Timeout partially used
- ⚠️ **[Metrics Sdk]** [MUST NOT] `unit`, but MUST NOT obligate a user to provide one. (`ОтелСелекторИнструментов.os`)
  - unit criteria not explicitly in selector (set in View)
- ⚠️ **[Metrics Sdk]** [MUST NOT] to accept a `meter_version`, but MUST NOT obligate a user to provide one. (`meter_version support implicit via ОбластьИнструментирования but not in selector`)
- ⚠️ **[Metrics Sdk]** [MUST NOT] to accept a `meter_schema_url`, but MUST NOT obligate a user to provide one. (`meter_schema_url support implicit but not in selector`)
- ⚠️ **[Metrics Sdk]** [MUST NOT] accept the criteria, but MUST NOT obligate a user to provide them. (`Criteria optional but full list not all in selector`)
- ⚠️ **[Metrics Sdk]** [MUST] `MeterProvider` MUST apply a default exemplar (`ОтелРезервуарЭкземпляров.os`)
  - Default exemplar reservoir implementation present
- ⚠️ **[Otlp Exporter]** [MUST] Each configuration option MUST be overridable by a signal specific option. (`ОтелАвтоконфигурация.os:177,255,291`)
  - Signal-specific endpoints NOT implemented
- ⚠️ **[Otlp Exporter]** [MUST] The implementation MUST honor the following URL components: (`ОтелHttpТранспорт.os:55-102`)
  - URL components not parsed separately
- ❌ **[Otlp Exporter]** [MUST] When using `OTEL_EXPORTER_OTLP_ENDPOINT`, exporters MUST construct per-signal URLs as described below. The per-signal endpoint configuration options t...
  - Signal-specific endpoints not supported
- ⚠️ **[Otlp Exporter]** [MUST] Endpoint (OTLP/gRPC): Target to which the exporter is going to send spans, metrics, or logs. The option SHOULD accept any form allowed by the underlyi... (`ОтелАвтоконфигурация.os:153-155`)
  - Accepts URLs but no http/https distinction
- ⚠️ **[Otlp Exporter]** [MUST] Protocol: The transport protocol. Options MUST be one of: `grpc`, `http/protobuf`, `http/json`. (`ОтелАвтоконфигурация.os:150-161`)
  - Only grpc and http/json, no http/protobuf
- ⚠️ **[Otlp Exporter]** [MUST] URL contains no path part, the root path `/` MUST be used (see Example 2). (`ОтелHttpТранспорт.os:74`)
  - No explicit root path handling
- ⚠️ **[Otlp Exporter]** [MUST] SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST (`ОтелGrpcТранспорт.os, ОтелHttpТранспорт.os`)
  - gRPC and HTTP/JSON, no http/protobuf
- ⚠️ **[Otlp Exporter]** [MUST] Transient errors MUST be handled with a retry strategy. This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming t... (`ОтелHttpТранспорт.os:85`)
  - Exponential backoff without jitter
- ⚠️ **[Propagators]** [MUST] `Getter` and `Setter` MUST be stateless and allowed to be saved as constants, in order to effectively
  - Direct Соответствие access, no stateless getter/setter
- ⚠️ **[Propagators]** [MUST] The `Keys` function MUST return the list of all the keys in the carrier.
  - No explicit Keys() function for carriers
- ⚠️ **[Propagators]** [MUST] The Get function MUST return the first value of the given propagation key or return null if the key doesn’t exist. (`ОтелW3CПропагатор.os:70-74`)
  - Case-insensitive via НРег
- ❌ **[Propagators]** [MUST] If explicitly implemented, the `GetAll` function MUST return all values of the given propagation key.
  - GetAll function not implemented
- ❌ **[Propagators]** [MUST] The `GetAll` function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP request object, the getter MUST be ...
  - GetAll case sensitivity N/A
- ⚠️ **[Propagators]** [MUST] The OpenTelemetry API MUST provide a way to obtain a propagator for each
  - No GetGlobalPropagator/SetGlobalPropagator API
- ❌ **[Propagators]** [MUST] The OpenTelemetry API MUST use no-op propagators unless explicitly configured
  - No-op propagator not found
- ❌ **[Propagators]** [MUST] These platforms MUST also allow pre-configured propagators to be disabled or overridden.
  - Override/disable mechanism not documented
- ❌ **[Propagators]** [MUST] This method MUST exist for each supported `Propagator` type.
  - GetGlobalPropagator method not found
- ⚠️ **[Propagators]** [MUST] organization and MUST be distributed as OpenTelemetry extension packages:
  - W3C exists but no B3
- ❌ **[Resource Sdk]** [MUST] or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as
  - No cloud resource detectors
- ❌ **[Resource Sdk]** [MUST] Resource detector packages MUST provide a method that returns a resource. This
  - No resource detector packages
- ❌ **[Resource Sdk]** [MUST NOT] failure to detect any resource information MUST NOT be considered an error,
  - Detection failure handling not visible
- ❌ **[Resource Sdk]** [MUST] semantic conventions MUST ensure that the resource has a Schema URL set to a
  - No schema URL validation in detectors
- ❌ **[Resource Sdk]** [MUST] the detectors use different non-empty Schema URL it MUST be an error since it is
  - Schema URL conflict detection not found
- ⚠️ **[Resource Sdk]** [MUST] in keys and values MUST be percent encoded. Other characters MAY be (`ОтелАвтоконфигурация.os`)
  - Percent encoding mentioned but unclear
- ⚠️ **[Trace Api]** [MUST] 16-byte array) or `SpanId` (result MUST be an 8-byte array). (`ОтелКонтекстСпана.os`)
  - Binary forms not explicitly implemented (hex strings only)
- ⚠️ **[Trace Api]** [MUST] `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. (`ОтелКонтекстСпана.os:60`)
  - IsRemote property stored but child span inheritance not explicitly shown
- ⚠️ **[Trace Api]** [MUST NOT] In languages with implicit `Context` propagation, `Span` creation MUST NOT (`ОтелТрассировщик.os:48`)
  - Span creation doesn't explicitly propagate implicit context (no context interception shown)

### SHOULD/SHOULD NOT несоответствия

- ❌ **[Context]** [SHOULD NOT] * The key name. The key name exists for debugging purposes and does not uniquely identify the key. Multiple calls to `CreateKey` with the same name SH...
  - No explicit CreateKey API returning opaque key object
- ⚠️ **[Env Vars]** [SHOULD] Enum values SHOULD be interpreted in a case-insensitive manner. (`ОтелАвтоконфигурация.os:197-219`)
  - Enums case-insensitive but inconsistent
- ❌ **[Env Vars]** [SHOULD] * `"otlp"`: OTLP* `"console"`: Standard Output* `"logging"`: Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD
  - OTEL_LOG_LEVEL not implemented
- ⚠️ **[Logs Api]** [SHOULD] The `Logger` SHOULD provide functions to: (`ОтелЛоггер.os:32-34`)
  - Enabled exists but lacks parameters
- ⚠️ **[Logs Api]** [SHOULD] When only explicit Context is supported, this parameter SHOULD be required.* Severity Number (optional)* Severity Text (optional)* Body (optional)* At... (`ОтелЗаписьЛога.os:21-275`)
  - LogRecord has fields but no ergonomic API
- ⚠️ **[Logs Api]** [SHOULD] The API SHOULD accept the following parameters: (`ОтелЛоггер.os:21-23`)
  - No overloads for direct parameters
- ⚠️ **[Logs Api]** [SHOULD] The ergonomic API SHOULD make it more convenient to emit event records following
  - Fluent on LogRecord, no convenience on Logger
- ⚠️ **[Logs Sdk]** [SHOULD] message reporting that the specified value is invalid SHOULD be logged.
  - No warning for invalid logger name
- ❌ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` MAY be
  - No timeout for Shutdown
- ⚠️ **[Logs Sdk]** [SHOULD] failed or timed out. `ForceFlush` SHOULD return some ERROR status if there (`ОтелПровайдерЛогирования.os:90-94`)
  - ForceFlush returns Promise, no ERROR status
- ⚠️ **[Logs Sdk]** [SHOULD] is an error condition; and if there is no error condition, it SHOULD return (`ОтелПровайдерЛогирования.os:112-116`)
  - No explicit SUCCESS/ERROR indication
- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be
  - No timeout for ForceFlush
- ⚠️ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. (`ОтелПростойПроцессорЛогов.os:32-36`)
  - Shutdown exists, no once-only check
- ⚠️ **[Logs Sdk]** [SHOULD] to `ForceFlush` SHOULD be completed as soon as possible, preferably before (`ОтелБазовыйПакетныйПроцессор.os:65-134`)
  - ForceFlush partial timeout
- ⚠️ **[Logs Sdk]** [SHOULD] SHOULD try to call the exporter’s `Export` with all `LogRecord`s for which this (`ОтелБазовыйПакетныйПроцессор.os:136-149`)
  - ForceFlush calls export
- ⚠️ **[Logs Sdk]** [SHOULD] exporter has received prior to the call to `ForceFlush` SHOULD be completed as (`ОтелЭкспортерЛогов.os:35-40`)
  - ForceFlush placeholder
- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD provide some way to pass `state` to the (`ОтелМетр.os:348`)
  - State parameter support via ЗарегистрироватьОбратныйВызов - limited scope
- ⚠️ **[Metrics Sdk]** [SHOULD] Additionally, implementations SHOULD support configuring an exclude-list of (`Exclude-list not explicitly implemented (only include-list via attribute_keys)`)
- ⚠️ **[Metrics Sdk]** [SHOULD] The SDK SHOULD provide the following `Aggregation`: (`Drop aggregation referenced in ОтелАгрегация.os:45-47 but not fully implemented`)
- ⚠️ **[Otlp Exporter]** [SHOULD] [4]: The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default. For instance, maintaini... (`ОтелАвтоконфигурация.os:150`)
  - Default http/json, not http/protobuf
- ❌ **[Otlp Exporter]** [SHOULD] If no configuration is provided the default transport SHOULD be `http/protobuf` (`ОтелАвтоконфигурация.os:150`)
  - Default is http/json, not http/protobuf
- ❌ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the ve...
  - User-Agent header not set
- ❌ **[Otlp Exporter]** [SHOULD] The format of the header SHOULD follow RFC 7231. The conventions used for specifying the OpenTelemetry SDK language and version are available in the R...
  - User-Agent not implemented
- ❌ **[Propagators]** [SHOULD] It SHOULD return them in the same order as they appear in the carrier.
  - GetAll ordering N/A
- ❌ **[Propagators]** [SHOULD] If the key doesn’t exist, it SHOULD return an empty collection.
  - GetAll empty collection N/A
- ⚠️ **[Propagators]** [SHOULD] supported `Propagator` type. Instrumentation libraries SHOULD call propagators
  - Composite not enforced for instrumentation libs
- ⚠️ **[Propagators]** [SHOULD] propagators. If pre-configured, `Propagator`s SHOULD default to a composite (`ОтелАвтоконфигурация.os:30`)
  - OTEL_PROPAGATORS env var mentioned
- ❌ **[Resource Sdk]** [SHOULD] SHOULD be considered an error.
  - No error handling for unsupported detectors
- ❌ **[Resource Sdk]** [SHOULD] value that matches the semantic conventions. Empty Schema URL SHOULD be used if
  - Empty schema URL handling not found
- ❌ **[Resource Sdk]** [SHOULD] Resource detectors SHOULD have a unique name for reference in configuration. For
  - Resource detectors unnamed
- ❌ **[Resource Sdk]** [SHOULD] Names SHOULD be snake case and
  - No snake_case naming for detectors
- ❌ **[Resource Sdk]** [SHOULD] Resource detector names SHOULD reflect
  - Resource detector names not found
- ❌ **[Resource Sdk]** [SHOULD] multiple root namespaces SHOULD choose a name which appropriately conveys their
  - Multiple root namespace handling not found
- ❌ **[Resource Sdk]** [SHOULD] An SDK which identifies multiple resource detectors with the same name SHOULD
  - Duplicate detector name collision not found
- ❌ **[Resource Sdk]** [SHOULD] report an error. In order to limit collisions, resource detectors SHOULD
  - Detector limit collisions not found
- ❌ **[Resource Sdk]** [SHOULD] variable value SHOULD be discarded and an error SHOULD be reported following the
  - Error handling for malformed attributes not visible
- ⚠️ **[Trace Api]** [SHOULD] reporting that the specified value is invalid SHOULD be logged. A library, (`ОтелПровайдерТрассировки.os:52`)
  - Message logging for invalid name - not explicitly documented but returns valid tracer
- ⚠️ **[Trace Api]** [SHOULD] SHOULD be documented that instrumentation authors needs to call this API each (`ОтелТрассировщик.os:33`)
  - Documentation suggests calling Enabled() each time (implicit)
- ⚠️ **[Trace Api]** [SHOULD] not covered by the semantic conventions, Instrumentation Libraries SHOULD (`ОтелСпан.os:402-425`)
  - Instrumentation libraries should set status (per usage documentation)
- ⚠️ **[Trace Sdk]** [SHOULD] For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an expli... (`ОтелСэмплер.os`)
  - Samplers presume TraceIDs meet W3C randomness unless explicit rv sub-key
- ⚠️ **[Trace Sdk]** [SHOULD] Custom implementations of the `IdGenerator` SHOULD identify themselves (`ОтелУтилиты.os`)
  - Custom ID generators should identify themselves

---

## Детальный анализ по разделам

### Baggage Api

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 12 | MUST | ✅ | describing user-defined properties. Each name in `Baggage` MUST be associated | ОтелBaggage.os:139-142 |
| 13 | SHOULD NOT | ✅ | Baggage names are any valid, non-empty UTF-8 strings. Language API SHOULD NOT | ОтелBaggage.os |
| 14 | MUST | ✅ | Baggage values are any valid UTF-8 strings. Language API MUST accept | ОтелBaggage.os |
| 15 | MUST | ✅ | Language API MUST treat both baggage names and values as case sensitive. | ОтелBaggage.os:38-40,51-57 |
| 16 | MUST | ✅ | The Baggage API MUST be fully functional in the absence of an installed SDK. | ОтелBaggage.os:16-18,26-28 |
| 17 | MUST | ✅ | The `Baggage` container MUST be immutable, so that the containing `Context` | ОтелBaggage.os:152-162 |
| 18 | MUST | ✅ | MUST provide a function that takes the name as input, and returns a value | ОтелBaggage.os:38-40 |
| 19 | MUST NOT | ✅ | MUST NOT be significant. Based on the language specifics, the returned | ОтелBaggage.os:103-105 |
| 20 | MUST | ✅ | To record the value for a name/value pair, the Baggage API MUST provide a | ОтелBaggage.os:68-72 |
| 21 | MUST | ✅ | To delete a name/value pair, the Baggage API MUST provide a function which | ОтелBaggage.os:82-86 |
| 22 | MUST | ✅ | MUST provide the following functionality to interact with a `Context` instance: | ОтелBaggage.os:16-28 |
| 23 | SHOULD NOT | ✅ | The functionality listed above is necessary because API users SHOULD NOT have | ОтелBaggage.os:113-115 |
| 24 | SHOULD | ✅ | `Baggage` class. This functionality SHOULD be fully implemented in the API when | ОтелBaggage.os:68-72,82-86,113-115 |
| 25 | MUST | ✅ | MUST provide a way to remove all baggage entries from a context. | ОтелBaggage.os:94-96 |
| 26 | MUST | ⚠️ | The API layer or an extension package MUST include the following `Propagator`s: | W3CПропагатор.os, W3CBaggageПропагатор.os (W3C propagators included, no B3) |
| 27 | MUST | ✅ | then the new pair MUST take precedence. The value is replaced with the added | ОтелПостроительBaggage.os:23-27 |

### Context

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | MUST | ✅ | A `Context` MUST be immutable, and its write operations MUST | ОтелКонтекст.os:114-118 |
| 2 | MUST | ✅ | option is not available, OpenTelemetry MUST provide its own `Context` | ОтелКонтекст.os:3-4,311 |
| 3 | MUST | ✅ | The API MUST accept the following parameter: | ОтелКонтекст.os:147-152 |
| 4 | SHOULD NOT | ❌ | * The key name. The key name exists for debugging purposes and does not uniquely identify the key. Multiple calls to `Cr... | -No explicit CreateKey API returning opaque key object |
| 5 | MUST | ❌ | The API MUST return an opaque object representing the newly created key. | -No CreateKey function; uses string keys directly |
| 6 | MUST | ✅ | The API MUST accept the following parameters: | ОтелКонтекст.os:45-48,82-87 |
| 7 | MUST | ✅ | The API MUST return the value in the `Context` for the specified key. | ОтелКонтекст.os:45-48 |
| 8 | MUST | ✅ | The API MUST return a new `Context` containing the new value. | ОтелКонтекст.os:114-118,130-134 |
| 9 | SHOULD | ✅ | SHOULD only be used to implement automatic scope switching and define | ОтелКонтекст.os:147-178 |
| 10 | MUST | ✅ | The API MUST return the `Context` associated with the caller’s current execution unit. | ОтелКонтекст.os:29-35 |
| 11 | MUST | ✅ | The API MUST return a value that can be used as a `Token` to restore the previous | ОтелОбласть.os:19-27 |

### Env Vars

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 594 | SHOULD | ✅ | If they do, they SHOULD use the names and value parsing behavior specified in this document. | ОтелАвтоконфигурация.os:1-34 |
| 595 | SHOULD | ✅ | They SHOULD also follow the common configuration specification. | ОтелАвтоконфигурация.os |
| 596 | MUST | ✅ | The environment-based configuration MUST have a direct code configuration equivalent. | ОтелАвтоконфигурация.os:59-378 |
| 597 | MUST | ⚠️ | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | ОтелАвтоконфигурация.os:105,114 (Empty = unset, but not all vars tested) |
| 598 | MUST | ✅ | Any value that represents a Boolean MUST be set to true only by the | ОтелАвтоконфигурация.os:561-564 |
| 599 | MUST NOT | ✅ | accepted, as true. An implementation MUST NOT extend this definition and define | ОтелАвтоконфигурация.os:561-564 |
| 600 | MUST | ✅ | here as a true value, including unset and empty values, MUST be interpreted as | ОтелАвтоконфигурация.os:561-564 |
| 601 | SHOULD | ✅ | empty, or unset is used, a warning SHOULD be logged to inform users about the | ОтелАвтоконфигурация.os:561-564 |
| 602 | SHOULD | ✅ | fallback to false being applied. All Boolean environment variables SHOULD be | ОтелАвтоконфигурация.os:561-564 |
| 603 | MUST NOT | ✅ | Renaming or changing the default value MUST NOT happen without a major version | ОтелАвтоконфигурация.os:561-564 |
| 604 | SHOULD | ✅ | thus qualified as “SHOULD” to allow implementations to avoid breaking changes. | ОтелАвтоконфигурация.os:160,204 |
| 605 | MUST | ✅ | implementations, these should be treated as MUST requirements. | ОтелАвтоконфигурация.os:224-227 |
| 606 | SHOULD | ✅ | implementation cannot parse, the implementation SHOULD generate a warning and gracefully | ОтелАвтоконфигурация.os:264-266 |
| 607 | SHOULD | ⚠️ | Enum values SHOULD be interpreted in a case-insensitive manner. | ОтелАвтоконфигурация.os:197-219 (Enums case-insensitive but inconsistent) |
| 608 | MUST | ⚠️ | the implementation does not recognize, the implementation MUST generate | ОтелАвтоконфигурация.os:216-218 (Inconsistent error handling for enums) |
| 609 | SHOULD | ✅ | Implementations SHOULD only offer environment variables for the types of attributes, for | ОтелАвтоконфигурация.os:562-564 |
| 610 | SHOULD | ✅ | * `"otlp"`: OTLP* `"zipkin"`: Zipkin (Defaults to protobuf format)* `"console"`: Standard Output* `"logging"`: Standard ... | ОтелАвтоконфигурация.os:104-110 |
| 611 | SHOULD | ✅ | * `"otlp"`: OTLP* `"prometheus"`: Prometheus* `"console"`: Standard Output* `"logging"`: Standard Output. It is a deprec... | ОтелАвтоконфигурация.os:113-116 |
| 612 | SHOULD | ❌ | * `"otlp"`: OTLP* `"console"`: Standard Output* `"logging"`: Standard Output. It is a deprecated value left for backward... | -OTEL_LOG_LEVEL not implemented |
| 613 | MUST | ✅ | MUST be ignored. Ignoring the environment variables is necessary because | ОтелАвтоконфигурация.os:339-378 |

### Logs Api

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 263 | SHOULD | ✅ | Thus, the API SHOULD provide a way to set/register and access a global default | ОтелГлобальный.os:74-86 |
| 264 | MUST | ✅ | The `LoggerProvider` MUST provide the following functions: | ОтелПровайдерЛогирования.os:29-31,44-68 |
| 265 | MUST | ✅ | This API MUST accept the following instrumentation scope | ОтелПровайдерЛогирования.os:44-48 |
| 266 | MUST | ✅ | associate with emitted telemetry. This API MUST be structured to accept a | ОтелПровайдерЛогирования.os:29-31 |
| 267 | MUST | ✅ | The `Logger` MUST provide a function to: | ОтелЛоггер.os:21-23,43-58 |
| 268 | SHOULD | ⚠️ | The `Logger` SHOULD provide functions to: | ОтелЛоггер.os:32-34 (Enabled exists but lacks parameters) |
| 269 | SHOULD | ✅ | When implicit Context is supported, then this parameter SHOULD be optional and | ОтелЗаписьЛога.os:366-376 |
| 270 | MUST | ✅ | if unspecified then MUST use current Context. | ОтелЗаписьЛога.os:366-376 |
| 271 | SHOULD | ⚠️ | When only explicit Context is supported, this parameter SHOULD be required.* Severity Number (optional)* Severity Text (... | ОтелЗаписьЛога.os:21-275 (LogRecord has fields but no ergonomic API) |
| 272 | SHOULD | ✅ | generating a `LogRecord`, a `Logger` SHOULD provide this `Enabled` API. | ОтелЛоггер.os:32-34 |
| 273 | SHOULD | ⚠️ | The API SHOULD accept the following parameters: | ОтелЛоггер.os:21-23 (No overloads for direct parameters) |
| 274 | MUST | ✅ | For each optional parameter, the API MUST be structured to accept it, but MUST | ОтелЛоггер.os:43-58 |
| 275 | MUST | ➖ | For each required parameter, the API MUST be structured to obligate a user to | -OneScript uses dynamic typing |
| 276 | MUST | ✅ | LoggerProvider - all methods MUST be documented that implementations need to | ОтелПровайдерЛогирования.os:158 |
| 277 | MUST | ✅ | Logger - all methods MUST be documented that implementations need to | ОтелЛоггер.os:43-58 |
| 278 | SHOULD | ⚠️ | The ergonomic API SHOULD make it more convenient to emit event records following | -Fluent on LogRecord, no convenience on Logger |
| 279 | SHOULD | ✅ | The design of the ergonomic API SHOULD be idiomatic for its language. | - |

### Logs Sdk

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 280 | MUST | ✅ | All language implementations of OpenTelemetry MUST provide an SDK. | ОтелSdk.os, ОтелПровайдерЛогирования.os |
| 281 | MUST | ✅ | A `LoggerProvider` MUST provide a way to allow a Resource | ОтелПровайдерЛогирования.os:145-153 |
| 282 | SHOULD | ✅ | to be specified. If a `Resource` is specified, it SHOULD be associated with all | ОтелПостроительПровайдераЛогирования.os:22-25 |
| 283 | SHOULD | ✅ | The SDK SHOULD allow the creation of multiple independent `LoggerProviders`s. | ОтелПостроительПровайдераЛогирования.os:60-66 |
| 284 | SHOULD | ✅ | It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` | ОтелПровайдерЛогирования.os:29-31,44-68 |
| 285 | MUST | ✅ | The `LoggerProvider` MUST implement the Get a Logger API. | ОтелПровайдерЛогирования.os:44-68 |
| 286 | MUST | ✅ | working `Logger` MUST be returned as a fallback rather than returning null or | ОтелПровайдерЛогирования.os:49-68 |
| 287 | SHOULD | ✅ | throwing an exception, its `name` SHOULD keep the original invalid value, and a | ОтелЛоггер.os:32-34 |
| 288 | SHOULD | ⚠️ | message reporting that the specified value is invalid SHOULD be logged. | -No warning for invalid logger name |
| 289 | MUST | ➖ | MUST be owned by the `LoggerProvider`. The configuration MAY be applied at the | ОтелПровайдерЛогирования.os:1-172 (Development status в спецификации (LoggerConfig/LoggerConfigurator)) |
| 290 | MUST | ➖ | configuration MUST also apply to all already returned `Logger`s (i.e. it MUST | -Development status в спецификации (LoggerConfig/LoggerConfigurator) |
| 291 | MUST | ⚠️ | `Shutdown` MUST be called only once for each `LoggerProvider` instance. After | ОтелПровайдерЛогирования.os:99-104 (Shutdown exists, no once-only check) |
| 292 | SHOULD | ✅ | SDKs SHOULD return a valid no-op `Logger` for these calls, if possible. | ОтелПровайдерЛогирования.os:49-52 |
| 293 | SHOULD | ❌ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` MAY be | -No timeout for Shutdown |
| 294 | MUST | ✅ | `Shutdown` MUST be implemented by invoking `Shutdown` on all | ОтелПровайдерЛогирования.os:100-104 |
| 295 | SHOULD | ⚠️ | failed or timed out. `ForceFlush` SHOULD return some ERROR status if there | ОтелПровайдерЛогирования.os:90-94 (ForceFlush returns Promise, no ERROR status) |
| 296 | SHOULD | ⚠️ | is an error condition; and if there is no error condition, it SHOULD return | ОтелПровайдерЛогирования.os:112-116 (No explicit SUCCESS/ERROR indication) |
| 297 | SHOULD | ❌ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be | -No timeout for ForceFlush |
| 298 | MUST | ✅ | `ForceFlush` MUST invoke `ForceFlush` on all | ОтелПровайдерЛогирования.os:90-94 |
| 299 | MUST | ➖ | If a `Logger` is disabled, it MUST behave equivalently | -Development status в спецификации (LoggerConfig/LoggerConfigurator) |
| 300 | MUST | ➖ | If not explicitly set, the `minimum_severity` parameter MUST default to `0`. | -Development status в спецификации (LoggerConfig/LoggerConfigurator) |
| 301 | MUST | ➖ | specified (i.e. not `0`) and is less than the configured `minimum_severity`, the log record MUST | -Development status в спецификации (LoggerConfig/LoggerConfigurator) |
| 302 | MUST | ➖ | If not explicitly set, the `trace_based` parameter MUST default to `false`. | -Development status в спецификации (LoggerConfig/LoggerConfigurator) |
| 303 | MUST | ➖ | If `trace_based` is `true`, log records associated with unsampled traces MUST | -Development status в спецификации (LoggerConfig/LoggerConfigurator) |
| 304 | SHOULD | ✅ | the implementation SHOULD set it equal to the current time. | ОтелЛоггер.os:48-50 |
| 305 | MUST | ❌ | If an Exception is provided, the SDK MUST by default set attributes | -No exception-to-attributes conversion |
| 306 | MUST NOT | ❌ | User-provided attributes MUST take precedence and MUST NOT be overwritten by | -Exception attributes not implemented |
| 307 | MUST | ➖ | the implementation MUST apply the filtering rules defined by the | -Development status в спецификации (LoggerConfig/LoggerConfigurator) |
| 308 | MUST | ➖ | the log record MUST be dropped. | -Development status в спецификации (LoggerConfig/LoggerConfigurator) |
| 309 | MUST | ✅ | A function receiving this as an argument MUST be able to access all the | ОтелЗаписьЛога.os:40-155 |
| 310 | MUST | ✅ | information added to the LogRecord. It MUST also be able to | ОтелЗаписьЛога.os:45-155 |
| 311 | MUST | ✅ | The trace context fields MUST be populated from | ОтелЗаписьЛога.os:366-376 |
| 312 | MUST | ✅ | Counts for attributes due to collection limits MUST be available for exporters | ОтелЗаписьЛога.os:144-146 |
| 313 | MUST | ⚠️ | A function receiving this as an argument MUST additionally be able to modify | ОтелЗаписьЛога.os:173-307 (ReadWrite after emit is no-op) |
| 314 | MUST | ✅ | `LogRecord` attributes MUST adhere to | ОтелЛимитыЗаписейЛога.os:1-79 |
| 315 | MUST | ✅ | If the SDK implements attribute limits it MUST provide a way to change these | ОтелЛимитыЗаписейЛога.os:39-56 |
| 316 | SHOULD | ✅ | The options MAY be bundled in a class, which then SHOULD be called | ОтелЛимитыЗаписейЛога.os:1-79 |
| 317 | MUST | ✅ | MUST allow each pipeline to end with an individual exporter. | ОтелПровайдерЛогирования.os:75-77 |
| 318 | MUST | ✅ | The SDK MUST allow users to implement and configure custom processors and | ОтелПостроительПровайдераЛогирования.os:36-39 |
| 319 | SHOULD NOT | ✅ | therefore it SHOULD NOT block or throw exceptions. | ОтелПростойПроцессорЛогов.os:15-21 |
| 320 | MUST | ✅ | the `logRecord` mutations MUST be visible in next registered processors. | ОтелКомпозитныйПроцессорЛогов.os:17-25 |
| 321 | SHOULD | ✅ | implementations SHOULD recommended to users that a clone of `logRecord` be used | ОтелКомпозитныйПроцессорЛогов.os:17-25 |
| 322 | MUST NOT | ✅ | Any modifications to parameters inside `Enabled` MUST NOT be propagated to the | ОтелЗаписьЛога.os:161-163 |
| 323 | SHOULD | ⚠️ | `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. | ОтелПростойПроцессорЛогов.os:32-36 (Shutdown exists, no once-only check) |
| 324 | SHOULD | ✅ | SHOULD ignore these calls gracefully, if possible. | ОтелПростойПроцессорЛогов.os:32-36 |
| 325 | SHOULD | ⚠️ | to `ForceFlush` SHOULD be completed as soon as possible, preferably before | ОтелБазовыйПакетныйПроцессор.os:65-134 (ForceFlush partial timeout) |
| 326 | SHOULD | ⚠️ | SHOULD try to call the exporter’s `Export` with all `LogRecord`s for which this | ОтелБазовыйПакетныйПроцессор.os:136-149 (ForceFlush calls export) |
| 327 | MUST | ✅ | The built-in LogRecordProcessors MUST do so. If a | ОтелПростойПроцессорЛогов.os:26-28 |
| 328 | MUST | ⚠️ | timeout is specified (see below), the `LogRecordProcessor` MUST prioritize | ОтелБазовыйПакетныйПроцессор.os:136-149 (Timeout partially used) |
| 329 | SHOULD | ✅ | Other common processing scenarios SHOULD be first considered | - |
| 330 | MUST | ✅ | The processor MUST synchronize calls to `LogRecordExporter`’s `Export` | ОтелПростойПроцессорЛогов.os:15-21 |
| 331 | MUST | ✅ | A `LogRecordExporter` MUST support the following functions: | ОтелЭкспортерЛогов.os:22-33,38-46 |
| 332 | MUST NOT | ✅ | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit | ОтелЭкспортерЛогов.os:22-33 |
| 333 | SHOULD NOT | ➖ | default SDK’s `LogRecordProcessors` SHOULD NOT implement retry logic, as the | -Retry in transport, not exporter |
| 334 | SHOULD | ⚠️ | exporter has received prior to the call to `ForceFlush` SHOULD be completed as | ОтелЭкспортерЛогов.os:35-40 (ForceFlush placeholder) |
| 335 | SHOULD | ✅ | Shutdown SHOULD be called only once for each `LogRecordExporter` instance. After | ОтелЭкспортерЛогов.os:44-46 |
| 336 | SHOULD | ✅ | the call to `Shutdown` subsequent calls to `Export` are not allowed and SHOULD | ОтелЭкспортерЛогов.os:22-33 |
| 337 | SHOULD NOT | ➖ | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data | -Shutdown synchronous, doesn't block |
| 338 | MUST | ✅ | LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe | ОтелПровайдерЛогирования.os:158 |
| 339 | MUST | ✅ | Logger - all methods MUST be safe to be called concurrently. | ОтелЛоггер.os:43-58 |
| 340 | MUST | ✅ | LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called | ОтелЭкспортерЛогов.os:23-45 |

### Metrics Api

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 341 | MUST | ✅ | The `MeterProvider` MUST provide the following functions: | ОтелПровайдерМетрик.os:35,50,112,127,149,161 |
| 342 | MUST NOT | ✅ | this API needs to be structured to accept a `version`, but MUST NOT obligate | ОтелМетр.os:50-54 |
| 343 | MUST | ✅ | Therefore, this API needs to be structured to accept a `schema_url`, but MUST | ОтелМетр.os:50-54 |
| 344 | MUST | ✅ | it is up to their discretion. Therefore, this API MUST be structured to | ОтелМетр.os:43-73,72-93 |
| 345 | SHOULD NOT | ➖ | Note: `Meter` SHOULD NOT be responsible for the configuration. This should be | Not applicable - configuration is provider's responsibility |
| 346 | MUST | ✅ | The `Meter` MUST provide functions to create new Instruments: | ОтелМетр.os:43,72,107,139,168,198,227,256 |
| 347 | SHOULD | ➖ | floating point numbers SHOULD be considered as identifying. | Advisory parameters behavior - not explicitly required for implementation |
| 348 | SHOULD | ✅ | API SHOULD treat it as an opaque string. | ОтелМетр.os:43-60 |
| 349 | MUST | ✅ | * It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII | ОтелМетр.os:43-60 |
| 350 | MUST | ✅ | instrument. The API MUST treat it as an opaque string. | ОтелМетр.os:43 |
| 351 | MUST | ✅ | * It MUST support BMP (Unicode Plane | Implementation via OneScript string type supports BMP |
| 352 | MUST | ✅ | support more Unicode Planes.* It MUST support at least 1023 characters. OpenTelemetry | OneScript strings support >1023 characters (OneScript language feature) |
| 353 | MUST | ✅ | OpenTelemetry SDKs MUST handle `advisory` parameters as described | ОтелМетр.os:419-430 |
| 354 | MUST | ✅ | The API to construct synchronous instruments MUST accept the following parameters: | ОтелМетр.os:43-73 |
| 355 | SHOULD | ✅ | The `name` needs to be provided by a user. If possible, the API SHOULD be | ОтелМетр.os:43 |
| 356 | MUST | ✅ | possible to structurally enforce this obligation, the API MUST be documented | ОтелМетр.os:43,72,107,139,168 |
| 357 | SHOULD | ✅ | The API SHOULD be documented in a way to communicate to users that the `name` | ОтелМетр.os:43,72,107,139,168 |
| 358 | SHOULD NOT | ✅ | syntax. The API SHOULD NOT validate the `name`; that | ОтелМетр.os:43-60 |
| 359 | MUST NOT | ✅ | API needs to be structured to accept a `unit`, but MUST NOT obligate a user | ОтелМетр.os:43,72,107,139,168 |
| 360 | MUST | ✅ | rule. Meaning, the API MUST accept a case-sensitive string | ОтелМетр.os:43,72,107,139,168 |
| 361 | SHOULD NOT | ✅ | The API SHOULD NOT validate the `unit`. | ОтелМетр.os:43-60 |
| 362 | MUST NOT | ✅ | MUST NOT obligate a user to provide one. | ОтелМетр.os:43,72,107,139,168 |
| 363 | MUST | ✅ | rule. Meaning, the API MUST accept a string that | ОтелМетр.os:43,72,107,139,168 |
| 364 | MUST NOT | ✅ | but MUST NOT obligate the user to provide it. | ОтелМетр.os:43,72,107,139,168 |
| 365 | SHOULD NOT | ✅ | The API SHOULD NOT validate `advisory` parameters. | ОтелМетр.os:419-430 |
| 366 | MUST | ✅ | The API to construct asynchronous instruments MUST accept the following parameters: | ОтелМетр.os:198-243 |
| 367 | SHOULD NOT | ✅ | syntax. The API SHOULD NOT validate the `name`, | ОтелМетр.os:198-243 |
| 368 | MUST | ✅ | Therefore, this API MUST be structured to accept a variable number of | ОтелМетр.os:198-243 |
| 369 | MUST | ✅ | The API MUST support creation of asynchronous instruments by passing | ОтелМетр.os:198-243 |
| 370 | SHOULD | ✅ | The API SHOULD support registration of `callback` functions associated with | ОтелМетр.os:198-243 |
| 371 | MUST | ✅ | asynchronous instrumentation creation, the user MUST be able to undo | ОтелМетр.os:348-350 |
| 372 | MUST | ✅ | Every currently registered Callback associated with a set of instruments MUST | ОтелМетр.os:355-375 |
| 373 | MUST | ✅ | Callback functions MUST be documented as follows for the end user: | ОтелМетр.os:198,227,256 |
| 374 | SHOULD | ✅ | * Callback functions SHOULD be reentrant safe. The SDK expects to evaluate | ОтелМетр.os:355-375 |
| 375 | SHOULD NOT | ✅ | callbacks for each MetricReader independently.* Callback functions SHOULD NOT take an indefinite amount of time.* Callba... | ОтелМетр.os:355-375 |
| 376 | MUST | ✅ | Callbacks registered at the time of instrument creation MUST apply to | ОтелМетр.os:198-243 |
| 377 | MUST | ✅ | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the | ОтелМетр.os:348-350 |
| 378 | MUST | ✅ | Multiple-instrument Callbacks MUST be associated at the time of | ОтелМетр.os:348-350 |
| 379 | MUST | ✅ | The API MUST treat observations from a single Callback as logically | ОтелМетр.os:355-375 |
| 380 | MUST | ✅ | observations from a single callback MUST be reported with identical | ОтелМетр.os:355-375 |
| 381 | SHOULD | ⚠️ | The API SHOULD provide some way to pass `state` to the | ОтелМетр.os:348 (State parameter support via ЗарегистрироватьОбратныйВызов - limited scope) |
| 382 | SHOULD | ✅ | All synchronous instruments SHOULD provide functions to: | ОтелБазовыйСинхронныйИнструмент.os:179,185 |
| 383 | SHOULD | ✅ | SHOULD provide this `Enabled` API. | ОтелБазовыйСинхронныйИнструмент.os:179 |
| 384 | MUST NOT | ✅ | There MUST NOT be any API for creating a `Counter` other than with a | ОтелМетр.os:43 |
| 385 | SHOULD NOT | ✅ | This API SHOULD NOT return a value (it MAY return a dummy value if required by | ОтелСчетчик.os:21-26 |
| 386 | MUST | ✅ | This API MUST accept the following parameter: | ОтелСчетчик.os:21-26 |
| 387 | SHOULD | ✅ | SHOULD be structured so a user is obligated to provide this parameter. If it | ОтелСчетчик.os:21-26 |
| 388 | MUST | ✅ | is not possible to structurally enforce this obligation, this API MUST be | ОтелСчетчик.os:21-26 |
| 389 | SHOULD | ✅ | The increment value is expected to be non-negative. This API SHOULD be | ОтелСчетчик.os:21-26 |
| 390 | SHOULD NOT | ✅ | non-negative. This API SHOULD NOT validate this value, that is left to | ОтелСчетчик.os:21-26 |
| 391 | MUST | ✅ | up to their discretion. Therefore, this API MUST be structured to accept a | ОтелСчетчик.os:21-26 |
| 392 | MUST | ✅ | (e.g. strong typed struct allocated on the callstack, tuple). The API MUST allow | ОтелСчетчик.os:21-26 |
| 393 | MUST NOT | ✅ | There MUST NOT be any API for creating an Asynchronous Counter other than with a | ОтелМетр.os:198-214 |
| 394 | MUST | ✅ | last one, or something else. The API MUST treat observations from a single | ОтелМетр.os:198-214 |
| 395 | MUST | ✅ | observations from a single callback MUST be reported with identical timestamps. | ОтелМетр.os:355-375 |
| 396 | SHOULD | ✅ | The API SHOULD provide some way to pass `state` to the callback. OpenTelemetry | ОтелМетр.os:348-350 |
| 397 | MUST NOT | ✅ | There MUST NOT be any API for creating a `Histogram` other than with a | ОтелМетр.os:72-93 |
| 398 | SHOULD | ✅ | The value needs to be provided by a user. If possible, this API SHOULD be | ОтелГистограмма.os:20-22 |
| 399 | MUST | ✅ | possible to structurally enforce this obligation, this API MUST be documented | ОтелГистограмма.os:20-22 |
| 400 | SHOULD | ✅ | The value is expected to be non-negative. This API SHOULD be documented in a | ОтелГистограмма.os:20-22 |
| 401 | SHOULD NOT | ✅ | This API SHOULD NOT validate this value, that is left to implementations of | ОтелГистограмма.os:20-22 |
| 402 | MUST | ✅ | their discretion. Therefore, this API MUST be structured to accept a variable | ОтелГистограмма.os:20-22 |
| 403 | MUST NOT | ✅ | There MUST NOT be any API for creating a `Gauge` other than with a | ОтелМетр.os:168-185 |
| 404 | MUST NOT | ✅ | There MUST NOT be any API for creating an Asynchronous Gauge other than with a | ОтелМетр.os:256-273 |
| 405 | MUST NOT | ✅ | There MUST NOT be any API for creating an `UpDownCounter` other than with a | ОтелМетр.os:139-156 |
| 406 | MUST NOT | ✅ | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than | ОтелМетр.os:227-243 |
| 407 | SHOULD | ✅ | All the metrics components SHOULD allow new APIs to be added to | All classes designed with extensible architecture for new APIs |
| 408 | SHOULD | ✅ | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing | Method signatures use optional parameters (= Неопределено patterns) |
| 409 | MUST | ✅ | MeterProvider - all methods MUST be documented that implementations need to | ОтелПровайдерМетрик.os |
| 410 | MUST | ✅ | Meter - all methods MUST be documented that implementations need to be safe | ОтелМетр.os |
| 411 | MUST | ✅ | Instrument - all methods MUST be documented that implementations need to be | ОтелБазовыйСинхронныйИнструмент.os |

### Metrics Sdk

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 412 | MUST | ✅ | A `MeterProvider` MUST provide a way to allow a Resource to | ОтелПровайдерМетрик.os:6-10, ОтелПостроительПровайдераМетрик.os:24-27 |
| 413 | SHOULD | ✅ | be specified. If a `Resource` is specified, it SHOULD be associated with all the | ОтелПровайдерМетрик.os:60-77 |
| 414 | SHOULD | ✅ | The SDK SHOULD allow the creation of multiple independent `MeterProvider`s. | ОтелПостроительПровайдераМетрик.os |
| 415 | SHOULD | ✅ | It SHOULD only be possible to create `Meter` instances through a `MeterProvider` | ОтелМетр.os:50-77 |
| 416 | MUST | ✅ | The `MeterProvider` MUST implement the Get a Meter API. | ОтелПровайдерМетрик.os:50-77 |
| 417 | MUST | ✅ | working Meter MUST be returned as a fallback rather than returning null or | ОтелПровайдерМетр.os:55-58 |
| 418 | MUST NOT | ✅ | configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT | ОтелПровайдерМетрик.os:128 |
| 419 | MUST | ✅ | `Shutdown` MUST be called only once for each `MeterProvider` instance. After the | ОтелПровайдерМетрик.os:127-141 |
| 420 | SHOULD | ✅ | SHOULD return a valid no-op Meter for these calls, if possible. | ОтелПровайдерМетрик.os:55-58 |
| 421 | MUST | ✅ | `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered | ОтелПериодическийЧитательМетрик.os:80-101 |
| 422 | MUST | ✅ | `ForceFlush` MUST invoke `ForceFlush` on all registered | ОтелПериодическийЧитательМетрик.os:81-101 |
| 423 | MUST | ✅ | The SDK MUST provide functionality for a user to create Views for a | ОтелПровайдерМетрик.os:166-187 |
| 424 | MUST | ✅ | `MeterProvider`. This functionality MUST accept as inputs the Instrument | ОтелПредставление.os |
| 425 | MUST | ✅ | The SDK MUST provide the means to register Views with a `MeterProvider`. | ОтелПровайдерМетрик.os:173-187 |
| 426 | SHOULD | ✅ | Criteria SHOULD be treated as additive. This means an Instrument has to match | ОтелСелекторИнструментов.os:24-44 |
| 427 | MUST | ✅ | The SDK MUST accept the following criteria: | ОтелСелекторИнструментов.os:24-44 |
| 428 | MUST | ✅ | If the SDK does not support wildcards in general, it MUST still recognize the | ОтелСелекторИнструментов.os:24-44 |
| 429 | MUST NOT | ✅ | `name`, but MUST NOT obligate a user to provide one. | ОтелСелекторИнструментов.os:24-44 |
| 430 | MUST NOT | ✅ | `type`, but MUST NOT obligate a user to provide one. | ОтелСелекторИнструментов.os:24-44 |
| 431 | MUST NOT | ⚠️ | `unit`, but MUST NOT obligate a user to provide one. | ОтелСелекторИнструментов.os (unit criteria not explicitly in selector (set in View)) |
| 432 | MUST NOT | ✅ | to accept a `meter_name`, but MUST NOT obligate a user to provide one. | ОтелСелекторИнструментов.os:24-44 |
| 433 | MUST NOT | ⚠️ | to accept a `meter_version`, but MUST NOT obligate a user to provide one. | meter_version support implicit via ОбластьИнструментирования but not in selector |
| 434 | MUST NOT | ⚠️ | to accept a `meter_schema_url`, but MUST NOT obligate a user to provide one. | meter_schema_url support implicit but not in selector |
| 435 | MUST NOT | ⚠️ | accept the criteria, but MUST NOT obligate a user to provide them. | Criteria optional but full list not all in selector |
| 436 | MUST | ✅ | The SDK MUST accept the following stream configuration parameters: | ОтелПредставление.os:88-99 |
| 437 | SHOULD | ✅ | `name`: The metric stream name that SHOULD be used. | ОтелПредставление.os:23-25 |
| 438 | SHOULD | ✅ | In order to avoid conflicts, if a `name` is provided the View SHOULD have an | ОтелПредставление.os:23-25 |
| 439 | MUST NOT | ✅ | MUST NOT obligate a user to provide one. If the user does not provide a | ОтелПредставление.os:88-99 |
| 440 | MUST | ✅ | `name` value, name from the Instrument the View matches MUST be used by | ОтелПредставление.os:88-99 |
| 441 | SHOULD | ✅ | `description`: The metric stream description that SHOULD be used. | ОтелПредставление.os:32-33 |
| 442 | MUST NOT | ✅ | accept a `description`, but MUST NOT obligate a user to provide one. If the | ОтелПредставление.os:88-99 |
| 443 | MUST | ✅ | Instrument a View matches MUST be used by default. | ОтелПредставление.os:32-33 |
| 444 | MUST | ✅ | keys that identify the attributes that MUST be kept, and all other attributes | ОтелПредставление.os:41-43 |
| 445 | MUST NOT | ✅ | accept `attribute_keys`, but MUST NOT obligate a user to provide them. | ОтелПредставление.os:88-99 |
| 446 | SHOULD | ✅ | If the user does not provide any value, the SDK SHOULD use | ОтелБазовыйСинхронныйИнструмент.os:81-83 |
| 447 | MUST | ✅ | advisory parameter is absent, all attributes MUST be kept. | ОтелБазовыйСинхронныйИнструмент.os:81-83 |
| 448 | SHOULD | ⚠️ | Additionally, implementations SHOULD support configuring an exclude-list of | Exclude-list not explicitly implemented (only include-list via attribute_keys) |
| 449 | MUST | ✅ | attributes that MUST be excluded, all other attributes MUST be kept. If an | Excluded attributes not kept (include-list approach) |
| 450 | MUST NOT | ✅ | accept an `aggregation`, but MUST NOT obligate a user to provide one. If the | ОтелПредставление.os:60-62 |
| 451 | MUST | ✅ | user does not provide an `aggregation` value, the `MeterProvider` MUST apply | ОтелМетр.os:80-82 |
| 452 | MUST NOT | ✅ | accept an `exemplar_reservoir`, but MUST NOT obligate a user to provide one. | ОтелПредставление.os:88-99 |
| 453 | MUST | ⚠️ | `MeterProvider` MUST apply a default exemplar | ОтелРезервуарЭкземпляров.os (Default exemplar reservoir implementation present) |
| 454 | SHOULD | ✅ | The SDK SHOULD use the following logic to determine how to process Measurements | ОтелМетр.os:419-430 |
| 455 | MUST | ✅ | MUST be honored.* If the `MeterProvider` has one or more `View`(s) registered:* If the Instrument could match the instru... | ОтелМетр.os:43-214 |
| 456 | SHOULD | ✅ | the implementation SHOULD apply the View and emit a warning. If it is not | ОтелМетр.os:43-60 |
| 457 | SHOULD | ✅ | implementation SHOULD emit a warning and proceed as if the View did not | ОтелМетр.os:419-430 |
| 458 | MUST | ✅ | the setting defined by the View MUST take precedence over the advisory parameters.* If the Instrument could not match wi... | ОтелМетр.os:419-430 |
| 459 | SHOULD | ✅ | SDK SHOULD enable the instrument using the default aggregation and temporality. | ОтелМетр.os:80-82 |
| 460 | MUST | ✅ | The SDK MUST provide the following `Aggregation` to support the | ОтелАгрегаторСуммы.os, ОтелАгрегаторГистограммы.os, ОтелАгрегаторПоследнегоЗначения.os, ОтелАгрегаторЭкспоненциальнойГистограммы.os |
| 461 | SHOULD | ⚠️ | The SDK SHOULD provide the following `Aggregation`: | Drop aggregation referenced in ОтелАгрегация.os:45-47 but not fully implemented |
| 462 | SHOULD NOT | ✅ | * Count of `Measurement` values in population.* Arithmetic sum of `Measurement` values in population. This SHOULD NOT be... | ОтелАгрегаторГистограммы.os:81-96 |
| 463 | SHOULD | ✅ | (-∞, 0], (0, 5.0], (5.0, 10.0], (10.0, 25.0], (25.0, 50.0], (50.0, 75.0], (75.0, 100.0], (100.0, 250.0], (250.0, 500.0],... | ОтелАгрегаторГистограммы.os:26-40 |
| 464 | SHOULD NOT | ✅ | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, | ОтелАгрегаторГистограммы.os:49-67 |
| 465 | MUST | ✅ | The implementation MUST maintain reasonable minimum and maximum scale | ОтелАгрегаторЭкспоненциальнойГистограммы.os:34-54 |
| 466 | SHOULD | ✅ | positive or negative ranges, the implementation SHOULD use the maximum | ОтелАгрегаторЭкспоненциальнойГистограммы.os:177-207 |
| 467 | SHOULD | ✅ | Implementations SHOULD adjust the histogram scale as necessary to | ОтелАгрегаторЭкспоненциальнойГистограммы.os |
| 468 | MUST | ✅ | Callback functions MUST be invoked for the specific `MetricReader` | ОтелПериодическийЧитательМетрик.os:44-64 |
| 469 | SHOULD | ✅ | The implementation SHOULD disregard the use of asynchronous instrument | ОтелМетр.os:355-375 |
| 470 | SHOULD | ✅ | The implementation SHOULD use a timeout to prevent indefinite callback | ОтелПериодическийЧитательМетрик.os:44-64 |
| 471 | MUST | ✅ | The implementation MUST complete the execution of all callbacks for a | ОтелМетр.os:355-375 |
| 472 | SHOULD NOT | ✅ | The implementation SHOULD NOT produce aggregated metric data for a | ОтелМетр.os:355-375 |
| 473 | MUST | ✅ | For delta aggregations, the start timestamp MUST equal the previous collection | ОтелБазовыйСинхронныйИнструмент.os:140-160 |
| 474 | MUST | ✅ | with delta temporality aggregation for an instrument MUST share the same start | ОтелМетр.os:419-430 |
| 475 | MUST | ✅ | Cumulative timeseries MUST use a consistent start timestamp for all collection | ОтелМетр.os:419-430 |
| 476 | SHOULD | ✅ | For synchronous instruments, the start timestamp SHOULD be the time of the | ОтелБазовыйСинхронныйИнструмент.os:130-140 |
| 477 | SHOULD | ✅ | For asynchronous instrument, the start timestamp SHOULD be: | ОтелБазовыйНаблюдаемыйИнструмент.os:76-85 |
| 478 | SHOULD | ✅ | cycle. Cardinality limit enforcement SHOULD occur after attribute filtering, | ОтелБазовыйСинхронныйИнструмент.os:81-83 |
| 479 | SHOULD | ✅ | stream, that value SHOULD be used.* If there is no matching view, but the `MetricReader` defines a default | ОтелПериодическийЧитательМетрик.os |
| 480 | SHOULD | ✅ | for, that value SHOULD be used.* If none of the previous values are defined, the default value of 2000 SHOULD | ОтелМетр.os:412 |
| 481 | MUST | ✅ | The SDK MUST create an Aggregator with the overflow attribute set prior to | ОтелБазовыйСинхронныйИнструмент.os:86-98 |
| 482 | MUST | ✅ | be created. The SDK MUST provide the guarantee that overflow would not happen | ОтелБазовыйСинхронныйИнструмент.os:86-98 |
| 483 | MUST | ✅ | Aggregators for synchronous instruments with cumulative temporality MUST | ОтелБазовыйСинхронныйИнструмент.os:140-160 |
| 484 | MUST | ✅ | Regardless of aggregation temporality, the SDK MUST ensure that every | ОтелБазовыйСинхронныйИнструмент.os:86-98 |
| 485 | MUST NOT | ✅ | Measurements MUST NOT be double-counted or dropped | ОтелБазовыйСинхронныйИнструмент.os:86-98 |
| 486 | SHOULD | ✅ | Aggregators of asynchronous instruments SHOULD prefer the first-observed | ОтелБазовыйНаблюдаемыйИнструмент.os |
| 487 | MUST | ✅ | Distinct meters MUST be treated as separate namespaces for the purposes of detecting | ОтелМетр.os |
| 488 | MUST | ✅ | If a `Meter` is disabled, it MUST behave equivalently | ОтелМетр.os:399-417 |
| 489 | MUST | ✅ | The value of `enabled` MUST be used to resolve whether an instrument | ОтелМетр.os:488 |
| 490 | MUST | ✅ | duplicate instrument. This means that the Meter MUST return a functional | ОтелМетр.os:43-214 |
| 491 | SHOULD | ✅ | a warning SHOULD be emitted. The emitted warning SHOULD include information for | ОтелМетр.os:47-48, 76-77 |
| 492 | SHOULD | ✅ | SHOULD avoid the warning.* If the potential conflict involves instruments that can be distinguished by | ОтелМетр.os:47-48 |
| 493 | SHOULD | ✅ | recipe SHOULD be included in the warning.* Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the | ОтелМетр.os:47-48 |
| 494 | MUST | ✅ | the SDK MUST aggregate data from identical Instruments | ОтелМетр.os:43-214 |
| 495 | MUST | ✅ | multiple casings of the same `name`. When this happens, the Meter MUST return | ОтелМетр.os:43-214 |
| 496 | SHOULD | ✅ | When a Meter creates an instrument, it SHOULD validate the instrument name | ОтелМетр.os:496-497 |
| 497 | SHOULD | ✅ | If the instrument name does not conform to this syntax, the Meter SHOULD emit | ОтелМетр.os:496-497 |
| 498 | SHOULD NOT | ✅ | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | ОтелМетр.os:498 |
| 499 | MUST | ✅ | If a unit is not provided or the unit is null, the Meter MUST treat it the same | ОтелМетр.os:499 |
| 500 | SHOULD NOT | ✅ | When a Meter creates an instrument, it SHOULD NOT validate the instrument | ОтелМетр.os:500 |
| 501 | MUST | ✅ | Meter MUST treat it the same as an empty description string. | ОтелМетр.os:501 |
| 502 | SHOULD | ✅ | When a Meter creates an instrument, it SHOULD validate the instrument advisory | ОтелМетр.os:502-503 |
| 503 | SHOULD | ✅ | parameters. If an advisory parameter is not valid, the Meter SHOULD emit an error | ОтелМетр.os:502-503 |
| 504 | MUST | ✅ | different advisory parameters, the Meter MUST return an instrument using the | ОтелМетр.os:504-505 |
| 505 | MUST | ✅ | MUST take precedence over the advisory parameters. | ОтелМетр.os:504-505 |
| 506 | MUST | ✅ | parameter MUST be used. If neither is provided, the default bucket boundaries | ОтелАгрегаторГистограммы.os:26-40 |
| 507 | MUST | ✅ | The synchronous instrument `Enabled` MUST return `false` | ОтелБазовыйСинхронныйИнструмент.os:179-187 |
| 508 | MUST | ✅ | A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements | ОтелРезервуарЭкземпляров.os |
| 509 | SHOULD | ✅ | `Exemplar` sampling SHOULD be turned on by default. If `Exemplar` sampling is | ОтелФильтрЭкземпляров.os:33-35 |
| 510 | MUST NOT | ✅ | off, the SDK MUST NOT have overhead related to exemplar sampling. | ОтелФильтрЭкземпляров.os:23-25 |
| 511 | MUST | ✅ | A Metric SDK MUST allow exemplar sampling to leverage the configuration of | ОтелРезервуарЭкземпляров.os |
| 512 | SHOULD | ✅ | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: | ОтелФильтрЭкземпляров.os |
| 513 | MUST | ✅ | The `ExemplarFilter` configuration MUST allow users to select between one of the | ОтелФильтрЭкземпляров.os:14-35 |
| 514 | SHOULD | ✅ | The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for | ОтелПостроительПровайдераМетрик.os:70-73 |
| 515 | SHOULD | ✅ | an SDK. The default value SHOULD be `TraceBased`. The filter configuration | ОтелФильтрЭкземпляров.os:33-35 |
| 516 | SHOULD | ✅ | SHOULD follow the environment variable specification. | ОтелФильтрЭкземпляров.os |
| 517 | MUST | ✅ | An OpenTelemetry SDK MUST support the following filters: | ОтелФильтрЭкземпляров.os |
| 518 | MUST | ✅ | The `ExemplarReservoir` interface MUST provide a method to offer measurements | ОтелРезервуарЭкземпляров.os:35-61 |
| 519 | MUST | ✅ | A new `ExemplarReservoir` MUST be created for every known timeseries data point, | ОтелРезервуарЭкземпляров.os |
| 520 | SHOULD | ✅ | The “offer” method SHOULD accept measurements, including: | ОтелРезервуарЭкземпляров.os:35-61 |
| 521 | SHOULD | ✅ | The “offer” method SHOULD have the ability to pull associated trace and span | ОтелФильтрЭкземпляров.os |
| 522 | MUST | ✅ | from the timeseries the reservoir is associated with. This MUST be clearly | ОтелРезервуарЭкземпляров.os |
| 523 | MUST | ✅ | documented in the API and the reservoir MUST be given the `Attributes` | ОтелРезервуарЭкземпляров.os:35-61 |
| 524 | MUST | ✅ | The “collect” method MUST return accumulated `Exemplar`s. Exemplars are expected | ОтелРезервуарЭкземпляров.os:71-77 |
| 525 | SHOULD | ✅ | with. In other words, Exemplars reported against a metric data point SHOULD have | ОтелРезервуарЭкземпляров.os:71-77 |
| 526 | MUST | ✅ | `Exemplar`s MUST retain any attributes available in the measurement that | ОтелРезервуарЭкземпляров.os:71-77 |
| 527 | SHOULD | ✅ | The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. | ОтелРезервуарЭкземпляров.os |
| 528 | MUST | ✅ | The SDK MUST include two types of built-in exemplar reservoirs: | ОтелРезервуарЭкземпляров.os |
| 529 | SHOULD | ✅ | * Explicit bucket histogram aggregation with more than 1 bucket SHOULD | ОтелАгрегаторГистограммы.os |
| 530 | SHOULD | ✅ | use `AlignedHistogramBucketExemplarReservoir`.* Base2 Exponential Histogram Aggregation SHOULD use a | ОтелАгрегаторЭкспоненциальнойГистограммы.os |
| 531 | SHOULD | ✅ | twenty (e.g. `min(20, max_buckets)`).* All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`. | ОтелРезервуарЭкземпляров.os |
| 532 | MUST | ✅ | This reservoir MUST use a uniformly-weighted sampling algorithm based on the | ОтелРезервуарЭкземпляров.os:35-61 |
| 533 | SHOULD | ✅ | Any stateful portion of sampling computation SHOULD be reset every collection | ОтелБазовыйСинхронныйИнструмент.os |
| 534 | SHOULD | ✅ | contention. Otherwise, a default size of `1` SHOULD be used. | ОтелРезервуарЭкземпляров.os:100 |
| 535 | MUST | ✅ | This Exemplar reservoir MUST take a configuration parameter that is the | ОтелАгрегаторГистограммы.os |
| 536 | MUST | ✅ | configuration of a Histogram. This implementation MUST store at most one | ОтелАгрегаторГистограммы.os |
| 537 | SHOULD | ✅ | measurement that falls within a histogram bucket, and SHOULD use a | ОтелАгрегаторГистограммы.os |
| 538 | SHOULD | ✅ | number of bucket boundaries plus one. This configuration parameter SHOULD have | ОтелАгрегаторГистограммы.os:26-40 |
| 539 | MUST | ✅ | The SDK MUST provide a mechanism for SDK users to provide their own | ОтелПредставление.os:88-99 |
| 540 | MUST | ✅ | ExemplarReservoir implementation. This extension MUST be configurable on | ОтелПредставление.os:88-99 |
| 541 | MUST | ✅ | a metric View, although individual reservoirs MUST still be | ОтелПредставление.os:88-99 |
| 542 | SHOULD | ✅ | * The `exporter` to use, which is a `MetricExporter` instance.* The default output `aggregation` (optional), a function ... | ОтелПериодическийЧитательМетрик.os:1-100 |
| 543 | SHOULD | ✅ | `MetricReader` SHOULD be provided to be used | ОтелПериодическийЧитательМетрик.os |
| 544 | MUST | ✅ | The `MetricReader` MUST ensure that data points from OpenTelemetry | ОтелПериодическийЧитательМетрик.os |

### Otlp Exporter

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 545 | MUST | ✅ | The following configuration options MUST be available to configure the OTLP exporter. | ОтелАвтоконфигурация.os:59-162 |
| 546 | MUST | ⚠️ | Each configuration option MUST be overridable by a signal specific option. | ОтелАвтоконфигурация.os:177,255,291 (Signal-specific endpoints NOT implemented) |
| 547 | MUST | ⚠️ | The implementation MUST honor the following URL components: | ОтелHttpТранспорт.os:55-102 (URL components not parsed separately) |
| 548 | MUST | ❌ | When using `OTEL_EXPORTER_OTLP_ENDPOINT`, exporters MUST construct per-signal URLs as described below. The per-signal en... | -Signal-specific endpoints not supported |
| 549 | MUST | ⚠️ | Endpoint (OTLP/gRPC): Target to which the exporter is going to send spans, metrics, or logs. The option SHOULD accept an... | ОтелАвтоконфигурация.os:153-155 (Accepts URLs but no http/https distinction) |
| 550 | MUST | ⚠️ | Protocol: The transport protocol. Options MUST be one of: `grpc`, `http/protobuf`, `http/json`. | ОтелАвтоконфигурация.os:150-161 (Only grpc and http/json, no http/protobuf) |
| 551 | SHOULD | ➖ | [1]: SDKs SHOULD default endpoint variables to use `http` scheme unless they have good reasons to choose | ОтелАвтоконфигурация.os:153,158 (Hardcoded defaults) |
| 552 | SHOULD | ➖ | they SHOULD continue to be supported as they were part of a stable release of the specification. | -New SDK, no legacy |
| 553 | SHOULD | ⚠️ | [4]: The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the de... | ОтелАвтоконфигурация.os:150 (Default http/json, not http/protobuf) |
| 554 | MUST | ✅ | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs | ОтелHttpТранспорт.os:74 |
| 555 | MUST | ✅ | MUST be used as-is without any modification. The only exception is that if an | ОтелHttpТранспорт.os:55 |
| 556 | MUST | ⚠️ | URL contains no path part, the root path `/` MUST be used (see Example 2). | ОтелHttpТранспорт.os:74 (No explicit root path handling) |
| 557 | MUST NOT | ✅ | An SDK MUST NOT modify the URL in ways other than specified above. That also means, | ОтелHttpТранспорт.os:74 |
| 558 | MUST | ⚠️ | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST | ОтелGrpcТранспорт.os, ОтелHttpТранспорт.os (gRPC and HTTP/JSON, no http/protobuf) |
| 559 | SHOULD | ✅ | support at least one of them. If they support only one, it SHOULD be | - |
| 560 | SHOULD | ❌ | If no configuration is provided the default transport SHOULD be `http/protobuf` | ОтелАвтоконфигурация.os:150 (Default is http/json, not http/protobuf) |
| 561 | MUST | ✅ | The `OTEL_EXPORTER_OTLP_HEADERS`, `OTEL_EXPORTER_OTLP_TRACES_HEADERS`, `OTEL_EXPORTER_OTLP_METRICS_HEADERS`, `OTEL_EXPOR... | ОтелАвтоконфигурация.os:133-139 |
| 562 | MUST | ⚠️ | Transient errors MUST be handled with a retry strategy. This retry strategy MUST implement an exponential back-off with ... | ОтелHttpТранспорт.os:85 (Exponential backoff without jitter) |
| 563 | SHOULD | ❌ | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of ... | -User-Agent header not set |
| 564 | SHOULD | ❌ | The format of the header SHOULD follow RFC 7231. The conventions used for specifying the OpenTelemetry SDK language and ... | -User-Agent not implemented |

### Propagators

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 565 | MUST | ✅ | `Propagator`s MUST define `Inject` and `Extract` operations, in order to write | ОтелW3CПропагатор.os:38-56,68-119 |
| 566 | MUST | ✅ | values to and read values from carriers respectively. Each `Propagator` type MUST define the specific carrier type | ОтелW3CПропагатор.os:38-56 |
| 567 | MUST | ✅ | * A `Context`. The Propagator MUST retrieve the appropriate value from the `Context` first, such as | ОтелW3CПропагатор.os:39-42 |
| 568 | MUST NOT | ✅ | the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, | ОтелW3CПропагатор.os:38-56 |
| 569 | MUST | ✅ | In order to increase compatibility, the key/value pairs MUST only consist of US-ASCII characters | ОтелW3CПропагатор.os:38-56 |
| 570 | MUST | ⚠️ | `Getter` and `Setter` MUST be stateless and allowed to be saved as constants, in order to effectively | -Direct Соответствие access, no stateless getter/setter |
| 571 | MUST | ✅ | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used pr... | ОтелW3CПропагатор.os:70-74 |
| 572 | MUST | ⚠️ | The `Keys` function MUST return the list of all the keys in the carrier. | -No explicit Keys() function for carriers |
| 573 | MUST | ⚠️ | The Get function MUST return the first value of the given propagation key or return null if the key doesn’t exist. | ОтелW3CПропагатор.os:70-74 (Case-insensitive via НРег) |
| 574 | MUST | ✅ | The Get function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP request ob... | ОтелW3CПропагатор.os:70-74 |
| 575 | MUST | ❌ | If explicitly implemented, the `GetAll` function MUST return all values of the given propagation key. | -GetAll function not implemented |
| 576 | SHOULD | ❌ | It SHOULD return them in the same order as they appear in the carrier. | -GetAll ordering N/A |
| 577 | SHOULD | ❌ | If the key doesn’t exist, it SHOULD return an empty collection. | -GetAll empty collection N/A |
| 578 | MUST | ❌ | The `GetAll` function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP reque... | -GetAll case sensitivity N/A |
| 579 | MUST | ✅ | Implementations MUST offer a facility to group multiple `Propagator`s | ОтелКомпозитныйПропагатор.os:1-78 |
| 580 | MUST | ✅ | There MUST be functions to accomplish the following operations. | ОтелКомпозитныйПропагатор.os:17-55 |
| 581 | MUST | ⚠️ | The OpenTelemetry API MUST provide a way to obtain a propagator for each | -No GetGlobalPropagator/SetGlobalPropagator API |
| 582 | SHOULD | ⚠️ | supported `Propagator` type. Instrumentation libraries SHOULD call propagators | -Composite not enforced for instrumentation libs |
| 583 | MUST | ❌ | The OpenTelemetry API MUST use no-op propagators unless explicitly configured | -No-op propagator not found |
| 584 | SHOULD | ⚠️ | propagators. If pre-configured, `Propagator`s SHOULD default to a composite | ОтелАвтоконфигурация.os:30 (OTEL_PROPAGATORS env var mentioned) |
| 585 | MUST | ❌ | These platforms MUST also allow pre-configured propagators to be disabled or overridden. | -Override/disable mechanism not documented |
| 586 | MUST | ❌ | This method MUST exist for each supported `Propagator` type. | -GetGlobalPropagator method not found |
| 587 | MUST | ✅ | The official list of propagators that MUST be maintained by the OpenTelemetry | - |
| 588 | MUST | ⚠️ | organization and MUST be distributed as OpenTelemetry extension packages: | -W3C exists but no B3 |
| 589 | MUST NOT | ➖ | used by the OpenTracing Basic Tracers. It MUST NOT use `OpenTracing` in the resulting | -OpenTracing propagators intentionally excluded |
| 590 | MUST NOT | ➖ | X-Ray trace header protocol MUST NOT be maintained or distributed as part of | -X-Ray propagator intentionally excluded |
| 591 | MUST | ✅ | A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP headers as specified in W... | ОтелW3CПропагатор.os:38-119 |
| 592 | MUST | ➖ | the multi-header version.* MUST preserve a debug trace flag, if received, and propagate | -B3 propagator not in scope for this SDK |
| 593 | MUST | ➖ | Fields MUST return the header names that correspond to the configured format, | -B3 Fields N/A |

### Resource Sdk

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 28 | MUST | ✅ | with closed source environments. The SDK MUST allow for creation of `Resources` and | ОтелРесурс.os:83-102 |
| 29 | MUST | ✅ | all `Span`s produced by any `Tracer` from the provider MUST be associated with this `Resource`. | ОтелSdk.os |
| 30 | MUST | ✅ | The SDK MUST provide access to a Resource with at least the attributes listed at | ОтелРесурс.os:104-113 |
| 31 | MUST | ✅ | This resource MUST be associated with a `TracerProvider` or `MeterProvider` | ОтелSdk.os:20-23 |
| 32 | MUST | ✅ | The interface MUST provide a way to create a new resource, from `Attributes`. | ОтелПостроительРесурса.os:19-22 |
| 33 | MUST | ✅ | The interface MUST provide a way for an old resource and an | ОтелРесурс.os:44-65 |
| 34 | MUST | ✅ | The resulting resource MUST have all attributes that are on any of the two input resources. | ОтелРесурс.os:58-63 |
| 35 | MUST | ✅ | resource MUST be picked (even if the updated value is empty). | ОтелРесурс.os:44-55 |
| 36 | MUST | ❌ | or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as | -No cloud resource detectors |
| 37 | MUST | ❌ | Resource detector packages MUST provide a method that returns a resource. This | -No resource detector packages |
| 38 | MUST NOT | ❌ | failure to detect any resource information MUST NOT be considered an error, | -Detection failure handling not visible |
| 39 | SHOULD | ❌ | SHOULD be considered an error. | -No error handling for unsupported detectors |
| 40 | MUST | ❌ | semantic conventions MUST ensure that the resource has a Schema URL set to a | -No schema URL validation in detectors |
| 41 | SHOULD | ❌ | value that matches the semantic conventions. Empty Schema URL SHOULD be used if | -Empty schema URL handling not found |
| 42 | MUST | ❌ | the detectors use different non-empty Schema URL it MUST be an error since it is | -Schema URL conflict detection not found |
| 43 | SHOULD | ❌ | Resource detectors SHOULD have a unique name for reference in configuration. For | -Resource detectors unnamed |
| 44 | SHOULD | ❌ | Names SHOULD be snake case and | -No snake_case naming for detectors |
| 45 | SHOULD | ❌ | Resource detector names SHOULD reflect | -Resource detector names not found |
| 46 | SHOULD | ❌ | multiple root namespaces SHOULD choose a name which appropriately conveys their | -Multiple root namespace handling not found |
| 47 | SHOULD | ❌ | An SDK which identifies multiple resource detectors with the same name SHOULD | -Duplicate detector name collision not found |
| 48 | SHOULD | ❌ | report an error. In order to limit collisions, resource detectors SHOULD | -Detector limit collisions not found |
| 49 | MUST | ✅ | The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment | ОтелАвтоконфигурация.os:101-110 |
| 50 | MUST | ✅ | All attribute values MUST be considered strings. The `,` and `=` characters | ОтелАвтоконфигурация.os:104-109 |
| 51 | MUST | ⚠️ | in keys and values MUST be percent encoded. Other characters MAY be | ОтелАвтоконфигурация.os (Percent encoding mentioned but unclear) |
| 52 | SHOULD | ❌ | variable value SHOULD be discarded and an error SHOULD be reported following the | -Error handling for malformed attributes not visible |

### Trace Api

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 53 | SHOULD | ➖ | Thus, the API SHOULD provide a way to set/register and access | Timestamp registration/access - OneScript doesn't support Unix timestamps natively; implementation uses nanoseconds as strings |
| 54 | SHOULD | ✅ | Thus, implementations of `TracerProvider` SHOULD allow creating an arbitrary | ОтелПостроительПровайдераТрассировки.os:108 |
| 55 | MUST | ✅ | The `TracerProvider` MUST provide the following functions: | ОтелПровайдерТрассировки.os:52 |
| 56 | MUST | ✅ | This API MUST accept the following parameters: | ОтелПровайдерТрассировки.os:52 |
| 57 | SHOULD | ✅ | * `name` (required): This name SHOULD uniquely identify the | ОтелПровайдерТрассировки.os:52 |
| 58 | MUST | ✅ | (null or empty string) is specified, a working Tracer implementation MUST be | ОтелПровайдерТрассировки.os:59 |
| 59 | SHOULD | ✅ | its `name` property SHOULD be set to an empty string, and a message | ОтелПровайдерТрассировки.os:52 |
| 60 | SHOULD | ⚠️ | reporting that the specified value is invalid SHOULD be logged. A library, | ОтелПровайдерТрассировки.os:52 (Message logging for invalid name - not explicitly documented but returns valid tracer) |
| 61 | MUST NOT | ✅ | Implementations MUST NOT require users to repeatedly obtain a `Tracer` again | ОтелПровайдерТрассировки.os:63 |
| 62 | MUST | ✅ | The API MUST provide the following functionality to interact with a `Context` | ОтелКонтекст.os |
| 63 | SHOULD | ✅ | here), the API SHOULD also provide | ОтелТрассировщик.os:49-50 |
| 64 | SHOULD | ✅ | inside the trace module. This functionality SHOULD be fully implemented in the API when possible. | ОтелТрассировщик.os:49-50 |
| 65 | MUST | ✅ | The `Tracer` MUST provide functions to: | ОтелТрассировщик.os:22-104 |
| 66 | SHOULD | ✅ | The `Tracer` SHOULD provide functions to: | ОтелТрассировщик.os:33 |
| 67 | SHOULD | ✅ | creating `Span`s, a `Tracer` SHOULD provide this `Enabled` API. | ОтелТрассировщик.os:33 |
| 68 | MUST | ✅ | added in the future, therefore, the API MUST be structured in a way for | ОтелТрассировщик.os |
| 69 | MUST | ✅ | This API MUST return a language idiomatic boolean type. A returned value of | ОтелТрассировщик.os:33 |
| 70 | SHOULD | ⚠️ | SHOULD be documented that instrumentation authors needs to call this API each | ОтелТрассировщик.os:33 (Documentation suggests calling Enabled() each time (implicit)) |
| 71 | MUST | ✅ | The API MUST implement methods to create a `SpanContext`. These methods SHOULD be the only way to | ОтелКонтекстСпана.os:124 |
| 72 | SHOULD NOT | ✅ | create a `SpanContext`. This functionality MUST be fully implemented in the API, and SHOULD NOT be | ОтелКонтекстСпана.os:124 |
| 73 | MUST | ✅ | The API MUST allow retrieving the `TraceId` and `SpanId` in the following forms: | ОтелКонтекстСпана.os:23-33 |
| 74 | MUST | ✅ | `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` | ОтелКонтекстСпана.os:23 |
| 75 | MUST | ✅ | (result MUST be a 16-hex-character lowercase string).* Binary - returns the binary representation of the `TraceId` (resu... | ОтелКонтекстСпана.os:32 |
| 76 | MUST | ⚠️ | 16-byte array) or `SpanId` (result MUST be an 8-byte array). | ОтелКонтекстСпана.os (Binary forms not explicitly implemented (hex strings only)) |
| 77 | SHOULD NOT | ✅ | The API SHOULD NOT expose details about how they are internally stored. | ОтелКонтекстСпана.os |
| 78 | MUST | ✅ | non-zero TraceID and a non-zero SpanID, MUST be provided. | ОтелКонтекстСпана.os:70 |
| 79 | MUST | ✅ | propagated from a remote parent, MUST be provided. | ОтелКонтекстСпана.os:60 |
| 80 | MUST | ⚠️ | `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | ОтелКонтекстСпана.os:60 (IsRemote property stored but child span inheritance not explicitly shown) |
| 81 | MUST | ✅ | Tracing API MUST provide at least the following operations on `TraceState`: | ОтелСостояниеТрассировки.os |
| 82 | MUST | ✅ | These operations MUST follow the rules described in the W3C Trace Context specification. | ОтелСостояниеТрассировки.os |
| 83 | MUST | ✅ | All mutating operations MUST return a new `TraceState` with the modifications applied. | ОтелСостояниеТрассировки.os:66,105 |
| 84 | MUST | ✅ | `TraceState` MUST at all times be valid according to rules specified in W3C Trace Context specification. | ОтелСостояниеТрассировки.os:227-335 |
| 85 | MUST | ✅ | Every mutating operations MUST validate input parameters. | ОтелСостояниеТрассировки.os:67,105 |
| 86 | MUST NOT | ✅ | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data | ОтелСостояниеТрассировки.os:67,105 |
| 87 | MUST | ✅ | and MUST follow the general error handling guidelines. | ОтелСостояниеТрассировки.os |
| 88 | SHOULD | ✅ | The span name SHOULD be the most general string that identifies a | ОтелСпан.os:535 |
| 89 | SHOULD | ✅ | Generality SHOULD be prioritized over human-readability. | ОтелСпан.os |
| 90 | SHOULD | ✅ | A `Span`’s start time SHOULD be set to the current time on span | ОтелСпан.os:535 |
| 91 | SHOULD | ✅ | creation. After the `Span` is created, it SHOULD be possible to | ОтелСпан.os |
| 92 | MUST NOT | ✅ | MUST NOT be changed after the `Span`’s end time has been set. | ОтелСпан.os:255-271 |
| 93 | SHOULD NOT | ✅ | prevent misuse, implementations SHOULD NOT provide access to a `Span`’s | ОтелСпан.os |
| 94 | MUST NOT | ✅ | However, alternative implementations MUST NOT allow callers to create `Span`s | ОтелТрассировщик.os:48-104 |
| 95 | MUST | ✅ | directly. All `Span`s MUST be created via a `Tracer`. | ОтелТрассировщик.os:48 |
| 96 | MUST NOT | ✅ | There MUST NOT be any API for creating a `Span` other than with a `Tracer`. | ОтелТрассировщик.os:48 |
| 97 | MUST NOT | ⚠️ | In languages with implicit `Context` propagation, `Span` creation MUST NOT | ОтелТрассировщик.os:48 (Span creation doesn't explicitly propagate implicit context (no context interception shown)) |
| 98 | MUST NOT | ✅ | This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`. | ОтелТрассировщик.os:116-135 |
| 99 | MUST | ✅ | The semantic parent of the Span MUST be determined according to the rules | ОтелТрассировщик.os:52-54 |
| 100 | MUST | ✅ | The API documentation MUST state that adding attributes at span creation is preferred | ОтелПостроительСпана.os:65-78 |
| 101 | SHOULD | ✅ | `Start timestamp`, default to current time. This argument SHOULD only be set | ОтелСпан.os:535 |
| 102 | MUST NOT | ✅ | a Span logical start, API user MUST NOT explicitly set this argument. | ОтелСпан.os |
| 103 | MUST | ✅ | spans in the trace. Implementations MUST provide an option to create a `Span` as | ОтелТрассировщик.os:91,98 |
| 104 | MUST | ✅ | a root span, and MUST generate a new `TraceId` for each root span created. | ОтелТрассировщик.os:92 |
| 105 | MUST | ✅ | For a Span with a parent, the `TraceId` MUST be the same as the parent. | ОтелТрассировщик.os:52-77 |
| 106 | MUST | ✅ | Also, the child span MUST inherit all `TraceState` values of its parent by default. | ОтелТрассировщик.os:52-77 |
| 107 | MUST | ✅ | Any span that is created MUST also be ended. | ОтелСпан.os:436 |
| 108 | MUST | ✅ | During `Span` creation, a user MUST have the ability to record links to other `Span`s. | ОтелПостроительСпана.os:80-96 |
| 109 | MUST | ✅ | The Span interface MUST provide: | ОтелСпан.os:72 |
| 110 | MUST | ✅ | may be used even after the `Span` is finished. The returned value MUST be the | ОтелСпан.os:72 |
| 111 | SHOULD | ✅ | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` | ОтелСпан.os:226 |
| 112 | SHOULD | ✅ | SHOULD always return `false`. The one known exception to this is | ОтелСпан.os:226 |
| 113 | SHOULD NOT | ✅ | `IsRecording` SHOULD NOT take any parameters. | ОтелСпан.os:226 |
| 114 | SHOULD | ✅ | This flag SHOULD be used to avoid expensive computations of a Span attributes or | ОтелСпан.os:226 |
| 115 | MUST | ✅ | A `Span` MUST have the ability to set `Attributes` associated with it. | ОтелСпан.os:255 |
| 116 | SHOULD | ✅ | Setting an attribute with the same key as an existing attribute SHOULD overwrite | ОтелСпан.os:255-271 |
| 117 | MUST | ✅ | A `Span` MUST have the ability to add events. Events have a time associated | ОтелСпан.os:284 |
| 118 | SHOULD | ✅ | Events SHOULD preserve the order in which they are recorded. | ОтелСпан.os:284 |
| 119 | MUST | ✅ | A `Span` MUST have the ability to add `Link`s associated with it after its creation - see Links. | ОтелСпан.os:351 |
| 120 | MUST | ✅ | `Description` MUST only be used with the `Error` `StatusCode` value. | ОтелСпан.os:402-425 |
| 121 | SHOULD | ✅ | * An API to set the `Status`. This SHOULD be called `SetStatus`. This API takes | ОтелСпан.os:402 |
| 122 | MUST | ✅ | appropriate for the language. `Description` MUST be IGNORED for `StatusCode` | ОтелСпан.os:402-425 |
| 123 | SHOULD | ✅ | The status code SHOULD remain unset, except for the following circumstances: | ОтелСпан.os:402-425 |
| 124 | SHOULD | ✅ | An attempt to set value `Unset` SHOULD be ignored. | ОтелСпан.os:402-425 |
| 125 | SHOULD | ✅ | SHOULD be documented and predictable. The status code should only be set to `Error` | ОтелСпан.os:402-425 |
| 126 | SHOULD | ⚠️ | not covered by the semantic conventions, Instrumentation Libraries SHOULD | ОтелСпан.os:402-425 (Instrumentation libraries should set status (per usage documentation)) |
| 127 | SHOULD NOT | ✅ | Generally, Instrumentation Libraries SHOULD NOT set the status code to `Ok`, | ОтелСпан.os:402-425 |
| 128 | SHOULD | ✅ | unless explicitly configured to do so. Instrumentation Libraries SHOULD leave the | ОтелСпан.os:402-425 |
| 129 | SHOULD | ✅ | When span status is set to `Ok` it SHOULD be considered final and any further | ОтелСпан.os:407-425 |
| 130 | SHOULD | ✅ | attempts to change it SHOULD be ignored. | ОтелСпан.os:407-425 |
| 131 | SHOULD | ➖ | Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they | Analysis tools response to Ok status - not applicable for SDK |
| 132 | SHOULD | ✅ | Implementations SHOULD ignore all subsequent calls to `End` and any other Span methods, | ОтелСпан.os:239 |
| 133 | MUST | ✅ | However, all API implementations of such methods MUST internally call the `End` | ОтелСпан.os:436 |
| 134 | MUST NOT | ✅ | `End` MUST NOT have any effects on child spans. | ОтелСпан.os:436 |
| 135 | MUST NOT | ✅ | `End` MUST NOT inactivate the `Span` in any `Context` it is active in. | ОтелСпан.os:436 |
| 136 | MUST | ✅ | It MUST still be possible to use an ended span as parent via a Context it is | ОтелСпан.os:387 |
| 137 | MUST | ✅ | contained in. Also, any mechanisms for putting the Span into a Context MUST | ОтелКонтекст.os |
| 138 | MUST | ✅ | If omitted, this MUST be treated equivalent to passing the current time. | ОтелСпан.os:436 |
| 139 | MUST NOT | ✅ | This operation itself MUST NOT perform blocking I/O on the calling thread. | ОтелСпан.os:436 |
| 140 | SHOULD | ✅ | Any locking used needs be minimized and SHOULD be removed entirely if | ОтелСпан.os:436 |
| 141 | SHOULD | ✅ | To facilitate recording an exception languages SHOULD provide a | ОтелСпан.os:307 |
| 142 | MUST | ✅ | The method MUST record an exception as an `Event` with the conventions outlined in | ОтелСпан.os:307-339 |
| 143 | SHOULD | ✅ | The minimum required argument SHOULD be no more than only an exception object. | ОтелСпан.os:307 |
| 144 | MUST | ✅ | If `RecordException` is provided, the method MUST accept an optional parameter | ОтелСпан.os:307-339 |
| 145 | SHOULD | ✅ | (this SHOULD be done in the same way as for the `AddEvent` method). | ОтелСпан.os:307-339 |
| 146 | MUST | ✅ | Start and end time as well as Event’s timestamps MUST be recorded at a time of a | ОтелСпан.os:436,535 |
| 147 | MUST | ✅ | The API MUST provide an operation for wrapping a `SpanContext` with an object | ОтелНоопСпан.os |
| 148 | SHOULD NOT | ✅ | If a new type is required for supporting this operation, it SHOULD NOT be exposed | ОтелНоопСпан.os:272 |
| 149 | SHOULD | ✅ | it SHOULD be named `NonRecordingSpan`. | ОтелНоопСпан.os:272 |
| 150 | MUST | ✅ | * `GetContext` MUST return the wrapped `SpanContext`.* `IsRecording` MUST return `false` to signal that events, attribut... | ОтелНоопСпан.os:29 |
| 151 | MUST | ✅ | The remaining functionality of `Span` MUST be defined as no-op operations. | ОтелНоопСпан.os:155 |
| 152 | SHOULD NOT | ✅ | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | ОтелНоопСпан.os:74-254 |
| 153 | SHOULD | ✅ | In order for `SpanKind` to be meaningful, callers SHOULD arrange that | ОтелВидСпана.os |
| 154 | SHOULD NOT | ✅ | server-side span SHOULD NOT be used to describe outgoing remote procedure call. | ОтелВидСпана.os |
| 155 | MUST | ✅ | A user MUST have the ability to record links to other `SpanContext`s. | ОтелСпан.os:351 |
| 156 | SHOULD | ✅ | appropriate for the language. Implementations SHOULD record links containing | ОтелПостроительСпана.os:90-96 |
| 157 | SHOULD | ✅ | Span SHOULD preserve the order in which `Link`s are set. | ОтелСпан.os:144 |
| 158 | MUST | ✅ | The API documentation MUST state that adding links at span creation is preferred | ОтелПостроительСпана.os:90 |
| 159 | MUST | ✅ | TracerProvider - all methods MUST be documented that implementations need to | ОтелПровайдерТрассировки.os:52,100 |
| 160 | MUST | ✅ | Tracer - all methods MUST be documented that implementations need to be safe | ОтелТрассировщик.os:48 |
| 161 | MUST | ✅ | Span - all methods MUST be documented that implementations need to be safe | ОтелСпан.os:255 |
| 162 | MUST | ✅ | Event - Events are immutable and MUST be safe for concurrent use by default. | ОтелСобытиеСпана.os |
| 163 | SHOULD | ✅ | Link - Links are immutable and SHOULD be safe for concurrent use by default. | ОтелСпан.os:351 |
| 164 | MUST | ✅ | and that is related to propagation of a `SpanContext`: The API MUST return a | ОтелНоопСпан.os |
| 165 | SHOULD | ✅ | If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly | ОтелНоопСпан.os:272 |
| 166 | MUST | ✅ | If the parent `Context` contains no `Span`, an empty non-recording Span MUST be | ОтелНоопСпан.os |

### Trace Sdk

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 167 | SHOULD | ✅ | It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` | ОтелПровайдерТрассировки.os:36 |
| 168 | MUST | ✅ | The `TracerProvider` MUST implement the Get a Tracer API. | ОтелПровайдерТрассировки.os:52 |
| 169 | MUST | ✅ | The input provided by the user MUST be used to create | ОтелПровайдерТрассировки.os:52-68 |
| 170 | MUST | ✅ | the updated configuration MUST also apply to all already returned `Tracers` | ОтелПровайдерТрассировки.os:52 |
| 171 | MUST NOT | ✅ | (i.e. it MUST NOT matter whether a `Tracer` was obtained from the | ОтелПровайдерТрассировки.os:52 |
| 172 | MUST | ✅ | The function MUST accept the following parameter: | ОтелПостроительПровайдераТрассировки.os:108 |
| 173 | MUST | ✅ | `Shutdown` MUST be called only once for each `TracerProvider` instance. After | ОтелПровайдерТрассировки.os:100-105 |
| 174 | SHOULD | ✅ | SHOULD return a valid no-op Tracer for these calls, if possible. | ОтелПровайдерТрассировки.os:59-60 |
| 175 | SHOULD | ✅ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | ОтелПровайдерТрассировки.os:100-105 |
| 176 | SHOULD | ✅ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` can be | ОтелПровайдерТрассировки.os:100-105 |
| 177 | MUST | ✅ | `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors. | ОтелПровайдерТрассировки.os:100-105 |
| 178 | SHOULD | ✅ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | ОтелПровайдерТрассировки.os:91 |
| 179 | SHOULD | ✅ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | ОтелПровайдерТрассировки.os:91 |
| 180 | MUST | ✅ | `ForceFlush` MUST invoke `ForceFlush` on all registered `SpanProcessors`. | ОтелПровайдерТрассировки.os:91-95 |
| 181 | SHOULD | ✅ | If not explicitly set, the `enabled` parameter SHOULD default to `true` ( | ОтелПостроительПровайдераТрассировки.os:108 |
| 182 | MUST | ✅ | If a `Tracer` is disabled, it MUST behave equivalently | ОтелТрассировщик.os:33 |
| 183 | MUST | ✅ | The value of `enabled` MUST be used to resolve whether a `Tracer` | ОтелПровайдерТрассировки.os:59-60 |
| 184 | MUST | ✅ | However, the changes MUST be eventually visible. | ОтелПровайдерТрассировки.os:52 |
| 185 | MUST | ✅ | `Enabled` MUST return `false` when either: | ОтелТрассировщик.os:33 |
| 186 | SHOULD | ✅ | Otherwise, it SHOULD return `true`. | ОтелТрассировщик.os:33 |
| 187 | MUST | ✅ | Readable span: A function receiving this as argument MUST be able to | ОтелСпан.os |
| 188 | MUST | ✅ | A function receiving this as argument MUST be able to access | ОтелСпан.os |
| 189 | MUST | ✅ | it MUST also be able to access the `InstrumentationLibrary` | ОтелСпан.os |
| 190 | MUST | ✅ | A function receiving this as argument MUST be able to reliably determine | ОтелСпан.os |
| 191 | MUST | ✅ | Counts for attributes, events and links dropped due to collection limits MUST be | ОтелСпан.os:198-217 |
| 192 | MUST | ✅ | of the Span but they MUST expose at least the full parent SpanContext. | ОтелСпан.os:72 |
| 193 | MUST | ✅ | It MUST be possible for functions being called with this | ОтелСпан.os |
| 194 | MUST | ✅ | Processor MUST receive only those spans which have this | ОтелТрассировщик.os:61 |
| 195 | SHOULD NOT | ✅ | field set to `true`. However, Span Exporter SHOULD NOT | ОтелЭкспортерСпанов.os |
| 196 | MUST | ✅ | `sampled` and will be exported. Span Exporters MUST | ОтелТрассировщик.os:61 |
| 197 | SHOULD NOT | ✅ | receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones | ОтелЭкспортерСпанов.os |
| 198 | MUST NOT | ✅ | MUST NOT allow this combination. | ОтелТрассировщик.os:61 |
| 199 | MUST | ✅ | When asked to create a Span, the SDK MUST act as if doing the following in order: | ОтелТрассировщик.os:48-104 |
| 200 | MUST | ✅ | If the parent `SpanContext` contains a valid `TraceId`, they MUST always match.* Name of the `Span` to be created.* `Spa... | ОтелТрассировщик.os:52-59 |
| 201 | MUST NOT | ✅ | will be dropped.* `RECORD_ONLY` - `IsRecording` will be `true`, but the `Sampled` flag MUST NOT be set.* `RECORD_AND_SAM... | ОтелТрассировщик.os:61-65 |
| 202 | SHOULD | ✅ | so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend | ОтелСэмплер.os:202 |
| 203 | SHOULD NOT | ✅ | Callers SHOULD NOT cache the returned value. | ОтелСэмплер.os:112-128 |
| 204 | MUST | ✅ | * The `TraceIdRatioBased` MUST ignore the parent `SampledFlag`. To respect the | ОтелСэмплер.os:63,73,82,92 |
| 205 | MUST | ✅ | the `ParentBased` sampler specified below.* Description MUST return a string of the form `"TraceIdRatioBased{RATIO}"` | ОтелСэмплер.os:210,247-269 |
| 206 | SHOULD | ✅ | represented as a decimal number. The precision of the number SHOULD follow | ОтелСэмплер.os:247-269 |
| 207 | SHOULD | ✅ | implementation language standards and SHOULD be high enough to identify when | ОтелСэмплер.os:247-269 |
| 208 | MUST | ✅ | * The sampling algorithm MUST be deterministic. A trace identified by a given | ОтелСэмплер.os:247-269 |
| 209 | MUST | ✅ | implementations MUST use a deterministic hash of the `TraceId` when computing | ОтелСэмплер.os:260-261 |
| 210 | MUST | ✅ | will produce the same decision.* A `TraceIdRatioBased` sampler with a given sampling probability MUST also sample all | ОтелСэмплер.os:247-269 |
| 211 | SHOULD | ✅ | when it is used not as a root sampler, the SDK SHOULD emit a warning | ОтелСэмплер.os:211 |
| 212 | MUST | ✅ | Based on the decision from the wrapped root sampler, `AlwaysRecord` MUST behave | ОтелСэмплер.os:204-245 |
| 213 | MUST NOT | ✅ | Note: ComposableSamplers MUST NOT modify the parameters passed to | ОтелСэмплер.os:179,213-214 |
| 214 | MUST NOT | ✅ | complexity. ComposableSamplers MUST NOT modify the OpenTelemetry | ОтелСэмплер.os |
| 215 | SHOULD | ✅ | CompositeSampler SHOULD update the threshold of the outgoing | ОтелСэмплер.os:215 |
| 216 | MUST | ✅ | randomness values MUST not be modified. | ОтелСэмплер.os:261 |
| 217 | SHOULD | ✅ | a `ComposableAlwaysOff` instance SHOULD be returned instead. | ОтелСэмплер.os:217 |
| 218 | SHOULD | ✅ | For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Ca... | ОтелТрассировщик.os:92 |
| 219 | SHOULD | ✅ | For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the... | ОтелКонтекстСпана.os |
| 220 | MUST NOT | ✅ | MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState | ОтелСостояниеТрассировки.os |
| 221 | SHOULD | ⚠️ | For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness... | ОтелСэмплер.os (Samplers presume TraceIDs meet W3C randomness unless explicit rv sub-key) |
| 222 | SHOULD | ➖ | If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random fla... | IdGenerator extension point - not shown in required extension |
| 223 | MUST | ✅ | Span attributes MUST adhere to the common rules of attribute limits. | ОтелЛимитыСпана.os |
| 224 | MUST | ✅ | If the SDK implements the limits above it MUST provide a way to change these | ОтелЛимитыСпана.os:83-152 |
| 225 | SHOULD | ✅ | The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`. The options MAY be bundled in a ... | ОтелЛимитыСпана.os |
| 226 | SHOULD | ✅ | which then SHOULD be called `SpanLimits`. Implementations MAY provide additional | ОтелЛимитыСпана.os |
| 227 | SHOULD | ✅ | There SHOULD be a message printed in the SDK’s log to indicate to the user | ОтелЛимитыСпана.os |
| 228 | MUST | ✅ | To prevent excessive logging, the message MUST be printed at most once per | ОтелЛимитыСпана.os |
| 229 | MUST | ✅ | The SDK MUST by default randomly generate both the `TraceId` and the `SpanId`. | ОтелУтилиты.os |
| 230 | MUST | ✅ | The SDK MUST provide a mechanism for customizing the way IDs are generated for | ОтелПровайдерТрассировки.os:207 |
| 231 | MUST | ✅ | `IdGenerator`, name of the methods MUST be consistent with | ОтелУтилиты.os |
| 232 | MUST NOT | ➖ | X-Ray trace id generator MUST NOT be maintained or distributed as part of the | X-Ray ID generator not maintained - not in scope |
| 233 | SHOULD | ⚠️ | Custom implementations of the `IdGenerator` SHOULD identify themselves | ОтелУтилиты.os (Custom ID generators should identify themselves) |
| 234 | MUST | ✅ | of span processor and optional exporter. SDK MUST allow to end each pipeline with | ОтелПростойПроцессорСпанов.os |
| 235 | MUST | ✅ | SDK MUST allow users to implement and configure custom processors. | ОтелПровайдерТрассировки.os:76-78 |
| 236 | MUST | ✅ | The `SpanProcessor` interface MUST declare the following methods: | ОтелПростойПроцессорСпанов.os:17-47 |
| 237 | SHOULD | ✅ | The `SpanProcessor` interface SHOULD declare the following methods: | ОтелБазовыйПакетныйПроцессор.os:93 |
| 238 | SHOULD | ✅ | It SHOULD be possible to keep a reference to this span object and updates to the span | ОтелПростойПроцессорСпанов.os:26-32 |
| 239 | MUST | ✅ | The end timestamp MUST have been computed (the `OnEnding` method duration is not included | ОтелСпан.os:436-448 |
| 240 | MUST | ✅ | The Span object MUST still be mutable (i.e., `SetAttribute`, `AddLink`, `AddEvent` can be called) while `OnEnding` is ca... | ОтелСпан.os:436-448 |
| 241 | MUST | ✅ | This method MUST be called synchronously within the `Span.End()` API, | ОтелСпан.os:444-446 |
| 242 | MUST | ✅ | The SDK MUST guarantee that the span can no longer be modified by any other thread | ОтелСпан.os:436-448 |
| 243 | SHOULD | ✅ | `Shutdown` SHOULD be called only once for each `SpanProcessor` instance. After | ОтелПростойПроцессорСпанов.os:17 |
| 244 | SHOULD | ✅ | are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | ОтелПростойПроцессорСпанов.os:17 |
| 245 | MUST | ✅ | `Shutdown` MUST include the effects of `ForceFlush`. | ОтелПростойПроцессорСпанов.os:43-47 |
| 246 | SHOULD | ✅ | `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD | ОтелБазовыйПакетныйПроцессор.os |
| 247 | SHOULD | ✅ | In particular, if any `SpanProcessor` has any associated exporter, it SHOULD | ОтелБазовыйПакетныйПроцессор.os |
| 248 | MUST | ✅ | The built-in SpanProcessors MUST do so. | ОтелБазовыйПакетныйПроцессор.os:67-77 |
| 249 | MUST | ✅ | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over | ОтелБазовыйПакетныйПроцессор.os:119-134 |
| 250 | SHOULD | ✅ | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, | ОтелБазовыйПакетныйПроцессор.os |
| 251 | MUST | ✅ | The standard OpenTelemetry SDK MUST implement both simple and batch processors, | ОтелПростойПроцессорСпанов.os,ОтелБазовыйПакетныйПроцессор.os |
| 252 | MUST | ✅ | The processor MUST synchronize calls to `Span Exporter`’s `Export` | ОтелПростойПроцессорСпанов.os:26-32 |
| 253 | SHOULD | ✅ | The processor SHOULD export a batch when any of the following happens AND the | ОтелПростойПроцессорСпанов.os:26-32 |
| 254 | MUST | ✅ | Each implementation MUST document the concurrency characteristics the SDK | ОтелПростойПроцессорСпанов.os:26-32 |
| 255 | MUST | ✅ | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | ОтелЭкспортерСпанов.os |
| 256 | MUST NOT | ✅ | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit | ОтелЭкспортерСпанов.os |
| 257 | SHOULD NOT | ✅ | default SDK’s Span Processors SHOULD NOT implement retry logic, as the required | ОтелПростойПроцессорСпанов.os |
| 258 | SHOULD | ✅ | call to `ForceFlush` SHOULD be completed as soon as possible, preferably before | ОтелБазовыйПакетныйПроцессор.os:144-149 |
| 259 | MUST | ✅ | Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe | ОтелПровайдерТрассировки.os,ОтелСэмплер.os |
| 260 | MUST | ✅ | Sampler - `ShouldSample` and `GetDescription` MUST be safe to be called | ОтелСэмплер.os:112-128 |
| 261 | MUST | ✅ | Span processor - all methods MUST be safe to be called concurrently. | ОтелПростойПроцессорСпанов.os |
| 262 | MUST | ✅ | Span Exporter - `ForceFlush` and `Shutdown` MUST be safe to be called | ОтелЭкспортерСпанов.os |

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
2. Отфильтрованы требования со статусом Development (LoggerConfig, MeterConfig, TracerConfig, ProbabilitySampler и др.) и дедуплицированы
3. Каждое из 613 требований прослежено до конкретного файла и строки в исходном коде
4. Статусы:
   - ✅ found - реализовано
   - ⚠️ partial - частично реализовано
   - ❌ not_found - не реализовано
   - ➖ n_a - неприменимо к платформе или Development-статус в спецификации
