# Анализ соответствия спецификации OpenTelemetry v1.55.0

> **Версия спецификации**: [v1.55.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-04-14
> **Методология**: spec-first - извлечены все MUST/SHOULD требования из спецификации, затем каждое прослежено до кода

## Сводка (Stable)

Учитываются только требования из стабильных разделов спецификации с универсальной областью применения.

| Показатель | Значение |
|---|---|
| Всего keywords в спецификации | 824 |
| Stable + universal keywords | 694 |
| Conditional keywords | 13 |
| Development keywords | 123 |
| Найдено требований (Stable universal) | 693 |
| ✅ Реализовано (found) | 565 (81.5%) |
| ⚠️ Частично (partial) | 93 (13.4%) |
| ❌ Не реализовано (not_found) | 35 (5.1%) |
| ➖ Неприменимо (n_a) | 1 |
| **MUST/MUST NOT found** | 384/418 (91.9%) |
| **SHOULD/SHOULD NOT found** | 181/275 (65.8%) |

## Соответствие по разделам (Stable)

| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |
|---|---|---|---|---|---|---|
| Context | 14 | 1 | 0 | 0 | 15 | 93.3% |
| Baggage Api | 15 | 1 | 1 | 0 | 17 | 88.2% |
| Resource Sdk | 15 | 3 | 2 | 0 | 20 | 75.0% |
| Trace Api | 109 | 11 | 2 | 0 | 122 | 89.3% |
| Trace Sdk | 61 | 16 | 5 | 0 | 82 | 74.4% |
| Logs Api | 19 | 1 | 0 | 1 | 20 | 95.0% |
| Logs Sdk | 53 | 10 | 1 | 0 | 64 | 82.8% |
| Metrics Api | 88 | 9 | 3 | 0 | 100 | 88.0% |
| Metrics Sdk | 120 | 36 | 15 | 0 | 171 | 70.2% |
| Otlp Exporter | 17 | 4 | 4 | 0 | 25 | 68.0% |
| Propagators | 33 | 0 | 0 | 0 | 33 | 100.0% |
| Env Vars | 21 | 1 | 2 | 0 | 24 | 87.5% |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Context]** [MUST] The API MUST accept the following parameters:
* The `Context`.  
  There is no generic Attach(Context) method accepting a Context object. Attach is implemented via specialized methods: УстановитьЗначение(Ключ, Значение) accepts Key+Value instead of a Context, and СделатьСпанТекущим/СделатьBaggageТекущим are domain-specific. No method accepts a whole Context (ФиксированноеСоответствие) and makes it current. (`src/Ядро/Модули/ОтелКонтекст.os:203`)

- ❌ **[Baggage Api]** [MUST] Language API MUST treat both baggage names and values as case sensitive.  
  ОтелBaggage stores entries in a plain Соответствие (Map) which in OneScript/1C is case-insensitive for string keys. This means Get('a') and Get('A') return the same value, violating the spec requirement for case-sensitive names. КартаСоответствие (case-sensitive) from collectionos is not used. (-)

- ⚠️ **[Resource Sdk]** [MUST] Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK.  
  Detectors exist as separate classes (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) but are part of the same SDK package, not separate packages. There is no pluggable API for external detector packages. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17`)

- ⚠️ **[Resource Sdk]** [MUST] If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources.  
  Merge detects schema URL conflict and returns an empty resource (line 43), but does not report an error as required by the spec - it silently returns an undefined/empty resource. (`src/Ядро/Классы/ОтелРесурс.os:41`)

- ⚠️ **[Trace Api]** [MUST NOT] However, alternative implementations MUST NOT allow callers to create `Span`s directly.  
  В OneScript конструкторы всегда публичные - нет механизма сокрытия конструктора (private/package-private). Пользователь технически может вызвать Новый ОтелСпан(...) напрямую, хотя дизайн API направляет через Трассировщик. (`src/Трассировка/Классы/ОтелСпан.os:578`)

- ⚠️ **[Trace Api]** [MUST NOT] There MUST NOT be any API for creating a `Span` other than with a `Tracer`.  
  В OneScript конструкторы классов всегда публичные. Конструктор ОтелСпан доступен для вызова напрямую через Новый ОтелСпан(...), хотя единственный документированный API для создания спанов - через ОтелТрассировщик. (`src/Трассировка/Классы/ОтелСпан.os:578`)

- ⚠️ **[Trace Api]** [MUST NOT] This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`.  
  ОтелПостроительСпана.УстановитьРодителя() принимает ОтелСпан или ОтелКонтекстСпана в качестве родителя, а не полный объект Context. Спецификация требует принимать только полный Context. (`src/Трассировка/Классы/ОтелПостроительСпана.os:33`)

- ⚠️ **[Trace Api]** [MUST] The API MUST return a non-recording `Span` with the `SpanContext` in the parent `Context` (whether explicitly given or implicit current).  
  При отсутствии SDK ОтелГлобальный создает no-op SDK с ВсегдаВключен семплером и без процессоров. Трассировщик создает полный ОтелСпан (ЗаписьАктивна=true), а не non-recording спан (ЗаписьАктивна=false). Данные никуда не отправляются, но контракт IsRecording не соблюдается. (`src/Ядро/Модули/ОтелГлобальный.os:141`)

- ⚠️ **[Trace Api]** [MUST] If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.e., having a `SpanContext` with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags).  
  ОтелНоопСпан поддерживает конструктор по умолчанию с all-zero SpanContext, но в сценарии без SDK (ОтелГлобальный с пустым провайдером) трассировщик использует ВсегдаВключен семплер и создает полный ОтелСпан с случайными ID вместо empty non-recording спана. (`src/Трассировка/Классы/ОтелНоопСпан.os:277`)

- ⚠️ **[Trace Sdk]** [MUST] Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, `Sampler`, and (Development) TracerConfigurator) MUST be owned by the `TracerProvider`.  
  SpanProcessors, SpanLimits, Sampler и TracerConfigurator принадлежат TracerProvider, но IdGenerator отсутствует как конфигурируемый компонент провайдера - генерация ID выполняется глобальным модулем ОтелУтилиты (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:4`)

- ⚠️ **[Trace Sdk]** [MUST] For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated since 1.10.0] having the same name and version values as the `InstrumentationScope`.  
  No separate InstrumentationLibrary accessor exists. Only ОбластьИнструментирования() (InstrumentationScope) is available. The name and version values are the same, but there is no dedicated backwards-compatible InstrumentationLibrary getter. (`src/Трассировка/Классы/ОтелСпан.os:170`)

- ⚠️ **[Trace Sdk]** [MUST] implementations MAY choose not to expose (and store) the full parent Context of the Span but they MUST expose at least the full parent SpanContext.  
  Only parent span ID is stored and exposed via ИдРодительскогоСпана(). The full parent SpanContext (traceId, spanId, traceFlags, traceState as a SpanContext object) is not preserved - only the parent's spanId string. (`src/Трассировка/Классы/ОтелСпан.os:89`)

- ❌ **[Trace Sdk]** [MUST NOT] SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value.  
  The sampler module (ОтелСэмплер.os) does not handle the `rv` sub-key of OpenTelemetry TraceState at all. The ДолженСэмплировать method passes the parent TraceState through to the result, but there is no logic to detect or protect the `rv` sub-key from being overwritten. No explicit randomness handling exists. (-)

- ⚠️ **[Trace Sdk]** [MUST] The SDK MAY provide this functionality by allowing custom implementations of an interface like the java example below (name of the interface MAY be `IdGenerator`, name of the methods MUST be consistent with SpanContext), which provides extension points for two methods, one to generate a `SpanId` and one for `TraceId`.  
  The extension point uses method names СгенерироватьИдТрассировки/СгенерироватьИдСпана which are consistent with SpanContext property names (ИдТрассировки/ИдСпана). However, there is no formal IdGenerator interface class - it's a duck-typing convention via module-level variable. The mechanism works but lacks a formal interface definition. (`src/Ядро/Модули/ОтелУтилиты.os:63`)

- ⚠️ **[Metrics Api]** [MUST] MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  Thread-safety IS implemented via СинхронизированнаяКарта for the meters cache, but the class/method documentation does not explicitly state that the implementation is safe for concurrent use. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:241`)

- ⚠️ **[Metrics Api]** [MUST] Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  Thread-safety IS implemented via СинхронизированнаяКарта for instruments cache and descriptors, but the class/method documentation does not explicitly state that the implementation is safe for concurrent use. (`src/Метрики/Классы/ОтелМетр.os:493`)

- ⚠️ **[Metrics Api]** [MUST] Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  Thread-safety IS implemented via СинхронизированнаяКарта for accumulators and attributes, but the class/method documentation does not explicitly state that the implementation is safe for concurrent use. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:261`)

- ⚠️ **[Metrics Sdk]** [MUST] The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept.  
  ОтелПредставление defines ИсключенныеКлючиАтрибутов but ОтелМетр.ПрименитьПредставлениеКИнструменту and ОтелБазовыйСинхронныйИнструмент never apply the exclude-list. The field exists but exclusion is not implemented. (`src/Метрики/Классы/ОтелПредставление.os:56`)

- ⚠️ **[Metrics Sdk]** [MUST] The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept.  
  Same as above - the exclude-list is defined in ОтелПредставление but never applied, so the 'keep all other attributes' behavior in exclude-list context is not implemented. (`src/Метрики/Классы/ОтелПредставление.os:56`)

- ⚠️ **[Metrics Sdk]** [MUST] If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance.  
  Default aggregation per instrument type exists (Counter→Sum, Histogram→ExplicitBucketHistogram, Gauge→LastValue), but it is hardcoded in ОтелМетр, not configurable per MetricReader instance. MetricReader has no aggregation property. (`src/Метрики/Классы/ОтелМетр.os:48`)

- ⚠️ **[Metrics Sdk]** [MUST] If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST apply the default aggregation cardinality limit the `MetricReader` is configured with.  
  Default cardinality limit of 2000 is hardcoded in ОтелБазовыйСинхронныйИнструмент and ОтелМетр. The spec requires the default to come from MetricReader configuration, but ОтелПериодическийЧитательМетрик has no cardinality limit property. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253`)

- ⚠️ **[Metrics Sdk]** [MUST] The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic scale parameter will not exceed.  
  MaxScale parameter (НачальнаяШкала, default 20) is maintained as the maximum scale. However, there is no explicit minimum scale parameter - the scale can decrease without bound through ПонизитьШкалуНа1 calls. (`src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:302`)

- ⚠️ **[Metrics Sdk]** [MUST] Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that observations made or produced by executing callbacks only apply to the intended `MetricReader` during collection.  
  Callbacks are invoked during collection via ВызватьМультиОбратныеВызовы(), but observations are not scoped to a specific MetricReader. With multiple readers, callbacks are invoked independently per reader, but there is no isolation mechanism - the ВнешниеНаблюдения array is shared and cleared after each collection without reader-specific scoping. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:157`)

- ⚠️ **[Metrics Sdk]** [MUST] If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit string.  
  Параметр ЕдиницаИзмерения имеет значение по умолчанию "" (пустая строка), что корректно обрабатывает случай "не предоставлен". Однако если явно передать Неопределено (null), значение не нормализуется в пустую строку - оно передаётся в конструктор ОтелБазовыйСинхронныйИнструмент как есть. (`src/Метрики/Классы/ОтелМетр.os:48`)

- ⚠️ **[Metrics Sdk]** [MUST] If a description is not provided or the description is null, the Meter MUST treat it the same as an empty description string.  
  Параметр Описание имеет значение по умолчанию "" (пустая строка), что корректно обрабатывает случай "не предоставлен". Однако если явно передать Неопределено (null), значение не нормализуется в пустую строку - оно передаётся в конструктор ОтелБазовыйСинхронныйИнструмент как есть. (`src/Метрики/Классы/ОтелМетр.os:48`)

- ⚠️ **[Metrics Sdk]** [MUST] A new `ExemplarReservoir` MUST be created for every known timeseries data point, as determined by aggregation and view configuration.  
  One ОтелРезервуарЭкземпляров is created per instrument, not per timeseries data point. The reservoir internally manages data per-key (КлючАтрибутов) via СинхронизированнаяКарта, which is functionally equivalent but architecturally different from a new reservoir per timeseries. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265`)

- ⚠️ **[Metrics Sdk]** [MUST] although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reservoir - Paragraph 2).  
  The custom reservoir from the View is set per-instrument via ПрименитьПредставлениеКИнструменту, not per metric-timeseries. The same reservoir instance is shared across all timeseries of an instrument, using internal keying by КлючАтрибутов instead of separate instantiation. (`src/Метрики/Классы/ОтелМетр.os:534`)

- ⚠️ **[Metrics Sdk]** [MUST NOT] `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure).  
  Export delegates to Транспорт.Отправить() which uses HTTP with default timeouts, but there is no explicit configurable timeout on the Export method itself (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:29`)

- ⚠️ **[Metrics Sdk]** [MUST] `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure).  
  Export relies on HTTP transport timeouts implicitly, no explicit timeout limit with error result (Failure) is configured in the exporter (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:29`)

- ❌ **[Metrics Sdk]** [MUST] The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry.  
  No explicit numerical limits handling found in the metrics SDK. There is no graceful error handling for overflow, underflow, or other numerical edge cases in aggregators or instruments. (-)

- ❌ **[Metrics Sdk]** [MUST] If the SDK receives float/double values from Instruments, it MUST handle all the possible values.  
  No explicit handling of special float/double values (NaN, Infinity, etc.) found in the metrics SDK. Instruments and aggregators accept numeric values without validation or special-value handling. (-)

- ⚠️ **[Metrics Sdk]** [MUST] MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.  
  Meter creation uses СинхронизированнаяКарта (thread-safe map) for caching meters. However, the Закрыт flag is a plain Булево (not АтомарноеБулево), so concurrent Закрыть()/ПолучитьМетр() calls have a data race. СброситьБуфер() and Закрыть() do not use locks for iteration over ЧитателиМетрик. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:241`)

- ⚠️ **[Metrics Sdk]** [MUST] ExemplarReservoir - all methods MUST be safe to be called concurrently.  
  Uses СинхронизированнаяКарта for bucket storage and АтомарноеЧисло for measurement counters. However, the array inside each bucket (МассивЭкземпляров) is a plain Массив - concurrent Предложить() calls can race on МассивЭкземпляров.Количество() check and МассивЭкземпляров.Добавить()/indexed assignment. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:167`)

- ❌ **[Env Vars]** [MUST] When `OTEL_CONFIG_FILE` is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored.  
  OTEL_CONFIG_FILE and OTEL_EXPERIMENTAL_CONFIG_FILE are not referenced anywhere in the codebase. Declarative configuration via file-based config is not implemented. (-)

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Baggage Api]** [SHOULD NOT] The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation.  
  Context key for Baggage is exposed via exported function ОтелКонтекст.КлючBaggage() (line 53), giving API users direct access to the internal Context Key. The spec recommends users should not need to access this key directly. (`src/Ядро/Модули/ОтелКонтекст.os:53`)

- ⚠️ **[Resource Sdk]** [SHOULD] failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error.  
  Errors during detection are caught but logged at debug level (Лог.Отладка), not treated as actual errors per OTel Error Handling principles which would require warning/error level logging. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:25`)

- ❌ **[Resource Sdk]** [SHOULD] In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles.  
  No error handling around OTEL_RESOURCE_ATTRIBUTES parsing in СоздатьРесурс(). If РаскодироватьСтроку fails on invalid percent encoding, the exception propagates instead of discarding the entire value. (-)

- ❌ **[Resource Sdk]** [SHOULD] In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles.  
  No error reporting mechanism for OTEL_RESOURCE_ATTRIBUTES parsing failures. Errors are not caught and reported per OTel Error Handling principles. (-)

- ⚠️ **[Trace Api]** [SHOULD] In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged.  
  Для пустой строки имя устанавливается в пустую строку естественным образом, но нет явной валидации и нормализации Неопределено (аналог null) к пустой строке (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58`)

- ❌ **[Trace Api]** [SHOULD] In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged.  
  Нет логирования сообщения о невалидном имени при передаче пустой строки или Неопределено в ПолучитьТрассировщик (-)

- ⚠️ **[Trace Api]** [SHOULD NOT] The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation.  
  Контекстный ключ спана доступен публично через ОтелКонтекст.КлючСпана(), хотя существуют convenience-методы СпанИзКонтекста и КонтекстСоСпаном, абстрагирующие от ключа (`src/Ядро/Модули/ОтелКонтекст.os:44`)

- ⚠️ **[Trace Api]** [SHOULD NOT] To prevent misuse, implementations SHOULD NOT provide access to a `Span`'s attributes besides its `SpanContext`.  
  ОтелСпан.Атрибуты() является публичным методом (Экспорт) и предоставляет прямой доступ к атрибутам спана. В OneScript нет возможности разделить API-интерфейс (без доступа к атрибутам) и SDK-интерфейс (с доступом для экспорта), поэтому атрибуты доступны всем. (`src/Трассировка/Классы/ОтелСпан.os:134`)

- ⚠️ **[Trace Api]** [SHOULD NOT] If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type).  
  ОтелНоопСпан зарегистрирован как публичный класс в lib.config (строка 32). Хотя OneScript требует регистрации классов для инстанцирования, можно было бы экспортировать только фабричную функцию. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ⚠️ **[Trace Api]** [SHOULD] If a new type is required to be publicly exposed, it SHOULD be named `NonRecordingSpan`.  
  Класс назван ОтелНоопСпан (NoopSpan), а не ОтелНеЗаписывающийСпан (NonRecordingSpan) как рекомендует спецификация. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ⚠️ **[Trace Api]** [SHOULD] Link - Links are immutable and SHOULD be safe for concurrent use by default.  
  Линки хранятся как Соответствие (Map), не имеют отдельного иммутабельного класса и не документированы как потокобезопасные или иммутабельные. (`src/Трассировка/Классы/ОтелСпан.os:372`)

- ❌ **[Trace Api]** [SHOULD] If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly without instantiating a new `Span`.  
  Трассировщик всегда создает новый экземпляр спана. Нет проверки, что родительский спан уже является non-recording, и нет логики для его прямого возврата. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] SDKs SHOULD return a valid no-op Tracer for these calls, if possible.  
  После Закрыть() метод ПолучитьТрассировщик возвращает обычный ОтелТрассировщик, а не выделенный no-op трассировщик; Включен() этого трассировщика вернёт Истина (процессоры существуют, хоть и закрыты), поэтому поведение не эквивалентно no-op (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:66`)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Синхронный метод Закрыть() - Процедура без возвращаемого значения; асинхронный ЗакрытьАсинхронно() возвращает Обещание, но основной синхронный метод не предоставляет обратной связи о результате (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:107`)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Синхронный метод Закрыть() не имеет встроенного таймаута и блокирует выполнение до завершения всех процессоров; асинхронный ЗакрытьАсинхронно() поддерживает таймаут через Обещание, но основной метод - нет (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:107`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Синхронный метод СброситьБуфер() - Процедура без возвращаемого значения; асинхронный СброситьБуферАсинхронно() возвращает Обещание, но основной синхронный метод не предоставляет обратной связи (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Синхронный метод СброситьБуфер() не имеет встроенного таймаута; асинхронный СброситьБуферАсинхронно() поддерживает таймаут через Обещание, но основной метод блокирует до завершения (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98`)

- ⚠️ **[Trace Sdk]** [SHOULD NOT] However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set.  
  No filtering of RECORD_ONLY spans (IsRecording=true, Sampled=false) at the processor or exporter level. If a custom sampler returns RECORD_ONLY, the span would still reach the exporter without checking the Sampled flag. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37`)

- ⚠️ **[Trace Sdk]** [SHOULD NOT] Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not.  
  No filtering mechanism in processor or exporter to exclude spans without the Sampled flag. RECORD_ONLY spans from custom samplers would reach the exporter. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37`)

- ⚠️ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values.  
  TraceIDs are generated using УникальныйИдентификатор (UUID) which provides substantial randomness but does not explicitly conform to the W3C Trace Context Level 2 requirement of 56 bits of randomness in the rightmost 7 bytes. UUID v4 has deterministic version and variant bits that reduce full randomness, and there is no explicit verification of the Level 2 randomness specification. (`src/Ядро/Модули/ОтелУтилиты.os:78`)

- ❌ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements.  
  The ВычислитьФлагиТрассировки function in ОтелТрассировщик.os only sets flag value 0 or 1 (sampled bit). The W3C Random flag (bit 1, value 0x02) is never set. There is no code that sets the Random trace flag for root span contexts. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the `rv` sub-key of the OpenTelemetry TraceState.  
  The TraceIdRatioBased sampler (СэмплироватьПоДоле) hashes TraceID to make sampling decisions, implicitly presuming TraceID randomness. However, there is no logic to check for the `rv` sub-key in TraceState and use it as an alternative randomness source when present. (`src/Трассировка/Модули/ОтелСэмплер.os:277`)

- ❌ **[Trace Sdk]** [SHOULD] If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated.  
  The SDK provides an IdGenerator extension point (ОтелУтилиты.УстановитьГенераторИд), but the custom generator has no way to signal whether generated IDs meet randomness requirements. There is no mechanism for the extension to control or influence the Random trace flag. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`.  
  The options are named МаксСобытий (MaxEvents) and МаксЛинков (MaxLinks) rather than EventCountLimit and LinkCountLimit. The functionality is equivalent but the naming convention does not match. (`src/Трассировка/Классы/ОтелЛимитыСпана.os:34`)

- ⚠️ **[Trace Sdk]** [SHOULD] After the call to `Shutdown`, subsequent calls to `OnStart`, `OnEnd`, or `ForceFlush` are not allowed. SDKs SHOULD ignore these calls gracefully, if possible.  
  ОтелПакетныйПроцессорСпанов (через базовый класс) проверяет флаг Закрыт в методе Обработать (OnEnd-путь), но СброситьБуфер (ForceFlush) не проверяет флаг. ОтелПростойПроцессорСпанов не имеет флага Закрыт и не игнорирует вызовы после Shutdown. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43`)

- ❌ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод Закрыть() определён как Процедура (void), не возвращает результат. Нет механизма обратного вызова или индикации успеха/неудачи/таймаута. (-)

- ❌ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() определён как Процедура (void), не возвращает результат. Нет механизма обратного вызова или индикации успеха/неудачи/таймаута. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  ForceFlush (СброситьБуфер) is defined as Процедура (void return). Failure can be signaled via exception, but there is no way to distinguish success from timeout - the caller only knows the call completed or threw. (`src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:19`)

- ⚠️ **[Logs Api]** [SHOULD] The API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response.  
  Метод Включен() задокументирован, но документация не содержит указания о необходимости вызывать его каждый раз перед emit для получения актуального ответа. Комментарий описывает только назначение метода, но не динамическую природу возвращаемого значения. (`src/Логирование/Классы/ОтелЛоггер.os:28`)

- ⚠️ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Синхронный Закрыть() не возвращает статус (void); асинхронный ЗакрытьАсинхронно() возвращает Обещание, но без явного статуса успеха/ошибки/таймаута (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:143`)

- ⚠️ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Метод Закрыть() провайдера не принимает параметр таймаута; ОтелКомпозитныйПроцессорЛогов.Закрыть поддерживает ТаймаутМс, но провайдер его не пробрасывает (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:116`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Синхронный СброситьБуфер() не возвращает статус (void); асинхронный СброситьБуферАсинхронно() возвращает Обещание, но без явного статуса успеха/ошибки/таймаута (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:131`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  СброситьБуфер() не возвращает явный ERROR-статус; исключения процессоров пробрасываются, но не как возвращаемый статус (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  СброситьБуфер() не возвращает явный NO ERROR статус (метод void) (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  СброситьБуфер() провайдера не принимает таймаут; ОтелКомпозитныйПроцессорЛогов.СброситьБуфер поддерживает ТаймаутМс, но провайдер его не использует (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD NOT] This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD NOT block or throw exceptions.  
  Simple processor (ОтелПростойПроцессорЛогов.ПриПоявлении) blocks synchronously during export with a lock and re-throws exceptions via ВызватьИсключение. Batch processor is non-blocking (adds to buffer). Composite processor swallows exceptions but simple does not. (`src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:18-30`)

- ❌ **[Logs Sdk]** [SHOULD] To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecord` be used for any concurrent processing, such as in a batching processor.  
  No documentation or code recommending cloning of logRecord for concurrent processing. The batch processor (ОтелБазовыйПакетныйПроцессор.Обработать) adds the element directly to the buffer without cloning or any advisory comment. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Synchronous Закрыть() is a void procedure (Процедура) that does not return success/failure/timeout status. The async variant ЗакрытьАсинхронно() returns an Обещание (Promise) but does not distinguish between success, failure, and timeout. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:116-123`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Synchronous СброситьБуфер() is a void procedure (Процедура) that does not return success/failure/timeout status. The async variant СброситьБуферАсинхронно() returns an Обещание (Promise) but does not distinguish between success, failure, and timeout. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107-111`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() определена как Процедура (void), не возвращает результат. Вызывающий не может узнать, был ли ForceFlush успешен, завершился с ошибкой или по таймауту. Интерфейс ИнтерфейсЭкспортерЛогов также определяет СброситьБуфер() как void. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:45`)

- ❌ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax.  
  API documentation for sync instrument creation methods does not explicitly mention that the name must conform to instrument name syntax rules. (-)

- ❌ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax.  
  API documentation for async instrument creation methods does not explicitly mention that the name must conform to instrument name syntax rules. (-)

- ⚠️ **[Metrics Api]** [SHOULD] Callback functions SHOULD be reentrant safe.  
  Callback functions are invoked from ОтелБазовыйНаблюдаемыйИнструмент but the documentation does not explicitly state that callbacks should be reentrant safe. (-)

- ⚠️ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT take an indefinite amount of time.  
  There is no explicit documentation warning users that callback functions should not take an indefinite amount of time. (-)

- ⚠️ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same `attributes`) across all registered callbacks.  
  There is no explicit documentation warning or enforcement that callbacks should not make duplicate observations with the same attributes. (-)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response.  
  The Enabled() method exists and documentation comments mention its purpose, but it does not explicitly document that authors need to call it each time before recording. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:192`)

- ⚠️ **[Metrics Api]** [SHOULD] The increment value is expected to be non-negative. This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative.  
  The method comment mentions 'положительное значение для добавления' but does not explicitly phrase it as 'non-negative' in the API documentation intended for end users. (`src/Метрики/Классы/ОтелСчетчик.os:14`)

- ⚠️ **[Metrics Api]** [SHOULD NOT] This API SHOULD NOT validate this value, that is left to implementations of the API.  
  Counter.Добавить() validates the value and silently drops negative values (Если Значение < 0 Тогда Возврат). The spec says the API SHOULD NOT validate, but the implementation does validate by rejecting negative values. (`src/Метрики/Классы/ОтелСчетчик.os:22`)

- ❌ **[Metrics Api]** [SHOULD] This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative.  
  Документация метода Записать в ОтелГистограмма.os не упоминает, что значение должно быть неотрицательным. Комментарий содержит только 'Значение - Число - измеренное значение' без указания на ожидание неотрицательности. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Synchronous Закрыть() is a void procedure with no return value indicating success, failure, or timeout. The async ЗакрытьАсинхронно() returns an Обещание which can signal failure, but the primary synchronous API has no status reporting. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:130`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  The MeterProvider's Закрыть() has no explicit timeout. The underlying reader's Закрыть has a timeout for waiting on the background export task (ИнтервалЭкспортаМс * МножительТаймаутаОжидания), but there is no overall timeout for the provider-level shutdown. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:130`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Synchronous СброситьБуфер() is a void procedure with no return value. The async СброситьБуферАсинхронно() returns an Обещание, but the primary synchronous API provides no status indication. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:115`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  СброситьБуфер() is a void procedure that does not return any error or success status. Errors in underlying readers are silently handled. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:115`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  The MeterProvider's СброситьБуфер() has no explicit timeout mechanism. The async variant СброситьБуферАсинхронно() returns an Обещание that supports timeouts, but the synchronous API has no timeout. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:115`)

- ⚠️ **[Metrics Sdk]** [SHOULD] Additionally, implementations SHOULD support configuring an exclude-list of attribute keys.  
  ОтелПредставление has ИсключенныеКлючиАтрибутов field defined in the constructor and getter, but the exclude-list is never applied during measurement filtering in ОтелБазовыйСинхронныйИнструмент - only the allow-list (РазрешенныеКлючиАтрибутов) is used. (`src/Метрики/Классы/ОтелПредставление.os:56`)

- ⚠️ **[Metrics Sdk]** [SHOULD] The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument:  
  Processing logic is partially implemented: default aggregation is applied when no Views are registered, and the first matching View is applied. However, the spec requires each matching View to be applied independently (producing separate streams), while the code applies only the first matching View and returns. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:192`)

- ❌ **[Metrics Sdk]** [SHOULD] If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning.  
  No conflict detection or warning is implemented when Views produce conflicting metric identities. Views are applied without checking for conflicts. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asynchronous instrument to use the Explicit bucket histogram aggregation) the implementation SHOULD emit a warning and proceed as if the View did not  
  No validation of semantic compatibility between View aggregation and instrument type is implemented. No warning is emitted for incompatible View-instrument combinations. (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpDownCounter` or `ObservableGauge`).  
  The histogram aggregator always collects the sum field (ОтелАгрегаторГистограммы.Записать line 51). There is no check for the instrument type to skip sum collection for instruments that record negative measurements. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different (e.g. for backward compatibility reasons in a stable SDK release).  
  Default boundaries are used when none provided, but the values [0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 10000] are missing 7500 compared to the spec's default [0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000]. (`src/Метрики/Классы/ОтелАгрегаторГистограммы.os:118`)

- ⚠️ **[Metrics Sdk]** [SHOULD] The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks.  
  Observable instruments only produce data through callbacks (ВызватьCallbackИСобрать), but ДобавитьВнешниеНаблюдения is a public method that can be called from outside registered callbacks without enforcement. (`src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:58`)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback execution.  
  Callbacks are invoked synchronously in ВызватьCallbackИСобрать with a try-catch for error handling but no timeout mechanism. An infinite callback would block the collection thread indefinitely. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardinality_limit` value defined for the stream, that value SHOULD be used.  
  ОтелПредставление has ЛимитМощностиАгрегации field, but ПрименитьПредставлениеКИнструменту in ОтелМетр.os does not apply the View's cardinality limit to the instrument's ЛимитМощности (`src/Метрики/Классы/ОтелПредставление.os:92`)

- ❌ **[Metrics Sdk]** [SHOULD] If there is no matching view, but the `MetricReader` defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used.  
  ОтелПериодическийЧитательМетрик does not define a per-instrument-type default cardinality limit; the cardinality limit is always set from the Meter's default, not from the MetricReader (-)

- ❌ **[Metrics Sdk]** [SHOULD] Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality.  
  ОтелБазовыйНаблюдаемыйИнструмент has no cardinality limiting; all callback observations are collected without any limit or preference for first-observed attributes (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible.  
  Warning message reports the conflicting parameters but does not include specific instructions on how to resolve the conflict (e.g., suggesting use of a View) (`src/Метрики/Классы/ОтелМетр.os:573`)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning.  
  ПроверитьКонфликтДескриптора does not check if a View resolves the description conflict; it always emits a warning when descriptions differ regardless of View configuration (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning.  
  Warning message does not mention Views or include any View-based resolution recipe (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument registration.  
  A warning is emitted, but the code returns the existing instrument instance rather than reporting both Metric objects; data from the duplicate registration merges into the original instrument (`src/Метрики/Классы/ОтелМетр.os:573`)

- ❌ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax  
  Методы создания инструментов (СоздатьСчетчик, СоздатьГистограмму и др.) в ОтелМетр не содержат валидации имени инструмента по синтаксическому шаблону спецификации. Имя нормализуется в нижний регистр (НРег), но не проверяется на соответствие допустимым символам. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name.  
  Нет валидации имени инструмента, поэтому нет и генерации ошибки при невалидном имени. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided.  
  Метод ПроверитьСовет выводит предупреждение через Лог.Предупреждение при невалидных типах advisory-параметров, но не обнуляет невалидный параметр - дальнейший код может попытаться использовать невалидное значение вместо того, чтобы действовать так, как будто параметр не был предоставлен. (`src/Метрики/Классы/ОтелМетр.os:648`)

- ⚠️ **[Metrics Sdk]** [SHOULD] The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars.  
  The reservoir creates new Соответствие objects for each exemplar in СоздатьЭкземпляр(), allocating on every measurement offer rather than avoiding allocations. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:112`)

- ⚠️ **[Metrics Sdk]** [SHOULD] and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled.  
  The implementation uses a last-seen strategy (replaces the exemplar on each measurement) instead of uniformly-weighted sampling per bucket. The spec permits this as an alternative (MAY keep last seen), but the SHOULD for uniform sampling is not met. (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50`)

- ❌ **[Metrics Sdk]** [SHOULD] `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СобратьИЭкспортировать is a void Процедура that catches errors internally and logs them, but does not return any result to the caller indicating success, failure, or timeout. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] SDKs SHOULD return some failure for these calls, if possible.  
  After Закрыть(), СброситьБуфер() (Collect) still executes СобратьИЭкспортировать() without checking Закрыт flag - no failure is returned for post-shutdown calls (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Закрыть() is a Процедура (void), does not return success/failure/timeout status to the caller (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:105`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD collect metrics, call `Export(batch)` and `ForceFlush()` on the configured Push Metric Exporter.  
  СброситьБуфер() calls СобратьИЭкспортировать() which collects and exports, but does not call Экспортер.СброситьБуфер() (ForceFlush on the exporter) (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() is a Процедура (void), does not return success/failure/timeout status (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  СброситьБуфер() is a void procedure with no return value - errors are caught silently in СобратьИЭкспортировать() (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88`)

- ❌ **[Metrics Sdk]** [SHOULD] Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsupported Aggregation or Aggregation Temporality, as this condition can be corrected by a change of `MetricReader` configuration.  
  ОтелЭкспортерМетрик.Экспортировать() does not validate aggregation type or temporality - no error is reported for unsupported aggregation/temporality combinations (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() on exporter is a void procedure (Процедура), does not return success/failure status (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47`)

- ⚠️ **[Metrics Sdk]** [SHOULD] Shutdown SHOULD be called only once for each `MetricExporter` instance.  
  Закрыть() uses АтомарноеБулево so multiple calls are safe, but subsequent Export calls return Ложь without explicitly returning a Failure result as spec requires (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:53`)

- ❌ **[Metrics Sdk]** [SHOULD] `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of produced metrics.  
  ИнтерфейсПродюсерМетрик has only Произвести() method with no parameters - no way to configure AggregationTemporality for produced metrics (-)

- ❌ **[Otlp Exporter]** [SHOULD] However, if they are already implemented, they SHOULD continue to be supported as they were part of a stable release of the specification.  
  Obsolete env vars OTEL_EXPORTER_OTLP_SPAN_INSECURE and OTEL_EXPORTER_OTLP_METRIC_INSECURE are not supported. The requirement is conditional ('if they are already implemented') and these were never implemented in this SDK, but they are still not supported. (-)

- ⚠️ **[Otlp Exporter]** [SHOULD] The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default.  
  Default protocol is 'http/json' instead of the recommended 'http/protobuf'. The SDK defaults to http/json at line 468 (ПараметрСигналаИлиОбщий default) and line 169 (СоздатьТранспорт default). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:468`)

- ⚠️ **[Otlp Exporter]** [SHOULD] SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them.  
  SDK supports grpc (ОтелGrpcТранспорт) and http/json (ОтелHttpТранспорт), but http/protobuf config value is accepted and routed to ОтелHttpТранспорт which sends JSON, not actual protobuf over HTTP. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:468`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If they support only one, it SHOULD be `http/protobuf`.  
  SDK supports grpc and http/json but not true http/protobuf transport. The HTTP transport always sends JSON-encoded data regardless of the configured protocol value. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:468`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If no configuration is provided the default transport SHOULD be `http/protobuf` unless SDKs have good reasons to choose `grpc` as the default (e.g. for backward compatibility reasons when `grpc` was already the default in a stable SDK release).  
  Default protocol is 'http/json' (line 468), not the recommended 'http/protobuf'. The SDK does not support true http/protobuf transport. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:468`)

- ❌ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter.  
  No User-Agent header is emitted by ОтелHttpТранспорт or ОтелGrpcТранспорт. No code sets a User-Agent header in the export requests. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The format of the header SHOULD follow RFC 7231.  
  User-Agent header is not implemented at all, so RFC 7231 format compliance is not applicable. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The resulting User-Agent SHOULD include the exporter's default User-Agent string.  
  User-Agent header is not implemented. No default User-Agent string exists to include. (-)

- ❌ **[Env Vars]** [SHOULD] If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied.  
  Функция Включено() возвращает НРег(Значение) = "true" без логирования предупреждения при нераспознанных значениях (например, "yes", "1", "on"). При некорректном булевом значении молча возвращается Ложь без предупреждения пользователю. (-)

- ⚠️ **[Env Vars]** [SHOULD] All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior.  
  Единственная булева переменная OTEL_ENABLED имеет значение по умолчанию "true". По спецификации безопасное поведение по умолчанию должно соответствовать значению false. Рекомендуемый подход - использовать OTEL_SDK_DISABLED=false (SDK включён) вместо OTEL_ENABLED=true. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:666`)

## Детальный анализ по разделам (Stable)

### Context

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:130` |  |
| 2 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:127` |  |
| 3 | MUST | ✅ found | In the cases where an extremely clear, pre-existing option is not available, OpenTelemetry MUST provide its own `Context` implementation. | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### Create a key

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#create-a-key)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The API MUST accept the following parameter: | `src/Ядро/Модули/ОтелКонтекст.os:35` |  |
| 5 | SHOULD NOT | ✅ found | Multiple calls to `CreateKey` with the same name SHOULD NOT return the same value unless language constraints dictate otherwise. | `src/Ядро/Модули/ОтелКонтекст.os:36` |  |
| 6 | MUST | ✅ found | The API MUST return an opaque object representing the newly created key. | `src/Ядро/Классы/ОтелКлючКонтекста.os:1` |  |

#### Get value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Ядро/Модули/ОтелКонтекст.os:113` |  |
| 8 | MUST | ✅ found | The API MUST return the value in the `Context` for the specified key. | `src/Ядро/Модули/ОтелКонтекст.os:114` |  |

#### Set value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Ядро/Модули/ОтелКонтекст.os:127` |  |
| 10 | MUST | ✅ found | The API MUST return a new `Context` containing the new value. | `src/Ядро/Модули/ОтелКонтекст.os:130` |  |

#### Optional Global operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#optional-global-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | These operations SHOULD only be used to implement automatic scope switching and define higher level APIs by SDK components and OpenTelemetry instrumentation libraries. | `src/Ядро/Модули/ОтелКонтекст.os:63` |  |

#### Get current Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-current-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST return the `Context` associated with the caller's current execution unit. | `src/Ядро/Модули/ОтелКонтекст.os:63` |  |

#### Attach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#attach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ⚠️ partial | The API MUST accept the following parameters: * The `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:203` | There is no generic Attach(Context) method accepting a Context object. Attach is implemented via specialized methods: УстановитьЗначение(Ключ, Значение) accepts Key+Value instead of a Context, and СделатьСпанТекущим/СделатьBaggageТекущим are domain-specific. No method accepts a whole Context (ФиксированноеСоответствие) and makes it current. |
| 14 | MUST | ✅ found | The API MUST return a value that can be used as a `Token` to restore the previous `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:207` |  |

#### Detach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#detach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The API MUST accept the following parameters: * A `Token` that was returned by a previous call to attach a `Context`. | `src/Ядро/Классы/ОтелОбласть.os:22` |  |

### Baggage Api

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Each name in `Baggage` MUST be associated with exactly one value. | `src/Ядро/Классы/ОтелBaggage.os:3` |  |
| 2 | SHOULD NOT | ✅ found | Language API SHOULD NOT restrict which strings are used as baggage names. | `src/Ядро/Классы/ОтелBaggage.os:38` |  |
| 3 | MUST | ✅ found | Language API MUST accept any valid UTF-8 string as baggage value in `Set` and return the same value from `Get`. | `src/Ядро/Классы/ОтелBaggage.os:68` |  |
| 4 | MUST | ❌ not_found | Language API MUST treat both baggage names and values as case sensitive. | - | ОтелBaggage stores entries in a plain Соответствие (Map) which in OneScript/1C is case-insensitive for string keys. This means Get('a') and Get('A') return the same value, violating the spec requirement for case-sensitive names. КартаСоответствие (case-sensitive) from collectionos is not used. |
| 5 | MUST | ✅ found | The Baggage API MUST be fully functional in the absence of an installed SDK. | `src/Ядро/Классы/ОтелBaggage.os:1` |  |
| 6 | MUST | ✅ found | The `Baggage` container MUST be immutable, so that the containing `Context` also remains immutable. | `src/Ядро/Классы/ОтелBaggage.os:156` |  |

#### Get Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | To access the value for a name/value pair set by a prior event, the Baggage API MUST provide a function that takes the name as input, and returns a value associated with the given name, or null if the given name is not present. | `src/Ядро/Классы/ОтелBaggage.os:38` |  |

#### Get All Values

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#get-all-values)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST NOT | ✅ found | The order of name/value pairs MUST NOT be significant. | `src/Ядро/Классы/ОтелBaggage.os:103` |  |

#### Set Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | To record the value for a name/value pair, the Baggage API MUST provide a function which takes a name, and a value as input. | `src/Ядро/Классы/ОтелBaggage.os:68` |  |

#### Remove Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#remove-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | To delete a name/value pair, the Baggage API MUST provide a function which takes a name as input. | `src/Ядро/Классы/ОтелBaggage.os:82` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | If an implementation of this API does not operate directly on the Context, it MUST provide the following functionality to interact with a Context instance: | `src/Ядро/Модули/ОтелКонтекст.os:156` |  |
| 12 | SHOULD NOT | ⚠️ partial | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:53` | Context key for Baggage is exposed via exported function ОтелКонтекст.КлючBaggage() (line 53), giving API users direct access to the internal Context Key. The spec recommends users should not need to access this key directly. |
| 13 | SHOULD | ✅ found | If the language has support for implicitly propagated Context (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Классы/ОтелBaggage.os:16` |  |
| 14 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Классы/ОтелBaggage.os:16` |  |

#### Clear Baggage in the Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#clear-baggage-in-the-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | To avoid sending any name/value pairs to an untrusted process, the Baggage API MUST provide a way to remove all baggage entries from a context. | `src/Ядро/Классы/ОтелBaggage.os:94` |  |

#### Propagation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#propagation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The API layer or an extension package MUST include the following Propagators: A TextMapPropagator implementing the W3C Baggage Specification. | `src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:1` |  |

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
| 1 | MUST | ✅ found | The SDK MUST allow for creation of `Resources` and for associating them with telemetry. | `src/Ядро/Классы/ОтелРесурс.os:94` |  |
| 2 | MUST | ✅ found | all `Span`s produced by any `Tracer` from the provider MUST be associated with this `Resource`. | `src/Трассировка/Классы/ОтелТрассировщик.os:85` |  |

#### SDK-provided resource attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#sdk-provided-resource-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The SDK MUST provide access to a Resource with at least the attributes listed at Semantic Attributes with SDK-provided Default Value. | `src/Ядро/Классы/ОтелРесурс.os:102` |  |
| 4 | MUST | ✅ found | This resource MUST be associated with a `TracerProvider` or `MeterProvider` if another resource was not explicitly specified. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:253` |  |

#### Create

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#create)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The interface MUST provide a way to create a new resource, from `Attributes`. | `src/Ядро/Классы/ОтелРесурс.os:94` |  |

#### Merge

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#merge)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | The interface MUST provide a way for an old resource and an updating resource to be merged into a new resource. | `src/Ядро/Классы/ОтелРесурс.os:39` |  |
| 7 | MUST | ✅ found | The resulting resource MUST have all attributes that are on any of the two input resources. | `src/Ядро/Классы/ОтелРесурс.os:53` |  |
| 8 | MUST | ✅ found | If a key exists on both the old and updating resource, the value of the updating resource MUST be picked (even if the updated value is empty). | `src/Ядро/Классы/ОтелРесурс.os:56` |  |

#### Detecting resource information from the environment

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#detecting-resource-information-from-the-environment)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ⚠️ partial | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17` | Detectors exist as separate classes (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) but are part of the same SDK package, not separate packages. There is no pluggable API for external detector packages. |
| 10 | MUST | ✅ found | Resource detector packages MUST provide a method that returns a resource. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17` |  |
| 11 | MUST NOT | ✅ found | failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:24` |  |
| 12 | SHOULD | ⚠️ partial | failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:25` | Errors during detection are caught but logged at debug level (Лог.Отладка), not treated as actual errors per OTel Error Handling principles which would require warning/error level logging. |
| 13 | MUST | ✅ found | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18` |  |
| 14 | SHOULD | ✅ found | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate (e.g. the detector that reads the attributes from environment values will not know what Schema URL to use). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:118` |  |
| 15 | MUST | ⚠️ partial | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources. | `src/Ядро/Классы/ОтелРесурс.os:41` | Merge detects schema URL conflict and returns an empty resource (line 43), but does not report an error as required by the spec - it silently returns an undefined/empty resource. |

#### Specifying resource information via an environment variable

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#specifying-resource-information-via-an-environment-variable)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge this, as the secondary resource, with any resource information provided by the user, i.e. the user provided resource information has higher priority. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:123` |  |
| 17 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:581` |  |
| 18 | MUST | ✅ found | The `,` and `=` characters in keys and values MUST be percent encoded. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:582` |  |
| 19 | SHOULD | ❌ not_found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | - | No error handling around OTEL_RESOURCE_ATTRIBUTES parsing in СоздатьРесурс(). If РаскодироватьСтроку fails on invalid percent encoding, the exception propagates instead of discarding the entire value. |
| 20 | SHOULD | ❌ not_found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | - | No error reporting mechanism for OTEL_RESOURCE_ATTRIBUTES parsing failures. Errors are not caught and reported per OTel Error Handling principles. |

### Trace Api

#### TracerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `TracerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:31` |  |
| 2 | SHOULD | ✅ found | Thus, implementations of `TracerProvider` SHOULD allow creating an arbitrary number of `TracerProvider` instances. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:244` |  |

#### TracerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The `TracerProvider` MUST provide the following functions: * Get a `Tracer` | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |

#### Get a Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-a-tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 5 | SHOULD | ✅ found | This name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library (e.g. `io.opentelemetry.contrib.mongodb`), package, module or class name. | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:57` |  |
| 6 | MUST | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 7 | SHOULD | ⚠️ partial | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` | Для пустой строки имя устанавливается в пустую строку естественным образом, но нет явной валидации и нормализации Неопределено (аналог null) к пустой строке |
| 8 | SHOULD | ❌ not_found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | - | Нет логирования сообщения о невалидном имени при передаче пустой строки или Неопределено в ПолучитьТрассировщик |
| 9 | MUST NOT | ✅ found | Implementations MUST NOT require users to repeatedly obtain a `Tracer` again with the same identity to pick up configuration changes. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:69` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API MUST provide the following functionality to interact with a `Context` instance: | `src/Ядро/Модули/ОтелКонтекст.os:141` |  |
| 11 | SHOULD NOT | ⚠️ partial | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:44` | Контекстный ключ спана доступен публично через ОтелКонтекст.КлючСпана(), хотя существуют convenience-методы СпанИзКонтекста и КонтекстСоСпаном, абстрагирующие от ключа |
| 12 | SHOULD | ✅ found | If the language has support for implicitly propagated `Context` (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Модули/ОтелКонтекст.os:90` |  |
| 13 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### Tracer operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracer-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The `Tracer` MUST provide functions to: * Create a new `Span` (see the section on `Span`) | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 15 | SHOULD | ✅ found | The `Tracer` SHOULD provide functions to: * Report if `Tracer` is `Enabled` | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |

#### SpanContext

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spancontext)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The API MUST implement methods to create a `SpanContext`. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:252` |  |
| 17 | SHOULD | ✅ found | These methods SHOULD be the only way to create a `SpanContext`. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:252` |  |
| 18 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:1` |  |
| 19 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:1` |  |

#### Retrieving the TraceId and SpanId

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#retrieving-the-traceid-and-spanid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | The API MUST allow retrieving the `TraceId` and `SpanId` in the following forms: | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 21 | MUST | ✅ found | Hex - returns the lowercase hex encoded `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` (result MUST be a 16-hex-character lowercase string). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 22 | MUST | ✅ found | Hex - returns the lowercase hex encoded `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` (result MUST be a 16-hex-character lowercase string). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:32` |  |
| 23 | MUST | ✅ found | Binary - returns the binary representation of the `TraceId` (result MUST be a 16-byte array) or `SpanId` (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:84` |  |
| 24 | MUST | ✅ found | Binary - returns the binary representation of the `TraceId` (result MUST be a 16-byte array) or `SpanId` (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:93` |  |
| 25 | SHOULD NOT | ✅ found | The API SHOULD NOT expose details about how they are internally stored. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:4` |  |

#### IsValid

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isvalid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | MUST | ✅ found | An API called `IsValid`, that returns a boolean value, which is `true` if the SpanContext has a non-zero TraceID and a non-zero SpanID, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:70` |  |

#### IsRemote

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isremote)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 27 | MUST | ✅ found | An API called `IsRemote`, that returns a boolean value, which is `true` if the SpanContext was propagated from a remote parent, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:60` |  |
| 28 | MUST | ✅ found | When extracting a `SpanContext` through the Propagators API, `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:126` |  |
| 29 | MUST | ✅ found | When extracting a `SpanContext` through the Propagators API, `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | `src/Трассировка/Классы/ОтелСпан.os:600` |  |

#### TraceState

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracestate)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | Tracing API MUST provide at least the following operations on `TraceState`: | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:44` |  |
| 31 | MUST | ✅ found | These operations MUST follow the rules described in the W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:227` |  |
| 32 | MUST | ✅ found | All mutating operations MUST return a new `TraceState` with the modifications applied. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:92` |  |
| 33 | MUST | ✅ found | `TraceState` MUST at all times be valid according to rules specified in W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:220` |  |
| 34 | MUST | ✅ found | Every mutating operations MUST validate input parameters. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 35 | MUST NOT | ✅ found | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data and MUST follow the general error handling guidelines. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 36 | MUST | ✅ found | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data and MUST follow the general error handling guidelines. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:69` |  |

#### Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | SHOULD | ✅ found | The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable. | `src/Трассировка/Классы/ОтелСпан.os:578` |  |
| 38 | SHOULD | ✅ found | Generality SHOULD be prioritized over human-readability. | `src/Трассировка/Классы/ОтелСпан.os:578` |  |
| 39 | SHOULD | ✅ found | A `Span`'s start time SHOULD be set to the current time on span creation. | `src/Трассировка/Классы/ОтелСпан.os:609` |  |
| 40 | SHOULD | ✅ found | After the `Span` is created, it SHOULD be possible to change its name, set its `Attribute`s, add `Event`s, and set the `Status`. | `src/Трассировка/Классы/ОтелСпан.os:247` |  |
| 41 | MUST NOT | ✅ found | These MUST NOT be changed after the `Span`'s end time has been set. | `src/Трассировка/Классы/ОтелСпан.os:248` |  |
| 42 | SHOULD NOT | ⚠️ partial | To prevent misuse, implementations SHOULD NOT provide access to a `Span`'s attributes besides its `SpanContext`. | `src/Трассировка/Классы/ОтелСпан.os:134` | ОтелСпан.Атрибуты() является публичным методом (Экспорт) и предоставляет прямой доступ к атрибутам спана. В OneScript нет возможности разделить API-интерфейс (без доступа к атрибутам) и SDK-интерфейс (с доступом для экспорта), поэтому атрибуты доступны всем. |
| 43 | MUST NOT | ⚠️ partial | However, alternative implementations MUST NOT allow callers to create `Span`s directly. | `src/Трассировка/Классы/ОтелСпан.os:578` | В OneScript конструкторы всегда публичные - нет механизма сокрытия конструктора (private/package-private). Пользователь технически может вызвать Новый ОтелСпан(...) напрямую, хотя дизайн API направляет через Трассировщик. |
| 44 | MUST | ✅ found | All `Span`s MUST be created via a `Tracer`. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |

#### Span Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST NOT | ⚠️ partial | There MUST NOT be any API for creating a `Span` other than with a `Tracer`. | `src/Трассировка/Классы/ОтелСпан.os:578` | В OneScript конструкторы классов всегда публичные. Конструктор ОтелСпан доступен для вызова напрямую через Новый ОтелСпан(...), хотя единственный документированный API для создания спанов - через ОтелТрассировщик. |
| 46 | MUST NOT | ✅ found | In languages with implicit `Context` propagation, `Span` creation MUST NOT set the newly created `Span` as the active `Span` in the current `Context` by default, but this functionality MAY be offered additionally as a separate operation. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 47 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПостроительСпана.os:1` |  |
| 48 | MUST NOT | ⚠️ partial | This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`. | `src/Трассировка/Классы/ОтелПостроительСпана.os:33` | ОтелПостроительСпана.УстановитьРодителя() принимает ОтелСпан или ОтелКонтекстСпана в качестве родителя, а не полный объект Context. Спецификация требует принимать только полный Context. |
| 49 | MUST | ✅ found | The semantic parent of the Span MUST be determined according to the rules described in Determining the Parent Span from a Context. | `src/Трассировка/Классы/ОтелТрассировщик.os:57` |  |
| 50 | MUST | ✅ found | The API documentation MUST state that adding attributes at span creation is preferred to calling `SetAttribute` later, as samplers can only consider information already present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os:66` |  |
| 51 | SHOULD | ✅ found | This argument SHOULD only be set when span creation time has already passed. | `src/Трассировка/Классы/ОтелПостроительСпана.os:109` |  |
| 52 | MUST NOT | ✅ found | If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument. | `src/Трассировка/Классы/ОтелСпан.os:609` |  |
| 53 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span, and MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:108` |  |
| 54 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span, and MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:109` |  |
| 55 | MUST | ✅ found | For a Span with a parent, the `TraceId` MUST be the same as the parent. | `src/Трассировка/Классы/ОтелТрассировщик.os:142` |  |
| 56 | MUST | ✅ found | Also, the child span MUST inherit all `TraceState` values of its parent by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:233` |  |
| 57 | MUST | ✅ found | Any span that is created MUST also be ended. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |

#### Specifying links

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#specifying-links)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 58 | MUST | ✅ found | During `Span` creation, a user MUST have the ability to record links to other `Span`s. | `src/Трассировка/Классы/ОтелПостроительСпана.os:92` |  |

#### Get Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | MUST | ✅ found | The Span interface MUST provide: An API that returns the `SpanContext` for the given `Span`. | `src/Трассировка/Классы/ОтелСпан.os:80` |  |
| 60 | MUST | ✅ found | The returned value MUST be the same for the entire Span lifetime. | `src/Трассировка/Классы/ОтелСпан.os:80` |  |

#### IsRecording

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isrecording)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:234` |  |
| 62 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:234` |  |
| 63 | SHOULD NOT | ✅ found | `IsRecording` SHOULD NOT take any parameters. | `src/Трассировка/Классы/ОтелСпан.os:234` |  |
| 64 | SHOULD | ✅ found | This flag SHOULD be used to avoid expensive computations of a Span attributes or events in case when a Span is definitely not recorded. | `src/Трассировка/Классы/ОтелСпан.os:264` |  |

#### Set Attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | MUST | ✅ found | A `Span` MUST have the ability to set `Attributes` associated with it. | `src/Трассировка/Классы/ОтелСпан.os:263` |  |
| 66 | MUST | ✅ found | The Span interface MUST provide: An API to set a single `Attribute` where the attribute properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:263` |  |
| 67 | SHOULD | ✅ found | Setting an attribute with the same key as an existing attribute SHOULD overwrite the existing attribute's value. | `src/Трассировка/Классы/ОтелСпан.os:278` |  |

#### Add Events

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-events)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | MUST | ✅ found | A `Span` MUST have the ability to add events. | `src/Трассировка/Классы/ОтелСпан.os:293` |  |
| 69 | MUST | ✅ found | The Span interface MUST provide: An API to record a single `Event` where the `Event` properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:293` |  |
| 70 | SHOULD | ✅ found | Events SHOULD preserve the order in which they are recorded. | `src/Трассировка/Классы/ОтелСпан.os:297` |  |

#### Add Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | MUST | ✅ found | A `Span` MUST have the ability to add `Link`s associated with it after its creation - see Links. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |

#### Set Status

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-status)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST | ✅ found | `Description` MUST only be used with the `Error` `StatusCode` value. | `src/Трассировка/Классы/ОтелСпан.os:429` |  |
| 73 | MUST | ✅ found | The Span interface MUST provide: An API to set the `Status`. | `src/Трассировка/Классы/ОтелСпан.os:413` |  |
| 74 | SHOULD | ✅ found | This SHOULD be called `SetStatus`. | `src/Трассировка/Классы/ОтелСпан.os:413` |  |
| 75 | MUST | ✅ found | `Description` MUST be IGNORED for `StatusCode` `Ok` & `Unset` values. | `src/Трассировка/Классы/ОтелСпан.os:429` |  |
| 76 | SHOULD | ✅ found | The status code SHOULD remain unset, except for the following circumstances: | `src/Трассировка/Классы/ОтелСпан.os:614` |  |
| 77 | SHOULD | ✅ found | An attempt to set value `Unset` SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:424` |  |
| 78 | SHOULD | ✅ found | When the status is set to `Error` by Instrumentation Libraries, the `Description` SHOULD be documented and predictable. | `src/Трассировка/Классы/ОтелСпан.os:413` |  |
| 79 | SHOULD | ✅ found | For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish their own conventions, including possible values of `Description` and what they mean. | `src/Трассировка/Классы/ОтелСпан.os:413` |  |
| 80 | SHOULD NOT | ✅ found | Generally, Instrumentation Libraries SHOULD NOT set the status code to `Ok`, unless explicitly configured to do so. | `src/Трассировка/Классы/ОтелСпан.os:413` |  |
| 81 | SHOULD | ✅ found | Instrumentation Libraries SHOULD leave the status code as `Unset` unless there is an error, as described above. | `src/Трассировка/Классы/ОтелСпан.os:614` |  |
| 82 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 83 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 84 | SHOULD | ✅ found | Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they would otherwise generate. | `src/Трассировка/Классы/ОтелСпан.os:179` |  |

#### End

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#end)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 85 | SHOULD | ✅ found | Implementations SHOULD ignore all subsequent calls to `End` and any other Span methods, i.e. the Span becomes non-recording by being ended | `src/Трассировка/Классы/ОтелСпан.os:448` |  |
| 86 | MUST | ✅ found | However, all API implementations of such methods MUST internally call the `End` method and be documented to do so. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 87 | MUST NOT | ✅ found | `End` MUST NOT have any effects on child spans. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 88 | MUST NOT | ✅ found | `End` MUST NOT inactivate the `Span` in any `Context` it is active in. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 89 | MUST | ✅ found | It MUST still be possible to use an ended span as parent via a Context it is contained in. | `src/Трассировка/Классы/ОтелСпан.os:398` |  |
| 90 | MUST | ✅ found | Also, any mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:398` |  |
| 91 | MUST | ✅ found | If omitted, this MUST be treated equivalent to passing the current time. | `src/Трассировка/Классы/ОтелСпан.os:449` |  |
| 92 | MUST NOT | ✅ found | This operation itself MUST NOT perform blocking I/O on the calling thread. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 93 | SHOULD | ✅ found | Any locking used needs be minimized and SHOULD be removed entirely if possible. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |

#### Record Exception

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#record-exception)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 94 | SHOULD | ✅ found | To facilitate recording an exception languages SHOULD provide a `RecordException` method if the language uses exceptions. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 95 | MUST | ✅ found | The method MUST record an exception as an `Event` with the conventions outlined in the exceptions document. | `src/Трассировка/Классы/ОтелСпан.os:346` |  |
| 96 | SHOULD | ✅ found | The minimum required argument SHOULD be no more than only an exception object. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 97 | MUST | ✅ found | If `RecordException` is provided, the method MUST accept an optional parameter to provide any additional event attributes | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 98 | SHOULD | ✅ found | (this SHOULD be done in the same way as for the `AddEvent` method). | `src/Трассировка/Классы/ОтелСпан.os:340` |  |

#### Span lifetime

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-lifetime)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 99 | MUST | ✅ found | Start and end time as well as Event's timestamps MUST be recorded at a time of a calling of corresponding API. | `src/Трассировка/Классы/ОтелСпан.os:609` |  |

#### Wrapping a SpanContext in a Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#wrapping-a-spancontext-in-a-span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 100 | MUST | ✅ found | The API MUST provide an operation for wrapping a `SpanContext` with an object implementing the `Span` interface. | `src/Трассировка/Классы/ОтелНоопСпан.os:272` |  |
| 101 | SHOULD NOT | ⚠️ partial | If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type). | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | ОтелНоопСпан зарегистрирован как публичный класс в lib.config (строка 32). Хотя OneScript требует регистрации классов для инстанцирования, можно было бы экспортировать только фабричную функцию. |
| 102 | SHOULD | ⚠️ partial | If a new type is required to be publicly exposed, it SHOULD be named `NonRecordingSpan`. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | Класс назван ОтелНоопСпан (NoopSpan), а не ОтелНеЗаписывающийСпан (NonRecordingSpan) как рекомендует спецификация. |
| 103 | MUST | ✅ found | `GetContext` MUST return the wrapped `SpanContext`. | `src/Трассировка/Классы/ОтелНоопСпан.os:29` |  |
| 104 | MUST | ✅ found | `IsRecording` MUST return `false` to signal that events, attributes and other elements are not being recorded, i.e. they are being dropped. | `src/Трассировка/Классы/ОтелНоопСпан.os:155` |  |
| 105 | MUST | ✅ found | The remaining functionality of `Span` MUST be defined as no-op operations. | `src/Трассировка/Классы/ОтелНоопСпан.os:167` |  |
| 106 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |
| 107 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |

#### SpanKind

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 108 | SHOULD | ✅ found | In order for `SpanKind` to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose. | `src/Трассировка/Модули/ОтелВидСпана.os:1` |  |
| 109 | SHOULD NOT | ✅ found | For example, a server-side span SHOULD NOT be used to describe outgoing remote procedure call. | `src/Трассировка/Модули/ОтелВидСпана.os:1` |  |

#### Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 110 | MUST | ✅ found | A user MUST have the ability to record links to other `SpanContext`s. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 111 | MUST | ✅ found | The API MUST provide: An API to record a single `Link` where the `Link` properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 112 | SHOULD | ✅ found | Implementations SHOULD record links containing `SpanContext` with empty `TraceId` or `SpanId` (all zeros) as long as either the attribute set or `TraceState` is non-empty. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 113 | SHOULD | ✅ found | Span SHOULD preserve the order in which `Link`s are set. | `src/Трассировка/Классы/ОтелСпан.os:613` |  |
| 114 | MUST | ✅ found | The API documentation MUST state that adding links at span creation is preferred to calling `AddLink` later, for contexts that are available during span creation, because head sampling decisions can only consider information present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os:82` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 115 | MUST | ✅ found | TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:6` |  |
| 116 | MUST | ✅ found | Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:3` |  |
| 117 | MUST | ✅ found | Span - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:3` |  |
| 118 | MUST | ✅ found | Event - Events are immutable and MUST be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСобытиеСпана.os:3` |  |
| 119 | SHOULD | ⚠️ partial | Link - Links are immutable and SHOULD be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:372` | Линки хранятся как Соответствие (Map), не имеют отдельного иммутабельного класса и не документированы как потокобезопасные или иммутабельные. |

#### Behavior of the API in the absence of an installed SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#behavior-of-the-api-in-the-absence-of-an-installed-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 120 | MUST | ⚠️ partial | The API MUST return a non-recording `Span` with the `SpanContext` in the parent `Context` (whether explicitly given or implicit current). | `src/Ядро/Модули/ОтелГлобальный.os:141` | При отсутствии SDK ОтелГлобальный создает no-op SDK с ВсегдаВключен семплером и без процессоров. Трассировщик создает полный ОтелСпан (ЗаписьАктивна=true), а не non-recording спан (ЗаписьАктивна=false). Данные никуда не отправляются, но контракт IsRecording не соблюдается. |
| 121 | SHOULD | ❌ not_found | If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly without instantiating a new `Span`. | - | Трассировщик всегда создает новый экземпляр спана. Нет проверки, что родительский спан уже является non-recording, и нет логики для его прямого возврата. |
| 122 | MUST | ⚠️ partial | If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.e., having a `SpanContext` with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags). | `src/Трассировка/Классы/ОтелНоопСпан.os:277` | ОтелНоопСпан поддерживает конструктор по умолчанию с all-zero SpanContext, но в сценарии без SDK (ОтелГлобальный с пустым провайдером) трассировщик использует ВсегдаВключен семплер и создает полный ОтелСпан с случайными ID вместо empty non-recording спана. |

### Trace Sdk

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, `Sampler`, and (Development) TracerConfigurator) MUST be owned by the `TracerProvider`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:4` | SpanProcessors, SpanLimits, Sampler и TracerConfigurator принадлежат TracerProvider, но IdGenerator отсутствует как конфигурируемый компонент провайдера - генерация ID выполняется глобальным модулем ОтелУтилиты |
| 2 | MUST | ✅ found | the updated configuration MUST also apply to all already returned `Tracers` (i.e. it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvider` before or after the configuration change). | `src/Трассировка/Классы/ОтелТрассировщик.os:82` |  |
| 3 | MUST NOT | ✅ found | it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvider` before or after the configuration change | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | `Shutdown` MUST be called only once for each `TracerProvider` instance. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:108` |  |
| 5 | SHOULD | ⚠️ partial | SDKs SHOULD return a valid no-op Tracer for these calls, if possible. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:66` | После Закрыть() метод ПолучитьТрассировщик возвращает обычный ОтелТрассировщик, а не выделенный no-op трассировщик; Включен() этого трассировщика вернёт Истина (процессоры существуют, хоть и закрыты), поэтому поведение не эквивалентно no-op |
| 6 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:107` | Синхронный метод Закрыть() - Процедура без возвращаемого значения; асинхронный ЗакрытьАсинхронно() возвращает Обещание, но основной синхронный метод не предоставляет обратной связи о результате |
| 7 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:107` | Синхронный метод Закрыть() не имеет встроенного таймаута и блокирует выполнение до завершения всех процессоров; асинхронный ЗакрытьАсинхронно() поддерживает таймаут через Обещание, но основной метод - нет |
| 8 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:111` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98` | Синхронный метод СброситьБуфер() - Процедура без возвращаемого значения; асинхронный СброситьБуферАсинхронно() возвращает Обещание, но основной синхронный метод не предоставляет обратной связи |
| 10 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98` | Синхронный метод СброситьБуфер() не имеет встроенного таймаута; асинхронный СброситьБуферАсинхронно() поддерживает таймаут через Обещание, но основной метод блокирует до завершения |
| 11 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered `SpanProcessors`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:99` |  |

#### Additional Span Interfaces

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#additional-span-interfaces)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | A function receiving this as argument MUST be able to access all information that was added to the span, as listed in the API spec for Span. | `src/Трассировка/Классы/ОтелСпан.os:64` |  |
| 13 | MUST | ✅ found | A function receiving this as argument MUST be able to access the `InstrumentationScope` [since 1.10.0] and `Resource` information (implicitly) associated with the span. | `src/Трассировка/Классы/ОтелСпан.os:161` |  |
| 14 | MUST | ⚠️ partial | For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated since 1.10.0] having the same name and version values as the `InstrumentationScope`. | `src/Трассировка/Классы/ОтелСпан.os:170` | No separate InstrumentationLibrary accessor exists. Only ОбластьИнструментирования() (InstrumentationScope) is available. The name and version values are the same, but there is no dedicated backwards-compatible InstrumentationLibrary getter. |
| 15 | MUST | ✅ found | A function receiving this as argument MUST be able to reliably determine whether the Span has ended (some languages might implement this by having an end timestamp of `null`, others might have an explicit `hasEnded` boolean). | `src/Трассировка/Классы/ОтелСпан.os:197` |  |
| 16 | MUST | ✅ found | Counts for attributes, events and links dropped due to collection limits MUST be available for exporters to report as described in the exporters specification. | `src/Трассировка/Классы/ОтелСпан.os:206` |  |
| 17 | MUST | ⚠️ partial | implementations MAY choose not to expose (and store) the full parent Context of the Span but they MUST expose at least the full parent SpanContext. | `src/Трассировка/Классы/ОтелСпан.os:89` | Only parent span ID is stored and exposed via ИдРодительскогоСпана(). The full parent SpanContext (traceId, spanId, traceFlags, traceState as a SpanContext object) is not preserved - only the parent's spanId string. |
| 18 | MUST | ✅ found | It MUST be possible for functions being called with this to somehow obtain the same `Span` instance and type that the span creation API returned (or will return) to the user (for example, the `Span` could be one of the parameters passed to such a function, or a getter could be provided). | `src/Трассировка/Классы/ОтелСпан.os:455` |  |

#### Sampling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | Span Processor MUST receive only those spans which have this field set to `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:71` |  |
| 20 | SHOULD NOT | ⚠️ partial | However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37` | No filtering of RECORD_ONLY spans (IsRecording=true, Sampled=false) at the processor or exporter level. If a custom sampler returns RECORD_ONLY, the span would still reach the exporter without checking the Sampled flag. |
| 21 | MUST | ✅ found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелТрассировщик.os:79` |  |
| 22 | SHOULD NOT | ⚠️ partial | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37` | No filtering mechanism in processor or exporter to exclude spans without the Sampled flag. RECORD_ONLY spans from custom samplers would reach the exporter. |
| 23 | MUST NOT | ✅ found | the OpenTelemetry SDK MUST NOT allow this combination. | `src/Трассировка/Классы/ОтелТрассировщик.os:71` |  |

#### SDK Span creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sdk-span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | When asked to create a Span, the SDK MUST act as if doing the following in order: | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |

#### ShouldSample

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shouldsample)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | If the parent `SpanContext` contains a valid `TraceId`, they MUST always match. | `src/Трассировка/Классы/ОтелТрассировщик.os:61` |  |
| 26 | MUST NOT | ✅ found | `RECORD_ONLY` - `IsRecording` will be `true`, but the `Sampled` flag MUST NOT be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:216` |  |
| 27 | MUST | ✅ found | `RECORD_AND_SAMPLE` - `IsRecording` will be `true` and the `Sampled` flag MUST be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:218` |  |
| 28 | SHOULD | ✅ found | so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend to change it. | `src/Трассировка/Модули/ОтелСэмплер.os:157` |  |

#### GetDescription

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#getdescription)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | SHOULD NOT | ✅ found | Callers SHOULD NOT cache the returned value. | `src/Трассировка/Модули/ОтелСэмплер.os:106` |  |

#### AlwaysOn

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwayson)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | Description MUST be `AlwaysOnSampler`. | `src/Трассировка/Модули/ОтелСэмплер.os:109` |  |

#### AlwaysOff

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwaysoff)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 31 | MUST | ✅ found | Description MUST be `AlwaysOffSampler`. | `src/Трассировка/Модули/ОтелСэмплер.os:111` |  |

#### TraceID randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#traceid-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 32 | SHOULD | ⚠️ partial | For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values. | `src/Ядро/Модули/ОтелУтилиты.os:78` | TraceIDs are generated using УникальныйИдентификатор (UUID) which provides substantial randomness but does not explicitly conform to the W3C Trace Context Level 2 requirement of 56 bits of randomness in the rightmost 7 bytes. UUID v4 has deterministic version and variant bits that reduce full randomness, and there is no explicit verification of the Level 2 randomness specification. |

#### Random trace flag

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#random-trace-flag)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | SHOULD | ❌ not_found | For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements. | - | The ВычислитьФлагиТрассировки function in ОтелТрассировщик.os only sets flag value 0 or 1 (sampled bit). The W3C Random flag (bit 1, value 0x02) is never set. There is no code that sets the Random trace flag for root span contexts. |

#### Explicit randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#explicit-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | MUST NOT | ❌ not_found | SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value. | - | The sampler module (ОтелСэмплер.os) does not handle the `rv` sub-key of OpenTelemetry TraceState at all. The ДолженСэмплировать method passes the parent TraceState through to the result, but there is no logic to detect or protect the `rv` sub-key from being overwritten. No explicit randomness handling exists. |

#### Presumption of TraceID randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#presumption-of-traceid-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | SHOULD | ⚠️ partial | For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the `rv` sub-key of the OpenTelemetry TraceState. | `src/Трассировка/Модули/ОтелСэмплер.os:277` | The TraceIdRatioBased sampler (СэмплироватьПоДоле) hashes TraceID to make sampling decisions, implicitly presuming TraceID randomness. However, there is no logic to check for the `rv` sub-key in TraceState and use it as an alternative randomness source when present. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | SHOULD | ❌ not_found | If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated. | - | The SDK provides an IdGenerator extension point (ОтелУтилиты.УстановитьГенераторИд), but the custom generator has no way to signal whether generated IDs meet randomness requirements. There is no mechanism for the extension to control or influence the Random trace flag. |

#### Span Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | MUST | ✅ found | Span attributes MUST adhere to the common rules of attribute limits. | `src/Трассировка/Классы/ОтелСпан.os:266` |  |
| 38 | MUST | ✅ found | If the SDK implements the limits above it MUST provide a way to change these limits, via a configuration to the TracerProvider, by allowing users to configure individual limits like in the Java example bellow. | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:74` |  |
| 39 | SHOULD | ⚠️ partial | The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:34` | The options are named МаксСобытий (MaxEvents) and МаксЛинков (MaxLinks) rather than EventCountLimit and LinkCountLimit. The functionality is equivalent but the naming convention does not match. |
| 40 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `SpanLimits`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:1` |  |
| 41 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute, event, or link was discarded due to such a limit. | `src/Трассировка/Классы/ОтелСпан.os:468` |  |
| 42 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per discarded attribute, event, or link). | `src/Трассировка/Классы/ОтелСпан.os:469` |  |

#### Id Generators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#id-generators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST | ✅ found | The SDK MUST by default randomly generate both the `TraceId` and the `SpanId`. | `src/Ядро/Модули/ОтелУтилиты.os:78` |  |
| 44 | MUST | ✅ found | The SDK MUST provide a mechanism for customizing the way IDs are generated for both the `TraceId` and the `SpanId`. | `src/Ядро/Модули/ОтелУтилиты.os:63` |  |
| 45 | MUST | ⚠️ partial | The SDK MAY provide this functionality by allowing custom implementations of an interface like the java example below (name of the interface MAY be `IdGenerator`, name of the methods MUST be consistent with SpanContext), which provides extension points for two methods, one to generate a `SpanId` and one for `TraceId`. | `src/Ядро/Модули/ОтелУтилиты.os:63` | The extension point uses method names СгенерироватьИдТрассировки/СгенерироватьИдСпана which are consistent with SpanContext property names (ИдТрассировки/ИдСпана). However, there is no formal IdGenerator interface class - it's a duck-typing convention via module-level variable. The mechanism works but lacks a formal interface definition. |
| 46 | MUST NOT | ✅ found | Additional `IdGenerator` implementing vendor-specific protocols such as AWS X-Ray trace id generator MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | - |  |

#### Span processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | MUST | ✅ found | SDK MUST allow to end each pipeline with individual exporter. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:91` |  |
| 48 | MUST | ✅ found | SDK MUST allow users to implement and configure custom processors. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:1` |  |

#### Interface definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | MUST | ✅ found | The `SpanProcessor` interface MUST declare the following methods: * OnStart * OnEnd * Shutdown * ForceFlush | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11` |  |
| 50 | SHOULD | ✅ found | The `SpanProcessor` interface SHOULD declare the following methods: * OnEnding method. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:21` |  |

#### OnStart

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onstart)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 51 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11` |  |
| 52 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11` |  |

#### OnEnd(Span)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onendspan)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 53 | MUST | ✅ found | This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |

#### Shutdown()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `SpanProcessor` instance. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:45` |  |
| 55 | SHOULD | ⚠️ partial | After the call to `Shutdown`, subsequent calls to `OnStart`, `OnEnd`, or `ForceFlush` are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43` | ОтелПакетныйПроцессорСпанов (через базовый класс) проверяет флаг Закрыт в методе Обработать (OnEnd-путь), но СброситьБуфер (ForceFlush) не проверяет флаг. ОтелПростойПроцессорСпанов не имеет флага Закрыт и не игнорирует вызовы после Shutdown. |
| 56 | SHOULD | ❌ not_found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Метод Закрыть() определён как Процедура (void), не возвращает результат. Нет механизма обратного вызова или индикации успеха/неудачи/таймаута. |
| 57 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:83` |  |
| 58 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:45` |  |

#### ForceFlush()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `Spans` for which the `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:72` |  |
| 60 | SHOULD | ✅ found | In particular, if any `SpanProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all spans for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:157` |  |
| 61 | MUST | ✅ found | The built-in SpanProcessors MUST do so. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:72` |  |
| 62 | MUST | ✅ found | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:129` |  |
| 63 | SHOULD | ❌ not_found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Метод СброситьБуфер() определён как Процедура (void), не возвращает результат. Нет механизма обратного вызова или индикации успеха/неудачи/таймаута. |
| 64 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `SpanProcessor` exports the completed spans. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:37` |  |
| 65 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:37` |  |

#### Built-in span processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#built-in-span-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:1` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:41` |  |

#### Batching processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#batching-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:155` |  |
| 69 | SHOULD | ✅ found | The processor SHOULD export a batch when any of the following happens AND the previous export call has returned: | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:54` |  |

#### Span Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 70 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:6` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | MUST | ✅ found | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:13` |  |

#### `Export(batch)`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST NOT | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 73 | MUST | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:149` |  |
| 74 | SHOULD NOT | ✅ found | The default SDK's Span Processors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the spans are being sent to. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37` |  |

#### `ForceFlush()`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Spans` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:44` |  |
| 76 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:19` | ForceFlush (СброситьБуфер) is defined as Процедура (void return). Failure can be signaled via exception, but there is no way to distinguish success from timeout - the caller only knows the call completed or threw. |
| 77 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed spans. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:44` |  |
| 78 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:44` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 79 | MUST | ✅ found | Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:17` |  |
| 80 | MUST | ✅ found | Sampler - `ShouldSample` and `GetDescription` MUST be safe to be called concurrently. | `src/Трассировка/Модули/ОтелСэмплер.os:4` |  |
| 81 | MUST | ✅ found | Span processor - all methods MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:7` |  |
| 82 | MUST | ✅ found | Span Exporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:12` |  |

### Logs Api

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `LoggerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:31` |  |

#### LoggerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `LoggerProvider` MUST provide the following functions: * Get a `Logger` | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |

#### Get a Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#get-a-logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following instrumentation scope parameters: | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 4 | MUST | ✅ found | This API MUST be structured to accept a variable number of attributes, including none. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:57` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The `Logger` MUST provide a function to: * Emit a `LogRecord` | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 6 | SHOULD | ✅ found | The `Logger` SHOULD provide functions to: * Report if `Logger` is `Enabled` | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Логирование/Классы/ОтелЗаписьЛога.os:44` |  |
| 8 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 9 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:82` |  |
| 10 | SHOULD | ➖ n_a | When only explicit Context is supported, this parameter SHOULD be required. | - | The implementation supports implicit Context via ОтелКонтекст.Текущий(), so the condition 'When only explicit Context is supported' is not met. The alternative branch (implicit Context supported, parameter optional) is correctly implemented. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when generating a `LogRecord`, a `Logger` SHOULD provide this `Enabled` API. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 12 | SHOULD | ✅ found | The API SHOULD accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 13 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 14 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:152` |  |
| 15 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 16 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response. | `src/Логирование/Классы/ОтелЛоггер.os:28` | Метод Включен() задокументирован, но документация не содержит указания о необходимости вызывать его каждый раз перед emit для получения актуального ответа. Комментарий описывает только назначение метода, но не динамическую природу возвращаемого значения. |

#### Optional and required parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#optional-and-required-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 18 | MUST NOT | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 19 | MUST | ✅ found | For each required parameter, the API MUST be structured to obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | LoggerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:7` |  |
| 21 | MUST | ✅ found | Logger - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелЛоггер.os:230` |  |

### Logs Sdk

#### Logs SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logs-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:1` |  |

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A `LoggerProvider` MUST provide a way to allow a Resource to be specified. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:22` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the `LogRecord`s produced by any `Logger` from the `LoggerProvider`. | `src/Логирование/Классы/ОтелЛоггер.os:78` |  |

#### LoggerProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `LoggerProviders`s. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:205` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration (i.e. LogRecordProcessors and (Development) LoggerConfigurator) MUST be owned by the `LoggerProvider`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:12` |  |
| 6 | MUST | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained from the `LoggerProvider` before or after the configuration change). | `src/Логирование/Классы/ОтелЛоггер.os:107` |  |
| 7 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained from the `LoggerProvider` before or after the configuration change). | `src/Логирование/Классы/ОтелЛоггер.os:107` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | `Shutdown` MUST be called only once for each `LoggerProvider` instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117` |  |
| 9 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op `Logger` for these calls, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:60` |  |
| 10 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:143` | Синхронный Закрыть() не возвращает статус (void); асинхронный ЗакрытьАсинхронно() возвращает Обещание, но без явного статуса успеха/ошибки/таймаута |
| 11 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:116` | Метод Закрыть() провайдера не принимает параметр таймаута; ОтелКомпозитныйПроцессорЛогов.Закрыть поддерживает ТаймаутМс, но провайдер его не пробрасывает |
| 12 | MUST | ✅ found | `Shutdown` MUST be implemented by invoking `Shutdown` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:120` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:131` | Синхронный СброситьБуфер() не возвращает статус (void); асинхронный СброситьБуферАсинхронно() возвращает Обещание, но без явного статуса успеха/ошибки/таймаута |
| 14 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | СброситьБуфер() не возвращает явный ERROR-статус; исключения процессоров пробрасываются, но не как возвращаемый статус |
| 15 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | СброситьБуфер() не возвращает явный NO ERROR статус (метод void) |
| 16 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | СброситьБуфер() провайдера не принимает таймаут; ОтелКомпозитныйПроцессорЛогов.СброситьБуфер поддерживает ТаймаутМс, но провайдер его не использует |
| 17 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:108` |  |

#### ReadableLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readablelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | A function receiving this as an argument MUST be able to access all the information added to the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:44` |  |
| 19 | MUST | ✅ found | It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) associated with the `LogRecord`. | `src/Логирование/Классы/ОтелЗаписьЛога.os:132` |  |
| 20 | MUST | ✅ found | The trace context fields MUST be populated from the resolved `Context` (either the explicitly passed `Context` or the current `Context`) when emitted. | `src/Логирование/Классы/ОтелЛоггер.os:81` |  |
| 21 | MUST | ✅ found | Counts for attributes due to collection limits MUST be available for exporters to report as described in the transformation to non-OTLP formats specification. | `src/Логирование/Классы/ОтелЗаписьЛога.os:150` |  |

#### ReadWriteLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readwritelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 22 | MUST | ✅ found | A function receiving this as an argument MUST additionally be able to modify the following information added to the LogRecord: * `Timestamp` * `ObservedTimestamp` * `SeverityText` * `SeverityNumber` * `Body` * `Attributes` (addition, modification, removal) * `TraceId` * `SpanId` * `TraceFlags` * `EventName` | `src/Логирование/Классы/ОтелЗаписьЛога.os:179` |  |

#### LogRecord Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecord-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | MUST | ✅ found | `LogRecord` attributes MUST adhere to the common rules of attribute limits. | `src/Логирование/Классы/ОтелЗаписьЛога.os:235` |  |
| 24 | MUST | ✅ found | If the SDK implements attribute limits it MUST provide a way to change these limits, via a configuration to the `LoggerProvider`, by allowing users to configure individual limits like in the Java example below. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:50` |  |
| 25 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `LogRecordLimits`. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:73` |  |
| 26 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute was discarded due to such a limit. | `src/Логирование/Классы/ОтелЗаписьЛога.os:384` |  |
| 27 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per `LogRecord` (i.e., not per discarded attribute). | `src/Логирование/Классы/ОтелЗаписьЛога.os:385` |  |

#### LogRecordProcessor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | The SDK MUST allow each pipeline to end with an individual exporter. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:81` |  |
| 29 | MUST | ✅ found | The SDK MUST allow users to implement and configure custom processors and decorate built-in processors for advanced scenarios such as enriching with attributes. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:1` |  |

#### OnEmit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#onemit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | SHOULD NOT | ⚠️ partial | This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD NOT block or throw exceptions. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:18-30` | Simple processor (ОтелПростойПроцессорЛогов.ПриПоявлении) blocks synchronously during export with a lock and re-throws exceptions via ВызватьИсключение. Batch processor is non-blocking (adds to buffer). Composite processor swallows exceptions but simple does not. |
| 31 | MUST | ✅ found | For a `LogRecordProcessor` registered directly on SDK `LoggerProvider`, the `logRecord` mutations MUST be visible in next registered processors. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17-24` |  |
| 32 | SHOULD | ❌ not_found | To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecord` be used for any concurrent processing, such as in a batching processor. | - | No documentation or code recommending cloning of logRecord for concurrent processing. The batch processor (ОтелБазовыйПакетныйПроцессор.Обработать) adds the element directly to the buffer without cloning or any advisory comment. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | MUST NOT | ✅ found | Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller. Parameters are immutable or passed by value. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:14-21` |  |

#### ShutDown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117` |  |
| 35 | SHOULD | ✅ found | After the call to `Shutdown`, subsequent calls to `OnEmit` are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Логирование/Классы/ОтелЛоггер.os:106` |  |
| 36 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:116-123` | Synchronous Закрыть() is a void procedure (Процедура) that does not return success/failure/timeout status. The async variant ЗакрытьАсинхронно() returns an Обещание (Promise) but does not distinguish between success, failure, and timeout. |
| 37 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80-87` |  |
| 38 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 39 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `LogRecord`s for which the `LogRecordProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71-73` |  |
| 40 | SHOULD | ✅ found | In particular, if any `LogRecordProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all `LogRecord`s for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:148-166` |  |
| 41 | MUST | ✅ found | The built-in LogRecordProcessors MUST do so. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71-73` |  |
| 42 | MUST | ✅ found | If a timeout is specified (see below), the `LogRecordProcessor` MUST prioritize honoring the timeout over finishing all calls. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:129-131` |  |
| 43 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107-111` | Synchronous СброситьБуфер() is a void procedure (Процедура) that does not return success/failure/timeout status. The async variant СброситьБуферАсинхронно() returns an Обещание (Promise) but does not distinguish between success, failure, and timeout. |
| 44 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `LogRecordProcessor` exports the emitted `LogRecord`s. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` |  |
| 45 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71-73` |  |

#### Built-in processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#built-in-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1` |  |
| 47 | SHOULD | ✅ found | Other common processing scenarios SHOULD be first considered for implementation out-of-process in OpenTelemetry Collector. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 48 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:22-29` |  |

#### Batching processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#batching-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:155-164` |  |

#### LogRecordExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 50 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:5-6` |  |

#### LogRecordExporter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 51 | MUST | ✅ found | A `LogRecordExporter` MUST support the following functions: | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:29` |  |

#### Export

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#export)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 52 | MUST NOT | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 53 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:149` |  |
| 54 | SHOULD NOT | ✅ found | The default SDK's `LogRecordProcessors` SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the logs are being sent to. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:18` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD | ✅ found | This is a hint to ensure that the export of any `ReadableLogRecords` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:45` |  |
| 56 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:45` | СброситьБуфер() определена как Процедура (void), не возвращает результат. Вызывающий не может узнать, был ли ForceFlush успешен, завершился с ошибкой или по таймауту. Интерфейс ИнтерфейсЭкспортерЛогов также определяет СброситьБуфер() как void. |
| 57 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the `ReadlableLogRecords`. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:45` |  |
| 58 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:45` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each `LogRecordExporter` instance. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:51` |  |
| 60 | SHOULD | ✅ found | After the call to `Shutdown` subsequent calls to `Export` are not allowed and SHOULD return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:30` |  |
| 61 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:51` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 62 | MUST | ✅ found | LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:224` |  |
| 63 | MUST | ✅ found | Logger - all methods MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 64 | MUST | ✅ found | LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:77` |  |

### Metrics Api

#### MeterProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `MeterProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:99` |  |

#### MeterProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `MeterProvider` MUST provide the following functions: Get a `Meter` | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |

#### Get a Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#get-a-meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 4 | MUST NOT | ✅ found | this API needs to be structured to accept a `version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:54` |  |
| 5 | MUST | ✅ found | Therefore, this API needs to be structured to accept a `schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:56` |  |
| 6 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:55` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ found | `Meter` SHOULD NOT be responsible for the configuration. This should be the responsibility of the `MeterProvider` instead. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:206` |  |

#### Meter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The `Meter` MUST provide functions to create new Instruments: | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Instrument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ✅ found | Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying. | `src/Метрики/Классы/ОтелМетр.os:562` |  |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | SHOULD | ✅ found | The API SHOULD treat it as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:66` |  |
| 11 | MUST | ✅ found | It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII string. | `src/Метрики/Классы/ОтелМетр.os:568` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST treat it as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:16` |  |
| 13 | MUST | ✅ found | It MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or `utf8mb3`). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:16` |  |
| 14 | MUST | ✅ found | It MUST support at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:16` |  |

#### Synchronous and Asynchronous instruments

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#synchronous-and-asynchronous-instruments)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The API to construct synchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 16 | SHOULD | ✅ found | The `name` needs to be provided by a user. If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 17 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 18 | SHOULD | ❌ not_found | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | - | API documentation for sync instrument creation methods does not explicitly mention that the name must conform to instrument name syntax rules. |
| 19 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`; that is left to implementations of the API, like the SDK. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 20 | MUST NOT | ✅ found | Users can provide a `unit`, but it is up to their discretion. Therefore, this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 21 | MUST | ✅ found | Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:18` |  |
| 22 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 23 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 24 | MUST | ✅ found | Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:16` |  |
| 25 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 26 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 27 | MUST | ✅ found | The API to construct asynchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:232` |  |
| 28 | SHOULD | ✅ found | The `name` needs to be provided by a user. If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:232` |  |
| 29 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:232` |  |
| 30 | SHOULD | ❌ not_found | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | - | API documentation for async instrument creation methods does not explicitly mention that the name must conform to instrument name syntax rules. |
| 31 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`, that is left to implementations of the API. | `src/Метрики/Классы/ОтелМетр.os:232` |  |
| 32 | MUST NOT | ✅ found | Users can provide a `unit`, but it is up to their discretion. Therefore, this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:232` |  |
| 33 | MUST | ✅ found | Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:10` |  |
| 34 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:232` |  |
| 35 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:232` |  |
| 36 | MUST | ✅ found | Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:8` |  |
| 37 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:232` |  |
| 38 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:232` |  |
| 39 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of `callback` functions, including none. | `src/Метрики/Классы/ОтелМетр.os:232` |  |
| 40 | MUST | ✅ found | The API MUST support creation of asynchronous instruments by passing zero or more `callback` functions to be permanently registered to the newly created instrument. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:155` |  |
| 41 | SHOULD | ✅ found | The API SHOULD support registration of `callback` functions associated with asynchronous instruments after they are created. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:67` |  |
| 42 | MUST | ✅ found | Where the API supports registration of `callback` functions after asynchronous instrumentation creation, the user MUST be able to undo registration of the specific callback after its registration by some means. | `src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os:16` |  |
| 43 | MUST | ✅ found | Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:130` |  |
| 44 | MUST | ✅ found | Callback functions MUST be documented as follows for the end user: | `src/Метрики/Классы/ОтелНаблюдениеМетрики.os:46` |  |
| 45 | SHOULD | ⚠️ partial | Callback functions SHOULD be reentrant safe. | - | Callback functions are invoked from ОтелБазовыйНаблюдаемыйИнструмент but the documentation does not explicitly state that callbacks should be reentrant safe. |
| 46 | SHOULD NOT | ⚠️ partial | Callback functions SHOULD NOT take an indefinite amount of time. | - | There is no explicit documentation warning users that callback functions should not take an indefinite amount of time. |
| 47 | SHOULD NOT | ⚠️ partial | Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same `attributes`) across all registered callbacks. | - | There is no explicit documentation warning or enforcement that callbacks should not make duplicate observations with the same attributes. |
| 48 | MUST | ✅ found | Callbacks registered at the time of instrument creation MUST apply to the single instruments which is under construction. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:155` |  |
| 49 | MUST | ✅ found | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the instrument associated with each observed `Measurement` value. | `src/Метрики/Классы/ОтелМетр.os:396` |  |
| 50 | MUST | ✅ found | Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of asynchronous instruments from the same `Meter` instance. | `src/Метрики/Классы/ОтелМетр.os:389` |  |
| 51 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147` |  |
| 52 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147` |  |
| 53 | SHOULD | ✅ found | The API SHOULD provide some way to pass `state` to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:155` |  |

#### General operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | SHOULD | ✅ found | All synchronous instruments SHOULD provide functions to: Report if instrument is `Enabled` | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when recording measurements, synchronous instruments SHOULD provide this `Enabled` API. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 56 | MUST | ✅ found | There are currently no required parameters for this API. Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 57 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:202` |  |
| 58 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:192` | The Enabled() method exists and documentation comments mention its purpose, but it does not explicitly document that authors need to call it each time before recording. |

#### Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | MUST NOT | ✅ found | There MUST NOT be any API for creating a `Counter` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:51` |  |

#### Counter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 61 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 62 | SHOULD | ✅ found | The increment value needs to be provided by a user. If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 63 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 64 | SHOULD | ⚠️ partial | The increment value is expected to be non-negative. This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелСчетчик.os:14` | The method comment mentions 'положительное значение для добавления' but does not explicitly phrase it as 'non-negative' in the API documentation intended for end users. |
| 65 | SHOULD NOT | ⚠️ partial | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелСчетчик.os:22` | Counter.Добавить() validates the value and silently drops negative values (Если Значение < 0 Тогда Возврат). The spec says the API SHOULD NOT validate, but the implementation does validate by rejecting negative values. |
| 66 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 67 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |

#### Asynchronous Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Counter other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 69 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` |  |
| 70 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` |  |
| 71 | SHOULD | ✅ found | The API SHOULD provide some way to pass state to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:1` |  |

#### Histogram creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#histogram-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Histogram other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:80` |  |

#### Histogram operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#histogram-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example null, undefined). | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 74 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 75 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 76 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелГистограмма.os:13` |  |
| 77 | SHOULD | ❌ not_found | This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | - | Документация метода Записать в ОтелГистограмма.os не упоминает, что значение должно быть неотрицательным. Комментарий содержит только 'Значение - Число - измеренное значение' без указания на ожидание неотрицательности. |
| 78 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 79 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |

#### Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 80 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Gauge other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:194` |  |

#### Gauge operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 81 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example null, undefined). | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 82 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 83 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 84 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелДатчик.os:13` |  |
| 85 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 86 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |

#### Asynchronous Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 87 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Gauge other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:308` |  |

#### UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 88 | MUST NOT | ✅ found | There MUST NOT be any API for creating an UpDownCounter other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:162` |  |

#### UpDownCounter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 90 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 91 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 92 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:13` |  |
| 93 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |

#### Asynchronous UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 94 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:268` |  |

#### Multiple-instrument callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#multiple-instrument-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 95 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: | `src/Метрики/Классы/ОтелМетр.os:428` |  |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | SHOULD | ✅ found | All the metrics components SHOULD allow new APIs to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 97 | SHOULD | ✅ found | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | MUST | ⚠️ partial | MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:241` | Thread-safety IS implemented via СинхронизированнаяКарта for the meters cache, but the class/method documentation does not explicitly state that the implementation is safe for concurrent use. |
| 99 | MUST | ⚠️ partial | Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелМетр.os:493` | Thread-safety IS implemented via СинхронизированнаяКарта for instruments cache and descriptors, but the class/method documentation does not explicitly state that the implementation is safe for concurrent use. |
| 100 | MUST | ⚠️ partial | Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:261` | Thread-safety IS implemented via СинхронизированнаяКарта for accumulators and attributes, but the class/method documentation does not explicitly state that the implementation is safe for concurrent use. |

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
| 2 | MUST | ✅ found | A `MeterProvider` MUST provide a way to allow a Resource to be specified. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:231` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the metrics produced by any `Meter` from the `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:69` |  |

#### MeterProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `MeterProvider`s. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:231` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration (i.e. MetricExporters, MetricReaders, Views, and (Development) MeterConfigurator) MUST be owned by the `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:6` |  |
| 6 | MUST | ✅ found | the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the `MeterProvider` before or after the configuration change). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:71` |  |
| 7 | MUST NOT | ✅ found | the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the `MeterProvider` before or after the configuration change). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:71` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MeterProvider` instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` |  |
| 9 | SHOULD | ✅ found | After the call to `Shutdown`, subsequent attempts to get a `Meter` are not allowed. SDKs SHOULD return a valid no-op Meter for these calls, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:57` |  |
| 10 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` | Synchronous Закрыть() is a void procedure with no return value indicating success, failure, or timeout. The async ЗакрытьАсинхронно() returns an Обещание which can signal failure, but the primary synchronous API has no status reporting. |
| 11 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` | The MeterProvider's Закрыть() has no explicit timeout. The underlying reader's Закрыть has a timeout for waiting on the background export task (ИнтервалЭкспортаМс * МножительТаймаутаОжидания), but there is no overall timeout for the provider-level shutdown. |
| 12 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered MetricReader and MetricExporter instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:136` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered MetricReader instances that implement `ForceFlush`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:116` |  |
| 14 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` | Synchronous СброситьБуфер() is a void procedure with no return value. The async СброситьБуферАсинхронно() returns an Обещание, but the primary synchronous API provides no status indication. |
| 15 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` | СброситьБуфер() is a void procedure that does not return any error or success status. Errors in underlying readers are silently handled. |
| 16 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` | The MeterProvider's СброситьБуфер() has no explicit timeout mechanism. The async variant СброситьБуферАсинхронно() returns an Обещание that supports timeouts, but the synchronous API has no timeout. |

#### View

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | The SDK MUST provide functionality for a user to create Views for a `MeterProvider`. | `src/Метрики/Классы/ОтелПредставление.os:1` |  |
| 18 | MUST | ✅ found | This functionality MUST accept as inputs the Instrument selection criteria and the resulting stream configuration. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:56` |  |
| 19 | MUST | ✅ found | The SDK MUST provide the means to register Views with a `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:176` |  |

#### Instrument selection criteria

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-selection-criteria)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | Criteria SHOULD be treated as additive. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:34` |  |
| 21 | MUST | ✅ found | The SDK MUST accept the following criteria: | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 22 | MUST | ✅ found | If the SDK does not support wildcards in general, it MUST still recognize the special single asterisk (`*`) character as matching all Instruments. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37` |  |
| 23 | MUST NOT | ✅ found | Users can provide a `name`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 24 | MUST NOT | ✅ found | Users can provide a `type`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `type`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 25 | MUST NOT | ✅ found | Users can provide a `unit`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:161` |  |
| 26 | MUST NOT | ✅ found | Users can provide a `meter_name`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:160` |  |
| 27 | MUST NOT | ✅ found | Users can provide a `meter_version`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:161` |  |
| 28 | MUST NOT | ✅ found | Users can provide a `meter_schema_url`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:161` |  |
| 29 | MUST NOT | ✅ found | Users can provide these additional criteria the SDK accepts, but it is up to their discretion. Therefore, the instrument selection criteria can be structured to accept the criteria, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |

#### Stream configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#stream-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | The SDK MUST accept the following stream configuration parameters: | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 31 | SHOULD | ✅ found | `name`: The metric stream name that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:29` |  |
| 32 | SHOULD | ✅ found | In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector that selects at most one instrument. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 33 | MUST NOT | ✅ found | Users can provide a `name`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:157` |  |
| 34 | MUST | ✅ found | If the user does not provide a `name` value, name from the Instrument the View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:230` |  |
| 35 | SHOULD | ✅ found | `description`: The metric stream description that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:38` |  |
| 36 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:158` |  |
| 37 | MUST | ✅ found | If the user does not provide a `description` value, the description from the Instrument a View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:233` |  |
| 38 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:291` |  |
| 39 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:291` |  |
| 40 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept `attribute_keys`, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелПредставление.os:159` |  |
| 41 | SHOULD | ✅ found | If the user does not provide any value, the SDK SHOULD use the `Attributes` advisory parameter configured on the instrument instead. | `src/Метрики/Классы/ОтелМетр.os:527` |  |
| 42 | MUST | ✅ found | If the `Attributes` advisory parameter is absent, all attributes MUST be kept. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:84` |  |
| 43 | SHOULD | ⚠️ partial | Additionally, implementations SHOULD support configuring an exclude-list of attribute keys. | `src/Метрики/Классы/ОтелПредставление.os:56` | ОтелПредставление has ИсключенныеКлючиАтрибутов field defined in the constructor and getter, but the exclude-list is never applied during measurement filtering in ОтелБазовыйСинхронныйИнструмент - only the allow-list (РазрешенныеКлючиАтрибутов) is used. |
| 44 | MUST | ⚠️ partial | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелПредставление.os:56` | ОтелПредставление defines ИсключенныеКлючиАтрибутов but ОтелМетр.ПрименитьПредставлениеКИнструменту and ОтелБазовыйСинхронныйИнструмент never apply the exclude-list. The field exists but exclusion is not implemented. |
| 45 | MUST | ⚠️ partial | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелПредставление.os:56` | Same as above - the exclude-list is defined in ОтелПредставление but never applied, so the 'keep all other attributes' behavior in exclude-list context is not implemented. |
| 46 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept an `aggregation`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:164` |  |
| 47 | MUST | ⚠️ partial | If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance. | `src/Метрики/Классы/ОтелМетр.os:48` | Default aggregation per instrument type exists (Counter→Sum, Histogram→ExplicitBucketHistogram, Gauge→LastValue), but it is hardcoded in ОтелМетр, not configurable per MetricReader instance. MetricReader has no aggregation property. |
| 48 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept an `exemplar_reservoir`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:164` |  |
| 49 | MUST | ✅ found | If the user does not provide an `exemplar_reservoir` value, the `MeterProvider` MUST apply a default exemplar reservoir. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |
| 50 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept an `aggregation_cardinality_limit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:164` |  |
| 51 | MUST | ⚠️ partial | If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST apply the default aggregation cardinality limit the `MetricReader` is configured with. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` | Default cardinality limit of 2000 is hardcoded in ОтелБазовыйСинхронныйИнструмент and ОтелМетр. The spec requires the default to come from MetricReader configuration, but ОтелПериодическийЧитательМетрик has no cardinality limit property. |

#### Measurement processing

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#measurement-processing)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 52 | SHOULD | ⚠️ partial | The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument: | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:192` | Processing logic is partially implemented: default aggregation is applied when no Views are registered, and the first matching View is applied. However, the spec requires each matching View to be applied independently (producing separate streams), while the code applies only the first matching View and returns. |
| 53 | MUST | ✅ found | Instrument advisory parameters, if any, MUST be honored. | `src/Метрики/Классы/ОтелМетр.os:527` |  |
| 54 | SHOULD | ❌ not_found | If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning. | - | No conflict detection or warning is implemented when Views produce conflicting metric identities. Views are applied without checking for conflicts. |
| 55 | SHOULD | ❌ not_found | If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asynchronous instrument to use the Explicit bucket histogram aggregation) the implementation SHOULD emit a warning and proceed as if the View did not | - | No validation of semantic compatibility between View aggregation and instrument type is implemented. No warning is emitted for incompatible View-instrument combinations. |
| 56 | MUST | ✅ found | If both a View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:524` |  |
| 57 | SHOULD | ✅ found | If the Instrument could not match with any of the registered `View`(s), the SDK SHOULD enable the instrument using the default aggregation and temporality. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 58 | MUST | ✅ found | The SDK MUST provide the following `Aggregation` to support the Metric Points in the Metrics Data Model. | `src/Метрики/Модули/ОтелАгрегация.os:1` |  |
| 59 | SHOULD | ✅ found | The SDK SHOULD provide the following `Aggregation`: | `src/Метрики/Модули/ОтелАгрегация.os:76` |  |

#### Histogram Aggregations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#histogram-aggregations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | SHOULD NOT | ❌ not_found | This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpDownCounter` or `ObservableGauge`). | - | The histogram aggregator always collects the sum field (ОтелАгрегаторГистограммы.Записать line 51). There is no check for the instrument type to skip sum collection for instruments that record negative measurements. |
| 61 | SHOULD | ⚠️ partial | SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different (e.g. for backward compatibility reasons in a stable SDK release). | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:118` | Default boundaries are used when none provided, but the values [0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 10000] are missing 7500 compared to the spec's default [0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000]. |
| 62 | SHOULD NOT | ✅ found | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`, `min`, and `max` fields, because these values do not map into a valid bucket. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:63` |  |
| 63 | MUST | ⚠️ partial | The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic scale parameter will not exceed. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:302` | MaxScale parameter (НачальнаяШкала, default 20) is maintained as the maximum scale. However, there is no explicit minimum scale parameter - the scale can decrease without bound through ПонизитьШкалуНа1 calls. |
| 64 | SHOULD | ✅ found | When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:302` |  |
| 65 | SHOULD | ✅ found | Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possible, within the constraint of maximum size (max number of buckets). | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:157` |  |

#### Observations inside asynchronous callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#observations-inside-asynchronous-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | MUST | ⚠️ partial | Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that observations made or produced by executing callbacks only apply to the intended `MetricReader` during collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:157` | Callbacks are invoked during collection via ВызватьМультиОбратныеВызовы(), but observations are not scoped to a specific MetricReader. With multiple readers, callbacks are invoked independently per reader, but there is no isolation mechanism - the ВнешниеНаблюдения array is shared and cleared after each collection without reader-specific scoping. |
| 67 | SHOULD | ⚠️ partial | The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:58` | Observable instruments only produce data through callbacks (ВызватьCallbackИСобрать), but ДобавитьВнешниеНаблюдения is a public method that can be called from outside registered callbacks without enforcement. |
| 68 | SHOULD | ❌ not_found | The implementation SHOULD use a timeout to prevent indefinite callback execution. | - | Callbacks are invoked synchronously in ВызватьCallbackИСобрать with a try-catch for error handling but no timeout mechanism. An infinite callback would block the collection thread indefinitely. |
| 69 | MUST | ✅ found | The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:157` |  |
| 70 | SHOULD NOT | ✅ found | The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160` |  |

#### Cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | SHOULD | ✅ found | SDKs SHOULD support being configured with a cardinality limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:163` |  |
| 72 | SHOULD | ✅ found | Cardinality limit enforcement SHOULD occur after attribute filtering, if any. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:84` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | SHOULD | ⚠️ partial | A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardinality_limit` value defined for the stream, that value SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:92` | ОтелПредставление has ЛимитМощностиАгрегации field, but ПрименитьПредставлениеКИнструменту in ОтелМетр.os does not apply the View's cardinality limit to the instrument's ЛимитМощности |
| 74 | SHOULD | ❌ not_found | If there is no matching view, but the `MetricReader` defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | - | ОтелПериодическийЧитательМетрик does not define a per-instrument-type default cardinality limit; the cardinality limit is always set from the Meter's default, not from the MetricReader |
| 75 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` |  |

#### Overflow attribute

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#overflow-attribute)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 76 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:325` |  |
| 77 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:92` |  |

#### Synchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#synchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | MUST | ✅ found | Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141` |  |
| 79 | MUST | ✅ found | Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in exactly one Aggregator, which is either an Aggregator associated with the correct attribute set or an aggregator associated with the overflow attribute set. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:78` |  |
| 80 | MUST NOT | ✅ found | Measurements MUST NOT be double-counted or dropped during an overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:105` |  |

#### Asynchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#asynchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 81 | SHOULD | ❌ not_found | Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality. | - | ОтелБазовыйНаблюдаемыйИнструмент has no cardinality limiting; all callback observations are collected without any limit or preference for first-observed attributes |

#### Duplicate instrument registration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#duplicate-instrument-registration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 82 | MUST | ✅ found | This means that the Meter MUST return a functional instrument that can be expected to export data even if this will cause semantic error in the data model. | `src/Метрики/Классы/ОтелМетр.os:52` |  |
| 83 | SHOULD | ✅ found | Additionally, users need to be informed about this error. Therefore, when a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted. | `src/Метрики/Классы/ОтелМетр.os:573` |  |
| 84 | SHOULD | ⚠️ partial | The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible. | `src/Метрики/Классы/ОтелМетр.os:573` | Warning message reports the conflicting parameters but does not include specific instructions on how to resolve the conflict (e.g., suggesting use of a View) |
| 85 | SHOULD | ❌ not_found | If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning. | - | ПроверитьКонфликтДескриптора does not check if a View resolves the description conflict; it always emits a warning when descriptions differ regardless of View configuration |
| 86 | SHOULD | ❌ not_found | If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning. | - | Warning message does not mention Views or include any View-based resolution recipe |
| 87 | SHOULD | ⚠️ partial | Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument registration. | `src/Метрики/Классы/ОтелМетр.os:573` | A warning is emitted, but the code returns the existing instrument instance rather than reporting both Metric objects; data from the duplicate registration merges into the original instrument |
| 88 | MUST | ✅ found | the SDK MUST aggregate data from identical Instruments together in its export pipeline. | `src/Метрики/Классы/ОтелМетр.os:52` |  |

#### Name conflict

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#name-conflict)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | MUST | ✅ found | When this happens, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above. | `src/Метрики/Классы/ОтелМетр.os:49` |  |

#### Instrument name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | SHOULD | ❌ not_found | When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax | - | Методы создания инструментов (СоздатьСчетчик, СоздатьГистограмму и др.) в ОтелМетр не содержат валидации имени инструмента по синтаксическому шаблону спецификации. Имя нормализуется в нижний регистр (НРег), но не проверяется на соответствие допустимым символам. |
| 91 | SHOULD | ❌ not_found | If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name. | - | Нет валидации имени инструмента, поэтому нет и генерации ошибки при невалидном имени. |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 92 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 93 | MUST | ⚠️ partial | If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit string. | `src/Метрики/Классы/ОтелМетр.os:48` | Параметр ЕдиницаИзмерения имеет значение по умолчанию "" (пустая строка), что корректно обрабатывает случай "не предоставлен". Однако если явно передать Неопределено (null), значение не нормализуется в пустую строку - оно передаётся в конструктор ОтелБазовыйСинхронныйИнструмент как есть. |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 94 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument description. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 95 | MUST | ⚠️ partial | If a description is not provided or the description is null, the Meter MUST treat it the same as an empty description string. | `src/Метрики/Классы/ОтелМетр.os:48` | Параметр Описание имеет значение по умолчанию "" (пустая строка), что корректно обрабатывает случай "не предоставлен". Однако если явно передать Неопределено (null), значение не нормализуется в пустую строку - оно передаётся в конструктор ОтелБазовыйСинхронныйИнструмент как есть. |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | SHOULD | ✅ found | When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:642` |  |
| 97 | SHOULD | ⚠️ partial | If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided. | `src/Метрики/Классы/ОтелМетр.os:648` | Метод ПроверитьСовет выводит предупреждение через Лог.Предупреждение при невалидных типах advisory-параметров, но не обнуляет невалидный параметр - дальнейший код может попытаться использовать невалидное значение вместо того, чтобы действовать так, как будто параметр не был предоставлен. |
| 98 | MUST | ✅ found | If multiple identical Instruments are created with different advisory parameters, the Meter MUST return an instrument using the first-seen advisory parameters and log an appropriate error as described in duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:562` |  |
| 99 | MUST | ✅ found | If both a View and advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:539` |  |

#### Instrument advisory parameter: `ExplicitBucketBoundaries`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameter-explicitbucketboundaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 100 | MUST | ✅ found | If no View matches, or if a matching View selects the default aggregation, the `ExplicitBucketBoundaries` advisory parameter MUST be used. | `src/Метрики/Классы/ОтелМетр.os:545` |  |

#### Exemplar

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 101 | MUST | ✅ found | A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements via the `ExemplarFilter` and `ExemplarReservoir` hooks. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:1` |  |
| 102 | SHOULD | ✅ found | `Exemplar` sampling SHOULD be turned on by default. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:245` |  |
| 103 | MUST NOT | ✅ found | If `Exemplar` sampling is off, the SDK MUST NOT have overhead related to exemplar sampling. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:335` |  |
| 104 | MUST | ✅ found | A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation. | `src/Метрики/Классы/ОтелМетр.os:99` |  |
| 105 | SHOULD | ✅ found | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: `ExemplarFilter`: filter which measurements can become exemplars. `ExemplarReservoir`: storage and sampling of exemplars. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:73` |  |

#### ExemplarFilter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarfilter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 106 | MUST | ✅ found | The `ExemplarFilter` configuration MUST allow users to select between one of the built-in ExemplarFilters. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:73` |  |
| 107 | SHOULD | ✅ found | The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for an SDK. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:73` |  |
| 108 | SHOULD | ✅ found | The default value SHOULD be `TraceBased`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:245` |  |
| 109 | SHOULD | ✅ found | The filter configuration SHOULD follow the environment variable specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114` |  |
| 110 | MUST | ✅ found | An OpenTelemetry SDK MUST support the following filters: AlwaysOn, AlwaysOff, TraceBased | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14` |  |

#### ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 111 | MUST | ✅ found | The `ExemplarReservoir` interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 112 | MUST | ⚠️ partial | A new `ExemplarReservoir` MUST be created for every known timeseries data point, as determined by aggregation and view configuration. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` | One ОтелРезервуарЭкземпляров is created per instrument, not per timeseries data point. The reservoir internally manages data per-key (КлючАтрибутов) via СинхронизированнаяКарта, which is functionally equivalent but architecturally different from a new reservoir per timeseries. |
| 113 | SHOULD | ✅ found | The "offer" method SHOULD accept measurements, including: The value of the measurement, the complete set of Attributes of the measurement, the Context of the measurement, a timestamp that best represents when the measurement was taken. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 114 | SHOULD | ✅ found | The "offer" method SHOULD have the ability to pull associated trace and span information without needing to record full context. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 115 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the "offer" method. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 116 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the "offer" method. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 117 | MUST | ✅ found | The "collect" method MUST return accumulated `Exemplar`s. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:55` |  |
| 118 | SHOULD | ✅ found | Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:139` |  |
| 119 | MUST | ✅ found | `Exemplar`s MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:130` |  |
| 120 | SHOULD | ⚠️ partial | The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:112` | The reservoir creates new Соответствие objects for each exemplar in СоздатьЭкземпляр(), allocating on every measurement offer rather than avoiding allocations. |

#### Exemplar defaults

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar-defaults)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 121 | MUST | ✅ found | The SDK MUST include two types of built-in exemplar reservoirs: `SimpleFixedSizeExemplarReservoir`, `AlignedHistogramBucketExemplarReservoir` | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1` |  |
| 122 | SHOULD | ✅ found | Explicit bucket histogram aggregation with more than 1 bucket SHOULD use `AlignedHistogramBucketExemplarReservoir`. | `src/Метрики/Классы/ОтелМетр.os:99` |  |
| 123 | SHOULD | ✅ found | Base2 Exponential Histogram Aggregation SHOULD use a `SimpleFixedSizeExemplarReservoir` with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty (e.g. `min(20, max_buckets)`). | `src/Метрики/Классы/ОтелМетр.os:137` |  |
| 124 | SHOULD | ✅ found | All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |

#### SimpleFixedSizeExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#simplefixedsizeexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 125 | MUST | ✅ found | This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the reservoir has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:80` |  |
| 126 | SHOULD | ✅ found | Any stateful portion of sampling computation SHOULD be reset every collection cycle. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:65` |  |
| 127 | SHOULD | ✅ found | Otherwise, a default size of `1` SHOULD be used. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:165` |  |

#### AlignedHistogramBucketExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#alignedhistogrambucketexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 128 | MUST | ✅ found | This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:158` |  |
| 129 | MUST | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50` |  |
| 130 | SHOULD | ⚠️ partial | and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50` | The implementation uses a last-seen strategy (replaces the exemplar on each measurement) instead of uniformly-weighted sampling per bucket. The spec permits this as an alternative (MAY keep last seen), but the SHOULD for uniform sampling is not met. |
| 131 | SHOULD | ✅ found | This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:158` |  |

#### Custom ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#custom-exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 132 | MUST | ✅ found | The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation. | `src/Метрики/Классы/ОтелПредставление.os:83` |  |
| 133 | MUST | ✅ found | This extension MUST be configurable on a metric View | `src/Метрики/Классы/ОтелПредставление.os:164` |  |
| 134 | MUST | ⚠️ partial | although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reservoir - Paragraph 2). | `src/Метрики/Классы/ОтелМетр.os:534` | The custom reservoir from the View is set per-instrument via ПрименитьПредставлениеКИнструменту, not per metric-timeseries. The same reservoir instance is shared across all timeseries of an instrument, using internal keying by КлючАтрибутов instead of separate instantiation. |

#### Collect

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#collect)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 135 | SHOULD | ❌ not_found | `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | СобратьИЭкспортировать is a void Процедура that catches errors internally and logs them, but does not return any result to the caller indicating success, failure, or timeout. |
| 136 | SHOULD | ✅ found | `Collect` SHOULD invoke Produce on registered MetricProducers. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:275` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 137 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MetricReader` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:106` |  |
| 138 | SHOULD | ⚠️ partial | SDKs SHOULD return some failure for these calls, if possible. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88` | After Закрыть(), СброситьБуфер() (Collect) still executes СобратьИЭкспортировать() without checking Закрыт flag - no failure is returned for post-shutdown calls |
| 139 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:105` | Закрыть() is a Процедура (void), does not return success/failure/timeout status to the caller |
| 140 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:111` |  |

#### Periodic exporting MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 141 | MUST | ✅ found | The reader MUST synchronize calls to `MetricExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:141` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 142 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD collect metrics, call `Export(batch)` and `ForceFlush()` on the configured Push Metric Exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88` | СброситьБуфер() calls СобратьИЭкспортировать() which collects and exports, but does not call Экспортер.СброситьБуфер() (ForceFlush on the exporter) |
| 143 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88` | СброситьБуфер() is a Процедура (void), does not return success/failure/timeout status |
| 144 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88` | СброситьБуфер() is a void procedure with no return value - errors are caught silently in СобратьИЭкспортировать() |
| 145 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88` |  |

#### MetricExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 146 | MUST | ✅ found | `MetricExporter` defines the interface that protocol-specific exporters MUST implement so that they can be plugged into OpenTelemetry SDK and support sending of telemetry data. | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1` |  |
| 147 | SHOULD | ❌ not_found | Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsupported Aggregation or Aggregation Temporality, as this condition can be corrected by a change of `MetricReader` configuration. | - | ОтелЭкспортерМетрик.Экспортировать() does not validate aggregation type or temporality - no error is reported for unsupported aggregation/temporality combinations |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 148 | MUST | ✅ found | A Push Metric Exporter MUST support the following functions: | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:13` |  |
| 149 | MUST | ✅ found | The SDK MUST provide a way for the exporter to get the Meter information (e.g. name, version, etc.) associated with each `Metric Point`. | `src/Метрики/Классы/ОтелДанныеМетрики.os:42` |  |
| 150 | MUST NOT | ⚠️ partial | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:29` | Export delegates to Транспорт.Отправить() which uses HTTP with default timeouts, but there is no explicit configurable timeout on the Export method itself |
| 151 | MUST | ⚠️ partial | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:29` | Export relies on HTTP transport timeouts implicitly, no explicit timeout limit with error result (Failure) is configured in the exporter |
| 152 | SHOULD NOT | ✅ found | The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the metrics are being sent to. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:29` |  |
| 153 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Metrics` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47` |  |
| 154 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47` | СброситьБуфер() on exporter is a void procedure (Процедура), does not return success/failure status |
| 155 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed metrics. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47` |  |
| 156 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47` |  |
| 157 | SHOULD | ⚠️ partial | Shutdown SHOULD be called only once for each `MetricExporter` instance. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:53` | Закрыть() uses АтомарноеБулево so multiple calls are safe, but subsequent Export calls return Ложь without explicitly returning a Failure result as spec requires |
| 158 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:53` |  |

#### MetricProducer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricproducer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 159 | MUST | ✅ found | `MetricProducer` defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:1` |  |
| 160 | SHOULD | ❌ not_found | `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of produced metrics. | - | ИнтерфейсПродюсерМетрик has only Произвести() method with no parameters - no way to configure AggregationTemporality for produced metrics |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 161 | MUST | ✅ found | A `MetricProducer` MUST support the following functions: | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:10` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 162 | MUST | ✅ found | A `MetricFilter` MUST support the following functions: | `src/Метрики/Классы/ОтелФильтрМетрик.os:29` |  |

#### Defaults and configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#defaults-and-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 163 | MUST | ✅ found | The SDK MUST provide configuration according to the SDK environment variables specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:16` |  |

#### Numerical limits handling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#numerical-limits-handling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 164 | MUST | ❌ not_found | The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry. | - | No explicit numerical limits handling found in the metrics SDK. There is no graceful error handling for overflow, underflow, or other numerical edge cases in aggregators or instruments. |
| 165 | MUST | ❌ not_found | If the SDK receives float/double values from Instruments, it MUST handle all the possible values. | - | No explicit handling of special float/double values (NaN, Infinity, etc.) found in the metrics SDK. Instruments and aggregators accept numeric values without validation or special-value handling. |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 166 | SHOULD | ✅ found | All the metrics components SHOULD allow new methods to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:26` |  |
| 167 | SHOULD | ✅ found | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to existing methods without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:105` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 168 | MUST | ⚠️ partial | MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:241` | Meter creation uses СинхронизированнаяКарта (thread-safe map) for caching meters. However, the Закрыт flag is a plain Булево (not АтомарноеБулево), so concurrent Закрыть()/ПолучитьМетр() calls have a data race. СброситьБуфер() and Закрыть() do not use locks for iteration over ЧитателиМетрик. |
| 169 | MUST | ⚠️ partial | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:167` | Uses СинхронизированнаяКарта for bucket storage and АтомарноеЧисло for measurement counters. However, the array inside each bucket (МассивЭкземпляров) is a plain Массив - concurrent Предложить() calls can race on МассивЭкземпляров.Количество() check and МассивЭкземпляров.Добавить()/indexed assignment. |
| 170 | MUST | ✅ found | MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:14` |  |
| 171 | MUST | ✅ found | MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:13` |  |

### Otlp Exporter

#### Configuration Options

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#configuration-options)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The following configuration options MUST be available to configure the OTLP exporter. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:149` |  |
| 2 | MUST | ✅ found | Each configuration option MUST be overridable by a signal specific option. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:695` |  |
| 3 | MUST | ✅ found | The implementation MUST honor the following URL components: | `src/Экспорт/Классы/ОтелHttpТранспорт.os:104` |  |
| 4 | MUST | ✅ found | When using `OTEL_EXPORTER_OTLP_ENDPOINT`, exporters MUST construct per-signal URLs as described below. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:510` |  |
| 5 | SHOULD | ✅ found | The option SHOULD accept any form allowed by the underlying gRPC client implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:147` |  |
| 6 | MUST | ✅ found | Additionally, the option MUST accept a URL with a scheme of either `http` or `https`. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:147` |  |
| 7 | SHOULD | ✅ found | If the gRPC client implementation does not support an endpoint with a scheme of `http` or `https` then the endpoint SHOULD be transformed to the most sensible format for that implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:174` |  |
| 8 | MUST | ✅ found | Options MUST be one of: `grpc`, `http/protobuf`, `http/json`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:470` |  |
| 9 | SHOULD | ✅ found | SDKs SHOULD default endpoint variables to use `http` scheme unless they have good reasons to choose `https` scheme for the default (e.g., for backward compatibility reasons in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:177` |  |
| 10 | SHOULD | ❌ not_found | However, if they are already implemented, they SHOULD continue to be supported as they were part of a stable release of the specification. | - | Obsolete env vars OTEL_EXPORTER_OTLP_SPAN_INSECURE and OTEL_EXPORTER_OTLP_METRIC_INSECURE are not supported. The requirement is conditional ('if they are already implemented') and these were never implemented in this SDK, but they are still not supported. |
| 11 | SHOULD | ⚠️ partial | The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:468` | Default protocol is 'http/json' instead of the recommended 'http/protobuf'. The SDK defaults to http/json at line 468 (ПараметрСигналаИлиОбщий default) and line 169 (СоздатьТранспорт default). |

#### Endpoint URLs for OTLP/HTTP

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#endpoint-urls-for-otlphttp)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal as follow: | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:510` |  |
| 13 | MUST | ✅ found | For the per-signal variables (`OTEL_EXPORTER_OTLP_<signal>_ENDPOINT`), the URL MUST be used as-is without any modification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:498` |  |
| 14 | MUST | ✅ found | The only exception is that if an URL contains no path part, the root path `/` MUST be used (see Example 2). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:716` |  |
| 15 | MUST NOT | ✅ found | An SDK MUST NOT modify the URL in ways other than specified above. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:707` |  |

#### Specify Protocol

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specify-protocol)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ⚠️ partial | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:468` | SDK supports grpc (ОтелGrpcТранспорт) and http/json (ОтелHttpТранспорт), but http/protobuf config value is accepted and routed to ОтелHttpТранспорт which sends JSON, not actual protobuf over HTTP. |
| 17 | MUST | ✅ found | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:37` |  |
| 18 | SHOULD | ⚠️ partial | If they support only one, it SHOULD be `http/protobuf`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:468` | SDK supports grpc and http/json but not true http/protobuf transport. The HTTP transport always sends JSON-encoded data regardless of the configured protocol value. |
| 19 | SHOULD | ⚠️ partial | If no configuration is provided the default transport SHOULD be `http/protobuf` unless SDKs have good reasons to choose `grpc` as the default (e.g. for backward compatibility reasons when `grpc` was already the default in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:468` | Default protocol is 'http/json' (line 468), not the recommended 'http/protobuf'. The SDK does not support true http/protobuf transport. |

#### Specifying headers via environment variables

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:569` |  |

#### Retry

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#retry)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | Transient errors MUST be handled with a retry strategy. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:76` |  |
| 22 | MUST | ✅ found | This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:166` |  |

#### User Agent

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#user-agent)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | SHOULD | ❌ not_found | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter. | - | No User-Agent header is emitted by ОтелHttpТранспорт or ОтелGrpcТранспорт. No code sets a User-Agent header in the export requests. |
| 24 | SHOULD | ❌ not_found | The format of the header SHOULD follow RFC 7231. | - | User-Agent header is not implemented at all, so RFC 7231 format compliance is not applicable. |
| 25 | SHOULD | ❌ not_found | The resulting User-Agent SHOULD include the exporter's default User-Agent string. | - | User-Agent header is not implemented. No default User-Agent string exists to include. |

### Propagators

#### Operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Propagator`s MUST define `Inject` and `Extract` operations, in order to write values to and read values from carriers respectively. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:45` |  |
| 2 | MUST | ✅ found | Each `Propagator` type MUST define the specific carrier type and MAY define additional parameters. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:45` |  |

#### Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The Propagator MUST retrieve the appropriate value from the `Context` first, such as `SpanContext`, `Baggage` or another cross-cutting concern context. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:46` |  |

#### Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any previously existing valid value. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:89` |  |
| 5 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any previously existing valid value. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:90` |  |

#### TextMap Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | In order to increase compatibility, the key/value pairs MUST only consist of US-ASCII characters that make up valid HTTP header fields as per RFC 9110. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:62` |  |
| 7 | MUST | ✅ found | `Getter` and `Setter` MUST be stateless and allowed to be saved as constants, in order to effectively avoid runtime allocations. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:71` |  |

#### Setter argument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#setter-argument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:19` |  |
| 9 | MUST | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:19` |  |

#### Getter argument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#getter-argument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The `Keys` function MUST return the list of all the keys in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:59` |  |
| 11 | MUST | ✅ found | The Get function MUST return the first value of the given propagation key or return null if the key doesn't exist. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:20` |  |
| 12 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:21` |  |
| 13 | MUST | ✅ found | If explicitly implemented, the `GetAll` function MUST return all values of the given propagation key. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40` |  |
| 14 | SHOULD | ✅ found | It SHOULD return them in the same order as they appear in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:42` |  |
| 15 | SHOULD | ✅ found | If the key doesn't exist, it SHOULD return an empty collection. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:41` |  |
| 16 | MUST | ✅ found | The `GetAll` function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:43` |  |

#### Composite Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | Implementations MUST offer a facility to group multiple `Propagator`s from different cross-cutting concerns in order to leverage them as a single entity. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:79` |  |
| 18 | MUST | ✅ found | There MUST be functions to accomplish the following operations. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:18` |  |

#### Global Propagators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#global-propagators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | The OpenTelemetry API MUST provide a way to obtain a propagator for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |
| 20 | SHOULD | ✅ found | Instrumentation libraries SHOULD call propagators to extract and inject the context on all remote calls. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |
| 21 | MUST | ✅ found | The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise. | `src/Ядро/Модули/ОтелГлобальный.os:132` |  |
| 22 | SHOULD | ✅ found | `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace Context Propagator and the Baggage `Propagator` specified in the Baggage API. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:362` |  |
| 23 | MUST | ✅ found | These platforms MUST also allow pre-configured propagators to be disabled or overridden. | `src/Ядро/Модули/ОтелГлобальный.os:110` |  |

#### Get Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#get-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | This method MUST exist for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |

#### Set Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#set-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | This method MUST exist for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:110` |  |

#### Propagators Distribution

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#propagators-distribution)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | MUST | ✅ found | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry extension packages: | `src/Пропагация/Классы/ОтелW3CПропагатор.os:1` |  |
| 27 | MUST | ✅ found | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry extension packages: | `src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:1` |  |
| 28 | MUST NOT | ✅ found | It MUST NOT use `OpenTracing` in the resulting propagator name as it is not widely adopted format in the OpenTracing ecosystem. | - |  |
| 29 | MUST NOT | ✅ found | Additional `Propagator`s implementing vendor-specific protocols such as AWS X-Ray trace header protocol MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | - |  |

#### W3C Trace Context Requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#w3c-trace-context-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP headers as specified in W3C Trace Context Level 2. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:81` |  |
| 31 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid `traceparent` value using the same header. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:63` |  |
| 32 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid `tracestate` unless the value is empty, in which case the `tracestate` header may be omitted. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:65` |  |

#### Fields

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#fields)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | MUST | ✅ found | Fields MUST return the header names that correspond to the configured format, i.e., the headers used for the inject operation. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:137` |  |

### Env Vars

#### Environment Variable Specification

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#environment-variable-specification)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If they do, they SHOULD use the names and value parsing behavior specified in this document. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:6` |  |
| 2 | SHOULD | ✅ found | They SHOULD also follow the common configuration specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:78` |  |

#### Implementation guidelines

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#implementation-guidelines)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The environment-based configuration MUST have a direct code configuration equivalent. | `src/Ядро/Классы/ОтелПостроительSdk.os:24` |  |

#### Parsing empty value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#parsing-empty-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:674` |  |

#### Boolean

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#boolean)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Any value that represents a Boolean MUST be set to true only by the case-insensitive string "true", meaning "True" or "TRUE" are also accepted, as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:667` |  |
| 6 | MUST NOT | ✅ found | An implementation MUST NOT extend this definition and define additional values that are interpreted as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:667` |  |
| 7 | MUST | ✅ found | Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:667` |  |
| 8 | SHOULD | ❌ not_found | If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied. | - | Функция Включено() возвращает НРег(Значение) = "true" без логирования предупреждения при нераспознанных значениях (например, "yes", "1", "on"). При некорректном булевом значении молча возвращается Ложь без предупреждения пользователю. |
| 9 | SHOULD | ⚠️ partial | All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:666` | Единственная булева переменная OTEL_ENABLED имеет значение по умолчанию "true". По спецификации безопасное поведение по умолчанию должно соответствовать значению false. Рекомендуемый подход - использовать OTEL_SDK_DISABLED=false (SDK включён) вместо OTEL_ENABLED=true. |
| 10 | MUST NOT | ✅ found | Renaming or changing the default value MUST NOT happen without a major version upgrade. | `packagedef:7` |  |

#### Numeric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#numeric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | The following paragraph was added after stabilization and the requirements are thus qualified as "SHOULD" to allow implementations to avoid breaking changes. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:682` |  |
| 12 | MUST | ✅ found | For new implementations, these should be treated as MUST requirements. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:682` |  |
| 13 | SHOULD | ✅ found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them as not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:686` |  |

#### Enum

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#enum)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | SHOULD | ✅ found | Enum values SHOULD be interpreted in a case-insensitive manner. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:196` |  |
| 15 | MUST | ✅ found | For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:237` |  |

#### General SDK Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | Values MUST be deduplicated in order to register a `Propagator` only once. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:390` |  |
| 17 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:686` |  |
| 18 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:688` |  |
| 19 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:224` |  |

#### Attribute Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#attribute-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | Implementations SHOULD only offer environment variables for the types of attributes, for which that SDK implements truncation mechanism. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:434` |  |

#### Exporter Selection

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#exporter-selection)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | SHOULD NOT | ✅ found | `"logging"`: Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:196` |  |
| 22 | SHOULD NOT | ✅ found | `"logging"`: Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:312` |  |
| 23 | SHOULD NOT | ✅ found | `"logging"`: Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:276` |  |

#### Declarative configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#declarative-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ❌ not_found | When `OTEL_CONFIG_FILE` is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored. | - | OTEL_CONFIG_FILE and OTEL_EXPERIMENTAL_CONFIG_FILE are not referenced anywhere in the codebase. Declarative configuration via file-based config is not implemented. |

## Требования Development-статуса

Эти требования находятся в секциях со статусом Development. Их реализация не обязательна для соответствия стабильной спецификации.

### Resource Sdk

#### Resource detector name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-detector-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ➖ n_a | Resource detectors SHOULD have a unique name for reference in configuration. | - | Resource Detector Naming feature is not implemented. Detectors have no name property or naming mechanism. |
| 2 | SHOULD | ➖ n_a | Names SHOULD be snake case and consist of lowercase alphanumeric and `_` characters, which ensures they conform to declarative configuration property name requirements. | - | Resource Detector Naming feature is not implemented. |
| 3 | SHOULD | ➖ n_a | Resource detector names SHOULD reflect the root namespace of attributes they populate. | - | Resource Detector Naming feature is not implemented. |
| 4 | SHOULD | ➖ n_a | Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name which appropriately conveys their purpose. | - | Resource Detector Naming feature is not implemented. |
| 5 | SHOULD | ➖ n_a | An SDK which identifies multiple resource detectors with the same name SHOULD report an error. | - | Resource Detector Naming feature is not implemented. |
| 6 | SHOULD | ➖ n_a | resource detectors SHOULD document their name in a manner which is easily discoverable. | - | Resource Detector Naming feature is not implemented. |

### Trace Api

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | a `Tracer` SHOULD provide this `Enabled` API. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 2 | MUST | ✅ found | the API MUST be structured in a way for parameters to be added. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 3 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 4 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they create a new `Span` to ensure they have the most up-to-date response. | `src/Трассировка/Классы/ОтелТрассировщик.os:31` | Метод Включен() документирован как способ пропустить создание спана, но не содержит указания вызывать его каждый раз перед созданием нового Span и что результат может меняться со временем |

### Trace Sdk

#### Tracer Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` (see API). | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 2 | MUST | ✅ found | The `TracerProvider` MUST implement the Get a Tracer API. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Tracer`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:63` |  |
| 4 | MUST | ✅ found | The `TracerProvider` MUST compute the relevant TracerConfig using the configured TracerConfigurator, and create a `Tracer` whose behavior conforms to that `TracerConfig`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:71` |  |

#### TracerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: * `tracer_scope`: The `InstrumentationScope` of the `Tracer`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:220` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `TracerConfig`, or some signal indicating that the default TracerConfig should be used. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:215` |  |

#### Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Tracer` MUST behave according to the TracerConfig computed during Tracer creation. | `src/Трассировка/Классы/ОтелТрассировщик.os:39` |  |
| 2 | MUST | ✅ found | the `Tracer` MUST be updated to behave according to the new `TracerConfig`. | `src/Трассировка/Классы/ОтелТрассировщик.os:178` |  |

#### TracerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the `enabled` parameter SHOULD default to `true` (i.e. `Tracer`s are enabled by default). | `src/Трассировка/Классы/ОтелКонфигурацияТрассировщика.os:35` |  |
| 2 | MUST | ⚠️ partial | If a `Tracer` is disabled, it MUST behave equivalently to a No-op Tracer. | `src/Трассировка/Классы/ОтелТрассировщик.os:39` | Метод Включен() корректно возвращает Ложь при отключённой конфигурации, но методы НачатьСпан/НачатьКорневойСпан/НачатьДочернийСпан не проверяют Включен() и не возвращают автоматически no-op спан при отключённом трассировщике; вызывающий код должен проверять Включен() самостоятельно |
| 3 | MUST | ✅ found | The value of `enabled` MUST be used to resolve whether a `Tracer` is Enabled. | `src/Трассировка/Классы/ОтелТрассировщик.os:39` |  |
| 4 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Трассировка/Классы/ОтелТрассировщик.os:13` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Enabled` MUST return `false` when either: there are no registered `SpanProcessors`, `Tracer` is disabled (`TracerConfig.enabled` is `false`). | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:42` |  |

#### TraceIdRatioBased

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#traceidratiobased)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The `TraceIdRatioBased` MUST ignore the parent `SampledFlag`. | `src/Трассировка/Модули/ОтелСэмплер.os:241` |  |
| 2 | MUST | ✅ found | Description MUST return a string of the form `"TraceIdRatioBased{RATIO}"` with `RATIO` replaced with the Sampler instance's trace sampling ratio represented as a decimal number. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 3 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 4 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 5 | MUST | ✅ found | The sampling algorithm MUST be deterministic. | `src/Трассировка/Модули/ОтелСэмплер.os:277` |  |
| 6 | MUST | ✅ found | To achieve this, implementations MUST use a deterministic hash of the `TraceId` when computing the sampling decision. | `src/Трассировка/Модули/ОтелСэмплер.os:290` |  |
| 7 | MUST | ✅ found | A `TraceIdRatioBased` sampler with a given sampling probability MUST also sample all traces that any `TraceIdRatioBased` sampler with a lower sampling probability would sample. | `src/Трассировка/Модули/ОтелСэмплер.os:292` |  |
| 8 | SHOULD | ❌ not_found | When this sampler observes a non-empty parent span context, meaning when it is used not as a root sampler, the SDK SHOULD emit a warning such as: | - | No warning is emitted when TraceIdRatioBased is used as a child sampler. The СэмплироватьПоДоле function does not check for parent context presence and does not log any warnings. |

#### ProbabilitySampler

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#probabilitysampler)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | The `ProbabilitySampler` sampler MUST ignore the parent `SampledFlag`. | - | ProbabilitySampler is not implemented. Only the deprecated TraceIdRatioBased sampler exists (ОтелСэмплер.ПоДолеТрассировок). There is no sampler using W3C Trace Context Level 2 56-bit randomness with rejection threshold comparison. |
| 2 | SHOULD | ❌ not_found | When (R >= T), the OpenTelemetry TraceState SHOULD be modified to include the key-value `th:T` for rejection threshold value (T), as specified for the OpenTelemetry TraceState `th` sub-key. | - | ProbabilitySampler is not implemented. No TraceState modification with threshold values occurs in the existing sampler code. |
| 3 | SHOULD | ❌ not_found | When a ProbabilitySampler Sampler makes a decision for a non-root Span using TraceID randomness when the Trace random flag was not set, the SDK SHOULD issue a warning statement in its log with a compatibility warning. | - | ProbabilitySampler is not implemented. No compatibility warning logic exists in the codebase. |

#### AlwaysRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwaysrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | Based on the decision from the wrapped root sampler, `AlwaysRecord` MUST behave as follows: | - | AlwaysRecord sampler decorator is not implemented. There is no sampler that wraps another sampler and converts DROP decisions to RECORD_ONLY. The existing samplers (AlwaysOn, AlwaysOff, TraceIdRatioBased, ParentBased) do not include this decorator pattern. |

#### CompositeSampler

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#compositesampler)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the parameters passed to delegate GetSamplingIntent methods, as they are considered read-only state. | - | CompositeSampler and ComposableSampler interfaces are not implemented. There is no GetSamplingIntent method or SamplingIntent structure in the codebase. |
| 2 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the OpenTelemetry TraceState (i.e., the `ot` sub-key of TraceState). | - | CompositeSampler and ComposableSampler interfaces are not implemented. |
| 3 | SHOULD | ❌ not_found | The calling CompositeSampler SHOULD update the threshold of the outgoing TraceState (unless `!threshold_reliable`) and that the explicit randomness values MUST not be modified. | - | CompositeSampler is not implemented. No threshold-based TraceState updates exist. |
| 4 | MUST | ❌ not_found | The calling CompositeSampler SHOULD update the threshold of the outgoing TraceState (unless `!threshold_reliable`) and that the explicit randomness values MUST not be modified. | - | CompositeSampler is not implemented. No protection of explicit randomness values in TraceState exists. |
| 5 | SHOULD | ❌ not_found | For the zero case a `ComposableAlwaysOff` instance SHOULD be returned instead. | - | ComposableProbability and ComposableAlwaysOff are not implemented. No ComposableSampler hierarchy exists in the codebase. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | Custom implementations of the `IdGenerator` SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace `random` flag will be set in the associated Trace contexts. | - | There is no mechanism for custom IdGenerator implementations to signal whether they produce random TraceIDs. The extension point (УстановитьГенераторИд) accepts any object with the two generation methods but provides no marker interface or property to indicate randomness characteristics. |

#### OnEnding

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onending)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The end timestamp MUST have been computed (the `OnEnding` method duration is not included in the span duration). | `src/Трассировка/Классы/ОтелСпан.os:450` |  |
| 2 | MUST | ✅ found | The Span object MUST still be mutable (i.e., `SetAttribute`, `AddLink`, `AddEvent` can be called) while `OnEnding` is called. | `src/Трассировка/Классы/ОтелСпан.os:455` |  |
| 3 | MUST | ✅ found | This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:455` |  |
| 4 | MUST | ⚠️ partial | The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking `OnEnding` of the first `SpanProcessor`. | `src/Трассировка/Классы/ОтелСпан.os:447` | Метод Завершить() не содержит явной синхронизации (БлокировкаРесурса) для предотвращения конкурентной модификации спана из другого потока (ФоновоеЗадание). Последовательный поток выполнения в рамках одного потока частично удовлетворяет требование, но явной гарантии нет. |

### Logs Api

#### Ergonomic API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#ergonomic-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | The ergonomic API SHOULD make it more convenient to emit event records following the event semantics. | - | В кодовой базе отсутствует эргономичный API для логирования. Текущий API требует явного создания ОтелЗаписьЛога, ручной установки полей и вызова Записать(). Нет удобных методов вроде Logger.Info(), Logger.Event() для быстрой отправки событий. |
| 2 | SHOULD | ❌ not_found | The design of the ergonomic API SHOULD be idiomatic for its language. | - | Эргономичный API не реализован, поэтому требование к его идиоматичности неприменимо в текущем состоянии кода. |

### Logs Sdk

#### Logger Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ⚠️ partial | It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` (see API). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` | OneScript не поддерживает ограничение видимости конструкторов; Logger может быть создан напрямую через Новый ОтелЛоггер(), хотя штатный путь - через ОтелПровайдерЛогирования |
| 2 | MUST | ✅ found | The `LoggerProvider` MUST implement the Get a Logger API. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Logger`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:64` |  |
| 4 | MUST | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:64` |  |
| 5 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:94` |  |
| 6 | SHOULD | ❌ not_found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | - | При получении логгера с пустым или невалидным именем не логируется предупреждающее сообщение о невалидности значения |
| 7 | MUST | ✅ found | The `LoggerProvider` MUST compute the relevant LoggerConfig using the configured LoggerConfigurator, and create a `Logger` whose behavior conforms to that `LoggerConfig`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:70` |  |

#### LoggerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: * `logger_scope`: The `InstrumentationScope` of the `Logger`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:72` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `LoggerConfig`, or some signal indicating that the default LoggerConfig should be used. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:72` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Logger` MUST behave according to the LoggerConfig computed during logger creation. | `src/Логирование/Классы/ОтелЛоггер.os:240` |  |
| 2 | MUST | ✅ found | If the `LoggerProvider` supports updating the LoggerConfigurator, then upon update the `Logger` MUST be updated to behave according to the new `LoggerConfig`. | `src/Логирование/Классы/ОтелЛоггер.os:123` |  |

#### LoggerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the `enabled` parameter SHOULD default to `true` (i.e. `Logger`s are enabled by default). | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 2 | MUST | ✅ found | If a `Logger` is disabled, it MUST behave equivalently to No-op Logger. | `src/Логирование/Классы/ОтелЛоггер.os:50` |  |
| 3 | MUST | ✅ found | If not explicitly set, the `minimum_severity` parameter MUST default to `0`. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 4 | MUST | ✅ found | If a log record's SeverityNumber is specified (i.e. not `0`) and is less than the configured `minimum_severity`, the log record MUST be dropped by the `Logger`. | `src/Логирование/Классы/ОтелЛоггер.os:138` |  |
| 5 | MUST | ✅ found | If not explicitly set, the `trace_based` parameter MUST default to `false`. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 6 | MUST | ✅ found | If `trace_based` is `true`, log records associated with unsampled traces MUST be dropped by the `Logger`. | `src/Логирование/Классы/ОтелЛоггер.os:143` |  |
| 7 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Логирование/Классы/ОтелЛоггер.os:123` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If Observed Timestamp is unspecified, the implementation SHOULD set it equal to the current time. | `src/Логирование/Классы/ОтелЛоггер.os:102` |  |
| 2 | MUST | ✅ found | If an Exception is provided, the SDK MUST by default set attributes from the exception on the `LogRecord` with the conventions outlined in the exception semantic conventions. | `src/Логирование/Классы/ОтелЛоггер.os:170` |  |
| 3 | MUST | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:183` |  |
| 4 | MUST NOT | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:184` |  |
| 5 | MUST | ✅ found | Before processing a log record, the implementation MUST apply the filtering rules defined by the LoggerConfig (in case `Enabled` was not called prior to emitting the record): | `src/Логирование/Классы/ОтелЛоггер.os:94` |  |
| 6 | MUST | ✅ found | Minimum severity: If the log record's SeverityNumber is specified (i.e. not `0`) and is less than the configured `minimum_severity`, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:138` |  |
| 7 | MUST | ✅ found | Trace-based: If `trace_based` is `true`, and if the log record has a `SpanId` and the `TraceFlags` SAMPLED flag is unset, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:143` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | `Enabled` MUST return `false` when either: * there are no registered `LogRecordProcessors`. * `Logger` is disabled (`LoggerConfig.enabled` is `false`). * the provided severity is specified (i.e. not `0`) and is less than the configured `minimum_severity` in the `LoggerConfig`. * `trace_based` is `true` in the `LoggerConfig` and the current context is associated with an unsampled trace. * all registered `LogRecordProcessors` implement `Enabled`, and a call to `Enabled` on each of them returns `false`. | `src/Логирование/Классы/ОтелЛоггер.os:42` | Conditions 1-4 are correctly implemented. Condition 5 (all processors' Enabled returns false) is missing - the code calls ЕстьПроцессоры() which only checks processor count > 0, but does not call Включен() on individual processors via the composite processor. |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Логирование/Классы/ОтелЛоггер.os:61` |  |

### Metrics Api

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | OpenTelemetry SDKs MUST handle `advisory` parameters as described here. | `src/Метрики/Классы/ОтелМетр.os:51` |  |

### Metrics Sdk

#### Meter Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create `Meter` instances through a `MeterProvider` (see API). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 2 | MUST | ✅ found | The `MeterProvider` MUST implement the Get a Meter API. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:62` |  |
| 4 | MUST | ⚠️ partial | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` | A working Meter is returned for empty string names, but null (Неопределено) would cause a type error in ОбластьИнструментирования.Ключ() during string concatenation. No explicit invalid-name guard exists. |
| 5 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:94` |  |
| 6 | SHOULD | ❌ not_found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | - | No logging of invalid name values in ПолучитьМетр. The method does not check for empty or null names and does not log any warning message. |
| 7 | MUST | ✅ found | The `MeterProvider` MUST compute the relevant MeterConfig using the configured MeterConfigurator, and create a `Meter` whose behavior conforms to that `MeterConfig`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:206` |  |

#### MeterConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: * `meter_scope`: The `InstrumentationScope` of the `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:210` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `MeterConfig`, or some signal indicating that the default MeterConfig should be used. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:211` |  |

#### Start timestamps

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#start-timestamps)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp, or the creation time of the instrument if this is the first collection interval for the instrument. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:145` |  |
| 2 | MUST | ✅ found | This implies that all data points with delta temporality aggregation for an instrument MUST share the same start timestamp. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:283` |  |
| 3 | MUST | ✅ found | Cumulative timeseries MUST use a consistent start timestamp for all collection intervals. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141` |  |
| 4 | SHOULD | ⚠️ partial | For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the series. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:263` | Start timestamp is set to instrument creation time (ОтелУтилиты.ТекущееВремяВНаносекундах() in constructor), not the time of the first measurement. While close in practice, the spec specifically asks for the first measurement time. |
| 5 | SHOULD | ⚠️ partial | For asynchronous instrument, the start timestamp SHOULD be: | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:184` | In ПреобразоватьЗаписиВТочки, startTimeUnixNano is set to the current collection time (ВремяСейчас), not the instrument creation time or prior collection interval timestamp as specified. |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:493` |  |
| 2 | MUST | ✅ found | `Meter` MUST behave according to the MeterConfig computed during Meter creation. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:206` |  |
| 3 | MUST | ❌ not_found | If the `MeterProvider` supports updating the MeterConfigurator, then upon update the `Meter` MUST be updated to behave according to the new `MeterConfig`. | - | ОтелПровайдерМетрик does not support updating the MeterConfigurator after creation; the Конфигуратор is set once in the constructor with no method to update it and re-apply configurations to existing Meters |

#### MeterConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the `enabled` parameter SHOULD default to `true` (i.e. `Meter`s are enabled by default). | `src/Метрики/Классы/ОтелКонфигурацияМетра.os:35` |  |
| 2 | MUST | ✅ found | If a `Meter` is disabled, it MUST behave equivalently to No-op Meter. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:79` |  |
| 3 | MUST | ✅ found | The value of `enabled` MUST be used to resolve whether an instrument is Enabled. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:202` |  |
| 4 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Метрики/Классы/ОтелМетр.os:504` |  |

#### Instrument enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | The synchronous instrument `Enabled` MUST return `false` when either: The MeterConfig of the `Meter` used to create the instrument has parameter `enabled=false`. All resolved views for the instrument are configured with the Drop Aggregation. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` | Метод Включен() корректно возвращает Ложь при MeterConfig.enabled=false (через разделяемый АтомарноеБулево МетрВключен). Однако условие 'все представления используют Drop Aggregation' не реализовано - нет кода, который проверяет агрегацию из View и устанавливает Включен в Ложь при Drop. |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:267` |  |

#### MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ⚠️ partial | To construct a `MetricReader` when setting up an SDK, at least the following SHOULD be provided: | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:320` | Constructor accepts exporter and interval, but does not directly accept optional aggregation function, temporality function, or cardinality limit parameters. MetricFilter and MetricProducers are set via separate methods rather than at construction. |
| 2 | SHOULD | ❌ not_found | This function SHOULD be obtained from the `exporter`. | - | The default output aggregation function is not obtained from the exporter. Aggregation is determined by instrument type in ОтелМетр, not configured through the MetricReader from the exporter. |
| 3 | SHOULD | ✅ found | If not configured, the default aggregation SHOULD be used. | `src/Метрики/Классы/ОтелМетр.os:58` |  |
| 4 | SHOULD | ✅ found | This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:189` |  |
| 5 | SHOULD | ✅ found | If not configured, the Cumulative temporality SHOULD be used. | `src/Метрики/Модули/ОтелСелекторВременнойАгрегации.os:24` |  |
| 6 | SHOULD | ✅ found | If not configured, a default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` |  |
| 7 | SHOULD | ✅ found | A `MetricReader` SHOULD provide the MetricFilter to the SDK or registered MetricProducer(s) when calling the `Produce` operation. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:132` |  |
| 8 | SHOULD | ✅ found | A common implementation of `MetricReader`, the periodic exporting `MetricReader` SHOULD be provided to be used typically with push-based metrics collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:1` |  |
| 9 | MUST | ✅ found | The `MetricReader` MUST ensure that data points from OpenTelemetry instruments are output in the configured aggregation temporality for each instrument kind. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:186` |  |
| 10 | MUST | ✅ found | For synchronous instruments with Cumulative aggregation temporality, MetricReader.Collect MUST receive data points exposed in previous collections regardless of whether new measurements have been recorded. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141` |  |
| 11 | MUST | ✅ found | For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:143` |  |
| 12 | MUST | ✅ found | For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:159` |  |
| 13 | MUST | ✅ found | For instruments with Cumulative aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST repeat the same starting timestamps (e.g. `(T0, T1], (T0, T2], (T0, T3]`). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141` |  |
| 14 | MUST | ✅ found | For instruments with Delta aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST advance the starting timestamp (e.g. `(T0, T1], (T1, T2], (T2, T3]`). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:145` |  |
| 15 | MUST | ✅ found | The ending timestamp (i.e. `TimeUnixNano`) MUST always be equal to time the metric data point took effect, which is equal to when MetricReader.Collect was invoked. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:274` |  |
| 16 | MUST | ✅ found | The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider` | `src/Метрики/Классы/ОтелПровайдерМетрик.os:250` |  |
| 17 | SHOULD NOT | ⚠️ partial | the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NOT introduce side-effects to other `MetricReader` instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:116` | Multiple readers share in-memory state (accumulators) in the same instruments. During independent periodic collection, one reader calling ОчиститьТочкиДанных for Delta temporality clears data that other readers may not have collected yet. The СброситьБуферБезОчистки mechanism only works for explicit flush, not for normal periodic cycles. |
| 18 | MUST NOT | ❌ not_found | The SDK MUST NOT allow a `MetricReader` instance to be registered on more than one `MeterProvider` instance. | - | No check exists in the code to prevent a MetricReader from being registered on multiple MeterProvider instances. The reader's ДобавитьМетр method accepts any Meter without verifying provider uniqueness. |
| 19 | SHOULD | ✅ found | The SDK SHOULD provide a way to allow `MetricReader` to respond to MeterProvider.ForceFlush and MeterProvider.Shutdown. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88` |  |

#### Produce batch

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#produce-batch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Produce` MUST return a batch of Metric Points, filtered by the optional `metricFilter` parameter. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:10` |  |
| 2 | SHOULD | ⚠️ partial | Implementation SHOULD use the filter as early as possible to gain as much performance gain possible (memory allocation, internal metric fetching, etc). | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:259` | MetricFilter is applied in the reader (ОтелПериодическийЧитательМетрик) after data collection, not in the producer's Произвести() method itself - filtering happens post-collection rather than as early as possible |
| 3 | SHOULD | ❌ not_found | If the batch of Metric Points includes resource information, `Produce` SHOULD require a resource as a parameter. | - | ИнтерфейсПродюсерМетрик.Произвести() has no parameters at all - no resource parameter even though the produced metrics include resource info |
| 4 | SHOULD | ❌ not_found | `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Произвести() returns a Массив of metrics data - no mechanism to report failure or timeout status to the caller |
| 5 | SHOULD | ❌ not_found | If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`. | - | ИнтерфейсПродюсерМетрик has no InstrumentationScope - the interface is a minimal stub with just Произвести() returning an empty array |

## Условные требования (Conditional)

Требования из условных секций. Применяются только при реализации соответствующей опциональной фичи.

### Propagators

#### B3 Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-extract) | Scope: conditional:B3 Propagator (extension)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | MUST attempt to extract B3 encoded using single and multi-header formats. | - | B3 Propagator is not implemented in this SDK. This is a conditional extension (scope: conditional:B3 Propagator) and no B3 propagator class exists in the codebase. |
| 2 | MUST | ➖ n_a | MUST preserve a debug trace flag, if received, and propagate it with subsequent requests. | - | B3 Propagator is not implemented in this SDK. This is a conditional extension (scope: conditional:B3 Propagator) and no B3 propagator class exists in the codebase. |
| 3 | MUST | ➖ n_a | Additionally, an OpenTelemetry implementation MUST set the sampled trace flag when the debug flag is set. | - | B3 Propagator is not implemented in this SDK. This is a conditional extension (scope: conditional:B3 Propagator) and no B3 propagator class exists in the codebase. |
| 4 | MUST NOT | ➖ n_a | MUST NOT reuse `X-B3-SpanId` as the id for the server-side span. | - | B3 Propagator is not implemented in this SDK. This is a conditional extension (scope: conditional:B3 Propagator) and no B3 propagator class exists in the codebase. |

#### B3 Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-inject) | Scope: conditional:B3 Propagator (extension)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | MUST default to injecting B3 using the single-header format | - | B3 Propagator is not implemented in this SDK. This is a conditional extension (scope: conditional:B3 Propagator) and no B3 propagator class exists in the codebase. |
| 2 | MUST | ➖ n_a | MUST provide configuration to change the default injection format to B3 multi-header | - | B3 Propagator is not implemented in this SDK. This is a conditional extension (scope: conditional:B3 Propagator) and no B3 propagator class exists in the codebase. |
| 3 | MUST NOT | ➖ n_a | MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support reusing the same id for both sides of a request. | - | B3 Propagator is not implemented in this SDK. This is a conditional extension (scope: conditional:B3 Propagator) and no B3 propagator class exists in the codebase. |

### Сводка условных секций

| Раздел | Секция | Scope | Stability | Keywords | Ссылка |
|---|---|---|---|---|---|
| Resource Sdk | Resource detector name | conditional:Resource Detector Naming (conditional) | Development | 6 | [spec](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-detector-name) |
| Propagators | B3 Extract | conditional:B3 Propagator (extension) | Stable | 4 | [spec](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-extract) |
| Propagators | B3 Inject | conditional:B3 Propagator (extension) | Stable | 3 | [spec](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-inject) |

## Ограничения платформы OneScript

| Ограничение | Влияние на спецификацию | Решение |
|---|---|---|
| Нет наносекундной точности | Временные метки с точностью до миллисекунд | Используется миллисекундная точность |
| Нет TLS/mTLS из SDK | Сертификаты конфигурируются вне SDK | Делегировано системе/прокси |
| Нет opaque-объектов | Ключи контекста - строки | Строковые константы как ключи |
| Нет thread-local | ФоновыеЗадания вместо goroutines | Передача контекста через параметры |

## Методология

### Процесс анализа

1. **Извлечение требований** (`extract_requirements.py`): загрузка 12 страниц спецификации, разбиение на секции, подсчёт MUST/SHOULD keywords
2. **Генерация промптов** (`generate_prompts.py`): группировка секций по доменам, генерация промптов с JSON-схемой вывода для агентов
3. **Верификация** (general-purpose агенты): каждый агент анализирует 5-8 секций, записывает результат в JSON
4. **Сборка отчёта** (`assemble_report.py`): детерминированная сборка markdown из JSON-результатов

### Статусы

| Статус | Значение |
|---|---|
| ✅ found | Требование полностью реализовано с корректной семантикой |
| ⚠️ partial | Код существует, но не полностью соответствует спецификации |
| ❌ not_found | Реализация отсутствует |
| ➖ n_a | Неприменимо из-за ограничений платформы |

### Статистика извлечения

| Метрика | Значение |
|---|---|
| Страниц спецификации | 12 |
| Всего секций | 242 |
| Stable секций | 213 |
| Development секций | 29 |
| Conditional секций | 3 |
| Всего keywords | 824 |
| Stable universal keywords | 694 |

