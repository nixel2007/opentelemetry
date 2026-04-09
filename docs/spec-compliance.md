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
| Найдено требований (Stable universal) | 652 |
| ✅ Реализовано (found) | 503 (77.1%) |
| ⚠️ Частично (partial) | 96 (14.7%) |
| ❌ Не реализовано (not_found) | 53 (8.1%) |
| ➖ Неприменимо (n_a) | 2 |
| **MUST/MUST NOT found** | 356/395 (90.1%) |
| **SHOULD/SHOULD NOT found** | 147/257 (57.2%) |

## Соответствие по разделам (Stable)

| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |
|---|---|---|---|---|---|---|
| Context | 14 | 1 | 0 | 0 | 15 | 93.3% |
| Baggage Api | 16 | 1 | 0 | 0 | 17 | 94.1% |
| Resource Sdk | 11 | 2 | 2 | 0 | 15 | 73.3% |
| Trace Api | 98 | 10 | 12 | 0 | 120 | 81.7% |
| Trace Sdk | 52 | 16 | 7 | 0 | 75 | 69.3% |
| Logs Api | 20 | 1 | 0 | 0 | 21 | 95.2% |
| Logs Sdk | 42 | 14 | 3 | 0 | 59 | 71.2% |
| Metrics Api | 87 | 8 | 0 | 0 | 95 | 91.6% |
| Metrics Sdk | 115 | 31 | 19 | 1 | 165 | 69.7% |
| Otlp Exporter | 11 | 7 | 6 | 1 | 24 | 45.8% |
| Propagators | 32 | 0 | 0 | 0 | 32 | 100.0% |
| Env Vars | 5 | 5 | 4 | 0 | 14 | 35.7% |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Context]** [MUST] The API MUST accept the following parameters: The Context.  
  Нет функции Attach, принимающей готовый объект Context. Вместо этого УстановитьЗначение(Ключ, Значение) принимает ключ и значение, строит новый контекст внутри и помещает в стек. СделатьСпанТекущим/СделатьBaggageТекущим - специализированные обёртки, тоже не принимают Context целиком. (`src/Ядро/Модули/ОтелКонтекст.os:203`)

- ⚠️ **[Resource Sdk]** [MUST] Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK.  
  Detectors exist as separate classes (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) but they are part of the same package (registered in the same lib.config), not implemented as separate packages from the SDK. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1`)

- ❌ **[Resource Sdk]** [MUST] Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions.  
  Detectors (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) create resources with Новый ОтелРесурс(Истина) which sets empty АдресСхемы, but they populate semantic convention attributes (host.name, os.type, process.pid, host.arch) without setting a matching Schema URL. (-)

- ❌ **[Resource Sdk]** [MUST] If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources.  
  In ОтелРесурс.ЗаполнитьАтрибутыПоУмолчанию() (line 108-118), detectors are combined by iterating and copying attributes directly without using Merge. There is no check for conflicting non-empty Schema URLs between detectors. (-)

- ⚠️ **[Trace Api]** [MUST] In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception.  
  ПолучитьТрассировщик не проверяет ИмяБиблиотеки на пустую строку или Неопределено - просто создает трассировщик с любым именем. Работает как fallback, но нет явной валидации и логирования предупреждения. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58`)

- ⚠️ **[Trace Api]** [MUST NOT] This API MUST NOT accept a Span or SpanContext as parent, only a full Context  
  НачатьДочернийСпан принимает как ОтелСпан, так и ОтелКонтекстСпана в качестве родителя (строка 134). Спецификация требует принимать только полный Context, а не Span или SpanContext. Однако НачатьСпан() без явного родителя использует неявный контекст (строка 57), что соответствует спецификации. (`src/Трассировка/Классы/ОтелТрассировщик.os:133-137`)

- ❌ **[Trace Api]** [MUST] The API documentation MUST state that adding links at span creation is preferred to calling AddLink later, for contexts that are available during span creation, because head sampling decisions can only consider information present during span creation.  
  В документации SpanBuilder.ДобавитьЛинк есть комментарий о предпочтительности, но в API документации Span.ДобавитьЛинк нет явного указания, что добавление линков при создании предпочтительнее. (-)

- ⚠️ **[Trace Api]** [MUST] The API MUST return a non-recording Span with the SpanContext in the parent Context (whether explicitly given or implicit current).  
  Трассировщик возвращает ОтелНоопСпан когда семплер отбрасывает спан, сохраняя traceId из родителя. Но нет отдельного API-уровня без SDK - API и SDK объединены, поведение без установленного SDK не определено как отдельный режим. (`src/Трассировка/Классы/ОтелТрассировщик.os:71`)

- ⚠️ **[Trace Sdk]** [MUST] For backwards compatibility it MUST also be able to access the InstrumentationLibrary (deprecated since 1.10.0) having the same name and version values as the InstrumentationScope.  
  ОтелСпан предоставляет доступ к ОбластьИнструментирования(), но отдельного метода или алиаса InstrumentationLibrary (deprecated) нет. Используется единый класс ОтелОбластьИнструментирования с тем же именем и версией, что фактически покрывает требование, но отдельной deprecated-сущности нет. (`src/Трассировка/Классы/ОтелСпан.os:170`)

- ⚠️ **[Trace Sdk]** [MUST NOT] SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value (the rv sub-key).  
  SDK не работает с подключами OpenTelemetry TraceState (ot=..., rv:...) вообще - не читает и не пишет их. Формально не перезаписывает, но и не имеет осознанной обработки. TraceState передается как непрозрачная строка. (-)

- ⚠️ **[Trace Sdk]** [MUST NOT] Root Samplers MAY insert an explicit randomness value into the OpenTelemetry TraceState value in cases where an explicit randomness value is not already set.  
  Семплер не вставляет явное значение случайности в OpenTelemetry TraceState. OTel подключи (ot=rv:...) не поддерживаются. (-)

- ❌ **[Trace Sdk]** [MUST] If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. It MAY skip or abort some or all Export or ForceFlush calls it has made to achieve this goal.  
  Метод СброситьБуфер() не принимает параметр таймаута. ЭкспортироватьВсеПакеты() выполняется до полного завершения без возможности прервать по таймауту. (-)

- ⚠️ **[Trace Sdk]** [MUST NOT] Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure).  
  HTTP transport has a configurable timeout (default 10s), but the Экспортировать method in ОтелЭкспортерСпанов itself does not enforce a timeout wrapper - it relies on the transport's timeout. This is a reasonable approach but the timeout is on the transport level, not on Export() directly. (`src/Экспорт/Классы/ОтелHttpТранспорт.os:69`)

- ⚠️ **[Trace Sdk]** [MUST] Span Exporter - ForceFlush and Shutdown MUST be safe to be called concurrently.  
  Закрыть() sets a boolean flag without synchronization (no БлокировкаРесурса or АтомарноеБулево). Concurrent calls to Закрыть() and Экспортировать() could race on the Закрыт variable. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:47`)

- ⚠️ **[Logs Sdk]** [MUST] The built-in LogRecordProcessors MUST do so (call exporter's Export with all LogRecords and then invoke ForceFlush on the exporter).  
  Встроенные процессоры экспортируют все накопленные записи через Экспортер.Экспортировать(), но не вызывают Экспортер.СброситьБуфер() (ForceFlush) на экспортере после экспорта. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68`)

- ❌ **[Logs Sdk]** [MUST] If a timeout is specified, the LogRecordProcessor MUST prioritize honoring the timeout over finishing all calls.  
  СброситьБуфер() не принимает параметр таймаута, поэтому невозможно приоритизировать выполнение таймаута над завершением всех вызовов. (-)

- ⚠️ **[Logs Sdk]** [MUST] LogRecordExporter - ForceFlush and Shutdown MUST be safe to be called concurrently.  
  Закрыть() sets Закрыт=Истина without synchronization (no lock or atomic). СброситьБуфер() is a no-op. There is no explicit concurrency protection on exporter's ForceFlush/Shutdown calls. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41`)

- ⚠️ **[Metrics Sdk]** [MUST] The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept.  
  ИсключенныеКлючиАтрибутов хранятся в ОтелПредставление, но не применяются в ОтелБазовыйСинхронныйИнструмент - ФильтроватьАтрибутыПоКлючам работает только с РазрешенныеКлючиАтрибутов (allow-list), exclude-list не используется при фильтрации. (`src/Метрики/Классы/ОтелПредставление.os:10`)

- ⚠️ **[Metrics Sdk]** [MUST] If the user does not provide an aggregation value, the MeterProvider MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance.  
  Агрегация по умолчанию задается жестко при создании инструмента (Counter->Sum, Histogram->Histogram, Gauge->LastValue), но не настраивается per MetricReader - один агрегатор разделяется между всеми читателями. (`src/Метрики/Классы/ОтелМетр.os:58-59`)

- ⚠️ **[Metrics Sdk]** [MUST] If the user does not provide an aggregation_cardinality_limit value, the MeterProvider MUST apply the default aggregation cardinality limit the MetricReader is configured with.  
  Лимит по умолчанию (2000) задан жестко в конструкторе ОтелБазовыйСинхронныйИнструмент и ОтелМетр, а не берется из MetricReader. MetricReader не имеет свойства cardinality limit. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253`)

- ⚠️ **[Metrics Sdk]** [MUST] If both a View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters.  
  Реализовано для attribute_keys (строки 523-528) и для ГраницыГистограммы (строки 540-550), но НЕ для aggregation - View.Агрегация() не применяется к уже созданному инструменту, агрегатор создается при создании инструмента и не заменяется представлением. (`src/Метрики/Классы/ОтелМетр.os:518-536`)

- ⚠️ **[Metrics Sdk]** [MUST] If both a View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters.  
  Приоритет View реализован для attribute_keys и границ гистограммы, но не для aggregation - View.Агрегация() не применяется динамически к инструменту. (`src/Метрики/Классы/ОтелМетр.os:523-528`)

- ⚠️ **[Metrics Sdk]** [MUST] Callback functions MUST be invoked for the specific MetricReader performing collection, such that observations made or produced by executing callbacks only apply to the intended MetricReader during collection.  
  Callbacks вызываются при сборе каждого MetricReader (через Метр.ВызватьМультиОбратныеВызовы), но наблюдения не изолированы per-reader - данные разделяются между всеми читателями. Каждый reader видит одни и те же observation данные. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:140-147`)

- ⚠️ **[Metrics Sdk]** [MUST] This MUST be clearly documented in the API and the reservoir MUST be given the Attributes associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the 'offer' method.  
  The reservoir receives both measurement attributes and series attributes per-offer call (not at construction). The filtered attributes computation works correctly but attributes are not given at construction time as an alternative. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39`)

- ⚠️ **[Metrics Sdk]** [MUST NOT] Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure).  
  Export зависит от транспорта (HTTP/gRPC). Таймаут может быть настроен на уровне транспорта (HTTPСоединение), но явного таймаута на уровне самого метода Export нет. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25`)

- ⚠️ **[Metrics Sdk]** [MUST] MetricProducer defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data.  
  No separate MetricProducer interface exists as a distinct class. The SDK does not bridge third-party metric sources via a MetricProducer interface - the MetricReader (ОтелПериодическийЧитательМетрик, ОтелПрометеусЧитательМетрик) collects from internal Meters directly. However, the pull exporter is modeled as MetricReader (ОтелПрометеусЧитательМетрик) which is explicitly allowed by the spec. Changing status to partial since MetricProducer as a pluggable interface for third-party sources is not implemented. (-)

- ❌ **[Metrics Sdk]** [MUST] A MetricProducer MUST support the following functions (Produce).  
  No MetricProducer interface or class exists with a Produce function. The readers (ОтелПериодическийЧитательМетрик, ОтелПрометеусЧитательМетрик) collect metrics internally via СобратьИЭкспортировать/СобратьСемейства, but there is no standalone MetricProducer with a Produce method that can be plugged into a MetricReader. (-)

- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry.  
  No explicit numerical limits handling is implemented. The SDK relies on OneScript's native number handling without any specific graceful error handling for numerical limits or overflows. (-)

- ⚠️ **[Metrics Sdk]** [MUST] MeterProvider - Meter creation, ForceFlush and Shutdown MUST be safe to be called concurrently.  
  ОтелПровайдерМетрик uses СинхронизированнаяКарта for Meter cache (line 241), providing thread-safe Meter creation. However, СброситьБуфер (ForceFlush) and Закрыть (Shutdown) do not use any locking or atomic guards - they iterate ЧитателиМетрик without synchronization. Partially safe. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:52`)

- ⚠️ **[Metrics Sdk]** [MUST] MetricExporter - ForceFlush and Shutdown MUST be safe to be called concurrently.  
  ОтелЭкспортерМетрик.Закрыть() sets Закрыт = Истина (line 50) without atomic operation or lock. СброситьБуфер() is empty (no-op). The Закрыт flag is a plain boolean, not an АтомарноеБулево, so concurrent calls to Закрыть/Экспортировать could have a race condition. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49`)

- ⚠️ **[Otlp Exporter]** [MUST] The following configuration options MUST be available to configure the OTLP exporter (Endpoint, Insecure, Certificate File, Client key file, Client certificate file, Headers, Compression, Timeout, Protocol).  
  Core options (endpoint, protocol, headers, compression, timeout) are available. TLS certificate options (Certificate File, Client key file, Client certificate file) and Insecure option are not implemented. Insecure is MAY, but TLS cert configs are listed as MUST-available options. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130`)

- ❌ **[Otlp Exporter]** [MUST] Each configuration option MUST be overridable by a signal specific option (e.g., OTEL_EXPORTER_OTLP_TRACES_ENDPOINT overrides OTEL_EXPORTER_OTLP_ENDPOINT for traces).  
  Only generic otel.exporter.otlp.* keys are read in СоздатьТранспорт(). No per-signal overrides (traces, logs, metrics) exist for endpoint, protocol, headers, compression, or timeout. (-)

- ❌ **[Otlp Exporter]** [MUST] For the per-signal variables (OTEL_EXPORTER_OTLP_<signal>_ENDPOINT), the URL MUST be used as-is without any modification.  
  Per-signal endpoint variables (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_LOGS_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_ENDPOINT) are not supported at all. (-)

- ❌ **[Otlp Exporter]** [MUST] The only exception is that if a per-signal URL contains no path part, the root path / MUST be used.  
  Per-signal endpoint variables are not implemented, so this root-path fallback logic is also absent. (-)

- ⚠️ **[Otlp Exporter]** [MUST NOT] An SDK MUST NOT modify the URL in ways other than specified above. If the port is empty or not given, TCP port 80 is the default for http and TCP port 443 for https.  
  Base URL construction from OTEL_EXPORTER_OTLP_ENDPOINT correctly appends signal paths. However, per-signal endpoint variables are not supported, so the 'as-is' requirement for them cannot be verified. Double-slash normalization (line 100-103) is a minor modification. (`src/Экспорт/Классы/ОтелHttpТранспорт.os:99`)

- ⚠️ **[Otlp Exporter]** [MUST] Protocol: The transport protocol. Options MUST be one of: grpc, http/protobuf, http/json.  
  grpc creates ОтелGrpcТранспорт (protobuf over gRPC). http/json and http/protobuf both create ОтелHttpТранспорт which sends JSON (Content-Type: application/json). http/protobuf is not truly supported as protobuf-over-HTTP - it falls through to JSON encoding. No validation rejects unknown protocol values. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ⚠️ **[Env Vars]** [MUST] The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset.  
  Большинство переменных проверяют пустую строку (<> Неопределено И <> ""), например otel.resource.attributes (строка 105), otel.exporter.otlp.headers (строка 137), лимиты (строки 398-447). Однако otel.service.name (строка 114) и otel.traces.sampler (строка 191) проверяют только Неопределено без проверки на пустую строку. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105`)

- ⚠️ **[Env Vars]** [MUST] Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false.  
  Логика парсинга булева верна (НРег(Значение) = "true"), но otel.enabled использует значение по умолчанию "true" (строка 562: Менеджер.Параметр("otel.enabled", "true")), из-за чего при отсутствии переменной возвращается true вместо false. Также используется нестандартная OTEL_ENABLED вместо спецификационной OTEL_SDK_DISABLED. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562`)

- ⚠️ **[Env Vars]** [MUST] For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting.  
  Для пропагаторов выводится предупреждение при неизвестном значении (строка 373: Сообщить("неизвестный пропагатор")). Однако неизвестный сэмплер молча использует fallback на ParentBased(AlwaysOn) без предупреждения (строки 216-218). Неизвестный экспортер молча обрабатывается как otlp. Фильтр экземпляров (ОтелПостроительПровайдераМетрик.os:123) молча игнорирует без предупреждения. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:373`)

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Baggage Api]** [SHOULD NOT] The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation.  
  Convenience methods BaggageИзКонтекста() and КонтекстСBaggage() exist so users don't need the key directly, but КлючBaggage() is exposed as a public export method, giving users direct access to the Context Key. (`src/Ядро/Модули/ОтелКонтекст.os:53`)

- ⚠️ **[Resource Sdk]** [SHOULD] Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate.  
  Detectors use empty schema URL (via Новый ОтелРесурс(Истина)), but they DO populate known semantic convention attributes (host.name, os.type, etc.), so they should set a schema URL rather than leaving it empty. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18`)

- ❌ **[Trace Api]** [SHOULD] Its name property SHOULD be set to an empty string (when invalid name specified).  
  Нет проверки на невалидное имя - имя просто передается как есть в ОбластьИнструментирования без корректировки на пустую строку. (-)

- ❌ **[Trace Api]** [SHOULD] A message reporting that the specified value is invalid SHOULD be logged (when invalid name specified).  
  Нет логирования предупреждения при передаче невалидного имени в ПолучитьТрассировщик. (-)

- ⚠️ **[Trace Api]** [SHOULD] The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable  
  Это рекомендация по использованию API, а не по реализации. API принимает строковое имя через параметр ИмяСпана, но нет валидации на общность имени. Реализация partial - нет принудительного соблюдения. (-)

- ⚠️ **[Trace Api]** [SHOULD] Generality SHOULD be prioritized over human-readability  
  Рекомендация по использованию API. API принимает произвольную строку, нет механизма для принуждения к общности. Реализация partial - нет принудительного соблюдения. (-)

- ⚠️ **[Trace Api]** [SHOULD] This SHOULD be called SetStatus.  
  Метод называется УстановитьСтатус, что является русскоязычным эквивалентом SetStatus. Допустимо для русскоязычного SDK, но не точное имя из спецификации. (`src/Трассировка/Классы/ОтелСпан.os:413`)

- ❌ **[Trace Api]** [SHOULD] The status code SHOULD remain unset, except for the following circumstances.  
  Это рекомендация для инструментирующих библиотек. SDK не контролирует это поведение напрямую, но и не документирует как рекомендацию. (-)

- ❌ **[Trace Api]** [SHOULD] When the status is set to Error by Instrumentation Libraries, the Description SHOULD be documented and predictable.  
  Это рекомендация для инструментирующих библиотек, не для SDK. Нет документации о стандартных Description для Error. (-)

- ❌ **[Trace Api]** [SHOULD] For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish their own conventions, including possible values of Description and what they mean.  
  Рекомендация для авторов инструментирующих библиотек. Нет опубликованных конвенций. (-)

- ❌ **[Trace Api]** [SHOULD NOT] Generally, Instrumentation Libraries SHOULD NOT set the status code to Ok, unless explicitly configured to do so.  
  Рекомендация для инструментирующих библиотек. SDK не ограничивает установку Ok. (-)

- ❌ **[Trace Api]** [SHOULD] Instrumentation Libraries SHOULD leave the status code as Unset unless there is an error.  
  Рекомендация для инструментирующих библиотек. SDK не документирует данное руководство. (-)

- ❌ **[Trace Api]** [SHOULD] Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generate.  
  Рекомендация для инструментов анализа, а не SDK. В коде нет обработки подавления ошибок на основе Ok-статуса. (-)

- ⚠️ **[Trace Api]** [SHOULD] Any locking used needs be minimized and SHOULD be removed entirely if possible.  
  Метод Завершить не использует блокировок напрямую, но вызывает Процессор.ПриЗавершении который может содержать блокировки (ОтелПростойПроцессорСпанов использует БлокировкаРесурса). Блокировки минимизированы, но не удалены. (`src/Трассировка/Классы/ОтелСпан.os:447`)

- ⚠️ **[Trace Api]** [SHOULD NOT] If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible.  
  ОтелНоопСпан является публичным классом, зарегистрированным в lib.config. Спецификация рекомендует не экспонировать тип публично, если возможно. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ⚠️ **[Trace Api]** [SHOULD] If a new type is required to be publicly exposed, it SHOULD be named NonRecordingSpan.  
  Класс назван ОтелНоопСпан (NoopSpan), а не NonRecordingSpan, хотя он фактически является non-recording span. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ❌ **[Trace Api]** [SHOULD] In order for SpanKind to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose.  
  Рекомендация для авторов инструментирующего кода. SDK не обеспечивает проверку или документацию данного ограничения. (-)

- ❌ **[Trace Api]** [SHOULD NOT] A server-side span SHOULD NOT be used to describe outgoing remote procedure call.  
  Рекомендация для авторов инструментирующего кода. SDK не контролирует правильность использования SpanKind. (-)

- ⚠️ **[Trace Api]** [SHOULD] Link - Links are immutable and SHOULD be safe for concurrent use by default.  
  Линки представлены как Соответствие (мутабельный тип), а не как иммутабельный объект. Нет отдельного класса Link с документацией о потокобезопасности. (`src/Трассировка/Классы/ОтелСпан.os:372`)

- ❌ **[Trace Api]** [SHOULD] If the Span in the parent Context is already non-recording, it SHOULD be returned directly without instantiating a new Span.  
  В текущей реализации всегда создается новый ОтелНоопСпан, даже если родительский спан уже является non-recording. Оптимизация возврата существующего non-recording спана не реализована. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() является процедурой (void), не возвращает статус успеха/неуспеха/таймаута. Асинхронный вариант СброситьБуферАсинхронно() возвращает Обещание, но синхронный не сообщает о результате. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98-102`)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  Метод СброситьБуфер() не имеет механизма таймаута. Асинхронный вариант через Обещание поддерживает таймаут, но синхронный метод не имеет ограничения по времени. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98-102`)

- ❌ **[Trace Sdk]** [SHOULD NOT] Span Exporter SHOULD NOT receive them unless the Sampled flag was also set.  
  Нет фильтрации RECORD_ONLY спанов между процессором и экспортером. Спаны с IsRecording=true и Sampled=false (RECORD_ONLY) проходят через процессор и попадают в экспортер. (-)

- ❌ **[Trace Sdk]** [SHOULD NOT] Span Exporters SHOULD NOT receive the ones that do not have Sampled flag set.  
  Нет фильтрации спанов без флага Sampled перед экспортером. RECORD_ONLY спаны передаются экспортеру без проверки флага. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] Samplers SHOULD normally return the passed-in Tracestate if they do not intend to change it.  
  Семплер ОтелСэмплер.ДолженСэмплировать() создает новый пустой ОтелРезультатСэмплирования без передачи входного TraceState. Компенсируется в ОтелТрассировщик.ОпределитьСостояниеТрассировки() через fallback на родительский TraceState, но сам семплер не возвращает переданный TraceState. (`src/Трассировка/Модули/ОтелСэмплер.os:155`)

- ⚠️ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values.  
  TraceID генерируется через УникальныйИдентификатор (UUID v4), что обеспечивает случайность, но нет явного соответствия W3C Trace Context Level 2 - младшие 7 байт (56 бит) не гарантированно случайны в UUID v4 (6 бит зарезервированы под version/variant). (`src/Ядро/Модули/ОтелУтилиты.os:78-92`)

- ❌ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD set the Random flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements.  
  Флаг Random (бит 1 TraceFlags) не устанавливается. ВычислитьФлагиТрассировки() устанавливает только бит Sampled (0 или 1), бит Random никогда не выставляется. (-)

- ❌ **[Trace Sdk]** [SHOULD] If the SDK uses an IdGenerator extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated.  
  SDK имеет расширение IdGenerator (ОтелУтилиты.УстановитьГенераторИд), но генератор не может влиять на установку флага Random. Флаг Random вообще не поддерживается в SDK. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] The name of the configuration options SHOULD be EventCountLimit and LinkCountLimit.  
  Опции называются МаксСобытий и МаксЛинков (русские эквиваленты). Семантически соответствуют EventCountLimit и LinkCountLimit, но имена не совпадают буквально со спецификацией. (`src/Трассировка/Классы/ОтелЛимитыСпана.os:34`)

- ⚠️ **[Trace Sdk]** [SHOULD] Shutdown SHOULD be called only once for each SpanProcessor instance. After the call to Shutdown, subsequent calls to OnStart, OnEnd, or ForceFlush are not allowed. SDKs SHOULD ignore these calls gracefully, if possible.  
  BatchProcessor устанавливает Закрыт = Истина и Обработать() проверяет флаг (строка 43), но ПростойПроцессорСпанов не имеет флага Закрыт и не игнорирует последующие вызовы ПриЗавершении/СброситьБуфер после Закрыть(). (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:74`)

- ❌ **[Trace Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод Закрыть() является процедурой (Void), не возвращает результат. Ни ОтелПростойПроцессорСпанов.Закрыть(), ни ОтелБазовыйПакетныйПроцессор.Закрыть() не сообщают вызывающему коду об успехе, неудаче или таймауте. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] Shutdown SHOULD complete or abort within some timeout.  
  Пакетный процессор ожидает фоновый экспорт с таймаутом (ТаймаутЭкспортаМс, строка 192), но ЭкспортироватьВсеПакеты() (строка 77) не имеет таймаута - может зависнуть при медленном экспортере. Простой процессор также не имеет таймаута. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192`)

- ⚠️ **[Trace Sdk]** [SHOULD] Shutdown SHOULD be called only once for each SpanProcessor instance. SDKs SHOULD ignore subsequent calls gracefully.  
  ОтелБазовыйПакетныйПроцессор устанавливает Закрыт = Истина, но повторный вызов Закрыть() снова выполнит ЭкспортироватьВсеПакеты() и Экспортер.Закрыть(). Нет раннего выхода при Закрыт = Истина в самом методе Закрыть(). (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:75`)

- ❌ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() является процедурой (Void) и не возвращает результат об успехе, неудаче или таймауте. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() вызывает ЭкспортироватьВсеПакеты() без таймаута - при медленном экспортере может зависнуть. Нет параметра timeout. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68`)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() is a void procedure (Процедура) that does not return a status. The caller has no way to know whether the flush succeeded, failed, or timed out. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41`)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() has no timeout parameter or timeout mechanism. The method will block as long as the underlying export takes. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:19`)

- ⚠️ **[Logs Api]** [SHOULD] The Enabled API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response.  
  Метод Включен() документирован (назначение, параметры, возвращаемый тип), но нет явного указания, что возвращаемое значение может меняться со временем и что метод нужно вызывать каждый раз перед emit. (`src/Логирование/Классы/ОтелЛоггер.os:28`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Синхронный СброситьБуфер() - Процедура (void), не возвращает статус успеха/неудачи. Асинхронный СброситьБуферАсинхронно() возвращает Обещание, но оно не различает успех и ошибку явно. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD return some ERROR status if there is an error condition.  
  СброситьБуфер() не возвращает значение (Процедура), нет механизма возврата ERROR статуса вызывающему. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] if there is no error condition, it SHOULD return some NO ERROR status.  
  СброситьБуфер() не возвращает значение (Процедура), нет механизма возврата NO ERROR статуса вызывающему. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:107`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуферАсинхронно() возвращает Обещание с поддержкой таймаута, но синхронный СброситьБуфер() не имеет встроенного таймаута. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:131`)

- ⚠️ **[Logs Sdk]** [SHOULD NOT] OnEmit is called synchronously on the thread that emitted the LogRecord, therefore it SHOULD NOT block or throw exceptions.  
  Композитный процессор оборачивает вызовы в Попытка/Исключение (не бросает исключения), но ОтелПростойПроцессорЛогов блокирует поток через БлокировкаЭкспорта при синхронном экспорте (строка 22). Пакетный процессор добавляет в буфер без длительной блокировки. (`src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17`)

- ❌ **[Logs Sdk]** [SHOULD] Implementations SHOULD recommended to users that a clone of logRecord be used for any concurrent processing, such as in a batching processor.  
  Нет механизма клонирования ОтелЗаписьЛога и нет документации/рекомендации пользователям использовать клон при конкурентной обработке. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Асинхронная версия ЗакрытьАсинхронно() возвращает Обещание (Promise) для обратной связи, но синхронная Закрыть() на процессорах и провайдере возвращает void без индикации результата. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:143`)

- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD complete or abort within some timeout.  
  Остановка фонового экспорта использует таймаут (Обещание.Получить(ТаймаутЭкспортаМс)), но основной поток Закрыть() выполняет ЭкспортироватьВсеПакеты() без ограничения по времени. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192`)

- ⚠️ **[Logs Sdk]** [SHOULD] If any LogRecordProcessor has any associated exporter, it SHOULD try to call the exporter's Export with all LogRecords for which this was not already done and then invoke ForceFlush on it.  
  ЭкспортироватьВсеПакеты() вызывает Экспортер.Экспортировать() для всех накопленных записей, но не вызывает Экспортер.СброситьБуфер() (ForceFlush) после экспорта. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:146`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  На уровне провайдера СброситьБуферАсинхронно() возвращает Обещание (Promise), но синхронный СброситьБуфер() на процессорах возвращает void. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:131`)

- ❌ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() не имеет механизма таймаута - ЭкспортироватьВсеПакеты() выполняется без ограничения по времени и может блокироваться бесконечно. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() is a Процедура (void), not a Функция. It does not return a success/failure/timeout result to the caller. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  The exporter's СброситьБуфер() is a no-op (synchronous exporter has no buffering), so it completes instantly. However there is no explicit timeout mechanism in case a subclass buffers data. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41`)

- ⚠️ **[Logs Sdk]** [SHOULD NOT] Shutdown SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable).  
  Закрыть() simply sets Закрыт=Истина which completes instantly, so it does not block. However there is no explicit timeout guard if the method were extended. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47`)

- ⚠️ **[Metrics Api]** [SHOULD] Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying.  
  Дескрипторы инструментов хранят Вид, ЕдиницаИзмерения, Описание, но OneScript не различает int/float на уровне языка - числовой тип единый. Дескриптор не хранит тип числа как идентифицирующий признак. (`src/Метрики/Классы/ОтелМетр.os:553`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax.  
  Документация параметра Имя есть в комментариях методов, но нет явной ссылки на синтаксис имён инструментов. (`src/Метрики/Классы/ОтелМетр.os:40`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (for asynchronous instruments).  
  Документация параметра Имя есть, но нет явной ссылки на синтаксис имён инструментов. (`src/Метрики/Классы/ОтелМетр.os:216`)

- ⚠️ **[Metrics Api]** [SHOULD] Callback functions SHOULD be reentrant safe. The SDK expects to evaluate callbacks for each MetricReader independently.  
  Callbacks вызываются последовательно для каждого reader, но нет документации для пользователя о реентерабельности. (`src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160`)

- ⚠️ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT take an indefinite amount of time.  
  Нет документации для пользователя о том, что callback не должен выполняться бесконечно. Нет таймаута. (`src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160`)

- ⚠️ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT make duplicate observations (more than one Measurement with the same attributes) across all registered callbacks.  
  Нет документации для пользователя и нет проверки дубликатов наблюдений. (`src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response  
  Метод Включен() задокументирован, но комментарий описывает условия возврата Ложь (MeterConfig.enabled=false, Drop Aggregation), а не рекомендацию вызывать перед каждым измерением (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:194`)

- ⚠️ **[Metrics Api]** [SHOULD NOT] This API SHOULD NOT validate this value, that is left to implementations of the API  
  Код выполняет валидацию: Если Значение < 0 Тогда Возврат - отрицательные значения молча отбрасываются на уровне API, тогда как спецификация рекомендует оставить валидацию реализации SDK (`src/Метрики/Классы/ОтелСчетчик.os:22`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() - Процедура (void), не возвращает статус успеха/ошибки. Нет индикации результата вызывающему коду. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:115`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status.  
  СброситьБуфер() не возвращает значения (void Процедура). Не реализован механизм возврата ERROR/NO ERROR статуса. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:115`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуферАсинхронно() возвращает Обещание с поддержкой таймаута, но синхронный метод СброситьБуфер() не принимает параметр таймаута. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:152`)

- ⚠️ **[Metrics Sdk]** [SHOULD] In order to avoid conflicts, if a name is provided the View SHOULD have an instrument selector that selects at most one instrument.  
  Представление принимает имя, но SDK не предупреждает если селектор с подстановочным именем и View с именем-переименованием используются вместе - нет валидации конфликта при регистрации. (`src/Метрики/Классы/ОтелПредставление.os:4`)

- ⚠️ **[Metrics Sdk]** [SHOULD] If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning.  
  Представления применяются (строки 207-218), но нет проверки на конфликтующие метрические идентичности между несколькими View и нет предупреждений при конфликтах. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:202-220`)

- ⚠️ **[Metrics Sdk]** [SHOULD] If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asynchronous instrument to use the Explicit bucket histogram aggregation) the implementation SHOULD emit a warning and proceed as if the View did not exist.  
  Нет валидации совместимости агрегации View с типом инструмента. SDK не проверяет семантические ошибки при применении View. (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] Histogram Aggregations: Arithmetic sum of Measurement values in population. This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. UpDownCounter or ObservableGauge).  
  ОтелАгрегаторГистограммы.Записать() безусловно суммирует все значения через Аккумулятор.Получить('sum').ПолучитьИДобавить(Значение) - нет проверки на отрицательные значения или тип инструмента. (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the sum, min, and max fields.  
  OneScript не имеет IEEE +Inf/-Inf/NaN как стандартных значений, но в ОтелАгрегаторЭкспоненциальнойГистограммы.Записать() нет явной проверки на ненормальные значения. (-)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks.  
  Нет механизма контроля использования асинхронных инструментов вне callback. ОтелБазовыйНаблюдаемыйИнструмент не проверяет контекст вызова. (-)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback execution.  
  В ОтелБазовыйНаблюдаемыйИнструмент.ВызватьCallbackИСобрать() callbacks выполняются синхронно без таймаута. Есть try-catch для ошибок, но нет ограничения по времени. (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback.  
  В ОтелБазовыйНаблюдаемыйИнструмент.ВызватьCallbackИСобрать() все записи из callback добавляются к результату, а ВнешниеНаблюдения очищаются (строка 174), но нет фильтрации ранее наблюдаемых наборов атрибутов - каждый вызов callback создает новый набор точек данных. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] A view with criteria matching the instrument an aggregation is created for has an aggregation_cardinality_limit value defined for the stream, that value SHOULD be used.  
  View (ОтелПредставление) has ЛимитМощностиАгрегации property, but ПрименитьПредставлениеКИнструменту in ОтелМетр.os:515 does not apply this limit to the instrument's УстановитьЛимитМощности - only attribute keys and reservoir are applied from View (`src/Метрики/Классы/ОтелПредставление.os:92`)

- ❌ **[Metrics Sdk]** [SHOULD] If there is no matching view, but the MetricReader defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used.  
  ОтелПериодическийЧитательМетрик does not have any cardinality limit configuration. Only the Meter/instrument-level default of 2000 exists. (-)

- ❌ **[Metrics Sdk]** [SHOULD] Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality.  
  ОтелБазовыйНаблюдаемыйИнструмент has no cardinality limiting at all. ВызватьCallbackИСобрать converts all callback records to data points without any limit or overflow handling. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible.  
  Warning describes the conflict (old vs new params) but does not include advice on how to resolve it, such as suggesting the use of Views for renaming or setting description. (`src/Метрики/Классы/ОтелМетр.os:573`)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves multiple description properties, setting the description through a configured View SHOULD avoid the warning.  
  ПроверитьКонфликтДескриптора treats description mismatch as a conflict regardless of whether a View is configured to resolve it. No check is made for whether a matching View resolves the description difference. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning.  
  The warning message does not include any View recipe or suggestion about how to use Views to rename instruments to resolve the conflict. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both Metric objects and emit a generic warning describing the duplicate instrument registration.  
  A warning is emitted for duplicate registration, but the SDK returns the first-seen instrument instead of reporting both Metric objects. Only one Metric stream is exported, not two. (`src/Метрики/Классы/ОтелМетр.os:54`)

- ❌ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax.  
  No instrument name validation is performed in any of the instrument creation methods (СоздатьСчетчик, СоздатьГистограмму, etc.). Names are only lowercased for duplicate detection but not validated against the syntax rules. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name.  
  No error is emitted for invalid instrument names since no validation is performed. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] The 'offer' method SHOULD have the ability to pull associated trace and span information without needing to record full context.  
  The offer method (Предложить) accepts КонтекстСпана directly rather than full Context - span/trace info is extracted before calling the reservoir in ОтелБазовыйСинхронныйИнструмент.ЗахватитьЭкземпляр. This is functionally equivalent but the reservoir itself doesn't pull from context. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39`)

- ❌ **[Metrics Sdk]** [SHOULD] The ExemplarReservoir SHOULD avoid allocations when sampling exemplars.  
  ОтелРезервуарЭкземпляров creates new Соответствие objects for each exemplar in СоздатьЭкземпляр and new arrays for filtered attributes - no object reuse or pre-allocation strategy is implemented. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] The 'offer' method MAY accept a filtered subset of Attributes which diverge from the timeseries the reservoir is associated with.  
  The offer method accepts both АтрибутыИзмерения and АтрибутыСерии and computes filtered attributes internally - but the spec says this MUST be clearly documented and the reservoir given timeseries attributes at construction. The API documentation does not explicitly call this out. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39`)

- ⚠️ **[Metrics Sdk]** [SHOULD] This implementation SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled.  
  Реализация использует стратегию 'последнее измерение заменяет предыдущее' (last-seen), а не reservoir sampling. Спецификация допускает это как альтернативу (MAY instead keep the last seen measurement), но SHOULD указывает на предпочтительность равномерного алгоритма. (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50`)

- ⚠️ **[Metrics Sdk]** [SHOULD] Collect SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() (Collect/ForceFlush) является процедурой без возвращаемого значения. Caller не получает информации об успехе, ошибке или таймауте. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71`)

- ❌ **[Metrics Sdk]** [SHOULD] Collect SHOULD invoke Produce on registered MetricProducers.  
  Нет концепции MetricProducer как отдельной сущности. MetricReader собирает данные только из зарегистрированных Meter'ов SDK, но не поддерживает внешние MetricProducer'ы. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] After the call to Shutdown, subsequent invocations to Collect are not allowed. SDKs SHOULD return some failure for these calls, if possible.  
  После Закрыть() флаг Закрыт устанавливается в Истина и фоновое задание останавливается. Однако метод СброситьБуфер() (Collect) не проверяет флаг Закрыт и не возвращает ошибку при вызове после shutdown. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:59`)

- ⚠️ **[Metrics Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод Закрыть() является процедурой без возвращаемого значения. Ошибки обрабатываются внутри через логирование, но caller не получает явного статуса результата. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() (ForceFlush) является процедурой без возвращаемого значения. Caller не получает информации об успехе или неудаче. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status.  
  Метод СброситьБуфер() не возвращает статус. Ошибки перехватываются и логируются, но не передаются вызывающему коду. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71`)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  ForceFlush (СброситьБуфер) не имеет механизма таймаута. Метод выполняется синхронно без ограничения по времени. (-)

- ❌ **[Metrics Sdk]** [SHOULD] Metric Exporters SHOULD report an error condition for data output by the MetricReader with unsupported Aggregation or Aggregation Temporality.  
  Экспортер не проверяет и не сообщает об ошибках для неподдерживаемых типов агрегации или временности. Экспортер просто сериализует и отправляет данные без валидации. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() экспортера является процедурой без возвращаемого значения. Вызывающий код не получает информации об успехе или неудаче. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43`)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  Метод СброситьБуфер() экспортера метрик не имеет таймаута. Для синхронного экспортера это не критично (он не буферизует), но формально таймаут отсутствует. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD NOT] Shutdown SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable).  
  Метод Закрыть() экспортера просто ставит флаг Закрыт = Истина и не блокируется. Однако нет явного механизма таймаута, если бы Shutdown включал flush операцию. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49`)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed metrics.  
  Это рекомендация по использованию, а не по реализации. Нет документации или предупреждения о том, что ForceFlush не должен вызываться часто. (-)

- ❌ **[Metrics Sdk]** [SHOULD] MetricProducer implementations SHOULD accept configuration for the AggregationTemporality of produced metrics.  
  There is no MetricProducer interface or implementation that accepts AggregationTemporality configuration. The ОтелПрометеусЧитательМетрик (pull reader) does not accept temporality configuration - it always produces cumulative data for Prometheus. The temporality selector exists on the exporter (ОтелЭкспортерМетрик) but not on any MetricProducer. (-)

- ⚠️ **[Otlp Exporter]** [SHOULD] The default protocol SHOULD be http/protobuf, unless there are strong reasons for SDKs to select grpc as the default.  
  Default protocol is set to 'http/json' (line 150: Менеджер.Параметр("otel.exporter.otlp.protocol", "http/json")), not the recommended 'http/protobuf'. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ⚠️ **[Otlp Exporter]** [SHOULD] SDKs SHOULD support both grpc and http/protobuf transports.  
  grpc is supported via ОтелGrpcТранспорт (protobuf encoding). HTTP transport exists (ОтелHttpТранспорт) but sends JSON, not protobuf. So http/protobuf is not truly supported - only grpc and http/json. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If SDKs support only one transport, it SHOULD be http/protobuf.  
  The SDK supports two transports (grpc and http/json). However, http/protobuf is not truly supported - the HTTP transport always sends JSON. The spec recommends http/protobuf as the preferred single transport. (`src/Экспорт/Классы/ОтелHttpТранспорт.os:53`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If no configuration is provided the default transport SHOULD be http/protobuf unless SDKs have good reasons to choose grpc as the default.  
  Default protocol is 'http/json' (not 'http/protobuf'). Line 150: Менеджер.Параметр("otel.exporter.otlp.protocol", "http/json"). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ❌ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter.  
  No User-Agent header is set anywhere in ОтелHttpТранспорт or ОтелGrpcТранспорт. The HTTP transport sets Content-Type and optionally Content-Encoding headers, but not User-Agent. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The format of the User-Agent header SHOULD follow RFC 7231.  
  User-Agent header is not emitted at all, so RFC 7231 format compliance is moot. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The resulting User-Agent SHOULD include the exporter's default User-Agent string when a product identifier is added.  
  User-Agent header is not emitted at all, so there is no default User-Agent string to preserve. (-)

- ⚠️ **[Env Vars]** [SHOULD] They SHOULD also follow the common configuration specification.  
  Используется configor (МенеджерПараметров) для чтения параметров, но не все аспекты common configuration specification реализованы (например, programmatic override, layered configuration). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:59`)

- ❌ **[Env Vars]** [SHOULD] If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied.  
  Нет логирования предупреждения при получении некорректного булева значения. Функция Включено() (строка 561-564) молча возвращает Ложь для любого не-true значения без предупреждения. (-)

- ❌ **[Env Vars]** [SHOULD] All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior.  
  Используется OTEL_ENABLED (по умолчанию true = включен) вместо спецификационной OTEL_SDK_DISABLED (по умолчанию false = включен). Спецификация требует, чтобы false было безопасным значением по умолчанию, но OTEL_ENABLED=false отключает SDK, а спецификация предусматривает OTEL_SDK_DISABLED=false для включённого состояния. (-)

- ❌ **[Env Vars]** [SHOULD] For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them as not set.  
  Числовые значения парсятся через Число() без обёртки в Попытка/Исключение (строки 224-227, 263-266, 312, 399-416). При некорректном значении возникает необработанное исключение вместо предупреждения и использования значения по умолчанию. (-)

- ❌ **[Env Vars]** [SHOULD] For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD gracefully ignore the setting, i.e., treat them as not set.  
  При непарсящемся числовом значении Число() выбрасывает исключение вместо того, чтобы молча использовать значение по умолчанию. Нет try/catch обёртки вокруг вызовов Число() для env-var параметров. (-)

- ⚠️ **[Env Vars]** [SHOULD] Enum values SHOULD be interpreted in a case-insensitive manner.  
  Пропагаторы (строка 344: НРег()) и фильтр экземпляров (ОтелПостроительПровайдераМетрик.os:115: НРег()) сравниваются case-insensitive. Однако имена сэмплеров (строки 197-218: прямое сравнение "always_on", "always_off" и т.д.) и имена экспортеров (строки 177, 255, 291: прямое сравнение "none", "otlp") НЕ используют case-insensitive сравнение. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:344`)

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
| 7 | MUST | ✅ found | The API MUST accept the following parameters: The Context and the key | `src/Ядро/Модули/ОтелКонтекст.os:113` |  |
| 8 | MUST | ✅ found | The API MUST return the value in the Context for the specified key | `src/Ядро/Модули/ОтелКонтекст.os:114` |  |

#### Set value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | The API MUST accept the following parameters: The Context, the key, and the value to be set | `src/Ядро/Модули/ОтелКонтекст.os:127` |  |
| 10 | MUST | ✅ found | The API MUST return a new Context containing the new value | `src/Ядро/Модули/ОтелКонтекст.os:130` |  |

#### Optional Global operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#optional-global-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | These operations SHOULD only be used to implement automatic scope switching and define higher level APIs by SDK components and OpenTelemetry instrumentation libraries | `src/Ядро/Модули/ОтелКонтекст.os:63` |  |

#### Get current Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-current-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST return the Context associated with the caller's current execution unit | `src/Ядро/Модули/ОтелКонтекст.os:63` |  |

#### Attach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#attach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ⚠️ partial | The API MUST accept the following parameters: The Context. | `src/Ядро/Модули/ОтелКонтекст.os:203` | Нет функции Attach, принимающей готовый объект Context. Вместо этого УстановитьЗначение(Ключ, Значение) принимает ключ и значение, строит новый контекст внутри и помещает в стек. СделатьСпанТекущим/СделатьBaggageТекущим - специализированные обёртки, тоже не принимают Context целиком. |
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
| 6 | MUST | ✅ found | The Baggage container MUST be immutable, so that the containing Context also remains immutable. | `src/Ядро/Классы/ОтелBaggage.os:154` |  |

#### Operations### Get Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#operations-get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The Baggage API MUST provide a function that takes the name as input, and returns a value associated with the given name, or null if the given name is not present. | `src/Ядро/Классы/ОтелBaggage.os:38` |  |

#### Get All Values

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#get-all-values)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST NOT | ✅ found | The order of name/value pairs MUST NOT be significant. | `src/Ядро/Классы/ОтелBaggage.os:103` |  |

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
| 11 | MUST | ✅ found | If an implementation of this API does not operate directly on the Context, it MUST provide the following functionality to interact with a Context instance: Extract the Baggage from a Context instance, Insert the Baggage to a Context instance. | `src/Ядро/Модули/ОтелКонтекст.os:156` |  |
| 12 | SHOULD NOT | ⚠️ partial | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:53` | Convenience methods BaggageИзКонтекста() and КонтекстСBaggage() exist so users don't need the key directly, but КлючBaggage() is exposed as a public export method, giving users direct access to the Context Key. |
| 13 | SHOULD | ✅ found | If the language has support for implicitly propagated Context, the API SHOULD also provide the following functionality: Get the currently active Baggage from the implicit context, Set the currently active Baggage to the implicit context. | `src/Ядро/Классы/ОтелBaggage.os:16` |  |
| 14 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:187` |  |

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
| 17 | MUST | ✅ found | If a new name/value pair is added and its name is the same as an existing name, then the new pair MUST take precedence. The value is replaced with the added value (regardless of whether it is locally generated or received from a remote peer). | `src/Ядро/Классы/ОтелПостроительBaggage.os:23` |  |

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
| 3 | MUST | ✅ found | The SDK MUST provide access to a Resource with at least the attributes listed at Semantic Attributes with SDK-provided Default Value (service.name, telemetry.sdk.name, telemetry.sdk.language, telemetry.sdk.version). | `src/Ядро/Классы/ОтелРесурс.os:102` |  |
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
| 9 | MUST | ⚠️ partial | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1` | Detectors exist as separate classes (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) but they are part of the same package (registered in the same lib.config), not implemented as separate packages from the SDK. |
| 10 | MUST | ✅ found | Resource detector packages MUST provide a method that returns a resource. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17` |  |
| 11 | MUST NOT | ✅ found | The failure to detect any resource information MUST NOT be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:19` |  |
| 12 | SHOULD | ✅ found | An error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:24` |  |
| 13 | MUST | ❌ not_found | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions. | - | Detectors (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) create resources with Новый ОтелРесурс(Истина) which sets empty АдресСхемы, but they populate semantic convention attributes (host.name, os.type, process.pid, host.arch) without setting a matching Schema URL. |
| 14 | SHOULD | ⚠️ partial | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18` | Detectors use empty schema URL (via Новый ОтелРесурс(Истина)), but they DO populate known semantic convention attributes (host.name, os.type, etc.), so they should set a schema URL rather than leaving it empty. |
| 15 | MUST | ❌ not_found | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources. | - | In ОтелРесурс.ЗаполнитьАтрибутыПоУмолчанию() (line 108-118), detectors are combined by iterating and copying attributes directly without using Merge. There is no check for conflicting non-empty Schema URLs between detectors. |

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
| 3 | MUST | ✅ found | The TracerProvider MUST provide the following functions: Get a Tracer. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 4 | MUST | ✅ found | This API MUST accept the following parameters: name (required). | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 5 | SHOULD | ✅ found | The name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library. | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:93` |  |
| 6 | MUST | ⚠️ partial | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` | ПолучитьТрассировщик не проверяет ИмяБиблиотеки на пустую строку или Неопределено - просто создает трассировщик с любым именем. Работает как fallback, но нет явной валидации и логирования предупреждения. |
| 7 | SHOULD | ❌ not_found | Its name property SHOULD be set to an empty string (when invalid name specified). | - | Нет проверки на невалидное имя - имя просто передается как есть в ОбластьИнструментирования без корректировки на пустую строку. |
| 8 | SHOULD | ❌ not_found | A message reporting that the specified value is invalid SHOULD be logged (when invalid name specified). | - | Нет логирования предупреждения при передаче невалидного имени в ПолучитьТрассировщик. |
| 9 | MUST NOT | ✅ found | Implementations MUST NOT require users to repeatedly obtain a Tracer again with the same identity to pick up configuration changes. | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API MUST provide the following functionality to interact with a Context instance: Extract the Span from a Context instance; Combine the Span with a Context instance, creating a new Context instance. | `src/Ядро/Модули/ОтелКонтекст.os:141` |  |
| 11 | SHOULD NOT | ✅ found | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:362` |  |
| 12 | SHOULD | ✅ found | If the language has support for implicitly propagated Context, the API SHOULD also provide: Get the currently active span from the implicit context; Set the currently active span into a new context, and make that the implicit context. | `src/Ядро/Модули/ОтелКонтекст.os:90` |  |
| 13 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### SpanContext

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spancontext)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The API MUST implement methods to create a SpanContext. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |
| 15 | SHOULD | ✅ found | These methods SHOULD be the only way to create a SpanContext. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |
| 16 | MUST | ✅ found | This functionality MUST be fully implemented in the API. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:1` |  |
| 17 | SHOULD NOT | ✅ found | This functionality SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:1` |  |

#### Retrieving the TraceId and SpanId

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#retrieving-the-traceid-and-spanid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | The API MUST allow retrieving the TraceId and SpanId in Hex and Binary forms. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 19 | MUST | ✅ found | Hex TraceId result MUST be a 32-hex-character lowercase string. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 20 | MUST | ✅ found | Hex SpanId result MUST be a 16-hex-character lowercase string. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:32` |  |
| 21 | MUST | ✅ found | Binary TraceId result MUST be a 16-byte array. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:82` |  |
| 22 | MUST | ✅ found | Binary SpanId result MUST be an 8-byte array. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:91` |  |
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
| 27 | MUST | ✅ found | For the SpanContext of any child spans, IsRemote MUST return false. | `src/Трассировка/Классы/ОтелСпан.os:600` |  |

#### TraceState

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracestate)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | Tracing API MUST provide at least the following operations on TraceState: Get value for a given key, Add a new key/value pair, Update an existing value for a given key, Delete a key/value pair | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:44,66,105` |  |
| 29 | MUST | ✅ found | These operations MUST follow the rules described in the W3C Trace Context specification | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:227-386` |  |
| 30 | MUST | ✅ found | All mutating operations MUST return a new TraceState with the modifications applied | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:92-94,114-116` |  |
| 31 | MUST | ✅ found | TraceState MUST at all times be valid according to rules specified in W3C Trace Context specification | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:220,227-386` |  |
| 32 | MUST | ✅ found | Every mutating operations MUST validate input parameters | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 33 | MUST NOT | ✅ found | If invalid value is passed the operation MUST NOT return TraceState containing invalid data | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67-68` |  |
| 34 | MUST | ✅ found | If invalid value is passed the operation MUST follow the general error handling guidelines | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:68` |  |

#### Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | SHOULD | ⚠️ partial | The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable | - | Это рекомендация по использованию API, а не по реализации. API принимает строковое имя через параметр ИмяСпана, но нет валидации на общность имени. Реализация partial - нет принудительного соблюдения. |
| 36 | SHOULD | ⚠️ partial | Generality SHOULD be prioritized over human-readability | - | Рекомендация по использованию API. API принимает произвольную строку, нет механизма для принуждения к общности. Реализация partial - нет принудительного соблюдения. |
| 37 | SHOULD | ✅ found | A Span's start time SHOULD be set to the current time on span creation | `src/Трассировка/Классы/ОтелСпан.os:609` |  |
| 38 | SHOULD | ✅ found | After the Span is created, it SHOULD be possible to change its name, set its Attributes, add Events, and set the Status | `src/Трассировка/Классы/ОтелСпан.os:247,263,293,413` |  |
| 39 | MUST NOT | ✅ found | These MUST NOT be changed after the Span's end time has been set | `src/Трассировка/Классы/ОтелСпан.os:248,264,294,414,448` |  |
| 40 | SHOULD NOT | ✅ found | Implementations SHOULD NOT provide access to a Span's attributes besides its SpanContext | `src/Трассировка/Классы/ОтелСпан.os:134` |  |
| 41 | MUST NOT | ✅ found | Alternative implementations MUST NOT allow callers to create Spans directly | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 42 | MUST | ✅ found | All Spans MUST be created via a Tracer | `src/Трассировка/Классы/ОтелТрассировщик.os:56,106,133` |  |

#### Span Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Span other than with a Tracer | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 44 | MUST NOT | ✅ found | In languages with implicit Context propagation, Span creation MUST NOT set the newly created Span as the active Span in the current Context by default | `src/Трассировка/Классы/ОтелТрассировщик.os:56-94` |  |
| 45 | MUST | ✅ found | The API MUST accept the following parameters: The span name (required parameter) | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 46 | MUST NOT | ⚠️ partial | This API MUST NOT accept a Span or SpanContext as parent, only a full Context | `src/Трассировка/Классы/ОтелТрассировщик.os:133-137` | НачатьДочернийСпан принимает как ОтелСпан, так и ОтелКонтекстСпана в качестве родителя (строка 134). Спецификация требует принимать только полный Context, а не Span или SpanContext. Однако НачатьСпан() без явного родителя использует неявный контекст (строка 57), что соответствует спецификации. |
| 47 | MUST | ✅ found | The semantic parent of the Span MUST be determined according to the rules described in Determining the Parent Span from a Context | `src/Трассировка/Классы/ОтелТрассировщик.os:57-69` |  |
| 48 | MUST | ✅ found | The API documentation MUST state that adding attributes at span creation is preferred to calling SetAttribute later, as samplers can only consider information already present during span creation | `src/Трассировка/Классы/ОтелПостроительСпана.os:66-67` |  |
| 49 | SHOULD | ✅ found | Start timestamp, default to current time. This argument SHOULD only be set when span creation time has already passed | `src/Трассировка/Классы/ОтелПостроительСпана.os:109` |  |
| 50 | MUST NOT | ✅ found | If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument | `src/Трассировка/Классы/ОтелПостроительСпана.os:100-112` |  |
| 51 | MUST | ✅ found | Implementations MUST provide an option to create a Span as a root span | `src/Трассировка/Классы/ОтелТрассировщик.os:106` |  |
| 52 | MUST | ✅ found | Implementations MUST generate a new TraceId for each root span created | `src/Трассировка/Классы/ОтелТрассировщик.os:107` |  |
| 53 | MUST | ✅ found | For a Span with a parent, the TraceId MUST be the same as the parent | `src/Трассировка/Классы/ОтелТрассировщик.os:61,140` |  |
| 54 | MUST | ✅ found | The child span MUST inherit all TraceState values of its parent by default | `src/Трассировка/Классы/ОтелТрассировщик.os:78,148,230-238` |  |
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
| 58 | MUST | ✅ found | The returned value MUST be the same for the entire Span lifetime | `src/Трассировка/Классы/ОтелСпан.os:80,600` |  |
| 59 | SHOULD | ✅ found | After a Span is ended, it SHOULD become non-recording and IsRecording SHOULD always return false | `src/Трассировка/Классы/ОтелСпан.os:234-236` |  |
| 60 | SHOULD NOT | ✅ found | IsRecording SHOULD NOT take any parameters | `src/Трассировка/Классы/ОтелСпан.os:234` |  |
| 61 | SHOULD | ✅ found | This flag SHOULD be used to avoid expensive computations of a Span attributes or events in case when a Span is definitely not recorded | `src/Трассировка/Классы/ОтелПостроительСпана.os:129-131` |  |
| 62 | SHOULD | ✅ found | After a Span is ended, IsRecording SHOULD always return false | `src/Трассировка/Классы/ОтелСпан.os:234-236` |  |

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
| 72 | SHOULD | ⚠️ partial | This SHOULD be called SetStatus. | `src/Трассировка/Классы/ОтелСпан.os:413` | Метод называется УстановитьСтатус, что является русскоязычным эквивалентом SetStatus. Допустимо для русскоязычного SDK, но не точное имя из спецификации. |
| 73 | MUST | ✅ found | Description MUST be IGNORED for StatusCode Ok & Unset values. | `src/Трассировка/Классы/ОтелСпан.os:431` |  |
| 74 | SHOULD | ❌ not_found | The status code SHOULD remain unset, except for the following circumstances. | - | Это рекомендация для инструментирующих библиотек. SDK не контролирует это поведение напрямую, но и не документирует как рекомендацию. |
| 75 | SHOULD | ✅ found | An attempt to set value Unset SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:424` |  |
| 76 | SHOULD | ❌ not_found | When the status is set to Error by Instrumentation Libraries, the Description SHOULD be documented and predictable. | - | Это рекомендация для инструментирующих библиотек, не для SDK. Нет документации о стандартных Description для Error. |
| 77 | SHOULD | ❌ not_found | For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish their own conventions, including possible values of Description and what they mean. | - | Рекомендация для авторов инструментирующих библиотек. Нет опубликованных конвенций. |
| 78 | SHOULD NOT | ❌ not_found | Generally, Instrumentation Libraries SHOULD NOT set the status code to Ok, unless explicitly configured to do so. | - | Рекомендация для инструментирующих библиотек. SDK не ограничивает установку Ok. |
| 79 | SHOULD | ❌ not_found | Instrumentation Libraries SHOULD leave the status code as Unset unless there is an error. | - | Рекомендация для инструментирующих библиотек. SDK не документирует данное руководство. |
| 80 | SHOULD | ✅ found | When span status is set to Ok it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 81 | SHOULD | ✅ found | Any further attempts to change Ok status SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 82 | SHOULD | ❌ not_found | Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generate. | - | Рекомендация для инструментов анализа, а не SDK. В коде нет обработки подавления ошибок на основе Ok-статуса. |

#### UpdateName

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#updatename)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 83 | SHOULD | ✅ found | Implementations SHOULD ignore all subsequent calls to End and any other Span methods, i.e. the Span becomes non-recording by being ended. | `src/Трассировка/Классы/ОтелСпан.os:448` |  |
| 84 | MUST | ✅ found | However, all API implementations of such methods MUST internally call the End method and be documented to do so. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 85 | MUST NOT | ✅ found | End MUST NOT have any effects on child spans. Those may still be running and can be ended later. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 86 | MUST NOT | ✅ found | End MUST NOT inactivate the Span in any Context it is active in. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 87 | MUST | ✅ found | It MUST still be possible to use an ended span as parent via a Context it is contained in. Also, any mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:398` |  |
| 88 | MUST | ✅ found | Also, any mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:398` |  |
| 89 | MUST | ✅ found | If omitted, this MUST be treated equivalent to passing the current time (optional end timestamp parameter). | `src/Трассировка/Классы/ОтелСпан.os:449` |  |
| 90 | MUST NOT | ✅ found | This operation itself MUST NOT perform blocking I/O on the calling thread. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 91 | SHOULD | ⚠️ partial | Any locking used needs be minimized and SHOULD be removed entirely if possible. | `src/Трассировка/Классы/ОтелСпан.os:447` | Метод Завершить не использует блокировок напрямую, но вызывает Процессор.ПриЗавершении который может содержать блокировки (ОтелПростойПроцессорСпанов использует БлокировкаРесурса). Блокировки минимизированы, но не удалены. |

#### Record Exception

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#record-exception)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 92 | SHOULD | ✅ found | To facilitate recording an exception languages SHOULD provide a RecordException method if the language uses exceptions. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 93 | MUST | ✅ found | The method MUST record an exception as an Event with the conventions outlined in the exceptions document. | `src/Трассировка/Классы/ОтелСпан.os:322` |  |
| 94 | SHOULD | ✅ found | The minimum required argument SHOULD be no more than only an exception object. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 95 | MUST | ✅ found | If RecordException is provided, the method MUST accept an optional parameter to provide any additional event attributes. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 96 | SHOULD | ✅ found | This SHOULD be done in the same way as for the AddEvent method (accepting additional attributes). | `src/Трассировка/Классы/ОтелСпан.os:340` |  |

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
| 99 | SHOULD NOT | ⚠️ partial | If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | ОтелНоопСпан является публичным классом, зарегистрированным в lib.config. Спецификация рекомендует не экспонировать тип публично, если возможно. |
| 100 | SHOULD | ⚠️ partial | If a new type is required to be publicly exposed, it SHOULD be named NonRecordingSpan. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | Класс назван ОтелНоопСпан (NoopSpan), а не NonRecordingSpan, хотя он фактически является non-recording span. |
| 101 | MUST | ✅ found | GetContext MUST return the wrapped SpanContext. | `src/Трассировка/Классы/ОтелНоопСпан.os:30` |  |
| 102 | MUST | ✅ found | IsRecording MUST return false to signal that events, attributes and other elements are not being recorded, i.e. they are being dropped. | `src/Трассировка/Классы/ОтелНоопСпан.os:155` |  |
| 103 | MUST | ✅ found | The remaining functionality of Span MUST be defined as no-op operations. | `src/Трассировка/Классы/ОтелНоопСпан.os:167` |  |
| 104 | MUST | ✅ found | This functionality MUST be fully implemented in the API. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |
| 105 | SHOULD NOT | ✅ found | This functionality SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |

#### SpanKind

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 106 | SHOULD | ❌ not_found | In order for SpanKind to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose. | - | Рекомендация для авторов инструментирующего кода. SDK не обеспечивает проверку или документацию данного ограничения. |
| 107 | SHOULD NOT | ❌ not_found | A server-side span SHOULD NOT be used to describe outgoing remote procedure call. | - | Рекомендация для авторов инструментирующего кода. SDK не контролирует правильность использования SpanKind. |
| 108 | MUST | ✅ found | A user MUST have the ability to record links to other SpanContexts. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 109 | MUST | ✅ found | The API MUST provide an API to record a single Link where the Link properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 110 | SHOULD | ✅ found | Implementations SHOULD record links containing SpanContext with empty TraceId or SpanId (all zeros) as long as either the attribute set or TraceState is non-empty. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 111 | SHOULD | ✅ found | Span SHOULD preserve the order in which Links are set. | `src/Трассировка/Классы/ОтелСпан.os:613` |  |
| 112 | MUST | ❌ not_found | The API documentation MUST state that adding links at span creation is preferred to calling AddLink later, for contexts that are available during span creation, because head sampling decisions can only consider information present during span creation. | - | В документации SpanBuilder.ДобавитьЛинк есть комментарий о предпочтительности, но в API документации Span.ДобавитьЛинк нет явного указания, что добавление линков при создании предпочтительнее. |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 113 | MUST | ✅ found | TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:6` |  |
| 114 | MUST | ✅ found | Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:3` |  |
| 115 | MUST | ✅ found | Span - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:3` |  |
| 116 | MUST | ✅ found | Event - Events are immutable and MUST be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСобытиеСпана.os:3` |  |
| 117 | SHOULD | ⚠️ partial | Link - Links are immutable and SHOULD be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:372` | Линки представлены как Соответствие (мутабельный тип), а не как иммутабельный объект. Нет отдельного класса Link с документацией о потокобезопасности. |

#### Behavior of the API in the absence of an installed SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#behavior-of-the-api-in-the-absence-of-an-installed-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 118 | MUST | ⚠️ partial | The API MUST return a non-recording Span with the SpanContext in the parent Context (whether explicitly given or implicit current). | `src/Трассировка/Классы/ОтелТрассировщик.os:71` | Трассировщик возвращает ОтелНоопСпан когда семплер отбрасывает спан, сохраняя traceId из родителя. Но нет отдельного API-уровня без SDK - API и SDK объединены, поведение без установленного SDK не определено как отдельный режим. |
| 119 | SHOULD | ❌ not_found | If the Span in the parent Context is already non-recording, it SHOULD be returned directly without instantiating a new Span. | - | В текущей реализации всегда создается новый ОтелНоопСпан, даже если родительский спан уже является non-recording. Оптимизация возврата существующего non-recording спана не реализована. |
| 120 | MUST | ✅ found | If the parent Context contains no Span, an empty non-recording Span MUST be returned instead (i.e., having a SpanContext with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags). | `src/Трассировка/Классы/ОтелНоопСпан.os:277` |  |

### Trace Sdk

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, Sampler, and TracerConfigurator) MUST be owned by the TracerProvider. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:9-28` |  |
| 2 | MUST | ✅ found | If configuration is updated (e.g., adding a SpanProcessor), the updated configuration MUST also apply to all already returned Tracers. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:80-85` |  |
| 3 | MUST NOT | ✅ found | It MUST NOT matter whether a Tracer was obtained from the TracerProvider before or after the configuration change. | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98-102` | Метод СброситьБуфер() является процедурой (void), не возвращает статус успеха/неуспеха/таймаута. Асинхронный вариант СброситьБуферАсинхронно() возвращает Обещание, но синхронный не сообщает о результате. |
| 5 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98-102` | Метод СброситьБуфер() не имеет механизма таймаута. Асинхронный вариант через Обещание поддерживает таймаут, но синхронный метод не имеет ограничения по времени. |
| 6 | MUST | ✅ found | ForceFlush MUST invoke ForceFlush on all registered SpanProcessors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:99-101` |  |

#### Additional Span Interfaces

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#additional-span-interfaces)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | Readable span: A function receiving this as argument MUST be able to access all information that was added to the span, as listed in the API spec for Span. | `src/Трассировка/Классы/ОтелСпан.os:64-199` |  |
| 8 | MUST | ✅ found | A function receiving this as argument MUST be able to access the InstrumentationScope and Resource information (implicitly) associated with the span. | `src/Трассировка/Классы/ОтелСпан.os:160-172` |  |
| 9 | MUST | ⚠️ partial | For backwards compatibility it MUST also be able to access the InstrumentationLibrary (deprecated since 1.10.0) having the same name and version values as the InstrumentationScope. | `src/Трассировка/Классы/ОтелСпан.os:170` | ОтелСпан предоставляет доступ к ОбластьИнструментирования(), но отдельного метода или алиаса InstrumentationLibrary (deprecated) нет. Используется единый класс ОтелОбластьИнструментирования с тем же именем и версией, что фактически покрывает требование, но отдельной deprecated-сущности нет. |
| 10 | MUST | ✅ found | A function receiving this as argument MUST be able to reliably determine whether the Span has ended. | `src/Трассировка/Классы/ОтелСпан.os:197-199` |  |
| 11 | MUST | ✅ found | Counts for attributes, events and links dropped due to collection limits MUST be available for exporters to report. | `src/Трассировка/Классы/ОтелСпан.os:206-226` |  |
| 12 | MUST | ✅ found | Implementations MUST expose at least the full parent SpanContext. | `src/Трассировка/Классы/ОтелСпан.os:89-91` |  |
| 13 | MUST | ✅ found | Read/write span: It MUST be possible for functions being called with this to somehow obtain the same Span instance and type that the span creation API returned to the user. | `src/Трассировка/Классы/ОтелСпан.os:578-641` |  |

#### Sampling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | Span Processor MUST receive only those spans which have this field [IsRecording] set to true. | `src/Трассировка/Классы/ОтелТрассировщик.os:71-75` |  |
| 15 | SHOULD NOT | ❌ not_found | Span Exporter SHOULD NOT receive them unless the Sampled flag was also set. | - | Нет фильтрации RECORD_ONLY спанов между процессором и экспортером. Спаны с IsRecording=true и Sampled=false (RECORD_ONLY) проходят через процессор и попадают в экспортер. |
| 16 | MUST | ✅ found | Span Exporters MUST receive those spans which have Sampled flag set to true. | `src/Трассировка/Классы/ОтелТрассировщик.os:213-218` |  |
| 17 | SHOULD NOT | ❌ not_found | Span Exporters SHOULD NOT receive the ones that do not have Sampled flag set. | - | Нет фильтрации спанов без флага Sampled перед экспортером. RECORD_ONLY спаны передаются экспортеру без проверки флага. |
| 18 | MUST NOT | ✅ found | The OpenTelemetry SDK MUST NOT allow the combination SampledFlag == true and IsRecording == false. | `src/Трассировка/Классы/ОтелТрассировщик.os:213-218` |  |

#### SDK Span creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sdk-span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | When asked to create a Span, the SDK MUST act as if doing the following in order: use valid parent trace ID or generate new, query Sampler's ShouldSample, generate new span ID independently of sampling decision, create span depending on ShouldSample result. | `src/Трассировка/Классы/ОтелТрассировщик.os:57-94` |  |

#### ShouldSample

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shouldsample)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | If the parent SpanContext contains a valid TraceId, they [TraceId argument and parent TraceId] MUST always match. | `src/Трассировка/Классы/ОтелТрассировщик.os:61` |  |
| 21 | MUST NOT | ✅ found | RECORD_ONLY - IsRecording will be true, but the Sampled flag MUST NOT be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:213-218` |  |
| 22 | MUST | ✅ found | RECORD_AND_SAMPLE - IsRecording will be true and the Sampled flag MUST be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:215-216` |  |
| 23 | SHOULD | ⚠️ partial | Samplers SHOULD normally return the passed-in Tracestate if they do not intend to change it. | `src/Трассировка/Модули/ОтелСэмплер.os:155` | Семплер ОтелСэмплер.ДолженСэмплировать() создает новый пустой ОтелРезультатСэмплирования без передачи входного TraceState. Компенсируется в ОтелТрассировщик.ОпределитьСостояниеТрассировки() через fallback на родительский TraceState, но сам семплер не возвращает переданный TraceState. |
| 24 | SHOULD NOT | ✅ found | Callers SHOULD NOT cache the returned value of GetDescription. | `src/Трассировка/Модули/ОтелСэмплер.os:106-122` |  |

#### TraceID randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#traceid-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | SHOULD | ⚠️ partial | For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values. | `src/Ядро/Модули/ОтелУтилиты.os:78-92` | TraceID генерируется через УникальныйИдентификатор (UUID v4), что обеспечивает случайность, но нет явного соответствия W3C Trace Context Level 2 - младшие 7 байт (56 бит) не гарантированно случайны в UUID v4 (6 бит зарезервированы под version/variant). |

#### Random trace flag

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#random-trace-flag)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | SHOULD | ❌ not_found | For root span contexts, the SDK SHOULD set the Random flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements. | - | Флаг Random (бит 1 TraceFlags) не устанавливается. ВычислитьФлагиТрассировки() устанавливает только бит Sampled (0 или 1), бит Random никогда не выставляется. |

#### Explicit randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#explicit-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 27 | MUST NOT | ⚠️ partial | SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value (the rv sub-key). | - | SDK не работает с подключами OpenTelemetry TraceState (ot=..., rv:...) вообще - не читает и не пишет их. Формально не перезаписывает, но и не имеет осознанной обработки. TraceState передается как непрозрачная строка. |
| 28 | MUST NOT | ⚠️ partial | Root Samplers MAY insert an explicit randomness value into the OpenTelemetry TraceState value in cases where an explicit randomness value is not already set. | - | Семплер не вставляет явное значение случайности в OpenTelemetry TraceState. OTel подключи (ot=rv:...) не поддерживаются. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | SHOULD | ❌ not_found | If the SDK uses an IdGenerator extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated. | - | SDK имеет расширение IdGenerator (ОтелУтилиты.УстановитьГенераторИд), но генератор не может влиять на установку флага Random. Флаг Random вообще не поддерживается в SDK. |

#### Span Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | Span attributes MUST adhere to the common rules of attribute limits. | `src/Трассировка/Классы/ОтелСпан.os:266` |  |
| 31 | MUST | ✅ found | If the SDK implements the limits above it MUST provide a way to change these limits, via a configuration to the TracerProvider, by allowing users to configure individual limits. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:83` |  |
| 32 | SHOULD | ⚠️ partial | The name of the configuration options SHOULD be EventCountLimit and LinkCountLimit. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:34` | Опции называются МаксСобытий и МаксЛинков (русские эквиваленты). Семантически соответствуют EventCountLimit и LinkCountLimit, но имена не совпадают буквально со спецификацией. |
| 33 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called SpanLimits. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:158` |  |
| 34 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute, event, or link was discarded due to such a limit. | `src/Трассировка/Классы/ОтелСпан.os:468` |  |
| 35 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per discarded attribute, event, or link). | `src/Трассировка/Классы/ОтелСпан.os:469` |  |

#### Id Generators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#id-generators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | The SDK MUST by default randomly generate both the TraceId and the SpanId. | `src/Ядро/Модули/ОтелУтилиты.os:78` |  |
| 37 | MUST | ✅ found | The SDK MUST provide a mechanism for customizing the way IDs are generated for both the TraceId and the SpanId. | `src/Ядро/Модули/ОтелУтилиты.os:63` |  |
| 38 | MUST | ✅ found | Name of the methods MUST be consistent with SpanContext (one to generate a SpanId and one for TraceId). | `src/Ядро/Модули/ОтелУтилиты.os:78` |  |
| 39 | MUST NOT | ✅ found | Additional IdGenerator implementing vendor-specific protocols such as AWS X-Ray trace id generator MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | - |  |

#### Span processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 40 | MUST | ✅ found | SDK MUST allow to end each pipeline with individual exporter. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:85` |  |
| 41 | MUST | ✅ found | SDK MUST allow users to implement and configure custom processors. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:1` |  |
| 42 | MUST | ✅ found | The SpanProcessor interface MUST declare the following methods: OnStart, OnEnd, Shutdown, ForceFlush. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11` |  |
| 43 | SHOULD | ✅ found | The SpanProcessor interface SHOULD declare the following methods: OnEnding method. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:21` |  |
| 44 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it (OnStart span parameter). | `src/Трассировка/Классы/ОтелСпан.os:639` |  |
| 45 | SHOULD | ✅ found | Updates to the span SHOULD be reflected in it (the OnStart span object is a live reference). | `src/Трассировка/Классы/ОтелСпан.os:639` |  |

#### OnEnd(Span)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onendspan)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | MUST | ✅ found | This method MUST be called synchronously within the Span.End() API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:458` |  |

#### Shutdown()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | SHOULD | ⚠️ partial | Shutdown SHOULD be called only once for each SpanProcessor instance. After the call to Shutdown, subsequent calls to OnStart, OnEnd, or ForceFlush are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:74` | BatchProcessor устанавливает Закрыт = Истина и Обработать() проверяет флаг (строка 43), но ПростойПроцессорСпанов не имеет флага Закрыт и не игнорирует последующие вызовы ПриЗавершении/СброситьБуфер после Закрыть(). |
| 48 | SHOULD | ❌ not_found | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Метод Закрыть() является процедурой (Void), не возвращает результат. Ни ОтелПростойПроцессорСпанов.Закрыть(), ни ОтелБазовыйПакетныйПроцессор.Закрыть() не сообщают вызывающему коду об успехе, неудаче или таймауте. |
| 49 | MUST | ✅ found | Shutdown MUST include the effects of ForceFlush. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:77` |  |
| 50 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192` | Пакетный процессор ожидает фоновый экспорт с таймаутом (ТаймаутЭкспортаМс, строка 192), но ЭкспортироватьВсеПакеты() (строка 77) не имеет таймаута - может зависнуть при медленном экспортере. Простой процессор также не имеет таймаута. |
| 51 | SHOULD | ⚠️ partial | Shutdown SHOULD be called only once for each SpanProcessor instance. SDKs SHOULD ignore subsequent calls gracefully. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:75` | ОтелБазовыйПакетныйПроцессор устанавливает Закрыт = Истина, но повторный вызов Закрыть() снова выполнит ЭкспортироватьВсеПакеты() и Экспортер.Закрыть(). Нет раннего выхода при Закрыт = Истина в самом методе Закрыть(). |

#### ForceFlush()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 52 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with Spans for which the SpanProcessor had already received events prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 53 | SHOULD | ✅ found | In particular, if any SpanProcessor has any associated exporter, it SHOULD try to call the exporter's Export with all spans for which this was not already done and then invoke ForceFlush on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 54 | MUST | ✅ found | The built-in SpanProcessors MUST do so (call exporter's Export and ForceFlush). | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120` |  |
| 55 | MUST | ❌ not_found | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. It MAY skip or abort some or all Export or ForceFlush calls it has made to achieve this goal. | - | Метод СброситьБуфер() не принимает параметр таймаута. ЭкспортироватьВсеПакеты() выполняется до полного завершения без возможности прервать по таймауту. |
| 56 | SHOULD | ❌ not_found | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Метод СброситьБуфер() является процедурой (Void) и не возвращает результат об успехе, неудаче или таймауте. |
| 57 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the SpanProcessor exports the completed spans. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 58 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` | СброситьБуфер() вызывает ЭкспортироватьВсеПакеты() без таймаута - при медленном экспортере может зависнуть. Нет параметра timeout. |

#### Built-in span processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#built-in-span-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:1, src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:1` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | MUST | ✅ found | The processor MUST synchronize calls to Span Exporter's Export to make sure that they are not invoked concurrently (SimpleSpanProcessor). | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:41` |  |
| 61 | MUST | ✅ found | The processor MUST synchronize calls to Span Exporter's Export to make sure that they are not invoked concurrently (BatchSpanProcessor). | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:144` |  |
| 62 | SHOULD | ✅ found | The batch processor SHOULD export a batch when scheduledDelayMillis after the processor is constructed OR the first span is received, OR the queue contains maxExportBatchSize or more spans, OR ForceFlush is called. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:54` |  |
| 63 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:5` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 64 | MUST | ✅ found | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:13` |  |

#### `Export(batch)`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | MUST NOT | ⚠️ partial | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` | HTTP transport has a configurable timeout (default 10s), but the Экспортировать method in ОтелЭкспортерСпанов itself does not enforce a timeout wrapper - it relies on the transport's timeout. This is a reasonable approach but the timeout is on the transport level, not on Export() directly. |
| 66 | SHOULD NOT | ✅ found | The default SDK's Span Processors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the spans are being sent to. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37` |  |
| 67 | MUST | ✅ found | The Exporter must send an ExportResult to the Processor. ExportResult has values of either Success or Failure. | `src/Ядро/Модули/ОтелРезультатыЭкспорта.os:13` |  |

#### `ForceFlush()`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | ForceFlush is a hint to ensure that the export of any Spans the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` |  |
| 69 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` | СброситьБуфер() is a void procedure (Процедура) that does not return a status. The caller has no way to know whether the flush succeeded, failed, or timed out. |
| 70 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed spans. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:19` |  |
| 71 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:19` | СброситьБуфер() has no timeout parameter or timeout mechanism. The method will block as long as the underlying export takes. |

#### Examples

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#examples)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST | ✅ found | Tracer Provider - Tracer creation, ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:6` |  |
| 73 | MUST | ✅ found | Sampler - ShouldSample and GetDescription MUST be safe to be called concurrently. | `src/Трассировка/Модули/ОтелСэмплер.os:4` |  |
| 74 | MUST | ✅ found | Span processor - all methods MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:7` |  |
| 75 | MUST | ⚠️ partial | Span Exporter - ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:47` | Закрыть() sets a boolean flag without synchronization (no БлокировкаРесурса or АтомарноеБулево). Concurrent calls to Закрыть() and Экспортировать() could race on the Закрыт variable. |

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
| 2 | MUST | ✅ found | The LoggerProvider MUST provide the following functions: Get a Logger. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 3 | MUST | ✅ found | Get a Logger API MUST accept the following instrumentation scope parameters: name, version (optional), schema_url (optional), attributes (optional). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 4 | MUST | ✅ found | The attributes parameter of Get a Logger API MUST be structured to accept a variable number of attributes, including none. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:57` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The Logger MUST provide a function to: Emit a LogRecord. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 6 | SHOULD | ✅ found | The Logger SHOULD provide functions to: Report if Logger is Enabled. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 7 | MUST | ✅ found | The Emit LogRecord API MUST accept the following parameters: Timestamp (optional), Observed Timestamp (optional), Context, Severity Number (optional), Severity Text (optional), Body (optional), Attributes (optional), Event Name (optional). | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 8 | SHOULD | ✅ found | When implicit Context is supported, then the Context parameter in Emit SHOULD be optional. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 9 | MUST | ✅ found | When the Context parameter in Emit is unspecified, it MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:82` |  |
| 10 | SHOULD | ✅ found | When only explicit Context is supported, the Context parameter in Emit SHOULD be required. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 11 | SHOULD | ✅ found | The Enabled API SHOULD accept the following parameters: Context, Severity Number (optional), Event Name (optional). | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 12 | SHOULD | ✅ found | When implicit Context is supported, then the Context parameter in Enabled SHOULD be optional. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 13 | MUST | ✅ found | When the Context parameter in Enabled is unspecified, it MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:151` |  |
| 14 | MUST | ✅ found | When only explicit Context is supported, accepting the Context parameter in Enabled is REQUIRED. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 15 | MUST | ✅ found | The Enabled API MUST return a language idiomatic boolean type. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 16 | SHOULD | ⚠️ partial | The Enabled API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response. | `src/Логирование/Классы/ОтелЛоггер.os:28` | Метод Включен() документирован (назначение, параметры, возвращаемый тип), но нет явного указания, что возвращаемое значение может меняться со временем и что метод нужно вызывать каждый раз перед emit. |

#### Optional and required parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#optional-and-required-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | For each optional parameter, the API MUST be structured to accept it. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 18 | MUST NOT | ✅ found | For each optional parameter, the API MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 19 | MUST | ✅ found | For each required parameter, the API MUST be structured to obligate a user to provide it. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | LoggerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:7` |  |
| 21 | MUST | ✅ found | Logger - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелЛоггер.os:231` |  |

### Logs Sdk

#### Logs SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logs-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Ядро/Классы/ОтелSdk.os:1` |  |

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A LoggerProvider MUST provide a way to allow a Resource to be specified. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:22` |  |
| 3 | SHOULD | ✅ found | If a Resource is specified, it SHOULD be associated with all the LogRecords produced by any Logger from the LoggerProvider. | `src/Логирование/Классы/ОтелЛоггер.os:78` |  |

#### LoggerProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent LoggerProviders. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:205` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration (i.e. LogRecordProcessors and (Development) LoggerConfigurator) MUST be owned by the LoggerProvider. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:12` |  |
| 6 | MUST | ✅ found | If configuration is updated (e.g., adding a LogRecordProcessor), the updated configuration MUST also apply to all already returned Loggers. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:157` |  |
| 7 | MUST NOT | ✅ found | it MUST NOT matter whether a Logger was obtained from the LoggerProvider before or after the configuration change. | `src/Логирование/Классы/ОтелЛоггер.os:106` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | Синхронный СброситьБуфер() - Процедура (void), не возвращает статус успеха/неудачи. Асинхронный СброситьБуферАсинхронно() возвращает Обещание, но оно не различает успех и ошибку явно. |
| 9 | SHOULD | ⚠️ partial | ForceFlush SHOULD return some ERROR status if there is an error condition. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | СброситьБуфер() не возвращает значение (Процедура), нет механизма возврата ERROR статуса вызывающему. |
| 10 | SHOULD | ⚠️ partial | if there is no error condition, it SHOULD return some NO ERROR status. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:107` | СброситьБуфер() не возвращает значение (Процедура), нет механизма возврата NO ERROR статуса вызывающему. |
| 11 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:131` | СброситьБуферАсинхронно() возвращает Обещание с поддержкой таймаута, но синхронный СброситьБуфер() не имеет встроенного таймаута. |
| 12 | MUST | ✅ found | ForceFlush MUST invoke ForceFlush on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:108` |  |

#### ReadableLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readablelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | A function receiving this as an argument MUST be able to access all the information added to the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:44-161` |  |
| 14 | MUST | ✅ found | It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) associated with the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:130-143` |  |
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
| 19 | MUST | ✅ found | If the SDK implements attribute limits it MUST provide a way to change these limits, via a configuration to the LoggerProvider, by allowing users to configure individual limits. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:17-56` |  |
| 20 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called LogRecordLimits. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:1` |  |
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
| 25 | SHOULD NOT | ⚠️ partial | OnEmit is called synchronously on the thread that emitted the LogRecord, therefore it SHOULD NOT block or throw exceptions. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17` | Композитный процессор оборачивает вызовы в Попытка/Исключение (не бросает исключения), но ОтелПростойПроцессорЛогов блокирует поток через БлокировкаЭкспорта при синхронном экспорте (строка 22). Пакетный процессор добавляет в буфер без длительной блокировки. |
| 26 | MUST | ✅ found | For a LogRecordProcessor registered directly on SDK LoggerProvider, the logRecord mutations MUST be visible in next registered processors. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:20` |  |
| 27 | SHOULD | ❌ not_found | Implementations SHOULD recommended to users that a clone of logRecord be used for any concurrent processing, such as in a batching processor. | - | Нет механизма клонирования ОтелЗаписьЛога и нет документации/рекомендации пользователям использовать клон при конкурентной обработке. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST NOT | ✅ found | Any modifications to parameters inside Enabled MUST NOT be propagated to the caller. Parameters are immutable or passed by value. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |

#### ShutDown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each LogRecordProcessor instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117` |  |
| 30 | SHOULD | ✅ found | After the call to Shutdown, subsequent calls to OnEmit are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Логирование/Классы/ОтелЛоггер.os:106` |  |
| 31 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:143` | Асинхронная версия ЗакрытьАсинхронно() возвращает Обещание (Promise) для обратной связи, но синхронная Закрыть() на процессорах и провайдере возвращает void без индикации результата. |
| 32 | MUST | ✅ found | Shutdown MUST include the effects of ForceFlush. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:77` |  |
| 33 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192` | Остановка фонового экспорта использует таймаут (Обещание.Получить(ТаймаутЭкспортаМс)), но основной поток Закрыть() выполняет ЭкспортироватьВсеПакеты() без ограничения по времени. |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | SHOULD | ✅ found | Any tasks associated with LogRecords for which the LogRecordProcessor had already received events prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 35 | SHOULD | ⚠️ partial | If any LogRecordProcessor has any associated exporter, it SHOULD try to call the exporter's Export with all LogRecords for which this was not already done and then invoke ForceFlush on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:146` | ЭкспортироватьВсеПакеты() вызывает Экспортер.Экспортировать() для всех накопленных записей, но не вызывает Экспортер.СброситьБуфер() (ForceFlush) после экспорта. |
| 36 | MUST | ⚠️ partial | The built-in LogRecordProcessors MUST do so (call exporter's Export with all LogRecords and then invoke ForceFlush on the exporter). | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` | Встроенные процессоры экспортируют все накопленные записи через Экспортер.Экспортировать(), но не вызывают Экспортер.СброситьБуфер() (ForceFlush) на экспортере после экспорта. |
| 37 | MUST | ❌ not_found | If a timeout is specified, the LogRecordProcessor MUST prioritize honoring the timeout over finishing all calls. | - | СброситьБуфер() не принимает параметр таймаута, поэтому невозможно приоритизировать выполнение таймаута над завершением всех вызовов. |
| 38 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:131` | На уровне провайдера СброситьБуферАсинхронно() возвращает Обещание (Promise), но синхронный СброситьБуфер() на процессорах возвращает void. |
| 39 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the LogRecordProcessor exports the emitted LogRecords. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 40 | SHOULD | ❌ not_found | ForceFlush SHOULD complete or abort within some timeout. | - | СброситьБуфер() не имеет механизма таймаута - ЭкспортироватьВсеПакеты() выполняется без ограничения по времени и может блокироваться бесконечно. |

#### Built-in processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#built-in-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 41 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1` |  |
| 42 | SHOULD | ✅ found | Other common processing scenarios SHOULD be first considered for implementation out-of-process in OpenTelemetry Collector. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST | ✅ found | The processor MUST synchronize calls to LogRecordExporter's Export to make sure that they are not invoked concurrently (Simple processor). | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:22` |  |
| 44 | MUST | ✅ found | The processor MUST synchronize calls to LogRecordExporter's Export to make sure that they are not invoked concurrently (Batching processor). | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:144` |  |
| 45 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:3` |  |

#### LogRecordExporter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | MUST | ✅ found | A LogRecordExporter MUST support the following functions: Export, ForceFlush, Shutdown | `src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:13` |  |

#### Export

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#export)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | MUST NOT | ✅ found | Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 48 | MUST | ✅ found | There MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:149` |  |
| 49 | SHOULD NOT | ✅ found | The default SDK's LogRecordProcessors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the logs are being sent to. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:18` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 50 | SHOULD | ✅ found | This is a hint to ensure that the export of any ReadableLogRecords the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41` |  |
| 51 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41` | СброситьБуфер() is a Процедура (void), not a Функция. It does not return a success/failure/timeout result to the caller. |
| 52 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the ReadableLogRecords. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41` |  |
| 53 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41` | The exporter's СброситьБуфер() is a no-op (synchronous exporter has no buffering), so it completes instantly. However there is no explicit timeout mechanism in case a subclass buffers data. |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each LogRecordExporter instance. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47` |  |
| 55 | SHOULD | ✅ found | After the call to Shutdown subsequent calls to Export are not allowed and SHOULD return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:26` |  |
| 56 | SHOULD NOT | ⚠️ partial | Shutdown SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47` | Закрыть() simply sets Закрыт=Истина which completes instantly, so it does not block. However there is no explicit timeout guard if the method were extended. |
| 57 | MUST | ✅ found | LoggerProvider - Logger creation, ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117` |  |
| 58 | MUST | ✅ found | Logger - all methods MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 59 | MUST | ⚠️ partial | LogRecordExporter - ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41` | Закрыть() sets Закрыт=Истина without synchronization (no lock or atomic). СброситьБуфер() is a no-op. There is no explicit concurrency protection on exporter's ForceFlush/Shutdown calls. |

### Metrics Api

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD provide a way to set/register and access a global default MeterProvider. | `src/Ядро/Модули/ОтелГлобальный.os:24` |  |

#### MeterProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The MeterProvider MUST provide the following functions: Get a Meter | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 3 | MUST | ✅ found | This API MUST accept the following parameters: name, version, schema_url, attributes | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 4 | MUST NOT | ✅ found | Users can provide a version, but it is up to their discretion. Therefore, this API needs to be structured to accept a version, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:54` |  |
| 5 | MUST NOT | ✅ found | Users can provide a schema_url, but it is up to their discretion. Therefore, this API needs to be structured to accept a schema_url, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:56` |  |
| 6 | MUST | ✅ found | This API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:55` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ found | Meter SHOULD NOT be responsible for the configuration. This should be the responsibility of the MeterProvider instead. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:206` |  |

#### Meter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The Meter MUST provide functions to create new Instruments: Counter, Asynchronous Counter, Histogram, Gauge, Asynchronous Gauge, UpDownCounter, Asynchronous UpDownCounter | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Instrument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ⚠️ partial | Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying. | `src/Метрики/Классы/ОтелМетр.os:553` | Дескрипторы инструментов хранят Вид, ЕдиницаИзмерения, Описание, но OneScript не различает int/float на уровне языка - числовой тип единый. Дескриптор не хранит тип числа как идентифицирующий признак. |

#### Synchronous and Asynchronous instruments

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#synchronous-and-asynchronous-instruments)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API to construct synchronous instruments MUST accept the following parameters: a name of the Instrument. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 11 | SHOULD | ✅ found | If possible, the API SHOULD be structured so a user is obligated to provide the name parameter. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 12 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that the name parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:40` |  |
| 13 | SHOULD | ⚠️ partial | The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:40` | Документация параметра Имя есть в комментариях методов, но нет явной ссылки на синтаксис имён инструментов. |
| 14 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the name; that is left to implementations of the API, like the SDK. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 15 | MUST NOT | ✅ found | This API needs to be structured to accept a unit, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 16 | MUST | ✅ found | The unit parameter needs to support the instrument unit rule. Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 17 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the unit. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 18 | MUST NOT | ✅ found | This API needs to be structured to accept a description, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 19 | MUST | ✅ found | The description needs to support the instrument description rule. Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 20 | MUST NOT | ✅ found | This API needs to be structured to accept advisory parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 21 | SHOULD NOT | ✅ found | The API SHOULD NOT validate advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:642` |  |
| 22 | MUST | ✅ found | The API to construct asynchronous instruments MUST accept the following parameters: a name of the Instrument. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 23 | SHOULD | ✅ found | If possible, the API SHOULD be structured so a user is obligated to provide the name parameter (for asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 24 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that the name parameter is needed (for asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:216` |  |
| 25 | SHOULD | ⚠️ partial | The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (for asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:216` | Документация параметра Имя есть, но нет явной ссылки на синтаксис имён инструментов. |
| 26 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the name, that is left to implementations of the API (for asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 27 | MUST NOT | ✅ found | This API needs to be structured to accept a unit, but MUST NOT obligate a user to provide one (for asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 28 | MUST | ✅ found | The unit parameter for asynchronous instruments: the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 29 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the unit (for asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 30 | MUST NOT | ✅ found | This API needs to be structured to accept a description, but MUST NOT obligate a user to provide one (for asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 31 | MUST | ✅ found | The description for asynchronous instruments: the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 32 | MUST NOT | ✅ found | This API needs to be structured to accept advisory parameters, but MUST NOT obligate the user to provide it (for asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 33 | SHOULD NOT | ✅ found | The API SHOULD NOT validate advisory parameters (for asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:642` |  |
| 34 | MUST | ✅ found | This API MUST be structured to accept a variable number of callback functions, including none. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 35 | MUST | ✅ found | The API MUST support creation of asynchronous instruments by passing zero or more callback functions to be permanently registered to the newly created instrument. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147` |  |
| 36 | SHOULD | ✅ found | The API SHOULD support registration of callback functions associated with asynchronous instruments after they are created. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:58` |  |
| 37 | MUST | ✅ found | Where the API supports registration of callback functions after asynchronous instrumentation creation, the user MUST be able to undo registration of the specific callback after its registration by some means. | `src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os:14` |  |
| 38 | MUST | ✅ found | Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160` |  |
| 39 | MUST | ✅ found | Callback functions MUST be documented as follows for the end user. | `src/Метрики/Классы/ОтелНаблюдениеМетрики.os:56` |  |
| 40 | SHOULD | ⚠️ partial | Callback functions SHOULD be reentrant safe. The SDK expects to evaluate callbacks for each MetricReader independently. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160` | Callbacks вызываются последовательно для каждого reader, но нет документации для пользователя о реентерабельности. |
| 41 | SHOULD NOT | ⚠️ partial | Callback functions SHOULD NOT take an indefinite amount of time. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160` | Нет документации для пользователя о том, что callback не должен выполняться бесконечно. Нет таймаута. |
| 42 | SHOULD NOT | ⚠️ partial | Callback functions SHOULD NOT make duplicate observations (more than one Measurement with the same attributes) across all registered callbacks. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160` | Нет документации для пользователя и нет проверки дубликатов наблюдений. |
| 43 | MUST | ✅ found | Callbacks registered at the time of instrument creation MUST apply to the single instruments which is under construction. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147` |  |
| 44 | MUST | ✅ found | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the instrument associated with each observed Measurement value. | `src/Метрики/Классы/ОтелМетр.os:428` |  |
| 45 | MUST | ✅ found | Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of asynchronous instruments from the same Meter instance. | `src/Метрики/Классы/ОтелМетр.os:428` |  |
| 46 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` |  |
| 47 | MUST | ✅ found | Observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` |  |
| 48 | SHOULD | ✅ found | The API SHOULD provide some way to pass state to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147` |  |

#### General operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | SHOULD | ✅ found | All synchronous instruments SHOULD provide functions to: Report if instrument is Enabled | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 50 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when recording measurements, synchronous instruments SHOULD provide this Enabled API | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 51 | MUST | ✅ found | There are currently no required parameters for this API. Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 52 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. A returned value of true means the instrument is enabled for the provided arguments, and a returned value of false means the instrument is disabled for the provided arguments | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 53 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:194` | Метод Включен() задокументирован, но комментарий описывает условия возврата Ложь (MeterConfig.enabled=false, Drop Aggregation), а не рекомендацию вызывать перед каждым измерением |

#### Counter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Counter other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 55 | SHOULD NOT | ✅ found | Counter.Add: This API SHOULD NOT return a value | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 56 | MUST | ✅ found | Counter.Add: This API MUST accept the following parameter: A numeric increment value | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 57 | SHOULD | ✅ found | Counter.Add: If possible, this API SHOULD be structured so a user is obligated to provide this parameter (the numeric increment value) | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 58 | MUST | ✅ found | Counter.Add: If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed | `src/Метрики/Классы/ОтелСчетчик.os:13` |  |
| 59 | SHOULD | ✅ found | The increment value is expected to be non-negative. This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative | `src/Метрики/Классы/ОтелСчетчик.os:14` |  |
| 60 | SHOULD NOT | ⚠️ partial | This API SHOULD NOT validate this value, that is left to implementations of the API | `src/Метрики/Классы/ОтелСчетчик.os:22` | Код выполняет валидацию: Если Значение < 0 Тогда Возврат - отрицательные значения молча отбрасываются на уровне API, тогда как спецификация рекомендует оставить валидацию реализации SDK |
| 61 | MUST | ✅ found | Counter.Add: This API MUST be structured to accept a variable number of attributes, including none | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 62 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 63 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Counter other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 64 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:179` |  |
| 65 | MUST | ✅ found | Observations from a single callback MUST be reported with identical timestamps | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` |  |
| 66 | SHOULD | ✅ found | The API SHOULD provide some way to pass state to the callback | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:58` |  |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Histogram other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:80` |  |
| 68 | SHOULD NOT | ✅ found | Histogram.Record: This API SHOULD NOT return a value | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 69 | MUST | ✅ found | Histogram.Record: This API MUST accept the following parameter: A numeric value to record | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 70 | SHOULD | ✅ found | Histogram.Record: If possible, this API SHOULD be structured so a user is obligated to provide this parameter (the numeric value) | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 71 | MUST | ✅ found | Histogram.Record: If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed | `src/Метрики/Классы/ОтелГистограмма.os:13` |  |
| 72 | SHOULD | ✅ found | Histogram.Record: The value is expected to be non-negative. This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative | `src/Метрики/Классы/ОтелГистограмма.os:13` |  |
| 73 | SHOULD NOT | ✅ found | Histogram.Record: This API SHOULD NOT validate this value, that is left to implementations of the API | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 74 | MUST | ✅ found | Histogram.Record: This API MUST be structured to accept a variable number of attributes, including none | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 75 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Gauge other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:194` |  |
| 76 | SHOULD NOT | ✅ found | Gauge.Record: This API SHOULD NOT return a value | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 77 | MUST | ✅ found | Gauge.Record: This API MUST accept the following parameter: A numeric value. The current absolute value | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 78 | SHOULD | ✅ found | Gauge.Record: If possible, this API SHOULD be structured so a user is obligated to provide this parameter (the numeric value) | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 79 | MUST | ✅ found | Gauge.Record: If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed | `src/Метрики/Классы/ОтелДатчик.os:13` |  |
| 80 | MUST | ✅ found | Gauge.Record: This API MUST be structured to accept a variable number of attributes, including none | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 81 | MUST | ✅ found | Gauge.Record: The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 82 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Gauge other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:308` |  |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 83 | MUST NOT | ✅ found | There MUST NOT be any API for creating an UpDownCounter other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:162` |  |
| 84 | SHOULD NOT | ✅ found | UpDownCounter.Add: This API SHOULD NOT return a value | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 85 | MUST | ✅ found | UpDownCounter.Add: This API MUST accept the following parameter: A numeric value to add | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 86 | SHOULD | ✅ found | UpDownCounter.Add: If possible, this API SHOULD be structured so a user is obligated to provide this parameter (the numeric value) | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 87 | MUST | ✅ found | UpDownCounter.Add: If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:13` |  |
| 88 | MUST | ✅ found | UpDownCounter.Add: This API MUST be structured to accept a variable number of attributes, including none | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 89 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:268` |  |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | MUST | ✅ found | For callback functions registered after an asynchronous instrument is created, the API is required to support a mechanism for unregistration | `src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os:14` |  |

#### Note the two associated instruments are passed to the callback.

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-the-two-associated-instruments-are-passed-to-the-callback)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 91 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: A callback function; A list (or tuple, etc.) of Instruments used in the callback function | `src/Метрики/Классы/ОтелМетр.os:428` |  |
| 92 | SHOULD | ✅ found | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introducing breaking changes, if possible | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 93 | MUST | ✅ found | MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default | `src/Метрики/Классы/ОтелПровайдерМетрик.os:241` |  |
| 94 | MUST | ✅ found | Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default | `src/Метрики/Классы/ОтелМетр.os:493` |  |
| 95 | MUST | ✅ found | Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:261` |  |

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
| 5 | MUST | ✅ found | Configuration (i.e. MetricExporters, MetricReaders, Views, and (Development) MeterConfigurator) MUST be owned by the MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:12` |  |
| 6 | MUST | ✅ found | If configuration is updated (e.g., adding a MetricReader), the updated configuration MUST also apply to all already returned Meters. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:71` |  |
| 7 | MUST NOT | ✅ found | it MUST NOT matter whether a Meter was obtained from the MeterProvider before or after the configuration change | `src/Метрики/Классы/ОтелПровайдерМетрик.os:71` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | ForceFlush MUST invoke ForceFlush on all registered MetricReader instances that implement ForceFlush. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` |  |
| 9 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` | СброситьБуфер() - Процедура (void), не возвращает статус успеха/ошибки. Нет индикации результата вызывающему коду. |
| 10 | SHOULD | ⚠️ partial | ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` | СброситьБуфер() не возвращает значения (void Процедура). Не реализован механизм возврата ERROR/NO ERROR статуса. |
| 11 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:152` | СброситьБуферАсинхронно() возвращает Обещание с поддержкой таймаута, но синхронный метод СброситьБуфер() не принимает параметр таймаута. |

#### View

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The SDK MUST provide functionality for a user to create Views for a MeterProvider. | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 13 | MUST | ✅ found | This functionality MUST accept as inputs the Instrument selection criteria and the resulting stream configuration. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:176` |  |
| 14 | MUST | ✅ found | The SDK MUST provide the means to register Views with a MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:176` |  |

#### Instrument selection criteria

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-selection-criteria)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | SHOULD | ✅ found | Criteria SHOULD be treated as additive. This means an Instrument has to match all the provided criteria for the View to be applied. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37-61` |  |
| 16 | MUST | ✅ found | The SDK MUST accept the following criteria: name, type, unit, meter_name, meter_version, meter_schema_url. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:4-14` |  |
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
| 25 | MUST | ✅ found | The SDK MUST accept the following stream configuration parameters: name, description, attribute_keys, aggregation, exemplar_reservoir, aggregation_cardinality_limit. | `src/Метрики/Классы/ОтелПредставление.os:4-18` |  |
| 26 | SHOULD | ✅ found | name: The metric stream name that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:4` |  |
| 27 | SHOULD | ⚠️ partial | In order to avoid conflicts, if a name is provided the View SHOULD have an instrument selector that selects at most one instrument. | `src/Метрики/Классы/ОтелПредставление.os:4` | Представление принимает имя, но SDK не предупреждает если селектор с подстановочным именем и View с именем-переименованием используются вместе - нет валидации конфликта при регистрации. |
| 28 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept a name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:157` |  |
| 29 | MUST | ✅ found | If the user does not provide a name value, name from the Instrument the View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:211-213` |  |
| 30 | SHOULD | ✅ found | description: The metric stream description that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:6` |  |
| 31 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept a description, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:158` |  |
| 32 | MUST | ✅ found | If the user does not provide a description value, the description from the Instrument a View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:214-216` |  |
| 33 | MUST | ✅ found | attribute_keys: This is, at a minimum, an allow-list of attribute keys for measurements captured in the metric stream. The allow-list contains attribute keys that identify the attributes that MUST be kept. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:84-86` |  |
| 34 | MUST | ✅ found | attribute_keys allow-list: all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:291-300` |  |
| 35 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept attribute_keys, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелПредставление.os:159` |  |
| 36 | SHOULD | ✅ found | If the user does not provide any value, the SDK SHOULD use the Attributes advisory parameter configured on the instrument instead. | `src/Метрики/Классы/ОтелМетр.os:523-528` |  |
| 37 | MUST | ✅ found | If the Attributes advisory parameter is absent, all attributes MUST be kept. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:83-86` |  |
| 38 | SHOULD | ✅ found | Additionally, implementations SHOULD support configuring an exclude-list of attribute keys. | `src/Метрики/Классы/ОтелПредставление.os:10` |  |
| 39 | MUST | ⚠️ partial | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелПредставление.os:10` | ИсключенныеКлючиАтрибутов хранятся в ОтелПредставление, но не применяются в ОтелБазовыйСинхронныйИнструмент - ФильтроватьАтрибутыПоКлючам работает только с РазрешенныеКлючиАтрибутов (allow-list), exclude-list не используется при фильтрации. |
| 40 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept an aggregation, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:161` |  |
| 41 | MUST | ⚠️ partial | If the user does not provide an aggregation value, the MeterProvider MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance. | `src/Метрики/Классы/ОтелМетр.os:58-59` | Агрегация по умолчанию задается жестко при создании инструмента (Counter->Sum, Histogram->Histogram, Gauge->LastValue), но не настраивается per MetricReader - один агрегатор разделяется между всеми читателями. |
| 42 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept an exemplar_reservoir, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:163` |  |
| 43 | MUST | ✅ found | If the user does not provide an exemplar_reservoir value, the MeterProvider MUST apply a default exemplar reservoir. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |
| 44 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept an aggregation_cardinality_limit, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:164` |  |
| 45 | MUST | ⚠️ partial | If the user does not provide an aggregation_cardinality_limit value, the MeterProvider MUST apply the default aggregation cardinality limit the MetricReader is configured with. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` | Лимит по умолчанию (2000) задан жестко в конструкторе ОтелБазовыйСинхронныйИнструмент и ОтелМетр, а не берется из MetricReader. MetricReader не имеет свойства cardinality limit. |
| 46 | MUST | ⚠️ partial | If both a View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:518-536` | Реализовано для attribute_keys (строки 523-528) и для ГраницыГистограммы (строки 540-550), но НЕ для aggregation - View.Агрегация() не применяется к уже созданному инструменту, агрегатор создается при создании инструмента и не заменяется представлением. |

#### Measurement processing

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#measurement-processing)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | SHOULD | ✅ found | The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument: Determine the MeterProvider, check Views, apply default Aggregation if no View. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:187-199` |  |
| 48 | MUST | ✅ found | If the MeterProvider has no View registered, take the Instrument and apply the default Aggregation. Instrument advisory parameters, if any, MUST be honored. | `src/Метрики/Классы/ОтелМетр.os:515-536` |  |
| 49 | SHOULD | ⚠️ partial | If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:202-220` | Представления применяются (строки 207-218), но нет проверки на конфликтующие метрические идентичности между несколькими View и нет предупреждений при конфликтах. |
| 50 | SHOULD | ⚠️ partial | If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asynchronous instrument to use the Explicit bucket histogram aggregation) the implementation SHOULD emit a warning and proceed as if the View did not exist. | - | Нет валидации совместимости агрегации View с типом инструмента. SDK не проверяет семантические ошибки при применении View. |
| 51 | MUST | ⚠️ partial | If both a View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:523-528` | Приоритет View реализован для attribute_keys и границ гистограммы, но не для aggregation - View.Агрегация() не применяется динамически к инструменту. |
| 52 | SHOULD | ✅ found | If the Instrument could not match with any of the registered Views, the SDK SHOULD enable the instrument using the default aggregation and temporality. | `src/Метрики/Классы/ОтелМетр.os:58-67` |  |

#### conflicting metric identities)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#conflicting-metric-identities)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 53 | MUST | ✅ found | The SDK MUST provide the following Aggregation to support the Metric Points in the Metrics Data Model: Drop, Default, Sum, Last Value, Explicit Bucket Histogram. | `src/Метрики/Модули/ОтелАгрегация.os:15-65` |  |
| 54 | SHOULD | ✅ found | The SDK SHOULD provide the following Aggregation: Base2 Exponential Bucket Histogram. | `src/Метрики/Модули/ОтелАгрегация.os:76-81` |  |

#### Sum Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#sum-aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD NOT | ❌ not_found | Histogram Aggregations: Arithmetic sum of Measurement values in population. This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. UpDownCounter or ObservableGauge). | - | ОтелАгрегаторГистограммы.Записать() безусловно суммирует все значения через Аккумулятор.Получить('sum').ПолучитьИДобавить(Значение) - нет проверки на отрицательные значения или тип инструмента. |
| 56 | SHOULD | ✅ found | SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different. | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:118-135` |  |
| 57 | MUST | ✅ found | The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic scale parameter will not exceed. The maximum scale is defined by the MaxScale configuration parameter. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:302-304` |  |
| 58 | SHOULD | ✅ found | When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:41` |  |
| 59 | SHOULD NOT | ❌ not_found | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the sum, min, and max fields. | - | OneScript не имеет IEEE +Inf/-Inf/NaN как стандартных значений, но в ОтелАгрегаторЭкспоненциальнойГистограммы.Записать() нет явной проверки на ненормальные значения. |
| 60 | SHOULD | ✅ found | Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possible, within the constraint of maximum size. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:157-185` |  |

#### Observations inside asynchronous callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#observations-inside-asynchronous-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | MUST | ⚠️ partial | Callback functions MUST be invoked for the specific MetricReader performing collection, such that observations made or produced by executing callbacks only apply to the intended MetricReader during collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:140-147` | Callbacks вызываются при сборе каждого MetricReader (через Метр.ВызватьМультиОбратныеВызовы), но наблюдения не изолированы per-reader - данные разделяются между всеми читателями. Каждый reader видит одни и те же observation данные. |
| 62 | SHOULD | ❌ not_found | The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks. | - | Нет механизма контроля использования асинхронных инструментов вне callback. ОтелБазовыйНаблюдаемыйИнструмент не проверяет контекст вызова. |
| 63 | SHOULD | ❌ not_found | The implementation SHOULD use a timeout to prevent indefinite callback execution. | - | В ОтелБазовыйНаблюдаемыйИнструмент.ВызватьCallbackИСобрать() callbacks выполняются синхронно без таймаута. Есть try-catch для ошибок, но нет ограничения по времени. |
| 64 | MUST | ✅ found | The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:140-147` |  |
| 65 | SHOULD NOT | ❌ not_found | The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback. | - | В ОтелБазовыйНаблюдаемыйИнструмент.ВызватьCallbackИСобрать() все записи из callback добавляются к результату, а ВнешниеНаблюдения очищаются (строка 174), но нет фильтрации ранее наблюдаемых наборов атрибутов - каждый вызов callback создает новый набор точек данных. |

#### Cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | SHOULD | ✅ found | SDKs SHOULD support being configured with a cardinality limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:92-101` |  |
| 67 | SHOULD | ✅ found | Cardinality limit enforcement SHOULD occur after attribute filtering, if any. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:84-92` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ⚠️ partial | A view with criteria matching the instrument an aggregation is created for has an aggregation_cardinality_limit value defined for the stream, that value SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:92` | View (ОтелПредставление) has ЛимитМощностиАгрегации property, but ПрименитьПредставлениеКИнструменту in ОтелМетр.os:515 does not apply this limit to the instrument's УстановитьЛимитМощности - only attribute keys and reservoir are applied from View |
| 69 | SHOULD | ❌ not_found | If there is no matching view, but the MetricReader defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | - | ОтелПериодическийЧитательМетрик does not have any cardinality limit configuration. Only the Meter/instrument-level default of 2000 exists. |
| 70 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` |  |
| 71 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:92` |  |
| 72 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:92` |  |

#### Synchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#synchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | MUST | ✅ found | Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138` |  |
| 74 | MUST | ✅ found | Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in exactly one Aggregator, which is either an Aggregator associated with the correct attribute set or an aggregator associated with the overflow attribute set. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:78` |  |
| 75 | MUST NOT | ✅ found | Measurements MUST NOT be double-counted or dropped during an overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:78` |  |

#### Asynchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#asynchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 76 | SHOULD | ❌ not_found | Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality. | - | ОтелБазовыйНаблюдаемыйИнструмент has no cardinality limiting at all. ВызватьCallbackИСобрать converts all callback records to data points without any limit or overflow handling. |

#### Duplicate instrument registration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#duplicate-instrument-registration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 77 | MUST | ✅ found | The Meter MUST return a functional instrument that can be expected to export data even if this will cause semantic error in the data model. | `src/Метрики/Классы/ОтелМетр.os:54` |  |
| 78 | SHOULD | ✅ found | When a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted. | `src/Метрики/Классы/ОтелМетр.os:573` |  |
| 79 | SHOULD | ⚠️ partial | The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible. | `src/Метрики/Классы/ОтелМетр.os:573` | Warning describes the conflict (old vs new params) but does not include advice on how to resolve it, such as suggesting the use of Views for renaming or setting description. |
| 80 | SHOULD | ❌ not_found | If the potential conflict involves multiple description properties, setting the description through a configured View SHOULD avoid the warning. | - | ПроверитьКонфликтДескриптора treats description mismatch as a conflict regardless of whether a View is configured to resolve it. No check is made for whether a matching View resolves the description difference. |
| 81 | SHOULD | ❌ not_found | If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning. | - | The warning message does not include any View recipe or suggestion about how to use Views to rename instruments to resolve the conflict. |
| 82 | SHOULD | ⚠️ partial | Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both Metric objects and emit a generic warning describing the duplicate instrument registration. | `src/Метрики/Классы/ОтелМетр.os:54` | A warning is emitted for duplicate registration, but the SDK returns the first-seen instrument instead of reporting both Metric objects. Only one Metric stream is exported, not two. |
| 83 | MUST | ✅ found | The SDK MUST aggregate data from identical Instruments together in its export pipeline. | `src/Метрики/Классы/ОтелМетр.os:54` |  |

#### Name conflict

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#name-conflict)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 84 | MUST | ✅ found | When a user passes multiple casings of the same name, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above. | `src/Метрики/Классы/ОтелМетр.os:49` |  |

#### Instrument name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 85 | SHOULD | ❌ not_found | When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax. | - | No instrument name validation is performed in any of the instrument creation methods (СоздатьСчетчик, СоздатьГистограмму, etc.). Names are only lowercased for duplicate detection but not validated against the syntax rules. |
| 86 | SHOULD | ❌ not_found | If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name. | - | No error is emitted for invalid instrument names since no validation is performed. |

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
| 95 | MUST | ✅ found | If no View matches, or if a matching View selects the default aggregation, the ExplicitBucketBoundaries advisory parameter MUST be used. If neither is provided, the default bucket boundaries apply. | `src/Метрики/Классы/ОтелМетр.os:539` |  |

#### Exemplar

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | MUST | ✅ found | A Metric SDK MUST provide a mechanism to sample Exemplars from measurements via the ExemplarFilter and ExemplarReservoir hooks. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:1` |  |
| 97 | SHOULD | ✅ found | Exemplar sampling SHOULD be turned on by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:264` |  |
| 98 | MUST NOT | ✅ found | If Exemplar sampling is off, the SDK MUST NOT have overhead related to exemplar sampling. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:335` |  |
| 99 | MUST | ✅ found | A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation. For example, Exemplar sampling of histograms should be able to leverage bucket boundaries. | `src/Метрики/Классы/ОтелМетр.os:99` |  |
| 100 | SHOULD | ✅ found | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: ExemplarFilter: filter which measurements can become exemplars; ExemplarReservoir: storage and sampling of exemplars. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 101 | MUST | ✅ found | The ExemplarFilter configuration MUST allow users to select between one of the built-in ExemplarFilters. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 102 | SHOULD | ✅ found | The ExemplarFilter SHOULD be a configuration parameter of a MeterProvider for an SDK. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 103 | SHOULD | ✅ found | The default value SHOULD be TraceBased. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:245` |  |
| 104 | SHOULD | ✅ found | The filter configuration SHOULD follow the environment variable specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:110` |  |
| 105 | MUST | ✅ found | An OpenTelemetry SDK MUST support the following filters: AlwaysOn, AlwaysOff, TraceBased. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14` |  |

#### ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 106 | MUST | ✅ found | The ExemplarReservoir interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 107 | MUST | ✅ found | A new ExemplarReservoir MUST be created for every known timeseries data point, as determined by aggregation and view configuration. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |
| 108 | SHOULD | ✅ found | The 'offer' method SHOULD accept measurements, including: the value of the measurement, the complete set of Attributes, the Context of the measurement, a timestamp that best represents when the measurement was taken. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` |  |
| 109 | SHOULD | ⚠️ partial | The 'offer' method SHOULD have the ability to pull associated trace and span information without needing to record full context. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` | The offer method (Предложить) accepts КонтекстСпана directly rather than full Context - span/trace info is extracted before calling the reservoir in ОтелБазовыйСинхронныйИнструмент.ЗахватитьЭкземпляр. This is functionally equivalent but the reservoir itself doesn't pull from context. |
| 110 | MUST | ⚠️ partial | This MUST be clearly documented in the API and the reservoir MUST be given the Attributes associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the 'offer' method. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` | The reservoir receives both measurement attributes and series attributes per-offer call (not at construction). The filtered attributes computation works correctly but attributes are not given at construction time as an alternative. |
| 111 | MUST | ✅ found | The 'collect' method MUST return accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:55` |  |
| 112 | SHOULD | ✅ found | Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138` |  |
| 113 | MUST | ✅ found | Exemplars MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:130` |  |
| 114 | SHOULD | ❌ not_found | The ExemplarReservoir SHOULD avoid allocations when sampling exemplars. | - | ОтелРезервуарЭкземпляров creates new Соответствие objects for each exemplar in СоздатьЭкземпляр and new arrays for filtered attributes - no object reuse or pre-allocation strategy is implemented. |
| 115 | SHOULD | ⚠️ partial | The 'offer' method MAY accept a filtered subset of Attributes which diverge from the timeseries the reservoir is associated with. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39` | The offer method accepts both АтрибутыИзмерения and АтрибутыСерии and computes filtered attributes internally - but the spec says this MUST be clearly documented and the reservoir given timeseries attributes at construction. The API documentation does not explicitly call this out. |

#### Exemplar defaults

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar-defaults)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 116 | MUST | ✅ found | The SDK MUST include two types of built-in exemplar reservoirs: SimpleFixedSizeExemplarReservoir, AlignedHistogramBucketExemplarReservoir. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1` |  |
| 117 | SHOULD | ✅ found | Explicit bucket histogram aggregation with more than 1 bucket SHOULD use AlignedHistogramBucketExemplarReservoir. | `src/Метрики/Классы/ОтелМетр.os:99` |  |
| 118 | SHOULD | ✅ found | Base2 Exponential Histogram Aggregation SHOULD use a SimpleFixedSizeExemplarReservoir with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty (e.g. min(20, max_buckets)). | `src/Метрики/Классы/ОтелМетр.os:137` |  |
| 119 | SHOULD | ✅ found | All other aggregations SHOULD use SimpleFixedSizeExemplarReservoir. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |

#### SimpleFixedSizeExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#simplefixedsizeexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 120 | MUST | ✅ found | This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the reservoir has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:80` |  |
| 121 | SHOULD | ✅ found | Any stateful portion of sampling computation SHOULD be reset every collection cycle. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:64` |  |
| 122 | SHOULD | ✅ found | Otherwise, a default size of 1 SHOULD be used. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:165` |  |

#### AlignedHistogramBucketExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#alignedhistogrambucketexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 123 | MUST | ✅ found | This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:158` |  |
| 124 | MUST | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50` |  |
| 125 | SHOULD | ⚠️ partial | This implementation SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50` | Реализация использует стратегию 'последнее измерение заменяет предыдущее' (last-seen), а не reservoir sampling. Спецификация допускает это как альтернативу (MAY instead keep the last seen measurement), но SHOULD указывает на предпочтительность равномерного алгоритма. |
| 126 | SHOULD | ✅ found | This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:158` |  |

#### Custom ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#custom-exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 127 | MUST | ✅ found | The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation. | `src/Метрики/Классы/ОтелПредставление.os:128` |  |
| 128 | MUST | ✅ found | This extension MUST be configurable on a metric View. | `src/Метрики/Классы/ОтелПредставление.os:151` |  |
| 129 | MUST | ✅ found | Individual reservoirs MUST still be instantiated per metric-timeseries. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:176` |  |

#### MetricReader operations#### Collect

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader-operations-collect)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 130 | SHOULD | ⚠️ partial | Collect SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` | Метод СброситьБуфер() (Collect/ForceFlush) является процедурой без возвращаемого значения. Caller не получает информации об успехе, ошибке или таймауте. |
| 131 | SHOULD | ❌ not_found | Collect SHOULD invoke Produce on registered MetricProducers. | - | Нет концепции MetricProducer как отдельной сущности. MetricReader собирает данные только из зарегистрированных Meter'ов SDK, но не поддерживает внешние MetricProducer'ы. |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 132 | MUST | ✅ found | Shutdown MUST be called only once for each MetricReader instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:89` |  |
| 133 | SHOULD | ⚠️ partial | After the call to Shutdown, subsequent invocations to Collect are not allowed. SDKs SHOULD return some failure for these calls, if possible. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:59` | После Закрыть() флаг Закрыт устанавливается в Истина и фоновое задание останавливается. Однако метод СброситьБуфер() (Collect) не проверяет флаг Закрыт и не возвращает ошибку при вызове после shutdown. |
| 134 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88` | Метод Закрыть() является процедурой без возвращаемого значения. Ошибки обрабатываются внутри через логирование, но caller не получает явного статуса результата. |
| 135 | SHOULD | ✅ found | Shutdown SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` |  |

#### Periodic exporting MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 136 | MUST | ✅ found | The reader MUST synchronize calls to MetricExporter's Export to make sure that they are not invoked concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:124` |  |
| 137 | SHOULD | ✅ found | ForceFlush SHOULD collect metrics, call Export(batch) and ForceFlush() on the configured Push Metric Exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` |  |
| 138 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` | Метод СброситьБуфер() (ForceFlush) является процедурой без возвращаемого значения. Caller не получает информации об успехе или неудаче. |
| 139 | SHOULD | ⚠️ partial | ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` | Метод СброситьБуфер() не возвращает статус. Ошибки перехватываются и логируются, но не передаются вызывающему коду. |
| 140 | SHOULD | ❌ not_found | ForceFlush SHOULD complete or abort within some timeout. | - | ForceFlush (СброситьБуфер) не имеет механизма таймаута. Метод выполняется синхронно без ограничения по времени. |

#### MetricExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 141 | MUST | ✅ found | MetricExporter defines the interface that protocol-specific exporters MUST implement so that they can be plugged into OpenTelemetry SDK and support sending of telemetry data. | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1` |  |
| 142 | SHOULD | ❌ not_found | Metric Exporters SHOULD report an error condition for data output by the MetricReader with unsupported Aggregation or Aggregation Temporality. | - | Экспортер не проверяет и не сообщает об ошибках для неподдерживаемых типов агрегации или временности. Экспортер просто сериализует и отправляет данные без валидации. |
| 143 | MUST | ✅ found | A Push Metric Exporter MUST support the Export(batch) function. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25` |  |
| 144 | MUST | ✅ found | The SDK MUST provide a way for the exporter to get the Meter information (e.g. name, version, etc.) associated with each Metric Point. | `src/Метрики/Классы/ОтелДанныеМетрики.os:42` |  |
| 145 | MUST NOT | ⚠️ partial | Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25` | Export зависит от транспорта (HTTP/gRPC). Таймаут может быть настроен на уровне транспорта (HTTPСоединение), но явного таймаута на уровне самого метода Export нет. |
| 146 | SHOULD NOT | ✅ found | The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the metrics are being sent to. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25` |  |
| 147 | SHOULD | ✅ found | ForceFlush is a hint to ensure that the export of any Metrics the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` |  |
| 148 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` | Метод СброситьБуфер() экспортера является процедурой без возвращаемого значения. Вызывающий код не получает информации об успехе или неудаче. |
| 149 | SHOULD | ❌ not_found | ForceFlush SHOULD complete or abort within some timeout. | - | Метод СброситьБуфер() экспортера метрик не имеет таймаута. Для синхронного экспортера это не критично (он не буферизует), но формально таймаут отсутствует. |
| 150 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each MetricExporter instance. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` |  |
| 151 | SHOULD | ✅ found | After the call to Shutdown subsequent calls to Export are not allowed and should return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:26` |  |
| 152 | SHOULD NOT | ⚠️ partial | Shutdown SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` | Метод Закрыть() экспортера просто ставит флаг Закрыт = Истина и не блокируется. Однако нет явного механизма таймаута, если бы Shutdown включал flush операцию. |
| 153 | SHOULD | ❌ not_found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed metrics. | - | Это рекомендация по использованию, а не по реализации. Нет документации или предупреждения о том, что ForceFlush не должен вызываться часто. |

#### Pull Metric Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#pull-metric-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 154 | MUST | ⚠️ partial | MetricProducer defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data. | - | No separate MetricProducer interface exists as a distinct class. The SDK does not bridge third-party metric sources via a MetricProducer interface - the MetricReader (ОтелПериодическийЧитательМетрик, ОтелПрометеусЧитательМетрик) collects from internal Meters directly. However, the pull exporter is modeled as MetricReader (ОтелПрометеусЧитательМетрик) which is explicitly allowed by the spec. Changing status to partial since MetricProducer as a pluggable interface for third-party sources is not implemented. |
| 155 | SHOULD | ❌ not_found | MetricProducer implementations SHOULD accept configuration for the AggregationTemporality of produced metrics. | - | There is no MetricProducer interface or implementation that accepts AggregationTemporality configuration. The ОтелПрометеусЧитательМетрик (pull reader) does not accept temporality configuration - it always produces cumulative data for Prometheus. The temporality selector exists on the exporter (ОтелЭкспортерМетрик) but not on any MetricProducer. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 156 | MUST | ❌ not_found | A MetricProducer MUST support the following functions (Produce). | - | No MetricProducer interface or class exists with a Produce function. The readers (ОтелПериодическийЧитательМетрик, ОтелПрометеусЧитательМетрик) collect metrics internally via СобратьИЭкспортировать/СобратьСемейства, but there is no standalone MetricProducer with a Produce method that can be plugged into a MetricReader. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 157 | MUST | ✅ found | A MetricFilter MUST support the following functions (TestMetric, TestAttributes). | `src/Метрики/Классы/ОтелФильтрМетрик.os:29` |  |

#### TestMetric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#testmetric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 158 | MUST | ✅ found | The SDK MUST provide configuration according to the SDK environment variables specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:110` |  |

#### Numerical limits handling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#numerical-limits-handling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 159 | MUST | ⚠️ partial | The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry. | - | No explicit numerical limits handling is implemented. The SDK relies on OneScript's native number handling without any specific graceful error handling for numerical limits or overflows. |
| 160 | MUST | ➖ n_a | If the SDK receives float/double values from Instruments, it MUST handle all the possible values (NaN, Infinities per IEEE 754). | - | OneScript does not support IEEE 754 floats natively - it uses its own number type. NaN and Infinity concepts do not exist in the OneScript runtime, making this requirement a platform limitation. |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 161 | SHOULD | ✅ found | All the metrics components SHOULD allow new methods to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:1` |  |
| 162 | SHOULD | ✅ found | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to existing methods without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 163 | MUST | ⚠️ partial | MeterProvider - Meter creation, ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` | ОтелПровайдерМетрик uses СинхронизированнаяКарта for Meter cache (line 241), providing thread-safe Meter creation. However, СброситьБуфер (ForceFlush) and Закрыть (Shutdown) do not use any locking or atomic guards - they iterate ЧитателиМетрик without synchronization. Partially safe. |
| 164 | MUST | ✅ found | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:167` |  |
| 165 | MUST | ✅ found | MetricReader - Collect, ForceFlush (for periodic exporting MetricReader) and Shutdown MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:283` |  |
| 166 | MUST | ⚠️ partial | MetricExporter - ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` | ОтелЭкспортерМетрик.Закрыть() sets Закрыт = Истина (line 50) without atomic operation or lock. СброситьБуфер() is empty (no-op). The Закрыт flag is a plain boolean, not an АтомарноеБулево, so concurrent calls to Закрыть/Экспортировать could have a race condition. |

### Otlp Exporter

#### Configuration Options

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#configuration-options)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | The following configuration options MUST be available to configure the OTLP exporter (Endpoint, Insecure, Certificate File, Client key file, Client certificate file, Headers, Compression, Timeout, Protocol). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130` | Core options (endpoint, protocol, headers, compression, timeout) are available. TLS certificate options (Certificate File, Client key file, Client certificate file) and Insecure option are not implemented. Insecure is MAY, but TLS cert configs are listed as MUST-available options. |
| 2 | MUST | ❌ not_found | Each configuration option MUST be overridable by a signal specific option (e.g., OTEL_EXPORTER_OTLP_TRACES_ENDPOINT overrides OTEL_EXPORTER_OTLP_ENDPOINT for traces). | - | Only generic otel.exporter.otlp.* keys are read in СоздатьТранспорт(). No per-signal overrides (traces, logs, metrics) exist for endpoint, protocol, headers, compression, or timeout. |
| 3 | MUST | ✅ found | The implementation MUST honor the following URL components: scheme (http or https), host, port, path. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:99` |  |
| 4 | MUST | ✅ found | When using OTEL_EXPORTER_OTLP_ENDPOINT, exporters MUST construct per-signal URLs as described below. The per-signal endpoint configuration options take precedence. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:35` |  |
| 5 | SHOULD | ✅ found | Endpoint (OTLP/gRPC): The option SHOULD accept any form allowed by the underlying gRPC client implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:174` |  |
| 6 | MUST | ✅ found | Endpoint (OTLP/gRPC): The option MUST accept a URL with a scheme of either http or https. A scheme of https indicates a secure connection. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:174` |  |
| 7 | SHOULD | ✅ found | If the gRPC client implementation does not support an endpoint with a scheme of http or https then the endpoint SHOULD be transformed to the most sensible format for that implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:174` |  |
| 8 | SHOULD | ✅ found | SDKs SHOULD default endpoint variables to use http scheme unless they have good reasons to choose https scheme for the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:153` |  |
| 9 | SHOULD | ➖ n_a | The environment variables OTEL_EXPORTER_OTLP_SPAN_INSECURE and OTEL_EXPORTER_OTLP_METRIC_INSECURE are obsolete. However, if they are already implemented, they SHOULD continue to be supported. | - | TLS/mTLS configuration is a platform limitation of OneScript. These obsolete insecure env vars were never implemented, so the conditional clause 'if they are already implemented' does not apply. |
| 10 | SHOULD | ⚠️ partial | The default protocol SHOULD be http/protobuf, unless there are strong reasons for SDKs to select grpc as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Default protocol is set to 'http/json' (line 150: Менеджер.Параметр("otel.exporter.otlp.protocol", "http/json")), not the recommended 'http/protobuf'. |
| 11 | MUST | ✅ found | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal: Traces v1/traces, Metrics v1/metrics, Logs v1/logs relative to OTEL_EXPORTER_OTLP_ENDPOINT base URL. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:35` |  |
| 12 | MUST | ❌ not_found | For the per-signal variables (OTEL_EXPORTER_OTLP_<signal>_ENDPOINT), the URL MUST be used as-is without any modification. | - | Per-signal endpoint variables (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_LOGS_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_ENDPOINT) are not supported at all. |
| 13 | MUST | ❌ not_found | The only exception is that if a per-signal URL contains no path part, the root path / MUST be used. | - | Per-signal endpoint variables are not implemented, so this root-path fallback logic is also absent. |
| 14 | MUST NOT | ⚠️ partial | An SDK MUST NOT modify the URL in ways other than specified above. If the port is empty or not given, TCP port 80 is the default for http and TCP port 443 for https. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:99` | Base URL construction from OTEL_EXPORTER_OTLP_ENDPOINT correctly appends signal paths. However, per-signal endpoint variables are not supported, so the 'as-is' requirement for them cannot be verified. Double-slash normalization (line 100-103) is a minor modification. |
| 15 | MUST | ⚠️ partial | Protocol: The transport protocol. Options MUST be one of: grpc, http/protobuf, http/json. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | grpc creates ОтелGrpcТранспорт (protobuf over gRPC). http/json and http/protobuf both create ОтелHttpТранспорт which sends JSON (Content-Type: application/json). http/protobuf is not truly supported as protobuf-over-HTTP - it falls through to JSON encoding. No validation rejects unknown protocol values. |

#### Specify Protocol

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specify-protocol)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ⚠️ partial | SDKs SHOULD support both grpc and http/protobuf transports. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | grpc is supported via ОтелGrpcТранспорт (protobuf encoding). HTTP transport exists (ОтелHttpТранспорт) but sends JSON, not protobuf. So http/protobuf is not truly supported - only grpc and http/json. |
| 17 | MUST | ✅ found | SDKs MUST support at least one of grpc and http/protobuf transports. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:37` |  |
| 18 | SHOULD | ⚠️ partial | If SDKs support only one transport, it SHOULD be http/protobuf. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:53` | The SDK supports two transports (grpc and http/json). However, http/protobuf is not truly supported - the HTTP transport always sends JSON. The spec recommends http/protobuf as the preferred single transport. |
| 19 | SHOULD | ⚠️ partial | If no configuration is provided the default transport SHOULD be http/protobuf unless SDKs have good reasons to choose grpc as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Default protocol is 'http/json' (not 'http/protobuf'). Line 150: Менеджер.Параметр("otel.exporter.otlp.protocol", "http/json"). |

#### Specifying headers via environment variables

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | All attribute values in OTEL_EXPORTER_OTLP_HEADERS (key1=value1,key2=value2 format) MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:467` |  |

#### Retry

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#retry)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | Transient errors MUST be handled with a retry strategy. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:166` |  |
| 22 | MUST | ✅ found | This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:167` |  |

#### Transient errors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#transient-errors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | SHOULD | ❌ not_found | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter. | - | No User-Agent header is set anywhere in ОтелHttpТранспорт or ОтелGrpcТранспорт. The HTTP transport sets Content-Type and optionally Content-Encoding headers, but not User-Agent. |
| 24 | SHOULD | ❌ not_found | The format of the User-Agent header SHOULD follow RFC 7231. | - | User-Agent header is not emitted at all, so RFC 7231 format compliance is moot. |
| 25 | SHOULD | ❌ not_found | The resulting User-Agent SHOULD include the exporter's default User-Agent string when a product identifier is added. | - | User-Agent header is not emitted at all, so there is no default User-Agent string to preserve. |

### Propagators

#### Operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Propagators MUST define Inject and Extract operations, in order to write values to and read values from carriers respectively. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:45` |  |
| 2 | MUST | ✅ found | Each Propagator type MUST define the specific carrier type and MAY define additional parameters. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:45` |  |

#### Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The Propagator MUST retrieve the appropriate value from the Context first, such as SpanContext, Baggage or another cross-cutting concern context. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:46` |  |
| 4 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception in order to preserve any previously existing valid value. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:90` |  |
| 5 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT store a new value in the Context, in order to preserve any previously existing valid value. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:90` |  |

#### TextMap Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | The key/value pairs MUST only consist of US-ASCII characters that make up valid HTTP header fields as per RFC 9110. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:62` |  |
| 7 | MUST | ✅ found | Getter and Setter MUST be stateless and allowed to be saved as constants, in order to effectively avoid runtime allocations. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:71` |  |

#### TextMap Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform Content-Type to content-type) if the used protocol is case insensitive. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:19` |  |
| 9 | MUST | ✅ found | The implementation MUST preserve casing if the used protocol is case sensitive. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:19` |  |

#### Getter argument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#getter-argument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The Keys function MUST return the list of all the keys in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:59` |  |
| 11 | MUST | ✅ found | The Get function MUST return the first value of the given propagation key or return null if the key doesn't exist. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:20` |  |
| 12 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the Get getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:21` |  |
| 13 | MUST | ✅ found | If explicitly implemented, the GetAll function MUST return all values of the given propagation key. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40` |  |
| 14 | SHOULD | ✅ found | GetAll SHOULD return values in the same order as they appear in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:43` |  |
| 15 | SHOULD | ✅ found | If the key doesn't exist, GetAll SHOULD return an empty collection. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:41` |  |
| 16 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the GetAll getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:42` |  |

#### Composite Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | Implementations MUST offer a facility to group multiple Propagators from different cross-cutting concerns in order to leverage them as a single entity. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:79` |  |
| 18 | MUST | ✅ found | There MUST be functions to accomplish the following operations: Create a composite propagator, Extract from a composite propagator, Inject into a composite propagator. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:18` |  |

#### Composite Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | The OpenTelemetry API MUST provide a way to obtain a propagator for each supported Propagator type | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |
| 20 | SHOULD | ✅ found | Instrumentation libraries SHOULD call propagators to extract and inject the context on all remote calls | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:18` |  |
| 21 | MUST | ✅ found | The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise | `src/Ядро/Модули/ОтелГлобальный.os:132` |  |
| 22 | SHOULD | ✅ found | If pre-configured, Propagators SHOULD default to a composite Propagator containing the W3C Trace Context Propagator and the Baggage Propagator specified in the Baggage API | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:341` |  |
| 23 | MUST | ✅ found | These platforms MUST also allow pre-configured propagators to be disabled or overridden | `src/Ядро/Модули/ОтелГлобальный.os:110` |  |

#### Get Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#get-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | This method MUST exist for each supported Propagator type. Returns a global Propagator. This usually will be composite instance. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |

#### Set Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#set-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | Set Global Propagator method MUST exist for each supported Propagator type. Sets the global Propagator instance. | `src/Ядро/Модули/ОтелГлобальный.os:110` |  |
| 26 | MUST | ✅ found | The official list of propagators that MUST be maintained by the OpenTelemetry organization: W3C TraceContext, W3C Baggage, B3 | `src/Пропагация/Классы/ОтелW3CПропагатор.os:1` |  |
| 27 | MUST | ✅ found | The official list of propagators MUST be distributed as OpenTelemetry extension packages: W3C TraceContext, W3C Baggage, B3 | `src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:1` |  |
| 28 | MUST NOT | ✅ found | OT Trace propagation format MUST NOT use 'OpenTracing' in the resulting propagator name as it is not widely adopted format in the OpenTracing ecosystem | - |  |
| 29 | MUST NOT | ✅ found | Additional Propagators implementing vendor-specific protocols such as AWS X-Ray trace header protocol MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories | - |  |

#### W3C Trace Context Requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#w3c-trace-context-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | A W3C Trace Context propagator MUST parse and validate the traceparent and tracestate HTTP headers as specified in W3C Trace Context Level 2 | `src/Пропагация/Классы/ОтелW3CПропагатор.os:81` |  |
| 31 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid traceparent value using the same header | `src/Пропагация/Классы/ОтелW3CПропагатор.os:63` |  |
| 32 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid tracestate unless the value is empty, in which case the tracestate header may be omitted | `src/Пропагация/Классы/ОтелW3CПропагатор.os:65` |  |

### Env Vars

#### Environment Variable Specification

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#environment-variable-specification)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If they do, they SHOULD use the names and value parsing behavior specified in this document. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:80` |  |
| 2 | SHOULD | ⚠️ partial | They SHOULD also follow the common configuration specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:59` | Используется configor (МенеджерПараметров) для чтения параметров, но не все аспекты common configuration specification реализованы (например, programmatic override, layered configuration). |

#### Implementation guidelines

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#implementation-guidelines)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The environment-based configuration MUST have a direct code configuration equivalent. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:59` |  |

#### Parsing empty value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#parsing-empty-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ⚠️ partial | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105` | Большинство переменных проверяют пустую строку (<> Неопределено И <> ""), например otel.resource.attributes (строка 105), otel.exporter.otlp.headers (строка 137), лимиты (строки 398-447). Однако otel.service.name (строка 114) и otel.traces.sampler (строка 191) проверяют только Неопределено без проверки на пустую строку. |

#### Type-specific guidance### Boolean

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#type-specific-guidance-boolean)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Any value that represents a Boolean MUST be set to true only by the case-insensitive string "true", meaning "True" or "TRUE" are also accepted, as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 6 | MUST NOT | ✅ found | An implementation MUST NOT extend this definition and define additional values that are interpreted as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 7 | MUST | ⚠️ partial | Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562` | Логика парсинга булева верна (НРег(Значение) = "true"), но otel.enabled использует значение по умолчанию "true" (строка 562: Менеджер.Параметр("otel.enabled", "true")), из-за чего при отсутствии переменной возвращается true вместо false. Также используется нестандартная OTEL_ENABLED вместо спецификационной OTEL_SDK_DISABLED. |
| 8 | SHOULD | ❌ not_found | If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied. | - | Нет логирования предупреждения при получении некорректного булева значения. Функция Включено() (строка 561-564) молча возвращает Ложь для любого не-true значения без предупреждения. |
| 9 | SHOULD | ❌ not_found | All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior. | - | Используется OTEL_ENABLED (по умолчанию true = включен) вместо спецификационной OTEL_SDK_DISABLED (по умолчанию false = включен). Спецификация требует, чтобы false было безопасным значением по умолчанию, но OTEL_ENABLED=false отключает SDK, а спецификация предусматривает OTEL_SDK_DISABLED=false для включённого состояния. |
| 10 | MUST NOT | ✅ found | Renaming or changing the default value MUST NOT happen without a major version upgrade. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562` |  |

#### Numeric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#numeric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ❌ not_found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them as not set. | - | Числовые значения парсятся через Число() без обёртки в Попытка/Исключение (строки 224-227, 263-266, 312, 399-416). При некорректном значении возникает необработанное исключение вместо предупреждения и использования значения по умолчанию. |
| 12 | SHOULD | ❌ not_found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD gracefully ignore the setting, i.e., treat them as not set. | - | При непарсящемся числовом значении Число() выбрасывает исключение вместо того, чтобы молча использовать значение по умолчанию. Нет try/catch обёртки вокруг вызовов Число() для env-var параметров. |

#### String

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#string)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | SHOULD | ⚠️ partial | Enum values SHOULD be interpreted in a case-insensitive manner. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:344` | Пропагаторы (строка 344: НРег()) и фильтр экземпляров (ОтелПостроительПровайдераМетрик.os:115: НРег()) сравниваются case-insensitive. Однако имена сэмплеров (строки 197-218: прямое сравнение "always_on", "always_off" и т.д.) и имена экспортеров (строки 177, 255, 291: прямое сравнение "none", "otlp") НЕ используют case-insensitive сравнение. |
| 14 | MUST | ⚠️ partial | For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:373` | Для пропагаторов выводится предупреждение при неизвестном значении (строка 373: Сообщить("неизвестный пропагатор")). Однако неизвестный сэмплер молча использует fallback на ParentBased(AlwaysOn) без предупреждения (строки 216-218). Неизвестный экспортер молча обрабатывается как otlp. Фильтр экземпляров (ОтелПостроительПровайдераМетрик.os:123) молча игнорирует без предупреждения. |

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
| 1 | SHOULD | ➖ n_a | Resource detectors SHOULD have a unique name for reference in configuration. | - | Resource Detector Naming is a conditional Development feature that is not implemented. Detectors exist but have no naming mechanism. |
| 2 | SHOULD | ➖ n_a | Names SHOULD be snake case and consist of lowercase alphanumeric and _ characters, which ensures they conform to declarative configuration property name requirements. | - | Resource Detector Naming is a conditional Development feature that is not implemented. |
| 3 | SHOULD | ➖ n_a | Resource detector names SHOULD reflect the root namespace of attributes they populate. | - | Resource Detector Naming is a conditional Development feature that is not implemented. |
| 4 | SHOULD | ➖ n_a | Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name which appropriately conveys their purpose. | - | Resource Detector Naming is a conditional Development feature that is not implemented. |
| 5 | SHOULD | ➖ n_a | An SDK which identifies multiple resource detectors with the same name SHOULD report an error. | - | Resource Detector Naming is a conditional Development feature that is not implemented. |
| 6 | SHOULD | ➖ n_a | Resource detectors SHOULD document their name in a manner which is easily discoverable. | - | Resource Detector Naming is a conditional Development feature that is not implemented. |
| 7 | MUST | ✅ found | The SDK MUST extract information from the OTEL_RESOURCE_ATTRIBUTES environment variable and merge this, as the secondary resource, with any resource information provided by the user, i.e. the user provided resource information has higher priority. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:96` |  |
| 8 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:479` |  |
| 9 | MUST | ❌ not_found | The , and = characters in keys and values MUST be percent encoded. | - | The parser in РазобратьПарыКлючЗначение (ОтелАвтоконфигурация.os:467) splits on ',' and '=' directly without any percent-decoding of the keys and values. Percent-encoded characters like %2C and %3D are not decoded. |
| 10 | SHOULD | ❌ not_found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | - | The parser in РазобратьПарыКлючЗначение does not have error handling for malformed input - it silently skips entries without '=' but does not discard the entire value or report an error. |
| 11 | SHOULD | ❌ not_found | In case of any error during decoding, an error SHOULD be reported following the Error Handling principles. | - | No error reporting mechanism exists for failures during OTEL_RESOURCE_ATTRIBUTES parsing. The parser silently ignores malformed entries. |

### Trace Api

#### Tracer operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracer-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The Tracer MUST provide functions to: Create a new Span. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 2 | SHOULD | ✅ found | The Tracer SHOULD provide functions to: Report if Tracer is Enabled. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 3 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when creating Spans, a Tracer SHOULD provide this Enabled API. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 4 | MUST | ✅ found | There are currently no required parameters for this API. Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 5 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 6 | SHOULD | ❌ not_found | The API SHOULD be documented that instrumentation authors needs to call this API each time they create a new Span to ensure they have the most up-to-date response. | - | Документация метода Включен() не содержит указания о необходимости вызывать его перед каждым созданием спана для получения актуального ответа. |

### Trace Sdk

#### Tracer Provider### Tracer Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer-provider-tracer-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create Tracer instances through a TracerProvider (see API). | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 2 | MUST | ✅ found | The TracerProvider MUST implement the Get a Tracer API. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Tracer. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:63-72` |  |
| 4 | MUST | ✅ found | The TracerProvider MUST compute the relevant TracerConfig using the configured TracerConfigurator, and create a Tracer whose behavior conforms to that TracerConfig. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:71-72` |  |

#### TracerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The TracerConfigurator function MUST accept the following parameter: tracer_scope - the InstrumentationScope of the Tracer. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:215-224` |  |
| 2 | MUST | ✅ found | The TracerConfigurator function MUST return the relevant TracerConfig, or some signal indicating that the default TracerConfig should be used. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:215-224` |  |
| 3 | MUST | ✅ found | Shutdown MUST be called only once for each TracerProvider instance. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:107-114` |  |
| 4 | SHOULD | ✅ found | After the call to Shutdown, subsequent attempts to get a Tracer are not allowed. SDKs SHOULD return a valid no-op Tracer for these calls, if possible. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65-66` |  |
| 5 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:107-114` | Метод Закрыть() является процедурой (void), не возвращает статус успеха/неуспеха/таймаута. Есть асинхронный вариант ЗакрытьАсинхронно() через Обещание, но синхронный не возвращает результат. |
| 6 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:107-114` | Метод Закрыть() не имеет механизма таймаута. Асинхронный вариант ЗакрытьАсинхронно() использует Обещание, которое поддерживает таймаут через Получить(секунды), но таймаут не встроен в сам метод. |
| 7 | MUST | ✅ found | Shutdown MUST be implemented at least by invoking Shutdown within all internal processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:111-113` |  |

#### Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Tracer MUST behave according to the TracerConfig computed during Tracer creation. | `src/Трассировка/Классы/ОтелТрассировщик.os:38-43` |  |
| 2 | MUST | ❌ not_found | If the TracerProvider supports updating the TracerConfigurator, then upon update the Tracer MUST be updated to behave according to the new TracerConfig. | - | TracerProvider хранит Конфигуратор (строка 28), но при его обновлении уже созданные трассировщики (кешированные в Трассировщики: СинхронизированнаяКарта) не пересчитывают свою конфигурацию. Нет механизма обновления TracerConfig у существующих Tracer-ов при изменении TracerConfigurator. |

#### TracerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the enabled parameter SHOULD default to true (i.e. Tracers are enabled by default). | `src/Трассировка/Классы/ОтелКонфигурацияТрассировщика.os:35` |  |
| 2 | MUST | ✅ found | If a Tracer is disabled, it MUST behave equivalently to a No-op Tracer. | `src/Трассировка/Классы/ОтелТрассировщик.os:38-43` |  |
| 3 | MUST | ⚠️ partial | The value of enabled MUST be used to resolve whether a Tracer is Enabled. If enabled is false, Enabled returns false. If enabled is true, Enabled returns true. | `src/Трассировка/Классы/ОтелТрассировщик.os:38-43` | Когда Конфигурация.Включен() = false, Включен() корректно возвращает Ложь. Однако когда Конфигурация.Включен() = true, результат зависит ещё от наличия процессоров (строка 42), что означает enabled=true не всегда даёт Enabled=true. Это пересекается с требованием секции Enabled, но формально данное требование говорит: если enabled=true, Enabled returns true. |
| 4 | MUST | ⚠️ partial | The changes to enabled parameter MUST be eventually visible. | - | Конфигурация хранится как ссылка на ОтелКонфигурацияТрассировщика в поле Трассировщик.Конфигурация, но нет механизма обновления конфигурации у существующего трассировщика. Поле устанавливается только при создании и не обновляется динамически. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Enabled MUST return false when either: there are no registered SpanProcessors, or Tracer is disabled (TracerConfig.enabled is false). | `src/Трассировка/Классы/ОтелТрассировщик.os:38-43` |  |
| 2 | SHOULD | ✅ found | Otherwise, Enabled SHOULD return true. | `src/Трассировка/Классы/ОтелТрассировщик.os:42` |  |

#### AlwaysOn* Returns `RECORD_AND_SAMPLE` always.* Description MUST be `AlwaysOnSampler`.#### AlwaysOff* Returns `DROP` always.* Description MUST be `AlwaysOffSampler`.#### TraceIdRatioBased

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwayson-returns-recordandsample-always-description-must-be-alwaysonsampler-alwaysoff-returns-drop-always-description-must-be-alwaysoffsampler-traceidratiobased)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | AlwaysOn Description MUST be AlwaysOnSampler. | `src/Трассировка/Модули/ОтелСэмплер.os:109` |  |
| 2 | MUST | ✅ found | AlwaysOff Description MUST be AlwaysOffSampler. | `src/Трассировка/Модули/ОтелСэмплер.os:111` |  |
| 3 | MUST NOT | ✅ found | OpenTelemetry SDK implementors SHALL NOT remove or modify the behavior of the original TraceIdRatioBased sampler until at least January 1, 2027. | `src/Трассировка/Модули/ОтелСэмплер.os:81-83` |  |
| 4 | MUST | ✅ found | The TraceIdRatioBased MUST ignore the parent SampledFlag. | `src/Трассировка/Модули/ОтелСэмплер.os:275-297` |  |
| 5 | MUST | ✅ found | Description MUST return a string of the form TraceIdRatioBased{RATIO} with RATIO replaced with the Sampler instance's trace sampling ratio represented as a decimal number. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 6 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 7 | SHOULD | ✅ found | The precision SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 8 | MUST | ✅ found | The sampling algorithm MUST be deterministic. A trace identified by a given TraceId is sampled or not independent of language, time, etc. | `src/Трассировка/Модули/ОтелСэмплер.os:288-296` |  |
| 9 | MUST | ✅ found | Implementations MUST use a deterministic hash of the TraceId when computing the sampling decision. | `src/Трассировка/Модули/ОтелСэмплер.os:288-290` |  |
| 10 | MUST | ✅ found | A TraceIdRatioBased sampler with a given sampling probability MUST also sample all traces that any TraceIdRatioBased sampler with a lower sampling probability would sample. | `src/Трассировка/Модули/ОтелСэмплер.os:290-296` |  |
| 11 | SHOULD | ❌ not_found | When this sampler observes a non-empty parent span context (used not as root sampler), the SDK SHOULD emit a warning such as: WARNING: The TraceIdRatioBased sampler is operating as a child sampler. | - | Нет предупреждения при использовании TraceIdRatioBased как дочернего семплера. Код СэмплироватьПоДоле не проверяет наличие родительского контекста. |
| 12 | MUST | ❌ not_found | The ProbabilitySampler sampler MUST ignore the parent SampledFlag. | - | ProbabilitySampler не реализован. Существуют только AlwaysOn, AlwaysOff, TraceIdRatioBased и ParentBased. |
| 13 | SHOULD | ❌ not_found | When ProbabilitySampler returns RECORD_AND_SAMPLE, the OpenTelemetry TraceState SHOULD be modified to include the key-value th:T for rejection threshold value. | - | ProbabilitySampler не реализован. |
| 14 | SHOULD | ❌ not_found | When a ProbabilitySampler Sampler makes a decision for a non-root Span using TraceID randomness when the Trace random flag was not set, the SDK SHOULD issue a warning statement. | - | ProbabilitySampler не реализован. |
| 15 | MUST | ❌ not_found | AlwaysRecord MUST behave as follows: DROP -> RECORD_ONLY, RECORD_ONLY -> RECORD_ONLY, RECORD_AND_SAMPLE -> RECORD_AND_SAMPLE. | - | AlwaysRecord семплер-декоратор не реализован. |
| 16 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the parameters passed to delegate GetSamplingIntent methods, as they are considered read-only state. | - | ComposableSampler и GetSamplingIntent не реализованы. |
| 17 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the OpenTelemetry TraceState (i.e., the ot sub-key of TraceState). | - | ComposableSampler не реализован. |
| 18 | MUST NOT | ❌ not_found | The explicit randomness values MUST not be modified by ComposableSamplers. | - | ComposableSampler не реализован. |
| 19 | SHOULD | ❌ not_found | A ComposableProbability ratio value of 0 is considered non-probabilistic. For the zero case a ComposableAlwaysOff instance SHOULD be returned instead. | - | ComposableProbability не реализован. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | Custom implementations of the IdGenerator SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace random flag will be set in the associated Trace contexts. | - | Нет механизма для пользовательского IdGenerator сообщить о соответствии W3C Level 2 randomness (маркерный интерфейс или свойство). Генератор устанавливается через УстановитьГенераторИд(), но нет способа указать, что он генерирует random-совместимые TraceId. |

#### OnEnding

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onending)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The end timestamp MUST have been computed (the OnEnding method duration is not included in the span duration). | `src/Трассировка/Классы/ОтелСпан.os:449` |  |
| 2 | MUST | ✅ found | The Span object MUST still be mutable (i.e., SetAttribute, AddLink, AddEvent can be called) while OnEnding is called. | `src/Трассировка/Классы/ОтелСпан.os:455` |  |
| 3 | MUST | ✅ found | This method MUST be called synchronously within the Span.End() API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:455` |  |
| 4 | MUST | ✅ found | The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking OnEnding of the first SpanProcessor. All registered SpanProcessor OnEnding callbacks are executed before any SpanProcessor's OnEnd callback is invoked. | `src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:33` |  |

### Logs Api

#### Ergonomic API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#ergonomic-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | The ergonomic API SHOULD make it more convenient to emit event records following the event semantics. | - | Удобное API для событий (event records) не реализовано. Есть только стандартное API через СоздатьЗаписьЛога() + Записать(), но нет дополнительного ergonomic слоя для упрощённой отправки событий (аналог logger.info('msg') или logger.event('name')). |
| 2 | SHOULD | ❌ not_found | The design of the ergonomic API SHOULD be idiomatic for its language. | - | Эргономичное API не реализовано, поэтому требование к его идиоматичному дизайну также не выполнено. |

### Logs Sdk

#### Logger Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create Logger instances through a LoggerProvider (see API). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 2 | MUST | ✅ found | The LoggerProvider MUST implement the Get a Logger API. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Logger. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:64` |  |
| 4 | MUST | ✅ found | In the case where an invalid name (null or empty string) is specified, a working Logger MUST be returned as a fallback rather than returning null or throwing an exception. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 5 | SHOULD | ✅ found | its name SHOULD keep the original invalid value | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:93` |  |
| 6 | SHOULD | ❌ not_found | and a message reporting that the specified value is invalid SHOULD be logged. | - | В ОтелПровайдерЛогирования.ПолучитьЛоггер() отсутствует проверка имени на пустоту/null и нет логирования предупреждения о невалидном имени. |
| 7 | MUST | ✅ found | The LoggerProvider MUST compute the relevant LoggerConfig using the configured LoggerConfigurator, and create a Logger whose behavior conforms to that LoggerConfig. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:69` |  |

#### LoggerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: logger_scope: The InstrumentationScope of the Logger. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:72` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant LoggerConfig, or some signal indicating that the default LoggerConfig should be used. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:72` |  |
| 3 | MUST | ✅ found | Shutdown MUST be called only once for each LoggerProvider instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117` |  |
| 4 | SHOULD | ✅ found | After the call to Shutdown, subsequent attempts to get a Logger are not allowed. SDKs SHOULD return a valid no-op Logger for these calls, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:59` |  |
| 5 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:116` | Синхронный метод Закрыть() - Процедура (void), не возвращает статус. Асинхронный ЗакрытьАсинхронно() возвращает Обещание, но без явного индикатора успеха/неудачи/таймаута. |
| 6 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:143` | ЗакрытьАсинхронно() возвращает Обещание, которое поддерживает таймаут через Обещание.Получить(таймаут), но синхронный Закрыть() не имеет встроенного таймаута. |
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
| 6 | MUST | ✅ found | If trace_based is true, log records associated with unsampled traces MUST be dropped by the Logger. | `src/Логирование/Классы/ОтелЛоггер.os:57-58` |  |
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
| 6 | MUST | ✅ found | Minimum severity: If the log record's SeverityNumber is specified (i.e. not 0) and is less than the configured minimum_severity, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:138-142` |  |
| 7 | MUST | ✅ found | Trace-based: If trace_based is true, and if the log record has a SpanId and the TraceFlags SAMPLED flag is unset, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:143-145` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Enabled MUST return false when either: there are no registered LogRecordProcessors; Logger is disabled (LoggerConfig.enabled is false); the provided severity is specified and is less than the configured minimum_severity; trace_based is true and current context is associated with an unsampled trace; all registered LogRecordProcessors implement Enabled and return false. | `src/Логирование/Классы/ОтелЛоггер.os:42-62` |  |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return true. | `src/Логирование/Классы/ОтелЛоггер.os:61` |  |

### Metrics Api

#### General characteristics#### Instrument name syntax

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-characteristics-instrument-name-syntax)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD treat the unit as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:219` |  |
| 2 | MUST | ✅ found | The unit MUST be case-sensitive, ASCII string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:219` |  |
| 3 | MUST | ✅ found | The API MUST treat the description as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:227` |  |
| 4 | MUST | ✅ found | The description MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:227` |  |
| 5 | MUST | ✅ found | The description MUST support at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:227` |  |
| 6 | MUST | ✅ found | OpenTelemetry SDKs MUST handle advisory parameters as described here. | `src/Метрики/Классы/ОтелМетр.os:642` |  |

### Metrics Sdk

#### Meter Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create Meter instances through a MeterProvider (see API). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 2 | MUST | ✅ found | The MeterProvider MUST implement the Get a Meter API. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Meter. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:62` |  |
| 4 | MUST | ⚠️ partial | In the case where an invalid name (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` | ПолучитьМетр не содержит явной обработки невалидного имени. Для пустой строки метр создаётся и работает (OK), но для null (Неопределено) произойдёт ошибка при создании ОтелОбластьИнструментирования и формировании ключа (конкатенация Неопределено + строка). |
| 5 | SHOULD | ⚠️ partial | its name SHOULD keep the original invalid value | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` | Для пустой строки имя сохраняется как есть (случайно корректное поведение), но нет явной обработки невалидного имени - для null случай не обработан. |
| 6 | SHOULD | ❌ not_found | a message reporting that the specified value is invalid SHOULD be logged | - | В методе ПолучитьМетр отсутствует какое-либо логирование предупреждений о невалидном имени. |
| 7 | MUST | ✅ found | The MeterProvider MUST compute the relevant MeterConfig using the configured MeterConfigurator, and create a Meter whose behavior conforms to that MeterConfig. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:206` |  |

#### MeterConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: meter_scope: The InstrumentationScope of the Meter. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:210` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant MeterConfig, or some signal indicating that the default MeterConfig should be used. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:210` |  |
| 3 | MUST | ⚠️ partial | Shutdown MUST be called only once for each MeterProvider instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` | Метод Закрыть() не содержит защиты от повторного вызова - нет проверки 'Если Закрыт Тогда Возврат' в начале метода. При повторном вызове будут попытки повторно закрыть читателей. |
| 4 | SHOULD | ✅ found | After the call to Shutdown, subsequent attempts to get a Meter are not allowed. SDKs SHOULD return a valid no-op Meter for these calls, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:57` |  |
| 5 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` | Синхронный метод Закрыть() - Процедура (void), не возвращает статус. Есть ЗакрытьАсинхронно возвращающий Обещание, но синхронный вариант не информирует о результате. |
| 6 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:164` | ЗакрытьАсинхронно возвращает Обещание с поддержкой таймаута, но синхронный метод Закрыть() не принимает параметр таймаута. |
| 7 | MUST | ✅ found | Shutdown MUST be implemented at least by invoking Shutdown on all registered MetricReader and MetricExporter instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:136` |  |

#### Start timestamps

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#start-timestamps)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp, or the creation time of the instrument if this is the first collection interval for the instrument. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138-146` | При delta-очистке (строка 145) ВремяСтарта обновляется на текущее время, что соответствует 'previous collection timestamp'. Но для первого интервала ВремяСтарта устанавливается в конструкторе (строка 263), что является временем создания инструмента - это корректно. |
| 2 | MUST | ⚠️ partial | This implies that all data points with delta temporality aggregation for an instrument MUST share the same start timestamp. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:283` | Все точки данных в одном цикле сбора используют одно и то же ВремяСтарта (строка 283), что соответствует требованию. Однако нет строгой гарантии что при одновременных сборах из разных reader'ов start timestamps совпадут. |
| 3 | MUST | ⚠️ partial | Cumulative timeseries MUST use a consistent start timestamp for all collection intervals. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141-146` | При кумулятивной временности (строка 141-142) аккумуляторы и ВремяСтарта не очищаются, что сохраняет начальный start timestamp. Это корректно реализует консистентный start timestamp. |
| 4 | SHOULD | ⚠️ partial | For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the series. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:263` | Start timestamp устанавливается при создании инструмента (строка 263), а не при первом измерении. Все серии используют одно время старта - время создания инструмента, а не время первого измерения для конкретной серии. |
| 5 | SHOULD | ⚠️ partial | For asynchronous instrument, the start timestamp SHOULD be: the creation time of the instrument if the first series measurement occurred in the first collection interval, otherwise the timestamp of the collection interval prior to the first series measurement. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:184` | В ОтелБазовыйНаблюдаемыйИнструмент.ПреобразоватьЗаписиВТочки() startTimeUnixNano устанавливается как ВремяСейчас (текущее время сбора), а не как время создания инструмента или предыдущего интервала. |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instrument registrations. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 2 | MUST | ✅ found | Meter MUST behave according to the MeterConfig computed during Meter creation. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:73` |  |
| 3 | MUST | ❌ not_found | If the MeterProvider supports updating the MeterConfigurator, then upon update the Meter MUST be updated to behave according to the new MeterConfig. | - | There is no mechanism to update MeterConfig after creation. The Конфигуратор is applied once during ПолучитьМетр but there is no method to recompute or update configs for already-created meters. |

#### MeterConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the enabled parameter SHOULD default to true (i.e. Meters are enabled by default). | `src/Метрики/Классы/ОтелКонфигурацияМетра.os:35` |  |
| 2 | MUST | ✅ found | If a Meter is disabled, it MUST behave equivalently to No-op Meter. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:79` |  |
| 3 | MUST | ✅ found | The value of enabled MUST be used to resolve whether an instrument is Enabled. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:202` |  |
| 4 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Метрики/Классы/ОтелМетр.os:504` |  |

#### Instrument enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | The synchronous instrument Enabled MUST return false when either: the MeterConfig of the Meter used to create the instrument has parameter enabled=false, or all resolved views for the instrument are configured with the Drop Aggregation. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` | Enabled checks MeterConfig.enabled via МетрВключен.Получить() and its own Включен flag, but the Drop Aggregation check is not automatically wired - Включен must be explicitly set to false by calling Отключить(), there is no automatic detection of all-Drop views at instrument creation time. |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return true. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |

#### MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | To construct a MetricReader when setting up an SDK, at least the exporter to use, which is a MetricExporter instance, SHOULD be provided. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:276` |  |
| 2 | SHOULD | ⚠️ partial | The default output aggregation (optional), a function of instrument kind, SHOULD be obtained from the exporter. | - | MetricReader не запрашивает у экспортера дефолтную агрегацию. Агрегация определяется на уровне инструментов и представлений, но MetricReader не конфигурируется отдельной функцией агрегации от экспортера. |
| 3 | SHOULD | ✅ found | The output temporality (optional), a function of instrument kind, SHOULD be obtained from the exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:167` |  |
| 4 | SHOULD | ✅ found | If temporality is not configured, the Cumulative temporality SHOULD be used. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:88` |  |
| 5 | SHOULD | ❌ not_found | The default aggregation cardinality limit (optional) to use, a function of instrument kind. If not configured, a default value of 2000 SHOULD be used. | - | MetricReader не имеет параметра лимита мощности по умолчанию 2000. Лимит мощности настраивается через View (ОтелПредставление.ЛимитМощностиАгрегации), но дефолтное значение 2000 на уровне MetricReader не реализовано. |
| 6 | SHOULD | ✅ found | A MetricReader SHOULD provide the MetricFilter to the SDK or registered MetricProducer(s) when calling the Produce operation. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:115` |  |
| 7 | SHOULD | ✅ found | A common implementation of MetricReader, the periodic exporting MetricReader SHOULD be provided to be used typically with push-based metrics collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:1` |  |
| 8 | MUST | ✅ found | The MetricReader MUST ensure that data points from OpenTelemetry instruments are output in the configured aggregation temporality for each instrument kind. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:167` |  |
| 9 | MUST | ✅ found | For synchronous instruments with Cumulative aggregation temporality, MetricReader.Collect MUST receive data points exposed in previous collections regardless of whether new measurements have been recorded. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138` |  |
| 10 | MUST | ✅ found | For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:142` |  |
| 11 | MUST | ✅ found | For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:112` |  |
| 12 | MUST | ✅ found | For instruments with Cumulative aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST repeat the same starting timestamps. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141` |  |
| 13 | MUST | ✅ found | For instruments with Delta aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST advance the starting timestamp. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:145` |  |
| 14 | MUST | ⚠️ partial | The ending timestamp (i.e. TimeUnixNano) MUST always be equal to time the metric data point took effect, which is equal to when MetricReader.Collect was invoked. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:283` | Время конца точки данных устанавливается при вызове Собрать() (ТекущееВремяВНаносекундах()), что соответствует моменту сбора. Однако это время берется при сборе каждого инструмента, а не строго при вызове MetricReader.Collect - может быть небольшое отклонение между инструментами. |
| 15 | MUST | ✅ found | The SDK MUST support multiple MetricReader instances to be registered on the same MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:107` |  |
| 16 | SHOULD NOT | ✅ found | The MetricReader.Collect invocation on one MetricReader instance SHOULD NOT introduce side-effects to other MetricReader instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` |  |
| 17 | MUST NOT | ❌ not_found | The SDK MUST NOT allow a MetricReader instance to be registered on more than one MeterProvider instance. | - | Нет проверки при регистрации читателя, что он уже не привязан к другому MeterProvider. Читатель может быть зарегистрирован на нескольких провайдерах без предупреждения. |
| 18 | SHOULD | ✅ found | The SDK SHOULD provide a way to allow MetricReader to respond to MeterProvider.ForceFlush and MeterProvider.Shutdown. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` |  |
| 19 | SHOULD | ⚠️ partial | If default aggregation is not configured, the default aggregation SHOULD be used. | - | Агрегация по умолчанию используется через механизм агрегаторов инструментов, но явной настройки дефолтной агрегации на уровне MetricReader нет - она определяется типом инструмента напрямую. |

#### Produce batch

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#produce-batch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | Produce MUST return a batch of Metric Points, filtered by the optional metricFilter parameter. | - | No Produce method exists on a MetricProducer interface. The filtering via MetricFilter is implemented inside the readers (ОтелПериодическийЧитательМетрик lines 240-254, ОтелПрометеусЧитательМетрик lines 167-182) but not as a standalone Produce method returning a batch. |
| 2 | SHOULD | ⚠️ partial | Implementation SHOULD use the filter as early as possible to gain as much performance gain possible (memory allocation, internal metric fetching, etc). | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:240` | Filtering is applied after data collection (in МетрикаОтброшена called after Инструмент.Собрать), not as early as possible. The metric-level filter (Drop) skips adding to results, but data is already collected. For partial acceptance, attributes are filtered after collection. |
| 3 | SHOULD | ❌ not_found | If the batch of Metric Points includes resource information, Produce SHOULD require a resource as a parameter. | - | No Produce method exists. The resource is obtained from the Meter internally (Метр.Ресурс() in СобратьДанныеМетра), not passed as a parameter to a Produce function. |
| 4 | SHOULD | ❌ not_found | Produce SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | No Produce method exists as a MetricProducer interface. The internal collection methods (СобратьИЭкспортировать) do not return success/failure status to callers. |
| 5 | SHOULD | ❌ not_found | If a batch of Metric Points can include InstrumentationScope information, Produce SHOULD include a single InstrumentationScope which identifies the MetricProducer. | - | No MetricProducer with Produce method exists. The readers include InstrumentationScope from each Meter (МетрОбласть = Метр.ОбластьИнструментирования()), but there is no InstrumentationScope identifying a MetricProducer itself. |

### Env Vars

#### Prometheus Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#prometheus-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD NOT | ✅ found | "logging" is a deprecated value for OTEL_TRACES_EXPORTER left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:177` |  |
| 2 | SHOULD NOT | ✅ found | "logging" is a deprecated value for OTEL_METRICS_EXPORTER left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:291` |  |
| 3 | SHOULD NOT | ✅ found | "logging" is a deprecated value for OTEL_LOGS_EXPORTER left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:255` |  |
| 4 | MUST | ❌ not_found | When OTEL_CONFIG_FILE is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored. | - | OTEL_CONFIG_FILE (декларативная конфигурация) не реализован в SDK. Нет кода для чтения файла конфигурации, парсинга и игнорирования других переменных окружения. |

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

