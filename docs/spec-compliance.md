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
| Найдено требований (Stable universal) | 631 |
| ✅ Реализовано (found) | 488 (77.3%) |
| ⚠️ Частично (partial) | 78 (12.4%) |
| ❌ Не реализовано (not_found) | 65 (10.3%) |
| ➖ Неприменимо (n_a) | 0 |
| **MUST/MUST NOT found** | 342/375 (91.2%) |
| **SHOULD/SHOULD NOT found** | 146/256 (57.0%) |

## Соответствие по разделам (Stable)

| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |
|---|---|---|---|---|---|---|
| Context | 14 | 1 | 0 | 0 | 15 | 93.3% |
| Baggage Api | 16 | 1 | 0 | 0 | 17 | 94.1% |
| Resource Sdk | 11 | 1 | 3 | 0 | 15 | 73.3% |
| Trace Api | 103 | 6 | 11 | 0 | 120 | 85.8% |
| Trace Sdk | 53 | 14 | 8 | 0 | 75 | 70.7% |
| Logs Api | 20 | 1 | 0 | 0 | 21 | 95.2% |
| Logs Sdk | 43 | 11 | 1 | 0 | 55 | 78.2% |
| Metrics Api | 60 | 3 | 10 | 0 | 73 | 82.2% |
| Metrics Sdk | 122 | 25 | 21 | 0 | 168 | 72.6% |
| Otlp Exporter | 10 | 9 | 6 | 0 | 25 | 40.0% |
| Propagators | 30 | 1 | 1 | 0 | 32 | 93.8% |
| Env Vars | 6 | 5 | 4 | 0 | 15 | 40.0% |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Context]** [MUST] The API MUST accept the following parameters: The Context.  
  Нет метода Attach/Присоединить, принимающего объект Context (ФиксированноеСоответствие). Вместо этого УстановитьЗначение(Ключ, Значение) создаёт новый контекст внутри себя. Нельзя сделать текущим произвольный заранее собранный контекст. (`src/Ядро/Модули/ОтелКонтекст.os:203`)

- ⚠️ **[Resource Sdk]** [MUST] Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK.  
  Детекторы реализованы как отдельные классы (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора), но они включены в тот же пакет SDK (lib.config), а не в отдельные пакеты. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1`)

- ❌ **[Resource Sdk]** [MUST] Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions.  
  Детекторы (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) создают ресурс через Новый ОтелРесурс(Истина), что означает без умолчаний и без SchemaURL. Ни один детектор не устанавливает Schema URL. (-)

- ❌ **[Resource Sdk]** [MUST] If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources.  
  В ОтелРесурс.ЗаполнитьАтрибутыПоУмолчанию() (строка 108-118) детекторы просто мержатся без проверки Schema URL конфликтов. Метод Слить() в строках 41-44 обрабатывает конфликт SchemaURL, но при инициализации ресурса мерж атрибутов детекторов происходит напрямую, минуя Слить(). (-)

- ⚠️ **[Trace Api]** [MUST NOT] This API MUST NOT accept a Span or SpanContext as parent, only a full Context  
  НачатьДочернийСпан accepts ОтелСпан or ОтелКонтекстСпана as parent (line 127-128), not a full Context object. The spec requires only a full Context as parent, not a Span or SpanContext directly (`src/Трассировка/Классы/ОтелТрассировщик.os:133`)

- ⚠️ **[Trace Sdk]** [MUST] For backwards compatibility it MUST also be able to access the InstrumentationLibrary [deprecated since 1.10.0] having the same name and version values as the InstrumentationScope  
  Нет отдельного класса/интерфейса InstrumentationLibrary. Есть только ОтелОбластьИнструментирования (InstrumentationScope), который содержит имя и версию, но устаревший InstrumentationLibrary не выделен как отдельная сущность для обратной совместимости (`src/Трассировка/Классы/ОтелСпан.os:170`)

- ⚠️ **[Trace Sdk]** [MUST] Span Exporters MUST receive those spans which have Sampled flag set to true.  
  Exporters receive all spans passed by processors. Since the SDK drops DROP-decision spans entirely (returns NoopSpan) and creates real spans only for RECORD_ONLY and RECORD_AND_SAMPLE, both reach the exporter. The RECORD_AND_SAMPLE spans (Sampled=true) do reach the exporter, but so do RECORD_ONLY spans (Sampled=false) since there is no filtering. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37`)

- ⚠️ **[Trace Sdk]** [MUST] If the parent SpanContext contains a valid TraceId, they [TraceId of the Span to be created and parent TraceId] MUST always match.  
  The code does reuse the parent's TraceId for child spans (line 61), so they match. However, the ShouldSample method signature (ОтелСэмплер.ДолженСэмплировать) does not receive the full set of required arguments per spec (Context with parent Span, TraceId, Name, SpanKind, initial Attributes, Links). It receives strategy, ratio, TraceId, parent-sampled, has-parent, root-strategy - different from spec. (`src/Трассировка/Классы/ОтелТрассировщик.os:61`)

- ❌ **[Trace Sdk]** [MUST NOT] SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value (the rv sub-key).  
  The SDK has no awareness of the rv sub-key in OpenTelemetry TraceState. There is no code that reads or writes the rv sub-key. Since the SDK never touches rv, it technically doesn't overwrite it, but there's also no explicit protection against overwriting it. (-)

- ⚠️ **[Trace Sdk]** [MUST] The built-in SpanProcessors MUST do so (call exporter's Export with all spans and then invoke ForceFlush on the exporter).  
  Встроенные процессоры вызывают Export для всех оставшихся спанов, но не вызывают ForceFlush на экспортере. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120`)

- ❌ **[Trace Sdk]** [MUST] If a timeout is specified, the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. It MAY skip or abort some or all Export or ForceFlush calls it has made to achieve this goal.  
  Метод СброситьБуфер() не принимает параметр таймаута и не реализует логику прерывания по таймауту. Нет возможности указать таймаут для ForceFlush. (-)

- ⚠️ **[Logs Sdk]** [MUST] maxExportBatchSize - the maximum batch size of every export. It must be smaller or equal to maxQueueSize.  
  Значения по умолчанию соответствуют (МаксРазмерПакета=512 <= МаксРазмерБуфера=2048), но нет валидации при установке пользовательских значений, что maxExportBatchSize <= maxQueueSize. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:243`)

- ⚠️ **[Logs Sdk]** [MUST] LogRecordExporter - ForceFlush and Shutdown MUST be safe to be called concurrently  
  СброситьБуфер() тривиально безопасна (no-op), но Закрыть() устанавливает обычный Перем Закрыт (не АтомарноеБулево), без синхронизации. Конкурентные вызовы Закрыть() и Экспортировать() могут иметь гонку данных при чтении/записи флага Закрыт. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-49`)

- ❌ **[Metrics Api]** [MUST] If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that the name parameter is needed (synchronous instruments).  
  Имя является обязательным позиционным параметром в сигнатуре СоздатьСчетчик(Имя, ...), поэтому оно структурно обязательно. Однако данное MUST касается случая, когда это НЕ возможно - здесь это возможно, поэтому данное требование не применяется напрямую. Тем не менее, отдельной документации для пользователя нет. (-)

- ❌ **[Metrics Api]** [MUST] If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that the name parameter is needed (asynchronous instruments).  
  Имя является обязательным позиционным параметром в СоздатьНаблюдаемыйСчетчик(Имя, ...), так что структурно обязательно. Данное MUST относится к случаю, когда это невозможно. (-)

- ❌ **[Metrics Api]** [MUST] Callback functions MUST be documented as follows for the end user.  
  Нет формальной пользовательской документации, описывающей правила для callback-функций (реентрантность, время выполнения, дубликаты). (-)

- ⚠️ **[Metrics Api]** [MUST] The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps.  
  ВремяСейчас вычисляется один раз перед циклом ПреобразоватьЗаписиВТочки, так что все точки от одного callback получают одинаковый timestamp. Однако для мульти-callback (ВызватьМультиОбратныеВызовы в ОтелМетр) каждый инструмент вызывает Собрать() отдельно с разным временем - partial. (`src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180`)

- ⚠️ **[Metrics Sdk]** [MUST] The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept.  
  ОтелПредставление хранит ИсключенныеКлючиАтрибутов, но логика исключения не применяется в ОтелБазовыйСинхронныйИнструмент - ФильтроватьАтрибутыПоКлючам работает только с разрешёнными ключами (`src/Метрики/Классы/ОтелПредставление.os:56-58`)

- ⚠️ **[Metrics Sdk]** [MUST] The exclude-list: all other attributes MUST be kept. If an attribute key is both included and excluded, the SDK MAY fail fast.  
  Исключённые ключи хранятся в View, но не применяются при фильтрации - нет логики проверки конфликта включение/исключение (`src/Метрики/Классы/ОтелПредставление.os:56-58`)

- ⚠️ **[Metrics Sdk]** [MUST] Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow.  
  ОчиститьТочкиДанных сохраняет аккумуляторы при кумулятивной временности (строка 142), что означает все ранее наблюдённые attribute sets продолжают экспортироваться. Однако нет явного разделения между pre-overflow и post-overflow attribute sets - все новые attribute sets после overflow попадают в overflow aggregator без различия. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138`)

- ⚠️ **[Metrics Sdk]** [MUST] When a user passes multiple casings of the same name, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above.  
  Имя нормализуется через НРег() (строка 49) и кэшируется по нормализованному имени (строка 64), поэтому при повторном вызове с другим регистром возвращается тот же инструмент. Однако предупреждение выводится только при конфликте дескрипторов (вид, единица, описание), а не при конфликте регистра имени. Если параметры совпадают, предупреждение не выводится, хотя спека требует log an appropriate error при разном регистре. (`src/Метрики/Классы/ОтелМетр.os:49`)

- ⚠️ **[Metrics Sdk]** [MUST NOT] Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure).  
  Export вызывает Транспорт.Отправить() синхронно. Таймаут зависит от транспорта (HTTP таймаут), но в самом экспортере нет явного верхнего предела. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25`)

- ⚠️ **[Metrics Sdk]** [MUST] The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry.  
  SDK обрабатывает лимиты мощности (cardinality limits) через overflow-механизм при превышении ЛимитМощности. Однако нет явной обработки числовых пределов типов (integer overflow, float limits) - SDK полагается на поведение рантайма OneScript. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:92`)

- ⚠️ **[Metrics Sdk]** [MUST] If the SDK receives float/double values from Instruments, it MUST handle all the possible values (e.g. NaNs and Infinites for IEEE 754).  
  OneScript использует числовой тип на базе .NET, который поддерживает IEEE 754. Однако нет явной обработки NaN и Infinity в агрегаторах (ОтелАгрегаторСуммы, ОтелАгрегаторГистограммы и т.д.) - SDK полагается на поведение рантайма без явных проверок. (-)

- ⚠️ **[Metrics Sdk]** [MUST] MetricExporter - ForceFlush and Shutdown MUST be safe to be called concurrently.  
  ОтелЭкспортерМетрик.Закрыть() устанавливает Закрыт = Истина (простое присваивание Булево без атомарности). СброситьБуфер() - пустая процедура. Нет механизмов синхронизации (БлокировкаРесурса или АтомарноеБулево) для обеспечения потокобезопасности при конкурентных вызовах ForceFlush и Shutdown. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43`)

- ❌ **[Otlp Exporter]** [MUST] Each configuration option MUST be overridable by a signal specific option.  
  Нет поддержки сигнал-специфичных переменных вроде OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_LOGS_ENDPOINT и т.д. Используется только общий OTEL_EXPORTER_OTLP_ENDPOINT для всех сигналов. (-)

- ⚠️ **[Otlp Exporter]** [MUST] When using OTEL_EXPORTER_OTLP_ENDPOINT, exporters MUST construct per-signal URLs as described below (appending v1/traces, v1/metrics, v1/logs).  
  Пути v1/traces, v1/logs, v1/metrics задаются в каждом экспортере и передаются в транспорт. URL конструируется в транспорте путём конкатенации базового URL + путь. Однако per-signal endpoint переменные (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT и т.д.) не поддерживаются - нет логики 'URL is used as-is' для per-signal. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:35`)

- ⚠️ **[Otlp Exporter]** [MUST] For the per-signal variables (OTEL_EXPORTER_OTLP_<signal>_ENDPOINT), the URL MUST be used as-is without any modification. The only exception is that if a URL contains no path part, the root path / MUST be used.  
  Per-signal endpoint переменные (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT и т.д.) не поддерживаются, поэтому логика 'URL as-is' не реализована. (-)

- ⚠️ **[Otlp Exporter]** [MUST] Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal: Traces v1/traces, Metrics v1/metrics, Logs v1/logs.  
  Пути /v1/traces, /v1/logs, /v1/metrics корректно используются каждым экспортером. Однако URL конструируется не из OTEL_EXPORTER_OTLP_ENDPOINT базы - используется единый транспорт с БазовыйURL. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:35`)

- ⚠️ **[Otlp Exporter]** [MUST] For per-signal variables, URL MUST be used as-is without modification, except if URL contains no path part, the root path / MUST be used (see Example 2).  
  Per-signal endpoint переменные не поддерживаются. Нет OTEL_EXPORTER_OTLP_TRACES_ENDPOINT и подобных. (-)

- ⚠️ **[Propagators]** [MUST] A W3C Trace Context propagator MUST parse and validate the traceparent and tracestate HTTP headers as specified in W3C Trace Context Level 2  
  Код парсит и валидирует traceparent (version ff, all-zeros, длины), но в комментарии указан Level 1, а спецификация требует Level 2. Также не валидируется формат tracestate полностью. (`src/Пропагация/Классы/ОтелW3CПропагатор.os:81`)

- ⚠️ **[Env Vars]** [MUST] The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset.  
  Обработка пустых значений реализована частично: для ресурсных атрибутов (строка 105) и пропагаторов (строка 340) пустые значения проверяются явно (<> ""), но для многих других параметров (например, otel.service.name строка 114, числовые параметры строки 224-227) пустая строка не проверяется и может привести к ошибкам. Библиотека configor не фильтрует пустые значения на уровне провайдера ENV (oscript_modules/configor/.../ПровайдерПараметровENV.os:57-59). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105,340`)

- ⚠️ **[Env Vars]** [MUST] For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting.  
  Для пропагаторов неизвестное значение вызывает Сообщить() (строка 373) и пропускается, но значение не игнорируется полностью - другие пропагаторы из списка всё равно применяются. Для семплеров (строки 216-218) нераспознанное значение молча заменяется на ParentBased(AlwaysOn) без предупреждения. Для экспортеров нераспознанное значение не обрабатывается. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:373`)

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Baggage Api]** [SHOULD NOT] The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation.  
  Ключ Baggage доступен пользователям через экспортную функцию ОтелКонтекст.КлючBaggage(). Хотя удобные методы BaggageИзКонтекста/КонтекстСBaggage существуют, сам ключ не скрыт от пользователей API. (`src/Ядро/Модули/ОтелКонтекст.os:53`)

- ❌ **[Resource Sdk]** [SHOULD] Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate.  
  Детекторы заполняют семантические атрибуты (host.name, os.type, process.pid), но при этом не осознанно выставляют Schema URL - они просто не работают со Schema URL вообще. Для host/process детекторов, которые заполняют стандартные semconv атрибуты, SchemaURL должен быть задан. (-)

- ❌ **[Trace Api]** [SHOULD] Its name property SHOULD be set to an empty string when an invalid name is specified.  
  При передаче пустой строки в ПолучитьТрассировщик, имя передаётся как есть в ОбластьИнструментирования - но нет явной нормализации (null -> empty string). Однако OneScript не имеет null, Неопределено заменяется на пустую строку фактически не будет работать, т.к. параметр ИмяБиблиотеки обязательный. (-)

- ❌ **[Trace Api]** [SHOULD] A message reporting that the specified value is invalid SHOULD be logged when an invalid name is specified.  
  Нет логирования предупреждения при передаче пустого или невалидного имени в ПолучитьТрассировщик. (-)

- ⚠️ **[Trace Api]** [SHOULD NOT] Implementations SHOULD NOT provide access to a Span's attributes besides its SpanContext  
  ОтелСпан exposes Атрибуты() publicly via Экспорт, providing direct access to span attributes beyond SpanContext (`src/Трассировка/Классы/ОтелСпан.os:134`)

- ⚠️ **[Trace Api]** [SHOULD] This SHOULD be called SetStatus.  
  Method is named УстановитьСтатус (Russian equivalent of SetStatus), acceptable for language adaptation but not exact name. (`src/Трассировка/Классы/ОтелСпан.os:413`)

- ❌ **[Trace Api]** [SHOULD] The status code SHOULD remain unset, except for the following circumstances.  
  There is no enforcement or guidance in code that the status code should remain unset by default; the implementation allows free setting. (-)

- ❌ **[Trace Api]** [SHOULD] When the status is set to Error by Instrumentation Libraries, the Description SHOULD be documented and predictable.  
  No documentation of specific Description values for Error status in instrumentation libraries. (-)

- ❌ **[Trace Api]** [SHOULD] For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish their own conventions, including possible values of Description and what they mean.  
  No published conventions for Description values found in the codebase. (-)

- ❌ **[Trace Api]** [SHOULD NOT] Generally, Instrumentation Libraries SHOULD NOT set the status code to Ok, unless explicitly configured to do so.  
  No enforcement or documentation of this guideline found in instrumentation code. (-)

- ❌ **[Trace Api]** [SHOULD] Instrumentation Libraries SHOULD leave the status code as Unset unless there is an error.  
  No enforcement or documentation of this guideline found in instrumentation code. (-)

- ❌ **[Trace Api]** [SHOULD] Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generate.  
  No analysis tool behavior implemented in the SDK; this is about downstream tool behavior. (-)

- ⚠️ **[Trace Api]** [SHOULD] If a new type is required to be publicly exposed, it SHOULD be named NonRecordingSpan.  
  The type is named ОтелНоопСпан (NoopSpan) rather than NonRecordingSpan. Functionally equivalent but name differs from spec recommendation. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ❌ **[Trace Api]** [SHOULD] In order for SpanKind to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose.  
  This is a guideline for callers/instrumentation, not enforced in code. No documentation of this guideline found. (-)

- ❌ **[Trace Api]** [SHOULD NOT] A server-side span SHOULD NOT be used to describe outgoing remote procedure call.  
  This is a guideline for callers/instrumentation, not enforced in code. No documentation of this guideline found. (-)

- ⚠️ **[Trace Api]** [SHOULD] Implementations SHOULD record links containing SpanContext with empty TraceId or SpanId (all zeros) as long as either the attribute set or TraceState is non-empty.  
  AddLink does not check for empty TraceId/SpanId with non-empty attributes or TraceState - it records any link unconditionally, which partially meets the spirit but doesn't explicitly implement this conditional logic. (`src/Трассировка/Классы/ОтелСпан.os:361`)

- ⚠️ **[Trace Api]** [SHOULD] Link - Links are immutable and SHOULD be safe for concurrent use by default.  
  Links are stored as Соответствие (Map) objects, not as a dedicated immutable class. They are not documented as immutable or thread-safe. (`src/Трассировка/Классы/ОтелСпан.os:372`)

- ❌ **[Trace Api]** [SHOULD] If the Span in the parent Context is already non-recording, it SHOULD be returned directly without instantiating a new Span.  
  The tracer always creates a new ОтелНоопСпан even when the parent is already non-recording. It does not check if the parent is non-recording to return it directly. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out  
  Метод СброситьБуфер() является процедурой (void), не возвращает статус. Есть СброситьБуферАсинхронно() с Обещанием, но синхронный вариант не сообщает результат (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98-102`)

- ⚠️ **[Trace Sdk]** [SHOULD NOT] Span Exporter SHOULD NOT receive them [spans with IsRecording=true] unless the Sampled flag was also set.  
  Processors pass all completed spans to exporters unconditionally. There is no filtering by Sampled flag between processor and exporter - the SimpleSpanProcessor and BatchSpanProcessor forward all spans they receive to the exporter without checking the Sampled flag. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37`)

- ⚠️ **[Trace Sdk]** [SHOULD NOT] Span Exporters SHOULD NOT receive the ones [spans] that do not [have Sampled flag set].  
  No filtering exists between processor and exporter based on Sampled flag. RECORD_ONLY spans (IsRecording=true, Sampled=false) will reach the exporter. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37`)

- ⚠️ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values.  
  TraceIDs are generated using UUID (УникальныйИдентификатор) which provides randomness, but the implementation does not explicitly ensure W3C Trace Context Level 2 randomness requirements (56 random bits in the rightmost 7 bytes). UUID v4 provides 122 random bits, which covers the requirement in practice, but the SDK makes no explicit claim about W3C Level 2 compliance. (`src/Ядро/Модули/ОтелУтилиты.os:78-92`)

- ❌ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD set the Random flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements.  
  The SDK does not set the Random trace flag (bit 1 of trace-flags). Trace flags are either 0 (not sampled) or 1 (sampled). The W3C Trace Context Level 2 Random flag is not handled. (-)

- ❌ **[Trace Sdk]** [SHOULD] For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the rv sub-key of the OpenTelemetry TraceState.  
  The SDK samplers have no concept of explicit randomness (rv sub-key) and do not check TraceState for randomness values. The TraceIdRatioBased sampler always uses the TraceId hash directly without considering whether it meets randomness requirements. (-)

- ❌ **[Trace Sdk]** [SHOULD] Custom implementations of the IdGenerator SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace random flag will be set in the associated Trace contexts.  
  УстановитьГенераторИд() принимает произвольный объект с методами генерации, но нет механизма для IdGenerator объявить соответствие требованиям W3C Level 2 randomness (нет маркерного интерфейса, метода IsRandom и т.п.). Флаг random не управляется генератором. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] Shutdown SHOULD be called only once for each SpanProcessor instance.  
  Пакетный процессор устанавливает флаг Закрыт=Истина, но не проверяет его перед выполнением логики закрытия (нет идемпотентности). Простой процессор (ОтелПростойПроцессорСпанов) вообще не имеет защиты от повторного вызова. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:74`)

- ⚠️ **[Trace Sdk]** [SHOULD] After the call to Shutdown, subsequent calls to OnStart, OnEnd, or ForceFlush are not allowed. SDKs SHOULD ignore these calls gracefully, if possible.  
  Пакетный процессор проверяет флаг Закрыт в методе Обработать() (OnEnd), но не в СброситьБуфер() (ForceFlush). Простой процессор не проверяет флаг закрытия ни в одном методе. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43`)

- ❌ **[Trace Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод Закрыть() возвращает Void во всех реализациях процессоров. Нет возвращаемого значения или механизма уведомления о результате (успех, ошибка, таймаут). (-)

- ⚠️ **[Trace Sdk]** [SHOULD] Shutdown SHOULD complete or abort within some timeout.  
  Остановка фонового экспорта имеет таймаут (Обещание.Получить(ТаймаутЭкспортаМс)), но последующие операции - ЭкспортироватьВсеПакеты() и Экспортер.Закрыть() - не имеют таймаута и могут зависнуть. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192`)

- ⚠️ **[Trace Sdk]** [SHOULD] If any SpanProcessor has any associated exporter, it SHOULD try to call the exporter's Export with all spans for which this was not already done and then invoke ForceFlush on it.  
  Пакетный процессор вызывает Экспортер.Экспортировать() для всех буферизованных спанов, но не вызывает ForceFlush/СброситьБуфер() на самом экспортере после экспорта. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120`)

- ❌ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() возвращает Void. Нет возвращаемого значения или механизма уведомления о результате (успех, ошибка, таймаут). (-)

- ❌ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() не принимает параметр таймаута. ЭкспортироватьВсеПакеты() выполняется до полного опустошения буфера без ограничения по времени - может зависнуть при проблемах с экспортером. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер (ForceFlush) is a Процедура (void) in both exporter and processors. It does not return a success/failure/timeout status to the caller. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41`)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout. ForceFlush can be implemented as a blocking API or an asynchronous API which notifies the caller via a callback or an event.  
  ForceFlush on exporter (СброситьБуфер) is a no-op for the synchronous exporter. The batch processor's СброситьБуфер calls ЭкспортироватьВсеПакеты which iterates all remaining batches with no overall timeout parameter - individual export calls have transport-level timeout but there is no configurable ForceFlush timeout. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41`)

- ⚠️ **[Logs Api]** [SHOULD] The Enabled API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response.  
  Метод документирован комментарием, но не содержит явного указания о необходимости вызова перед каждым Emit для получения актуального результата. Документация говорит лишь что метод позволяет пропустить создание LogRecord. (`src/Логирование/Классы/ОтелЛоггер.os:28`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out  
  СброситьБуфер() объявлена как Процедура (void) без возвращаемого значения. Нет способа узнать, завершилась ли операция успешно, с ошибкой или по таймауту. Асинхронная версия СброситьБуферАсинхронно() на провайдере возвращает Обещание, но само Обещание оборачивает void-процедуру. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout  
  В пакетном процессоре СброситьБуфер() вызывает ЭкспортироватьВсеПакеты(), которая в цикле отправляет пакеты до опустошения буфера. Каждый отдельный вызов экспорта имеет таймаут через транспорт, но общий таймаут на всю операцию ForceFlush отсутствует - при большом буфере операция может занять продолжительное время. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68-70`)

- ❌ **[Logs Sdk]** [SHOULD] To avoid race conditions, implementations SHOULD recommended to users that a clone of logRecord be used for any concurrent processing, such as in a batching processor.  
  Нет документации или рекомендации пользователям о клонировании записей лога для конкурентной обработки. Пакетный процессор буферизует ссылки на объекты без клонирования. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Синхронный метод Закрыть() возвращает void и не сообщает об успехе/ошибке/таймауте. Только асинхронный ЗакрытьАсинхронно() возвращает Обещание, по которому можно определить результат. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:143`)

- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD complete or abort within some timeout.  
  Пакетный процессор имеет таймаут при остановке фонового экспорта (ОстановитьФоновыйЭкспорт с ТаймаутЭкспортаМс), но на уровне провайдера нет общего таймаута для всей операции Shutdown. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:190`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out  
  СброситьБуфер() объявлена как Процедура (void) без возвращаемого значения. Нет способа узнать, завершилась ли операция успешно, с ошибкой или по таймауту. Асинхронная версия СброситьБуферАсинхронно() на провайдере возвращает Обещание, но само Обещание оборачивает void-процедуру. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout  
  В пакетном процессоре СброситьБуфер() вызывает ЭкспортироватьВсеПакеты(), которая в цикле отправляет пакеты до опустошения буфера. Каждый отдельный вызов экспорта имеет таймаут через транспорт, но общий таймаут на всю операцию ForceFlush отсутствует - при большом буфере операция может занять продолжительное время. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68-70`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out  
  СброситьБуфер() объявлена как Процедура (void) без возвращаемого значения. Нет способа узнать, завершилась ли операция успешно, с ошибкой или по таймауту. Асинхронная версия СброситьБуферАсинхронно() на провайдере возвращает Обещание, но само Обещание оборачивает void-процедуру. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout  
  В пакетном процессоре СброситьБуфер() вызывает ЭкспортироватьВсеПакеты(), которая в цикле отправляет пакеты до опустошения буфера. Каждый отдельный вызов экспорта имеет таймаут через транспорт, но общий таймаут на всю операцию ForceFlush отсутствует - при большом буфере операция может занять продолжительное время. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68-70`)

- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD be called only once for each LogRecordExporter instance  
  Метод Закрыть() экспортера просто устанавливает Закрыт = Истина без защиты от повторного вызова. Провайдер (ОтелПровайдерЛогирования) использует АтомарноеБулево с СравнитьИУстановить для идемпотентного Shutdown, но сам экспортер не имеет такой защиты. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47-49`)

- ❌ **[Metrics Api]** [SHOULD] Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying.  
  OneScript не различает int/float на уровне типов; инструменты не используют тип числа как часть идентификации. Тип данных ('int'/'double') задаётся внутри агрегатора, но не влияет на идентификацию инструмента при сравнении дескрипторов в ПроверитьКонфликтДескриптора. (-)

- ❌ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (synchronous instruments).  
  Нет пользовательской документации, описывающей требования к синтаксису имени инструмента. (-)

- ❌ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (asynchronous instruments).  
  Нет пользовательской документации, описывающей требования к синтаксису имени инструмента для асинхронных инструментов. (-)

- ❌ **[Metrics Api]** [SHOULD] Callback functions SHOULD be reentrant safe. The SDK expects to evaluate callbacks for each MetricReader independently.  
  Нет документации для пользователя о том, что callback-функции должны быть реентрантно-безопасными. (-)

- ❌ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT take an indefinite amount of time.  
  Нет документации для пользователя о том, что callback-функции не должны занимать неопределённое время. (-)

- ❌ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT make duplicate observations (more than one Measurement with the same attributes) across all registered callbacks.  
  Нет документации для пользователя о том, что callback-функции не должны дублировать наблюдения. (-)

- ❌ **[Metrics Api]** [SHOULD] The Enabled API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response  
  Метод Включен() существует, но документация к нему не содержит рекомендации вызывать его перед каждым измерением. Комментарий в коде описывает поведение, но не адресует авторам инструментирования. (-)

- ⚠️ **[Metrics Api]** [SHOULD NOT] Counter Add API SHOULD NOT validate the increment value, that is left to implementations of the API  
  Код проверяет Значение < 0 и делает Возврат - это фактически валидация на уровне API. Спецификация говорит что API SHOULD NOT validate, это оставлено реализациям SDK. (`src/Метрики/Классы/ОтелСчетчик.os:22`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD provide some way to pass state to the callback  
  Callback принимается как Действие (lambda) - замыкание позволяет захватить состояние, но нет явного параметра state в API. Реализовано через lambda closure, что допустимо спецификацией, но неявно. (`src/Метрики/Классы/ОтелМетр.os:229`)

- ❌ **[Metrics Sdk]** [SHOULD] If there is no matching view, but the MetricReader defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used.  
  MetricReader (ОтелПериодическийЧитательМетрик) не определяет дефолтный cardinality limit на уровне reader. Лимит задаётся на уровне ОтелМетр, а не на уровне reader. (-)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Процедура СброситьБуфер() не возвращает значения - вызывающий не может узнать результат операции. СброситьБуферАсинхронно возвращает Обещание, но синхронный вариант - Процедура без возвращаемого значения. (-)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status.  
  СброситьБуфер() - это Процедура, не Функция. Не возвращает никакого статуса (ни ERROR, ни NO ERROR). (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  Синхронный СброситьБуфер() не имеет таймаута. СброситьБуферАсинхронно() возвращает Обещание, которое можно ожидать с таймаутом, но нет встроенного таймаута для самой операции flush. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:115`)

- ⚠️ **[Metrics Sdk]** [SHOULD] If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning.  
  Предупреждение при конфликте дескрипторов инструментов есть, но не при конфликте метрических идентичностей из-за наложения нескольких View (`src/Метрики/Классы/ОтелМетр.os:562-578`)

- ❌ **[Metrics Sdk]** [SHOULD] If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asynchronous instrument to use the Explicit bucket histogram aggregation) the implementation SHOULD emit a warning and proceed as if the View did not exist.  
  Нет проверки совместимости агрегации View с типом инструмента; нет логики отклонения семантически несовместимого View (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] Histogram Aggregations: Arithmetic sum of Measurement values in population. This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. UpDownCounter or ObservableGauge).  
  ОтелАгрегаторГистограммы всегда собирает sum (строка 51) без проверки типа инструмента; нет логики пропуска суммы для UpDownCounter/ObservableGauge (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different.  
  Дефолтные границы реализованы, но отсутствует значение 7500 по сравнению со спецификацией (0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000) (`src/Метрики/Классы/ОтелАгрегаторГистограммы.os:118-135`)

- ❌ **[Metrics Sdk]** [SHOULD NOT] Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the sum, min, and max fields, because these values do not map into a valid bucket.  
  Нет проверки на Inf/NaN в ОтелАгрегаторЭкспоненциальнойГистограммы.Записать() - значения записываются в sum/min/max без фильтрации (-)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks.  
  Нет механизма предотвращения использования асинхронных API вне зарегистрированных callback; внешние наблюдения принимаются всегда через ДобавитьВнешниеНаблюдения() (-)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback execution.  
  Callback-и вызываются синхронно в ВызватьCallbackИСобрать() без таймаута; нет механизма ограничения времени выполнения callback (-)

- ❌ **[Metrics Sdk]** [SHOULD] If there is no matching view, but the MetricReader defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used.  
  MetricReader (ОтелПериодическийЧитательМетрик) не определяет дефолтный cardinality limit на уровне reader. Лимит задаётся на уровне ОтелМетр, а не на уровне reader. (-)

- ❌ **[Metrics Sdk]** [SHOULD] Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality.  
  ОтелБазовыйНаблюдаемыйИнструмент не реализует cardinality limiting вообще. Нет ни лимита мощности, ни overflow-логики для наблюдаемых инструментов. Все записи из callback обрабатываются без ограничений. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] When a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted.  
  Предупреждение выводится при конфликте дескрипторов (строка 573), но нет проверки, был ли конфликт скорректирован представлением (View). Предупреждение всегда выводится при любом конфликте, независимо от наличия View. (`src/Метрики/Классы/ОтелМетр.os:573`)

- ⚠️ **[Metrics Sdk]** [SHOULD] The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible.  
  Предупреждение содержит информацию о конфликте (какие параметры различаются), но не содержит рекомендаций по разрешению конфликта (например, использовать View для переименования или установки описания). (`src/Метрики/Классы/ОтелМетр.os:573`)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves multiple description properties, setting the description through a configured View SHOULD avoid the warning.  
  Нет логики, которая проверяет наличие View с установленным описанием для подавления предупреждения при конфликте описаний. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning.  
  Предупреждение о конфликте не содержит рецепта использования View для переименования инструмента. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both Metric objects and emit a generic warning describing the duplicate instrument registration.  
  При дублировании возвращается ранее зарегистрированный инструмент (строка 54), а не создаётся отдельный Metric object. Данные агрегируются в один инструмент, а не экспортируются как два отдельных Metric объекта. (`src/Метрики/Классы/ОтелМетр.os:54`)

- ❌ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax.  
  Нет валидации имени инструмента в ОтелМетр. Имя принимается как есть без проверки соответствия синтаксису (regex pattern из спецификации). Нет ни регулярного выражения, ни проверки длины/символов. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name.  
  Поскольку валидация имени не реализована (предыдущее требование), ошибка о невалидном имени также не выводится. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] Exemplars are expected to abide by the AggregationTemporality of any metric point they are recorded with. Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point.  
  Exemplars are cleared on ОчиститьТочкиДанных (line 139), which provides temporal alignment for delta. However there is no explicit check that exemplar timestamps fall within the data point's time window. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138-147`)

- ❌ **[Metrics Sdk]** [SHOULD] The ExemplarReservoir SHOULD avoid allocations when sampling exemplars.  
  The reservoir creates new Соответствие (Map) objects on every Предложить call (line 113 СоздатьЭкземпляр), allocating new maps and arrays each time rather than reusing pre-allocated structures. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] This implementation SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled.  
  Реализация хранит последнее измерение (last-seen), а не использует равномерное взвешенное сэмплирование. Спецификация допускает это как альтернативу (MAY instead keep the last seen measurement), но основная рекомендация SHOULD - сэмплирование. (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50`)

- ⚠️ **[Metrics Sdk]** [SHOULD] Collect SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() (Collect) не возвращает статус успеха/ошибки/таймаута - это процедура без возвращаемого значения. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71`)

- ❌ **[Metrics Sdk]** [SHOULD] Collect SHOULD invoke Produce on registered MetricProducers.  
  MetricProducer как отдельная сущность не реализована. Сбор данных происходит напрямую из зарегистрированных метров, без вызова Produce на внешних MetricProducer. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] After the call to Shutdown, subsequent invocations to Collect are not allowed. SDKs SHOULD return some failure for these calls, if possible.  
  После Закрыть() метод ПериодическийСбор проверяет флаг Закрыт и прекращает цикл, но метод СброситьБуфер() (Collect) не проверяет флаг Закрыт и не возвращает ошибку при вызове после shutdown. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:59`)

- ⚠️ **[Metrics Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод Закрыть() - процедура без возвращаемого значения, не сообщает вызывающему о результате. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD collect metrics, call Export(batch) and ForceFlush() on the configured Push Metric Exporter.  
  СброситьБуфер() вызывает СобратьИЭкспортировать(), что собирает метрики и вызывает Export, но не вызывает ForceFlush() на экспортере. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() - процедура без возвращаемого значения, не сообщает о результате. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status.  
  Метод СброситьБуфер() не возвращает статус - является процедурой. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71`)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  Метод СброситьБуфер() не имеет механизма таймаута - выполняется синхронно без ограничения по времени. (-)

- ❌ **[Metrics Sdk]** [SHOULD] Metric Exporters SHOULD report an error condition for data output by the MetricReader with unsupported Aggregation or Aggregation Temporality.  
  Экспортер метрик не проверяет поддерживаемые типы агрегации или временности - принимает любые данные без валидации. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush of the exporter SHOULD be completed as soon as possible, preferably before returning from this method.  
  СброситьБуфер() реализован как пустая процедура (нет буферизации - синхронный экспорт), что формально корректно, но не сообщает результат. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() - процедура без возвращаемого значения. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43`)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed metrics.  
  Это рекомендация по использованию, не по реализации - но нет документации или проверок, ограничивающих вызов ForceFlush. (-)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  Метод СброситьБуфер() экспортера не имеет таймаута. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD NOT] Shutdown SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable).  
  Закрыть() просто устанавливает флаг Закрыт = Истина и не блокируется, но нет явного таймаута если бы была очистка. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49`)

- ❌ **[Metrics Sdk]** [SHOULD] MetricProducer implementations SHOULD accept configuration for the AggregationTemporality of produced metrics.  
  ОтелПрометеусЧитательМетрик не принимает конфигурацию AggregationTemporality. Prometheus reader работает только с cumulative temporality, нет параметра для настройки временной агрегации. (-)

- ⚠️ **[Otlp Exporter]** [SHOULD] Endpoint (OTLP/gRPC): The option SHOULD accept any form allowed by the underlying gRPC client implementation.  
  Принимает строку адреса и передаёт в OPI_GRPC, но формат зависит от реализации OPI_GRPC. (`src/Экспорт/Классы/ОтелGrpcТранспорт.os:146-170`)

- ❌ **[Otlp Exporter]** [SHOULD] If the gRPC client implementation does not support an endpoint with a scheme of http or https then the endpoint SHOULD be transformed to the most sensible format for that implementation.  
  Нет трансформации эндпоинта - адрес передаётся в OPI_GRPC как есть. (-)

- ⚠️ **[Otlp Exporter]** [SHOULD] SDKs SHOULD default endpoint variables to use http scheme unless they have good reasons to choose https scheme for the default.  
  Дефолт http://localhost:4317 для gRPC и http://localhost:4318 для HTTP - используется http. Реализовано корректно. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:153-158`)

- ❌ **[Otlp Exporter]** [SHOULD] The obsolete environment variables OTEL_EXPORTER_OTLP_SPAN_INSECURE and OTEL_EXPORTER_OTLP_METRIC_INSECURE SHOULD continue to be supported if they were already implemented.  
  Эти устаревшие переменные не реализованы, но это допустимо - они и не были реализованы ранее. (-)

- ⚠️ **[Otlp Exporter]** [SHOULD] The default protocol SHOULD be http/protobuf, unless there are strong reasons for SDKs to select grpc as the default.  
  Дефолт протокола - 'http/json', а не 'http/protobuf' как рекомендует спецификация. Код: Менеджер.Параметр("otel.exporter.otlp.protocol", "http/json"). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If they support only one, it SHOULD be http/protobuf.  
  HTTP-транспорт отправляет Content-Type: application/json, т.е. http/json, а не http/protobuf. Реализованы оба транспорта (HTTP и gRPC), но HTTP-транспорт использует JSON, а не protobuf. (`src/Экспорт/Классы/ОтелHttpТранспорт.os:171`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If no configuration is provided the default transport SHOULD be http/protobuf unless SDKs have good reasons to choose grpc as the default.  
  Дефолт - 'http/json', а не 'http/protobuf'. Код: Менеджер.Параметр("otel.exporter.otlp.protocol", "http/json"). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ❌ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter.  
  Нет установки заголовка User-Agent ни в HTTP-транспорте, ни в gRPC-транспорте. Заголовки включают только Content-Type и пользовательские заголовки. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The format of the User-Agent header SHOULD follow RFC 7231.  
  User-Agent заголовок не реализован. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The resulting User-Agent SHOULD include the exporter's default User-Agent string when a product identifier is added.  
  User-Agent заголовок не реализован. (-)

- ❌ **[Propagators]** [SHOULD] Platforms with pre-configured propagators SHOULD default to a composite Propagator containing the W3C Trace Context Propagator and the Baggage Propagator  
  Нет автоконфигурации пропагаторов по умолчанию - SDK не создаёт по умолчанию композитный пропагатор с W3C TraceContext + Baggage, пользователь должен явно сконфигурировать (-)

- ⚠️ **[Env Vars]** [SHOULD] Implementations that choose to allow configuration via environment variables SHOULD use the names and value parsing behavior specified in this document.  
  Большинство стандартных OTEL_* переменных поддержано через configor (OTEL_SERVICE_NAME, OTEL_RESOURCE_ATTRIBUTES, OTEL_TRACES_EXPORTER и т.д.), но вместо OTEL_SDK_DISABLED используется нестандартная OTEL_ENABLED с инвертированной логикой. OTEL_LOG_LEVEL и OTEL_ENTITIES не поддержаны. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:6-34`)

- ❌ **[Env Vars]** [SHOULD] If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied.  
  Функция Включено() (строка 562) просто сравнивает НРег(Значение) = "true" без логирования предупреждения для нераспознанных значений (не "true" и не "false"). (-)

- ⚠️ **[Env Vars]** [SHOULD] All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior.  
  Используется нестандартная переменная OTEL_ENABLED (по умолчанию true), а не OTEL_SDK_DISABLED (по умолчанию false). Имя OTEL_ENABLED нарушает принцип: false для неё означает отключение SDK, что не является "безопасным по умолчанию". (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562`)

- ❌ **[Env Vars]** [SHOULD] For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning.  
  Числовые параметры парсятся вызовом Число() без обработки ошибок (например, строки 224-227). Невалидное значение вызовет исключение OneScript, а не предупреждение с fallback на значение по умолчанию. (-)

- ❌ **[Env Vars]** [SHOULD] For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD gracefully ignore the setting, i.e., treat them as not set.  
  При невалидном числовом значении вызов Число() бросит исключение вместо того чтобы проигнорировать значение и использовать значение по умолчанию. Нет try/catch обработки для парсинга чисел. (-)

- ❌ **[Env Vars]** [SHOULD] For new implementations, the SHOULD requirements for numeric parsing should be treated as MUST requirements.  
  Проект opentelemetry версии 0.1.0 является новой реализацией, поэтому SHOULD-требования по парсингу числовых значений должны рассматриваться как MUST. Ни предупреждение, ни graceful ignore не реализованы. (-)

- ⚠️ **[Env Vars]** [SHOULD] Enum values SHOULD be interpreted in a case-insensitive manner.  
  Регистронезависимая обработка реализована только для пропагаторов (НРег на строке 344) и компрессии (строка 144). Для семплеров (строки 197-218) и экспортеров (строки 177-178, 255-256, 291-292) сравнение выполняется регистрозависимо (= "always_on", = "otlp", = "none"). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:344`)

## Детальный анализ по разделам (Stable)

### Context

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | A Context MUST be immutable | `src/Ядро/Модули/ОтелКонтекст.os:364` |  |
| 2 | MUST | ✅ found | its write operations MUST result in the creation of a new Context containing the original values and the specified values updated | `src/Ядро/Модули/ОтелКонтекст.os:127` |  |
| 3 | MUST | ✅ found | OpenTelemetry MUST provide its own Context implementation | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### Create a key

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#create-a-key)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The API MUST accept the following parameter: The key name. The key name exists for debugging purposes and does not uniquely identify the key. | `src/Ядро/Модули/ОтелКонтекст.os:35` |  |
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
| 13 | MUST | ⚠️ partial | The API MUST accept the following parameters: The Context. | `src/Ядро/Модули/ОтелКонтекст.os:203` | Нет метода Attach/Присоединить, принимающего объект Context (ФиксированноеСоответствие). Вместо этого УстановитьЗначение(Ключ, Значение) создаёт новый контекст внутри себя. Нельзя сделать текущим произвольный заранее собранный контекст. |
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
| 11 | MUST | ✅ found | If an implementation of this API does not operate directly on the Context, it MUST provide the following functionality to interact with a Context instance: Extract the Baggage from a Context instance; Insert the Baggage to a Context instance. | `src/Ядро/Модули/ОтелКонтекст.os:156` |  |
| 12 | SHOULD NOT | ⚠️ partial | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:53` | Ключ Baggage доступен пользователям через экспортную функцию ОтелКонтекст.КлючBaggage(). Хотя удобные методы BaggageИзКонтекста/КонтекстСBaggage существуют, сам ключ не скрыт от пользователей API. |
| 13 | SHOULD | ✅ found | If the language has support for implicitly propagated Context, the API SHOULD also provide the following functionality: Get the currently active Baggage from the implicit context; Set the currently active Baggage to the implicit context. | `src/Ядро/Классы/ОтелBaggage.os:16` |  |
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
| 17 | MUST | ✅ found | If a new name/value pair is added and its name is the same as an existing name, then the new pair MUST take precedence. The value is replaced with the added value (regardless of whether it is locally generated or received from a remote peer). | `src/Ядро/Классы/ОтелПостроительBaggage.os:23` |  |

### Resource Sdk

#### Resource SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The SDK MUST allow for creation of Resources and for associating them with telemetry. | `src/Ядро/Классы/ОтелРесурс.os:94` |  |
| 2 | MUST | ✅ found | When associated with a TracerProvider, all Spans produced by any Tracer from the provider MUST be associated with this Resource. | `src/Трассировка/Классы/ОтелСпан.os:33` |  |

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
| 9 | MUST | ⚠️ partial | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1` | Детекторы реализованы как отдельные классы (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора), но они включены в тот же пакет SDK (lib.config), а не в отдельные пакеты. |
| 10 | MUST | ✅ found | Resource detector packages MUST provide a method that returns a resource. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17` |  |
| 11 | MUST NOT | ✅ found | The failure to detect any resource information MUST NOT be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:19` |  |
| 12 | SHOULD | ✅ found | An error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:23` |  |
| 13 | MUST | ❌ not_found | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions. | - | Детекторы (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора) создают ресурс через Новый ОтелРесурс(Истина), что означает без умолчаний и без SchemaURL. Ни один детектор не устанавливает Schema URL. |
| 14 | SHOULD | ❌ not_found | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate. | - | Детекторы заполняют семантические атрибуты (host.name, os.type, process.pid), но при этом не осознанно выставляют Schema URL - они просто не работают со Schema URL вообще. Для host/process детекторов, которые заполняют стандартные semconv атрибуты, SchemaURL должен быть задан. |
| 15 | MUST | ❌ not_found | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources. | - | В ОтелРесурс.ЗаполнитьАтрибутыПоУмолчанию() (строка 108-118) детекторы просто мержатся без проверки Schema URL конфликтов. Метод Слить() в строках 41-44 обрабатывает конфликт SchemaURL, но при инициализации ресурса мерж атрибутов детекторов происходит напрямую, минуя Слить(). |

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
| 5 | SHOULD | ✅ found | This name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 6 | MUST | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 7 | SHOULD | ❌ not_found | Its name property SHOULD be set to an empty string when an invalid name is specified. | - | При передаче пустой строки в ПолучитьТрассировщик, имя передаётся как есть в ОбластьИнструментирования - но нет явной нормализации (null -> empty string). Однако OneScript не имеет null, Неопределено заменяется на пустую строку фактически не будет работать, т.к. параметр ИмяБиблиотеки обязательный. |
| 8 | SHOULD | ❌ not_found | A message reporting that the specified value is invalid SHOULD be logged when an invalid name is specified. | - | Нет логирования предупреждения при передаче пустого или невалидного имени в ПолучитьТрассировщик. |
| 9 | MUST NOT | ✅ found | Implementations MUST NOT require users to repeatedly obtain a Tracer again with the same identity to pick up configuration changes. | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API MUST provide the following functionality to interact with a Context instance: Extract the Span from a Context instance, Combine the Span with a Context instance creating a new Context instance. | `src/Ядро/Модули/ОтелКонтекст.os:141` |  |
| 11 | SHOULD NOT | ✅ found | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:362` |  |
| 12 | SHOULD | ✅ found | If the language has support for implicitly propagated Context, the API SHOULD also provide the following functionality: Get the currently active span from the implicit context; Set the currently active span into a new context and make that the implicit context. | `src/Ядро/Модули/ОтелКонтекст.os:90` |  |
| 13 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### SpanContext

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spancontext)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The API MUST implement methods to create a SpanContext. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |
| 15 | SHOULD | ✅ found | These methods SHOULD be the only way to create a SpanContext. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |
| 16 | MUST | ✅ found | This functionality MUST be fully implemented in the API. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:1` |  |
| 17 | SHOULD NOT | ✅ found | This functionality SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:194` |  |

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
| 28 | MUST | ✅ found | Tracing API MUST provide at least the following operations on TraceState: Get value for a given key, Add a new key/value pair, Update an existing value for a given key, Delete a key/value pair | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:44` |  |
| 29 | MUST | ✅ found | These operations MUST follow the rules described in the W3C Trace Context specification | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:227` |  |
| 30 | MUST | ✅ found | All mutating operations MUST return a new TraceState with the modifications applied | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:92` |  |
| 31 | MUST | ✅ found | TraceState MUST at all times be valid according to rules specified in W3C Trace Context specification | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:220` |  |
| 32 | MUST | ✅ found | Every mutating operations MUST validate input parameters | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 33 | MUST NOT | ✅ found | If invalid value is passed the operation MUST NOT return TraceState containing invalid data | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 34 | MUST | ✅ found | If invalid value is passed the operation MUST follow the general error handling guidelines | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:68` |  |

#### Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | SHOULD | ✅ found | The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable | `src/Трассировка/Классы/ОтелСпан.os:7` |  |
| 36 | SHOULD | ✅ found | Generality SHOULD be prioritized over human-readability | `src/Трассировка/Классы/ОтелСпан.os:7` |  |
| 37 | SHOULD | ✅ found | A Span's start time SHOULD be set to the current time on span creation | `src/Трассировка/Классы/ОтелСпан.os:609` |  |
| 38 | SHOULD | ✅ found | After the Span is created, it SHOULD be possible to change its name, set its Attributes, add Events, and set the Status | `src/Трассировка/Классы/ОтелСпан.os:247` |  |
| 39 | MUST NOT | ✅ found | These (name, Attributes, Events, Status) MUST NOT be changed after the Span's end time has been set | `src/Трассировка/Классы/ОтелСпан.os:248` |  |
| 40 | SHOULD NOT | ⚠️ partial | Implementations SHOULD NOT provide access to a Span's attributes besides its SpanContext | `src/Трассировка/Классы/ОтелСпан.os:134` | ОтелСпан exposes Атрибуты() publicly via Экспорт, providing direct access to span attributes beyond SpanContext |
| 41 | MUST NOT | ✅ found | Alternative implementations MUST NOT allow callers to create Spans directly | `src/Трассировка/Классы/ОтелТрассировщик.os:82` |  |
| 42 | MUST | ✅ found | All Spans MUST be created via a Tracer | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |

#### Span Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Span other than with a Tracer | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 44 | MUST NOT | ✅ found | Span creation MUST NOT set the newly created Span as the active Span in the current Context by default | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 45 | MUST | ✅ found | The API MUST accept the following parameters: The span name (required parameter) | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 46 | MUST NOT | ⚠️ partial | This API MUST NOT accept a Span or SpanContext as parent, only a full Context | `src/Трассировка/Классы/ОтелТрассировщик.os:133` | НачатьДочернийСпан accepts ОтелСпан or ОтелКонтекстСпана as parent (line 127-128), not a full Context object. The spec requires only a full Context as parent, not a Span or SpanContext directly |
| 47 | MUST | ✅ found | The semantic parent of the Span MUST be determined according to the rules described in Determining the Parent Span from a Context | `src/Трассировка/Классы/ОтелТрассировщик.os:57` |  |
| 48 | MUST | ✅ found | The API documentation MUST state that adding attributes at span creation is preferred to calling SetAttribute later, as samplers can only consider information already present during span creation | `src/Трассировка/Классы/ОтелПостроительСпана.os:66` |  |
| 49 | SHOULD | ✅ found | Start timestamp, default to current time. This argument SHOULD only be set when span creation time has already passed | `src/Трассировка/Классы/ОтелПостроительСпана.os:109` |  |
| 50 | MUST NOT | ✅ found | If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument | `src/Трассировка/Классы/ОтелПостроительСпана.os:109` |  |
| 51 | MUST | ✅ found | Implementations MUST provide an option to create a Span as a root span | `src/Трассировка/Классы/ОтелТрассировщик.os:106` |  |
| 52 | MUST | ✅ found | Implementations MUST generate a new TraceId for each root span created | `src/Трассировка/Классы/ОтелТрассировщик.os:107` |  |
| 53 | MUST | ✅ found | For a Span with a parent, the TraceId MUST be the same as the parent | `src/Трассировка/Классы/ОтелТрассировщик.os:140` |  |
| 54 | MUST | ✅ found | The child span MUST inherit all TraceState values of its parent by default | `src/Трассировка/Классы/ОтелТрассировщик.os:236` |  |
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
| 58 | MUST | ✅ found | The returned value MUST be the same for the entire Span lifetime | `src/Трассировка/Классы/ОтелСпан.os:9` |  |
| 59 | SHOULD | ✅ found | After a Span is ended, it SHOULD become non-recording and IsRecording SHOULD always return false | `src/Трассировка/Классы/ОтелСпан.os:234` |  |
| 60 | SHOULD | ✅ found | After a Span is ended, IsRecording SHOULD always return false | `src/Трассировка/Классы/ОтелСпан.os:235` |  |
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
| 71 | MUST | ✅ found | The Span interface MUST provide: An API to set the Status. | `src/Трассировка/Классы/ОтелСпан.os:413` |  |
| 72 | SHOULD | ⚠️ partial | This SHOULD be called SetStatus. | `src/Трассировка/Классы/ОтелСпан.os:413` | Method is named УстановитьСтатус (Russian equivalent of SetStatus), acceptable for language adaptation but not exact name. |
| 73 | MUST | ✅ found | Description MUST be IGNORED for StatusCode Ok & Unset values. | `src/Трассировка/Классы/ОтелСпан.os:429` |  |
| 74 | SHOULD | ❌ not_found | The status code SHOULD remain unset, except for the following circumstances. | - | There is no enforcement or guidance in code that the status code should remain unset by default; the implementation allows free setting. |
| 75 | SHOULD | ✅ found | An attempt to set value Unset SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:424` |  |
| 76 | SHOULD | ❌ not_found | When the status is set to Error by Instrumentation Libraries, the Description SHOULD be documented and predictable. | - | No documentation of specific Description values for Error status in instrumentation libraries. |
| 77 | SHOULD | ❌ not_found | For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish their own conventions, including possible values of Description and what they mean. | - | No published conventions for Description values found in the codebase. |
| 78 | SHOULD NOT | ❌ not_found | Generally, Instrumentation Libraries SHOULD NOT set the status code to Ok, unless explicitly configured to do so. | - | No enforcement or documentation of this guideline found in instrumentation code. |
| 79 | SHOULD | ❌ not_found | Instrumentation Libraries SHOULD leave the status code as Unset unless there is an error. | - | No enforcement or documentation of this guideline found in instrumentation code. |
| 80 | SHOULD | ✅ found | When span status is set to Ok it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 81 | SHOULD | ✅ found | Any further attempts to change Ok status SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 82 | SHOULD | ❌ not_found | Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generate. | - | No analysis tool behavior implemented in the SDK; this is about downstream tool behavior. |

#### UpdateName

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#updatename)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 83 | SHOULD | ✅ found | Implementations SHOULD ignore all subsequent calls to End and any other Span methods, i.e. the Span becomes non-recording by being ended. | `src/Трассировка/Классы/ОтелСпан.os:448` |  |
| 84 | MUST | ✅ found | All API implementations of such methods MUST internally call the End method and be documented to do so. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 85 | MUST NOT | ✅ found | End MUST NOT have any effects on child spans. Those may still be running and can be ended later. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 86 | MUST NOT | ✅ found | End MUST NOT inactivate the Span in any Context it is active in. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 87 | MUST | ✅ found | It MUST still be possible to use an ended span as parent via a Context it is contained in. | `src/Трассировка/Классы/ОтелСпан.os:398` |  |
| 88 | MUST | ✅ found | Also, any mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:398` |  |
| 89 | MUST | ✅ found | If omitted, this (end timestamp) MUST be treated equivalent to passing the current time. | `src/Трассировка/Классы/ОтелСпан.os:449` |  |
| 90 | MUST NOT | ✅ found | This operation itself MUST NOT perform blocking I/O on the calling thread. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |
| 91 | SHOULD | ✅ found | Any locking used needs be minimized and SHOULD be removed entirely if possible. | `src/Трассировка/Классы/ОтелСпан.os:447` |  |

#### Record Exception

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#record-exception)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 92 | SHOULD | ✅ found | To facilitate recording an exception languages SHOULD provide a RecordException method if the language uses exceptions. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 93 | MUST | ✅ found | The method MUST record an exception as an Event with the conventions outlined in the exceptions document. | `src/Трассировка/Классы/ОтелСпан.os:322` |  |
| 94 | SHOULD | ✅ found | The minimum required argument SHOULD be no more than only an exception object. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 95 | MUST | ✅ found | If RecordException is provided, the method MUST accept an optional parameter to provide any additional event attributes. | `src/Трассировка/Классы/ОтелСпан.os:317` |  |
| 96 | SHOULD | ✅ found | This SHOULD be done in the same way as for the AddEvent method (additional attributes parameter). | `src/Трассировка/Классы/ОтелСпан.os:340` |  |

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
| 99 | SHOULD NOT | ✅ found | If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |
| 100 | SHOULD | ⚠️ partial | If a new type is required to be publicly exposed, it SHOULD be named NonRecordingSpan. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | The type is named ОтелНоопСпан (NoopSpan) rather than NonRecordingSpan. Functionally equivalent but name differs from spec recommendation. |
| 101 | MUST | ✅ found | GetContext MUST return the wrapped SpanContext. | `src/Трассировка/Классы/ОтелНоопСпан.os:30` |  |
| 102 | MUST | ✅ found | IsRecording MUST return false to signal that events, attributes and other elements are not being recorded. | `src/Трассировка/Классы/ОтелНоопСпан.os:155` |  |
| 103 | MUST | ✅ found | The remaining functionality of Span MUST be defined as no-op operations. | `src/Трассировка/Классы/ОтелНоопСпан.os:167` |  |
| 104 | MUST | ✅ found | This functionality MUST be fully implemented in the API. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |
| 105 | SHOULD NOT | ✅ found | This functionality SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |

#### SpanKind

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 106 | SHOULD | ❌ not_found | In order for SpanKind to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose. | - | This is a guideline for callers/instrumentation, not enforced in code. No documentation of this guideline found. |
| 107 | SHOULD NOT | ❌ not_found | A server-side span SHOULD NOT be used to describe outgoing remote procedure call. | - | This is a guideline for callers/instrumentation, not enforced in code. No documentation of this guideline found. |
| 108 | MUST | ✅ found | A user MUST have the ability to record links to other SpanContexts. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 109 | MUST | ✅ found | The API MUST provide: An API to record a single Link where the Link properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:361` |  |
| 110 | SHOULD | ⚠️ partial | Implementations SHOULD record links containing SpanContext with empty TraceId or SpanId (all zeros) as long as either the attribute set or TraceState is non-empty. | `src/Трассировка/Классы/ОтелСпан.os:361` | AddLink does not check for empty TraceId/SpanId with non-empty attributes or TraceState - it records any link unconditionally, which partially meets the spirit but doesn't explicitly implement this conditional logic. |
| 111 | SHOULD | ✅ found | Span SHOULD preserve the order in which Links are set. | `src/Трассировка/Классы/ОтелСпан.os:613` |  |
| 112 | MUST | ✅ found | The API documentation MUST state that adding links at span creation is preferred to calling AddLink later, for contexts that are available during span creation, because head sampling decisions can only consider information present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os:82` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 113 | MUST | ✅ found | TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:6` |  |
| 114 | MUST | ✅ found | Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:3` |  |
| 115 | MUST | ✅ found | Span - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:3` |  |
| 116 | MUST | ✅ found | Event - Events are immutable and MUST be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСобытиеСпана.os:3` |  |
| 117 | SHOULD | ⚠️ partial | Link - Links are immutable and SHOULD be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:372` | Links are stored as Соответствие (Map) objects, not as a dedicated immutable class. They are not documented as immutable or thread-safe. |

#### Behavior of the API in the absence of an installed SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#behavior-of-the-api-in-the-absence-of-an-installed-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 118 | MUST | ✅ found | The API MUST return a non-recording Span with the SpanContext in the parent Context (whether explicitly given or implicit current). | `src/Трассировка/Классы/ОтелТрассировщик.os:71` |  |
| 119 | SHOULD | ❌ not_found | If the Span in the parent Context is already non-recording, it SHOULD be returned directly without instantiating a new Span. | - | The tracer always creates a new ОтелНоопСпан even when the parent is already non-recording. It does not check if the parent is non-recording to return it directly. |
| 120 | MUST | ✅ found | If the parent Context contains no Span, an empty non-recording Span MUST be returned instead (i.e., having a SpanContext with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags). | `src/Трассировка/Классы/ОтелНоопСпан.os:277` |  |

### Trace Sdk

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, Sampler, and TracerConfigurator) MUST be owned by the TracerProvider | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:9-28` |  |
| 2 | MUST | ✅ found | The updated configuration MUST also apply to all already returned Tracers (i.e. it MUST NOT matter whether a Tracer was obtained from the TracerProvider before or after the configuration change) | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |
| 3 | MUST NOT | ✅ found | It MUST NOT matter whether a Tracer was obtained from the TracerProvider before or after the configuration change | `src/Трассировка/Классы/ОтелТрассировщик.os:80-93` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98-102` | Метод СброситьБуфер() является процедурой (void), не возвращает статус. Есть СброситьБуферАсинхронно() с Обещанием, но синхронный вариант не сообщает результат |
| 5 | SHOULD | ✅ found | ForceFlush SHOULD complete or abort within some timeout | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:121-125` |  |
| 6 | MUST | ✅ found | ForceFlush MUST invoke ForceFlush on all registered SpanProcessors | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:99-101` |  |

#### Additional Span Interfaces

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#additional-span-interfaces)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | Readable span: A function receiving this as argument MUST be able to access all information that was added to the span, as listed in the API spec for Span | `src/Трассировка/Классы/ОтелСпан.os:71-226` |  |
| 8 | MUST | ✅ found | A function receiving this as argument MUST be able to access the InstrumentationScope and Resource information (implicitly) associated with the span | `src/Трассировка/Классы/ОтелСпан.os:161-172` |  |
| 9 | MUST | ⚠️ partial | For backwards compatibility it MUST also be able to access the InstrumentationLibrary [deprecated since 1.10.0] having the same name and version values as the InstrumentationScope | `src/Трассировка/Классы/ОтелСпан.os:170` | Нет отдельного класса/интерфейса InstrumentationLibrary. Есть только ОтелОбластьИнструментирования (InstrumentationScope), который содержит имя и версию, но устаревший InstrumentationLibrary не выделен как отдельная сущность для обратной совместимости |
| 10 | MUST | ✅ found | A function receiving this as argument MUST be able to reliably determine whether the Span has ended | `src/Трассировка/Классы/ОтелСпан.os:197-199` |  |
| 11 | MUST | ✅ found | Counts for attributes, events and links dropped due to collection limits MUST be available for exporters to report as described in the exporters specification | `src/Трассировка/Классы/ОтелСпан.os:206-226` |  |
| 12 | MUST | ✅ found | Implementations MAY choose not to expose the full parent Context but they MUST expose at least the full parent SpanContext | `src/Трассировка/Классы/ОтелСпан.os:89-91` |  |
| 13 | MUST | ✅ found | Read/write span: It MUST be possible for functions being called with this to somehow obtain the same Span instance and type that the span creation API returned (or will return) to the user | `src/Трассировка/Классы/ОтелСпан.os:639-641` |  |

#### Sampling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | Span Processor MUST receive only those spans which have this field [IsRecording] set to true. | `src/Трассировка/Классы/ОтелТрассировщик.os:71` |  |
| 15 | SHOULD NOT | ⚠️ partial | Span Exporter SHOULD NOT receive them [spans with IsRecording=true] unless the Sampled flag was also set. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37` | Processors pass all completed spans to exporters unconditionally. There is no filtering by Sampled flag between processor and exporter - the SimpleSpanProcessor and BatchSpanProcessor forward all spans they receive to the exporter without checking the Sampled flag. |
| 16 | MUST | ⚠️ partial | Span Exporters MUST receive those spans which have Sampled flag set to true. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37` | Exporters receive all spans passed by processors. Since the SDK drops DROP-decision spans entirely (returns NoopSpan) and creates real spans only for RECORD_ONLY and RECORD_AND_SAMPLE, both reach the exporter. The RECORD_AND_SAMPLE spans (Sampled=true) do reach the exporter, but so do RECORD_ONLY spans (Sampled=false) since there is no filtering. |
| 17 | SHOULD NOT | ⚠️ partial | Span Exporters SHOULD NOT receive the ones [spans] that do not [have Sampled flag set]. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37` | No filtering exists between processor and exporter based on Sampled flag. RECORD_ONLY spans (IsRecording=true, Sampled=false) will reach the exporter. |
| 18 | MUST NOT | ✅ found | The OpenTelemetry SDK MUST NOT allow the combination SampledFlag == true and IsRecording == false. | `src/Трассировка/Классы/ОтелТрассировщик.os:213-218` |  |

#### SDK Span creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sdk-span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | When asked to create a Span, the SDK MUST act as if doing the following in order: use valid parent trace ID or generate new, query ShouldSample, generate new span ID independently of sampling decision, create span depending on decision. | `src/Трассировка/Классы/ОтелТрассировщик.os:56-94` |  |

#### ShouldSample

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shouldsample)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ⚠️ partial | If the parent SpanContext contains a valid TraceId, they [TraceId of the Span to be created and parent TraceId] MUST always match. | `src/Трассировка/Классы/ОтелТрассировщик.os:61` | The code does reuse the parent's TraceId for child spans (line 61), so they match. However, the ShouldSample method signature (ОтелСэмплер.ДолженСэмплировать) does not receive the full set of required arguments per spec (Context with parent Span, TraceId, Name, SpanKind, initial Attributes, Links). It receives strategy, ratio, TraceId, parent-sampled, has-parent, root-strategy - different from spec. |
| 21 | MUST NOT | ✅ found | RECORD_ONLY - IsRecording will be true, but the Sampled flag MUST NOT be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:213-218` |  |
| 22 | MUST | ✅ found | RECORD_AND_SAMPLE - IsRecording will be true and the Sampled flag MUST be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:214-216` |  |
| 23 | SHOULD | ✅ found | Samplers SHOULD normally return the passed-in Tracestate if they do not intend to change it. | `src/Трассировка/Классы/ОтелРезультатСэмплирования.os:84-88` |  |
| 24 | SHOULD NOT | ✅ found | Callers SHOULD NOT cache the returned value [of GetDescription]. | `src/Трассировка/Модули/ОтелСэмплер.os:106` |  |

#### TraceID randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#traceid-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | SHOULD | ⚠️ partial | For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values. | `src/Ядро/Модули/ОтелУтилиты.os:78-92` | TraceIDs are generated using UUID (УникальныйИдентификатор) which provides randomness, but the implementation does not explicitly ensure W3C Trace Context Level 2 randomness requirements (56 random bits in the rightmost 7 bytes). UUID v4 provides 122 random bits, which covers the requirement in practice, but the SDK makes no explicit claim about W3C Level 2 compliance. |

#### Random trace flag

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#random-trace-flag)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | SHOULD | ❌ not_found | For root span contexts, the SDK SHOULD set the Random flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements. | - | The SDK does not set the Random trace flag (bit 1 of trace-flags). Trace flags are either 0 (not sampled) or 1 (sampled). The W3C Trace Context Level 2 Random flag is not handled. |

#### Explicit randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#explicit-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 27 | MUST NOT | ❌ not_found | SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value (the rv sub-key). | - | The SDK has no awareness of the rv sub-key in OpenTelemetry TraceState. There is no code that reads or writes the rv sub-key. Since the SDK never touches rv, it technically doesn't overwrite it, but there's also no explicit protection against overwriting it. |
| 28 | SHOULD | ❌ not_found | For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the rv sub-key of the OpenTelemetry TraceState. | - | The SDK samplers have no concept of explicit randomness (rv sub-key) and do not check TraceState for randomness values. The TraceIdRatioBased sampler always uses the TraceId hash directly without considering whether it meets randomness requirements. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | SHOULD | ❌ not_found | Custom implementations of the IdGenerator SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace random flag will be set in the associated Trace contexts. | - | УстановитьГенераторИд() принимает произвольный объект с методами генерации, но нет механизма для IdGenerator объявить соответствие требованиям W3C Level 2 randomness (нет маркерного интерфейса, метода IsRandom и т.п.). Флаг random не управляется генератором. |

#### Span Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | Span attributes MUST adhere to the common rules of attribute limits. | `src/Трассировка/Классы/ОтелСпан.os:266` |  |
| 31 | MUST | ✅ found | If the SDK implements the limits above it MUST provide a way to change these limits, via a configuration to the TracerProvider, by allowing users to configure individual limits. | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:74` |  |
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
| 38 | MUST | ✅ found | Name of the methods MUST be consistent with SpanContext, providing extension points for generating SpanId and TraceId. | `src/Ядро/Модули/ОтелУтилиты.os:78` |  |
| 39 | MUST NOT | ✅ found | Additional IdGenerator implementing vendor-specific protocols such as AWS X-Ray trace id generator MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | - |  |

#### Span processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 40 | MUST | ✅ found | SDK MUST allow to end each pipeline with individual exporter. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:85` |  |
| 41 | MUST | ✅ found | SDK MUST allow users to implement and configure custom processors. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:1` |  |
| 42 | MUST | ✅ found | The SpanProcessor interface MUST declare the following methods: OnStart, OnEnd, Shutdown, ForceFlush. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11` |  |
| 43 | SHOULD | ✅ found | The SpanProcessor interface SHOULD declare the following methods: OnEnding method. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:21` |  |
| 44 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object passed in OnStart. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11` |  |
| 45 | SHOULD | ✅ found | Updates to the span SHOULD be reflected in the span object reference kept from OnStart. | `src/Трассировка/Классы/ОтелСпан.os:578` |  |

#### OnEnd(Span)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onendspan)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | MUST | ✅ found | This method MUST be called synchronously within the Span.End() API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |

#### Shutdown()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | SHOULD | ⚠️ partial | Shutdown SHOULD be called only once for each SpanProcessor instance. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:74` | Пакетный процессор устанавливает флаг Закрыт=Истина, но не проверяет его перед выполнением логики закрытия (нет идемпотентности). Простой процессор (ОтелПростойПроцессорСпанов) вообще не имеет защиты от повторного вызова. |
| 48 | SHOULD | ⚠️ partial | After the call to Shutdown, subsequent calls to OnStart, OnEnd, or ForceFlush are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43` | Пакетный процессор проверяет флаг Закрыт в методе Обработать() (OnEnd), но не в СброситьБуфер() (ForceFlush). Простой процессор не проверяет флаг закрытия ни в одном методе. |
| 49 | SHOULD | ❌ not_found | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Метод Закрыть() возвращает Void во всех реализациях процессоров. Нет возвращаемого значения или механизма уведомления о результате (успех, ошибка, таймаут). |
| 50 | MUST | ✅ found | Shutdown MUST include the effects of ForceFlush. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:77` |  |
| 51 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:192` | Остановка фонового экспорта имеет таймаут (Обещание.Получить(ТаймаутЭкспортаМс)), но последующие операции - ЭкспортироватьВсеПакеты() и Экспортер.Закрыть() - не имеют таймаута и могут зависнуть. |

#### ForceFlush()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 52 | SHOULD | ✅ found | Any tasks associated with Spans for which the SpanProcessor had already received events prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 53 | SHOULD | ⚠️ partial | If any SpanProcessor has any associated exporter, it SHOULD try to call the exporter's Export with all spans for which this was not already done and then invoke ForceFlush on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120` | Пакетный процессор вызывает Экспортер.Экспортировать() для всех буферизованных спанов, но не вызывает ForceFlush/СброситьБуфер() на самом экспортере после экспорта. |
| 54 | MUST | ⚠️ partial | The built-in SpanProcessors MUST do so (call exporter's Export with all spans and then invoke ForceFlush on the exporter). | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:120` | Встроенные процессоры вызывают Export для всех оставшихся спанов, но не вызывают ForceFlush на экспортере. |
| 55 | MUST | ❌ not_found | If a timeout is specified, the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. It MAY skip or abort some or all Export or ForceFlush calls it has made to achieve this goal. | - | Метод СброситьБуфер() не принимает параметр таймаута и не реализует логику прерывания по таймауту. Нет возможности указать таймаут для ForceFlush. |
| 56 | SHOULD | ❌ not_found | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Метод СброситьБуфер() возвращает Void. Нет возвращаемого значения или механизма уведомления о результате (успех, ошибка, таймаут). |
| 57 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the SpanProcessor exports the completed spans. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 58 | SHOULD | ❌ not_found | ForceFlush SHOULD complete or abort within some timeout. | - | СброситьБуфер() не принимает параметр таймаута. ЭкспортироватьВсеПакеты() выполняется до полного опустошения буфера без ограничения по времени - может зависнуть при проблемах с экспортером. |

#### Built-in span processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#built-in-span-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:1, src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:1` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | MUST | ✅ found | The [Simple] processor MUST synchronize calls to Span Exporter's Export to make sure that they are not invoked concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:41` |  |
| 61 | MUST | ✅ found | The [Batching] processor MUST synchronize calls to Span Exporter's Export to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:144` |  |
| 62 | SHOULD | ✅ found | The [Batching] processor SHOULD export a batch when any of the following happens AND the previous export call has returned: scheduledDelayMillis timer, maxExportBatchSize reached, ForceFlush called. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:54` |  |
| 63 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:5` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 64 | MUST | ✅ found | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:13, src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:19, src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:24` |  |

#### `Export(batch)`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | MUST NOT | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:149, src/Экспорт/Классы/ОтелGrpcТранспорт.os:151` |  |
| 66 | MUST | ✅ found | There MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:149` |  |
| 67 | SHOULD NOT | ✅ found | The default SDK's Span Processors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the spans are being sent to. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:137` |  |

#### `ForceFlush()`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | This is a hint to ensure that the export of any Spans the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68` |  |
| 69 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` | СброситьБуфер (ForceFlush) is a Процедура (void) in both exporter and processors. It does not return a success/failure/timeout status to the caller. |
| 70 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed spans. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:98` |  |
| 71 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. ForceFlush can be implemented as a blocking API or an asynchronous API which notifies the caller via a callback or an event. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` | ForceFlush on exporter (СброситьБуфер) is a no-op for the synchronous exporter. The batch processor's СброситьБуфер calls ЭкспортироватьВсеПакеты which iterates all remaining batches with no overall timeout parameter - individual export calls have transport-level timeout but there is no configurable ForceFlush timeout. |

#### Examples

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#examples)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST | ✅ found | Tracer Provider - Tracer creation, ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:264` |  |
| 73 | MUST | ✅ found | Sampler - ShouldSample and GetDescription MUST be safe to be called concurrently. | `src/Трассировка/Модули/ОтелСэмплер.os:140` |  |
| 74 | MUST | ✅ found | Span processor - all methods MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:7, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:11` |  |
| 75 | MUST | ✅ found | Span Exporter - ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:41` |  |

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
| 3 | MUST | ✅ found | This API MUST accept the following instrumentation scope parameters: name (required), version (optional), schema_url (optional), attributes (optional). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 4 | MUST | ✅ found | This API MUST be structured to accept a variable number of attributes, including none. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The Logger MUST provide a function to: Emit a LogRecord. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 6 | SHOULD | ✅ found | The Logger SHOULD provide functions to: Report if Logger is Enabled. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 7 | MUST | ✅ found | The Emit API MUST accept the following parameters: Timestamp (optional), Observed Timestamp (optional), Context, Severity Number (optional), Severity Text (optional), Body (optional), Attributes (optional), Event Name (optional). | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 8 | SHOULD | ✅ found | When implicit Context is supported, then the Context parameter of Emit SHOULD be optional. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 9 | MUST | ✅ found | When implicit Context is supported and Context is unspecified in Emit, it MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:82` |  |
| 10 | SHOULD | ✅ found | When only explicit Context is supported, the Context parameter of Emit SHOULD be required. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 11 | SHOULD | ✅ found | A Logger SHOULD provide this Enabled API to help users avoid performing computationally expensive operations when generating a LogRecord. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 12 | SHOULD | ✅ found | The Enabled API SHOULD accept the following parameters: Context, Severity Number (optional), Event Name (optional). | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 13 | SHOULD | ✅ found | When implicit Context is supported, then the Context parameter of Enabled SHOULD be optional. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 14 | MUST | ✅ found | When implicit Context is supported and Context is unspecified in Enabled, it MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:150` |  |
| 15 | MUST | ✅ found | The Enabled API MUST return a language idiomatic boolean type. A returned value of true means the Logger is enabled, false means disabled. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 16 | SHOULD | ⚠️ partial | The Enabled API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response. | `src/Логирование/Классы/ОтелЛоггер.os:28` | Метод документирован комментарием, но не содержит явного указания о необходимости вызова перед каждым Emit для получения актуального результата. Документация говорит лишь что метод позволяет пропустить создание LogRecord. |

#### Optional and required parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#optional-and-required-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | For each optional parameter, the API MUST be structured to accept it. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 18 | MUST NOT | ✅ found | For each optional parameter, the API MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
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
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:1` |  |

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A LoggerProvider MUST provide a way to allow a Resource to be specified. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:205` |  |
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
| 5 | MUST | ✅ found | Configuration (i.e. LogRecordProcessors and LoggerConfigurator) MUST be owned by the LoggerProvider. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:12` |  |
| 6 | MUST | ✅ found | the updated configuration MUST also apply to all already returned Loggers | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:222` |  |
| 7 | MUST NOT | ✅ found | it MUST NOT matter whether a Logger was obtained from the LoggerProvider before or after the configuration change | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:157` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ✅ found | The export of any ReadableLogRecords the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68-70` |  |
| 9 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43` | СброситьБуфер() объявлена как Процедура (void) без возвращаемого значения. Нет способа узнать, завершилась ли операция успешно, с ошибкой или по таймауту. Асинхронная версия СброситьБуферАсинхронно() на провайдере возвращает Обещание, но само Обещание оборачивает void-процедуру. |
| 10 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the ReadableLogRecords | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43` |  |
| 11 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68-70` | В пакетном процессоре СброситьБуфер() вызывает ЭкспортироватьВсеПакеты(), которая в цикле отправляет пакеты до опустошения буфера. Каждый отдельный вызов экспорта имеет таймаут через транспорт, но общий таймаут на всю операцию ForceFlush отсутствует - при большом буфере операция может занять продолжительное время. |

#### ReadableLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readablelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | A function receiving this as an argument MUST be able to access all the information added to the LogRecord | `src/Логирование/Классы/ОтелЗаписьЛога.os:44-161` |  |
| 13 | MUST | ✅ found | It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) associated with the LogRecord | `src/Логирование/Классы/ОтелЗаписьЛога.os:130-143` |  |
| 14 | MUST | ✅ found | The trace context fields MUST be populated from the resolved Context (either the explicitly passed Context or the current Context) when emitted | `src/Логирование/Классы/ОтелЛоггер.os:81-91` |  |
| 15 | MUST | ✅ found | Counts for attributes due to collection limits MUST be available for exporters to report as described in the transformation to non-OTLP formats specification | `src/Логирование/Классы/ОтелЗаписьЛога.os:150-152` |  |

#### ReadWriteLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readwritelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | A function receiving ReadWriteLogRecord as an argument MUST additionally be able to modify the following information added to the LogRecord: Timestamp, ObservedTimestamp, SeverityText, SeverityNumber, Body, Attributes (addition, modification, removal), TraceId, SpanId, TraceFlags, EventName | `src/Логирование/Классы/ОтелЗаписьЛога.os:179-298` |  |

#### LogRecord Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecord-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | LogRecord attributes MUST adhere to the common rules of attribute limits | `src/Логирование/Классы/ОтелЗаписьЛога.os:235-247` |  |
| 18 | MUST | ✅ found | If the SDK implements attribute limits it MUST provide a way to change these limits, via a configuration to the LoggerProvider, by allowing users to configure individual limits | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:39-56` |  |
| 19 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called LogRecordLimits | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:1-79` |  |
| 20 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute was discarded due to such a limit | `src/Логирование/Классы/ОтелЗаписьЛога.os:384-389` |  |
| 21 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per LogRecord (i.e., not per discarded attribute) | `src/Логирование/Классы/ОтелЗаписьЛога.os:385-388` |  |

#### LogRecordProcessor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 22 | MUST | ✅ found | The SDK MUST allow each pipeline to end with an individual exporter. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:66` |  |
| 23 | MUST | ✅ found | The SDK MUST allow users to implement and configure custom processors and decorate built-in processors for advanced scenarios such as enriching with attributes. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:1` |  |

#### LogRecordProcessor operations#### OnEmit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor-operations-onemit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | SHOULD NOT | ✅ found | OnEmit is called when a LogRecord is emitted. This method is called synchronously on the thread that emitted the LogRecord, therefore it SHOULD NOT block or throw exceptions. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:18` |  |
| 25 | MUST | ✅ found | For a LogRecordProcessor registered directly on SDK LoggerProvider, the logRecord mutations MUST be visible in next registered processors. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:18` |  |
| 26 | SHOULD | ❌ not_found | To avoid race conditions, implementations SHOULD recommended to users that a clone of logRecord be used for any concurrent processing, such as in a batching processor. | - | Нет документации или рекомендации пользователям о клонировании записей лога для конкурентной обработки. Пакетный процессор буферизует ссылки на объекты без клонирования. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 27 | MUST NOT | ✅ found | Any modifications to parameters inside Enabled MUST NOT be propagated to the caller. Parameters are immutable or passed by value. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |

#### ShutDown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each LogRecordProcessor instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117` |  |
| 29 | SHOULD | ✅ found | After the call to Shutdown, subsequent calls to OnEmit are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Логирование/Классы/ОтелЛоггер.os:106` |  |
| 30 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:143` | Синхронный метод Закрыть() возвращает void и не сообщает об успехе/ошибке/таймауте. Только асинхронный ЗакрытьАсинхронно() возвращает Обещание, по которому можно определить результат. |
| 31 | MUST | ✅ found | Shutdown MUST include the effects of ForceFlush. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:74` |  |
| 32 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:190` | Пакетный процессор имеет таймаут при остановке фонового экспорта (ОстановитьФоновыйЭкспорт с ТаймаутЭкспортаМс), но на уровне провайдера нет общего таймаута для всей операции Shutdown. |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | SHOULD | ✅ found | The export of any ReadableLogRecords the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68-70` |  |
| 34 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43` | СброситьБуфер() объявлена как Процедура (void) без возвращаемого значения. Нет способа узнать, завершилась ли операция успешно, с ошибкой или по таймауту. Асинхронная версия СброситьБуферАсинхронно() на провайдере возвращает Обещание, но само Обещание оборачивает void-процедуру. |
| 35 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the ReadableLogRecords | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43` |  |
| 36 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68-70` | В пакетном процессоре СброситьБуфер() вызывает ЭкспортироватьВсеПакеты(), которая в цикле отправляет пакеты до опустошения буфера. Каждый отдельный вызов экспорта имеет таймаут через транспорт, но общий таймаут на всю операцию ForceFlush отсутствует - при большом буфере операция может занять продолжительное время. |

#### Built-in processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#built-in-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1` |  |
| 38 | SHOULD | ✅ found | Other common processing scenarios SHOULD be first considered for implementation out-of-process in OpenTelemetry Collector. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 39 | MUST | ✅ found | The Simple processor MUST synchronize calls to LogRecordExporter's Export to make sure that they are not invoked concurrently. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:22` |  |
| 40 | MUST | ✅ found | The Batching processor MUST synchronize calls to LogRecordExporter's Export to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:144` |  |
| 41 | MUST | ⚠️ partial | maxExportBatchSize - the maximum batch size of every export. It must be smaller or equal to maxQueueSize. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:243` | Значения по умолчанию соответствуют (МаксРазмерПакета=512 <= МаксРазмерБуфера=2048), но нет валидации при установке пользовательских значений, что maxExportBatchSize <= maxQueueSize. |

#### LogRecordExporter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 42 | MUST | ✅ found | A LogRecordExporter MUST support the following functions: Export, ForceFlush, Shutdown | `src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:13-25` |  |

#### Export

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#export)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST NOT | ✅ found | Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure) | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 44 | MUST | ✅ found | There MUST be a reasonable upper limit after which the call must time out with an error result (Failure) | `src/Экспорт/Классы/ОтелHttpТранспорт.os:148-150` |  |
| 45 | SHOULD NOT | ✅ found | The default SDK's LogRecordProcessors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the logs are being sent to | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:18-31` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | SHOULD | ✅ found | The export of any ReadableLogRecords the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68-70` |  |
| 47 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43` | СброситьБуфер() объявлена как Процедура (void) без возвращаемого значения. Нет способа узнать, завершилась ли операция успешно, с ошибкой или по таймауту. Асинхронная версия СброситьБуферАсинхронно() на провайдере возвращает Обещание, но само Обещание оборачивает void-процедуру. |
| 48 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the ReadableLogRecords | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-43` |  |
| 49 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:68-70` | В пакетном процессоре СброситьБуфер() вызывает ЭкспортироватьВсеПакеты(), которая в цикле отправляет пакеты до опустошения буфера. Каждый отдельный вызов экспорта имеет таймаут через транспорт, но общий таймаут на всю операцию ForceFlush отсутствует - при большом буфере операция может занять продолжительное время. |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 50 | SHOULD | ⚠️ partial | Shutdown SHOULD be called only once for each LogRecordExporter instance | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47-49` | Метод Закрыть() экспортера просто устанавливает Закрыт = Истина без защиты от повторного вызова. Провайдер (ОтелПровайдерЛогирования) использует АтомарноеБулево с СравнитьИУстановить для идемпотентного Shutdown, но сам экспортер не имеет такой защиты. |
| 51 | SHOULD | ✅ found | After the call to Shutdown subsequent calls to Export are not allowed and SHOULD return a Failure result | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:26-28` |  |
| 52 | SHOULD NOT | ✅ found | Shutdown SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable) | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47-49` |  |
| 53 | MUST | ✅ found | LoggerProvider - Logger creation, ForceFlush and Shutdown MUST be safe to be called concurrently | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117-123` |  |
| 54 | MUST | ✅ found | Logger - all methods MUST be safe to be called concurrently | `src/Логирование/Классы/ОтелЛоггер.os:76-112` |  |
| 55 | MUST | ⚠️ partial | LogRecordExporter - ForceFlush and Shutdown MUST be safe to be called concurrently | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:41-49` | СброситьБуфер() тривиально безопасна (no-op), но Закрыть() устанавливает обычный Перем Закрыт (не АтомарноеБулево), без синхронизации. Конкурентные вызовы Закрыть() и Экспортировать() могут иметь гонку данных при чтении/записи флага Закрыт. |

### Metrics Api

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD provide a way to set/register and access a global default MeterProvider. | `src/Ядро/Модули/ОтелГлобальный.os:31` |  |

#### MeterProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The MeterProvider MUST provide the following functions: Get a Meter. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 3 | MUST | ✅ found | This API MUST accept the following parameters: name (specifies the name of the instrumentation scope). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 4 | MUST NOT | ✅ found | Users can provide a version, but it is up to their discretion. Therefore, this API needs to be structured to accept a version, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:54` |  |
| 5 | MUST NOT | ✅ found | Users can provide a schema_url, but it is up to their discretion. Therefore, this API needs to be structured to accept a schema_url, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:56` |  |
| 6 | MUST | ✅ found | This API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:55` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ found | Meter SHOULD NOT be responsible for the configuration. This should be the responsibility of the MeterProvider instead. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:231` |  |

#### Meter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The Meter MUST provide functions to create new Instruments: Counter, Asynchronous Counter, Histogram, Gauge, Asynchronous Gauge, UpDownCounter, Asynchronous UpDownCounter. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Instrument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ❌ not_found | Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying. | - | OneScript не различает int/float на уровне типов; инструменты не используют тип числа как часть идентификации. Тип данных ('int'/'double') задаётся внутри агрегатора, но не влияет на идентификацию инструмента при сравнении дескрипторов в ПроверитьКонфликтДескриптора. |

#### Synchronous and Asynchronous instruments

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#synchronous-and-asynchronous-instruments)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API to construct synchronous instruments MUST accept the following parameters: a name of the Instrument. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 11 | SHOULD | ✅ found | The name needs to be provided by a user. If possible, the API SHOULD be structured so a user is obligated to provide this parameter (synchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 12 | MUST | ❌ not_found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that the name parameter is needed (synchronous instruments). | - | Имя является обязательным позиционным параметром в сигнатуре СоздатьСчетчик(Имя, ...), поэтому оно структурно обязательно. Однако данное MUST касается случая, когда это НЕ возможно - здесь это возможно, поэтому данное требование не применяется напрямую. Тем не менее, отдельной документации для пользователя нет. |
| 13 | SHOULD | ❌ not_found | The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (synchronous instruments). | - | Нет пользовательской документации, описывающей требования к синтаксису имени инструмента. |
| 14 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the name; that is left to implementations of the API, like the SDK (synchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 15 | MUST NOT | ✅ found | This API needs to be structured to accept a unit, but MUST NOT obligate a user to provide one (synchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 16 | MUST | ✅ found | The unit parameter needs to support the instrument unit rule. Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters (synchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 17 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the unit (synchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 18 | MUST NOT | ✅ found | This API needs to be structured to accept a description, but MUST NOT obligate a user to provide one (synchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 19 | MUST | ✅ found | The description needs to support the instrument description rule. Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters (synchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 20 | MUST NOT | ✅ found | This API needs to be structured to accept advisory parameters, but MUST NOT obligate the user to provide it (synchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 21 | SHOULD NOT | ✅ found | The API SHOULD NOT validate advisory parameters (synchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:642` |  |
| 22 | MUST | ✅ found | The API to construct asynchronous instruments MUST accept the following parameters: a name of the Instrument. | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 23 | SHOULD | ✅ found | The name needs to be provided by a user. If possible, the API SHOULD be structured so a user is obligated to provide this parameter (asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 24 | MUST | ❌ not_found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that the name parameter is needed (asynchronous instruments). | - | Имя является обязательным позиционным параметром в СоздатьНаблюдаемыйСчетчик(Имя, ...), так что структурно обязательно. Данное MUST относится к случаю, когда это невозможно. |
| 25 | SHOULD | ❌ not_found | The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (asynchronous instruments). | - | Нет пользовательской документации, описывающей требования к синтаксису имени инструмента для асинхронных инструментов. |
| 26 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the name, that is left to implementations of the API (asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 27 | MUST NOT | ✅ found | This API needs to be structured to accept a unit, but MUST NOT obligate a user to provide one (asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 28 | MUST | ✅ found | The unit parameter needs to support the instrument unit rule. Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters (asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 29 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the unit (asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 30 | MUST NOT | ✅ found | This API needs to be structured to accept a description, but MUST NOT obligate a user to provide one (asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 31 | MUST | ✅ found | The description needs to support the instrument description rule. Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters (asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 32 | MUST NOT | ✅ found | This API needs to be structured to accept advisory parameters, but MUST NOT obligate the user to provide it (asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 33 | SHOULD NOT | ✅ found | The API SHOULD NOT validate advisory parameters (asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:642` |  |
| 34 | MUST | ✅ found | This API MUST be structured to accept a variable number of callback functions, including none (asynchronous instruments). | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 35 | MUST | ✅ found | The API MUST support creation of asynchronous instruments by passing zero or more callback functions to be permanently registered to the newly created instrument. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147` |  |
| 36 | SHOULD | ✅ found | The API SHOULD support registration of callback functions associated with asynchronous instruments after they are created. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:58` |  |
| 37 | MUST | ✅ found | Where the API supports registration of callback functions after asynchronous instrumentation creation, the user MUST be able to undo registration of the specific callback after its registration by some means. | `src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os:14` |  |
| 38 | MUST | ✅ found | Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160` |  |
| 39 | MUST | ❌ not_found | Callback functions MUST be documented as follows for the end user. | - | Нет формальной пользовательской документации, описывающей правила для callback-функций (реентрантность, время выполнения, дубликаты). |
| 40 | SHOULD | ❌ not_found | Callback functions SHOULD be reentrant safe. The SDK expects to evaluate callbacks for each MetricReader independently. | - | Нет документации для пользователя о том, что callback-функции должны быть реентрантно-безопасными. |
| 41 | SHOULD NOT | ❌ not_found | Callback functions SHOULD NOT take an indefinite amount of time. | - | Нет документации для пользователя о том, что callback-функции не должны занимать неопределённое время. |
| 42 | SHOULD NOT | ❌ not_found | Callback functions SHOULD NOT make duplicate observations (more than one Measurement with the same attributes) across all registered callbacks. | - | Нет документации для пользователя о том, что callback-функции не должны дублировать наблюдения. |
| 43 | MUST | ✅ found | Callbacks registered at the time of instrument creation MUST apply to the single instruments which is under construction. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:154` |  |
| 44 | MUST | ✅ found | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the instrument associated with each observed Measurement value. | `src/Метрики/Классы/ОтелМетр.os:438` |  |
| 45 | MUST | ✅ found | Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of asynchronous instruments from the same Meter instance. | `src/Метрики/Классы/ОтелМетр.os:428` |  |
| 46 | MUST | ⚠️ partial | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` | ВремяСейчас вычисляется один раз перед циклом ПреобразоватьЗаписиВТочки, так что все точки от одного callback получают одинаковый timestamp. Однако для мульти-callback (ВызватьМультиОбратныеВызовы в ОтелМетр) каждый инструмент вызывает Собрать() отдельно с разным временем - partial. |
| 47 | SHOULD | ✅ found | The API SHOULD provide some way to pass state to the callback. | `src/Метрики/Классы/ОтелМетр.os:229` |  |

#### General operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 48 | SHOULD | ✅ found | All synchronous instruments SHOULD provide functions to: Report if instrument is Enabled | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 49 | SHOULD | ✅ found | Synchronous instruments SHOULD provide this Enabled API to help users avoid performing computationally expensive operations when recording measurements | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 50 | MUST | ✅ found | The Enabled API MUST be structured in a way for parameters to be added | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 51 | MUST | ✅ found | This Enabled API MUST return a language idiomatic boolean type. A returned value of true means the instrument is enabled, false means disabled | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 52 | SHOULD | ❌ not_found | The Enabled API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response | - | Метод Включен() существует, но документация к нему не содержит рекомендации вызывать его перед каждым измерением. Комментарий в коде описывает поведение, но не адресует авторам инструментирования. |

#### Counter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 53 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Counter other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 54 | SHOULD NOT | ✅ found | Counter Add API SHOULD NOT return a value | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 55 | MUST | ✅ found | Counter Add API MUST accept a numeric increment value parameter | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 56 | SHOULD | ✅ found | If possible, Counter Add API SHOULD be structured so a user is obligated to provide the increment value parameter | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 57 | MUST | ✅ found | If it is not possible to structurally enforce obligation to provide increment value, Counter Add API MUST be documented in a way to communicate to users that this parameter is needed | `src/Метрики/Классы/ОтелСчетчик.os:13` |  |
| 58 | SHOULD | ✅ found | The increment value is expected to be non-negative. Counter Add API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative | `src/Метрики/Классы/ОтелСчетчик.os:14` |  |
| 59 | SHOULD NOT | ⚠️ partial | Counter Add API SHOULD NOT validate the increment value, that is left to implementations of the API | `src/Метрики/Классы/ОтелСчетчик.os:22` | Код проверяет Значение < 0 и делает Возврат - это фактически валидация на уровне API. Спецификация говорит что API SHOULD NOT validate, это оставлено реализациям SDK. |
| 60 | MUST | ✅ found | Counter Add API MUST be structured to accept a variable number of attributes, including none | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 61 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 62 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Counter other than with a Meter | `src/Метрики/Классы/ОтелМетр.os:229` |  |
| 63 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` |  |
| 64 | MUST | ✅ found | Observations from a single callback MUST be reported with identical timestamps | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180` |  |
| 65 | SHOULD | ⚠️ partial | The API SHOULD provide some way to pass state to the callback | `src/Метрики/Классы/ОтелМетр.os:229` | Callback принимается как Действие (lambda) - замыкание позволяет захватить состояние, но нет явного параметра state в API. Реализовано через lambda closure, что допустимо спецификацией, но неявно. |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: a callback function and a list of Instruments used in the callback function | `src/Метрики/Классы/ОтелМетр.os:428` |  |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: a callback function and a list of Instruments used in the callback function | `src/Метрики/Классы/ОтелМетр.os:428` |  |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: a callback function and a list of Instruments used in the callback function | `src/Метрики/Классы/ОтелМетр.os:428` |  |

#### Note the two associated instruments are passed to the callback.

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-the-two-associated-instruments-are-passed-to-the-callback)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | SHOULD | ✅ found | All the metrics components SHOULD allow new APIs to be added to existing components without introducing breaking changes | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:1` |  |
| 70 | SHOULD | ✅ found | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introducing breaking changes, if possible | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | MUST | ✅ found | MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default | `src/Метрики/Классы/ОтелПровайдерМетрик.os:241` |  |
| 72 | MUST | ✅ found | Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default | `src/Метрики/Классы/ОтелМетр.os:493` |  |
| 73 | MUST | ✅ found | Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:17` |  |

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
| 2 | MUST | ✅ found | A MeterProvider MUST provide a way to allow a Resource to be specified. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:231` |  |
| 3 | SHOULD | ✅ found | If a Resource is specified, it SHOULD be associated with all the metrics produced by any Meter from the MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:67` |  |

#### MeterProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent MeterProviders. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:80` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | SHOULD | ✅ found | A view with criteria matching the instrument an aggregation is created for has an aggregation_cardinality_limit value defined for the stream, that value SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:92` |  |
| 6 | SHOULD | ❌ not_found | If there is no matching view, but the MetricReader defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | - | MetricReader (ОтелПериодическийЧитательМетрик) не определяет дефолтный cardinality limit на уровне reader. Лимит задаётся на уровне ОтелМетр, а не на уровне reader. |
| 7 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` |  |
| 8 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:325` |  |
| 9 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:92` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | ForceFlush MUST invoke ForceFlush on all registered MetricReader instances that implement ForceFlush. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` |  |
| 11 | SHOULD | ❌ not_found | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Процедура СброситьБуфер() не возвращает значения - вызывающий не может узнать результат операции. СброситьБуферАсинхронно возвращает Обещание, но синхронный вариант - Процедура без возвращаемого значения. |
| 12 | SHOULD | ❌ not_found | ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status. | - | СброситьБуфер() - это Процедура, не Функция. Не возвращает никакого статуса (ни ERROR, ни NO ERROR). |
| 13 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` | Синхронный СброситьБуфер() не имеет таймаута. СброситьБуферАсинхронно() возвращает Обещание, которое можно ожидать с таймаутом, но нет встроенного таймаута для самой операции flush. |

#### View

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The SDK MUST provide functionality for a user to create Views for a MeterProvider. | `src/Метрики/Классы/ОтелПредставление.os:156` |  |
| 15 | MUST | ✅ found | This functionality MUST accept as inputs the Instrument selection criteria and the resulting stream configuration. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 16 | MUST | ✅ found | The SDK MUST provide the means to register Views with a MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:176` |  |

#### Instrument selection criteria

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-selection-criteria)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | SHOULD | ✅ found | Criteria SHOULD be treated as additive. This means an Instrument has to match all the provided criteria for the View to be applied. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37-61` |  |
| 18 | MUST | ✅ found | The SDK MUST accept the following criteria: name, type, unit, meter_name, meter_version, meter_schema_url. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:4-14` |  |
| 19 | MUST | ✅ found | If the SDK does not support wildcards in general, it MUST still recognize the special single asterisk (*) character as matching all Instruments. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37` |  |
| 20 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 21 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a type, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 22 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a unit, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:160` |  |
| 23 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a meter_name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:160` |  |
| 24 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a meter_version, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:161` |  |
| 25 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a meter_schema_url, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:161` |  |
| 26 | MUST NOT | ✅ found | The instrument selection criteria can be structured to accept additional criteria the SDK accepts, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159-161` |  |

#### Stream configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#stream-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 27 | MUST | ✅ found | The SDK MUST accept the following stream configuration parameters: name, description, attribute_keys, aggregation, exemplar_reservoir, aggregation_cardinality_limit. | `src/Метрики/Классы/ОтелПредставление.os:4-18` |  |
| 28 | SHOULD | ✅ found | name: The metric stream name that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:29-31` |  |
| 29 | SHOULD | ✅ found | In order to avoid conflicts, if a name is provided the View SHOULD have an instrument selector that selects at most one instrument. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37` |  |
| 30 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept a name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:157` |  |
| 31 | MUST | ✅ found | If the user does not provide a name value, name from the Instrument the View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:188-212` |  |
| 32 | SHOULD | ✅ found | description: The metric stream description that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:38-40` |  |
| 33 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept a description, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:158` |  |
| 34 | MUST | ✅ found | If the user does not provide a description value, the description from the Instrument a View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:189-215` |  |
| 35 | MUST | ✅ found | attribute_keys: This is, at a minimum, an allow-list of attribute keys for measurements captured in the metric stream. The allow-list contains attribute keys that identify the attributes that MUST be kept. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:291-299` |  |
| 36 | MUST | ✅ found | attribute_keys: all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:291-299` |  |
| 37 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept attribute_keys, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелПредставление.os:159` |  |
| 38 | SHOULD | ✅ found | If the user does not provide any value, the SDK SHOULD use the Attributes advisory parameter configured on the instrument instead. | `src/Метрики/Классы/ОтелМетр.os:524-528` |  |
| 39 | MUST | ✅ found | If the Attributes advisory parameter is absent, all attributes MUST be kept. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:84-86` |  |
| 40 | SHOULD | ✅ found | Additionally, implementations SHOULD support configuring an exclude-list of attribute keys. | `src/Метрики/Классы/ОтелПредставление.os:8-10` |  |
| 41 | MUST | ⚠️ partial | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелПредставление.os:56-58` | ОтелПредставление хранит ИсключенныеКлючиАтрибутов, но логика исключения не применяется в ОтелБазовыйСинхронныйИнструмент - ФильтроватьАтрибутыПоКлючам работает только с разрешёнными ключами |
| 42 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept an aggregation, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:161` |  |
| 43 | MUST | ✅ found | If the user does not provide an aggregation value, the MeterProvider MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance. | `src/Метрики/Классы/ОтелМетр.os:58-59` |  |
| 44 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept an exemplar_reservoir, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:163` |  |
| 45 | MUST | ✅ found | If the user does not provide an exemplar_reservoir value, the MeterProvider MUST apply a default exemplar reservoir. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |
| 46 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept an aggregation_cardinality_limit, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:164` |  |
| 47 | MUST | ✅ found | If the user does not provide an aggregation_cardinality_limit value, the MeterProvider MUST apply the default aggregation cardinality limit the MetricReader is configured with. | `src/Метрики/Классы/ОтелМетр.os:500` |  |
| 48 | MUST | ⚠️ partial | The exclude-list: all other attributes MUST be kept. If an attribute key is both included and excluded, the SDK MAY fail fast. | `src/Метрики/Классы/ОтелПредставление.os:56-58` | Исключённые ключи хранятся в View, но не применяются при фильтрации - нет логики проверки конфликта включение/исключение |

#### Measurement processing

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#measurement-processing)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | SHOULD | ✅ found | The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument: determine the MeterProvider, apply default Aggregation if no View, or match Views. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:173-220` |  |
| 50 | MUST | ✅ found | Instrument advisory parameters, if any, MUST be honored. | `src/Метрики/Классы/ОтелМетр.os:515-537` |  |
| 51 | SHOULD | ⚠️ partial | If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning. | `src/Метрики/Классы/ОтелМетр.os:562-578` | Предупреждение при конфликте дескрипторов инструментов есть, но не при конфликте метрических идентичностей из-за наложения нескольких View |
| 52 | SHOULD | ❌ not_found | If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asynchronous instrument to use the Explicit bucket histogram aggregation) the implementation SHOULD emit a warning and proceed as if the View did not exist. | - | Нет проверки совместимости агрегации View с типом инструмента; нет логики отклонения семантически несовместимого View |
| 53 | MUST | ✅ found | If both a View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:524-528` |  |
| 54 | SHOULD | ✅ found | If the Instrument could not match with any of the registered Views, the SDK SHOULD enable the instrument using the default aggregation and temporality. | `src/Метрики/Классы/ОтелМетр.os:58-59` |  |

#### conflicting metric identities)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#conflicting-metric-identities)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | MUST | ✅ found | The SDK MUST provide the following Aggregation to support the Metric Points in the Metrics Data Model: Drop, Default, Sum, Last Value, Explicit Bucket Histogram. | `src/Метрики/Модули/ОтелАгрегация.os:15-65` |  |
| 56 | SHOULD | ✅ found | The SDK SHOULD provide the following Aggregation: Base2 Exponential Bucket Histogram. | `src/Метрики/Модули/ОтелАгрегация.os:76-81` |  |

#### Sum Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#sum-aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 57 | SHOULD NOT | ❌ not_found | Histogram Aggregations: Arithmetic sum of Measurement values in population. This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. UpDownCounter or ObservableGauge). | - | ОтелАгрегаторГистограммы всегда собирает sum (строка 51) без проверки типа инструмента; нет логики пропуска суммы для UpDownCounter/ObservableGauge |
| 58 | SHOULD | ⚠️ partial | SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different. | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:118-135` | Дефолтные границы реализованы, но отсутствует значение 7500 по сравнению со спецификацией (0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000) |
| 59 | MUST | ✅ found | Implementations are REQUIRED to accept the entire normal range of IEEE floating point values (i.e., all values except for +Inf, -Inf and NaN values) for Base2 Exponential Bucket Histogram. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:63-78` |  |
| 60 | SHOULD NOT | ❌ not_found | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the sum, min, and max fields, because these values do not map into a valid bucket. | - | Нет проверки на Inf/NaN в ОтелАгрегаторЭкспоненциальнойГистограммы.Записать() - значения записываются в sum/min/max без фильтрации |
| 61 | MUST | ✅ found | The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic scale parameter will not exceed. The maximum scale is defined by the MaxScale configuration parameter. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:302-304` |  |
| 62 | SHOULD | ✅ found | When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:41` |  |

#### Observations inside asynchronous callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#observations-inside-asynchronous-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 63 | MUST | ✅ found | Callback functions MUST be invoked for the specific MetricReader performing collection, such that observations made or produced by executing callbacks only apply to the intended MetricReader during collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:140-147` |  |
| 64 | SHOULD | ❌ not_found | The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks. | - | Нет механизма предотвращения использования асинхронных API вне зарегистрированных callback; внешние наблюдения принимаются всегда через ДобавитьВнешниеНаблюдения() |
| 65 | SHOULD | ❌ not_found | The implementation SHOULD use a timeout to prevent indefinite callback execution. | - | Callback-и вызываются синхронно в ВызватьCallbackИСобрать() без таймаута; нет механизма ограничения времени выполнения callback |
| 66 | MUST | ✅ found | The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160-177` |  |
| 67 | SHOULD NOT | ✅ found | The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:112-114` |  |

#### Cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | SDKs SHOULD support being configured with a cardinality limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:163-164` |  |
| 69 | SHOULD | ✅ found | Cardinality limit enforcement SHOULD occur after attribute filtering, if any. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:84-92` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 70 | SHOULD | ✅ found | A view with criteria matching the instrument an aggregation is created for has an aggregation_cardinality_limit value defined for the stream, that value SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:92` |  |
| 71 | SHOULD | ❌ not_found | If there is no matching view, but the MetricReader defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | - | MetricReader (ОтелПериодическийЧитательМетрик) не определяет дефолтный cardinality limit на уровне reader. Лимит задаётся на уровне ОтелМетр, а не на уровне reader. |
| 72 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` |  |
| 73 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:325` |  |
| 74 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:92` |  |

#### Synchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#synchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | MUST | ⚠️ partial | Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138` | ОчиститьТочкиДанных сохраняет аккумуляторы при кумулятивной временности (строка 142), что означает все ранее наблюдённые attribute sets продолжают экспортироваться. Однако нет явного разделения между pre-overflow и post-overflow attribute sets - все новые attribute sets после overflow попадают в overflow aggregator без различия. |
| 76 | MUST | ✅ found | Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in exactly one Aggregator, which is either an Aggregator associated with the correct attribute set or an aggregator associated with the overflow attribute set. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:88` |  |
| 77 | MUST NOT | ✅ found | Measurements MUST NOT be double-counted or dropped during an overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:78` |  |

#### Asynchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#asynchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | SHOULD | ❌ not_found | Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality. | - | ОтелБазовыйНаблюдаемыйИнструмент не реализует cardinality limiting вообще. Нет ни лимита мощности, ни overflow-логики для наблюдаемых инструментов. Все записи из callback обрабатываются без ограничений. |

#### Duplicate instrument registration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#duplicate-instrument-registration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 79 | MUST | ✅ found | The Meter MUST return a functional instrument that can be expected to export data even if this will cause semantic error in the data model. | `src/Метрики/Классы/ОтелМетр.os:54` |  |
| 80 | SHOULD | ⚠️ partial | When a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted. | `src/Метрики/Классы/ОтелМетр.os:573` | Предупреждение выводится при конфликте дескрипторов (строка 573), но нет проверки, был ли конфликт скорректирован представлением (View). Предупреждение всегда выводится при любом конфликте, независимо от наличия View. |
| 81 | SHOULD | ⚠️ partial | The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible. | `src/Метрики/Классы/ОтелМетр.os:573` | Предупреждение содержит информацию о конфликте (какие параметры различаются), но не содержит рекомендаций по разрешению конфликта (например, использовать View для переименования или установки описания). |
| 82 | SHOULD | ❌ not_found | If the potential conflict involves multiple description properties, setting the description through a configured View SHOULD avoid the warning. | - | Нет логики, которая проверяет наличие View с установленным описанием для подавления предупреждения при конфликте описаний. |
| 83 | SHOULD | ❌ not_found | If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning. | - | Предупреждение о конфликте не содержит рецепта использования View для переименования инструмента. |
| 84 | SHOULD | ⚠️ partial | Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both Metric objects and emit a generic warning describing the duplicate instrument registration. | `src/Метрики/Классы/ОтелМетр.os:54` | При дублировании возвращается ранее зарегистрированный инструмент (строка 54), а не создаётся отдельный Metric object. Данные агрегируются в один инструмент, а не экспортируются как два отдельных Metric объекта. |
| 85 | MUST | ✅ found | The SDK MUST aggregate data from identical Instruments together in its export pipeline. | `src/Метрики/Классы/ОтелМетр.os:54` |  |

#### Name conflict

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#name-conflict)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 86 | MUST | ⚠️ partial | When a user passes multiple casings of the same name, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above. | `src/Метрики/Классы/ОтелМетр.os:49` | Имя нормализуется через НРег() (строка 49) и кэшируется по нормализованному имени (строка 64), поэтому при повторном вызове с другим регистром возвращается тот же инструмент. Однако предупреждение выводится только при конфликте дескрипторов (вид, единица, описание), а не при конфликте регистра имени. Если параметры совпадают, предупреждение не выводится, хотя спека требует log an appropriate error при разном регистре. |

#### Instrument name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 87 | SHOULD | ❌ not_found | When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax. | - | Нет валидации имени инструмента в ОтелМетр. Имя принимается как есть без проверки соответствия синтаксису (regex pattern из спецификации). Нет ни регулярного выражения, ни проверки длины/символов. |
| 88 | SHOULD | ❌ not_found | If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name. | - | Поскольку валидация имени не реализована (предыдущее требование), ошибка о невалидном имени также не выводится. |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 90 | MUST | ✅ found | If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit string. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 91 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument description. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 92 | MUST | ✅ found | If a description is not provided or the description is null, the Meter MUST treat it the same as an empty description string. | `src/Метрики/Классы/ОтелМетр.os:48` |  |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 93 | SHOULD | ✅ found | When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:642` |  |
| 94 | SHOULD | ✅ found | If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided. | `src/Метрики/Классы/ОтелМетр.os:648` |  |
| 95 | MUST | ✅ found | If multiple identical Instruments are created with different advisory parameters, the Meter MUST return an instrument using the first-seen advisory parameters and log an appropriate error as described in duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:51-54` |  |
| 96 | MUST | ✅ found | If both a View and advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:515-537` |  |

#### Instrument advisory parameter: `ExplicitBucketBoundaries`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameter-explicitbucketboundaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | MUST | ✅ found | If no View matches, or if a matching View selects the default aggregation, the ExplicitBucketBoundaries advisory parameter MUST be used. | `src/Метрики/Классы/ОтелМетр.os:539-551` |  |

#### Exemplar

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | MUST | ✅ found | A Metric SDK MUST provide a mechanism to sample Exemplars from measurements via the ExemplarFilter and ExemplarReservoir hooks. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:333-354` |  |
| 99 | SHOULD | ✅ found | Exemplar sampling SHOULD be turned on by default. | `src/Метрики/Классы/ОтелМетр.os:496` |  |
| 100 | MUST NOT | ✅ found | If Exemplar sampling is off, the SDK MUST NOT have overhead related to exemplar sampling. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:335-337` |  |
| 101 | MUST | ✅ found | A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation. For example, Exemplar sampling of histograms should be able to leverage bucket boundaries. | `src/Метрики/Классы/ОтелМетр.os:99-100` |  |
| 102 | SHOULD | ✅ found | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: ExemplarFilter and ExemplarReservoir. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70-73` |  |
| 103 | MUST | ✅ found | The ExemplarFilter configuration MUST allow users to select between one of the built-in ExemplarFilters. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70-73` |  |
| 104 | SHOULD | ✅ found | The ExemplarFilter SHOULD be a configuration parameter of a MeterProvider for an SDK. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70-73` |  |
| 105 | SHOULD | ✅ found | The default value SHOULD be TraceBased. | `src/Метрики/Классы/ОтелМетр.os:496` |  |
| 106 | SHOULD | ✅ found | The filter configuration SHOULD follow the environment variable specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:109-125` |  |
| 107 | MUST | ✅ found | An OpenTelemetry SDK MUST support the following filters: AlwaysOn, AlwaysOff, TraceBased. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14-35` |  |

#### ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 108 | MUST | ✅ found | The ExemplarReservoir interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39-61` |  |
| 109 | MUST | ✅ found | A new ExemplarReservoir MUST be created for every known timeseries data point, as determined by aggregation and view configuration. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |
| 110 | SHOULD | ✅ found | The 'offer' method SHOULD accept measurements, including: the value of the measurement, the complete set of Attributes, the Context (Baggage and active Span), and a timestamp. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39-45` |  |
| 111 | SHOULD | ✅ found | The 'offer' method SHOULD have the ability to pull associated trace and span information without needing to record full context. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:112-120` |  |
| 112 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the Attributes associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the 'offer' method. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39-45` |  |
| 113 | MUST | ✅ found | The 'collect' method MUST return accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:55-61` |  |
| 114 | SHOULD | ⚠️ partial | Exemplars are expected to abide by the AggregationTemporality of any metric point they are recorded with. Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138-147` | Exemplars are cleared on ОчиститьТочкиДанных (line 139), which provides temporal alignment for delta. However there is no explicit check that exemplar timestamps fall within the data point's time window. |
| 115 | MUST | ✅ found | Exemplars MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:130-153` |  |
| 116 | SHOULD | ❌ not_found | The ExemplarReservoir SHOULD avoid allocations when sampling exemplars. | - | The reservoir creates new Соответствие (Map) objects on every Предложить call (line 113 СоздатьЭкземпляр), allocating new maps and arrays each time rather than reusing pre-allocated structures. |
| 117 | MUST | ✅ found | The 'offer' method MAY accept a filtered subset of Attributes which diverge from the timeseries the reservoir is associated with. This MUST be clearly documented in the API. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:33-37` |  |

#### Exemplar defaults

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar-defaults)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 118 | MUST | ✅ found | The SDK MUST include two types of built-in exemplar reservoirs: SimpleFixedSizeExemplarReservoir and AlignedHistogramBucketExemplarReservoir. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1, src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:1` |  |
| 119 | SHOULD | ✅ found | Explicit bucket histogram aggregation with more than 1 bucket SHOULD use AlignedHistogramBucketExemplarReservoir. | `src/Метрики/Классы/ОтелМетр.os:99-100` |  |
| 120 | SHOULD | ✅ found | Base2 Exponential Histogram Aggregation SHOULD use a SimpleFixedSizeExemplarReservoir with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty (e.g. min(20, max_buckets)). | `src/Метрики/Классы/ОтелМетр.os:137-139` |  |
| 121 | SHOULD | ✅ found | All other aggregations SHOULD use SimpleFixedSizeExemplarReservoir. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265` |  |

#### SimpleFixedSizeExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#simplefixedsizeexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 122 | MUST | ✅ found | This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the reservoir has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:80` |  |
| 123 | SHOULD | ✅ found | Any stateful portion of sampling computation SHOULD be reset every collection cycle. For the above example, that would mean that the num_measurements_seen count is reset every time the reservoir is collected. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:65` |  |
| 124 | SHOULD | ✅ found | Otherwise, a default size of 1 SHOULD be used if no size configuration is provided. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:165` |  |

#### AlignedHistogramBucketExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#alignedhistogrambucketexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 125 | MUST | ✅ found | This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:158` |  |
| 126 | MUST | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50` |  |
| 127 | SHOULD | ⚠️ partial | This implementation SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50` | Реализация хранит последнее измерение (last-seen), а не использует равномерное взвешенное сэмплирование. Спецификация допускает это как альтернативу (MAY instead keep the last seen measurement), но основная рекомендация SHOULD - сэмплирование. |
| 128 | SHOULD | ✅ found | This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:158` |  |

#### Custom ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#custom-exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 129 | MUST | ✅ found | The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation. | `src/Метрики/Классы/ОтелПредставление.os:128` |  |
| 130 | MUST | ✅ found | This extension MUST be configurable on a metric View. | `src/Метрики/Классы/ОтелПредставление.os:151` |  |
| 131 | MUST | ✅ found | Individual reservoirs MUST still be instantiated per metric-timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:80` |  |

#### MetricReader operations#### Collect

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader-operations-collect)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 132 | SHOULD | ⚠️ partial | Collect SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` | Метод СброситьБуфер() (Collect) не возвращает статус успеха/ошибки/таймаута - это процедура без возвращаемого значения. |
| 133 | SHOULD | ❌ not_found | Collect SHOULD invoke Produce on registered MetricProducers. | - | MetricProducer как отдельная сущность не реализована. Сбор данных происходит напрямую из зарегистрированных метров, без вызова Produce на внешних MetricProducer. |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 134 | MUST | ✅ found | Shutdown MUST be called only once for each MetricReader instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:89` |  |
| 135 | SHOULD | ⚠️ partial | After the call to Shutdown, subsequent invocations to Collect are not allowed. SDKs SHOULD return some failure for these calls, if possible. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:59` | После Закрыть() метод ПериодическийСбор проверяет флаг Закрыт и прекращает цикл, но метод СброситьБуфер() (Collect) не проверяет флаг Закрыт и не возвращает ошибку при вызове после shutdown. |
| 136 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88` | Метод Закрыть() - процедура без возвращаемого значения, не сообщает вызывающему о результате. |
| 137 | SHOULD | ✅ found | Shutdown SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` |  |

#### Periodic exporting MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 138 | MUST | ✅ found | The reader MUST synchronize calls to MetricExporter's Export to make sure that they are not invoked concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:124` |  |
| 139 | SHOULD | ⚠️ partial | ForceFlush SHOULD collect metrics, call Export(batch) and ForceFlush() on the configured Push Metric Exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` | СброситьБуфер() вызывает СобратьИЭкспортировать(), что собирает метрики и вызывает Export, но не вызывает ForceFlush() на экспортере. |
| 140 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` | СброситьБуфер() - процедура без возвращаемого значения, не сообщает о результате. |
| 141 | SHOULD | ⚠️ partial | ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:71` | Метод СброситьБуфер() не возвращает статус - является процедурой. |
| 142 | SHOULD | ❌ not_found | ForceFlush SHOULD complete or abort within some timeout. | - | Метод СброситьБуфер() не имеет механизма таймаута - выполняется синхронно без ограничения по времени. |

#### MetricExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 143 | MUST | ✅ found | MetricExporter defines the interface that protocol-specific exporters MUST implement so that they can be plugged into OpenTelemetry SDK and support sending of telemetry data. | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1` |  |
| 144 | SHOULD | ❌ not_found | Metric Exporters SHOULD report an error condition for data output by the MetricReader with unsupported Aggregation or Aggregation Temporality. | - | Экспортер метрик не проверяет поддерживаемые типы агрегации или временности - принимает любые данные без валидации. |
| 145 | MUST | ✅ found | A Push Metric Exporter MUST support the following functions: Export(batch), ForceFlush, Shutdown. | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:13` |  |
| 146 | MUST | ✅ found | The SDK MUST provide a way for the exporter to get the Meter information (e.g. name, version, etc.) associated with each Metric Point. | `src/Метрики/Классы/ОтелДанныеМетрики.os:42` |  |
| 147 | MUST NOT | ⚠️ partial | Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25` | Export вызывает Транспорт.Отправить() синхронно. Таймаут зависит от транспорта (HTTP таймаут), но в самом экспортере нет явного верхнего предела. |
| 148 | SHOULD NOT | ✅ found | The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the metrics are being sent to. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:25` |  |
| 149 | SHOULD | ⚠️ partial | ForceFlush of the exporter SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` | СброситьБуфер() реализован как пустая процедура (нет буферизации - синхронный экспорт), что формально корректно, но не сообщает результат. |
| 150 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` | СброситьБуфер() - процедура без возвращаемого значения. |
| 151 | SHOULD | ❌ not_found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed metrics. | - | Это рекомендация по использованию, не по реализации - но нет документации или проверок, ограничивающих вызов ForceFlush. |
| 152 | SHOULD | ❌ not_found | ForceFlush SHOULD complete or abort within some timeout. | - | Метод СброситьБуфер() экспортера не имеет таймаута. |
| 153 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each MetricExporter instance. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` |  |
| 154 | SHOULD | ✅ found | After the call to Shutdown subsequent calls to Export are not allowed and should return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:26` |  |
| 155 | SHOULD NOT | ⚠️ partial | Shutdown SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` | Закрыть() просто устанавливает флаг Закрыт = Истина и не блокируется, но нет явного таймаута если бы была очистка. |

#### Pull Metric Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#pull-metric-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 156 | MUST | ✅ found | MetricProducer defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:71` |  |
| 157 | SHOULD | ❌ not_found | MetricProducer implementations SHOULD accept configuration for the AggregationTemporality of produced metrics. | - | ОтелПрометеусЧитательМетрик не принимает конфигурацию AggregationTemporality. Prometheus reader работает только с cumulative temporality, нет параметра для настройки временной агрегации. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 158 | MUST | ✅ found | A MetricFilter MUST support the following functions (TestMetric, TestAttributes). | `src/Метрики/Классы/ОтелФильтрМетрик.os:29` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 159 | MUST | ✅ found | A MetricFilter MUST support the following functions (TestMetric, TestAttributes). | `src/Метрики/Классы/ОтелФильтрМетрик.os:29` |  |

#### TestMetric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#testmetric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 160 | MUST | ✅ found | The SDK MUST provide configuration according to the SDK environment variables specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:110` |  |

#### Numerical limits handling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#numerical-limits-handling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 161 | MUST | ⚠️ partial | The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:92` | SDK обрабатывает лимиты мощности (cardinality limits) через overflow-механизм при превышении ЛимитМощности. Однако нет явной обработки числовых пределов типов (integer overflow, float limits) - SDK полагается на поведение рантайма OneScript. |
| 162 | MUST | ⚠️ partial | If the SDK receives float/double values from Instruments, it MUST handle all the possible values (e.g. NaNs and Infinites for IEEE 754). | - | OneScript использует числовой тип на базе .NET, который поддерживает IEEE 754. Однако нет явной обработки NaN и Infinity в агрегаторах (ОтелАгрегаторСуммы, ОтелАгрегаторГистограммы и т.д.) - SDK полагается на поведение рантайма без явных проверок. |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 163 | SHOULD | ✅ found | All the metrics components SHOULD allow new methods to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:231` |  |
| 164 | SHOULD | ✅ found | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to existing methods without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:231` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 165 | MUST | ✅ found | MeterProvider - Meter creation, ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:241` |  |
| 166 | MUST | ✅ found | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:167` |  |
| 167 | MUST | ✅ found | MetricReader - Collect, ForceFlush (for periodic exporting MetricReader) and Shutdown MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:283` |  |
| 168 | MUST | ⚠️ partial | MetricExporter - ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` | ОтелЭкспортерМетрик.Закрыть() устанавливает Закрыт = Истина (простое присваивание Булево без атомарности). СброситьБуфер() - пустая процедура. Нет механизмов синхронизации (БлокировкаРесурса или АтомарноеБулево) для обеспечения потокобезопасности при конкурентных вызовах ForceFlush и Shutdown. |

### Otlp Exporter

#### Configuration Options

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#configuration-options)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The following configuration options MUST be available to configure the OTLP exporter. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130` |  |
| 2 | MUST | ❌ not_found | Each configuration option MUST be overridable by a signal specific option. | - | Нет поддержки сигнал-специфичных переменных вроде OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_LOGS_ENDPOINT и т.д. Используется только общий OTEL_EXPORTER_OTLP_ENDPOINT для всех сигналов. |
| 3 | MUST | ✅ found | The implementation MUST honor the following URL components: scheme (http or https), host, port, path. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:99-103` |  |
| 4 | MUST | ⚠️ partial | When using OTEL_EXPORTER_OTLP_ENDPOINT, exporters MUST construct per-signal URLs as described below (appending v1/traces, v1/metrics, v1/logs). | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:35` | Пути v1/traces, v1/logs, v1/metrics задаются в каждом экспортере и передаются в транспорт. URL конструируется в транспорте путём конкатенации базового URL + путь. Однако per-signal endpoint переменные (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT и т.д.) не поддерживаются - нет логики 'URL is used as-is' для per-signal. |
| 5 | SHOULD | ⚠️ partial | Endpoint (OTLP/gRPC): The option SHOULD accept any form allowed by the underlying gRPC client implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:146-170` | Принимает строку адреса и передаёт в OPI_GRPC, но формат зависит от реализации OPI_GRPC. |
| 6 | MUST | ✅ found | Endpoint (OTLP/gRPC): the option MUST accept a URL with a scheme of either http or https. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:146` |  |
| 7 | SHOULD | ❌ not_found | If the gRPC client implementation does not support an endpoint with a scheme of http or https then the endpoint SHOULD be transformed to the most sensible format for that implementation. | - | Нет трансформации эндпоинта - адрес передаётся в OPI_GRPC как есть. |
| 8 | SHOULD | ⚠️ partial | SDKs SHOULD default endpoint variables to use http scheme unless they have good reasons to choose https scheme for the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:153-158` | Дефолт http://localhost:4317 для gRPC и http://localhost:4318 для HTTP - используется http. Реализовано корректно. |
| 9 | SHOULD | ❌ not_found | The obsolete environment variables OTEL_EXPORTER_OTLP_SPAN_INSECURE and OTEL_EXPORTER_OTLP_METRIC_INSECURE SHOULD continue to be supported if they were already implemented. | - | Эти устаревшие переменные не реализованы, но это допустимо - они и не были реализованы ранее. |
| 10 | MUST | ✅ found | Protocol: Options MUST be one of: grpc, http/protobuf, http/json. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150-161` |  |
| 11 | SHOULD | ⚠️ partial | The default protocol SHOULD be http/protobuf, unless there are strong reasons for SDKs to select grpc as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Дефолт протокола - 'http/json', а не 'http/protobuf' как рекомендует спецификация. Код: Менеджер.Параметр("otel.exporter.otlp.protocol", "http/json"). |
| 12 | MUST | ⚠️ partial | For the per-signal variables (OTEL_EXPORTER_OTLP_<signal>_ENDPOINT), the URL MUST be used as-is without any modification. The only exception is that if a URL contains no path part, the root path / MUST be used. | - | Per-signal endpoint переменные (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT и т.д.) не поддерживаются, поэтому логика 'URL as-is' не реализована. |
| 13 | MUST NOT | ✅ found | An SDK MUST NOT modify the URL in ways other than specified above (appending signal paths to base URL). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:99-103` |  |
| 14 | MUST | ⚠️ partial | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal: Traces v1/traces, Metrics v1/metrics, Logs v1/logs. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:35` | Пути /v1/traces, /v1/logs, /v1/metrics корректно используются каждым экспортером. Однако URL конструируется не из OTEL_EXPORTER_OTLP_ENDPOINT базы - используется единый транспорт с БазовыйURL. |
| 15 | MUST | ⚠️ partial | For per-signal variables, URL MUST be used as-is without modification, except if URL contains no path part, the root path / MUST be used (see Example 2). | - | Per-signal endpoint переменные не поддерживаются. Нет OTEL_EXPORTER_OTLP_TRACES_ENDPOINT и подобных. |

#### Specify Protocol

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specify-protocol)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ✅ found | SDKs SHOULD support both grpc and http/protobuf transports. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:1` |  |
| 17 | MUST | ✅ found | SDKs MUST support at least one of grpc and http/protobuf transports. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:1` |  |
| 18 | SHOULD | ⚠️ partial | If they support only one, it SHOULD be http/protobuf. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:171` | HTTP-транспорт отправляет Content-Type: application/json, т.е. http/json, а не http/protobuf. Реализованы оба транспорта (HTTP и gRPC), но HTTP-транспорт использует JSON, а не protobuf. |
| 19 | SHOULD | ⚠️ partial | If no configuration is provided the default transport SHOULD be http/protobuf unless SDKs have good reasons to choose grpc as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Дефолт - 'http/json', а не 'http/protobuf'. Код: Менеджер.Параметр("otel.exporter.otlp.protocol", "http/json"). |

#### Specifying headers via environment variables

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | All attribute values MUST be considered strings (for OTEL_EXPORTER_OTLP_HEADERS in format key1=value1,key2=value2). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:467-487` |  |

#### Retry

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#retry)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | Transient errors MUST be handled with a retry strategy. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:76` |  |
| 22 | MUST | ✅ found | This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:165-168` |  |

#### Transient errors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#transient-errors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | SHOULD | ❌ not_found | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter. | - | Нет установки заголовка User-Agent ни в HTTP-транспорте, ни в gRPC-транспорте. Заголовки включают только Content-Type и пользовательские заголовки. |
| 24 | SHOULD | ❌ not_found | The format of the User-Agent header SHOULD follow RFC 7231. | - | User-Agent заголовок не реализован. |
| 25 | SHOULD | ❌ not_found | The resulting User-Agent SHOULD include the exporter's default User-Agent string when a product identifier is added. | - | User-Agent заголовок не реализован. |

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
| 5 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT store a new value in the Context, in order to preserve any previously existing valid value. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:90,96,100,110,114` |  |

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
| 9 | MUST | ✅ found | The implementation SHOULD preserve casing if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:19` |  |

#### Getter argument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#getter-argument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The Keys function MUST return the list of all the keys in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:59-65` |  |
| 11 | MUST | ✅ found | The Get function MUST return the first value of the given propagation key or return null if the key doesn't exist. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:20-28` |  |
| 12 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter (Get) MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:21-23` |  |
| 13 | MUST | ✅ found | If explicitly implemented, the GetAll function MUST return all values of the given propagation key. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40-49` |  |
| 14 | SHOULD | ✅ found | GetAll SHOULD return values in the same order as they appear in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40-49` |  |
| 15 | SHOULD | ✅ found | If the key doesn't exist, GetAll SHOULD return an empty collection. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:41` |  |
| 16 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter (GetAll) MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:43-44` |  |

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
| 19 | MUST | ✅ found | The OpenTelemetry API MUST provide a way to obtain a propagator for each supported Propagator type | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |
| 20 | SHOULD | ✅ found | Instrumentation libraries SHOULD call propagators to extract and inject the context on all remote calls | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:18` |  |
| 21 | MUST | ✅ found | The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise | `src/Ядро/Модули/ОтелГлобальный.os:132` |  |
| 22 | SHOULD | ❌ not_found | Platforms with pre-configured propagators SHOULD default to a composite Propagator containing the W3C Trace Context Propagator and the Baggage Propagator | - | Нет автоконфигурации пропагаторов по умолчанию - SDK не создаёт по умолчанию композитный пропагатор с W3C TraceContext + Baggage, пользователь должен явно сконфигурировать |
| 23 | MUST | ✅ found | Platforms with pre-configured propagators MUST also allow pre-configured propagators to be disabled or overridden | `src/Ядро/Модули/ОтелГлобальный.os:110` |  |

#### Get Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#get-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | Get Global Propagator method MUST exist for each supported Propagator type. Returns a global Propagator, usually a composite instance. | `src/Ядро/Модули/ОтелГлобальный.os:121` |  |

#### Set Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#set-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | Set Global Propagator method MUST exist for each supported Propagator type. Sets the global Propagator instance. | `src/Ядро/Модули/ОтелГлобальный.os:110` |  |
| 26 | MUST | ✅ found | The official list of propagators that MUST be maintained by the OpenTelemetry organization: W3C TraceContext, W3C Baggage, B3 | `src/Пропагация/Классы/ОтелW3CПропагатор.os:1` |  |
| 27 | MUST | ✅ found | Official propagators MUST be distributed as OpenTelemetry extension packages | `src/Пропагация/Классы/ОтелW3CПропагатор.os:1` |  |
| 28 | MUST NOT | ✅ found | OT Trace propagator MUST NOT use 'OpenTracing' in the resulting propagator name as it is not widely adopted format in the OpenTracing ecosystem | - |  |
| 29 | MUST NOT | ✅ found | Additional Propagators implementing vendor-specific protocols such as AWS X-Ray trace header protocol MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories | - |  |

#### W3C Trace Context Requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#w3c-trace-context-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ⚠️ partial | A W3C Trace Context propagator MUST parse and validate the traceparent and tracestate HTTP headers as specified in W3C Trace Context Level 2 | `src/Пропагация/Классы/ОтелW3CПропагатор.os:81` | Код парсит и валидирует traceparent (version ff, all-zeros, длины), но в комментарии указан Level 1, а спецификация требует Level 2. Также не валидируется формат tracestate полностью. |
| 31 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid traceparent value using the same header | `src/Пропагация/Классы/ОтелW3CПропагатор.os:62` |  |
| 32 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid tracestate unless the value is empty, in which case the tracestate header may be omitted | `src/Пропагация/Классы/ОтелW3CПропагатор.os:65` |  |

### Env Vars

#### Environment Variable Specification

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#environment-variable-specification)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ⚠️ partial | Implementations that choose to allow configuration via environment variables SHOULD use the names and value parsing behavior specified in this document. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:6-34` | Большинство стандартных OTEL_* переменных поддержано через configor (OTEL_SERVICE_NAME, OTEL_RESOURCE_ATTRIBUTES, OTEL_TRACES_EXPORTER и т.д.), но вместо OTEL_SDK_DISABLED используется нестандартная OTEL_ENABLED с инвертированной логикой. OTEL_LOG_LEVEL и OTEL_ENTITIES не поддержаны. |
| 2 | SHOULD | ✅ found | Implementations that choose to allow configuration via environment variables SHOULD also follow the common configuration specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:80-86` |  |

#### Implementation guidelines

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#implementation-guidelines)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The environment-based configuration MUST have a direct code configuration equivalent. | `src/Ядро/Классы/ОтелПостроительSdk.os:24-66` |  |

#### Parsing empty value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#parsing-empty-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ⚠️ partial | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105,340` | Обработка пустых значений реализована частично: для ресурсных атрибутов (строка 105) и пропагаторов (строка 340) пустые значения проверяются явно (<> ""), но для многих других параметров (например, otel.service.name строка 114, числовые параметры строки 224-227) пустая строка не проверяется и может привести к ошибкам. Библиотека configor не фильтрует пустые значения на уровне провайдера ENV (oscript_modules/configor/.../ПровайдерПараметровENV.os:57-59). |

#### Type-specific guidance### Boolean

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#type-specific-guidance-boolean)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Any value that represents a Boolean MUST be set to true only by the case-insensitive string "true", meaning "True" or "TRUE" are also accepted, as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 6 | MUST NOT | ✅ found | An implementation MUST NOT extend this definition and define additional values that are interpreted as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 7 | MUST | ✅ found | Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563` |  |
| 8 | SHOULD | ❌ not_found | If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied. | - | Функция Включено() (строка 562) просто сравнивает НРег(Значение) = "true" без логирования предупреждения для нераспознанных значений (не "true" и не "false"). |
| 9 | SHOULD | ⚠️ partial | All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562` | Используется нестандартная переменная OTEL_ENABLED (по умолчанию true), а не OTEL_SDK_DISABLED (по умолчанию false). Имя OTEL_ENABLED нарушает принцип: false для неё означает отключение SDK, что не является "безопасным по умолчанию". |
| 10 | MUST NOT | ✅ found | Renaming or changing the default value MUST NOT happen without a major version upgrade. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562` |  |

#### Numeric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#numeric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ❌ not_found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning. | - | Числовые параметры парсятся вызовом Число() без обработки ошибок (например, строки 224-227). Невалидное значение вызовет исключение OneScript, а не предупреждение с fallback на значение по умолчанию. |
| 12 | SHOULD | ❌ not_found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD gracefully ignore the setting, i.e., treat them as not set. | - | При невалидном числовом значении вызов Число() бросит исключение вместо того чтобы проигнорировать значение и использовать значение по умолчанию. Нет try/catch обработки для парсинга чисел. |
| 13 | SHOULD | ❌ not_found | For new implementations, the SHOULD requirements for numeric parsing should be treated as MUST requirements. | - | Проект opentelemetry версии 0.1.0 является новой реализацией, поэтому SHOULD-требования по парсингу числовых значений должны рассматриваться как MUST. Ни предупреждение, ни graceful ignore не реализованы. |

#### String

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#string)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | SHOULD | ⚠️ partial | Enum values SHOULD be interpreted in a case-insensitive manner. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:344` | Регистронезависимая обработка реализована только для пропагаторов (НРег на строке 344) и компрессии (строка 144). Для семплеров (строки 197-218) и экспортеров (строки 177-178, 255-256, 291-292) сравнение выполняется регистрозависимо (= "always_on", = "otlp", = "none"). |
| 15 | MUST | ⚠️ partial | For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:373` | Для пропагаторов неизвестное значение вызывает Сообщить() (строка 373) и пропускается, но значение не игнорируется полностью - другие пропагаторы из списка всё равно применяются. Для семплеров (строки 216-218) нераспознанное значение молча заменяется на ParentBased(AlwaysOn) без предупреждения. Для экспортеров нераспознанное значение не обрабатывается. |

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
| 1 | SHOULD | ❌ not_found | Resource detectors SHOULD have a unique name for reference in configuration. | - | Детекторы (ОтелДетекторРесурсаХоста и т.д.) не имеют свойства или метода для получения уникального имени. Нет механизма именования детекторов. |
| 2 | SHOULD | ❌ not_found | Names SHOULD be snake case and consist of lowercase alphanumeric and _ characters, which ensures they conform to declarative configuration property name requirements. | - | Именование детекторов не реализовано, поэтому формат имени не применим. |
| 3 | SHOULD | ❌ not_found | Resource detector names SHOULD reflect the root namespace of attributes they populate. | - | Именование детекторов не реализовано. |
| 4 | SHOULD | ❌ not_found | Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name which appropriately conveys their purpose. | - | Именование детекторов не реализовано. |
| 5 | SHOULD | ❌ not_found | An SDK which identifies multiple resource detectors with the same name SHOULD report an error. | - | Нет механизма именования детекторов, поэтому нет и проверки дубликатов. |
| 6 | SHOULD | ❌ not_found | In order to limit collisions, resource detectors SHOULD document their name in a manner which is easily discoverable. | - | Именование детекторов не реализовано, документирование имён отсутствует. |
| 7 | MUST | ✅ found | The SDK MUST extract information from the OTEL_RESOURCE_ATTRIBUTES environment variable and merge this, as the secondary resource, with any resource information provided by the user. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:96` |  |
| 8 | MUST | ⚠️ partial | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:467` | РазобратьПарыКлючЗначение возвращает строковые значения, но нет явной спецификации типа. Значения по факту строки, что соответствует требованию. |
| 9 | MUST | ❌ not_found | The , and = characters in keys and values MUST be percent encoded. | - | Парсер РазобратьПарыКлючЗначение (строка 467) разбивает по запятой и знаку равенства, но не выполняет процентное декодирование (percent-decode). Если ключ или значение содержат %2C или %3D, они не будут декодированы обратно. |
| 10 | SHOULD | ❌ not_found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded. | - | В коде парсинга OTEL_RESOURCE_ATTRIBUTES нет обработки ошибок - невалидные пары просто пропускаются (ПозицияРавно <= 0), а не вызывают отброс всей переменной. |
| 11 | SHOULD | ❌ not_found | An error during decoding SHOULD be reported following the Error Handling principles. | - | Ошибки парсинга не логируются и не репортятся. |

### Trace Api

#### Tracer operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracer-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The Tracer MUST provide functions to: Create a new Span. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 2 | SHOULD | ✅ found | The Tracer SHOULD provide functions to: Report if Tracer is Enabled. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 3 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when creating Spans, a Tracer SHOULD provide this Enabled API. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 4 | MUST | ✅ found | The API MUST be structured in a way for parameters to be added (to the Enabled API). | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 5 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. A returned value of true means the Tracer is enabled, false means disabled. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 6 | SHOULD | ❌ not_found | The API SHOULD be documented that instrumentation authors needs to call this API each time they create a new Span to ensure they have the most up-to-date response. | - | Документация метода Включен() не содержит указания на то, что инструментирующий код должен вызывать этот метод каждый раз перед созданием спана для получения актуального ответа. |

### Trace Sdk

#### Tracer Provider### Tracer Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer-provider-tracer-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create Tracer instances through a TracerProvider | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 2 | MUST | ✅ found | The TracerProvider MUST implement the Get a Tracer API | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:58` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Tracer | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:63-72` |  |
| 4 | MUST | ✅ found | The TracerProvider MUST compute the relevant TracerConfig using the configured TracerConfigurator, and create a Tracer whose behavior conforms to that TracerConfig | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:71-72` |  |

#### TracerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: tracer_scope: The InstrumentationScope of the Tracer | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:215-223` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant TracerConfig, or some signal indicating that the default TracerConfig should be used | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:215-223` |  |
| 3 | MUST | ✅ found | Shutdown MUST be called only once for each TracerProvider instance | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:107-114` |  |
| 4 | SHOULD | ✅ found | After the call to Shutdown, subsequent attempts to get a Tracer are not allowed. SDKs SHOULD return a valid no-op Tracer for these calls, if possible | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65-66` |  |
| 5 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:107-114` | Метод Закрыть() является процедурой (void), не возвращает статус успеха/неудачи/таймаута. Есть ЗакрытьАсинхронно() с Обещанием, но синхронный вариант не сообщает результат |
| 6 | SHOULD | ✅ found | Shutdown SHOULD complete or abort within some timeout | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:132-135` |  |
| 7 | MUST | ✅ found | Shutdown MUST be implemented at least by invoking Shutdown within all internal processors | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:111-113` |  |

#### Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Tracer MUST behave according to the TracerConfig computed during Tracer creation | `src/Трассировка/Классы/ОтелТрассировщик.os:38-43` |  |
| 2 | MUST | ❌ not_found | If the TracerProvider supports updating the TracerConfigurator, then upon update the Tracer MUST be updated to behave according to the new TracerConfig | - | TracerProvider не поддерживает динамическое обновление TracerConfigurator. Конфигуратор задаётся при создании провайдера и не обновляется; существующие трассировщики в кэше не переконфигурируются при изменении |

#### TracerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the enabled parameter SHOULD default to true (i.e. Tracers are enabled by default) | `src/Трассировка/Классы/ОтелКонфигурацияТрассировщика.os:35` |  |
| 2 | MUST | ✅ found | If a Tracer is disabled, it MUST behave equivalently to a No-op Tracer | `src/Трассировка/Классы/ОтелТрассировщик.os:38-43` |  |
| 3 | MUST | ✅ found | The value of enabled MUST be used to resolve whether a Tracer is Enabled. If enabled is false, Enabled returns false. If enabled is true, Enabled returns true | `src/Трассировка/Классы/ОтелТрассировщик.os:38-43` |  |
| 4 | MUST | ❌ not_found | The changes MUST be eventually visible (changes to TracerConfig parameters must be eventually visible to callers of Enabled) | - | Конфигурация трассировщика задаётся при создании и не обновляется динамически. Нет механизма обновления TracerConfig на существующих трассировщиках - ссылка на конфигурацию фиксируется при создании |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Enabled MUST return false when either: there are no registered SpanProcessors, or Tracer is disabled (TracerConfig.enabled is false) | `src/Трассировка/Классы/ОтелТрассировщик.os:38-43` |  |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return true | `src/Трассировка/Классы/ОтелТрассировщик.os:42` |  |

#### AlwaysOn* Returns `RECORD_AND_SAMPLE` always.* Description MUST be `AlwaysOnSampler`.#### AlwaysOff* Returns `DROP` always.* Description MUST be `AlwaysOffSampler`.#### TraceIdRatioBased

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwayson-returns-recordandsample-always-description-must-be-alwaysonsampler-alwaysoff-returns-drop-always-description-must-be-alwaysoffsampler-traceidratiobased)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | AlwaysOn: Description MUST be AlwaysOnSampler. | `src/Трассировка/Модули/ОтелСэмплер.os:109` |  |
| 2 | MUST | ✅ found | AlwaysOff: Description MUST be AlwaysOffSampler. | `src/Трассировка/Модули/ОтелСэмплер.os:111` |  |
| 3 | MUST | ✅ found | The TraceIdRatioBased MUST ignore the parent SampledFlag. | `src/Трассировка/Модули/ОтелСэмплер.os:275-297` |  |
| 4 | MUST | ✅ found | Description MUST return a string of the form TraceIdRatioBased{RATIO} with RATIO replaced with the Sampler instance's trace sampling ratio represented as a decimal number. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 5 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 6 | SHOULD | ✅ found | The precision of the number SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 7 | MUST | ✅ found | The sampling algorithm MUST be deterministic. A trace identified by a given TraceId is sampled or not independent of language, time, etc. | `src/Трассировка/Модули/ОтелСэмплер.os:288-296` |  |
| 8 | MUST | ✅ found | Implementations MUST use a deterministic hash of the TraceId when computing the sampling decision. | `src/Трассировка/Модули/ОтелСэмплер.os:288-290` |  |
| 9 | MUST | ⚠️ partial | A TraceIdRatioBased sampler with a given sampling probability MUST also sample all traces that any TraceIdRatioBased sampler with a lower sampling probability would sample. | `src/Трассировка/Модули/ОтелСэмплер.os:275-296` | The implementation uses first 8 hex chars (32 bits) and compares hash < threshold. This approach does satisfy the subset property because a higher ratio means a higher threshold, so any trace sampled at a lower threshold is also sampled at a higher one. However, using only the first 8 chars (leftmost) instead of rightmost bytes is non-standard and may not be compatible with other SDKs. |
| 10 | SHOULD | ❌ not_found | When this sampler observes a non-empty parent span context (used as non-root sampler), the SDK SHOULD emit a warning about TraceIdRatioBased being used as child sampler. | - | No warning is emitted when TraceIdRatioBased is used as a child sampler. The ПоДолеТрассировок strategy always computes the sampling decision without checking parent context or emitting any warnings. |
| 11 | MUST | ❌ not_found | The ProbabilitySampler sampler MUST ignore the parent SampledFlag. | - | ProbabilitySampler is not implemented. Only TraceIdRatioBased exists. |
| 12 | SHOULD | ❌ not_found | When ProbabilitySampler returns RECORD_AND_SAMPLE, the OpenTelemetry TraceState SHOULD be modified to include the key-value th:T for rejection threshold value. | - | ProbabilitySampler is not implemented. No TraceState th: sub-key handling exists. |
| 13 | SHOULD | ❌ not_found | When a ProbabilitySampler Sampler makes a decision for a non-root Span using TraceID randomness when the Trace random flag was not set, the SDK SHOULD issue a warning statement. | - | ProbabilitySampler is not implemented. |
| 14 | MUST | ❌ not_found | AlwaysRecord MUST behave as follows: DROP->RECORD_ONLY, RECORD_ONLY->RECORD_ONLY, RECORD_AND_SAMPLE->RECORD_AND_SAMPLE. | - | AlwaysRecord sampler decorator is not implemented in this SDK. |
| 15 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the parameters passed to delegate GetSamplingIntent methods, as they are considered read-only state. | - | ComposableSampler/CompositeSampler are not implemented in this SDK. |
| 16 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the OpenTelemetry TraceState (i.e., the ot sub-key of TraceState). | - | ComposableSampler is not implemented in this SDK. |
| 17 | SHOULD | ❌ not_found | The calling CompositeSampler SHOULD update the threshold of the outgoing TraceState (unless !threshold_reliable). | - | CompositeSampler is not implemented in this SDK. |
| 18 | MUST | ❌ not_found | Explicit randomness values MUST not be modified [by ComposableSamplers]. | - | ComposableSampler is not implemented in this SDK. |
| 19 | SHOULD | ❌ not_found | For ComposableProbability, a ratio value of 0 is considered non-probabilistic. For the zero case a ComposableAlwaysOff instance SHOULD be returned instead. | - | ComposableProbability is not implemented in this SDK. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | Custom implementations of the IdGenerator SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace random flag will be set in the associated Trace contexts. | - | УстановитьГенераторИд() принимает произвольный объект с методами генерации, но нет механизма для IdGenerator объявить соответствие требованиям W3C Level 2 randomness (нет маркерного интерфейса, метода IsRandom и т.п.). Флаг random не управляется генератором. |

#### OnEnding

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onending)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The end timestamp MUST have been computed (the OnEnding method duration is not included in the span duration). | `src/Трассировка/Классы/ОтелСпан.os:449` |  |
| 2 | MUST | ✅ found | The Span object MUST still be mutable (i.e., SetAttribute, AddLink, AddEvent can be called) while OnEnding is called. | `src/Трассировка/Классы/ОтелСпан.os:455` |  |
| 3 | MUST | ✅ found | This method MUST be called synchronously within the Span.End() API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:455` |  |
| 4 | MUST | ⚠️ partial | The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking OnEnding of the first SpanProcessor. From that point on, modifications are only allowed synchronously from within the invoked OnEnding callbacks. | `src/Трассировка/Классы/ОтелСпан.os:447` | Порядок вызовов внутри Завершить() корректен (OnEnding вызывается до установки Завершен=Истина), но отсутствует явная синхронизация (БлокировкаРесурса) для предотвращения конкурентной модификации спана из другого потока. Другой поток может вызвать УстановитьАтрибут() во время выполнения ПередЗавершением(). |

### Logs Api

#### Ergonomic API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#ergonomic-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | The ergonomic API SHOULD make it more convenient to emit event records following the event semantics. | - | Отдельного эргономичного API для эмиссии событий (event records) с семантикой событий не реализовано. ОтелАппендерLogos является мостом для logos-библиотеки, но не предоставляет удобного API для создания именно event-записей с EventName. |
| 2 | SHOULD | ❌ not_found | The design of the ergonomic API SHOULD be idiomatic for its language. | - | Отдельный эргономичный API для логирования не реализован, поэтому требование к идиоматичности неприменимо на практике - нет объекта для оценки. |

### Logs Sdk

#### Logger Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create Logger instances through a LoggerProvider (see API). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:39` |  |
| 2 | MUST | ✅ found | The LoggerProvider MUST implement the Get a Logger API. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Logger. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:64` |  |
| 4 | MUST | ✅ found | In the case where an invalid name (null or empty string) is specified, a working Logger MUST be returned as a fallback rather than returning null or throwing an exception. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 5 | SHOULD | ✅ found | its name SHOULD keep the original invalid value | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:94` |  |
| 6 | SHOULD | ❌ not_found | a message reporting that the specified value is invalid SHOULD be logged | - | ПолучитьЛоггер не проверяет имя на пустоту/null и не логирует предупреждение при передаче невалидного имени. Нет вызова Лог.Предупреждение() при пустом ИмяБиблиотеки. |
| 7 | MUST | ✅ found | The LoggerProvider MUST compute the relevant LoggerConfig using the configured LoggerConfigurator, and create a Logger whose behavior conforms to that LoggerConfig. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:69` |  |

#### LoggerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: logger_scope: The InstrumentationScope of the Logger. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:72` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant LoggerConfig, or some signal indicating that the default LoggerConfig should be used. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:69` |  |
| 3 | MUST | ✅ found | Shutdown MUST be called only once for each LoggerProvider instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:117` |  |
| 4 | SHOULD | ✅ found | After the call to Shutdown, subsequent attempts to get a Logger are not allowed. SDKs SHOULD return a valid no-op Logger for these calls, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:59` |  |
| 5 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:116` | Синхронный метод Закрыть() - void-процедура без возвращаемого значения. ЗакрытьАсинхронно() возвращает Обещание, но нет явного кода ошибки/успеха. |
| 6 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:116` | Нет встроенного таймаута в Закрыть(). ЗакрытьАсинхронно() делегирует в async-фреймворк с поддержкой таймаутов, но сам провайдер не задаёт timeout. |
| 7 | MUST | ✅ found | Shutdown MUST be implemented by invoking Shutdown on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:120` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Logger MUST behave according to the LoggerConfig computed during logger creation | `src/Логирование/Классы/ОтелЛоггер.os:49-59` |  |
| 2 | MUST | ✅ found | If the LoggerProvider supports updating the LoggerConfigurator, then upon update the Logger MUST be updated to behave according to the new LoggerConfig | `src/Логирование/Классы/ОтелЛоггер.os:123-125` |  |

#### LoggerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The enabled parameter SHOULD default to true (i.e. Loggers are enabled by default) | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 2 | MUST | ✅ found | If a Logger is disabled, it MUST behave equivalently to No-op Logger | `src/Логирование/Классы/ОтелЛоггер.os:49-51` |  |
| 3 | MUST | ✅ found | If not explicitly set, the minimum_severity parameter MUST default to 0 | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 4 | MUST | ✅ found | If a log record's SeverityNumber is specified (i.e. not 0) and is less than the configured minimum_severity, the log record MUST be dropped by the Logger | `src/Логирование/Классы/ОтелЛоггер.os:53-56` |  |
| 5 | MUST | ✅ found | If not explicitly set, the trace_based parameter MUST default to false | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 6 | MUST | ✅ found | If trace_based is true, log records associated with unsampled traces MUST be dropped by the Logger | `src/Логирование/Классы/ОтелЛоггер.os:57-59` |  |
| 7 | MUST | ✅ found | Changes to LoggerConfig parameters MUST be eventually visible | `src/Логирование/Классы/ОтелЛоггер.os:123-125` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If Observed Timestamp is unspecified, the implementation SHOULD set it equal to the current time | `src/Логирование/Классы/ОтелЛоггер.os:102-104` |  |
| 2 | MUST | ✅ found | If an Exception is provided, the SDK MUST by default set attributes from the exception on the LogRecord with the conventions outlined in the exception semantic conventions | `src/Логирование/Классы/ОтелЛоггер.os:170-181` |  |
| 3 | MUST | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes | `src/Логирование/Классы/ОтелЛоггер.os:183-187` |  |
| 4 | MUST NOT | ✅ found | User-provided attributes MUST NOT be overwritten by exception-derived attributes | `src/Логирование/Классы/ОтелЛоггер.os:183-187` |  |
| 5 | MUST | ✅ found | Before processing a log record, the implementation MUST apply the filtering rules defined by the LoggerConfig (in case Enabled was not called prior to emitting the record) | `src/Логирование/Классы/ОтелЛоггер.os:94-96` |  |
| 6 | MUST | ✅ found | Minimum severity: If the log record's SeverityNumber is specified (i.e. not 0) and is less than the configured minimum_severity, the log record MUST be dropped | `src/Логирование/Классы/ОтелЛоггер.os:138-141` |  |
| 7 | MUST | ✅ found | Trace-based: If trace_based is true, and if the log record has a SpanId and the TraceFlags SAMPLED flag is unset, the log record MUST be dropped | `src/Логирование/Классы/ОтелЛоггер.os:143-144` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST NOT | ✅ found | Any modifications to parameters inside Enabled MUST NOT be propagated to the caller. Parameters are immutable or passed by value. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |

### Metrics Api

#### General characteristics#### Instrument name syntax

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-characteristics-instrument-name-syntax)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD treat the unit as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:219` |  |
| 2 | MUST | ✅ found | The unit MUST be case-sensitive (e.g. kb and kB are different units), ASCII string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:219` |  |
| 3 | MUST | ✅ found | The API MUST treat the description as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:226` |  |
| 4 | MUST | ✅ found | The description MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or utf8mb3). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:226` |  |
| 5 | MUST | ✅ found | The description MUST support at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:226` |  |
| 6 | MUST | ✅ found | OpenTelemetry SDKs MUST handle advisory parameters as described here. | `src/Метрики/Классы/ОтелМетр.os:642` |  |

### Metrics Sdk

#### Meter Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create Meter instances through a MeterProvider (see API). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 2 | MUST | ✅ found | The MeterProvider MUST implement the Get a Meter API. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Meter. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:62` |  |
| 4 | MUST | ⚠️ partial | In the case where an invalid name (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` | ПолучитьМетр не проверяет на пустое/null имя и не обрабатывает этот случай специально - метр создаётся, но нет явной проверки и fallback-логики |
| 5 | SHOULD | ⚠️ partial | its name SHOULD keep the original invalid value | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` | Имя сохраняется как есть, но нет явной обработки невалидного имени - формально значение сохраняется, но без осознанной обработки |
| 6 | SHOULD | ❌ not_found | a message reporting that the specified value is invalid SHOULD be logged | - | Нет логирования предупреждения при передаче невалидного (пустого или null) имени в ПолучитьМетр |
| 7 | MUST | ✅ found | The MeterProvider MUST compute the relevant MeterConfig using the configured MeterConfigurator, and create a Meter whose behavior conforms to that MeterConfig. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:73` |  |

#### MeterConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: meter_scope: The InstrumentationScope of the Meter. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:210` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant MeterConfig, or some signal indicating that the default MeterConfig should be used. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:211` |  |
| 3 | MUST | ✅ found | Shutdown MUST be called only once for each MeterProvider instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:130` |  |
| 4 | SHOULD | ✅ found | After the call to Shutdown, subsequent attempts to get a Meter are not allowed. SDKs SHOULD return a valid no-op Meter for these calls, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:57` |  |
| 5 | SHOULD | ❌ not_found | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Процедура Закрыть() не возвращает значения (Процедура, а не Функция), вызывающий не может узнать, успешно ли завершение. ЗакрытьАсинхронно возвращает Обещание, но синхронный Закрыть - нет. |
| 6 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` | Таймаут реализован на уровне MetricReader (ожидание фонового задания с таймаутом), но не на уровне MeterProvider.Закрыть() - нет общего таймаута для всей операции |
| 7 | MUST | ✅ found | Shutdown MUST be implemented at least by invoking Shutdown on all registered MetricReader and MetricExporter instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:136` |  |

#### Start timestamps

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#start-timestamps)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp, or the creation time of the instrument if this is the first collection interval for the instrument. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141-146` |  |
| 2 | MUST | ✅ found | This implies that all data points with delta temporality aggregation for an instrument MUST share the same start timestamp. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:272-286` |  |
| 3 | MUST | ✅ found | Cumulative timeseries MUST use a consistent start timestamp for all collection intervals. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141-146` |  |
| 4 | SHOULD | ⚠️ partial | For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the series. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:263` | Время старта устанавливается при создании инструмента (ВремяСтарта = ОтелУтилиты.ТекущееВремяВНаносекундах()), а не при первом измерении для серии |
| 5 | SHOULD | ⚠️ partial | For asynchronous instruments, the start timestamp SHOULD be: the creation time of the instrument if the first series measurement occurred in the first collection interval, otherwise the timestamp of the collection interval prior to the first series measurement. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:184` | startTimeUnixNano устанавливается равным текущему времени сбора (ВремяСейчас), а не времени создания инструмента или предыдущему интервалу сбора |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instrument registrations. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:64` |  |
| 2 | MUST | ✅ found | Meter MUST behave according to the MeterConfig computed during Meter creation. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:206` |  |
| 3 | MUST | ❌ not_found | If the MeterProvider supports updating the MeterConfigurator, then upon update the Meter MUST be updated to behave according to the new MeterConfig. | - | ОтелПровайдерМетрик не поддерживает обновление конфигуратора после создания. Конфигуратор задаётся только при создании провайдера (конструктор, строка 267) и применяется однократно при создании метра. Нет метода для обновления конфигуратора и переприменения конфигурации к существующим метрам. |

#### MeterConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the enabled parameter SHOULD default to true (i.e. Meters are enabled by default). | `src/Метрики/Классы/ОтелКонфигурацияМетра.os:35` |  |
| 2 | MUST | ✅ found | If a Meter is disabled, it MUST behave equivalently to No-op Meter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:174` |  |
| 3 | MUST | ✅ found | The value of enabled MUST be used to resolve whether an instrument is Enabled. See Instrument Enabled for details. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201` |  |
| 4 | MUST | ✅ found | It is not necessary for implementations to ensure that changes to any of these parameters are immediately visible to callers of Enabled. However, the changes MUST be eventually visible. | `src/Метрики/Классы/ОтелМетр.os:504` |  |

#### Instrument enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The synchronous instrument Enabled MUST return false when either: the MeterConfig of the Meter used to create the instrument has parameter enabled=false, or all resolved views for the instrument are configured with the Drop Aggregation. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:201-202` |  |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return true. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:267` |  |

#### MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | To construct a MetricReader, the exporter to use, which is a MetricExporter instance, SHOULD be provided. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:276` |  |
| 2 | SHOULD | ⚠️ partial | The default output aggregation (optional), a function of instrument kind, SHOULD be obtained from the exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:168` | Агрегация по умолчанию управляется через ОтелАгрегация и View, но не получается напрямую из экспортера через MetricReader. |
| 3 | SHOULD | ✅ found | If not configured, the default aggregation SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` |  |
| 4 | SHOULD | ✅ found | The output temporality (optional), a function of instrument kind, SHOULD be obtained from the exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:168` |  |
| 5 | SHOULD | ✅ found | If not configured, the Cumulative temporality SHOULD be used. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:88` |  |
| 6 | SHOULD | ✅ found | If not configured, a default aggregation cardinality limit value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253` |  |
| 7 | SHOULD | ✅ found | A MetricReader SHOULD provide the MetricFilter to the SDK or registered MetricProducer(s) when calling the Produce operation. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:110` |  |
| 8 | SHOULD | ✅ found | A common implementation of MetricReader, the periodic exporting MetricReader SHOULD be provided to be used typically with push-based metrics collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:1` |  |
| 9 | MUST | ✅ found | The MetricReader MUST ensure that data points from OpenTelemetry instruments are output in the configured aggregation temporality for each instrument kind. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:168` |  |
| 10 | MUST | ⚠️ partial | For synchronous instruments with Cumulative aggregation temporality, MetricReader.Collect MUST receive data points exposed in previous collections regardless of whether new measurements have been recorded. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138` | Для кумулятивной временности аккумуляторы и время старта сохраняются (ОчиститьТочкиДанных не очищает при Кумулятивная), но механика полного соответствия зависит от интеграционного поведения. |
| 11 | MUST | ✅ found | For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138` |  |
| 12 | MUST | ✅ found | For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:112` |  |
| 13 | MUST | ⚠️ partial | For instruments with Cumulative aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST repeat the same starting timestamps (e.g. (T0, T1], (T0, T2], (T0, T3]). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:138` | Для кумулятивной временности время старта сохраняется при очистке, но явной проверки повторения StartTime нет в коде - это следствие логики ОчиститьТочкиДанных. |
| 14 | MUST | ✅ found | For instruments with Delta aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST advance the starting timestamp (e.g. (T0, T1], (T1, T2], (T2, T3]). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:145` |  |
| 15 | MUST | ✅ found | The ending timestamp (i.e. TimeUnixNano) MUST always be equal to time the metric data point took effect, which is equal to when MetricReader.Collect was invoked. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:121` |  |
| 16 | MUST | ✅ found | The SDK MUST support multiple MetricReader instances to be registered on the same MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:107` |  |
| 17 | SHOULD NOT | ✅ found | The MetricReader.Collect invocation on one MetricReader instance SHOULD NOT introduce side-effects to other MetricReader instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:112` |  |
| 18 | MUST NOT | ❌ not_found | The SDK MUST NOT allow a MetricReader instance to be registered on more than one MeterProvider instance. | - | Нет проверки на регистрацию читателя в нескольких MeterProvider. Читатель можно добавить в несколько провайдеров без ошибки. |
| 19 | SHOULD | ✅ found | The SDK SHOULD provide a way to allow MetricReader to respond to MeterProvider.ForceFlush and MeterProvider.Shutdown. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:115` |  |

#### Produce batch

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#produce-batch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | Produce MUST return a batch of Metric Points, filtered by the optional metricFilter parameter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:173` | СобратьИЭкспортировать() собирает данные и применяет ФильтрМетрик через МетрикаОтброшена(). Однако метод не возвращает batch Metric Points - он внутренне экспортирует их. Фильтр metricFilter поддерживается через ОтелФильтрМетрик, но архитектура Produce как возвращающего данные вызывающему не реализована. |
| 2 | SHOULD | ⚠️ partial | Implementation SHOULD use the filter as early as possible to gain as much performance gain possible (memory allocation, internal metric fetching, etc). | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:193` | Фильтрация метрик происходит после сбора данных инструментом (Инструмент.Собрать вызывается до проверки фильтром), а не до сбора. Для частичного принятия (Accept_Partial) фильтрация атрибутов тоже выполняется post-hoc. Фильтрация не применяется на самом раннем этапе. |
| 3 | SHOULD | ❌ not_found | If the batch of Metric Points includes resource information, Produce SHOULD require a resource as a parameter. | - | Ресурс берется из объекта Метр (Метр.Ресурс()), а не передается как параметр Produce. Нет метода Produce, принимающего ресурс в качестве параметра. |
| 4 | SHOULD | ❌ not_found | Produce SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | СобратьИЭкспортировать() - приватная процедура без возвращаемого значения. Ошибки логируются, но вызывающий код не получает информации об успехе/неудаче/таймауте. |
| 5 | SHOULD | ❌ not_found | If a batch of Metric Points can include InstrumentationScope information, Produce SHOULD include a single InstrumentationScope which identifies the MetricProducer. | - | InstrumentationScope берется из каждого Метра (Метр.ОбластьИнструментирования()), но нет InstrumentationScope, идентифицирующего сам MetricProducer. MetricProducer как отдельный интерфейс не реализован. |

### Env Vars

#### Prometheus Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#prometheus-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD NOT | ✅ found | "logging" value for OTEL_TRACES_EXPORTER is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:177-180` |  |
| 2 | SHOULD NOT | ✅ found | "logging" value for OTEL_METRICS_EXPORTER is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:291-294` |  |
| 3 | SHOULD NOT | ✅ found | "logging" value for OTEL_LOGS_EXPORTER is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:255-258` |  |
| 4 | MUST | ❌ not_found | When OTEL_CONFIG_FILE is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored. | - | OTEL_CONFIG_FILE и декларативная конфигурация не реализованы. Нет поддержки файловой конфигурации SDK и механизма игнорирования остальных переменных окружения при её использовании. |

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

- ⚠️ Секция Metrics Api/Note: in the real world these would be retrieved from the operating system: 1 требований (ожидалось ~16)
- ⚠️ Секция Metrics Api/Note: in the real world these would be retrieved from the operating system: 1 требований (ожидалось ~7)
- ⚠️ Секция Metrics Sdk/Configuration: 5 требований (ожидалось ~3)
- ⚠️ Секция Env Vars/General SDK ConfigurationNameDescriptionDefaultTypeNotesOTEL_SDK_DISABLEDDisable the SDK for all signalsfalseBooleanIf “true”, a no-op SDK implementation will be used for all telemetry signals. Any other value or absence of the variable will have no effect and the SDK will remain enabled. This setting has no effect on propagators configured through the OTEL_PROPAGATORS variable.OTEL_ENTITIESEntity information to be associated with the resourceStringSee Entities SDK for more details.OTEL_RESOURCE_ATTRIBUTESKey-value pairs to be used as resource attributesSee Resource semantic conventions for details.StringSee Resource SDK for more details.OTEL_SERVICE_NAMESets the value of the `service.name` resource attributeStringIf `service.name` is also provided in `OTEL_RESOURCE_ATTRIBUTES`, then `OTEL_SERVICE_NAME` takes precedence.OTEL_LOG_LEVELLog level used by the SDK internal logger“info”EnumOTEL_PROPAGATORSPropagators to be used as a comma-separated list“tracecontext,baggage”EnumValues MUST be deduplicated in order to register a `Propagator` only once.OTEL_TRACES_SAMPLERSampler to be used for traces“parentbased_always_on”EnumSee SamplingOTEL_TRACES_SAMPLER_ARGValue to be used as the sampler argumentSee footnoteThe specified value will only be used if OTEL_TRACES_SAMPLER is set. Each Sampler type defines its own expected input, if any. Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. (5 kw) - нет результата от агента

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

