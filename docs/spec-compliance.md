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
| Найдено требований (Stable universal) | 660 |
| ✅ Реализовано (found) | 502 (76.1%) |
| ⚠️ Частично (partial) | 102 (15.5%) |
| ❌ Не реализовано (not_found) | 56 (8.5%) |
| ➖ Неприменимо (n_a) | 0 |
| **MUST/MUST NOT found** | 346/400 (86.5%) |
| **SHOULD/SHOULD NOT found** | 156/260 (60.0%) |

## Соответствие по разделам (Stable)

| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |
|---|---|---|---|---|---|---|
| Context | 14 | 1 | 0 | 0 | 15 | 93.3% |
| Baggage Api | 16 | 1 | 0 | 0 | 17 | 94.1% |
| Resource Sdk | 10 | 4 | 1 | 0 | 15 | 66.7% |
| Trace Api | 102 | 13 | 5 | 0 | 120 | 85.0% |
| Trace Sdk | 50 | 20 | 5 | 0 | 75 | 66.7% |
| Logs Api | 20 | 1 | 0 | 0 | 21 | 95.2% |
| Logs Sdk | 38 | 12 | 9 | 0 | 59 | 64.4% |
| Metrics Api | 84 | 7 | 4 | 0 | 95 | 88.4% |
| Metrics Sdk | 120 | 29 | 17 | 0 | 166 | 72.3% |
| Otlp Exporter | 12 | 6 | 7 | 0 | 25 | 48.0% |
| Propagators | 29 | 2 | 1 | 0 | 32 | 90.6% |
| Env Vars | 7 | 6 | 7 | 0 | 20 | 35.0% |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Context]** [MUST] The API MUST accept the following parameters: * The `Context`.  
  УстановитьЗначение(Ключ, Значение) and СделатьСпанТекущим/СделатьBaggageТекущим push a new context onto the stack, but none accept a Context object directly as a parameter. The API uses a key-value approach instead of accepting a whole Context. (`src/Ядро/Модули/ОтелКонтекст.os:203`)

- ⚠️ **[Resource Sdk]** [MUST] Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK.  
  Детекторы ресурсов реализованы (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора), но они размещены inline в пакете SDK (src/Ядро/Классы/), а не в отдельных пакетах. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1`)

- ❌ **[Resource Sdk]** [MUST] Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions.  
  Детекторы ресурсов (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) заполняют семантические атрибуты (host.name, os.type, process.pid и др.), но создают ресурс через Новый ОтелРесурс(Истина) без указания Schema URL. (-)

- ⚠️ **[Resource Sdk]** [MUST] If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources.  
  Метод Слить() обрабатывает случай конфликта Schema URL - возвращает пустой ресурс (Новый ОтелРесурс(Истина)), но не сообщает об ошибке (не вызывает исключение и не логирует ошибку). Спецификация требует, чтобы это считалось ошибкой. (`src/Ядро/Классы/ОтелРесурс.os:41`)

- ⚠️ **[Trace Api]** [MUST] In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception,  
  Метод ПолучитьТрассировщик не проверяет пустое имя и не возвращает fallback-трассировщик с пустым именем. Пустая строка передаётся как есть в ОбластьИнструментирования без обработки. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:56`)

- ⚠️ **[Trace Api]** [MUST] All mutating operations MUST return a new `TraceState` with the modifications applied.  
  Установить() and Удалить() return new ОтелСостояниеТрассировки instances (immutable pattern), which is correct. However, Установить() returns ЭтотОбъект when validation fails instead of a new TraceState, which is a minor deviation. (`src/Трассировка/Классы/ОтелСостояниеТрассировки.os:66`)

- ⚠️ **[Trace Api]** [MUST NOT] This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`.  
  УстановитьРодителя() accepts both ОтелСпан and ОтелКонтекстСпана as parent, not a full Context object. The spec requires only a full Context (not Span/SpanContext). (`src/Трассировка/Классы/ОтелПостроительСпана.os:36`)

- ❌ **[Trace Api]** [MUST] However, all API implementations of such methods MUST internally call the End method and be documented to do so.  
  No language-specific convenience methods (like Python 'with' statement) that wrap End are implemented. (-)

- ⚠️ **[Trace Api]** [MUST NOT] This operation itself MUST NOT perform blocking I/O on the calling thread.  
  End() calls processor.ПриЗавершении synchronously which may invoke exporters that perform blocking I/O depending on the processor type (e.g. SimpleSpanProcessor). (`src/Трассировка/Классы/ОтелСпан.os:447`)

- ⚠️ **[Trace Api]** [MUST] If the parent Context contains no Span, an empty non-recording Span MUST be returned instead (i.e., having a SpanContext with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags).  
  When there is no parent and sampling fails, a NoopSpan is returned with a new generated TraceId and SpanId (not all-zeros). The spec requires all-zero IDs when no parent context exists and no SDK is installed. The ОтелНоопСпан default constructor does create all-zero IDs, but the Tracer path generates new IDs. (`src/Трассировка/Классы/ОтелТрассировщик.os:66`)

- ⚠️ **[Trace Sdk]** [MUST] Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, `Sampler`, and (Development) TracerConfigurator) MUST be owned by the `TracerProvider`.  
  SpanProcessors, Sampler, SpanLimits и TracerConfigurator принадлежат провайдеру, но IdGenerator не конфигурируется через провайдер - используется статический ОтелУтилиты.СгенерироватьИдТрассировки() (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:11`)

- ⚠️ **[Trace Sdk]** [MUST] For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated since 1.10.0] having the same name and version values as the `InstrumentationScope`.  
  ОбластьИнструментирования (InstrumentationScope) содержит те же данные (имя и версию), но отдельного аксессора InstrumentationLibrary для обратной совместимости нет (`src/Трассировка/Классы/ОтелСпан.os:170`)

- ⚠️ **[Trace Sdk]** [MUST] implementations MAY choose not to expose (and store) the full parent Context of the Span but they MUST expose at least the full parent SpanContext.  
  Спан хранит только ИдРодительскогоСпана (строка с ID родительского спана), но не полный родительский SpanContext (который включает TraceId, SpanId, TraceFlags, TraceState, IsRemote) (`src/Трассировка/Классы/ОтелСпан.os:89`)

- ⚠️ **[Trace Sdk]** [MUST NOT] SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value.  
  The SDK has no explicit awareness of the rv sub-key in OpenTelemetry TraceState. However, parent TraceState (including rv) is preserved by default through ОпределитьСостояниеТрассировки fallback. The SDK does not overwrite rv, but also does not explicitly protect it - it's preserved incidentally through TraceState pass-through. (`src/Трассировка/Классы/ОтелТрассировщик.os:183`)

- ⚠️ **[Trace Sdk]** [MUST] The built-in SpanProcessors MUST do so.  
  Built-in ОтелПакетныйПроцессорСпанов exports all buffered spans via ЭкспортироватьВсеПакеты, but does not call ForceFlush on the exporter after exporting. ОтелПростойПроцессорСпанов has empty СброситьБуфер (no buffering, correct) but also does not call ForceFlush on its exporter. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68`)

- ❌ **[Trace Sdk]** [MUST] If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls.  
  СброситьБуфер methods in all processor implementations accept no timeout parameter. ОтелБазовыйПакетныйПроцессор.ЭкспортироватьВсеПакеты loops without any timeout mechanism, so there is no way to prioritize honoring a timeout. (-)

- ⚠️ **[Trace Sdk]** [MUST] Each implementation MUST document the concurrency characteristics the SDK requires of the exporter.  
  Есть комментарий 'Export и Shutdown/ForceFlush могут вызываться конкурентно' в файле экспортера, но нет формальной документации о характеристиках конкурентности, которые SDK требует от экспортера. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:5`)

- ❌ **[Logs Sdk]** [MUST NOT] Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller. Parameters are immutable or passed by value.  
  Интерфейс ИнтерфейсПроцессорЛогов не содержит метода Enabled. Метод Включен() реализован только на уровне Logger (ОтелЛоггер.os:42), но не на уровне LogRecordProcessor. Требование о неизменности параметров в processor-level Enabled не может быть проверено. (-)

- ❌ **[Logs Sdk]** [MUST] If a timeout is specified (see below), the `LogRecordProcessor` MUST prioritize honoring the timeout over finishing all calls.  
  Метод СброситьБуфер() не принимает параметр таймаута и не имеет механизма прерывания экспорта по таймауту. (-)

- ❌ **[Logs Sdk]** [MUST] Each implementation MUST document the concurrency characteristics the SDK  
  Нет явной документации о характеристиках конкурентности для реализаций экспортера логов. (-)

- ⚠️ **[Logs Sdk]** [MUST] LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.  
  Флаг Закрыт в экспортере - обычный Булево, а не АтомарноеБулево. В отличие от ОтелПровайдерЛогирования (строка 224), который использует АтомарноеБулево для потокобезопасности, экспортер не обеспечивает формальную потокобезопасность при конкурентных вызовах Закрыть(). (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47`)

- ⚠️ **[Metrics Api]** [MUST] Callback functions MUST be documented as follows for the end user:  
  Документация callback существует в комментариях ОтелНаблюдениеМетрики, но не описывает все три рекомендации (reentrant safe, не бесконечные, не дублировать наблюдения). (`src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:130`)

- ⚠️ **[Metrics Api]** [MUST] MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  ОтелПровайдерМетрик использует СинхронизированнаяКарта для потокобезопасности, но документация класса не содержит явного указания на потокобезопасность методов (`src/Метрики/Классы/ОтелПровайдерМетрик.os:241`)

- ⚠️ **[Metrics Api]** [MUST] Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  ОтелМетр использует СинхронизированнаяКарта для ИнструментыПоИмени и ДескрипторыИнструментов, обеспечивая потокобезопасность, но это не задокументировано явно в комментариях класса (`src/Метрики/Классы/ОтелМетр.os:493`)

- ⚠️ **[Metrics Api]** [MUST] Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  ОтелБазовыйСинхронныйИнструмент использует СинхронизированнаяКарта и АтомарноеБулево для потокобезопасности, но комментарии не документируют явно, что все методы безопасны для конкурентного использования (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:16`)

- ⚠️ **[Metrics Sdk]** [MUST] If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the `MeterProvider` before or after the configuration change).  
  Views registered after Meter creation via ЗарегистрироватьПредставление are stored at the provider level but Meters get a copy of views at creation time (line 71: Метрика.УстановитьПредставления). New views added later do not automatically propagate to already-created Meters. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:71`)

- ⚠️ **[Metrics Sdk]** [MUST NOT] If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the `MeterProvider` before or after the configuration change).  
  Same issue as above - Views are copied to Meters at creation time, so configuration changes after Meter creation may not fully propagate. MetricReaders are managed at the provider level and do apply to all Meters. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:71`)

- ⚠️ **[Metrics Sdk]** [MUST] The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept.  
  ОтелПредставление хранит ИсключенныеКлючиАтрибутов, но ОтелБазовыйСинхронныйИнструмент не обрабатывает exclude-list - фильтрация атрибутов использует только allow-list (РазрешенныеКлючиАтрибутов) (`src/Метрики/Классы/ОтелПредставление.os:57`)

- ⚠️ **[Metrics Sdk]** [MUST] The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept.  
  Exclude-list сохраняется в ОтелПредставление, но не применяется при фильтрации в ОтелБазовыйСинхронныйИнструмент (`src/Метрики/Классы/ОтелПредставление.os:57`)

- ⚠️ **[Metrics Sdk]** [MUST] If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST apply the default aggregation cardinality limit the `MetricReader` is configured with.  
  Лимит мощности по умолчанию 2000 задаётся в ОтелМетр, а не берётся из конфигурации MetricReader (`src/Метрики/Классы/ОтелМетр.os:500`)

- ⚠️ **[Metrics Sdk]** [MUST] Instrument advisory parameters, if any, MUST be honored.  
  Advisory-параметры (ГраницыГистограммы, КлючиАтрибутов) учитываются при создании инструмента, но только когда нет View; спецификация требует их применения и в случае отсутствия View (`src/Метрики/Классы/ОтелМетр.os:512`)

- ⚠️ **[Metrics Sdk]** [MUST] Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that observations made or produced by executing callbacks only apply to the intended `MetricReader` during collection.  
  Callbacks вызываются в ОтелПериодическийЧитательМетрик.СобратьИЭкспортировать через Метр.ВызватьМультиОбратныеВызовы(), но наблюдения не изолированы по конкретному MetricReader - они общие для всех reader'ов (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:106`)

- ⚠️ **[Metrics Sdk]** [MUST] Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow.  
  Кумулятивная временность сохраняет аккумуляторы (не очищает в ОчиститьТочкиДанных при Кумулятивная=Истина), но специальной логики для разделения pre-overflow и post-overflow attribute sets нет - все аккумуляторы экспортируются одинаково. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138`)

- ⚠️ **[Metrics Sdk]** [MUST NOT] `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure).  
  Метод Экспортировать() вызывает Транспорт.Отправить() синхронно. Таймаут зависит от настроек транспорта (HTTP), но экспортер сам не устанавливает явный верхний предел таймаута. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:27`)

- ⚠️ **[Metrics Sdk]** [MUST] `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure).  
  Экспортер не устанавливает собственный таймаут, полагаясь на настройки транспорта. Нет явного error result (Failure) при таймауте - метод возвращает Булево. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:27`)

- ❌ **[Metrics Sdk]** [MUST] A `MetricProducer` MUST support the following functions:  
  Отдельный интерфейс/класс MetricProducer не реализован. Функциональность сбора метрик встроена в MetricReader (ОтелПериодическийЧитательМетрик и ОтелПрометеусЧитательМетрик), но не выделена в отдельную сущность MetricProducer. (-)

- ❌ **[Metrics Sdk]** [MUST] The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry.  
  В коде метрик нет явной обработки числовых пределов (NaN, Infinity, переполнение). Значения принимаются и записываются как есть без валидации. (-)

- ❌ **[Metrics Sdk]** [MUST] If the SDK receives float/double values from Instruments, it MUST handle all the possible values.  
  Нет специальной обработки NaN, Infinity или других предельных значений float/double. OneScript использует Число, который обрабатывает числа через .NET runtime, но явная обработка по спецификации отсутствует. (-)

- ⚠️ **[Metrics Sdk]** [MUST] MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.  
  Метрики хранятся в СинхронизированнаяКарта (thread-safe), создание метров безопасно. Однако СброситьБуфер() и Закрыть() не используют блокировку - они напрямую вызывают методы читателей без синхронизации на уровне провайдера. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:241`)

- ⚠️ **[Metrics Sdk]** [MUST] MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.  
  В коде есть комментарий о потокобезопасности ("Export и Shutdown/ForceFlush могут вызываться конкурентно. Реализация MUST быть безопасна"), но фактически Закрыть() использует простое присваивание Закрыт = Истина без атомарной операции или блокировки. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:3`)

- ⚠️ **[Otlp Exporter]** [MUST] The following configuration options MUST be available to configure the OTLP exporter.  
  Endpoint, Protocol, Headers, Compression, Timeout доступны. Certificate File, Client key file, Client certificate file (TLS/mTLS) отсутствуют. Insecure не реализован (spec допускает MAY не реализовывать). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130`)

- ❌ **[Otlp Exporter]** [MUST] Each configuration option MUST be overridable by a signal specific option.  
  Только общие ключи otel.exporter.otlp.* читаются в СоздатьТранспорт(). Посигнальные переопределения (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_LOGS_PROTOCOL и т.д.) не реализованы. (-)

- ⚠️ **[Otlp Exporter]** [MUST] Options MUST be one of: `grpc`, `http/protobuf`, `http/json`.  
  grpc и http/json поддерживаются. http/protobuf указан в комментарии как поддерживаемый, но фактически при установке http/protobuf создаётся ОтелHttpТранспорт, который отправляет JSON (Content-Type: application/json), а не protobuf. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ❌ **[Otlp Exporter]** [MUST] For the per-signal variables (`OTEL_EXPORTER_OTLP_<signal>_ENDPOINT`), the URL MUST be used as-is without any modification.  
  Посигнальные переменные OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_LOGS_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_ENDPOINT не реализованы. (-)

- ❌ **[Otlp Exporter]** [MUST] The only exception is that if an URL contains no path part, the root path `/` MUST be used (see Example 2).  
  Посигнальные переменные endpoint не реализованы, поэтому логика обработки URL без пути отсутствует. (-)

- ⚠️ **[Propagators]** [MUST] The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry extension packages:  
  W3C TraceContext и W3C Baggage пропагаторы реализованы, но B3 пропагатор отсутствует в SDK. (`src/Пропагация/Классы/`)

- ⚠️ **[Propagators]** [MUST] The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry extension packages:  
  W3C TraceContext и W3C Baggage распространяются как часть API (допускается спецификацией через MAY), но B3 пропагатор не доступен как отдельный пакет расширения. (`src/Пропагация/Классы/`)

- ⚠️ **[Env Vars]** [MUST] The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset.  
  Пустые значения обрабатываются в некоторых местах (строки 105, 137, 339: проверка '<> ""'), но не во всех. Например, otel.traces.exporter (строка 177), otel.traces.sampler (строка 190) и числовые параметры (строки 224-227) не проверяют пустые значения - пустая строка будет обработана как значение, а не как отсутствие переменной. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105`)

- ❌ **[Env Vars]** [MUST] For new implementations, these should be treated as MUST requirements.  
  Требование обязывает новые реализации трактовать SHOULD-требования о числовом парсинге как MUST. Реализация не генерирует предупреждений и не игнорирует невалидные числовые значения gracefully - вызов Число() с невалидным значением приведет к исключению. (-)

- ⚠️ **[Env Vars]** [MUST] For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting.  
  Для пропагаторов реализовано предупреждение (строка 373: Сообщить("неизвестный пропагатор")). Но для семплеров неизвестное значение молча заменяется на parentbased_always_on без предупреждения (строка 216). Для экспортеров неизвестное значение не обрабатывается. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:373`)

- ❌ **[Env Vars]** [MUST] Values MUST be deduplicated in order to register a Propagator only once.  
  В функции СоздатьПропагаторы() (строка 336) нет логики дедупликации. Если пользователь укажет OTEL_PROPAGATORS="tracecontext,tracecontext", оба экземпляра ОтелW3CПропагатор будут созданы и добавлены в МассивПропагаторов. (-)

- ❌ **[Env Vars]** [MUST] Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set.  
  В функции СоздатьПровайдерТрассировки() (строка 172) невалидное значение OTEL_TRACES_SAMPLER_ARG (например, нечисловая строка) передается в Число() без try/catch, что вызовет исключение вместо логирования предупреждения. (-)

- ❌ **[Env Vars]** [MUST] Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set.  
  Невалидный ввод OTEL_TRACES_SAMPLER_ARG не игнорируется gracefully - вызов Число(АргументСэмплера) на строках 204, 215 приведет к исключению вместо возврата к поведению по умолчанию. (-)

- ❌ **[Env Vars]** [MUST] Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set.  
  При невалидном OTEL_TRACES_SAMPLER_ARG реализация не переходит к поведению 'как если бы переменная не установлена' (значение по умолчанию 1.0) - вместо этого выбрасывается исключение при конвертации строки в число. (-)

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Baggage Api]** [SHOULD NOT] The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation.  
  Высокоуровневые методы (BaggageИзКонтекста, КонтекстСBaggage, ТекущийBaggage, СделатьBaggageТекущим) существуют, но функция КлючBaggage() экспортирована публично (строка 53), что даёт пользователям прямой доступ к ключу контекста. (`src/Ядро/Модули/ОтелКонтекст.os:53`)

- ⚠️ **[Resource Sdk]** [SHOULD] Note the failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error.  
  Ошибки при детекции перехватываются через Попытка/Исключение, но логируются на уровне Отладка (Лог.Отладка), а не как ошибки (Лог.Ошибка). Спецификация требует, чтобы ошибки при попытке детекции считались ошибками. (`src/Ядро/Классы/ОтелДетекторРесурсаПроцесса.os:22`)

- ⚠️ **[Resource Sdk]** [SHOULD] Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate (e.g. the detector that reads the attributes from environment values will not know what Schema URL to use).  
  Все детекторы используют пустой Schema URL (Новый ОтелРесурс(Истина)), но они заполняют известные семантические атрибуты (host.*, os.*, process.*), для которых по предыдущему требованию должен быть указан непустой Schema URL. Нет логики выбора Schema URL в зависимости от типа атрибутов. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18`)

- ⚠️ **[Trace Api]** [SHOULD] `name` (required): This name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library (e.g. `io.opentelemetry.contrib.mongodb`), package, module or class name.  
  Параметр name принимается, но нет валидации или документации о том, что имя должно уникально идентифицировать область инструментирования. Однако параметр используется корректно. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:59`)

- ❌ **[Trace Api]** [SHOULD] its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged.  
  Нет логирования предупреждения при передаче пустого или невалидного имени в ПолучитьТрассировщик. (-)

- ❌ **[Trace Api]** [SHOULD] its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged.  
  Нет установки имени в пустую строку при невалидном значении - значение передаётся как есть, нет специальной обработки. (-)

- ⚠️ **[Trace Api]** [SHOULD NOT] `Span`s are not meant to be used to propagate information within a process. To prevent misuse, implementations SHOULD NOT provide access to a `Span`'s attributes besides its `SpanContext`.  
  ОтелСпан exposes Атрибуты() as a public method returning the full ОтелАтрибуты object, which the spec says SHOULD NOT be accessible. This is needed for export but violates the API-level recommendation. (`src/Трассировка/Классы/ОтелСпан.os:155`)

- ⚠️ **[Trace Api]** [SHOULD] When the status is set to Error by Instrumentation Libraries, the Description SHOULD be documented and predictable.  
  SetStatus API exists and accepts Description for Error, but there is no documentation of predictable Description values for instrumentation libraries. (`src/Трассировка/Классы/ОтелСпан.os:413`)

- ⚠️ **[Trace Api]** [SHOULD] Instrumentation Libraries SHOULD publish their own conventions, including possible values of Description and what they mean.  
  No published conventions for Description values found in the codebase. (-)

- ❌ **[Trace Api]** [SHOULD] Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generate.  
  This requirement is about analysis tools consuming spans, not about SDK implementation. No analysis tool functionality exists in this SDK. (-)

- ⚠️ **[Trace Api]** [SHOULD NOT] If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type).  
  ОтелНоопСпан is a public class available to all consumers. The spec recommends hiding this type if possible. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ⚠️ **[Trace Api]** [SHOULD] If a new type is required to be publicly exposed, it SHOULD be named NonRecordingSpan.  
  The class is named ОтелНоопСпан (NoopSpan) instead of the recommended NonRecordingSpan naming. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ⚠️ **[Trace Api]** [SHOULD] Implementations SHOULD record links containing SpanContext with empty TraceId or SpanId (all zeros) as long as either the attribute set or TraceState is non-empty.  
  AddLink records all links regardless of SpanContext validity - it does not specifically check for empty TraceId/SpanId with non-empty attributes/TraceState. (`src/Трассировка/Классы/ОтелСпан.os:361`)

- ⚠️ **[Trace Api]** [SHOULD] Link - Links are immutable and SHOULD be safe for concurrent use by default.  
  Links are stored as plain Соответствие (Map) objects, not as a dedicated immutable Link class. They are effectively immutable after creation but there's no explicit Link class guaranteeing immutability. (`src/Трассировка/Классы/ОтелСпан.os:373`)

- ❌ **[Trace Api]** [SHOULD] If the Span in the parent Context is already non-recording, it SHOULD be returned directly without instantiating a new Span.  
  The tracer always creates a new ОтелНоопСпан when sampling fails, even if the parent is already non-recording. It does not check if parent is non-recording to return it directly. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Синхронный СброситьБуфер() - процедура без возвращаемого значения. Асинхронный СброситьБуферАсинхронно() возвращает Обещание, через которое можно узнать результат, но синхронная версия не сообщает об успехе/неудаче (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:121`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Синхронный СброситьБуфер() не имеет встроенного таймаута. Асинхронный вариант через Обещание позволяет задать таймаут на стороне вызывающего, но встроенного таймаута нет (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98`)

- ⚠️ **[Trace Sdk]** [SHOULD NOT] However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set.  
  The processor passes all received spans to the exporter without checking the Sampled flag. In practice, built-in samplers never produce RECORD_ONLY spans, but there's no explicit filtering for the Sampled flag before export. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37`)

- ⚠️ **[Trace Sdk]** [SHOULD NOT] Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not.  
  The processor/exporter pipeline has no filtering based on the Sampled flag. All spans passed from the processor reach the exporter. Built-in samplers only produce DROP or RECORD_AND_SAMPLE, so in practice non-sampled recording spans don't reach the exporter, but the filtering is not enforced at the exporter level. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37`)

- ⚠️ **[Trace Sdk]** [SHOULD] so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend to change it.  
  The sampler (ОтелСэмплер.ДолженСэмплировать) creates ОтелРезультатСэмплирования without passing through the parent Tracestate. The Tracer compensates by falling back to parent's Tracestate in ОпределитьСостояниеТрассировки when the sampler result has empty Tracestate. The spec intends the sampler itself to return the passed-in Tracestate. (`src/Трассировка/Классы/ОтелРезультатСэмплирования.os:77`)

- ⚠️ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values.  
  TraceIDs are generated using УникальныйИдентификатор (UUID v4) which provides randomness, but not specifically compliant with W3C Trace Context Level 2 requirements (which specify the least significant 56 bits must be random). UUID v4 has 122 random bits but with fixed version/variant bits that reduce randomness in specific positions. (`src/Ядро/Модули/ОтелУтилиты.os:78`)

- ❌ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements.  
  The SDK only sets bit 0 (Sampled) in trace flags via ВычислитьФлагиТрассировки() which returns 0 or 1. The Random flag (bit 1 per W3C Trace Context Level 2) is never set. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the `rv` sub-key of the OpenTelemetry TraceState.  
  The TraceIdRatioBased sampler uses TraceId bytes as random source, implicitly presuming TraceIDs are random. However, the 'unless' clause is not implemented - the SDK never checks for explicit randomness (rv sub-key) in OpenTelemetry TraceState as an alternative randomness source. (`src/Трассировка/Модули/ОтелСэмплер.os:288`)

- ⚠️ **[Trace Sdk]** [SHOULD] If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated.  
  The SDK supports custom IdGenerator via ОтелУтилиты.УстановитьГенераторИд(). However, the IdGenerator extension has no way to influence the Random trace flag - flag computation is in ОтелТрассировщик.ВычислитьФлагиТрассировки() which only considers the sampling decision, not the IdGenerator. (`src/Ядро/Модули/ОтелУтилиты.os:63`)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD be called only once for each `SpanProcessor` instance.  
  ОтелБазовыйПакетныйПроцессор sets Закрыт=Истина in Закрыть and checks it in Обработать, but Закрыть itself does not guard against double invocation. ОтелПростойПроцессорСпанов.Закрыть has no once-only guard at all. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:75`)

- ⚠️ **[Trace Sdk]** [SHOULD] After the call to `Shutdown`, subsequent calls to `OnStart`, `OnEnd`, or `ForceFlush` are not allowed. SDKs SHOULD ignore these calls gracefully, if possible.  
  ОтелБазовыйПакетныйПроцессор.Обработать checks Закрыт flag at line 43, but СброситьБуфер (ForceFlush) does not check Закрыт before executing. ОтелПростойПроцессорСпанов has no shutdown state tracking at all. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43`)

- ❌ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  All Закрыть methods are void procedures (Процедура) returning no status. Neither ОтелБазовыйПакетныйПроцессор.Закрыть, ОтелПростойПроцессорСпанов.Закрыть, nor ОтелКомпозитныйПроцессорСпанов.Закрыть provide any success/failure/timeout indication to the caller. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  ОтелБазовыйПакетныйПроцессор.ОстановитьФоновыйЭкспорт uses ТаймаутЭкспортаМс for background task wait, but the Закрыть method itself has no explicit timeout parameter for the caller to control, and ЭкспортироватьВсеПакеты loops without a timeout bound. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192`)

- ⚠️ **[Trace Sdk]** [SHOULD] In particular, if any `SpanProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all spans for which this was not already done and then invoke `ForceFlush` on it.  
  ОтелБазовыйПакетныйПроцессор.ЭкспортироватьВсеПакеты calls Экспортер.Экспортировать for all buffered data, but does not invoke ForceFlush (СброситьБуфер) on the exporter itself after exporting. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120`)

- ❌ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  All СброситьБуфер methods are void procedures (Процедура) with no return value or callback mechanism to report success, failure, or timeout to the caller. (-)

- ❌ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  СброситьБуфер accepts no timeout parameter. ОтелБазовыйПакетныйПроцессор.ЭкспортироватьВсеПакеты loops through all buffered data without any timeout bound, so there is no mechanism to abort within a specified time. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() реализован как Процедура (void), а не Функция - не возвращает результат успеха/неудачи/таймаута вызывающей стороне. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  СброситьБуфер() в ОтелЭкспортерСпанов выполняется синхронно без таймаута. В базовом пакетном процессоре есть ТаймаутЭкспортаМс для фонового экспорта, но сам метод СброситьБуфер экспортера не имеет механизма таймаута. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41`)

- ⚠️ **[Logs Api]** [SHOULD] The API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response.  
  Метод Включен() документирован, но комментарий не содержит явного указания вызывать этот API каждый раз перед отправкой LogRecord для получения актуального ответа. (`src/Логирование/Классы/ОтелЛоггер.os:28`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Синхронный метод СброситьБуфер() является процедурой (void) и не возвращает статус. Асинхронный СброситьБуферАсинхронно() возвращает Обещание, но синхронный вариант не сигнализирует об успехе или ошибке. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  СброситьБуфер() является процедурой (void) и не возвращает статус ERROR при ошибке. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  СброситьБуфер() является процедурой (void) и не возвращает статус NO ERROR при отсутствии ошибок. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Синхронный метод СброситьБуфер() не имеет механизма таймаута. Асинхронная версия СброситьБуферАсинхронно() опирается на таймаут Promise, но сам метод не принимает параметр таймаута. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD NOT] This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD NOT block or throw exceptions.  
  Композитный процессор оборачивает вызовы в Попытка-Исключение (не выбрасывает исключения), но простой процессор ОтелПростойПроцессорЛогов.ПриПоявлении() блокируется на БлокировкаЭкспорта и может выбрасывать исключения (ВызватьИсключение в строке 27). (`src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17`)

- ❌ **[Logs Sdk]** [SHOULD] To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecord` be used for any concurrent processing, such as in a batching processor.  
  Нет документации или рекомендаций пользователям о клонировании logRecord для конкурентной обработки. Пакетный процессор добавляет оригинальный объект записи в буфер без клонирования. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance.  
  Провайдер защищает от повторного вызова через атомарный флаг Закрыт.СравнитьИУстановить(), но простой процессор ОтелПростойПроцессорЛогов.Закрыть() не имеет защиты от повторного вызова. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:117`)

- ⚠️ **[Logs Sdk]** [SHOULD] After the call to `Shutdown`, subsequent calls to `OnEmit` are not allowed. SDKs SHOULD ignore these calls gracefully, if possible.  
  Пакетный процессор проверяет флаг Закрыт и возвращает Возврат в методе Обработать (строка 43-44), но простой процессор ОтелПростойПроцессорЛогов.ПриПоявлении() не проверяет состояние завершения. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43`)

- ❌ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод Закрыть() реализован как Процедура (void) во всех процессорах - не возвращает индикацию успеха, неудачи или таймаута. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Пакетный процессор использует таймаут при остановке фонового экспорта (Обещание.Получить(ТаймаутЭкспортаМс)), но метод Закрыть() не принимает параметр таймаута и финальный экспорт ЭкспортироватьВсеПакеты() не ограничен по времени. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192`)

- ⚠️ **[Logs Sdk]** [SHOULD] In particular, if any `LogRecordProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all `LogRecord`s for which this was not already done and then invoke `ForceFlush` on it.  
  СброситьБуфер() вызывает ЭкспортироватьВсеПакеты(), который вызывает Экспортер.Экспортировать() для всех оставшихся записей, но не вызывает ForceFlush (СброситьБуфер) на самом экспортере. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68`)

- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() реализован как Процедура (void) - не возвращает индикацию успеха, неудачи или таймаута. (-)

- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `LogRecordProcessor` exports the emitted `LogRecord`s.  
  Нет документации или руководства, ограничивающего использование ForceFlush только необходимыми случаями. (-)

- ❌ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Метод СброситьБуфер() не имеет механизма таймаута - выполняется синхронно до завершения без ограничения по времени. (-)

- ❌ **[Logs Sdk]** [SHOULD] Other common processing scenarios SHOULD be first considered for implementation out-of-process in OpenTelemetry Collector.  
  Нет документации, рекомендующей использовать OpenTelemetry Collector для дополнительных сценариев обработки. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() определена как Процедура (void), не возвращает результат успеха/неудачи/таймаута. Интерфейс и реализация не предоставляют обратной связи вызывающему коду. (`src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:19`)

- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD be called only once for each `LogRecordExporter` instance.  
  Метод Закрыть() экспортера не имеет защиты от повторного вызова (нет проверки флага Закрыт перед установкой). В отличие от ОтелПровайдерЛогирования, который использует АтомарноеБулево.СравнитьИУстановить(), экспортер просто устанавливает Закрыт = Истина без проверки. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47`)

- ❌ **[Metrics Api]** [SHOULD] Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying.  
  OneScript не делает различий между целыми и вещественными числами на уровне типов (единый тип Число). Дескриптор инструмента не включает тип данных числа как идентифицирующий признак. (-)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax.  
  Метод СоздатьСчетчик документирует параметр Имя как Строка, но не указывает требования к синтаксису имени инструмента. (`src/Метрики/Классы/ОтелМетр.os:39`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax.  
  Метод СоздатьНаблюдаемыйСчетчик документирует Имя как Строка, но не указывает требования к синтаксису имени. (`src/Метрики/Классы/ОтелМетр.os:218`)

- ❌ **[Metrics Api]** [SHOULD] Callback functions SHOULD be reentrant safe. The SDK expects to evaluate callbacks for each MetricReader independently.  
  Нет документации для пользователей о реентерабельности callback-функций. (-)

- ❌ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT take an indefinite amount of time.  
  Нет документации для пользователей о недопустимости бесконечного выполнения callback. (-)

- ❌ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same `attributes`) across all registered callbacks.  
  Нет документации или проверки дублирования наблюдений с одинаковыми атрибутами. (-)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response.  
  Метод Включен() существует и документирован, но комментарий не упоминает явно, что его нужно вызывать перед каждым измерением для получения актуального состояния (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:194`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() is a Процедура (void), does not return a status. The async variant СброситьБуферАсинхронно() returns an Обещание, but the sync method provides no success/failure indication. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:115`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  СброситьБуфер() is a Процедура (void) that does not return any status - neither ERROR nor NO ERROR. Errors in individual readers are silently swallowed. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:115`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  СброситьБуфер() does not accept or enforce a timeout parameter. The async variant СброситьБуферАсинхронно() returns a Promise that could be awaited with timeout externally, but the sync method itself has no timeout mechanism. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:115`)

- ❌ **[Metrics Sdk]** [SHOULD] In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector that selects at most one instrument.  
  Нет валидации при регистрации представления, что селектор с name выбирает не более одного инструмента (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning.  
  Представления применяются независимо в ОтелПериодическийЧитательМетрик.ПрименитьПредставление, но нет проверки конфликтов метрических идентичностей и нет предупреждения (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asynchronous instrument to use the Explicit bucket histogram aggregation) the implementation SHOULD emit a warning and proceed as if the View did not exist.  
  Нет проверки семантических ошибок при применении View (например, задание гистограммной агрегации для асинхронного инструмента) (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] If the Instrument could not match with any of the registered `View`(s), the SDK SHOULD enable the instrument using the default aggregation and temporality.  
  Инструменты создаются с агрегацией по умолчанию, но если ни одно View не совпало, инструмент всё равно работает - поведение корректно. Однако временность не конфигурируется отдельно для этого случая. (`src/Метрики/Классы/ОтелМетр.os:50`)

- ❌ **[Metrics Sdk]** [SHOULD NOT] This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpDownCounter` or `ObservableGauge`).  
  Агрегатор гистограммы всегда собирает sum, нет логики пропуска sum для инструментов с отрицательными измерениями (UpDownCounter, ObservableGauge) (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`, `min`, and `max` fields, because these values do not map into a valid bucket.  
  Экспоненциальная гистограмма не имеет защиты от non-normal values (Inf, NaN) - OneScript не имеет нативных Inf/NaN, но нет явной проверки (-)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks.  
  Нет механизма предотвращения использования API асинхронных инструментов вне зарегистрированных callback-ов (-)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback execution.  
  Нет таймаута при вызове callback-ов в ОтелБазовыйНаблюдаемыйИнструмент.ВызватьCallbackИСобрать() (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback.  
  В ОтелБазовыйНаблюдаемыйИнструмент данные формируются из записей callback-а и внешних наблюдений. Метод ОчиститьТочкиДанных() сбрасывает ВнешниеНаблюдения, но нет механизма удаления старых attribute set-ов, которые не были наблюдены в текущем callback (-)

- ❌ **[Metrics Sdk]** [SHOULD] If there is no matching view, but the `MetricReader` defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used.  
  MetricReader (ОтелПериодическийЧитательМетрик) не имеет метода для задания default cardinality limit per instrument. Лимит задаётся только на уровне Meter или View. (-)

- ❌ **[Metrics Sdk]** [SHOULD] Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality.  
  ОтелБазовыйНаблюдаемыйИнструмент не имеет механизма cardinality limiting - все наблюдения из callback и внешних наблюдений конвертируются в точки данных без ограничения количества атрибутных наборов. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible.  
  Предупреждение содержит информацию о конфликте (вид инструмента и единица измерения), но не включает рекомендации по разрешению конфликта (например, использование View). (`src/Метрики/Классы/ОтелМетр.os:573`)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning.  
  ПроверитьКонфликтДескриптора всегда сравнивает описания и выдаёт предупреждение при различии - нет проверки, настроено ли описание через View для подавления предупреждения. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning.  
  Предупреждение при конфликте дескриптора не включает рецепт View для переименования - сообщение содержит только параметры конфликтующих инструментов. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument registration.  
  При дублировании SDK возвращает первый зарегистрированный инструмент (а не оба) и выдаёт предупреждение. Данные второго инструмента агрегируются в первый, но отдельного объекта Metric не создаётся. (`src/Метрики/Классы/ОтелМетр.os:52`)

- ❌ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax  
  ОтелМетр при создании инструментов (СоздатьСчетчик, СоздатьГистограмму и т.д.) не выполняет валидацию имени на соответствие синтаксису instrument name из спецификации. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name.  
  Нет проверки имени инструмента при создании - невалидные имена принимаются без предупреждения. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] `Exemplar` sampling SHOULD be turned on by default.  
  Default filter is ПоТрассировке (TraceBased), which only samples when there is an active sampled span. The spec says sampling SHOULD be on by default - TraceBased is the recommended default per spec, so this is acceptable, but it means exemplars are only captured when tracing is active. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:264`)

- ⚠️ **[Metrics Sdk]** [SHOULD] The default value SHOULD be `TraceBased`.  
  The default is ПоТрассировке (TraceBased) at the Meter level, but the ОтелПостроительПровайдераМетрик does not explicitly set TraceBased as default in the builder - it only sets the filter from environment variable. The Meter defaults to TraceBased in its constructor. (`src/Метрики/Классы/ОтелМетр.os:496`)

- ⚠️ **[Metrics Sdk]** [SHOULD] The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars.  
  The reservoir creates a new Соответствие (Map) for each exemplar in СоздатьЭкземпляр, which allocates on every offer call. OneScript's GC-based model makes zero-allocation difficult, but the implementation does not pre-allocate exemplar objects. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:42`)

- ⚠️ **[Metrics Sdk]** [SHOULD] This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled.  
  Реализация хранит последнее измерение в каждом бакете (MAY alternative), а не использует reservoir sampling с равномерной вероятностью. Спецификация допускает это как альтернативу ('MAY instead keep the last seen measurement'), но SHOULD указывает на предпочтительность reservoir sampling. (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:55`)

- ❌ **[Metrics Sdk]** [SHOULD] `Collect` SHOULD invoke Produce on registered MetricProducers.  
  Нет поддержки внешних MetricProducer. ОтелПериодическийЧитательМетрик собирает данные только из зарегистрированных ОтелМетр, но не поддерживает регистрацию и вызов Produce на внешних MetricProducer. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] After the call to `Shutdown`, subsequent invocations to `Collect` are not allowed. SDKs SHOULD return some failure for these calls, if possible.  
  Метод Закрыть() устанавливает флаг Закрыт через АтомарноеБулево и предотвращает повторный вызов через СравнитьИУстановить, но метод СобратьИЭкспортировать (аналог Collect) не проверяет флаг Закрыт и не возвращает ошибку после Shutdown. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:93`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  Метод СброситьБуфер() вызывает СобратьИЭкспортировать() но не возвращает статус (SUCCESS/ERROR). Процедура выполняется без возвращаемого значения. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:74`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() реализован как Процедура без возвращаемого значения, не информирует вызывающую сторону о результате. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:48`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Метод СброситьБуфер() не имеет параметра таймаута и не прерывается по времени. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:48`)

- ⚠️ **[Metrics Sdk]** [SHOULD NOT] `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable).  
  Метод Закрыть() просто устанавливает флаг Закрыт = Истина, что не блокируется. Однако нет явного таймаута если бы Закрыть включал flush данных. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:53`)

- ❌ **[Metrics Sdk]** [SHOULD] `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of produced metrics.  
  Нет отдельного интерфейса MetricProducer с конфигурацией AggregationTemporality. ОтелПрометеусЧитательМетрик - это pull MetricReader, а не MetricProducer. MetricProducer как отдельная сущность (мост к сторонним источникам метрик) не реализован. (-)

- ❌ **[Otlp Exporter]** [SHOULD] However, if they are already implemented, they SHOULD continue to be supported as they were part of a stable release of the specification.  
  Опция Insecure никогда не была реализована в данном SDK. Устаревшие переменные OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE также не поддерживаются. (-)

- ⚠️ **[Otlp Exporter]** [SHOULD] The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default (e.g. for backward compatibility reasons when `grpc` was already the default in a stable SDK release).  
  Протокол по умолчанию - http/json, а не http/protobuf как рекомендует спецификация. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ⚠️ **[Otlp Exporter]** [SHOULD] SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them.  
  grpc поддерживается (ОтелGrpcТранспорт), но http/protobuf не реализован - вместо него используется http/json (ОтелHttpТранспорт с Content-Type: application/json). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If they support only one, it SHOULD be `http/protobuf`.  
  SDK поддерживает два транспорта (grpc и http/json), но ни один из них не является http/protobuf. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If no configuration is provided the default transport SHOULD be `http/protobuf` unless SDKs have good reasons to choose `grpc` as the default (e.g. for backward compatibility reasons when `grpc` was already the default in a stable SDK release).  
  Транспорт по умолчанию - http/json, а не http/protobuf как рекомендует спецификация. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ❌ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter.  
  Заголовок User-Agent не устанавливается ни в ОтелHttpТранспорт, ни в ОтелGrpcТранспорт. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The format of the header SHOULD follow RFC 7231.  
  Заголовок User-Agent не реализован, поэтому формат RFC 7231 также не соблюдается. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The resulting User-Agent SHOULD include the exporter's default User-Agent string.  
  Заголовок User-Agent не реализован. (-)

- ❌ **[Propagators]** [SHOULD] If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace Context Propagator and the Baggage `Propagator` specified in the Baggage API.  
  Платформа OneScript не имеет предварительно сконфигурированных пропагаторов. По умолчанию возвращается ОтелНоопПропагатор, а не композитный пропагатор с W3C TraceContext и Baggage. (-)

- ⚠️ **[Env Vars]** [SHOULD] They SHOULD also follow the common configuration specification.  
  Реализация использует configor для чтения переменных окружения, но полная общая спецификация конфигурации (common configuration specification) не реализована - отсутствует поддержка OTEL_CONFIG_FILE, нет иерархии переопределения конфигураций из разных источников. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:80`)

- ❌ **[Env Vars]** [SHOULD] If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied.  
  Функция Включено() (строка 561) не логирует предупреждение при получении невалидного булевого значения (например, "yes", "1"). Значение просто интерпретируется как false без уведомления пользователя. (-)

- ⚠️ **[Env Vars]** [SHOULD] All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior.  
  Используется переменная otel.enabled (из OTEL_ENABLED) вместо стандартной OTEL_SDK_DISABLED. При false SDK отключается, что противоречит конвенции 'false = безопасное значение по умолчанию' (безопасное - SDK включен). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562`)

- ⚠️ **[Env Vars]** [SHOULD] The following paragraph was added after stabilization and the requirements are thus qualified as "SHOULD" to allow implementations to avoid breaking changes.  
  Реализация парсит числовые значения через Число(), но не генерирует предупреждений при невалидных значениях и не обрабатывает их gracefully (выбрасывает исключение вместо возврата к значению по умолчанию). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:224`)

- ❌ **[Env Vars]** [SHOULD] For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them as not set.  
  Числовые значения (otel.bsp.max.queue.size, otel.bsp.schedule.delay и др.) конвертируются через Число() без обработки ошибок. Невалидное значение вызовет исключение вместо предупреждения и возврата к значению по умолчанию. (-)

- ⚠️ **[Env Vars]** [SHOULD] Enum values SHOULD be interpreted in a case-insensitive manner.  
  Пропагаторы обрабатываются case-insensitive (строка 342: НРег(СтрокаПропагаторов)), но семплеры сравниваются case-sensitive (строки 196-215: прямое сравнение ИмяСэмплера = "always_on"). Экспортеры (otel.traces.exporter и др.) также сравниваются case-sensitive. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:342`)

## Детальный анализ по разделам (Stable)

### Context

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:19` |  |
| 2 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:127` |  |
| 3 | MUST | ✅ found | In the cases where an extremely clear, pre-existing option is not available, OpenTelemetry MUST provide its own `Context` implementation. | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### Create a key

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#create-a-key)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The API MUST accept the following parameter: | `src/Ядро/Модули/ОтелКонтекст.os:35` |  |
| 5 | SHOULD NOT | ✅ found | Multiple calls to `CreateKey` with the same name SHOULD NOT return the same value unless language constraints dictate otherwise. | `src/Ядро/Модули/ОтелКонтекст.os:36` |  |
| 6 | MUST | ✅ found | The API MUST return an opaque object representing the newly created key. | `src/Ядро/Модули/ОтелКонтекст.os:36` |  |

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
| 13 | MUST | ⚠️ partial | The API MUST accept the following parameters: * The `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:203` | УстановитьЗначение(Ключ, Значение) and СделатьСпанТекущим/СделатьBaggageТекущим push a new context onto the stack, but none accept a Context object directly as a parameter. The API uses a key-value approach instead of accepting a whole Context. |
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
| 2 | SHOULD NOT | ✅ found | Language API SHOULD NOT restrict which strings are used as baggage names. | `src/Ядро/Классы/ОтелПостроительBaggage.os:23` |  |
| 3 | MUST | ✅ found | Language API MUST accept any valid UTF-8 string as baggage value in `Set` and return the same value from `Get`. | `src/Ядро/Классы/ОтелBaggage.os:68` |  |
| 4 | MUST | ✅ found | Language API MUST treat both baggage names and values as case sensitive. | `src/Ядро/Классы/ОтелBaggage.os:152` |  |
| 5 | MUST | ✅ found | The Baggage API MUST be fully functional in the absence of an installed SDK. | `src/Ядро/Классы/ОтелBaggage.os:1` |  |
| 6 | MUST | ✅ found | The `Baggage` container MUST be immutable, so that the containing `Context` also remains immutable. | `src/Ядро/Классы/ОтелBaggage.os:156` |  |

#### Operations### Get Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#operations-get-value)

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
| 12 | SHOULD NOT | ⚠️ partial | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:53` | Высокоуровневые методы (BaggageИзКонтекста, КонтекстСBaggage, ТекущийBaggage, СделатьBaggageТекущим) существуют, но функция КлючBaggage() экспортирована публично (строка 53), что даёт пользователям прямой доступ к ключу контекста. |
| 13 | SHOULD | ✅ found | If the language has support for implicitly propagated Context (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Модули/ОтелКонтекст.os:100` |  |
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
| 16 | MUST | ✅ found | The API layer or an extension package MUST include the following Propagators: | `src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:1` |  |

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
| 6 | MUST | ✅ found | The interface MUST provide a way for an old resource and an updating resource to be merged into a new resource. | `src/Ядро/Классы/ОтелРесурс.os:39` |  |
| 7 | MUST | ✅ found | The resulting resource MUST have all attributes that are on any of the two input resources. | `src/Ядро/Классы/ОтелРесурс.os:53` |  |
| 8 | MUST | ✅ found | If a key exists on both the old and updating resource, the value of the updating resource MUST be picked (even if the updated value is empty). | `src/Ядро/Классы/ОтелРесурс.os:56` |  |

#### Detecting resource information from the environment

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#detecting-resource-information-from-the-environment)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ⚠️ partial | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1` | Детекторы ресурсов реализованы (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора), но они размещены inline в пакете SDK (src/Ядро/Классы/), а не в отдельных пакетах. |
| 10 | MUST | ✅ found | Resource detector packages MUST provide a method that returns a resource. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17` |  |
| 11 | MUST NOT | ✅ found | Note the failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаПроцесса.os:19` |  |
| 12 | SHOULD | ⚠️ partial | Note the failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаПроцесса.os:22` | Ошибки при детекции перехватываются через Попытка/Исключение, но логируются на уровне Отладка (Лог.Отладка), а не как ошибки (Лог.Ошибка). Спецификация требует, чтобы ошибки при попытке детекции считались ошибками. |
| 13 | MUST | ❌ not_found | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions. | - | Детекторы ресурсов (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) заполняют семантические атрибуты (host.name, os.type, process.pid и др.), но создают ресурс через Новый ОтелРесурс(Истина) без указания Schema URL. |
| 14 | SHOULD | ⚠️ partial | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate (e.g. the detector that reads the attributes from environment values will not know what Schema URL to use). | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18` | Все детекторы используют пустой Schema URL (Новый ОтелРесурс(Истина)), но они заполняют известные семантические атрибуты (host.*, os.*, process.*), для которых по предыдущему требованию должен быть указан непустой Schema URL. Нет логики выбора Schema URL в зависимости от типа атрибутов. |
| 15 | MUST | ⚠️ partial | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources. | `src/Ядро/Классы/ОтелРесурс.os:41` | Метод Слить() обрабатывает случай конфликта Schema URL - возвращает пустой ресурс (Новый ОтелРесурс(Истина)), но не сообщает об ошибке (не вызывает исключение и не логирует ошибку). Спецификация требует, чтобы это считалось ошибкой. |

### Trace Api

#### Timestamp

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#timestamp)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `TracerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:30` |  |
| 2 | SHOULD | ✅ found | Thus, implementations of `TracerProvider` SHOULD allow creating an arbitrary number of `TracerProvider` instances. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:244` |  |

#### TracerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The `TracerProvider` MUST provide the following functions: Get a `Tracer` | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:56` |  |
| 4 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:56` |  |
| 5 | SHOULD | ⚠️ partial | `name` (required): This name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library (e.g. `io.opentelemetry.contrib.mongodb`), package, module or class name. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:59` | Параметр name принимается, но нет валидации или документации о том, что имя должно уникально идентифицировать область инструментирования. Однако параметр используется корректно. |
| 6 | MUST | ⚠️ partial | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:56` | Метод ПолучитьТрассировщик не проверяет пустое имя и не возвращает fallback-трассировщик с пустым именем. Пустая строка передаётся как есть в ОбластьИнструментирования без обработки. |
| 7 | SHOULD | ❌ not_found | its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | - | Нет логирования предупреждения при передаче пустого или невалидного имени в ПолучитьТрассировщик. |
| 8 | SHOULD | ❌ not_found | its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | - | Нет установки имени в пустую строку при невалидном значении - значение передаётся как есть, нет специальной обработки. |
| 9 | MUST NOT | ✅ found | Implementations MUST NOT require users to repeatedly obtain a `Tracer` again with the same identity to pick up configuration changes. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API MUST provide the following functionality to interact with a `Context` instance: | `src/Ядро/Модули/ОтелКонтекст.os:137` |  |
| 11 | SHOULD NOT | ✅ found | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:137` |  |
| 12 | SHOULD | ✅ found | If the language has support for implicitly propagated `Context` (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Модули/ОтелКонтекст.os:95` |  |
| 13 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### SpanContext

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spancontext)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The API MUST implement methods to create a `SpanContext`. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |
| 15 | SHOULD | ✅ found | These methods SHOULD be the only way to create a `SpanContext`. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |
| 16 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |
| 17 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |

#### Retrieving the TraceId and SpanId

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#retrieving-the-traceid-and-spanid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | The API MUST allow retrieving the `TraceId` and `SpanId` in the following forms: | `src/Трассировка/Классы/ОтелКонтекстСпана.os:22` |  |
| 19 | MUST | ✅ found | Hex - returns the lowercase hex encoded `TraceId` (result MUST be a 32-hex-character lowercase string) | `src/Трассировка/Классы/ОтелКонтекстСпана.os:22` |  |
| 20 | MUST | ✅ found | or `SpanId` (result MUST be a 16-hex-character lowercase string). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:32` |  |
| 21 | MUST | ✅ found | Binary - returns the binary representation of the `TraceId` (result MUST be a 16-byte array) | `src/Трассировка/Классы/ОтелКонтекстСпана.os:82` |  |
| 22 | MUST | ✅ found | or `SpanId` (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:92` |  |
| 23 | SHOULD NOT | ✅ found | The API SHOULD NOT expose details about how they are internally stored. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:12` |  |

#### IsValid

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isvalid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | An API called `IsValid`, that returns a boolean value, which is `true` if the SpanContext has a non-zero TraceID and a non-zero SpanID, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:72` |  |

#### IsRemote

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isremote)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | An API called `IsRemote`, that returns a boolean value, which is `true` if the SpanContext was propagated from a remote parent, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:60` |  |
| 26 | MUST | ✅ found | When extracting a `SpanContext` through the Propagators API, `IsRemote` MUST return true, | `src/Пропагация/Классы/ОтелW3CПропагатор.os:126` |  |
| 27 | MUST | ✅ found | whereas for the SpanContext of any child spans it MUST return false. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:198` |  |

#### TraceState

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracestate)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | Tracing API MUST provide at least the following operations on `TraceState`: | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:46` |  |
| 29 | MUST | ✅ found | These operations MUST follow the rules described in the W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:161` |  |
| 30 | MUST | ⚠️ partial | All mutating operations MUST return a new `TraceState` with the modifications applied. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:66` | Установить() and Удалить() return new ОтелСостояниеТрассировки instances (immutable pattern), which is correct. However, Установить() returns ЭтотОбъект when validation fails instead of a new TraceState, which is a minor deviation. |
| 31 | MUST | ✅ found | `TraceState` MUST at all times be valid according to rules specified in W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:172` |  |
| 32 | MUST | ✅ found | Every mutating operations MUST validate input parameters. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 33 | MUST NOT | ✅ found | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 34 | MUST | ✅ found | If invalid value is passed the operation ... MUST follow the general error handling guidelines. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:68` |  |

#### Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | SHOULD | ✅ found | The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable. | `src/Трассировка/Классы/ОтелСпан.os:66` |  |
| 36 | SHOULD | ✅ found | Generality SHOULD be prioritized over human-readability. | - |  |
| 37 | SHOULD | ✅ found | A `Span`'s start time SHOULD be set to the current time on span creation. | `src/Трассировка/Классы/ОтелСпан.os:610` |  |
| 38 | SHOULD | ✅ found | After the `Span` is created, it SHOULD be possible to change its name, set its `Attribute`s, add `Event`s, and set the `Status`. | `src/Трассировка/Классы/ОтелСпан.os:244` |  |
| 39 | MUST NOT | ✅ found | These MUST NOT be changed after the `Span`'s end time has been set. | `src/Трассировка/Классы/ОтелСпан.os:248` |  |
| 40 | SHOULD NOT | ⚠️ partial | `Span`s are not meant to be used to propagate information within a process. To prevent misuse, implementations SHOULD NOT provide access to a `Span`'s attributes besides its `SpanContext`. | `src/Трассировка/Классы/ОтелСпан.os:155` | ОтелСпан exposes Атрибуты() as a public method returning the full ОтелАтрибуты object, which the spec says SHOULD NOT be accessible. This is needed for export but violates the API-level recommendation. |
| 41 | MUST NOT | ✅ found | However, alternative implementations MUST NOT allow callers to create `Span`s directly. | `src/Трассировка/Классы/ОтелТрассировщик.os:68` |  |
| 42 | MUST | ✅ found | All `Span`s MUST be created via a `Tracer`. | `src/Трассировка/Классы/ОтелТрассировщик.os:68` |  |

#### Span Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST NOT | ✅ found | There MUST NOT be any API for creating a `Span` other than with a `Tracer`. | `src/Трассировка/Классы/ОтелТрассировщик.os:68` |  |
| 44 | MUST NOT | ✅ found | In languages with implicit `Context` propagation, `Span` creation MUST NOT set the newly created `Span` as the active `Span` in the current `Context` by default, but this functionality MAY be offered additionally as a separate operation. | `src/Трассировка/Классы/ОтелТрассировщик.os:68` |  |
| 45 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПостроительСпана.os:1` |  |
| 46 | MUST NOT | ⚠️ partial | This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`. | `src/Трассировка/Классы/ОтелПостроительСпана.os:36` | УстановитьРодителя() accepts both ОтелСпан and ОтелКонтекстСпана as parent, not a full Context object. The spec requires only a full Context (not Span/SpanContext). |
| 47 | MUST | ✅ found | The semantic parent of the Span MUST be determined according to the rules described in Determining the Parent Span from a Context. | `src/Трассировка/Классы/ОтелТрассировщик.os:68` |  |
| 48 | MUST | ✅ found | The API documentation MUST state that adding attributes at span creation is preferred to calling `SetAttribute` later, as samplers can only consider information already present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os:80` |  |
| 49 | SHOULD | ✅ found | `Start timestamp`, default to current time. This argument SHOULD only be set when span creation time has already passed. | `src/Трассировка/Классы/ОтелПостроительСпана.os:118` |  |
| 50 | MUST NOT | ✅ found | If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument. | `src/Трассировка/Классы/ОтелПостроительСпана.os:118` |  |
| 51 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span, and MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:102` |  |
| 52 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span, and MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:104` |  |
| 53 | MUST | ✅ found | For a Span with a parent, the `TraceId` MUST be the same as the parent. | `src/Трассировка/Классы/ОтелТрассировщик.os:75` |  |
| 54 | MUST | ✅ found | Also, the child span MUST inherit all `TraceState` values of its parent by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:228` |  |
| 55 | MUST | ✅ found | Any span that is created MUST also be ended. | `src/Трассировка/Классы/ОтелСпан.os:444` |  |

#### Specifying links

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#specifying-links)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 56 | MUST | ✅ found | During `Span` creation, a user MUST have the ability to record links to other `Span`s. | `src/Трассировка/Классы/ОтелПостроительСпана.os:99` |  |

#### Get Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 57 | MUST | ✅ found | The Span interface MUST provide: | `src/Трассировка/Классы/ОтелСпан.os:78` |  |
| 58 | MUST | ✅ found | The returned value MUST be the same for the entire Span lifetime. | `src/Трассировка/Классы/ОтелСпан.os:78` |  |
| 59 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:234` |  |
| 60 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:234` |  |
| 61 | SHOULD NOT | ✅ found | `IsRecording` SHOULD NOT take any parameters. | `src/Трассировка/Классы/ОтелСпан.os:234` |  |
| 62 | SHOULD | ✅ found | This flag SHOULD be used to avoid expensive computations of a Span attributes or events in case when a Span is definitely not recorded. | `src/Трассировка/Классы/ОтелСпан.os:234` |  |

#### Set Attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 63 | MUST | ✅ found | A `Span` MUST have the ability to set `Attributes` associated with it. | `src/Трассировка/Классы/ОтелСпан.os:260` |  |
| 64 | MUST | ✅ found | The Span interface MUST provide: | `src/Трассировка/Классы/ОтелСпан.os:260` |  |
| 65 | SHOULD | ✅ found | Setting an attribute with the same key as an existing attribute SHOULD overwrite the existing attribute's value. | `src/Трассировка/Классы/ОтелСпан.os:264` |  |

#### Add Events

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-events)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | MUST | ✅ found | A `Span` MUST have the ability to add events. Events have a time associated with the moment when they are added to the `Span`. | `src/Трассировка/Классы/ОтелСпан.os:290` |  |
| 67 | MUST | ✅ found | The Span interface MUST provide: | `src/Трассировка/Классы/ОтелСпан.os:290` |  |
| 68 | SHOULD | ✅ found | Events SHOULD preserve the order in which they are recorded. | `src/Трассировка/Классы/ОтелСпан.os:298` |  |

#### Add Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | MUST | ✅ found | A `Span` MUST have the ability to add `Link`s associated with it after its creation - see Links. | `src/Трассировка/Классы/ОтелСпан.os:375` |  |

#### Set Status

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-status)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 70 | MUST | ✅ found | Description MUST only be used with the Error StatusCode value. | `src/Трассировка/Классы/ОтелСпан.os:429` |  |
| 71 | MUST | ✅ found | The Span interface MUST provide: An API to set the Status. | `src/Трассировка/Классы/ОтелСпан.os:413` |  |
| 72 | MUST | ✅ found | Description MUST be IGNORED for StatusCode Ok & Unset values. | `src/Трассировка/Классы/ОтелСпан.os:432` |  |
| 73 | SHOULD | ✅ found | This SHOULD be called SetStatus. | `src/Трассировка/Классы/ОтелСпан.os:413` |  |
| 74 | SHOULD | ✅ found | The status code SHOULD remain unset, except for the following circumstances: | `src/Трассировка/Классы/ОтелСпан.os:614` |  |
| 75 | SHOULD | ✅ found | An attempt to set value Unset SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:424` |  |
| 76 | SHOULD | ⚠️ partial | When the status is set to Error by Instrumentation Libraries, the Description SHOULD be documented and predictable. | `src/Трассировка/Классы/ОтелСпан.os:413` | SetStatus API exists and accepts Description for Error, but there is no documentation of predictable Description values for instrumentation libraries. |
| 77 | SHOULD | ⚠️ partial | Instrumentation Libraries SHOULD publish their own conventions, including possible values of Description and what they mean. | - | No published conventions for Description values found in the codebase. |
| 78 | SHOULD NOT | ✅ found | Generally, Instrumentation Libraries SHOULD NOT set the status code to Ok, unless explicitly configured to do so. | `src/Трассировка/Классы/ОтелСпан.os:413` |  |
| 79 | SHOULD | ✅ found | Instrumentation Libraries SHOULD leave the status code as Unset unless there is an error, as described above. | `src/Трассировка/Классы/ОтелСпан.os:614` |  |
| 80 | SHOULD | ✅ found | When span status is set to Ok it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 81 | SHOULD | ✅ found | When span status is set to Ok it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 82 | SHOULD | ❌ not_found | Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generate. | - | This requirement is about analysis tools consuming spans, not about SDK implementation. No analysis tool functionality exists in this SDK. |

#### UpdateName

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#updatename)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 83 | SHOULD | ✅ found | Implementations SHOULD ignore all subsequent calls to End and any other Span methods, i.e. the Span becomes non-recording by being ended | `src/Трассировка/Классы/ОтелСпан.os:448` |  |
| 84 | MUST | ❌ not_found | However, all API implementations of such methods MUST internally call the End method and be documented to do so. | - | No language-specific convenience methods (like Python 'with' statement) that wrap End are implemented. |
| 85 | MUST NOT | ✅ found | End MUST NOT have any effects on child spans. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 86 | MUST NOT | ✅ found | End MUST NOT inactivate the Span in any Context it is active in. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 87 | MUST | ✅ found | It MUST still be possible to use an ended span as parent via a Context it is contained in. | `src/Трассировка/Классы/ОтелСпан.os:80` |  |
| 88 | MUST | ✅ found | Also, any mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:398` |  |
| 89 | MUST | ✅ found | If omitted, this MUST be treated equivalent to passing the current time. | `src/Трассировка/Классы/ОтелСпан.os:449` |  |
| 90 | MUST NOT | ⚠️ partial | This operation itself MUST NOT perform blocking I/O on the calling thread. | `src/Трассировка/Классы/ОтелСпан.os:447` | End() calls processor.ПриЗавершении synchronously which may invoke exporters that perform blocking I/O depending on the processor type (e.g. SimpleSpanProcessor). |
| 91 | SHOULD | ✅ found | Any locking used needs be minimized and SHOULD be removed entirely if possible. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |

#### Record Exception

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#record-exception)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 92 | SHOULD | ✅ found | To facilitate recording an exception languages SHOULD provide a RecordException method if the language uses exceptions. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 93 | MUST | ✅ found | The method MUST record an exception as an Event with the conventions outlined in the exceptions document. | `src/Трассировка/Классы/ОтелСпан.os:346` |  |
| 94 | SHOULD | ✅ found | The minimum required argument SHOULD be no more than only an exception object. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 95 | MUST | ✅ found | If RecordException is provided, the method MUST accept an optional parameter to provide any additional event attributes | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 96 | SHOULD | ✅ found | (this SHOULD be done in the same way as for the AddEvent method). | `src/Трассировка/Классы/ОтелСпан.os:346` |  |

#### Span lifetime

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-lifetime)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | MUST | ✅ found | Start and end time as well as Event's timestamps MUST be recorded at a time of a calling of corresponding API. | `src/Трассировка/Классы/ОтелСпан.os:603` |  |

#### Wrapping a SpanContext in a Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#wrapping-a-spancontext-in-a-span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | MUST | ✅ found | The API MUST provide an operation for wrapping a SpanContext with an object implementing the Span interface. | `src/Трассировка/Классы/ОтелНоопСпан.os:271` |  |
| 99 | SHOULD NOT | ⚠️ partial | If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type). | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | ОтелНоопСпан is a public class available to all consumers. The spec recommends hiding this type if possible. |
| 100 | SHOULD | ⚠️ partial | If a new type is required to be publicly exposed, it SHOULD be named NonRecordingSpan. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | The class is named ОтелНоопСпан (NoopSpan) instead of the recommended NonRecordingSpan naming. |
| 101 | MUST | ✅ found | GetContext MUST return the wrapped SpanContext. | `src/Трассировка/Классы/ОтелНоопСпан.os:34` |  |
| 102 | MUST | ✅ found | IsRecording MUST return false to signal that events, attributes and other elements are not being recorded, i.e. they are being dropped. | `src/Трассировка/Классы/ОтелНоопСпан.os:158` |  |
| 103 | MUST | ✅ found | The remaining functionality of Span MUST be defined as no-op operations. | `src/Трассировка/Классы/ОтелНоопСпан.os:165` |  |
| 104 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |
| 105 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |

#### SpanKind

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 106 | SHOULD | ✅ found | In order for SpanKind to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose. | `src/Трассировка/Модули/ОтелВидСпана.os:1` |  |
| 107 | SHOULD NOT | ✅ found | For example, a server-side span SHOULD NOT be used to describe outgoing remote procedure call. | `src/Трассировка/Модули/ОтелВидСпана.os:1` |  |
| 108 | MUST | ✅ found | A user MUST have the ability to record links to other SpanContexts. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 109 | MUST | ✅ found | The API MUST provide: An API to record a single Link where the Link properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 110 | SHOULD | ⚠️ partial | Implementations SHOULD record links containing SpanContext with empty TraceId or SpanId (all zeros) as long as either the attribute set or TraceState is non-empty. | `src/Трассировка/Классы/ОтелСпан.os:361` | AddLink records all links regardless of SpanContext validity - it does not specifically check for empty TraceId/SpanId with non-empty attributes/TraceState. |
| 111 | SHOULD | ✅ found | Span SHOULD preserve the order in which Links are set. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 112 | MUST | ✅ found | The API documentation MUST state that adding links at span creation is preferred to calling AddLink later, for contexts that are available during span creation, because head sampling decisions can only consider information present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os:96` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 113 | MUST | ✅ found | TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:6` |  |
| 114 | MUST | ✅ found | Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:3` |  |
| 115 | MUST | ✅ found | Span - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:3` |  |
| 116 | MUST | ✅ found | Event - Events are immutable and MUST be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСобытиеСпана.os:3` |  |
| 117 | SHOULD | ⚠️ partial | Link - Links are immutable and SHOULD be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:373` | Links are stored as plain Соответствие (Map) objects, not as a dedicated immutable Link class. They are effectively immutable after creation but there's no explicit Link class guaranteeing immutability. |

#### Behavior of the API in the absence of an installed SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#behavior-of-the-api-in-the-absence-of-an-installed-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 118 | MUST | ✅ found | The API MUST return a non-recording Span with the SpanContext in the parent Context (whether explicitly given or implicit current). | `src/Трассировка/Классы/ОтелТрассировщик.os:74` |  |
| 119 | SHOULD | ❌ not_found | If the Span in the parent Context is already non-recording, it SHOULD be returned directly without instantiating a new Span. | - | The tracer always creates a new ОтелНоопСпан when sampling fails, even if the parent is already non-recording. It does not check if parent is non-recording to return it directly. |
| 120 | MUST | ⚠️ partial | If the parent Context contains no Span, an empty non-recording Span MUST be returned instead (i.e., having a SpanContext with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags). | `src/Трассировка/Классы/ОтелТрассировщик.os:66` | When there is no parent and sampling fails, a NoopSpan is returned with a new generated TraceId and SpanId (not all-zeros). The spec requires all-zero IDs when no parent context exists and no SDK is installed. The ОтелНоопСпан default constructor does create all-zero IDs, but the Tracer path generates new IDs. |

### Trace Sdk

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, `Sampler`, and (Development) TracerConfigurator) MUST be owned by the `TracerProvider`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:11` | SpanProcessors, Sampler, SpanLimits и TracerConfigurator принадлежат провайдеру, но IdGenerator не конфигурируется через провайдер - используется статический ОтелУтилиты.СгенерироватьИдТрассировки() |
| 2 | MUST | ✅ found | the updated configuration MUST also apply to all already returned `Tracers` | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |
| 3 | MUST NOT | ✅ found | it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvider` before or after the configuration change | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:121` | Синхронный СброситьБуфер() - процедура без возвращаемого значения. Асинхронный СброситьБуферАсинхронно() возвращает Обещание, через которое можно узнать результат, но синхронная версия не сообщает об успехе/неудаче |
| 5 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98` | Синхронный СброситьБуфер() не имеет встроенного таймаута. Асинхронный вариант через Обещание позволяет задать таймаут на стороне вызывающего, но встроенного таймаута нет |
| 6 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered `SpanProcessors`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:99` |  |

#### Additional Span Interfaces

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#additional-span-interfaces)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | A function receiving this as argument MUST be able to access all information that was added to the span, as listed in the API spec for Span. | `src/Трассировка/Классы/ОтелСпан.os:71` |  |
| 8 | MUST | ✅ found | A function receiving this as argument MUST be able to access the `InstrumentationScope` [since 1.10.0] and `Resource` information (implicitly) associated with the span. | `src/Трассировка/Классы/ОтелСпан.os:170` |  |
| 9 | MUST | ⚠️ partial | For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated since 1.10.0] having the same name and version values as the `InstrumentationScope`. | `src/Трассировка/Классы/ОтелСпан.os:170` | ОбластьИнструментирования (InstrumentationScope) содержит те же данные (имя и версию), но отдельного аксессора InstrumentationLibrary для обратной совместимости нет |
| 10 | MUST | ✅ found | A function receiving this as argument MUST be able to reliably determine whether the Span has ended | `src/Трассировка/Классы/ОтелСпан.os:197` |  |
| 11 | MUST | ✅ found | Counts for attributes, events and links dropped due to collection limits MUST be available for exporters to report as described in the exporters specification. | `src/Трассировка/Классы/ОтелСпан.os:206` |  |
| 12 | MUST | ⚠️ partial | implementations MAY choose not to expose (and store) the full parent Context of the Span but they MUST expose at least the full parent SpanContext. | `src/Трассировка/Классы/ОтелСпан.os:89` | Спан хранит только ИдРодительскогоСпана (строка с ID родительского спана), но не полный родительский SpanContext (который включает TraceId, SpanId, TraceFlags, TraceState, IsRemote) |
| 13 | MUST | ✅ found | It MUST be possible for functions being called with this to somehow obtain the same `Span` instance and type that the span creation API returned (or will return) to the user | `src/Трассировка/Классы/ОтелСпан.os:455` |  |

#### Sampling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | Span Processor MUST receive only those spans which have this field set to `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:69` |  |
| 15 | SHOULD NOT | ⚠️ partial | However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37` | The processor passes all received spans to the exporter without checking the Sampled flag. In practice, built-in samplers never produce RECORD_ONLY spans, but there's no explicit filtering for the Sampled flag before export. |
| 16 | MUST | ✅ found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелСпан.os:458` |  |
| 17 | SHOULD NOT | ⚠️ partial | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37` | The processor/exporter pipeline has no filtering based on the Sampled flag. All spans passed from the processor reach the exporter. Built-in samplers only produce DROP or RECORD_AND_SAMPLE, so in practice non-sampled recording spans don't reach the exporter, but the filtering is not enforced at the exporter level. |
| 18 | MUST NOT | ✅ found | the OpenTelemetry SDK MUST NOT allow this combination. | `src/Трассировка/Классы/ОтелТрассировщик.os:73` |  |

#### SDK Span creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sdk-span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | When asked to create a Span, the SDK MUST act as if doing the following in order: | `src/Трассировка/Классы/ОтелТрассировщик.os:59` |  |

#### ShouldSample

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shouldsample)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | If the parent `SpanContext` contains a valid `TraceId`, they MUST always match. | `src/Трассировка/Классы/ОтелТрассировщик.os:62` |  |
| 21 | MUST NOT | ✅ found | `RECORD_ONLY` - `IsRecording` will be `true`, but the `Sampled` flag MUST NOT be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:167` |  |
| 22 | MUST | ✅ found | `RECORD_AND_SAMPLE` - `IsRecording` will be `true` and the `Sampled` flag MUST be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:168` |  |
| 23 | SHOULD | ⚠️ partial | so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend to change it. | `src/Трассировка/Классы/ОтелРезультатСэмплирования.os:77` | The sampler (ОтелСэмплер.ДолженСэмплировать) creates ОтелРезультатСэмплирования without passing through the parent Tracestate. The Tracer compensates by falling back to parent's Tracestate in ОпределитьСостояниеТрассировки when the sampler result has empty Tracestate. The spec intends the sampler itself to return the passed-in Tracestate. |
| 24 | SHOULD NOT | ✅ found | Callers SHOULD NOT cache the returned value. | `src/Трассировка/Модули/ОтелСэмплер.os:106` |  |

#### TraceID randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#traceid-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | SHOULD | ⚠️ partial | For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values. | `src/Ядро/Модули/ОтелУтилиты.os:78` | TraceIDs are generated using УникальныйИдентификатор (UUID v4) which provides randomness, but not specifically compliant with W3C Trace Context Level 2 requirements (which specify the least significant 56 bits must be random). UUID v4 has 122 random bits but with fixed version/variant bits that reduce randomness in specific positions. |

#### Random trace flag

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#random-trace-flag)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | SHOULD | ❌ not_found | For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements. | - | The SDK only sets bit 0 (Sampled) in trace flags via ВычислитьФлагиТрассировки() which returns 0 or 1. The Random flag (bit 1 per W3C Trace Context Level 2) is never set. |

#### Explicit randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#explicit-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 27 | MUST NOT | ⚠️ partial | SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value. | `src/Трассировка/Классы/ОтелТрассировщик.os:183` | The SDK has no explicit awareness of the rv sub-key in OpenTelemetry TraceState. However, parent TraceState (including rv) is preserved by default through ОпределитьСостояниеТрассировки fallback. The SDK does not overwrite rv, but also does not explicitly protect it - it's preserved incidentally through TraceState pass-through. |
| 28 | SHOULD | ⚠️ partial | For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the `rv` sub-key of the OpenTelemetry TraceState. | `src/Трассировка/Модули/ОтелСэмплер.os:288` | The TraceIdRatioBased sampler uses TraceId bytes as random source, implicitly presuming TraceIDs are random. However, the 'unless' clause is not implemented - the SDK never checks for explicit randomness (rv sub-key) in OpenTelemetry TraceState as an alternative randomness source. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | SHOULD | ⚠️ partial | If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated. | `src/Ядро/Модули/ОтелУтилиты.os:63` | The SDK supports custom IdGenerator via ОтелУтилиты.УстановитьГенераторИд(). However, the IdGenerator extension has no way to influence the Random trace flag - flag computation is in ОтелТрассировщик.ВычислитьФлагиТрассировки() which only considers the sampling decision, not the IdGenerator. |

#### Span Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | Span attributes MUST adhere to the common rules of attribute limits. | `src/Трассировка/Классы/ОтелСпан.os:263` |  |
| 31 | MUST | ✅ found | If the SDK implements the limits above it MUST provide a way to change these limits, via a configuration to the TracerProvider, by allowing users to configure individual limits like in the Java example bellow. | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:74` |  |
| 32 | SHOULD | ✅ found | The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:96` |  |
| 33 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `SpanLimits`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:1` |  |
| 34 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute, event, or link was discarded due to such a limit. | `src/Трассировка/Классы/ОтелСпан.os:468` |  |
| 35 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per discarded attribute, event, or link). | `src/Трассировка/Классы/ОтелСпан.os:469` |  |

#### Id Generators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#id-generators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | The SDK MUST by default randomly generate both the `TraceId` and the `SpanId`. | `src/Ядро/Модули/ОтелУтилиты.os:78` |  |
| 37 | MUST | ✅ found | The SDK MUST provide a mechanism for customizing the way IDs are generated for both the `TraceId` and the `SpanId`. | `src/Ядро/Модули/ОтелУтилиты.os:63` |  |
| 38 | MUST | ✅ found | The SDK MAY provide this functionality by allowing custom implementations of an interface like the java example below (name of the interface MAY be `IdGenerator`, name of the methods MUST be consistent with SpanContext), which provides extension points for two methods, one to generate a `SpanId` and one for `TraceId`. | `src/Ядро/Модули/ОтелУтилиты.os:78` |  |
| 39 | MUST NOT | ✅ found | Additional `IdGenerator` implementing vendor-specific protocols such as AWS X-Ray trace id generator MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | - |  |

#### Span processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 40 | MUST | ✅ found | SDK MUST allow to end each pipeline with individual exporter. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:85` |  |
| 41 | MUST | ✅ found | SDK MUST allow users to implement and configure custom processors. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:1` |  |
| 42 | MUST | ✅ found | The `SpanProcessor` interface MUST declare the following methods: | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11` |  |
| 43 | SHOULD | ✅ found | The `SpanProcessor` interface SHOULD declare the following methods: | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:21` |  |
| 44 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:18` |  |
| 45 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ОтелСпан.os:263` |  |

#### OnEnd(Span)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onendspan)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | MUST | ✅ found | This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:458` |  |

#### Shutdown()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | SHOULD | ⚠️ partial | `Shutdown` SHOULD be called only once for each `SpanProcessor` instance. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:75` | ОтелБазовыйПакетныйПроцессор sets Закрыт=Истина in Закрыть and checks it in Обработать, but Закрыть itself does not guard against double invocation. ОтелПростойПроцессорСпанов.Закрыть has no once-only guard at all. |
| 48 | SHOULD | ⚠️ partial | After the call to `Shutdown`, subsequent calls to `OnStart`, `OnEnd`, or `ForceFlush` are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43` | ОтелБазовыйПакетныйПроцессор.Обработать checks Закрыт flag at line 43, but СброситьБуфер (ForceFlush) does not check Закрыт before executing. ОтелПростойПроцессорСпанов has no shutdown state tracking at all. |
| 49 | SHOULD | ❌ not_found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | All Закрыть methods are void procedures (Процедура) returning no status. Neither ОтелБазовыйПакетныйПроцессор.Закрыть, ОтелПростойПроцессорСпанов.Закрыть, nor ОтелКомпозитныйПроцессорСпанов.Закрыть provide any success/failure/timeout indication to the caller. |
| 50 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:77` |  |
| 51 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192` | ОтелБазовыйПакетныйПроцессор.ОстановитьФоновыйЭкспорт uses ТаймаутЭкспортаМс for background task wait, but the Закрыть method itself has no explicit timeout parameter for the caller to control, and ЭкспортироватьВсеПакеты loops without a timeout bound. |

#### ForceFlush()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 52 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `Spans` for which the `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 53 | SHOULD | ⚠️ partial | In particular, if any `SpanProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all spans for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120` | ОтелБазовыйПакетныйПроцессор.ЭкспортироватьВсеПакеты calls Экспортер.Экспортировать for all buffered data, but does not invoke ForceFlush (СброситьБуфер) on the exporter itself after exporting. |
| 54 | MUST | ⚠️ partial | The built-in SpanProcessors MUST do so. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` | Built-in ОтелПакетныйПроцессорСпанов exports all buffered spans via ЭкспортироватьВсеПакеты, but does not call ForceFlush on the exporter after exporting. ОтелПростойПроцессорСпанов has empty СброситьБуфер (no buffering, correct) but also does not call ForceFlush on its exporter. |
| 55 | MUST | ❌ not_found | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. | - | СброситьБуфер methods in all processor implementations accept no timeout parameter. ОтелБазовыйПакетныйПроцессор.ЭкспортироватьВсеПакеты loops without any timeout mechanism, so there is no way to prioritize honoring a timeout. |
| 56 | SHOULD | ❌ not_found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | All СброситьБуфер methods are void procedures (Процедура) with no return value or callback mechanism to report success, failure, or timeout to the caller. |
| 57 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `SpanProcessor` exports the completed spans. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 58 | SHOULD | ❌ not_found | `ForceFlush` SHOULD complete or abort within some timeout. | - | СброситьБуфер accepts no timeout parameter. ОтелБазовыйПакетныйПроцессор.ЭкспортироватьВсеПакеты loops through all buffered data without any timeout bound, so there is no mechanism to abort within a specified time. |

#### Built-in span processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#built-in-span-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:1, src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:1` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:41` |  |
| 61 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:144` |  |
| 62 | SHOULD | ✅ found | The processor SHOULD export a batch when any of the following happens AND the previous export call has returned: | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:54` |  |
| 63 | MUST | ⚠️ partial | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:5` | Есть комментарий 'Export и Shutdown/ForceFlush могут вызываться конкурентно' в файле экспортера, но нет формальной документации о характеристиках конкурентности, которые SDK требует от экспортера. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 64 | MUST | ✅ found | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:13` |  |

#### `Export(batch)`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | MUST NOT | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 66 | MUST | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 67 | SHOULD NOT | ✅ found | The default SDK's Span Processors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the spans are being sent to. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37` |  |

#### `ForceFlush()`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Spans` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` |  |
| 69 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` | СброситьБуфер() реализован как Процедура (void), а не Функция - не возвращает результат успеха/неудачи/таймаута вызывающей стороне. |
| 70 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed spans. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` |  |
| 71 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` | СброситьБуфер() в ОтелЭкспортерСпанов выполняется синхронно без таймаута. В базовом пакетном процессоре есть ТаймаутЭкспортаМс для фонового экспорта, но сам метод СброситьБуфер экспортера не имеет механизма таймаута. |

#### Examples

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#examples)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST | ✅ found | Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:17` |  |
| 73 | MUST | ✅ found | Sampler - `ShouldSample` and `GetDescription` MUST be safe to be called concurrently. | `src/Трассировка/Модули/ОтелСэмплер.os:140` |  |
| 74 | MUST | ✅ found | Span processor - all methods MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:7` |  |
| 75 | MUST | ✅ found | Span Exporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:5` |  |

### Logs Api

#### Logs API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logs-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `LoggerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:31` |  |

#### LoggerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `LoggerProvider` MUST provide the following functions: | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 3 | MUST | ✅ found | This API MUST accept the following instrumentation scope parameters: | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 4 | MUST | ✅ found | This API MUST be structured to accept a variable number of attributes, including none. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:58` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The `Logger` MUST provide a function to: | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 6 | SHOULD | ✅ found | The `Logger` SHOULD provide functions to: | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 7 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Логирование/Классы/ОтелЗаписьЛога.os:44` |  |
| 8 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 9 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:82` |  |
| 10 | SHOULD | ✅ found | When only explicit Context is supported, this parameter SHOULD be required. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 11 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when generating a `LogRecord`, a `Logger` SHOULD provide this `Enabled` API. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 12 | SHOULD | ✅ found | The API SHOULD accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 13 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 14 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:150` |  |
| 15 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 16 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response. | `src/Логирование/Классы/ОтелЛоггер.os:28` | Метод Включен() документирован, но комментарий не содержит явного указания вызывать этот API каждый раз перед отправкой LogRecord для получения актуального ответа. |

#### Optional and required parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#optional-and-required-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 18 | MUST NOT | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 19 | MUST | ✅ found | For each required parameter, the API MUST be structured to obligate a user to provide it. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |

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
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `LoggerProviders`s. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:61` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration (i.e. LogRecordProcessors and (Development) LoggerConfigurator) MUST be owned by the `LoggerProvider`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:12` |  |
| 6 | MUST | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained from the `LoggerProvider` before or after the configuration change). | `src/Логирование/Классы/ОтелЛоггер.os:107` |  |
| 7 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained from the `LoggerProvider` before or after the configuration change). | `src/Логирование/Классы/ОтелЛоггер.os:107` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | Синхронный метод СброситьБуфер() является процедурой (void) и не возвращает статус. Асинхронный СброситьБуферАсинхронно() возвращает Обещание, но синхронный вариант не сигнализирует об успехе или ошибке. |
| 9 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | СброситьБуфер() является процедурой (void) и не возвращает статус ERROR при ошибке. |
| 10 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | СброситьБуфер() является процедурой (void) и не возвращает статус NO ERROR при отсутствии ошибок. |
| 11 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | Синхронный метод СброситьБуфер() не имеет механизма таймаута. Асинхронная версия СброситьБуферАсинхронно() опирается на таймаут Promise, но сам метод не принимает параметр таймаута. |
| 12 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:108` |  |

#### ReadableLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readablelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | A function receiving this as an argument MUST be able to access all the information added to the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:42` |  |
| 14 | MUST | ✅ found | It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) associated with the `LogRecord`. | `src/Логирование/Классы/ОтелЗаписьЛога.os:131` |  |
| 15 | MUST | ✅ found | The trace context fields MUST be populated from the resolved `Context` (either the explicitly passed `Context` or the current `Context`) when emitted. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 16 | MUST | ✅ found | Counts for attributes due to collection limits MUST be available for exporters to report as described in the transformation to non-OTLP formats specification. | `src/Логирование/Классы/ОтелЗаписьЛога.os:152` |  |

#### ReadWriteLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readwritelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | A function receiving this as an argument MUST additionally be able to modify the following information added to the LogRecord: `Timestamp`, `ObservedTimestamp`, `SeverityText`, `SeverityNumber`, `Body`, `Attributes` (addition, modification, removal), `TraceId`, `SpanId`, `TraceFlags`, `EventName`. | `src/Логирование/Классы/ОтелЗаписьЛога.os:178` |  |

#### LogRecord Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecord-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | `LogRecord` attributes MUST adhere to the common rules of attribute limits. | `src/Логирование/Классы/ОтелЗаписьЛога.os:226` |  |
| 19 | MUST | ✅ found | If the SDK implements attribute limits it MUST provide a way to change these limits, via a configuration to the `LoggerProvider`, by allowing users to configure individual limits like in the Java example below. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:56` |  |
| 20 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `LogRecordLimits`. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:1` |  |
| 21 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute was discarded due to such a limit. | `src/Логирование/Классы/ОтелЗаписьЛога.os:310` |  |
| 22 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per `LogRecord` (i.e., not per discarded attribute). | `src/Логирование/Классы/ОтелЗаписьЛога.os:311` |  |

#### LogRecordProcessor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | MUST | ✅ found | The SDK MUST allow each pipeline to end with an individual exporter. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:66` |  |
| 24 | MUST | ✅ found | The SDK MUST allow users to implement and configure custom processors and decorate built-in processors for advanced scenarios such as enriching with attributes. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:10` |  |

#### LogRecordProcessor operations#### OnEmit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor-operations-onemit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | SHOULD NOT | ⚠️ partial | This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD NOT block or throw exceptions. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17` | Композитный процессор оборачивает вызовы в Попытка-Исключение (не выбрасывает исключения), но простой процессор ОтелПростойПроцессорЛогов.ПриПоявлении() блокируется на БлокировкаЭкспорта и может выбрасывать исключения (ВызватьИсключение в строке 27). |
| 26 | MUST | ✅ found | For a `LogRecordProcessor` registered directly on SDK `LoggerProvider`, the `logRecord` mutations MUST be visible in next registered processors. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:18` |  |
| 27 | SHOULD | ❌ not_found | To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecord` be used for any concurrent processing, such as in a batching processor. | - | Нет документации или рекомендаций пользователям о клонировании logRecord для конкурентной обработки. Пакетный процессор добавляет оригинальный объект записи в буфер без клонирования. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST NOT | ❌ not_found | Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller. Parameters are immutable or passed by value. | - | Интерфейс ИнтерфейсПроцессорЛогов не содержит метода Enabled. Метод Включен() реализован только на уровне Logger (ОтелЛоггер.os:42), но не на уровне LogRecordProcessor. Требование о неизменности параметров в processor-level Enabled не может быть проверено. |

#### ShutDown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | SHOULD | ⚠️ partial | `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117` | Провайдер защищает от повторного вызова через атомарный флаг Закрыт.СравнитьИУстановить(), но простой процессор ОтелПростойПроцессорЛогов.Закрыть() не имеет защиты от повторного вызова. |
| 30 | SHOULD | ⚠️ partial | After the call to `Shutdown`, subsequent calls to `OnEmit` are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43` | Пакетный процессор проверяет флаг Закрыт и возвращает Возврат в методе Обработать (строка 43-44), но простой процессор ОтелПростойПроцессорЛогов.ПриПоявлении() не проверяет состояние завершения. |
| 31 | SHOULD | ❌ not_found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Метод Закрыть() реализован как Процедура (void) во всех процессорах - не возвращает индикацию успеха, неудачи или таймаута. |
| 32 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:77` |  |
| 33 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192` | Пакетный процессор использует таймаут при остановке фонового экспорта (Обещание.Получить(ТаймаутЭкспортаМс)), но метод Закрыть() не принимает параметр таймаута и финальный экспорт ЭкспортироватьВсеПакеты() не ограничен по времени. |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `LogRecord`s for which the `LogRecordProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 35 | SHOULD | ⚠️ partial | In particular, if any `LogRecordProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all `LogRecord`s for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` | СброситьБуфер() вызывает ЭкспортироватьВсеПакеты(), который вызывает Экспортер.Экспортировать() для всех оставшихся записей, но не вызывает ForceFlush (СброситьБуфер) на самом экспортере. |
| 36 | MUST | ✅ found | The built-in LogRecordProcessors MUST do so. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 37 | MUST | ❌ not_found | If a timeout is specified (see below), the `LogRecordProcessor` MUST prioritize honoring the timeout over finishing all calls. | - | Метод СброситьБуфер() не принимает параметр таймаута и не имеет механизма прерывания экспорта по таймауту. |
| 38 | SHOULD | ❌ not_found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Метод СброситьБуфер() реализован как Процедура (void) - не возвращает индикацию успеха, неудачи или таймаута. |
| 39 | SHOULD | ❌ not_found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `LogRecordProcessor` exports the emitted `LogRecord`s. | - | Нет документации или руководства, ограничивающего использование ForceFlush только необходимыми случаями. |
| 40 | SHOULD | ❌ not_found | `ForceFlush` SHOULD complete or abort within some timeout. | - | Метод СброситьБуфер() не имеет механизма таймаута - выполняется синхронно до завершения без ограничения по времени. |

#### Built-in processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#built-in-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 41 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1` |  |
| 42 | SHOULD | ❌ not_found | Other common processing scenarios SHOULD be first considered for implementation out-of-process in OpenTelemetry Collector. | - | Нет документации, рекомендующей использовать OpenTelemetry Collector для дополнительных сценариев обработки. |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:22` |  |
| 44 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:144` |  |
| 45 | MUST | ❌ not_found | Each implementation MUST document the concurrency characteristics the SDK | - | Нет явной документации о характеристиках конкурентности для реализаций экспортера логов. |

#### LogRecordExporter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | MUST | ✅ found | A `LogRecordExporter` MUST support the following functions: | `src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:13` |  |

#### Export

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#export)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | MUST NOT | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 48 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:149` |  |
| 49 | SHOULD NOT | ✅ found | The default SDK's `LogRecordProcessors` SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the logs are being sent to. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:18` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 50 | SHOULD | ✅ found | This is a hint to ensure that the export of any `ReadableLogRecords` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41` |  |
| 51 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:19` | СброситьБуфер() определена как Процедура (void), не возвращает результат успеха/неудачи/таймаута. Интерфейс и реализация не предоставляют обратной связи вызывающему коду. |
| 52 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the `ReadlableLogRecords`. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41` |  |
| 53 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | SHOULD | ⚠️ partial | Shutdown SHOULD be called only once for each `LogRecordExporter` instance. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47` | Метод Закрыть() экспортера не имеет защиты от повторного вызова (нет проверки флага Закрыт перед установкой). В отличие от ОтелПровайдерЛогирования, который использует АтомарноеБулево.СравнитьИУстановить(), экспортер просто устанавливает Закрыт = Истина без проверки. |
| 55 | SHOULD | ✅ found | After the call to `Shutdown` subsequent calls to `Export` are not allowed and SHOULD return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:26` |  |
| 56 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47` |  |
| 57 | MUST | ✅ found | LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:224` |  |
| 58 | MUST | ✅ found | Logger - all methods MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелЛоггер.os:230` |  |
| 59 | MUST | ⚠️ partial | LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47` | Флаг Закрыт в экспортере - обычный Булево, а не АтомарноеБулево. В отличие от ОтелПровайдерЛогирования (строка 224), который использует АтомарноеБулево для потокобезопасности, экспортер не обеспечивает формальную потокобезопасность при конкурентных вызовах Закрыть(). |

### Metrics Api

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `MeterProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:31` |  |

#### MeterProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `MeterProvider` MUST provide the following functions: * Get a `Meter` | `src/Метрики/Классы/ОтелПровайдерМетрик.os:38` |  |
| 3 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Метрики/Классы/ОтелПровайдерМетрик.os:38` |  |
| 4 | MUST NOT | ✅ found | Users can provide a `version`, but it is up to their discretion. Therefore, this API needs to be structured to accept a `version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:40` |  |
| 5 | MUST | ✅ found | Users can provide a `schema_url`, but it is up to their discretion. Therefore, this API needs to be structured to accept a `schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:42` |  |
| 6 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:40` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ found | Note: `Meter` SHOULD NOT be responsible for the configuration. This should be the responsibility of the `MeterProvider` instead. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:1` |  |

#### Meter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The `Meter` MUST provide functions to create new Instruments: | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Instrument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ❌ not_found | Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying. | - | OneScript не делает различий между целыми и вещественными числами на уровне типов (единый тип Число). Дескриптор инструмента не включает тип данных числа как идентифицирующий признак. |

#### Synchronous and Asynchronous instruments

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#synchronous-and-asynchronous-instruments)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API to construct synchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 11 | SHOULD | ✅ found | The `name` needs to be provided by a user. If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 12 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 13 | SHOULD | ⚠️ partial | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:39` | Метод СоздатьСчетчик документирует параметр Имя как Строка, но не указывает требования к синтаксису имени инструмента. |
| 14 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`; that is left to implementations of the API, like the SDK. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 15 | MUST NOT | ✅ found | Users can provide a `unit`, but it is up to their discretion. Therefore, this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 16 | MUST | ✅ found | The `unit` parameter needs to support the instrument unit rule. Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 17 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 18 | MUST NOT | ✅ found | Users can provide a `description`, but it is up to their discretion. Therefore, this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 19 | MUST | ✅ found | The `description` needs to support the instrument description rule. Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 20 | MUST NOT | ✅ found | Users can provide `advisory` parameters, but its up to their discretion. Therefore, this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 21 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:642` |  |
| 22 | MUST | ✅ found | The API to construct asynchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 23 | SHOULD | ✅ found | The `name` needs to be provided by a user. If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 24 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:215` |  |
| 25 | SHOULD | ⚠️ partial | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:218` | Метод СоздатьНаблюдаемыйСчетчик документирует Имя как Строка, но не указывает требования к синтаксису имени. |
| 26 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`, that is left to implementations of the API. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 27 | MUST NOT | ✅ found | Users can provide a `unit`, but it is up to their discretion. Therefore, this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 28 | MUST | ✅ found | The `unit` parameter needs to support the instrument unit rule. Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 29 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 30 | MUST NOT | ✅ found | Users can provide a `description`, but it is up to their discretion. Therefore, this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 31 | MUST | ✅ found | The `description` needs to support the instrument description rule. Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 32 | MUST NOT | ✅ found | Users can provide `advisory` parameters, but its up to their discretion. Therefore, this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 33 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 34 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of `callback` functions, including none. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 35 | MUST | ✅ found | The API MUST support creation of asynchronous instruments by passing zero or more `callback` functions to be permanently registered to the newly created instrument. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:130` |  |
| 36 | SHOULD | ✅ found | The API SHOULD support registration of `callback` functions associated with asynchronous instruments after they are created. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:59` |  |
| 37 | MUST | ✅ found | Where the API supports registration of `callback` functions after asynchronous instrumentation creation, the user MUST be able to undo registration of the specific callback after its registration by some means. | `src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os:13` |  |
| 38 | MUST | ✅ found | Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:140` |  |
| 39 | MUST | ⚠️ partial | Callback functions MUST be documented as follows for the end user: | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:130` | Документация callback существует в комментариях ОтелНаблюдениеМетрики, но не описывает все три рекомендации (reentrant safe, не бесконечные, не дублировать наблюдения). |
| 40 | SHOULD | ❌ not_found | Callback functions SHOULD be reentrant safe. The SDK expects to evaluate callbacks for each MetricReader independently. | - | Нет документации для пользователей о реентерабельности callback-функций. |
| 41 | SHOULD NOT | ❌ not_found | Callback functions SHOULD NOT take an indefinite amount of time. | - | Нет документации для пользователей о недопустимости бесконечного выполнения callback. |
| 42 | SHOULD NOT | ❌ not_found | Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same `attributes`) across all registered callbacks. | - | Нет документации или проверки дублирования наблюдений с одинаковыми атрибутами. |
| 43 | MUST | ✅ found | Callbacks registered at the time of instrument creation MUST apply to the single instruments which is under construction. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:135` |  |
| 44 | MUST | ✅ found | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the instrument associated with each observed `Measurement` value. | `src/Метрики/Классы/ОтелМетр.os:438` |  |
| 45 | MUST | ✅ found | Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of asynchronous instruments from the same `Meter` instance. | `src/Метрики/Классы/ОтелМетр.os:428` |  |
| 46 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:150` |  |
| 47 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:150` |  |
| 48 | SHOULD | ✅ found | The API SHOULD provide some way to pass `state` to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:130` |  |

#### General operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | SHOULD | ✅ found | All synchronous instruments SHOULD provide functions to: Report if instrument is Enabled | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 50 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when recording measurements, synchronous instruments SHOULD provide this Enabled API. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 51 | MUST | ✅ found | There are currently no required parameters for this API. Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 52 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 53 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:194` | Метод Включен() существует и документирован, но комментарий не упоминает явно, что его нужно вызывать перед каждым измерением для получения актуального состояния |

#### Counter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Counter other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 55 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example null, undefined). | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 56 | MUST | ✅ found | This API MUST accept the following parameter: A numeric increment value. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 57 | SHOULD | ✅ found | The increment value needs to be provided by a user. If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 58 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелСчетчик.os:16` |  |
| 59 | SHOULD | ✅ found | The increment value is expected to be non-negative. This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелСчетчик.os:14` |  |
| 60 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелСчетчик.os:22` |  |
| 61 | MUST | ✅ found | Users can provide attributes to associate with the increment value, but it is up to their discretion. Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 62 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 63 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Counter other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 64 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` |  |
| 65 | MUST | ✅ found | observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:184` |  |
| 66 | SHOULD | ✅ found | The API SHOULD provide some way to pass state to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:58` |  |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Histogram other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:80` |  |
| 68 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example null, undefined). | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 69 | MUST | ✅ found | This API MUST accept the following parameter: A numeric value to record. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 70 | SHOULD | ✅ found | The value needs to be provided by a user. If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 71 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелГистограмма.os:16` |  |
| 72 | SHOULD | ✅ found | The value is expected to be non-negative. This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелГистограмма.os:16` |  |
| 73 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелГистограмма.os:21` |  |
| 74 | MUST | ✅ found | Users can provide attributes to associate with the value, but it is up to their discretion. Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 75 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Gauge other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:194` |  |
| 76 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example null, undefined). | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 77 | MUST | ✅ found | This API MUST accept the following parameter: A numeric value. The current absolute value. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 78 | SHOULD | ✅ found | The value needs to be provided by a user. If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 79 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелДатчик.os:15` |  |
| 80 | MUST | ✅ found | Users can provide attributes to associate with the value, but it is up to their discretion. Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 81 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 82 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Gauge other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:308` |  |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 83 | MUST NOT | ✅ found | There MUST NOT be any API for creating an UpDownCounter other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:162` |  |
| 84 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example null, undefined). | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 85 | MUST | ✅ found | This API MUST accept the following parameter: A numeric value to add. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 86 | SHOULD | ✅ found | The value needs to be provided by a user. If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 87 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:13` |  |
| 88 | MUST | ✅ found | Users can provide attributes to associate with the value, but it is up to their discretion. Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 89 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:268` |  |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: A callback function, A list (or tuple, etc.) of Instruments used in the callback function. | `src/Метрики/Классы/ОтелМетр.os:428` |  |

#### Note the two associated instruments are passed to the callback.

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-the-two-associated-instruments-are-passed-to-the-callback)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 91 | SHOULD | ✅ found | All the metrics components SHOULD allow new APIs to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 92 | SHOULD | ✅ found | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 93 | MUST | ⚠️ partial | MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:241` | ОтелПровайдерМетрик использует СинхронизированнаяКарта для потокобезопасности, но документация класса не содержит явного указания на потокобезопасность методов |
| 94 | MUST | ⚠️ partial | Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелМетр.os:493` | ОтелМетр использует СинхронизированнаяКарта для ИнструментыПоИмени и ДескрипторыИнструментов, обеспечивая потокобезопасность, но это не задокументировано явно в комментариях класса |
| 95 | MUST | ⚠️ partial | Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:16` | ОтелБазовыйСинхронныйИнструмент использует СинхронизированнаяКарта и АтомарноеБулево для потокобезопасности, но комментарии не документируют явно, что все методы безопасны для конкурентного использования |

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
| 6 | MUST | ⚠️ partial | If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the `MeterProvider` before or after the configuration change). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:71` | Views registered after Meter creation via ЗарегистрироватьПредставление are stored at the provider level but Meters get a copy of views at creation time (line 71: Метрика.УстановитьПредставления). New views added later do not automatically propagate to already-created Meters. |
| 7 | MUST NOT | ⚠️ partial | If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the `MeterProvider` before or after the configuration change). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:71` | Same issue as above - Views are copied to Meters at creation time, so configuration changes after Meter creation may not fully propagate. MetricReaders are managed at the provider level and do apply to all Meters. |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered MetricReader instances that implement `ForceFlush`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` |  |
| 9 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` | СброситьБуфер() is a Процедура (void), does not return a status. The async variant СброситьБуферАсинхронно() returns an Обещание, but the sync method provides no success/failure indication. |
| 10 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` | СброситьБуфер() is a Процедура (void) that does not return any status - neither ERROR nor NO ERROR. Errors in individual readers are silently swallowed. |
| 11 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` | СброситьБуфер() does not accept or enforce a timeout parameter. The async variant СброситьБуферАсинхронно() returns a Promise that could be awaited with timeout externally, but the sync method itself has no timeout mechanism. |

#### View

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The SDK MUST provide functionality for a user to create Views for a `MeterProvider`. | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 13 | MUST | ✅ found | This functionality MUST accept as inputs the Instrument selection criteria and the resulting stream configuration. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:176` |  |
| 14 | MUST | ✅ found | The SDK MUST provide the means to register Views with a `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:176` |  |

#### Instrument selection criteria

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-selection-criteria)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | SHOULD | ✅ found | Criteria SHOULD be treated as additive. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:24` |  |
| 16 | MUST | ✅ found | The SDK MUST accept the following criteria: | `src/Метрики/Классы/ОтелСелекторИнструментов.os:1` |  |
| 17 | MUST | ✅ found | If the SDK does not support wildcards in general, it MUST still recognize the special single asterisk (`*`) character as matching all Instruments. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:25` |  |
| 18 | MUST NOT | ✅ found | Users can provide a `name`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:153` |  |
| 19 | MUST NOT | ✅ found | Users can provide a `type`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `type`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:153` |  |
| 20 | MUST NOT | ✅ found | Users can provide a `unit`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:153` |  |
| 21 | MUST NOT | ✅ found | Users can provide a `meter_name`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:153` |  |
| 22 | MUST NOT | ✅ found | Users can provide a `meter_version`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:153` |  |
| 23 | MUST NOT | ✅ found | Users can provide a `meter_schema_url`, but it is up to their discretion. Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:153` |  |
| 24 | MUST NOT | ✅ found | Users can provide these additional criteria the SDK accepts, but it is up to their discretion. Therefore, the instrument selection criteria can be structured to accept the criteria, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:153` |  |

#### Stream configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#stream-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | The SDK MUST accept the following stream configuration parameters: | `src/Метрики/Классы/ОтелПредставление.os:1` |  |
| 26 | SHOULD | ✅ found | `name`: The metric stream name that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:30` |  |
| 27 | SHOULD | ❌ not_found | In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector that selects at most one instrument. | - | Нет валидации при регистрации представления, что селектор с name выбирает не более одного инструмента |
| 28 | MUST NOT | ✅ found | Users can provide a `name`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:157` |  |
| 29 | MUST | ✅ found | If the user does not provide a `name` value, name from the Instrument the View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:188` |  |
| 30 | SHOULD | ✅ found | `description`: The metric stream description that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:39` |  |
| 31 | MUST NOT | ✅ found | Users can provide a `description`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:157` |  |
| 32 | MUST | ✅ found | If the user does not provide a `description` value, the description from the Instrument a View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:192` |  |
| 33 | MUST | ✅ found | `attribute_keys`: This is, at a minimum, an allow-list of attribute keys for measurements captured in the metric stream. The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:237` |  |
| 34 | MUST | ✅ found | `attribute_keys`: This is, at a minimum, an allow-list of attribute keys for measurements captured in the metric stream. The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:237` |  |
| 35 | MUST NOT | ✅ found | Users can provide `attribute_keys`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept `attribute_keys`, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелПредставление.os:157` |  |
| 36 | SHOULD | ✅ found | If the user does not provide any value, the SDK SHOULD use the `Attributes` advisory parameter configured on the instrument instead. | `src/Метрики/Классы/ОтелМетр.os:524` |  |
| 37 | MUST | ✅ found | If the `Attributes` advisory parameter is absent, all attributes MUST be kept. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:95` |  |
| 38 | SHOULD | ✅ found | Additionally, implementations SHOULD support configuring an exclude-list of attribute keys. | `src/Метрики/Классы/ОтелПредставление.os:57` |  |
| 39 | MUST | ⚠️ partial | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелПредставление.os:57` | ОтелПредставление хранит ИсключенныеКлючиАтрибутов, но ОтелБазовыйСинхронныйИнструмент не обрабатывает exclude-list - фильтрация атрибутов использует только allow-list (РазрешенныеКлючиАтрибутов) |
| 40 | MUST | ⚠️ partial | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелПредставление.os:57` | Exclude-list сохраняется в ОтелПредставление, но не применяется при фильтрации в ОтелБазовыйСинхронныйИнструмент |
| 41 | MUST NOT | ✅ found | Users can provide an `aggregation`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept an `aggregation`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:157` |  |
| 42 | MUST | ✅ found | If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance. | `src/Метрики/Классы/ОтелМетр.os:50` |  |
| 43 | MUST NOT | ✅ found | Users can provide an `exemplar_reservoir`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept an `exemplar_reservoir`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:157` |  |
| 44 | MUST | ✅ found | If the user does not provide an `exemplar_reservoir` value, the `MeterProvider` MUST apply a default exemplar reservoir. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:267` |  |
| 45 | MUST NOT | ✅ found | Users can provide an `aggregation_cardinality_limit`, but it is up to their discretion. Therefore, the stream configuration parameter needs to be structured to accept an `aggregation_cardinality_limit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:157` |  |
| 46 | MUST | ⚠️ partial | If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST apply the default aggregation cardinality limit the `MetricReader` is configured with. | `src/Метрики/Классы/ОтелМетр.os:500` | Лимит мощности по умолчанию 2000 задаётся в ОтелМетр, а не берётся из конфигурации MetricReader |

#### Measurement processing

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#measurement-processing)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | SHOULD | ✅ found | The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument: | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:162` |  |
| 48 | MUST | ⚠️ partial | Instrument advisory parameters, if any, MUST be honored. | `src/Метрики/Классы/ОтелМетр.os:512` | Advisory-параметры (ГраницыГистограммы, КлючиАтрибутов) учитываются при создании инструмента, но только когда нет View; спецификация требует их применения и в случае отсутствия View |
| 49 | SHOULD | ⚠️ partial | If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning. | - | Представления применяются независимо в ОтелПериодическийЧитательМетрик.ПрименитьПредставление, но нет проверки конфликтов метрических идентичностей и нет предупреждения |
| 50 | SHOULD | ⚠️ partial | If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asynchronous instrument to use the Explicit bucket histogram aggregation) the implementation SHOULD emit a warning and proceed as if the View did not exist. | - | Нет проверки семантических ошибок при применении View (например, задание гистограммной агрегации для асинхронного инструмента) |
| 51 | MUST | ✅ found | If both a View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:519` |  |
| 52 | SHOULD | ⚠️ partial | If the Instrument could not match with any of the registered `View`(s), the SDK SHOULD enable the instrument using the default aggregation and temporality. | `src/Метрики/Классы/ОтелМетр.os:50` | Инструменты создаются с агрегацией по умолчанию, но если ни одно View не совпало, инструмент всё равно работает - поведение корректно. Однако временность не конфигурируется отдельно для этого случая. |

#### conflicting metric identities)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#conflicting-metric-identities)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 53 | MUST | ✅ found | The SDK MUST provide the following `Aggregation` to support the Metric Points in the Metrics Data Model. | `src/Метрики/Модули/ОтелАгрегация.os:1` |  |
| 54 | SHOULD | ✅ found | The SDK SHOULD provide the following `Aggregation`: Base2 Exponential Bucket Histogram | `src/Метрики/Модули/ОтелАгрегация.os:83` |  |

#### Sum Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#sum-aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD NOT | ❌ not_found | This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpDownCounter` or `ObservableGauge`). | - | Агрегатор гистограммы всегда собирает sum, нет логики пропуска sum для инструментов с отрицательными измерениями (UpDownCounter, ObservableGauge) |
| 56 | SHOULD | ✅ found | SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different (e.g. for backward compatibility reasons in a stable SDK release). | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:120` |  |
| 57 | SHOULD NOT | ❌ not_found | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`, `min`, and `max` fields, because these values do not map into a valid bucket. | - | Экспоненциальная гистограмма не имеет защиты от non-normal values (Inf, NaN) - OneScript не имеет нативных Inf/NaN, но нет явной проверки |
| 58 | MUST | ✅ found | The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic scale parameter will not exceed. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:227` |  |
| 59 | SHOULD | ✅ found | When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:42` |  |
| 60 | SHOULD | ✅ found | Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possible, within the constraint of maximum size (max number of buckets). | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:143` |  |

#### Observations inside asynchronous callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#observations-inside-asynchronous-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | MUST | ⚠️ partial | Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that observations made or produced by executing callbacks only apply to the intended `MetricReader` during collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:106` | Callbacks вызываются в ОтелПериодическийЧитательМетрик.СобратьИЭкспортировать через Метр.ВызватьМультиОбратныеВызовы(), но наблюдения не изолированы по конкретному MetricReader - они общие для всех reader'ов |
| 62 | SHOULD | ❌ not_found | The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks. | - | Нет механизма предотвращения использования API асинхронных инструментов вне зарегистрированных callback-ов |
| 63 | SHOULD | ❌ not_found | The implementation SHOULD use a timeout to prevent indefinite callback execution. | - | Нет таймаута при вызове callback-ов в ОтелБазовыйНаблюдаемыйИнструмент.ВызватьCallbackИСобрать() |
| 64 | MUST | ✅ found | The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:106` |  |
| 65 | SHOULD NOT | ❌ not_found | The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback. | - | В ОтелБазовыйНаблюдаемыйИнструмент данные формируются из записей callback-а и внешних наблюдений. Метод ОчиститьТочкиДанных() сбрасывает ВнешниеНаблюдения, но нет механизма удаления старых attribute set-ов, которые не были наблюдены в текущем callback |

#### Cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | SHOULD | ✅ found | SDKs SHOULD support being configured with a cardinality limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:152` |  |
| 67 | SHOULD | ✅ found | Cardinality limit enforcement SHOULD occur after attribute filtering, if any. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:95` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardinality_limit` value defined for the stream, that value SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:92` |  |
| 69 | SHOULD | ❌ not_found | If there is no matching view, but the `MetricReader` defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | - | MetricReader (ОтелПериодическийЧитательМетрик) не имеет метода для задания default cardinality limit per instrument. Лимит задаётся только на уровне Meter или View. |
| 70 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` |  |
| 71 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:325` |  |
| 72 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:92` |  |

#### Synchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#synchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | MUST | ⚠️ partial | Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138` | Кумулятивная временность сохраняет аккумуляторы (не очищает в ОчиститьТочкиДанных при Кумулятивная=Истина), но специальной логики для разделения pre-overflow и post-overflow attribute sets нет - все аккумуляторы экспортируются одинаково. |
| 74 | MUST | ✅ found | Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in exactly one Aggregator, which is either an Aggregator associated with the correct attribute set or an aggregator associated with the overflow attribute set. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:88` |  |
| 75 | MUST NOT | ✅ found | Measurements MUST NOT be double-counted or dropped during an overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:88` |  |

#### Asynchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#asynchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 76 | SHOULD | ❌ not_found | Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality. | - | ОтелБазовыйНаблюдаемыйИнструмент не имеет механизма cardinality limiting - все наблюдения из callback и внешних наблюдений конвертируются в точки данных без ограничения количества атрибутных наборов. |

#### Duplicate instrument registration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#duplicate-instrument-registration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 77 | MUST | ✅ found | This means that the Meter MUST return a functional instrument that can be expected to export data even if this will cause semantic error in the data model. | `src/Метрики/Классы/ОтелМетр.os:52` |  |
| 78 | SHOULD | ✅ found | Therefore, when a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted. | `src/Метрики/Классы/ОтелМетр.os:573` |  |
| 79 | SHOULD | ⚠️ partial | The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible. | `src/Метрики/Классы/ОтелМетр.os:573` | Предупреждение содержит информацию о конфликте (вид инструмента и единица измерения), но не включает рекомендации по разрешению конфликта (например, использование View). |
| 80 | SHOULD | ❌ not_found | If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning. | - | ПроверитьКонфликтДескриптора всегда сравнивает описания и выдаёт предупреждение при различии - нет проверки, настроено ли описание через View для подавления предупреждения. |
| 81 | SHOULD | ❌ not_found | If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning. | - | Предупреждение при конфликте дескриптора не включает рецепт View для переименования - сообщение содержит только параметры конфликтующих инструментов. |
| 82 | SHOULD | ⚠️ partial | Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument registration. | `src/Метрики/Классы/ОтелМетр.os:52` | При дублировании SDK возвращает первый зарегистрированный инструмент (а не оба) и выдаёт предупреждение. Данные второго инструмента агрегируются в первый, но отдельного объекта Metric не создаётся. |
| 83 | MUST | ✅ found | the SDK MUST aggregate data from identical Instruments together in its export pipeline. | `src/Метрики/Классы/ОтелМетр.os:52` |  |

#### Name conflict

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#name-conflict)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 84 | MUST | ✅ found | When this happens, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above. | `src/Метрики/Классы/ОтелМетр.os:49` |  |

#### Instrument name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 85 | SHOULD | ❌ not_found | When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax | - | ОтелМетр при создании инструментов (СоздатьСчетчик, СоздатьГистограмму и т.д.) не выполняет валидацию имени на соответствие синтаксису instrument name из спецификации. |
| 86 | SHOULD | ❌ not_found | If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name. | - | Нет проверки имени инструмента при создании - невалидные имена принимаются без предупреждения. |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 87 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 88 | MUST | ✅ found | If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit string. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument description. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 90 | MUST | ✅ found | If a description is not provided or the description is null, the Meter MUST treat it the same as an empty description string. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 91 | SHOULD | ✅ found | When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:642` |  |
| 92 | SHOULD | ✅ found | If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided. | `src/Метрики/Классы/ОтелМетр.os:648` |  |
| 93 | MUST | ✅ found | If multiple identical Instruments are created with different advisory parameters, the Meter MUST return an instrument using the first-seen advisory parameters and log an appropriate error as described in duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:562` |  |
| 94 | MUST | ✅ found | If both a View and advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:515` |  |

#### Instrument advisory parameter: `ExplicitBucketBoundaries`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameter-explicitbucketboundaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 95 | MUST | ✅ found | If no View matches, or if a matching View selects the default aggregation, the `ExplicitBucketBoundaries` advisory parameter MUST be used. | `src/Метрики/Классы/ОтелМетр.os:539` |  |

#### Exemplar

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | MUST | ✅ found | A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements via the `ExemplarFilter` and `ExemplarReservoir` hooks. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14` |  |
| 97 | SHOULD | ⚠️ partial | `Exemplar` sampling SHOULD be turned on by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:264` | Default filter is ПоТрассировке (TraceBased), which only samples when there is an active sampled span. The spec says sampling SHOULD be on by default - TraceBased is the recommended default per spec, so this is acceptable, but it means exemplars are only captured when tracing is active. |
| 98 | MUST NOT | ✅ found | If `Exemplar` sampling is off, the SDK MUST NOT have overhead related to exemplar sampling. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:335` |  |
| 99 | MUST | ✅ found | A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation. | `src/Метрики/Классы/ОтелМетр.os:99` |  |
| 100 | SHOULD | ✅ found | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: `ExemplarFilter`: filter which measurements can become exemplars. `ExemplarReservoir`: storage and sampling of exemplars. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 101 | MUST | ✅ found | The `ExemplarFilter` configuration MUST allow users to select between one of the built-in ExemplarFilters. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 102 | SHOULD | ✅ found | The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for an SDK. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 103 | SHOULD | ⚠️ partial | The default value SHOULD be `TraceBased`. | `src/Метрики/Классы/ОтелМетр.os:496` | The default is ПоТрассировке (TraceBased) at the Meter level, but the ОтелПостроительПровайдераМетрик does not explicitly set TraceBased as default in the builder - it only sets the filter from environment variable. The Meter defaults to TraceBased in its constructor. |
| 104 | SHOULD | ✅ found | The filter configuration SHOULD follow the environment variable specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:110` |  |
| 105 | MUST | ✅ found | An OpenTelemetry SDK MUST support the following filters: AlwaysOn, AlwaysOff, TraceBased. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14` |  |

#### ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 106 | MUST | ✅ found | The `ExemplarReservoir` interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 107 | MUST | ✅ found | A new `ExemplarReservoir` MUST be created for every known timeseries data point, as determined by aggregation and view configuration. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |
| 108 | SHOULD | ✅ found | The "offer" method SHOULD accept measurements, including: The `value` of the measurement. The complete set of `Attributes` of the measurement. The Context of the measurement, which covers the Baggage and the current active Span. A `timestamp` that best represents when the measurement was taken. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 109 | SHOULD | ✅ found | The "offer" method SHOULD have the ability to pull associated trace and span information without needing to record full context. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:112` |  |
| 110 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the "offer" method. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 111 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the "offer" method. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 112 | MUST | ✅ found | The "collect" method MUST return accumulated `Exemplar`s. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:55` |  |
| 113 | SHOULD | ✅ found | Exemplars are expected to abide by the `AggregationTemporality` of any metric point they are recorded with. In other words, Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:139` |  |
| 114 | MUST | ✅ found | `Exemplar`s MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:130` |  |
| 115 | SHOULD | ⚠️ partial | The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:42` | The reservoir creates a new Соответствие (Map) for each exemplar in СоздатьЭкземпляр, which allocates on every offer call. OneScript's GC-based model makes zero-allocation difficult, but the implementation does not pre-allocate exemplar objects. |

#### Exemplar defaults

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar-defaults)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 116 | MUST | ✅ found | The SDK MUST include two types of built-in exemplar reservoirs: `SimpleFixedSizeExemplarReservoir` `AlignedHistogramBucketExemplarReservoir` | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1` |  |
| 117 | SHOULD | ✅ found | Explicit bucket histogram aggregation with more than 1 bucket SHOULD use `AlignedHistogramBucketExemplarReservoir`. | `src/Метрики/Классы/ОтелМетр.os:99` |  |
| 118 | SHOULD | ✅ found | Base2 Exponential Histogram Aggregation SHOULD use a `SimpleFixedSizeExemplarReservoir` with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty (e.g. `min(20, max_buckets)`). | `src/Метрики/Классы/ОтелМетр.os:137` |  |
| 119 | SHOULD | ✅ found | All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |

#### SimpleFixedSizeExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#simplefixedsizeexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 120 | MUST | ✅ found | This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the reservoir has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:88` |  |
| 121 | SHOULD | ✅ found | Any stateful portion of sampling computation SHOULD be reset every collection cycle. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:139` |  |
| 122 | SHOULD | ✅ found | Otherwise, a default size of `1` SHOULD be used. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:148` |  |

#### AlignedHistogramBucketExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#alignedhistogrambucketexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 123 | MUST | ✅ found | This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:149` |  |
| 124 | MUST | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:55` |  |
| 125 | SHOULD | ⚠️ partial | This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:55` | Реализация хранит последнее измерение в каждом бакете (MAY alternative), а не использует reservoir sampling с равномерной вероятностью. Спецификация допускает это как альтернативу ('MAY instead keep the last seen measurement'), но SHOULD указывает на предпочтительность reservoir sampling. |
| 126 | SHOULD | ✅ found | This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:149` |  |

#### Custom ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#custom-exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 127 | MUST | ✅ found | The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation. | `src/Метрики/Классы/ОтелПредставление.os:89` |  |
| 128 | MUST | ✅ found | This extension MUST be configurable on a metric View, although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reservoir - Paragraph 2). | `src/Метрики/Классы/ОтелПредставление.os:89` |  |
| 129 | MUST | ✅ found | This extension MUST be configurable on a metric View, although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reservoir - Paragraph 2). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:139` |  |

#### MetricReader operations#### Collect

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader-operations-collect)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 130 | SHOULD | ✅ found | `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:130` |  |
| 131 | SHOULD | ❌ not_found | `Collect` SHOULD invoke Produce on registered MetricProducers. | - | Нет поддержки внешних MetricProducer. ОтелПериодическийЧитательМетрик собирает данные только из зарегистрированных ОтелМетр, но не поддерживает регистрацию и вызов Produce на внешних MetricProducer. |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 132 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MetricReader` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:93` |  |
| 133 | SHOULD | ⚠️ partial | After the call to `Shutdown`, subsequent invocations to `Collect` are not allowed. SDKs SHOULD return some failure for these calls, if possible. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:93` | Метод Закрыть() устанавливает флаг Закрыт через АтомарноеБулево и предотвращает повторный вызов через СравнитьИУстановить, но метод СобратьИЭкспортировать (аналог Collect) не проверяет флаг Закрыт и не возвращает ошибку после Shutdown. |
| 134 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:93` |  |
| 135 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:100` |  |

#### Periodic exporting MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 136 | MUST | ✅ found | The reader MUST synchronize calls to `MetricExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:127` |  |
| 137 | SHOULD | ✅ found | `ForceFlush` SHOULD collect metrics, call `Export(batch)` and `ForceFlush()` on the configured Push Metric Exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:74` |  |
| 138 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:74` |  |
| 139 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:74` | Метод СброситьБуфер() вызывает СобратьИЭкспортировать() но не возвращает статус (SUCCESS/ERROR). Процедура выполняется без возвращаемого значения. |
| 140 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:74` |  |

#### MetricExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 141 | MUST | ✅ found | `MetricExporter` defines the interface that protocol-specific exporters MUST implement so that they can be plugged into OpenTelemetry SDK and support sending of telemetry data. | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1` |  |
| 142 | SHOULD | ✅ found | Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsupported Aggregation or Aggregation Temporality, as this condition can be corrected by a change of `MetricReader` configuration. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:27` |  |
| 143 | MUST | ✅ found | A Push Metric Exporter MUST support the following functions: | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:11` |  |
| 144 | MUST | ✅ found | The SDK MUST provide a way for the exporter to get the Meter information (e.g. name, version, etc.) associated with each `Metric Point`. | `src/Метрики/Классы/ОтелДанныеМетрики.os:42` |  |
| 145 | MUST NOT | ⚠️ partial | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:27` | Метод Экспортировать() вызывает Транспорт.Отправить() синхронно. Таймаут зависит от настроек транспорта (HTTP), но экспортер сам не устанавливает явный верхний предел таймаута. |
| 146 | MUST | ⚠️ partial | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:27` | Экспортер не устанавливает собственный таймаут, полагаясь на настройки транспорта. Нет явного error result (Failure) при таймауте - метод возвращает Булево. |
| 147 | SHOULD NOT | ✅ found | The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the metrics are being sent to. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:27` |  |
| 148 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Metrics` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:48` |  |
| 149 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:48` | Метод СброситьБуфер() реализован как Процедура без возвращаемого значения, не информирует вызывающую сторону о результате. |
| 150 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed metrics. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:48` |  |
| 151 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:48` | Метод СброситьБуфер() не имеет параметра таймаута и не прерывается по времени. |
| 152 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each `MetricExporter` instance. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:53` |  |
| 153 | SHOULD NOT | ⚠️ partial | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:53` | Метод Закрыть() просто устанавливает флаг Закрыт = Истина, что не блокируется. Однако нет явного таймаута если бы Закрыть включал flush данных. |

#### Pull Metric Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#pull-metric-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 154 | MUST | ✅ found | `MetricProducer` defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:44` |  |
| 155 | SHOULD | ❌ not_found | `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of produced metrics. | - | Нет отдельного интерфейса MetricProducer с конфигурацией AggregationTemporality. ОтелПрометеусЧитательМетрик - это pull MetricReader, а не MetricProducer. MetricProducer как отдельная сущность (мост к сторонним источникам метрик) не реализован. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 156 | MUST | ❌ not_found | A `MetricProducer` MUST support the following functions: | - | Отдельный интерфейс/класс MetricProducer не реализован. Функциональность сбора метрик встроена в MetricReader (ОтелПериодическийЧитательМетрик и ОтелПрометеусЧитательМетрик), но не выделена в отдельную сущность MetricProducer. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 157 | MUST | ✅ found | A `MetricFilter` MUST support the following functions: | `src/Метрики/Классы/ОтелФильтрМетрик.os:30` |  |

#### TestMetric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#testmetric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 158 | MUST | ✅ found | The SDK MUST provide configuration according to the SDK environment variables specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:3` |  |

#### Numerical limits handling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#numerical-limits-handling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 159 | MUST | ❌ not_found | The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry. | - | В коде метрик нет явной обработки числовых пределов (NaN, Infinity, переполнение). Значения принимаются и записываются как есть без валидации. |
| 160 | MUST | ❌ not_found | If the SDK receives float/double values from Instruments, it MUST handle all the possible values. | - | Нет специальной обработки NaN, Infinity или других предельных значений float/double. OneScript использует Число, который обрабатывает числа через .NET runtime, но явная обработка по спецификации отсутствует. |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 161 | SHOULD | ✅ found | All the metrics components SHOULD allow new methods to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:1` |  |
| 162 | SHOULD | ✅ found | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to existing methods without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:48` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 163 | MUST | ⚠️ partial | MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:241` | Метрики хранятся в СинхронизированнаяКарта (thread-safe), создание метров безопасно. Однако СброситьБуфер() и Закрыть() не используют блокировку - они напрямую вызывают методы читателей без синхронизации на уровне провайдера. |
| 164 | MUST | ✅ found | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:10` |  |
| 165 | MUST | ✅ found | MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:13` |  |
| 166 | MUST | ⚠️ partial | MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:3` | В коде есть комментарий о потокобезопасности ("Export и Shutdown/ForceFlush могут вызываться конкурентно. Реализация MUST быть безопасна"), но фактически Закрыть() использует простое присваивание Закрыт = Истина без атомарной операции или блокировки. |

### Otlp Exporter

#### Configuration Options

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#configuration-options)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | The following configuration options MUST be available to configure the OTLP exporter. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130` | Endpoint, Protocol, Headers, Compression, Timeout доступны. Certificate File, Client key file, Client certificate file (TLS/mTLS) отсутствуют. Insecure не реализован (spec допускает MAY не реализовывать). |
| 2 | MUST | ❌ not_found | Each configuration option MUST be overridable by a signal specific option. | - | Только общие ключи otel.exporter.otlp.* читаются в СоздатьТранспорт(). Посигнальные переопределения (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_LOGS_PROTOCOL и т.д.) не реализованы. |
| 3 | MUST | ✅ found | The implementation MUST honor the following URL components: | `src/Экспорт/Классы/ОтелHttpТранспорт.os:161` |  |
| 4 | MUST | ✅ found | When using `OTEL_EXPORTER_OTLP_ENDPOINT`, exporters MUST construct per-signal URLs as described below. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:35` |  |
| 5 | SHOULD | ✅ found | The option SHOULD accept any form allowed by the underlying gRPC client implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:147` |  |
| 6 | MUST | ✅ found | Additionally, the option MUST accept a URL with a scheme of either `http` or `https`. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:147` |  |
| 7 | SHOULD | ✅ found | If the gRPC client implementation does not support an endpoint with a scheme of `http` or `https` then the endpoint SHOULD be transformed to the most sensible format for that implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:174` |  |
| 8 | MUST | ⚠️ partial | Options MUST be one of: `grpc`, `http/protobuf`, `http/json`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | grpc и http/json поддерживаются. http/protobuf указан в комментарии как поддерживаемый, но фактически при установке http/protobuf создаётся ОтелHttpТранспорт, который отправляет JSON (Content-Type: application/json), а не protobuf. |
| 9 | SHOULD | ✅ found | SDKs SHOULD default endpoint variables to use `http` scheme unless they have good reasons to choose `https` scheme for the default (e.g., for backward compatibility reasons in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:153` |  |
| 10 | SHOULD | ❌ not_found | However, if they are already implemented, they SHOULD continue to be supported as they were part of a stable release of the specification. | - | Опция Insecure никогда не была реализована в данном SDK. Устаревшие переменные OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE также не поддерживаются. |
| 11 | SHOULD | ⚠️ partial | The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default (e.g. for backward compatibility reasons when `grpc` was already the default in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Протокол по умолчанию - http/json, а не http/protobuf как рекомендует спецификация. |
| 12 | MUST | ✅ found | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal as follow: | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:35` |  |
| 13 | MUST | ❌ not_found | For the per-signal variables (`OTEL_EXPORTER_OTLP_<signal>_ENDPOINT`), the URL MUST be used as-is without any modification. | - | Посигнальные переменные OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_LOGS_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_ENDPOINT не реализованы. |
| 14 | MUST | ❌ not_found | The only exception is that if an URL contains no path part, the root path `/` MUST be used (see Example 2). | - | Посигнальные переменные endpoint не реализованы, поэтому логика обработки URL без пути отсутствует. |
| 15 | MUST NOT | ✅ found | An SDK MUST NOT modify the URL in ways other than specified above. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:99` |  |

#### Specify Protocol

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specify-protocol)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ⚠️ partial | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | grpc поддерживается (ОтелGrpcТранспорт), но http/protobuf не реализован - вместо него используется http/json (ОтелHttpТранспорт с Content-Type: application/json). |
| 17 | MUST | ✅ found | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:152` |  |
| 18 | SHOULD | ⚠️ partial | If they support only one, it SHOULD be `http/protobuf`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | SDK поддерживает два транспорта (grpc и http/json), но ни один из них не является http/protobuf. |
| 19 | SHOULD | ⚠️ partial | If no configuration is provided the default transport SHOULD be `http/protobuf` unless SDKs have good reasons to choose `grpc` as the default (e.g. for backward compatibility reasons when `grpc` was already the default in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Транспорт по умолчанию - http/json, а не http/protobuf как рекомендует спецификация. |

#### Specifying headers via environment variables

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:467` |  |

#### Retry

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#retry)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | Transient errors MUST be handled with a retry strategy. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:166` |  |
| 22 | MUST | ✅ found | This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:166` |  |

#### Transient errors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#transient-errors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | SHOULD | ❌ not_found | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter. | - | Заголовок User-Agent не устанавливается ни в ОтелHttpТранспорт, ни в ОтелGrpcТранспорт. |
| 24 | SHOULD | ❌ not_found | The format of the header SHOULD follow RFC 7231. | - | Заголовок User-Agent не реализован, поэтому формат RFC 7231 также не соблюдается. |
| 25 | SHOULD | ❌ not_found | The resulting User-Agent SHOULD include the exporter's default User-Agent string. | - | Заголовок User-Agent не реализован. |

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
| 4 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any previously existing valid value. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:81` |  |
| 5 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any previously existing valid value. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:90` |  |

#### TextMap Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | In order to increase compatibility, the key/value pairs MUST only consist of US-ASCII characters that make up valid HTTP header fields as per RFC 9110. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:62` |  |
| 7 | MUST | ✅ found | `Getter` and `Setter` MUST be stateless and allowed to be saved as constants, in order to effectively avoid runtime allocations. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:72` |  |

#### TextMap Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-inject)

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
| 14 | SHOULD | ✅ found | It SHOULD return them in the same order as they appear in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:43` |  |
| 15 | SHOULD | ✅ found | If the key doesn't exist, it SHOULD return an empty collection. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:41` |  |
| 16 | MUST | ✅ found | The `GetAll` function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:42` |  |

#### Composite Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | Implementations MUST offer a facility to group multiple `Propagator`s from different cross-cutting concerns in order to leverage them as a single entity. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:79` |  |
| 18 | MUST | ✅ found | There MUST be functions to accomplish the following operations. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:18` |  |

#### Composite Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | The OpenTelemetry API MUST provide a way to obtain a propagator for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |
| 20 | SHOULD | ✅ found | Instrumentation libraries SHOULD call propagators to extract and inject the context on all remote calls. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |
| 21 | MUST | ✅ found | The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise. | `src/Ядро/Модули/ОтелГлобальный.os:132` |  |
| 22 | SHOULD | ❌ not_found | If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace Context Propagator and the Baggage `Propagator` specified in the Baggage API. | - | Платформа OneScript не имеет предварительно сконфигурированных пропагаторов. По умолчанию возвращается ОтелНоопПропагатор, а не композитный пропагатор с W3C TraceContext и Baggage. |
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
| 26 | MUST | ⚠️ partial | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry extension packages: | `src/Пропагация/Классы/` | W3C TraceContext и W3C Baggage пропагаторы реализованы, но B3 пропагатор отсутствует в SDK. |
| 27 | MUST | ⚠️ partial | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry extension packages: | `src/Пропагация/Классы/` | W3C TraceContext и W3C Baggage распространяются как часть API (допускается спецификацией через MAY), но B3 пропагатор не доступен как отдельный пакет расширения. |
| 28 | MUST NOT | ✅ found | It MUST NOT use `OpenTracing` in the resulting propagator name as it is not widely adopted format in the OpenTracing ecosystem. | `src/Пропагация/Классы/` |  |
| 29 | MUST NOT | ✅ found | Additional `Propagator`s implementing vendor-specific protocols such as AWS X-Ray trace header protocol MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | `src/Пропагация/Классы/` |  |

#### W3C Trace Context Requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#w3c-trace-context-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP headers as specified in W3C Trace Context Level 2. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:81` |  |
| 31 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid `traceparent` value using the same header. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:63` |  |
| 32 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid `tracestate` unless the value is empty, in which case the `tracestate` header may be omitted. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:65` |  |

### Env Vars

#### Environment Variable Specification

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#environment-variable-specification)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If they do, they SHOULD use the names and value parsing behavior specified in this document. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:6` |  |
| 2 | SHOULD | ⚠️ partial | They SHOULD also follow the common configuration specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:80` | Реализация использует configor для чтения переменных окружения, но полная общая спецификация конфигурации (common configuration specification) не реализована - отсутствует поддержка OTEL_CONFIG_FILE, нет иерархии переопределения конфигураций из разных источников. |

#### Implementation guidelines

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#implementation-guidelines)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The environment-based configuration MUST have a direct code configuration equivalent. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:59` |  |

#### Parsing empty value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#parsing-empty-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ⚠️ partial | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105` | Пустые значения обрабатываются в некоторых местах (строки 105, 137, 339: проверка '<> ""'), но не во всех. Например, otel.traces.exporter (строка 177), otel.traces.sampler (строка 190) и числовые параметры (строки 224-227) не проверяют пустые значения - пустая строка будет обработана как значение, а не как отсутствие переменной. |

#### Type-specific guidance### Boolean

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#type-specific-guidance-boolean)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Any value that represents a Boolean MUST be set to true only by the case-insensitive string "true", meaning "True" or "TRUE" are also accepted, as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 6 | MUST NOT | ✅ found | An implementation MUST NOT extend this definition and define additional values that are interpreted as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 7 | MUST | ✅ found | Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 8 | SHOULD | ❌ not_found | If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied. | - | Функция Включено() (строка 561) не логирует предупреждение при получении невалидного булевого значения (например, "yes", "1"). Значение просто интерпретируется как false без уведомления пользователя. |
| 9 | SHOULD | ⚠️ partial | All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562` | Используется переменная otel.enabled (из OTEL_ENABLED) вместо стандартной OTEL_SDK_DISABLED. При false SDK отключается, что противоречит конвенции 'false = безопасное значение по умолчанию' (безопасное - SDK включен). |
| 10 | MUST NOT | ✅ found | Renaming or changing the default value MUST NOT happen without a major version upgrade. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562` |  |

#### Numeric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#numeric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ⚠️ partial | The following paragraph was added after stabilization and the requirements are thus qualified as "SHOULD" to allow implementations to avoid breaking changes. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:224` | Реализация парсит числовые значения через Число(), но не генерирует предупреждений при невалидных значениях и не обрабатывает их gracefully (выбрасывает исключение вместо возврата к значению по умолчанию). |
| 12 | MUST | ❌ not_found | For new implementations, these should be treated as MUST requirements. | - | Требование обязывает новые реализации трактовать SHOULD-требования о числовом парсинге как MUST. Реализация не генерирует предупреждений и не игнорирует невалидные числовые значения gracefully - вызов Число() с невалидным значением приведет к исключению. |
| 13 | SHOULD | ❌ not_found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them as not set. | - | Числовые значения (otel.bsp.max.queue.size, otel.bsp.schedule.delay и др.) конвертируются через Число() без обработки ошибок. Невалидное значение вызовет исключение вместо предупреждения и возврата к значению по умолчанию. |

#### String

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#string)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | SHOULD | ⚠️ partial | Enum values SHOULD be interpreted in a case-insensitive manner. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:342` | Пропагаторы обрабатываются case-insensitive (строка 342: НРег(СтрокаПропагаторов)), но семплеры сравниваются case-sensitive (строки 196-215: прямое сравнение ИмяСэмплера = "always_on"). Экспортеры (otel.traces.exporter и др.) также сравниваются case-sensitive. |
| 15 | MUST | ⚠️ partial | For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:373` | Для пропагаторов реализовано предупреждение (строка 373: Сообщить("неизвестный пропагатор")). Но для семплеров неизвестное значение молча заменяется на parentbased_always_on без предупреждения (строка 216). Для экспортеров неизвестное значение не обрабатывается. |

#### General SDK ConfigurationNameDescriptionDefaultTypeNotesOTEL_SDK_DISABLEDDisable the SDK for all signalsfalseBooleanIf “true”, a no-op SDK implementation will be used for all telemetry signals. Any other value or absence of the variable will have no effect and the SDK will remain enabled. This setting has no effect on propagators configured through the OTEL_PROPAGATORS variable.OTEL_ENTITIESEntity information to be associated with the resourceStringSee Entities SDK for more details.OTEL_RESOURCE_ATTRIBUTESKey-value pairs to be used as resource attributesSee Resource semantic conventions for details.StringSee Resource SDK for more details.OTEL_SERVICE_NAMESets the value of the `service.name` resource attributeStringIf `service.name` is also provided in `OTEL_RESOURCE_ATTRIBUTES`, then `OTEL_SERVICE_NAME` takes precedence.OTEL_LOG_LEVELLog level used by the SDK internal logger“info”EnumOTEL_PROPAGATORSPropagators to be used as a comma-separated list“tracecontext,baggage”EnumValues MUST be deduplicated in order to register a `Propagator` only once.OTEL_TRACES_SAMPLERSampler to be used for traces“parentbased_always_on”EnumSee SamplingOTEL_TRACES_SAMPLER_ARGValue to be used as the sampler argumentSee footnoteThe specified value will only be used if OTEL_TRACES_SAMPLER is set. Each Sampler type defines its own expected input, if any. Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set.

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configurationnamedescriptiondefaulttypenotesotelsdkdisableddisable-the-sdk-for-all-signalsfalsebooleanif-true-a-no-op-sdk-implementation-will-be-used-for-all-telemetry-signals-any-other-value-or-absence-of-the-variable-will-have-no-effect-and-the-sdk-will-remain-enabled-this-setting-has-no-effect-on-propagators-configured-through-the-otelpropagators-variableotelentitiesentity-information-to-be-associated-with-the-resourcestringsee-entities-sdk-for-more-detailsotelresourceattributeskey-value-pairs-to-be-used-as-resource-attributessee-resource-semantic-conventions-for-detailsstringsee-resource-sdk-for-more-detailsotelservicenamesets-the-value-of-the-servicename-resource-attributestringif-servicename-is-also-provided-in-otelresourceattributes-then-otelservicename-takes-precedenceotelloglevellog-level-used-by-the-sdk-internal-loggerinfoenumotelpropagatorspropagators-to-be-used-as-a-comma-separated-listtracecontextbaggageenumvalues-must-be-deduplicated-in-order-to-register-a-propagator-only-onceoteltracessamplersampler-to-be-used-for-tracesparentbasedalwaysonenumsee-samplingoteltracessamplerargvalue-to-be-used-as-the-sampler-argumentsee-footnotethe-specified-value-will-only-be-used-if-oteltracessampler-is-set-each-sampler-type-defines-its-own-expected-input-if-any-invalid-or-unrecognized-input-must-be-logged-and-must-be-otherwise-ignored-ie-the-implementation-must-behave-as-if-oteltracessamplerarg-is-not-set)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ❌ not_found | Values MUST be deduplicated in order to register a Propagator only once. | - | В функции СоздатьПропагаторы() (строка 336) нет логики дедупликации. Если пользователь укажет OTEL_PROPAGATORS="tracecontext,tracecontext", оба экземпляра ОтелW3CПропагатор будут созданы и добавлены в МассивПропагаторов. |
| 17 | MUST | ❌ not_found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | - | В функции СоздатьПровайдерТрассировки() (строка 172) невалидное значение OTEL_TRACES_SAMPLER_ARG (например, нечисловая строка) передается в Число() без try/catch, что вызовет исключение вместо логирования предупреждения. |
| 18 | MUST | ❌ not_found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | - | Невалидный ввод OTEL_TRACES_SAMPLER_ARG не игнорируется gracefully - вызов Число(АргументСэмплера) на строках 204, 215 приведет к исключению вместо возврата к поведению по умолчанию. |
| 19 | MUST | ❌ not_found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | - | При невалидном OTEL_TRACES_SAMPLER_ARG реализация не переходит к поведению 'как если бы переменная не установлена' (значение по умолчанию 1.0) - вместо этого выбрасывается исключение при конвертации строки в число. |
| 20 | SHOULD | ✅ found | Implementations SHOULD only offer environment variables for the types of attributes, for which that SDK implements truncation mechanism. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:391` |  |

## Требования Development-статуса

Эти требования находятся в секциях со статусом Development. Их реализация не обязательна для соответствия стабильной спецификации.

### Resource Sdk

#### Resource detector name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-detector-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ➖ n_a | Resource detectors SHOULD have a unique name for reference in configuration. | - | Фича Resource Detector Naming не реализована. Детекторы ресурсов не имеют именованных идентификаторов для ссылки в конфигурации. |
| 2 | SHOULD | ➖ n_a | Names SHOULD be snake case and consist of lowercase alphanumeric and `_` characters, which ensures they conform to declarative configuration property name requirements. | - | Фича Resource Detector Naming не реализована. Нет системы именования детекторов. |
| 3 | SHOULD | ➖ n_a | Resource detector names SHOULD reflect the root namespace of attributes they populate. | - | Фича Resource Detector Naming не реализована. Детекторы не имеют именованных идентификаторов. |
| 4 | SHOULD | ➖ n_a | Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name which appropriately conveys their purpose. | - | Фича Resource Detector Naming не реализована. |
| 5 | SHOULD | ➖ n_a | An SDK which identifies multiple resource detectors with the same name SHOULD report an error. | - | Фича Resource Detector Naming не реализована. Нет проверки уникальности имён детекторов. |
| 6 | SHOULD | ➖ n_a | In order to limit collisions, resource detectors SHOULD document their name in a manner which is easily discoverable. | - | Фича Resource Detector Naming не реализована. Детекторы не имеют документированных имён. |
| 7 | MUST | ✅ found | The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge this, as the secondary resource, with any resource information provided by the user, i.e. the user provided resource information has higher priority. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:96` |  |
| 8 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:479` |  |
| 9 | MUST | ⚠️ partial | The `,` and `=` characters in keys and values MUST be percent encoded. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:467` | Парсер РазобратьПарыКлючЗначение разбирает формат key1=value1,key2=value2, но не выполняет percent-декодирование ключей и значений. Символы `,` и `=` в значениях, закодированные как %2C и %3D, не декодируются обратно. |
| 10 | SHOULD | ❌ not_found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | - | Функция РазобратьПарыКлючЗначение пропускает некорректные пары без символа '=', но не отбрасывает всё значение переменной окружения целиком при ошибке, как требует спецификация. |
| 11 | SHOULD | ❌ not_found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | - | При ошибке парсинга OTEL_RESOURCE_ATTRIBUTES не логируется и не сообщается об ошибке. Спецификация требует сообщать об ошибке в соответствии с принципами Error Handling. |

### Trace Api

#### Tracer operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracer-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The `Tracer` MUST provide functions to: Create a new `Span` (see the section on `Span`) | `src/Трассировка/Классы/ОтелТрассировщик.os:59` |  |
| 2 | SHOULD | ✅ found | The `Tracer` SHOULD provide functions to: Report if `Tracer` is `Enabled` | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 3 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when creating `Span`s, a `Tracer` SHOULD provide this `Enabled` API. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 4 | MUST | ✅ found | There are currently no required parameters for this API. Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 5 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Трассировка/Классы/ОтелТрассировщик.os:41` |  |
| 6 | SHOULD | ❌ not_found | The API SHOULD be documented that instrumentation authors needs to call this API each time they create a new `Span` to ensure they have the most up-to-date response. | - | Документация метода Включен() не содержит указания о том, что авторы инструментации должны вызывать его каждый раз перед созданием нового спана. |

### Trace Sdk

#### Tracer Provider### Tracer Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer-provider-tracer-creation)

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
| 3 | MUST | ✅ found | `Shutdown` MUST be called only once for each `TracerProvider` instance. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:108` |  |
| 4 | SHOULD | ⚠️ partial | SDKs SHOULD return a valid no-op Tracer for these calls, if possible. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65` | После Shutdown ПолучитьТрассировщик возвращает обычный ОтелТрассировщик, а не no-op трассировщик. Трассировщик ссылается на закрытый провайдер, поэтому функционально ограничен, но формально не является no-op |
| 5 | SHOULD | ❌ not_found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Метод Закрыть() - процедура без возвращаемого значения, не сообщает вызывающему коду об успехе/неудаче/таймауте |
| 6 | SHOULD | ❌ not_found | `Shutdown` SHOULD complete or abort within some timeout. | - | Метод Закрыть() не имеет механизма таймаута, выполняется синхронно без ограничения по времени |
| 7 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:111` |  |

#### Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Tracer` MUST behave according to the TracerConfig computed during Tracer creation. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 2 | MUST | ❌ not_found | the `Tracer` MUST be updated to behave according to the new `TracerConfig`. | - | Нет механизма обновления TracerConfig после создания трассировщика. TracerProvider не поддерживает обновление TracerConfigurator для уже созданных трассировщиков - кэшированные трассировщики сохраняют исходную конфигурацию |

#### TracerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the `enabled` parameter SHOULD default to `true` (i.e. `Tracer`s are enabled by default). | `src/Трассировка/Классы/ОтелКонфигурацияТрассировщика.os:35` |  |
| 2 | MUST | ⚠️ partial | If a `Tracer` is disabled, it MUST behave equivalently to a No-op Tracer. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` | Метод Включен() возвращает Ложь при отключенной конфигурации, но НачатьСпан() не проверяет Включен() - отключенный трассировщик всё равно создаёт реальные спаны вместо no-op поведения |
| 3 | MUST | ✅ found | The value of `enabled` MUST be used to resolve whether a `Tracer` is Enabled. | `src/Трассировка/Классы/ОтелТрассировщик.os:39` |  |
| 4 | MUST | ❌ not_found | However, the changes MUST be eventually visible. | - | Нет механизма динамического обновления параметров TracerConfig после создания трассировщика. Конфигурация фиксируется при создании и не может быть изменена |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Enabled` MUST return `false` when either: * there are no registered `SpanProcessors`, * `Tracer` is disabled (`TracerConfig.enabled` is `false`). | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:42` |  |

#### AlwaysOn* Returns `RECORD_AND_SAMPLE` always.* Description MUST be `AlwaysOnSampler`.#### AlwaysOff* Returns `DROP` always.* Description MUST be `AlwaysOffSampler`.#### TraceIdRatioBased

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwayson-returns-recordandsample-always-description-must-be-alwaysonsampler-alwaysoff-returns-drop-always-description-must-be-alwaysoffsampler-traceidratiobased)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Description MUST be `AlwaysOnSampler`. | `src/Трассировка/Модули/ОтелСэмплер.os:109` |  |
| 2 | MUST | ✅ found | Description MUST be `AlwaysOffSampler`. | `src/Трассировка/Модули/ОтелСэмплер.os:111` |  |
| 3 | MUST | ✅ found | The `TraceIdRatioBased` MUST ignore the parent `SampledFlag`. | `src/Трассировка/Модули/ОтелСэмплер.os:275` |  |
| 4 | MUST | ✅ found | Description MUST return a string of the form `"TraceIdRatioBased{RATIO}"` | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 5 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 6 | SHOULD | ✅ found | and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 7 | MUST | ✅ found | The sampling algorithm MUST be deterministic. | `src/Трассировка/Модули/ОтелСэмплер.os:275` |  |
| 8 | MUST | ✅ found | implementations MUST use a deterministic hash of the `TraceId` when computing the sampling decision. | `src/Трассировка/Модули/ОтелСэмплер.os:288` |  |
| 9 | MUST | ✅ found | A `TraceIdRatioBased` sampler with a given sampling probability MUST also sample all traces that any `TraceIdRatioBased` sampler with a lower sampling probability would sample. | `src/Трассировка/Модули/ОтелСэмплер.os:290` |  |
| 10 | SHOULD | ❌ not_found | the SDK SHOULD emit a warning such as: | - | No warning is emitted when TraceIdRatioBased is used as a child sampler (non-root context). The SDK does not detect or warn about this deprecated usage pattern. |
| 11 | MUST | ❌ not_found | The `ProbabilitySampler` sampler MUST ignore the parent `SampledFlag`. | - | ProbabilitySampler is not implemented. Only TraceIdRatioBased, AlwaysOn, AlwaysOff, and ParentBased samplers exist. |
| 12 | SHOULD | ❌ not_found | the OpenTelemetry TraceState SHOULD be modified to include the key-value `th:T` for rejection threshold value (T), as specified for the OpenTelemetry TraceState `th` sub-key. | - | ProbabilitySampler is not implemented. No TraceState th:T modification exists in the SDK. |
| 13 | SHOULD | ❌ not_found | the SDK SHOULD issue a warning statement in its log with a compatibility warning. | - | ProbabilitySampler is not implemented, so no compatibility warning for non-root span decisions using TraceID randomness without the Random flag. |
| 14 | MUST | ❌ not_found | Based on the decision from the wrapped root sampler, `AlwaysRecord` MUST behave as follows: | - | AlwaysRecord sampler decorator is not implemented. The SDK does not have a mechanism to convert DROP decisions to RECORD_ONLY. |
| 15 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the parameters passed to delegate GetSamplingIntent methods, as they are considered read-only state. | - | ComposableSampler interface and GetSamplingIntent method are not implemented. CompositeSampler architecture is absent from the SDK. |
| 16 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the OpenTelemetry TraceState (i.e., the `ot` sub-key of TraceState). | - | ComposableSampler interface is not implemented. No composable sampling architecture exists in the SDK. |
| 17 | SHOULD | ❌ not_found | The calling CompositeSampler SHOULD update the threshold of the outgoing TraceState (unless `!threshold_reliable`) | - | CompositeSampler is not implemented. The SDK has no composable sampling framework. |
| 18 | MUST | ❌ not_found | and that the explicit randomness values MUST not be modified. | - | CompositeSampler and ComposableSampler are not implemented. There is no explicit randomness value handling in the SDK's sampling framework. |
| 19 | SHOULD | ❌ not_found | For the zero case a `ComposableAlwaysOff` instance SHOULD be returned instead. | - | ComposableAlwaysOff and ComposableProbability samplers are not implemented. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | Custom implementations of the `IdGenerator` SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace `random` flag will be set in the associated Trace contexts. | - | No mechanism exists for IdGenerator implementations to declare W3C Level 2 randomness compliance. УстановитьГенераторИд accepts any object with СгенерироватьИдТрассировки/СгенерироватьИдСпана but there is no marker interface or property to identify randomness characteristics. |

#### OnEnding

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onending)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The end timestamp MUST have been computed (the `OnEnding` method duration is not included in the span duration). | `src/Трассировка/Классы/ОтелСпан.os:449` |  |
| 2 | MUST | ✅ found | The Span object MUST still be mutable (i.e., `SetAttribute`, `AddLink`, `AddEvent` can be called) while `OnEnding` is called. | `src/Трассировка/Классы/ОтелСпан.os:455` |  |
| 3 | MUST | ✅ found | This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:455` |  |
| 4 | MUST | ⚠️ partial | The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking `OnEnding` of the first `SpanProcessor`. | `src/Трассировка/Классы/ОтелСпан.os:448` | ОтелСпан does not use locks or synchronization primitives around mutation methods. Although the span calls ПередЗавершением before setting Завершен=Истина, there is no explicit mechanism to prevent other threads (ФоновыеЗадания) from modifying the span concurrently during the OnEnding callback. |

### Logs Api

#### Ergonomic API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#ergonomic-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | The ergonomic API SHOULD make it more convenient to emit event records following the event semantics. | - | Отдельный удобный (ergonomic) API для эмиссии событий (event records) не реализован. Логирование выполняется через стандартный Logger.Записать() с ручной настройкой ОтелЗаписьЛога. |
| 2 | SHOULD | ❌ not_found | The design of the ergonomic API SHOULD be idiomatic for its language. | - | Отдельный ergonomic API не реализован, поэтому требование к его идиоматичности неприменимо в текущей кодовой базе. |

### Logs Sdk

#### Logger Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` (see API). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 2 | MUST | ✅ found | The `LoggerProvider` MUST implement the Get a Logger API. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Logger`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:64` |  |
| 4 | MUST | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 5 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:92` |  |
| 6 | SHOULD | ❌ not_found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | - | Отсутствует диагностическое логирование при передаче невалидного (пустого или null) имени в ПолучитьЛоггер. Код не проверяет валидность имени и не выводит предупреждение. |
| 7 | MUST | ✅ found | The `LoggerProvider` MUST compute the relevant LoggerConfig using the configured LoggerConfigurator, and create a `Logger` whose behavior conforms to that `LoggerConfig`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:70` |  |

#### LoggerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: `logger_scope`: The `InstrumentationScope` of the `Logger`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:72` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `LoggerConfig`, or some signal indicating that the default LoggerConfig should be used. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:72` |  |
| 3 | MUST | ✅ found | `Shutdown` MUST be called only once for each `LoggerProvider` instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117` |  |
| 4 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op `Logger` for these calls, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:59` |  |
| 5 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:116` | Синхронный метод Закрыть() является процедурой (void) и не возвращает статус успеха/ошибки. Асинхронный ЗакрытьАсинхронно() возвращает Обещание, но синхронный вариант не сигнализирует о результате. |
| 6 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:116` | Синхронный метод Закрыть() не имеет механизма таймаута. Асинхронная версия ЗакрытьАсинхронно() опирается на таймаут Promise, но сам метод не принимает параметр таймаута. |
| 7 | MUST | ✅ found | `Shutdown` MUST be implemented by invoking `Shutdown` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:120` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Logger` MUST behave according to the LoggerConfig computed during logger creation. | `src/Логирование/Классы/ОтелЛоггер.os:47` |  |
| 2 | MUST | ✅ found | If the `LoggerProvider` supports updating the LoggerConfigurator, then upon update the `Logger` MUST be updated to behave according to the new `LoggerConfig`. | `src/Логирование/Классы/ОтелЛоггер.os:108` |  |

#### LoggerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the `enabled` parameter SHOULD default to `true` (i.e. `Logger`s are enabled by default). | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:73` |  |
| 2 | MUST | ✅ found | If a `Logger` is disabled, it MUST behave equivalently to No-op Logger. | `src/Логирование/Классы/ОтелЛоггер.os:50` |  |
| 3 | MUST | ✅ found | If not explicitly set, the `minimum_severity` parameter MUST default to `0`. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:73` |  |
| 4 | MUST | ✅ found | If a log record's SeverityNumber is specified (i.e. not `0`) and is less than the configured `minimum_severity`, the log record MUST be dropped by the `Logger`. | `src/Логирование/Классы/ОтелЛоггер.os:54` |  |
| 5 | MUST | ✅ found | If not explicitly set, the `trace_based` parameter MUST default to `false`. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:73` |  |
| 6 | MUST | ✅ found | If `trace_based` is `true`, log records associated with unsampled traces MUST be dropped by the `Logger`. | `src/Логирование/Классы/ОтелЛоггер.os:58` |  |
| 7 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Логирование/Классы/ОтелЛоггер.os:108` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If Observed Timestamp is unspecified, the implementation SHOULD set it equal to the current time. | `src/Логирование/Классы/ОтелЛоггер.os:92` |  |
| 2 | MUST | ✅ found | If an Exception is provided, the SDK MUST by default set attributes from the exception on the `LogRecord` with the conventions outlined in the exception semantic conventions. | `src/Логирование/Классы/ОтелЛоггер.os:143` |  |
| 3 | MUST | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:155` |  |
| 4 | MUST NOT | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:155` |  |
| 5 | MUST | ✅ found | Before processing a log record, the implementation MUST apply the filtering rules defined by the LoggerConfig (in case `Enabled` was not called prior to emitting the record): | `src/Логирование/Классы/ОтелЛоггер.os:86` |  |
| 6 | MUST | ✅ found | Minimum severity: If the log record's SeverityNumber is specified (i.e. not `0`) and is less than the configured `minimum_severity`, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:123` |  |
| 7 | MUST | ✅ found | Trace-based: If `trace_based` is `true`, and if the log record has a `SpanId` and the `TraceFlags` SAMPLED flag is unset, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:127` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Enabled` MUST return `false` when either: there are no registered `LogRecordProcessors`; `Logger` is disabled (`LoggerConfig.enabled` is `false`); the provided severity is specified (i.e. not `0`) and is less than the configured `minimum_severity` in the `LoggerConfig`; `trace_based` is `true` in the `LoggerConfig` and the current context is associated with an unsampled trace; all registered `LogRecordProcessors` implement `Enabled`, and a call to `Enabled` on each of them returns `false`. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Логирование/Классы/ОтелЛоггер.os:63` |  |

### Metrics Api

#### General characteristics#### Instrument name syntax

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-characteristics-instrument-name-syntax)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD treat it as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:41` |  |
| 2 | MUST | ✅ found | It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:41` |  |
| 3 | MUST | ✅ found | The API MUST treat it as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:45` |  |
| 4 | MUST | ✅ found | It MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or `utf8mb3`). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:45` |  |
| 5 | MUST | ✅ found | It MUST support at least 1023 characters. OpenTelemetry API authors MAY decide if they want to support more. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:45` |  |
| 6 | MUST | ✅ found | OpenTelemetry SDKs MUST handle `advisory` parameters as described here. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

### Metrics Sdk

#### Meter Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create `Meter` instances through a `MeterProvider` (see API). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 2 | MUST | ✅ found | The `MeterProvider` MUST implement the Get a Meter API. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:62` |  |
| 4 | MUST | ⚠️ partial | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` | ПолучитьМетр returns a working Meter for any name (including empty), but there is no explicit validation or warning for null/empty names - it silently proceeds. The Meter is returned but the invalid name case is not specifically handled with logging. |
| 5 | SHOULD | ⚠️ partial | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:62` | The original invalid name value is preserved (passed to InstrumentationScope as-is), but this is incidental rather than by explicit design - there is no explicit validation code that preserves it. |
| 6 | SHOULD | ❌ not_found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | - | No logging of invalid/empty name is implemented. ПолучитьМетр does not check for empty/null names and does not log any warning message. |
| 7 | MUST | ✅ found | The `MeterProvider` MUST compute the relevant MeterConfig using the configured MeterConfigurator, and create a `Meter` whose behavior conforms to that `MeterConfig`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:206` |  |

#### MeterConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: `meter_scope`: The `InstrumentationScope` of the `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:210` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `MeterConfig`, or some signal indicating that the default MeterConfig should be used. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:210` |  |
| 3 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MeterProvider` instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:131` |  |
| 4 | SHOULD | ✅ found | After the call to `Shutdown`, subsequent attempts to get a `Meter` are not allowed. SDKs SHOULD return a valid no-op Meter for these calls, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:57` |  |
| 5 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` | Закрыть() is a Процедура (void), not a Функция. It does not return a status. The async variant ЗакрытьАсинхронно() returns an Обещание but the sync method provides no success/failure indication. |
| 6 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` | The synchronous Закрыть() method does not accept or enforce a timeout. The async variant ЗакрытьАсинхронно() returns a Promise but the sync path has no timeout mechanism. |
| 7 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered MetricReader and MetricExporter instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:136` |  |

#### Start timestamps

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#start-timestamps)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp, or the creation time of the instrument if this is the first collection interval for the instrument. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:134` | ВремяСтарта устанавливается при создании и обновляется в ОчиститьТочкиДанных (для дельты), но обновляется на текущее время при очистке, а не на время предыдущего интервала сбора |
| 2 | MUST | ⚠️ partial | This implies that all data points with delta temporality aggregation for an instrument MUST share the same start timestamp. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:134` | Все точки данных используют общий ВремяСтарта из инструмента, что соответствует требованию, но значение ВремяСтарта может быть некорректным (см. предыдущее требование) |
| 3 | MUST | ⚠️ partial | Cumulative timeseries MUST use a consistent start timestamp for all collection intervals. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:134` | Для кумулятивной временности аккумуляторы и ВремяСтарта не сбрасываются в ОчиститьТочкиДанных, что обеспечивает постоянный start timestamp. Реализация корректна для этого случая, но start timestamp устанавливается при создании инструмента, а не при первом измерении. |
| 4 | SHOULD | ❌ not_found | For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the series. | - | ВремяСтарта задаётся при создании инструмента, а не при первом измерении серии |
| 5 | SHOULD | ❌ not_found | For asynchronous instrument, the start timestamp SHOULD be: The creation time of the instrument, if the first series measurement occurred in the first collection interval, Otherwise, the timestamp of the collection interval prior to the first series measurement. | - | Для асинхронных инструментов ОтелБазовыйНаблюдаемыйИнструмент.ПреобразоватьЗаписиВТочки использует текущее время как startTimeUnixNano, а не логику из спецификации |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instrument registrations. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:64` |  |
| 2 | MUST | ✅ found | `Meter` MUST behave according to the MeterConfig computed during Meter creation. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:73` |  |
| 3 | MUST | ❌ not_found | If the `MeterProvider` supports updating the MeterConfigurator, then upon update the `Meter` MUST be updated to behave according to the new `MeterConfig`. | - | MeterProvider (ОтелПровайдерМетрик) применяет конфигурацию при создании метра в ПрименитьКонфигурацию(), но не поддерживает обновление конфигуратора после создания - нет метода для обновления MeterConfigurator и повторного применения к существующим метрам. |

#### MeterConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the `enabled` parameter SHOULD default to `true` (i.e. `Meter`s are enabled by default). | `src/Метрики/Классы/ОтелКонфигурацияМетра.os:35` |  |
| 2 | MUST | ✅ found | If a `Meter` is disabled, it MUST behave equivalently to No-op Meter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:174` |  |
| 3 | MUST | ✅ found | The value of `enabled` MUST be used to resolve whether an instrument is Enabled. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 4 | MUST | ⚠️ partial | However, the changes MUST be eventually visible. | `src/Метрики/Классы/ОтелМетр.os:344` | МетрВключен использует АтомарноеБулево, что обеспечивает видимость изменений для инструментов, однако нет механизма динамического обновления MeterConfig после создания Meter - конфигурация применяется только при создании. |

#### Instrument enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The synchronous instrument `Enabled` MUST return `false` when either: The MeterConfig of the `Meter` used to create the instrument has parameter `enabled=false`. All resolved views for the instrument are configured with the Drop Aggregation. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:267` |  |

#### MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | To construct a `MetricReader` when setting up an SDK, at least the following SHOULD be provided: | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:228` |  |
| 2 | SHOULD | ✅ found | The default output `aggregation` (optional), a function of instrument kind. This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:162` |  |
| 3 | SHOULD | ✅ found | If not configured, the default aggregation SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:162` |  |
| 4 | SHOULD | ✅ found | The output `temporality` (optional), a function of instrument kind. This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:162` |  |
| 5 | SHOULD | ✅ found | If not configured, the Cumulative temporality SHOULD be used. | `src/Метрики/Модули/ОтелСелекторВременнойАгрегации.os:28` |  |
| 6 | SHOULD | ❌ not_found | The default aggregation cardinality limit (optional) to use, a function of instrument kind. If not configured, a default value of 2000 SHOULD be used. | - | Лимит мощности агрегации (cardinality limit) не задаётся в ОтелПериодическийЧитательМетрик. Значение по умолчанию 2000 не используется. Лимит можно задать через ОтелПредставление.ЛимитМощностиАгрегации, но дефолтное значение 2000 для читателя не реализовано. |
| 7 | SHOULD | ✅ found | A `MetricReader` SHOULD provide the MetricFilter to the SDK or registered MetricProducer(s) when calling the `Produce` operation. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:110` |  |
| 8 | SHOULD | ✅ found | A common implementation of `MetricReader`, the periodic exporting `MetricReader` SHOULD be provided to be used typically with push-based metrics collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:1` |  |
| 9 | MUST | ✅ found | The `MetricReader` MUST ensure that data points from OpenTelemetry instruments are output in the configured aggregation temporality for each instrument kind. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:158` |  |
| 10 | MUST | ⚠️ partial | For synchronous instruments with Cumulative aggregation temporality, MetricReader.Collect MUST receive data points exposed in previous collections regardless of whether new measurements have been recorded. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:155` | Данные очищаются после экспорта в методе СобратьИЭкспортировать через ОчиститьТочкиДанных, но обрабатываются с учётом временности. Накопленные (cumulative) данные сохраняются в аккумуляторах инструментов, однако отсутствует явная конверсия Delta->Cumulative для синхронных инструментов. |
| 11 | MUST | ⚠️ partial | For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:155` | Delta-точки очищаются после экспорта, что обеспечивает только новые данные, но нет явного механизма различения Delta/Cumulative поведения для синхронных инструментов на уровне reader. |
| 12 | MUST | ⚠️ partial | For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:130` | Асинхронные инструменты (observable) вызывают callback-и при каждом сборе через ВызватьМультиОбратныеВызовы(), но нет явного разделения на Delta/Cumulative поведение для асинхронных инструментов. |
| 13 | MUST | ⚠️ partial | For instruments with Cumulative aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST repeat the same starting timestamps (e.g. `(T0, T1], (T0, T2], (T0, T3]`). | `src/Метрики/Классы/ОтелБазовыйАгрегатор.os:48` | Шаблон точки данных содержит ВремяСтарта, но нет явного механизма сохранения начального timestamp для cumulative агрегации между вызовами Collect. |
| 14 | MUST | ⚠️ partial | For instruments with Delta aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST advance the starting timestamp (e.g. `(T0, T1], (T1, T2], (T2, T3]`). | `src/Метрики/Классы/ОтелБазовыйАгрегатор.os:48` | Нет явного механизма продвижения начального timestamp для delta агрегации между последовательными вызовами Collect. |
| 15 | MUST | ⚠️ partial | The ending timestamp (i.e. `TimeUnixNano`) MUST always be equal to time the metric data point took effect, which is equal to when MetricReader.Collect was invoked. | `src/Метрики/Классы/ОтелБазовыйАгрегатор.os:48` | Timestamp ВремяСейчас передаётся при сборе, но он генерируется в инструменте при вызове Собрать, а не строго при вызове MetricReader.Collect. |
| 16 | MUST | ✅ found | The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`, and the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NOT introduce side-effects to other `MetricReader` instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:103` |  |
| 17 | SHOULD NOT | ✅ found | The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`, and the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NOT introduce side-effects to other `MetricReader` instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:117` |  |
| 18 | MUST NOT | ❌ not_found | The SDK MUST NOT allow a `MetricReader` instance to be registered on more than one `MeterProvider` instance. | - | Нет проверки при регистрации MetricReader на MeterProvider, что этот reader ещё не зарегистрирован на другом MeterProvider. Читатель можно добавить на несколько провайдеров без ошибки. |
| 19 | SHOULD | ✅ found | The SDK SHOULD provide a way to allow `MetricReader` to respond to MeterProvider.ForceFlush and MeterProvider.Shutdown. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:125` |  |

#### Produce batch

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#produce-batch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | `Produce` MUST return a batch of Metric Points, filtered by the optional `metricFilter` parameter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:119` | Функция Produce как отдельная операция MetricProducer не существует, но MetricReader (СобратьИЭкспортировать) собирает метрики и применяет ФильтрМетрик. Фильтрация реализована через УстановитьФильтрМетрик и МетрикаОтброшена, но не как параметр метода Produce. |
| 2 | SHOULD | ✅ found | Implementation SHOULD use the filter as early as possible to gain as much performance gain possible (memory allocation, internal metric fetching, etc). | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:241` |  |
| 3 | SHOULD | ❌ not_found | If the batch of Metric Points includes resource information, `Produce` SHOULD require a resource as a parameter. | - | Метод Produce не существует как отдельная функция. Ресурс доступен через Метр.Ресурс() внутри СобратьИЭкспортировать, но не передаётся как параметр. |
| 4 | SHOULD | ⚠️ partial | `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:119` | СобратьИЭкспортировать - процедура (не функция), не возвращает результат. Ошибки логируются, но вызывающий код не узнаёт об успехе/неудаче. |
| 5 | SHOULD | ❌ not_found | If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`. | - | MetricProducer как отдельная сущность не реализован, поэтому нет InstrumentationScope, идентифицирующего его. |

### Env Vars

#### Prometheus Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#prometheus-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | "logging": Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:177` |  |
| 2 | SHOULD | ✅ found | "logging": Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:291` |  |
| 3 | SHOULD | ✅ found | "logging": Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:255` |  |
| 4 | MUST | ❌ not_found | When OTEL_CONFIG_FILE is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored. | - | Переменная OTEL_CONFIG_FILE не поддерживается реализацией. Декларативная конфигурация через файл конфигурации не реализована - отсутствуют функции Parse и Create, нет чтения файла конфигурации. |

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

