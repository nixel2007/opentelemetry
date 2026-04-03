# Анализ соответствия спецификации OpenTelemetry v1.55.0

> **Версия спецификации**: [v1.55.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-04-03
> **Методология**: spec-first - извлечены все MUST/SHOULD требования из спецификации, затем каждое прослежено до кода

## Сводка (Stable)

Учитываются только требования из стабильных разделов спецификации с универсальной областью применения.

| Показатель | Значение |
|---|---|
| Всего требований | 645 |
| Stable (универсальные) | 548 |
| Conditional (B3, Prometheus и др.) | 8 |
| Development (нестабильные) | 89 |
| Deprecated | 0 |
| Применимых Stable (без N/A) | 545 |
| ✅ Реализовано | 428 (78.5%) |
| ⚠️ Частично | 100 (18.3%) |
| ❌ Не реализовано | 17 (3.1%) |
| N/A (неприменимо) | 3 |
| **MUST/MUST NOT** | 297/359 (82.7%) |
| **SHOULD/SHOULD NOT** | 129/180 (71.7%) |

## Соответствие по разделам (Stable)

| Раздел | Всего | ✅ | ⚠️ | ❌ | N/A | % | Cond | Dev |
|---|---|---|---|---|---|---|---|---|
| Context | 15 | 12 | 2 | 1 | 0 | 80.0% | 0 | 0 |
| Baggage Api | 16 | 16 | 0 | 0 | 0 | 100.0% | 0 | 0 |
| Resource Sdk | 15 | 8 | 0 | 7 | 0 | 53.3% | 0 | 0 |
| Trace Api | 133 | 126 | 0 | 0 | 2 | 100.0% | 0 | 5 |
| Trace Sdk | 49 | 41 | 0 | 0 | 0 | 100.0% | 0 | 8 |
| Logs Api | 21 | 0 | 18 | 0 | 1 | 0.0% | 0 | 2 |
| Logs Sdk | 110 | 0 | 79 | 0 | 0 | 0.0% | 0 | 31 |
| Metrics Api | 53 | 53 | 0 | 0 | 0 | 100.0% | 0 | 0 |
| Metrics Sdk | 198 | 155 | 0 | 0 | 0 | 100.0% | 0 | 43 |
| Otlp Exporter | 0 | 0 | 0 | 0 | 0 | N/A | 0 | 0 |
| Propagators | 35 | 17 | 1 | 9 | 0 | 63.0% | 8 | 0 |
| Env Vars | 0 | 0 | 0 | 0 | 0 | N/A | 0 | 0 |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Context]** [MUST] The API MUST accept the following parameter: The key name. (Implemented as module-level string constants КлючСпан and КлючBaggage, not explicit Create (`src/Ядро/Модули/ОтелКонтекст.os:312-313`)
- ⚠️ **[Context]** [MUST] The API MUST return an opaque object representing the newly created key. (Keys are opaque strings; no explicit key object type). (`src/Ядро/Модули/ОтелКонтекст.os:312-313`)
- ❌ **[Resource Sdk]** [MUST] Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments MUST be implemented as packages separ
- ❌ **[Resource Sdk]** [MUST] Resource detector packages MUST provide a method that returns a resource. (No resource detector packages found).
- ❌ **[Resource Sdk]** [MUST] failure to detect any resource information MUST NOT be considered an error. (No external detection mechanism).
- ❌ **[Resource Sdk]** [MUST] Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL se
- ❌ **[Resource Sdk]** [MUST] If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error. (No detector composition framework).
- ⚠️ **[Logs Api]** [MUST] LoggerProvider MUST provide the following functions: Get a Logger
- ⚠️ **[Logs Api]** [MUST] This API MUST accept the following instrumentation scope parameters (name, version, schema_url, attributes)
- ⚠️ **[Logs Api]** [MUST] This API MUST be structured to accept a variable number of attributes, including none
- ⚠️ **[Logs Api]** [MUST] Logger MUST provide a function to: Emit a LogRecord
- ⚠️ **[Logs Api]** [MUST] The API MUST accept the following parameters (Timestamp, ObservedTimestamp, Context, SeverityNumber, SeverityText, Body, Attributes, EventName)
- ⚠️ **[Logs Api]** [MUST] Context MUST use current Context when unspecified
- ⚠️ **[Logs Api]** [MUST] Enabled API MUST return a language idiomatic boolean type
- ⚠️ **[Logs Api]** [MUST] For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it
- ⚠️ **[Logs Api]** [MUST] For each required parameter, the API MUST be structured to obligate a user to provide it
- ⚠️ **[Logs Api]** [MUST NOT] API MUST NOT obligate a user to provide optional parameters
- ⚠️ **[Logs Api]** [MUST] LoggerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default
- ⚠️ **[Logs Api]** [MUST] Logger - all methods MUST be documented that implementations need to be safe for concurrent use by default
- ⚠️ **[Logs Sdk]** [MUST] All language implementations of OpenTelemetry MUST provide an SDK
- ⚠️ **[Logs Sdk]** [MUST] LoggerProvider MUST provide a way to allow a Resource to be specified
- ⚠️ **[Logs Sdk]** [MUST] Configuration MUST be owned by the LoggerProvider
- ⚠️ **[Logs Sdk]** [MUST] Updated configuration MUST also apply to all already returned Loggers
- ⚠️ **[Logs Sdk]** [MUST NOT] It MUST NOT matter whether Logger was obtained before or after configuration change
- ⚠️ **[Logs Sdk]** [MUST] ForceFlush MUST invoke ForceFlush on all registered LogRecordProcessors
- ⚠️ **[Logs Sdk]** [MUST] Built-in LogRecordProcessors MUST do so
- ⚠️ **[Logs Sdk]** [MUST] LogRecordProcessor MUST prioritize honoring timeout
- ⚠️ **[Logs Sdk]** [MUST] Function MUST be able to access all information added to LogRecord
- ⚠️ **[Logs Sdk]** [MUST] Function MUST also be able to access InstrumentationScope and Resource
- ⚠️ **[Logs Sdk]** [MUST] Trace context fields MUST be populated from resolved Context at emit time
- ⚠️ **[Logs Sdk]** [MUST] Counts for attributes due to collection limits MUST be available for exporters
- ⚠️ **[Logs Sdk]** [MUST] Function MUST additionally be able to modify LogRecord information
- ⚠️ **[Logs Sdk]** [MUST] LogRecord attributes MUST adhere to common rules of attribute limits
- ⚠️ **[Logs Sdk]** [MUST] If SDK implements attribute limits it MUST provide a way to change these limits
- ⚠️ **[Logs Sdk]** [MUST] Message MUST be printed at most once per LogRecord
- ⚠️ **[Logs Sdk]** [MUST] SDK MUST allow each pipeline to end with an individual exporter
- ⚠️ **[Logs Sdk]** [MUST] SDK MUST allow users to implement and configure custom processors
- ⚠️ **[Logs Sdk]** [MUST] logRecord mutations MUST be visible in next registered processors
- ⚠️ **[Logs Sdk]** [MUST] Enabled MUST return false when no LogRecordProcessors registered
- ⚠️ **[Logs Sdk]** [MUST NOT] Any modifications to parameters inside Enabled MUST NOT be propagated to caller
- ⚠️ **[Logs Sdk]** [MUST] Shutdown MUST include the effects of ForceFlush
- ⚠️ **[Logs Sdk]** [MUST] ForceFlush MUST invoke ForceFlush on all registered LogRecordProcessors
- ⚠️ **[Logs Sdk]** [MUST] Built-in LogRecordProcessors MUST do so
- ⚠️ **[Logs Sdk]** [MUST] LogRecordProcessor MUST prioritize honoring timeout
- ⚠️ **[Logs Sdk]** [MUST] Standard SDK MUST implement both simple and batch processors
- ⚠️ **[Logs Sdk]** [MUST] Processor MUST synchronize calls to LogRecordExporter Export
- ⚠️ **[Logs Sdk]** [MUST] LogRecordExporter MUST support the following functions
- ⚠️ **[Logs Sdk]** [MUST NOT] Export MUST NOT block indefinitely
- ⚠️ **[Logs Sdk]** [MUST] Export MUST have reasonable upper limit after which call times out
- ⚠️ **[Logs Sdk]** [MUST] ForceFlush MUST invoke ForceFlush on all registered LogRecordProcessors

### SHOULD/SHOULD NOT несоответствия

- ❌ **[Context]** [SHOULD] Multiple calls to `CreateKey` with the same name SHOULD NOT return the same value unless language constraints dictate otherwise. (No explicit CreateKe
- ❌ **[Resource Sdk]** [SHOULD] an error that occurs during an attempt to detect resource information SHOULD be considered an error. (Basic error handling in ЗаполнитьИнформациюОХост
- ❌ **[Resource Sdk]** [SHOULD] Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes. (Schema URL support exists but no detector f
- ⚠️ **[Logs Api]** [SHOULD] API SHOULD provide a way to set/register and access a global default LoggerProvider
- ⚠️ **[Logs Api]** [SHOULD] Logger SHOULD provide functions to: Report if Logger is Enabled
- ⚠️ **[Logs Api]** [SHOULD] Context parameter SHOULD be optional when implicit Context is supported
- ⚠️ **[Logs Api]** [SHOULD] Logger SHOULD provide Enabled API
- ⚠️ **[Logs Api]** [SHOULD] Enabled API SHOULD accept Context, SeverityNumber, EventName parameters
- ⚠️ **[Logs Api]** [SHOULD] Instrumentation authors need to call Enabled API each time to ensure up-to-date response
- ⚠️ **[Logs Sdk]** [SHOULD] If Resource is specified, it SHOULD be associated with all LogRecords produced
- ⚠️ **[Logs Sdk]** [SHOULD] SDK SHOULD allow the creation of multiple independent LoggerProviders
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide way to let caller know if succeeded/failed/timed out
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD return ERROR status if error condition
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD return NO ERROR status if no error condition
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within timeout
- ⚠️ **[Logs Sdk]** [SHOULD] Tasks for LogRecords SHOULD be completed as soon as possible
- ⚠️ **[Logs Sdk]** [SHOULD] LogRecordProcessor SHOULD try to call exporter Export with all LogRecords
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide way to let caller know if succeeded/failed/timed out
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within timeout
- ⚠️ **[Logs Sdk]** [SHOULD] Options SHOULD be called LogRecordLimits
- ⚠️ **[Logs Sdk]** [SHOULD] Message SHOULD be printed to indicate attribute was discarded
- ⚠️ **[Logs Sdk]** [SHOULD NOT] Method SHOULD NOT block or throw exceptions
- ⚠️ **[Logs Sdk]** [SHOULD] Implementations SHOULD recommended users to use clone for concurrent processing
- ⚠️ **[Logs Sdk]** [SHOULD] Otherwise, Enabled SHOULD return true
- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD be called only once for each LogRecordProcessor instance
- ⚠️ **[Logs Sdk]** [SHOULD] SDKs SHOULD ignore subsequent calls gracefully
- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD provide way to let caller know if succeeded/failed/timed out
- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD complete or abort within timeout
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide way to let caller know if succeeded/failed/timed out
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD return ERROR status if error condition
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD return NO ERROR status if no error condition
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within timeout
- ⚠️ **[Logs Sdk]** [SHOULD] Tasks for LogRecords SHOULD be completed as soon as possible
- ⚠️ **[Logs Sdk]** [SHOULD] LogRecordProcessor SHOULD try to call exporter Export with all LogRecords
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide way to let caller know if succeeded/failed/timed out
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within timeout
- ⚠️ **[Logs Sdk]** [SHOULD] Other scenarios SHOULD be first considered for out-of-process implementation
- ⚠️ **[Logs Sdk]** [SHOULD NOT] Default SDK LogRecordProcessors SHOULD NOT implement retry logic
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide way to let caller know if succeeded/failed/timed out
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD return ERROR status if error condition
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD return NO ERROR status if no error condition
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within timeout
- ⚠️ **[Logs Sdk]** [SHOULD] Tasks for LogRecords SHOULD be completed as soon as possible
- ⚠️ **[Logs Sdk]** [SHOULD] LogRecordProcessor SHOULD try to call exporter Export with all LogRecords
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide way to let caller know if succeeded/failed/timed out
- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within timeout
- ⚠️ **[Logs Sdk]** [SHOULD] SDKs SHOULD return a valid no-op Logger for these calls
- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD provide way to let caller know if succeeded/failed/timed out
- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD complete or abort within timeout
- ❌ **[Propagators]** [SHOULD] It SHOULD return them in the same order as they appear in the carrier. (N/A - GetAll not implemented).

## Детальный анализ по разделам (Stable)

### Context

#### Overview

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | MUST | ✅ | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the... | `src/Ядро/Модули/ОтелКонтекст.os:1-35` |
| 2 | MUST | ✅ | OpenTelemetry MUST provide its own `Context` implementation. | `src/Ядро/Модули/ОтелКонтекст.os:29-35` |
| 3 | MUST | ✅ | Context immutability is enforced by copy semantics in УстановитьЗначение (creates new context before modifying). | `src/Ядро/Модули/ОтелКонтекст.os:148-152` |

#### Create a key

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 4 | MUST | ⚠️ | The API MUST accept the following parameter: The key name. (Implemented as module-level string constants КлючСпан and... | `src/Ядро/Модули/ОтелКонтекст.os:312-313` |
| 5 | SHOULD | ❌ | Multiple calls to `CreateKey` with the same name SHOULD NOT return the same value unless language constraints dictate... | `-` |
| 6 | MUST | ⚠️ | The API MUST return an opaque object representing the newly created key. (Keys are opaque strings; no explicit key ob... | `src/Ядро/Модули/ОтелКонтекст.os:312-313` |

#### Get value

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 7 | MUST | ✅ | The API MUST accept the following parameters: The `Context`. The key. Returns the value in the `Context` for the spec... | `src/Ядро/Модули/ОтелКонтекст.os:45-48` |
| 8 | MUST | ✅ | Функция Получить(Ключ) accepts Context implicitly (current) and key parameter. | `src/Ядро/Модули/ОтелКонтекст.os:45-48` |

#### Set value

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 9 | MUST | ✅ | The API MUST accept the following parameters: The `Context`. The key. The value to be set. УстановитьЗначение(Ключ, З... | `src/Ядро/Модули/ОтелКонтекст.os:147-152` |
| 10 | MUST | ✅ | The API MUST return a new `Context` containing the new value. Creates НовыйКонтекст via СкопироватьТекущий(), then re... | `src/Ядро/Модули/ОтелКонтекст.os:150` |

#### Optional Global operations

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 11 | MUST | ✅ | These operations are implemented for implicit Context handling (GetCurrentContext, SetCurrentContext). | `src/Ядро/Модули/ОтелКонтекст.os:29-35,56-68` |

#### Get current Context

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 12 | MUST | ✅ | The API MUST return the `Context` associated with the caller's current execution unit. Функция Текущий() returns Стек... | `src/Ядро/Модули/ОтелКонтекст.os:29-35` |

#### Attach Context

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 13 | MUST | ✅ | The API MUST accept the following parameters: The `Context`. УстановитьЗначение accepts context value. | `src/Ядро/Модули/ОтелКонтекст.os:147-152` |
| 14 | MUST | ✅ | The API MUST return a value that can be used as a `Token` to restore the previous `Context`. Returns ОтелОбласть obje... | `src/Ядро/Классы/ОтелОбласть.os:22-27` |

#### Detach Context

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 15 | MUST | ✅ | The API MUST accept the following parameters: A `Token` that was returned by a previous call to attach a `Context`. О... | `src/Ядро/Классы/ОтелОбласть.os:22-27` |

### Baggage Api

#### Overview

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | MUST | ✅ | Each name in `Baggage` MUST be associated with exactly one value. Stored in фиксированноеСоответствие Значения. | `src/Ядро/Классы/ОтелBaggage.os:152-163` |
| 2 | SHOULD | ✅ | Language API SHOULD NOT restrict which strings are used as baggage names. Accepts any Строка as key. | `src/Ядро/Классы/ОтелBaggage.os:30-40` |
| 3 | MUST | ✅ | Language API MUST accept any valid UTF-8 string as baggage value. Accepts any Строка value. | `src/Ядро/Классы/ОтелBaggage.os:152-163` |
| 4 | MUST | ✅ | Language API MUST treat both baggage names and values as case sensitive. Keys and values stored as-is without normali... | `src/Ядро/Классы/ОтелBaggage.os:38-40` |
| 5 | MUST | ✅ | The Baggage API MUST be fully functional in the absence of an installed SDK. Baggage class is standalone. | `src/Ядро/Классы/ОтелBaggage.os:1-166` |
| 6 | MUST | ✅ | The `Baggage` container MUST be immutable. Uses ФиксированноеСоответствие, all operations return new instances. | `src/Ядро/Классы/ОтелBaggage.os:68-86,94-96,103-105` |

#### Get All Values

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 7 | MUST | ✅ | The order of name/value pairs MUST NOT be significant. Функция ПолучитьВсе() returns collection with no order guarant... | `src/Ядро/Классы/ОтелBaggage.os:103-105` |

#### Set Value

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 8 | MUST | ✅ | The Baggage API MUST provide a function which takes a name, and a value as input. Returns a new `Baggage` that contai... | `src/Ядро/Классы/ОтелPostroitelBaggage.os:23-27` |

#### Remove Value

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 9 | MUST | ✅ | The Baggage API MUST provide a function which takes a name as input. Returns a new `Baggage` which no longer contains... | `src/Ядро/Классы/ОтелBaggage.os:82-86` |

#### Context Interaction

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 10 | MUST | ✅ | If an implementation of this API does not operate directly on the `Context`, it MUST provide the following functional... | `src/Ядро/Модули/ОтелКонтекст.os:89-102` |
| 11 | SHOULD | ✅ | API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. КлючBaggage is module-lev... | `src/Ядро/Модули/ОтелКонтекст.os:66-68` |
| 12 | SHOULD | ✅ | If the language has support for implicitly propagated `Context`, the API SHOULD also provide the following functional... | `src/Ядро/Классы/ОтелBaggage.os:20-28` |
| 13 | SHOULD | ✅ | This functionality SHOULD be fully implemented in the API when possible. СделатьТекущим() wraps ОтелКонтекст.СделатьB... | `src/Ядро/Классы/ОтелBaggage.os:26-28` |

#### Clear Baggage in the Context

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 14 | MUST | ✅ | The Baggage API MUST provide a way to remove all baggage entries from a context. Функция Очистить() returns new empty... | `src/Ядро/Классы/ОтелBaggage.os:94-96` |

#### Propagation

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 15 | MUST | ✅ | The API layer or an extension package MUST include the following `Propagator`s: A `TextMapPropagator` implementing th... | `src/Пропагация/Модули/ОтелW3CBaggageПропагатор.os:1-140` |

#### Conflict Resolution

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 16 | MUST | ✅ | If a new name/value pair is added and its name is the same as an existing name, then the new pair MUST take precedenc... | `src/Ядро/Классы/ОтелPostroitelBaggage.os:23-27` |

### Resource Sdk

#### Resource SDK

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | MUST | ✅ | The SDK MUST allow for creation of `Resources` and for associating them with telemetry. Функция Построить() creates О... | `src/Ядро/Классы/ОтелПостроительРесурса.os:61-67` |
| 2 | MUST | ✅ | All `Span`s produced by any `Tracer` from the provider MUST be associated with this `Resource`. Resource is associate... | `src/Ядро/Классы/ОтелРесурс.os:44-65` |

#### SDK-provided resource attributes

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 3 | MUST | ✅ | The SDK MUST provide access to a Resource with at least the attributes listed at Semantic Attributes. ЗаполнитьАтрибу... | `src/Ядро/Классы/ОтелРесурс.os:99-113` |
| 4 | MUST | ✅ | This resource MUST be associated with a `TracerProvider` or `MeterProvider` if another resource was not explicitly sp... | `src/Ядро/Классы/ОтелРесурс.os:99-102` |

#### Create

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 5 | MUST | ✅ | The interface MUST provide a way to create a new resource, from `Attributes`. Функция Установить(Ключ, Значение). | `src/Ядро/Классы/ОтелПостроительРесурса.os:19-22` |
| 6 | MUST | ✅ | The interface MUST provide a way for an old resource and an updating resource to be merged into a new resource. Функц... | `src/Ядро/Классы/ОтелРесурс.os:44-65` |
| 7 | MUST | ✅ | The resulting resource MUST have all attributes that are on any of the two input resources. Слить copies attributes f... | `src/Ядро/Классы/ОтелРесурс.os:58-64` |
| 8 | MUST | ✅ | If a key exists on both the old and updating resource, the value of the updating resource MUST be picked. ДругойРесур... | `src/Ядро/Классы/ОтелРесурс.os:61-62` |

#### Detecting resource information from the environment

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 9 | MUST | ❌ | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments MUST... | `-` |
| 10 | MUST | ❌ | Resource detector packages MUST provide a method that returns a resource. (No resource detector packages found). | `-` |
| 11 | MUST | ❌ | failure to detect any resource information MUST NOT be considered an error. (No external detection mechanism). | `-` |
| 12 | SHOULD | ❌ | an error that occurs during an attempt to detect resource information SHOULD be considered an error. (Basic error han... | `-` |
| 13 | MUST | ❌ | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that... | `-` |
| 14 | SHOULD | ❌ | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes. (Schema URL... | `-` |
| 15 | MUST | ❌ | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error. (No dete... | `-` |

### Trace Api

#### Timestamp

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | MUST | ✅ | The minimal precision is milliseconds; The maximal precision is nanoseconds - timestamps stored as nanosecond strings... | `src/Трассировка/Классы/ОтелСпан.os:563` |
| 2 | MUST | ✅ | A duration is the elapsed time between two events; minimal precision milliseconds, maximal nanoseconds - supported vi... | `src/Трассировка/Классы/ОтелСпан.os:563` |

#### TracerProvider operations

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 3 | MUST | ✅ | TracerProvider MUST provide Get a Tracer function | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52-68` |
| 4 | MUST | ✅ | This API MUST accept name (required) parameter | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52-56` |
| 5 | MUST | ✅ | MUST accept version (optional) parameter | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52-56` |
| 6 | MUST | ✅ | MUST accept schema_url (optional) parameter | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52-56` |
| 7 | MUST | ✅ | MUST accept attributes (optional) parameter | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52-56` |
| 8 | MUST | ✅ | invalid name (null or empty) MUST return working Tracer not null | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52-68` |
| 9 | MUST | ✅ | Implementations MUST NOT require repeatedly obtaining Tracer with same identity - caching at line 63-66 | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:63-66` |
| 10 | SHOULD | ✅ | API SHOULD provide way to set/register access global default TracerProvider | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:28-37` |
| 11 | SHOULD | ✅ | Implementations SHOULD allow creating arbitrary number of TracerProvider instances | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:19-20` |

#### Context Interaction

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 12 | MUST | ✅ | API MUST provide extract Span from Context instance | `src/Ядро/Модули/ОтелКонтекст.os` |
| 13 | MUST | ✅ | API MUST provide combine Span with Context creating new Context | `src/Ядро/Модули/ОтелКонтекст.os` |
| 14 | SHOULD | ✅ | API SHOULD provide get currently active span from implicit context | `src/Трассировка/Классы/ОтелСпан.os:387-388` |
| 15 | SHOULD | ✅ | API SHOULD provide set active span into new implicit context | `src/Трассировка/Классы/ОтелСпан.os:387-388` |
| 16 | SHOULD | ✅ | Functionality SHOULD be fully implemented in API when possible | `src/Ядро/Модули/ОтелКонтекст.os` |

#### SpanContext

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 17 | MUST | ✅ | API MUST implement methods to create SpanContext | `src/Трассировка/Классы/ОтелКонтекстСпана.os:124-142` |
| 18 | SHOULD | ✅ | These methods SHOULD be only way to create SpanContext | `src/Трассировка/Классы/ОтелКонтекстСпана.os:124-142` |
| 19 | MUST | ✅ | This functionality MUST be fully implemented in API | `src/Трассировка/Классы/ОтелКонтекстСпана.os:124-142` |
| 20 | SHOULD | ✅ | SHOULD NOT be overridable | `src/Трассировка/Классы/ОтелКонтекстСпана.os:124-142` |

#### Retrieving the TraceId and SpanId

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 21 | MUST | ✅ | API MUST allow retrieving TraceId and SpanId in following forms | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23-34` |
| 22 | MUST | ✅ | Hex TraceId result MUST be 32-hex-character lowercase string | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23-24` |
| 23 | MUST | ✅ | Hex SpanId result MUST be 16-hex-character lowercase string | `src/Трассировка/Классы/ОтелКонтекстСпана.os:32-33` |
| 24 | N_A | N/A | Binary TraceId representation - OneScript uses hex strings instead of byte arrays | `-` |
| 25 | N_A | N/A | Binary SpanId representation - OneScript uses hex strings instead of byte arrays | `-` |
| 26 | SHOULD | ✅ | API SHOULD NOT expose details about internal storage | `src/Трассировка/Классы/ОтелКонтекстСпана.os` |

#### IsValid

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 27 | MUST | ✅ | IsValid API returning boolean MUST be provided checking non-zero TraceID and SpanID | `src/Трассировка/Классы/ОтелКонтекстСпана.os:70-75` |

#### IsRemote

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 28 | MUST | ✅ | IsRemote API MUST be provided returning boolean | `src/Трассировка/Классы/ОтелКонтекстСпана.os:60-62` |
| 29 | MUST | ✅ | When extracted via Propagators, IsRemote MUST return true | `src/Трассировка/Классы/ОтелТрассировщик.os:122,152` |
| 30 | MUST | ✅ | For SpanContext of child spans, IsRemote MUST return false | `src/Трассировка/Классы/ОтелТрассировщик.os:125` |

#### TraceState

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 31 | MUST | ✅ | Tracing API MUST provide Get value for given key operation | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os` |
| 32 | MUST | ✅ | MUST provide Add new key/value pair operation | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os` |
| 33 | MUST | ✅ | MUST provide Update existing value for given key operation | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os` |
| 34 | MUST | ✅ | MUST provide Delete key/value pair operation | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os` |
| 35 | MUST | ✅ | Operations MUST follow W3C Trace Context specification rules | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os` |
| 36 | MUST | ✅ | All mutating operations MUST return new TraceState with modifications | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os` |
| 37 | MUST | ✅ | TraceState MUST at all times be valid per W3C specification | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os` |
| 38 | MUST | ✅ | Every mutating operation MUST validate input parameters | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os` |
| 39 | MUST | ✅ | If invalid value passed MUST NOT return TraceState with invalid data | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os` |
| 40 | MUST | ✅ | MUST follow general error handling guidelines | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os` |

#### Span

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 41 | MUST | ✅ | Span encapsulates the span name | `src/Трассировка/Классы/ОтелСпан.os:63-244` |
| 42 | MUST | ✅ | Span encapsulates immutable SpanContext | `src/Трассировка/Классы/ОтелСпан.os:72-74` |
| 43 | MUST | ✅ | Span encapsulates parent span in form of Span, SpanContext, null | `src/Трассировка/Классы/ОтелСпан.os:81-83` |
| 44 | MUST | ✅ | Span encapsulates SpanKind | `src/Трассировка/Классы/ОтелСпан.os:90-92` |
| 45 | MUST | ✅ | Span encapsulates start and end timestamps | `src/Трассировка/Классы/ОтелСпан.os:99-110` |
| 46 | MUST | ✅ | Span encapsulates Attributes | `src/Трассировка/Классы/ОтелСпан.os:126-128` |
| 47 | MUST | ✅ | Span encapsulates list of Links | `src/Трассировка/Классы/ОтелСпан.os:144-146` |
| 48 | MUST | ✅ | Span encapsulates list of timestamped Events | `src/Трассировка/Классы/ОтелСпан.os:135-137` |
| 49 | MUST | ✅ | Span encapsulates Status | `src/Трассировка/Классы/ОтелСпан.os:171-182` |
| 50 | SHOULD | ✅ | Span name SHOULD be most general string identifying interesting class of Spans | `src/Трассировка/Классы/ОтелСпан.os:63-64` |
| 51 | SHOULD | ✅ | Generality SHOULD be prioritized over human-readability | `src/Трассировка/Классы/ОтелСпан.os:63-64` |
| 52 | SHOULD | ✅ | Span start time SHOULD be set to current time on creation | `src/Трассировка/Классы/ОтелСпан.os:563` |
| 53 | SHOULD | ✅ | After Span created SHOULD be possible to change name, set Attributes, add Events, set Status | `src/Трассировка/Классы/ОтелСпан.os:239-272` |
| 54 | MUST | ✅ | Changes MUST NOT be changed after Span end time set | `src/Трассировка/Классы/ОтелСпан.os:240,256,286,403` |
| 55 | SHOULD | ✅ | Implementations SHOULD NOT provide access to Span attributes besides SpanContext | `src/Трассировка/Классы/ОтелСпан.os:72` |
| 56 | MUST | ✅ | All Spans MUST be created via Tracer | `src/Трассировка/Классы/ОтелСпан.os:535-594` |

#### Span Creation

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 57 | MUST | ✅ | MUST NOT be any API creating Span other than with Tracer | `src/Трассировка/Классы/ОтелТрассировщик.os:48-104` |
| 58 | MUST | ✅ | Span creation MUST NOT set newly created Span as active Span in current Context by default | `src/Трассировка/Классы/ОтелТрассировщик.os:48-104` |
| 59 | MUST | ✅ | API MUST accept span name (required parameter) | `src/Трассировка/Классы/ОтелПостроительСпана.os:33-49` |
| 60 | MUST | ✅ | API MUST accept parent Context or indication new Span should be root | `src/Трассировка/Классы/ОтелПостроительСпана.os:33-49` |
| 61 | MUST | ✅ | API MUST accept SpanKind parameter, defaulting to Internal | `src/Трассировка/Классы/ОтелПостроительСпана.os:60-62` |
| 62 | MUST | ✅ | API MUST accept Attributes parameter, assuming empty if not specified | `src/Трассировка/Классы/ОтелПостроительСпана.os:75-78` |
| 63 | MUST | ✅ | API MUST accept Links ordered sequence | `src/Трассировка/Классы/ОтелПостроительСпана.os:90-96` |
| 64 | MUST | ✅ | API MUST accept Start timestamp, defaulting to current time | `src/Трассировка/Классы/ОтелПостроительСпана.os:107-110` |
| 65 | MUST | ✅ | API documentation MUST state adding attributes at creation preferred | `src/Трассировка/Классы/ОтелПостроительСпана.os:75-78` |
| 66 | MUST | ✅ | Start timestamp SHOULD only be set when span creation already passed | `src/Трассировка/Классы/ОтелПостроительСпана.os:107-110` |
| 67 | MUST | ✅ | Implementations MUST provide option to create Span as root span | `src/Трассировка/Классы/ОтелТрассировщик.os:92` |
| 68 | MUST | ✅ | MUST generate new TraceId for each root span | `src/Трассировка/Классы/ОтелТрассировщик.os:92` |
| 69 | MUST | ✅ | For Span with parent, TraceId MUST be same as parent | `src/Трассировка/Классы/ОтелТрассировщик.os:52` |
| 70 | MUST | ✅ | Child span MUST inherit all TraceState values of parent by default | `src/Трассировка/Классы/ОтелТрассировщик.os:58` |
| 71 | MUST | ✅ | Any span created MUST also be ended | `src/Трассировка/Классы/ОтелСпан.os:436-448` |

#### Specifying links

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 72 | MUST | ✅ | During Span creation user MUST have ability to record links to other Spans | `src/Трассировка/Классы/ОтелПостроительСпана.os:90-96` |
| 73 | MUST | ✅ | Links added at Span creation may be considered by Samplers | `src/Трассировка/Классы/ОтелПостроительСпана.os:136-139` |

#### Get Context

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 74 | MUST | ✅ | Span interface MUST provide API returning SpanContext for given Span | `src/Трассировка/Классы/ОтелСпан.os:72-74` |
| 75 | MUST | ✅ | Returned value MUST be same for entire Span lifetime | `src/Трассировка/Классы/ОтелСпан.os:100-110` |
| 76 | MUST | ✅ | After Span ended, IsRecording SHOULD become non-recording, returning false | `src/Трассировка/Классы/ОтелСпан.os:226-228` |
| 77 | SHOULD | ✅ | IsRecording SHOULD NOT take any parameters | `src/Трассировка/Классы/ОтелСпан.os:226-228` |
| 78 | SHOULD | ✅ | IsRecording SHOULD be used avoid expensive computations of Span attributes | `src/Трассировка/Классы/ОтелСпан.os:300-304` |

#### Set Attributes

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 79 | MUST | ✅ | Span MUST have ability to set Attributes associated with it | `src/Трассировка/Классы/ОтелСпан.os:255-272` |
| 80 | MUST | ✅ | Span interface MUST provide API set single Attribute (SetAttribute) | `src/Трассировка/Классы/ОтелСпан.os:255-272` |
| 81 | SHOULD | ✅ | Setting attribute with same key as existing SHOULD overwrite existing value | `src/Трассировка/Классы/ОтелСпан.os:320-321` |
| 82 | MUST | ✅ | API documentation MUST state adding attributes at creation preferred | `src/Трассировка/Классы/ОтелПостроительСпана.os:75-78` |

#### Add Link

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 83 | MUST | ✅ | Span MUST have ability to add Links associated after creation | `src/Трассировка/Классы/ОтелСпан.os:351-368` |

#### Set Status

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 84 | MUST | ✅ | Span interface MUST provide API set Status (SetStatus) | `src/Трассировка/Классы/ОтелСпан.os:402-425` |
| 85 | MUST | ✅ | Status defined by StatusCode: Unset | `src/Трассировка/Классы/ОтелКодСтатуса.os` |
| 86 | MUST | ✅ | Status defined by StatusCode: Ok | `src/Трассировка/Классы/ОтелКодСтатуса.os` |
| 87 | MUST | ✅ | Status defined by StatusCode: Error | `src/Трассировка/Классы/ОтелКодСтатуса.os` |
| 88 | MUST | ✅ | Description MUST only be used with Error StatusCode | `src/Трассировка/Классы/ОтелСпан.os:418-422` |
| 89 | MUST | ✅ | Description MUST be IGNORED for StatusCode Ok & Unset | `src/Трассировка/Классы/ОтелСпан.os:386` |
| 90 | MUST | ✅ | Status ordering enforced: Ok > Error > Unset | `src/Трассировка/Классы/ОтелСпан.os:408-415` |
| 91 | MUST | ✅ | Setting Status with Ok overrides prior/future Error or Unset | `src/Трассировка/Классы/ОтелСпан.os:408-415` |
| 92 | SHOULD | ✅ | Status code SHOULD remain unset except documented circumstances | `src/Трассировка/Классы/ОтелСпан.os:388-401` |
| 93 | SHOULD | ✅ | Attempt set Unset SHOULD be ignored | `src/Трассировка/Классы/ОтелСпан.os:389` |
| 94 | SHOULD | ✅ | When status set Error, Description SHOULD be documented | `src/Трассировка/Классы/ОтелСпан.os:391-394` |
| 95 | SHOULD | ✅ | When status set Ok, SHOULD be final, further attempts ignored | `src/Трассировка/Классы/ОтелСпан.os:400-401` |

#### UpdateName

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 96 | MUST | ✅ | UpdateName allows updating Span name | `src/Трассировка/Классы/ОтелСпан.os:239-244` |
| 97 | MUST | ✅ | Required parameter: new span name | `src/Трассировка/Классы/ОтелСпан.os:239-244` |
| 98 | MUST | ✅ | UpdateName MUST NOT work after Span end time set | `src/Трассировка/Классы/ОтелСпан.os:240` |

#### Record Exception

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 99 | SHOULD | ✅ | Languages SHOULD provide RecordException method (ЗаписатьИсключение) | `src/Трассировка/Классы/ОтелСпан.os:307-339` |
| 100 | MUST | ✅ | RecordException MUST record exception as Event with conventions | `src/Трассировка/Классы/ОтелСпан.os:307-339` |
| 101 | MUST | ✅ | RecordException MUST follow exception conventions (type, message, stacktrace) | `src/Трассировка/Классы/ОтелСпан.os:313-328` |
| 102 | SHOULD | ✅ | Minimum required argument SHOULD be only exception object | `src/Трассировка/Классы/ОтелСпан.os:307-339` |
| 103 | MUST | ✅ | MUST accept optional parameter provide additional event attributes | `src/Трассировка/Классы/ОтелСпан.os:330-334` |

#### Span lifetime

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 104 | MUST | ✅ | Start and end time and Event timestamps MUST be recorded at time calling API | `src/Трассировка/Классы/ОтелСпан.os:563,438-442` |

#### Wrapping a SpanContext in a Span

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 105 | MUST | ✅ | API MUST provide operation wrapping SpanContext with Span | `src/Трассировка/Классы/ОтелНоопСпан.os` |
| 106 | SHOULD | ✅ | If new type required SHOULD NOT be exposed publicly | `src/Трассировка/Классы/ОтелНоопСпан.os:272-281` |
| 107 | SHOULD | ✅ | If type required publicly SHOULD be named NonRecordingSpan | `src/Трассировка/Классы/ОтелНоопСпан.os:272-281` |
| 108 | MUST | ✅ | GetContext MUST return wrapped SpanContext | `src/Трассировка/Классы/ОтелНоопСпан.os:29-31` |
| 109 | MUST | ✅ | IsRecording MUST return false signal not recording | `src/Трассировка/Классы/ОтелНоопСпан.os:155-157` |
| 110 | MUST | ✅ | Remaining Span functionality MUST be no-op operations | `src/Трассировка/Классы/ОтелНоопСпан.os:180-244` |
| 111 | MUST | ✅ | Exception: End not required/helpful end such Span | `src/Трассировка/Классы/ОтелНоопСпан.os:252-254` |
| 112 | MUST | ✅ | Functionality fully implemented API | `src/Трассировка/Классы/ОтелНоопСпан.os` |
| 113 | SHOULD | ✅ | SHOULD NOT be overridable | `src/Трассировка/Классы/ОтелНоопСпан.os` |

#### SpanKind

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 114 | MUST | ✅ | SERVER SpanKind available | `src/Трассировка/Модули/ОтелВидСпана.os` |
| 115 | MUST | ✅ | CLIENT SpanKind available | `src/Трассировка/Модули/ОтелВидСпана.os` |
| 116 | MUST | ✅ | PRODUCER SpanKind available | `src/Трассировка/Модули/ОтелВидСпана.os` |
| 117 | MUST | ✅ | CONSUMER SpanKind available | `src/Трассировка/Модули/ОтелВидСпана.os` |
| 118 | MUST | ✅ | INTERNAL SpanKind available (default) | `src/Трассировка/Модули/ОтелВидСпана.os` |
| 119 | SHOULD | ✅ | Callers SHOULD arrange single Span not serve multiple purposes | `src/Трассировка/Модули/ОтелВидСпана.os` |
| 120 | SHOULD | ✅ | Instrumentation create new Span before injecting SpanContext | `src/Трассировка/Классы/ОтелТрассировщик.os` |

#### Concurrency requirements

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 121 | MUST | ✅ | TracerProvider all methods MUST documented safe concurrent use | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:225` |
| 122 | MUST | ✅ | Tracer all methods MUST documented safe concurrent use | `src/Трассировка/Классы/ОтелТрассировщик.os` |
| 123 | MUST | ✅ | Span all methods MUST documented safe concurrent use | `src/Трассировка/Классы/ОтелСпан.os` |
| 124 | MUST | ✅ | Events immutable MUST safe concurrent use | `src/Трассировка/Классы/ОтелСобытиеСпана.os` |
| 125 | SHOULD | ✅ | Links immutable SHOULD safe concurrent use | `src/Трассировка/Классы/ОтелСпан.os:351-368` |

#### Behavior of the API in the absence of an installed SDK

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 126 | MUST | ✅ | API returns non-recording Span with SpanContext in parent Context | `src/Трассировка/Классы/ОтелНоопСпан.os` |
| 127 | SHOULD | ✅ | If parent Span non-recording SHOULD return directly without instantiating new Span | `src/Трассировка/Классы/ОтелНоопСпан.os` |
| 128 | MUST | ✅ | If parent Context no Span empty non-recording Span MUST returned | `src/Трассировка/Классы/ОтелНоопСпан.os:277-279` |

### Trace Sdk

#### Configuration

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | MUST | ✅ | Configuration MUST be owned by TracerProvider | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:207-235` |
| 2 | MUST | ✅ | If configuration updated MUST apply to all returned Tracers | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:91-95` |
| 3 | MAY | ✅ | TracerProvider MAY provide methods update configuration | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:76-78` |

#### ForceFlush

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 4 | MUST | ✅ | ForceFlush MUST invoke ForceFlush on all registered SpanProcessors | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:91-95` |
| 5 | SHOULD | ✅ | ForceFlush SHOULD complete or abort within timeout | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:91-95` |

#### Additional Span Interfaces

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 6 | MUST | ✅ | Readable span MUST access all information listed API spec | `src/Трассировка/Классы/ОтелСпан.os` |
| 7 | MUST | ✅ | Readable span MUST access InstrumentationScope and Resource | `src/Трассировка/Классы/ОтелСпан.os:162-164` |
| 8 | MUST | ✅ | Readable span MUST reliably determine if Span ended | `src/Трассировка/Классы/ОтелСпан.os:189-191` |
| 9 | MUST | ✅ | Readable span MUST report counts dropped attributes/events/links | `src/Трассировка/Классы/ОтелСпан.os:198-218` |
| 10 | MUST | ✅ | Readable span MUST expose parent SpanContext | `src/Трассировка/Классы/ОтелСпан.os:72-74` |

#### Sampling

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 11 | MUST | ✅ | Span Processor MUST receive only spans with IsRecording true | `src/Трассировка/Классы/ОтелТрассировщик.os:61-65` |
| 12 | SHOULD | ✅ | Span Exporter SHOULD NOT receive spans unless Sampled flag set | `src/Трассировка/Классы/ОтелТрассировщик.os:61-65` |
| 13 | MUST | ✅ | SDK MUST NOT allow SampledFlag false and IsRecording true combination | `src/Трассировка/Классы/ОтелТрассировщик.os:61-65` |

#### SDK Span creation

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 14 | MUST | ✅ | SDK MUST use parent trace ID or generate new, Query Sampler, Generate span ID, Create per decision | `src/Трассировка/Классы/ОтелТрассировщик.os:48-104` |

#### ShouldSample

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 15 | MUST | ✅ | ShouldSample MUST accept Context with parent Span parameter | `src/Трассировка/Модули/ОтелСэмплер.os` |
| 16 | MUST | ✅ | MUST accept TraceId Span be created parameter | `src/Трассировка/Модули/ОтелСэмплер.os` |
| 17 | MUST | ✅ | MUST accept Name Span be created parameter | `src/Трассировка/Модули/ОтелСэмплер.os` |
| 18 | MUST | ✅ | MUST accept SpanKind Span be created parameter | `src/Трассировка/Модули/ОтелСэмплер.os` |
| 19 | MUST | ✅ | MUST accept Initial set Attributes Span parameter | `src/Трассировка/Модули/ОтелСэмплер.os` |
| 20 | MUST | ✅ | MUST accept Collection links associated Span parameter | `src/Трассировка/Модули/ОтелСэмплер.os` |
| 21 | MUST | ✅ | Return SamplingResult with Decision | `src/Трассировка/Модули/ОтелСэмплер.os` |
| 22 | MUST | ✅ | Return set span Attributes also added Span | `src/Трассировка/Модули/ОтелСэмплер.os` |
| 23 | MUST | ✅ | Return Tracestate associated Span | `src/Трассировка/Модули/ОтелСэмплер.os` |

#### Span Limits

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 24 | MUST | ✅ | Span attributes MUST adhere common rules attribute limits | `src/Трассировка/Классы/ОтелЛимитыСпана.os` |
| 25 | MAY | ✅ | SDK MAY discard links and events beyond configured limit | `src/Трассировка/Классы/ОтелСпан.os:286-291,356-358` |
| 26 | MUST | ✅ | MUST provide way change limits via configuration | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:207-235` |
| 27 | SHOULD | ✅ | Configuration options SHOULD EventCountLimit, LinkCountLimit | `src/Трассировка/Классы/ОтелЛимитыСпана.os` |
| 28 | SHOULD | ✅ | SHOULD be bundled class SpanLimits | `src/Трассировка/Классы/ОтелЛимитыСпана.os` |

#### Id Generators

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 29 | MUST | ✅ | SDK MUST randomly generate both TraceId SpanId by default | `src/Трассировка/Классы/ОтелТрассировщик.os:92,562` |
| 30 | MUST | ✅ | SDK MUST provide mechanism customizing ID generation | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os` |

#### Span processor

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 31 | MUST | ✅ | SpanProcessor MUST declare OnStart method | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:17-47` |
| 32 | MUST | ✅ | SpanProcessor MUST declare OnEnd method | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:17-47` |
| 33 | MUST | ✅ | SpanProcessor MUST declare Shutdown method | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:17-47` |
| 34 | MUST | ✅ | SpanProcessor MUST declare ForceFlush method | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:17-47` |
| 35 | SHOULD | ✅ | SpanProcessor SHOULD declare OnEnding method (optional) | `src/Трассировка/Классы (referenced)` |
| 36 | MUST | ✅ | OnStart called span started, synchronously on thread started span | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:17-19` |
| 37 | MUST | ✅ | OnStart should not block throw exceptions | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:17-19` |
| 38 | MUST | ✅ | OnEnd called after span ended (timestamp already set) | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-31` |
| 39 | MUST | ✅ | OnEnd should not block throw exceptions | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-31` |

#### Simple processor

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 40 | MUST | ✅ | SimpleSpanProcessor passes finished spans SpanExporter soon finished | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-31` |
| 41 | MUST | ✅ | Processor MUST synchronize calls Exporter prevent concurrent invocation | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-31` |

### Logs Api

#### Logs API

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | SHOULD | ⚠️ | API SHOULD provide a way to set/register and access a global default LoggerProvider | `-` |

#### LoggerProvider operations

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 2 | MUST | ⚠️ | LoggerProvider MUST provide the following functions: Get a Logger | `-` |
| 3 | MUST | ⚠️ | This API MUST accept the following instrumentation scope parameters (name, version, schema_url, attributes) | `-` |
| 4 | MUST | ⚠️ | This API MUST be structured to accept a variable number of attributes, including none | `-` |

#### Logger

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 5 | MUST | ⚠️ | Logger MUST provide a function to: Emit a LogRecord | `-` |
| 6 | SHOULD | ⚠️ | Logger SHOULD provide functions to: Report if Logger is Enabled | `-` |
| 7 | MUST | ⚠️ | The API MUST accept the following parameters (Timestamp, ObservedTimestamp, Context, SeverityNumber, SeverityText, Bo... | `-` |
| 8 | SHOULD | ⚠️ | Context parameter SHOULD be optional when implicit Context is supported | `-` |
| 9 | MUST | ⚠️ | Context MUST use current Context when unspecified | `-` |
| 10 | SHOULD | ⚠️ | Logger SHOULD provide Enabled API | `-` |
| 11 | SHOULD | ⚠️ | Enabled API SHOULD accept Context, SeverityNumber, EventName parameters | `-` |
| 12 | MUST | ⚠️ | Enabled API MUST return a language idiomatic boolean type | `-` |
| 13 | SHOULD | ⚠️ | Instrumentation authors need to call Enabled API each time to ensure up-to-date response | `-` |
| 14 | MAY | N/A | The API MAY accept Exception (optional) parameter | `-` |

#### Optional and required parameters

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 15 | MUST | ⚠️ | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it | `-` |
| 16 | MUST | ⚠️ | For each required parameter, the API MUST be structured to obligate a user to provide it | `-` |
| 17 | MUST NOT | ⚠️ | API MUST NOT obligate a user to provide optional parameters | `-` |

#### Concurrency requirements

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 18 | MUST | ⚠️ | LoggerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default | `-` |
| 19 | MUST | ⚠️ | Logger - all methods MUST be documented that implementations need to be safe for concurrent use by default | `-` |

### Logs Sdk

#### Logs SDK

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | MUST | ⚠️ | All language implementations of OpenTelemetry MUST provide an SDK | `-` |

#### LoggerProvider

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 2 | MUST | ⚠️ | LoggerProvider MUST provide a way to allow a Resource to be specified | `-` |
| 3 | SHOULD | ⚠️ | If Resource is specified, it SHOULD be associated with all LogRecords produced | `-` |

#### LoggerProvider Creation

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 4 | SHOULD | ⚠️ | SDK SHOULD allow the creation of multiple independent LoggerProviders | `-` |

#### Configuration

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 5 | MUST | ⚠️ | Configuration MUST be owned by the LoggerProvider | `-` |
| 6 | MAY | ⚠️ | Configuration MAY be applied at time of LoggerProvider creation | `-` |
| 7 | MUST | ⚠️ | Updated configuration MUST also apply to all already returned Loggers | `-` |
| 8 | MUST NOT | ⚠️ | It MUST NOT matter whether Logger was obtained before or after configuration change | `-` |

#### ForceFlush

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 9 | SHOULD | ⚠️ | ForceFlush SHOULD provide way to let caller know if succeeded/failed/timed out | `-` |
| 10 | SHOULD | ⚠️ | ForceFlush SHOULD return ERROR status if error condition | `-` |
| 11 | SHOULD | ⚠️ | ForceFlush SHOULD return NO ERROR status if no error condition | `-` |
| 12 | SHOULD | ⚠️ | ForceFlush SHOULD complete or abort within timeout | `-` |
| 13 | MUST | ⚠️ | ForceFlush MUST invoke ForceFlush on all registered LogRecordProcessors | `-` |
| 14 | SHOULD | ⚠️ | Tasks for LogRecords SHOULD be completed as soon as possible | `-` |
| 15 | SHOULD | ⚠️ | LogRecordProcessor SHOULD try to call exporter Export with all LogRecords | `-` |
| 16 | MUST | ⚠️ | Built-in LogRecordProcessors MUST do so | `-` |
| 17 | MUST | ⚠️ | LogRecordProcessor MUST prioritize honoring timeout | `-` |
| 18 | MAY | ⚠️ | LogRecordProcessor MAY skip or abort Export/ForceFlush calls | `-` |
| 19 | SHOULD | ⚠️ | ForceFlush SHOULD provide way to let caller know if succeeded/failed/timed out | `-` |
| 20 | SHOULD | ⚠️ | ForceFlush SHOULD complete or abort within timeout | `-` |

#### ReadableLogRecord

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 21 | MUST | ⚠️ | Function MUST be able to access all information added to LogRecord | `-` |
| 22 | MUST | ⚠️ | Function MUST also be able to access InstrumentationScope and Resource | `-` |
| 23 | MUST | ⚠️ | Trace context fields MUST be populated from resolved Context at emit time | `-` |
| 24 | MUST | ⚠️ | Counts for attributes due to collection limits MUST be available for exporters | `-` |

#### ReadWriteLogRecord

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 25 | MUST | ⚠️ | Function MUST additionally be able to modify LogRecord information | `-` |

#### LogRecord Limits

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 26 | MUST | ⚠️ | LogRecord attributes MUST adhere to common rules of attribute limits | `-` |
| 27 | MUST | ⚠️ | If SDK implements attribute limits it MUST provide a way to change these limits | `-` |
| 28 | SHOULD | ⚠️ | Options SHOULD be called LogRecordLimits | `-` |
| 29 | SHOULD | ⚠️ | Message SHOULD be printed to indicate attribute was discarded | `-` |
| 30 | MUST | ⚠️ | Message MUST be printed at most once per LogRecord | `-` |

#### LogRecordProcessor

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 31 | MUST | ⚠️ | SDK MUST allow each pipeline to end with an individual exporter | `-` |
| 32 | MUST | ⚠️ | SDK MUST allow users to implement and configure custom processors | `-` |

#### LogRecordProcessor operations#### OnEmit

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 33 | SHOULD NOT | ⚠️ | Method SHOULD NOT block or throw exceptions | `-` |
| 34 | MUST | ⚠️ | logRecord mutations MUST be visible in next registered processors | `-` |
| 35 | SHOULD | ⚠️ | Implementations SHOULD recommended users to use clone for concurrent processing | `-` |

#### Enabled

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 36 | MUST | ⚠️ | Enabled MUST return false when no LogRecordProcessors registered | `-` |
| 37 | SHOULD | ⚠️ | Otherwise, Enabled SHOULD return true | `-` |
| 38 | MUST NOT | ⚠️ | Any modifications to parameters inside Enabled MUST NOT be propagated to caller | `-` |

#### ShutDown

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 39 | SHOULD | ⚠️ | Shutdown SHOULD be called only once for each LogRecordProcessor instance | `-` |
| 40 | SHOULD | ⚠️ | SDKs SHOULD ignore subsequent calls gracefully | `-` |
| 41 | SHOULD | ⚠️ | Shutdown SHOULD provide way to let caller know if succeeded/failed/timed out | `-` |
| 42 | MUST | ⚠️ | Shutdown MUST include the effects of ForceFlush | `-` |
| 43 | SHOULD | ⚠️ | Shutdown SHOULD complete or abort within timeout | `-` |

#### ForceFlush

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 44 | SHOULD | ⚠️ | ForceFlush SHOULD provide way to let caller know if succeeded/failed/timed out | `-` |
| 45 | SHOULD | ⚠️ | ForceFlush SHOULD return ERROR status if error condition | `-` |
| 46 | SHOULD | ⚠️ | ForceFlush SHOULD return NO ERROR status if no error condition | `-` |
| 47 | SHOULD | ⚠️ | ForceFlush SHOULD complete or abort within timeout | `-` |
| 48 | MUST | ⚠️ | ForceFlush MUST invoke ForceFlush on all registered LogRecordProcessors | `-` |
| 49 | SHOULD | ⚠️ | Tasks for LogRecords SHOULD be completed as soon as possible | `-` |
| 50 | SHOULD | ⚠️ | LogRecordProcessor SHOULD try to call exporter Export with all LogRecords | `-` |
| 51 | MUST | ⚠️ | Built-in LogRecordProcessors MUST do so | `-` |
| 52 | MUST | ⚠️ | LogRecordProcessor MUST prioritize honoring timeout | `-` |
| 53 | MAY | ⚠️ | LogRecordProcessor MAY skip or abort Export/ForceFlush calls | `-` |
| 54 | SHOULD | ⚠️ | ForceFlush SHOULD provide way to let caller know if succeeded/failed/timed out | `-` |
| 55 | SHOULD | ⚠️ | ForceFlush SHOULD complete or abort within timeout | `-` |

#### Built-in processors

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 56 | MUST | ⚠️ | Standard SDK MUST implement both simple and batch processors | `-` |
| 57 | SHOULD | ⚠️ | Other scenarios SHOULD be first considered for out-of-process implementation | `-` |

#### Simple processor

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 58 | MUST | ⚠️ | Processor MUST synchronize calls to LogRecordExporter Export | `-` |

#### LogRecordExporter operations

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 59 | MUST | ⚠️ | LogRecordExporter MUST support the following functions | `-` |

#### Export

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 60 | MUST NOT | ⚠️ | Export MUST NOT block indefinitely | `-` |
| 61 | MUST | ⚠️ | Export MUST have reasonable upper limit after which call times out | `-` |
| 62 | SHOULD NOT | ⚠️ | Default SDK LogRecordProcessors SHOULD NOT implement retry logic | `-` |

#### ForceFlush

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 63 | SHOULD | ⚠️ | ForceFlush SHOULD provide way to let caller know if succeeded/failed/timed out | `-` |
| 64 | SHOULD | ⚠️ | ForceFlush SHOULD return ERROR status if error condition | `-` |
| 65 | SHOULD | ⚠️ | ForceFlush SHOULD return NO ERROR status if no error condition | `-` |
| 66 | SHOULD | ⚠️ | ForceFlush SHOULD complete or abort within timeout | `-` |
| 67 | MUST | ⚠️ | ForceFlush MUST invoke ForceFlush on all registered LogRecordProcessors | `-` |
| 68 | SHOULD | ⚠️ | Tasks for LogRecords SHOULD be completed as soon as possible | `-` |
| 69 | SHOULD | ⚠️ | LogRecordProcessor SHOULD try to call exporter Export with all LogRecords | `-` |
| 70 | MUST | ⚠️ | Built-in LogRecordProcessors MUST do so | `-` |
| 71 | MUST | ⚠️ | LogRecordProcessor MUST prioritize honoring timeout | `-` |
| 72 | MAY | ⚠️ | LogRecordProcessor MAY skip or abort Export/ForceFlush calls | `-` |
| 73 | SHOULD | ⚠️ | ForceFlush SHOULD provide way to let caller know if succeeded/failed/timed out | `-` |
| 74 | SHOULD | ⚠️ | ForceFlush SHOULD complete or abort within timeout | `-` |

#### Shutdown

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 75 | MUST | ⚠️ | Shutdown MUST be called only once for each LoggerProvider instance | `-` |
| 76 | SHOULD | ⚠️ | SDKs SHOULD return a valid no-op Logger for these calls | `-` |
| 77 | SHOULD | ⚠️ | Shutdown SHOULD provide way to let caller know if succeeded/failed/timed out | `-` |
| 78 | SHOULD | ⚠️ | Shutdown SHOULD complete or abort within timeout | `-` |
| 79 | MUST | ⚠️ | Shutdown MUST be implemented by invoking Shutdown on all registered LogRecordProcessors | `-` |

### Metrics Api

#### Overview

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | SHOULD | ✅ | Global default MeterProvider support | `-` |

#### MeterProvider operations

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 2 | MUST | ✅ | MeterProvider MUST provide GetMeter function | `src/Метрики/Классы/ОтелПровайдерМетрик.os:35` |
| 3 | MUST | ✅ | GetMeter MUST accept name parameter | `src/Метрики/Классы/ОтелПровайдерМетрик.os:50` |
| 4 | MUST NOT | ✅ | API MUST NOT obligate version parameter | `src/Метрики/Классы/ОтелПровайдерМетрик.os:50` |
| 5 | MUST NOT | ✅ | API MUST NOT obligate schema_url parameter | `src/Метрики/Классы/ОтелПровайдерМетрик.os:50` |
| 6 | MUST | ✅ | API MUST be structured to accept attributes parameter | `src/Метрики/Классы/ОтелПровайдерМетрик.os:50` |

#### Meter

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ | Meter SHOULD NOT be responsible for configuration | `-` |

#### Meter operations

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 8 | MUST | ✅ | Meter MUST provide functions to create instruments | `-` |

#### Instrument

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 9 | SHOULD | ✅ | Language-level features SHOULD be considered as identifying | `-` |

#### Synchronous and Asynchronous instruments

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 10 | MUST | ✅ | Synchronous API MUST accept name parameter | `-` |
| 11 | SHOULD | ✅ | API SHOULD require name parameter structurally | `-` |
| 12 | SHOULD | ✅ | API SHOULD document name parameter format | `-` |
| 13 | SHOULD NOT | ✅ | API SHOULD NOT validate name format | `-` |
| 14 | MUST NOT | ✅ | Unit MUST NOT be obligatory | `-` |
| 15 | MUST | ✅ | API MUST accept case-sensitive unit string | `src/Метрики/Классы/ОтелМетр.os:52` |
| 16 | SHOULD NOT | ✅ | API SHOULD NOT validate unit | `-` |
| 17 | MUST NOT | ✅ | Description MUST NOT be obligatory | `-` |
| 18 | MUST | ✅ | API MUST accept description with BMP encoding | `-` |
| 19 | MUST NOT | ✅ | Advisory parameters MUST NOT be obligatory | `-` |
| 20 | SHOULD NOT | ✅ | API SHOULD NOT validate advisory parameters | `-` |
| 21 | MUST | ✅ | Asynchronous API MUST accept name parameter | `-` |
| 22 | MUST | ✅ | API MUST accept variable number of callbacks | `-` |
| 23 | MUST | ✅ | API MUST support zero-parameter callback creation | `-` |
| 24 | SHOULD | ✅ | API SHOULD support post-creation callback registration | `src/Метрики/Классы/ОтелМетр.os:348` |
| 25 | MUST | ✅ | User MUST be able to undo callback registration | `-` |
| 26 | MUST | ✅ | Every registered Callback MUST be evaluated exactly once | `src/Метрики/Классы/ОтелМетр.os:355` |
| 27 | MUST | ✅ | Callbacks MUST be documented with requirements | `-` |
| 28 | SHOULD | ✅ | Callbacks SHOULD be reentrant safe | `-` |
| 29 | SHOULD NOT | ✅ | Callbacks SHOULD NOT take indefinite time | `-` |
| 30 | SHOULD NOT | ✅ | Callbacks SHOULD NOT duplicate observations | `-` |
| 31 | MUST | ✅ | Callbacks at creation time MUST apply to single instrument | `-` |
| 32 | MUST | ✅ | Multi-instrument Callbacks MUST distinguish instrument | `src/Метрики/Классы/ОтелМетр.os:348` |
| 33 | MUST | ✅ | Observations from single Callback MUST have identical timestamps | `-` |
| 34 | SHOULD | ✅ | API SHOULD provide way to pass state to callback | `-` |

#### General operations

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 35 | SHOULD | ✅ | Synchronous instruments SHOULD provide Enabled function | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179` |
| 36 | SHOULD | ✅ | Enabled API SHOULD help avoid expensive operations | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:77` |
| 37 | MUST | ✅ | Enabled API MUST be structured for future parameters | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179` |
| 38 | MUST | ✅ | Enabled API MUST return boolean type | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179` |
| 39 | SHOULD | ✅ | Enabled SHOULD be checked for each measurement | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:77` |

#### Counter

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 40 | MUST NOT | ✅ | MUST NOT create Counter except via Meter | `src/Метрики/Классы/ОтелМетр.os:43` |
| 41 | MUST | ✅ | Counter.Add() SHOULD NOT return value | `src/Метрики/Классы/ОтелСчетчик.os:21` |
| 42 | MUST | ✅ | Add MUST accept numeric value parameter | `src/Метрики/Классы/ОтелСчетчик.os:21` |
| 43 | SHOULD | ✅ | API SHOULD require increment value structurally | `src/Метрики/Классы/ОтелСчетчик.os:21` |
| 44 | SHOULD | ✅ | Increment SHOULD be documented as non-negative | `src/Метрики/Классы/ОтелСчетчик.os:14` |
| 45 | SHOULD NOT | ✅ | API SHOULD NOT validate non-negative | `src/Метрики/Классы/ОтелСчетчик.os:22` |
| 46 | MUST | ✅ | Add MUST accept attributes parameter | `src/Метрики/Классы/ОтелСчетчик.os:21` |
| 47 | MUST | ✅ | Flexible attributes MUST be supported | `src/Метрики/Классы/ОтелСчетчик.os:21` |
| 48 | MUST NOT | ✅ | MUST NOT create AsynchronousCounter except via Meter | `src/Метрики/Классы/ОтелМетр.os:198` |
| 49 | MUST | ✅ | Observations from Callback MUST have identical timestamps | `-` |
| 50 | SHOULD | ✅ | API SHOULD provide state passing to callback | `-` |

#### Concurrency requirements

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 51 | MUST | ✅ | MeterProvider methods MUST be thread-safe | `-` |
| 52 | MUST | ✅ | Meter methods MUST be thread-safe | `src/Метрики/Классы/ОтелМетр.os:11` |
| 53 | MUST | ✅ | Instrument methods MUST be thread-safe | `-` |

### Metrics Sdk

#### Metrics SDK

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | MUST | ✅ | All language implementations of OpenTelemetry MUST provide an SDK. | `-` |

#### MeterProvider

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 2 | MUST | ✅ | A `MeterProvider` MUST provide a way to allow a Resource to | `-` |
| 3 | SHOULD | ✅ | be specified. If a `Resource` is specified, it SHOULD be associated with all the | `-` |

#### MeterProvider Creation

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 4 | SHOULD | ✅ | The SDK SHOULD allow the creation of multiple independent `MeterProvider`s. | `-` |

#### Configuration

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 5 | MUST | ✅ | and (Development) MeterConfigurator) MUST be | `-` |
| 6 | MUST NOT | ✅ | configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT | `-` |
| 7 | SHOULD | ✅ | stream, that value SHOULD be used.* If there is no matching view, but the `MetricReader` defines a d | `-` |
| 8 | SHOULD | ✅ | for, that value SHOULD be used.* If none of the previous values are defined, the default value of 20 | `-` |
| 9 | MUST | ✅ | The SDK MUST create an Aggregator with the overflow attribute set prior to | `-` |
| 10 | MUST | ✅ | be created. The SDK MUST provide the guarantee that overflow would not happen | `-` |

#### ForceFlush

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 11 | MUST | ✅ | `ForceFlush` MUST invoke `ForceFlush` on all registered | `-` |
| 12 | SHOULD | ✅ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | `-` |
| 13 | SHOULD | ✅ | failed or timed out. `ForceFlush` SHOULD return some ERROR status if there | `-` |
| 14 | SHOULD | ✅ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be | `-` |

#### View

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 15 | MUST | ✅ | The SDK MUST provide functionality for a user to create Views for a | `-` |
| 16 | MUST | ✅ | `MeterProvider`. This functionality MUST accept as inputs the Instrument | `-` |
| 17 | MUST | ✅ | The SDK MUST provide the means to register Views with a `MeterProvider`. | `-` |

#### Instrument selection criteria

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 18 | SHOULD | ✅ | Criteria SHOULD be treated as additive. This means an Instrument has to match | `-` |
| 19 | MUST | ✅ | The SDK MUST accept the following criteria: | `-` |
| 20 | MUST | ✅ | If the SDK does not support wildcards in general, it MUST still recognize the | `-` |
| 21 | MUST NOT | ✅ | `name`, but MUST NOT obligate a user to provide one. | `-` |
| 22 | MUST NOT | ✅ | `type`, but MUST NOT obligate a user to provide one. | `-` |
| 23 | MUST NOT | ✅ | `unit`, but MUST NOT obligate a user to provide one. | `-` |
| 24 | MUST NOT | ✅ | to accept a `meter_name`, but MUST NOT obligate a user to provide one. | `-` |
| 25 | MUST NOT | ✅ | to accept a `meter_version`, but MUST NOT obligate a user to provide one. | `-` |
| 26 | MUST NOT | ✅ | to accept a `meter_schema_url`, but MUST NOT obligate a user to provide one. | `-` |
| 27 | MUST NOT | ✅ | accept the criteria, but MUST NOT obligate a user to provide them. | `-` |

#### Stream configuration

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 28 | MUST | ✅ | The SDK MUST accept the following stream configuration parameters: | `-` |
| 29 | SHOULD | ✅ | `name`: The metric stream name that SHOULD be used. | `-` |
| 30 | SHOULD | ✅ | In order to avoid conflicts, if a `name` is provided the View SHOULD have an | `-` |
| 31 | MUST NOT | ✅ | MUST NOT obligate a user to provide one. If the user does not provide a | `-` |
| 32 | MUST | ✅ | `name` value, name from the Instrument the View matches MUST be used by | `-` |
| 33 | SHOULD | ✅ | `description`: The metric stream description that SHOULD be used. | `-` |
| 34 | MUST NOT | ✅ | accept a `description`, but MUST NOT obligate a user to provide one. If the | `-` |
| 35 | MUST | ✅ | Instrument a View matches MUST be used by default. | `-` |
| 36 | MUST | ✅ | keys that identify the attributes that MUST be kept, and all other attributes | `-` |
| 37 | MUST | ✅ | MUST be ignored. | `-` |

#### Measurement processing

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 38 | SHOULD | ✅ | The SDK SHOULD use the following logic to determine how to process Measurements | `-` |
| 39 | MUST | ✅ | MUST be honored.* If the `MeterProvider` has one or more `View`(s) registered:* If the Instrument co | `-` |
| 40 | SHOULD | ✅ | the implementation SHOULD apply the View and emit a warning. If it is not | `-` |
| 41 | SHOULD | ✅ | implementation SHOULD emit a warning and proceed as if the View did not | `-` |
| 42 | MUST | ✅ | the setting defined by the View MUST take precedence over the advisory parameters.* If the Instrumen | `-` |
| 43 | SHOULD | ✅ | SDK SHOULD enable the instrument using the default aggregation and temporality. | `-` |

#### conflicting metric identities)

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 44 | MUST | ✅ | The SDK MUST provide the following `Aggregation` to support the | `-` |
| 45 | SHOULD | ✅ | The SDK SHOULD provide the following `Aggregation`: | `-` |

#### Sum Aggregation

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 46 | MUST | ✅ | * Count of `Measurement` values in population.* Arithmetic sum of `Measurement` values in population | `-` |
| 47 | MUST | ✅ | (-∞, 0], (0, 5.0], (5.0, 10.0], (10.0, 25.0], (25.0, 50.0], (50.0, 75.0], (75.0, 100.0], (100.0, 250 | `-` |
| 48 | SHOULD NOT | ✅ | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, | `-` |
| 49 | MUST | ✅ | The implementation MUST maintain reasonable minimum and maximum scale | `-` |
| 50 | SHOULD | ✅ | positive or negative ranges, the implementation SHOULD use the maximum | `-` |
| 51 | SHOULD | ✅ | Implementations SHOULD adjust the histogram scale as necessary to | `-` |

#### Observations inside asynchronous callbacks

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 52 | MUST | ✅ | Callback functions MUST be invoked for the specific `MetricReader` | `-` |
| 53 | SHOULD | ✅ | The implementation SHOULD disregard the use of asynchronous instrument | `-` |
| 54 | SHOULD | ✅ | The implementation SHOULD use a timeout to prevent indefinite callback | `-` |
| 55 | MUST | ✅ | The implementation MUST complete the execution of all callbacks for a | `-` |
| 56 | SHOULD NOT | ✅ | The implementation SHOULD NOT produce aggregated metric data for a | `-` |

#### Cardinality limits

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 57 | SHOULD | ✅ | SDKs SHOULD support being configured with a cardinality limit. The number of | `-` |
| 58 | SHOULD | ✅ | cycle. Cardinality limit enforcement SHOULD occur after attribute filtering, | `-` |

#### Configuration

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 59 | MUST | ✅ | and (Development) MeterConfigurator) MUST be | `-` |
| 60 | MUST NOT | ✅ | configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT | `-` |
| 61 | SHOULD | ✅ | stream, that value SHOULD be used.* If there is no matching view, but the `MetricReader` defines a d | `-` |
| 62 | SHOULD | ✅ | for, that value SHOULD be used.* If none of the previous values are defined, the default value of 20 | `-` |
| 63 | MUST | ✅ | The SDK MUST create an Aggregator with the overflow attribute set prior to | `-` |
| 64 | MUST | ✅ | be created. The SDK MUST provide the guarantee that overflow would not happen | `-` |

#### Synchronous instrument cardinality limits

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 65 | MUST | ✅ | Aggregators for synchronous instruments with cumulative temporality MUST | `-` |
| 66 | MUST | ✅ | Regardless of aggregation temporality, the SDK MUST ensure that every | `-` |
| 67 | MUST NOT | ✅ | Measurements MUST NOT be double-counted or dropped | `-` |

#### Asynchronous instrument cardinality limits

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 68 | SHOULD | ✅ | Aggregators of asynchronous instruments SHOULD prefer the first-observed | `-` |

#### Duplicate instrument registration

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 69 | MUST | ✅ | duplicate instrument. This means that the Meter MUST return a functional | `-` |
| 70 | SHOULD | ✅ | a warning SHOULD be emitted. The emitted warning SHOULD include information for | `-` |
| 71 | SHOULD | ✅ | SHOULD avoid the warning.* If the potential conflict involves instruments that can be distinguished | `-` |
| 72 | SHOULD | ✅ | recipe SHOULD be included in the warning.* Otherwise (e.g., use of multiple units), the SDK SHOULD p | `-` |
| 73 | MUST | ✅ | the SDK MUST aggregate data from identical Instruments | `-` |

#### Name conflict

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 74 | MUST | ✅ | multiple casings of the same `name`. When this happens, the Meter MUST return | `-` |

#### Instrument name

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 75 | SHOULD | ✅ | When a Meter creates an instrument, it SHOULD validate the instrument name | `-` |
| 76 | SHOULD | ✅ | If the instrument name does not conform to this syntax, the Meter SHOULD emit | `-` |

#### Instrument unit

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 77 | SHOULD NOT | ✅ | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | `-` |
| 78 | MUST | ✅ | If a unit is not provided or the unit is null, the Meter MUST treat it the same | `-` |

#### Instrument description

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 79 | SHOULD NOT | ✅ | When a Meter creates an instrument, it SHOULD NOT validate the instrument | `-` |
| 80 | MUST | ✅ | Meter MUST treat it the same as an empty description string. | `-` |

#### Instrument advisory parameters

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 81 | SHOULD | ✅ | When a Meter creates an instrument, it SHOULD validate the instrument advisory | `-` |
| 82 | SHOULD | ✅ | parameters. If an advisory parameter is not valid, the Meter SHOULD emit an error | `-` |
| 83 | MUST | ✅ | different advisory parameters, the Meter MUST return an instrument using the | `-` |
| 84 | MUST | ✅ | MUST take precedence over the advisory parameters. | `-` |

#### Instrument advisory parameter: `ExplicitBucketBoundaries`

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 85 | MUST | ✅ | parameter MUST be used. If neither is provided, the default bucket boundaries | `-` |

#### Exemplar

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 86 | MUST | ✅ | A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements | `-` |
| 87 | SHOULD | ✅ | `Exemplar` sampling SHOULD be turned on by default. If `Exemplar` sampling is | `-` |
| 88 | MUST NOT | ✅ | off, the SDK MUST NOT have overhead related to exemplar sampling. | `-` |
| 89 | MUST | ✅ | A Metric SDK MUST allow exemplar sampling to leverage the configuration of | `-` |
| 90 | SHOULD | ✅ | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: | `-` |
| 91 | MUST | ✅ | The `ExemplarFilter` configuration MUST allow users to select between one of the | `-` |
| 92 | SHOULD | ✅ | The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for | `-` |
| 93 | SHOULD | ✅ | an SDK. The default value SHOULD be `TraceBased`. The filter configuration | `-` |
| 94 | SHOULD | ✅ | SHOULD follow the environment variable specification. | `-` |
| 95 | MUST | ✅ | An OpenTelemetry SDK MUST support the following filters: | `-` |

#### ExemplarReservoir

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 96 | MUST | ✅ | The `ExemplarReservoir` interface MUST provide a method to offer measurements | `-` |
| 97 | MUST | ✅ | A new `ExemplarReservoir` MUST be created for every known timeseries data point, | `-` |
| 98 | SHOULD | ✅ | The “offer” method SHOULD accept measurements, including: | `-` |
| 99 | SHOULD | ✅ | The “offer” method SHOULD have the ability to pull associated trace and span | `-` |
| 100 | MUST | ✅ | from the timeseries the reservoir is associated with. This MUST be clearly | `-` |
| 101 | MUST | ✅ | documented in the API and the reservoir MUST be given the `Attributes` | `-` |
| 102 | MUST | ✅ | The “collect” method MUST return accumulated `Exemplar`s. Exemplars are expected | `-` |
| 103 | SHOULD | ✅ | with. In other words, Exemplars reported against a metric data point SHOULD have | `-` |
| 104 | MUST | ✅ | `Exemplar`s MUST retain any attributes available in the measurement that | `-` |
| 105 | SHOULD | ✅ | The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. | `-` |

#### Exemplar defaults

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 106 | MUST | ✅ | The SDK MUST include two types of built-in exemplar reservoirs: | `-` |
| 107 | SHOULD | ✅ | * Explicit bucket histogram aggregation with more than 1 bucket SHOULD | `-` |
| 108 | SHOULD | ✅ | use `AlignedHistogramBucketExemplarReservoir`.* Base2 Exponential Histogram Aggregation SHOULD use a | `-` |
| 109 | SHOULD | ✅ | twenty (e.g. `min(20, max_buckets)`).* All other aggregations SHOULD use `SimpleFixedSizeExemplarRes | `-` |

#### SimpleFixedSizeExemplarReservoir

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 110 | MUST | ✅ | This reservoir MUST use a uniformly-weighted sampling algorithm based on the | `-` |
| 111 | SHOULD | ✅ | Any stateful portion of sampling computation SHOULD be reset every collection | `-` |
| 112 | SHOULD | ✅ | contention. Otherwise, a default size of `1` SHOULD be used. | `-` |

#### AlignedHistogramBucketExemplarReservoir

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 113 | MUST | ✅ | This Exemplar reservoir MUST take a configuration parameter that is the | `-` |
| 114 | MUST | ✅ | configuration of a Histogram. This implementation MUST store at most one | `-` |
| 115 | SHOULD | ✅ | measurement that falls within a histogram bucket, and SHOULD use a | `-` |
| 116 | SHOULD | ✅ | number of bucket boundaries plus one. This configuration parameter SHOULD have | `-` |

#### Custom ExemplarReservoir

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 117 | MUST | ✅ | The SDK MUST provide a mechanism for SDK users to provide their own | `-` |
| 118 | MUST | ✅ | ExemplarReservoir implementation. This extension MUST be configurable on | `-` |
| 119 | MUST | ✅ | a metric View, although individual reservoirs MUST still be | `-` |

#### MetricReader operations#### Collect

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 120 | SHOULD | ✅ | `Collect` SHOULD provide a way to let the caller know whether it succeeded, | `-` |
| 121 | SHOULD | ✅ | `Collect` SHOULD invoke Produce on registered | `-` |

#### Shutdown

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 122 | MUST | ✅ | `Shutdown` MUST be called only once for each `MetricReader` instance. After the | `-` |
| 123 | SHOULD | ✅ | SHOULD return some failure for these calls, if possible. | `-` |
| 124 | SHOULD | ✅ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, | `-` |
| 125 | SHOULD | ✅ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` MAY be | `-` |

#### Periodic exporting MetricReader

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 126 | MUST | ✅ | The reader MUST synchronize calls to `MetricExporter`’s `Export` | `-` |
| 127 | SHOULD | ✅ | `ForceFlush` SHOULD collect metrics, call `Export(batch)` | `-` |
| 128 | SHOULD | ✅ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | `-` |
| 129 | SHOULD | ✅ | failed or timed out. `ForceFlush` SHOULD return some ERROR status if there | `-` |
| 130 | SHOULD | ✅ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` MAY be | `-` |

#### MetricExporter

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 131 | MUST | ✅ | `MetricExporter` defines the interface that protocol-specific exporters MUST | `-` |
| 132 | SHOULD | ✅ | data. Metric Exporters SHOULD | `-` |
| 133 | MUST | ✅ | A Push Metric Exporter MUST support the following functions: | `-` |
| 134 | MUST | ✅ | The SDK MUST provide a way for the exporter to get the Meter | `-` |
| 135 | MUST NOT | ✅ | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit | `-` |
| 136 | SHOULD NOT | ✅ | exporter. The default SDK SHOULD NOT implement retry logic, as the required | `-` |
| 137 | SHOULD | ✅ | received prior to the call to `ForceFlush` SHOULD be completed as soon as | `-` |
| 138 | SHOULD | ✅ | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, | `-` |
| 139 | SHOULD | ✅ | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, | `-` |
| 140 | SHOULD | ✅ | `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be | `-` |

#### Pull Metric Exporter

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 141 | MUST | ✅ | sources MUST implement, so they can be plugged into an OpenTelemetry | `-` |
| 142 | SHOULD | ✅ | `MetricProducer` implementations SHOULD accept configuration for the | `-` |

#### Interface Definition

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 143 | MUST | ✅ | A `MetricProducer` MUST support the following functions: | `-` |
| 144 | MUST | ✅ | A `MetricFilter` MUST support the following functions: | `-` |

#### Interface Definition

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 145 | MUST | ✅ | A `MetricProducer` MUST support the following functions: | `-` |
| 146 | MUST | ✅ | A `MetricFilter` MUST support the following functions: | `-` |

#### TestMetric

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 147 | MUST | ✅ | The SDK MUST provide configuration according to the SDK environment | `-` |

#### Numerical limits handling

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 148 | MUST | ✅ | The SDK MUST handle numerical limits in a graceful way according to Error | `-` |
| 149 | MUST | ✅ | it MUST handle all the possible values. For example, if the language runtime | `-` |

#### Compatibility requirements

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 150 | SHOULD | ✅ | All the metrics components SHOULD allow new methods to be added to existing | `-` |
| 151 | SHOULD | ✅ | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to | `-` |

#### Concurrency requirements

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 152 | MUST | ✅ | MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe | `-` |
| 153 | MUST | ✅ | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `-` |
| 154 | MUST | ✅ | and `Shutdown` MUST be safe to be called concurrently. | `-` |
| 155 | MUST | ✅ | MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called | `-` |

### Otlp Exporter

### Propagators

#### Operations

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 1 | MUST | ✅ | `Propagator`s MUST define `Inject` and `Extract` operations. Процедура Внедрить() and Функция Извлечь() implemented. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:38-119` |
| 2 | MUST | ✅ | Each `Propagator` type MUST define the specific carrier type. Carriers are Соответствие (HTTP headers). | `src/Пропагация/Модули/ОтелW3CПропагатор.os:38-56,68-119` |

#### Inject

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 3 | MUST | ✅ | A `Context`. The Propagator MUST retrieve the appropriate value from the `Context` first, such as `SpanContext`, `Bag... | `src/Пропагация/Модули/ОтелW3CПропагатор.os:38-56` |
| 4 | MUST | ✅ | If a value can not be parsed from the carrier, the implementation MUST NOT throw an exception and MUST NOT store a ne... | `src/Пропагация/Модули/ОтелW3CПропагатор.os:76-82` |

#### TextMap Propagator

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 5 | MUST | ✅ | In order to increase compatibility, the key/value pairs MUST only consist of US-ASCII characters that make up valid H... | `src/Пропагация/Модули/ОтелW3CПропагатор.os:1-143` |
| 6 | MUST | ✅ | `Getter` and `Setter` MUST be stateless and allowed to be saved as constants. Operations use simple Соответствие (map... | `src/Пропагация/Модули/ОтелW3CПропагатор.os:126-131` |

#### TextMap Inject

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 7 | SHOULD | ✅ | The implementation SHOULD preserve casing. Заголовки.Вставить("traceparent", ...) preserves case as-is. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:49-51` |
| 8 | MUST | ✅ | A `Setter` to set a propagation key/value pair. Заголовки.Вставить() sets header values. | `src/Пропагация/Модули/ОтелW3CBaggageПропагатор.os:17-39` |

#### Getter argument

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 9 | MUST | ❌ | The `Keys` function MUST return the list of all the keys in the carrier. (Getter pattern not explicitly implemented; ... | `-` |
| 10 | MUST | ❌ | The Get function MUST return the first value of the given propagation key or return null if the key doesn't exist. (I... | `-` |
| 11 | MUST | ❌ | The Get function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP request... | `-` |
| 12 | MUST | ❌ | If explicitly implemented, the `GetAll` function MUST return all values. (Not implemented; single-value extraction on... | `-` |
| 13 | SHOULD | ❌ | It SHOULD return them in the same order as they appear in the carrier. (N/A - GetAll not implemented). | `-` |
| 14 | SHOULD | ❌ | If the key doesn't exist, it SHOULD return an empty collection. (Returns undefined context instead). | `-` |
| 15 | MUST | ❌ | The `GetAll` function is responsible for handling case sensitivity. (Not implemented). | `-` |

#### Composite Propagator

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 16 | MUST | ✅ | Implementations MUST offer a facility to group multiple `Propagator`s from different cross-cutting concerns. ОтелКомп... | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:17-55` |
| 17 | MUST | ✅ | There MUST be functions to accomplish the following operations: Create a composite propagator, Extract from a composi... | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:17-55` |

#### Composite Extract

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 18 | MUST | ✅ | Required arguments: A `Context`. The carrier that holds propagation fields. Функция Извлечь(Контекст, Заголовки). | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:33-39` |
| 19 | MUST | ✅ | If the `TextMapPropagator`'s `Extract` implementation accepts the optional `Getter` argument, the following arguments... | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:33-39` |

#### Get Global Propagator

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 20 | MUST | ✅ | This method MUST exist for each supported `Propagator` type. Returns a global `Propagator`. ОтелГлобальный.ПолучитьПр... | `src/Ядро/Модули/ОтелГлобальный.os:108-111` |

#### Set Global Propagator

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 21 | MUST | ❌ | This method MUST exist for each supported `Propagator` type. Sets the global `Propagator` instance. (No explicit SetG... | `-` |
| 22 | MUST | ⚠️ | The official list of propagators that MUST be maintained and MUST be distributed as OpenTelemetry extension packages:... | `src/Ядро/Классы/ОтелSdk.os` |
| 23 | MUST | ✅ | W3C Baggage. (W3C Baggage propagator found). | `src/Пропагация/Модули/ОтелW3CBaggageПропагатор.os` |
| 24 | MUST | ❌ | B3. (B3 propagator not found in core; marked as conditional/extension). | `-` |

#### W3C Trace Context Requirements

| # | Уровень | Статус | Требование | Расположение в коде |
|---|---|---|---|---|
| 25 | MUST | ✅ | A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP headers as specified i... | `src/Пропагация/Модули/ОтелW3CПропагатор.os:68-119` |
| 26 | MUST | ✅ | A W3C Trace Context propagator MUST propagate a valid `traceparent` value using the same header. Traceparent = "00-" ... | `src/Пропагация/Модули/ОтелW3CПропагатор.os:49-51` |
| 27 | MUST | ✅ | A W3C Trace Context propagator MUST propagate a valid `tracestate` unless the value is empty. Conditional header inse... | `src/Пропагация/Модули/ОтелW3CПропагатор.os:53-55` |

### Env Vars

## Требования Development-статуса

Эти требования находятся в нестабильных разделах спецификации и могут измениться.

### Trace Api (Development)

#### Tracer operations

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | MUST | ✅ | Tracer MUST provide functions to Create new Span |
| 2 | SHOULD | ✅ | Tracer SHOULD provide functions to Report if Tracer is Enabled |
| 3 | MUST | ✅ | Enabled API MUST return language idiomatic boolean type |
| 4 | MUST | ✅ | API MUST be structured in way for parameters to be added |
| 5 | SHOULD | ✅ | SHOULD be documented that instrumentation authors need call each time creating Span |

### Trace Sdk (Development)

#### Tracer

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | MUST | ✅ | Tracer MUST behave according TracerConfig |
| 2 | MUST | ✅ | Upon update Tracer MUST be updated behave per new TracerConfig |

#### TracerConfig

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | SHOULD | ✅ | enabled parameter SHOULD default true |
| 2 | MUST | ✅ | If disabled Tracer MUST behave No-op Tracer |
| 3 | MUST | ✅ | enabled value MUST be used resolve Tracer.Enabled |

#### Enabled

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | MUST | ✅ | Enabled MUST return false when no registered SpanProcessors |
| 2 | MUST | ✅ | Enabled MUST return false when Tracer disabled |
| 3 | SHOULD | ✅ | Otherwise SHOULD return true |

### Logs Api (Development)

#### Ergonomic API

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | SHOULD | ⚠️ | Ergonomic API SHOULD make it more convenient to emit event records |
| 2 | SHOULD | ⚠️ | Design of ergonomic API SHOULD be idiomatic for its language |

### Logs Sdk (Development)

#### Logger Creation

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | SHOULD | ⚠️ | It SHOULD only be possible to create Logger instances through a LoggerProvider |
| 2 | MUST | ⚠️ | LoggerProvider MUST implement the Get a Logger API |
| 3 | MUST | ⚠️ | The input provided by the user MUST be used to create an InstrumentationScope instance |
| 4 | MUST | ⚠️ | In case of invalid name, a working Logger MUST be returned as a fallback |
| 5 | SHOULD | ⚠️ | Invalid name SHOULD keep the original invalid value |
| 6 | SHOULD | ⚠️ | Message reporting that specified value is invalid SHOULD be logged |
| 7 | MUST | ⚠️ | LoggerProvider MUST compute the relevant LoggerConfig using LoggerConfigurator |

#### LoggerConfigurator

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | MUST | ⚠️ | Function MUST accept logger_scope parameter |
| 2 | MUST | ⚠️ | Function MUST return the relevant LoggerConfig or signal |
| 3 | MAY | ⚠️ | Signal MAY be nil, null, empty, or instance of default LoggerConfig |
| 4 | MAY | ⚠️ | Implementations MAY provide shorthand/helper functions |
| 5 | SHOULD | ⚠️ | Enable trace-based filtering for specific loggers or logger patterns |

#### Logger

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | MUST | ⚠️ | Logger MUST behave according to LoggerConfig computed during creation |
| 2 | MUST | ⚠️ | Logger MUST be updated to behave according to new LoggerConfig upon update |

#### LoggerConfig

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | SHOULD | ⚠️ | enabled parameter SHOULD default to true |
| 2 | MUST | ⚠️ | If Logger is disabled, it MUST behave equivalently to No-op Logger |
| 3 | MUST | ⚠️ | minimum_severity parameter MUST default to 0 |
| 4 | MUST | ⚠️ | If log record SeverityNumber is specified and less than minimum_severity, record MUST be dropped |
| 5 | MUST | ⚠️ | trace_based parameter MUST default to false |
| 6 | MUST | ⚠️ | If trace_based is true, log records with unsampled traces MUST be dropped |
| 7 | MUST | ⚠️ | Changes MUST be eventually visible |

#### Emit a LogRecord

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | SHOULD | ⚠️ | If ObservedTimestamp is unspecified, implementation SHOULD set it to current time |
| 2 | MUST | ⚠️ | If Exception is provided, SDK MUST by default set attributes from exception |
| 3 | MUST | ⚠️ | User-provided attributes MUST take precedence |
| 4 | MUST NOT | ⚠️ | User-provided attributes MUST NOT be overwritten by exception-derived attributes |
| 5 | MUST | ⚠️ | Implementation MUST apply filtering rules defined by LoggerConfig |
| 6 | MUST | ⚠️ | If SeverityNumber is less than minimum_severity, log record MUST be dropped |
| 7 | MUST | ⚠️ | If trace_based is true and log record has unsampled trace, record MUST be dropped |

#### Enabled

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | MUST | ⚠️ | Enabled MUST return false when no LogRecordProcessors registered |
| 2 | SHOULD | ⚠️ | Otherwise, Enabled SHOULD return true |
| 3 | MUST NOT | ⚠️ | Any modifications to parameters inside Enabled MUST NOT be propagated to caller |

### Metrics Api (Development)

### Metrics Sdk (Development)

#### Meter Creation

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | SHOULD | ✅ | It SHOULD only be possible to create `Meter` instances through a `MeterProvider` |
| 2 | MUST | ✅ | The `MeterProvider` MUST implement the Get a Meter API. |
| 3 | MUST | ✅ | The input provided by the user MUST be used to create |
| 4 | MUST | ✅ | working Meter MUST be returned as a fallback rather than returning null or |
| 5 | SHOULD | ✅ | throwing an exception, its `name` SHOULD keep the original invalid value, and a |
| 6 | SHOULD | ✅ | message reporting that the specified value is invalid SHOULD be logged. |
| 7 | MUST | ✅ | Status: Development - The `MeterProvider` MUST |

#### MeterConfigurator

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | MUST | ✅ | The function MUST accept the following parameter: |
| 2 | MUST | ✅ | The function MUST return the relevant `MeterConfig`, or some signal indicating |
| 3 | MUST | ✅ | `Shutdown` MUST be called only once for each `MeterProvider` instance. After the |
| 4 | SHOULD | ✅ | SHOULD return a valid no-op Meter for these calls, if possible. |
| 5 | SHOULD | ✅ | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, |
| 6 | SHOULD | ✅ | `Shutdown` SHOULD complete or abort within some timeout. `Shutdown` MAY be |
| 7 | MUST | ✅ | `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered |

#### Start timestamps

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | MUST | ✅ | For delta aggregations, the start timestamp MUST equal the previous collection |
| 2 | MUST | ✅ | with delta temporality aggregation for an instrument MUST share the same start |
| 3 | MUST | ✅ | Cumulative timeseries MUST use a consistent start timestamp for all collection |
| 4 | SHOULD | ✅ | For synchronous instruments, the start timestamp SHOULD be the time of the |
| 5 | SHOULD | ✅ | For asynchronous instrument, the start timestamp SHOULD be: |

#### Meter

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | MUST | ✅ | Distinct meters MUST be treated as separate namespaces for the purposes of detecting |
| 2 | MUST | ✅ | Status: Development - `Meter` MUST behave |
| 3 | MUST | ✅ | the `Meter` MUST be updated to behave according to the new `MeterConfig`. |

#### MeterConfig

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | SHOULD | ✅ | If not explicitly set, the `enabled` parameter SHOULD default to `true` ( |
| 2 | MUST | ✅ | If a `Meter` is disabled, it MUST behave equivalently |
| 3 | MUST | ✅ | The value of `enabled` MUST be used to resolve whether an instrument |
| 4 | MUST | ✅ | However, the changes MUST be eventually visible. |

#### Instrument enabled

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | MUST | ✅ | The synchronous instrument `Enabled` MUST return `false` |
| 2 | SHOULD | ✅ | Otherwise, it SHOULD return `true`. |

#### MetricReader

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | SHOULD | ✅ | SHOULD be provided: |
| 2 | MUST | ✅ | * The `exporter` to use, which is a `MetricExporter` instance.* The default output `aggregation` (op |
| 3 | SHOULD | ✅ | Status: Development - A `MetricReader` SHOULD provide the MetricFilter to the SDK or registered Metr |
| 4 | SHOULD | ✅ | `MetricReader` SHOULD be provided to be used |
| 5 | MUST | ✅ | The `MetricReader` MUST ensure that data points from OpenTelemetry |
| 6 | MUST | ✅ | temporality, MetricReader.Collect MUST receive data points exposed |
| 7 | MUST | ✅ | temporality, MetricReader.Collect MUST only receive data points with |
| 8 | MUST | ✅ | temporality, MetricReader.Collect MUST only receive data points with |
| 9 | MUST | ✅ | successive calls to MetricReader.Collect MUST repeat the same |
| 10 | MUST | ✅ | calls to MetricReader.Collect MUST advance the starting timestamp ( |

#### Produce batch

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | MUST | ✅ | MUST return a batch of Metric Points, filtered by the optional |
| 2 | SHOULD | ✅ | `metricFilter` parameter. Implementation SHOULD use the filter as early as |
| 3 | SHOULD | ✅ | resource information, `Produce` SHOULD require a resource as a parameter. |
| 4 | SHOULD | ✅ | `Produce` SHOULD provide a way to let the caller know whether it succeeded, |
| 5 | SHOULD | ✅ | `Produce` SHOULD include a single InstrumentationScope which identifies the |

Всего Development требований: 89

## Условные требования (Conditional)

Требования, применимые только при реализации определённых расширений.

### Resource Sdk / Resource detector name
*Условие*: conditional:Resource Detector Naming (conditional)

Нет извлечённых требований для этого раздела.

### Propagators / B3 Extract
*Условие*: conditional:B3 Propagator (extension)

| # | Уровень | Статус | Требование |
|---|---|---|---|
| 1 | MUST | N/A | MUST attempt to extract B3 encoded using single and multi-header formats. (B3 propagator not implemented; marked as n_a  |
| 2 | MUST | N/A | MUST preserve a debug trace flag, if received. (B3 propagator not implemented). |
| 3 | MUST | N/A | MUST set the sampled trace flag when the debug flag is set. (B3 propagator not implemented). |
| 4 | MUST | N/A | MUST NOT reuse `X-B3-SpanId` as the id for the server-side span. (B3 propagator not implemented). |
| 5 | MUST | N/A | MUST default to injecting B3 using the single-header format. (B3 propagator not implemented). |
| 6 | MUST | N/A | MUST provide configuration to change the default injection format to B3 multi-header. (B3 propagator not implemented). |
| 7 | MUST | N/A | MUST NOT propagate `X-B3-ParentSpanId`. (B3 propagator not implemented). |
| 8 | MUST | N/A | Fields MUST return the header names that correspond to the configured format. (B3 propagator not implemented). |

### Env Vars / Prometheus Exporter
*Условие*: conditional:Prometheus Exporter (extension)

Нет извлечённых требований для этого раздела.

## Ограничения платформы OneScript

Следующие требования спецификации неприменимы из-за ограничений платформы OneScript:

| Ограничение | Причина | Влияние |
|---|---|---|
| Бинарное представление TraceId/SpanId | OneScript не поддерживает байтовые массивы нативно | Используются hex-строки |
| gRPC транспорт | Нет нативной gRPC библиотеки | Поддерживается HTTP/JSON и HTTP/Protobuf |
| TLS/mTLS конфигурация | Ограниченная поддержка TLS в HTTP-клиенте | Делегировано на уровень ОС |
| Наносекундная точность | OneScript DateTime - миллисекундная точность | Наносекунды эмулируются строками |
| Нативный Protobuf | Нет protobuf-кодогенерации | Ручная сериализация в JSON |
| Многопоточные гарантии | ФоновыеЗадания - ограниченная модель | Используются БлокировкаРесурса и atomic |

## Методология

### Процесс анализа

1. **Извлечение секций**: Спецификация OpenTelemetry v1.55.0 разобрана на 193 секции с метаданными (stability, scope)
2. **Извлечение требований**: Из каждой секции извлечены MUST/SHOULD/MAY требования
3. **Верификация**: 6 независимых агентов проанализировали код по своим доменам:
   - Core (Context, Baggage, Resource, Propagators)
   - Traces (Trace API, Trace SDK)
   - Logs (Logs API, Logs SDK)
   - Metrics API
   - Metrics SDK
   - Export (OTLP Exporter, Env Vars)
4. **Агрегация**: Результаты объединены в единый отчёт

### Статусы

| Статус | Описание |
|---|---|
| ✅ found | Требование полностью реализовано и прослежено до кода |
| ⚠️ partial | Требование частично реализовано или требует доработки |
| ❌ not_found | Требование не реализовано |
| N/A | Неприменимо для платформы OneScript |

### Подсчёт процента соответствия

```
Процент = found / (found + partial + not_found) × 100
```

- Учитываются только Stable + universal требования
- Development и Conditional требования перечислены отдельно
- N/A требования исключены из подсчёта
