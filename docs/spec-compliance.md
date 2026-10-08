# Анализ соответствия спецификации OpenTelemetry v1.61.0

> **Версия спецификации**: [v1.61.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-10-08
> **Методология**: spec-first - извлечены все MUST/SHOULD требования стабильных разделов спецификации, затем каждое прослежено до кода

## Сводка (Stable)

Учитываются только требования из стабильных разделов спецификации с универсальной областью применения.

| Показатель | Значение |
|---|---|
| Всего Stable-требований | 909 |
| Stable + universal | 869 |
| Stable + conditional | 40 |
| Найдено требований (Stable universal) | 837 |
| ✅ Реализовано (found) | 833 (99.5%) |
| ⚠️ Частично (partial) | 4 (0.5%) |
| ❌ Не реализовано (not_found) | 0 (0.0%) |
| ➖ Неприменимо (n_a) | 32 |
| **MUST/MUST NOT found** | 509/510 (99.8%) |
| **SHOULD/SHOULD NOT found** | 324/327 (99.1%) |

## Соответствие по разделам (Stable)

| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |
|---|---|---|---|---|---|---|
| Context | 14 | 0 | 0 | 1 | 14 | 100.0% |
| Baggage Api | 17 | 0 | 0 | 0 | 17 | 100.0% |
| Resource Sdk | 21 | 0 | 0 | 0 | 21 | 100.0% |
| Trace Api | 113 | 0 | 0 | 13 | 113 | 100.0% |
| Trace Sdk | 86 | 0 | 0 | 3 | 86 | 100.0% |
| Logs Api | 22 | 0 | 0 | 0 | 22 | 100.0% |
| Logs Sdk | 73 | 0 | 0 | 4 | 73 | 100.0% |
| Metrics Api | 96 | 0 | 0 | 5 | 96 | 100.0% |
| Metrics Sdk | 204 | 1 | 0 | 3 | 205 | 99.5% |
| Otlp Exporter | 23 | 2 | 0 | 0 | 25 | 92.0% |
| Propagators | 33 | 0 | 0 | 3 | 33 | 100.0% |
| Env Vars | 24 | 0 | 0 | 0 | 24 | 100.0% |
| Prometheus Compatibility | 54 | 0 | 0 | 0 | 54 | 100.0% |
| Prometheus Exporter | 12 | 1 | 0 | 0 | 13 | 92.3% |
| Configuration Sdk | 24 | 0 | 0 | 0 | 24 | 100.0% |
| Configuration Api | 5 | 0 | 0 | 0 | 5 | 100.0% |
| Configuration Data Model | 12 | 0 | 0 | 0 | 12 | 100.0% |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Otlp Exporter]** [MUST] The following configuration options MUST be available to configure the OTLP exporter.  
  Endpoint, headers, compression, timeout, protocol, certificate, client key/certificate, insecure и max request/response size (ОтелHttpТранспорт.os:84-114) доступны. Но файлы сертификатов TLS HTTP-транспортом игнорируются (HTTP-клиент OneScript их не поддерживает, ОтелHttpТранспорт.os:513-518), а сжатие для gRPC не поддерживается клиентом OPI_GRPC (ОтелАвтоконфигурация.os:1061) - опции читаются, но не действуют. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:508`)

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback execution.  
  Soft-timeout: callback запускается в фоновом задании, SDK перестаёт ждать и отбрасывает измерения; hard cancel недоступен в OneScript (EvilBeaver/OneScript#1672), задание продолжает работу в фоне. (`src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:128`)

- ⚠️ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter.  
  OTLP/HTTP отправляет User-Agent OTel-OTLP-Exporter-OneScript/<версия>. Для OTLP/gRPC user-agent кладется в метаданные (ОтелGrpcТранспорт.os:402), но до сервера не доходит: tonic в OPI_GRPC ставит свой user-agent (OpenIntegrations issue 111). (`src/Экспорт/Классы/ОтелHttpТранспорт.os:507`)

- ⚠️ **[Prometheus Exporter]** [SHOULD NOT] A Prometheus Exporter SHOULD use an official Prometheus client library when one exists for the implementation language and it is practical to do so (e.g., dependency concerns) for serving Prometheus metrics; it SHOULD NOT use an unofficial Prometheus client library.  
  Official Prometheus client for OneScript does not exist; the reader uses the community 'prometheus' OneScript package (packagedef dependency 1.0.6), which is unofficial. (`src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:4`)

## Детальный анализ по разделам (Stable)

### Context

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:125` |  |
| 2 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:125` |  |
| 3 | MUST | ✅ found | In the cases where an extremely clear, pre-existing option is not available, OpenTelemetry MUST provide its own `Context` implementation. | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### Create a key

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#create-a-key)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The API MUST accept the following parameter: | `src/Ядро/Модули/ОтелКонтекст.os:42` |  |
| 5 | SHOULD NOT | ✅ found | The key name exists for debugging purposes and does not uniquely identify the key. Multiple calls to `CreateKey` with the same name SHOULD NOT return the same value unless language constraints dictate otherwise. | `src/Ядро/Классы/ОтелКлючКонтекста.os:38` |  |
| 6 | MUST | ✅ found | The API MUST return an opaque object representing the newly created key. | `src/Ядро/Модули/ОтелКонтекст.os:42` |  |

#### Get value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Ядро/Модули/ОтелКонтекст.os:108` |  |
| 8 | MUST | ✅ found | The API MUST return the value in the `Context` for the specified key. | `src/Ядро/Модули/ОтелКонтекст.os:108` |  |

#### Set value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Ядро/Модули/ОтелКонтекст.os:125` |  |
| 10 | MUST | ✅ found | The API MUST return a new `Context` containing the new value. | `src/Ядро/Модули/ОтелКонтекст.os:125` |  |

#### Optional Global operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#optional-global-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ➖ n_a | These operations SHOULD only be used to implement automatic scope switching and define higher level APIs by SDK components and OpenTelemetry instrumentation libraries. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение |

#### Get current Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-current-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST return the `Context` associated with the caller’s current execution unit. | `src/Ядро/Модули/ОтелКонтекст.os:58` |  |

#### Attach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#attach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Ядро/Модули/ОтелКонтекст.os:245` |  |
| 14 | MUST | ✅ found | The API MUST return a value that can be used as a `Token` to restore the previous `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:245` |  |

#### Detach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#detach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Ядро/Модули/ОтелКонтекст.os:267` |  |

### Baggage Api

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Each name in `Baggage` MUST be associated with exactly one value. | `src/Ядро/Классы/ОтелПостроительBaggage.os:187` |  |
| 2 | SHOULD NOT | ✅ found | Language API SHOULD NOT restrict which strings are used as baggage names. | `src/Ядро/Классы/ОтелПостроительBaggage.os:187` |  |
| 3 | MUST | ✅ found | Language API MUST accept any valid UTF-8 string as baggage value in `Set` and return the same value from `Get`. | `src/Ядро/Классы/ОтелBaggage.os:37` |  |
| 4 | MUST | ✅ found | Language API MUST treat both baggage names and values as case sensitive. | `src/Ядро/Классы/ОтелBaggage.os:37` |  |
| 5 | MUST | ✅ found | The Baggage API MUST be fully functional in the absence of an installed SDK. | `src/Ядро/Классы/ОтелBaggage.os:25` |  |
| 6 | MUST | ✅ found | The `Baggage` container MUST be immutable, so that the containing `Context` also remains immutable. | `src/Ядро/Классы/ОтелBaggage.os:151` |  |

#### Get Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | To access the value for a name/value pair set by a prior event, the Baggage API MUST provide a function that takes the name as input, and returns a value associated with the given name, or null if the given name is not present. | `src/Ядро/Классы/ОтелBaggage.os:37` |  |

#### Get All Values

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#get-all-values)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST NOT | ✅ found | The order of name/value pairs MUST NOT be significant. | `src/Ядро/Классы/ОтелBaggage.os:102` |  |

#### Set Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | To record the value for a name/value pair, the Baggage API MUST provide a function which takes a name, and a value as input. | `src/Ядро/Классы/ОтелBaggage.os:67` |  |

#### Remove Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#remove-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | To delete a name/value pair, the Baggage API MUST provide a function which takes a name as input. | `src/Ядро/Классы/ОтелBaggage.os:81` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | If an implementation of this API does not operate directly on the `Context`, it MUST provide the following functionality to interact with a `Context` instance: | `src/Ядро/Модули/ОтелКонтекст.os:154` |  |
| 12 | SHOULD NOT | ✅ found | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:23` |  |
| 13 | SHOULD | ✅ found | If the language has support for implicitly propagated `Context` (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Классы/ОтелBaggage.os:16` |  |
| 14 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:185` |  |

#### Clear Baggage in the Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#clear-baggage-in-the-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | To avoid sending any name/value pairs to an untrusted process, the Baggage API MUST provide a way to remove all baggage entries from a context. | `src/Ядро/Классы/ОтелBaggage.os:93` |  |

#### Propagation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#propagation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The API layer or an extension package MUST include the following `Propagator`s: | `src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:31` |  |

#### Conflict Resolution

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#conflict-resolution)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | If a new name/value pair is added and its name is the same as an existing name, then the new pair MUST take precedence. | `src/Ядро/Классы/ОтелПостроительBaggage.os:23` |  |

### Resource Sdk

#### Resource SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The SDK MUST allow for creation of `Resources` and for associating them with telemetry. | `src/Ядро/Классы/ОтелРесурс.os:102` |  |
| 2 | MUST | ✅ found | When associated with a `TracerProvider`, all `Span`s produced by any `Tracer` from the provider MUST be associated with this `Resource`. | `src/Трассировка/Классы/ОтелТрассировщик.os:253` |  |

#### SDK-provided resource attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#sdk-provided-resource-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The SDK MUST provide access to a Resource with at least the attributes listed at Semantic Attributes with SDK-provided Default Value. | `src/Ядро/Классы/ОтелРесурс.os:110` |  |
| 4 | MUST | ✅ found | This resource MUST be associated with a `TracerProvider`, `MeterProvider`, or `LoggerProvider` if another resource was not explicitly specified. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:366` |  |

#### Create

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#create)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The interface MUST provide a way to create a new resource. | `src/Ядро/Классы/ОтелРесурс.os:102` |  |

#### Merge

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#merge)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | The interface MUST provide a way for an old resource and an updating resource to be merged into a new resource. | `src/Ядро/Классы/ОтелРесурс.os:41` |  |
| 7 | MUST | ✅ found | If either resource contains `Entities` then merge behavior with Entities MUST be used, otherwise merge behavior without Entities MUST be used. | `src/Ядро/Классы/ОтелРесурс.os:41` |  |

#### Merge behavior without Entities

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#merge-behavior-without-entities)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The resulting resource MUST have all attributes that are on any of the two input resources. | `src/Ядро/Классы/ОтелРесурс.os:59` |  |
| 9 | MUST | ✅ found | If a key exists on both the old and updating resource, the value of the updating resource MUST be picked (even if the updated value is empty). | `src/Ядро/Классы/ОтелРесурс.os:62` |  |

#### Detecting resource information from the environment

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#detecting-resource-information-from-the-environment)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17` |  |
| 11 | MUST | ✅ found | Resource detector packages MUST provide a method that returns a resource. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17` |  |
| 12 | MUST NOT | ✅ found | Note the failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Модули/ОтелУтилиты.os:540` |  |
| 13 | SHOULD | ✅ found | Note the failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:27` |  |
| 14 | MUST | ✅ found | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:30` |  |
| 15 | SHOULD | ✅ found | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate (e.g. the detector ... | `src/Ядро/Модули/ОтелУтилиты.os:541` |  |
| 16 | MUST | ✅ found | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources. | `src/Ядро/Классы/ОтелРесурс.os:46` |  |

#### Specifying resource information via an environment variable

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#specifying-resource-information-via-an-environment-variable)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge this, as the secondary resource, with any resource information provided by the user, i.e. the user provided... | `src/Ядро/Классы/ОтелРесурс.os:143` |  |
| 18 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Ядро/Классы/ОтелРесурс.os:187` |  |
| 19 | MUST | ✅ found | The `,` and `=` characters in keys and values MUST be percent encoded. | `src/Ядро/Классы/ОтелРесурс.os:188` |  |
| 20 | SHOULD | ✅ found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | `src/Ядро/Классы/ОтелРесурс.os:197` |  |
| 21 | SHOULD | ✅ found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | `src/Ядро/Классы/ОтелРесурс.os:194` |  |

### Trace Api

#### TracerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `TracerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:39 (Установить), src/Ядро/Модули/ОтелГлобальный.os:129 (ПолучитьПровайдерТрассировки)` |  |
| 2 | SHOULD | ✅ found | Thus, implementations of `TracerProvider` SHOULD allow creating an arbitrary number of `TracerProvider` instances. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:358 (ПриСозданииОбъекта, публичный конструктор)` |  |

#### TracerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The `TracerProvider` MUST provide the following functions: | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:60 (ПолучитьТрассировщик)` |  |

#### Get a Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-a-tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:60 (ИмяБиблиотеки, ВерсияБиблиотеки, АтрибутыОбласти, АдресСхемы)` |  |
| 5 | SHOULD | ✅ found | `name` (required): This name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library (e.g. `io.opentelemetry.contrib.mongodb`), package, module or class name. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:60 (ИмяБиблиотеки - обязательный позиционный параметр)` |  |
| 6 | MUST | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, ... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65-77` |  |
| 7 | SHOULD | ✅ found | its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65-71` |  |
| 8 | SHOULD | ✅ found | its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65-68 (Лог.Предупреждение)` |  |
| 9 | MUST NOT | ✅ found | Implementations MUST NOT require users to repeatedly obtain a `Tracer` again with the same identity to pick up configuration changes. | `src/Трассировка/Классы/ОтелТрассировщик.os:395-399 (Трассировщик хранит ссылку на Провайдер, конфигурация делегируется провайдеру)` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API MUST provide the following functionality to interact with a `Context` instance: | `src/Ядро/Модули/ОтелКонтекст.os:139 (СпанИзКонтекста), src/Ядро/Модули/ОтелКонтекст.os:170 (КонтекстСоСпаном)` |  |
| 11 | SHOULD NOT | ✅ found | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:21 (КлючСпан - приватная переменная модуля, не экспортируется)` |  |
| 12 | SHOULD | ✅ found | If the language has support for implicitly propagated `Context` (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Модули/ОтелКонтекст.os:85 (ТекущийСпан), src/Ядро/Модули/ОтелКонтекст.os:216 (СделатьСпанТекущим)` |  |
| 13 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:139-216 (реализовано в едином пакете API+SDK, независимо от SDK-классов)` |  |

#### Tracer operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracer-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The `Tracer` MUST provide functions to: | `src/Трассировка/Классы/ОтелТрассировщик.os:75 (НачатьСпан), src/Трассировка/Классы/ОтелТрассировщик.os:29 (ПостроительСпана)` |  |
| 15 | SHOULD | ✅ found | The `Tracer` SHOULD provide functions to: | `src/Трассировка/Классы/ОтелТрассировщик.os:54 (Включен)` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when creating `Span`s, a `Tracer` SHOULD provide this `Enabled` API. | `src/Трассировка/Классы/ОтелТрассировщик.os:54` |  |
| 17 | MUST | ✅ found | Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Трассировка/Классы/ОтелТрассировщик.os:54 (Функция Включен() без параметров; необязательные параметры можно добавить без поломки совместимости)` |  |
| 18 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Трассировка/Классы/ОтелТрассировщик.os:54-56 (Булево)` |  |
| 19 | SHOULD | ✅ found | The API SHOULD be documented that instrumentation authors needs to call this API each time they create a new `Span` to ensure they have the most up-to-date response. | `src/Трассировка/Классы/ОтелТрассировщик.os:33-37 (документирующий комментарий)` |  |

#### SpanContext

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spancontext)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | The API MUST implement methods to create a `SpanContext`. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:252 (ПриСозданииОбъекта - конструктор ОтелКонтекстСпана)` |  |
| 21 | SHOULD | ✅ found | These methods SHOULD be the only way to create a `SpanContext`. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:252 (конструктор - единственный способ; поля приватные, без экспортных мутаторов)` |  |
| 22 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os (API и SDK в одном пакете, класс самодостаточен)` |  |
| 23 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os (OneScript не поддерживает наследование классов; переопределить невозможно)` |  |

#### Retrieving the TraceId and SpanId

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#retrieving-the-traceid-and-spanid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | The API MUST allow retrieving the `TraceId` and `SpanId` in the following forms: | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 25 | MUST | ✅ found | Hex - returns the lowercase hex encoded `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` (result MUST be a 16-hex-character lowercase string). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 26 | MUST | ✅ found | Hex - returns the lowercase hex encoded `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` (result MUST be a 16-hex-character lowercase string). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:32` |  |
| 27 | MUST | ✅ found | Binary - returns the binary representation of the `TraceId` (result MUST be a 16-byte array) or `SpanId` (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:84` |  |
| 28 | MUST | ✅ found | Binary - returns the binary representation of the `TraceId` (result MUST be a 16-byte array) or `SpanId` (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:93` |  |
| 29 | SHOULD NOT | ✅ found | The API SHOULD NOT expose details about how they are internally stored. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |

#### IsValid

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isvalid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | An API called `IsValid`, that returns a boolean value, which is `true` if the SpanContext has a non-zero TraceID and a non-zero SpanID, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:70` |  |

#### IsRemote

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isremote)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 31 | MUST | ✅ found | An API called `IsRemote`, that returns a boolean value, which is `true` if the SpanContext was propagated from a remote parent, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:60` |  |
| 32 | MUST | ✅ found | When extracting a `SpanContext` through the Propagators API, `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:163` |  |
| 33 | MUST | ✅ found | When extracting a `SpanContext` through the Propagators API, `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | `src/Трассировка/Классы/ОтелСпан.os:849` |  |

#### TraceState

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracestate)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | MUST | ✅ found | Tracing API MUST provide at least the following operations on `TraceState`: | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:50` |  |
| 35 | MUST | ✅ found | These operations MUST follow the rules described in the W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:73` |  |
| 36 | MUST | ✅ found | All mutating operations MUST return a new `TraceState` with the modifications applied. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:73` |  |
| 37 | MUST | ✅ found | `TraceState` MUST at all times be valid according to rules specified in W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:188` |  |
| 38 | MUST | ✅ found | Every mutating operations MUST validate input parameters. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:73` |  |
| 39 | MUST NOT | ✅ found | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:73` |  |
| 40 | MUST | ✅ found | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data and MUST follow the general error handling guidelines. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:73` |  |

#### Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 41 | SHOULD | ➖ n_a | The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance): выбор имени спана за инструментирующим кодом; SDK не может программно обеспечить это ограничение. |
| 42 | SHOULD | ➖ n_a | Generality SHOULD be prioritized over human-readability. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. |
| 43 | SHOULD | ✅ found | A `Span`’s start time SHOULD be set to the current time on span creation. | `src/Трассировка/Классы/ОтелСпан.os:855` |  |
| 44 | SHOULD | ✅ found | After the `Span` is created, it SHOULD be possible to change its name, set its `Attribute`s, add `Event`s, and set the `Status`. | `src/Трассировка/Классы/ОтелСпан.os:307` |  |
| 45 | MUST NOT | ✅ found | These MUST NOT be changed after the `Span`’s end time has been set. | `src/Трассировка/Классы/ОтелСпан.os:307` |  |
| 46 | SHOULD NOT | ➖ n_a | To prevent misuse, implementations SHOULD NOT provide access to a `Span`’s attributes besides its `SpanContext`. | `src/Трассировка/Классы/ОтелСпан.os:168` | OneScript не поддерживает internal/package-private модификаторы; SDK-геттеры (Атрибуты(), События(), Линки() и т.п.) обязаны быть Экспорт, иначе процессоры/экспортёры не смогут читать данные спана. Аналогично приватным конструкторам. |
| 47 | MUST NOT | ➖ n_a | However, alternative implementations MUST NOT allow callers to create `Span`s directly. | `src/Трассировка/Классы/ОтелСпан.os:818` | OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. |
| 48 | MUST | ✅ found | All `Span`s MUST be created via a `Tracer`. | `src/Трассировка/Классы/ОтелТрассировщик.os:226` |  |

#### Span Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating a `Span` other than with a `Tracer`. | `src/Трассировка/Классы/ОтелСпан.os:818` | OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. |
| 50 | MUST NOT | ✅ found | In languages with implicit `Context` propagation, `Span` creation MUST NOT set the newly created `Span` as the active `Span` in the current `Context` by default, but this functionality MAY be offered additionally as a separate operation. | `src/Трассировка/Классы/ОтелТрассировщик.os:167` |  |
| 51 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелТрассировщик.os:75` |  |
| 52 | MUST NOT | ✅ found | This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`. | `src/Трассировка/Классы/ОтелТрассировщик.os:130` |  |
| 53 | MUST | ✅ found | The semantic parent of the Span MUST be determined according to the rules described in Determining the Parent Span from a Context. | `src/Трассировка/Классы/ОтелТрассировщик.os:167` |  |
| 54 | MUST | ✅ found | The API documentation MUST state that adding attributes at span creation is preferred to calling `SetAttribute` later, as samplers can only consider information already present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os:76` |  |
| 55 | SHOULD | ✅ found | This argument SHOULD only be set when span creation time has already passed. | `src/Трассировка/Классы/ОтелПостроительСпана.os:110` |  |
| 56 | MUST NOT | ✅ found | If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument. | `src/Трассировка/Классы/ОтелПостроительСпана.os:110` |  |
| 57 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span, and MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:97` |  |
| 58 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span, and MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:240` |  |
| 59 | MUST | ✅ found | For a Span with a parent, the `TraceId` MUST be the same as the parent. | `src/Трассировка/Классы/ОтелТрассировщик.os:243` |  |
| 60 | MUST | ✅ found | Also, the child span MUST inherit all `TraceState` values of its parent by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:437` |  |
| 61 | MUST | ✅ found | Any span that is created MUST also be ended. | `src/Трассировка/Классы/ОтелСпан.os:529` |  |

#### Specifying links

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#specifying-links)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 62 | MUST | ✅ found | During `Span` creation, a user MUST have the ability to record links to other `Span`s. | `src/Трассировка/Классы/ОтелПостроительСпана.os:97` |  |

#### Get Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 63 | MUST | ✅ found | The Span interface MUST provide: | `src/Трассировка/Классы/ОтелСпан.os:97` |  |
| 64 | MUST | ✅ found | The returned value MUST be the same for the entire Span lifetime. | `src/Трассировка/Классы/ОтелСпан.os:97` |  |

#### IsRecording

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isrecording)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:294` |  |
| 66 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:294` |  |
| 67 | SHOULD NOT | ✅ found | `IsRecording` SHOULD NOT take any parameters. | `src/Трассировка/Классы/ОтелСпан.os:294` |  |
| 68 | SHOULD | ➖ n_a | This flag SHOULD be used to avoid expensive computations of a Span attributes or events in case when a Span is definitely not recorded. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Флаг предоставлен: ЗаписьАктивна(). |

#### Set Attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | MUST | ✅ found | A `Span` MUST have the ability to set `Attributes` associated with it. | `src/Трассировка/Классы/ОтелСпан.os:328` |  |
| 70 | MUST | ✅ found | The Span interface MUST provide: | `src/Трассировка/Классы/ОтелСпан.os:328` |  |
| 71 | SHOULD | ✅ found | Setting an attribute with the same key as an existing attribute SHOULD overwrite the existing attribute’s value. | `src/Трассировка/Классы/ОтелСпан.os:559` |  |

#### Add Events

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-events)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST | ✅ found | A `Span` MUST have the ability to add events. | `src/Трассировка/Классы/ОтелСпан.os:358` |  |
| 73 | MUST | ✅ found | The Span interface MUST provide: | `src/Трассировка/Классы/ОтелСпан.os:358` |  |
| 74 | SHOULD | ✅ found | Events SHOULD preserve the order in which they are recorded. | `src/Трассировка/Классы/ОтелСпан.os:577` |  |

#### Add Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | MUST | ✅ found | A `Span` MUST have the ability to add `Link`s associated with it after its creation - see Links. | `src/Трассировка/Классы/ОтелСпан.os:433` |  |

#### Set Status

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-status)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 76 | MUST | ✅ found | `Description` MUST only be used with the `Error` `StatusCode` value. | `src/Трассировка/Классы/ОтелСпан.os:507` |  |
| 77 | MUST | ✅ found | The Span interface MUST provide: | `src/Трассировка/Классы/ОтелСпан.os:499` |  |
| 78 | SHOULD | ✅ found | This SHOULD be called `SetStatus`. | `src/Трассировка/Классы/ОтелСпан.os:499` |  |
| 79 | MUST | ✅ found | `Description` MUST be IGNORED for `StatusCode` `Ok` & `Unset` values. | `src/Трассировка/Классы/ОтелСпан.os:507` |  |
| 80 | SHOULD | ✅ found | The status code SHOULD remain unset, except for the following circumstances: | `src/Трассировка/Классы/ОтелСпан.os:499` |  |
| 81 | SHOULD | ✅ found | An attempt to set value `Unset` SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:501` |  |
| 82 | SHOULD | ➖ n_a | When the status is set to `Error` by Instrumentation Libraries, the `Description` SHOULD be documented and predictable. | - | Требование адресовано Instrumentation Libraries (политика их поведения); данный пакет реализует только API+SDK, IL не включены |
| 83 | SHOULD | ➖ n_a | For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish their own conventions, including possible values of `Description` and what they mean. | - | Требование адресовано Instrumentation Libraries (политика их поведения); данный пакет реализует только API+SDK, IL не включены |
| 84 | SHOULD NOT | ➖ n_a | Generally, Instrumentation Libraries SHOULD NOT set the status code to `Ok`, unless explicitly configured to do so. | - | Требование адресовано Instrumentation Libraries (политика их поведения); данный пакет реализует только API+SDK, IL не включены |
| 85 | SHOULD | ➖ n_a | Instrumentation Libraries SHOULD leave the status code as `Unset` unless there is an error, as described above. | - | Требование адресовано Instrumentation Libraries (политика их поведения); данный пакет реализует только API+SDK, IL не включены |
| 86 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:506` |  |
| 87 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:506` |  |
| 88 | SHOULD | ➖ n_a | Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they would otherwise generate. | - | Требование адресовано инструментам анализа (бэкендам), а не API/SDK; данный пакет реализует только API+SDK |

#### End

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#end)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | SHOULD | ✅ found | Implementations SHOULD ignore all subsequent calls to `End` and any other Span methods, i.e. the Span becomes non-recording by being ended (there might be exceptions when Tracer is streaming events and... | `src/Трассировка/Классы/ОтелСпан.os:531` |  |
| 90 | MUST | ✅ found | However, all API implementations of such methods MUST internally call the `End` method and be documented to do so. | `src/Трассировка/Классы/ОтелСпан.os:529` |  |
| 91 | MUST NOT | ✅ found | `End` MUST NOT have any effects on child spans. | `src/Трассировка/Классы/ОтелСпан.os:529` |  |
| 92 | MUST NOT | ✅ found | `End` MUST NOT inactivate the `Span` in any `Context` it is active in. | `src/Трассировка/Классы/ОтелСпан.os:529` |  |
| 93 | MUST | ✅ found | It MUST still be possible to use an ended span as parent via a Context it is contained in. | `src/Трассировка/Классы/ОтелСпан.os:97` |  |
| 94 | MUST | ✅ found | Also, any mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:483` |  |
| 95 | MUST | ✅ found | If omitted, this MUST be treated equivalent to passing the current time. | `src/Трассировка/Классы/ОтелСпан.os:534` |  |
| 96 | MUST NOT | ✅ found | This operation itself MUST NOT perform blocking I/O on the calling thread. | `src/Трассировка/Классы/ОтелСпан.os:529` |  |
| 97 | SHOULD | ✅ found | Any locking used needs be minimized and SHOULD be removed entirely if possible. | `src/Трассировка/Классы/ОтелСпан.os:541` |  |

#### Record Exception

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#record-exception)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | SHOULD | ✅ found | To facilitate recording an exception languages SHOULD provide a `RecordException` method if the language uses exceptions. | `src/Трассировка/Классы/ОтелСпан.os:386` |  |
| 99 | MUST | ✅ found | The method MUST record an exception as an `Event` with the conventions outlined in the exceptions document. | `src/Трассировка/Классы/ОтелСпан.os:386-415` |  |
| 100 | SHOULD | ✅ found | The minimum required argument SHOULD be no more than only an exception object. | `src/Трассировка/Классы/ОтелСпан.os:386` |  |
| 101 | MUST | ✅ found | If `RecordException` is provided, the method MUST accept an optional parameter to provide any additional event attributes (this SHOULD be done in the same way as for the `AddEvent` method). | `src/Трассировка/Классы/ОтелСпан.os:386,409-413` |  |
| 102 | SHOULD | ✅ found | If `RecordException` is provided, the method MUST accept an optional parameter to provide any additional event attributes (this SHOULD be done in the same way as for the `AddEvent` method). | `src/Трассировка/Классы/ОтелСпан.os:358,386` |  |

#### Span lifetime

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-lifetime)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 103 | MUST | ✅ found | Start and end time as well as Event’s timestamps MUST be recorded at a time of a calling of corresponding API. | `src/Трассировка/Классы/ОтелСпан.os:856 (старт), src/Трассировка/Классы/ОтелСпан.os:535 (конец), src/Трассировка/Классы/ОтелСобытиеСпана.os:95 (событие)` |  |

#### Wrapping a SpanContext in a Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#wrapping-a-spancontext-in-a-span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 104 | MUST | ✅ found | The API MUST provide an operation for wrapping a `SpanContext` with an object implementing the `Span` interface. | `src/Трассировка/Модули/ОтелСпаны.os:37` |  |
| 105 | SHOULD NOT | ✅ found | If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type). | `src/Трассировка/Модули/ОтелСпаны.os:1-15,37,55; src/Трассировка/Классы/ОтелНезаписывающийСпан.os:268-276; docs/api/Трассировка/ОтелНезаписывающийСпан.md` |  |
| 106 | SHOULD | ✅ found | If a new type is required to be publicly exposed, it SHOULD be named `NonRecordingSpan`. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os` |  |
| 107 | MUST | ✅ found | `GetContext` MUST return the wrapped `SpanContext`. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:29-31,276-287` |  |
| 108 | MUST | ✅ found | `IsRecording` MUST return `false` to signal that events, attributes and other elements are not being recorded, i.e. they are being dropped. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:155-157` |  |
| 109 | MUST | ✅ found | The remaining functionality of `Span` MUST be defined as no-op operations. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:167-262` |  |
| 110 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Модули/ОтелСпаны.os:37-62; src/Трассировка/Классы/ОтелНезаписывающийСпан.os` |  |
| 111 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os` |  |

#### SpanKind

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 112 | SHOULD | ➖ n_a | In order for `SpanKind` to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. |
| 113 | SHOULD NOT | ➖ n_a | For example, a server-side span SHOULD NOT be used to describe outgoing remote procedure call. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. |

#### Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 114 | MUST | ✅ found | A user MUST have the ability to record links to other `SpanContext`s. | `src/Трассировка/Классы/ОтелСпан.os:433; src/Трассировка/Классы/ОтелПостроительСпана.os:97` |  |
| 115 | MUST | ✅ found | The API MUST provide: | `src/Трассировка/Классы/ОтелСпан.os:433-463` |  |
| 116 | SHOULD | ✅ found | Implementations SHOULD record links containing `SpanContext` with empty `TraceId` or `SpanId` (all zeros) as long as either the attribute set or `TraceState` is non-empty. | `src/Трассировка/Классы/ОтелСпан.os:438-445,623-626` |  |
| 117 | SHOULD | ✅ found | Span SHOULD preserve the order in which `Link`s are set. | `src/Трассировка/Классы/ОтелСпан.os:597-612` |  |
| 118 | MUST | ✅ found | The API documentation MUST state that adding links at span creation is preferred to calling `AddLink` later, for contexts that are available during span creation, because head sampling decisions can on... | `src/Трассировка/Классы/ОтелСпан.os:420-425; src/Трассировка/Классы/ОтелПостроительСпана.os:85-88` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 119 | MUST | ✅ found | TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:7` |  |
| 120 | MUST | ✅ found | Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:3-4` |  |
| 121 | MUST | ✅ found | Span - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:5-6` |  |
| 122 | MUST | ✅ found | Event - Events are immutable and MUST be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСобытиеСпана.os:3` |  |
| 123 | SHOULD | ✅ found | Link - Links are immutable and SHOULD be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелЛинк.os:6-12` |  |

#### Behavior of the API in the absence of an installed SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#behavior-of-the-api-in-the-absence-of-an-installed-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 124 | MUST | ✅ found | The API MUST return a non-recording `Span` with the `SpanContext` in the parent `Context` (whether explicitly given or implicit current). | `src/Трассировка/Классы/ОтелТрассировщик.os:170-181,331-332; src/Трассировка/Модули/ОтелСпаны.os:37-45` |  |
| 125 | SHOULD | ✅ found | If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly without instantiating a new `Span`. | `src/Трассировка/Классы/ОтелТрассировщик.os:177-179` |  |
| 126 | MUST | ✅ found | If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.e., having a `SpanContext` with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags). | `src/Трассировка/Классы/ОтелТрассировщик.os:100-102,170-181; src/Трассировка/Модули/ОтелСпаны.os:37-62` |  |

### Trace Sdk

#### Tracer Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ➖ n_a | It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` (see API). | `src/Трассировка/Классы/ОтелТрассировщик.os:393` | OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен). Штатный путь создания - ОтелПровайдерТрассировки.ПолучитьТрассировщик / ОтелПостроительТрассировщика. |
| 2 | MUST | ✅ found | The `TracerProvider` MUST implement the Get a Tracer API. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:60` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Tracer`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:73` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | Configuration ( i.e., SpanProcessors, IdGenerator, SpanLimits, `Sampler`, and (Development) TracerConfigurator) MUST be owned by the `TracerProvider`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:358` |  |
| 5 | MUST | ✅ found | If configuration is updated (e.g., adding a `SpanProcessor`), the updated configuration MUST also apply to all already returned `Tracers` (i.e. it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvider` before or after the configuration change). | `src/Трассировка/Классы/ОтелТрассировщик.os:239` |  |
| 6 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `SpanProcessor`), the updated configuration MUST also apply to all already returned `Tracers` (i.e. it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvider` before or after the configuration change). | `src/Трассировка/Классы/ОтелТрассировщик.os:239` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | `Shutdown` MUST be called only once for each `TracerProvider` instance. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:143` |  |
| 8 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op Tracer for these calls, if possible. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:75` |  |
| 9 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:143` |  |
| 10 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:143` |  |
| 11 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:149` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:130` |  |
| 13 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:130` |  |
| 14 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered `SpanProcessors`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:316` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | `Enabled` MUST return `false` when either: * there are no registered `SpanProcessors`,* Status: Development - `Tracer` is disabled (`TracerConfig.enabled` is `false`). | `src/Трассировка/Классы/ОтелТрассировщик.os:54` |  |
| 16 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:54` |  |

#### Additional Span Interfaces

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#additional-span-interfaces)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | Readable span: A function receiving this as argument MUST be able to access all information that was added to the span, as listed in the API spec for Span. | `src/Трассировка/Классы/ОтелСпан.os:88` |  |
| 18 | MUST | ✅ found | A function receiving this as argument MUST be able to access the `InstrumentationScope` [since 1.10.0] and `Resource` information (implicitly) associated with the span. | `src/Трассировка/Классы/ОтелСпан.os:208` |  |
| 19 | MUST | ✅ found | For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated since 1.10.0] having the same name and version values as the `InstrumentationScope`. | `src/Трассировка/Классы/ОтелСпан.os:230` |  |
| 20 | MUST | ✅ found | A function receiving this as argument MUST be able to reliably determine whether the Span has ended (some languages might implement this by having an end timestamp of `null`, others might have an explici... | `src/Трассировка/Классы/ОтелСпан.os:257` |  |
| 21 | MUST | ✅ found | Counts for attributes, events and links dropped due to collection limits MUST be available for exporters to report as described in the exporters specification. | `src/Трассировка/Классы/ОтелСпан.os:266` |  |
| 22 | MUST | ✅ found | As an exception to the authoritative set of span properties defined in the API spec, implementations MAY choose not to expose (and store) the full parent Context of the Span but they MUST expose at lea... | `src/Трассировка/Классы/ОтелСпан.os:118` |  |
| 23 | MUST | ✅ found | It MUST be possible for functions being called with this to somehow obtain the same `Span` instance and type that the span creation API returned (or will return) to the user (for example, the `Span` c... | `src/Трассировка/Классы/ОтелСпан.os:545` |  |

#### Sampling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | Span Processor MUST receive only those spans which have this field set to `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:244` |  |
| 25 | SHOULD NOT | ✅ found | However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:50` |  |
| 26 | MUST | ✅ found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:32` |  |
| 27 | SHOULD NOT | ✅ found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:32` |  |
| 28 | MUST NOT | ✅ found | The flag combination `SampledFlag == true` and `IsRecording == false` could cause gaps in the distributed trace, and because of this the OpenTelemetry SDK MUST NOT allow this combination. | `src/Трассировка/Классы/ОтелТрассировщик.os:245` |  |

#### SDK Span creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sdk-span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | MUST | ✅ found | When asked to create a Span, the SDK MUST act as if doing the following in order: | `src/Трассировка/Классы/ОтелТрассировщик.os:226` |  |

#### ShouldSample

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shouldsample)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | If the parent `SpanContext` contains a valid `TraceId`, they MUST always match. | `src/Трассировка/Классы/ОтелТрассировщик.os:232` |  |
| 31 | MUST NOT | ✅ found | * `RECORD_ONLY` - `IsRecording` will be `true`, but the `Sampled` flag MUST NOT be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:413` |  |
| 32 | MUST | ✅ found | * `RECORD_AND_SAMPLE` - `IsRecording` will be `true` and the `Sampled` flag MUST be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:415` |  |
| 33 | SHOULD | ✅ found | If the sampler returns an empty `Tracestate` here, the `Tracestate` will be cleared, so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend to change it. | `src/Трассировка/Классы/ОтелСэмплерВсегдаВключен.os:24` |  |

#### GetDescription

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#getdescription)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | SHOULD NOT | ✅ found | Callers SHOULD NOT cache the returned value. | `src/Трассировка/Классы/ИнтерфейсСэмплер.os:36` |  |

#### AlwaysOn

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwayson)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | MUST | ✅ found | Description MUST be `AlwaysOnSampler`. | `src/Трассировка/Классы/ОтелСэмплерВсегдаВключен.os:34` |  |

#### AlwaysOff

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwaysoff)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | Description MUST be `AlwaysOffSampler`. | `src/Трассировка/Классы/ОтелСэмплерВсегдаВыключен.os:34` |  |

#### TraceIdRatioBased

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#traceidratiobased)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | MUST | ✅ found | The `TraceIdRatioBased` MUST ignore the parent `SampledFlag`. | `src/Трассировка/Классы/ОтелСэмплерПоДолеТрассировок.os:43` |  |
| 38 | MUST | ✅ found | Description MUST return a string of the form `"TraceIdRatioBased{RATIO}"` with `RATIO` replaced with the Sampler instance’s trace sampling ratio represented as a decimal number. | `src/Трассировка/Классы/ОтелСэмплерПоДолеТрассировок.os:57` |  |
| 39 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Классы/ОтелСэмплерПоДолеТрассировок.os:57` |  |
| 40 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Классы/ОтелСэмплерПоДолеТрассировок.os:57` |  |

#### Requirements for `TraceIdRatioBased` sampler algorithm

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#requirements-for-traceidratiobased-sampler-algorithm)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 41 | MUST | ✅ found | The sampling algorithm MUST be deterministic. | `src/Трассировка/Классы/ОтелСэмплерПоДолеТрассировок.os:68` |  |
| 42 | MUST | ✅ found | To achieve this, implementations MUST use a deterministic hash of the `TraceId` when computing the sampling decision. | `src/Трассировка/Классы/ОтелСэмплерПоДолеТрассировок.os:68` |  |
| 43 | MUST | ✅ found | A `TraceIdRatioBased` sampler with a given sampling probability MUST also sample all traces that any `TraceIdRatioBased` sampler with a lower sampling probability would sample. | `src/Трассировка/Классы/ОтелСэмплерПоДолеТрассировок.os:68` |  |

#### AlwaysRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwaysrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 44 | MUST | ✅ found | Based on the decision from the wrapped root sampler, `AlwaysRecord` MUST behave as follows: | `src/Трассировка/Классы/ОтелСэмплерВсегдаЗаписывать.os:29` |  |

#### Span Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST | ✅ found | Span attributes MUST adhere to the common rules of attribute limits. | `src/Трассировка/Классы/ОтелСпан.os:884` |  |
| 46 | MUST | ✅ found | If the SDK implements the limits above it MUST provide a way to change these limits, via a configuration to the TracerProvider, by allowing users to configure individual limits like in the Java example bellow. | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:69` |  |
| 47 | SHOULD | ✅ found | The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:121` |  |
| 48 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `SpanLimits`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:1` |  |
| 49 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK’s log to indicate to the user that an attribute, event, or link was discarded due to such a limit. | `src/Трассировка/Классы/ОтелСпан.os:631` |  |
| 50 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per discarded attribute, event, or link). | `src/Трассировка/Классы/ОтелСпан.os:632` |  |

#### ID Generators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#id-generators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 51 | MUST | ✅ found | The SDK MUST by default randomly generate both the `TraceId` and the `SpanId`. | `src/Ядро/Модули/ОтелУтилиты.os:96` |  |
| 52 | MUST | ✅ found | The SDK MUST provide a mechanism for customizing the way IDs are generated for both the `TraceId` and the `SpanId`. | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:88` |  |
| 53 | MUST | ✅ found | The SDK MAY provide this functionality by allowing custom implementations of an interface like the Java example below (name of the interface MAY be `IdGenerator`, name of the methods MUST be consistent with Sp... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:257` |  |
| 54 | MUST NOT | ✅ found | Additional `IdGenerator` implementing vendor-specific protocols such as AWS X-Ray trace ID generator MUST NOT be maintained or distributed as part of the OpenTelemetry Core packages. | `src/Ядро/Модули/ОтелУтилиты.os:96` |  |

#### Span processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | MUST | ✅ found | SDK MUST allow to end each pipeline with individual exporter. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:143` |  |
| 56 | MUST | ✅ found | SDK MUST allow users to implement and configure custom processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:107` |  |

#### Interface definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 57 | MUST | ✅ found | The `SpanProcessor` interface MUST declare the following methods: | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11` |  |

#### OnStart

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onstart)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 58 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ОтелСпан.os:907` |  |
| 59 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ОтелСпан.os:907` |  |

#### OnEnd(Span)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onendspan)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | MUST | ✅ found | This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:545` |  |

#### Shutdown()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `SpanProcessor` instance. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:96` |  |
| 62 | SHOULD | ✅ found | SDKs SHOULD ignore these calls gracefully, if possible. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:47` |  |
| 63 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:41` |  |
| 64 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95` |  |
| 65 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95` |  |

#### ForceFlush()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `Spans` for which the `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, prefe... | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79` |  |
| 67 | SHOULD | ✅ found | In particular, if any `SpanProcessor` has any associated exporter, it SHOULD try to call the exporter’s `Export` with all spans for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191` |  |
| 68 | MUST | ✅ found | The built-in SpanProcessors MUST do so. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:79` |  |
| 69 | MUST | ✅ found | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191` |  |
| 70 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:28` |  |
| 71 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `SpanProcessor` exp... | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. |
| 72 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79` |  |

#### Built-in span processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#built-in-span-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:143; src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:60` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 74 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:57-64,146` |  |

#### Batching processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#batching-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:231-252` |  |
| 76 | SHOULD | ✅ found | The processor SHOULD export a batch when any of the following happens AND the previous export call has returned: | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:168-174,351-368,79-81` |  |

#### Span Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 77 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:6-7` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | MUST | ✅ found | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:14,26,35; src/Экспорт/Классы/ОтелЭкспортерСпанов.os:36,65,76` |  |

#### `Export(batch)`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 79 | MUST NOT | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:36-54 (таймаут по умолчанию 10000 мс, оставшееся время передается транспорту; Ложь при сбое)` |  |
| 80 | MUST | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:36-54,112` |  |
| 81 | SHOULD NOT | ✅ found | The default SDK’s Span Processors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the spans are being sent to. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:263-279; src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:58-63` |  |

#### `ForceFlush()`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 82 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Spans` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:65-68 (экспорт синхронный, буфера нет); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217` |  |
| 83 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:65 (возвращает ОтелРезультатЭкспорта: успех/ошибка/таймаут)` |  |
| 84 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed spans. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. |
| 85 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:65 (параметр ТаймаутМс); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-217 (срок соблюдается)` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 86 | MUST | ✅ found | Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:60-100,377-378` |  |
| 87 | MUST | ✅ found | Sampler - `ShouldSample` and `GetDescription` MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелСэмплерПоДолеТрассировок.os:43-57 (встроенные сэмплеры неизменяемы после конструктора)` |  |
| 88 | MUST | ✅ found | Span processor - all methods MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-69,98,155; src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:47-104` |  |
| 89 | MUST | ✅ found | Span Exporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:65-81,119` |  |

### Logs Api

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `LoggerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:147` |  |

#### LoggerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `LoggerProvider` MUST provide the following functions: | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:60` |  |

#### Get a Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#get-a-logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following instrumentation scope parameters: | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:58` |  |
| 4 | MUST | ✅ found | This API MUST be structured to accept a variable number of attributes, including none. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:58` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The `Logger` MUST provide a function to: | `src/Логирование/Классы/ОтелЛоггер.os:99` |  |
| 6 | SHOULD | ✅ found | The `Logger` SHOULD provide functions to: | `src/Логирование/Классы/ОтелЛоггер.os:58` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:99` |  |
| 8 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:99` |  |
| 9 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:104` |  |
| 10 | SHOULD | ✅ found | When only explicit Context is supported, this parameter SHOULD be required. | `src/Логирование/Классы/ОтелЛоггер.os:99` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when generating a `LogRecord`, a `Logger` SHOULD provide this `Enabled` API. | `src/Логирование/Классы/ОтелЛоггер.os:58` |  |
| 12 | SHOULD | ✅ found | The API SHOULD accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:58` |  |
| 13 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:59` |  |
| 14 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:73` |  |
| 15 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Логирование/Классы/ОтелЛоггер.os:64` |  |
| 16 | SHOULD | ✅ found | The API documentation SHOULD state that calling `Enabled` is optional and is not required before emitting a `LogRecord`. | `src/Логирование/Классы/ОтелЛоггер.os:27` |  |
| 17 | SHOULD | ✅ found | The documentation SHOULD also state that the returned value is not static and can change over time, so a cached value can become stale. | `src/Логирование/Классы/ОтелЛоггер.os:35` |  |

#### Optional and required parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#optional-and-required-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:58` |  |
| 19 | MUST NOT | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:99` |  |
| 20 | MUST | ✅ found | For each required parameter, the API MUST be structured to obligate a user to provide it. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:58` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | LoggerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:9` |  |
| 22 | MUST | ✅ found | Logger - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелЛоггер.os:33` |  |

### Logs Sdk

#### Logs SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logs-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:259` |  |

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A `LoggerProvider` MUST provide a way to allow a Resource to be specified. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:259` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the `LogRecord`s produced by any `Logger` from the `LoggerProvider`. | `src/Логирование/Классы/ОтелЛоггер.os:101` |  |

#### LoggerProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `LoggerProviders`s. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:259` |  |

#### Logger Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | SHOULD | ➖ n_a | It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` (see API). | `src/Логирование/Классы/ОтелЛоггер.os:255` | OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен); штатный путь создания - ОтелПровайдерЛогирования.ПолучитьЛоггер/ПостроительЛоггера. |
| 6 | MUST | ✅ found | The `LoggerProvider` MUST implement the Get a Logger API. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:58` |  |
| 7 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Logger`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:73` |  |
| 8 | MUST | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:63` |  |
| 9 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:73` |  |
| 10 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:64` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | Configuration (i.e. LogRecordProcessors and (Development) LoggerConfigurator) MUST be owned by the `LoggerProvider`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:273` |  |
| 12 | MUST | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained from the `LoggerProvider` before or after the configuration change). | `src/Логирование/Классы/ОтелЛоггер.os:123` |  |
| 13 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained from the `LoggerProvider` before or after the configuration change). | `src/Логирование/Классы/ОтелЛоггер.os:123` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | `Shutdown` MUST be called only once for each `LoggerProvider` instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:139` |  |
| 15 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op `Logger` for these calls, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:68` |  |
| 16 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:138` |  |
| 17 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:138` |  |
| 18 | MUST | ✅ found | `Shutdown` MUST be implemented by invoking `Shutdown` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:145` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:124` |  |
| 20 | SHOULD | ✅ found | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:124` |  |
| 21 | SHOULD | ✅ found | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:125` |  |
| 22 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:124` |  |
| 23 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:240` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | SHOULD | ✅ found | If Observed Timestamp is unspecified, the implementation SHOULD set it equal to the current time. | `src/Логирование/Классы/ОтелЛоггер.os:119` |  |
| 25 | MUST | ✅ found | If an Exception is provided, the SDK MUST by default set attributes from the exception on the `LogRecord` with the conventions outlined in the exception semantic conventions. | `src/Логирование/Классы/ОтелЛоггер.os:190` |  |
| 26 | MUST | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:206` |  |
| 27 | MUST NOT | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:206` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | `Enabled` MUST return `false` when either: | `src/Логирование/Классы/ОтелЛоггер.os:77` |  |
| 29 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:85` |  |

#### ReadableLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readablelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | A function receiving this as an argument MUST be able to access all the information added to the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:56` |  |
| 31 | MUST | ✅ found | It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) associated with the `LogRecord`. | `src/Логирование/Классы/ОтелЗаписьЛога.os:141` |  |
| 32 | MUST | ✅ found | The trace context fields MUST be populated from the resolved `Context` (either the explicitly passed `Context` or the current `Context`) when emitted. | `src/Логирование/Классы/ОтелЛоггер.os:99` |  |
| 33 | MUST | ✅ found | Counts for attributes due to collection limits MUST be available for exporters to report as described in the transformation to non-OTLP formats specification. | `src/Логирование/Классы/ОтелЗаписьЛога.os:159` |  |

#### ReadWriteLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readwritelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | MUST | ✅ found | A function receiving this as an argument MUST additionally be able to modify the following information added to the LogRecord: | `src/Логирование/Классы/ОтелЗаписьЛога.os:246` |  |

#### LogRecord Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecord-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | MUST | ✅ found | `LogRecord` attributes MUST adhere to the common rules of attribute limits. | `src/Логирование/Классы/ОтелЗаписьЛога.os:246` |  |
| 36 | MUST | ✅ found | If the SDK implements attribute limits it MUST provide a way to change these limits, via a configuration to the `LoggerProvider`, by allowing users to configure individual limits like in the Java example below. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:50` |  |
| 37 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `LogRecordLimits`. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os` |  |
| 38 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK’s log to indicate to the user that an attribute was discarded due to such a limit. | `src/Логирование/Классы/ОтелЗаписьЛога.os:414` |  |
| 39 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per `LogRecord` (i.e., not per discarded attribute). | `src/Логирование/Классы/ОтелЗаписьЛога.os:414` |  |

#### LogRecordProcessor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 40 | MUST | ✅ found | The SDK MUST allow each pipeline to end with an individual exporter. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os` |  |
| 41 | MUST | ✅ found | The SDK MUST allow users to implement and configure custom processors and decorate built-in processors for advanced scenarios such as enriching with attributes. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:36` |  |

#### OnEmit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#onemit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 42 | SHOULD NOT | ✅ found | This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD NOT block or throw exceptions. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48` |  |
| 43 | MUST | ✅ found | For a `LogRecordProcessor` registered directly on SDK `LoggerProvider`, the `logRecord` mutations MUST be visible in next registered processors. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:21` |  |
| 44 | SHOULD | ✅ found | To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecord` be used for any concurrent processing, such as in a batching processor. | `src/Логирование/Классы/ОтелПакетныйПроцессорЛогов.os:13` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST NOT | ✅ found | Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:85` |  |

#### ShutDown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:111` |  |
| 47 | SHOULD | ✅ found | SDKs SHOULD ignore these calls gracefully, if possible. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:40` |  |
| 48 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:60` |  |
| 49 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95` |  |
| 50 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 51 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `LogRecord`s for which the `LogRecordProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79` |  |
| 52 | SHOULD | ✅ found | In particular, if any `LogRecordProcessor` has any associated exporter, it SHOULD try to call the exporter’s `Export` with all `LogRecord`s for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191` |  |
| 53 | MUST | ✅ found | The built-in LogRecordProcessors MUST do so. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191` |  |
| 54 | MUST | ✅ found | If a timeout is specified (see below), the `LogRecordProcessor` MUST prioritize honoring the timeout over finishing all calls. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191` |  |
| 55 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79` |  |
| 56 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `LogRecordProcessor` exports the emitted `LogRecord`s. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение |
| 57 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79` |  |

#### Built-in processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#built-in-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 58 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:166` |  |
| 59 | SHOULD | ➖ n_a | Other common processing scenarios SHOULD be first considered for implementation out-of-process in OpenTelemetry Collector. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение |
| 60 | SHOULD | ✅ found | Additional processors defined in this document SHOULD be provided by SDK packages. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:181` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:46` |  |

#### Batching processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#batching-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 62 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:231` |  |

#### LogRecordExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 63 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:5` |  |

#### LogRecordExporter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 64 | MUST | ✅ found | A `LogRecordExporter` MUST support the following functions: | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:37` |  |

#### Export

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#export)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | MUST NOT | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:37` |  |
| 66 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47` |  |
| 67 | SHOULD NOT | ✅ found | The default SDK’s `LogRecordProcessors` SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the logs are being sent to. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:34` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | This is a hint to ensure that the export of any `ReadableLogRecords` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:66` |  |
| 69 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:66` |  |
| 70 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the `ReadlableLogRecords`. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение |
| 71 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:66` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each `LogRecordExporter` instance. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:77` |  |
| 73 | SHOULD | ✅ found | After the call to `Shutdown` subsequent calls to `Export` are not allowed and SHOULD return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38` |  |
| 74 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:77` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | MUST | ✅ found | LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:81` |  |
| 76 | MUST | ✅ found | Logger - all methods MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелЛоггер.os:99` |  |
| 77 | MUST | ✅ found | LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:77` |  |

### Metrics Api

#### MeterProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `MeterProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:175` |  |

#### MeterProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `MeterProvider` MUST provide the following functions: | `src/Метрики/Классы/ОтелПровайдерМетрик.os:80` |  |

#### Get a Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#get-a-meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Метрики/Классы/ОтелПровайдерМетрик.os:76` |  |
| 4 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:76` |  |
| 5 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:76` |  |
| 6 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:76` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ found | Note: `Meter` SHOULD NOT be responsible for the configuration. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:111` |  |

#### Meter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The `Meter` MUST provide functions to create new Instruments: | `src/Метрики/Классы/ОтелМетр.os:83` |  |

#### Instrument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ✅ found | Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying. | `src/Метрики/Классы/ОтелМетр.os:1243` |  |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | SHOULD | ✅ found | The API SHOULD treat it as an opaque string. | `src/Метрики/Классы/ОтелМетр.os:1140` |  |
| 11 | MUST | ✅ found | It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII string. | `src/Метрики/Классы/ОтелМетр.os:628` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST treat it as an opaque string. | `src/Метрики/Классы/ОтелМетр.os:1140` |  |
| 13 | MUST | ✅ found | It MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or `utf8mb3`). | `src/Метрики/Классы/ОтелМетр.os:1140` |  |
| 14 | MUST | ✅ found | It MUST support at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:1140` |  |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | OpenTelemetry SDKs MUST handle `advisory` parameters as described here. | `src/Метрики/Классы/ОтелМетр.os:1658` |  |

#### Synchronous Instrument API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#synchronous-instrument-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The API to construct synchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:83` |  |
| 17 | SHOULD | ✅ found | If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:83` |  |
| 18 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:63` |  |
| 19 | SHOULD | ✅ found | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:63` |  |
| 20 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`; that is left to implementations of the API, like the SDK. | `src/Метрики/Классы/ОтелМетр.os:1161` |  |
| 21 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:83` |  |
| 22 | MUST | ✅ found | Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелМетр.os:1140` |  |
| 23 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:622` |  |
| 24 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:83` |  |
| 25 | MUST | ✅ found | Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:1140` |  |
| 26 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:83` |  |
| 27 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:1658` |  |

#### Asynchronous Instrument API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-instrument-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | The API to construct asynchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:163` |  |
| 29 | SHOULD | ✅ found | If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:163` |  |
| 30 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:63` |  |
| 31 | SHOULD | ✅ found | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:63` |  |
| 32 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`, that is left to implementations of the API. | `src/Метрики/Классы/ОтелМетр.os:1161` |  |
| 33 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:163` |  |
| 34 | MUST | ✅ found | Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелМетр.os:1140` |  |
| 35 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:663` |  |
| 36 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:163` |  |
| 37 | MUST | ✅ found | Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:1140` |  |
| 38 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:163` |  |
| 39 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:1658` |  |
| 40 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of `callback` functions, including none. | `src/Метрики/Классы/ОтелМетр.os:163` |  |
| 41 | MUST | ✅ found | The API MUST support creation of asynchronous instruments by passing zero or more `callback` functions to be permanently registered to the newly created instrument. | `src/Метрики/Классы/ОтелМетр.os:663` |  |
| 42 | SHOULD | ✅ found | The API SHOULD support registration of `callback` functions associated with asynchronous instruments after they are created. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:127` |  |
| 43 | MUST | ✅ found | Where the API supports registration of `callback` functions after asynchronous instrumentation creation, the user MUST be able to undo registration of the specific callback after its registration by so... | `src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os:11` |  |
| 44 | MUST | ✅ found | Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:412` |  |
| 45 | MUST | ✅ found | Callback functions MUST be documented as follows for the end user: | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:106` |  |
| 46 | SHOULD | ✅ found | Callback functions SHOULD be reentrant safe. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:110` |  |
| 47 | SHOULD NOT | ✅ found | Callback functions SHOULD NOT take an indefinite amount of time. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:112` |  |
| 48 | SHOULD NOT | ✅ found | Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same `attributes`) across all registered callbacks. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:114` |  |
| 49 | MUST | ✅ found | Callbacks registered at the time of instrument creation MUST apply to the single instruments which is under construction. | `src/Метрики/Классы/ОтелМетр.os:663` |  |
| 50 | MUST | ✅ found | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the instrument associated with each observed `Measurement` value. | `src/Метрики/Классы/ОтелМетр.os:527` |  |
| 51 | MUST | ✅ found | Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of asynchronous instruments from the same `Meter` instance. | `src/Метрики/Классы/ОтелМетр.os:527` |  |
| 52 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timest... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:428` |  |
| 53 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timest... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` |  |
| 54 | SHOULD | ✅ found | The API SHOULD provide some way to pass `state` to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:127` |  |

#### General operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD | ✅ found | All synchronous instruments SHOULD provide functions to: Report if instrument is `Enabled` | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:251` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 56 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when recording measurements, synchronous instruments SHOULD provide this `Enabled` API. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:251` |  |
| 57 | MUST | ✅ found | Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:251` |  |
| 58 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` |  |
| 59 | SHOULD | ✅ found | The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:241` |  |

#### Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating a `Counter` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:83` | OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен), поэтому запретить прямое создание ОтелСчетчик через Новый нельзя; штатный путь создания - ОтелМетр.СоздатьСчетчик. |

#### Add

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#add)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелСчетчик.os:38` |  |
| 62 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелСчетчик.os:38` |  |
| 63 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелСчетчик.os:38` |  |
| 64 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелСчетчик.os:20` |  |
| 65 | SHOULD | ✅ found | This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелСчетчик.os:20` |  |
| 66 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелСчетчик.os:39` |  |
| 67 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелСчетчик.os:38` |  |
| 68 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелСчетчик.os:38` |  |

#### Asynchronous Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating an Asynchronous Counter other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:163` | Штатный путь создания - только ОтелМетр.СоздатьНаблюдаемыйСчетчик; OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен), поэтому запретить прямой Новый ОтелНаблюдаемыйСчетчик невозможно. Ограничение платформы. |
| 70 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:412` |  |
| 71 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:431` |  |
| 72 | SHOULD | ✅ found | The API SHOULD provide some way to pass `state` to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:127` |  |

#### Histogram creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#histogram-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating a `Histogram` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:99` | Штатный путь создания - только ОтелМетр.СоздатьГистограмму; OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен), поэтому запретить прямой Новый ОтелГистограмма невозможно. Ограничение платформы. |

#### Record

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#record)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 74 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелГистограмма.os:32` |  |
| 75 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелГистограмма.os:32` |  |
| 76 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелГистограмма.os:32` |  |
| 77 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелГистограмма.os:13` |  |
| 78 | SHOULD | ✅ found | This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелГистограмма.os:15` |  |
| 79 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелГистограмма.os:33` |  |
| 80 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелГистограмма.os:32` |  |

#### Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 81 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating a `Gauge` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:129` | Штатный путь создания - только ОтелМетр.СоздатьДатчик; OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен), поэтому запретить прямой Новый ОтелДатчик невозможно. Ограничение платформы. |

#### Record

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#record)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 82 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 83 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 84 | SHOULD | ✅ found | The value needs to be provided by a user. If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 85 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелДатчик.os:13` |  |
| 86 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 87 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |

#### Asynchronous Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 88 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating an Asynchronous Gauge other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:234` | Штатный путь создания - только ОтелМетр.СоздатьНаблюдаемыйДатчик; OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен), поэтому запретить прямой Новый ОтелНаблюдаемыйДатчик невозможно. Ограничение платформы. |

#### UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | MUST NOT | ✅ found | There MUST NOT be any API for creating an `UpDownCounter` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:114` |  |

#### Add

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#add)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:19` |  |
| 91 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:19` |  |
| 92 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:19` |  |
| 93 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:12-18` |  |
| 94 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:19` |  |

#### Asynchronous UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 95 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:199` |  |

#### Multiple-instrument callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#multiple-instrument-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: | `src/Метрики/Классы/ОтелМетр.os:527` |  |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | SHOULD | ✅ found | All the metrics components SHOULD allow new APIs to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелМетр.os` |  |
| 98 | SHOULD | ✅ found | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелМетр.os:114` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 99 | MUST | ✅ found | MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:41` |  |
| 100 | MUST | ✅ found | Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелМетр.os:61` |  |
| 101 | MUST | ✅ found | Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:33` |  |

### Metrics Sdk

#### Metrics SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metrics-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:1` |  |

#### MeterProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A `MeterProvider` MUST provide a way to allow a Resource to be specified. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:455` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the metrics produced by any `Meter` from the `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:109` |  |

#### MeterProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `MeterProvider`s. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:455` |  |

#### Meter Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | SHOULD | ➖ n_a | It SHOULD only be possible to create `Meter` instances through a `MeterProvider` (see API). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:76` | OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен); штатный путь создания - ОтелПровайдерМетрик.ПолучитьМетр / ПостроительМетра. |
| 6 | MUST | ✅ found | The `MeterProvider` MUST implement the Get a Meter API. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:76` |  |
| 7 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:81` |  |
| 8 | MUST | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:87` |  |
| 9 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:81` |  |
| 10 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:88` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | Configuration ( i.e. MetricExporters, MetricReaders, Views, and (Development) MeterConfigurator and (Development) view_matching_mode) MUST be owned by the `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:455` |  |
| 12 | MUST | ✅ found | If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the `MeterProvider` before or after the configuration change). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:272` |  |
| 13 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the `MeterProvider` before or after the configuration change). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:286` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MeterProvider` instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:194` |  |
| 15 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op Meter for these calls, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:92` |  |
| 16 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:194` |  |
| 17 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:194` |  |
| 18 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered MetricReader and MetricExporter instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:210` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered MetricReader instances that implement `ForceFlush`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:380` |  |
| 20 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:182` |  |
| 21 | SHOULD | ✅ found | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:182` |  |
| 22 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:182` |  |

#### View

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | MUST | ✅ found | The SDK MUST provide functionality for a user to create Views for a `MeterProvider`. | `src/Метрики/Классы/ОтелПредставление.os:1` |  |
| 24 | MUST | ✅ found | This functionality MUST accept as inputs the Instrument selection criteria and the resulting stream configuration. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:272` |  |
| 25 | MUST | ✅ found | The SDK MUST provide the means to register Views with a `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:272` |  |

#### Instrument selection criteria

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-selection-criteria)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | SHOULD | ✅ found | Criteria SHOULD be treated as additive. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37` |  |
| 27 | MUST | ✅ found | The SDK MUST accept the following criteria: | `src/Метрики/Классы/ОтелСелекторИнструментов.os:163` |  |
| 28 | MUST | ✅ found | If the SDK does not support wildcards in general, it MUST still recognize the special single asterisk (`*`) character as matching all Instruments. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:40` |  |
| 29 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:163` |  |
| 30 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `type`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:163` |  |
| 31 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:163` |  |
| 32 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:163` |  |
| 33 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:163` |  |
| 34 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:163` |  |
| 35 | MUST NOT | ✅ found | Therefore, the instrument selection criteria can be structured to accept the criteria, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:163` |  |

#### Stream configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#stream-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | The SDK MUST accept the following stream configuration parameters: | `src/Метрики/Классы/ОтелПредставление.os:162` |  |
| 37 | SHOULD | ✅ found | `name`: The metric stream name that SHOULD be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:319` |  |
| 38 | SHOULD | ✅ found | In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector that selects at most one instrument. | `src/Метрики/Классы/ОтелМетр.os:937` |  |
| 39 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:162` |  |
| 40 | MUST | ✅ found | If the user does not provide a `name` value, name from the Instrument the View matches MUST be used by default. | `src/Метрики/Модули/ОтелПотокиМетрик.os:251` |  |
| 41 | MUST NOT | ✅ found | The `name` provided via stream configuration is NOT REQUIRED to conform to the instrument name syntax, and the SDK MUST NOT validate it against that syntax. | `src/Метрики/Модули/ОтелПотокиМетрик.os:319` |  |
| 42 | SHOULD | ✅ found | `description`: The metric stream description that SHOULD be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:319` |  |
| 43 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:162` |  |
| 44 | MUST | ✅ found | If the user does not provide a `description` value, the description from the Instrument a View matches MUST be used by default. | `src/Метрики/Модули/ОтелПотокиМетрик.os:251` |  |
| 45 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:55` |  |
| 46 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:55` |  |
| 47 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept `attribute_keys`, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелПредставление.os:162` |  |
| 48 | MUST | ✅ found | If the `Attributes` advisory parameter is absent, all attributes MUST be kept. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:30` |  |
| 49 | SHOULD | ✅ found | Additionally, implementations SHOULD support configuring an exclude-list of attribute keys. | `src/Метрики/Классы/ОтелПредставление.os:168` |  |
| 50 | MUST | ✅ found | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:55` |  |
| 51 | MUST | ✅ found | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:55` |  |
| 52 | SHOULD | ✅ found | SDK documentation SHOULD inform users that attributes excluded from a metric stream by View configuration may still be exported on Exemplars as filtered attributes, and describe how to disable or otherwise configure ... | `src/Метрики/Классы/ОтелПредставление.os:142` |  |
| 53 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept an `aggregation`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:162` |  |
| 54 | MUST | ✅ found | If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance. | `src/Метрики/Модули/ОтелПотокиМетрик.os:359` |  |
| 55 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept an `exemplar_reservoir`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:162` |  |
| 56 | MUST | ✅ found | If the user does not provide an `exemplar_reservoir` value, the `MeterProvider` MUST apply a default exemplar reservoir. | `src/Метрики/Модули/ОтелПотокиМетрик.os:454` |  |
| 57 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept an `aggregation_cardinality_limit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:162` |  |
| 58 | MUST | ✅ found | If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST apply the default aggregation cardinality limit the `MetricReader` is configured with. | `src/Метрики/Модули/ОтелПотокиМетрик.os:439` |  |

#### Measurement processing

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#measurement-processing)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | SHOULD | ✅ found | The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument: | `src/Метрики/Модули/ОтелПотокиМетрик.os:211` |  |
| 60 | MUST | ✅ found | Instrument advisory parameters, if any, MUST be honored. | `src/Метрики/Модули/ОтелПотокиМетрик.os:384` |  |
| 61 | SHOULD | ✅ found | If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning. | `src/Метрики/Классы/ОтелМетр.os:965` |  |
| 62 | SHOULD | ✅ found | If applying the View would produce semantic errors (for example, configuring an asynchronous instrument to use the Explicit bucket histogram aggregation), the implementation SHOULD emit a warning and proceed as if that View did not exist. | `src/Метрики/Модули/ОтелПотокиМетрик.os:281` |  |
| 63 | MUST | ✅ found | If both the View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Модули/ОтелПотокиМетрик.os:384` |  |
| 64 | SHOULD | ✅ found | If the Instrument could not match with any of the registered `View`(s), the SDK SHOULD enable the instrument using the default aggregation and temporality. | `src/Метрики/Модули/ОтелПотокиМетрик.os:211` |  |

#### Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | MUST | ✅ found | The SDK MUST provide the following `Aggregation` to support the Metric Points in the Metrics Data Model. | `src/Метрики/Модули/ОтелАгрегация.os:15` |  |
| 66 | SHOULD | ✅ found | The SDK SHOULD provide the following `Aggregation`: | `src/Метрики/Модули/ОтелАгрегация.os:81` |  |

#### Histogram Aggregations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#histogram-aggregations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | SHOULD NOT | ✅ found | Arithmetic sum of `Measurement` values in population. This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpDownCounter` or `ObservableGauge`). | `src/Метрики/Модули/ОтелАгрегация.os:172` |  |

#### Explicit Bucket Histogram Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#explicit-bucket-histogram-aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different (e.g. for backward compatibility reasons in a stable SDK release). | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:180` |  |

#### Handle all normal values

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#handle-all-normal-values)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | SHOULD NOT | ➖ n_a | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`, `min`, and `max` fields, because these values do not map into a valid bucket. | - | Число в OneScript = System.Decimal (не IEEE 754): +Inf, -Inf и NaN невозможны, операции выбрасывают исключение, поэтому non-normal значения не могут попасть в sum/min/max. |

#### Support a minimum and maximum scale

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#support-a-minimum-and-maximum-scale)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 70 | MUST | ✅ found | The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic scale parameter will not exceed. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:323` |  |

#### Use the maximum scale for single measurements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#use-the-maximum-scale-for-single-measurements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | SHOULD | ✅ found | When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:48` |  |

#### Maintain the ideal scale

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#maintain-the-ideal-scale)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | SHOULD | ✅ found | Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possible, within the constraint of maximum size (max number of buckets). | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:238` |  |

#### Observations inside asynchronous callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#observations-inside-asynchronous-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | MUST | ✅ found | Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that observations made or produced by executing callbacks only apply to the intended `MetricReader` during collec... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:259` |  |
| 74 | SHOULD | ✅ found | The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` |  |
| 75 | SHOULD | ⚠️ partial | The implementation SHOULD use a timeout to prevent indefinite callback execution. | `src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:128` | Soft-timeout: callback запускается в фоновом задании, SDK перестаёт ждать и отбрасывает измерения; hard cancel недоступен в OneScript (EvilBeaver/OneScript#1672), задание продолжает работу в фоне. |
| 76 | MUST | ✅ found | The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:399` |  |
| 77 | SHOULD NOT | ✅ found | The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback. | `src/Метрики/Классы/ОтелХранилищеНаблюдений.os:249` |  |

#### Cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | SHOULD | ✅ found | SDKs SHOULD support being configured with a cardinality limit. | `src/Метрики/Классы/ОтелПредставление.os:92` |  |
| 79 | SHOULD | ✅ found | Cardinality limit enforcement SHOULD occur after attribute filtering, if any. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:58` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 80 | SHOULD | ✅ found | A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardinality_limit` value defined for the stream, that value SHOULD be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:331` |  |
| 81 | SHOULD | ✅ found | If there is no matching view, but the `MetricReader` defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:368` |  |
| 82 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:26` |  |

#### Overflow attribute

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#overflow-attribute)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 83 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:316` |  |
| 84 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:321` |  |

#### Synchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#synchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 85 | MUST | ✅ found | Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:316` |  |
| 86 | MUST | ✅ found | Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in exactly one Aggregator, which is either an Aggregator associated with the correct attribute set or an aggregat... | `src/Метрики/Классы/ОтелХранилищеМетрики.os:65` |  |
| 87 | MUST NOT | ✅ found | Measurements MUST NOT be double-counted or dropped during an overflow. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:316` |  |

#### Asynchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#asynchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 88 | SHOULD | ✅ found | Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality. | `src/Метрики/Классы/ОтелХранилищеНаблюдений.os:299` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | MUST | ✅ found | Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:1344` |  |

#### Duplicate instrument registration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#duplicate-instrument-registration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | MUST | ✅ found | This means that the Meter MUST return a functional instrument that can be expected to export data even if this will cause semantic error in the data model. | `src/Метрики/Классы/ОтелМетр.os:1243` |  |
| 91 | SHOULD | ✅ found | Therefore, when a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted. | `src/Метрики/Классы/ОтелМетр.os:1426` |  |
| 92 | SHOULD | ✅ found | The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible. | `src/Метрики/Классы/ОтелМетр.os:1775` |  |
| 93 | SHOULD | ✅ found | If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning. | `src/Метрики/Классы/ОтелМетр.os:1749` |  |
| 94 | SHOULD | ✅ found | If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning. | `src/Метрики/Классы/ОтелМетр.os:1775` |  |
| 95 | SHOULD | ✅ found | Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument registration. | `src/Метрики/Классы/ОтелМетр.os:1344` |  |
| 96 | MUST | ✅ found | To accommodate the recommendations from the data model, the SDK MUST aggregate data from identical Instruments together in its export pipeline. | `src/Метрики/Классы/ОтелМетр.os:1243` |  |

#### Name conflict

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#name-conflict)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | MUST | ✅ found | When this happens, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above. | `src/Метрики/Классы/ОтелМетр.os:1273` |  |

#### Instrument name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | SHOULD | ✅ found | When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax | `src/Метрики/Классы/ОтелМетр.os:1161` |  |
| 99 | SHOULD | ✅ found | If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name. | `src/Метрики/Классы/ОтелМетр.os:1161` |  |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 100 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | `src/Метрики/Классы/ОтелМетр.os:622` |  |
| 101 | MUST | ✅ found | If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit string. | `src/Метрики/Классы/ОтелМетр.os:1140` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 102 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument description. | `src/Метрики/Классы/ОтелМетр.os:622` |  |
| 103 | MUST | ✅ found | If a description is not provided or the description is null, the Meter MUST treat it the same as an empty description string. | `src/Метрики/Классы/ОтелМетр.os:1140` |  |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 104 | SHOULD | ✅ found | When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:1658` |  |
| 105 | SHOULD | ✅ found | If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided. | `src/Метрики/Классы/ОтелМетр.os:1658` |  |
| 106 | MUST | ✅ found | If multiple identical Instruments are created with different advisory parameters, the Meter MUST return an instrument using the first-seen advisory parameters and log an appropriate error as described in duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:1243` |  |
| 107 | MUST | ✅ found | If both a View and advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Модули/ОтелПотокиМетрик.os:380` |  |

#### Instrument advisory parameter: `ExplicitBucketBoundaries`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameter-explicitbucketboundaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 108 | MUST | ✅ found | If no View matches, or if a matching View selects the default aggregation, the `ExplicitBucketBoundaries` advisory parameter MUST be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:380` |  |

#### Instrument enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 109 | MUST | ✅ found | The synchronous instrument `Enabled` MUST return `false` when either: * Status: Development - The MeterConfig of the `Meter` used to create the instrument has parameter `enabled=false`. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:251` |  |
| 110 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` |  |

#### Exemplar

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 111 | MUST | ✅ found | A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements via the `ExemplarFilter` and `ExemplarReservoir` hooks. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:60` |  |
| 112 | SHOULD | ✅ found | `Exemplar` sampling SHOULD be turned on by default. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:618` |  |
| 113 | MUST NOT | ✅ found | If `Exemplar` sampling is off, the SDK MUST NOT have overhead related to exemplar sampling. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:494` |  |
| 114 | MUST | ✅ found | A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation. | `src/Метрики/Модули/ОтелАгрегация.os:207` |  |
| 115 | SHOULD | ✅ found | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: * `ExemplarFilter`: filter which measurements can become exemplars.* `ExemplarReservoir`: storage and sampling of exemplars. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:65` |  |

#### ExemplarFilter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarfilter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 116 | MUST | ✅ found | The `ExemplarFilter` configuration MUST allow users to select between one of the built-in ExemplarFilters. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:65` |  |
| 117 | SHOULD | ✅ found | The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for an SDK. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:22` |  |
| 118 | SHOULD | ✅ found | The default value SHOULD be `TraceBased`. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:618` |  |
| 119 | SHOULD | ✅ found | The filter configuration SHOULD follow the environment variable specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114` |  |
| 120 | MUST | ✅ found | An OpenTelemetry SDK MUST support the following filters: * AlwaysOn* AlwaysOff* TraceBased | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14` |  |

#### ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 121 | MUST | ✅ found | The `ExemplarReservoir` interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:51` |  |
| 122 | MUST | ✅ found | A new `ExemplarReservoir` MUST be created for every known timeseries data point, as determined by aggregation and view configuration. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:337` |  |
| 123 | SHOULD | ✅ found | The “offer” method SHOULD accept measurements, including: * The `value` of the measurement.* The complete set of `Attributes` of the measurement.* The Context of the measurement, which covers the Bagg... | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:51` |  |
| 124 | SHOULD | ✅ found | The “offer” method SHOULD have the ability to pull associated trace and span information without needing to record full context. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:203` |  |
| 125 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additional sampling performed by the reser... | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 126 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additional sampling performed by the reser... | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:51` |  |
| 127 | MUST | ✅ found | The “collect” method MUST return accumulated `Exemplar`s. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:103` |  |
| 128 | SHOULD | ✅ found | In other words, Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:133` |  |
| 129 | MUST | ✅ found | `Exemplar`s MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:225` |  |
| 130 | SHOULD | ✅ found | The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:77` |  |

#### Exemplar defaults

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar-defaults)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 131 | MUST | ✅ found | The SDK MUST include two types of built-in exemplar reservoirs: * `SimpleFixedSizeExemplarReservoir`* `AlignedHistogramBucketExemplarReservoir` | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:264` |  |
| 132 | SHOULD | ✅ found | By default: * Explicit bucket histogram aggregation with more than 1 bucket SHOULD use `AlignedHistogramBucketExemplarReservoir`. | `src/Метрики/Модули/ОтелАгрегация.os:211` |  |
| 133 | SHOULD | ✅ found | * Base2 Exponential Histogram Aggregation SHOULD use a `SimpleFixedSizeExemplarReservoir` with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty... | `src/Метрики/Модули/ОтелАгрегация.os:214` |  |
| 134 | SHOULD | ✅ found | * All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`. | `src/Метрики/Модули/ОтелАгрегация.os:217` |  |

#### SimpleFixedSizeExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#simplefixedsizeexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 135 | MUST | ✅ found | This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the reservoir has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:64` |  |
| 136 | SHOULD | ✅ found | Any stateful portion of sampling computation SHOULD be reset every collection cycle. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:461` |  |
| 137 | SHOULD | ✅ found | Otherwise, a default size of `1` SHOULD be used. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:264` |  |

#### AlignedHistogramBucketExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#alignedhistogrambucketexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 138 | MUST | ✅ found | This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:280` |  |
| 139 | MUST | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has see... | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:65` |  |
| 140 | SHOULD | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has see... | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:131` |  |
| 141 | SHOULD | ✅ found | This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:280` |  |

#### Custom ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#custom-exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 142 | MUST | ✅ found | The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation. | `src/Метрики/Модули/ОтелПотокиМетрик.os:334` |  |
| 143 | MUST | ✅ found | This extension MUST be configurable on a metric View, although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reservoir - Paragraph 2). | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 144 | MUST | ✅ found | This extension MUST be configurable on a metric View, although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reservoir - Paragraph 2). | `src/Метрики/Классы/ОтелХранилищеМетрики.os:337` |  |

#### MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 145 | SHOULD | ✅ found | To construct a `MetricReader` when setting up an SDK, at least the following SHOULD be provided: | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:811` |  |
| 146 | SHOULD | ✅ found | This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:302` |  |
| 147 | SHOULD | ✅ found | If not configured, the default aggregation SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:302` |  |
| 148 | SHOULD | ✅ found | This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:335` |  |
| 149 | SHOULD | ✅ found | If not configured, the Cumulative temporality SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:335` |  |
| 150 | SHOULD | ✅ found | If not configured, a default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:811` |  |
| 151 | SHOULD | ✅ found | A common implementation of `MetricReader`, the periodic exporting `MetricReader` SHOULD be provided to be used typically with push-based metrics collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:1` |  |
| 152 | MUST | ✅ found | The `MetricReader` MUST ensure that data points from OpenTelemetry instruments are output in the configured aggregation temporality for each instrument kind. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:84` |  |
| 153 | MUST | ✅ found | For synchronous instruments with Cumulative aggregation temporality, MetricReader.Collect MUST receive data points exposed in previous collections regardless of whether new measurements have been recorded. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:362` |  |
| 154 | MUST | ✅ found | For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:362` |  |
| 155 | MUST | ✅ found | For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелХранилищеНаблюдений.os:232` |  |
| 156 | MUST | ✅ found | For instruments with Cumulative aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST repeat the same starting timestamps (e.g. `(T0, T1], (T0, T2], (T0, T3]`). | `src/Метрики/Классы/ОтелХранилищеМетрики.os:362` |  |
| 157 | MUST | ✅ found | For instruments with Delta aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST advance the starting timestamp ( e.g. `(T0, T1], (T1, T2], (T2, T3]`). | `src/Метрики/Классы/ОтелХранилищеМетрики.os:362` |  |
| 158 | MUST | ✅ found | The ending timestamp (i.e. `TimeUnixNano`) MUST always be equal to time the metric data point took effect, which is equal to when MetricReader.Collect was invoked. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:446` |  |
| 159 | MUST | ✅ found | The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`, and the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NOT introduce side-effects to other `MetricReader` instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:472` |  |
| 160 | SHOULD NOT | ✅ found | The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`, and the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NOT introduce side-effects to other `MetricReader` instances. | `src/Метрики/Классы/ОтелМетр.os:429` |  |
| 161 | MUST NOT | ✅ found | The SDK MUST NOT allow a `MetricReader` instance to be registered on more than one `MeterProvider` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:354` |  |
| 162 | SHOULD | ✅ found | The SDK SHOULD provide a way to allow `MetricReader` to respond to MeterProvider.ForceFlush and MeterProvider.Shutdown. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:182` |  |

#### Collect

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#collect)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 163 | SHOULD | ✅ found | `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:399` |  |
| 164 | SHOULD | ✅ found | `Collect` SHOULD invoke Produce on registered MetricProducers. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:729` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 165 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MetricReader` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:151` |  |
| 166 | SHOULD | ✅ found | SDKs SHOULD return some failure for these calls, if possible. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:113` |  |
| 167 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:149` |  |
| 168 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:149` |  |

#### Periodic exporting MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 169 | MUST | ✅ found | When `maxExportBatchSize` is configured, the reader MUST ensure no batch provided to `Export` exceeds the `maxExportBatchSize` by splitting the batch of metric data points into smaller batches. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:570` |  |
| 170 | MUST | ✅ found | The initial batch of metric data MUST be split into as many “full” batches of size `maxExportBatchSize` as possible – even if this splits up data points that belong to the same metric into different batches. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:570` |  |
| 171 | MUST | ✅ found | The reader MUST ensure all batches produced from a single `Collect()` are provided to `Export` serially and in-order before metric data points from a subsequent `Collect()` are provided. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:484` |  |
| 172 | MUST NOT | ✅ found | The reader MUST NOT combine metrics from different `Collect()` calls into the same batch provided to `Export`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:429` |  |
| 173 | MUST | ✅ found | The reader MUST synchronize calls to `MetricExporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:399` |  |
| 174 | MUST | ✅ found | If an export is still in progress when the next scheduled interval occurs, the reader MUST either delay the subsequent collection and export until the in-progress export finishes, or skip the scheduled collection for that interval. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:404` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 175 | SHOULD | ✅ found | `ForceFlush` SHOULD collect metrics, split into batches if necessary, call `Export(batch)` on each batch serially, and call `ForceFlush()` on the configured Push Metric Exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:187` |  |
| 176 | SHOULD | ✅ found | `ForceFlush` MAY skip `Export(batch)` calls if the timeout is already expired, but SHOULD still call `ForceFlush()` on the configured Push Metric Exporter even if the timeout has passed. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:201` |  |
| 177 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:187` |  |
| 178 | SHOULD | ✅ found | If any `Export(batch)` call fails or times out, or if the configured exporter’s `ForceFlush()` fails or times out, `ForceFlush` SHOULD return some ERROR status. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:204` |  |
| 179 | SHOULD | ✅ found | If all calls succeed, `ForceFlush` SHOULD return some NO ERROR status. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:204` |  |
| 180 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:187` |  |

#### MetricExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 181 | MUST | ✅ found | `MetricExporter` defines the interface that protocol-specific exporters MUST implement so that they can be plugged into OpenTelemetry SDK and support sending of telemetry data. | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1` |  |
| 182 | SHOULD | ✅ found | Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsupported Aggregation or Aggregation Temporality, as this condition can be corrected by a change of `MetricReader` configuration. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:181` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 183 | MUST | ✅ found | A Push Metric Exporter MUST support the following functions: | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:67` |  |

#### Export(batch)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 184 | MUST | ✅ found | The SDK MUST provide a way for the exporter to get the Meter information (e.g. name, version, etc.) associated with each `Metric Point`. | `src/Метрики/Классы/ОтелДанныеМетрики.os:1` |  |
| 185 | MUST NOT | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47` |  |
| 186 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47` |  |
| 187 | SHOULD NOT | ✅ found | The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the metrics are being sent to. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:515` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 188 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Metrics` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:125` |  |
| 189 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:125` |  |
| 190 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed metrics. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение |
| 191 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:187` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 192 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each `MetricExporter` instance. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:107` |  |
| 193 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:172` |  |

#### MetricProducer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricproducer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 194 | MUST | ✅ found | `MetricProducer` defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:29` |  |
| 195 | SHOULD | ✅ found | `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of produced metrics. | `src/Метрики/Классы/ОтелДанныеМетрики.os:121` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 196 | MUST | ✅ found | A `MetricProducer` MUST support the following functions: | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:29` |  |

#### Produce batch

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#produce-batch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 197 | SHOULD | ✅ found | If the batch of Metric Points includes resource information, `Produce` SHOULD require a resource as a parameter. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:29` |  |
| 198 | SHOULD | ✅ found | `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелРезультатПроизводстваМетрик.os:47` |  |
| 199 | SHOULD | ✅ found | If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:14` |  |

#### Defaults and configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#defaults-and-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 200 | MUST | ✅ found | The SDK MUST provide configuration according to the SDK environment variables specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:366` |  |

#### Numerical limits handling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#numerical-limits-handling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 201 | MUST | ✅ found | The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:81` |  |
| 202 | MUST | ✅ found | If the SDK receives float/double values from Instruments, it MUST handle all the possible values. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:81` |  |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 203 | SHOULD | ✅ found | All the metrics components SHOULD allow new methods to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелПровайдерМетрик.os` |  |
| 204 | SHOULD | ✅ found | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to existing methods without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелСчетчик.os:38` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 205 | MUST | ✅ found | MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:76` |  |
| 206 | MUST | ✅ found | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:269` |  |
| 207 | MUST | ✅ found | MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:149` |  |
| 208 | MUST | ✅ found | MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:107` |  |

### Otlp Exporter

#### Configuration Options

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#configuration-options)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | The following configuration options MUST be available to configure the OTLP exporter. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:508` | Endpoint, headers, compression, timeout, protocol, certificate, client key/certificate, insecure и max request/response size (ОтелHttpТранспорт.os:84-114) доступны. Но файлы сертификатов TLS HTTP-транспортом игнорируются (HTTP-клиент OneScript их не поддерживает, ОтелHttpТранспорт.os:513-518), а сжатие для gRPC не поддерживается клиентом OPI_GRPC (ОтелАвтоконфигурация.os:1061) - опции читаются, но не действуют. |
| 2 | MUST | ✅ found | Each configuration option MUST be overridable by a signal specific option. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1308` |  |
| 3 | MUST | ✅ found | The implementation MUST honor the following URL components: | `src/Экспорт/Классы/ОтелHttpТранспорт.os:316` |  |
| 4 | MUST | ✅ found | When using `OTEL_EXPORTER_OTLP_ENDPOINT`, exporters MUST construct per-signal URLs as described below. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:553` |  |
| 5 | SHOULD | ✅ found | The option SHOULD accept any form allowed by the underlying gRPC client implementation. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1360` |  |
| 6 | MUST | ✅ found | Additionally, the option MUST accept a URL with a scheme of either `http` or `https`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:653` |  |
| 7 | SHOULD | ✅ found | If the gRPC client implementation does not support an endpoint with a scheme of `http` or `https` then the endpoint SHOULD be transformed to the most sensible format for that implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:416` |  |
| 8 | MUST | ✅ found | Protocol: The transport protocol. Options MUST be one of: `grpc`, `http/protobuf`, `http/json`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:928` |  |
| 9 | SHOULD | ✅ found | [1]: SDKs SHOULD default endpoint variables to use `http` scheme unless they have good reasons to choose `https` scheme for the default (e.g., for backward compatibility reasons in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:555` |  |
| 10 | SHOULD | ✅ found | However, if they are already implemented, they SHOULD continue to be supported as they were part of a stable release of the specification. | - |  |
| 11 | SHOULD | ✅ found | [4]: The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:518` |  |

#### Endpoint URLs for OTLP/HTTP

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#endpoint-urls-for-otlphttp)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal as follow: | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:536` |  |
| 13 | MUST | ✅ found | For the per-signal variables (`OTEL_EXPORTER_OTLP_<signal>_ENDPOINT`), the URL MUST be used as-is without any modification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:543` |  |
| 14 | MUST | ✅ found | The only exception is that if an URL contains no path part, the root path `/` MUST be used (see Example 2). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1327` |  |
| 15 | MUST NOT | ✅ found | An SDK MUST NOT modify the URL in ways other than specified above. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1327` |  |

#### Specify Protocol

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specify-protocol)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ✅ found | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:928` |  |
| 17 | MUST | ✅ found | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:151` |  |
| 18 | SHOULD | ✅ found | If they support only one, it SHOULD be `http/protobuf`. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:151` |  |
| 19 | SHOULD | ✅ found | If no configuration is provided the default transport SHOULD be `http/protobuf` unless SDKs have good reasons to choose `grpc` as the default (e.g. for backward compatibility reasons when `grpc` was already the default in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:518` |  |

#### Specifying headers via environment variables

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:1787` |  |

#### Retry

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#retry)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | Transient errors MUST be handled with a retry strategy. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:221` |  |
| 22 | MUST | ✅ found | This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:490` |  |

#### User Agent

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#user-agent)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | SHOULD | ⚠️ partial | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:507` | OTLP/HTTP отправляет User-Agent OTel-OTLP-Exporter-OneScript/<версия>. Для OTLP/gRPC user-agent кладется в метаданные (ОтелGrpcТранспорт.os:402), но до сервера не доходит: tonic в OPI_GRPC ставит свой user-agent (OpenIntegrations issue 111). |
| 24 | SHOULD | ✅ found | The format of the header SHOULD follow RFC 7231. | `src/Ядро/Модули/ОтелУтилиты.os:485` |  |
| 25 | SHOULD | ✅ found | The resulting User-Agent SHOULD include the exporter’s default User-Agent string. | `src/Ядро/Модули/ОтелУтилиты.os:485` |  |

### Propagators

#### Operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Propagator`s MUST define `Inject` and `Extract` operations, in order to write values to and read values from carriers respectively. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:63` |  |
| 2 | MUST | ✅ found | Each `Propagator` type MUST define the specific carrier type and MAY define additional parameters. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:94` |  |

#### Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The Propagator MUST retrieve the appropriate value from the `Context` first, such as `SpanContext`, `Baggage` or another cross-cutting concern context. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:64` |  |

#### Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any previously... | `src/Пропагация/Классы/ОтелW3CПропагатор.os:99` |  |
| 5 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any previously... | `src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:147` |  |

#### TextMap Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | In order to increase compatibility, the key-value pairs MUST only consist of US-ASCII characters that make up valid HTTP header fields as per RFC 9110. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:110` |  |
| 7 | MUST | ✅ found | `Getter` and `Setter` MUST be stateless and allowed to be saved as constants, in order to effectively avoid runtime allocations. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:73` |  |

#### Set

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#set)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:117` |  |
| 9 | MUST | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:117` |  |

#### Keys

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#keys)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The `Keys` function MUST return the list of all the keys in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:59` |  |

#### Get

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#get)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | The Get function MUST return the first value of the given propagation key or return null if the key doesn’t exist. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:20` |  |
| 12 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:21` |  |

#### Composite Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | Implementations MUST offer a facility to group multiple `Propagator`s from different cross-cutting concerns in order to leverage them as a single entity. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:166` |  |
| 14 | MUST | ✅ found | There MUST be functions to accomplish the following operations. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:97` |  |

#### Global Propagators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#global-propagators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The OpenTelemetry API MUST provide a way to obtain a propagator for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:215` |  |
| 16 | SHOULD | ➖ n_a | Instrumentation libraries SHOULD call propagators to extract and inject the context on all remote calls. | - | Требование адресовано Instrumentation Libraries (политика их поведения); данный пакет реализует только API+SDK, IL не включены |
| 17 | MUST | ✅ found | The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise. | `src/Ядро/Модули/ОтелГлобальный.os:215` |  |
| 18 | SHOULD | ✅ found | If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace Context Propagator and the Baggage `Propagator` specified in the Baggage API. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:441` |  |
| 19 | MUST | ✅ found | These platforms MUST also allow pre-configured propagators to be disabled or overridden. | `src/Ядро/Модули/ОтелГлобальный.os:201` |  |

#### Get Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#get-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | This method SHOULD exist for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:215` |  |

#### Set Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#set-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | SHOULD | ✅ found | This method SHOULD exist for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:201` |  |

#### Propagators Distribution

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#propagators-distribution)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 22 | MUST | ➖ n_a | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry Core packages: | - | Требование адресовано OpenTelemetry Organization (официальный реестр пропагаторов); данный пакет является независимой SDK-реализацией, не официальным дистрибутивом OTel |
| 23 | MUST | ➖ n_a | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry Core packages: | - | Требование адресовано OpenTelemetry Organization (официальный реестр пропагаторов); данный пакет является независимой SDK-реализацией, не официальным дистрибутивом OTel |
| 24 | MUST NOT | ✅ found | It MUST NOT use `OpenTracing` in the resulting propagator name as it is not widely adopted format in the OpenTracing ecosystem. | `/home/user/opentelemetry/src/Пропагация/Классы` | OT Trace пропагатор в пакете не реализован, имён с OpenTracing нет (в Пропагация/Классы только W3C, W3C Baggage, композитный, noop). |
| 25 | MUST NOT | ✅ found | Additional `Propagator`s implementing vendor-specific protocols such as AWS X-Ray trace header protocol MUST NOT be maintained or distributed as part of the OpenTelemetry Core packages. | `/home/user/opentelemetry/src/Пропагация/Классы` |  |

#### W3C Trace Context Requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#w3c-trace-context-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | MUST | ✅ found | A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP headers as specified in W3C Trace Context Level 2. | `/home/user/opentelemetry/src/Пропагация/Классы/ОтелW3CПропагатор.os:99` |  |
| 27 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid `traceparent` value using the same header. | `/home/user/opentelemetry/src/Пропагация/Классы/ОтелW3CПропагатор.os:63` |  |
| 28 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid `tracestate` unless the value is empty, in which case the `tracestate` header may be omitted. | `/home/user/opentelemetry/src/Пропагация/Классы/ОтелW3CПропагатор.os:83` |  |

#### B3 Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | MUST | ✅ found | MUST attempt to extract B3 encoded using single and multi-header formats. | `opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:65` |  |
| 30 | MUST | ✅ found | MUST preserve a debug trace flag, if received, and propagate it with subsequent requests. | `opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:137` |  |
| 31 | MUST | ✅ found | Additionally, an OpenTelemetry implementation MUST set the sampled trace flag when the debug flag is set. | `opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:137` |  |
| 32 | MUST NOT | ✅ found | MUST NOT reuse `X-B3-SpanId` as the ID for the server-side span. | `opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:201` |  |

#### B3 Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | MUST | ✅ found | MUST default to injecting B3 using the single-header format | `opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:259` |  |
| 34 | MUST | ✅ found | MUST provide configuration to change the default injection format to B3 multi-header | `opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:259` |  |
| 35 | MUST NOT | ✅ found | MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support reusing the same ID for both sides of a request. | `opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:113` |  |

#### Fields

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#fields)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | Fields MUST return the header names that correspond to the configured format, i.e., the headers used for the inject operation. | `opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:86` |  |

### Env Vars

#### Environment Variable Specification

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#environment-variable-specification)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If they do, they SHOULD use the names and value parsing behavior specified in this document. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:149` |  |
| 2 | SHOULD | ✅ found | They SHOULD also follow the common configuration specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1123` |  |

#### Implementation guidelines

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#implementation-guidelines)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The environment-based configuration MUST have a direct code configuration equivalent. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:135` |  |

#### Parsing empty value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#parsing-empty-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1103` |  |

#### Boolean

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#boolean)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Any value that represents a Boolean MUST be set to true only by the case-insensitive string "true", meaning "True" or "TRUE" are also accepted, as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1283` |  |
| 6 | MUST NOT | ✅ found | An implementation MUST NOT extend this definition and define additional values that are interpreted as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1284` |  |
| 7 | MUST | ✅ found | Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1280` |  |
| 8 | SHOULD | ✅ found | If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1289` |  |
| 9 | SHOULD | ✅ found | All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:896` |  |
| 10 | MUST NOT | ✅ found | Renaming or changing the default value MUST NOT happen without a major version upgrade. | - |  |

#### Numeric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#numeric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | The following paragraph was added after stabilization and the requirements are thus qualified as “SHOULD” to allow implementations to avoid breaking changes. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1123` |  |
| 12 | MUST | ✅ found | For new implementations, these should be treated as MUST requirements. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1123` |  |
| 13 | SHOULD | ✅ found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them as not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1138` |  |

#### Enum

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#enum)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | SHOULD | ✅ found | Enum values SHOULD be interpreted in a case-insensitive manner. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:959` |  |
| 15 | MUST | ✅ found | For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1234` |  |

#### General SDK Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | Values MUST be deduplicated in order to register a `Propagator` only once. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:431` |  |
| 17 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1005` |  |
| 18 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1005` |  |
| 19 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1005` |  |

#### Attribute Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#attribute-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | Implementations SHOULD only offer environment variables for the types of attributes, for which that SDK implements truncation mechanism. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:445` |  |

#### Exporter Selection

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#exporter-selection)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | SHOULD NOT | ✅ found | It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1234` |  |
| 22 | SHOULD NOT | ✅ found | It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1234` |  |
| 23 | SHOULD NOT | ✅ found | It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1234` |  |

#### Declarative configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#declarative-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | When `OTEL_CONFIG_FILE` is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:107` |  |

### Prometheus Compatibility

#### Differences between Prometheus formats

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#differences-between-prometheus-formats)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Exemplars MUST be dropped if they are not supported. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:728` |  |
| 2 | MUST | ✅ found | If the specification below requires producing a Prometheus Info-typed metric, a Prometheus Gauge with an additional `_info` name suffix MUST be produced if Info-typed metrics are not supported. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:511` |  |
| 3 | MUST | ✅ found | If the specification below requires producing a Prometheus StateSet-typed metric, a Prometheus Gauge MUST be produced instead if StateSet-typed metrics are not supported. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:570` |  |
| 4 | SHOULD | ✅ found | Exponential (Native) Histograms SHOULD be dropped if they are not supported, or MAY be converted to fixed-bucket histograms. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:644` |  |

#### Metric Metadata

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#metric-metadata)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST NOT | ✅ found | Prometheus Pull exporters for OpenTelemetry metric data MUST NOT allow duplicate UNIT, HELP, or TYPE comments for the same metric name to be returned in a single scrape of the Prometheus endpoint. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:702` |  |
| 6 | MUST | ✅ found | Exporters MUST drop entire metrics to prevent conflicting TYPE comments, but SHOULD NOT drop metric points as a result of conflicting UNIT or HELP comments. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1197` |  |
| 7 | SHOULD NOT | ✅ found | Exporters MUST drop entire metrics to prevent conflicting TYPE comments, but SHOULD NOT drop metric points as a result of conflicting UNIT or HELP comments. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:702` |  |
| 8 | SHOULD | ✅ found | Instead, all but one of the conflicting UNIT and HELP comments (but not metric points) SHOULD be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:702` |  |
| 9 | SHOULD | ✅ found | If dropping a comment or metric points, the exporter SHOULD warn the user through error logging. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1052` |  |
| 10 | MUST | ✅ found | The Name of an OTLP metric MUST be added as the Prometheus Metric Name. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1292` |  |
| 11 | SHOULD | ✅ found | Discouraged characters in the metric name SHOULD be replaced with the `_` character by default, aiming for compatibility with Prometheus conventions. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1823` |  |
| 12 | SHOULD | ✅ found | Multiple consecutive `_` characters SHOULD be replaced with a single `_` character. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1823` |  |
| 13 | MUST | ✅ found | The Unit of an OTLP metric point MUST be converted from the UCUM unit to the equivalent unit word in Prometheus if it is included in the table in Metric Metadata above. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1317` |  |
| 14 | MUST | ✅ found | Portions of the Unit within brackets (e.g. {packet}) MUST be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1317` |  |
| 15 | MUST | ✅ found | Units defined as rates over time (e.g. “m/s”) MUST be converted to words (e.g. “meters_per_second”). | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1348` |  |
| 16 | SHOULD | ✅ found | The resulting unit SHOULD be added to the metric as UNIT metadata. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:702` |  |
| 17 | SHOULD | ✅ found | A suffix to the metric name SHOULD be added unless the metric name already ends with the unit (before type-specific suffixes). | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1292` |  |
| 18 | MUST | ✅ found | The description of an OTLP metrics point MUST be added as HELP metadata. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:702` |  |
| 19 | MUST | ✅ found | The data point type of an OTLP metric MUST be added as TYPE metadata. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:556` |  |

#### Instrumentation Scope

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#instrumentation-scope)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | Prometheus exporters MUST by default add the scope name as the `otel_scope_name` label, the scope version as the `otel_scope_version` label, the scope schema URL as the `otel_scope_schema_url` label, the sc... | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1495` |  |
| 21 | MUST | ✅ found | Scope attributes that, after adding the `otel_scope_` prefix and applying the label-name conversion described in `Metric Attributes`, would conflict with `otel_scope_name`, `otel_scope_version`, or `o... | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1495` |  |

#### Gauges

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#gauges)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 22 | MUST | ✅ found | An OpenTelemetry Gauge MUST be converted following a hint present in metric.metadata: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:567` |  |
| 23 | MUST | ✅ found | If the `prometheus.type` key is absent, or its value is equal to `gauge`, the datapoint MUST be transformed to a Prometheus Gauge. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:572` |  |
| 24 | MUST | ✅ found | If the `prometheus.type` key has value equal to `unkown`, the datapoint MUST be transformed to a Prometheus Unknown. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:568` |  |
| 25 | SHOULD | ✅ found | If the `prometheus.type` key has value equal to `info`, the datapoint SHOULD be transformed to a Prometheus Info. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:570` |  |
| 26 | SHOULD | ✅ found | If the `prometheus.type` key has value equal to `stateset`, the datapoint SHOULD be transformed to a Prometheus Stateset. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:570` |  |
| 27 | SHOULD | ✅ found | Exemplars on OpenTelemetry Gauges SHOULD be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:737` |  |

#### Sums

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#sums)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | An OpenTelemetry Sum MUST be converted following the rules below: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:599` |  |
| 29 | MUST | ✅ found | If the aggregation temporality is cumulative and the sum is monotonic, it MUST be converted to a Prometheus Counter. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:556` |  |
| 30 | SHOULD | ✅ found | If the metric name for monotonic Sum metric points does not end in a suffix of `_total` a suffix of `_total` SHOULD be added by default, otherwise the name MUST remain unchanged. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1292` |  |
| 31 | MUST | ✅ found | If the metric name for monotonic Sum metric points does not end in a suffix of `_total` a suffix of `_total` SHOULD be added by default, otherwise the name MUST remain unchanged. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1292` |  |
| 32 | SHOULD | ✅ found | Monotonic Sum metric points with `StartTimeUnixNano` SHOULD transform `StartTimeUnixNano` into Prometheus `StartTime`, following the appropriate format used by each Prometheus protocol. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:825` |  |
| 33 | MUST | ✅ found | If Sum is converted to a Prometheus Counter, then `Exemplars` MUST be converted as described in the Exemplar Conversion section. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:747` |  |
| 34 | SHOULD | ✅ found | Otherwise, `Exemplars` SHOULD be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:749` |  |
| 35 | SHOULD | ✅ found | If the Prometheus protocol only supports a single exemplar on the Counter sample, the latest exemplar SHOULD be converted. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:852` |  |

#### Histograms

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#histograms)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | An OpenTelemetry Histogram with a cumulative aggregation temporality MUST be converted to a Prometheus Histogram by default. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:556` |  |
| 37 | MUST | ✅ found | OpenTelemetry Histograms with Delta aggregation temporality MAY be aggregated into a Cumulative aggregation temporality and follow the logic below, or MUST be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:673` |  |

#### Histograms as Prometheus Histograms

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#histograms-as-prometheus-histograms)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 38 | MUST | ✅ found | When converting to a Prometheus Histogram, an OpenTelemetry Histogram MUST be converted following the rules below: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:767` |  |
| 39 | SHOULD | ✅ found | If set, `StartTimeUnixNano` SHOULD be transformed into Prometheus `StartTime`, following the appropriate format used by each Prometheus protocol. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:825` |  |
| 40 | SHOULD | ✅ found | If the Prometheus protocol only supports a single exemplar per-bucket, the latest exemplar that falls into each bucket SHOULD be converted. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:867` |  |

#### Summaries

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#summaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 41 | MUST | ✅ found | An OpenTelemetry Summary MUST be converted to a Prometheus Summary as follows: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:804` |  |
| 42 | MUST | ✅ found | The `quantile` label value MUST be the stringified floating point value of each quantile (between 0.0 and 1.0), starting from lowest to highest, and all being non-negative. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:997` |  |
| 43 | SHOULD NOT | ✅ found | Explicit timestamps SHOULD NOT be used for pull protocols, such as the Prometheus text exposition format, where Prometheus assigns the scrape timestamp. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1024` |  |
| 44 | SHOULD | ✅ found | Exemplars on OpenTelemetry Summaries SHOULD be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:804` |  |

#### Metric Attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#metric-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST | ✅ found | OpenTelemetry Metric Attributes MUST be converted to Prometheus labels. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1389` |  |
| 46 | MUST | ✅ found | String Attribute values are converted directly to Metric Attributes, and non-string Attribute values MUST be converted to string attributes following the attribute specification. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1665` |  |
| 47 | SHOULD | ✅ found | Discouraged characters SHOULD be replaced with the `_` character. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1823` |  |
| 48 | SHOULD | ✅ found | Multiple consecutive `_` characters SHOULD be replaced with a single `_` character. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1823` |  |
| 49 | MUST | ✅ found | In such cases, the values MUST be concatenated together, separated by `;`, and ordered by the lexicographical order of the original keys. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1604` |  |

#### Exemplar Conversion

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#exemplar-conversion)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 50 | MUST | ✅ found | When an exemplar is converted per the metric-type-specific sections above, the OpenTelemetry Exemplar MUST be converted to a Prometheus exemplar if the Prometheus (push or pull) protocol being used supports them, as follows: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:918` |  |
| 51 | MUST | ✅ found | If present, the OpenTelemetry Exemplar’s Trace ID and Span ID MUST be added as Exemplar labels using the `trace_id` and `span_id` keys, respectively. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:922` |  |
| 52 | MUST | ✅ found | These labels MUST take precedence over labels from `filtered_attributes` in cases where there is a key collision. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:927` |  |
| 53 | MUST | ✅ found | Timestamps MUST be added as timestamps on the Prometheus exemplar. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:939` |  |
| 54 | MUST | ✅ found | `filtered_attributes` MUST be added as labels on the Prometheus exemplar, unless they would exceed the Prometheus protocol’s exemplar limits. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:920` |  |

### Prometheus Exporter

#### Client Libraries

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#client-libraries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | A Prometheus Exporter SHOULD use an official Prometheus client library when one exists for the implementation language and it is practical to do so (e.g., dependency concerns) for serving Prometheus metrics; it SHOULD NOT use an unofficial Prometheus client library. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:107` |  |
| 2 | SHOULD NOT | ⚠️ partial | A Prometheus Exporter SHOULD use an official Prometheus client library when one exists for the implementation language and it is practical to do so (e.g., dependency concerns) for serving Prometheus metrics; it SHOULD NOT use an unofficial Prometheus client library. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:4` | Official Prometheus client for OneScript does not exist; the reader uses the community 'prometheus' OneScript package (packagedef dependency 1.0.6), which is unofficial. |
| 3 | SHOULD | ✅ found | If a Prometheus client library is used, the OpenTelemetry Prometheus Exporter SHOULD be modeled as a custom Collector so it can be used in conjunction with existing Prometheus instrumentation. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:202` |  |

#### Version and Format

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#version-and-format)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | Regardless of whether a Prometheus client library is used, the Prometheus Exporter MUST support version `0.0.4` of the Text-based format. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:102` |  |
| 5 | MUST NOT | ✅ found | A Prometheus Exporter for an OpenTelemetry metrics SDK MUST NOT use Prometheus Remote Write format or OpenMetrics protobuf format. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:102` |  |
| 6 | SHOULD NOT | ✅ found | A Prometheus Exporter for an OpenTelemetry metrics SDK SHOULD NOT add explicit timestamps on Metric points. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1024` |  |

#### Target

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#target)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | There MUST be at most one `target` info metric exposed by an SDK Prometheus exporter. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:102` |  |

#### Temporality

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#temporality)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | A Prometheus Exporter MUST set the MetricReader `temporality` as a function of instrument kind to be `cumulative` for all instrument kinds. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:329` |  |

#### Default Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#default-aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ✅ found | A Prometheus Exporter SHOULD support a configuration option to set the MetricReader default `aggregation` as a function of instrument kind. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:318` |  |
| 10 | MUST | ✅ found | This option MAY be named `default_aggregation`, and MUST use the default aggregation by default. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:307` |  |

#### Resource Attributes as Metric Labels

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#resource-attributes-as-metric-labels)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST NOT | ✅ found | By default, it MUST NOT add any resource attributes as metric labels. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1405` |  |
| 12 | SHOULD | ✅ found | The configuration SHOULD allow the user to select resource attributes to include or exclude. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:222` |  |

#### Scope Info

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#scope-info)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | The option MAY be named `scope_info_enabled`, and MUST be `true` by default. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1495` |  |

### Configuration Sdk

#### In-Memory configuration model

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk/#in-memory-configuration-model)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | SDKs SHOULD provide an in-memory representation of the configuration model. | `src/Конфигурация/Классы/ОтелКонфигурация.os:38` |  |
| 2 | SHOULD | ✅ found | Whereas `ConfigProperties` is a schemaless representation of any mapping node, the in-memory configuration model SHOULD reflect the schema of the configuration model. | `src/Конфигурация/Классы/ОтелКонфигурация.os:38` |  |

#### SDK extension components

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk/#sdk-extension-components)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | SHOULD | ✅ found | The configuration data model SHOULD define specific types for built-in implementations of these plugin components. | `src/Конфигурация/Классы/ОтелКонфигурацияПакетногоПроцессора.os:1` |  |
| 4 | SHOULD | ✅ found | The schema SHOULD support the ability to specify custom implementations of plugin components defined by libraries or users. | `src/Конфигурация/Классы/ОтелКонфигурацияКомпонента.os:1` |  |

#### PluginComponentProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk/#plugincomponentprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The `PluginComponentProvider` MUST provide the following functions: | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:1672` |  |

#### Create Component

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk/#create-component)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | SHOULD | ✅ found | A `PluginComponentProvider` SHOULD document its configuration schema and include examples. | `docs/api/Конфигурация/ОтелКонфигурационнаяФабрика.md:338` |  |
| 7 | SHOULD | ✅ found | If this fails (e.g. a required property is not present, a type is mismatches, etc.), Create Component SHOULD return an error. | `src/Конфигурация/Классы/ОтелСвойстваКонфигурации.os:238` |  |

#### SDK operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk/#sdk-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | SDK implementations of configuration MUST provide the following operations. | `src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:37` |  |

#### Parse

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk/#parse)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ✅ found | If `parse` accepts `file_format`, the API SHOULD be structured so a user is obligated to provide it. | `src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:37` |  |
| 10 | MUST | ✅ found | Parse MUST perform environment variable substitution. | `src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:110` |  |
| 11 | MUST | ✅ found | Parse MUST differentiate between properties that are missing and properties that are present but null. | `src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:1450` |  |
| 12 | MUST | ✅ found | The user MUST not be required to specify an empty object (i.e. `drop: {}`) in these cases. | `src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:562` |  |
| 13 | MUST | ✅ found | When encountering a reference to a SDK extension component which is not built-in to the SDK, Parse MUST resolve corresponding configuration to a generic ConfigProperties representation as described in Create Component. | `src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:878` |  |
| 14 | SHOULD | ✅ found | Parse SHOULD return an error if: | `src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:178` |  |

#### Create

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk/#create)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | If a property is present and the value is null, Create MUST use the `nullBehavior`, or `defaultBehavior` if `nullBehavior` is not set. | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:260` |  |
| 16 | MUST | ✅ found | If a property is required, and not present, Create MUST return an error. | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:75` |  |
| 17 | SHOULD | ✅ found | Create SHOULD return an error if it encounters a value which is invalid according to the property `description`. | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:921` |  |
| 18 | MUST | ✅ found | When encountering a reference to an SDK plugin component which is not built-in to the SDK, Create MUST resolve the component using Create Component of the `PluginComponentProvider` of the correspondin... | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:1658` |  |
| 19 | SHOULD | ✅ found | If no `PluginComponentProvider` is registered with the `type` and `name`, Create SHOULD return an error. | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:1666` |  |
| 20 | SHOULD | ✅ found | If Create Component returns an error, Create SHOULD propagate the error. | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:1671` |  |
| 21 | SHOULD | ✅ found | This SHOULD return an error if it encounters an error in `configuration` (i.e. fail fast) in accordance with initialization error handling principles. | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:69` |  |

#### Register PluginComponentProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk/#register-plugincomponentprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 22 | MUST | ✅ found | The SDK MUST provide a mechanism to register `PluginComponentProvider`. | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:37` |  |
| 23 | MUST | ✅ found | Register MUST return an error if it is called multiple times with the same `type` and `name` combination. | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:47` |  |
| 24 | SHOULD | ✅ found | SDKs SHOULD represent `type` in a manner that is idiomatic for their language. | `src/Конфигурация/Модули/ОтелТипКомпонентаКонфигурации.os:14` |  |

### Configuration Api

#### ConfigProperties

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/api/#configproperties)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `ConfigProperties` MUST provide accessors for reading all properties from the mapping node it represents, including: | `src/Конфигурация/Классы/ОтелСвойстваКонфигурации.os:34` |  |
| 2 | SHOULD | ✅ found | mappings, which SHOULD be represented as `ConfigProperties` | `src/Конфигурация/Классы/ОтелСвойстваКонфигурации.os:90` |  |
| 3 | SHOULD | ✅ found | sequences of mappings, which SHOULD be represented as `ConfigProperties` | `src/Конфигурация/Классы/ОтелСвойстваКонфигурации.os:169` |  |
| 4 | SHOULD | ✅ found | `ConfigProperties` SHOULD provide access to properties in a type safe manner, based on what is idiomatic in the language. | `src/Конфигурация/Классы/ОтелСвойстваКонфигурации.os:238` |  |
| 5 | SHOULD | ✅ found | `ConfigProperties` SHOULD allow a caller to determine if a property is present with a null value, versus not set. | `src/Конфигурация/Классы/ОтелСвойстваКонфигурации.os:208` |  |

### Configuration Data Model

#### File-based configuration model

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/data-model/#file-based-configuration-model)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Configuration files SHOULD use one the following serialization formats: | `src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:98` |  |

#### YAML file format

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/data-model/#yaml-file-format)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | SHOULD | ✅ found | YAML configuration files SHOULD follow YAML spec revision >= 1.2. | `src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:39` |  |
| 3 | SHOULD | ✅ found | YAML configuration files SHOULD be parsed using v1.2 YAML core schema. | `src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:502` |  |
| 4 | MUST | ✅ found | YAML configuration files MUST use file extensions `.yaml` or `.yml`. | `src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:98` |  |

#### Environment variable substitution

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/data-model/#environment-variable-substitution)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | When `PREFIX` is absent or `env`, `GENERIC-SUBSTITUTION` MUST conform to `ENV-SUBSTITUTION`: | `src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:221` |  |
| 6 | SHOULD | ✅ found | Language implementations SHOULD document any additional prefixes they support. | `src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:12` |  |
| 7 | MUST | ✅ found | Environment variable substitution MUST only apply to scalar values. | `src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:353` |  |
| 8 | MUST | ✅ found | If a referenced environment variable is not defined and does not have a `DEFAULT-VALUE`, it MUST be replaced with an empty value. | `src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:246` |  |
| 9 | MUST NOT | ✅ found | The resolved `$` from an escape sequence MUST NOT be considered when matching input against the environment variable substitution regular expression. | `src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:100` |  |
| 10 | MUST | ✅ found | Node types MUST be interpreted after environment variable substitution takes place. | `src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:502` |  |
| 11 | MUST NOT | ✅ found | It MUST NOT be possible to inject YAML structures by environment variables. | `src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:275` |  |
| 12 | MUST NOT | ✅ found | It MUST NOT be possible to inject environment variable by environment variables. | `src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:275` |  |

## Условные требования (Conditional)

Требования из условных секций. Применяются только при реализации соответствующей опциональной фичи.

### Propagators

#### GetAll

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#getall) | Scope: conditional:GetAll Getter (post-stable extension)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | If explicitly implemented, the `GetAll` function MUST return all values of the given propagation key. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40` |  |
| 2 | SHOULD | ✅ found | It SHOULD return them in the same order as they appear in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:43` |  |
| 3 | SHOULD | ✅ found | If the key doesn’t exist, it SHOULD return an empty collection. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:41` |  |
| 4 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:42` |  |

### Prometheus Compatibility

#### Metric Metadata

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#metric-metadata) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | The Prometheus Metric Name MUST be added as the Name of the OTLP metric. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 2 | SHOULD NOT | ➖ n_a | The name SHOULD NOT be altered. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 3 | MUST | ➖ n_a | Prometheus UNIT metadata, if present, MUST be converted to the unit of the OTLP metric. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 4 | MUST | ➖ n_a | The unit MUST be translated from words to the UCUM abbreviation if it is in the following set of commonly-used units: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 5 | MUST | ➖ n_a | Prometheus HELP metadata, if present, MUST be added as the description of the OTLP metric. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 6 | MUST | ➖ n_a | Prometheus TYPE metadata, if present, MUST be used to determine the OTLP data type, and dictates type-specific conversion rules listed below. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 7 | MUST | ➖ n_a | The TYPE metadata MUST also be added to the OTLP metric.metadata under the `prometheus.type` key (e.g. `prometheus.type="unknown"`). | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |

#### Timestamps

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#timestamps) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | If present, the Prometheus Metric Sample’s Start timestamp (also referred to as the Created timestamp) MUST be converted to the Start timestamp of the OTLP data point. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 2 | SHOULD | ➖ n_a | If no start timestamp is present, the start time of the OTLP data point SHOULD be left unset. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 3 | MUST | ➖ n_a | If present, the Prometheus Metric Sample’s Timestamp MUST be converted to the Timestamp of the OTLP data point. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 4 | MUST | ➖ n_a | For metrics scraped from a Prometheus endpoint without an explicit timestamp, the timestamp of the OTLP data point MUST be set to the time of the scrape. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |

#### Counters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#counters) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | A Prometheus Counter MUST be converted to an OTLP Sum with `is_monotonic` equal to `true`. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 2 | MUST | ➖ n_a | Exemplars on the Prometheus Counter Sample MUST be converted to OpenTelemetry Exemplars on the OpenTelemetry Sum data point following the rules in Exemplars. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |

#### Gauges

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#gauges) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | A Prometheus Gauge MUST be converted to an OTLP Gauge. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |

#### Histograms

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#histograms) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | A Prometheus Histogram MUST be converted to an OTLP Histogram. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 2 | MUST | ➖ n_a | In the text format, Prometheus histograms buckets, count and sum are sent as separate samples and they MUST be merged together when forming an OTLP Histogram. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 3 | MUST | ➖ n_a | If `_count` is not present, the metric MUST be dropped. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 4 | MUST | ➖ n_a | If `_sum` is not present, the histogram’s sum MUST be unset. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 5 | MUST | ➖ n_a | Exemplars on the Prometheus Histogram Sample MUST be converted to OpenTelemetry Exemplars on the OpenTelemetry Histogram data point following the rules in Exemplars. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |

#### Native Histograms

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#native-histograms) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | A Prometheus Native Histogram with standard (exponential) schema (i.e. schemas -4 to 8) and which are of the integer and counter flavor MUST be converted to an OTLP Exponential Histogram as follows: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 2 | MUST | ➖ n_a | Overflow buckets MUST be dropped and not counted in the overall `Count`. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 3 | MUST | ➖ n_a | A Native histogram with custom buckets (NHCB) schema (i.e. schema -53) and which are of the integer and counter flavor MUST be converted to an OTLP Histogram as follows: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 4 | MUST | ➖ n_a | Native histograms of the float or gauge flavors MUST be dropped. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 5 | MUST | ➖ n_a | Native Histograms with `Schema` outside of the range [-4, 8] and not equal to -53 MUST be dropped. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |
| 6 | MUST | ➖ n_a | Exemplars on the Prometheus Native Histogram Sample MUST be converted to OpenTelemetry Exemplars on the OpenTelemetry Exponential Histogram data point following the rules in Exemplars. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. |

#### Summaries

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#summaries) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | Prometheus Summary MUST be converted to an OTLP Summary. | - | Prometheus Receiver (Prometheus → OTLP) не реализован: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приёма Prometheus-метрик и их перевода в OTLP нет. |
| 2 | MUST | ➖ n_a | In text formats where Prometheus Summaries are represented by multiple samples, samples with same metric family name MUST be merged together into a single OTLP Summary. | - | Prometheus Receiver (Prometheus → OTLP) не реализован: SDK только экспортирует метрики в Prometheus, приёма Prometheus-метрик и их перевода в OTLP нет. |
| 3 | MUST | ➖ n_a | If `_count` is not present, the metric MUST be dropped. | - | Prometheus Receiver (Prometheus → OTLP) не реализован: SDK только экспортирует метрики в Prometheus, приёма Prometheus-метрик и их перевода в OTLP нет. |
| 4 | MUST | ➖ n_a | If `_sum` is not present, the summary’s sum MUST be set to zero. | - | Prometheus Receiver (Prometheus → OTLP) не реализован: SDK только экспортирует метрики в Prometheus, приёма Prometheus-метрик и их перевода в OTLP нет. |

#### Dropped Types

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#dropped-types) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | The following Prometheus types MUST be dropped: | - | Prometheus Receiver (Prometheus → OTLP) не реализован: SDK только экспортирует метрики в Prometheus, приёма Prometheus-метрик и их перевода в OTLP нет. |

#### Exemplars

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#exemplars) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | MUST be converted to OpenTelemetry Exemplars as follows: | - | Prometheus Receiver (Prometheus → OTLP) не реализован: SDK только экспортирует метрики в Prometheus, приёма Prometheus-метрик и их перевода в OTLP нет. |
| 2 | MUST | ➖ n_a | If present, the timestamp MUST be used as the OpenTelemetry exemplar’s timestamp. | - | Prometheus Receiver (Prometheus → OTLP) не реализован: SDK только экспортирует метрики в Prometheus, приёма Prometheus-метрик и их перевода в OTLP нет. |
| 3 | MUST | ➖ n_a | If present, and if the values are valid Trace and Span IDs, the `trace_id` and `span_id` labels MUST be converted to the OpenTelemetry Exemplar’s Trace ID and Span ID, respectively. | - | Prometheus Receiver (Prometheus → OTLP) не реализован: SDK только экспортирует метрики в Prometheus, приёма Prometheus-метрик и их перевода в OTLP нет. |
| 4 | MUST | ➖ n_a | All labels other than `trace_id` and `span_id` MUST be added to the OpenTelemetry exemplar as filtered attributes. | - | Prometheus Receiver (Prometheus → OTLP) не реализован: SDK только экспортирует метрики в Prometheus, приёма Prometheus-метрик и их перевода в OTLP нет. |

#### Instrumentation Scope

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#instrumentation-scope) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | Labels with `otel_scope_` prefix MUST be dropped from all metric points and used as the Instrumentation Scope name (`otel_scope_name`), version (`otel_scope_version`), schema URL (`otel_scope_schema_url`), attributes (`otel_scope_[attribute]`). | - | Prometheus Receiver (Prometheus → OTLP) не реализован: SDK только экспортирует метрики в Prometheus, приёма Prometheus-метрик и их перевода в OTLP нет. |
| 2 | MUST | ➖ n_a | Metrics which do not have any label with `otel_scope_` prefix MUST be assigned an instrumentation scope identifying the entity performing the translation from Prometheus to OpenTelemetry (e.g. the collector’s Prometheus receiver). | - | Prometheus Receiver (Prometheus → OTLP) не реализован: SDK только экспортирует метрики в Prometheus, приёма Prometheus-метрик и их перевода в OTLP нет. |

### Сводка условных секций

| Раздел | Секция | Scope | Keywords | Ссылка |
|---|---|---|---|---|
| Propagators | GetAll | conditional:GetAll Getter (post-stable extension) | 4 | [spec](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#getall) |
| Prometheus Compatibility | Metric Metadata | conditional:Prometheus Receiver (Prometheus → OTLP) | 7 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#metric-metadata) |
| Prometheus Compatibility | Timestamps | conditional:Prometheus Receiver (Prometheus → OTLP) | 4 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#timestamps) |
| Prometheus Compatibility | Counters | conditional:Prometheus Receiver (Prometheus → OTLP) | 2 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#counters) |
| Prometheus Compatibility | Gauges | conditional:Prometheus Receiver (Prometheus → OTLP) | 1 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#gauges) |
| Prometheus Compatibility | Histograms | conditional:Prometheus Receiver (Prometheus → OTLP) | 5 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#histograms) |
| Prometheus Compatibility | Native Histograms | conditional:Prometheus Receiver (Prometheus → OTLP) | 6 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#native-histograms) |
| Prometheus Compatibility | Summaries | conditional:Prometheus Receiver (Prometheus → OTLP) | 4 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#summaries) |
| Prometheus Compatibility | Dropped Types | conditional:Prometheus Receiver (Prometheus → OTLP) | 1 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#dropped-types) |
| Prometheus Compatibility | Exemplars | conditional:Prometheus Receiver (Prometheus → OTLP) | 4 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#exemplars) |
| Prometheus Compatibility | Instrumentation Scope | conditional:Prometheus Receiver (Prometheus → OTLP) | 2 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#instrumentation-scope) |

## Ограничения платформы OneScript

| Ограничение | Влияние на спецификацию | Решение |
|---|---|---|
| Нет наносекундной точности | Временные метки с точностью до миллисекунд | Используется миллисекундная точность |
| Нет принудительной отмены фоновых заданий | У `ФоновоеЗадание` только `ОжидатьЗавершения(Таймаут)` ([OneScript#1672](https://github.com/EvilBeaver/OneScript/issues/1672)) | Мягкий таймаут: SDK перестаёт ждать и отбрасывает результат, задание продолжает работу; фоновые циклы останавливаются атомарным флагом |
| Число = System.Decimal (не IEEE 754) | NaN, Infinity, отрицательный ноль невозможны | Операции, порождающие NaN/Inf, выбрасывают исключение - требования к обработке NaN/Inf неприменимы |
| Нет varargs (переменного числа параметров) | Спека требует "variable number of attributes" (metrics) и "zero or more callbacks" | Используется контейнерный объект: `ОтелАтрибуты` для атрибутов, один полиморфный параметр `Callback = Неопределено \| Действие \| Массив` для callback-ов. Семантически эквивалентно. |

## Методология

### Процесс анализа

1. **Извлечение требований** (`extract_requirements.py`): загрузка 17 страниц спецификации, разбиение на секции, подсчёт MUST/SHOULD keywords; в отчёт входят только требования разделов со статусом Stable
2. **Генерация промптов** (`generate_prompts.py`): группировка секций по доменам, генерация промптов с JSON-схемой вывода для агентов
3. **Верификация** (general-purpose агенты): каждый агент анализирует 5-8 секций, записывает результат в JSON
4. **Сборка отчёта** (`assemble_report.py`): детерминированная сборка markdown из JSON-результатов

### Статусы

| Статус | Значение |
|---|---|
| ✅ found | Требование полностью реализовано с корректной семантикой |
| ⚠️ partial | Код существует, но не полностью соответствует спецификации |
| ❌ not_found | Реализация отсутствует |
| ➖ n_a | Неприменимо: ограничение платформы или не выполнено условие требования |

### Статистика извлечения

| Метрика | Значение |
|---|---|
| Страниц спецификации | 17 |
| Stable секций | 276 |
| Из них условных | 11 |
| Stable-требований | 909 |
| Из них universal | 869 |

