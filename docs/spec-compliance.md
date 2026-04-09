# Анализ соответствия спецификации OpenTelemetry v1.55.0

> **Версия спецификации**: [v1.55.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-04-09
> **Методология**: spec-first - извлечены все MUST/SHOULD требования из спецификации, затем каждое прослежено до кода

## Сводка (Stable)

Учитываются только требования из стабильных разделов спецификации с универсальной областью применения.

| Показатель | Значение |
|---|---|
| Всего keywords в спецификации | 824 |
| Stable + universal keywords | 660 |
| Conditional keywords | 23 |
| Development keywords | 156 |
| Найдено требований (Stable universal) | 654 |
| ✅ Реализовано (found) | 501 (76.6%) |
| ⚠️ Частично (partial) | 94 (14.4%) |
| ❌ Не реализовано (not_found) | 59 (9.0%) |
| ➖ Неприменимо (n_a) | 2 |
| **MUST/MUST NOT found** | 346/394 (87.8%) |
| **SHOULD/SHOULD NOT found** | 155/260 (59.6%) |

## Соответствие по разделам (Stable)

| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |
|---|---|---|---|---|---|---|
| Context | 14 | 1 | 0 | 0 | 15 | 93.3% |
| Baggage Api | 16 | 1 | 0 | 0 | 17 | 94.1% |
| Resource Sdk | 10 | 4 | 1 | 0 | 15 | 66.7% |
| Trace Api | 106 | 9 | 5 | 0 | 120 | 88.3% |
| Trace Sdk | 49 | 17 | 9 | 0 | 75 | 65.3% |
| Logs Api | 19 | 1 | 1 | 0 | 21 | 90.5% |
| Logs Sdk | 41 | 11 | 7 | 0 | 59 | 69.5% |
| Metrics Api | 83 | 7 | 5 | 0 | 95 | 87.4% |
| Metrics Sdk | 116 | 31 | 20 | 0 | 167 | 69.5% |
| Otlp Exporter | 12 | 6 | 6 | 1 | 24 | 50.0% |
| Propagators | 28 | 2 | 1 | 1 | 31 | 90.3% |
| Env Vars | 7 | 4 | 4 | 0 | 15 | 46.7% |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Context]** [MUST] The API MUST accept the following parameters: The Context.  
  Attach-функциональность реализована через УстановитьЗначение(Ключ, Значение), которая создаёт новый контекст и кладёт его в стек. Но нет API, принимающего целый объект Context - вместо этого контекст собирается внутренне из отдельных key-value пар. (`src/Ядро/Модули/ОтелКонтекст.os:203`)

- ⚠️ **[Resource Sdk]** [MUST] Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK.  
  Детекторы реализованы как отдельные классы (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора), но находятся в том же пакете src/Ядро/, а не в отдельных пакетах от SDK (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1`)

- ❌ **[Resource Sdk]** [MUST] Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions.  
  Детекторы заполняют атрибуты семантических конвенций (host.name, os.type, process.pid, host.arch и др.), но не устанавливают Schema URL в возвращаемом ресурсе (-)

- ⚠️ **[Resource Sdk]** [MUST] If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources.  
  Метод Слить() корректно обрабатывает конфликт Schema URL (строки 41-44), однако комбинирование детекторов в ЗаполнитьАтрибутыПоУмолчанию (строки 113-118) копирует атрибуты напрямую без использования Слить() и без проверки Schema URL (`src/Ядро/Классы/ОтелРесурс.os:41`)

- ⚠️ **[Trace Api]** [MUST] In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception  
  ПолучитьТрассировщик принимает пустую строку и создаёт ОтелОбластьИнструментирования с ней, возвращая рабочий Tracer. Однако нет явной проверки на null/пустую строку с логированием предупреждения. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58`)

- ⚠️ **[Trace Api]** [MUST NOT] This API MUST NOT accept a Span or SpanContext as parent, only a full Context  
  НачатьДочернийСпан принимает ОтелСпан или ОтелКонтекстСпана напрямую, а не полный Context. Построитель УстановитьРодителя также принимает Span/SpanContext, а не Context (`src/Трассировка/Классы/ОтелТрассировщик.os:133`)

- ❌ **[Trace Api]** [MUST] The API documentation MUST state that adding links at span creation is preferred to calling AddLink later, for contexts that are available during span creation, because head sampling decisions can only consider information present during span creation.  
  В документации метода ДобавитьЛинк нет явного указания, что добавление линков при создании спана предпочтительно. Есть комментарий в ОтелПостроительСпана.os:81, но нет такого предупреждения в самом API ДобавитьЛинк. (-)

- ⚠️ **[Trace Sdk]** [MUST] Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, Sampler, and TracerConfigurator) MUST be owned by the TracerProvider  
  SpanProcessors, SpanLimits, Sampler, TracerConfigurator are owned by TracerProvider. However, IdGenerator is not configurable - ID generation is hardcoded in ОтелУтилиты utility module, not owned by TracerProvider (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:11`)

- ⚠️ **[Trace Sdk]** [MUST] Implementations MUST expose at least the full parent SpanContext  
  Only ИдРодительскогоСпана() (parent span ID string) is exposed. The full parent SpanContext (including TraceId, TraceFlags, TraceState) is not stored or accessible - only the parent span ID is preserved (`src/Трассировка/Классы/ОтелСпан.os:89`)

- ⚠️ **[Trace Sdk]** [MUST] Span Exporters MUST receive those spans which have Sampled flag set to true  
  Spans with RECORD_AND_SAMPLE (Sampled=true) do reach the exporter via the processor chain. However, there is no explicit Sampled flag check - it works only because DROP spans never reach processors. The spec's intent is satisfied for the RECORD_AND_SAMPLE case but not explicitly verified. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37-50`)

- ⚠️ **[Trace Sdk]** [MUST] If the parent SpanContext contains a valid TraceId, they MUST always match (ShouldSample TraceId argument must match parent's TraceId)  
  The tracer uses the parent's TraceId directly (line 61: ИдТрассировки = КонтекстРодителяСпана.ИдТрассировки()), so they always match by construction. However, the ДолженСэмплировать method itself does not explicitly validate this constraint - it accepts ИдТрассировки as a parameter without checking it against parent context. (`src/Трассировка/Классы/ОтелТрассировщик.os:61`)

- ❌ **[Trace Sdk]** [MUST NOT] SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value (rv sub-key)  
  There is no handling of the OpenTelemetry TraceState rv sub-key anywhere in the sampler or SDK code. The ОтелСостояниеТрассировки class handles generic key-value pairs but has no awareness of OpenTelemetry-specific sub-keys like rv or ot. (-)

- ⚠️ **[Trace Sdk]** [MUST] Name of the methods MUST be consistent with SpanContext (one to generate a SpanId and one for TraceId).  
  Methods are named СгенерироватьИдТрассировки/СгенерироватьИдСпана which are consistent in Russian naming but there is no formal IdGenerator interface class - the contract is duck-typed via comments in ОтелУтилиты. (`src/Ядро/Модули/ОтелУтилиты.os:78`)

- ❌ **[Trace Sdk]** [MUST] If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls.  
  СброситьБуфер() does not accept a timeout parameter. ЭкспортироватьВсеПакеты() runs until all batches are exported with no timeout mechanism to abort early. (-)

- ⚠️ **[Trace Sdk]** [MUST] Sampler - ShouldSample and GetDescription MUST be safe to be called concurrently  
  Сэмплер реализован как модуль с функциями-константами (ВсегдаВключен, ВсегдаВыключен и т.д.), по сути stateless. Безопасность конкурентного доступа обеспечивается неявно через отсутствие мутабельного состояния, но нет явного GetDescription метода. (`src/Трассировка/Модули/ОтелСэмплер.os:1`)

- ⚠️ **[Trace Sdk]** [MUST] Span processor - all methods MUST be safe to be called concurrently  
  SimpleSpanProcessor синхронизирует Export через БлокировкаЭкспорта, но методы СброситьБуфер() и Закрыть() не защищены блокировкой. BatchSpanProcessor использует блокировку через базовый класс, но не все методы фасада защищены. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:41`)

- ⚠️ **[Trace Sdk]** [MUST] Span Exporter - ForceFlush and Shutdown MUST be safe to be called concurrently  
  СброситьБуфер() - noop, безопасно. Закрыть() устанавливает Закрыт = Истина без блокировки или атомарного доступа - потенциально не потокобезопасно при конкурентных вызовах с Экспортировать(). (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:47`)

- ❌ **[Logs Sdk]** [MUST NOT] Any modifications to parameters inside Enabled MUST NOT be propagated to the caller. Parameters are immutable or passed by value.  
  ИнтерфейсПроцессорЛогов does not define an Enabled operation. The Logger has Включен() (src/Логирование/Классы/ОтелЛоггер.os:42) but it does not delegate to processor-level Enabled. The processor interface only has ПриПоявлении, СброситьБуфер, Закрыть - no Enabled/Включен method. (-)

- ⚠️ **[Logs Sdk]** [MUST] The built-in LogRecordProcessors MUST do so (call exporter's Export with all LogRecords and then invoke ForceFlush on the exporter).  
  Built-in processors call Экспортер.Экспортировать() for all remaining records but do not invoke Экспортер.СброситьБуфер() (ForceFlush) on the exporter. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120`)

- ❌ **[Logs Sdk]** [MUST] If a timeout is specified, the LogRecordProcessor MUST prioritize honoring the timeout over finishing all calls.  
  СброситьБуфер() has no timeout parameter. ЭкспортироватьВсеПакеты() exports all batches synchronously without any timeout consideration. (-)

- ⚠️ **[Logs Sdk]** [MUST] LogRecordExporter - ForceFlush and Shutdown MUST be safe to be called concurrently  
  Закрыть() sets Закрыт=Истина without synchronization (no lock or atomic). СброситьБуфер() is a no-op so concurrent calls are safe, but Shutdown itself is not protected against concurrent calls (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-49`)

- ⚠️ **[Metrics Api]** [MUST] Callback functions MUST be documented as follows for the end user (reentrant safe, not indefinite, no duplicate observations).  
  Конструктор ОтелБазовыйНаблюдаемыйИнструмент содержит комментарий о параметрах, но документация не содержит предупреждений для конечного пользователя о реентрантной безопасности, длительности выполнения и дублировании наблюдений. (`src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:136-158`)

- ⚠️ **[Metrics Sdk]** [MUST] The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept.  
  ОтелПредставление accepts ИсключенныеКлючиАтрибутов parameter, but ПрименитьПредставлениеКИнструменту does not apply exclude-list filtering - only allow-list (РазрешенныеКлючиАтрибутов) is applied via УстановитьРазрешенныеКлючиАтрибутов. (`src/Метрики/Классы/ОтелПредставление.os:56-58`)

- ⚠️ **[Metrics Sdk]** [MUST] If an attribute key is both included and excluded, the SDK MAY fail fast - the exclude-list: all other attributes MUST be kept.  
  Exclude-list parameter is accepted in the View constructor but its semantics are not enforced during collection. Only allow-list filtering is applied. (`src/Метрики/Классы/ОтелПредставление.os:162`)

- ⚠️ **[Metrics Sdk]** [MUST] If the user does not provide an aggregation value, the MeterProvider MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance.  
  Default aggregation is applied based on instrument type (Sum for Counter, Histogram for Histogram, etc.) but it is hardcoded at Meter level, not configurable per MetricReader instance. The MetricReader does not have a separate default_aggregation property. (`src/Метрики/Классы/ОтелМетр.os:58-59`)

- ⚠️ **[Metrics Sdk]** [MUST] If the user does not provide an aggregation_cardinality_limit value, the MeterProvider MUST apply the default aggregation cardinality limit the MetricReader is configured with.  
  Default cardinality limit is 2000 (hardcoded in constructor), but it is set from Meter, not configured per MetricReader. The MetricReader has no aggregation_cardinality_limit configuration property. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253`)

- ⚠️ **[Metrics Sdk]** [MUST] When a user passes multiple casings of the same name, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above.  
  Instrument names are normalized with НРег() (lowercase) and stored by normalized key, so the first-seen instrument is correctly returned for different casings. However, when the second request comes with different casing but identical descriptors (kind, unit, description), no warning is logged because ПроверитьКонфликтДескриптора only warns when descriptors differ, not for pure casing conflicts. (`src/Метрики/Классы/ОтелМетр.os:49`)

- ⚠️ **[Metrics Sdk]** [MUST] This MUST be clearly documented in the API and the reservoir MUST be given the Attributes associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the 'offer' method.  
  Reservoir receives timeseries attributes in the 'offer' method call (АтрибутыСерии parameter) rather than at construction time, but it does have access to both measurement and timeseries attributes during offer. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39`)

- ⚠️ **[Metrics Sdk]** [MUST] The 'offer' method MAY accept a filtered subset of Attributes which diverge from the timeseries. This MUST be clearly documented in the API.  
  The offer method accepts both АтрибутыИзмерения and АтрибутыСерии, but there is no explicit API documentation explaining the filtered attributes divergence behavior as required. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39`)

- ⚠️ **[Metrics Sdk]** [MUST] Individual reservoirs MUST still be instantiated per metric-timeseries.  
  Резервуар создаётся один на инструмент, а не per metric-timeseries. Внутри резервуара данные разделены по КлючАтрибутов, что функционально эквивалентно per-timeseries, но архитектурно это один экземпляр резервуара. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265`)

- ⚠️ **[Metrics Sdk]** [MUST NOT] Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure).  
  Экспорт делегирует транспорту (HTTP), который имеет таймауты на уровне HTTP-клиента, но в самом экспортере нет явного верхнего ограничения таймаута. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25`)

- ❌ **[Metrics Sdk]** [MUST] MetricProducer defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data.  
  No MetricProducer interface/class exists in the codebase. The pull exporter (ОтелПрометеусЧитательМетрик) is modeled as a MetricReader, not via a separate MetricProducer interface for bridging third-party sources. (-)

- ❌ **[Metrics Sdk]** [MUST] A MetricProducer MUST support the following functions (Produce).  
  No MetricProducer interface exists. There is no Produce method. Metric collection is done internally within MetricReader implementations (СобратьИЭкспортировать), not via a separate MetricProducer.Produce interface. (-)

- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST provide configuration according to the SDK environment variables specification.  
  Some metrics env vars are read (OTEL_METRICS_EXEMPLAR_FILTER in builder, OTEL_METRICS_EXPORTER and OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE in autoconfiguration), but not all SDK env vars for metrics are fully supported (e.g., OTEL_METRIC_EXPORT_INTERVAL, OTEL_METRIC_EXPORT_TIMEOUT are not read from environment). (`src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:110`)

- ❌ **[Metrics Sdk]** [MUST] The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry.  
  No explicit numerical limits handling found in metrics code. No checks for overflow, underflow, or special float values in aggregators or instruments. (-)

- ❌ **[Metrics Sdk]** [MUST] If the SDK receives float/double values from Instruments, it MUST handle all the possible values (e.g. NaN and Infinities for IEEE 754).  
  No NaN or Infinity handling found in metrics aggregators (ОтелАгрегаторСуммы, ОтелАгрегаторГистограммы, ОтелАгрегаторПоследнегоЗначения). Values are used directly without any special-value checks. (-)

- ⚠️ **[Metrics Sdk]** [MUST] MeterProvider - Meter creation, ForceFlush and Shutdown MUST be safe to be called concurrently.  
  Meter creation uses СинхронизированнаяКарта (thread-safe map) for meter cache, but the Закрыт flag is a plain Булево (not atomic), creating potential race conditions between ПолучитьМетр, СброситьБуфер, and Закрыть. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:241`)

- ⚠️ **[Metrics Sdk]** [MUST] ExemplarReservoir - all methods MUST be safe to be called concurrently.  
  Uses СинхронизированнаяКарта and АтомарноеЧисло for individual operations, but the compound operation in ДобавитьВРезервуар (get array, check size, add/replace element) is not atomic - concurrent threads may race on the same array. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:167`)

- ⚠️ **[Metrics Sdk]** [MUST] MetricExporter - ForceFlush and Shutdown MUST be safe to be called concurrently.  
  ОтелЭкспортерМетрик.Закрыть sets Закрыт = Истина (plain boolean, not atomic) without any lock. No concurrency protection between Экспортировать and Закрыть. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49`)

- ⚠️ **[Otlp Exporter]** [MUST] The following configuration options MUST be available to configure the OTLP exporter (Endpoint, Insecure, Certificate File, Client key file, Client certificate file, Headers, Compression, Timeout, Protocol).  
  Endpoint, Headers, Compression, Timeout, Protocol доступны. TLS-опции (Certificate File, Client key, Client certificate) не реализованы (ограничение платформы). Insecure не реализован (спецификация допускает MAY для этой опции). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130`)

- ❌ **[Otlp Exporter]** [MUST] Each configuration option MUST be overridable by a signal specific option (e.g. OTEL_EXPORTER_OTLP_TRACES_ENDPOINT overrides OTEL_EXPORTER_OTLP_ENDPOINT for traces).  
  Сигнал-специфичные переменные (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_ENDPOINT и т.д.) не реализованы. Используется только общий otel.exporter.otlp.endpoint без возможности переопределения по сигналу. (-)

- ⚠️ **[Otlp Exporter]** [MUST] Protocol: Options MUST be one of: grpc, http/protobuf, http/json.  
  Поддерживаются grpc и http/json. Протокол http/protobuf не реализован - HTTP-транспорт всегда отправляет JSON (Content-Type: application/json). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ❌ **[Otlp Exporter]** [MUST] For the per-signal variables (OTEL_EXPORTER_OTLP_<signal>_ENDPOINT), the URL MUST be used as-is without any modification.  
  Сигнал-специфичные переменные окружения (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT и т.д.) не реализованы, поэтому поведение 'use as-is' невозможно проверить. (-)

- ❌ **[Otlp Exporter]** [MUST] The only exception is that if an URL contains no path part, the root path / MUST be used (for per-signal endpoint variables).  
  Сигнал-специфичные переменные окружения не реализованы, поэтому обработка URL без пути невозможна. (-)

- ⚠️ **[Propagators]** [MUST] The official list of propagators that MUST be maintained by the OpenTelemetry organization: W3C TraceContext, W3C Baggage, B3.  
  W3C TraceContext (ОтелW3CПропагатор) и W3C Baggage (ОтелW3CBaggageПропагатор) реализованы. B3 Propagator не реализован. (`src/Пропагация/Классы/ОтелW3CПропагатор.os:1`)

- ⚠️ **[Propagators]** [MUST] The official list of propagators MUST be distributed as OpenTelemetry extension packages: W3C TraceContext (MAY be part of API), W3C Baggage (MAY be part of API), B3.  
  W3C TraceContext и Baggage распространяются как часть основного пакета (допустимо по спецификации через MAY). B3 Propagator не реализован и не распространяется. (`src/Пропагация/Классы/ОтелW3CПропагатор.os:1`)

- ⚠️ **[Env Vars]** [MUST] The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset.  
  Обработка пустых значений реализована частично: для ресурсных атрибутов (строка 105) и пропагаторов (строка 340) пустые значения проверяются явно (<> ""), но для многих других параметров (otel.service.name строка 114, числовые параметры строки 224-227) пустая строка не проверяется и может привести к ошибкам. ПровайдерПараметровENV не фильтрует пустые значения на уровне провайдера. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105,340`)

- ⚠️ **[Env Vars]** [MUST] For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting.  
  Для пропагаторов неизвестное значение логируется через Сообщить() (строка 373) и пропускается. Однако для семплеров неизвестное значение молча подменяется на parentbased_always_on без предупреждения (строка 216-218). Для экспортеров неизвестное значение не обрабатывается - вероятно вызовет ошибку. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:373`)

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Baggage Api]** [SHOULD NOT] API users SHOULD NOT have access to the Context Key used by the Baggage API implementation.  
  Удобные методы BaggageИзКонтекста/КонтекстСBaggage существуют, но ключ контекста КлючBaggage также публично доступен через экспортную функцию КлючBaggage() (`src/Ядро/Модули/ОтелКонтекст.os:53`)

- ⚠️ **[Resource Sdk]** [SHOULD] An error that occurs during an attempt to detect resource information SHOULD be considered an error.  
  Ошибки при обнаружении ресурсов перехватываются, но логируются на уровне Отладка (Debug), а не как ошибки (Error) согласно спецификации (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:24`)

- ⚠️ **[Resource Sdk]** [SHOULD] Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate.  
  Детекторы используют пустой Schema URL, но при этом заполняют известные атрибуты семантических конвенций (host.name, os.type и др.) - в этом случае по спецификации должен быть установлен соответствующий Schema URL (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18`)

- ⚠️ **[Trace Api]** [SHOULD] its name property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged  
  Имя устанавливается как есть (будет пустой строкой), но предупреждение о невалидном имени не логируется. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58`)

- ⚠️ **[Trace Api]** [SHOULD] a message reporting that the specified value is invalid SHOULD be logged  
  Нет логирования предупреждения при пустом или null имени. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58`)

- ⚠️ **[Trace Api]** [SHOULD] This SHOULD be called SetStatus.  
  Метод называется УстановитьСтатус, что является русским переводом SetStatus. Семантически верно, но имя отличается от спеки. (`src/Трассировка/Классы/ОтелСпан.os:413`)

- ❌ **[Trace Api]** [SHOULD] When the status is set to Error by Instrumentation Libraries, the Description SHOULD be documented and predictable.  
  Нет документации по предсказуемым значениям Description для ошибок, устанавливаемых инструментирующими библиотеками. (-)

- ❌ **[Trace Api]** [SHOULD] Instrumentation Libraries SHOULD publish their own conventions for Description values, including possible values and what they mean.  
  Нет публикации конвенций по значениям Description для ошибок. (-)

- ❌ **[Trace Api]** [SHOULD] Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generate.  
  Это требование относится к инструментам анализа, а не к SDK, но в кодовой базе нет инструментов анализа, подавляющих ошибки при Ok-статусе. (-)

- ⚠️ **[Trace Api]** [SHOULD NOT] If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible.  
  ОтелНоопСпан является публичным классом, зарегистрированным в lib.config, хотя спека рекомендует не экспонировать его публично. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ⚠️ **[Trace Api]** [SHOULD] If a new type is required to be publicly exposed, it SHOULD be named NonRecordingSpan.  
  Класс назван ОтелНоопСпан вместо рекомендуемого NonRecordingSpan (или ОтелНеЗаписывающийСпан). Нооп - не то же самое что NonRecording. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ⚠️ **[Trace Api]** [SHOULD] Implementations SHOULD record links containing SpanContext with empty TraceId or SpanId (all zeros) as long as either the attribute set or TraceState is non-empty.  
  ДобавитьЛинк не проверяет валидность SpanContext и принимает любой, что частично покрывает требование, но нет явной логики проверки empty TraceId/SpanId с non-empty attributes/TraceState. (`src/Трассировка/Классы/ОтелСпан.os:361`)

- ⚠️ **[Trace Api]** [SHOULD] Link - Links are immutable and SHOULD be safe for concurrent use by default.  
  Линки представлены как Соответствие (mutable), а не как отдельный иммутабельный класс. Нет документации об их потокобезопасности. (`src/Трассировка/Классы/ОтелСпан.os:372`)

- ❌ **[Trace Api]** [SHOULD] If the Span in the parent Context is already non-recording, it SHOULD be returned directly without instantiating a new Span.  
  В НачатьСпан нет проверки, является ли родительский спан уже non-recording. Всегда создается новый ОтелНоопСпан даже если родитель уже non-recording. (-)

- ❌ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out  
  СброситьБуфер() is a Процедура (void return), provides no indication of success, failure, or timeout to the caller (-)

- ❌ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout  
  СброситьБуфер() has no timeout mechanism - it blocks indefinitely while iterating over processors (-)

- ⚠️ **[Trace Sdk]** [SHOULD NOT] Span Exporter SHOULD NOT receive spans unless the Sampled flag was also set  
  When sampler returns DROP, a NoOp span is created and never reaches the processor/exporter. When RECORD_ONLY, the span IS passed to the processor (line 639-641 of ОтелСпан.os) and then to the exporter (ПриЗавершении). There is no explicit check in the processor/exporter chain to filter out spans with Sampled=false but IsRecording=true (RECORD_ONLY). The SimpleSpanProcessor and BatchSpanProcessor forward all spans they receive to the exporter without checking the Sampled flag. (`src/Трассировка/Классы/ОтелТрассировщик.os:71-94`)

- ⚠️ **[Trace Sdk]** [SHOULD NOT] Span Exporters SHOULD NOT receive spans that do not have Sampled flag set  
  There is no filtering in processors or exporters based on the Sampled flag. Spans with RECORD_ONLY decision (IsRecording=true, Sampled=false) would be passed to the exporter. The processor does not check ФлагиТрассировки before forwarding to exporter. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37-50`)

- ❌ **[Trace Sdk]** [SHOULD NOT] Callers SHOULD NOT cache the returned value of GetDescription  
  This is a guidance for callers, not an implementation requirement. The Описание() method exists (ОтелСэмплер.os:106-122) but there is no mechanism or documentation preventing callers from caching the result. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 when generating TraceID values  
  TraceIDs are generated using УникальныйИдентификатор (UUID v4), which provides randomness, but there is no explicit verification that the generated IDs meet W3C Trace Context Level 2 requirements for 56 bits of randomness in the rightmost 7 bytes. UUID v4 has 122 random bits total but the randomness distribution across specific byte positions may not match the W3C requirement exactly. (`src/Ядро/Модули/ОтелУтилиты.os:78-92`)

- ❌ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD set the Random flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements  
  The trace flags handling in the SDK only deals with the Sampled flag (bit 0). There is no implementation of the Random flag (bit 1 of W3C Trace Context Level 2). ВычислитьФлагиТрассировки() in ОтелТрассировщик.os only returns 0 or 1 based on sampling decision, never setting the Random flag. (-)

- ❌ **[Trace Sdk]** [SHOULD] For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the rv sub-key of the OpenTelemetry TraceState  
  The sampler does not inspect or use the rv sub-key of TraceState. It always uses TraceID-based hashing without considering explicit randomness values. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] If the SDK uses an IdGenerator extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated  
  The SDK provides an IdGenerator extension point (УстановитьГенераторИд) that allows custom generators for TraceId and SpanId. However, the extension point does not include any mechanism for the generator to indicate whether generated IDs meet randomness requirements or to control the Random trace flag. The ВычислитьФлагиТрассировки() method in the tracer does not consult the ID generator about the Random flag. (`src/Ядро/Модули/ОтелУтилиты.os:54-65`)

- ⚠️ **[Trace Sdk]** [SHOULD] Shutdown SHOULD be called only once for each SpanProcessor instance. After the call to Shutdown, subsequent calls to OnStart, OnEnd, or ForceFlush are not allowed. SDKs SHOULD ignore these calls gracefully, if possible.  
  BatchSpanProcessor checks Закрыт flag in Обработать() and returns early, but SimpleSpanProcessor (ОтелПростойПроцессорСпанов) does not track shutdown state - Закрыть() just closes the exporter without setting any flag to prevent subsequent OnStart/OnEnd/ForceFlush calls. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43`)

- ❌ **[Trace Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Закрыть() in both SimpleSpanProcessor and BatchSpanProcessor (via ОтелБазовыйПакетныйПроцессор) is a Процедура (void), it does not return success/failure/timeout status. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] Shutdown SHOULD complete or abort within some timeout.  
  BatchSpanProcessor uses ТаймаутЭкспортаМс to wait for background export to stop, but the subsequent ЭкспортироватьВсеПакеты() call in Закрыть() has no timeout - it runs until buffer is empty. SimpleSpanProcessor has no timeout mechanism at all. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192`)

- ⚠️ **[Trace Sdk]** [SHOULD] SDKs SHOULD ignore these calls gracefully, if possible (subsequent calls to OnStart, OnEnd, ForceFlush after Shutdown).  
  BatchSpanProcessor ignores Обработать() after shutdown (Закрыт flag), but SimpleSpanProcessor does not track shutdown state and may still attempt to export after Закрыть(). (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43`)

- ❌ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() is a Процедура (void) - it does not return success/failure/timeout status to the caller. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() delegates to ЭкспортироватьВсеПакеты() which loops exporting batches until buffer is empty, but has no timeout mechanism to abort. The async variant СброситьБуферАсинхронно() exists on the provider level but individual processor ForceFlush has no timeout. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68`)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out  
  СброситьБуфер() определена как Процедура (void), не возвращает результат успеха/ошибки/таймаута. В ОтелЭкспортерСпанов.os:41 аналогично - Процедура без возвращаемого значения. (`src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:19`)

- ❌ **[Logs Api]** [SHOULD] The API (Enabled) SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response.  
  Документация метода Включен() не содержит явного указания о необходимости вызывать его перед каждым emit. Комментарий описывает назначение метода, но не включает рекомендацию вызывать его повторно для актуального результата. (-)

- ⚠️ **[Logs Api]** [SHOULD] When only explicit Context is supported, this parameter (Context for Emit) SHOULD be required.  
  Реализация поддерживает implicit Context (через ОтелКонтекст.Текущий()), поэтому параметр сделан опциональным. Требование SHOULD для explicit-only контекста не применяется напрямую, но Контекст передается как optional параметр в Записать(), что соответствует implicit-поддерживающей реализации. (`src/Логирование/Классы/ОтелЛоггер.os:76`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() - Процедура (void), не возвращает статус. СброситьБуферАсинхронно() возвращает Обещание, но синхронный метод не сообщает об успехе/ошибке. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD return some ERROR status if there is an error condition.  
  СброситьБуфер() не возвращает значение, ошибки процессоров не пробрасываются вызывающему коду. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] if there is no error condition, it SHOULD return some NO ERROR status.  
  СброситьБуфер() не возвращает значение - нет способа узнать об успешном выполнении. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ❌ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  Метод СброситьБуфер() не имеет механизма таймаута - вызывает СброситьБуфер() на каждом процессоре без ограничения по времени. (-)

- ⚠️ **[Logs Sdk]** [SHOULD NOT] OnEmit is called synchronously on the thread that emitted the LogRecord, therefore it SHOULD NOT block or throw exceptions.  
  Composite processor catches exceptions from individual processors, but ОтелПростойПроцессорЛогов.ПриПоявлении re-throws export errors (line 26-27) and blocks synchronously during export. Batch processor handles correctly (non-blocking buffer add). (`src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17`)

- ❌ **[Logs Sdk]** [SHOULD] Implementations SHOULD recommended to users that a clone of logRecord be used for any concurrent processing, such as in a batching processor.  
  ОтелЗаписьЛога has no clone method and there is no documentation recommending cloning for concurrent processing scenarios. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD be called only once for each LogRecordProcessor instance.  
  Batch processor sets Закрыт=Истина but does not guard against double-close (no atomic CAS). Simple processor has no shutdown guard at all - multiple Закрыть() calls would close exporter multiple times. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:75`)

- ⚠️ **[Logs Sdk]** [SHOULD] After the call to Shutdown, subsequent calls to OnEmit are not allowed. SDKs SHOULD ignore these calls gracefully, if possible.  
  Batch processor checks Закрыт flag in Обработать() and returns early (graceful ignore). Simple processor ОтелПростойПроцессорЛогов.ПриПоявлении does not check shutdown state - would attempt to call closed exporter. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43`)

- ❌ **[Logs Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Both processor Закрыть() methods are Процедура (void). No return value or callback to indicate success, failure, or timeout. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] If any LogRecordProcessor has any associated exporter, it SHOULD try to call the exporter's Export with all LogRecords for which this was not already done and then invoke ForceFlush on it.  
  ЭкспортироватьВсеПакеты() calls Экспортер.Экспортировать() for all remaining records, but does NOT call Экспортер.СброситьБуфер() (ForceFlush on the exporter) afterwards. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120`)

- ❌ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() is a Процедура (void) on both simple and batch processors. No return value or callback to indicate result. (-)

- ❌ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() has no timeout mechanism. It synchronously exports all batches via ЭкспортироватьВсеПакеты() without any timeout or abort logic. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out  
  СброситьБуфер() is a Процедура (void), does not return success/failure/timeout status to the caller (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout  
  СброситьБуфер() on the exporter has no timeout mechanism - it is a synchronous no-op for the OTLP exporter but there is no configurable timeout for cases where flush could block (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43`)

- ⚠️ **[Metrics Api]** [SHOULD] Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying.  
  Дескрипторы инструментов хранят Вид/ЕдиницуИзмерения/Описание/Совет, но не хранят тип числа (int vs double). OneScript не имеет явного разделения int/double на уровне языка, дескриптор не включает тип значения как идентифицирующее поле. (`src/Метрики/Классы/ОтелМетр.os:553-579`)

- ❌ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (sync instruments).  
  Документация метода СоздатьСчетчик и аналогичных не содержит указания на синтаксические требования к имени инструмента. (-)

- ❌ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (async instruments).  
  Документация метода СоздатьНаблюдаемыйСчетчик и аналогичных не содержит указания на синтаксические требования к имени инструмента. (-)

- ⚠️ **[Metrics Api]** [SHOULD] Callback functions SHOULD be reentrant safe. The SDK expects to evaluate callbacks for each MetricReader independently.  
  Документация callback не содержит рекомендации о реентрантной безопасности для конечного пользователя. (-)

- ⚠️ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT take an indefinite amount of time.  
  Документация callback не содержит предупреждения о времени выполнения для конечного пользователя. (-)

- ⚠️ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT make duplicate observations (more than one Measurement with the same attributes) across all registered callbacks.  
  Документация callback не содержит предупреждения о дублировании наблюдений для конечного пользователя. (-)

- ❌ **[Metrics Api]** [SHOULD] The Enabled API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response  
  Документация метода Включен() не содержит рекомендации вызывать его перед каждым измерением. Комментарий описывает лишь что возвращает метод, но не содержит рекомендации по частоте вызова. (-)

- ❌ **[Metrics Api]** [SHOULD] The increment value is expected to be non-negative. This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative  
  Комментарий к методу Добавить (строка 14) говорит 'положительное значение', но формально спека требует 'non-negative' (включая ноль). Тем не менее код проверяет Значение < 0 (строка 22), а документация описывает это. Ставлю not_found поскольку формальная документация для конечного пользователя (API doc) не содержит явного указания 'non-negative'. (-)

- ⚠️ **[Metrics Api]** [SHOULD NOT] This API SHOULD NOT validate the non-negative value, that is left to implementations of the API  
  Counter.Добавить() фактически валидирует значение - отбрасывает отрицательные (Если Значение < 0 Тогда Возврат). Спецификация говорит API SHOULD NOT validate. (`src/Метрики/Классы/ОтелСчетчик.os:22-24`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD provide some way to pass state to the callback  
  Callback реализован через Действие (lambdas), что позволяет замыкание (closure) для передачи состояния. Однако явного параметра state нет - состояние передаётся только через замыкание, что является идиоматическим подходом для OneScript. (`src/Метрики/Классы/ОтелМетр.os:229`)

- ❌ **[Metrics Api]** [SHOULD] The recorded value is expected to be non-negative. This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative  
  Документация метода Записать в ОтелГистограмма не содержит указания что значение должно быть неотрицательным. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() - процедура без возвращаемого значения. Есть СброситьБуферАсинхронно() с Обещание, но синхронный вариант не информирует вызывающий код о результате (`src/Метрики/Классы/ОтелПровайдерМетрик.os:115`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status.  
  Метод СброситьБуфер() не возвращает ни ERROR, ни NO ERROR статус - это процедура (void) (`src/Метрики/Классы/ОтелПровайдерМетрик.os:115`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() не принимает параметр таймаута и не имеет механизма прерывания по таймауту (`src/Метрики/Классы/ОтелПровайдерМетрик.os:115`)

- ⚠️ **[Metrics Sdk]** [SHOULD] In order to avoid conflicts, if a name is provided the View SHOULD have an instrument selector that selects at most one instrument.  
  No validation in the code to check that a View with name selects at most one instrument; name is accepted but no warning is emitted when a wildcard selector is combined with a name override. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning.  
  Views are applied independently but no conflict detection or warning emission occurs when multiple Views produce conflicting metric identities (same name from different Views). (-)

- ❌ **[Metrics Sdk]** [SHOULD] If it is not possible to apply the View without producing semantic errors the implementation SHOULD emit a warning and proceed as if the View did not exist.  
  No semantic validation of View compatibility (e.g., checking if async instrument is set to use explicit bucket histogram aggregation). Views are always applied without semantic error checking. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] If the Instrument could not match with any of the registered Views, the SDK SHOULD enable the instrument using the default aggregation and temporality.  
  Default aggregation is applied when no View matches (instrument is always created with a default aggregator). However, temporality is determined by the MetricReader/exporter, not explicitly set at View miss point. (`src/Метрики/Классы/ОтелМетр.os:48-67`)

- ❌ **[Metrics Sdk]** [SHOULD NOT] Arithmetic sum of Measurement values in population - this SHOULD NOT be collected when used with instruments that record negative measurements (e.g. UpDownCounter or ObservableGauge).  
  The histogram aggregator always collects sum regardless of instrument type. No check prevents sum collection for UpDownCounter or ObservableGauge histogram aggregations. (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the sum, min, and max fields.  
  No explicit check for +Inf, -Inf, or NaN values in the exponential histogram aggregator's Записать method. All values are processed without filtering non-normal values. (-)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks.  
  No mechanism to detect or disregard async instrument API usage outside of registered callbacks. The ОтелНаблюдениеМетрики can be used and populated anywhere, not just within callback context. (-)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback execution.  
  No timeout for individual callback execution. Callbacks are invoked in a simple loop (ВызватьCallbackИСобрать) without any timeout mechanism. Only the periodic reader has a shutdown timeout, not per-callback timeout. (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback.  
  Observable instruments clear external observations after each collect (ВнешниеНаблюдения = Новый Массив at line 174 of ОтелБазовыйНаблюдаемыйИнструмент.os) but data points from callbacks are freshly created each time. However, there is no explicit mechanism to track 'previously-observed attribute sets' vs 'currently-observed' for persistence filtering across collection cycles. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] A view with criteria matching the instrument an aggregation is created for has an aggregation_cardinality_limit value defined for the stream, that value SHOULD be used.  
  ОтелПредставление has ЛимитМощностиАгрегации property (line 92), but in ОтелМетр.ПрименитьПредставлениеКИнструменту the view's cardinality limit is never read or applied to the instrument's ЛимитМощности. Only РазрешенныеКлючиАтрибутов, РезервуарЭкземпляров, and ГраницыГистограммы from the View are applied. (`src/Метрики/Классы/ОтелПредставление.os:92`)

- ❌ **[Metrics Sdk]** [SHOULD] If there is no matching view, but the MetricReader defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used.  
  ОтелПериодическийЧитательМетрик has no cardinality limit configuration. There is no API on the MetricReader to define a default cardinality limit per instrument kind. (-)

- ❌ **[Metrics Sdk]** [SHOULD] Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality.  
  ОтелБазовыйНаблюдаемыйИнструмент has no cardinality limiting at all. All observations from callbacks are converted directly to data points without any cardinality checks or overflow handling. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible.  
  The warning message includes information about conflicting parameters (existing vs requested kind/unit), but does not include any resolution guidance such as suggesting the user configure a View to resolve the conflict. (`src/Метрики/Классы/ОтелМетр.os:573`)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves multiple description properties, setting the description through a configured View SHOULD avoid the warning.  
  There is no logic to check if a View resolves the description conflict and suppress the warning accordingly. The warning is emitted purely based on descriptor comparison, without considering configured Views. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning.  
  The warning message does not include any View recipe or suggestion for resolving the conflict through View configuration. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both Metric objects and emit a generic warning describing the duplicate instrument registration.  
  The SDK returns the first-registered instrument for duplicate names, so data is reported only for the first instrument, not both. The generic warning is emitted, but the 'pass through both Metric objects' behavior is not implemented. (`src/Метрики/Классы/ОтелМетр.os:54`)

- ❌ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax.  
  No instrument name validation is implemented in ОтелМетр. Instrument creation methods (СоздатьСчетчик, СоздатьГистограмму, etc.) accept any string as name without checking against the OTel instrument name syntax (alphanumeric, _, ., -, /, starting with letter). (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name.  
  Since no name validation exists, no error is emitted for invalid instrument names. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] The ExemplarReservoir SHOULD avoid allocations when sampling exemplars.  
  Reservoir always creates a new Соответствие (Map) for each exemplar in СоздатьЭкземпляр. OneScript lacks object pooling, so avoiding all allocations is impractical, but reservoir sampling itself (Algorithm R) is done without extra allocations. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:42`)

- ⚠️ **[Metrics Sdk]** [SHOULD] This implementation SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled.  
  Реализация использует стратегию 'последнее измерение заменяет предыдущее' (last-seen), а не reservoir sampling с равномерной вероятностью. Спецификация допускает этот вариант через MAY ('the implementation MAY instead keep the last seen measurement'), но SHOULD предпочитает sampling. (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50`)

- ❌ **[Metrics Sdk]** [SHOULD] Collect SHOULD invoke Produce on registered MetricProducers.  
  MetricProducer интерфейс не реализован. Нет механизма регистрации внешних MetricProducer'ов и вызова Produce при Collect. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] After the call to Shutdown, subsequent invocations to Collect are not allowed. SDKs SHOULD return some failure for these calls, if possible.  
  Метод ПериодическийСбор проверяет флаг Закрыт и прекращает цикл, но публичный метод СброситьБуфер (аналог Collect) не проверяет состояние Закрыт и не возвращает ошибку при вызове после Shutdown. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:59`)

- ⚠️ **[Metrics Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод Закрыть() является процедурой и не возвращает результат (успех/неуспех/таймаут). Внутри обрабатывает таймаут фонового задания через исключение, но вызывающий код не получает результат. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() является процедурой, не возвращает результат (успех/ошибка/таймаут). Ошибки экспорта перехватываются внутри через Попытка, но не транслируются вызывающему коду. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status.  
  СброситьБуфер() не возвращает статус ERROR/NO ERROR. Внутри экспортер возвращает Булево, но эта информация не пробрасывается вызывающему коду. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() вызывает СобратьИЭкспортировать() синхронно без таймаута. Нет механизма ограничения времени выполнения ForceFlush. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71`)

- ❌ **[Metrics Sdk]** [SHOULD] Metric Exporters SHOULD report an error condition for data output by the MetricReader with unsupported Aggregation or Aggregation Temporality.  
  Экспортер не проверяет неподдерживаемые типы агрегации или временности. Данные передаются на транспорт без валидации. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() является процедурой и не возвращает статус успеха/ошибки/таймаута. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers.  
  Это рекомендация к использованию, а не к реализации. Метод существует, но нет документации/ограничения на стороне SDK о том, когда его вызывать. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() синхронный no-op (нет буферизации), фактически завершается мгновенно, но нет механизма таймаута, если бы логика была сложнее. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43`)

- ❌ **[Metrics Sdk]** [SHOULD] MetricProducer implementations SHOULD accept configuration for the AggregationTemporality of produced metrics.  
  No MetricProducer exists, so there is no temporality configuration for it. The Prometheus reader does not accept AggregationTemporality configuration. (-)

- ⚠️ **[Otlp Exporter]** [SHOULD] The default protocol SHOULD be http/protobuf, unless there are strong reasons for SDKs to select grpc as the default.  
  Протокол по умолчанию http/json (строка 150: Параметр 'otel.exporter.otlp.protocol', 'http/json'), а не рекомендуемый http/protobuf. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ⚠️ **[Otlp Exporter]** [SHOULD] SDKs SHOULD support both grpc and http/protobuf transports.  
  Поддерживаются grpc (ОтелGrpcТранспорт) и http/json (ОтелHttpТранспорт). Транспорт http/protobuf не реализован. (`src/Экспорт/Классы/ОтелGrpcТранспорт.os:1`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If they support only one transport, it SHOULD be http/protobuf.  
  SDK поддерживает два транспорта (grpc и http/json), но ни один из них не является http/protobuf. (`src/Экспорт/Классы/ОтелHttpТранспорт.os:1`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If no configuration is provided the default transport SHOULD be http/protobuf unless SDKs have good reasons to choose grpc as the default.  
  Транспорт по умолчанию - http/json, а не рекомендуемый http/protobuf. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ❌ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter.  
  Ни HTTP-транспорт, ни gRPC-транспорт не устанавливают заголовок User-Agent. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The format of the User-Agent header SHOULD follow RFC 7231.  
  Заголовок User-Agent не реализован вообще. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The resulting User-Agent SHOULD include the exporter's default User-Agent string when a product identifier is added via configuration.  
  Заголовок User-Agent не реализован вообще, конфигурация product identifier отсутствует. (-)

- ❌ **[Propagators]** [SHOULD] If pre-configured, Propagators SHOULD default to a composite Propagator containing the W3C Trace Context Propagator and the Baggage Propagator specified in the Baggage API.  
  Реализация не предоставляет предконфигурированных пропагаторов по умолчанию. При отсутствии явной конфигурации ОтелГлобальный.ПолучитьПропагаторы() возвращает NoOp пропагатор, а не композитный пропагатор с W3C TraceContext + Baggage. (-)

- ❌ **[Env Vars]** [SHOULD] If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied.  
  Функция Включено() на строке 561-564 просто проверяет НРег(Значение) = "true" и возвращает Ложь для любого другого значения, но не логирует предупреждение при получении нестандартного значения (например "yes", "1"). (-)

- ⚠️ **[Env Vars]** [SHOULD] All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior.  
  Вместо стандартной OTEL_SDK_DISABLED (где false = SDK включен, безопасное значение по умолчанию) используется нестандартная OTEL_ENABLED (где true = SDK включен). Логика инвертирована относительно спецификации: в спеке disabled=false это безопасный дефолт, здесь enabled=true. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:7,562`)

- ❌ **[Env Vars]** [SHOULD] For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning.  
  Числовые параметры (строки 224-227, 263-266, 312, 395-416) конвертируются через Число() без try/catch. Если передана нечисловая строка, это вызовет исключение времени выполнения, а не предупреждение с graceful-игнорированием. (-)

- ❌ **[Env Vars]** [SHOULD] For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD gracefully ignore the setting, i.e., treat them as not set.  
  Вместо graceful-игнорирования некорректного числового значения, вызов Число() с невалидной строкой приведет к ошибке выполнения. Нет логики fallback на значение по умолчанию. (-)

- ❌ **[Env Vars]** [SHOULD] For new implementations, these should be treated as MUST requirements.  
  Так как предыдущие два SHOULD не реализованы, это meta-требование также не выполнено. (-)

- ⚠️ **[Env Vars]** [SHOULD] Enum values SHOULD be interpreted in a case-insensitive manner.  
  Пропагаторы обрабатываются case-insensitive (НРег на строке 344), но значения семплеров (строки 197-219) сравниваются case-sensitive (прямое сравнение без НРег). Аналогично exporter names (строки 177-178, 255-256, 291-292) сравниваются case-sensitive. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:344`)

## Детальный анализ по разделам (Stable)

### Context

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | A Context MUST be immutable | `src/Ядро/Модули/ОтелКонтекст.os:19` |  |
| 2 | MUST | ✅ found | its write operations MUST result in the creation of a new Context containing the original values and the specified values updated | `src/Ядро/Модули/ОтелКонтекст.os:127` |  |
| 3 | MUST | ✅ found | OpenTelemetry MUST provide its own Context implementation | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### Create a key

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#create-a-key)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The API MUST accept the following parameter: The key name | `src/Ядро/Модули/ОтелКонтекст.os:35` |  |
| 5 | SHOULD NOT | ✅ found | Multiple calls to CreateKey with the same name SHOULD NOT return the same value unless language constraints dictate otherwise | `src/Ядро/Модули/ОтелКонтекст.os:36` |  |
| 6 | MUST | ✅ found | The API MUST return an opaque object representing the newly created key | `src/Ядро/Классы/ОтелКлючКонтекста.os:1` |  |

#### Get value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The API MUST accept the following parameters: The Context, The key | `src/Ядро/Модули/ОтелКонтекст.os:113` |  |
| 8 | MUST | ✅ found | The API MUST return the value in the Context for the specified key | `src/Ядро/Модули/ОтелКонтекст.os:114` |  |

#### Set value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | The API MUST accept the following parameters: The Context, The key, The value to be set | `src/Ядро/Модули/ОтелКонтекст.os:127` |  |
| 10 | MUST | ✅ found | The API MUST return a new Context containing the new value | `src/Ядро/Модули/ОтелКонтекст.os:130` |  |

#### Optional Global operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#optional-global-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | These operations SHOULD only be used to implement automatic scope switching and define higher level APIs by SDK components and OpenTelemetry instrumentation libraries | `src/Ядро/Модули/ОтелКонтекст.os:203` |  |

#### Get current Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-current-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST return the Context associated with the caller's current execution unit | `src/Ядро/Модули/ОтелКонтекст.os:63` |  |

#### Attach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#attach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ⚠️ partial | The API MUST accept the following parameters: The Context. | `src/Ядро/Модули/ОтелКонтекст.os:203` | Attach-функциональность реализована через УстановитьЗначение(Ключ, Значение), которая создаёт новый контекст и кладёт его в стек. Но нет API, принимающего целый объект Context - вместо этого контекст собирается внутренне из отдельных key-value пар. |
| 14 | MUST | ✅ found | The API MUST return a value that can be used as a Token to restore the previous Context. | `src/Ядро/Модули/ОтелКонтекст.os:207` |  |

#### Detach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#detach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The API MUST accept the following parameters: A Token that was returned by a previous call to attach a Context. | `src/Ядро/Классы/ОтелОбласть.os:22` |  |

### Baggage Api

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Each name in Baggage MUST be associated with exactly one value. | `src/Ядро/Классы/ОтелBaggage.os:3` |  |
| 2 | SHOULD NOT | ✅ found | Language API SHOULD NOT restrict which strings are used as baggage names. | `src/Ядро/Классы/ОтелBaggage.os:38` |  |
| 3 | MUST | ✅ found | Language API MUST accept any valid UTF-8 string as baggage value in Set and return the same value from Get. | `src/Ядро/Классы/ОтелBaggage.os:68` |  |
| 4 | MUST | ✅ found | Language API MUST treat both baggage names and values as case sensitive. | `src/Ядро/Классы/ОтелBaggage.os:3` |  |
| 5 | MUST | ✅ found | The Baggage API MUST be fully functional in the absence of an installed SDK. | `src/Ядро/Классы/ОтелBaggage.os:1` |  |
| 6 | MUST | ✅ found | The Baggage container MUST be immutable, so that the containing Context also remains immutable. | `src/Ядро/Классы/ОтелBaggage.os:152` |  |

#### Operations### Get Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#operations-get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The Baggage API MUST provide a function that takes the name as input, and returns a value associated with the given name, or null if the given name is not present. | `src/Ядро/Классы/ОтелBaggage.os:38` |  |

#### Get All Values

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#get-all-values)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST NOT | ✅ found | The order of name/value pairs MUST NOT be significant. Based on the language specifics, the returned value can be either an immutable collection or an iterator on the immutable collection of name/value pairs in the Baggage. | `src/Ядро/Классы/ОтелBaggage.os:103` |  |

#### Set Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | The Baggage API MUST provide a function which takes a name, and a value as input. Returns a new Baggage that contains the new value. | `src/Ядро/Классы/ОтелBaggage.os:68` |  |

#### Remove Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#remove-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | To delete a name/value pair, the Baggage API MUST provide a function which takes a name as input. Returns a new Baggage which no longer contains the selected name. | `src/Ядро/Классы/ОтелBaggage.os:82` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | If an implementation of this API does not operate directly on the Context, it MUST provide the following functionality to interact with a Context instance: Extract the Baggage from a Context instance; Insert the Baggage to a Context instance. | `src/Ядро/Модули/ОтелКонтекст.os:156` |  |
| 12 | SHOULD NOT | ⚠️ partial | API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:53` | Удобные методы BaggageИзКонтекста/КонтекстСBaggage существуют, но ключ контекста КлючBaggage также публично доступен через экспортную функцию КлючBaggage() |
| 13 | SHOULD | ✅ found | If the language has support for implicitly propagated Context, the API SHOULD also provide the following functionality: Get the currently active Baggage from the implicit context; Set the currently active Baggage to the implicit context. | `src/Ядро/Классы/ОтелBaggage.os:16` |  |
| 14 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Классы/ОтелBaggage.os:16` |  |

#### Clear Baggage in the Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#clear-baggage-in-the-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The Baggage API MUST provide a way to remove all baggage entries from a context. | `src/Ядро/Классы/ОтелBaggage.os:94` |  |

#### Propagation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#propagation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The API layer or an extension package MUST include the following Propagators: A TextMapPropagator implementing the W3C Baggage Specification. | `src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:1` |  |

#### Conflict Resolution

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#conflict-resolution)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | If a new name/value pair is added and its name is the same as an existing name, then the new pair MUST take precedence. The value is replaced with the added value (regardless of whether it is locally generated or received from a remote peer). | `src/Ядро/Классы/ОтелПостроительBaggage.os:24` |  |

### Resource Sdk

#### Resource SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The SDK MUST allow for creation of Resources and for associating them with telemetry. | `src/Ядро/Классы/ОтелРесурс.os:94` |  |
| 2 | MUST | ✅ found | When associated with a TracerProvider, all Spans produced by any Tracer from the provider MUST be associated with this Resource. | `src/Трассировка/Классы/ОтелТрассировщик.os:83` |  |

#### SDK-provided resource attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#sdk-provided-resource-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The SDK MUST provide access to a Resource with at least the attributes listed at Semantic Attributes with SDK-provided Default Value. | `src/Ядро/Классы/ОтелРесурс.os:102` |  |
| 4 | MUST | ✅ found | This resource MUST be associated with a TracerProvider or MeterProvider if another resource was not explicitly specified. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:253` |  |

#### Create

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#create)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The interface MUST provide a way to create a new resource, from Attributes. | `src/Ядро/Классы/ОтелРесурс.os:94` |  |
| 6 | MUST | ✅ found | The interface MUST provide a way for an old resource and an updating resource to be merged into a new resource. | `src/Ядро/Классы/ОтелРесурс.os:39` |  |
| 7 | MUST | ✅ found | The resulting resource MUST have all attributes that are on any of the two input resources. | `src/Ядро/Классы/ОтелРесурс.os:53` |  |
| 8 | MUST | ✅ found | If a key exists on both the old and updating resource, the value of the updating resource MUST be picked (even if the updated value is empty). | `src/Ядро/Классы/ОтелРесурс.os:56` |  |

#### Detecting resource information from the environment

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#detecting-resource-information-from-the-environment)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ⚠️ partial | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1` | Детекторы реализованы как отдельные классы (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора), но находятся в том же пакете src/Ядро/, а не в отдельных пакетах от SDK |
| 10 | MUST | ✅ found | Resource detector packages MUST provide a method that returns a resource. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17` |  |
| 11 | MUST NOT | ✅ found | Failure to detect any resource information MUST NOT be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:19` |  |
| 12 | SHOULD | ⚠️ partial | An error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:24` | Ошибки при обнаружении ресурсов перехватываются, но логируются на уровне Отладка (Debug), а не как ошибки (Error) согласно спецификации |
| 13 | MUST | ❌ not_found | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions. | - | Детекторы заполняют атрибуты семантических конвенций (host.name, os.type, process.pid, host.arch и др.), но не устанавливают Schema URL в возвращаемом ресурсе |
| 14 | SHOULD | ⚠️ partial | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18` | Детекторы используют пустой Schema URL, но при этом заполняют известные атрибуты семантических конвенций (host.name, os.type и др.) - в этом случае по спецификации должен быть установлен соответствующий Schema URL |
| 15 | MUST | ⚠️ partial | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources. | `src/Ядро/Классы/ОтелРесурс.os:41` | Метод Слить() корректно обрабатывает конфликт Schema URL (строки 41-44), однако комбинирование детекторов в ЗаполнитьАтрибутыПоУмолчанию (строки 113-118) копирует атрибуты напрямую без использования Слить() и без проверки Schema URL |

### Trace Api

#### Timestamp

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#timestamp)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD provide a way to set/register and access a global default TracerProvider. | `src/Ядро/Модули/ОтелГлобальный.os:31` |  |
| 2 | SHOULD | ✅ found | Implementations of TracerProvider SHOULD allow creating an arbitrary number of TracerProvider instances. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:244` |  |

#### TracerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The TracerProvider MUST provide the following functions: Get a Tracer | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 4 | MUST | ✅ found | This API MUST accept the following parameters: name (required) | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 5 | SHOULD | ✅ found | name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 6 | MUST | ⚠️ partial | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` | ПолучитьТрассировщик принимает пустую строку и создаёт ОтелОбластьИнструментирования с ней, возвращая рабочий Tracer. Однако нет явной проверки на null/пустую строку с логированием предупреждения. |
| 7 | SHOULD | ⚠️ partial | its name property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` | Имя устанавливается как есть (будет пустой строкой), но предупреждение о невалидном имени не логируется. |
| 8 | SHOULD | ⚠️ partial | a message reporting that the specified value is invalid SHOULD be logged | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` | Нет логирования предупреждения при пустом или null имени. |
| 9 | MUST NOT | ✅ found | Implementations MUST NOT require users to repeatedly obtain a Tracer again with the same identity to pick up configuration changes. | `src/Трассировка/Классы/ОтелТрассировщик.os:193` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API MUST provide the following functionality to interact with a Context instance: Extract the Span from a Context instance; Combine the Span with a Context instance, creating a new Context instance | `src/Ядро/Модули/ОтелКонтекст.os:141` |  |
| 11 | SHOULD NOT | ✅ found | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:362` |  |
| 12 | SHOULD | ✅ found | If the language has support for implicitly propagated Context, the API SHOULD also provide the following functionality: Get the currently active span from the implicit context; Set the currently active span into a new context, and make that the implicit context. | `src/Ядро/Модули/ОтелКонтекст.os:90` |  |
| 13 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:219` |  |

#### SpanContext

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spancontext)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The API MUST implement methods to create a SpanContext. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |
| 15 | SHOULD | ✅ found | These methods SHOULD be the only way to create a SpanContext. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |
| 16 | MUST | ✅ found | This functionality MUST be fully implemented in the API. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |
| 17 | SHOULD NOT | ✅ found | This functionality SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |

#### Retrieving the TraceId and SpanId

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#retrieving-the-traceid-and-spanid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | The API MUST allow retrieving the TraceId and SpanId in the following forms: Hex - returns the lowercase hex encoded TraceId or SpanId. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 19 | MUST | ✅ found | TraceId hex result MUST be a 32-hex-character lowercase string. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 20 | MUST | ✅ found | SpanId hex result MUST be a 16-hex-character lowercase string. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:32` |  |
| 21 | MUST | ✅ found | Binary - returns the binary representation of the TraceId (result MUST be a 16-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:82` |  |
| 22 | MUST | ✅ found | Binary - returns the binary representation of the SpanId (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:91` |  |
| 23 | SHOULD NOT | ✅ found | The API SHOULD NOT expose details about how they are internally stored. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:4` |  |

#### IsValid

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isvalid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | An API called IsValid, that returns a boolean value, which is true if the SpanContext has a non-zero TraceID and a non-zero SpanID, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:70` |  |

#### IsRemote

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isremote)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | An API called IsRemote, that returns a boolean value, which is true if the SpanContext was propagated from a remote parent, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:60` |  |
| 26 | MUST | ✅ found | When extracting a SpanContext through the Propagators API, IsRemote MUST return true. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:126` |  |
| 27 | MUST | ✅ found | For the SpanContext of any child spans it MUST return false. | `src/Трассировка/Классы/ОтелСпан.os:600` |  |

#### TraceState

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracestate)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | Tracing API MUST provide at least the following operations on TraceState: Get value for a given key, Add a new key/value pair, Update an existing value for a given key, Delete a key/value pair | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:44,66,105` |  |
| 29 | MUST | ✅ found | These operations MUST follow the rules described in the W3C Trace Context specification | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:227-386` |  |
| 30 | MUST | ✅ found | All mutating operations MUST return a new TraceState with the modifications applied | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:92-94,114-116` |  |
| 31 | MUST | ✅ found | TraceState MUST at all times be valid according to rules specified in W3C Trace Context specification | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:227-386` |  |
| 32 | MUST | ✅ found | Every mutating operations MUST validate input parameters | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 33 | MUST NOT | ✅ found | If invalid value is passed the operation MUST NOT return TraceState containing invalid data | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67-68` |  |
| 34 | MUST | ✅ found | If invalid value is passed the operation MUST follow the general error handling guidelines | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67-68` |  |

#### Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | SHOULD | ✅ found | The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable | `src/Трассировка/Классы/ОтелСпан.os:564` |  |
| 36 | SHOULD | ✅ found | Generality SHOULD be prioritized over human-readability | - |  |
| 37 | SHOULD | ✅ found | A Span's start time SHOULD be set to the current time on span creation | `src/Трассировка/Классы/ОтелСпан.os:609` |  |
| 38 | SHOULD | ✅ found | After the Span is created, it SHOULD be possible to change its name, set its Attributes, add Events, and set the Status | `src/Трассировка/Классы/ОтелСпан.os:247,263,293,413` |  |
| 39 | MUST NOT | ✅ found | These (name, Attributes, Events, Status) MUST NOT be changed after the Span's end time has been set | `src/Трассировка/Классы/ОтелСпан.os:248,264,294,414` |  |
| 40 | SHOULD NOT | ✅ found | Implementations SHOULD NOT provide access to a Span's attributes besides its SpanContext | `src/Трассировка/Классы/ОтелСпан.os:134` |  |
| 41 | MUST NOT | ✅ found | Alternative implementations MUST NOT allow callers to create Spans directly | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 42 | MUST | ✅ found | All Spans MUST be created via a Tracer | `src/Трассировка/Классы/ОтелТрассировщик.os:56,106,133` |  |

#### Span Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Span other than with a Tracer | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 44 | MUST NOT | ✅ found | In languages with implicit Context propagation, Span creation MUST NOT set the newly created Span as the active Span in the current Context by default | `src/Трассировка/Классы/ОтелТрассировщик.os:56-95` |  |
| 45 | MUST | ✅ found | The API MUST accept the following parameters: The span name (required), parent Context, SpanKind, Attributes, Links, Start timestamp | `src/Трассировка/Классы/ОтелПостроительСпана.os:33,60,76,92,109` |  |
| 46 | MUST NOT | ⚠️ partial | This API MUST NOT accept a Span or SpanContext as parent, only a full Context | `src/Трассировка/Классы/ОтелТрассировщик.os:133` | НачатьДочернийСпан принимает ОтелСпан или ОтелКонтекстСпана напрямую, а не полный Context. Построитель УстановитьРодителя также принимает Span/SpanContext, а не Context |
| 47 | MUST | ✅ found | The semantic parent of the Span MUST be determined according to the rules described in Determining the Parent Span from a Context | `src/Трассировка/Классы/ОтелТрассировщик.os:57-69` |  |
| 48 | MUST | ✅ found | The API documentation MUST state that adding attributes at span creation is preferred to calling SetAttribute later, as samplers can only consider information already present during span creation | `src/Трассировка/Классы/ОтелПостроительСпана.os:66-67` |  |
| 49 | SHOULD | ✅ found | Start timestamp, default to current time. This argument SHOULD only be set when span creation time has already passed | `src/Трассировка/Классы/ОтелПостроительСпана.os:109` |  |
| 50 | MUST NOT | ✅ found | If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument | `src/Трассировка/Классы/ОтелПостроительСпана.os:100-101` |  |
| 51 | MUST | ✅ found | Implementations MUST provide an option to create a Span as a root span | `src/Трассировка/Классы/ОтелТрассировщик.os:106` |  |
| 52 | MUST | ✅ found | Implementations MUST generate a new TraceId for each root span created | `src/Трассировка/Классы/ОтелТрассировщик.os:107` |  |
| 53 | MUST | ✅ found | For a Span with a parent, the TraceId MUST be the same as the parent | `src/Трассировка/Классы/ОтелТрассировщик.os:61,140` |  |
| 54 | MUST | ✅ found | The child span MUST inherit all TraceState values of its parent by default | `src/Трассировка/Классы/ОтелТрассировщик.os:230-238` |  |
| 55 | MUST | ✅ found | Any span that is created MUST also be ended. This is the responsibility of the user | `src/Трассировка/Классы/ОтелСпан.os:447` |  |

#### Specifying links

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#specifying-links)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 56 | MUST | ✅ found | During Span creation, a user MUST have the ability to record links to other Spans | `src/Трассировка/Классы/ОтелПостроительСпана.os:92` |  |

#### Get Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 57 | MUST | ✅ found | The Span interface MUST provide an API that returns the SpanContext for the given Span | `src/Трассировка/Классы/ОтелСпан.os:80` |  |
| 58 | MUST | ✅ found | The returned value MUST be the same for the entire Span lifetime | `src/Трассировка/Классы/ОтелСпан.os:80-82` |  |
| 59 | SHOULD | ✅ found | After a Span is ended, it SHOULD become non-recording and IsRecording SHOULD always return false | `src/Трассировка/Классы/ОтелСпан.os:234-236` |  |
| 60 | SHOULD | ✅ found | IsRecording SHOULD always return false after a Span is ended | `src/Трассировка/Классы/ОтелСпан.os:234-236` |  |
| 61 | SHOULD NOT | ✅ found | IsRecording SHOULD NOT take any parameters | `src/Трассировка/Классы/ОтелСпан.os:234` |  |
| 62 | SHOULD | ✅ found | This flag (IsRecording) SHOULD be used to avoid expensive computations of a Span attributes or events in case when a Span is definitely not recorded | `src/Трассировка/Классы/ОтелПостроительСпана.os:129` |  |

#### Set Attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 63 | MUST | ✅ found | A Span MUST have the ability to set Attributes associated with it | `src/Трассировка/Классы/ОтелСпан.os:263` |  |
| 64 | MUST | ✅ found | The Span interface MUST provide an API to set a single Attribute where the attribute properties are passed as arguments | `src/Трассировка/Классы/ОтелСпан.os:263` |  |
| 65 | SHOULD | ✅ found | Setting an attribute with the same key as an existing attribute SHOULD overwrite the existing attribute's value | `src/Трассировка/Классы/ОтелСпан.os:278` |  |

#### Add Events

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-events)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | MUST | ✅ found | A Span MUST have the ability to add events. Events have a time associated with the moment when they are added to the Span | `src/Трассировка/Классы/ОтелСпан.os:293` |  |
| 67 | MUST | ✅ found | The Span interface MUST provide an API to record a single Event where the Event properties are passed as arguments | `src/Трассировка/Классы/ОтелСпан.os:293` |  |
| 68 | SHOULD | ✅ found | Events SHOULD preserve the order in which they are recorded | `src/Трассировка/Классы/ОтелСпан.os:297` |  |

#### Add Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | MUST | ✅ found | A Span MUST have the ability to add Links associated with it after its creation | `src/Трассировка/Классы/ОтелСпан.os:361` |  |

#### Set Status

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-status)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 70 | MUST | ✅ found | Description MUST only be used with the Error StatusCode value. | `src/Трассировка/Классы/ОтелСпан.os:429` |  |
| 71 | MUST | ✅ found | The Span interface MUST provide an API to set the Status. | `src/Трассировка/Классы/ОтелСпан.os:413` |  |
| 72 | SHOULD | ⚠️ partial | This SHOULD be called SetStatus. | `src/Трассировка/Классы/ОтелСпан.os:413` | Метод называется УстановитьСтатус, что является русским переводом SetStatus. Семантически верно, но имя отличается от спеки. |
| 73 | MUST | ✅ found | Description MUST be IGNORED for StatusCode Ok & Unset values. | `src/Трассировка/Классы/ОтелСпан.os:429` |  |
| 74 | SHOULD | ✅ found | The status code SHOULD remain unset, except for the following circumstances. | `src/Трассировка/Классы/ОтелСпан.os:614` |  |
| 75 | SHOULD | ✅ found | An attempt to set value Unset SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:424` |  |
| 76 | SHOULD | ❌ not_found | When the status is set to Error by Instrumentation Libraries, the Description SHOULD be documented and predictable. | - | Нет документации по предсказуемым значениям Description для ошибок, устанавливаемых инструментирующими библиотеками. |
| 77 | SHOULD | ❌ not_found | Instrumentation Libraries SHOULD publish their own conventions for Description values, including possible values and what they mean. | - | Нет публикации конвенций по значениям Description для ошибок. |
| 78 | SHOULD NOT | ✅ found | Instrumentation Libraries SHOULD NOT set the status code to Ok, unless explicitly configured to do so. | `src/Трассировка/Классы/ОтелСпан.os:413` |  |
| 79 | SHOULD | ✅ found | Instrumentation Libraries SHOULD leave the status code as Unset unless there is an error. | `src/Трассировка/Классы/ОтелСпан.os:614` |  |
| 80 | SHOULD | ✅ found | When span status is set to Ok it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 81 | SHOULD | ✅ found | Any further attempts to change Ok status SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 82 | SHOULD | ❌ not_found | Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generate. | - | Это требование относится к инструментам анализа, а не к SDK, но в кодовой базе нет инструментов анализа, подавляющих ошибки при Ok-статусе. |

#### UpdateName

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#updatename)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 83 | SHOULD | ✅ found | Implementations SHOULD ignore all subsequent calls to End and any other Span methods, i.e. the Span becomes non-recording by being ended. | `src/Трассировка/Классы/ОтелСпан.os:448` |  |
| 84 | MUST | ✅ found | All API implementations of methods that end the span MUST internally call the End method and be documented to do so. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 85 | MUST NOT | ✅ found | End MUST NOT have any effects on child spans. Those may still be running and can be ended later. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 86 | MUST NOT | ✅ found | End MUST NOT inactivate the Span in any Context it is active in. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 87 | MUST | ✅ found | It MUST still be possible to use an ended span as parent via a Context it is contained in. Also, any mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:80` |  |
| 88 | MUST | ✅ found | If end timestamp is omitted, this MUST be treated equivalent to passing the current time. | `src/Трассировка/Классы/ОтелСпан.os:449` |  |
| 89 | MUST NOT | ✅ found | This operation itself MUST NOT perform blocking I/O on the calling thread. | `src/Трассировка/Классы/ОтелСпан.os:454` |  |
| 90 | SHOULD | ✅ found | Any locking used needs be minimized and SHOULD be removed entirely if possible. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 91 | MUST | ✅ found | Mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:398` |  |

#### Record Exception

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#record-exception)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 92 | SHOULD | ✅ found | To facilitate recording an exception languages SHOULD provide a RecordException method if the language uses exceptions. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 93 | MUST | ✅ found | The method MUST record an exception as an Event with the conventions outlined in the exceptions document. | `src/Трассировка/Классы/ОтелСпан.os:322` |  |
| 94 | SHOULD | ✅ found | The minimum required argument SHOULD be no more than only an exception object. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 95 | MUST | ✅ found | If RecordException is provided, the method MUST accept an optional parameter to provide any additional event attributes. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 96 | SHOULD | ✅ found | Accepting additional attributes SHOULD be done in the same way as for the AddEvent method. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |

#### Span lifetime

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-lifetime)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | MUST | ✅ found | Start and end time as well as Event's timestamps MUST be recorded at a time of a calling of corresponding API. | `src/Трассировка/Классы/ОтелСпан.os:609` |  |

#### Wrapping a SpanContext in a Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#wrapping-a-spancontext-in-a-span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | MUST | ✅ found | The API MUST provide an operation for wrapping a SpanContext with an object implementing the Span interface. | `src/Трассировка/Классы/ОтелНоопСпан.os:272` |  |
| 99 | SHOULD NOT | ⚠️ partial | If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | ОтелНоопСпан является публичным классом, зарегистрированным в lib.config, хотя спека рекомендует не экспонировать его публично. |
| 100 | SHOULD | ⚠️ partial | If a new type is required to be publicly exposed, it SHOULD be named NonRecordingSpan. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | Класс назван ОтелНоопСпан вместо рекомендуемого NonRecordingSpan (или ОтелНеЗаписывающийСпан). Нооп - не то же самое что NonRecording. |
| 101 | MUST | ✅ found | GetContext MUST return the wrapped SpanContext. | `src/Трассировка/Классы/ОтелНоопСпан.os:29` |  |
| 102 | MUST | ✅ found | IsRecording MUST return false to signal that events, attributes and other elements are not being recorded. | `src/Трассировка/Классы/ОтелНоопСпан.os:155` |  |
| 103 | MUST | ✅ found | The remaining functionality of Span MUST be defined as no-op operations. | `src/Трассировка/Классы/ОтелНоопСпан.os:167` |  |
| 104 | MUST | ✅ found | This functionality MUST be fully implemented in the API. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |
| 105 | SHOULD NOT | ✅ found | This functionality SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |

#### SpanKind

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 106 | SHOULD | ✅ found | In order for SpanKind to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose. | `src/Трассировка/Модули/ОтелВидСпана.os:1` |  |
| 107 | SHOULD NOT | ✅ found | A server-side span SHOULD NOT be used to describe outgoing remote procedure call. | `src/Трассировка/Модули/ОтелВидСпана.os:23` |  |
| 108 | MUST | ✅ found | A user MUST have the ability to record links to other SpanContexts. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 109 | MUST | ✅ found | The API MUST provide an API to record a single Link where the Link properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 110 | SHOULD | ⚠️ partial | Implementations SHOULD record links containing SpanContext with empty TraceId or SpanId (all zeros) as long as either the attribute set or TraceState is non-empty. | `src/Трассировка/Классы/ОтелСпан.os:361` | ДобавитьЛинк не проверяет валидность SpanContext и принимает любой, что частично покрывает требование, но нет явной логики проверки empty TraceId/SpanId с non-empty attributes/TraceState. |
| 111 | SHOULD | ✅ found | Span SHOULD preserve the order in which Links are set. | `src/Трассировка/Классы/ОтелСпан.os:613` |  |
| 112 | MUST | ❌ not_found | The API documentation MUST state that adding links at span creation is preferred to calling AddLink later, for contexts that are available during span creation, because head sampling decisions can only consider information present during span creation. | - | В документации метода ДобавитьЛинк нет явного указания, что добавление линков при создании спана предпочтительно. Есть комментарий в ОтелПостроительСпана.os:81, но нет такого предупреждения в самом API ДобавитьЛинк. |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 113 | MUST | ✅ found | TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:6` |  |
| 114 | MUST | ✅ found | Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:3` |  |
| 115 | MUST | ✅ found | Span - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:3` |  |
| 116 | MUST | ✅ found | Event - Events are immutable and MUST be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСобытиеСпана.os:3` |  |
| 117 | SHOULD | ⚠️ partial | Link - Links are immutable and SHOULD be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:372` | Линки представлены как Соответствие (mutable), а не как отдельный иммутабельный класс. Нет документации об их потокобезопасности. |

#### Behavior of the API in the absence of an installed SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#behavior-of-the-api-in-the-absence-of-an-installed-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 118 | MUST | ✅ found | The API MUST return a non-recording Span with the SpanContext in the parent Context (whether explicitly given or implicit current). | `src/Трассировка/Классы/ОтелТрассировщик.os:71` |  |
| 119 | SHOULD | ❌ not_found | If the Span in the parent Context is already non-recording, it SHOULD be returned directly without instantiating a new Span. | - | В НачатьСпан нет проверки, является ли родительский спан уже non-recording. Всегда создается новый ОтелНоопСпан даже если родитель уже non-recording. |
| 120 | MUST | ✅ found | If the parent Context contains no Span, an empty non-recording Span MUST be returned instead (having a SpanContext with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags). | `src/Трассировка/Классы/ОтелНоопСпан.os:277` |  |

### Trace Sdk

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, Sampler, and TracerConfigurator) MUST be owned by the TracerProvider | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:11` | SpanProcessors, SpanLimits, Sampler, TracerConfigurator are owned by TracerProvider. However, IdGenerator is not configurable - ID generation is hardcoded in ОтелУтилиты utility module, not owned by TracerProvider |
| 2 | MUST | ✅ found | The updated configuration MUST also apply to all already returned Tracers (i.e. it MUST NOT matter whether a Tracer was obtained from the TracerProvider before or after the configuration change) | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |
| 3 | MUST NOT | ✅ found | it MUST NOT matter whether a Tracer was obtained from the TracerProvider before or after the configuration change | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ❌ not_found | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out | - | СброситьБуфер() is a Процедура (void return), provides no indication of success, failure, or timeout to the caller |
| 5 | SHOULD | ❌ not_found | ForceFlush SHOULD complete or abort within some timeout | - | СброситьБуфер() has no timeout mechanism - it blocks indefinitely while iterating over processors |
| 6 | MUST | ✅ found | ForceFlush MUST invoke ForceFlush on all registered SpanProcessors | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:99` |  |

#### Additional Span Interfaces

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#additional-span-interfaces)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | Readable span: A function receiving this as argument MUST be able to access all information that was added to the span, as listed in the API spec for Span | `src/Трассировка/Классы/ОтелСпан.os:71` |  |
| 8 | MUST | ✅ found | A function receiving this as argument MUST be able to access the InstrumentationScope and Resource information (implicitly) associated with the span | `src/Трассировка/Классы/ОтелСпан.os:161` |  |
| 9 | MUST | ✅ found | For backwards compatibility it MUST also be able to access the InstrumentationLibrary having the same name and version values as the InstrumentationScope | `src/Трассировка/Классы/ОтелСпан.os:170` |  |
| 10 | MUST | ✅ found | A function receiving this as argument MUST be able to reliably determine whether the Span has ended | `src/Трассировка/Классы/ОтелСпан.os:197` |  |
| 11 | MUST | ✅ found | Counts for attributes, events and links dropped due to collection limits MUST be available for exporters to report as described in the exporters specification | `src/Трассировка/Классы/ОтелСпан.os:206` |  |
| 12 | MUST | ⚠️ partial | Implementations MUST expose at least the full parent SpanContext | `src/Трассировка/Классы/ОтелСпан.os:89` | Only ИдРодительскогоСпана() (parent span ID string) is exposed. The full parent SpanContext (including TraceId, TraceFlags, TraceState) is not stored or accessible - only the parent span ID is preserved |
| 13 | MUST | ✅ found | It MUST be possible for functions being called with Read/write span to somehow obtain the same Span instance and type that the span creation API returned | `src/Трассировка/Классы/ОтелСпан.os:640` |  |

#### Sampling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | Span Processor MUST receive only those spans which have IsRecording field set to true | `src/Трассировка/Классы/ОтелТрассировщик.os:71-74` |  |
| 15 | SHOULD NOT | ⚠️ partial | Span Exporter SHOULD NOT receive spans unless the Sampled flag was also set | `src/Трассировка/Классы/ОтелТрассировщик.os:71-94` | When sampler returns DROP, a NoOp span is created and never reaches the processor/exporter. When RECORD_ONLY, the span IS passed to the processor (line 639-641 of ОтелСпан.os) and then to the exporter (ПриЗавершении). There is no explicit check in the processor/exporter chain to filter out spans with Sampled=false but IsRecording=true (RECORD_ONLY). The SimpleSpanProcessor and BatchSpanProcessor forward all spans they receive to the exporter without checking the Sampled flag. |
| 16 | MUST | ⚠️ partial | Span Exporters MUST receive those spans which have Sampled flag set to true | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37-50` | Spans with RECORD_AND_SAMPLE (Sampled=true) do reach the exporter via the processor chain. However, there is no explicit Sampled flag check - it works only because DROP spans never reach processors. The spec's intent is satisfied for the RECORD_AND_SAMPLE case but not explicitly verified. |
| 17 | SHOULD NOT | ⚠️ partial | Span Exporters SHOULD NOT receive spans that do not have Sampled flag set | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37-50` | There is no filtering in processors or exporters based on the Sampled flag. Spans with RECORD_ONLY decision (IsRecording=true, Sampled=false) would be passed to the exporter. The processor does not check ФлагиТрассировки before forwarding to exporter. |
| 18 | MUST NOT | ✅ found | The OpenTelemetry SDK MUST NOT allow the combination SampledFlag == true and IsRecording == false | `src/Трассировка/Классы/ОтелТрассировщик.os:213-218` |  |

#### SDK Span creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sdk-span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | When asked to create a Span, the SDK MUST act as if doing the following in order: use valid parent trace ID or generate new one (before ShouldSample), query Sampler's ShouldSample, generate new span ID independently of sampling decision, create span depending on ShouldSample decision | `src/Трассировка/Классы/ОтелТрассировщик.os:56-94` |  |

#### ShouldSample

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shouldsample)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ⚠️ partial | If the parent SpanContext contains a valid TraceId, they MUST always match (ShouldSample TraceId argument must match parent's TraceId) | `src/Трассировка/Классы/ОтелТрассировщик.os:61` | The tracer uses the parent's TraceId directly (line 61: ИдТрассировки = КонтекстРодителяСпана.ИдТрассировки()), so they always match by construction. However, the ДолженСэмплировать method itself does not explicitly validate this constraint - it accepts ИдТрассировки as a parameter without checking it against parent context. |
| 21 | MUST NOT | ✅ found | RECORD_ONLY - IsRecording will be true, but the Sampled flag MUST NOT be set | `src/Трассировка/Классы/ОтелТрассировщик.os:213-218` |  |
| 22 | MUST | ✅ found | RECORD_AND_SAMPLE - IsRecording will be true and the Sampled flag MUST be set | `src/Трассировка/Классы/ОтелТрассировщик.os:213-218` |  |
| 23 | SHOULD | ✅ found | Samplers SHOULD normally return the passed-in Tracestate if they do not intend to change it | `src/Трассировка/Классы/ОтелРезультатСэмплирования.os:75-88` |  |
| 24 | SHOULD NOT | ❌ not_found | Callers SHOULD NOT cache the returned value of GetDescription | - | This is a guidance for callers, not an implementation requirement. The Описание() method exists (ОтелСэмплер.os:106-122) but there is no mechanism or documentation preventing callers from caching the result. |

#### TraceID randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#traceid-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | SHOULD | ⚠️ partial | For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 when generating TraceID values | `src/Ядро/Модули/ОтелУтилиты.os:78-92` | TraceIDs are generated using УникальныйИдентификатор (UUID v4), which provides randomness, but there is no explicit verification that the generated IDs meet W3C Trace Context Level 2 requirements for 56 bits of randomness in the rightmost 7 bytes. UUID v4 has 122 random bits total but the randomness distribution across specific byte positions may not match the W3C requirement exactly. |

#### Random trace flag

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#random-trace-flag)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | SHOULD | ❌ not_found | For root span contexts, the SDK SHOULD set the Random flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements | - | The trace flags handling in the SDK only deals with the Sampled flag (bit 0). There is no implementation of the Random flag (bit 1 of W3C Trace Context Level 2). ВычислитьФлагиТрассировки() in ОтелТрассировщик.os only returns 0 or 1 based on sampling decision, never setting the Random flag. |

#### Explicit randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#explicit-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 27 | MUST NOT | ❌ not_found | SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value (rv sub-key) | - | There is no handling of the OpenTelemetry TraceState rv sub-key anywhere in the sampler or SDK code. The ОтелСостояниеТрассировки class handles generic key-value pairs but has no awareness of OpenTelemetry-specific sub-keys like rv or ot. |
| 28 | SHOULD | ❌ not_found | For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the rv sub-key of the OpenTelemetry TraceState | - | The sampler does not inspect or use the rv sub-key of TraceState. It always uses TraceID-based hashing without considering explicit randomness values. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | SHOULD | ⚠️ partial | If the SDK uses an IdGenerator extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated | `src/Ядро/Модули/ОтелУтилиты.os:54-65` | The SDK provides an IdGenerator extension point (УстановитьГенераторИд) that allows custom generators for TraceId and SpanId. However, the extension point does not include any mechanism for the generator to indicate whether generated IDs meet randomness requirements or to control the Random trace flag. The ВычислитьФлагиТрассировки() method in the tracer does not consult the ID generator about the Random flag. |

#### Span Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | Span attributes MUST adhere to the common rules of attribute limits. | `src/Трассировка/Классы/ОтелСпан.os:266` |  |
| 31 | MUST | ✅ found | If the SDK implements the limits above it MUST provide a way to change these limits, via a configuration to the TracerProvider, by allowing users to configure individual limits. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:83` |  |
| 32 | SHOULD | ✅ found | The name of the configuration options SHOULD be EventCountLimit and LinkCountLimit. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:34` |  |
| 33 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called SpanLimits. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:1` |  |
| 34 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute, event, or link was discarded due to such a limit. | `src/Трассировка/Классы/ОтелСпан.os:468` |  |
| 35 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per discarded attribute, event, or link). | `src/Трассировка/Классы/ОтелСпан.os:469` |  |

#### Id Generators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#id-generators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | The SDK MUST by default randomly generate both the TraceId and the SpanId. | `src/Ядро/Модули/ОтелУтилиты.os:78` |  |
| 37 | MUST | ✅ found | The SDK MUST provide a mechanism for customizing the way IDs are generated for both the TraceId and the SpanId. | `src/Ядро/Модули/ОтелУтилиты.os:63` |  |
| 38 | MUST | ⚠️ partial | Name of the methods MUST be consistent with SpanContext (one to generate a SpanId and one for TraceId). | `src/Ядро/Модули/ОтелУтилиты.os:78` | Methods are named СгенерироватьИдТрассировки/СгенерироватьИдСпана which are consistent in Russian naming but there is no formal IdGenerator interface class - the contract is duck-typed via comments in ОтелУтилиты. |
| 39 | MUST NOT | ✅ found | Additional IdGenerator implementing vendor-specific protocols such as AWS X-Ray trace id generator MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | - |  |

#### Span processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 40 | MUST | ✅ found | SDK MUST allow to end each pipeline with individual exporter. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:85` |  |
| 41 | MUST | ✅ found | SDK MUST allow users to implement and configure custom processors. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:1` |  |
| 42 | MUST | ✅ found | The SpanProcessor interface MUST declare the following methods: OnStart, OnEnd, Shutdown, ForceFlush. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11` |  |
| 43 | SHOULD | ✅ found | The SpanProcessor interface SHOULD declare the following methods: OnEnding method. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:21` |  |
| 44 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it (OnStart parameter). | `src/Трассировка/Классы/ОтелСпан.os:639` |  |
| 45 | SHOULD | ✅ found | Updates to the span SHOULD be reflected in it (the span object passed to OnStart). | `src/Трассировка/Классы/ОтелСпан.os:639` |  |

#### OnEnd(Span)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onendspan)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | MUST | ✅ found | This method MUST be called synchronously within the Span.End() API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |

#### Shutdown()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | SHOULD | ⚠️ partial | Shutdown SHOULD be called only once for each SpanProcessor instance. After the call to Shutdown, subsequent calls to OnStart, OnEnd, or ForceFlush are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43` | BatchSpanProcessor checks Закрыт flag in Обработать() and returns early, but SimpleSpanProcessor (ОтелПростойПроцессорСпанов) does not track shutdown state - Закрыть() just closes the exporter without setting any flag to prevent subsequent OnStart/OnEnd/ForceFlush calls. |
| 48 | SHOULD | ❌ not_found | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Закрыть() in both SimpleSpanProcessor and BatchSpanProcessor (via ОтелБазовыйПакетныйПроцессор) is a Процедура (void), it does not return success/failure/timeout status. |
| 49 | MUST | ✅ found | Shutdown MUST include the effects of ForceFlush. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:77` |  |
| 50 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192` | BatchSpanProcessor uses ТаймаутЭкспортаМс to wait for background export to stop, but the subsequent ЭкспортироватьВсеПакеты() call in Закрыть() has no timeout - it runs until buffer is empty. SimpleSpanProcessor has no timeout mechanism at all. |
| 51 | SHOULD | ⚠️ partial | SDKs SHOULD ignore these calls gracefully, if possible (subsequent calls to OnStart, OnEnd, ForceFlush after Shutdown). | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43` | BatchSpanProcessor ignores Обработать() after shutdown (Закрыт flag), but SimpleSpanProcessor does not track shutdown state and may still attempt to export after Закрыть(). |

#### ForceFlush()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 52 | SHOULD | ✅ found | Any tasks associated with Spans for which the SpanProcessor had already received events prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 53 | SHOULD | ✅ found | If any SpanProcessor has any associated exporter, it SHOULD try to call the exporter's Export with all spans for which this was not already done and then invoke ForceFlush on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120` |  |
| 54 | MUST | ✅ found | The built-in SpanProcessors MUST do so (call exporter's Export and ForceFlush). | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 55 | MUST | ❌ not_found | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. | - | СброситьБуфер() does not accept a timeout parameter. ЭкспортироватьВсеПакеты() runs until all batches are exported with no timeout mechanism to abort early. |
| 56 | SHOULD | ❌ not_found | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | СброситьБуфер() is a Процедура (void) - it does not return success/failure/timeout status to the caller. |
| 57 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the SpanProcessor exports the completed spans. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98` |  |
| 58 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` | СброситьБуфер() delegates to ЭкспортироватьВсеПакеты() which loops exporting batches until buffer is empty, but has no timeout mechanism to abort. The async variant СброситьБуферАсинхронно() exists on the provider level but individual processor ForceFlush has no timeout. |

#### Built-in span processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#built-in-span-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:1, src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:1` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | MUST | ✅ found | The [Simple] processor MUST synchronize calls to Span Exporter's Export to make sure that they are not invoked concurrently | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:41` |  |
| 61 | MUST | ✅ found | The [Batch] processor MUST synchronize calls to Span Exporter's Export to make sure that they are not invoked concurrently | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:144` |  |
| 62 | SHOULD | ✅ found | The [Batch] processor SHOULD export a batch when scheduledDelayMillis expires, the queue contains maxExportBatchSize or more spans, or ForceFlush is called, AND the previous export call has returned | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:54` |  |
| 63 | MUST | ✅ found | Each [exporter] implementation MUST document the concurrency characteristics the SDK requires of the exporter | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:5` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 64 | MUST | ✅ found | The exporter MUST support three functions: Export, Shutdown, and ForceFlush | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:13` |  |

#### `Export(batch)`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | MUST NOT | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure) | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 66 | MUST | ✅ found | There MUST be a reasonable upper limit after which the [Export] call must time out with an error result (Failure) | `src/Экспорт/Классы/ОтелHttpТранспорт.os:149` |  |
| 67 | SHOULD NOT | ✅ found | The default SDK's Span Processors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37` |  |

#### `ForceFlush()`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | The export of any Spans the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` |  |
| 69 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:19` | СброситьБуфер() определена как Процедура (void), не возвращает результат успеха/ошибки/таймаута. В ОтелЭкспортерСпанов.os:41 аналогично - Процедура без возвращаемого значения. |
| 70 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed spans | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` |  |
| 71 | SHOULD | ✅ found | ForceFlush SHOULD complete or abort within some timeout. ForceFlush can be implemented as a blocking API or an asynchronous API which notifies the caller via a callback or an event | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` |  |

#### Examples

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#examples)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST | ✅ found | Tracer Provider - Tracer creation, ForceFlush and Shutdown MUST be safe to be called concurrently | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:265` |  |
| 73 | MUST | ⚠️ partial | Sampler - ShouldSample and GetDescription MUST be safe to be called concurrently | `src/Трассировка/Модули/ОтелСэмплер.os:1` | Сэмплер реализован как модуль с функциями-константами (ВсегдаВключен, ВсегдаВыключен и т.д.), по сути stateless. Безопасность конкурентного доступа обеспечивается неявно через отсутствие мутабельного состояния, но нет явного GetDescription метода. |
| 74 | MUST | ⚠️ partial | Span processor - all methods MUST be safe to be called concurrently | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:41` | SimpleSpanProcessor синхронизирует Export через БлокировкаЭкспорта, но методы СброситьБуфер() и Закрыть() не защищены блокировкой. BatchSpanProcessor использует блокировку через базовый класс, но не все методы фасада защищены. |
| 75 | MUST | ⚠️ partial | Span Exporter - ForceFlush and Shutdown MUST be safe to be called concurrently | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:47` | СброситьБуфер() - noop, безопасно. Закрыть() устанавливает Закрыт = Истина без блокировки или атомарного доступа - потенциально не потокобезопасно при конкурентных вызовах с Экспортировать(). |

### Logs Api

#### Logs API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logs-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD provide a way to set/register and access a global default LoggerProvider. | `src/Ядро/Модули/ОтелГлобальный.os:31` |  |

#### LoggerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The LoggerProvider MUST provide the following functions: Get a Logger | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 3 | MUST | ✅ found | This API MUST accept the following instrumentation scope parameters: name, version (optional), schema_url (optional), attributes (optional) | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 4 | MUST | ✅ found | This API (attributes parameter) MUST be structured to accept a variable number of attributes, including none. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:57` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The Logger MUST provide a function to: Emit a LogRecord | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 6 | SHOULD | ✅ found | The Logger SHOULD provide functions to: Report if Logger is Enabled | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 7 | MUST | ✅ found | The API (Emit a LogRecord) MUST accept the following parameters: Timestamp (optional), Observed Timestamp (optional), Context, Severity Number (optional), Severity Text (optional), Body (optional), Attributes (optional), Event Name (optional) | `src/Логирование/Классы/ОтелЗаписьЛога.os:44` |  |
| 8 | SHOULD | ✅ found | When implicit Context is supported, then this parameter (Context for Emit) SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 9 | MUST | ✅ found | When implicit Context is supported and Context for Emit is unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:82` |  |
| 10 | SHOULD | ✅ found | A Logger SHOULD provide this Enabled API to help users avoid performing computationally expensive operations when generating a LogRecord. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 11 | SHOULD | ✅ found | The API (Enabled) SHOULD accept the following parameters: Context, Severity Number (optional), Event Name (optional). | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 12 | SHOULD | ✅ found | When implicit Context is supported, then this parameter (Context for Enabled) SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 13 | MUST | ✅ found | When implicit Context is supported and Context for Enabled is unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 14 | MUST | ✅ found | This API (Enabled) MUST return a language idiomatic boolean type. A returned value of true means the Logger is enabled for the provided arguments, and a returned value of false means the Logger is disabled for the provided arguments. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 15 | SHOULD | ❌ not_found | The API (Enabled) SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response. | - | Документация метода Включен() не содержит явного указания о необходимости вызывать его перед каждым emit. Комментарий описывает назначение метода, но не включает рекомендацию вызывать его повторно для актуального результата. |
| 16 | SHOULD | ⚠️ partial | When only explicit Context is supported, this parameter (Context for Emit) SHOULD be required. | `src/Логирование/Классы/ОтелЛоггер.os:76` | Реализация поддерживает implicit Context (через ОтелКонтекст.Текущий()), поэтому параметр сделан опциональным. Требование SHOULD для explicit-only контекста не применяется напрямую, но Контекст передается как optional параметр в Записать(), что соответствует implicit-поддерживающей реализации. |

#### Optional and required parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#optional-and-required-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | For each optional parameter, the API MUST be structured to accept it. | `src/Логирование/Классы/ОтелЗаписьЛога.os:44` |  |
| 18 | MUST NOT | ✅ found | For each optional parameter, the API MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЗаписьЛога.os:44` |  |
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
| 2 | MUST | ✅ found | A LoggerProvider MUST provide a way to allow a Resource to be specified. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:206` |  |
| 3 | SHOULD | ✅ found | If a Resource is specified, it SHOULD be associated with all the LogRecords produced by any Logger from the LoggerProvider. | `src/Логирование/Классы/ОтелЛоггер.os:78` |  |

#### LoggerProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent LoggerProviders. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:60` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration (i.e. LogRecordProcessors and LoggerConfigurator) MUST be owned by the LoggerProvider. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:12` |  |
| 6 | MUST | ✅ found | the updated configuration MUST also apply to all already returned Loggers | `src/Логирование/Классы/ОтелЛоггер.os:107` |  |
| 7 | MUST NOT | ✅ found | it MUST NOT matter whether a Logger was obtained from the LoggerProvider before or after the configuration change | `src/Логирование/Классы/ОтелЛоггер.os:8` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | Метод СброситьБуфер() - Процедура (void), не возвращает статус. СброситьБуферАсинхронно() возвращает Обещание, но синхронный метод не сообщает об успехе/ошибке. |
| 9 | SHOULD | ⚠️ partial | ForceFlush SHOULD return some ERROR status if there is an error condition. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | СброситьБуфер() не возвращает значение, ошибки процессоров не пробрасываются вызывающему коду. |
| 10 | SHOULD | ⚠️ partial | if there is no error condition, it SHOULD return some NO ERROR status. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | СброситьБуфер() не возвращает значение - нет способа узнать об успешном выполнении. |
| 11 | SHOULD | ❌ not_found | ForceFlush SHOULD complete or abort within some timeout. | - | Метод СброситьБуфер() не имеет механизма таймаута - вызывает СброситьБуфер() на каждом процессоре без ограничения по времени. |
| 12 | MUST | ✅ found | ForceFlush MUST invoke ForceFlush on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:108` |  |

#### ReadableLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readablelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | A function receiving this as an argument MUST be able to access all the information added to the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:44-161` |  |
| 14 | MUST | ✅ found | It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) associated with the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:131-143` |  |
| 15 | MUST | ✅ found | The trace context fields MUST be populated from the resolved Context (either the explicitly passed Context or the current Context) when emitted. | `src/Логирование/Классы/ОтелЛоггер.os:81-91` |  |
| 16 | MUST | ✅ found | Counts for attributes due to collection limits MUST be available for exporters to report as described in the transformation to non-OTLP formats specification. | `src/Логирование/Классы/ОтелЗаписьЛога.os:150-152` |  |

#### ReadWriteLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readwritelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | A function receiving this as an argument MUST additionally be able to modify the following information added to the LogRecord: Timestamp, ObservedTimestamp, SeverityText, SeverityNumber, Body, Attributes (addition, modification, removal), TraceId, SpanId, TraceFlags, EventName. | `src/Логирование/Классы/ОтелЗаписьЛога.os:179-298` |  |

#### LogRecord Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecord-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | LogRecord attributes MUST adhere to the common rules of attribute limits. | `src/Логирование/Классы/ОтелЗаписьЛога.os:235-247` |  |
| 19 | MUST | ✅ found | If the SDK implements attribute limits it MUST provide a way to change these limits, via a configuration to the LoggerProvider, by allowing users to configure individual limits. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:50-53` |  |
| 20 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called LogRecordLimits. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:1-79` |  |
| 21 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute was discarded due to such a limit. | `src/Логирование/Классы/ОтелЗаписьЛога.os:384-389` |  |
| 22 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per LogRecord (i.e., not per discarded attribute). | `src/Логирование/Классы/ОтелЗаписьЛога.os:385-388` |  |

#### LogRecordProcessor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | MUST | ✅ found | The SDK MUST allow each pipeline to end with an individual exporter. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:66` |  |
| 24 | MUST | ✅ found | The SDK MUST allow users to implement and configure custom processors and decorate built-in processors for advanced scenarios such as enriching with attributes. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:1` |  |

#### LogRecordProcessor operations#### OnEmit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor-operations-onemit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | SHOULD NOT | ⚠️ partial | OnEmit is called synchronously on the thread that emitted the LogRecord, therefore it SHOULD NOT block or throw exceptions. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17` | Composite processor catches exceptions from individual processors, but ОтелПростойПроцессорЛогов.ПриПоявлении re-throws export errors (line 26-27) and blocks synchronously during export. Batch processor handles correctly (non-blocking buffer add). |
| 26 | MUST | ✅ found | For a LogRecordProcessor registered directly on SDK LoggerProvider, the logRecord mutations MUST be visible in next registered processors. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17` |  |
| 27 | SHOULD | ❌ not_found | Implementations SHOULD recommended to users that a clone of logRecord be used for any concurrent processing, such as in a batching processor. | - | ОтелЗаписьЛога has no clone method and there is no documentation recommending cloning for concurrent processing scenarios. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST NOT | ❌ not_found | Any modifications to parameters inside Enabled MUST NOT be propagated to the caller. Parameters are immutable or passed by value. | - | ИнтерфейсПроцессорЛогов does not define an Enabled operation. The Logger has Включен() (src/Логирование/Классы/ОтелЛоггер.os:42) but it does not delegate to processor-level Enabled. The processor interface only has ПриПоявлении, СброситьБуфер, Закрыть - no Enabled/Включен method. |

#### ShutDown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | SHOULD | ⚠️ partial | Shutdown SHOULD be called only once for each LogRecordProcessor instance. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:75` | Batch processor sets Закрыт=Истина but does not guard against double-close (no atomic CAS). Simple processor has no shutdown guard at all - multiple Закрыть() calls would close exporter multiple times. |
| 30 | SHOULD | ⚠️ partial | After the call to Shutdown, subsequent calls to OnEmit are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43` | Batch processor checks Закрыт flag in Обработать() and returns early (graceful ignore). Simple processor ОтелПростойПроцессорЛогов.ПриПоявлении does not check shutdown state - would attempt to call closed exporter. |
| 31 | SHOULD | ❌ not_found | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Both processor Закрыть() methods are Процедура (void). No return value or callback to indicate success, failure, or timeout. |
| 32 | MUST | ✅ found | Shutdown MUST include the effects of ForceFlush. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:77` |  |
| 33 | SHOULD | ✅ found | Shutdown SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | SHOULD | ✅ found | Any tasks associated with LogRecords for which the LogRecordProcessor had already received events prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 35 | SHOULD | ⚠️ partial | If any LogRecordProcessor has any associated exporter, it SHOULD try to call the exporter's Export with all LogRecords for which this was not already done and then invoke ForceFlush on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120` | ЭкспортироватьВсеПакеты() calls Экспортер.Экспортировать() for all remaining records, but does NOT call Экспортер.СброситьБуфер() (ForceFlush on the exporter) afterwards. |
| 36 | MUST | ⚠️ partial | The built-in LogRecordProcessors MUST do so (call exporter's Export with all LogRecords and then invoke ForceFlush on the exporter). | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120` | Built-in processors call Экспортер.Экспортировать() for all remaining records but do not invoke Экспортер.СброситьБуфер() (ForceFlush) on the exporter. |
| 37 | MUST | ❌ not_found | If a timeout is specified, the LogRecordProcessor MUST prioritize honoring the timeout over finishing all calls. | - | СброситьБуфер() has no timeout parameter. ЭкспортироватьВсеПакеты() exports all batches synchronously without any timeout consideration. |
| 38 | SHOULD | ❌ not_found | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | СброситьБуфер() is a Процедура (void) on both simple and batch processors. No return value or callback to indicate result. |
| 39 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 40 | SHOULD | ❌ not_found | ForceFlush SHOULD complete or abort within some timeout. | - | СброситьБуфер() has no timeout mechanism. It synchronously exports all batches via ЭкспортироватьВсеПакеты() without any timeout or abort logic. |

#### Built-in processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#built-in-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 41 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1` |  |
| 42 | SHOULD | ✅ found | Other common processing scenarios SHOULD be first considered for implementation out-of-process in OpenTelemetry Collector. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST | ✅ found | The simple processor MUST synchronize calls to LogRecordExporter's Export to make sure that they are not invoked concurrently. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:22` |  |
| 44 | MUST | ✅ found | The batching processor MUST synchronize calls to LogRecordExporter's Export to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:144` |  |
| 45 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:3` |  |

#### LogRecordExporter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | MUST | ✅ found | A LogRecordExporter MUST support the following functions: Export, ForceFlush, Shutdown | `src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:13,19,24` |  |

#### Export

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#export)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | MUST NOT | ✅ found | Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure) | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69,148-150` |  |
| 48 | MUST | ✅ found | There MUST be a reasonable upper limit after which the call must time out with an error result (Failure) | `src/Экспорт/Классы/ОтелHttpТранспорт.os:148-150` |  |
| 49 | SHOULD NOT | ✅ found | The default SDK's LogRecordProcessors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the logs are being sent to | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:18-31` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 50 | SHOULD | ✅ found | The export of any ReadableLogRecords the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43` |  |
| 51 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43` | СброситьБуфер() is a Процедура (void), does not return success/failure/timeout status to the caller |
| 52 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the ReadableLogRecords | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43` |  |
| 53 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43` | СброситьБуфер() on the exporter has no timeout mechanism - it is a synchronous no-op for the OTLP exporter but there is no configurable timeout for cases where flush could block |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each LogRecordExporter instance | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47-49` |  |
| 55 | SHOULD | ✅ found | After the call to Shutdown subsequent calls to Export are not allowed and SHOULD return a Failure result | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:26-28` |  |
| 56 | SHOULD NOT | ✅ found | Shutdown SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable) | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47-49` |  |
| 57 | MUST | ✅ found | LoggerProvider - Logger creation, ForceFlush and Shutdown MUST be safe to be called concurrently | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:18,107-123` |  |
| 58 | MUST | ✅ found | Logger - all methods MUST be safe to be called concurrently | `src/Логирование/Классы/ОтелЛоггер.os:1-251` |  |
| 59 | MUST | ⚠️ partial | LogRecordExporter - ForceFlush and Shutdown MUST be safe to be called concurrently | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-49` | Закрыть() sets Закрыт=Истина without synchronization (no lock or atomic). СброситьБуфер() is a no-op so concurrent calls are safe, but Shutdown itself is not protected against concurrent calls |

### Metrics Api

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD provide a way to set/register and access a global default MeterProvider. | `src/Ядро/Модули/ОтелГлобальный.os:99` |  |

#### MeterProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The MeterProvider MUST provide the following functions: Get a Meter | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 3 | MUST | ✅ found | This API (Get a Meter) MUST accept the following parameters: name, version, schema_url, attributes | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52-56` |  |
| 4 | MUST NOT | ✅ found | This API needs to be structured to accept a version, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:54` |  |
| 5 | MUST NOT | ✅ found | This API needs to be structured to accept a schema_url, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:56` |  |
| 6 | MUST | ✅ found | This API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:55` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ found | Meter SHOULD NOT be responsible for the configuration. This should be the responsibility of the MeterProvider instead. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:231-268` |  |

#### Meter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The Meter MUST provide functions to create new Instruments: Counter, Asynchronous Counter, Histogram, Gauge, Asynchronous Gauge, UpDownCounter, Asynchronous UpDownCounter | `src/Метрики/Классы/ОтелМетр.os:48-332` |  |

#### Instrument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ⚠️ partial | Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying. | `src/Метрики/Классы/ОтелМетр.os:553-579` | Дескрипторы инструментов хранят Вид/ЕдиницуИзмерения/Описание/Совет, но не хранят тип числа (int vs double). OneScript не имеет явного разделения int/double на уровне языка, дескриптор не включает тип значения как идентифицирующее поле. |

#### Synchronous and Asynchronous instruments

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#synchronous-and-asynchronous-instruments)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API to construct synchronous instruments MUST accept the following parameters: name, unit, description, advisory. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 11 | SHOULD | ✅ found | The name needs to be provided by a user. If possible, the API SHOULD be structured so a user is obligated to provide this parameter (sync instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 12 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that the name parameter is needed (sync instruments). | `src/Метрики/Классы/ОтелМетр.os:38-42` |  |
| 13 | SHOULD | ❌ not_found | The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (sync instruments). | - | Документация метода СоздатьСчетчик и аналогичных не содержит указания на синтаксические требования к имени инструмента. |
| 14 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the name; that is left to implementations of the API, like the SDK (sync instruments). | `src/Метрики/Классы/ОтелМетр.os:48-67` |  |
| 15 | MUST NOT | ✅ found | This API needs to be structured to accept a unit, but MUST NOT obligate a user to provide one (sync instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 16 | MUST | ✅ found | The API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters for the unit (sync instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 17 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the unit (sync instruments). | `src/Метрики/Классы/ОтелМетр.os:48-67` |  |
| 18 | MUST NOT | ✅ found | This API needs to be structured to accept a description, but MUST NOT obligate a user to provide one (sync instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 19 | MUST | ✅ found | The API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters for the description (sync instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 20 | MUST NOT | ✅ found | This API needs to be structured to accept advisory parameters, but MUST NOT obligate the user to provide it (sync instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 21 | SHOULD NOT | ✅ found | The API SHOULD NOT validate advisory parameters (sync instruments). | `src/Метрики/Классы/ОтелМетр.os:642-661` |  |
| 22 | MUST | ✅ found | The API to construct asynchronous instruments MUST accept the following parameters: name, unit, description, advisory, callback. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 23 | SHOULD | ✅ found | The name needs to be provided by a user. If possible, the API SHOULD be structured so a user is obligated to provide this parameter (async instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 24 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that the name parameter is needed (async instruments). | `src/Метрики/Классы/ОтелМетр.os:216-222` |  |
| 25 | SHOULD | ❌ not_found | The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (async instruments). | - | Документация метода СоздатьНаблюдаемыйСчетчик и аналогичных не содержит указания на синтаксические требования к имени инструмента. |
| 26 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the name, that is left to implementations of the API (async instruments). | `src/Метрики/Классы/ОтелМетр.os:229-251` |  |
| 27 | MUST NOT | ✅ found | This API needs to be structured to accept a unit, but MUST NOT obligate a user to provide one (async instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 28 | MUST | ✅ found | The API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters for the unit (async instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 29 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the unit (async instruments). | `src/Метрики/Классы/ОтелМетр.os:229-251` |  |
| 30 | MUST NOT | ✅ found | This API needs to be structured to accept a description, but MUST NOT obligate a user to provide one (async instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 31 | MUST | ✅ found | The API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters for the description (async instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 32 | MUST NOT | ✅ found | This API needs to be structured to accept advisory parameters, but MUST NOT obligate the user to provide it (async instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 33 | SHOULD NOT | ✅ found | The API SHOULD NOT validate advisory parameters (async instruments). | `src/Метрики/Классы/ОтелМетр.os:642-661` |  |
| 34 | MUST | ✅ found | This API MUST be structured to accept a variable number of callback functions, including none. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 35 | MUST | ✅ found | The API MUST support creation of asynchronous instruments by passing zero or more callback functions to be permanently registered to the newly created instrument. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147-157` |  |
| 36 | SHOULD | ✅ found | The API SHOULD support registration of callback functions associated with asynchronous instruments after they are created. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:58-62` |  |
| 37 | MUST | ✅ found | Where the API supports registration of callback functions after asynchronous instrumentation creation, the user MUST be able to undo registration of the specific callback after its registration by some means. | `src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os:14-19` |  |
| 38 | MUST | ✅ found | Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160-177` |  |
| 39 | MUST | ⚠️ partial | Callback functions MUST be documented as follows for the end user (reentrant safe, not indefinite, no duplicate observations). | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:136-158` | Конструктор ОтелБазовыйНаблюдаемыйИнструмент содержит комментарий о параметрах, но документация не содержит предупреждений для конечного пользователя о реентрантной безопасности, длительности выполнения и дублировании наблюдений. |
| 40 | SHOULD | ⚠️ partial | Callback functions SHOULD be reentrant safe. The SDK expects to evaluate callbacks for each MetricReader independently. | - | Документация callback не содержит рекомендации о реентрантной безопасности для конечного пользователя. |
| 41 | SHOULD NOT | ⚠️ partial | Callback functions SHOULD NOT take an indefinite amount of time. | - | Документация callback не содержит предупреждения о времени выполнения для конечного пользователя. |
| 42 | SHOULD NOT | ⚠️ partial | Callback functions SHOULD NOT make duplicate observations (more than one Measurement with the same attributes) across all registered callbacks. | - | Документация callback не содержит предупреждения о дублировании наблюдений для конечного пользователя. |
| 43 | MUST | ✅ found | Callbacks registered at the time of instrument creation MUST apply to the single instruments which is under construction. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147-157` |  |
| 44 | MUST | ✅ found | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the instrument associated with each observed Measurement value. | `src/Метрики/Классы/ОтелМетр.os:428-455` |  |
| 45 | MUST | ✅ found | Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of asynchronous instruments from the same Meter instance. | `src/Метрики/Классы/ОтелМетр.os:428-431` |  |
| 46 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180-188` |  |
| 47 | MUST | ✅ found | Observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180-188` |  |
| 48 | SHOULD | ✅ found | The API SHOULD provide some way to pass state to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147` |  |

#### General operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | SHOULD | ✅ found | All synchronous instruments SHOULD provide functions to: Report if instrument is Enabled | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 50 | SHOULD | ✅ found | synchronous instruments SHOULD provide this Enabled API to help users avoid performing computationally expensive operations when recording measurements | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 51 | MUST | ✅ found | the Enabled API MUST be structured in a way for parameters to be added (no required parameters currently, but extensible) | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 52 | MUST | ✅ found | This Enabled API MUST return a language idiomatic boolean type. true means enabled, false means disabled | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201-203` |  |
| 53 | SHOULD | ❌ not_found | The Enabled API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response | - | Документация метода Включен() не содержит рекомендации вызывать его перед каждым измерением. Комментарий описывает лишь что возвращает метод, но не содержит рекомендации по частоте вызова. |

#### Counter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Counter other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 55 | SHOULD NOT | ✅ found | Counter Add API SHOULD NOT return a value | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 56 | MUST | ✅ found | Counter Add API MUST accept a numeric increment value as parameter | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 57 | SHOULD | ✅ found | Counter Add API SHOULD be structured so a user is obligated to provide the increment value parameter | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 58 | MUST | ✅ found | If it is not possible to structurally enforce obligation to provide increment value, the API MUST be documented in a way to communicate to users that this parameter is needed | `src/Метрики/Классы/ОтелСчетчик.os:16` |  |
| 59 | SHOULD | ❌ not_found | The increment value is expected to be non-negative. This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative | - | Комментарий к методу Добавить (строка 14) говорит 'положительное значение', но формально спека требует 'non-negative' (включая ноль). Тем не менее код проверяет Значение < 0 (строка 22), а документация описывает это. Ставлю not_found поскольку формальная документация для конечного пользователя (API doc) не содержит явного указания 'non-negative'. |
| 60 | SHOULD NOT | ⚠️ partial | This API SHOULD NOT validate the non-negative value, that is left to implementations of the API | `src/Метрики/Классы/ОтелСчетчик.os:22-24` | Counter.Добавить() фактически валидирует значение - отбрасывает отрицательные (Если Значение < 0 Тогда Возврат). Спецификация говорит API SHOULD NOT validate. |
| 61 | MUST | ✅ found | Counter Add API MUST be structured to accept a variable number of attributes, including none | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 62 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 63 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Counter other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 64 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180-186` |  |
| 65 | MUST | ✅ found | observations from a single callback MUST be reported with identical timestamps | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` |  |
| 66 | SHOULD | ⚠️ partial | The API SHOULD provide some way to pass state to the callback | `src/Метрики/Классы/ОтелМетр.os:229` | Callback реализован через Действие (lambdas), что позволяет замыкание (closure) для передачи состояния. Однако явного параметра state нет - состояние передаётся только через замыкание, что является идиоматическим подходом для OneScript. |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Histogram other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:80` |  |
| 68 | SHOULD NOT | ✅ found | Histogram Record API SHOULD NOT return a value | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 69 | MUST | ✅ found | Histogram Record API MUST accept a numeric value to record as parameter | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 70 | SHOULD | ✅ found | Histogram Record API SHOULD be structured so a user is obligated to provide the value parameter | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 71 | MUST | ✅ found | If it is not possible to structurally enforce the obligation for value parameter, the Histogram Record API MUST be documented in a way to communicate to users that this parameter is needed | `src/Метрики/Классы/ОтелГистограмма.os:16` |  |
| 72 | SHOULD | ❌ not_found | The recorded value is expected to be non-negative. This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative | - | Документация метода Записать в ОтелГистограмма не содержит указания что значение должно быть неотрицательным. |
| 73 | SHOULD NOT | ✅ found | This Histogram Record API SHOULD NOT validate the non-negative value, that is left to implementations of the API | `src/Метрики/Классы/ОтелГистограмма.os:20-22` |  |
| 74 | MUST | ✅ found | Histogram Record API MUST be structured to accept a variable number of attributes, including none | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 75 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Gauge other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:194` |  |
| 76 | SHOULD NOT | ✅ found | Gauge Record API SHOULD NOT return a value | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 77 | MUST | ✅ found | Gauge Record API MUST accept a numeric value (the current absolute value) as parameter | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 78 | SHOULD | ✅ found | Gauge Record API SHOULD be structured so a user is obligated to provide the value parameter | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 79 | MUST | ✅ found | If it is not possible to structurally enforce the obligation for value parameter, the Gauge Record API MUST be documented in a way to communicate to users that this parameter is needed | `src/Метрики/Классы/ОтелДатчик.os:14` |  |
| 80 | MUST | ✅ found | Gauge Record API MUST be structured to accept a variable number of attributes, including none | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 81 | MUST | ✅ found | The Gauge API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 82 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Gauge other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:308` |  |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 83 | MUST NOT | ✅ found | There MUST NOT be any API for creating an UpDownCounter other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:162` |  |
| 84 | SHOULD NOT | ✅ found | UpDownCounter Add API SHOULD NOT return a value | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 85 | MUST | ✅ found | UpDownCounter Add API MUST accept a numeric value to add as parameter | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 86 | SHOULD | ✅ found | UpDownCounter Add API SHOULD be structured so a user is obligated to provide the value parameter | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 87 | MUST | ✅ found | If it is not possible to structurally enforce the obligation for value parameter, the UpDownCounter Add API MUST be documented in a way to communicate to users that this parameter is needed | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:16` |  |
| 88 | MUST | ✅ found | UpDownCounter Add API MUST be structured to accept a variable number of attributes, including none | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 89 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:268` |  |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: a callback function and a list of Instruments used in the callback function | `src/Метрики/Классы/ОтелМетр.os:428-431` |  |

#### Note the two associated instruments are passed to the callback.

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-the-two-associated-instruments-are-passed-to-the-callback)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 91 | SHOULD | ✅ found | All the metrics components SHOULD allow new APIs to be added to existing components without introducing breaking changes | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:1` |  |
| 92 | SHOULD | ✅ found | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introducing breaking changes, if possible | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 93 | MUST | ✅ found | MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default | `src/Метрики/Классы/ОтелПровайдерМетрик.os:241` |  |
| 94 | MUST | ✅ found | Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default | `src/Метрики/Классы/ОтелМетр.os:493` |  |
| 95 | MUST | ✅ found | Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:16` |  |

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
| 2 | MUST | ✅ found | A MeterProvider MUST provide a way to allow a Resource to be specified. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:24` |  |
| 3 | SHOULD | ✅ found | If a Resource is specified, it SHOULD be associated with all the metrics produced by any Meter from the MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:67` |  |

#### MeterProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent MeterProviders. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:231` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration (i.e. MetricExporters, MetricReaders, Views, and (Development) MeterConfigurator) MUST be owned by the MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:6` |  |
| 6 | MUST | ✅ found | the updated configuration MUST also apply to all already returned Meters | `src/Метрики/Классы/ОтелПровайдерМетрик.os:71` |  |
| 7 | MUST NOT | ✅ found | it MUST NOT matter whether a Meter was obtained from the MeterProvider before or after the configuration change | `src/Метрики/Классы/ОтелПровайдерМетрик.os:71` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | ForceFlush MUST invoke ForceFlush on all registered MetricReader instances that implement ForceFlush. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` |  |
| 9 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` | СброситьБуфер() - процедура без возвращаемого значения. Есть СброситьБуферАсинхронно() с Обещание, но синхронный вариант не информирует вызывающий код о результате |
| 10 | SHOULD | ⚠️ partial | ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` | Метод СброситьБуфер() не возвращает ни ERROR, ни NO ERROR статус - это процедура (void) |
| 11 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` | СброситьБуфер() не принимает параметр таймаута и не имеет механизма прерывания по таймауту |

#### View

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The SDK MUST provide functionality for a user to create Views for a MeterProvider. | `src/Метрики/Классы/ОтелПредставление.os:1` |  |
| 13 | MUST | ✅ found | This functionality MUST accept as inputs the Instrument selection criteria and the resulting stream configuration. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 14 | MUST | ✅ found | The SDK MUST provide the means to register Views with a MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:176` |  |

#### Instrument selection criteria

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-selection-criteria)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | SHOULD | ✅ found | Criteria SHOULD be treated as additive. This means an Instrument has to match all the provided criteria for the View to be applied. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37-61` |  |
| 16 | MUST | ✅ found | The SDK MUST accept the following criteria: name, type, unit, meter_name, meter_version, meter_schema_url. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159-168` |  |
| 17 | MUST | ✅ found | If the SDK does not support wildcards in general, it MUST still recognize the special single asterisk (*) character as matching all Instruments. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37` |  |
| 18 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 19 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a type, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 20 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a unit, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:160` |  |
| 21 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a meter_name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:160` |  |
| 22 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a meter_version, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:161` |  |
| 23 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a meter_schema_url, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:161` |  |
| 24 | MUST NOT | ✅ found | The instrument selection criteria can be structured to accept additional criteria the SDK accepts, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159-161` |  |

#### Stream configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#stream-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | The SDK MUST accept the following stream configuration parameters: name, description, attribute_keys, aggregation, exemplar_reservoir, aggregation_cardinality_limit. | `src/Метрики/Классы/ОтелПредставление.os:156-164` |  |
| 26 | SHOULD | ✅ found | name: The metric stream name that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:29-31` |  |
| 27 | SHOULD | ⚠️ partial | In order to avoid conflicts, if a name is provided the View SHOULD have an instrument selector that selects at most one instrument. | - | No validation in the code to check that a View with name selects at most one instrument; name is accepted but no warning is emitted when a wildcard selector is combined with a name override. |
| 28 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept a name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:157` |  |
| 29 | MUST | ✅ found | If the user does not provide a name value, name from the Instrument the View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:188-212` |  |
| 30 | SHOULD | ✅ found | description: The metric stream description that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:38-40` |  |
| 31 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept a description, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:158` |  |
| 32 | MUST | ✅ found | If the user does not provide a description value, the description from the Instrument a View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:189-215` |  |
| 33 | MUST | ✅ found | attribute_keys: The allow-list contains attribute keys that identify the attributes that MUST be kept. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:291-299` |  |
| 34 | MUST | ✅ found | attribute_keys: all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:84-86` |  |
| 35 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept attribute_keys, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелПредставление.os:159` |  |
| 36 | SHOULD | ✅ found | If the user does not provide any value, the SDK SHOULD use the Attributes advisory parameter configured on the instrument instead. | `src/Метрики/Классы/ОтелМетр.os:523-528` |  |
| 37 | MUST | ✅ found | If the Attributes advisory parameter is absent, all attributes MUST be kept. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:269` |  |
| 38 | SHOULD | ✅ found | Additionally, implementations SHOULD support configuring an exclude-list of attribute keys. | `src/Метрики/Классы/ОтелПредставление.os:56-58` |  |
| 39 | MUST | ⚠️ partial | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелПредставление.os:56-58` | ОтелПредставление accepts ИсключенныеКлючиАтрибутов parameter, but ПрименитьПредставлениеКИнструменту does not apply exclude-list filtering - only allow-list (РазрешенныеКлючиАтрибутов) is applied via УстановитьРазрешенныеКлючиАтрибутов. |
| 40 | MUST | ⚠️ partial | If an attribute key is both included and excluded, the SDK MAY fail fast - the exclude-list: all other attributes MUST be kept. | `src/Метрики/Классы/ОтелПредставление.os:162` | Exclude-list parameter is accepted in the View constructor but its semantics are not enforced during collection. Only allow-list filtering is applied. |
| 41 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept an aggregation, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:161` |  |
| 42 | MUST | ⚠️ partial | If the user does not provide an aggregation value, the MeterProvider MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance. | `src/Метрики/Классы/ОтелМетр.os:58-59` | Default aggregation is applied based on instrument type (Sum for Counter, Histogram for Histogram, etc.) but it is hardcoded at Meter level, not configurable per MetricReader instance. The MetricReader does not have a separate default_aggregation property. |
| 43 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept an exemplar_reservoir, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:163` |  |
| 44 | MUST | ✅ found | If the user does not provide an exemplar_reservoir value, the MeterProvider MUST apply a default exemplar reservoir. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |
| 45 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept an aggregation_cardinality_limit, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:164` |  |
| 46 | MUST | ⚠️ partial | If the user does not provide an aggregation_cardinality_limit value, the MeterProvider MUST apply the default aggregation cardinality limit the MetricReader is configured with. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` | Default cardinality limit is 2000 (hardcoded in constructor), but it is set from Meter, not configured per MetricReader. The MetricReader has no aggregation_cardinality_limit configuration property. |

#### Measurement processing

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#measurement-processing)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | SHOULD | ✅ found | The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument: determine the MeterProvider, check Views, apply default aggregation. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:173-220` |  |
| 48 | MUST | ✅ found | If the MeterProvider has no View registered, take the Instrument and apply the default Aggregation - Instrument advisory parameters, if any, MUST be honored. | `src/Метрики/Классы/ОтелМетр.os:515-537` |  |
| 49 | SHOULD | ❌ not_found | If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning. | - | Views are applied independently but no conflict detection or warning emission occurs when multiple Views produce conflicting metric identities (same name from different Views). |
| 50 | SHOULD | ❌ not_found | If it is not possible to apply the View without producing semantic errors the implementation SHOULD emit a warning and proceed as if the View did not exist. | - | No semantic validation of View compatibility (e.g., checking if async instrument is set to use explicit bucket histogram aggregation). Views are always applied without semantic error checking. |
| 51 | MUST | ✅ found | If both a View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:519-528` |  |
| 52 | SHOULD | ⚠️ partial | If the Instrument could not match with any of the registered Views, the SDK SHOULD enable the instrument using the default aggregation and temporality. | `src/Метрики/Классы/ОтелМетр.os:48-67` | Default aggregation is applied when no View matches (instrument is always created with a default aggregator). However, temporality is determined by the MetricReader/exporter, not explicitly set at View miss point. |

#### conflicting metric identities)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#conflicting-metric-identities)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 53 | MUST | ✅ found | The SDK MUST provide the following Aggregation to support the Metric Points in the Metrics Data Model: Drop, Default, Sum, Last Value, Explicit Bucket Histogram. | `src/Метрики/Модули/ОтелАгрегация.os:15-81` |  |
| 54 | SHOULD | ✅ found | The SDK SHOULD provide the following Aggregation: Base2 Exponential Bucket Histogram. | `src/Метрики/Модули/ОтелАгрегация.os:72-81` |  |

#### Sum Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#sum-aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD NOT | ❌ not_found | Arithmetic sum of Measurement values in population - this SHOULD NOT be collected when used with instruments that record negative measurements (e.g. UpDownCounter or ObservableGauge). | - | The histogram aggregator always collects sum regardless of instrument type. No check prevents sum collection for UpDownCounter or ObservableGauge histogram aggregations. |
| 56 | SHOULD | ✅ found | SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different. | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:118-134` |  |
| 57 | MUST | ✅ found | Implementations are REQUIRED to accept the entire normal range of IEEE floating point values (i.e., all values except for +Inf, -Inf and NaN values). | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:111-134` |  |
| 58 | SHOULD NOT | ❌ not_found | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the sum, min, and max fields. | - | No explicit check for +Inf, -Inf, or NaN values in the exponential histogram aggregator's Записать method. All values are processed without filtering non-normal values. |
| 59 | MUST | ✅ found | The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic scale parameter will not exceed. The maximum scale is defined by the MaxScale configuration parameter. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:302-303` |  |
| 60 | SHOULD | ✅ found | When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:35-53` |  |
| 61 | SHOULD | ✅ found | Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possible, within the constraint of maximum size. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:157-185` |  |

#### Observations inside asynchronous callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#observations-inside-asynchronous-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 62 | MUST | ✅ found | Callback functions MUST be invoked for the specific MetricReader performing collection, such that observations made or produced by executing callbacks only apply to the intended MetricReader during collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:140-147` |  |
| 63 | SHOULD | ❌ not_found | The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks. | - | No mechanism to detect or disregard async instrument API usage outside of registered callbacks. The ОтелНаблюдениеМетрики can be used and populated anywhere, not just within callback context. |
| 64 | SHOULD | ❌ not_found | The implementation SHOULD use a timeout to prevent indefinite callback execution. | - | No timeout for individual callback execution. Callbacks are invoked in a simple loop (ВызватьCallbackИСобрать) without any timeout mechanism. Only the periodic reader has a shutdown timeout, not per-callback timeout. |
| 65 | MUST | ✅ found | The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:140-147` |  |
| 66 | SHOULD NOT | ❌ not_found | The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback. | - | Observable instruments clear external observations after each collect (ВнешниеНаблюдения = Новый Массив at line 174 of ОтелБазовыйНаблюдаемыйИнструмент.os) but data points from callbacks are freshly created each time. However, there is no explicit mechanism to track 'previously-observed attribute sets' vs 'currently-observed' for persistence filtering across collection cycles. |

#### Cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | SHOULD | ✅ found | SDKs SHOULD support being configured with a cardinality limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:163-164` |  |
| 68 | SHOULD | ✅ found | Cardinality limit enforcement SHOULD occur after attribute filtering, if any. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:84-92` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | SHOULD | ⚠️ partial | A view with criteria matching the instrument an aggregation is created for has an aggregation_cardinality_limit value defined for the stream, that value SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:92` | ОтелПредставление has ЛимитМощностиАгрегации property (line 92), but in ОтелМетр.ПрименитьПредставлениеКИнструменту the view's cardinality limit is never read or applied to the instrument's ЛимитМощности. Only РазрешенныеКлючиАтрибутов, РезервуарЭкземпляров, and ГраницыГистограммы from the View are applied. |
| 70 | SHOULD | ❌ not_found | If there is no matching view, but the MetricReader defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | - | ОтелПериодическийЧитательМетрик has no cardinality limit configuration. There is no API on the MetricReader to define a default cardinality limit per instrument kind. |
| 71 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` |  |
| 72 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:325` |  |
| 73 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:92` |  |

#### Synchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#synchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 74 | MUST | ✅ found | Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138` |  |
| 75 | MUST | ✅ found | Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in exactly one Aggregator, which is either an Aggregator associated with the correct attribute set or an aggregator associated with the overflow attribute set. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:78` |  |
| 76 | MUST NOT | ✅ found | Measurements MUST NOT be double-counted or dropped during an overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:105` |  |

#### Asynchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#asynchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 77 | SHOULD | ❌ not_found | Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality. | - | ОтелБазовыйНаблюдаемыйИнструмент has no cardinality limiting at all. All observations from callbacks are converted directly to data points without any cardinality checks or overflow handling. |

#### Duplicate instrument registration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#duplicate-instrument-registration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | MUST | ✅ found | The Meter MUST return a functional instrument that can be expected to export data even if this will cause semantic error in the data model. | `src/Метрики/Классы/ОтелМетр.os:54` |  |
| 79 | SHOULD | ✅ found | When a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted. | `src/Метрики/Классы/ОтелМетр.os:573` |  |
| 80 | SHOULD | ⚠️ partial | The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible. | `src/Метрики/Классы/ОтелМетр.os:573` | The warning message includes information about conflicting parameters (existing vs requested kind/unit), but does not include any resolution guidance such as suggesting the user configure a View to resolve the conflict. |
| 81 | SHOULD | ❌ not_found | If the potential conflict involves multiple description properties, setting the description through a configured View SHOULD avoid the warning. | - | There is no logic to check if a View resolves the description conflict and suppress the warning accordingly. The warning is emitted purely based on descriptor comparison, without considering configured Views. |
| 82 | SHOULD | ❌ not_found | If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning. | - | The warning message does not include any View recipe or suggestion for resolving the conflict through View configuration. |
| 83 | SHOULD | ⚠️ partial | Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both Metric objects and emit a generic warning describing the duplicate instrument registration. | `src/Метрики/Классы/ОтелМетр.os:54` | The SDK returns the first-registered instrument for duplicate names, so data is reported only for the first instrument, not both. The generic warning is emitted, but the 'pass through both Metric objects' behavior is not implemented. |
| 84 | MUST | ✅ found | The SDK MUST aggregate data from identical Instruments together in its export pipeline. | `src/Метрики/Классы/ОтелМетр.os:54` |  |

#### Name conflict

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#name-conflict)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 85 | MUST | ⚠️ partial | When a user passes multiple casings of the same name, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above. | `src/Метрики/Классы/ОтелМетр.os:49` | Instrument names are normalized with НРег() (lowercase) and stored by normalized key, so the first-seen instrument is correctly returned for different casings. However, when the second request comes with different casing but identical descriptors (kind, unit, description), no warning is logged because ПроверитьКонфликтДескриптора only warns when descriptors differ, not for pure casing conflicts. |

#### Instrument name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 86 | SHOULD | ❌ not_found | When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax. | - | No instrument name validation is implemented in ОтелМетр. Instrument creation methods (СоздатьСчетчик, СоздатьГистограмму, etc.) accept any string as name without checking against the OTel instrument name syntax (alphanumeric, _, ., -, /, starting with letter). |
| 87 | SHOULD | ❌ not_found | If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name. | - | Since no name validation exists, no error is emitted for invalid instrument names. |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 88 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 89 | MUST | ✅ found | If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit string. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument description. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 91 | MUST | ✅ found | If a description is not provided or the description is null, the Meter MUST treat it the same as an empty description string. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 92 | SHOULD | ✅ found | When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:642` |  |
| 93 | SHOULD | ✅ found | If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided. | `src/Метрики/Классы/ОтелМетр.os:648` |  |
| 94 | MUST | ✅ found | If multiple identical Instruments are created with different advisory parameters, the Meter MUST return an instrument using the first-seen advisory parameters and log an appropriate error as described in duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:562` |  |
| 95 | MUST | ✅ found | If both a View and advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:515` |  |

#### Instrument advisory parameter: `ExplicitBucketBoundaries`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameter-explicitbucketboundaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | MUST | ✅ found | If no View matches, or if a matching View selects the default aggregation, the ExplicitBucketBoundaries advisory parameter MUST be used. | `src/Метрики/Классы/ОтелМетр.os:539` |  |

#### Exemplar

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | MUST | ✅ found | A Metric SDK MUST provide a mechanism to sample Exemplars from measurements via the ExemplarFilter and ExemplarReservoir hooks. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:1` |  |
| 98 | SHOULD | ✅ found | Exemplar sampling SHOULD be turned on by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:264` |  |
| 99 | MUST NOT | ✅ found | If Exemplar sampling is off, the SDK MUST NOT have overhead related to exemplar sampling. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:335` |  |
| 100 | MUST | ✅ found | A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation. For example, Exemplar sampling of histograms should be able to leverage bucket boundaries. | `src/Метрики/Классы/ОтелМетр.os:99` |  |
| 101 | SHOULD | ✅ found | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: ExemplarFilter and ExemplarReservoir. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 102 | MUST | ✅ found | The ExemplarFilter configuration MUST allow users to select between one of the built-in ExemplarFilters. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 103 | SHOULD | ✅ found | The ExemplarFilter SHOULD be a configuration parameter of a MeterProvider for an SDK. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 104 | SHOULD | ✅ found | The default value SHOULD be TraceBased. | `src/Метрики/Классы/ОтелМетр.os:496` |  |
| 105 | SHOULD | ✅ found | The filter configuration SHOULD follow the environment variable specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:110` |  |
| 106 | MUST | ✅ found | An OpenTelemetry SDK MUST support the following filters: AlwaysOn, AlwaysOff, TraceBased. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14` |  |

#### ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 107 | MUST | ✅ found | The ExemplarReservoir interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 108 | MUST | ✅ found | A new ExemplarReservoir MUST be created for every known timeseries data point, as determined by aggregation and view configuration. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |
| 109 | SHOULD | ✅ found | The 'offer' method SHOULD accept measurements, including: the value of the measurement, the complete set of Attributes, the Context, and a timestamp. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 110 | SHOULD | ✅ found | The 'offer' method SHOULD have the ability to pull associated trace and span information without needing to record full context. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:340` |  |
| 111 | MUST | ⚠️ partial | This MUST be clearly documented in the API and the reservoir MUST be given the Attributes associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the 'offer' method. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` | Reservoir receives timeseries attributes in the 'offer' method call (АтрибутыСерии parameter) rather than at construction time, but it does have access to both measurement and timeseries attributes during offer. |
| 112 | MUST | ✅ found | The 'collect' method MUST return accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:55` |  |
| 113 | SHOULD | ✅ found | Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:114` |  |
| 114 | MUST | ✅ found | Exemplars MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:130` |  |
| 115 | SHOULD | ⚠️ partial | The ExemplarReservoir SHOULD avoid allocations when sampling exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:42` | Reservoir always creates a new Соответствие (Map) for each exemplar in СоздатьЭкземпляр. OneScript lacks object pooling, so avoiding all allocations is impractical, but reservoir sampling itself (Algorithm R) is done without extra allocations. |
| 116 | MUST | ⚠️ partial | The 'offer' method MAY accept a filtered subset of Attributes which diverge from the timeseries. This MUST be clearly documented in the API. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` | The offer method accepts both АтрибутыИзмерения and АтрибутыСерии, but there is no explicit API documentation explaining the filtered attributes divergence behavior as required. |

#### Exemplar defaults

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar-defaults)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 117 | MUST | ✅ found | The SDK MUST include two types of built-in exemplar reservoirs: SimpleFixedSizeExemplarReservoir and AlignedHistogramBucketExemplarReservoir. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1` |  |
| 118 | SHOULD | ✅ found | Explicit bucket histogram aggregation with more than 1 bucket SHOULD use AlignedHistogramBucketExemplarReservoir. | `src/Метрики/Классы/ОтелМетр.os:99` |  |
| 119 | SHOULD | ✅ found | Base2 Exponential Histogram Aggregation SHOULD use a SimpleFixedSizeExemplarReservoir with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty (e.g. min(20, max_buckets)). | `src/Метрики/Классы/ОтелМетр.os:137` |  |
| 120 | SHOULD | ✅ found | All other aggregations SHOULD use SimpleFixedSizeExemplarReservoir. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |

#### SimpleFixedSizeExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#simplefixedsizeexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 121 | MUST | ✅ found | This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the reservoir has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:80` |  |
| 122 | SHOULD | ✅ found | Any stateful portion of sampling computation SHOULD be reset every collection cycle. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:64` |  |
| 123 | SHOULD | ✅ found | Otherwise, a default size of 1 SHOULD be used if no size configuration is provided. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:165` |  |

#### AlignedHistogramBucketExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#alignedhistogrambucketexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 124 | MUST | ✅ found | This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram (bucket boundaries). | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:158` |  |
| 125 | MUST | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50` |  |
| 126 | SHOULD | ⚠️ partial | This implementation SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50` | Реализация использует стратегию 'последнее измерение заменяет предыдущее' (last-seen), а не reservoir sampling с равномерной вероятностью. Спецификация допускает этот вариант через MAY ('the implementation MAY instead keep the last seen measurement'), но SHOULD предпочитает sampling. |
| 127 | SHOULD | ✅ found | This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:158` |  |

#### Custom ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#custom-exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 128 | MUST | ✅ found | The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation. | `src/Метрики/Классы/ОтелПредставление.os:83` |  |
| 129 | MUST | ✅ found | This extension MUST be configurable on a metric View. | `src/Метрики/Классы/ОтелПредставление.os:163` |  |
| 130 | MUST | ⚠️ partial | Individual reservoirs MUST still be instantiated per metric-timeseries. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` | Резервуар создаётся один на инструмент, а не per metric-timeseries. Внутри резервуара данные разделены по КлючАтрибутов, что функционально эквивалентно per-timeseries, но архитектурно это один экземпляр резервуара. |

#### MetricReader operations#### Collect

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader-operations-collect)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 131 | SHOULD | ✅ found | Collect SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:123` |  |
| 132 | SHOULD | ❌ not_found | Collect SHOULD invoke Produce on registered MetricProducers. | - | MetricProducer интерфейс не реализован. Нет механизма регистрации внешних MetricProducer'ов и вызова Produce при Collect. |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 133 | MUST | ✅ found | Shutdown MUST be called only once for each MetricReader instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:89` |  |
| 134 | SHOULD | ⚠️ partial | After the call to Shutdown, subsequent invocations to Collect are not allowed. SDKs SHOULD return some failure for these calls, if possible. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:59` | Метод ПериодическийСбор проверяет флаг Закрыт и прекращает цикл, но публичный метод СброситьБуфер (аналог Collect) не проверяет состояние Закрыт и не возвращает ошибку при вызове после Shutdown. |
| 135 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88` | Метод Закрыть() является процедурой и не возвращает результат (успех/неуспех/таймаут). Внутри обрабатывает таймаут фонового задания через исключение, но вызывающий код не получает результат. |
| 136 | SHOULD | ✅ found | Shutdown SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` |  |

#### Periodic exporting MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 137 | MUST | ✅ found | The reader MUST synchronize calls to MetricExporter's Export to make sure that they are not invoked concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:124` |  |
| 138 | SHOULD | ✅ found | ForceFlush SHOULD collect metrics, call Export(batch) and ForceFlush() on the configured Push Metric Exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` |  |
| 139 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` | СброситьБуфер() является процедурой, не возвращает результат (успех/ошибка/таймаут). Ошибки экспорта перехватываются внутри через Попытка, но не транслируются вызывающему коду. |
| 140 | SHOULD | ⚠️ partial | ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` | СброситьБуфер() не возвращает статус ERROR/NO ERROR. Внутри экспортер возвращает Булево, но эта информация не пробрасывается вызывающему коду. |
| 141 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` | СброситьБуфер() вызывает СобратьИЭкспортировать() синхронно без таймаута. Нет механизма ограничения времени выполнения ForceFlush. |

#### MetricExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 142 | MUST | ✅ found | MetricExporter defines the interface that protocol-specific exporters MUST implement so that they can be plugged into OpenTelemetry SDK and support sending of telemetry data. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25` |  |
| 143 | SHOULD | ❌ not_found | Metric Exporters SHOULD report an error condition for data output by the MetricReader with unsupported Aggregation or Aggregation Temporality. | - | Экспортер не проверяет неподдерживаемые типы агрегации или временности. Данные передаются на транспорт без валидации. |
| 144 | MUST | ✅ found | A Push Metric Exporter MUST support the following functions: Export(batch). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25` |  |
| 145 | MUST | ✅ found | The SDK MUST provide a way for the exporter to get the Meter information (e.g. name, version, etc.) associated with each Metric Point. | `src/Метрики/Классы/ОтелДанныеМетрики.os:42` |  |
| 146 | MUST NOT | ⚠️ partial | Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25` | Экспорт делегирует транспорту (HTTP), который имеет таймауты на уровне HTTP-клиента, но в самом экспортере нет явного верхнего ограничения таймаута. |
| 147 | SHOULD NOT | ✅ found | The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25` |  |
| 148 | SHOULD | ✅ found | ForceFlush of the export of any Metrics the exporter has received prior to the call SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` |  |
| 149 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` | СброситьБуфер() является процедурой и не возвращает статус успеха/ошибки/таймаута. |
| 150 | SHOULD | ⚠️ partial | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` | Это рекомендация к использованию, а не к реализации. Метод существует, но нет документации/ограничения на стороне SDK о том, когда его вызывать. |
| 151 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` | СброситьБуфер() синхронный no-op (нет буферизации), фактически завершается мгновенно, но нет механизма таймаута, если бы логика была сложнее. |
| 152 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each MetricExporter instance. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` |  |
| 153 | SHOULD | ✅ found | After the call to Shutdown subsequent calls to Export are not allowed and should return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:26` |  |
| 154 | SHOULD NOT | ✅ found | Shutdown SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` |  |

#### Pull Metric Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#pull-metric-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 155 | MUST | ❌ not_found | MetricProducer defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data. | - | No MetricProducer interface/class exists in the codebase. The pull exporter (ОтелПрометеусЧитательМетрик) is modeled as a MetricReader, not via a separate MetricProducer interface for bridging third-party sources. |
| 156 | SHOULD | ❌ not_found | MetricProducer implementations SHOULD accept configuration for the AggregationTemporality of produced metrics. | - | No MetricProducer exists, so there is no temporality configuration for it. The Prometheus reader does not accept AggregationTemporality configuration. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 157 | MUST | ❌ not_found | A MetricProducer MUST support the following functions (Produce). | - | No MetricProducer interface exists. There is no Produce method. Metric collection is done internally within MetricReader implementations (СобратьИЭкспортировать), not via a separate MetricProducer.Produce interface. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 158 | MUST | ✅ found | A MetricFilter MUST support the following functions (TestMetric, TestAttributes). | `src/Метрики/Классы/ОтелФильтрМетрик.os:29` |  |

#### TestMetric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#testmetric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 159 | MUST | ⚠️ partial | The SDK MUST provide configuration according to the SDK environment variables specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:110` | Some metrics env vars are read (OTEL_METRICS_EXEMPLAR_FILTER in builder, OTEL_METRICS_EXPORTER and OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE in autoconfiguration), but not all SDK env vars for metrics are fully supported (e.g., OTEL_METRIC_EXPORT_INTERVAL, OTEL_METRIC_EXPORT_TIMEOUT are not read from environment). |

#### Numerical limits handling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#numerical-limits-handling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 160 | MUST | ❌ not_found | The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry. | - | No explicit numerical limits handling found in metrics code. No checks for overflow, underflow, or special float values in aggregators or instruments. |
| 161 | MUST | ❌ not_found | If the SDK receives float/double values from Instruments, it MUST handle all the possible values (e.g. NaN and Infinities for IEEE 754). | - | No NaN or Infinity handling found in metrics aggregators (ОтелАгрегаторСуммы, ОтелАгрегаторГистограммы, ОтелАгрегаторПоследнегоЗначения). Values are used directly without any special-value checks. |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 162 | SHOULD | ✅ found | All the metrics components SHOULD allow new methods to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:231` |  |
| 163 | SHOULD | ✅ found | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to existing methods without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 164 | MUST | ⚠️ partial | MeterProvider - Meter creation, ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:241` | Meter creation uses СинхронизированнаяКарта (thread-safe map) for meter cache, but the Закрыт flag is a plain Булево (not atomic), creating potential race conditions between ПолучитьМетр, СброситьБуфер, and Закрыть. |
| 165 | MUST | ⚠️ partial | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:167` | Uses СинхронизированнаяКарта and АтомарноеЧисло for individual operations, but the compound operation in ДобавитьВРезервуар (get array, check size, add/replace element) is not atomic - concurrent threads may race on the same array. |
| 166 | MUST | ✅ found | MetricReader - Collect, ForceFlush (for periodic exporting MetricReader) and Shutdown MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:283` |  |
| 167 | MUST | ⚠️ partial | MetricExporter - ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` | ОтелЭкспортерМетрик.Закрыть sets Закрыт = Истина (plain boolean, not atomic) without any lock. No concurrency protection between Экспортировать and Закрыть. |

### Otlp Exporter

#### Configuration Options

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#configuration-options)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | The following configuration options MUST be available to configure the OTLP exporter (Endpoint, Insecure, Certificate File, Client key file, Client certificate file, Headers, Compression, Timeout, Protocol). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130` | Endpoint, Headers, Compression, Timeout, Protocol доступны. TLS-опции (Certificate File, Client key, Client certificate) не реализованы (ограничение платформы). Insecure не реализован (спецификация допускает MAY для этой опции). |
| 2 | MUST | ❌ not_found | Each configuration option MUST be overridable by a signal specific option (e.g. OTEL_EXPORTER_OTLP_TRACES_ENDPOINT overrides OTEL_EXPORTER_OTLP_ENDPOINT for traces). | - | Сигнал-специфичные переменные (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_ENDPOINT и т.д.) не реализованы. Используется только общий otel.exporter.otlp.endpoint без возможности переопределения по сигналу. |
| 3 | MUST | ✅ found | The implementation MUST honor the following URL components: scheme (http or https), host, port, path. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:161` |  |
| 4 | MUST | ✅ found | When using OTEL_EXPORTER_OTLP_ENDPOINT, exporters MUST construct per-signal URLs as described below (Traces: v1/traces, Metrics: v1/metrics, Logs: v1/logs). | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:35` |  |
| 5 | SHOULD | ✅ found | Endpoint (OTLP/gRPC): The option SHOULD accept any form allowed by the underlying gRPC client implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:174` |  |
| 6 | MUST | ✅ found | Endpoint (OTLP/gRPC): the option MUST accept a URL with a scheme of either http or https. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:174` |  |
| 7 | SHOULD | ✅ found | If the gRPC client implementation does not support an endpoint with a scheme of http or https then the endpoint SHOULD be transformed to the most sensible format for that implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:174` |  |
| 8 | MUST | ⚠️ partial | Protocol: Options MUST be one of: grpc, http/protobuf, http/json. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Поддерживаются grpc и http/json. Протокол http/protobuf не реализован - HTTP-транспорт всегда отправляет JSON (Content-Type: application/json). |
| 9 | SHOULD | ✅ found | SDKs SHOULD default endpoint variables to use http scheme unless they have good reasons to choose https scheme for the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:158` |  |
| 10 | SHOULD | ➖ n_a | The environment variables OTEL_EXPORTER_OTLP_SPAN_INSECURE and OTEL_EXPORTER_OTLP_METRIC_INSECURE are obsolete. However, if they are already implemented, they SHOULD continue to be supported as they were part of a stable release of the specification. | - | Требование условное: применяется только к SDK, которые ранее реализовали эти устаревшие переменные. Данный SDK никогда их не реализовывал, поэтому условие неприменимо. |
| 11 | SHOULD | ⚠️ partial | The default protocol SHOULD be http/protobuf, unless there are strong reasons for SDKs to select grpc as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Протокол по умолчанию http/json (строка 150: Параметр 'otel.exporter.otlp.protocol', 'http/json'), а не рекомендуемый http/protobuf. |
| 12 | MUST | ✅ found | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal: Traces v1/traces, Metrics v1/metrics, Logs v1/logs relative to the base URL. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:99` |  |
| 13 | MUST | ❌ not_found | For the per-signal variables (OTEL_EXPORTER_OTLP_<signal>_ENDPOINT), the URL MUST be used as-is without any modification. | - | Сигнал-специфичные переменные окружения (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT и т.д.) не реализованы, поэтому поведение 'use as-is' невозможно проверить. |
| 14 | MUST | ❌ not_found | The only exception is that if an URL contains no path part, the root path / MUST be used (for per-signal endpoint variables). | - | Сигнал-специфичные переменные окружения не реализованы, поэтому обработка URL без пути невозможна. |
| 15 | MUST NOT | ✅ found | An SDK MUST NOT modify the URL in ways other than specified above. If the port is empty or not given, TCP port 80 is the default for http and 443 for https as per RFC 7230. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:99` |  |

#### Specify Protocol

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specify-protocol)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ⚠️ partial | SDKs SHOULD support both grpc and http/protobuf transports. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:1` | Поддерживаются grpc (ОтелGrpcТранспорт) и http/json (ОтелHttpТранспорт). Транспорт http/protobuf не реализован. |
| 17 | MUST | ✅ found | SDKs MUST support at least one of grpc or http/protobuf transports. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:1` |  |
| 18 | SHOULD | ⚠️ partial | If they support only one transport, it SHOULD be http/protobuf. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:1` | SDK поддерживает два транспорта (grpc и http/json), но ни один из них не является http/protobuf. |
| 19 | SHOULD | ⚠️ partial | If no configuration is provided the default transport SHOULD be http/protobuf unless SDKs have good reasons to choose grpc as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Транспорт по умолчанию - http/json, а не рекомендуемый http/protobuf. |

#### Specifying headers via environment variables

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | All attribute values in OTEL_EXPORTER_OTLP_HEADERS MUST be considered strings (format: key1=value1,key2=value2 matching W3C Baggage). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:479` |  |

#### Retry

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#retry)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | Transient errors MUST be handled with a retry strategy. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:76` |  |
| 22 | MUST | ✅ found | This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:166` |  |

#### Transient errors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#transient-errors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | SHOULD | ❌ not_found | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter. | - | Ни HTTP-транспорт, ни gRPC-транспорт не устанавливают заголовок User-Agent. |
| 24 | SHOULD | ❌ not_found | The format of the User-Agent header SHOULD follow RFC 7231. | - | Заголовок User-Agent не реализован вообще. |
| 25 | SHOULD | ❌ not_found | The resulting User-Agent SHOULD include the exporter's default User-Agent string when a product identifier is added via configuration. | - | Заголовок User-Agent не реализован вообще, конфигурация product identifier отсутствует. |

### Propagators

#### Operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Propagators MUST define Inject and Extract operations, in order to write values to and read values from carriers respectively. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:45,81` |  |
| 2 | MUST | ✅ found | Each Propagator type MUST define the specific carrier type and MAY define additional parameters. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:45` |  |

#### Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The Propagator MUST retrieve the appropriate value from the Context first, such as SpanContext, Baggage or another cross-cutting concern context. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:46` |  |
| 4 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:89-115` |  |
| 5 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, the implementation MUST NOT store a new value in the Context, in order to preserve any previously existing valid value. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:90,95,100,114` |  |

#### TextMap Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | The key/value pairs MUST only consist of US-ASCII characters that make up valid HTTP header fields as per RFC 9110. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:62-63` |  |
| 7 | MUST | ✅ found | Getter and Setter MUST be stateless and allowed to be saved as constants, in order to effectively avoid runtime allocations. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:71-73` |  |

#### TextMap Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform Content-Type to content-type) if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:18-20` |  |
| 9 | MUST | ✅ found | The implementation MUST preserve casing if the used protocol is case sensitive. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:18-20` |  |

#### Getter argument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#getter-argument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The Keys function MUST return the list of all the keys in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:59-65` |  |
| 11 | MUST | ✅ found | The Get function MUST return the first value of the given propagation key or return null if the key doesn't exist. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:20-28` |  |
| 12 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter (Get) MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:21-23` |  |
| 13 | MUST | ✅ found | If explicitly implemented, the GetAll function MUST return all values of the given propagation key. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40-49` |  |
| 14 | SHOULD | ✅ found | GetAll SHOULD return values in the same order as they appear in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40-49` |  |
| 15 | SHOULD | ✅ found | If the key doesn't exist, GetAll SHOULD return an empty collection. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:41-48` |  |
| 16 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter (GetAll) MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:42-45` |  |

#### Composite Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | Implementations MUST offer a facility to group multiple Propagators from different cross-cutting concerns in order to leverage them as a single entity. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:1-84` |  |
| 18 | MUST | ✅ found | There MUST be functions to accomplish the following operations: Create a composite propagator, Extract from a composite propagator, Inject into a composite propagator. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:79,18,35` |  |

#### Composite Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | The OpenTelemetry API MUST provide a way to obtain a propagator for each supported Propagator type. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |
| 20 | SHOULD | ✅ found | Instrumentation libraries SHOULD call propagators to extract and inject the context on all remote calls. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:18` |  |
| 21 | MUST | ✅ found | The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise. | `src/Ядро/Модули/ОтелГлобальный.os:132` |  |
| 22 | SHOULD | ❌ not_found | If pre-configured, Propagators SHOULD default to a composite Propagator containing the W3C Trace Context Propagator and the Baggage Propagator specified in the Baggage API. | - | Реализация не предоставляет предконфигурированных пропагаторов по умолчанию. При отсутствии явной конфигурации ОтелГлобальный.ПолучитьПропагаторы() возвращает NoOp пропагатор, а не композитный пропагатор с W3C TraceContext + Baggage. |
| 23 | MUST | ✅ found | These platforms MUST also allow pre-configured propagators to be disabled or overridden. | `src/Ядро/Модули/ОтелГлобальный.os:110` |  |

#### Get Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#get-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | This method MUST exist for each supported Propagator type. Returns a global Propagator. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |

#### Set Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#set-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | This method MUST exist for each supported Propagator type. Sets the global Propagator instance. | `src/Ядро/Модули/ОтелГлобальный.os:110` |  |
| 26 | MUST | ⚠️ partial | The official list of propagators that MUST be maintained by the OpenTelemetry organization: W3C TraceContext, W3C Baggage, B3. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:1` | W3C TraceContext (ОтелW3CПропагатор) и W3C Baggage (ОтелW3CBaggageПропагатор) реализованы. B3 Propagator не реализован. |
| 27 | MUST | ⚠️ partial | The official list of propagators MUST be distributed as OpenTelemetry extension packages: W3C TraceContext (MAY be part of API), W3C Baggage (MAY be part of API), B3. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:1` | W3C TraceContext и Baggage распространяются как часть основного пакета (допустимо по спецификации через MAY). B3 Propagator не реализован и не распространяется. |
| 28 | MUST NOT | ➖ n_a | OT Trace propagator MUST NOT use `OpenTracing` in the resulting propagator name as it is not widely adopted format in the OpenTracing ecosystem. | - | OT Trace propagator не реализован (deprecated формат). Условная фича, не реализована. |
| 29 | MUST NOT | ✅ found | Additional Propagators implementing vendor-specific protocols such as AWS X-Ray trace header protocol MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | `src/Пропагация/Классы/` |  |

#### W3C Trace Context Requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#w3c-trace-context-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | A W3C Trace Context propagator MUST parse and validate the traceparent and tracestate HTTP headers as specified in W3C Trace Context Level 2. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:81` |  |
| 31 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid traceparent value using the same header. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:63` |  |
| 32 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid tracestate unless the value is empty, in which case the tracestate header may be omitted. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:65` |  |

### Env Vars

#### Environment Variable Specification

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#environment-variable-specification)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If they do, they SHOULD use the names and value parsing behavior specified in this document. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:6-34` |  |
| 2 | SHOULD | ✅ found | They SHOULD also follow the common configuration specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:80-86` |  |

#### Implementation guidelines

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#implementation-guidelines)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The environment-based configuration MUST have a direct code configuration equivalent. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:59` |  |

#### Parsing empty value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#parsing-empty-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ⚠️ partial | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105,340` | Обработка пустых значений реализована частично: для ресурсных атрибутов (строка 105) и пропагаторов (строка 340) пустые значения проверяются явно (<> ""), но для многих других параметров (otel.service.name строка 114, числовые параметры строки 224-227) пустая строка не проверяется и может привести к ошибкам. ПровайдерПараметровENV не фильтрует пустые значения на уровне провайдера. |

#### Type-specific guidance### Boolean

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#type-specific-guidance-boolean)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Any value that represents a Boolean MUST be set to true only by the case-insensitive string "true", meaning "True" or "TRUE" are also accepted, as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 6 | MUST NOT | ✅ found | An implementation MUST NOT extend this definition and define additional values that are interpreted as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 7 | MUST | ✅ found | Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563` |  |
| 8 | SHOULD | ❌ not_found | If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied. | - | Функция Включено() на строке 561-564 просто проверяет НРег(Значение) = "true" и возвращает Ложь для любого другого значения, но не логирует предупреждение при получении нестандартного значения (например "yes", "1"). |
| 9 | SHOULD | ⚠️ partial | All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:7,562` | Вместо стандартной OTEL_SDK_DISABLED (где false = SDK включен, безопасное значение по умолчанию) используется нестандартная OTEL_ENABLED (где true = SDK включен). Логика инвертирована относительно спецификации: в спеке disabled=false это безопасный дефолт, здесь enabled=true. |
| 10 | MUST NOT | ✅ found | Renaming or changing the default value MUST NOT happen without a major version upgrade. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562` |  |

#### Numeric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#numeric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ❌ not_found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning. | - | Числовые параметры (строки 224-227, 263-266, 312, 395-416) конвертируются через Число() без try/catch. Если передана нечисловая строка, это вызовет исключение времени выполнения, а не предупреждение с graceful-игнорированием. |
| 12 | SHOULD | ❌ not_found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD gracefully ignore the setting, i.e., treat them as not set. | - | Вместо graceful-игнорирования некорректного числового значения, вызов Число() с невалидной строкой приведет к ошибке выполнения. Нет логики fallback на значение по умолчанию. |
| 13 | SHOULD | ❌ not_found | For new implementations, these should be treated as MUST requirements. | - | Так как предыдущие два SHOULD не реализованы, это meta-требование также не выполнено. |

#### String

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#string)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | SHOULD | ⚠️ partial | Enum values SHOULD be interpreted in a case-insensitive manner. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:344` | Пропагаторы обрабатываются case-insensitive (НРег на строке 344), но значения семплеров (строки 197-219) сравниваются case-sensitive (прямое сравнение без НРег). Аналогично exporter names (строки 177-178, 255-256, 291-292) сравниваются case-sensitive. |
| 15 | MUST | ⚠️ partial | For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:373` | Для пропагаторов неизвестное значение логируется через Сообщить() (строка 373) и пропускается. Однако для семплеров неизвестное значение молча подменяется на parentbased_always_on без предупреждения (строка 216-218). Для экспортеров неизвестное значение не обрабатывается - вероятно вызовет ошибку. |

#### General SDK ConfigurationNameDescriptionDefaultTypeNotesOTEL_SDK_DISABLEDDisable the SDK for all signalsfalseBooleanIf “true”, a no-op SDK implementation will be used for all telemetry signals. Any other value or absence of the variable will have no effect and the SDK will remain enabled. This setting has no effect on propagators configured through the OTEL_PROPAGATORS variable.OTEL_ENTITIESEntity information to be associated with the resourceStringSee Entities SDK for more details.OTEL_RESOURCE_ATTRIBUTESKey-value pairs to be used as resource attributesSee Resource semantic conventions for details.StringSee Resource SDK for more details.OTEL_SERVICE_NAMESets the value of the `service.name` resource attributeStringIf `service.name` is also provided in `OTEL_RESOURCE_ATTRIBUTES`, then `OTEL_SERVICE_NAME` takes precedence.OTEL_LOG_LEVELLog level used by the SDK internal logger“info”EnumOTEL_PROPAGATORSPropagators to be used as a comma-separated list“tracecontext,baggage”EnumValues MUST be deduplicated in order to register a `Propagator` only once.OTEL_TRACES_SAMPLERSampler to be used for traces“parentbased_always_on”EnumSee SamplingOTEL_TRACES_SAMPLER_ARGValue to be used as the sampler argumentSee footnoteThe specified value will only be used if OTEL_TRACES_SAMPLER is set. Each Sampler type defines its own expected input, if any. Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set.

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configurationnamedescriptiondefaulttypenotesotelsdkdisableddisable-the-sdk-for-all-signalsfalsebooleanif-true-a-no-op-sdk-implementation-will-be-used-for-all-telemetry-signals-any-other-value-or-absence-of-the-variable-will-have-no-effect-and-the-sdk-will-remain-enabled-this-setting-has-no-effect-on-propagators-configured-through-the-otelpropagators-variableotelentitiesentity-information-to-be-associated-with-the-resourcestringsee-entities-sdk-for-more-detailsotelresourceattributeskey-value-pairs-to-be-used-as-resource-attributessee-resource-semantic-conventions-for-detailsstringsee-resource-sdk-for-more-detailsotelservicenamesets-the-value-of-the-servicename-resource-attributestringif-servicename-is-also-provided-in-otelresourceattributes-then-otelservicename-takes-precedenceotelloglevellog-level-used-by-the-sdk-internal-loggerinfoenumotelpropagatorspropagators-to-be-used-as-a-comma-separated-listtracecontextbaggageenumvalues-must-be-deduplicated-in-order-to-register-a-propagator-only-onceoteltracessamplersampler-to-be-used-for-tracesparentbasedalwaysonenumsee-samplingoteltracessamplerargvalue-to-be-used-as-the-sampler-argumentsee-footnotethe-specified-value-will-only-be-used-if-oteltracessampler-is-set-each-sampler-type-defines-its-own-expected-input-if-any-invalid-or-unrecognized-input-must-be-logged-and-must-be-otherwise-ignored-ie-the-implementation-must-behave-as-if-oteltracessamplerarg-is-not-set)

> ⚠️ Нет данных от агента (ожидалось ~5 требований)

## Требования Development-статуса

Эти требования находятся в секциях со статусом Development. Их реализация не обязательна для соответствия стабильной спецификации.

### Resource Sdk

#### Resource detector name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-detector-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | Resource detectors SHOULD have a unique name for reference in configuration. | - | Детекторы ресурсов (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) не имеют свойства имени для конфигурации |
| 2 | SHOULD | ❌ not_found | Names SHOULD be snake case and consist of lowercase alphanumeric and _ characters, which ensures they conform to declarative configuration property name requirements. | - | У детекторов отсутствуют имена, соответственно конвенция snake_case не применяется |
| 3 | SHOULD | ❌ not_found | Resource detector names SHOULD reflect the root namespace of attributes they populate. | - | У детекторов отсутствуют имена |
| 4 | SHOULD | ❌ not_found | Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name which appropriately conveys their purpose. | - | У детекторов отсутствуют имена |
| 5 | SHOULD | ❌ not_found | An SDK which identifies multiple resource detectors with the same name SHOULD report an error. | - | У детекторов отсутствуют имена, проверка дублирования не реализована |
| 6 | SHOULD | ❌ not_found | Resource detectors SHOULD document their name in a manner which is easily discoverable. | - | У детекторов отсутствуют имена, документация имён не реализована |
| 7 | MUST | ✅ found | The SDK MUST extract information from the OTEL_RESOURCE_ATTRIBUTES environment variable and merge this, as the secondary resource, with any resource information provided by the user, i.e. the user provided resource information has higher priority. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:101` |  |
| 8 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:479` |  |
| 9 | MUST | ❌ not_found | The , and = characters in keys and values MUST be percent encoded. Other characters MAY be percent-encoded. | - | Парсер РазобратьПарыКлючЗначение разбивает строку по , и = без percent-декодирования ключей и значений - символы %2C, %3D и другие percent-кодированные последовательности не декодируются |
| 10 | SHOULD | ⚠️ partial | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:477` | Отдельные некорректные пары (без =) пропускаются, но при ошибке не отбрасывается всё значение переменной целиком как требует спецификация |
| 11 | SHOULD | ❌ not_found | In case of any error an error SHOULD be reported following the Error Handling principles. | - | При ошибках парсинга OTEL_RESOURCE_ATTRIBUTES не генерируется сообщение об ошибке |

### Trace Api

#### Tracer operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracer-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The Tracer MUST provide functions to: Create a new Span | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 2 | SHOULD | ✅ found | The Tracer SHOULD provide functions to: Report if Tracer is Enabled | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 3 | SHOULD | ✅ found | A Tracer SHOULD provide this Enabled API to help users avoid performing computationally expensive operations when creating Spans. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 4 | MUST | ✅ found | The API MUST be structured in a way for parameters to be added. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 5 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 6 | SHOULD | ❌ not_found | The API SHOULD be documented that instrumentation authors needs to call this API each time they create a new Span to ensure they have the most up-to-date response. | - | Метод Включен() существует, но в его документации (комментарии) нет указания о том, что инструментаторы должны вызывать его каждый раз перед созданием нового спана для получения актуального ответа. |

### Trace Sdk

#### Tracer Provider### Tracer Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer-provider-tracer-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ⚠️ partial | It SHOULD only be possible to create Tracer instances through a TracerProvider | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` | TracerProvider.ПолучитьТрассировщик() is the intended factory method, but OneScript cannot restrict constructor access - ОтелТрассировщик can be instantiated directly via Новый ОтелТрассировщик() |
| 2 | MUST | ✅ found | The TracerProvider MUST implement the Get a Tracer API | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Tracer | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:63` |  |
| 4 | MUST | ✅ found | The TracerProvider MUST compute the relevant TracerConfig using the configured TracerConfigurator, and create a Tracer whose behavior conforms to that TracerConfig | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:71` |  |

#### TracerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The TracerConfigurator function MUST accept the following parameter: tracer_scope - the InstrumentationScope of the Tracer | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:220` |  |
| 2 | MUST | ✅ found | The TracerConfigurator function MUST return the relevant TracerConfig, or some signal indicating that the default TracerConfig should be used | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:215` |  |
| 3 | MUST | ✅ found | Shutdown MUST be called only once for each TracerProvider instance | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:108` |  |
| 4 | SHOULD | ⚠️ partial | After the call to Shutdown, subsequent attempts to get a Tracer are not allowed. SDKs SHOULD return a valid no-op Tracer for these calls, if possible | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65` | After Shutdown, ПолучитьТрассировщик returns a regular ОтелТрассировщик (not a no-op Tracer). The returned Tracer references the closed Provider but is not a true no-op implementation |
| 5 | SHOULD | ❌ not_found | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out | - | Закрыть() is a Процедура (void return), provides no indication of success, failure, or timeout to the caller |
| 6 | SHOULD | ❌ not_found | Shutdown SHOULD complete or abort within some timeout | - | Закрыть() has no timeout mechanism - it blocks indefinitely while iterating over processors calling Закрыть() on each |
| 7 | MUST | ✅ found | Shutdown MUST be implemented at least by invoking Shutdown within all internal processors | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:111` |  |

#### Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Tracer MUST behave according to the TracerConfig computed during Tracer creation | `src/Трассировка/Классы/ОтелТрассировщик.os:39` |  |
| 2 | MUST | ❌ not_found | If the TracerProvider supports updating the TracerConfigurator, then upon update the Tracer MUST be updated to behave according to the new TracerConfig | - | TracerConfig is set once during Tracer creation and stored as a reference. There is no mechanism to re-compute and update TracerConfig for already-created Tracers when the TracerConfigurator changes. The Конфигурация field has no public setter and cached Tracers are not revisited |

#### TracerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the enabled parameter SHOULD default to true (i.e. Tracers are enabled by default) | `src/Трассировка/Классы/ОтелКонфигурацияТрассировщика.os:35` |  |
| 2 | MUST | ⚠️ partial | If a Tracer is disabled, it MUST behave equivalently to a No-op Tracer | `src/Трассировка/Классы/ОтелТрассировщик.os:39` | Tracer.Включен() reports disabled state via TracerConfig, but НачатьСпан()/НачатьКорневойСпан()/НачатьДочернийСпан() do not check Включен() before creating spans. A disabled Tracer still creates real spans instead of returning no-op spans |
| 3 | MUST | ✅ found | The value of enabled MUST be used to resolve whether a Tracer is Enabled. If enabled is false, Enabled returns false. If enabled is true, Enabled returns true | `src/Трассировка/Классы/ОтелТрассировщик.os:39` |  |
| 4 | MUST | ❌ not_found | The changes to TracerConfig parameters MUST be eventually visible to callers of Enabled | - | TracerConfig is immutable after creation - УстановитьВключен() is private (not exported). There is no mechanism to update TracerConfig for existing Tracers, so changes cannot become visible |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Enabled MUST return false when either: there are no registered SpanProcessors, or Tracer is disabled (TracerConfig.enabled is false) | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 2 | SHOULD | ✅ found | Otherwise, Enabled SHOULD return true | `src/Трассировка/Классы/ОтелТрассировщик.os:42` |  |

#### AlwaysOn* Returns `RECORD_AND_SAMPLE` always.* Description MUST be `AlwaysOnSampler`.#### AlwaysOff* Returns `DROP` always.* Description MUST be `AlwaysOffSampler`.#### TraceIdRatioBased

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwayson-returns-recordandsample-always-description-must-be-alwaysonsampler-alwaysoff-returns-drop-always-description-must-be-alwaysoffsampler-traceidratiobased)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | AlwaysOn: Description MUST be AlwaysOnSampler | `src/Трассировка/Модули/ОтелСэмплер.os:109` |  |
| 2 | MUST | ✅ found | AlwaysOff: Description MUST be AlwaysOffSampler | `src/Трассировка/Модули/ОтелСэмплер.os:111` |  |
| 3 | MUST | ✅ found | The TraceIdRatioBased MUST ignore the parent SampledFlag | `src/Трассировка/Модули/ОтелСэмплер.os:275-297` |  |
| 4 | MUST | ✅ found | TraceIdRatioBased Description MUST return a string of the form TraceIdRatioBased{RATIO} | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 5 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 6 | MUST | ✅ found | The sampling algorithm MUST be deterministic. A trace identified by a given TraceId is sampled or not independent of language, time, etc. | `src/Трассировка/Модули/ОтелСэмплер.os:275-297` |  |
| 7 | MUST | ✅ found | Implementations MUST use a deterministic hash of the TraceId when computing the sampling decision | `src/Трассировка/Модули/ОтелСэмплер.os:288-296` |  |
| 8 | MUST | ⚠️ partial | A TraceIdRatioBased sampler with a given sampling probability MUST also sample all traces that any TraceIdRatioBased sampler with a lower sampling probability would sample | `src/Трассировка/Модули/ОтелСэмплер.os:288-296` | The implementation uses first 8 hex chars of TraceId as hash and compares against threshold (MaxUint32 * ratio). This is a consistent monotonic comparison, so a higher ratio yields a higher threshold, and all traces sampled at lower ratio are also sampled at higher ratio. The property is satisfied by the algorithm design, but the hash only uses the first 32 bits of the TraceId, which may not be fully compatible with other SDK implementations that use different bits. |
| 9 | SHOULD | ❌ not_found | When this sampler observes a non-empty parent span context (used not as root sampler), the SDK SHOULD emit a warning about TraceIdRatioBased being used as child sampler | - | No warning is emitted when TraceIdRatioBased is used as a child sampler. The СэмплироватьПоДоле function has no awareness of parent context and no logging/warning mechanism. |
| 10 | MUST | ❌ not_found | The ProbabilitySampler sampler MUST ignore the parent SampledFlag | - | ProbabilitySampler is not implemented. Only TraceIdRatioBased sampler exists. |
| 11 | SHOULD | ❌ not_found | When ProbabilitySampler returns RECORD_AND_SAMPLE, the OpenTelemetry TraceState SHOULD be modified to include key-value th:T for rejection threshold | - | ProbabilitySampler is not implemented. |
| 12 | SHOULD | ❌ not_found | When ProbabilitySampler makes a decision for non-root Span using TraceID randomness when Random flag not set, the SDK SHOULD issue a warning | - | ProbabilitySampler is not implemented. |
| 13 | MUST | ❌ not_found | AlwaysRecord MUST behave as follows: DROP->RECORD_ONLY, RECORD_ONLY->RECORD_ONLY, RECORD_AND_SAMPLE->RECORD_AND_SAMPLE | - | AlwaysRecord sampler decorator is not implemented in the codebase. |
| 14 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the parameters passed to delegate GetSamplingIntent methods, as they are considered read-only state | - | ComposableSampler / CompositeSampler is not implemented. |
| 15 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the OpenTelemetry TraceState (the ot sub-key of TraceState) | - | ComposableSampler is not implemented. |
| 16 | SHOULD | ❌ not_found | The calling CompositeSampler SHOULD update the threshold of the outgoing TraceState (unless !threshold_reliable) | - | CompositeSampler is not implemented. |
| 17 | MUST | ❌ not_found | Explicit randomness values MUST not be modified (in ComposableSampler trace_state_provider) | - | ComposableSampler is not implemented. |
| 18 | SHOULD | ❌ not_found | For ComposableProbability, a ratio value of 0 is considered non-probabilistic. For the zero case a ComposableAlwaysOff instance SHOULD be returned instead | - | ComposableProbability is not implemented. |
| 19 | SHOULD | ✅ found | OpenTelemetry SDK implementors SHALL NOT remove or modify the behavior of the original TraceIdRatioBased sampler until at least January 1, 2027 | `src/Трассировка/Модули/ОтелСэмплер.os:81-83` |  |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | Custom implementations of the IdGenerator SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace random flag will be set in the associated Trace contexts. | - | No mechanism exists for custom IdGenerator implementations to declare whether they produce W3C Level 2 random TraceIDs. There is no marker interface or property to signal randomness compliance, and the random flag is not set based on IdGenerator identity. |

#### OnEnding

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onending)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The end timestamp MUST have been computed (the OnEnding method duration is not included in the span duration). | `src/Трассировка/Классы/ОтелСпан.os:449` |  |
| 2 | MUST | ✅ found | The Span object MUST still be mutable (i.e., SetAttribute, AddLink, AddEvent can be called) while OnEnding is called. | `src/Трассировка/Классы/ОтелСпан.os:455` |  |
| 3 | MUST | ✅ found | This method MUST be called synchronously within the Span.End() API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:455` |  |
| 4 | MUST | ⚠️ partial | The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking OnEnding of the first SpanProcessor. From that point on, modifications are only allowed synchronously from within the invoked OnEnding callbacks. All registered SpanProcessor OnEnding callbacks are executed before any SpanProcessor's OnEnd callback is invoked. | `src/Трассировка/Классы/ОтелСпан.os:455` | OnEnding (ПередЗавершением) is called before setting Завершен=Истина (line 457), so span is still mutable during OnEnding and immutable during OnEnd. However there is no explicit thread-safety guarantee that no other thread can modify the span before OnEnding - the Span class does not use locks/synchronization around mutations. The ordering of all OnEnding before any OnEnd is ensured by the CompositeProcessor calling ПередЗавершением for all processors first, then ПриЗавершении - but this happens inside Span.Завершить() which calls Процессор.ПередЗавершением then Процессор.ПриЗавершении sequentially. |

### Logs Api

#### Ergonomic API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#ergonomic-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | The ergonomic API SHOULD make it more convenient to emit event records following the event semantics. | - | Нет отдельного эргономичного API для генерации событий. Логирование выполняется через СоздатьЗаписьЛога() + ручное заполнение полей + Записать(), без упрощённого высокоуровневого метода для event records. |
| 2 | SHOULD | ❌ not_found | The design of the ergonomic API SHOULD be idiomatic for its language. | - | Эргономичный API отсутствует, поэтому оценить его идиоматичность невозможно. |

### Logs Sdk

#### Logger Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create Logger instances through a LoggerProvider (see API). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 2 | MUST | ✅ found | The LoggerProvider MUST implement the Get a Logger API. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Logger. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:64` |  |
| 4 | MUST | ✅ found | In the case where an invalid name (null or empty string) is specified, a working Logger MUST be returned as a fallback rather than returning null or throwing an exception. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 5 | SHOULD | ✅ found | its name SHOULD keep the original invalid value | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:64` |  |
| 6 | SHOULD | ❌ not_found | a message reporting that the specified value is invalid SHOULD be logged | - | ПолучитьЛоггер не проверяет ИмяБиблиотеки на пустую строку или null и не логирует предупреждение о невалидном имени |
| 7 | MUST | ✅ found | The LoggerProvider MUST compute the relevant LoggerConfig using the configured LoggerConfigurator, and create a Logger whose behavior conforms to that LoggerConfig. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:69` |  |

#### LoggerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: logger_scope: The InstrumentationScope of the Logger. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:72` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant LoggerConfig, or some signal indicating that the default LoggerConfig should be used. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:69` |  |
| 3 | MUST | ✅ found | Shutdown MUST be called only once for each LoggerProvider instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117` |  |
| 4 | SHOULD | ✅ found | After the call to Shutdown, subsequent attempts to get a Logger are not allowed. SDKs SHOULD return a valid no-op Logger for these calls, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:59` |  |
| 5 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:116` | Метод Закрыть() - Процедура (void), не возвращает статус успеха/ошибки/таймаута. Асинхронная версия ЗакрытьАсинхронно() возвращает Обещание, но синхронный Закрыть() молчит о результате. |
| 6 | SHOULD | ❌ not_found | Shutdown SHOULD complete or abort within some timeout. | - | Метод Закрыть() не имеет механизма таймаута - вызывает Закрыть() на каждом процессоре без ограничения по времени. |
| 7 | MUST | ✅ found | Shutdown MUST be implemented by invoking Shutdown on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:120` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Logger MUST behave according to the LoggerConfig computed during logger creation. | `src/Логирование/Классы/ОтелЛоггер.os:49-59` |  |
| 2 | MUST | ✅ found | If the LoggerProvider supports updating the LoggerConfigurator, then upon update the Logger MUST be updated to behave according to the new LoggerConfig. | `src/Логирование/Классы/ОтелЛоггер.os:123-125` |  |

#### LoggerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the enabled parameter SHOULD default to true (i.e. Loggers are enabled by default). | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 2 | MUST | ✅ found | If a Logger is disabled, it MUST behave equivalently to No-op Logger. | `src/Логирование/Классы/ОтелЛоггер.os:50-51` |  |
| 3 | MUST | ✅ found | If not explicitly set, the minimum_severity parameter MUST default to 0. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 4 | MUST | ✅ found | If a log record's SeverityNumber is specified (i.e. not 0) and is less than the configured minimum_severity, the log record MUST be dropped by the Logger. | `src/Логирование/Классы/ОтелЛоггер.os:53-56` |  |
| 5 | MUST | ✅ found | If not explicitly set, the trace_based parameter MUST default to false. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 6 | MUST | ✅ found | If trace_based is true, log records associated with unsampled traces MUST be dropped by the Logger. | `src/Логирование/Классы/ОтелЛоггер.os:57-59` |  |
| 7 | MUST | ✅ found | It is not necessary for implementations to ensure that changes to any of these parameters are immediately visible to callers of Enabled. However, the changes MUST be eventually visible. | `src/Логирование/Классы/ОтелЛоггер.os:123-125` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If Observed Timestamp is unspecified, the implementation SHOULD set it equal to the current time. | `src/Логирование/Классы/ОтелЛоггер.os:102-104` |  |
| 2 | MUST | ✅ found | If an Exception is provided, the SDK MUST by default set attributes from the exception on the LogRecord with the conventions outlined in the exception semantic conventions. | `src/Логирование/Классы/ОтелЛоггер.os:170-181` |  |
| 3 | MUST | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:183-187` |  |
| 4 | MUST NOT | ✅ found | User-provided attributes MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:183-187` |  |
| 5 | MUST | ✅ found | Before processing a log record, the implementation MUST apply the filtering rules defined by the LoggerConfig (in case Enabled was not called prior to emitting the record). | `src/Логирование/Классы/ОтелЛоггер.os:94-96` |  |
| 6 | MUST | ✅ found | Minimum severity: If the log record's SeverityNumber is specified (i.e. not 0) and is less than the configured minimum_severity, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:138-141` |  |
| 7 | MUST | ✅ found | Trace-based: If trace_based is true, and if the log record has a SpanId and the TraceFlags SAMPLED flag is unset, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:143-144` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | Enabled MUST return false when either: there are no registered LogRecordProcessors; Logger is disabled (LoggerConfig.enabled is false); the provided severity is specified (i.e. not 0) and is less than the configured minimum_severity; trace_based is true and the current context is associated with an unsampled trace; all registered LogRecordProcessors implement Enabled and a call to Enabled on each of them returns false. | `src/Логирование/Классы/ОтелЛоггер.os:42-62` | Conditions 1-4 are implemented correctly. Condition 5 (delegating Enabled to each processor) is not implemented - the code does not check individual processor Enabled methods. |
| 2 | SHOULD | ✅ found | Otherwise, Enabled SHOULD return true. | `src/Логирование/Классы/ОтелЛоггер.os:61` |  |

### Metrics Api

#### General characteristics#### Instrument name syntax

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-characteristics-instrument-name-syntax)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD treat the unit as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:66-67` |  |
| 2 | MUST | ✅ found | The unit MUST be case-sensitive (e.g. kb and kB are different units), ASCII string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:219-221` |  |
| 3 | MUST | ✅ found | The API MUST treat the description as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:226-229` |  |
| 4 | MUST | ✅ found | The description MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:226-229` |  |
| 5 | MUST | ✅ found | The description MUST support at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:226-229` |  |
| 6 | MUST | ✅ found | OpenTelemetry SDKs MUST handle advisory parameters as described here. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

### Metrics Sdk

#### Meter Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create Meter instances through a MeterProvider (see API). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 2 | MUST | ✅ found | The MeterProvider MUST implement the Get a Meter API. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Meter. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:62` |  |
| 4 | MUST | ✅ found | In the case where an invalid name (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 5 | SHOULD | ✅ found | its name SHOULD keep the original invalid value | `src/Метрики/Классы/ОтелПровайдерМетрик.os:62` |  |
| 6 | SHOULD | ❌ not_found | a message reporting that the specified value is invalid SHOULD be logged | - | В методе ПолучитьМетр нет проверки имени на пустое/null значение и нет логирования предупреждения о невалидном имени |
| 7 | MUST | ✅ found | The MeterProvider MUST compute the relevant MeterConfig using the configured MeterConfigurator, and create a Meter whose behavior conforms to that MeterConfig. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:206` |  |

#### MeterConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: meter_scope: The InstrumentationScope of the Meter. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:210` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant MeterConfig, or some signal indicating that the default MeterConfig should be used. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:211` |  |
| 3 | MUST | ✅ found | Shutdown MUST be called only once for each MeterProvider instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` |  |
| 4 | SHOULD | ✅ found | After the call to Shutdown, subsequent attempts to get a Meter are not allowed. SDKs SHOULD return a valid no-op Meter for these calls, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:57` |  |
| 5 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` | Метод Закрыть() - процедура без возвращаемого значения. Есть ЗакрытьАсинхронно() с Обещание, но синхронный вариант не возвращает статус успеха/ошибки/таймаута |
| 6 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` | Синхронный Закрыть() не имеет явного таймаута. Читатели внутри используют таймаут при ожидании фонового задания, но сам метод провайдера таймаут не принимает |
| 7 | MUST | ✅ found | Shutdown MUST be implemented at least by invoking Shutdown on all registered MetricReader and MetricExporter instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:136` |  |

#### Start timestamps

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#start-timestamps)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp, or the creation time of the instrument if this is the first collection interval for the instrument. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138-146` | For delta, ВремяСтарта is reset to current time after each export (line 145). This makes the start timestamp equal the end of the previous interval, not the start. The first interval uses instrument creation time (line 263) which is correct. |
| 2 | MUST | ⚠️ partial | This implies that all data points with delta temporality aggregation for an instrument MUST share the same start timestamp. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:283` | All data points in one collection share ВремяСтарта (line 283), but for new series created mid-interval they also use the same ВремяСтарта which is correct. The issue is the same as above - after clear, the start time is current time, not previous collection time. |
| 3 | MUST | ⚠️ partial | Cumulative timeseries MUST use a consistent start timestamp for all collection intervals. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141-142` | For cumulative, ВремяСтарта is preserved (not reset in ОчиститьТочкиДанных), so it stays as instrument creation time. This is correct for synchronous instruments. For asynchronous instruments, startTimeUnixNano is set to current time each collection (line 184 of ОтелБазовыйНаблюдаемыйИнструмент.os), which violates consistent start timestamp. |
| 4 | SHOULD | ⚠️ partial | For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the series. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:263` | Start timestamp is set to instrument creation time, not the time of the first measurement for a specific series. All series share the same start time from instrument init. |
| 5 | SHOULD | ❌ not_found | For asynchronous instruments, the start timestamp SHOULD be: the creation time of the instrument if first series measurement occurred in the first collection interval, otherwise the timestamp of the collection interval prior to the first series measurement. | - | Async instruments (ОтелБазовыйНаблюдаемыйИнструмент.os:184) set both startTimeUnixNano and timeUnixNano to current time on every collection. There is no tracking of instrument creation time or first measurement timing for start timestamp calculation. |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instrument registrations. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:64` |  |
| 2 | MUST | ✅ found | Meter MUST behave according to the MeterConfig computed during Meter creation. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:206` |  |
| 3 | MUST | ⚠️ partial | If the MeterProvider supports updating the MeterConfigurator, then upon update the Meter MUST be updated to behave according to the new MeterConfig. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:267` | МетрВключен is an АтомарноеБулево shared between meter and instruments, enabling dynamic updates. However, ОтелПровайдерМетрик has no public API to update the MeterConfigurator after construction - the Конфигуратор is set once in the constructor and never updated. |

#### MeterConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the enabled parameter SHOULD default to true (i.e. Meters are enabled by default). | `src/Метрики/Классы/ОтелКонфигурацияМетра.os:35` |  |
| 2 | MUST | ✅ found | If a Meter is disabled, it MUST behave equivalently to No-op Meter. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:79` |  |
| 3 | MUST | ✅ found | The value of enabled MUST be used to resolve whether an instrument is Enabled. See Instrument Enabled for details. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 4 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Метрики/Классы/ОтелМетр.os:344` |  |

#### Instrument enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The synchronous instrument Enabled MUST return false when either: the MeterConfig of the Meter used to create the instrument has parameter enabled=false, or all resolved views for the instrument are configured with the Drop Aggregation. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return true. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:267` |  |

#### MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | To construct a MetricReader when setting up an SDK, the exporter to use, which is a MetricExporter instance, SHOULD be provided. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:276` |  |
| 2 | SHOULD | ✅ found | The default output aggregation (optional), a function of instrument kind, SHOULD be obtained from the exporter. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:61` |  |
| 3 | SHOULD | ✅ found | If default aggregation is not configured, the default aggregation SHOULD be used. | `src/Метрики/Модули/ОтелАгрегация.os:15` |  |
| 4 | SHOULD | ✅ found | The output temporality (optional), a function of instrument kind, SHOULD be obtained from the exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:168` |  |
| 5 | SHOULD | ✅ found | If temporality is not configured, the Cumulative temporality SHOULD be used. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:88` |  |
| 6 | SHOULD | ✅ found | The default aggregation cardinality limit (optional), if not configured, a default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` |  |
| 7 | SHOULD | ✅ found | A MetricReader SHOULD provide the MetricFilter to the SDK or registered MetricProducer(s) when calling the Produce operation. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:110` |  |
| 8 | SHOULD | ✅ found | A common implementation of MetricReader, the periodic exporting MetricReader SHOULD be provided to be used typically with push-based metrics collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:1` |  |
| 9 | MUST | ✅ found | The MetricReader MUST ensure that data points from OpenTelemetry instruments are output in the configured aggregation temporality for each instrument kind. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:168` |  |
| 10 | MUST | ✅ found | For synchronous instruments with Cumulative aggregation temporality, MetricReader.Collect MUST receive data points exposed in previous collections regardless of whether new measurements have been recorded. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138` |  |
| 11 | MUST | ✅ found | For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:142` |  |
| 12 | MUST | ✅ found | For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:112` |  |
| 13 | MUST | ✅ found | For instruments with Cumulative aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST repeat the same starting timestamps. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141` |  |
| 14 | MUST | ✅ found | For instruments with Delta aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST advance the starting timestamp. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:145` |  |
| 15 | MUST | ✅ found | The ending timestamp (TimeUnixNano) MUST always be equal to time the metric data point took effect, which is equal to when MetricReader.Collect was invoked. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:274` |  |
| 16 | MUST | ✅ found | The SDK MUST support multiple MetricReader instances to be registered on the same MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:107` |  |
| 17 | SHOULD NOT | ⚠️ partial | The MetricReader.Collect invocation on one MetricReader instance SHOULD NOT introduce side-effects to other MetricReader instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:116` | Реализация пытается обеспечить изоляцию через СброситьБуферБезОчистки для всех кроме последнего читателя, но инструменты являются общими - очистка данных последним читателем влияет на delta-данные для других читателей. Полная изоляция per-reader не реализована. |
| 18 | MUST NOT | ❌ not_found | The SDK MUST NOT allow a MetricReader instance to be registered on more than one MeterProvider instance. | - | Нет проверки, что MetricReader уже зарегистрирован на другом MeterProvider. Один и тот же читатель можно передать нескольким провайдерам без ошибки. |
| 19 | SHOULD | ✅ found | The SDK SHOULD provide a way to allow MetricReader to respond to MeterProvider.ForceFlush and MeterProvider.Shutdown. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` |  |

#### Produce batch

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#produce-batch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | Produce MUST return a batch of Metric Points, filtered by the optional metricFilter parameter. | - | No MetricProducer.Produce method exists. Metric filtering via MetricFilter is implemented inline in MetricReader (ОтелПериодическийЧитательМетрик.МетрикаОтброшена), but not as part of a separate MetricProducer interface. |
| 2 | SHOULD | ❌ not_found | Implementation SHOULD use the filter as early as possible to gain as much performance gain possible (memory allocation, internal metric fetching, etc). | - | No MetricProducer.Produce method exists. The MetricReader does apply filtering before export (МетрикаОтброшена is called per instrument before adding to export batch), but this is not part of a MetricProducer interface. |
| 3 | SHOULD | ❌ not_found | If the batch of Metric Points includes resource information, Produce SHOULD require a resource as a parameter. | - | No MetricProducer.Produce method exists. Resource is accessed via Метр.Ресурс() internally, not passed as a parameter to a Produce function. |
| 4 | SHOULD | ❌ not_found | Produce SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | No MetricProducer.Produce method exists. The internal collection method (СобратьИЭкспортировать) is a Процедура (void), not a Функция returning success/failure. |
| 5 | SHOULD | ❌ not_found | If a batch of Metric Points can include InstrumentationScope information, Produce SHOULD include a single InstrumentationScope which identifies the MetricProducer. | - | No MetricProducer.Produce method exists. InstrumentationScope is included per-metric in the export data, but not as a single scope identifying a MetricProducer. |

### Env Vars

#### Prometheus Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#prometheus-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD NOT | ✅ found | OTEL_TRACES_EXPORTER known value "logging" is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:177` |  |
| 2 | SHOULD NOT | ✅ found | OTEL_METRICS_EXPORTER known value "logging" is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:291` |  |
| 3 | SHOULD NOT | ✅ found | OTEL_LOGS_EXPORTER known value "logging" is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:255` |  |
| 4 | MUST | ❌ not_found | When OTEL_CONFIG_FILE is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored. | - | Поддержка OTEL_CONFIG_FILE не реализована. Нет кода для чтения или обработки файловой конфигурации в src/Конфигурация/. |

## Условные требования (Conditional)

| Раздел | Секция | Scope | Keywords | Ссылка |
|---|---|---|---|---|
| Resource Sdk | Resource detector name | conditional:Resource Detector Naming (conditional) | 11 | [spec](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-detector-name) |
| Propagators | B3 Extract | conditional:B3 Propagator (extension) | 8 | [spec](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-extract) |
| Env Vars | Prometheus Exporter | conditional:Prometheus Exporter (extension) | 4 | [spec](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#prometheus-exporter) |

## Ограничения платформы OneScript

| Ограничение | Влияние на спецификацию | Решение |
|---|---|---|
| Нет байтовых массивов | TraceId/SpanId хранятся как hex-строки | Функциональный эквивалент через строки |
| Нет наносекундной точности | Временные метки с точностью до миллисекунд | Используется миллисекундная точность |
| Нет TLS/mTLS из SDK | Сертификаты конфигурируются вне SDK | Делегировано системе/прокси |
| Нет opaque-объектов | Ключи контекста - строки | Строковые константы как ключи |
| Нет thread-local | ФоновыеЗадания вместо goroutines | Передача контекста через параметры |

## Предупреждения валидации

- ⚠️ Секция Env Vars/Environment Variable Specification/General SDK ConfigurationNameDescriptionDefaultTypeNotesOTEL_SDK_DISABLEDDisable the SDK for all signalsfalseBooleanIf “true”, a no-op SDK implementation will be used for all telemetry signals. Any other value or absence of the variable will have no effect and the SDK will remain enabled. This setting has no effect on propagators configured through the OTEL_PROPAGATORS variable.OTEL_ENTITIESEntity information to be associated with the resourceStringSee Entities SDK for more details.OTEL_RESOURCE_ATTRIBUTESKey-value pairs to be used as resource attributesSee Resource semantic conventions for details.StringSee Resource SDK for more details.OTEL_SERVICE_NAMESets the value of the `service.name` resource attributeStringIf `service.name` is also provided in `OTEL_RESOURCE_ATTRIBUTES`, then `OTEL_SERVICE_NAME` takes precedence.OTEL_LOG_LEVELLog level used by the SDK internal logger“info”EnumOTEL_PROPAGATORSPropagators to be used as a comma-separated list“tracecontext,baggage”EnumValues MUST be deduplicated in order to register a `Propagator` only once.OTEL_TRACES_SAMPLERSampler to be used for traces“parentbased_always_on”EnumSee SamplingOTEL_TRACES_SAMPLER_ARGValue to be used as the sampler argumentSee footnoteThe specified value will only be used if OTEL_TRACES_SAMPLER is set. Each Sampler type defines its own expected input, if any. Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. (5 kw) - нет результата от агента

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
| Всего секций | 193 |
| Stable секций | 166 |
| Development секций | 27 |
| Conditional секций | 3 |
| Всего keywords | 824 |
| Stable universal keywords | 660 |

