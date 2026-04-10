# Анализ соответствия спецификации OpenTelemetry v1.55.0

> **Версия спецификации**: [v1.55.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-04-10
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
| ✅ Реализовано (found) | 521 (75.2%) |
| ⚠️ Частично (partial) | 106 (15.3%) |
| ❌ Не реализовано (not_found) | 66 (9.5%) |
| ➖ Неприменимо (n_a) | 2 |
| **MUST/MUST NOT found** | 353/418 (84.4%) |
| **SHOULD/SHOULD NOT found** | 168/275 (61.1%) |

## Соответствие по разделам (Stable)

| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |
|---|---|---|---|---|---|---|
| Context | 14 | 1 | 0 | 0 | 15 | 93.3% |
| Baggage Api | 16 | 1 | 0 | 0 | 17 | 94.1% |
| Resource Sdk | 12 | 4 | 4 | 0 | 20 | 60.0% |
| Trace Api | 103 | 15 | 4 | 0 | 122 | 84.4% |
| Trace Sdk | 58 | 16 | 8 | 0 | 82 | 70.7% |
| Logs Api | 19 | 1 | 0 | 1 | 20 | 95.0% |
| Logs Sdk | 47 | 14 | 3 | 0 | 64 | 73.4% |
| Metrics Api | 85 | 16 | 0 | 0 | 101 | 84.2% |
| Metrics Sdk | 112 | 27 | 32 | 0 | 171 | 65.5% |
| Otlp Exporter | 11 | 7 | 6 | 1 | 24 | 45.8% |
| Propagators | 32 | 0 | 1 | 0 | 33 | 97.0% |
| Env Vars | 12 | 4 | 8 | 0 | 24 | 50.0% |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Context]** [MUST] The API MUST accept the following parameters: * The `Context`.  
  Нет прямого Attach(Context) API, принимающего объект контекста. Методы УстановитьЗначение(Ключ, Значение), СделатьСпанТекущим(Спан), СделатьBaggageТекущим(Багаж) создают контекст внутри из key-value, а не принимают готовый Context как параметр. (`src/Ядро/Модули/ОтелКонтекст.os:203`)

- ⚠️ **[Resource Sdk]** [MUST] Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK.  
  Detectors exist (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) but are all within src/Ядро/Классы/ - inline in the SDK package, not in separate packages. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1`)

- ❌ **[Resource Sdk]** [MUST] Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions.  
  Detectors (host, process, cpu) populate known semconv attributes (host.name, os.type, process.pid) but create resources via Новый ОтелРесурс(Истина) with empty Schema URL. No Schema URL matching semantic conventions is ever set. (-)

- ⚠️ **[Resource Sdk]** [MUST] If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources.  
  The Слить() method detects Schema URL conflicts and returns an empty resource, but the detector combining in ЗаполнитьАтрибутыПоУмолчанию() copies attributes directly without using Слить() and does not check Schema URLs. Also no error is reported on conflict. (`src/Ядро/Классы/ОтелРесурс.os:41`)

- ❌ **[Resource Sdk]** [MUST] The `,` and `=` characters in keys and values MUST be percent encoded.  
  РазобратьПарыКлючЗначение() splits by ',' and '=' but performs no percent-decoding. Values containing %2C or %3D will not be decoded back to ',' or '='. (-)

- ⚠️ **[Trace Api]** [MUST] `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false.  
  IsRemote method exists but the logic for propagated contexts vs child spans is handled during span creation, not explicitly in the IsRemote method itself (`src/Трассировка/Классы/ОтелКонтекстСпана.os:60`)

- ⚠️ **[Trace Api]** [MUST] When extracting a `SpanContext` through the Propagators API, `IsRemote` MUST return true  
  The Удаленный flag is set during construction and can be set via УстановитьУдаленный, but the integration with Propagators API needs verification in propagation components (`src/Трассировка/Классы/ОтелКонтекстСпана.os:172`)

- ⚠️ **[Trace Api]** [MUST NOT] `Span` creation MUST NOT set the newly created `Span` as the active `Span` in the current `Context` by default  
  Span creation doesn't set it as active by default, but the separate СделатьТекущим() method must be called explicitly (`src/Трассировка/Классы/ОтелСпан.os:398`)

- ❌ **[Trace Api]** [MUST] The API MUST provide an operation for wrapping a `SpanContext` with an object implementing the `Span` interface.  
  No explicit wrapping operation found. The code creates spans from span contexts but doesn't expose a direct wrapping API. (-)

- ⚠️ **[Trace Api]** [MUST] `GetContext` MUST return the wrapped `SpanContext`.  
  NoopSpan returns a context but it's not wrapped from an external SpanContext - it's internally generated. (`src/Трассировка/Классы/ОтелНоопСпан.os:29`)

- ⚠️ **[Trace Api]** [MUST] This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable.  
  NoOp functionality exists but no SpanContext wrapping operation is implemented. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ⚠️ **[Trace Api]** [MUST] Event - Events are immutable and MUST be safe for concurrent use by default.  
  Event class exists but no explicit documentation about immutability or thread safety. (`src/Трассировка/Классы/ОтелСобытиеСпана.os:1`)

- ⚠️ **[Trace Api]** [MUST] The API MUST return a non-recording `Span` with the `SpanContext` in the parent `Context` (whether explicitly given or implicit current).  
  Provider returns tracers when closed, but they don't properly propagate parent context - they create new tracers with no special no-op behavior. (`src/Трассировка/Классы/ОтелТрассировщик.os:65`)

- ⚠️ **[Trace Api]** [MUST] If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.e., having a `SpanContext` with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags).  
  NoopSpan exists but when provider is closed, it still creates normal tracers rather than ensuring all spans are non-recording with empty contexts. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ⚠️ **[Trace Sdk]** [MUST] Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, `Sampler`, and (Development) TracerConfigurator) MUST be owned by the `TracerProvider`.  
  SpanProcessors, SpanLimits, Sampler и TracerConfigurator принадлежат TracerProvider, но IdGenerator отсутствует как конфигурируемый компонент - генерация ID реализована через статические утилиты ОтелУтилиты.СгенерироватьИдТрассировки(), а не как заменяемый генератор на провайдере (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:9`)

- ⚠️ **[Trace Sdk]** [MUST] For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated since 1.10.0] having the same name and version values as the `InstrumentationScope`.  
  ОтелСпан exposes ОбластьИнструментирования() (InstrumentationScope) but there is no separate deprecated InstrumentationLibrary accessor. The same object is used, but there is no explicit backward-compatible alias. (`src/Трассировка/Классы/ОтелСпан.os:170`)

- ❌ **[Trace Sdk]** [MUST NOT] SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value.  
  The sampler module does not handle the OpenTelemetry TraceState rv sub-key at all. There is no code to read, preserve, or avoid overwriting explicit randomness values in TraceState. The function returns a new result without any TraceState handling related to the rv sub-key. (-)

- ⚠️ **[Trace Sdk]** [MUST] The SDK MAY provide this functionality by allowing custom implementations of an interface like the java example below (name of the interface MAY be `IdGenerator`, name of the methods MUST be consistent with SpanContext), which provides extension points for two methods, one to generate a `SpanId` and one for `TraceId`.  
  The IdGenerator is implemented as a duck-typed object passed to УстановитьГенераторИд(). Methods are named СгенерироватьИдТрассировки() and СгенерироватьИдСпана() which are consistent with SpanContext's ИдТрассировки/ИдСпана. However there is no formal interface class - it relies on duck typing. (`src/Ядро/Модули/ОтелУтилиты.os:63`)

- ⚠️ **[Trace Sdk]** [MUST] The built-in SpanProcessors MUST do so.  
  Пакетный процессор экспортирует все буферизированные спаны через ЭкспортироватьВсеПакеты(), но не вызывает ForceFlush (СброситьБуфер) на экспортере после экспорта, как требует спецификация (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68`)

- ❌ **[Trace Sdk]** [MUST] If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls.  
  Метод СброситьБуфер() не принимает параметр таймаута. ЭкспортироватьВсеПакеты() выполняет цикл до полного опустошения буфера без возможности прерывания по таймауту (-)

- ⚠️ **[Trace Sdk]** [MUST] Span Exporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.  
  Закрыт is a plain Булево, not АтомарноеБулево - concurrent Shutdown calls may have race conditions; compare with ОтелПровайдерТрассировки which uses АтомарноеБулево for its Закрыт flag (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:47`)

- ❌ **[Logs Sdk]** [MUST NOT] Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller.  
  LogRecordProcessor не реализует операцию Enabled. Интерфейс ИнтерфейсПроцессорЛогов не содержит метода Enabled. Фильтрация реализована на уровне ОтелЛоггер.Включен(), а не на уровне процессора. (-)

- ⚠️ **[Logs Sdk]** [MUST] The built-in LogRecordProcessors MUST do so.  
  Встроенные процессоры экспортируют все буферизованные записи, но не вызывают ForceFlush на экспортере после экспорта, как требует предыдущее предложение. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68-70`)

- ❌ **[Logs Sdk]** [MUST] If a timeout is specified (see below), the `LogRecordProcessor` MUST prioritize honoring the timeout over finishing all calls.  
  Метод СброситьБуфер() не принимает параметр таймаута. Нет механизма приоритизации таймаута над завершением всех вызовов экспорта в ForceFlush. (-)

- ⚠️ **[Logs Sdk]** [MUST] LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.  
  Код экспортера содержит комментарий о необходимости потокобезопасности (строка 3-4), но переменная Закрыт - обычный Булево без атомарной защиты (не АтомарноеБулево). В отличие от ОтелПровайдерЛогирования, который использует АтомарноеБулево и СинхронизированнаяКарта, экспортер не использует примитивы синхронизации для флага Закрыт. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:3`)

- ⚠️ **[Metrics Api]** [MUST] Therefore, this API MUST be structured to accept a variable number of `callback` functions, including none.  
  API создания асинхронных инструментов принимает 0 или 1 callback через параметр Callback = Неопределено. Переменное количество callback не поддерживается при создании - дополнительные добавляются через ДобавитьCallback() после создания (`src/Метрики/Классы/ОтелМетр.os:229`)

- ⚠️ **[Metrics Api]** [MUST] The API MUST support creation of asynchronous instruments by passing zero or more `callback` functions to be permanently registered to the newly created instrument.  
  При создании можно передать 0 или 1 callback. Передача более одного callback при создании не поддерживается - нужно использовать ДобавитьCallback() после создания (`src/Метрики/Классы/ОтелМетр.os:229`)

- ⚠️ **[Metrics Api]** [MUST] Callback functions MUST be documented as follows for the end user:  
  Комментарии в ОтелНаблюдениеМетрики описывают использование callback, но не документируют три рекомендации (reentrant safe, не бесконечное время, не дублировать наблюдения) (`src/Метрики/Классы/ОтелНаблюдениеМетрики.os:56`)

- ⚠️ **[Metrics Api]** [MUST] MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  Реализация потокобезопасна (СинхронизированнаяКарта для кэша метрик), но методы не документированы явно как safe for concurrent use. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:241`)

- ⚠️ **[Metrics Api]** [MUST] Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  Реализация потокобезопасна (СинхронизированнаяКарта, АтомарноеБулево), но методы не документированы явно как safe for concurrent use. (`src/Метрики/Классы/ОтелМетр.os:493`)

- ⚠️ **[Metrics Api]** [MUST] Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  Реализация потокобезопасна (СинхронизированнаяКарта для аккумуляторов, АтомарноеБулево для флагов), но методы не документированы явно как safe for concurrent use. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:261`)

- ⚠️ **[Metrics Sdk]** [MUST] updated configuration MUST also apply to all already returned `Meters`  
  Configuration is applied only at Meter creation time. No dynamic configuration update mechanism for existing Meters is implemented. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:71`)

- ❌ **[Metrics Sdk]** [MUST NOT] it MUST NOT matter whether a `Meter` was obtained from the `MeterProvider` before or after the configuration change  
  No configuration change mechanism exists - configuration is only applied at creation time (-)

- ⚠️ **[Metrics Sdk]** [MUST] `Shutdown` MUST be called only once for each `MeterProvider` instance.  
  Закрыть() method sets Закрыт flag but does not prevent multiple calls - no guard against repeated shutdown (`src/Метрики/Классы/ОтелПровайдерМетрик.os:130`)

- ❌ **[Metrics Sdk]** [MUST] The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept.  
  Exclude-list field exists in ОтелПредставление (ИсключенныеКлючиАтрибутов) but the actual exclusion filtering is not implemented in the measurement pipeline. (-)

- ❌ **[Metrics Sdk]** [MUST] The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept.  
  Exclude-list field exists in ОтелПредставление (ИсключенныеКлючиАтрибутов) but the keep-remaining logic for excluded attributes is not implemented. (-)

- ⚠️ **[Metrics Sdk]** [MUST] If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance.  
  Default aggregation is applied per instrument type (Sum for Counter, Histogram for Histogram, LastValue for Gauge). However, the aggregation is not configurable per MetricReader instance - all readers share the same aggregation strategy set at instrument creation time. (`src/Метрики/Классы/ОтелМетр.os:58`)

- ⚠️ **[Metrics Sdk]** [MUST] If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST apply the default aggregation cardinality limit the `MetricReader` is configured with.  
  A default cardinality limit of 2000 is applied per instrument, but it is hardcoded in ОтелБазовыйСинхронныйИнструмент rather than being configurable on the MetricReader instance as the spec requires. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253`)

- ⚠️ **[Metrics Sdk]** [MUST] Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that observations made or produced by executing callbacks only apply to the intended `MetricReader` during collection.  
  Callbacks are invoked during each reader's collection cycle, but observations go into the instrument's shared state (ВнешниеНаблюдения on ОтелБазовыйНаблюдаемыйИнструмент). Multiple readers share the same instrument state, so observations are not truly isolated per MetricReader. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:140`)

- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created.  
  Overflow aggregator with otel.metric.overflow=true attribute is created lazily on first overflow (line 92: Если Аккумуляторы.Количество() >= ЛимитМощности), not prior to reaching the limit. The overflow bucket is not pre-allocated, so total accumulators can exceed the configured limit by 1 (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:325`)

- ⚠️ **[Metrics Sdk]** [MUST] When this happens, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above.  
  Meter returns the first-seen instrument correctly (name normalized via НРег, lookup by lowercase key returns original). However, ПроверитьКонфликтДескриптора (line 562) only logs a warning when instrument parameters (kind/unit/description/advisory) differ. For pure case-different duplicates with identical parameters, no log/error is emitted, violating the 'log an appropriate error' part of the requirement. (`src/Метрики/Классы/ОтелМетр.os:51`)

- ⚠️ **[Metrics Sdk]** [MUST] If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit string.  
  The 'not provided' case is handled by the default parameter value ЕдиницаИзмерения = "". However, if Неопределено (null) is passed explicitly, it is stored as Неопределено without coercion to empty string. No explicit null-to-empty conversion exists in the instrument creation methods. (`src/Метрики/Классы/ОтелМетр.os:48`)

- ⚠️ **[Metrics Sdk]** [MUST] If a description is not provided or the description is null, the Meter MUST treat it the same as an empty description string.  
  The 'not provided' case is handled by the default parameter value Описание = "". However, if Неопределено (null) is passed explicitly, it is stored as Неопределено without coercion to empty string. No explicit null-to-empty conversion exists in the instrument creation methods. (`src/Метрики/Классы/ОтелМетр.os:48`)

- ⚠️ **[Metrics Sdk]** [MUST] The reader MUST synchronize calls to `MetricExporter`'s `Export` to make sure that they are not invoked concurrently.  
  БлокировкаРесурса (lock) используется только для потокобезопасного копирования массива Метров (строка 124-135), но сам вызов Экспортер.Экспортировать() (строка 154) находится вне блокировки. При одновременном вызове ПериодическийСбор (фоновое задание) и СброситьБуфер (основной поток) возможен конкурентный вызов Export. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:124`)

- ❌ **[Metrics Sdk]** [MUST] `MetricProducer` defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data.  
  Интерфейс MetricProducer не реализован. Нет отдельного класса или интерфейса для подключения сторонних источников метрик к MetricReader. (-)

- ❌ **[Metrics Sdk]** [MUST] A `MetricProducer` MUST support the following functions:  
  MetricProducer не реализован как отдельный интерфейс или класс. Функции Produce не существует. (-)

- ❌ **[Metrics Sdk]** [MUST] The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry.  
  Нет явного кода обработки числовых пределов (overflow, underflow) в метрическом SDK. Агрегаторы и инструменты не содержат проверок на выход за пределы числовых типов. (-)

- ❌ **[Metrics Sdk]** [MUST] If the SDK receives float/double values from Instruments, it MUST handle all the possible values.  
  Нет явной обработки NaN и Infinity в агрегаторах метрик. Код принимает значения от инструментов без проверки на специальные значения IEEE 754 (NaN, +Infinity, -Infinity). (-)

- ⚠️ **[Metrics Sdk]** [MUST] MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.  
  Meter creation использует СинхронизированнаяКарта (потокобезопасно). Однако ForceFlush (СброситьБуфер) и Shutdown (Закрыть) итерируют массив ЧитателиМетрик без блокировки, а флаг Закрыт - обычный Булево, не АтомарноеБулево. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:241`)

- ⚠️ **[Metrics Sdk]** [MUST] ExemplarReservoir - all methods MUST be safe to be called concurrently.  
  Используется СинхронизированнаяКарта для Данные и Счетчики, АтомарноеЧисло для счетчиков измерений. Однако операции с внутренним Массивом экземпляров (Добавить, присваивание по индексу) в методе ДобавитьВРезервуар не синхронизированы - возможна гонка при конкурентных вызовах Предложить для одного КлючАтрибутов. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:167`)

- ⚠️ **[Metrics Sdk]** [MUST] MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.  
  Комментарий в коде признает необходимость конкурентной безопасности, но реализация не использует ни БлокировкаРесурса, ни АтомарноеБулево. Флаг Закрыт - обычный Булево без синхронизации. ForceFlush (СброситьБуфер) - пустой метод (inherently safe), но Shutdown и Export имеют гонку данных на флаге Закрыт. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:3`)

- ⚠️ **[Otlp Exporter]** [MUST] The following configuration options MUST be available to configure the OTLP exporter.  
  Endpoint, Protocol, Headers, Compression, Timeout доступны через env vars; Certificate File, Client key file, Client certificate file, Insecure не реализованы (TLS/mTLS - ограничение платформы OneScript) (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130`)

- ❌ **[Otlp Exporter]** [MUST] Each configuration option MUST be overridable by a signal specific option.  
  Per-signal переменные окружения (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_TRACES_HEADERS и т.д.) не поддерживаются; все сигналы используют общую конфигурацию (-)

- ⚠️ **[Otlp Exporter]** [MUST] Options MUST be one of: `grpc`, `http/protobuf`, `http/json`.  
  Код принимает grpc и http/json, но http/protobuf не реализован полноценно - HTTP-транспорт всегда отправляет JSON; валидация допустимых значений протокола отсутствует (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ⚠️ **[Otlp Exporter]** [MUST] Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal as follow:  
  URL конструируются из базового OTEL_EXPORTER_OTLP_ENDPOINT + относительные пути (/v1/traces, /v1/logs, /v1/metrics), но per-signal endpoint переменные (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT и т.д.) не поддерживаются (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:35`)

- ❌ **[Otlp Exporter]** [MUST] For the per-signal variables (`OTEL_EXPORTER_OTLP_<signal>_ENDPOINT`), the URL MUST be used as-is without any modification.  
  Per-signal endpoint переменные (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_ENDPOINT, OTEL_EXPORTER_OTLP_LOGS_ENDPOINT) не поддерживаются (-)

- ❌ **[Otlp Exporter]** [MUST] The only exception is that if an URL contains no path part, the root path `/` MUST be used (see Example 2).  
  Per-signal endpoint переменные не поддерживаются, поэтому обработка пустого пути для per-signal URL не реализована (-)

- ⚠️ **[Env Vars]** [MUST] The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset.  
  Некоторые параметры проверяют пустую строку (строки 105, 137, 398, 411, 439, 447 через '<> ""'), но параметры использующие значение по умолчанию в Менеджер.Параметр(ключ, умолчание) не обрабатывают пустую строку как неустановленное значение - пустая строка обходит значение по умолчанию (например строки 150, 160, 177, 255, 291, 562) (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105`)

- ❌ **[Env Vars]** [MUST] For new implementations, these should be treated as MUST requirements.  
  Как новая реализация, код должен обрабатывать числовые значения на уровне MUST (предупреждение + graceful ignore), но вызовы Число() (строки 160, 204, 215, 224-227, 263-266, 312, 399, 401, 412, 414, 440, 448) не обёрнуты в Попытка/Исключение, не генерируют предупреждений и не обрабатывают невалидные значения gracefully. (-)

- ⚠️ **[Env Vars]** [MUST] For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting.  
  Для пропагаторов выводится предупреждение через Сообщить (строка 373) и значение пропускается. Но для OTEL_TRACES_SAMPLER (строка 216) нераспознанное значение молча заменяется на parentbased_always_on без предупреждения. Для OTEL_METRICS_EXEMPLAR_FILTER (ОтелПостроительПровайдераМетрик.os:123) нераспознанное значение игнорируется без предупреждения. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:373`)

- ❌ **[Env Vars]** [MUST] Values MUST be deduplicated in order to register a `Propagator` only once.  
  В СоздатьПропагаторы (ОтелАвтоконфигурация.os:336-378) список пропагаторов разбирается через СтрРазделить, но дедупликация не выполняется. Если пользователь укажет 'tracecontext,tracecontext', будут созданы два экземпляра ОтелW3CПропагатор. (-)

- ❌ **[Env Vars]** [MUST] Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set.  
  В коде обработки OTEL_TRACES_SAMPLER_ARG (ОтелАвтоконфигурация.os:203-204) значение напрямую преобразуется через Число() без обработки ошибок. Невалидный ввод (например, нечисловая строка) вызовет исключение вместо логирования. (-)

- ❌ **[Env Vars]** [MUST] Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set.  
  Невалидный OTEL_TRACES_SAMPLER_ARG не игнорируется gracefully - вызов Число() с нечисловым значением приведёт к исключению, а не к игнорированию параметра. (-)

- ❌ **[Env Vars]** [MUST] Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set.  
  При невалидном OTEL_TRACES_SAMPLER_ARG реализация не ведёт себя так, как будто параметр не установлен. Вместо фолбэка на значение по умолчанию (1.0 для traceidratio) происходит исключение. (-)

- ❌ **[Env Vars]** [MUST] When `OTEL_CONFIG_FILE` is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored.  
  Переменная OTEL_CONFIG_FILE не поддерживается в реализации. Нет кода, который бы проверял наличие этой переменной или реализовывал декларативную конфигурацию из файла. (-)

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Baggage Api]** [SHOULD NOT] The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation.  
  Контекстный ключ КлючBaggage экспортируется через публичный метод КлючBaggage() в области ПрограммныйИнтерфейс, давая пользователям API прямой доступ к ключу контекста. Хотя удобные методы BaggageИзКонтекста/КонтекстСBaggage делают прямой доступ необязательным, ключ всё равно доступен. (`src/Ядро/Модули/ОтелКонтекст.os:53`)

- ⚠️ **[Resource Sdk]** [SHOULD] whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error.  
  Detection errors are caught and logged via Лог.Отладка() (debug level) instead of being treated as errors at error log level. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:24`)

- ⚠️ **[Resource Sdk]** [SHOULD] Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate (e.g. the detector that reads the attributes from environment values will not know what Schema URL to use).  
  All detectors use empty Schema URL including those that populate known semconv attributes (host.name, os.type, process.pid). Empty Schema URL is correct for unknown-attribute detectors but incorrect for detectors that populate known semconv attributes - they should set a proper Schema URL instead. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18`)

- ❌ **[Resource Sdk]** [SHOULD] In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded  
  No error handling exists for OTEL_RESOURCE_ATTRIBUTES parsing. Invalid pairs are silently skipped rather than discarding the entire value. (-)

- ❌ **[Resource Sdk]** [SHOULD] and an error SHOULD be reported following the Error Handling principles.  
  No error reporting for OTEL_RESOURCE_ATTRIBUTES parsing failures. No logging or exception is raised on malformed input. (-)

- ❌ **[Trace Api]** [SHOULD] In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its name property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged.  
  Нет логирования предупреждения при передаче пустого или невалидного имени в ПолучитьТрассировщик(). Код принимает любое имя без валидации и не выводит сообщение о невалидном значении. (-)

- ⚠️ **[Trace Api]** [SHOULD NOT] The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation.  
  Ключ контекста для спана доступен публично через ОтелКонтекст.КлючСпана(). Хотя существуют удобные методы (СпанИзКонтекста, КонтекстСоСпаном), пользователи имеют прямой доступ к ключу. (`src/Ядро/Модули/ОтелКонтекст.os:44`)

- ⚠️ **[Trace Api]** [SHOULD] The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable.  
  Span name can be changed via ИзменитьИмя method, but there's no validation or guidance enforcement for naming conventions (`src/Трассировка/Классы/ОтелСпан.os:247`)

- ⚠️ **[Trace Api]** [SHOULD] Generality SHOULD be prioritized over human-readability.  
  Implementation allows setting any name without enforcing generality vs readability guidelines (`src/Трассировка/Классы/ОтелСпан.os:247`)

- ❌ **[Trace Api]** [SHOULD NOT] If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible  
  No wrapping functionality implemented to evaluate this requirement. (-)

- ❌ **[Trace Api]** [SHOULD] If a new type is required to be publicly exposed, it SHOULD be named `NonRecordingSpan`.  
  No NonRecordingSpan class found, only ОтелНоопСпан which serves a different purpose. (-)

- ⚠️ **[Trace Api]** [SHOULD] In order for `SpanKind` to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose.  
  SpanKind enum exists but there's no enforcement or guidance in the API to prevent spans serving multiple purposes. (`src/Трассировка/Модули/ОтелВидСпана.os:1`)

- ⚠️ **[Trace Api]** [SHOULD NOT] For example, a server-side span SHOULD NOT be used to describe outgoing remote procedure call.  
  SpanKind enum exists but there's no enforcement or guidance in the API to prevent misuse. (`src/Трассировка/Модули/ОтелВидСпана.os:1`)

- ⚠️ **[Trace Api]** [SHOULD] Link - Links are immutable and SHOULD be safe for concurrent use by default.  
  Links are implemented as dictionaries but no explicit documentation about immutability or thread safety. (`src/Трассировка/Классы/ОтелСпан.os:372`)

- ⚠️ **[Trace Api]** [SHOULD] If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly without instantiating a new `Span`.  
  No specific logic to detect and return existing non-recording spans. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] SDKs SHOULD return a valid no-op Tracer for these calls, if possible.  
  После Закрыть() метод ПолучитьТрассировщик возвращает обычный ОтелТрассировщик (не ОтелНоопСпан-based), который продолжает пытаться создавать спаны через закрытые процессоры, вместо возврата настоящего no-op трассировщика (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65`)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Синхронный метод Закрыть() - Процедура без возвращаемого значения. Асинхронный ЗакрытьАсинхронно() возвращает Обещание, через которое можно обнаружить ошибку, но основной метод не сигнализирует об успехе/неудаче (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:132`)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Синхронный Закрыть() не имеет механизма таймаута. Асинхронный ЗакрытьАсинхронно() возвращает Обещание, на котором вызывающая сторона может установить таймаут через Получить(timeout), но сам метод не контролирует таймаут (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:132`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Синхронный СброситьБуфер() - Процедура без возвращаемого значения. Асинхронный СброситьБуферАсинхронно() возвращает Обещание для обнаружения ошибок, но основной метод не сигнализирует об успехе/неудаче (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:121`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Синхронный СброситьБуфер() не имеет механизма таймаута. Асинхронный СброситьБуферАсинхронно() возвращает Обещание с возможностью таймаута через Получить(timeout), но сам метод не контролирует таймаут (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:121`)

- ❌ **[Trace Sdk]** [SHOULD NOT] Callers SHOULD NOT cache the returned value.  
  This is a caller-side requirement about not caching the result of GetDescription. The implementation provides ОтелСэмплер.Описание() which returns a fresh string each time, but there is no enforcement or documentation warning callers not to cache. This is largely a usage guideline rather than an implementation requirement. (-)

- ❌ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements.  
  The Random flag (bit 1, value 2) is never set in trace flags. ВычислитьФлагиТрассировки() in ОтелТрассировщик.os only returns 0 or 1 (Sampled flag), with no handling of the Random trace flag. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the `rv` sub-key of the OpenTelemetry TraceState.  
  The TraceIdRatio sampler does use the TraceID for sampling decisions, effectively presuming randomness. However, there is no handling of the rv sub-key of the OpenTelemetry TraceState as an alternative source of randomness - the sampler always relies on TraceID randomness without checking for explicit randomness. (`src/Трассировка/Модули/ОтелСэмплер.os:275`)

- ❌ **[Trace Sdk]** [SHOULD] If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated.  
  The SDK supports a custom IdGenerator via УстановитьГенераторИд(), but there is no mechanism for the custom IdGenerator to indicate whether it produces random TraceIDs. The Random flag (W3C Trace Context Level 2) is not exposed to or controlled by the IdGenerator extension. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`.  
  The SDK uses names МаксСобытий (MaxEvents) and МаксЛинков (MaxLinks) instead of EventCountLimit and LinkCountLimit as recommended by the spec. Functionality is equivalent but naming convention differs. (`src/Трассировка/Классы/ОтелЛимитыСпана.os:26`)

- ⚠️ **[Trace Sdk]** [SHOULD] After the call to `Shutdown`, subsequent calls to `OnStart`, `OnEnd`, or `ForceFlush` are not allowed. SDKs SHOULD ignore these calls gracefully, if possible.  
  Пакетный процессор проверяет флаг Закрыт в методе Обработать (OnEnd), но не проверяет в ПриНачале (OnStart) и СброситьБуфер (ForceFlush). Простой процессор не имеет флага Закрыт и не игнорирует вызовы после Закрыть() (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43`)

- ❌ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод Закрыть() возвращает Void во всех реализациях процессоров спанов - нет способа сообщить вызывающему коду об успехе, ошибке или таймауте (-)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Пакетный процессор имеет таймаут для остановки фонового экспорта (ОстановитьФоновыйЭкспорт с ТаймаутЭкспортаМс), но ЭкспортироватьВсеПакеты() не ограничена таймаутом и может выполняться бесконечно. Простой процессор не имеет таймаута (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192`)

- ⚠️ **[Trace Sdk]** [SHOULD] In particular, if any `SpanProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all spans for which this was not already done and then invoke `ForceFlush` on it.  
  СброситьБуфер() вызывает ЭкспортироватьВсеПакеты(), который вызывает Экспортер.Экспортировать() для всех буферизированных спанов, но не вызывает Экспортер.СброситьБуфер() (ForceFlush экспортера) после экспорта (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68`)

- ❌ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() возвращает Void во всех реализациях процессоров спанов - нет способа сообщить вызывающему коду об успехе, ошибке или таймауте (-)

- ❌ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Метод СброситьБуфер() не имеет механизма таймаута. ЭкспортироватьВсеПакеты() в пакетном процессоре выполняет бесконечный цикл до полного опустошения буфера без ограничения по времени (-)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() is a Процедура (void) - it does not return any status indicator (success, failure, or timeout) to the caller (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41`)

- ⚠️ **[Logs Api]** [SHOULD] The API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response.  
  Метод Включен() задокументирован (строки 28-41), но документация не содержит указания о том, что авторы инструментирования должны вызывать его каждый раз перед emit для получения актуального ответа. (`src/Логирование/Классы/ОтелЛоггер.os:28`)

- ⚠️ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод Закрыть() - процедура (void), не возвращает статус успеха/неуспеха/таймаута (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:116`)

- ⚠️ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Метод Закрыть() не принимает параметр таймаута и не имеет механизма прерывания по времени (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:116`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() - процедура (void), не возвращает статус успеха/неуспеха/таймаута (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  СброситьБуфер() не возвращает ERROR статус - является процедурой (void) (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  СброситьБуфер() не возвращает NO ERROR статус - является процедурой (void) (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Метод СброситьБуфер() не принимает параметр таймаута и не имеет механизма прерывания по времени (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ❌ **[Logs Sdk]** [SHOULD] To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecord` be used for any concurrent processing, such as in a batching processor.  
  Нет рекомендации по клонированию logRecord для конкурентной обработки. Пакетный процессор (ОтелБазовыйПакетныйПроцессор) добавляет оригинал в буфер без клонирования, и нет документации о необходимости клонирования. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Асинхронная версия ЗакрытьАсинхронно() возвращает Обещание, позволяющее узнать результат. Однако синхронный метод Закрыть() является Процедурой (void) и не сообщает вызывающему об успехе/неудаче/таймауте. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:143-146`)

- ⚠️ **[Logs Sdk]** [SHOULD] In particular, if any `LogRecordProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all `LogRecord`s for which this was not already done and then invoke `ForceFlush` on it.  
  СброситьБуфер() вызывает ЭкспортироватьВсеПакеты(), который экспортирует все буферизованные записи через Экспортер.Экспортировать(). Однако после экспорта не вызывается Экспортер.СброситьБуфер() (ForceFlush экспортера). (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120-135`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Асинхронная версия СброситьБуферАсинхронно() возвращает Обещание. Однако синхронный метод СброситьБуфер() является Процедурой (void) и не возвращает результат. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:131-135`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Асинхронная версия СброситьБуферАсинхронно() возвращает Обещание с поддержкой таймаута через Получить(). Однако синхронный СброситьБуфер() блокирует до полного экспорта без таймаута. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:131-135`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() определена как Процедура (void) без возвращаемого значения. Вызывающий код не получает информацию об успехе, ошибке или таймауте. Провайдер предлагает асинхронный вариант СброситьБуферАсинхронно() через Promise, но сам интерфейс экспортера не возвращает результат. (`src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:19`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  ForceFlush (СброситьБуфер) не имеет собственного параметра таймаута и не прерывает выполнение по таймауту. Индивидуальные вызовы экспорта ограничены таймаутом транспорта (HTTP: 10с), но сама операция ForceFlush не имеет общего таймаута для прерывания. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41`)

- ⚠️ **[Metrics Api]** [SHOULD] Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying.  
  Дескриптор инструмента (ЗарегистрироватьДескриптор) хранит Вид, ЕдиницаИзмерения, Описание, Совет, но не хранит тип значения (int/double). Тип числа зашит внутри агрегатора при создании, но не участвует в идентификации инструмента при проверке конфликтов дескрипторов (ПроверитьКонфликтДескриптора). (`src/Метрики/Классы/ОтелМетр.os:553`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax.  
  Комментарии к методам создания инструментов описывают параметр Имя, но не упоминают требования к синтаксису имени инструмента (instrument name syntax) (`src/Метрики/Классы/ОтелМетр.os:36`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax.  
  Комментарии к асинхронным методам создания описывают параметр Имя, но не упоминают требования к синтаксису имени инструмента (`src/Метрики/Классы/ОтелМетр.os:215`)

- ⚠️ **[Metrics Api]** [SHOULD] Callback functions SHOULD be reentrant safe.  
  Рекомендация о reentrant safety callback не задокументирована для пользователей. SDK выполняет callback последовательно для каждого MetricReader (-)

- ⚠️ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT take an indefinite amount of time.  
  Рекомендация о времени выполнения callback не задокументирована для пользователей (-)

- ⚠️ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same `attributes`) across all registered callbacks.  
  Рекомендация о дублировании наблюдений не задокументирована для пользователей, дедупликация не реализована (-)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response.  
  Комментарий к методу Включен() описывает логику возврата, но не содержит рекомендации авторам инструментирования вызывать его перед каждым измерением (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:194`)

- ⚠️ **[Metrics Api]** [SHOULD NOT] This API SHOULD NOT validate this value, that is left to implementations of the API.  
  Метод Добавить() проверяет Значение < 0 и игнорирует отрицательные значения (строка 22-24), хотя спецификация рекомендует не валидировать на уровне API (`src/Метрики/Классы/ОтелСчетчик.os:22`)

- ⚠️ **[Metrics Api]** [SHOULD] If possible, this API SHOULD be structured so a user is obligated to provide this parameter.  
  В OneScript нет обязательных параметров на уровне языка - все параметры опциональные по умолчанию, но первый параметр Значение не имеет значения по умолчанию (`src/Метрики/Классы/ОтелГистограмма.os:20`)

- ⚠️ **[Metrics Api]** [SHOULD] If possible, this API SHOULD be structured so a user is obligated to provide this parameter.  
  В OneScript нет обязательных параметров на уровне языка - все параметры опциональные по умолчанию, но первый параметр Значение не имеет значения по умолчанию (`src/Метрики/Классы/ОтелДатчик.os:21`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Async version ЗакрытьАсинхронно() returns Promise but sync version Закрыть() does not return status (`src/Метрики/Классы/ОтелПровайдерМетрик.os:164`)

- ❌ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  No timeout mechanism implemented in shutdown methods (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Async version СброситьБуферАсинхронно() returns Promise but sync version СброситьБуфер() does not return status (`src/Метрики/Классы/ОтелПровайдерМетрик.os:152`)

- ❌ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status  
  СброситьБуфер() does not return any status - it is a void procedure (-)

- ❌ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  No timeout mechanism implemented in flush methods (-)

- ❌ **[Metrics Sdk]** [SHOULD] In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector that selects at most one instrument.  
  No validation exists to check whether a View with a name parameter selects at most one instrument. No warning or fast-fail is implemented. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] Additionally, implementations SHOULD support configuring an exclude-list of attribute keys.  
  ОтелПредставление has ИсключенныеКлючиАтрибутов field defined, but the exclude-list filtering is not applied during measurement collection - only the allow-list (РазрешенныеКлючиАтрибутов) is actually applied in ОтелБазовыйСинхронныйИнструмент. (`src/Метрики/Классы/ОтелПредставление.os:9`)

- ❌ **[Metrics Sdk]** [SHOULD] If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning.  
  No detection of conflicting metric identities from View application exists. Views are applied without checking for identity conflicts and no warning is emitted. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asynchronous instrument to use the Explicit bucket histogram aggregation) the implementation SHOULD emit a warning and proceed as if the View did not exist.  
  No validation exists for semantic incompatibility between View aggregation settings and instrument types. No warning is emitted for such cases. (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] Arithmetic sum of `Measurement` values in population. This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpDownCounter` or `ObservableGauge`).  
  Histogram aggregator always collects sum regardless of instrument type. No check exists to skip sum collection for instruments that record negative measurements. (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`, `min`, and `max` fields, because these values do not map into a valid bucket.  
  No special handling exists for non-normal IEEE floating point values (Inf, -Inf, NaN) in ОтелАгрегаторЭкспоненциальнойГистограммы. All values are incorporated into sum, min, and max without filtering. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale.  
  Initial scale is set to НачальнаяШкала (MaxScale, default 20), so first values use max scale. However, there is no explicit logic to return to max scale when the histogram has only one value after downscaling has occurred. (`src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:41`)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks.  
  No mechanism exists to detect or discard observations made on asynchronous instruments outside of registered callback invocations. (-)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback execution.  
  Callbacks are invoked synchronously without any timeout mechanism. An indefinitely blocking callback will block the entire collection cycle. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardinality_limit` value defined for the stream, that value SHOULD be used.  
  View class has ЛимитМощностиАгрегации property (line 18, getter line 92, setter line 112), but ПрименитьПредставлениеКИнструменту in ОтелМетр.os:515-537 does NOT apply the view cardinality limit to instruments - only attribute filters and exemplar reservoirs are applied (`src/Метрики/Классы/ОтелПредставление.os:92`)

- ❌ **[Metrics Sdk]** [SHOULD] If there is no matching view, but the `MetricReader` defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used.  
  ОтелПериодическийЧитательМетрик.os has no cardinality limit configuration at all - no default limit per instrument type (-)

- ❌ **[Metrics Sdk]** [SHOULD] Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality.  
  ОтелБазовыйНаблюдаемыйИнструмент.os has no cardinality limit logic at all - no overflow handling, no first-observed attribute preference, observations are converted directly to data points without cardinality restrictions (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible.  
  Warning includes conflicting instrument name and parameters (kind/unit), but does not include resolution guidance such as View configuration suggestions (`src/Метрики/Классы/ОтелМетр.os:573`)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning.  
  ПроверитьКонфликтДескриптора (line 562) does not check whether a View resolves the description conflict - Views are applied to instruments after duplicate detection, not during conflict resolution (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning.  
  The warning message (lines 573-577) does not include any View renaming recipe or View-related resolution guidance (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument registration.  
  A warning is emitted (line 572-577), but the SDK returns the first registered instrument instead of reporting both Metric objects - duplicate registrations always return the existing instrument, so only one Metric object is reported (`src/Метрики/Классы/ОтелМетр.os:54`)

- ❌ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax  
  No instrument name validation exists in ОтелМетр. The Meter accepts any string as instrument name without checking conformance to the instrument name syntax (e.g., allowed characters, length, pattern). The name is only lowercased via НРег() for duplicate detection. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name.  
  Since no name validation exists, no error is emitted for invalid instrument names. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided.  
  ПроверитьСовет() emits warnings via Лог.Предупреждение() for invalid advisory parameters (e.g., non-Structure type, non-Array boundaries). However, after the warning the invalid parameter is NOT discarded - it continues to be used as-is. The spec requires proceeding 'as if the parameter was not provided', but the code does not nullify invalid advisory parameters. (`src/Метрики/Классы/ОтелМетр.os:648`)

- ⚠️ **[Metrics Sdk]** [SHOULD] The "offer" method SHOULD have the ability to pull associated trace and span information without needing to record full context.  
  Trace/span context is extracted in ЗахватитьЭкземпляр before calling Предложить, but the reservoir itself does not pull context - it receives already-extracted КонтекстСпана as a parameter. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:333`)

- ⚠️ **[Metrics Sdk]** [SHOULD] Exemplars are expected to abide by the `AggregationTemporality` of any metric point they are recorded with. In other words, Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point.  
  The reservoir is cleared on ОчиститьТочкиДанных, but there is no explicit enforcement that exemplars fall within the start/stop timestamps of the data point. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138`)

- ⚠️ **[Metrics Sdk]** [SHOULD] The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars.  
  Implementation creates new Соответствие objects for each exemplar in СоздатьЭкземпляр; OneScript GC-managed allocations are unavoidable, no special allocation avoidance is implemented. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:80`)

- ⚠️ **[Metrics Sdk]** [SHOULD] This implementation ... SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled.  
  Implementation keeps the last seen measurement per bucket (always replaces) instead of using a uniformly-weighted sampling algorithm with a counter. Spec allows this as alternative (MAY keep last seen), but SHOULD prefers uniform sampling. (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СобратьИЭкспортировать is a Процедура (void return), does not return success/failure status to the caller. Errors are logged but not propagated. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:123`)

- ❌ **[Metrics Sdk]** [SHOULD] `Collect` SHOULD invoke Produce on registered MetricProducers.  
  There is no MetricProducer interface or registration mechanism. The reader collects only from SDK meters, not from external MetricProducers. (-)

- ❌ **[Metrics Sdk]** [SHOULD] SDKs SHOULD return some failure for these calls, if possible.  
  СброситьБуфер() (Collect) не проверяет флаг Закрыт и не возвращает ошибку при вызове после Закрыть(). Нет механизма отклонения Collect-вызовов после Shutdown. (-)

- ❌ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод Закрыть() является Процедурой (void), не возвращает результат. Вызывающий код не может узнать, успешно ли завершился shutdown или произошёл таймаут. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD collect metrics, call `Export(batch)` and `ForceFlush()` on the configured Push Metric Exporter.  
  СброситьБуфер() вызывает СобратьИЭкспортировать(), который собирает метрики и вызывает Экспортер.Экспортировать(). Однако не вызывается Экспортер.СброситьБуфер() (ForceFlush на экспортере), как требует спецификация. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71`)

- ❌ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() является Процедурой (void), не возвращает результат успеха/ошибки/таймаута. (-)

- ❌ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  СброситьБуфер() является Процедурой (void), не возвращает статус ERROR/NO ERROR. Ошибки перехватываются внутри СобратьИЭкспортировать и логируются, но не передаются вызывающему коду. (-)

- ❌ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  СброситьБуфер() вызывает СобратьИЭкспортировать() синхронно без таймаута. Операция может зависнуть при недоступности бэкенда (таймаут есть только на уровне HTTP-транспорта, но не на уровне читателя). (-)

- ❌ **[Metrics Sdk]** [SHOULD] Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsupported Aggregation or Aggregation Temporality, as this condition can be corrected by a change of `MetricReader` configuration.  
  ОтелЭкспортерМетрик.Экспортировать() не проверяет типы агрегации или временной агрегации на поддерживаемость. Данные принимаются без валидации, ошибка о неподдерживаемых агрегациях не генерируется. (-)

- ❌ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() в ОтелЭкспортерМетрик является Процедурой (void), не возвращает результат успеха/ошибки/таймаута вызывающему коду. (-)

- ❌ **[Metrics Sdk]** [SHOULD] `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of produced metrics.  
  MetricProducer не реализован, поэтому конфигурация AggregationTemporality для него отсутствует. (-)

- ⚠️ **[Otlp Exporter]** [SHOULD] The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default.  
  Протокол по умолчанию - http/json, а не рекомендуемый http/protobuf (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ⚠️ **[Otlp Exporter]** [SHOULD] SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them.  
  Поддерживается grpc (ОтелGrpcТранспорт) и http/json (ОтелHttpТранспорт), но http/protobuf не реализован - HTTP-транспорт отправляет только JSON (`src/Экспорт/Классы/ОтелGrpcТранспорт.os:1`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If they support only one, it SHOULD be `http/protobuf`.  
  Из двух обязательных (grpc и http/protobuf) поддерживается только grpc; http/protobuf не реализован (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If no configuration is provided the default transport SHOULD be `http/protobuf` unless SDKs have good reasons to choose `grpc` as the default (e.g., for backward compatibility reasons when `grpc` was already the default in a stable SDK release).  
  По умолчанию используется http/json, а не рекомендуемый http/protobuf (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ❌ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter.  
  User-Agent заголовок не устанавливается ни в HTTP-транспорте (ОтелHttpТранспорт), ни в gRPC-транспорте (ОтелGrpcТранспорт) (-)

- ❌ **[Otlp Exporter]** [SHOULD] The format of the header SHOULD follow RFC 7231.  
  User-Agent заголовок не реализован (-)

- ❌ **[Otlp Exporter]** [SHOULD] The resulting User-Agent SHOULD include the exporter's default User-Agent string.  
  User-Agent заголовок не реализован (-)

- ❌ **[Propagators]** [SHOULD] If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace Context Propagator and the Baggage `Propagator` specified in the Baggage API.  
  The SDK does not pre-configure propagators. ОтелГлобальный.ПолучитьПропагаторы() returns ОтелНоопПропагатор by default (line 132), not a composite of W3C TraceContext + Baggage. Both propagators exist as separate classes but are never assembled as a default composite. (-)

- ❌ **[Env Vars]** [SHOULD] If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied.  
  Функция Включено() (строка 561-564) не логирует предупреждение при получении невалидного значения булевой переменной (например 'yes', '1', 'on'). Значение молча интерпретируется как false без уведомления пользователя. (-)

- ⚠️ **[Env Vars]** [SHOULD] All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior.  
  Используется OTEL_ENABLED со значением по умолчанию 'true' (строка 562), вместо рекомендуемого спецификацией паттерна OTEL_SDK_DISABLED где false = безопасное поведение по умолчанию (SDK включен). Текущее именование инвертировано относительно рекомендации спецификации. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562`)

- ❌ **[Env Vars]** [SHOULD] For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them as not set.  
  Все числовые параметры парсятся через Число() без обработки ошибок (например строка 160: Число(Менеджер.Параметр("otel.exporter.otlp.timeout", "10"))). Если пользователь задаст невалидное значение (например 'abc'), вызов Число() выбросит исключение вместо генерации предупреждения и использования значения по умолчанию. (-)

- ⚠️ **[Env Vars]** [SHOULD] Enum values SHOULD be interpreted in a case-insensitive manner.  
  Пропагаторы обрабатываются case-insensitive через НРег (строка 344), как и boolean (строка 563) и exemplar filter (ОтелПостроительПровайдераМетрик.os:115). Однако OTEL_TRACES_SAMPLER (строка 197) и OTEL_*_EXPORTER (строки 177, 255, 291) сравниваются без приведения к нижнему регистру. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:344`)

## Детальный анализ по разделам (Stable)

### Context

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:130` |  |
| 2 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:127` |  |
| 3 | MUST | ✅ found | OpenTelemetry MUST provide its own `Context` implementation. | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

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
| 13 | MUST | ⚠️ partial | The API MUST accept the following parameters: * The `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:203` | Нет прямого Attach(Context) API, принимающего объект контекста. Методы УстановитьЗначение(Ключ, Значение), СделатьСпанТекущим(Спан), СделатьBaggageТекущим(Багаж) создают контекст внутри из key-value, а не принимают готовый Context как параметр. |
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
| 4 | MUST | ✅ found | Language API MUST treat both baggage names and values as case sensitive. | `src/Ядро/Классы/ОтелBaggage.os:3` |  |
| 5 | MUST | ✅ found | The Baggage API MUST be fully functional in the absence of an installed SDK. | `src/Ядро/Классы/ОтелBaggage.os:1` |  |
| 6 | MUST | ✅ found | The `Baggage` container MUST be immutable, so that the containing `Context` also remains immutable. | `src/Ядро/Классы/ОтелBaggage.os:154` |  |

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
| 11 | MUST | ✅ found | If an implementation of this API does not operate directly on the `Context`, it MUST provide the following functionality to interact with a `Context` instance: | `src/Ядро/Модули/ОтелКонтекст.os:156` |  |
| 12 | SHOULD NOT | ⚠️ partial | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:53` | Контекстный ключ КлючBaggage экспортируется через публичный метод КлючBaggage() в области ПрограммныйИнтерфейс, давая пользователям API прямой доступ к ключу контекста. Хотя удобные методы BaggageИзКонтекста/КонтекстСBaggage делают прямой доступ необязательным, ключ всё равно доступен. |
| 13 | SHOULD | ✅ found | If the language has support for implicitly propagated `Context` (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Классы/ОтелBaggage.os:16` |  |
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
| 16 | MUST | ✅ found | The API layer or an extension package MUST include the following `Propagator`s: | `src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:1` |  |

#### Conflict Resolution

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#conflict-resolution)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | If a new name/value pair is added and its name is the same as an existing name, then the new pair MUST take precedence. | `src/Ядро/Классы/ОтелПостроительBaggage.os:24` |  |

### Resource Sdk

#### Resource SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The SDK MUST allow for creation of `Resources` and for associating them with telemetry. | `src/Ядро/Классы/ОтелРесурс.os:94` |  |
| 2 | MUST | ✅ found | all `Span`s produced by any `Tracer` from the provider MUST be associated with this `Resource`. | `src/Трассировка/Классы/ОтелТрассировщик.os:83` |  |

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
| 5 | MUST | ✅ found | The interface MUST provide a way to create a new resource, from `Attributes`. | `src/Ядро/Классы/ОтелПостроительРесурса.os:61` |  |

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
| 9 | MUST | ⚠️ partial | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1` | Detectors exist (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) but are all within src/Ядро/Классы/ - inline in the SDK package, not in separate packages. |
| 10 | MUST | ✅ found | Resource detector packages MUST provide a method that returns a resource. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17` |  |
| 11 | MUST NOT | ✅ found | the failure to detect any resource information MUST NOT be considered an error, | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:23` |  |
| 12 | SHOULD | ⚠️ partial | whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:24` | Detection errors are caught and logged via Лог.Отладка() (debug level) instead of being treated as errors at error log level. |
| 13 | MUST | ❌ not_found | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions. | - | Detectors (host, process, cpu) populate known semconv attributes (host.name, os.type, process.pid) but create resources via Новый ОтелРесурс(Истина) with empty Schema URL. No Schema URL matching semantic conventions is ever set. |
| 14 | SHOULD | ⚠️ partial | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate (e.g. the detector that reads the attributes from environment values will not know what Schema URL to use). | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18` | All detectors use empty Schema URL including those that populate known semconv attributes (host.name, os.type, process.pid). Empty Schema URL is correct for unknown-attribute detectors but incorrect for detectors that populate known semconv attributes - they should set a proper Schema URL instead. |
| 15 | MUST | ⚠️ partial | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources. | `src/Ядро/Классы/ОтелРесурс.os:41` | The Слить() method detects Schema URL conflicts and returns an empty resource, but the detector combining in ЗаполнитьАтрибутыПоУмолчанию() copies attributes directly without using Слить() and does not check Schema URLs. Also no error is reported on conflict. |

#### Specifying resource information via an environment variable

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#specifying-resource-information-via-an-environment-variable)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge this, as the secondary resource, with any resource information provided by the user, i.e. the user provided resource information has higher priority. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:104` |  |
| 17 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:479` |  |
| 18 | MUST | ❌ not_found | The `,` and `=` characters in keys and values MUST be percent encoded. | - | РазобратьПарыКлючЗначение() splits by ',' and '=' but performs no percent-decoding. Values containing %2C or %3D will not be decoded back to ',' or '='. |
| 19 | SHOULD | ❌ not_found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded | - | No error handling exists for OTEL_RESOURCE_ATTRIBUTES parsing. Invalid pairs are silently skipped rather than discarding the entire value. |
| 20 | SHOULD | ❌ not_found | and an error SHOULD be reported following the Error Handling principles. | - | No error reporting for OTEL_RESOURCE_ATTRIBUTES parsing failures. No logging or exception is raised on malformed input. |

### Trace Api

#### TracerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default TracerProvider. | `src/Ядро/Модули/ОтелГлобальный.os:31` |  |
| 2 | SHOULD | ✅ found | Thus, implementations of TracerProvider SHOULD allow creating an arbitrary number of TracerProvider instances. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:244` |  |

#### TracerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The TracerProvider MUST provide the following functions: Get a Tracer | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |

#### Get a Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-a-tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 5 | SHOULD | ✅ found | This name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library (e.g. io.opentelemetry.contrib.mongodb), package, module or class name. | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:57` |  |
| 6 | MUST | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its name property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 7 | SHOULD | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its name property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:93` |  |
| 8 | SHOULD | ❌ not_found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its name property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | - | Нет логирования предупреждения при передаче пустого или невалидного имени в ПолучитьТрассировщик(). Код принимает любое имя без валидации и не выводит сообщение о невалидном значении. |
| 9 | MUST NOT | ✅ found | Implementations MUST NOT require users to repeatedly obtain a Tracer again with the same identity to pick up configuration changes. | `src/Трассировка/Классы/ОтелТрассировщик.os:80` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API MUST provide the following functionality to interact with a Context instance: | `src/Ядро/Модули/ОтелКонтекст.os:141` |  |
| 11 | SHOULD NOT | ⚠️ partial | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:44` | Ключ контекста для спана доступен публично через ОтелКонтекст.КлючСпана(). Хотя существуют удобные методы (СпанИзКонтекста, КонтекстСоСпаном), пользователи имеют прямой доступ к ключу. |
| 12 | SHOULD | ✅ found | If the language has support for implicitly propagated Context (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Модули/ОтелКонтекст.os:90` |  |
| 13 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### Tracer operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracer-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The Tracer MUST provide functions to: Create a new Span (see the section on Span) | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 15 | SHOULD | ✅ found | The Tracer SHOULD provide functions to: Report if Tracer is Enabled | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |

#### SpanContext

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spancontext)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The API MUST implement methods to create a SpanContext. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |
| 17 | SHOULD | ✅ found | These methods SHOULD be the only way to create a SpanContext. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |
| 18 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:1` |  |
| 19 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:1` |  |

#### Retrieving the TraceId and SpanId

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#retrieving-the-traceid-and-spanid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | The API MUST allow retrieving the `TraceId` and `SpanId` in the following forms: | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 21 | MUST | ✅ found | result MUST be a 32-hex-character lowercase string | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 22 | MUST | ✅ found | result MUST be a 16-hex-character lowercase string | `src/Трассировка/Классы/ОтелКонтекстСпана.os:32` |  |
| 23 | MUST | ✅ found | result MUST be a 16-byte array | `src/Трассировка/Классы/ОтелКонтекстСпана.os:82` |  |
| 24 | MUST | ✅ found | result MUST be an 8-byte array | `src/Трассировка/Классы/ОтелКонтекстСпана.os:91` |  |
| 25 | SHOULD NOT | ✅ found | The API SHOULD NOT expose details about how they are internally stored. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |

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
| 28 | MUST | ⚠️ partial | `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:60` | IsRemote method exists but the logic for propagated contexts vs child spans is handled during span creation, not explicitly in the IsRemote method itself |
| 29 | MUST | ⚠️ partial | When extracting a `SpanContext` through the Propagators API, `IsRemote` MUST return true | `src/Трассировка/Классы/ОтелКонтекстСпана.os:172` | The Удаленный flag is set during construction and can be set via УстановитьУдаленный, but the integration with Propagators API needs verification in propagation components |

#### TraceState

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracestate)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | Tracing API MUST provide at least the following operations on `TraceState`: | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:44` |  |
| 31 | MUST | ✅ found | These operations MUST follow the rules described in the W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:66` |  |
| 32 | MUST | ✅ found | All mutating operations MUST return a new `TraceState` with the modifications applied. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:92` |  |
| 33 | MUST | ✅ found | `TraceState` MUST at all times be valid according to rules specified in W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:227` |  |
| 34 | MUST | ✅ found | Every mutating operations MUST validate input parameters. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 35 | MUST NOT | ✅ found | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 36 | MUST | ✅ found | MUST follow the general error handling guidelines. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |

#### Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | SHOULD | ⚠️ partial | The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable. | `src/Трассировка/Классы/ОтелСпан.os:247` | Span name can be changed via ИзменитьИмя method, but there's no validation or guidance enforcement for naming conventions |
| 38 | SHOULD | ⚠️ partial | Generality SHOULD be prioritized over human-readability. | `src/Трассировка/Классы/ОтелСпан.os:247` | Implementation allows setting any name without enforcing generality vs readability guidelines |
| 39 | SHOULD | ✅ found | A `Span`'s start time SHOULD be set to the current time on span creation. | `src/Трассировка/Классы/ОтелТрассировщик.os:82` |  |
| 40 | SHOULD | ✅ found | After the `Span` is created, it SHOULD be possible to change its name, set its `Attribute`s, add `Event`s, and set the `Status`. | `src/Трассировка/Классы/ОтелСпан.os:247` |  |
| 41 | MUST NOT | ✅ found | These MUST NOT be changed after the `Span`'s end time has been set. | `src/Трассировка/Классы/ОтелСпан.os:248` |  |
| 42 | SHOULD NOT | ✅ found | implementations SHOULD NOT provide access to a `Span`'s attributes besides its `SpanContext`. | `src/Трассировка/Классы/ОтелСпан.os:134` |  |
| 43 | MUST NOT | ✅ found | alternative implementations MUST NOT allow callers to create `Span`s directly. | `src/Трассировка/Классы/ОтелТрассировщик.os:27` |  |
| 44 | MUST | ✅ found | All `Span`s MUST be created via a `Tracer`. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |

#### Span Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST NOT | ✅ found | There MUST NOT be any API for creating a `Span` other than with a `Tracer`. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 46 | MUST NOT | ⚠️ partial | `Span` creation MUST NOT set the newly created `Span` as the active `Span` in the current `Context` by default | `src/Трассировка/Классы/ОтелСпан.os:398` | Span creation doesn't set it as active by default, but the separate СделатьТекущим() method must be called explicitly |
| 47 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПостроительСпана.os:33` |  |
| 48 | MUST NOT | ✅ found | This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`. | `src/Трассировка/Классы/ОтелПостроительСпана.os:33` |  |
| 49 | MUST | ✅ found | The semantic parent of the Span MUST be determined according to the rules described in Determining the Parent Span from a Context. | `src/Трассировка/Классы/ОтелТрассировщик.os:57` |  |
| 50 | MUST | ✅ found | The API documentation MUST state that adding attributes at span creation is preferred to calling `SetAttribute` later | `src/Трассировка/Классы/ОтелПостроительСпана.os:66` |  |
| 51 | SHOULD | ✅ found | This argument SHOULD only be set when span creation time has already passed. | `src/Трассировка/Классы/ОтелПостроительСпана.os:109` |  |
| 52 | MUST NOT | ✅ found | If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument. | `src/Трассировка/Классы/ОтелПостроительСпана.os:109` |  |
| 53 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span | `src/Трассировка/Классы/ОтелПостроительСпана.os:45` |  |
| 54 | MUST | ✅ found | MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:107` |  |
| 55 | MUST | ✅ found | the `TraceId` MUST be the same as the parent. | `src/Трассировка/Классы/ОтелТрассировщик.os:140` |  |
| 56 | MUST | ✅ found | the child span MUST inherit all `TraceState` values of its parent by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:78` |  |
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
| 64 | SHOULD | ✅ found | This flag SHOULD be used to avoid expensive computations of a Span attributes or events in case when a Span is definitely not recorded. | `src/Трассировка/Классы/ОтелСпан.os:234` |  |

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
| 75 | MUST | ✅ found | `Description` MUST be IGNORED for `StatusCode` `Ok` & `Unset` values. | `src/Трассировка/Классы/ОтелСпан.os:431` |  |
| 76 | SHOULD | ✅ found | The status code SHOULD remain unset, except for the following circumstances: | `src/Трассировка/Классы/ОтелСпан.os:614` |  |
| 77 | SHOULD | ✅ found | An attempt to set value `Unset` SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:424` |  |
| 78 | SHOULD | ✅ found | When the status is set to `Error` by Instrumentation Libraries, the `Description` SHOULD be documented and predictable. | - |  |
| 79 | SHOULD | ✅ found | For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish their own conventions, including possible values of `Description` and what they mean. | - |  |
| 80 | SHOULD NOT | ✅ found | Generally, Instrumentation Libraries SHOULD NOT set the status code to `Ok`, unless explicitly configured to do so. | - |  |
| 81 | SHOULD | ✅ found | Instrumentation Libraries SHOULD leave the status code as `Unset` unless there is an error, as described above. | - |  |
| 82 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 83 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 84 | SHOULD | ✅ found | Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they would otherwise generate. | - |  |

#### End

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#end)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 85 | SHOULD | ✅ found | Implementations SHOULD ignore all subsequent calls to `End` and any other Span methods, i.e. the Span becomes non-recording by being ended. | `src/Трассировка/Классы/ОтелСпан.os:448` |  |
| 86 | MUST | ✅ found | However, all API implementations of such methods MUST internally call the `End` method and be documented to do so. | - |  |
| 87 | MUST NOT | ✅ found | `End` MUST NOT have any effects on child spans. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 88 | MUST NOT | ✅ found | `End` MUST NOT inactivate the `Span` in any `Context` it is active in. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 89 | MUST | ✅ found | It MUST still be possible to use an ended span as parent via a Context it is contained in. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
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
| 99 | MUST | ✅ found | Start and end time as well as Event's timestamps MUST be recorded at a time of a calling of corresponding API. | `src/Трассировка/Классы/ОтелСпан.os:609,450` |  |

#### Wrapping a SpanContext in a Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#wrapping-a-spancontext-in-a-span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 100 | MUST | ❌ not_found | The API MUST provide an operation for wrapping a `SpanContext` with an object implementing the `Span` interface. | - | No explicit wrapping operation found. The code creates spans from span contexts but doesn't expose a direct wrapping API. |
| 101 | SHOULD NOT | ❌ not_found | If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible | - | No wrapping functionality implemented to evaluate this requirement. |
| 102 | SHOULD | ❌ not_found | If a new type is required to be publicly exposed, it SHOULD be named `NonRecordingSpan`. | - | No NonRecordingSpan class found, only ОтелНоопСпан which serves a different purpose. |
| 103 | MUST | ⚠️ partial | `GetContext` MUST return the wrapped `SpanContext`. | `src/Трассировка/Классы/ОтелНоопСпан.os:29` | NoopSpan returns a context but it's not wrapped from an external SpanContext - it's internally generated. |
| 104 | MUST | ✅ found | `IsRecording` MUST return `false` to signal that events, attributes and other elements are not being recorded, i.e. they are being dropped. | `src/Трассировка/Классы/ОтелНоопСпан.os:67` |  |
| 105 | MUST | ✅ found | The remaining functionality of `Span` MUST be defined as no-op operations. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |
| 106 | MUST | ⚠️ partial | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | NoOp functionality exists but no SpanContext wrapping operation is implemented. |
| 107 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |

#### SpanKind

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 108 | SHOULD | ⚠️ partial | In order for `SpanKind` to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose. | `src/Трассировка/Модули/ОтелВидСпана.os:1` | SpanKind enum exists but there's no enforcement or guidance in the API to prevent spans serving multiple purposes. |
| 109 | SHOULD NOT | ⚠️ partial | For example, a server-side span SHOULD NOT be used to describe outgoing remote procedure call. | `src/Трассировка/Модули/ОтелВидСпана.os:1` | SpanKind enum exists but there's no enforcement or guidance in the API to prevent misuse. |

#### Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 110 | MUST | ✅ found | A user MUST have the ability to record links to other `SpanContext`s. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 111 | MUST | ✅ found | The API MUST provide: * An API to record a single `Link` where the `Link` properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 112 | SHOULD | ✅ found | Implementations SHOULD record links containing `SpanContext` with empty `TraceId` or `SpanId` (all zeros) as long as either the attribute set or `TraceState` is non-empty. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 113 | SHOULD | ✅ found | Span SHOULD preserve the order in which `Link`s are set. | `src/Трассировка/Классы/ОтелСпан.os:377` |  |
| 114 | MUST | ✅ found | The API documentation MUST state that adding links at span creation is preferred to calling `AddLink` later, for contexts that are available during span creation, because head sampling decisions can only consider information present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os:83` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 115 | MUST | ✅ found | TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:6` |  |
| 116 | MUST | ✅ found | Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:3` |  |
| 117 | MUST | ✅ found | Span - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:3` |  |
| 118 | MUST | ⚠️ partial | Event - Events are immutable and MUST be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСобытиеСпана.os:1` | Event class exists but no explicit documentation about immutability or thread safety. |
| 119 | SHOULD | ⚠️ partial | Link - Links are immutable and SHOULD be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:372` | Links are implemented as dictionaries but no explicit documentation about immutability or thread safety. |

#### Behavior of the API in the absence of an installed SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#behavior-of-the-api-in-the-absence-of-an-installed-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 120 | MUST | ⚠️ partial | The API MUST return a non-recording `Span` with the `SpanContext` in the parent `Context` (whether explicitly given or implicit current). | `src/Трассировка/Классы/ОтелТрассировщик.os:65` | Provider returns tracers when closed, but they don't properly propagate parent context - they create new tracers with no special no-op behavior. |
| 121 | SHOULD | ⚠️ partial | If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly without instantiating a new `Span`. | - | No specific logic to detect and return existing non-recording spans. |
| 122 | MUST | ⚠️ partial | If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.e., having a `SpanContext` with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags). | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | NoopSpan exists but when provider is closed, it still creates normal tracers rather than ensuring all spans are non-recording with empty contexts. |

### Trace Sdk

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, `Sampler`, and (Development) TracerConfigurator) MUST be owned by the `TracerProvider`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:9` | SpanProcessors, SpanLimits, Sampler и TracerConfigurator принадлежат TracerProvider, но IdGenerator отсутствует как конфигурируемый компонент - генерация ID реализована через статические утилиты ОтелУтилиты.СгенерироватьИдТрассировки(), а не как заменяемый генератор на провайдере |
| 2 | MUST | ✅ found | the updated configuration MUST also apply to all already returned `Tracers` | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |
| 3 | MUST NOT | ✅ found | it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvider` before or after the configuration change | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | `Shutdown` MUST be called only once for each `TracerProvider` instance. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:108` |  |
| 5 | SHOULD | ⚠️ partial | SDKs SHOULD return a valid no-op Tracer for these calls, if possible. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65` | После Закрыть() метод ПолучитьТрассировщик возвращает обычный ОтелТрассировщик (не ОтелНоопСпан-based), который продолжает пытаться создавать спаны через закрытые процессоры, вместо возврата настоящего no-op трассировщика |
| 6 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:132` | Синхронный метод Закрыть() - Процедура без возвращаемого значения. Асинхронный ЗакрытьАсинхронно() возвращает Обещание, через которое можно обнаружить ошибку, но основной метод не сигнализирует об успехе/неудаче |
| 7 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:132` | Синхронный Закрыть() не имеет механизма таймаута. Асинхронный ЗакрытьАсинхронно() возвращает Обещание, на котором вызывающая сторона может установить таймаут через Получить(timeout), но сам метод не контролирует таймаут |
| 8 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:111` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:121` | Синхронный СброситьБуфер() - Процедура без возвращаемого значения. Асинхронный СброситьБуферАсинхронно() возвращает Обещание для обнаружения ошибок, но основной метод не сигнализирует об успехе/неудаче |
| 10 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:121` | Синхронный СброситьБуфер() не имеет механизма таймаута. Асинхронный СброситьБуферАсинхронно() возвращает Обещание с возможностью таймаута через Получить(timeout), но сам метод не контролирует таймаут |
| 11 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered `SpanProcessors`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:99` |  |

#### Additional Span Interfaces

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#additional-span-interfaces)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | Readable span: A function receiving this as argument MUST be able to access all information that was added to the span, as listed in the API spec for Span. | `src/Трассировка/Классы/ОтелСпан.os:71` |  |
| 13 | MUST | ✅ found | A function receiving this as argument MUST be able to access the `InstrumentationScope` [since 1.10.0] and `Resource` information (implicitly) associated with the span. | `src/Трассировка/Классы/ОтелСпан.os:170` |  |
| 14 | MUST | ⚠️ partial | For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated since 1.10.0] having the same name and version values as the `InstrumentationScope`. | `src/Трассировка/Классы/ОтелСпан.os:170` | ОтелСпан exposes ОбластьИнструментирования() (InstrumentationScope) but there is no separate deprecated InstrumentationLibrary accessor. The same object is used, but there is no explicit backward-compatible alias. |
| 15 | MUST | ✅ found | A function receiving this as argument MUST be able to reliably determine whether the Span has ended (some languages might implement this by having an end timestamp of `null`, others might have an explicit `hasEnded` boolean). | `src/Трассировка/Классы/ОтелСпан.os:197` |  |
| 16 | MUST | ✅ found | Counts for attributes, events and links dropped due to collection limits MUST be available for exporters to report as described in the exporters specification. | `src/Трассировка/Классы/ОтелСпан.os:206` |  |
| 17 | MUST | ✅ found | As an exception to the authoritative set of span properties defined in the API spec, implementations MAY choose not to expose (and store) the full parent Context of the Span but they MUST expose at least the full parent SpanContext. | `src/Трассировка/Классы/ОтелСпан.os:89` |  |
| 18 | MUST | ✅ found | It MUST be possible for functions being called with this to somehow obtain the same `Span` instance and type that the span creation API returned (or will return) to the user (for example, the `Span` could be one of the parameters passed to such a function, or a getter could be provided). | `src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:18` |  |

#### Sampling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | Span Processor MUST receive only those spans which have this field set to `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:71` |  |
| 20 | SHOULD NOT | ✅ found | However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set. | `src/Трассировка/Классы/ОтелТрассировщик.os:213` |  |
| 21 | MUST | ✅ found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелТрассировщик.os:213` |  |
| 22 | SHOULD NOT | ✅ found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелТрассировщик.os:213` |  |
| 23 | MUST NOT | ✅ found | the OpenTelemetry SDK MUST NOT allow this combination. | `src/Трассировка/Классы/ОтелТрассировщик.os:71` |  |

#### SDK Span creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sdk-span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | When asked to create a Span, the SDK MUST act as if doing the following in order: If there is a valid parent trace ID, use it. Otherwise generate a new trace ID; Query the Sampler's ShouldSample method; Generate a new span ID for the Span, independently of the sampling decision; Create a span depending on the decision returned by ShouldSample. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |

#### ShouldSample

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shouldsample)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | If the parent `SpanContext` contains a valid `TraceId`, they MUST always match. | `src/Трассировка/Классы/ОтелТрассировщик.os:61` |  |
| 26 | MUST NOT | ✅ found | `RECORD_ONLY` - `IsRecording` will be `true`, but the `Sampled` flag MUST NOT be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:213` |  |
| 27 | MUST | ✅ found | `RECORD_AND_SAMPLE` - `IsRecording` will be `true` and the `Sampled` flag MUST be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:213` |  |
| 28 | SHOULD | ✅ found | If the sampler returns an empty `Tracestate` here, the `Tracestate` will be cleared, so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend to change it. | `src/Трассировка/Классы/ОтелТрассировщик.os:230` |  |

#### GetDescription

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#getdescription)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | SHOULD NOT | ❌ not_found | Callers SHOULD NOT cache the returned value. | - | This is a caller-side requirement about not caching the result of GetDescription. The implementation provides ОтелСэмплер.Описание() which returns a fresh string each time, but there is no enforcement or documentation warning callers not to cache. This is largely a usage guideline rather than an implementation requirement. |

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
| 32 | SHOULD | ✅ found | For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values. | `src/Ядро/Модули/ОтелУтилиты.os:85` |  |

#### Random trace flag

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#random-trace-flag)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | SHOULD | ❌ not_found | For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements. | - | The Random flag (bit 1, value 2) is never set in trace flags. ВычислитьФлагиТрассировки() in ОтелТрассировщик.os only returns 0 or 1 (Sampled flag), with no handling of the Random trace flag. |

#### Explicit randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#explicit-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | MUST NOT | ❌ not_found | SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value. | - | The sampler module does not handle the OpenTelemetry TraceState rv sub-key at all. There is no code to read, preserve, or avoid overwriting explicit randomness values in TraceState. The function returns a new result without any TraceState handling related to the rv sub-key. |

#### Presumption of TraceID randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#presumption-of-traceid-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | SHOULD | ⚠️ partial | For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the `rv` sub-key of the OpenTelemetry TraceState. | `src/Трассировка/Модули/ОтелСэмплер.os:275` | The TraceIdRatio sampler does use the TraceID for sampling decisions, effectively presuming randomness. However, there is no handling of the rv sub-key of the OpenTelemetry TraceState as an alternative source of randomness - the sampler always relies on TraceID randomness without checking for explicit randomness. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | SHOULD | ❌ not_found | If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated. | - | The SDK supports a custom IdGenerator via УстановитьГенераторИд(), but there is no mechanism for the custom IdGenerator to indicate whether it produces random TraceIDs. The Random flag (W3C Trace Context Level 2) is not exposed to or controlled by the IdGenerator extension. |

#### Span Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | MUST | ✅ found | Span attributes MUST adhere to the common rules of attribute limits. | `src/Трассировка/Классы/ОтелСпан.os:266` |  |
| 38 | MUST | ✅ found | If the SDK implements the limits above it MUST provide a way to change these limits, via a configuration to the TracerProvider, by allowing users to configure individual limits like in the Java example bellow. | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:79` |  |
| 39 | SHOULD | ⚠️ partial | The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:26` | The SDK uses names МаксСобытий (MaxEvents) and МаксЛинков (MaxLinks) instead of EventCountLimit and LinkCountLimit as recommended by the spec. Functionality is equivalent but naming convention differs. |
| 40 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `SpanLimits`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:1` |  |
| 41 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute, event, or link was discarded due to such a limit. | `src/Трассировка/Классы/ОтелСпан.os:470` |  |
| 42 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per discarded attribute, event, or link). | `src/Трассировка/Классы/ОтелСпан.os:469` |  |

#### Id Generators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#id-generators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST | ✅ found | The SDK MUST by default randomly generate both the `TraceId` and the `SpanId`. | `src/Ядро/Модули/ОтелУтилиты.os:78` |  |
| 44 | MUST | ✅ found | The SDK MUST provide a mechanism for customizing the way IDs are generated for both the `TraceId` and the `SpanId`. | `src/Ядро/Модули/ОтелУтилиты.os:63` |  |
| 45 | MUST | ⚠️ partial | The SDK MAY provide this functionality by allowing custom implementations of an interface like the java example below (name of the interface MAY be `IdGenerator`, name of the methods MUST be consistent with SpanContext), which provides extension points for two methods, one to generate a `SpanId` and one for `TraceId`. | `src/Ядро/Модули/ОтелУтилиты.os:63` | The IdGenerator is implemented as a duck-typed object passed to УстановитьГенераторИд(). Methods are named СгенерироватьИдТрассировки() and СгенерироватьИдСпана() which are consistent with SpanContext's ИдТрассировки/ИдСпана. However there is no formal interface class - it relies on duck typing. |
| 46 | MUST NOT | ✅ found | Additional `IdGenerator` implementing vendor-specific protocols such as AWS X-Ray trace id generator MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | - |  |

#### Span processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | MUST | ✅ found | SDK MUST allow to end each pipeline with individual exporter. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:83` |  |
| 48 | MUST | ✅ found | SDK MUST allow users to implement and configure custom processors. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:1` |  |

#### Interface definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | MUST | ✅ found | The `SpanProcessor` interface MUST declare the following methods: * OnStart* OnEnd* Shutdown* ForceFlush | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11` |  |
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
| 54 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `SpanProcessor` instance. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:61` |  |
| 55 | SHOULD | ⚠️ partial | After the call to `Shutdown`, subsequent calls to `OnStart`, `OnEnd`, or `ForceFlush` are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43` | Пакетный процессор проверяет флаг Закрыт в методе Обработать (OnEnd), но не проверяет в ПриНачале (OnStart) и СброситьБуфер (ForceFlush). Простой процессор не имеет флага Закрыт и не игнорирует вызовы после Закрыть() |
| 56 | SHOULD | ❌ not_found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Метод Закрыть() возвращает Void во всех реализациях процессоров спанов - нет способа сообщить вызывающему коду об успехе, ошибке или таймауте |
| 57 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:77` |  |
| 58 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192` | Пакетный процессор имеет таймаут для остановки фонового экспорта (ОстановитьФоновыйЭкспорт с ТаймаутЭкспортаМс), но ЭкспортироватьВсеПакеты() не ограничена таймаутом и может выполняться бесконечно. Простой процессор не имеет таймаута |

#### ForceFlush()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `Spans` for which the `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 60 | SHOULD | ⚠️ partial | In particular, if any `SpanProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all spans for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` | СброситьБуфер() вызывает ЭкспортироватьВсеПакеты(), который вызывает Экспортер.Экспортировать() для всех буферизированных спанов, но не вызывает Экспортер.СброситьБуфер() (ForceFlush экспортера) после экспорта |
| 61 | MUST | ⚠️ partial | The built-in SpanProcessors MUST do so. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` | Пакетный процессор экспортирует все буферизированные спаны через ЭкспортироватьВсеПакеты(), но не вызывает ForceFlush (СброситьБуфер) на экспортере после экспорта, как требует спецификация |
| 62 | MUST | ❌ not_found | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. | - | Метод СброситьБуфер() не принимает параметр таймаута. ЭкспортироватьВсеПакеты() выполняет цикл до полного опустошения буфера без возможности прерывания по таймауту |
| 63 | SHOULD | ❌ not_found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Метод СброситьБуфер() возвращает Void во всех реализациях процессоров спанов - нет способа сообщить вызывающему коду об успехе, ошибке или таймауте |
| 64 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `SpanProcessor` exports the completed spans. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 65 | SHOULD | ❌ not_found | `ForceFlush` SHOULD complete or abort within some timeout. | - | Метод СброситьБуфер() не имеет механизма таймаута. ЭкспортироватьВсеПакеты() в пакетном процессоре выполняет бесконечный цикл до полного опустошения буфера без ограничения по времени |

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
| 68 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:144` |  |
| 69 | SHOULD | ✅ found | The processor SHOULD export a batch when any of the following happens AND the previous export call has returned: | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:54` |  |

#### Span Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 70 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:5` |  |

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
| 73 | MUST | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:76` |  |
| 74 | SHOULD NOT | ✅ found | The default SDK's Span Processors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the spans are being sent to. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37` |  |

#### `ForceFlush()`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Spans` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` |  |
| 76 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` | СброситьБуфер() is a Процедура (void) - it does not return any status indicator (success, failure, or timeout) to the caller |
| 77 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed spans. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` |  |
| 78 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 79 | MUST | ✅ found | Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:6` |  |
| 80 | MUST | ✅ found | Sampler - `ShouldSample` and `GetDescription` MUST be safe to be called concurrently. | `src/Трассировка/Модули/ОтелСэмплер.os:140` |  |
| 81 | MUST | ✅ found | Span processor - all methods MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:41` |  |
| 82 | MUST | ⚠️ partial | Span Exporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:47` | Закрыт is a plain Булево, not АтомарноеБулево - concurrent Shutdown calls may have race conditions; compare with ОтелПровайдерТрассировки which uses АтомарноеБулево for its Закрыт flag |

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
| 7 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 8 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 9 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:82` |  |
| 10 | SHOULD | ➖ n_a | When only explicit Context is supported, this parameter SHOULD be required. | - | Реализация поддерживает неявный контекст через ОтелКонтекст.Текущий(), поэтому условие 'only explicit Context is supported' не выполняется. Требование условное и неприменимо к данной реализации. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when generating a `LogRecord`, a `Logger` SHOULD provide this `Enabled` API. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 12 | SHOULD | ✅ found | The API SHOULD accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 13 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 14 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:149` |  |
| 15 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 16 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response. | `src/Логирование/Классы/ОтелЛоггер.os:28` | Метод Включен() задокументирован (строки 28-41), но документация не содержит указания о том, что авторы инструментирования должны вызывать его каждый раз перед emit для получения актуального ответа. |

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
| 2 | MUST | ✅ found | A `LoggerProvider` MUST provide a way to allow a Resource to be specified. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:206` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the `LogRecord`s produced by any `Logger` from the `LoggerProvider`. | `src/Логирование/Классы/ОтелЛоггер.os:78` |  |

#### LoggerProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `LoggerProviders`s. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:60` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration (i.e. LogRecordProcessors and (Development) LoggerConfigurator) MUST be owned by the `LoggerProvider`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:12` |  |
| 6 | MUST | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained from the `LoggerProvider` before or after the configuration change). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:157` |  |
| 7 | MUST | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained from the `LoggerProvider` before or after the configuration change). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:157` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | `Shutdown` MUST be called only once for each `LoggerProvider` instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117` |  |
| 9 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op `Logger` for these calls, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:59` |  |
| 10 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:116` | Метод Закрыть() - процедура (void), не возвращает статус успеха/неуспеха/таймаута |
| 11 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:116` | Метод Закрыть() не принимает параметр таймаута и не имеет механизма прерывания по времени |
| 12 | MUST | ✅ found | `Shutdown` MUST be implemented by invoking `Shutdown` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:120` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | Метод СброситьБуфер() - процедура (void), не возвращает статус успеха/неуспеха/таймаута |
| 14 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | СброситьБуфер() не возвращает ERROR статус - является процедурой (void) |
| 15 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | СброситьБуфер() не возвращает NO ERROR статус - является процедурой (void) |
| 16 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | Метод СброситьБуфер() не принимает параметр таймаута и не имеет механизма прерывания по времени |
| 17 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:108` |  |

#### ReadableLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readablelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | A function receiving this as an argument MUST be able to access all the information added to the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:44` |  |
| 19 | MUST | ✅ found | It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) associated with the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:132` |  |
| 20 | MUST | ✅ found | The trace context fields MUST be populated from the resolved Context (either the explicitly passed Context or the current Context) when emitted. | `src/Логирование/Классы/ОтелЛоггер.os:81` |  |
| 21 | MUST | ✅ found | Counts for attributes due to collection limits MUST be available for exporters to report as described in the transformation to non-OTLP formats specification. | `src/Логирование/Классы/ОтелЗаписьЛога.os:150` |  |

#### ReadWriteLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readwritelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 22 | MUST | ✅ found | A function receiving this as an argument MUST additionally be able to modify the following information added to the LogRecord: Timestamp, ObservedTimestamp, SeverityText, SeverityNumber, Body, Attributes (addition, modification, removal), TraceId, SpanId, TraceFlags, EventName. | `src/Логирование/Классы/ОтелЗаписьЛога.os:179` |  |

#### LogRecord Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecord-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | MUST | ✅ found | LogRecord attributes MUST adhere to the common rules of attribute limits. | `src/Логирование/Классы/ОтелЗаписьЛога.os:235` |  |
| 24 | MUST | ✅ found | If the SDK implements attribute limits it MUST provide a way to change these limits, via a configuration to the LoggerProvider, by allowing users to configure individual limits like in the Java example below. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:39` |  |
| 25 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called LogRecordLimits. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:1` |  |
| 26 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute was discarded due to such a limit. | `src/Логирование/Классы/ОтелЗаписьЛога.os:384` |  |
| 27 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per LogRecord (i.e., not per discarded attribute). | `src/Логирование/Классы/ОтелЗаписьЛога.os:385` |  |

#### LogRecordProcessor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | The SDK MUST allow each pipeline to end with an individual exporter. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:66` |  |
| 29 | MUST | ✅ found | The SDK MUST allow users to implement and configure custom processors and decorate built-in processors for advanced scenarios such as enriching with attributes. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:1` |  |

#### OnEmit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#onemit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | SHOULD NOT | ✅ found | This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD NOT block or throw exceptions. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:19-23` |  |
| 31 | MUST | ✅ found | For a `LogRecordProcessor` registered directly on SDK `LoggerProvider`, the `logRecord` mutations MUST be visible in next registered processors. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17-24` |  |
| 32 | SHOULD | ❌ not_found | To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecord` be used for any concurrent processing, such as in a batching processor. | - | Нет рекомендации по клонированию logRecord для конкурентной обработки. Пакетный процессор (ОтелБазовыйПакетныйПроцессор) добавляет оригинал в буфер без клонирования, и нет документации о необходимости клонирования. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | MUST NOT | ❌ not_found | Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller. | - | LogRecordProcessor не реализует операцию Enabled. Интерфейс ИнтерфейсПроцессорЛогов не содержит метода Enabled. Фильтрация реализована на уровне ОтелЛоггер.Включен(), а не на уровне процессора. |

#### ShutDown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117` |  |
| 35 | SHOULD | ✅ found | After the call to `Shutdown`, subsequent calls to `OnEmit` are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Логирование/Классы/ОтелЛоггер.os:106` |  |
| 36 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:143-146` | Асинхронная версия ЗакрытьАсинхронно() возвращает Обещание, позволяющее узнать результат. Однако синхронный метод Закрыть() является Процедурой (void) и не сообщает вызывающему об успехе/неудаче/таймауте. |
| 37 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:74-81` |  |
| 38 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:190-198` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 39 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `LogRecord`s for which the `LogRecordProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68-70` |  |
| 40 | SHOULD | ⚠️ partial | In particular, if any `LogRecordProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all `LogRecord`s for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120-135` | СброситьБуфер() вызывает ЭкспортироватьВсеПакеты(), который экспортирует все буферизованные записи через Экспортер.Экспортировать(). Однако после экспорта не вызывается Экспортер.СброситьБуфер() (ForceFlush экспортера). |
| 41 | MUST | ⚠️ partial | The built-in LogRecordProcessors MUST do so. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68-70` | Встроенные процессоры экспортируют все буферизованные записи, но не вызывают ForceFlush на экспортере после экспорта, как требует предыдущее предложение. |
| 42 | MUST | ❌ not_found | If a timeout is specified (see below), the `LogRecordProcessor` MUST prioritize honoring the timeout over finishing all calls. | - | Метод СброситьБуфер() не принимает параметр таймаута. Нет механизма приоритизации таймаута над завершением всех вызовов экспорта в ForceFlush. |
| 43 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:131-135` | Асинхронная версия СброситьБуферАсинхронно() возвращает Обещание. Однако синхронный метод СброситьБуфер() является Процедурой (void) и не возвращает результат. |
| 44 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `LogRecordProcessor` exports the emitted `LogRecord`s. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107-111` |  |
| 45 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:131-135` | Асинхронная версия СброситьБуферАсинхронно() возвращает Обещание с поддержкой таймаута через Получить(). Однако синхронный СброситьБуфер() блокирует до полного экспорта без таймаута. |

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
| 49 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:144-153` |  |

#### LogRecordExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 50 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:3-4` |  |

#### LogRecordExporter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 51 | MUST | ✅ found | A `LogRecordExporter` MUST support the following functions: | `src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:13` |  |

#### Export

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#export)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 52 | MUST NOT | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 53 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:149` |  |
| 54 | SHOULD NOT | ✅ found | The default SDK's `LogRecordProcessors` SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the logs are being sent to. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:24` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD | ✅ found | This is a hint to ensure that the export of any `ReadableLogRecords` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41` |  |
| 56 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:19` | СброситьБуфер() определена как Процедура (void) без возвращаемого значения. Вызывающий код не получает информацию об успехе, ошибке или таймауте. Провайдер предлагает асинхронный вариант СброситьБуферАсинхронно() через Promise, но сам интерфейс экспортера не возвращает результат. |
| 57 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the `ReadlableLogRecords`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` |  |
| 58 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41` | ForceFlush (СброситьБуфер) не имеет собственного параметра таймаута и не прерывает выполнение по таймауту. Индивидуальные вызовы экспорта ограничены таймаутом транспорта (HTTP: 10с), но сама операция ForceFlush не имеет общего таймаута для прерывания. |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each `LogRecordExporter` instance. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47` |  |
| 60 | SHOULD | ✅ found | After the call to `Shutdown` subsequent calls to `Export` are not allowed and SHOULD return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:26` |  |
| 61 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 62 | MUST | ✅ found | LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:224` |  |
| 63 | MUST | ✅ found | Logger - all methods MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 64 | MUST | ⚠️ partial | LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:3` | Код экспортера содержит комментарий о необходимости потокобезопасности (строка 3-4), но переменная Закрыт - обычный Булево без атомарной защиты (не АтомарноеБулево). В отличие от ОтелПровайдерЛогирования, который использует АтомарноеБулево и СинхронизированнаяКарта, экспортер не использует примитивы синхронизации для флага Закрыт. |

### Metrics Api

#### MeterProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default MeterProvider. | `src/Ядро/Модули/ОтелГлобальный.os:31` |  |

#### MeterProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The MeterProvider MUST provide the following functions: Get a Meter | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |

#### Get a Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#get-a-meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 4 | MUST NOT | ✅ found | Users can provide a version, but it is up to their discretion. Therefore, this API needs to be structured to accept a version, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:54` |  |
| 5 | MUST NOT | ✅ found | Users can provide a schema_url, but it is up to their discretion. Therefore, this API needs to be structured to accept a schema_url, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:56` |  |
| 6 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:55` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ found | Meter SHOULD NOT be responsible for the configuration. This should be the responsibility of the MeterProvider instead. | `src/Метрики/Классы/ОтелМетр.os:1` |  |

#### Meter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The Meter MUST provide functions to create new Instruments: | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Instrument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ⚠️ partial | Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying. | `src/Метрики/Классы/ОтелМетр.os:553` | Дескриптор инструмента (ЗарегистрироватьДескриптор) хранит Вид, ЕдиницаИзмерения, Описание, Совет, но не хранит тип значения (int/double). Тип числа зашит внутри агрегатора при создании, но не участвует в идентификации инструмента при проверке конфликтов дескрипторов (ПроверитьКонфликтДескриптора). |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | SHOULD | ✅ found | The API SHOULD treat it as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:257` |  |
| 11 | MUST | ✅ found | It MUST be case-sensitive (e.g. kb and kB are different units), ASCII string. | `src/Метрики/Классы/ОтелМетр.os:568` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST treat it as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:57` |  |
| 13 | MUST | ✅ found | It MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or `utf8mb3`). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:10` |  |
| 14 | MUST | ✅ found | It MUST support at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:10` |  |

#### Synchronous and Asynchronous instruments

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#synchronous-and-asynchronous-instruments)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The API to construct synchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 16 | SHOULD | ✅ found | If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 17 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:36` |  |
| 18 | SHOULD | ⚠️ partial | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:36` | Комментарии к методам создания инструментов описывают параметр Имя, но не упоминают требования к синтаксису имени инструмента (instrument name syntax) |
| 19 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`; that is left to implementations of the API, like the SDK. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 20 | MUST NOT | ✅ found | this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 21 | MUST | ✅ found | the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:13` |  |
| 22 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 23 | MUST NOT | ✅ found | this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 24 | MUST | ✅ found | the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:11` |  |
| 25 | MUST NOT | ✅ found | this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 26 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 27 | MUST | ✅ found | The API to construct asynchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 28 | SHOULD | ✅ found | If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 29 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:215` |  |
| 30 | SHOULD | ⚠️ partial | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:215` | Комментарии к асинхронным методам создания описывают параметр Имя, но не упоминают требования к синтаксису имени инструмента |
| 31 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`, that is left to implementations of the API. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 32 | MUST NOT | ✅ found | this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 33 | MUST | ✅ found | the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:12` |  |
| 34 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 35 | MUST NOT | ✅ found | this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 36 | MUST | ✅ found | the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:10` |  |
| 37 | MUST NOT | ✅ found | this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 38 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 39 | MUST | ⚠️ partial | Therefore, this API MUST be structured to accept a variable number of `callback` functions, including none. | `src/Метрики/Классы/ОтелМетр.os:229` | API создания асинхронных инструментов принимает 0 или 1 callback через параметр Callback = Неопределено. Переменное количество callback не поддерживается при создании - дополнительные добавляются через ДобавитьCallback() после создания |
| 40 | MUST | ⚠️ partial | The API MUST support creation of asynchronous instruments by passing zero or more `callback` functions to be permanently registered to the newly created instrument. | `src/Метрики/Классы/ОтелМетр.os:229` | При создании можно передать 0 или 1 callback. Передача более одного callback при создании не поддерживается - нужно использовать ДобавитьCallback() после создания |
| 41 | SHOULD | ✅ found | The API SHOULD support registration of `callback` functions associated with asynchronous instruments after they are created. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:58` |  |
| 42 | MUST | ✅ found | the user MUST be able to undo registration of the specific callback after its registration by some means. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:69` |  |
| 43 | MUST | ✅ found | Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:163` |  |
| 44 | MUST | ⚠️ partial | Callback functions MUST be documented as follows for the end user: | `src/Метрики/Классы/ОтелНаблюдениеМетрики.os:56` | Комментарии в ОтелНаблюдениеМетрики описывают использование callback, но не документируют три рекомендации (reentrant safe, не бесконечное время, не дублировать наблюдения) |
| 45 | SHOULD | ⚠️ partial | Callback functions SHOULD be reentrant safe. | - | Рекомендация о reentrant safety callback не задокументирована для пользователей. SDK выполняет callback последовательно для каждого MetricReader |
| 46 | SHOULD NOT | ⚠️ partial | Callback functions SHOULD NOT take an indefinite amount of time. | - | Рекомендация о времени выполнения callback не задокументирована для пользователей |
| 47 | SHOULD NOT | ⚠️ partial | Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same `attributes`) across all registered callbacks. | - | Рекомендация о дублировании наблюдений не задокументирована для пользователей, дедупликация не реализована |
| 48 | MUST | ✅ found | Callbacks registered at the time of instrument creation MUST apply to the single instruments which is under construction. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:154` |  |
| 49 | MUST | ✅ found | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the instrument associated with each observed `Measurement` value. | `src/Метрики/Классы/ОтелМетр.os:440` |  |
| 50 | MUST | ✅ found | Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of asynchronous instruments from the same `Meter` instance. | `src/Метрики/Классы/ОтелМетр.os:428` |  |
| 51 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` |  |
| 52 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:184` |  |
| 53 | SHOULD | ✅ found | The API SHOULD provide some way to pass `state` to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147` |  |

#### General operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | SHOULD | ✅ found | All synchronous instruments SHOULD provide functions to: | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD | ✅ found | synchronous instruments SHOULD provide this `Enabled` API. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 56 | MUST | ✅ found | the API MUST be structured in a way for parameters to be added. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 57 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:202` |  |
| 58 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:194` | Комментарий к методу Включен() описывает логику возврата, но не содержит рекомендации авторам инструментирования вызывать его перед каждым измерением |

#### Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | MUST NOT | ✅ found | There MUST NOT be any API for creating a `Counter` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Counter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 61 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 62 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 63 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелСчетчик.os:13` |  |
| 64 | SHOULD | ✅ found | This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелСчетчик.os:17` |  |
| 65 | SHOULD NOT | ⚠️ partial | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелСчетчик.os:22` | Метод Добавить() проверяет Значение < 0 и игнорирует отрицательные значения (строка 22-24), хотя спецификация рекомендует не валидировать на уровне API |
| 66 | MUST | ✅ found | this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 67 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |

#### Asynchronous Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Counter other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 69 | MAY | ✅ found | This MAY be called CreateObservableCounter. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 70 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:1` |  |
| 71 | MUST | ✅ found | observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:1` |  |
| 72 | SHOULD | ✅ found | The API SHOULD provide some way to pass state to the callback. | `src/Метрики/Классы/ОтелМетр.os:229` |  |

#### Histogram creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#histogram-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Histogram other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:80` |  |

#### Histogram operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#histogram-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 74 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example null, undefined). | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 75 | MAY | ✅ found | (it MAY return a dummy value if required by certain programming languages or systems, for example null, undefined). | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 76 | MUST | ✅ found | This API MUST accept the following parameter: A numeric value to record. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 77 | SHOULD | ⚠️ partial | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелГистограмма.os:20` | В OneScript нет обязательных параметров на уровне языка - все параметры опциональные по умолчанию, но первый параметр Значение не имеет значения по умолчанию |
| 78 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелГистограмма.os:16` |  |
| 79 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:78` |  |
| 80 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |

#### Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 81 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Gauge other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:194` |  |

#### Gauge operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 82 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example null, undefined). | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 83 | MUST | ✅ found | This API MUST accept the following parameter: A numeric value. The current absolute value. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 84 | SHOULD | ⚠️ partial | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелДатчик.os:21` | В OneScript нет обязательных параметров на уровне языка - все параметры опциональные по умолчанию, но первый параметр Значение не имеет значения по умолчанию |
| 85 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелДатчик.os:17` |  |
| 86 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 87 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:78` |  |

#### Asynchronous Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 88 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Gauge other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:308` |  |

#### UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | MUST NOT | ✅ found | There MUST NOT be any API for creating an UpDownCounter other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:162` |  |

#### UpDownCounter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 91 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 92 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 93 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:13-19` |  |
| 94 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |

#### Asynchronous UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 95 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:268` |  |

#### Multiple-instrument callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#multiple-instrument-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: | `src/Метрики/Классы/ОтелМетр.os:428` |  |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | SHOULD | ✅ found | All the metrics components SHOULD allow new APIs to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелМетр.os:35` |  |
| 98 | SHOULD | ✅ found | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 99 | MUST | ⚠️ partial | MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:241` | Реализация потокобезопасна (СинхронизированнаяКарта для кэша метрик), но методы не документированы явно как safe for concurrent use. |
| 100 | MUST | ⚠️ partial | Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелМетр.os:493` | Реализация потокобезопасна (СинхронизированнаяКарта, АтомарноеБулево), но методы не документированы явно как safe for concurrent use. |
| 101 | MUST | ⚠️ partial | Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:261` | Реализация потокобезопасна (СинхронизированнаяКарта для аккумуляторов, АтомарноеБулево для флагов), но методы не документированы явно как safe for concurrent use. |

### Metrics Sdk

#### Metrics SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metrics-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Ядро/Классы/ОтелSdk.os:177` |  |

#### MeterProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A `MeterProvider` MUST provide a way to allow a Resource to be specified. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:24` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the metrics produced by any `Meter` from the `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:68` |  |

#### MeterProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `MeterProvider`s. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:103` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration (i.e. MetricExporters, MetricReaders, Views, and (Development) MeterConfigurator) MUST be owned by the `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:22` |  |
| 6 | MUST | ⚠️ partial | updated configuration MUST also apply to all already returned `Meters` | `src/Метрики/Классы/ОтелПровайдерМетрик.os:71` | Configuration is applied only at Meter creation time. No dynamic configuration update mechanism for existing Meters is implemented. |
| 7 | MUST NOT | ❌ not_found | it MUST NOT matter whether a `Meter` was obtained from the `MeterProvider` before or after the configuration change | - | No configuration change mechanism exists - configuration is only applied at creation time |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ⚠️ partial | `Shutdown` MUST be called only once for each `MeterProvider` instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` | Закрыть() method sets Закрыт flag but does not prevent multiple calls - no guard against repeated shutdown |
| 9 | SHOULD | ✅ found | After the call to `Shutdown`, subsequent attempts to get a `Meter` are not allowed. SDKs SHOULD return a valid no-op Meter for these calls, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:57` |  |
| 10 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:164` | Async version ЗакрытьАсинхронно() returns Promise but sync version Закрыть() does not return status |
| 11 | SHOULD | ❌ not_found | `Shutdown` SHOULD complete or abort within some timeout. | - | No timeout mechanism implemented in shutdown methods |
| 12 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered MetricReader and MetricExporter instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:137` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered MetricReader instances that implement `ForceFlush`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` |  |
| 14 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:152` | Async version СброситьБуферАсинхронно() returns Promise but sync version СброситьБуфер() does not return status |
| 15 | SHOULD | ❌ not_found | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status | - | СброситьБуфер() does not return any status - it is a void procedure |
| 16 | SHOULD | ❌ not_found | `ForceFlush` SHOULD complete or abort within some timeout. | - | No timeout mechanism implemented in flush methods |

#### View

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | The SDK MUST provide functionality for a user to create Views for a `MeterProvider`. | `src/Метрики/Классы/ОтелПредставление.os:1` |  |
| 18 | MUST | ✅ found | This functionality MUST accept as inputs the Instrument selection criteria and the resulting stream configuration. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:53` |  |
| 19 | MUST | ✅ found | The SDK MUST provide the means to register Views with a `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:176` |  |

#### Instrument selection criteria

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-selection-criteria)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | Criteria SHOULD be treated as additive. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37` |  |
| 21 | MUST | ✅ found | The SDK MUST accept the following criteria: | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 22 | MUST | ✅ found | If the SDK does not support wildcards in general, it MUST still recognize the special single asterisk (`*`) character as matching all Instruments. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37` |  |
| 23 | MUST NOT | ✅ found | Users can provide a `name`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 24 | MUST NOT | ✅ found | Users can provide a `type`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `type`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 25 | MUST NOT | ✅ found | Users can provide a `unit`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 26 | MUST NOT | ✅ found | Users can provide a `meter_name`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 27 | MUST NOT | ✅ found | Users can provide a `meter_version`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 28 | MUST NOT | ✅ found | Users can provide a `meter_schema_url`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 29 | MUST NOT | ✅ found | Users can provide these additional criteria the SDK accepts, but it is up to their discretion. Therefore, the instrument selection criteria can be structured to accept the criteria, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |

#### Stream configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#stream-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | The SDK MUST accept the following stream configuration parameters: | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 31 | SHOULD | ✅ found | `name`: The metric stream name that SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:211` |  |
| 32 | SHOULD | ❌ not_found | In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector that selects at most one instrument. | - | No validation exists to check whether a View with a name parameter selects at most one instrument. No warning or fast-fail is implemented. |
| 33 | MUST NOT | ✅ found | Users can provide a `name`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:157` |  |
| 34 | MUST | ✅ found | If the user does not provide a `name` value, name from the Instrument the View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:211` |  |
| 35 | SHOULD | ✅ found | `description`: The metric stream description that SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:214` |  |
| 36 | MUST NOT | ✅ found | Users can provide a `description`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:158` |  |
| 37 | MUST | ✅ found | If the user does not provide a `description` value, the description from the Instrument a View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:214` |  |
| 38 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:291` |  |
| 39 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:291` |  |
| 40 | MUST NOT | ✅ found | Users can provide `attribute_keys`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept `attribute_keys`, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелПредставление.os:159` |  |
| 41 | SHOULD | ✅ found | If the user does not provide any value, the SDK SHOULD use the `Attributes` advisory parameter configured on the instrument instead. | `src/Метрики/Классы/ОтелМетр.os:527` |  |
| 42 | MUST | ✅ found | If the `Attributes` advisory parameter is absent, all attributes MUST be kept. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:84` |  |
| 43 | SHOULD | ⚠️ partial | Additionally, implementations SHOULD support configuring an exclude-list of attribute keys. | `src/Метрики/Классы/ОтелПредставление.os:9` | ОтелПредставление has ИсключенныеКлючиАтрибутов field defined, but the exclude-list filtering is not applied during measurement collection - only the allow-list (РазрешенныеКлючиАтрибутов) is actually applied in ОтелБазовыйСинхронныйИнструмент. |
| 44 | MUST | ❌ not_found | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | - | Exclude-list field exists in ОтелПредставление (ИсключенныеКлючиАтрибутов) but the actual exclusion filtering is not implemented in the measurement pipeline. |
| 45 | MUST | ❌ not_found | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | - | Exclude-list field exists in ОтелПредставление (ИсключенныеКлючиАтрибутов) but the keep-remaining logic for excluded attributes is not implemented. |
| 46 | MUST NOT | ✅ found | Users can provide an `aggregation`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept an `aggregation`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:161` |  |
| 47 | MUST | ⚠️ partial | If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance. | `src/Метрики/Классы/ОтелМетр.os:58` | Default aggregation is applied per instrument type (Sum for Counter, Histogram for Histogram, LastValue for Gauge). However, the aggregation is not configurable per MetricReader instance - all readers share the same aggregation strategy set at instrument creation time. |
| 48 | MUST NOT | ✅ found | Users can provide an `exemplar_reservoir`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept an `exemplar_reservoir`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:163` |  |
| 49 | MUST | ✅ found | If the user does not provide an `exemplar_reservoir` value, the `MeterProvider` MUST apply a default exemplar reservoir. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |
| 50 | MUST NOT | ✅ found | Users can provide an `aggregation_cardinality_limit`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept an `aggregation_cardinality_limit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:164` |  |
| 51 | MUST | ⚠️ partial | If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST apply the default aggregation cardinality limit the `MetricReader` is configured with. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` | A default cardinality limit of 2000 is applied per instrument, but it is hardcoded in ОтелБазовыйСинхронныйИнструмент rather than being configurable on the MetricReader instance as the spec requires. |

#### Measurement processing

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#measurement-processing)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 52 | SHOULD | ✅ found | The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument: | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:173` |  |
| 53 | MUST | ✅ found | Instrument advisory parameters, if any, MUST be honored. | `src/Метрики/Классы/ОтелМетр.os:527` |  |
| 54 | SHOULD | ❌ not_found | If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning. | - | No detection of conflicting metric identities from View application exists. Views are applied without checking for identity conflicts and no warning is emitted. |
| 55 | SHOULD | ❌ not_found | If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asynchronous instrument to use the Explicit bucket histogram aggregation) the implementation SHOULD emit a warning and proceed as if the View did not exist. | - | No validation exists for semantic incompatibility between View aggregation settings and instrument types. No warning is emitted for such cases. |
| 56 | MUST | ✅ found | If both a View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:524` |  |
| 57 | SHOULD | ✅ found | If the Instrument could not match with any of the registered `View`(s), the SDK SHOULD enable the instrument using the default aggregation and temporality. | `src/Метрики/Классы/ОтелМетр.os:58` |  |

#### Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 58 | MUST | ✅ found | The SDK MUST provide the following `Aggregation` to support the Metric Points in the Metrics Data Model. | `src/Метрики/Модули/ОтелАгрегация.os:1` |  |
| 59 | SHOULD | ✅ found | The SDK SHOULD provide the following `Aggregation`: Base2 Exponential Bucket Histogram | `src/Метрики/Модули/ОтелАгрегация.os:76` |  |

#### Histogram Aggregations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#histogram-aggregations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | SHOULD NOT | ❌ not_found | Arithmetic sum of `Measurement` values in population. This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpDownCounter` or `ObservableGauge`). | - | Histogram aggregator always collects sum regardless of instrument type. No check exists to skip sum collection for instruments that record negative measurements. |
| 61 | SHOULD | ✅ found | SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different (e.g. for backward compatibility reasons in a stable SDK release). | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:118` |  |
| 62 | SHOULD NOT | ❌ not_found | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`, `min`, and `max` fields, because these values do not map into a valid bucket. | - | No special handling exists for non-normal IEEE floating point values (Inf, -Inf, NaN) in ОтелАгрегаторЭкспоненциальнойГистограммы. All values are incorporated into sum, min, and max without filtering. |
| 63 | MUST | ✅ found | The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic scale parameter will not exceed. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:302` |  |
| 64 | SHOULD | ⚠️ partial | When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:41` | Initial scale is set to НачальнаяШкала (MaxScale, default 20), so first values use max scale. However, there is no explicit logic to return to max scale when the histogram has only one value after downscaling has occurred. |
| 65 | SHOULD | ✅ found | Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possible, within the constraint of maximum size (max number of buckets). | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:157` |  |

#### Observations inside asynchronous callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#observations-inside-asynchronous-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | MUST | ⚠️ partial | Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that observations made or produced by executing callbacks only apply to the intended `MetricReader` during collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:140` | Callbacks are invoked during each reader's collection cycle, but observations go into the instrument's shared state (ВнешниеНаблюдения on ОтелБазовыйНаблюдаемыйИнструмент). Multiple readers share the same instrument state, so observations are not truly isolated per MetricReader. |
| 67 | SHOULD | ❌ not_found | The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks. | - | No mechanism exists to detect or discard observations made on asynchronous instruments outside of registered callback invocations. |
| 68 | SHOULD | ❌ not_found | The implementation SHOULD use a timeout to prevent indefinite callback execution. | - | Callbacks are invoked synchronously without any timeout mechanism. An indefinitely blocking callback will block the entire collection cycle. |
| 69 | MUST | ✅ found | The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:140` |  |
| 70 | SHOULD NOT | ✅ found | The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:174` |  |

#### Cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | SHOULD | ✅ found | SDKs SHOULD support being configured with a cardinality limit. | `src/Метрики/Классы/ОтелМетр.os:418` |  |
| 72 | SHOULD | ✅ found | Cardinality limit enforcement SHOULD occur after attribute filtering, if any. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:84` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | SHOULD | ⚠️ partial | A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardinality_limit` value defined for the stream, that value SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:92` | View class has ЛимитМощностиАгрегации property (line 18, getter line 92, setter line 112), but ПрименитьПредставлениеКИнструменту in ОтелМетр.os:515-537 does NOT apply the view cardinality limit to instruments - only attribute filters and exemplar reservoirs are applied |
| 74 | SHOULD | ❌ not_found | If there is no matching view, but the `MetricReader` defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | - | ОтелПериодическийЧитательМетрик.os has no cardinality limit configuration at all - no default limit per instrument type |
| 75 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелМетр.os:500` |  |

#### Overflow attribute

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#overflow-attribute)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 76 | MUST | ⚠️ partial | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:325` | Overflow aggregator with otel.metric.overflow=true attribute is created lazily on first overflow (line 92: Если Аккумуляторы.Количество() >= ЛимитМощности), not prior to reaching the limit. The overflow bucket is not pre-allocated, so total accumulators can exceed the configured limit by 1 |
| 77 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:92` |  |

#### Synchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#synchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | MUST | ✅ found | Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141` |  |
| 79 | MUST | ✅ found | Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in exactly one Aggregator, which is either an Aggregator associated with the correct attribute set or an aggregator associated with the overflow attribute set. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:90` |  |
| 80 | MUST NOT | ✅ found | Measurements MUST NOT be double-counted or dropped during an overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:105` |  |

#### Asynchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#asynchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 81 | SHOULD | ❌ not_found | Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality. | - | ОтелБазовыйНаблюдаемыйИнструмент.os has no cardinality limit logic at all - no overflow handling, no first-observed attribute preference, observations are converted directly to data points without cardinality restrictions |

#### Duplicate instrument registration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#duplicate-instrument-registration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 82 | MUST | ✅ found | This means that the Meter MUST return a functional instrument that can be expected to export data even if this will cause semantic error in the data model. | `src/Метрики/Классы/ОтелМетр.os:54` |  |
| 83 | SHOULD | ✅ found | Therefore, when a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted. | `src/Метрики/Классы/ОтелМетр.os:572` |  |
| 84 | SHOULD | ⚠️ partial | The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible. | `src/Метрики/Классы/ОтелМетр.os:573` | Warning includes conflicting instrument name and parameters (kind/unit), but does not include resolution guidance such as View configuration suggestions |
| 85 | SHOULD | ❌ not_found | If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning. | - | ПроверитьКонфликтДескриптора (line 562) does not check whether a View resolves the description conflict - Views are applied to instruments after duplicate detection, not during conflict resolution |
| 86 | SHOULD | ❌ not_found | If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning. | - | The warning message (lines 573-577) does not include any View renaming recipe or View-related resolution guidance |
| 87 | SHOULD | ⚠️ partial | Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument registration. | `src/Метрики/Классы/ОтелМетр.os:54` | A warning is emitted (line 572-577), but the SDK returns the first registered instrument instead of reporting both Metric objects - duplicate registrations always return the existing instrument, so only one Metric object is reported |
| 88 | MUST | ✅ found | the SDK MUST aggregate data from identical Instruments together in its export pipeline. | `src/Метрики/Классы/ОтелМетр.os:51` |  |

#### Name conflict

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#name-conflict)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | MUST | ⚠️ partial | When this happens, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above. | `src/Метрики/Классы/ОтелМетр.os:51` | Meter returns the first-seen instrument correctly (name normalized via НРег, lookup by lowercase key returns original). However, ПроверитьКонфликтДескриптора (line 562) only logs a warning when instrument parameters (kind/unit/description/advisory) differ. For pure case-different duplicates with identical parameters, no log/error is emitted, violating the 'log an appropriate error' part of the requirement. |

#### Instrument name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | SHOULD | ❌ not_found | When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax | - | No instrument name validation exists in ОтелМетр. The Meter accepts any string as instrument name without checking conformance to the instrument name syntax (e.g., allowed characters, length, pattern). The name is only lowercased via НРег() for duplicate detection. |
| 91 | SHOULD | ❌ not_found | If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name. | - | Since no name validation exists, no error is emitted for invalid instrument names. |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 92 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 93 | MUST | ⚠️ partial | If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit string. | `src/Метрики/Классы/ОтелМетр.os:48` | The 'not provided' case is handled by the default parameter value ЕдиницаИзмерения = "". However, if Неопределено (null) is passed explicitly, it is stored as Неопределено without coercion to empty string. No explicit null-to-empty conversion exists in the instrument creation methods. |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 94 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument description. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 95 | MUST | ⚠️ partial | If a description is not provided or the description is null, the Meter MUST treat it the same as an empty description string. | `src/Метрики/Классы/ОтелМетр.os:48` | The 'not provided' case is handled by the default parameter value Описание = "". However, if Неопределено (null) is passed explicitly, it is stored as Неопределено without coercion to empty string. No explicit null-to-empty conversion exists in the instrument creation methods. |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | SHOULD | ✅ found | When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:642` |  |
| 97 | SHOULD | ⚠️ partial | If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided. | `src/Метрики/Классы/ОтелМетр.os:648` | ПроверитьСовет() emits warnings via Лог.Предупреждение() for invalid advisory parameters (e.g., non-Structure type, non-Array boundaries). However, after the warning the invalid parameter is NOT discarded - it continues to be used as-is. The spec requires proceeding 'as if the parameter was not provided', but the code does not nullify invalid advisory parameters. |
| 98 | MUST | ✅ found | If multiple identical Instruments are created with different advisory parameters, the Meter MUST return an instrument using the first-seen advisory parameters and log an appropriate error as described in duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:562` |  |
| 99 | MUST | ✅ found | If both a View and advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:539` |  |

#### Instrument advisory parameter: `ExplicitBucketBoundaries`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameter-explicitbucketboundaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 100 | MUST | ✅ found | If no View matches, or if a matching View selects the default aggregation, the `ExplicitBucketBoundaries` advisory parameter MUST be used. | `src/Метрики/Классы/ОтелМетр.os:539` |  |

#### Exemplar

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 101 | MUST | ✅ found | A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements via the `ExemplarFilter` and `ExemplarReservoir` hooks. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:7` |  |
| 102 | SHOULD | ✅ found | `Exemplar` sampling SHOULD be turned on by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:264` |  |
| 103 | MUST NOT | ✅ found | If `Exemplar` sampling is off, the SDK MUST NOT have overhead related to exemplar sampling. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:335` |  |
| 104 | MUST | ✅ found | A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation. | `src/Метрики/Классы/ОтелМетр.os:99` |  |
| 105 | SHOULD | ✅ found | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: * `ExemplarFilter`: filter which measurements can become exemplars. * `ExemplarReservoir`: storage and sampling of exemplars. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |

#### ExemplarFilter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarfilter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 106 | MUST | ✅ found | The `ExemplarFilter` configuration MUST allow users to select between one of the built-in ExemplarFilters. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 107 | SHOULD | ✅ found | The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for an SDK. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 108 | SHOULD | ✅ found | The default value SHOULD be `TraceBased`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:245` |  |
| 109 | SHOULD | ✅ found | The filter configuration SHOULD follow the environment variable specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:109` |  |
| 110 | MUST | ✅ found | An OpenTelemetry SDK MUST support the following filters: AlwaysOn, AlwaysOff, TraceBased. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14` |  |

#### ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 111 | MUST | ✅ found | The `ExemplarReservoir` interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 112 | MUST | ✅ found | A new `ExemplarReservoir` MUST be created for every known timeseries data point, as determined by aggregation and view configuration. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |
| 113 | SHOULD | ✅ found | The "offer" method SHOULD accept measurements, including: The `value` of the measurement, the complete set of `Attributes` of the measurement, the Context of the measurement, a `timestamp` that best represents when the measurement was taken. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 114 | SHOULD | ⚠️ partial | The "offer" method SHOULD have the ability to pull associated trace and span information without needing to record full context. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:333` | Trace/span context is extracted in ЗахватитьЭкземпляр before calling Предложить, but the reservoir itself does not pull context - it receives already-extracted КонтекстСпана as a parameter. |
| 115 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the "offer" method. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 116 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the "offer" method. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 117 | MUST | ✅ found | The "collect" method MUST return accumulated `Exemplar`s. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:55` |  |
| 118 | SHOULD | ⚠️ partial | Exemplars are expected to abide by the `AggregationTemporality` of any metric point they are recorded with. In other words, Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138` | The reservoir is cleared on ОчиститьТочкиДанных, but there is no explicit enforcement that exemplars fall within the start/stop timestamps of the data point. |
| 119 | MUST | ✅ found | `Exemplar`s MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:130` |  |
| 120 | SHOULD | ⚠️ partial | The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:80` | Implementation creates new Соответствие objects for each exemplar in СоздатьЭкземпляр; OneScript GC-managed allocations are unavoidable, no special allocation avoidance is implemented. |

#### Exemplar defaults

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar-defaults)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 121 | MUST | ✅ found | The SDK MUST include two types of built-in exemplar reservoirs: `SimpleFixedSizeExemplarReservoir`, `AlignedHistogramBucketExemplarReservoir`. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1` |  |
| 122 | SHOULD | ✅ found | Explicit bucket histogram aggregation with more than 1 bucket SHOULD use `AlignedHistogramBucketExemplarReservoir`. | `src/Метрики/Классы/ОтелМетр.os:99` |  |
| 123 | SHOULD | ✅ found | Base2 Exponential Histogram Aggregation SHOULD use a `SimpleFixedSizeExemplarReservoir` with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty (e.g. `min(20, max_buckets)`). | `src/Метрики/Классы/ОтелМетр.os:137` |  |
| 124 | SHOULD | ✅ found | All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |

#### SimpleFixedSizeExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#simplefixedsizeexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 125 | MUST | ✅ found | This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the reservoir has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:80` |  |
| 126 | SHOULD | ✅ found | Any stateful portion of sampling computation SHOULD be reset every collection cycle. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:64` |  |
| 127 | SHOULD | ✅ found | Otherwise, a default size of `1` SHOULD be used. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:165` |  |

#### AlignedHistogramBucketExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#alignedhistogrambucketexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 128 | MUST | ✅ found | This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:158` |  |
| 129 | MUST | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50` |  |
| 130 | SHOULD | ⚠️ partial | This implementation ... SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50` | Implementation keeps the last seen measurement per bucket (always replaces) instead of using a uniformly-weighted sampling algorithm with a counter. Spec allows this as alternative (MAY keep last seen), but SHOULD prefers uniform sampling. |
| 131 | SHOULD | ✅ found | This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:158` |  |

#### Custom ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#custom-exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 132 | MUST | ✅ found | The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation. | `src/Метрики/Классы/ОтелПредставление.os:83` |  |
| 133 | MUST | ✅ found | This extension MUST be configurable on a metric View. | `src/Метрики/Классы/ОтелПредставление.os:163` |  |
| 134 | MUST | ✅ found | although individual reservoirs MUST still be instantiated per metric-timeseries. | `src/Метрики/Классы/ОтелМетр.os:534` |  |

#### Collect

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#collect)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 135 | SHOULD | ⚠️ partial | `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:123` | СобратьИЭкспортировать is a Процедура (void return), does not return success/failure status to the caller. Errors are logged but not propagated. |
| 136 | SHOULD | ❌ not_found | `Collect` SHOULD invoke Produce on registered MetricProducers. | - | There is no MetricProducer interface or registration mechanism. The reader collects only from SDK meters, not from external MetricProducers. |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 137 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MetricReader` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:89` |  |
| 138 | SHOULD | ❌ not_found | SDKs SHOULD return some failure for these calls, if possible. | - | СброситьБуфер() (Collect) не проверяет флаг Закрыт и не возвращает ошибку при вызове после Закрыть(). Нет механизма отклонения Collect-вызовов после Shutdown. |
| 139 | SHOULD | ❌ not_found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Метод Закрыть() является Процедурой (void), не возвращает результат. Вызывающий код не может узнать, успешно ли завершился shutdown или произошёл таймаут. |
| 140 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` |  |

#### Periodic exporting MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 141 | MUST | ⚠️ partial | The reader MUST synchronize calls to `MetricExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:124` | БлокировкаРесурса (lock) используется только для потокобезопасного копирования массива Метров (строка 124-135), но сам вызов Экспортер.Экспортировать() (строка 154) находится вне блокировки. При одновременном вызове ПериодическийСбор (фоновое задание) и СброситьБуфер (основной поток) возможен конкурентный вызов Export. |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 142 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD collect metrics, call `Export(batch)` and `ForceFlush()` on the configured Push Metric Exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` | СброситьБуфер() вызывает СобратьИЭкспортировать(), который собирает метрики и вызывает Экспортер.Экспортировать(). Однако не вызывается Экспортер.СброситьБуфер() (ForceFlush на экспортере), как требует спецификация. |
| 143 | SHOULD | ❌ not_found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | СброситьБуфер() является Процедурой (void), не возвращает результат успеха/ошибки/таймаута. |
| 144 | SHOULD | ❌ not_found | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | - | СброситьБуфер() является Процедурой (void), не возвращает статус ERROR/NO ERROR. Ошибки перехватываются внутри СобратьИЭкспортировать и логируются, но не передаются вызывающему коду. |
| 145 | SHOULD | ❌ not_found | `ForceFlush` SHOULD complete or abort within some timeout. | - | СброситьБуфер() вызывает СобратьИЭкспортировать() синхронно без таймаута. Операция может зависнуть при недоступности бэкенда (таймаут есть только на уровне HTTP-транспорта, но не на уровне читателя). |

#### MetricExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 146 | MUST | ✅ found | `MetricExporter` defines the interface that protocol-specific exporters MUST implement so that they can be plugged into OpenTelemetry SDK and support sending of telemetry data. | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1` |  |
| 147 | SHOULD | ❌ not_found | Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsupported Aggregation or Aggregation Temporality, as this condition can be corrected by a change of `MetricReader` configuration. | - | ОтелЭкспортерМетрик.Экспортировать() не проверяет типы агрегации или временной агрегации на поддерживаемость. Данные принимаются без валидации, ошибка о неподдерживаемых агрегациях не генерируется. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 148 | MUST | ✅ found | A Push Metric Exporter MUST support the following functions: | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1` |  |
| 149 | MUST | ✅ found | The SDK MUST provide a way for the exporter to get the Meter information (e.g. name, version, etc.) associated with each `Metric Point`. | `src/Метрики/Классы/ОтелДанныеМетрики.os:42` |  |
| 150 | MUST NOT | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 151 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 152 | SHOULD NOT | ✅ found | The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the metrics are being sent to. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25` |  |
| 153 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Metrics` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` |  |
| 154 | SHOULD | ❌ not_found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | СброситьБуфер() в ОтелЭкспортерМетрик является Процедурой (void), не возвращает результат успеха/ошибки/таймаута вызывающему коду. |
| 155 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed metrics. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` |  |
| 156 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` |  |
| 157 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each `MetricExporter` instance. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` |  |
| 158 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` |  |

#### MetricProducer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricproducer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 159 | MUST | ❌ not_found | `MetricProducer` defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data. | - | Интерфейс MetricProducer не реализован. Нет отдельного класса или интерфейса для подключения сторонних источников метрик к MetricReader. |
| 160 | SHOULD | ❌ not_found | `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of produced metrics. | - | MetricProducer не реализован, поэтому конфигурация AggregationTemporality для него отсутствует. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 161 | MUST | ❌ not_found | A `MetricProducer` MUST support the following functions: | - | MetricProducer не реализован как отдельный интерфейс или класс. Функции Produce не существует. |

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
| 164 | MUST | ❌ not_found | The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry. | - | Нет явного кода обработки числовых пределов (overflow, underflow) в метрическом SDK. Агрегаторы и инструменты не содержат проверок на выход за пределы числовых типов. |
| 165 | MUST | ❌ not_found | If the SDK receives float/double values from Instruments, it MUST handle all the possible values. | - | Нет явной обработки NaN и Infinity в агрегаторах метрик. Код принимает значения от инструментов без проверки на специальные значения IEEE 754 (NaN, +Infinity, -Infinity). |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 166 | SHOULD | ✅ found | All the metrics components SHOULD allow new methods to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 167 | SHOULD | ✅ found | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to existing methods without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:231` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 168 | MUST | ⚠️ partial | MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:241` | Meter creation использует СинхронизированнаяКарта (потокобезопасно). Однако ForceFlush (СброситьБуфер) и Shutdown (Закрыть) итерируют массив ЧитателиМетрик без блокировки, а флаг Закрыт - обычный Булево, не АтомарноеБулево. |
| 169 | MUST | ⚠️ partial | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:167` | Используется СинхронизированнаяКарта для Данные и Счетчики, АтомарноеЧисло для счетчиков измерений. Однако операции с внутренним Массивом экземпляров (Добавить, присваивание по индексу) в методе ДобавитьВРезервуар не синхронизированы - возможна гонка при конкурентных вызовах Предложить для одного КлючАтрибутов. |
| 170 | MUST | ✅ found | MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:12` |  |
| 171 | MUST | ⚠️ partial | MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:3` | Комментарий в коде признает необходимость конкурентной безопасности, но реализация не использует ни БлокировкаРесурса, ни АтомарноеБулево. Флаг Закрыт - обычный Булево без синхронизации. ForceFlush (СброситьБуфер) - пустой метод (inherently safe), но Shutdown и Export имеют гонку данных на флаге Закрыт. |

### Otlp Exporter

#### Configuration Options

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#configuration-options)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | The following configuration options MUST be available to configure the OTLP exporter. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130` | Endpoint, Protocol, Headers, Compression, Timeout доступны через env vars; Certificate File, Client key file, Client certificate file, Insecure не реализованы (TLS/mTLS - ограничение платформы OneScript) |
| 2 | MUST | ❌ not_found | Each configuration option MUST be overridable by a signal specific option. | - | Per-signal переменные окружения (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_TRACES_HEADERS и т.д.) не поддерживаются; все сигналы используют общую конфигурацию |
| 3 | MUST | ✅ found | The implementation MUST honor the following URL components: | `src/Экспорт/Классы/ОтелHttpТранспорт.os:104` |  |
| 4 | MUST | ✅ found | When using `OTEL_EXPORTER_OTLP_ENDPOINT`, exporters MUST construct per-signal URLs as described below. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:35` |  |
| 5 | SHOULD | ✅ found | The option SHOULD accept any form allowed by the underlying gRPC client implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:147` |  |
| 6 | MUST | ✅ found | Additionally, the option MUST accept a URL with a scheme of either `http` or `https`. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:174` |  |
| 7 | SHOULD | ✅ found | If the gRPC client implementation does not support an endpoint with a scheme of `http` or `https` then the endpoint SHOULD be transformed to the most sensible format for that implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:174` |  |
| 8 | MUST | ⚠️ partial | Options MUST be one of: `grpc`, `http/protobuf`, `http/json`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Код принимает grpc и http/json, но http/protobuf не реализован полноценно - HTTP-транспорт всегда отправляет JSON; валидация допустимых значений протокола отсутствует |
| 9 | SHOULD | ✅ found | SDKs SHOULD default endpoint variables to use `http` scheme unless they have good reasons to choose `https` scheme for the default (e.g., for backward compatibility reasons in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:158` |  |
| 10 | SHOULD | ➖ n_a | However, if they are already implemented, they SHOULD continue to be supported as they were part of a stable release of the specification. | - | OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE относятся к TLS-конфигурации (Insecure), которая является ограничением платформы OneScript; эти переменные никогда не были реализованы в SDK |
| 11 | SHOULD | ⚠️ partial | The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Протокол по умолчанию - http/json, а не рекомендуемый http/protobuf |

#### Endpoint URLs for OTLP/HTTP

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#endpoint-urls-for-otlphttp)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ⚠️ partial | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal as follow: | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:35` | URL конструируются из базового OTEL_EXPORTER_OTLP_ENDPOINT + относительные пути (/v1/traces, /v1/logs, /v1/metrics), но per-signal endpoint переменные (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT и т.д.) не поддерживаются |
| 13 | MUST | ❌ not_found | For the per-signal variables (`OTEL_EXPORTER_OTLP_<signal>_ENDPOINT`), the URL MUST be used as-is without any modification. | - | Per-signal endpoint переменные (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_ENDPOINT, OTEL_EXPORTER_OTLP_LOGS_ENDPOINT) не поддерживаются |
| 14 | MUST | ❌ not_found | The only exception is that if an URL contains no path part, the root path `/` MUST be used (see Example 2). | - | Per-signal endpoint переменные не поддерживаются, поэтому обработка пустого пути для per-signal URL не реализована |
| 15 | MUST NOT | ✅ found | An SDK MUST NOT modify the URL in ways other than specified above. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:99` |  |

#### Specify Protocol

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specify-protocol)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ⚠️ partial | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:1` | Поддерживается grpc (ОтелGrpcТранспорт) и http/json (ОтелHttpТранспорт), но http/protobuf не реализован - HTTP-транспорт отправляет только JSON |
| 17 | MUST | ✅ found | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:1` |  |
| 18 | SHOULD | ⚠️ partial | If they support only one, it SHOULD be `http/protobuf`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Из двух обязательных (grpc и http/protobuf) поддерживается только grpc; http/protobuf не реализован |
| 19 | SHOULD | ⚠️ partial | If no configuration is provided the default transport SHOULD be `http/protobuf` unless SDKs have good reasons to choose `grpc` as the default (e.g., for backward compatibility reasons when `grpc` was already the default in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | По умолчанию используется http/json, а не рекомендуемый http/protobuf |

#### Specifying headers via environment variables

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:479` |  |

#### Retry

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#retry)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | Transient errors MUST be handled with a retry strategy. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:76` |  |
| 22 | MUST | ✅ found | This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:167` |  |

#### User Agent

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#user-agent)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | SHOULD | ❌ not_found | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter. | - | User-Agent заголовок не устанавливается ни в HTTP-транспорте (ОтелHttpТранспорт), ни в gRPC-транспорте (ОтелGrpcТранспорт) |
| 24 | SHOULD | ❌ not_found | The format of the header SHOULD follow RFC 7231. | - | User-Agent заголовок не реализован |
| 25 | SHOULD | ❌ not_found | The resulting User-Agent SHOULD include the exporter's default User-Agent string. | - | User-Agent заголовок не реализован |

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
| 4 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any previously existing valid value. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:90` |  |
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
| 14 | SHOULD | ✅ found | It SHOULD return them in the same order as they appear in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40` |  |
| 15 | SHOULD | ✅ found | If the key doesn't exist, it SHOULD return an empty collection. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:41` |  |
| 16 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:44` |  |

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
| 22 | SHOULD | ❌ not_found | If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace Context Propagator and the Baggage `Propagator` specified in the Baggage API. | - | The SDK does not pre-configure propagators. ОтелГлобальный.ПолучитьПропагаторы() returns ОтелНоопПропагатор by default (line 132), not a composite of W3C TraceContext + Baggage. Both propagators exist as separate classes but are never assembled as a default composite. |
| 23 | MUST | ✅ found | These platforms MUST also allow pre-configured propagators to be disabled or overridden. | `src/Ядро/Модули/ОтелГлобальный.os:110` |  |

#### Get Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#get-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | This method MUST exist for each supported Propagator type. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |

#### Set Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#set-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | This method MUST exist for each supported Propagator type. | `src/Ядро/Модули/ОтелГлобальный.os:110` |  |

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
| 2 | SHOULD | ✅ found | They SHOULD also follow the common configuration specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:81` |  |

#### Implementation guidelines

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#implementation-guidelines)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The environment-based configuration MUST have a direct code configuration equivalent. | `src/Ядро/Классы/ОтелПостроительSdk.os:24` |  |

#### Parsing empty value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#parsing-empty-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ⚠️ partial | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105` | Некоторые параметры проверяют пустую строку (строки 105, 137, 398, 411, 439, 447 через '<> ""'), но параметры использующие значение по умолчанию в Менеджер.Параметр(ключ, умолчание) не обрабатывают пустую строку как неустановленное значение - пустая строка обходит значение по умолчанию (например строки 150, 160, 177, 255, 291, 562) |

#### Boolean

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#boolean)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Any value that represents a Boolean MUST be set to true only by the case-insensitive string "true", meaning "True" or "TRUE" are also accepted, as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 6 | MUST NOT | ✅ found | An implementation MUST NOT extend this definition and define additional values that are interpreted as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 7 | MUST | ✅ found | Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 8 | SHOULD | ❌ not_found | If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied. | - | Функция Включено() (строка 561-564) не логирует предупреждение при получении невалидного значения булевой переменной (например 'yes', '1', 'on'). Значение молча интерпретируется как false без уведомления пользователя. |
| 9 | SHOULD | ⚠️ partial | All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562` | Используется OTEL_ENABLED со значением по умолчанию 'true' (строка 562), вместо рекомендуемого спецификацией паттерна OTEL_SDK_DISABLED где false = безопасное поведение по умолчанию (SDK включен). Текущее именование инвертировано относительно рекомендации спецификации. |
| 10 | MUST NOT | ✅ found | Renaming or changing the default value MUST NOT happen without a major version upgrade. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562` |  |

#### Numeric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#numeric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | The following paragraph was added after stabilization and the requirements are thus qualified as "SHOULD" to allow implementations to avoid breaking changes. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:160` |  |
| 12 | MUST | ❌ not_found | For new implementations, these should be treated as MUST requirements. | - | Как новая реализация, код должен обрабатывать числовые значения на уровне MUST (предупреждение + graceful ignore), но вызовы Число() (строки 160, 204, 215, 224-227, 263-266, 312, 399, 401, 412, 414, 440, 448) не обёрнуты в Попытка/Исключение, не генерируют предупреждений и не обрабатывают невалидные значения gracefully. |
| 13 | SHOULD | ❌ not_found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them as not set. | - | Все числовые параметры парсятся через Число() без обработки ошибок (например строка 160: Число(Менеджер.Параметр("otel.exporter.otlp.timeout", "10"))). Если пользователь задаст невалидное значение (например 'abc'), вызов Число() выбросит исключение вместо генерации предупреждения и использования значения по умолчанию. |

#### Enum

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#enum)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | SHOULD | ⚠️ partial | Enum values SHOULD be interpreted in a case-insensitive manner. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:344` | Пропагаторы обрабатываются case-insensitive через НРег (строка 344), как и boolean (строка 563) и exemplar filter (ОтелПостроительПровайдераМетрик.os:115). Однако OTEL_TRACES_SAMPLER (строка 197) и OTEL_*_EXPORTER (строки 177, 255, 291) сравниваются без приведения к нижнему регистру. |
| 15 | MUST | ⚠️ partial | For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:373` | Для пропагаторов выводится предупреждение через Сообщить (строка 373) и значение пропускается. Но для OTEL_TRACES_SAMPLER (строка 216) нераспознанное значение молча заменяется на parentbased_always_on без предупреждения. Для OTEL_METRICS_EXEMPLAR_FILTER (ОтелПостроительПровайдераМетрик.os:123) нераспознанное значение игнорируется без предупреждения. |

#### General SDK Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ❌ not_found | Values MUST be deduplicated in order to register a `Propagator` only once. | - | В СоздатьПропагаторы (ОтелАвтоконфигурация.os:336-378) список пропагаторов разбирается через СтрРазделить, но дедупликация не выполняется. Если пользователь укажет 'tracecontext,tracecontext', будут созданы два экземпляра ОтелW3CПропагатор. |
| 17 | MUST | ❌ not_found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | - | В коде обработки OTEL_TRACES_SAMPLER_ARG (ОтелАвтоконфигурация.os:203-204) значение напрямую преобразуется через Число() без обработки ошибок. Невалидный ввод (например, нечисловая строка) вызовет исключение вместо логирования. |
| 18 | MUST | ❌ not_found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | - | Невалидный OTEL_TRACES_SAMPLER_ARG не игнорируется gracefully - вызов Число() с нечисловым значением приведёт к исключению, а не к игнорированию параметра. |
| 19 | MUST | ❌ not_found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | - | При невалидном OTEL_TRACES_SAMPLER_ARG реализация не ведёт себя так, как будто параметр не установлен. Вместо фолбэка на значение по умолчанию (1.0 для traceidratio) происходит исключение. |

#### Attribute Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#attribute-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | Implementations SHOULD only offer environment variables for the types of attributes, for which that SDK implements truncation mechanism. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:395` |  |

#### Exporter Selection

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#exporter-selection)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | SHOULD NOT | ✅ found | "logging": Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:177` |  |
| 22 | SHOULD NOT | ✅ found | "logging": Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:291` |  |
| 23 | SHOULD NOT | ✅ found | "logging": Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:255` |  |

#### Declarative configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#declarative-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ❌ not_found | When `OTEL_CONFIG_FILE` is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored. | - | Переменная OTEL_CONFIG_FILE не поддерживается в реализации. Нет кода, который бы проверял наличие этой переменной или реализовывал декларативную конфигурацию из файла. |

## Требования Development-статуса

Эти требования находятся в секциях со статусом Development. Их реализация не обязательна для соответствия стабильной спецификации.

### Resource Sdk

#### Resource detector name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-detector-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ➖ n_a | Resource detectors SHOULD have a unique name for reference in configuration. | - | Conditional feature 'Resource Detector Naming' is not implemented. Detectors have no naming mechanism. |
| 2 | SHOULD | ➖ n_a | Names SHOULD be snake case and consist of lowercase alphanumeric and `_` characters, which ensures they conform to declarative configuration property name requirements. | - | Conditional feature 'Resource Detector Naming' is not implemented. Detectors have no naming mechanism. |
| 3 | SHOULD | ➖ n_a | Resource detector names SHOULD reflect the root namespace of attributes they populate. | - | Conditional feature 'Resource Detector Naming' is not implemented. Detectors have no naming mechanism. |
| 4 | SHOULD | ➖ n_a | Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name which appropriately conveys their purpose. | - | Conditional feature 'Resource Detector Naming' is not implemented. Detectors have no naming mechanism. |
| 5 | SHOULD | ➖ n_a | An SDK which identifies multiple resource detectors with the same name SHOULD report an error. | - | Conditional feature 'Resource Detector Naming' is not implemented. Detectors have no naming mechanism. |
| 6 | SHOULD | ➖ n_a | In order to limit collisions, resource detectors SHOULD document their name in a manner which is easily discoverable. | - | Conditional feature 'Resource Detector Naming' is not implemented. Detectors have no naming mechanism. |

### Trace Api

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when creating Spans, a Tracer SHOULD provide this Enabled API. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 2 | MUST | ✅ found | There are currently no required parameters for this API. Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 3 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 4 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they create a new Span to ensure they have the most up-to-date response. | `src/Трассировка/Классы/ОтелТрассировщик.os:31` | Документация метода Включен() описывает назначение (позволяет пропустить создание спана), но не указывает явно, что метод следует вызывать каждый раз перед созданием нового спана для получения актуального ответа. |

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
| 1 | MUST | ✅ found | The function MUST accept the following parameter: `tracer_scope`: The `InstrumentationScope` of the `Tracer`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:220` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `TracerConfig`, or some signal indicating that the default TracerConfig should be used. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:220` |  |

#### Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | `Tracer` MUST behave according to the TracerConfig computed during Tracer creation. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` | TracerConfig вычисляется и хранится в трассировщике, метод Включен() отражает значение enabled, но НачатьСпан/НачатьКорневойСпан не проверяют Включен() - при disabled TracerConfig спаны всё равно создаются вместо no-op поведения |
| 2 | MUST | ❌ not_found | the `Tracer` MUST be updated to behave according to the new `TracerConfig`. | - | Нет механизма обновления TracerConfig на уже созданных трассировщиках при изменении TracerConfigurator в провайдере. Конфигурация устанавливается однократно при создании трассировщика и не обновляется |

#### TracerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | the `enabled` parameter SHOULD default to `true` (i.e. `Tracer`s are enabled by default). | `src/Трассировка/Классы/ОтелКонфигурацияТрассировщика.os:35` |  |
| 2 | MUST | ⚠️ partial | If a `Tracer` is disabled, it MUST behave equivalently to a No-op Tracer. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` | Метод Включен() корректно возвращает Ложь при disabled TracerConfig, но методы НачатьСпан/НачатьКорневойСпан/НачатьДочернийСпан не проверяют Включен() и создают реальные спаны даже при отключенном трассировщике вместо no-op поведения |
| 3 | MUST | ⚠️ partial | The value of `enabled` MUST be used to resolve whether a `Tracer` is Enabled. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` | При enabled=false метод Включен() корректно возвращает Ложь, но при enabled=true результат зависит также от наличия процессоров (Провайдер.Процессор().ЕстьПроцессоры()), а спецификация требует: если enabled=true, Enabled возвращает true |
| 4 | MUST | ❌ not_found | the changes MUST be eventually visible. | - | Нет механизма обновления параметров TracerConfig на существующих трассировщиках. Конфигурация устанавливается при создании и не обновляется, поэтому изменения не могут стать видимыми |

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
| 1 | MUST | ✅ found | The `TraceIdRatioBased` MUST ignore the parent `SampledFlag`. | `src/Трассировка/Модули/ОтелСэмплер.os:275` |  |
| 2 | MUST | ✅ found | Description MUST return a string of the form `"TraceIdRatioBased{RATIO}"` with `RATIO` replaced with the Sampler instance's trace sampling ratio represented as a decimal number. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 3 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 4 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 5 | MUST | ✅ found | The sampling algorithm MUST be deterministic. | `src/Трассировка/Модули/ОтелСэмплер.os:288` |  |
| 6 | MUST | ✅ found | To achieve this, implementations MUST use a deterministic hash of the `TraceId` when computing the sampling decision. | `src/Трассировка/Модули/ОтелСэмплер.os:288` |  |
| 7 | MUST | ✅ found | A `TraceIdRatioBased` sampler with a given sampling probability MUST also sample all traces that any `TraceIdRatioBased` sampler with a lower sampling probability would sample. | `src/Трассировка/Модули/ОтелСэмплер.os:290` |  |
| 8 | SHOULD | ❌ not_found | When this sampler observes a non-empty parent span context, meaning when it is used not as a root sampler, the SDK SHOULD emit a warning such as: | - | No warning is emitted when TraceIdRatioBased is used as a child sampler. The СэмплироватьПоДоле function does not check for parent context or emit any deprecation/compatibility warnings. |

#### ProbabilitySampler

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#probabilitysampler)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | The `ProbabilitySampler` sampler MUST ignore the parent `SampledFlag`. | - | No ProbabilitySampler implementation exists in the codebase. Only TraceIdRatioBased sampler is implemented via ОтелСэмплер.ПоДолеТрассировок(). |
| 2 | SHOULD | ❌ not_found | When (R >= T), the OpenTelemetry TraceState SHOULD be modified to include the key-value `th:T` for rejection threshold value (T), as specified for the OpenTelemetry TraceState `th` sub-key. | - | No ProbabilitySampler implementation exists. The existing TraceIdRatioBased sampler does not use rejection thresholds or modify TraceState with `th:T` values. |
| 3 | SHOULD | ❌ not_found | When a ProbabilitySampler Sampler makes a decision for a non-root Span using TraceID randomness when the Trace random flag was not set, the SDK SHOULD issue a warning statement in its log with a compatibility warning. | - | No ProbabilitySampler implementation exists. No compatibility warning is emitted for any sampling scenario. |

#### AlwaysRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwaysrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | Based on the decision from the wrapped root sampler, `AlwaysRecord` MUST behave as follows: | - | No AlwaysRecord sampler decorator exists in the codebase. There is no implementation that wraps another sampler and converts DROP decisions into RECORD_ONLY. |

#### CompositeSampler

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#compositesampler)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the parameters passed to delegate GetSamplingIntent methods, as they are considered read-only state. | - | No CompositeSampler or ComposableSampler implementation exists. The GetSamplingIntent interface is not implemented. |
| 2 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the OpenTelemetry TraceState (i.e., the `ot` sub-key of TraceState). | - | No ComposableSampler implementation exists in the codebase. |
| 3 | SHOULD | ❌ not_found | The calling CompositeSampler SHOULD update the threshold of the outgoing TraceState (unless `!threshold_reliable`) and that the explicit randomness values MUST not be modified. | - | No CompositeSampler implementation exists. TraceState threshold management is not implemented. |
| 4 | MUST | ❌ not_found | The calling CompositeSampler SHOULD update the threshold of the outgoing TraceState (unless `!threshold_reliable`) and that the explicit randomness values MUST not be modified. | - | No CompositeSampler implementation exists. Randomness value immutability is not enforced because the entire composable sampling framework is absent. |
| 5 | SHOULD | ❌ not_found | For the zero case a `ComposableAlwaysOff` instance SHOULD be returned instead. | - | No ComposableProbability or ComposableAlwaysOff implementations exist in the codebase. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | Custom implementations of the `IdGenerator` SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace `random` flag will be set in the associated Trace contexts. | - | The custom IdGenerator extension point accepts any duck-typed object with generate methods but has no mechanism for the generator to identify itself as producing random TraceIDs. There is no marker interface, flag, or property that would allow the SDK to set the W3C Trace Context Level 2 random flag based on the generator capabilities. |

#### OnEnding

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onending)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The end timestamp MUST have been computed (the `OnEnding` method duration is not included in the span duration). | `src/Трассировка/Классы/ОтелСпан.os:450` |  |
| 2 | MUST | ✅ found | The Span object MUST still be mutable (i.e., `SetAttribute`, `AddLink`, `AddEvent` can be called) while `OnEnding` is called. | `src/Трассировка/Классы/ОтелСпан.os:455` |  |
| 3 | MUST | ✅ found | This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:455` |  |
| 4 | MUST | ⚠️ partial | The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking `OnEnding` of the first `SpanProcessor`. | `src/Трассировка/Классы/ОтелСпан.os:447` | Метод Завершить() вызывает ПередЗавершением синхронно, но нет явного механизма синхронизации (блокировки) для защиты спана от модификации из других потоков (ФоновыхЗаданий) перед вызовом OnEnding |

### Logs Api

#### Ergonomic API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#ergonomic-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | The ergonomic API SHOULD make it more convenient to emit event records following the event semantics. | - | Отдельный эргономичный API для удобной записи событий (event records) не реализован. Текущий API требует ручного создания ОтелЗаписьЛога, настройки полей и вызова Записать(). |
| 2 | SHOULD | ❌ not_found | The design of the ergonomic API SHOULD be idiomatic for its language. | - | Эргономичный API не реализован, поэтому требование к идиоматичности дизайна неприменимо в текущем состоянии кодовой базы. |

### Logs Sdk

#### Logger Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` (see API). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 2 | MUST | ✅ found | The `LoggerProvider` MUST implement the Get a Logger API. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Logger`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:64` |  |
| 4 | MUST | ⚠️ partial | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` | ПолучитьЛоггер не проверяет пустое/null имя явно - Logger будет создан с пустым именем (не упадёт), но нет диагностического сообщения о невалидном имени |
| 5 | SHOULD | ⚠️ partial | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` | Имя сохраняется как есть (пустая строка), но отсутствует явная проверка и логирование предупреждения о невалидном имени |
| 6 | SHOULD | ❌ not_found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | - | Нет логирования диагностического сообщения о том, что указанное имя невалидно (нет проверки ПустаяСтрока(ИмяБиблиотеки) и последующего Лог.Предупреждение) |
| 7 | MUST | ✅ found | The `LoggerProvider` MUST compute the relevant LoggerConfig using the configured LoggerConfigurator, and create a `Logger` whose behavior conforms to that `LoggerConfig`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:69` |  |

#### LoggerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: `logger_scope`: The `InstrumentationScope` of the `Logger`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:72` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `LoggerConfig`, or some signal indicating that the default LoggerConfig should be used. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:69` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Logger MUST behave according to the LoggerConfig computed during logger creation. | `src/Логирование/Классы/ОтелЛоггер.os:240` |  |
| 2 | MUST | ⚠️ partial | If the LoggerProvider supports updating the LoggerConfigurator, then upon update the Logger MUST be updated to behave according to the new LoggerConfig. | `src/Логирование/Классы/ОтелЛоггер.os:123` | Logger has УстановитьКонфигурацию setter method, but LoggerProvider lacks a public method to update the LoggerConfigurator and propagate new configs to already-created loggers. |

#### LoggerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the enabled parameter SHOULD default to true (i.e. Loggers are enabled by default). | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 2 | MUST | ✅ found | If a Logger is disabled, it MUST behave equivalently to No-op Logger. | `src/Логирование/Классы/ОтелЛоггер.os:50` |  |
| 3 | MUST | ✅ found | If not explicitly set, the minimum_severity parameter MUST default to 0. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 4 | MUST | ✅ found | If a log record's SeverityNumber is specified (i.e. not 0) and is less than the configured minimum_severity, the log record MUST be dropped by the Logger. | `src/Логирование/Классы/ОтелЛоггер.os:138` |  |
| 5 | MUST | ✅ found | If not explicitly set, the trace_based parameter MUST default to false. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 6 | MUST | ✅ found | If trace_based is true, log records associated with unsampled traces MUST be dropped by the Logger. | `src/Логирование/Классы/ОтелЛоггер.os:143` |  |
| 7 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Логирование/Классы/ОтелЛоггер.os:123` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If Observed Timestamp is unspecified, the implementation SHOULD set it equal to the current time. | `src/Логирование/Классы/ОтелЛоггер.os:102` |  |
| 2 | MUST | ✅ found | If an Exception is provided, the SDK MUST by default set attributes from the exception on the LogRecord with the conventions outlined in the exception semantic conventions. | `src/Логирование/Классы/ОтелЛоггер.os:170` |  |
| 3 | MUST | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:183` |  |
| 4 | MUST NOT | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:183` |  |
| 5 | MUST | ✅ found | Before processing a log record, the implementation MUST apply the filtering rules defined by the LoggerConfig (in case Enabled was not called prior to emitting the record): | `src/Логирование/Классы/ОтелЛоггер.os:94` |  |
| 6 | MUST | ✅ found | Minimum severity: If the log record's SeverityNumber is specified (i.e. not 0) and is less than the configured minimum_severity, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:138` |  |
| 7 | MUST | ✅ found | Trace-based: If trace_based is true, and if the log record has a SpanId and the TraceFlags SAMPLED flag is unset, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:143` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Enabled MUST return false when either: there are no registered LogRecordProcessors; Logger is disabled (LoggerConfig.enabled is false); the provided severity is specified (i.e. not 0) and is less than the configured minimum_severity in the LoggerConfig; trace_based is true in the LoggerConfig and the current context is associated with an unsampled trace; all registered LogRecordProcessors implement Enabled, and a call to Enabled on each of them returns false. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return true. | `src/Логирование/Классы/ОтелЛоггер.os:61` |  |

### Metrics Api

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | OpenTelemetry SDKs MUST handle `advisory` parameters as described here. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

### Metrics Sdk

#### Meter Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create `Meter` instances through a `MeterProvider` | `src/Метрики/Классы/ОтелПостроительМетра.os:36` |  |
| 2 | MUST | ✅ found | The `MeterProvider` MUST implement the Get a Meter API. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:62` |  |
| 4 | MUST | ❌ not_found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception | - | No validation of invalid names in ОтелПровайдерМетрик.ПолучитьМетр() - it passes any name directly to ОтелОбластьИнструментирования constructor without validation |
| 5 | SHOULD | ❌ not_found | its `name` SHOULD keep the original invalid value | - | No invalid name handling implemented |
| 6 | SHOULD | ❌ not_found | a message reporting that the specified value is invalid SHOULD be logged. | - | No invalid name logging implemented |
| 7 | MUST | ✅ found | The `MeterProvider` MUST compute the relevant MeterConfig using the configured MeterConfigurator, and create a `Meter` whose behavior conforms to that `MeterConfig`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:73` |  |

#### MeterConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: * `meter_scope`: The `InstrumentationScope` of the `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:210` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `MeterConfig`, or some signal indicating that the default MeterConfig should be used. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:210` |  |

#### Start timestamps

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#start-timestamps)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp, or the creation time of the instrument if this is the first collection interval for the instrument. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:145` |  |
| 2 | MUST | ✅ found | This implies that all data points with delta temporality aggregation for an instrument MUST share the same start timestamp. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:276` |  |
| 3 | MUST | ✅ found | Cumulative timeseries MUST use a consistent start timestamp for all collection intervals. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141` |  |
| 4 | SHOULD | ⚠️ partial | For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the series. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:263` | Start timestamp is set to the instrument creation time rather than the time of the first measurement for the series. All series share the same ВремяСтарта from instrument creation. |
| 5 | SHOULD | ⚠️ partial | For asynchronous instrument, the start timestamp SHOULD be: the creation time of the instrument, if the first series measurement occurred in the first collection interval, otherwise, the timestamp of the collection interval prior to the first series measurement. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:184` | Asynchronous instruments set startTimeUnixNano to the current collection time (ВремяСейчас) for every data point, rather than tracking whether the first observation was in the first collection interval and using the creation time or prior interval timestamp accordingly. |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instrument registrations. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:64` |  |
| 2 | MUST | ✅ found | `Meter` MUST behave according to the MeterConfig computed during Meter creation. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:73` |  |
| 3 | MUST | ❌ not_found | If the `MeterProvider` supports updating the MeterConfigurator, then upon update the `Meter` MUST be updated to behave according to the new `MeterConfig`. | - | MeterProvider has no public method to update the MeterConfigurator after creation. The Конфигуратор field is set only during ПриСозданииОбъекта (line 267) and there is no mechanism to re-apply configuration to already-cached meters |

#### MeterConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the `enabled` parameter SHOULD default to `true` (i.e. `Meter`s are enabled by default). | `src/Метрики/Классы/ОтелКонфигурацияМетра.os:35` |  |
| 2 | MUST | ✅ found | If a `Meter` is disabled, it MUST behave equivalently to No-op Meter. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:79` |  |
| 3 | MUST | ✅ found | The value of `enabled` MUST be used to resolve whether an instrument is Enabled. | `src/Метрики/Классы/ОтелМетр.os:511` |  |
| 4 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Метрики/Классы/ОтелМетр.os:504` |  |

#### Instrument enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | The synchronous instrument `Enabled` MUST return `false` when either: * The MeterConfig of the `Meter` used to create the instrument has parameter `enabled=false`. * All resolved views for the instrument are configured with the Drop Aggregation. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` | Включен() checks МетрВключен.Получить() (MeterConfig.enabled) correctly. However, it does not check whether all resolved views use Drop aggregation. The Включен atomic boolean is only set to false via Отключить() called from ОтелПровайдерМетрик.Закрыть(), not in response to view Drop aggregation configuration. The Drop aggregation condition is not implemented. |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |

#### MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | To construct a `MetricReader` when setting up an SDK, at least the following SHOULD be provided: The `exporter` to use, which is a `MetricExporter` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:276` |  |
| 2 | SHOULD | ✅ found | The default output `aggregation` (optional), a function of instrument kind. This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:168` |  |
| 3 | SHOULD | ⚠️ partial | If not configured, the default aggregation SHOULD be used. | - | Default aggregation is determined per-instrument type in ОтелМетр, not configurable at MetricReader level as a function of instrument kind. |
| 4 | SHOULD | ✅ found | The output `temporality` (optional), a function of instrument kind. This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:167` |  |
| 5 | SHOULD | ✅ found | If not configured, the Cumulative temporality SHOULD be used. | `src/Метрики/Модули/ОтелСелекторВременнойАгрегации.os:24` |  |
| 6 | SHOULD | ⚠️ partial | The default aggregation cardinality limit (optional) to use, a function of instrument kind. If not configured, a default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` | Default cardinality limit of 2000 is used, but it is set per instrument as a fixed value, not as a function of instrument kind at the MetricReader level. |
| 7 | SHOULD | ⚠️ partial | A `MetricReader` SHOULD provide the MetricFilter to the SDK or registered MetricProducer(s) when calling the `Produce` operation. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:115` | MetricFilter (ОтелФильтрМетрик) is supported and applied during collection, but there is no separate MetricProducer interface - the reader directly collects from meters. |
| 8 | SHOULD | ✅ found | A common implementation of `MetricReader`, the periodic exporting `MetricReader` SHOULD be provided to be used typically with push-based metrics collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:1` |  |
| 9 | MUST | ✅ found | The `MetricReader` MUST ensure that data points from OpenTelemetry instruments are output in the configured aggregation temporality for each instrument kind. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:167` |  |
| 10 | MUST | ✅ found | For synchronous instruments with Cumulative aggregation temporality, MetricReader.Collect MUST receive data points exposed in previous collections regardless of whether new measurements have been recorded. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141` |  |
| 11 | MUST | ✅ found | For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:143` |  |
| 12 | MUST | ✅ found | For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:112` |  |
| 13 | MUST | ✅ found | For instruments with Cumulative aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST repeat the same starting timestamps (e.g. `(T0, T1], (T0, T2], (T0, T3]`). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141` |  |
| 14 | MUST | ✅ found | For instruments with Delta aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST advance the starting timestamp (e.g. `(T0, T1], (T1, T2], (T2, T3]`). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:145` |  |
| 15 | MUST | ✅ found | The ending timestamp (i.e. `TimeUnixNano`) MUST always be equal to time the metric data point took effect, which is equal to when MetricReader.Collect was invoked. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:274` |  |
| 16 | MUST | ✅ found | The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:107` |  |
| 17 | SHOULD NOT | ✅ found | the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NOT introduce side-effects to other `MetricReader` instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` |  |
| 18 | MUST NOT | ❌ not_found | The SDK MUST NOT allow a `MetricReader` instance to be registered on more than one `MeterProvider` instance. | - | There is no check preventing a MetricReader from being registered on multiple MeterProvider instances. The same reader object can be passed to multiple providers without error. |
| 19 | SHOULD | ✅ found | The SDK SHOULD provide a way to allow `MetricReader` to respond to MeterProvider.ForceFlush and MeterProvider.Shutdown. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` |  |

#### Produce batch

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#produce-batch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | `Produce` MUST return a batch of Metric Points, filtered by the optional `metricFilter` parameter. | - | MetricProducer и его метод Produce не реализованы. Фильтрация метрик через ОтелФильтрМетрик существует в ОтелПериодическийЧитательМетрик, но не как часть MetricProducer интерфейса. |
| 2 | SHOULD | ❌ not_found | Implementation SHOULD use the filter as early as possible to gain as much performance gain possible (memory allocation, internal metric fetching, etc). | - | MetricProducer не реализован. Фильтрация в читателе применяется после сбора данных (в МетрикаОтброшена), а не на ранних этапах. |
| 3 | SHOULD | ❌ not_found | If the batch of Metric Points includes resource information, `Produce` SHOULD require a resource as a parameter. | - | MetricProducer и метод Produce не реализованы. Ресурс передаётся через Meter, но не как параметр Produce. |
| 4 | SHOULD | ❌ not_found | `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | MetricProducer и метод Produce не реализованы. |
| 5 | SHOULD | ❌ not_found | If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`. | - | MetricProducer и метод Produce не реализованы. |

## Условные требования (Conditional)

Требования из условных секций. Применяются только при реализации соответствующей опциональной фичи.

### Propagators

#### B3 Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-extract) | Scope: conditional:B3 Propagator (extension)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | MUST attempt to extract B3 encoded using single and multi-header formats. | - | B3 Propagator is a conditional extension that is not implemented in this SDK. |
| 2 | MUST | ➖ n_a | MUST preserve a debug trace flag, if received, and propagate it with subsequent requests. | - | B3 Propagator is a conditional extension that is not implemented in this SDK. |
| 3 | MUST | ➖ n_a | Additionally, an OpenTelemetry implementation MUST set the sampled trace flag when the debug flag is set. | - | B3 Propagator is a conditional extension that is not implemented in this SDK. |
| 4 | MUST NOT | ➖ n_a | MUST NOT reuse `X-B3-SpanId` as the id for the server-side span. | - | B3 Propagator is a conditional extension that is not implemented in this SDK. |

#### B3 Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-inject) | Scope: conditional:B3 Propagator (extension)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | MUST default to injecting B3 using the single-header format | - | B3 Propagator is a conditional extension that is not implemented in this SDK. |
| 2 | MUST | ➖ n_a | MUST provide configuration to change the default injection format to B3 multi-header | - | B3 Propagator is a conditional extension that is not implemented in this SDK. |
| 3 | MUST NOT | ➖ n_a | MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support reusing the same id for both sides of a request. | - | B3 Propagator is a conditional extension that is not implemented in this SDK. |

### Сводка условных секций

| Раздел | Секция | Scope | Stability | Keywords | Ссылка |
|---|---|---|---|---|---|
| Resource Sdk | Resource detector name | conditional:Resource Detector Naming (conditional) | Development | 6 | [spec](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-detector-name) |
| Propagators | B3 Extract | conditional:B3 Propagator (extension) | Stable | 4 | [spec](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-extract) |
| Propagators | B3 Inject | conditional:B3 Propagator (extension) | Stable | 3 | [spec](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-inject) |

## Ограничения платформы OneScript

| Ограничение | Влияние на спецификацию | Решение |
|---|---|---|
| Нет байтовых массивов | TraceId/SpanId хранятся как hex-строки | Функциональный эквивалент через строки |
| Нет наносекундной точности | Временные метки с точностью до миллисекунд | Используется миллисекундная точность |
| Нет TLS/mTLS из SDK | Сертификаты конфигурируются вне SDK | Делегировано системе/прокси |
| Нет opaque-объектов | Ключи контекста - строки | Строковые константы как ключи |
| Нет thread-local | ФоновыеЗадания вместо goroutines | Передача контекста через параметры |

## Предупреждения валидации

- ⚠️ Секция Metrics Api/Instrument/Asynchronous Counter/Asynchronous Counter creation: 5 требований (ожидалось ровно 4)

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

