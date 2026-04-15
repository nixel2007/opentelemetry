# Анализ соответствия спецификации OpenTelemetry v1.55.0

> **Версия спецификации**: [v1.55.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-04-15
> **Методология**: spec-first - извлечены все MUST/SHOULD требования из спецификации, затем каждое прослежено до кода

## Сводка (Stable)

Учитываются только требования из стабильных разделов спецификации с универсальной областью применения.

| Показатель | Значение |
|---|---|
| Всего keywords в спецификации | 824 |
| Stable + universal keywords | 701 |
| Conditional keywords | 6 |
| Development keywords | 123 |
| Найдено требований (Stable universal) | 699 |
| ✅ Реализовано (found) | 606 (86.7%) |
| ⚠️ Частично (partial) | 53 (7.6%) |
| ❌ Не реализовано (not_found) | 40 (5.7%) |
| ➖ Неприменимо (n_a) | 2 |
| **MUST/MUST NOT found** | 406/423 (96.0%) |
| **SHOULD/SHOULD NOT found** | 200/276 (72.5%) |

## Соответствие по разделам (Stable)

| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |
|---|---|---|---|---|---|---|
| Context | 15 | 0 | 0 | 0 | 15 | 100.0% |
| Baggage Api | 16 | 1 | 0 | 0 | 17 | 94.1% |
| Resource Sdk | 17 | 1 | 2 | 0 | 20 | 85.0% |
| Trace Api | 114 | 7 | 1 | 0 | 122 | 93.4% |
| Trace Sdk | 65 | 12 | 5 | 0 | 82 | 79.3% |
| Logs Api | 21 | 0 | 0 | 0 | 21 | 100.0% |
| Logs Sdk | 60 | 4 | 0 | 0 | 64 | 93.8% |
| Metrics Api | 91 | 7 | 2 | 0 | 100 | 91.0% |
| Metrics Sdk | 135 | 16 | 18 | 2 | 169 | 79.9% |
| Otlp Exporter | 17 | 1 | 7 | 0 | 25 | 68.0% |
| Propagators | 37 | 3 | 0 | 0 | 40 | 92.5% |
| Env Vars | 18 | 1 | 5 | 0 | 24 | 75.0% |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Resource Sdk]** [MUST] Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK.  
  Детекторы реализованы как отдельные классы (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора), но они находятся внутри того же пакета SDK (зарегистрированы в lib.config), а не в отдельных пакетах. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1`)

- ⚠️ **[Trace Api]** [MUST NOT] This operation itself MUST NOT perform blocking I/O on the calling thread.  
  End() вызывает Процессор.ПриЗавершении(), а SimpleSpanProcessor синхронно вызывает Экспортер.Экспортировать(), что может выполнять блокирующий HTTP-запрос. BatchSpanProcessor не блокирует. Спецификация допускает это для отладочных процессоров, но сам End() формально не гарантирует отсутствие блокирующего I/O. (`src/Трассировка/Классы/ОтелСпан.os:459`)

- ⚠️ **[Trace Sdk]** [MUST] For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated since 1.10.0] having the same name and version values as the `InstrumentationScope`.  
  InstrumentationScope is accessible via ОбластьИнструментирования() and contains the same name/version data, but there is no explicit InstrumentationLibrary type or accessor alias for backwards compatibility. (`src/Трассировка/Классы/ОтелСпан.os:182`)

- ❌ **[Trace Sdk]** [MUST NOT] SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value.  
  В коде нет проверки подключа 'rv' в TraceState и предотвращения его перезаписи. ОтелСостояниеТрассировки поддерживает работу с TraceState, но нет специальной обработки подключа 'rv' для explicit randomness. (-)

- ⚠️ **[Trace Sdk]** [MUST] name of the methods MUST be consistent with SpanContext  
  Методы названы СгенерироватьИдТрассировки/СгенерироватьИдСпана (русские названия), что семантически корректно, но не точно соответствует английской конвенции SpanContext (generateSpanId/generateTraceId). (`src/Ядро/Модули/ОтелУтилиты.os:57-58`)

- ❌ **[Metrics Api]** [MUST] It MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or `utf8mb3`).  
  Нет явной проверки или ограничения на BMP Unicode. Строки обрабатываются как есть через НормализоватьСтроку(). (-)

- ❌ **[Metrics Api]** [MUST] It MUST support at least 1023 characters.  
  Нет ограничений на длину строки описания. Строка принимается без проверки длины. (-)

- ⚠️ **[Metrics Api]** [MUST] Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set.  
  Callbacks выполняются при сборе, но нет явного механизма предотвращения двойного вызова в течение одного цикла сборки. (`src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160-180`)

- ⚠️ **[Metrics Api]** [MUST] Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added.  
  Метод Включен() не принимает параметры, но можно добавить перегрузку в будущем. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:231`)

- ❌ **[Metrics Sdk]** [MUST] Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow.  
  Implementation does not distinguish between cumulative and delta temporality for overflow handling. All overflow measurements go to single overflow aggregator regardless of temporality (-)

- ⚠️ **[Metrics Sdk]** [MUST NOT] the SDK MUST NOT have overhead related to exemplar sampling  
  Filter check is implemented to skip sampling when disabled, but complete overhead elimination when sampling is off may not be fully implemented throughout all aggregators. (`/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Модули/ОтелФильтрЭкземпляров.os:46`)

- ⚠️ **[Metrics Sdk]** [MUST] This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled.  
  Uses simple replacement (last measurement wins) instead of uniformly-weighted sampling algorithm (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:40-51`)

- ⚠️ **[Propagators]** [MUST] MUST preserve a debug trace flag, if received, and propagate it with subsequent requests.  
  Debug flag is detected during extract ("d" in single-header, X-B3-Flags=1 in multi-header) and causes sampled=1, but is not preserved as debug in SpanContext. Inject never writes debug back (no "d" in single-header, no X-B3-Flags in multi-header), so debug state is lost during propagation. (`src/Пропагация/Классы/ОтелB3Пропагатор.os:139`)

- ⚠️ **[Propagators]** [MUST] MUST default to injecting B3 using the single-header format  
  Constructor defaults to ОтелФорматB3.Мульти() (multi-header) when no format is provided. The spec requires the default to be single-header format. (`src/Пропагация/Классы/ОтелB3Пропагатор.os:203`)

- ⚠️ **[Propagators]** [MUST] Fields MUST return the header names that correspond to the configured format, i.e., the headers used for the inject operation.  
  For single-header format, Fields correctly returns ["b3"]. For multi-header format, Fields returns ["X-B3-TraceId", "X-B3-SpanId", "X-B3-Sampled", "X-B3-ParentSpanId", "X-B3-Flags"] but inject only writes X-B3-TraceId, X-B3-SpanId, X-B3-Sampled. X-B3-ParentSpanId and X-B3-Flags are listed but never used in inject. (`src/Пропагация/Классы/ОтелB3Пропагатор.os:85`)

- ⚠️ **[Env Vars]** [MUST] Values MUST be deduplicated in order to register a Propagator only once.  
  Правильная дедупликация пропагаторов реализована через Соответствие как Set, но используется неправильная переменная окружения - код читает otel.propagators вместо OTEL_PROPAGATORS (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:468-474`)

- ✅ **[Env Vars]** [MUST] When OTEL_CONFIG_FILE is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored.  
  Реализовано в ОтелФайловаяКонфигурация + ОтелПодстановкаПеременных. При наличии OTEL_CONFIG_FILE автоконфигурация делегирует парсинг YAML-файла с подстановкой переменных окружения. (src/Конфигурация/Модули/)

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Baggage Api]** [SHOULD NOT] The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation.  
  КлючBaggage() экспортирован в ПрограммныйИнтерфейс модуля ОтелКонтекст, что даёт пользователям API прямой доступ к ключу контекста. Высокоуровневые методы (BaggageИзКонтекста, КонтекстСBaggage, ТекущийBaggage, СделатьBaggageТекущим) скрывают необходимость в прямом доступе к ключу, но сам ключ доступен. (`src/Ядро/Модули/ОтелКонтекст.os:53`)

- ❌ **[Resource Sdk]** [SHOULD] In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles.  
  Функция РазобратьПарыКлючЗначение и СоздатьРесурс не содержат обработки ошибок декодирования - нет Попытка/Исключение вокруг РаскодироватьСтроку, и при ошибке значение не отбрасывается целиком. (-)

- ❌ **[Resource Sdk]** [SHOULD] In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles.  
  Вторая часть того же предложения (второй SHOULD) - ошибка не логируется и не сообщается при неудачном декодировании переменной OTEL_RESOURCE_ATTRIBUTES. (-)

- ⚠️ **[Trace Api]** [SHOULD NOT] The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation.  
  КлючСпана() экспортирована публично и доступна пользователям API. Высокоуровневые API (СпанИзКонтекста, КонтекстСоСпаном) существуют, но ключ контекста всё равно доступен напрямую. (`src/Ядро/Модули/ОтелКонтекст.os:44`)

- ⚠️ **[Trace Api]** [SHOULD NOT] The API SHOULD NOT expose details about how they are internally stored.  
  Binary getters (ИдТрассировкиВДвоичномВиде, ИдСпанаВДвоичномВиде) return the internal ДвоичныеДанные directly, exposing the internal storage format. However, hex getters convert from internal binary, so partial compliance. (`src/Трассировка/Классы/ОтелКонтекстСпана.os:84`)

- ⚠️ **[Trace Api]** [SHOULD NOT] To prevent misuse, implementations SHOULD NOT provide access to a `Span`'s attributes besides its `SpanContext`.  
  ОтелСпан exposes Атрибуты() as a public export method, providing direct access to span attributes. The spec recommends not exposing attributes besides SpanContext. (`src/Трассировка/Классы/ОтелСпан.os:146`)

- ⚠️ **[Trace Api]** [SHOULD NOT] If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type).  
  ОтелНоопСпан is publicly exposed as a class in lib.config. A factory function (e.g. on Tracer or a module) could hide the class, but it is directly instantiated by consumers. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ⚠️ **[Trace Api]** [SHOULD] If a new type is required to be publicly exposed, it SHOULD be named `NonRecordingSpan`.  
  The class is named ОтелНоопСпан (NoopSpan) instead of the recommended NonRecordingSpan (НеЗаписывающийСпан). (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ⚠️ **[Trace Api]** [SHOULD] Link - Links are immutable and SHOULD be safe for concurrent use by default.  
  Links are stored as plain Соответствие (Map) objects without a dedicated immutable class. They are effectively immutable by convention (never modified after creation), but lack explicit documentation about immutability and thread-safety. (`src/Трассировка/Классы/ОтелСпан.os:384`)

- ❌ **[Trace Api]** [SHOULD] If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly without instantiating a new `Span`.  
  ОтелТрассировщик.НачатьСпан always creates a new ОтелНоопСпан(КонтекстРодителяСпана) when sampling fails, even if the parent span is already a non-recording ОтелНоопСпан. There is no check to return the existing parent span directly. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] After the call to `Shutdown`, subsequent attempts to get a `Tracer` are not allowed. SDKs SHOULD return a valid no-op Tracer for these calls, if possible.  
  After shutdown, ПолучитьТрассировщик returns a regular ОтелТрассировщик (not a no-op). The returned Tracer references the closed Provider and will still attempt to create real spans, allocate memory, and run sampling logic - it is not a true no-op Tracer. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:76`)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Закрыть() is a Процедура (void) - it does not return a success/failure/timeout result. Exceptions propagate on failure, and ЗакрытьАсинхронно() returns a Promise, but there is no explicit result status. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:118`)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Закрыть() has no timeout parameter. ЗакрытьАсинхронно() returns a Promise where the caller can apply a timeout via Получить(Таймаут), but the shutdown method itself does not accept or enforce a timeout. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:118`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() is a Процедура (void) - it does not return a success/failure/timeout result. Exceptions propagate on failure, and СброситьБуферАсинхронно() returns a Promise, but there is no explicit result status. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:109`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  СброситьБуфер() has no timeout parameter. СброситьБуферАсинхронно() returns a Promise where the caller can apply a timeout, but the flush method itself does not accept or enforce a timeout. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:109`)

- ❌ **[Trace Sdk]** [SHOULD NOT] However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set.  
  Процессоры (ОтелПростойПроцессорСпанов, ОтелПакетныйПроцессорСпанов) передают экспортеру все завершенные спаны без проверки флага Sampled. Если пользовательский семплер вернет RECORD_ONLY, экспортер получит спан с Sampled=false. (-)

- ❌ **[Trace Sdk]** [SHOULD NOT] Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not.  
  Процессоры передают экспортеру все завершенные спаны без фильтрации по флагу Sampled. Нет механизма, предотвращающего передачу RECORD_ONLY спанов экспортеру. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values.  
  TraceIDs are generated using UUID v4 (Новый УникальныйИдентификатор()), which provides 122 random bits out of 128. However, UUID v4 has fixed version (4) and variant (10xx) bits baked into the output, so the rightmost 7 bytes do not contain a full 56 bits of randomness as required by W3C Trace Context Level 2. The implementation provides practical randomness but does not specifically target the W3C TC L2 bit-layout requirements. (`src/Ядро/Модули/ОтелУтилиты.os:78-92`)

- ❌ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements.  
  The ВычислитьФлагиТрассировки() method in ОтелТрассировщик.os (line 247) only sets the Sampled flag (bit 0, value 0 or 1) based on sampling result. The Random flag (bit 1, value 0x02 per W3C TC Level 2) is never set on generated TraceIDs. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the `rv` sub-key of the OpenTelemetry TraceState.  
  Семплер ПоДолеТрассировок использует первые 8 символов TraceId для вычисления хеша и предполагает равномерное распределение (W3C Level 2 randomness), но нет проверки подключа 'rv' в TraceState для explicit randomness. (`src/Трассировка/Модули/ОтелСэмплер.os:290-298`)

- ❌ **[Trace Sdk]** [SHOULD] If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated.  
  Хотя SDK поддерживает пользовательские IdGenerator через УстановитьГенераторИд(), нет механизма для указания или проверки Random flag в TraceContext. Интерфейс IdGenerator не предусматривает метод для определения random flag. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`.  
  Конфигурационные опции названы МаксСобытий/МаксЛинков (не EventCountLimit/LinkCountLimit), что является корректным переводом на русский язык, но не точно соответствует указанным в спецификации именам. (`src/Трассировка/Классы/ОтелЛимитыСпана.os:34-44`)

- ⚠️ **[Trace Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Параметр ТаймаутМс принимается, но простой процессор не использует его - вызов Экспортер.Закрыть() не ограничен таймаутом. Пакетный процессор корректно учитывает таймаут через ЭкспортироватьВсеПакеты (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:77`)

- ⚠️ **[Trace Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() определена как Процедура (void) без возвращаемого значения - вызывающий код не может программно узнать результат (успех/ошибка/таймаут). Об ошибке можно узнать только по исключению. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:44`)

- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD complete or abort within some timeout.  
  Timeout is supported at processor level but not exposed at LoggerProvider.Закрыть() level - only async version supports timeout via Promise (`src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:81`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD return some ERROR status if there is an error condition  
  Synchronous method returns void, only async method can return status via Promise. Error handling is implicit through exception propagation. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:113`)

- ⚠️ **[Logs Sdk]** [SHOULD] and if there is no error condition, it SHOULD return some NO ERROR status  
  Synchronous method returns void, only async method can return status via Promise. Success is implicit through normal completion. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:113`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  Timeout is supported at processor level but not exposed at LoggerProvider.СброситьБуфер() level - only async version supports timeout via Promise (`src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:61`)

- ⚠️ **[Metrics Api]** [SHOULD] If possible, the API SHOULD be structured so a user is obligated to provide this parameter.  
  Имя обязательный первый параметр, но технически можно передать пустую строку без проверки. (`src/Метрики/Классы/ОтелМетр.os:51`)

- ⚠️ **[Metrics Api]** [SHOULD] If possible, the API SHOULD be structured so a user is obligated to provide this parameter.  
  Имя обязательный первый параметр, но технически можно передать пустую строку без проверки. (`src/Метрики/Классы/ОтелМетр.os:242`)

- ⚠️ **[Metrics Api]** [SHOULD] If possible, this API SHOULD be structured so a user is obligated to provide this parameter.  
  Параметр Значение обязательный, но может быть 0 или отрицательным (игнорируется). (`src/Метрики/Классы/ОтелСчетчик.os:21`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD provide some way to pass `state` to the callback.  
  Callbacks are created as lambda functions that can capture closure variables, but there's no explicit state parameter mechanism provided by the API (-)

- ⚠️ **[Metrics Api]** [SHOULD] This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative.  
  Documentation doesn't explicitly state non-negative expectation for histogram values (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Асинхронная версия возвращает Обещание, но синхронная версия не возвращает статус (`src/Метрики/Классы/ОтелПровайдерМетрик.os:177`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `Shutdown` SHOULD complete or abort within some timeout.  
  Таймаут реализован только в асинхронной версии через библиотеку async (`src/Метрики/Классы/ОтелПровайдерМетрик.os:177`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Асинхронная версия возвращает Обещание, но синхронная версия не возвращает статус (`src/Метрики/Классы/ОтелПровайдерМетрик.os:165`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  Статус ошибки реализован только в асинхронной версии через исключения в Обещании (`src/Метрики/Классы/ОтелПровайдерМетрик.os:165`)

- ⚠️ **[Metrics Sdk]** [SHOULD] `ForceFlush` SHOULD complete or abort within some timeout.  
  Таймаут реализован только в асинхронной версии через библиотеку async (`src/Метрики/Классы/ОтелПровайдерМетрик.os:165`)

- ⚠️ **[Metrics Sdk]** [SHOULD] The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks.  
  No validation to disregard asynchronous instrument API usage outside of registered callbacks (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback execution.  
  No timeout mechanism implemented for callback execution (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardinality_limit` value defined for the stream, that value SHOULD be used.  
  ОтелПредставление has ЛимитМощностиАгрегации field but it is not applied to instruments in ПрименитьПредставлениеКИнструменту method (`src/Метрики/Классы/ОтелПредставление.os:92`)

- ⚠️ **[Metrics Sdk]** [SHOULD] If there is no matching view, but the `MetricReader` defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used.  
  MetricReader has ЛимитМощности method returning default 2000, but this is not applied to instruments when no View is matched (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:151`)

- ❌ **[Metrics Sdk]** [SHOULD] Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality.  
  Asynchronous instruments (ОтелБазовыйНаблюдаемыйИнструмент) do not implement cardinality limits. They collect all observations from callbacks without overflow handling (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning.  
  Warning is always emitted for descriptor conflicts. There is no check if View corrects the description conflict to suppress the warning (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning.  
  Warning message does not include renaming View recipe. It only shows the conflicting parameters without suggesting View-based solution (-)

- ❌ **[Metrics Sdk]** [SHOULD] Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument registration.  
  SDK returns the first registered instrument, not both Metric objects. No data pass-through for conflicting instruments with different units (-)

- ❌ **[Metrics Sdk]** [SHOULD] it SHOULD validate the instrument name conforms to the instrument name syntax  
  No name validation is implemented in any instrument creation methods. Names are only normalized via НРег() but not validated for syntax conformance. (-)

- ❌ **[Metrics Sdk]** [SHOULD] the Meter SHOULD emit an error notifying the user about the invalid name  
  No error logging for invalid names since name validation itself is not implemented. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] The ExemplarReservoir SHOULD avoid allocations when sampling exemplars.  
  Algorithm R implementation allocates arrays but this is standard practice for reservoir sampling (-)

- ❌ **[Metrics Sdk]** [SHOULD] Explicit bucket histogram aggregation with more than 1 bucket SHOULD use AlignedHistogramBucketExemplarReservoir.  
  No automatic assignment of reservoir type based on aggregation configuration found (-)

- ❌ **[Metrics Sdk]** [SHOULD] Base2 Exponential Histogram Aggregation SHOULD use a SimpleFixedSizeExemplarReservoir with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty.  
  No automatic assignment of reservoir type for exponential histograms found (-)

- ❌ **[Metrics Sdk]** [SHOULD] All other aggregations SHOULD use SimpleFixedSizeExemplarReservoir.  
  No automatic assignment of reservoir type based on aggregation type found (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled.  
  Uses simple replacement (last measurement wins) instead of uniformly-weighted sampling algorithm (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:40-51`)

- ❌ **[Metrics Sdk]** [SHOULD] Collect SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Collect methods do not provide failure/timeout return values - they handle errors internally with logging (-)

- ❌ **[Metrics Sdk]** [SHOULD] SDKs SHOULD return some failure for these calls, if possible.  
  СброситьБуфер() (Collect) is a void procedure with no guard checking Закрыт flag after shutdown. No failure is returned to the caller for Collect calls after shutdown. (-)

- ❌ **[Metrics Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Закрыть() is a void procedure. All exceptions (timeout, exporter close errors) are caught internally and only logged, never propagated to the caller. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD collect metrics, call Export(batch) and ForceFlush() on the configured Push Metric Exporter.  
  СброситьБуфер() calls СобратьИЭкспортировать() which collects metrics and calls Экспортер.Экспортировать(). However, it does not call Экспортер.СброситьБуфер() (ForceFlush on the exporter). (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94`)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() is a void procedure (Процедура). There is no return value or mechanism to communicate success, failure, or timeout to the caller. (-)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR.  
  СброситьБуфер() is a void procedure. Errors during collection and export are caught internally (try/catch in СобратьИЭкспортировать) and only logged, never returned to the caller. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() has no explicit timeout parameter. It relies on the underlying transport timeout (10 seconds for HTTP). There is no configurable ForceFlush timeout at the reader level. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94`)

- ❌ **[Metrics Sdk]** [SHOULD] Metric Exporters SHOULD report an error condition for data output by the MetricReader with unsupported Aggregation or Aggregation Temporality, as this condition can be corrected by a change of MetricReader configuration.  
  ОтелЭкспортерМетрик.Экспортировать() does not validate or report unsupported Aggregation or Aggregation Temporality. No error reporting exists for this condition. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD NOT] The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the metrics are being sent to.  
  ОтелHttpТранспорт implements retry with exponential backoff (СтратегияПовтора) for HTTP 429, 502, 503, 504. Retry is in the protocol-specific transport, not the exporter itself, which partially aligns with the spec's reasoning about protocol-dependent retry, but the SDK does ship with built-in retry. (`src/Экспорт/Классы/ОтелHttpТранспорт.os:76`)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() on the exporter is a void procedure (Процедура). No return value or mechanism to communicate success, failure, or timeout. (-)

- ❌ **[Metrics Sdk]** [SHOULD] MetricProducer implementations SHOULD accept configuration for the AggregationTemporality of produced metrics.  
  ИнтерфейсПродюсерМетрик.Произвести() accepts only ФильтрМетрик parameter. There is no mechanism to configure AggregationTemporality for MetricProducer implementations. (-)

- ❌ **[Otlp Exporter]** [SHOULD] If the gRPC client implementation does not support an endpoint with a scheme of `http` or `https` then the endpoint SHOULD be transformed to the most sensible format for that implementation.  
  gRPC transport uses OPI_GRPC library which handles URL formats internally, but no explicit transformation logic found in the codebase (-)

- ❌ **[Otlp Exporter]** [SHOULD] they SHOULD continue to be supported as they were part of a stable release of the specification.  
  Obsolete environment variables OTEL_EXPORTER_OTLP_SPAN_INSECURE and OTEL_EXPORTER_OTLP_METRIC_INSECURE are not supported in the codebase (-)

- ❌ **[Otlp Exporter]** [SHOULD] The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default.  
  Default protocol is set to "http/json" instead of "http/protobuf" as required by spec (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:168`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If they support only one, it SHOULD be `http/protobuf`.  
  SDK supports grpc and http/json, but not http/protobuf specifically (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563-571`)

- ❌ **[Otlp Exporter]** [SHOULD] If no configuration is provided the default transport SHOULD be `http/protobuf` unless SDKs have good reasons to choose `grpc` as the default.  
  Default protocol is "http/json" instead of "http/protobuf" as recommended (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:168`)

- ❌ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter.  
  No User-Agent header implementation found in HTTP or gRPC transports (-)

- ❌ **[Otlp Exporter]** [SHOULD] The format of the header SHOULD follow RFC 7231.  
  No User-Agent header implementation found in HTTP or gRPC transports (-)

- ❌ **[Otlp Exporter]** [SHOULD] The resulting User-Agent SHOULD include the exporter's default User-Agent string.  
  No User-Agent header implementation found in HTTP or gRPC transports (-)

- ❌ **[Env Vars]** [SHOULD] If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied.  
  Boolean parsing only checks НРег(Значение) = "true" without logging warnings for invalid values like "maybe" or "yes". No БезопасныйБулев function exists. (-)

- ❌ **[Env Vars]** [SHOULD] It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations.  
  Код не поддерживает deprecated значение "logging" для экспортеров - только "otlp", "console" и "none". Это соответствует рекомендации не поддерживать deprecated значения в новых реализациях. (-)

- ❌ **[Env Vars]** [SHOULD] It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations.  
  Код не поддерживает deprecated значение "logging" для метрик экспортера - только "otlp" и "none". Это соответствует рекомендации не поддерживать deprecated значения в новых реализациях. (-)

- ❌ **[Env Vars]** [SHOULD] It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations.  
  Код не поддерживает deprecated значение "logging" для логов экспортера - только "otlp" и "none". Это соответствует рекомендации не поддерживать deprecated значения в новых реализациях. (-)

## Детальный анализ по разделам (Stable)

### Context

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:5` |  |
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
| 13 | MUST | ✅ found | The API MUST accept the following parameters: * The `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:246` |  |
| 14 | MUST | ✅ found | The API MUST return a value that can be used as a `Token` to restore the previous `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:252` |  |

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
| 1 | MUST | ✅ found | Each name in `Baggage` MUST be associated with exactly one value. | `src/Ядро/Классы/ОтелПостроительBaggage.os:24` |  |
| 2 | SHOULD NOT | ✅ found | Language API SHOULD NOT restrict which strings are used as baggage names. | `src/Ядро/Классы/ОтелПостроительBaggage.os:23` |  |
| 3 | MUST | ✅ found | Language API MUST accept any valid UTF-8 string as baggage value in `Set` and return the same value from `Get`. | `src/Ядро/Классы/ОтелBaggage.os:38` |  |
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
| 11 | MUST | ✅ found | If an implementation of this API does not operate directly on the Context, it MUST provide the following functionality to interact with a Context instance: | `src/Ядро/Модули/ОтелКонтекст.os:156` |  |
| 12 | SHOULD NOT | ⚠️ partial | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:53` | КлючBaggage() экспортирован в ПрограммныйИнтерфейс модуля ОтелКонтекст, что даёт пользователям API прямой доступ к ключу контекста. Высокоуровневые методы (BaggageИзКонтекста, КонтекстСBaggage, ТекущийBaggage, СделатьBaggageТекущим) скрывают необходимость в прямом доступе к ключу, но сам ключ доступен. |
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
| 17 | MUST | ✅ found | If a new name/value pair is added and its name is the same as an existing name, then the new pair MUST take precedence. | `src/Ядро/Классы/ОтелПостроительBaggage.os:24` |  |

### Resource Sdk

#### Resource SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The SDK MUST allow for creation of `Resources` and for associating them with telemetry. | `src/Ядро/Классы/ОтелРесурс.os:99` |  |
| 2 | MUST | ✅ found | all `Span`s produced by any `Tracer` from the provider MUST be associated with this `Resource`. | `src/Трассировка/Классы/ОтелТрассировщик.os:95` |  |

#### SDK-provided resource attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#sdk-provided-resource-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The SDK MUST provide access to a Resource with at least the attributes listed at Semantic Attributes with SDK-provided Default Value. | `src/Ядро/Классы/ОтелРесурс.os:107` |  |
| 4 | MUST | ✅ found | This resource MUST be associated with a `TracerProvider` or `MeterProvider` if another resource was not explicitly specified. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:324` |  |

#### Create

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#create)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The interface MUST provide a way to create a new resource, from `Attributes`. | `src/Ядро/Классы/ОтелРесурс.os:99` |  |

#### Merge

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#merge)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | The interface MUST provide a way for an old resource and an updating resource to be merged into a new resource. | `src/Ядро/Классы/ОтелРесурс.os:41` |  |
| 7 | MUST | ✅ found | The resulting resource MUST have all attributes that are on any of the two input resources. | `src/Ядро/Классы/ОтелРесурс.os:58` |  |
| 8 | MUST | ✅ found | If a key exists on both the old and updating resource, the value of the updating resource MUST be picked (even if the updated value is empty). | `src/Ядро/Классы/ОтелРесурс.os:61` |  |

#### Detecting resource information from the environment

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#detecting-resource-information-from-the-environment)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ⚠️ partial | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1` | Детекторы реализованы как отдельные классы (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора), но они находятся внутри того же пакета SDK (зарегистрированы в lib.config), а не в отдельных пакетах. |
| 10 | MUST | ✅ found | Resource detector packages MUST provide a method that returns a resource. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17` |  |
| 11 | MUST NOT | ✅ found | failure to detect any resource information MUST NOT be considered an error, | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:20` |  |
| 12 | SHOULD | ✅ found | whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:24` |  |
| 13 | MUST | ✅ found | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18` |  |
| 14 | SHOULD | ✅ found | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate (e.g. the detector that reads the attributes from environment values will not know what Schema URL to use). | `src/Ядро/Классы/ОтелРесурс.os:99` |  |
| 15 | MUST | ✅ found | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources. | `src/Ядро/Классы/ОтелРесурс.os:43` |  |

#### Specifying resource information via an environment variable

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#specifying-resource-information-via-an-environment-variable)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge this, as the secondary resource, with any resource information provided by the user, i.e. the user provided resource information has higher priority. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:122` |  |
| 17 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:693` |  |
| 18 | MUST | ✅ found | The `,` and `=` characters in keys and values MUST be percent encoded. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:694` |  |
| 19 | SHOULD | ❌ not_found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | - | Функция РазобратьПарыКлючЗначение и СоздатьРесурс не содержат обработки ошибок декодирования - нет Попытка/Исключение вокруг РаскодироватьСтроку, и при ошибке значение не отбрасывается целиком. |
| 20 | SHOULD | ❌ not_found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | - | Вторая часть того же предложения (второй SHOULD) - ошибка не логируется и не сообщается при неудачном декодировании переменной OTEL_RESOURCE_ATTRIBUTES. |

### Trace Api

#### TracerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `TracerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:31` |  |
| 2 | SHOULD | ✅ found | Thus, implementations of `TracerProvider` SHOULD allow creating an arbitrary number of `TracerProvider` instances. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:313` |  |

#### TracerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The `TracerProvider` MUST provide the following functions: * Get a `Tracer` | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:63` |  |

#### Get a Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-a-tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:63` |  |
| 5 | SHOULD | ✅ found | This name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library (e.g. `io.opentelemetry.contrib.mongodb`), package, module or class name. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:63` |  |
| 6 | MUST | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:68` |  |
| 7 | SHOULD | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:71` |  |
| 8 | SHOULD | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:69` |  |
| 9 | MUST NOT | ✅ found | Implementations MUST NOT require users to repeatedly obtain a `Tracer` again with the same identity to pick up configuration changes. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:154` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API MUST provide the following functionality to interact with a `Context` instance: | `src/Ядро/Модули/ОтелКонтекст.os:141` |  |
| 11 | SHOULD NOT | ⚠️ partial | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:44` | КлючСпана() экспортирована публично и доступна пользователям API. Высокоуровневые API (СпанИзКонтекста, КонтекстСоСпаном) существуют, но ключ контекста всё равно доступен напрямую. |
| 12 | SHOULD | ✅ found | If the language has support for implicitly propagated `Context` (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Модули/ОтелКонтекст.os:90` |  |
| 13 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### Tracer operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracer-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The `Tracer` MUST provide functions to: * Create a new `Span` | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
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
| 21 | MUST | ✅ found | Hex - returns the lowercase hex encoded `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 22 | MUST | ✅ found | Hex - returns the lowercase hex encoded `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` (result MUST be a 16-hex-character lowercase string). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:32` |  |
| 23 | MUST | ✅ found | Binary - returns the binary representation of the `TraceId` (result MUST be a 16-byte array) or `SpanId` | `src/Трассировка/Классы/ОтелКонтекстСпана.os:84` |  |
| 24 | MUST | ✅ found | Binary - returns the binary representation of the `TraceId` (result MUST be a 16-byte array) or `SpanId` (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:93` |  |
| 25 | SHOULD NOT | ⚠️ partial | The API SHOULD NOT expose details about how they are internally stored. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:84` | Binary getters (ИдТрассировкиВДвоичномВиде, ИдСпанаВДвоичномВиде) return the internal ДвоичныеДанные directly, exposing the internal storage format. However, hex getters convert from internal binary, so partial compliance. |

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
| 29 | MUST | ✅ found | When extracting a `SpanContext` through the Propagators API, `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:256` |  |

#### TraceState

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracestate)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | Tracing API MUST provide at least the following operations on `TraceState`: | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:44` |  |
| 31 | MUST | ✅ found | These operations MUST follow the rules described in the W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:227` |  |
| 32 | MUST | ✅ found | All mutating operations MUST return a new `TraceState` with the modifications applied. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:92` |  |
| 33 | MUST | ✅ found | `TraceState` MUST at all times be valid according to rules specified in W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:220` |  |
| 34 | MUST | ✅ found | Every mutating operations MUST validate input parameters. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 35 | MUST NOT | ✅ found | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 36 | MUST | ✅ found | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data and MUST follow the general error handling guidelines. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:68` |  |

#### Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | SHOULD | ✅ found | The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable. | - |  |
| 38 | SHOULD | ✅ found | Generality SHOULD be prioritized over human-readability. | - |  |
| 39 | SHOULD | ✅ found | A `Span`'s start time SHOULD be set to the current time on span creation. | `src/Трассировка/Классы/ОтелСпан.os:632` |  |
| 40 | SHOULD | ✅ found | After the `Span` is created, it SHOULD be possible to change its name, set its `Attribute`s, add `Event`s, and set the `Status`. | `src/Трассировка/Классы/ОтелСпан.os:259` |  |
| 41 | MUST NOT | ✅ found | These MUST NOT be changed after the `Span`'s end time has been set. | `src/Трассировка/Классы/ОтелСпан.os:260` |  |
| 42 | SHOULD NOT | ⚠️ partial | To prevent misuse, implementations SHOULD NOT provide access to a `Span`'s attributes besides its `SpanContext`. | `src/Трассировка/Классы/ОтелСпан.os:146` | ОтелСпан exposes Атрибуты() as a public export method, providing direct access to span attributes. The spec recommends not exposing attributes besides SpanContext. |
| 43 | MUST NOT | ✅ found | However, alternative implementations MUST NOT allow callers to create `Span`s directly. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 44 | MUST | ✅ found | All `Span`s MUST be created via a `Tracer`. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |

#### Span Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST NOT | ✅ found | There MUST NOT be any API for creating a `Span` other than with a `Tracer`. | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |
| 46 | MUST NOT | ✅ found | In languages with implicit `Context` propagation, `Span` creation MUST NOT set the newly created `Span` as the active `Span` in the current `Context` by default, but this functionality MAY be offered additionally as a separate operation. | `src/Трассировка/Классы/ОтелСпан.os:410` |  |
| 47 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПостроительСпана.os:192` |  |
| 48 | MUST NOT | ✅ found | This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`. | `src/Трассировка/Классы/ОтелПостроительСпана.os:33` |  |
| 49 | MUST | ✅ found | The semantic parent of the Span MUST be determined according to the rules described in Determining the Parent Span from a Context. | `src/Трассировка/Классы/ОтелТрассировщик.os:60` |  |
| 50 | MUST | ✅ found | The API documentation MUST state that adding attributes at span creation is preferred to calling `SetAttribute` later, as samplers can only consider information already present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os:71` |  |
| 51 | SHOULD | ✅ found | `Start timestamp`, default to current time. This argument SHOULD only be set when span creation time has already passed. | `src/Трассировка/Классы/ОтелПостроительСпана.os:114` |  |
| 52 | MUST NOT | ✅ found | If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument. | `src/Трассировка/Классы/ОтелПостроительСпана.os:114` |  |
| 53 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span, and MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:118` |  |
| 54 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span, and MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:122` |  |
| 55 | MUST | ✅ found | For a Span with a parent, the `TraceId` MUST be the same as the parent. | `src/Трассировка/Классы/ОтелТрассировщик.os:64` |  |
| 56 | MUST | ✅ found | Also, the child span MUST inherit all `TraceState` values of its parent by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:264` |  |
| 57 | MUST | ✅ found | Any span that is created MUST also be ended. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |

#### Specifying links

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#specifying-links)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 58 | MUST | ✅ found | During `Span` creation, a user MUST have the ability to record links to other `Span`s. | `src/Трассировка/Классы/ОтелПостроительСпана.os:97` |  |

#### Get Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | MUST | ✅ found | The Span interface MUST provide: | `src/Трассировка/Классы/ОтелСпан.os:80` |  |
| 60 | MUST | ✅ found | The returned value MUST be the same for the entire Span lifetime. | `src/Трассировка/Классы/ОтелСпан.os:80` |  |

#### IsRecording

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isrecording)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:247` |  |
| 62 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:247` |  |
| 63 | SHOULD NOT | ✅ found | `IsRecording` SHOULD NOT take any parameters. | `src/Трассировка/Классы/ОтелСпан.os:246` |  |
| 64 | SHOULD | ✅ found | This flag SHOULD be used to avoid expensive computations of a Span attributes or events in case when a Span is definitely not recorded. | `src/Трассировка/Классы/ОтелСпан.os:246` |  |

#### Set Attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | MUST | ✅ found | A `Span` MUST have the ability to set `Attributes` associated with it. | `src/Трассировка/Классы/ОтелСпан.os:275` |  |
| 66 | MUST | ✅ found | The Span interface MUST provide: | `src/Трассировка/Классы/ОтелСпан.os:275` |  |
| 67 | SHOULD | ✅ found | Setting an attribute with the same key as an existing attribute SHOULD overwrite the existing attribute's value. | `src/Трассировка/Классы/ОтелСпан.os:290` |  |

#### Add Events

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-events)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | MUST | ✅ found | A `Span` MUST have the ability to add events. | `src/Трассировка/Классы/ОтелСпан.os:305` |  |
| 69 | MUST | ✅ found | The Span interface MUST provide: | `src/Трассировка/Классы/ОтелСпан.os:305` |  |
| 70 | SHOULD | ✅ found | Events SHOULD preserve the order in which they are recorded. | `src/Трассировка/Классы/ОтелСпан.os:309` |  |

#### Add Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | MUST | ✅ found | A `Span` MUST have the ability to add `Link`s associated with it after its creation - see Links. | `src/Трассировка/Классы/ОтелСпан.os:373` |  |

#### Set Status

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-status)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST | ✅ found | `Description` MUST only be used with the `Error` `StatusCode` value. | `src/Трассировка/Классы/ОтелСпан.os:441` |  |
| 73 | MUST | ✅ found | The Span interface MUST provide: | `src/Трассировка/Классы/ОтелСпан.os:425` |  |
| 74 | SHOULD | ✅ found | An API to set the `Status`. This SHOULD be called `SetStatus`. | `src/Трассировка/Классы/ОтелСпан.os:425` |  |
| 75 | MUST | ✅ found | `Description` MUST be IGNORED for `StatusCode` `Ok` & `Unset` values. | `src/Трассировка/Классы/ОтелСпан.os:441` |  |
| 76 | SHOULD | ✅ found | The status code SHOULD remain unset, except for the following circumstances: | `src/Трассировка/Классы/ОтелСпан.os:637` |  |
| 77 | SHOULD | ✅ found | An attempt to set value `Unset` SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:436` |  |
| 78 | SHOULD | ✅ found | When the status is set to `Error` by Instrumentation Libraries, the `Description` SHOULD be documented and predictable. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 79 | SHOULD | ✅ found | For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish their own conventions, including possible values of `Description` and what they mean. | `src/Трассировка/Классы/ОтелСпан.os:419` |  |
| 80 | SHOULD NOT | ✅ found | Generally, Instrumentation Libraries SHOULD NOT set the status code to `Ok`, unless explicitly configured to do so. | `src/Трассировка/Классы/ОтелСпан.os:425` |  |
| 81 | SHOULD | ✅ found | Instrumentation Libraries SHOULD leave the status code as `Unset` unless there is an error, as described above. | `src/Трассировка/Классы/ОтелСпан.os:637` |  |
| 82 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:431` |  |
| 83 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:431` |  |
| 84 | SHOULD | ✅ found | Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they would otherwise generate. | `src/Трассировка/Классы/ОтелСпан.os:425` |  |

#### End

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#end)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 85 | SHOULD | ✅ found | Implementations SHOULD ignore all subsequent calls to `End` and any other Span methods, i.e. the Span becomes non-recording by being ended (there might be exceptions when Tracer is streaming events and has no mutable state associated with the `Span`). | `src/Трассировка/Классы/ОтелСпан.os:460` |  |
| 86 | MUST | ✅ found | However, all API implementations of such methods MUST internally call the `End` method and be documented to do so. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |
| 87 | MUST NOT | ✅ found | `End` MUST NOT have any effects on child spans. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |
| 88 | MUST NOT | ✅ found | `End` MUST NOT inactivate the `Span` in any `Context` it is active in. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |
| 89 | MUST | ✅ found | It MUST still be possible to use an ended span as parent via a Context it is contained in. | `src/Трассировка/Классы/ОтелСпан.os:80` |  |
| 90 | MUST | ✅ found | Also, any mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:410` |  |
| 91 | MUST | ✅ found | If omitted, this MUST be treated equivalent to passing the current time. | `src/Трассировка/Классы/ОтелСпан.os:462` |  |
| 92 | MUST NOT | ⚠️ partial | This operation itself MUST NOT perform blocking I/O on the calling thread. | `src/Трассировка/Классы/ОтелСпан.os:459` | End() вызывает Процессор.ПриЗавершении(), а SimpleSpanProcessor синхронно вызывает Экспортер.Экспортировать(), что может выполнять блокирующий HTTP-запрос. BatchSpanProcessor не блокирует. Спецификация допускает это для отладочных процессоров, но сам End() формально не гарантирует отсутствие блокирующего I/O. |
| 93 | SHOULD | ✅ found | Any locking used needs be minimized and SHOULD be removed entirely if possible. | `src/Трассировка/Классы/ОтелСпан.os:459` |  |

#### Record Exception

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#record-exception)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 94 | SHOULD | ✅ found | To facilitate recording an exception languages SHOULD provide a `RecordException` method if the language uses exceptions. | `src/Трассировка/Классы/ОтелСпан.os:329` |  |
| 95 | MUST | ✅ found | The method MUST record an exception as an `Event` with the conventions outlined in the exceptions document. | `src/Трассировка/Классы/ОтелСпан.os:358` |  |
| 96 | SHOULD | ✅ found | The minimum required argument SHOULD be no more than only an exception object. | `src/Трассировка/Классы/ОтелСпан.os:329` |  |
| 97 | MUST | ✅ found | If `RecordException` is provided, the method MUST accept an optional parameter to provide any additional event attributes | `src/Трассировка/Классы/ОтелСпан.os:329` |  |
| 98 | SHOULD | ✅ found | (this SHOULD be done in the same way as for the `AddEvent` method). | `src/Трассировка/Классы/ОтелСпан.os:352` |  |

#### Span lifetime

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-lifetime)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 99 | MUST | ✅ found | Start and end time as well as Event's timestamps MUST be recorded at a time of a calling of corresponding API. | `src/Трассировка/Классы/ОтелСпан.os:632` |  |

#### Wrapping a SpanContext in a Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#wrapping-a-spancontext-in-a-span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 100 | MUST | ✅ found | The API MUST provide an operation for wrapping a `SpanContext` with an object implementing the `Span` interface. | `src/Трассировка/Классы/ОтелНоопСпан.os:272` |  |
| 101 | SHOULD NOT | ⚠️ partial | If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type). | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | ОтелНоопСпан is publicly exposed as a class in lib.config. A factory function (e.g. on Tracer or a module) could hide the class, but it is directly instantiated by consumers. |
| 102 | SHOULD | ⚠️ partial | If a new type is required to be publicly exposed, it SHOULD be named `NonRecordingSpan`. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | The class is named ОтелНоопСпан (NoopSpan) instead of the recommended NonRecordingSpan (НеЗаписывающийСпан). |
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
| 110 | MUST | ✅ found | A user MUST have the ability to record links to other `SpanContext`s. | `src/Трассировка/Классы/ОтелСпан.os:373` |  |
| 111 | MUST | ✅ found | The API MUST provide: An API to record a single `Link` where the `Link` properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:373` |  |
| 112 | SHOULD | ✅ found | Implementations SHOULD record links containing `SpanContext` with empty `TraceId` or `SpanId` (all zeros) as long as either the attribute set or `TraceState` is non-empty. | `src/Трассировка/Классы/ОтелСпан.os:373` |  |
| 113 | SHOULD | ✅ found | Span SHOULD preserve the order in which `Link`s are set. | `src/Трассировка/Классы/ОтелСпан.os:636` |  |
| 114 | MUST | ✅ found | The API documentation MUST state that adding links at span creation is preferred to calling `AddLink` later, for contexts that are available during span creation, because head sampling decisions can only consider information present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os:87` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 115 | MUST | ✅ found | TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:7` |  |
| 116 | MUST | ✅ found | Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:3` |  |
| 117 | MUST | ✅ found | Span - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:3` |  |
| 118 | MUST | ✅ found | Event - Events are immutable and MUST be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСобытиеСпана.os:3` |  |
| 119 | SHOULD | ⚠️ partial | Link - Links are immutable and SHOULD be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:384` | Links are stored as plain Соответствие (Map) objects without a dedicated immutable class. They are effectively immutable by convention (never modified after creation), but lack explicit documentation about immutability and thread-safety. |

#### Behavior of the API in the absence of an installed SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#behavior-of-the-api-in-the-absence-of-an-installed-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 120 | MUST | ✅ found | The API MUST return a non-recording `Span` with the `SpanContext` in the parent `Context` (whether explicitly given or implicit current). | `src/Трассировка/Классы/ОтелТрассировщик.os:82` |  |
| 121 | SHOULD | ❌ not_found | If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly without instantiating a new `Span`. | - | ОтелТрассировщик.НачатьСпан always creates a new ОтелНоопСпан(КонтекстРодителяСпана) when sampling fails, even if the parent span is already a non-recording ОтелНоопСпан. There is no check to return the existing parent span directly. |
| 122 | MUST | ✅ found | If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.e., having a `SpanContext` with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags). | `src/Трассировка/Классы/ОтелНоопСпан.os:277` |  |

### Trace Sdk

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, `Sampler`, and (Development) TracerConfigurator) MUST be owned by the `TracerProvider`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:12` |  |
| 2 | MUST | ✅ found | the updated configuration MUST also apply to all already returned `Tracers` (i.e. it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvider` before or after the configuration change). | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |
| 3 | MUST NOT | ✅ found | the updated configuration MUST also apply to all already returned `Tracers` (i.e. it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvider` before or after the configuration change). | `src/Трассировка/Классы/ОтелТрассировщик.os:9` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | `Shutdown` MUST be called only once for each `TracerProvider` instance. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:119` |  |
| 5 | SHOULD | ⚠️ partial | After the call to `Shutdown`, subsequent attempts to get a `Tracer` are not allowed. SDKs SHOULD return a valid no-op Tracer for these calls, if possible. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:76` | After shutdown, ПолучитьТрассировщик returns a regular ОтелТрассировщик (not a no-op). The returned Tracer references the closed Provider and will still attempt to create real spans, allocate memory, and run sampling logic - it is not a true no-op Tracer. |
| 6 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:118` | Закрыть() is a Процедура (void) - it does not return a success/failure/timeout result. Exceptions propagate on failure, and ЗакрытьАсинхронно() returns a Promise, but there is no explicit result status. |
| 7 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:118` | Закрыть() has no timeout parameter. ЗакрытьАсинхронно() returns a Promise where the caller can apply a timeout via Получить(Таймаут), but the shutdown method itself does not accept or enforce a timeout. |
| 8 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:122` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:109` | СброситьБуфер() is a Процедура (void) - it does not return a success/failure/timeout result. Exceptions propagate on failure, and СброситьБуферАсинхронно() returns a Promise, but there is no explicit result status. |
| 10 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:109` | СброситьБуфер() has no timeout parameter. СброситьБуферАсинхронно() returns a Promise where the caller can apply a timeout, but the flush method itself does not accept or enforce a timeout. |
| 11 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered `SpanProcessors`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:110` |  |

#### Additional Span Interfaces

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#additional-span-interfaces)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | A function receiving this as argument MUST be able to access all information that was added to the span, as listed in the API spec for Span. | `src/Трассировка/Классы/ОтелСпан.os:71` |  |
| 13 | MUST | ✅ found | A function receiving this as argument MUST be able to access the `InstrumentationScope` [since 1.10.0] and `Resource` information (implicitly) associated with the span. | `src/Трассировка/Классы/ОтелСпан.os:173` |  |
| 14 | MUST | ⚠️ partial | For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated since 1.10.0] having the same name and version values as the `InstrumentationScope`. | `src/Трассировка/Классы/ОтелСпан.os:182` | InstrumentationScope is accessible via ОбластьИнструментирования() and contains the same name/version data, but there is no explicit InstrumentationLibrary type or accessor alias for backwards compatibility. |
| 15 | MUST | ✅ found | A function receiving this as argument MUST be able to reliably determine whether the Span has ended | `src/Трассировка/Классы/ОтелСпан.os:209` |  |
| 16 | MUST | ✅ found | Counts for attributes, events and links dropped due to collection limits MUST be available for exporters to report as described in the exporters specification. | `src/Трассировка/Классы/ОтелСпан.os:218` |  |
| 17 | MUST | ✅ found | implementations MAY choose not to expose (and store) the full parent Context of the Span but they MUST expose at least the full parent SpanContext. | `src/Трассировка/Классы/ОтелСпан.os:101` |  |
| 18 | MUST | ✅ found | It MUST be possible for functions being called with this to somehow obtain the same `Span` instance and type that the span creation API returned (or will return) to the user | `src/Трассировка/Классы/ОтелСпан.os:467` |  |

#### Sampling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | Span Processor MUST receive only those spans which have this field set to `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:79` |  |
| 20 | SHOULD NOT | ❌ not_found | However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set. | - | Процессоры (ОтелПростойПроцессорСпанов, ОтелПакетныйПроцессорСпанов) передают экспортеру все завершенные спаны без проверки флага Sampled. Если пользовательский семплер вернет RECORD_ONLY, экспортер получит спан с Sampled=false. |
| 21 | MUST | ✅ found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:42` |  |
| 22 | SHOULD NOT | ❌ not_found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | - | Процессоры передают экспортеру все завершенные спаны без фильтрации по флагу Sampled. Нет механизма, предотвращающего передачу RECORD_ONLY спанов экспортеру. |
| 23 | MUST NOT | ✅ found | the OpenTelemetry SDK MUST NOT allow this combination. | `src/Трассировка/Классы/ОтелТрассировщик.os:247` |  |

#### SDK Span creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sdk-span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | When asked to create a Span, the SDK MUST act as if doing the following in order: | `src/Трассировка/Классы/ОтелТрассировщик.os:56` |  |

#### ShouldSample

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shouldsample)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | If the parent `SpanContext` contains a valid `TraceId`, they MUST always match. | `src/Трассировка/Классы/ОтелТрассировщик.os:64` |  |
| 26 | MUST NOT | ✅ found | `RECORD_ONLY` - `IsRecording` will be `true`, but the `Sampled` flag MUST NOT be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:247` |  |
| 27 | MUST | ✅ found | `RECORD_AND_SAMPLE` - `IsRecording` will be `true` and the `Sampled` flag MUST be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:249` |  |
| 28 | SHOULD | ✅ found | samplers SHOULD normally return the passed-in `Tracestate` if they do not intend to change it. | `src/Трассировка/Модули/ОтелСэмплер.os:157` |  |

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
| 32 | SHOULD | ⚠️ partial | For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values. | `src/Ядро/Модули/ОтелУтилиты.os:78-92` | TraceIDs are generated using UUID v4 (Новый УникальныйИдентификатор()), which provides 122 random bits out of 128. However, UUID v4 has fixed version (4) and variant (10xx) bits baked into the output, so the rightmost 7 bytes do not contain a full 56 bits of randomness as required by W3C Trace Context Level 2. The implementation provides practical randomness but does not specifically target the W3C TC L2 bit-layout requirements. |

#### Random trace flag

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#random-trace-flag)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | SHOULD | ❌ not_found | For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements. | - | The ВычислитьФлагиТрассировки() method in ОтелТрассировщик.os (line 247) only sets the Sampled flag (bit 0, value 0 or 1) based on sampling result. The Random flag (bit 1, value 0x02 per W3C TC Level 2) is never set on generated TraceIDs. |

#### Explicit randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#explicit-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | MUST NOT | ❌ not_found | SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value. | - | В коде нет проверки подключа 'rv' в TraceState и предотвращения его перезаписи. ОтелСостояниеТрассировки поддерживает работу с TraceState, но нет специальной обработки подключа 'rv' для explicit randomness. |

#### Presumption of TraceID randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#presumption-of-traceid-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | SHOULD | ⚠️ partial | For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the `rv` sub-key of the OpenTelemetry TraceState. | `src/Трассировка/Модули/ОтелСэмплер.os:290-298` | Семплер ПоДолеТрассировок использует первые 8 символов TraceId для вычисления хеша и предполагает равномерное распределение (W3C Level 2 randomness), но нет проверки подключа 'rv' в TraceState для explicit randomness. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | SHOULD | ❌ not_found | If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine whether the Random flag is set when new IDs are generated. | - | Хотя SDK поддерживает пользовательские IdGenerator через УстановитьГенераторИд(), нет механизма для указания или проверки Random flag в TraceContext. Интерфейс IdGenerator не предусматривает метод для определения random flag. |

#### Span Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | MUST | ✅ found | Span attributes MUST adhere to the common rules of attribute limits. | `src/Трассировка/Классы/ОтелСпан.os:270-285` |  |
| 38 | MUST | ✅ found | If the SDK implements the limits above it MUST provide a way to change these limits, via a configuration to the TracerProvider, by allowing users to configure individual limits like in the Java example bellow. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:83-152` |  |
| 39 | SHOULD | ⚠️ partial | The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:34-44` | Конфигурационные опции названы МаксСобытий/МаксЛинков (не EventCountLimit/LinkCountLimit), что является корректным переводом на русский язык, но не точно соответствует указанным в спецификации именам. |
| 40 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `SpanLimits`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:1` |  |
| 41 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute, event, or link was discarded due to such a limit. | `src/Трассировка/Классы/ОтелСпан.os:481-483` |  |
| 42 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per discarded attribute, event, or link). | `src/Трассировка/Классы/ОтелСпан.os:481-483` |  |

#### Id Generators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#id-generators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST | ✅ found | The SDK MUST by default randomly generate both the `TraceId` and the `SpanId`. | `src/Ядро/Модули/ОтелУтилиты.os:78-114` |  |
| 44 | MUST | ✅ found | The SDK MUST provide a mechanism for customizing the way IDs are generated for both the `TraceId` and the `SpanId`. | `src/Ядро/Модули/ОтелУтилиты.os:63-71` |  |
| 45 | MUST | ⚠️ partial | name of the methods MUST be consistent with SpanContext | `src/Ядро/Модули/ОтелУтилиты.os:57-58` | Методы названы СгенерироватьИдТрассировки/СгенерироватьИдСпана (русские названия), что семантически корректно, но не точно соответствует английской конвенции SpanContext (generateSpanId/generateTraceId). |
| 46 | MUST NOT | ✅ found | Additional `IdGenerator` implementing vendor-specific protocols such as AWS X-Ray trace id generator MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | - |  |

#### Span processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | MUST | ✅ found | SDK MUST allow to end each pipeline with individual exporter. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:1-57` |  |
| 48 | MUST | ✅ found | SDK MUST allow users to implement and configure custom processors. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:1-57` |  |

#### Interface definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | MUST | ✅ found | The `SpanProcessor` interface MUST declare the following methods: OnStart, OnEnd, Shutdown, ForceFlush | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11` |  |
| 50 | SHOULD | ✅ found | The `SpanProcessor` interface SHOULD declare the following methods: OnEnding method. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:21` |  |

#### OnStart

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onstart)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 51 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:21` |  |
| 52 | SHOULD | ✅ found | SHOULD be reflected in it. | `src/Трассировка/Классы/ОтелСпан.os:467` |  |

#### OnEnd(Span)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onendspan)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 53 | MUST | ✅ found | This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:471` |  |

#### Shutdown()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `SpanProcessor` instance. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:78` |  |
| 55 | SHOULD | ✅ found | SDKs SHOULD ignore these calls gracefully, if possible. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:43` |  |
| 56 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80` |  |
| 57 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:83` |  |
| 58 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:77` | Параметр ТаймаутМс принимается, но простой процессор не использует его - вызов Экспортер.Закрыть() не ограничен таймаутом. Пакетный процессор корректно учитывает таймаут через ЭкспортироватьВсеПакеты |

#### ForceFlush()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `Spans` for which the `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:72` |  |
| 60 | SHOULD | ✅ found | In particular, if any `SpanProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all spans for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:72` |  |
| 61 | MUST | ✅ found | The built-in SpanProcessors MUST do so. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:68` |  |
| 62 | MUST | ✅ found | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. | `src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:75` |  |
| 63 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:72` |  |
| 64 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `SpanProcessor` exports the completed spans. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:37` |  |
| 65 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:75` |  |

#### Built-in span processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#built-in-span-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:1` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:49` |  |

#### Batching processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#batching-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:155` |  |
| 69 | SHOULD | ✅ found | The processor SHOULD export a batch when any of the following happens AND the previous export call has returned: | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:42` |  |

#### Span Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 70 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:6` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | MUST | ✅ found | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:28` |  |

#### `Export(batch)`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST NOT | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 73 | MUST | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:149` |  |
| 74 | SHOULD NOT | ✅ found | The default SDK's Span Processors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the spans are being sent to. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:42` |  |

#### `ForceFlush()`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Spans` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:44` |  |
| 76 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:44` | СброситьБуфер() определена как Процедура (void) без возвращаемого значения - вызывающий код не может программно узнать результат (успех/ошибка/таймаут). Об ошибке можно узнать только по исключению. |
| 77 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed spans. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:44` |  |
| 78 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:44` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 79 | MUST | ✅ found | Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:336` |  |
| 80 | MUST | ✅ found | Sampler - `ShouldSample` and `GetDescription` MUST be safe to be called concurrently. | `src/Трассировка/Модули/ОтелСэмплер.os:141` |  |
| 81 | MUST | ✅ found | Span processor - all methods MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:49` |  |
| 82 | MUST | ✅ found | Span Exporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:12` |  |

### Logs Api

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `LoggerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:85-87` |  |

#### LoggerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `LoggerProvider` MUST provide the following functions: * Get a `Logger` | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54-91` |  |

#### Get a Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#get-a-logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following instrumentation scope parameters: | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54-58` |  |
| 4 | MUST | ✅ found | This API MUST be structured to accept a variable number of attributes, including none. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54-58` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The `Logger` MUST provide a function to: * Emit a `LogRecord` | `src/Логирование/Классы/ОтелЛоггер.os:76-112` |  |
| 6 | SHOULD | ✅ found | The `Logger` SHOULD provide functions to: * Report if `Logger` is `Enabled` | `src/Логирование/Классы/ОтелЛоггер.os:42-62` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |
| 8 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:76,82-84` |  |
| 9 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:82-84` |  |
| 10 | SHOULD | ✅ found | When only explicit Context is supported, this parameter SHOULD be required. | `src/Логирование/Классы/ОтелЛоггер.os:76` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when generating a `LogRecord`, a `Logger` SHOULD provide this `Enabled` API. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 12 | SHOULD | ✅ found | The API SHOULD accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 13 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:82-84` |  |
| 14 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:82-84` |  |
| 15 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Логирование/Классы/ОтелЛоггер.os:40` |  |
| 16 | SHOULD | ✅ found | The API SHOULD be documented that instrumentation authors needs to call this API each time they emit a LogRecord to ensure they have the most up-to-date response. | `src/Логирование/Классы/ОтелЛоггер.os:28-31` |  |

#### Optional and required parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#optional-and-required-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 18 | MUST NOT | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:42` |  |
| 19 | MUST | ✅ found | For each required parameter, the API MUST be structured to obligate a user to provide it. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | LoggerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:7` |  |
| 21 | MUST | ✅ found | Logger - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелЛоггер.os:31,67,239` |  |

### Logs Sdk

#### Logs SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logs-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Ядро/Классы/ОтелSdk.os:30` |  |

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
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent LoggerProviders. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:60` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration (i.e. LogRecordProcessors and (Development) LoggerConfigurator) MUST be owned by the LoggerProvider. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:12` |  |
| 6 | MUST | ✅ found | If configuration is updated (e.g., adding a LogRecordProcessor), the updated configuration MUST also apply to all already returned Loggers | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:213` |  |
| 7 | MUST | ✅ found | it MUST NOT matter whether a Logger was obtained from the LoggerProvider before or after the configuration change | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:213` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | Shutdown MUST be called only once for each LoggerProvider instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:123` |  |
| 9 | SHOULD | ✅ found | After the call to Shutdown, subsequent attempts to get a Logger are not allowed. SDKs SHOULD return a valid no-op Logger for these calls, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:65` |  |
| 10 | SHOULD | ✅ found | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:149` |  |
| 11 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:81` | Timeout is supported at processor level but not exposed at LoggerProvider.Закрыть() level - only async version supports timeout via Promise |
| 12 | MUST | ✅ found | Shutdown MUST be implemented by invoking Shutdown on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:126` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | SHOULD | ✅ found | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:137` |  |
| 14 | SHOULD | ⚠️ partial | ForceFlush SHOULD return some ERROR status if there is an error condition | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:113` | Synchronous method returns void, only async method can return status via Promise. Error handling is implicit through exception propagation. |
| 15 | SHOULD | ⚠️ partial | and if there is no error condition, it SHOULD return some NO ERROR status | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:113` | Synchronous method returns void, only async method can return status via Promise. Success is implicit through normal completion. |
| 16 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:61` | Timeout is supported at processor level but not exposed at LoggerProvider.СброситьБуфер() level - only async version supports timeout via Promise |
| 17 | MUST | ✅ found | ForceFlush MUST invoke ForceFlush on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:114` |  |

#### ReadableLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readablelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | A function receiving this as an argument MUST be able to access all the information added to the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:51-125` |  |
| 19 | MUST | ✅ found | It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) associated with the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:135-145` |  |
| 20 | MUST | ✅ found | The trace context fields MUST be populated from the resolved Context (either the explicitly passed Context or the current Context) when emitted. | `src/Логирование/Классы/ОтелЛоггер.os:80-91` |  |
| 21 | MUST | ✅ found | Counts for attributes due to collection limits MUST be available for exporters to report as described in the transformation to non-OTLP formats specification. | `src/Логирование/Классы/ОтелЗаписьЛога.os:130-135` |  |

#### ReadWriteLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readwritelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 22 | MUST | ✅ found | A function receiving this as an argument MUST additionally be able to modify the following information added to the LogRecord: Timestamp, ObservedTimestamp, SeverityText, SeverityNumber, Body, Attributes (addition, modification, removal), TraceId, SpanId, TraceFlags, EventName. | `src/Логирование/Классы/ОтелЗаписьЛога.os:308-347` |  |

#### LogRecord Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecord-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | MUST | ✅ found | LogRecord attributes MUST adhere to the common rules of attribute limits. | `src/Логирование/Классы/ОтелЗаписьЛога.os:235-247` |  |
| 24 | MUST | ✅ found | If the SDK implements attribute limits it MUST provide a way to change these limits, via a configuration to the LoggerProvider, by allowing users to configure individual limits like in the Java example below. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:50-53` |  |
| 25 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called LogRecordLimits. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:1` |  |
| 26 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK log to indicate to the user that an attribute was discarded due to such a limit. | `src/Логирование/Классы/ОтелЗаписьЛога.os:386` |  |
| 27 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per LogRecord (i.e., not per discarded attribute). | `src/Логирование/Классы/ОтелЗаписьЛога.os:385-388` |  |

#### LogRecordProcessor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | The SDK MUST allow each pipeline to end with an individual exporter. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:81-82,src/Логирование/Классы/ОтелПакетныйПроцессорЛогов.os:38` |  |
| 29 | MUST | ✅ found | The SDK MUST allow users to implement and configure custom processors and decorate built-in processors for advanced scenarios such as enriching with attributes. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:36-39` |  |

#### OnEmit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#onemit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | SHOULD NOT | ✅ found | This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD NOT block or throw exceptions. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:19-23` |  |
| 31 | MUST | ✅ found | For a `LogRecordProcessor` registered directly on SDK `LoggerProvider`, the `logRecord` mutations MUST be visible in next registered processors. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17-25` |  |
| 32 | SHOULD | ✅ found | Therefore, any concurrent modifications and reads of `logRecord` may result in race conditions. To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecord` be used for any concurrent processing, such as in a batching processor. | `src/Логирование/Классы/ОтелЛоггер.os:111` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | MUST NOT | ✅ found | Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:14` |  |

#### ShutDown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:81` |  |
| 35 | SHOULD | ✅ found | After the call to `Shutdown`, subsequent calls to `OnEmit` are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:42-45` |  |
| 36 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:81-95` |  |
| 37 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:83` |  |
| 38 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:84-87` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 39 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `LogRecord`s for which the `LogRecordProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:126-146` |  |
| 40 | SHOULD | ✅ found | In particular, if any `LogRecordProcessor` has any associated exporter, it SHOULD try to call the exporter's `Export` with all `LogRecord`s for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:157-158` |  |
| 41 | MUST | ✅ found | The built-in LogRecordProcessors MUST do so. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:157-158` |  |
| 42 | MUST | ✅ found | If a timeout is specified (see below), the `LogRecordProcessor` MUST prioritize honoring the timeout over finishing all calls. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:129-131` |  |
| 43 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:61-74` |  |
| 44 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `LogRecordProcessor` exports the emitted `LogRecord`s. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:28` |  |
| 45 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:64-67` |  |

#### Built-in processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#built-in-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:1` |  |
| 47 | SHOULD | ✅ found | Other common processing scenarios SHOULD be first considered for implementation out-of-process in OpenTelemetry Collector. | - |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 48 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:22-29` |  |

#### Batching processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#batching-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`'s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:155-165` |  |

#### LogRecordExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 50 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:5-6` |  |

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
| 53 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 54 | SHOULD NOT | ✅ found | The default SDK's `LogRecordProcessors` SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the logs are being sent to. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:76` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD | ✅ found | This is a hint to ensure that the export of any `ReadableLogRecords` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:42` |  |
| 56 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71` |  |
| 57 | SHOULD | ✅ found | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the `ReadlableLogRecords`. | - | This is a usage guideline for consumers of the SDK, not an implementation requirement. The implementation provides the ForceFlush method correctly. |
| 58 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each `LogRecordExporter` instance. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:51` |  |
| 60 | SHOULD | ✅ found | After the call to `Shutdown` subsequent calls to `Export` are not allowed and SHOULD return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:30` |  |
| 61 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:49` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 62 | MUST | ✅ found | LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:256` |  |
| 63 | MUST | ✅ found | Logger - all methods MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелЛоггер.os:31` |  |
| 64 | MUST | ✅ found | LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:5` |  |

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
| 2 | MUST | ✅ found | The MeterProvider MUST provide the following functions: * Get a Meter | `src/Метрики/Классы/ОтелПровайдерМетрик.os:59` |  |

#### Get a Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#get-a-meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following parameters: * name | `src/Метрики/Классы/ОтелПровайдерМетрик.os:59` |  |
| 4 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a version, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:61` |  |
| 5 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a schema_url, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:54` |  |
| 6 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:53` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ found | Note: Meter SHOULD NOT be responsible for the configuration. This should be the responsibility of the MeterProvider instead. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:221` |  |

#### Meter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The Meter MUST provide functions to create new Instruments | `src/Метрики/Классы/ОтелМетр.os:51` |  |

#### Instrument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ✅ found | Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying. | - |  |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | SHOULD | ✅ found | The API SHOULD treat it as an opaque string. | `src/Метрики/Классы/ОтелМетр.os:540` |  |
| 11 | MUST | ✅ found | It MUST be case-sensitive (e.g. kb and kB are different units), ASCII string. | `src/Метрики/Классы/ОтелМетр.os:540` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST treat it as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:257-259` |  |
| 13 | MUST | ❌ not_found | It MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or `utf8mb3`). | - | Нет явной проверки или ограничения на BMP Unicode. Строки обрабатываются как есть через НормализоватьСтроку(). |
| 14 | MUST | ❌ not_found | It MUST support at least 1023 characters. | - | Нет ограничений на длину строки описания. Строка принимается без проверки длины. |

#### Synchronous and Asynchronous instruments

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#synchronous-and-asynchronous-instruments)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The API to construct synchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 16 | SHOULD | ⚠️ partial | If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:51` | Имя обязательный первый параметр, но технически можно передать пустую строку без проверки. |
| 17 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:43-44` |  |
| 18 | SHOULD | ✅ found | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:43-44` |  |
| 19 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`; that is left to implementations of the API, like the SDK. | `src/Метрики/Классы/ОтелМетр.os:52-71` |  |
| 20 | MUST NOT | ✅ found | this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 21 | MUST | ✅ found | Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелМетр.os:52-53` |  |
| 22 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:52-71` |  |
| 23 | MUST NOT | ✅ found | this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 24 | MUST | ✅ found | Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:52` |  |
| 25 | MUST NOT | ✅ found | this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:51` |  |
| 26 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:687-706` |  |
| 27 | MUST | ✅ found | The API to construct asynchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:242` |  |
| 28 | SHOULD | ⚠️ partial | If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:242` | Имя обязательный первый параметр, но технически можно передать пустую строку без проверки. |
| 29 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:230-231` |  |
| 30 | SHOULD | ✅ found | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:230-231` |  |
| 31 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`, that is left to implementations of the API. | `src/Метрики/Классы/ОтелМетр.os:245-265` |  |
| 32 | MUST NOT | ✅ found | this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:242` |  |
| 33 | MUST | ✅ found | Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелМетр.os:245-246` |  |
| 34 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:245-265` |  |
| 35 | MUST NOT | ✅ found | this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:242` |  |
| 36 | MUST | ✅ found | Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:245` |  |
| 37 | MUST NOT | ✅ found | this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:242` |  |
| 38 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:687-706` |  |
| 39 | MUST | ✅ found | this API MUST be structured to accept a variable number of `callback` functions, including none. | `src/Метрики/Классы/ОтелМетр.os:242` |  |
| 40 | MUST | ✅ found | The API MUST support creation of asynchronous instruments by passing zero or more `callback` functions to be permanently registered to the newly created instrument. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147-156` |  |
| 41 | SHOULD | ✅ found | The API SHOULD support registration of `callback` functions associated with asynchronous instruments after they are created. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:58-62` |  |
| 42 | MUST | ✅ found | Where the API supports registration of `callback` functions after asynchronous instrumentation creation, the user MUST be able to undo registration of the specific callback after its registration by some means. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:69-74` |  |
| 43 | MUST | ⚠️ partial | Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160-180` | Callbacks выполняются при сборе, но нет явного механизма предотвращения двойного вызова в течение одного цикла сборки. |
| 44 | MUST | ✅ found | Callback functions MUST be documented as follows for the end user: | `src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69` |  |
| 45 | SHOULD | ✅ found | Callback functions SHOULD be reentrant safe. | `src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69` |  |
| 46 | SHOULD NOT | ✅ found | Callback functions SHOULD NOT take an indefinite amount of time. | `src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69` |  |
| 47 | SHOULD NOT | ✅ found | Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same `attributes`) across all registered callbacks. | `src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69` |  |
| 48 | MUST | ✅ found | Callbacks registered at the time of instrument creation MUST apply to the single instruments which is under construction. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147-156` |  |
| 49 | MUST | ✅ found | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the instrument associated with each observed `Measurement` value. | `src/Метрики/Классы/ОтелМетр.os:447-480` |  |
| 50 | MUST | ✅ found | Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of asynchronous instruments from the same `Meter` instance. | `src/Метрики/Классы/ОтелМетр.os:447-450` |  |
| 51 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160-180` |  |
| 52 | MUST | ✅ found | observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160-180` |  |
| 53 | SHOULD | ✅ found | The API SHOULD provide some way to pass `state` to the callback. | `src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69` |  |

#### General operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | SHOULD | ✅ found | All synchronous instruments SHOULD provide functions to: Report if instrument is `Enabled` | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:231-233` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when recording measurements, synchronous instruments SHOULD provide this `Enabled` API. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:231-233` |  |
| 56 | MUST | ⚠️ partial | Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:231` | Метод Включен() не принимает параметры, но можно добавить перегрузку в будущем. |
| 57 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:231-233` |  |
| 58 | SHOULD | ✅ found | The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:83-86` |  |

#### Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | MUST NOT | ✅ found | There MUST NOT be any API for creating a `Counter` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:51-72` |  |

#### Counter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелСчетчик.os:21-26` |  |
| 61 | MUST | ✅ found | This API MUST accept the following parameter: A numeric increment value. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 62 | SHOULD | ⚠️ partial | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелСчетчик.os:21` | Параметр Значение обязательный, но может быть 0 или отрицательным (игнорируется). |
| 63 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелСчетчик.os:17` |  |
| 64 | SHOULD | ✅ found | This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелСчетчик.os:17` |  |
| 65 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелСчетчик.os:22-24` |  |
| 66 | MUST | ✅ found | this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 67 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |

#### Asynchronous Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Counter other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:242` |  |
| 69 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:99-120` |  |
| 70 | MUST | ✅ found | observations from a single callback MUST be reported with identical timestamps | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:99-120` |  |
| 71 | SHOULD | ⚠️ partial | The API SHOULD provide some way to pass `state` to the callback. | - | Callbacks are created as lambda functions that can capture closure variables, but there's no explicit state parameter mechanism provided by the API |

#### Histogram creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#histogram-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST NOT | ✅ found | There MUST NOT be any API for creating a `Histogram` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:85` |  |

#### Histogram operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#histogram-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 74 | MUST | ✅ found | This API MUST accept the following parameter: A numeric value to record. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 75 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |
| 76 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелГистограмма.os:14-19` |  |
| 77 | SHOULD | ⚠️ partial | This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | - | Documentation doesn't explicitly state non-negative expectation for histogram values |
| 78 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелГистограмма.os:20-22` |  |
| 79 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелГистограмма.os:20` |  |

#### Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 80 | MUST NOT | ✅ found | There MUST NOT be any API for creating a `Gauge` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:205` |  |

#### Gauge operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 81 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 82 | MUST | ✅ found | This API MUST accept the following parameter: A numeric value. The current absolute value. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 83 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 84 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелДатчик.os:13-20` |  |
| 85 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 86 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |

#### Asynchronous Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 87 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Gauge other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:325` |  |

#### UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 88 | MUST NOT | ✅ found | There MUST NOT be any API for creating an `UpDownCounter` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:171` |  |

#### UpDownCounter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 90 | MUST | ✅ found | This API MUST accept the following parameter: A numeric value to add. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 91 | SHOULD | ✅ found | The value needs to be provided by a user. If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 92 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:17` |  |
| 93 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |

#### Asynchronous UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 94 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:227` |  |

#### Multiple-instrument callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#multiple-instrument-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 95 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: A `callback` function* A list (or tuple, etc.) of Instruments used in the `callback` function. | `src/Метрики/Классы/ОтелМетр.os:388` |  |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | SHOULD | ✅ found | All the metrics components SHOULD allow new APIs to be added to existing components without introducing breaking changes. | - | This is a design principle that is evident from the use of optional parameters and backwards-compatible API design throughout the codebase, but not explicitly enforced by code |
| 97 | SHOULD | ✅ found | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелМетр.os:171` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | MUST | ✅ found | MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:44` |  |
| 99 | MUST | ✅ found | Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелМетр.os:41` |  |
| 100 | MUST | ✅ found | Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:45` |  |

### Metrics Sdk

#### Metrics SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metrics-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Ядро/Классы/ОтелSdk.os:1` |  |

#### MeterProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A `MeterProvider` MUST provide a way to allow a Resource to be specified. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:295` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the metrics produced by any `Meter` from the `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:80` |  |

#### MeterProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `MeterProvider`s. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:84` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration (i.e. MetricExporters, MetricReaders, Views, and (Development) MeterConfigurator) MUST be owned by the `MeterProvider`. | `src/Метрики/Классы/ОтелПrovайдерМетрик.os:17` |  |
| 6 | MUST | ✅ found | If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the `MeterProvider` before or after the configuration change). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:221` |  |
| 7 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the `MeterProvider` before or after the configuration change). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:221` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MeterProvider` instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:144` |  |
| 9 | SHOULD | ✅ found | After the call to `Shutdown`, subsequent attempts to get a `Meter` are not allowed. SDKs SHOULD return a valid no-op Meter for these calls, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:70` |  |
| 10 | SHOULD | ⚠️ partial | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:177` | Асинхронная версия возвращает Обещание, но синхронная версия не возвращает статус |
| 11 | SHOULD | ⚠️ partial | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:177` | Таймаут реализован только в асинхронной версии через библиотеку async |
| 12 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered MetricReader and MetricExporter instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:149` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered MetricReader instances that implement `ForceFlush`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:128` |  |
| 14 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:165` | Асинхронная версия возвращает Обещание, но синхронная версия не возвращает статус |
| 15 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:165` | Статус ошибки реализован только в асинхронной версии через исключения в Обещании |
| 16 | SHOULD | ⚠️ partial | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:165` | Таймаут реализован только в асинхронной версии через библиотеку async |

#### View

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | The SDK MUST provide functionality for a user to create Views for a MeterProvider. | `src/Метрики/Классы/ОтелПредставление.os:132-175` |  |
| 18 | MUST | ✅ found | This functionality MUST accept as inputs the Instrument selection criteria and the resulting stream configuration. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:57` |  |
| 19 | MUST | ✅ found | The SDK MUST provide the means to register Views with a MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:189` |  |

#### Instrument selection criteria

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-selection-criteria)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | Criteria SHOULD be treated as additive. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:34-62` |  |
| 21 | MUST | ✅ found | The SDK MUST accept the following criteria: name, type, unit, meter_name, meter_version, meter_schema_url. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159-168` |  |
| 22 | MUST | ✅ found | If the SDK does not support wildcards in general, it MUST still recognize the special single asterisk (*) character as matching all Instruments. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37-38` |  |
| 23 | MUST NOT | ✅ found | the instrument selection criteria parameter needs to be structured to accept a name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 24 | MUST NOT | ✅ found | the instrument selection criteria parameter needs to be structured to accept a type, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 25 | MUST NOT | ✅ found | the instrument selection criteria parameter needs to be structured to accept a unit, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 26 | MUST NOT | ✅ found | the instrument selection criteria parameter needs to be structured to accept a meter_name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 27 | MUST NOT | ✅ found | the instrument selection criteria parameter needs to be structured to accept a meter_version, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 28 | MUST NOT | ✅ found | the instrument selection criteria parameter needs to be structured to accept a meter_schema_url, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |
| 29 | MUST NOT | ✅ found | the instrument selection criteria can be structured to accept the criteria, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:159` |  |

#### Stream configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#stream-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | The SDK MUST accept the following stream configuration parameters: name, description, attribute_keys, aggregation, exemplar_reservoir, aggregation_cardinality_limit. | `src/Метрики/Классы/ОтелПредставление.os:156-164` |  |
| 31 | SHOULD | ✅ found | The metric stream name that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:29` |  |
| 32 | SHOULD | ✅ found | In order to avoid conflicts, if a name is provided the View SHOULD have an instrument selector that selects at most one instrument. | - | Not implemented - no conflict detection for view names selecting multiple instruments |
| 33 | MUST NOT | ✅ found | the stream configuration parameter needs to be structured to accept a name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:157` |  |
| 34 | MUST | ✅ found | If the user does not provide a name value, name from the Instrument the View matches MUST be used by default. | `src/Метрики/Классы/ОтелМетр.os:754-760` |  |
| 35 | SHOULD | ✅ found | The metric stream description that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:37` |  |
| 36 | MUST NOT | ✅ found | the stream configuration parameter needs to be structured to accept a description, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:158` |  |
| 37 | MUST | ✅ found | If the user does not provide a description value, the description from the Instrument a View matches MUST be used by default. | `src/Метрики/Классы/ОтелМетр.os:754-760` |  |
| 38 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелПредставление.os:47` |  |
| 39 | MUST | ✅ found | all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелМетр.os:792-813` |  |
| 40 | MUST NOT | ✅ found | the stream configuration parameter needs to be structured to accept attribute_keys, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелПредставление.os:159` |  |
| 41 | SHOULD | ✅ found | If the user does not provide any value, the SDK SHOULD use the Attributes advisory parameter configured on the instrument instead. | `src/Метрики/Классы/ОтелМетр.os:792-813` |  |
| 42 | MUST | ✅ found | If the Attributes advisory parameter is absent, all attributes MUST be kept. | `src/Метрики/Классы/ОтелМетр.os:792-813` |  |
| 43 | SHOULD | ✅ found | implementations SHOULD support configuring an exclude-list of attribute keys. | `src/Метрики/Классы/ОтелПредставление.os:55` |  |
| 44 | MUST | ✅ found | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелМетр.os:792-813` |  |
| 45 | MUST | ✅ found | all other attributes MUST be kept. | `src/Метрики/Классы/ОтелМетр.os:792-813` |  |
| 46 | MUST NOT | ✅ found | the stream configuration parameter needs to be structured to accept an aggregation, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:161` |  |
| 47 | MUST | ✅ found | If the user does not provide an aggregation value, the MeterProvider MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance. | `src/Метрики/Классы/ОтелМетр.os:829-871` |  |
| 48 | MUST NOT | ✅ found | the stream configuration parameter needs to be structured to accept an exemplar_reservoir, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:162` |  |
| 49 | MUST | ✅ found | If the user does not provide an exemplar_reservoir value, the MeterProvider MUST apply a default exemplar reservoir. | `src/Метрики/Классы/ОтелМетр.os:829-871` |  |
| 50 | MUST NOT | ✅ found | the stream configuration parameter needs to be structured to accept an aggregation_cardinality_limit, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:164` |  |
| 51 | MUST | ✅ found | If the user does not provide an aggregation_cardinality_limit value, the MeterProvider MUST apply the default aggregation cardinality limit the MetricReader is configured with. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:249-255` |  |

#### Measurement processing

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#measurement-processing)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 52 | SHOULD | ✅ found | The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument. | `src/Метрики/Классы/ОтелМетр.os:754-871` |  |
| 53 | MUST | ✅ found | Instrument advisory parameters, if any, MUST be honored. | `src/Метрики/Классы/ОтелМетр.os:792-813` |  |
| 54 | SHOULD | ✅ found | If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning. | - | Not implemented - no conflict detection or warning emission for conflicting metric identities |
| 55 | SHOULD | ✅ found | If it is not possible to apply the View without producing semantic errors the implementation SHOULD emit a warning and proceed as if the View did not match. | - | Not implemented - no validation for semantic errors when applying Views |
| 56 | MUST | ✅ found | If both a View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:792-813` |  |
| 57 | SHOULD | ✅ found | If the Instrument could not match with any of the registered View(s), the SDK SHOULD enable the instrument using the default aggregation and temporality. | `src/Метрики/Классы/ОтелМетр.os:829-871` |  |

#### Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 58 | MUST | ✅ found | The SDK MUST provide the following Aggregation to support the Metric Points in the Metrics Data Model: Drop, Default, Sum, Last Value, Explicit Bucket Histogram. | `src/Метрики/Модули/ОтелАгрегация.os:15-65` |  |
| 59 | SHOULD | ✅ found | The SDK SHOULD provide the following Aggregation: Base2 Exponential Bucket Histogram. | `src/Метрики/Модули/ОтелАгрегация.os:76-81` |  |

#### Histogram Aggregations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#histogram-aggregations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | SHOULD NOT | ✅ found | Arithmetic sum of Measurement values in population. This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. UpDownCounter or ObservableGauge). | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:51` |  |
| 61 | MUST | ✅ found | Implementations are REQUIRED to accept the entire normal range of IEEE floating point values (i.e., all values except for +Inf, -Inf and NaN values). | - | Not explicitly implemented - no validation for IEEE floating point values range in histogram aggregations |
| 62 | SHOULD NOT | ✅ found | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the sum, min, and max fields, because these values do not map into a valid bucket. | - | Not implemented - no filtering of non-normal values (+Inf, -Inf, NaN) in histogram aggregations |
| 63 | SHOULD | ✅ found | SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different. | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:185-202` |  |
| 64 | SHOULD | ✅ found | When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:245-260` |  |
| 65 | SHOULD | ✅ found | Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possible, within the constraint of maximum size. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:296-320` |  |

#### Observations inside asynchronous callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#observations-inside-asynchronous-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | MUST | ✅ found | Callback functions MUST be invoked for the specific MetricReader performing collection, such that observations made or produced by executing callbacks only apply to the intended MetricReader during collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:281-305` |  |
| 67 | SHOULD | ⚠️ partial | The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks. | - | No validation to disregard asynchronous instrument API usage outside of registered callbacks |
| 68 | SHOULD | ⚠️ partial | The implementation SHOULD use a timeout to prevent indefinite callback execution. | - | No timeout mechanism implemented for callback execution |
| 69 | MUST | ✅ found | The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160-185` |  |
| 70 | SHOULD NOT | ✅ found | The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:281-305` |  |

#### Cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | SHOULD | ✅ found | SDKs SHOULD support being configured with a cardinality limit. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:401` |  |
| 72 | SHOULD | ✅ found | Cardinality limit enforcement SHOULD occur after attribute filtering, if any. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:108` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | SHOULD | ⚠️ partial | A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardinality_limit` value defined for the stream, that value SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:92` | ОтелПредставление has ЛимитМощностиАгрегации field but it is not applied to instruments in ПрименитьПредставлениеКИнструменту method |
| 74 | SHOULD | ⚠️ partial | If there is no matching view, but the `MetricReader` defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:151` | MetricReader has ЛимитМощности method returning default 2000, but this is not applied to instruments when no View is matched |
| 75 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:283` |  |

#### Overflow attribute

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#overflow-attribute)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 76 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:370` |  |
| 77 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:108` |  |

#### Synchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#synchronous-instrument-cardinality limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | MUST | ❌ not_found | Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow. | - | Implementation does not distinguish between cumulative and delta temporality for overflow handling. All overflow measurements go to single overflow aggregator regardless of temporality |
| 79 | MUST | ✅ found | Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in exactly one Aggregator, which is either an Aggregator associated with the correct attribute set or an aggregator associated with the overflow attribute set. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:106-118` |  |
| 80 | MUST NOT | ✅ found | Measurements MUST NOT be double-counted or dropped during an overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:106-118` |  |

#### Asynchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#asynchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 81 | SHOULD | ❌ not_found | Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality. | - | Asynchronous instruments (ОтелБазовыйНаблюдаемыйИнструмент) do not implement cardinality limits. They collect all observations from callbacks without overflow handling |

#### Duplicate instrument registration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#duplicate-instrument-registration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 82 | MUST | ✅ found | This means that the Meter MUST return a functional instrument that can be expected to export data even if this will cause semantic error in the data model. | `src/Метрики/Классы/ОтелМетр.os:56-60` |  |
| 83 | SHOULD | ✅ found | Therefore, when a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted. | `src/Метрики/Классы/ОтелМетр.os:619-622` |  |
| 84 | SHOULD | ✅ found | The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible. | `src/Метрики/Классы/ОтелМетр.os:619-622` |  |
| 85 | SHOULD | ❌ not_found | If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning. | - | Warning is always emitted for descriptor conflicts. There is no check if View corrects the description conflict to suppress the warning |
| 86 | SHOULD | ❌ not_found | If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning. | - | Warning message does not include renaming View recipe. It only shows the conflicting parameters without suggesting View-based solution |
| 87 | SHOULD | ❌ not_found | Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument registration. | - | SDK returns the first registered instrument, not both Metric objects. No data pass-through for conflicting instruments with different units |
| 88 | MUST | ✅ found | To accommodate the recommendations from the data model, the SDK MUST aggregate data from identical Instruments together in its export pipeline. | `src/Метрики/Классы/ОтелМетр.os:56-60` |  |

#### Name conflict

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#name-conflict)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | MUST | ✅ found | the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелМетр.os:54` |  |

#### Instrument name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | SHOULD | ❌ not_found | it SHOULD validate the instrument name conforms to the instrument name syntax | - | No name validation is implemented in any instrument creation methods. Names are only normalized via НРег() but not validated for syntax conformance. |
| 91 | SHOULD | ❌ not_found | the Meter SHOULD emit an error notifying the user about the invalid name | - | No error logging for invalid names since name validation itself is not implemented. |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 92 | SHOULD NOT | ✅ found | it SHOULD NOT validate the instrument unit | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелМетр.os:53` |  |
| 93 | MUST | ✅ found | the Meter MUST treat it the same as an empty unit string | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелМетр.os:540` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 94 | SHOULD NOT | ✅ found | it SHOULD NOT validate the instrument description | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелМетр.os:52` |  |
| 95 | MUST | ✅ found | the Meter MUST treat it the same as an empty description string | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелМетр.os:540` |  |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | SHOULD | ✅ found | it SHOULD validate the instrument advisory parameters | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелМетр.os:687` |  |
| 97 | SHOULD | ✅ found | the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелМетр.os:693` |  |
| 98 | MUST | ✅ found | the Meter MUST return an instrument using the first-seen advisory parameters and log an appropriate error as described in duplicate instrument registrations | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелМетр.os:58` |  |
| 99 | MUST | ✅ found | MUST take precedence over the advisory parameters | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелМетр.os:586` |  |

#### Instrument advisory parameter: `ExplicitBucketBoundaries`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameter-explicitbucketboundaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 100 | MUST | ✅ found | the `ExplicitBucketBoundaries` advisory parameter MUST be used | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелМетр.os:590` |  |

#### Exemplar

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 101 | MUST | ✅ found | A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements via the `ExemplarFilter` and `ExemplarReservoir` hooks | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14` |  |
| 102 | SHOULD | ✅ found | `Exemplar` sampling SHOULD be turned on by default | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелМетр.os:528` |  |
| 103 | MUST NOT | ⚠️ partial | the SDK MUST NOT have overhead related to exemplar sampling | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Модули/ОтелФильтрЭкземпляров.os:46` | Filter check is implemented to skip sampling when disabled, but complete overhead elimination when sampling is off may not be fully implemented throughout all aggregators. |
| 104 | MUST | ✅ found | A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:88` |  |
| 105 | SHOULD | ✅ found | A Metric SDK SHOULD provide configuration for Exemplar sampling | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:122` |  |

#### ExemplarFilter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarfilter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 106 | MUST | ✅ found | The ExemplarFilter configuration MUST allow users to select between one of the built-in ExemplarFilters. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:74-77` |  |
| 107 | SHOULD | ✅ found | The ExemplarFilter SHOULD be a configuration parameter of a MeterProvider for an SDK. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:74-77` |  |
| 108 | SHOULD | ✅ found | The default value SHOULD be TraceBased. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:27-35` |  |
| 109 | SHOULD | ✅ found | The filter configuration SHOULD follow the environment variable specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114-133` |  |
| 110 | MUST | ✅ found | An OpenTelemetry SDK MUST support the following filters: AlwaysOn, AlwaysOff, TraceBased | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:9-35` |  |

#### ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 111 | MUST | ✅ found | The ExemplarReservoir interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:41-47,57-63` |  |
| 112 | MUST | ✅ found | A new ExemplarReservoir MUST be created for every known timeseries data point, as determined by aggregation and view configuration. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:82-97` |  |
| 113 | SHOULD | ✅ found | The offer method SHOULD accept measurements, including: The value of the measurement, The complete set of Attributes of the measurement, The Context of the measurement, which covers the Baggage and the current active Span, A timestamp that best represents when the measurement was taken. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:41-47` |  |
| 114 | SHOULD | ✅ found | The offer method SHOULD have the ability to pull associated trace and span information without needing to record full context. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:125-129` |  |
| 115 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the Attributes associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the offer method. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:139-159` |  |
| 116 | MUST | ✅ found | The collect method MUST return accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:57-63` |  |
| 117 | SHOULD | ✅ found | Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:123` |  |
| 118 | MUST | ✅ found | Exemplars MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:139-159` |  |
| 119 | SHOULD | ⚠️ partial | The ExemplarReservoir SHOULD avoid allocations when sampling exemplars. | - | Algorithm R implementation allocates arrays but this is standard practice for reservoir sampling |
| 120 | MUST | ✅ found | The reservoir MUST be given the Attributes associated with its timeseries point either at construction. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:41-47` |  |

#### Exemplar defaults

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar-defaults)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 121 | MUST | ✅ found | The SDK MUST include two types of built-in exemplar reservoirs: SimpleFixedSizeExemplarReservoir, AlignedHistogramBucketExemplarReservoir | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1,src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:1` |  |
| 122 | SHOULD | ❌ not_found | Explicit bucket histogram aggregation with more than 1 bucket SHOULD use AlignedHistogramBucketExemplarReservoir. | - | No automatic assignment of reservoir type based on aggregation configuration found |
| 123 | SHOULD | ❌ not_found | Base2 Exponential Histogram Aggregation SHOULD use a SimpleFixedSizeExemplarReservoir with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty. | - | No automatic assignment of reservoir type for exponential histograms found |
| 124 | SHOULD | ❌ not_found | All other aggregations SHOULD use SimpleFixedSizeExemplarReservoir. | - | No automatic assignment of reservoir type based on aggregation type found |

#### SimpleFixedSizeExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#simplefixedsizeexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 125 | MUST | ✅ found | This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the reservoir has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:98-114` |  |
| 126 | SHOULD | ✅ found | Any stateful portion of sampling computation SHOULD be reset every collection cycle. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:67-70` |  |
| 127 | SHOULD | ✅ found | If no size configuration is provided, the default size MAY be the number of possible concurrent threads (e.g., number of CPUs) to help reduce contention. Otherwise, a default size of 1 SHOULD be used. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:174` |  |

#### AlignedHistogramBucketExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#alignedhistogrambucketexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 128 | MUST | ✅ found | This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:158-161` |  |
| 129 | MUST | ⚠️ partial | This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:40-51` | Uses simple replacement (last measurement wins) instead of uniformly-weighted sampling algorithm |
| 130 | SHOULD | ✅ found | This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:158-161` |  |
| 131 | SHOULD | ⚠️ partial | This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:40-51` | Uses simple replacement (last measurement wins) instead of uniformly-weighted sampling algorithm |

#### Custom ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#custom-exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 132 | MUST | ✅ found | The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation. | `src/Метрики/Классы/ОтелПредставление.os:83-85` |  |
| 133 | MUST | ✅ found | This extension MUST be configurable on a metric View, although individual reservoirs MUST still be instantiated per metric-timeseries. | `src/Метрики/Классы/ОтелПредставление.os:83-85` |  |
| 134 | MUST | ✅ found | Individual reservoirs MUST still be instantiated per metric-timeseries. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:82-97` |  |

#### Collect

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#collect)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 135 | SHOULD | ❌ not_found | Collect SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Collect methods do not provide failure/timeout return values - they handle errors internally with logging |
| 136 | SHOULD | ✅ found | Collect SHOULD invoke Produce on registered MetricProducers. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:235` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 137 | MUST | ✅ found | Shutdown MUST be called only once for each MetricReader instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:112` |  |
| 138 | SHOULD | ❌ not_found | SDKs SHOULD return some failure for these calls, if possible. | - | СброситьБуфер() (Collect) is a void procedure with no guard checking Закрыт flag after shutdown. No failure is returned to the caller for Collect calls after shutdown. |
| 139 | SHOULD | ❌ not_found | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Закрыть() is a void procedure. All exceptions (timeout, exporter close errors) are caught internally and only logged, never propagated to the caller. |
| 140 | SHOULD | ✅ found | Shutdown SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:117` |  |

#### Periodic exporting MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 141 | MUST | ✅ found | The reader MUST synchronize calls to MetricExporter's Export to make sure that they are not invoked concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:242` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 142 | SHOULD | ⚠️ partial | ForceFlush SHOULD collect metrics, call Export(batch) and ForceFlush() on the configured Push Metric Exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` | СброситьБуфер() calls СобратьИЭкспортировать() which collects metrics and calls Экспортер.Экспортировать(). However, it does not call Экспортер.СброситьБуфер() (ForceFlush on the exporter). |
| 143 | SHOULD | ❌ not_found | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | СброситьБуфер() is a void procedure (Процедура). There is no return value or mechanism to communicate success, failure, or timeout to the caller. |
| 144 | SHOULD | ❌ not_found | ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model ERROR and NO ERROR. | - | СброситьБуфер() is a void procedure. Errors during collection and export are caught internally (try/catch in СобратьИЭкспортировать) and only logged, never returned to the caller. |
| 145 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94` | СброситьБуфер() has no explicit timeout parameter. It relies on the underlying transport timeout (10 seconds for HTTP). There is no configurable ForceFlush timeout at the reader level. |

#### MetricExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 146 | MUST | ✅ found | MetricExporter defines the interface that protocol-specific exporters MUST implement so that they can be plugged into OpenTelemetry SDK and support sending of telemetry data. | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:1` |  |
| 147 | SHOULD | ❌ not_found | Metric Exporters SHOULD report an error condition for data output by the MetricReader with unsupported Aggregation or Aggregation Temporality, as this condition can be corrected by a change of MetricReader configuration. | - | ОтелЭкспортерМетрик.Экспортировать() does not validate or report unsupported Aggregation or Aggregation Temporality. No error reporting exists for this condition. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 148 | MUST | ✅ found | A Push Metric Exporter MUST support the following functions: | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:29` |  |
| 149 | MUST | ✅ found | The SDK MUST provide a way for the exporter to get the Meter information (e.g. name, version, etc.) associated with each Metric Point. | `src/Метрики/Классы/ОтелДанныеМетрики.os:42` |  |
| 150 | MUST NOT | ✅ found | Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:69` |  |
| 151 | MUST | ✅ found | Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:149` |  |
| 152 | SHOULD NOT | ⚠️ partial | The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the metrics are being sent to. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:76` | ОтелHttpТранспорт implements retry with exponential backoff (СтратегияПовтора) for HTTP 429, 502, 503, 504. Retry is in the protocol-specific transport, not the exporter itself, which partially aligns with the spec's reasoning about protocol-dependent retry, but the SDK does ship with built-in retry. |
| 153 | SHOULD | ✅ found | This is a hint to ensure that the export of any Metrics the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47` |  |
| 154 | SHOULD | ❌ not_found | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | СброситьБуфер() on the exporter is a void procedure (Процедура). No return value or mechanism to communicate success, failure, or timeout. |
| 155 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed metrics. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47` |  |
| 156 | SHOULD | ✅ found | ForceFlush SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47` |  |
| 157 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each MetricExporter instance. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:53` |  |
| 158 | SHOULD NOT | ✅ found | Shutdown SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:54` |  |

#### MetricProducer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricproducer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 159 | MUST | ✅ found | MetricProducer defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:1` |  |
| 160 | SHOULD | ❌ not_found | MetricProducer implementations SHOULD accept configuration for the AggregationTemporality of produced metrics. | - | ИнтерфейсПродюсерМетрик.Произвести() accepts only ФильтрМетрик parameter. There is no mechanism to configure AggregationTemporality for MetricProducer implementations. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 161 | MUST | ✅ found | A MetricProducer MUST support the following functions: | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 162 | MUST | ✅ found | A `MetricFilter` MUST support the following functions: | `src/Метрики/Классы/ОтелФильтрМетрик.os:29` |  |

#### Defaults and configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#defaults-and-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 163 | MUST | ✅ found | The SDK MUST provide configuration according to the SDK environment variables specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:3` |  |

#### Numerical limits handling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#numerical-limits-handling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 164 | MUST | ➖ n_a | The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry. | - | OneScript uses System.Decimal instead of IEEE 754, so NaN and Infinity are not possible - operations throw exceptions instead of returning special values. This is a platform limitation. |
| 165 | MUST | ➖ n_a | If the SDK receives float/double values from Instruments, it MUST handle all the possible values. For example, if the language runtime supports IEEE 754, the SDK needs to handle NaNs and Infinites. | - | OneScript Decimal type does not support IEEE 754 special values like NaN and Infinity. Operations with invalid values throw exceptions rather than producing special float values. This is a platform-specific limitation. |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 166 | SHOULD | ✅ found | All the metrics components SHOULD allow new methods to be added to existing components without introducing breaking changes. | - |  |
| 167 | SHOULD | ✅ found | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to existing methods without introducing breaking changes, if possible. | - |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 168 | MUST | ✅ found | MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:128` |  |
| 169 | MUST | ✅ found | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:15` |  |
| 170 | MUST | ✅ found | MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:14` |  |
| 171 | MUST | ✅ found | MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:12` |  |

### Otlp Exporter

#### Configuration Options

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#configuration-options)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The following configuration options MUST be available to configure the OTLP exporter. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:148-186` |  |
| 2 | MUST | ✅ found | Each configuration option MUST be overridable by a signal specific option. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:820-828` |  |
| 3 | MUST | ✅ found | The implementation MUST honor the following URL components: | `src/Экспорт/Классы/ОтелHttpТранспорт.os:98-104` |  |
| 4 | MUST | ✅ found | When using `OTEL_EXPORTER_OTLP_ENDPOINT`, exporters MUST construct per-signal URLs as described below. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:598-613` |  |
| 5 | MUST | ✅ found | Additionally, the option MUST accept a URL with a scheme of either `http` or `https`. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:174-175` |  |
| 6 | MUST | ✅ found | Options MUST be one of: `grpc`, `http/protobuf`, `http/json`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563-571` |  |
| 7 | SHOULD | ✅ found | The option SHOULD accept any form allowed by the underlying gRPC client implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:174-175` |  |
| 8 | SHOULD | ❌ not_found | If the gRPC client implementation does not support an endpoint with a scheme of `http` or `https` then the endpoint SHOULD be transformed to the most sensible format for that implementation. | - | gRPC transport uses OPI_GRPC library which handles URL formats internally, but no explicit transformation logic found in the codebase |
| 9 | SHOULD | ✅ found | SDKs SHOULD default endpoint variables to use `http` scheme unless they have good reasons to choose `https` scheme for the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:171,176` |  |
| 10 | SHOULD | ❌ not_found | they SHOULD continue to be supported as they were part of a stable release of the specification. | - | Obsolete environment variables OTEL_EXPORTER_OTLP_SPAN_INSECURE and OTEL_EXPORTER_OTLP_METRIC_INSECURE are not supported in the codebase |
| 11 | SHOULD | ❌ not_found | The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:168` | Default protocol is set to "http/json" instead of "http/protobuf" as required by spec |

#### Endpoint URLs for OTLP/HTTP

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#endpoint-urls-for-otlphttp)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal as follow: | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:598-613` |  |
| 13 | MUST | ✅ found | For the per-signal variables (`OTEL_EXPORTER_OTLP_<signal>_ENDPOINT`), the URL MUST be used as-is without any modification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:599-601` |  |
| 14 | MUST | ✅ found | The only exception is that if an URL contains no path part, the root path `/` MUST be used (see Example 2). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:839-850` |  |
| 15 | MUST NOT | ✅ found | An SDK MUST NOT modify the URL in ways other than specified above. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:599-601` |  |

#### Specify Protocol

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specify-protocol)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563-571` |  |
| 17 | SHOULD | ✅ found | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563-571` |  |
| 18 | SHOULD | ⚠️ partial | If they support only one, it SHOULD be `http/protobuf`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563-571` | SDK supports grpc and http/json, but not http/protobuf specifically |
| 19 | SHOULD | ❌ not_found | If no configuration is provided the default transport SHOULD be `http/protobuf` unless SDKs have good reasons to choose `grpc` as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:168` | Default protocol is "http/json" instead of "http/protobuf" as recommended |

#### Specifying headers via environment variables

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:688-703` |  |

#### Retry

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#retry)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | Transient errors MUST be handled with a retry strategy. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:76,111-115` |  |
| 22 | MUST | ✅ found | This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:165-168` |  |

#### User Agent

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#user-agent)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | SHOULD | ❌ not_found | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter. | - | No User-Agent header implementation found in HTTP or gRPC transports |
| 24 | SHOULD | ❌ not_found | The format of the header SHOULD follow RFC 7231. | - | No User-Agent header implementation found in HTTP or gRPC transports |
| 25 | SHOULD | ❌ not_found | The resulting User-Agent SHOULD include the exporter's default User-Agent string. | - | No User-Agent header implementation found in HTTP or gRPC transports |

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
| 4 | MUST NOT | ✅ found | the implementation MUST NOT throw an exception | `src/Пропагация/Классы/ОтелW3CПропагатор.os:81` |  |
| 5 | MUST NOT | ✅ found | MUST NOT store a new value in the `Context`, in order to preserve any previously existing valid value. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:90` |  |

#### TextMap Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | the key/value pairs MUST only consist of US-ASCII characters that make up valid HTTP header fields as per RFC 9110. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:62` |  |
| 7 | MUST | ✅ found | `Getter` and `Setter` MUST be stateless and allowed to be saved as constants, in order to effectively avoid runtime allocations. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:72` |  |

#### Setter argument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#setter-argument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used protocol is case insensitive | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:19` |  |
| 9 | MUST | ✅ found | otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:19` |  |

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
| 16 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:42` |  |

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
| 22 | SHOULD | ✅ found | If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace Context Propagator and the Baggage `Propagator` specified in the Baggage API. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:443` |  |
| 23 | MUST | ✅ found | These platforms MUST also allow pre-configured propagators to be disabled or overridden. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:441` |  |

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
| 27 | MUST | ✅ found | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry extension packages: | `src/Пропагация/Классы/ОтелB3Пропагатор.os:1` |  |
| 28 | MUST NOT | ✅ found | It MUST NOT use OpenTracing in the resulting propagator name as it is not widely adopted format in the OpenTracing ecosystem. | - |  |
| 29 | MUST NOT | ✅ found | Additional Propagators implementing vendor-specific protocols such as AWS X-Ray trace header protocol MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | - |  |

#### W3C Trace Context Requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#w3c-trace-context-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | A W3C Trace Context propagator MUST parse and validate the traceparent and tracestate HTTP headers as specified in W3C Trace Context Level 2. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:81` |  |
| 31 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid traceparent value using the same header. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:63` |  |
| 32 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid tracestate unless the value is empty, in which case the tracestate header may be omitted. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:65` |  |

#### B3 Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | MUST | ✅ found | MUST attempt to extract B3 encoded using single and multi-header formats. The single-header variant takes precedence over the multi-header version. | `src/Пропагация/Классы/ОтелB3Пропагатор.os:64` |  |
| 34 | MUST | ⚠️ partial | MUST preserve a debug trace flag, if received, and propagate it with subsequent requests. | `src/Пропагация/Классы/ОтелB3Пропагатор.os:139` | Debug flag is detected during extract ("d" in single-header, X-B3-Flags=1 in multi-header) and causes sampled=1, but is not preserved as debug in SpanContext. Inject never writes debug back (no "d" in single-header, no X-B3-Flags in multi-header), so debug state is lost during propagation. |
| 35 | MUST | ✅ found | Additionally, an OpenTelemetry implementation MUST set the sampled trace flag when the debug flag is set. | `src/Пропагация/Классы/ОтелB3Пропагатор.os:162` |  |
| 36 | MUST NOT | ✅ found | MUST NOT reuse X-B3-SpanId as the id for the server-side span. | `src/Пропагация/Классы/ОтелB3Пропагатор.os:189` |  |

#### B3 Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | MUST | ⚠️ partial | MUST default to injecting B3 using the single-header format | `src/Пропагация/Классы/ОтелB3Пропагатор.os:203` | Constructor defaults to ОтелФорматB3.Мульти() (multi-header) when no format is provided. The spec requires the default to be single-header format. |
| 38 | MUST | ✅ found | MUST provide configuration to change the default injection format to B3 multi-header | `src/Пропагация/Классы/ОтелB3Пропагатор.os:198` |  |
| 39 | MUST NOT | ✅ found | MUST NOT propagate X-B3-ParentSpanId as OpenTelemetry does not support reusing the same id for both sides of a request. | `src/Пропагация/Классы/ОтелB3Пропагатор.os:103` |  |

#### Fields

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#fields)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 40 | MUST | ⚠️ partial | Fields MUST return the header names that correspond to the configured format, i.e., the headers used for the inject operation. | `src/Пропагация/Классы/ОтелB3Пропагатор.os:85` | For single-header format, Fields correctly returns ["b3"]. For multi-header format, Fields returns ["X-B3-TraceId", "X-B3-SpanId", "X-B3-Sampled", "X-B3-ParentSpanId", "X-B3-Flags"] but inject only writes X-B3-TraceId, X-B3-SpanId, X-B3-Sampled. X-B3-ParentSpanId and X-B3-Flags are listed but never used in inject. |

### Env Vars

#### Environment Variable Specification

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#environment-variable-specification)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If they do, they SHOULD use the names and value parsing behavior specified in this document. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:6-46` |  |
| 2 | SHOULD | ✅ found | They SHOULD also follow the common configuration specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1-104` |  |

#### Implementation guidelines

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#implementation-guidelines)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The environment-based configuration MUST have a direct code configuration equivalent. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:85-90` |  |

#### Parsing empty value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#parsing-empty-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:780` |  |

#### Boolean

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#boolean)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Any value that represents a Boolean MUST be set to true only by the case-insensitive string "true", meaning "True" or "TRUE" are also accepted, as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:764` |  |
| 6 | MUST NOT | ✅ found | An implementation MUST NOT extend this definition and define additional values that are interpreted as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:764` |  |
| 7 | MUST | ✅ found | Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:764` |  |
| 8 | SHOULD | ❌ not_found | If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied. | - | Boolean parsing only checks НРег(Значение) = "true" without logging warnings for invalid values like "maybe" or "yes". No БезопасныйБулев function exists. |
| 9 | SHOULD | ✅ found | All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:763` |  |
| 10 | MUST NOT | ✅ found | Renaming or changing the default value MUST NOT happen without a major version upgrade. | - |  |

#### Numeric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#numeric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | For new implementations, these should be treated as MUST requirements. | - |  |
| 12 | MUST | ✅ found | For new implementations, these should be treated as MUST requirements. | - |  |
| 13 | SHOULD | ✅ found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them as not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:801-803` |  |

#### Enum

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#enum)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | SHOULD | ✅ found | Enum values SHOULD be interpreted in a case-insensitive manner. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:220,397,446,562,584,764` |  |
| 15 | MUST | ✅ found | For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:253,480` |  |

#### General SDK Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ⚠️ partial | Values MUST be deduplicated in order to register a Propagator only once. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:468-474` | Правильная дедупликация пропагаторов реализована через Соответствие как Set, но используется неправильная переменная окружения - код читает otel.propagators вместо OTEL_PROPAGATORS |
| 17 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:253-258` |  |
| 18 | MUST | ✅ found | Invalid or unrecognized input MUST be logged | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:253` |  |
| 19 | MUST | ✅ found | MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:253-258` |  |

#### Attribute Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#attribute-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | Implementations SHOULD only offer environment variables for the types of attributes, for which that SDK implements truncation mechanism. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:648-665` |  |

#### Exporter Selection

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#exporter-selection)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | SHOULD | ❌ not_found | It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | - | Код не поддерживает deprecated значение "logging" для экспортеров - только "otlp", "console" и "none". Это соответствует рекомендации не поддерживать deprecated значения в новых реализациях. |
| 22 | SHOULD | ❌ not_found | It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | - | Код не поддерживает deprecated значение "logging" для метрик экспортера - только "otlp" и "none". Это соответствует рекомендации не поддерживать deprecated значения в новых реализациях. |
| 23 | SHOULD | ❌ not_found | It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations. | - | Код не поддерживает deprecated значение "logging" для логов экспортера - только "otlp" и "none". Это соответствует рекомендации не поддерживать deprecated значения в новых реализациях. |

#### Declarative configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#declarative-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ verified | When OTEL_CONFIG_FILE is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored. | src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os, src/Конфигурация/Модули/ОтелПодстановкаПеременных.os | Реализовано: YAML-парсинг с подстановкой переменных окружения, 12 DTO-классов дата-модели. |

## Требования Development-статуса

Эти требования находятся в секциях со статусом Development. Их реализация не обязательна для соответствия стабильной спецификации.

### Resource Sdk

#### Resource detector name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-detector-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ➖ n_a | Resource detectors SHOULD have a unique name for reference in configuration. | - | Условная фича Resource Detector Naming не реализована в данном SDK - детекторы не имеют именования для конфигурации. |
| 2 | SHOULD | ➖ n_a | Names SHOULD be snake case and consist of lowercase alphanumeric and `_` characters, which ensures they conform to declarative configuration property name requirements. | - | Условная фича Resource Detector Naming не реализована в данном SDK. |
| 3 | SHOULD | ➖ n_a | Resource detector names SHOULD reflect the root namespace of attributes they populate. | - | Условная фича Resource Detector Naming не реализована в данном SDK. |
| 4 | SHOULD | ➖ n_a | Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name which appropriately conveys their purpose. | - | Условная фича Resource Detector Naming не реализована в данном SDK. |
| 5 | SHOULD | ➖ n_a | An SDK which identifies multiple resource detectors with the same name SHOULD report an error. | - | Условная фича Resource Detector Naming не реализована в данном SDK. |
| 6 | SHOULD | ➖ n_a | In order to limit collisions, resource detectors SHOULD document their name in a manner which is easily discoverable. | - | Условная фича Resource Detector Naming не реализована в данном SDK. |

### Trace Api

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when creating `Span`s, a `Tracer` SHOULD provide this `Enabled` API. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 2 | MUST | ✅ found | There are currently no required parameters for this API. Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 3 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` |  |
| 4 | SHOULD | ⚠️ partial | The API SHOULD be documented that instrumentation authors needs to call this API each time they create a new `Span` to ensure they have the most up-to-date response. | `src/Трассировка/Классы/ОтелТрассировщик.os:31` | Метод Включен() документирован, но не содержит указания вызывать его каждый раз перед созданием нового спана и что значение может меняться со временем. |

### Trace Sdk

#### Tracer Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` (see API). | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:47` |  |
| 2 | MUST | ✅ found | The `TracerProvider` MUST implement the Get a Tracer API. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:63` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Tracer`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:74` |  |
| 4 | MUST | ✅ found | The `TracerProvider` MUST compute the relevant TracerConfig using the configured TracerConfigurator, and create a `Tracer` whose behavior conforms to that `TracerConfig`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:82` |  |

#### TracerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: * `tracer_scope`: The `InstrumentationScope` of the `Tracer`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:280` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `TracerConfig`, or some signal indicating that the default TracerConfig should be used. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:275` |  |

#### Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Tracer` MUST behave according to the TracerConfig computed during Tracer creation. | `src/Трассировка/Классы/ОтелТрассировщик.os:39` |  |
| 2 | MUST | ✅ found | the `Tracer` MUST be updated to behave according to the new `TracerConfig`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:154` |  |

#### TracerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the `enabled` parameter SHOULD default to `true` (i.e. `Tracer`s are enabled by default). | `src/Трассировка/Классы/ОтелКонфигурацияТрассировщика.os:35` |  |
| 2 | MUST | ✅ found | If a `Tracer` is disabled, it MUST behave equivalently to a No-op Tracer. | `src/Трассировка/Классы/ОтелТрассировщик.os:57` |  |
| 3 | MUST | ⚠️ partial | The value of `enabled` MUST be used to resolve whether a `Tracer` is Enabled. If `enabled` is `false`, `Enabled` returns `false`. If `enabled` is `true`, `Enabled` returns `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:38` | When enabled is false, Включен() correctly returns false. However, when enabled is true (or no config), Включен() returns Провайдер.Процессор().ЕстьПроцессоры() instead of true. The spec requires that if enabled is true, Enabled returns true unconditionally. |
| 4 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Трассировка/Классы/ОтелТрассировщик.os:191` |  |

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
| 1 | MUST | ✅ found | The `TraceIdRatioBased` MUST ignore the parent `SampledFlag`. | `src/Трассировка/Модули/ОтелСэмплер.os:240-241` |  |
| 2 | MUST | ✅ found | Description MUST return a string of the form `"TraceIdRatioBased{RATIO}"` with `RATIO` replaced with the Sampler instance's trace sampling ratio represented as a decimal number. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 3 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 4 | SHOULD | ✅ found | and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:113` |  |
| 5 | MUST | ✅ found | The sampling algorithm MUST be deterministic. | `src/Трассировка/Модули/ОтелСэмплер.os:277-298` |  |
| 6 | MUST | ✅ found | implementations MUST use a deterministic hash of the `TraceId` when computing the sampling decision. | `src/Трассировка/Модули/ОтелСэмплер.os:290-291` |  |
| 7 | MUST | ✅ found | A `TraceIdRatioBased` sampler with a given sampling probability MUST also sample all traces that any `TraceIdRatioBased` sampler with a lower sampling probability would sample. | `src/Трассировка/Модули/ОтелСэмплер.os:292-296` |  |
| 8 | SHOULD | ❌ not_found | When this sampler observes a non-empty parent span context, meaning when it is used not as a root sampler, the SDK SHOULD emit a warning such as: | - | No warning is emitted when TraceIdRatioBased sampler is used as a child sampler with a non-empty parent span context. The sampler simply processes the request without any deprecation/compatibility warning. |

#### ProbabilitySampler

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#probabilitysampler)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | The `ProbabilitySampler` sampler MUST ignore the parent `SampledFlag`. | - | No ProbabilitySampler implementation exists. The codebase only implements TraceIdRatioBased (ПоДолеТрассировок), AlwaysOn/AlwaysOff, and ParentBased samplers. ProbabilitySampler as a separate W3C TC Level 2-based sampler is not implemented. |
| 2 | SHOULD | ❌ not_found | When (R >= T), the OpenTelemetry TraceState SHOULD be modified to include the key-value `th:T` for rejection threshold value (T), as specified for the OpenTelemetry TraceState `th` sub-key. | - | No ProbabilitySampler implementation exists. No threshold (th) sub-key is written to TraceState during sampling decisions. |
| 3 | SHOULD | ❌ not_found | When a ProbabilitySampler Sampler makes a decision for a non-root Span using TraceID randomness when the Trace random flag was not set, the SDK SHOULD issue a warning statement in its log with a compatibility warning. | - | No ProbabilitySampler implementation exists. No compatibility warning logic for non-root spans with missing Random flag. |

#### AlwaysRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwaysrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | Based on the decision from the wrapped root sampler, `AlwaysRecord` MUST behave as follows: | - | No AlwaysRecord sampler decorator is implemented. There is no mechanism to convert DROP decisions into RECORD_ONLY decisions. The codebase has only AlwaysOn (ВсегдаВключен), AlwaysOff (ВсегдаВыключен), TraceIdRatioBased (ПоДолеТрассировок), and ParentBased (НаОсновеРодителя) samplers. |

#### CompositeSampler

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#compositesampler)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the parameters passed to delegate GetSamplingIntent methods, as they are considered read-only state. | - | No ComposableSampler or CompositeSampler interface is implemented. The codebase has no GetSamplingIntent method or SamplingIntent structure. |
| 2 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the OpenTelemetry TraceState (i.e., the `ot` sub-key of TraceState). | - | No ComposableSampler implementation exists. There is no composable sampler architecture that would need to enforce TraceState immutability. |
| 3 | SHOULD | ❌ not_found | The calling CompositeSampler SHOULD update the threshold of the outgoing TraceState (unless `!threshold_reliable`) | - | No CompositeSampler implementation exists. No threshold update logic for outgoing TraceState. |
| 4 | MUST | ❌ not_found | and that the explicit randomness values MUST not be modified. | - | No CompositeSampler implementation exists. No randomness value handling in TraceState context. |
| 5 | SHOULD | ❌ not_found | For the zero case a `ComposableAlwaysOff` instance SHOULD be returned instead. | - | No ComposableProbability or ComposableAlwaysOff implementation exists. The entire composable sampler architecture (ComposableSampler, CompositeSampler, ComposableAlwaysOn/Off/Probability/ParentThreshold/RuleBased/Annotating) is not implemented. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | Custom implementations of the `IdGenerator` SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace `random` flag will be set in the associated Trace contexts. | - | Нет механизма для IdGenerator сообщать SDK о соответствии W3C Level 2 randomness requirements или установки random flag в TraceContext. Интерфейс IdGenerator не предусматривает такую функциональность. |

#### OnEnding

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onending)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The end timestamp MUST have been computed (the `OnEnding` method duration is not included in the span duration). | `src/Трассировка/Классы/ОтелСпан.os:462` |  |
| 2 | MUST | ✅ found | The Span object MUST still be mutable (i.e., `SetAttribute`, `AddLink`, `AddEvent` can be called) while `OnEnding` is called. | `src/Трассировка/Классы/ОтелСпан.os:467` |  |
| 3 | MUST | ✅ found | This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:467` |  |
| 4 | MUST | ✅ found | The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking `OnEnding` of the first `SpanProcessor`. | `src/Трассировка/Классы/ОтелСпан.os:467` |  |

### Logs Api

#### Ergonomic API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#ergonomic-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | The ergonomic API SHOULD make it more convenient to emit event records following the event semantics. | - | No ergonomic API found. The SDK only provides the basic Logger.СоздатьЗаписьЛога() and Logger.Записать() methods. There are no convenience methods like logger.info(), logger.error(), etc. for direct event emission. |
| 2 | SHOULD | ❌ not_found | The design of the ergonomic API SHOULD be idiomatic for its language. | - | No ergonomic API is implemented to evaluate idiomaticity. The existing API follows OneScript naming conventions but lacks convenient logging methods typical for the platform. |

### Logs Sdk

#### Logger Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create Logger instances through a LoggerProvider (see API). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 2 | MUST | ✅ found | The LoggerProvider MUST implement the Get a Logger API. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:54` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Logger. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:70` |  |
| 4 | MUST | ✅ found | In the case where an invalid name (null or empty string) is specified, a working Logger MUST be returned as a fallback rather than returning null or throwing an exception | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:59` |  |
| 5 | SHOULD | ✅ found | its name SHOULD keep the original invalid value | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:60` |  |
| 6 | SHOULD | ✅ found | and a message reporting that the specified value is invalid SHOULD be logged. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:60` |  |
| 7 | MUST | ✅ found | The LoggerProvider MUST compute the relevant LoggerConfig using the configured LoggerConfigurator, and create a Logger whose behavior conforms to that LoggerConfig. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:75` |  |

#### LoggerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: logger_scope: The InstrumentationScope of the Logger. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:78` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant LoggerConfig, or some signal indicating that the default LoggerConfig should be used. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:206` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Logger MUST behave according to the LoggerConfig computed during logger creation. | `src/Логирование/Классы/ОтелЛоггер.os:42-61` |  |
| 2 | MUST | ✅ found | If the LoggerProvider supports updating the LoggerConfigurator, then upon update the Logger MUST be updated to behave according to the new LoggerConfig. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:160-163` |  |

#### LoggerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the enabled parameter SHOULD default to true (i.e. Loggers are enabled by default). | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 2 | MUST | ✅ found | If a Logger is disabled, it MUST behave equivalently to No-op Logger. | `src/Логирование/Классы/ОтелЛоггер.os:50-51,144-145` |  |
| 3 | MUST | ✅ found | If not explicitly set, the minimum_severity parameter MUST default to 0. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 4 | MUST | ✅ found | If a log records SeverityNumber is specified (i.e. not 0) and is less than the configured minimum_severity, the log record MUST be dropped by the Logger. | `src/Логирование/Классы/ОтелЛоггер.os:147-151` |  |
| 5 | MUST | ✅ found | If not explicitly set, the trace_based parameter MUST default to false. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:67` |  |
| 6 | MUST | ✅ found | If trace_based is true, log records associated with unsampled traces MUST be dropped by the Logger. | `src/Логирование/Классы/ОтелЛоггер.os:152-154` |  |
| 7 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:160-163` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If Observed Timestamp is unspecified, the implementation SHOULD set it equal to the current time. | `src/Логирование/Классы/ОтелЛоггер.os:102-104` |  |
| 2 | MUST | ✅ found | If an Exception is provided, the SDK MUST by default set attributes from the exception on the LogRecord with the conventions outlined in the exception semantic conventions. | `src/Логирование/Классы/ОтелЛоггер.os:179-190` |  |
| 3 | MUST | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:192-196` |  |
| 4 | MUST NOT | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:192-196` |  |
| 5 | MUST | ✅ found | Before processing a log record, the implementation MUST apply the filtering rules defined by the LoggerConfig. | `src/Логирование/Классы/ОтелЛоггер.os:93-96` |  |
| 6 | MUST | ✅ found | If the log records SeverityNumber is specified (i.e. not 0) and is less than the configured minimum_severity, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:147-151` |  |
| 7 | MUST | ✅ found | If trace_based is true, and if the log record has a SpanId and the TraceFlags SAMPLED flag is unset, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:152-154` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Enabled MUST return false when either: there are no registered LogRecordProcessors, Logger is disabled (LoggerConfig.enabled is false), the provided severity is specified (i.e. not 0) and is less than the configured minimum_severity in the LoggerConfig, trace_based is true in the LoggerConfig and the current context is associated with an unsampled trace, all registered LogRecordProcessors implement Enabled, and a call to Enabled on each of them returns false. | `src/Логирование/Классы/ОтелЛоггер.os:42-62` |  |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return true. | `src/Логирование/Классы/ОтелЛоггер.os:61` |  |

### Metrics Api

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | OpenTelemetry SDKs MUST handle `advisory` parameters as described here. | `src/Метрики/Классы/ОтелМетр.os:687-706` |  |

### Metrics Sdk

#### Meter Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create `Meter` instances through a `MeterProvider` (see API). | `src/Метрики/Классы/ОтелПровайдерМетрик.os:59` |  |
| 2 | MUST | ✅ found | The `MeterProvider` MUST implement the Get a Meter API. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:59` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:75` |  |
| 4 | MUST | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:64` |  |
| 5 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:65` |  |
| 6 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the original invalid value, and a message reporting that the specified value is invalid SHOULD be logged. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:65` |  |
| 7 | MUST | ✅ found | The `MeterProvider` MUST compute the relevant MeterConfig using the configured MeterConfigurator, and create a `Meter` whose behavior conforms to that `MeterConfig`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:86` |  |

#### MeterConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The function MUST accept the following parameter: * `meter_scope`: The `InstrumentationScope` of the `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:262` |  |
| 2 | MUST | ✅ found | The function MUST return the relevant `MeterConfig`, or some signal indicating that the default MeterConfig should be used. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:262` |  |

#### Start timestamps

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#start-timestamps)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp, or the creation time of the instrument if this is the first collection interval for the instrument. | - | Start timestamp handling for delta aggregations not fully implemented according to spec |
| 2 | MUST | ⚠️ partial | This implies that all data points with delta temporality aggregation for an instrument MUST share the same start timestamp. | - | Delta temporality start timestamp consistency not enforced |
| 3 | MUST | ⚠️ partial | Cumulative timeseries MUST use a consistent start timestamp for all collection intervals. | - | Cumulative start timestamp consistency not fully implemented |
| 4 | SHOULD | ⚠️ partial | For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the series. | - | Start timestamp tracking for first measurement not implemented |
| 5 | SHOULD | ⚠️ partial | For asynchronous instrument, the start timestamp SHOULD be the creation time of the instrument, if the first series measurement occurred in the first collection interval, otherwise the timestamp of the collection interval prior to the first series measurement. | - | Complex start timestamp logic for asynchronous instruments not implemented |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:56-60` |  |
| 2 | MUST | ✅ found | `Meter` MUST behave according to the MeterConfig computed during Meter creation. | `src/Метрики/Классы/ОтелМетр.os:428` |  |
| 3 | MUST | ❌ not_found | If the `MeterProvider` supports updating the MeterConfigurator, then upon update the `Meter` MUST be updated to behave according to the new `MeterConfig`. | - | MeterProvider does not support updating MeterConfigurator. The конфигураторМетров callback is only called once during meter creation, not dynamically updated |

#### MeterConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the `enabled` parameter SHOULD default to `true` (i.e. `Meter`s are enabled by default). | `src/Метрики/Классы/ОтелКонфигурацияМетра.os:35` |  |
| 2 | MUST | ✅ found | If a `Meter` is disabled, it MUST behave equivalently to No-op Meter. | `src/Метрики/Классы/ОтелМетр.os:428` |  |
| 3 | MUST | ✅ found | The value of `enabled` MUST be used to resolve whether an instrument is Enabled. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:34` |  |
| 4 | MUST | ✅ found | However, the changes MUST be eventually visible. | `src/Метрики/Классы/ОтелМетр.os:364` |  |

#### Instrument enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The synchronous instrument `Enabled` MUST return `false` when either: | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:231` |  |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return `true` | `/home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:232` |  |

#### MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | To construct a MetricReader when setting up an SDK, at least the following SHOULD be provided: The exporter to use, which is a MetricExporter instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:8` |  |
| 2 | SHOULD | ⚠️ partial | This function SHOULD be obtained from the exporter. | - | Default aggregation is not obtained from exporter - it is hardcoded in SDK |
| 3 | SHOULD | ✅ found | If not configured, the default aggregation SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:29` |  |
| 4 | SHOULD | ⚠️ partial | This function SHOULD be obtained from the exporter. | - | Temporality is not obtained from exporter - it is hardcoded in SDK |
| 5 | SHOULD | ✅ found | If not configured, the Cumulative temporality SHOULD be used. | `src/Метрики/Модули/ОтелВременнаяАгрегация.os` |  |
| 6 | SHOULD | ✅ found | If not configured, a default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:28` |  |
| 7 | SHOULD | ✅ found | A MetricReader SHOULD provide the MetricFilter to the SDK or registered MetricProducer(s) when calling the Produce operation. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:127` |  |
| 8 | SHOULD | ✅ found | A common implementation of MetricReader, the periodic exporting MetricReader SHOULD be provided to be used typically with push-based metrics collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:1` |  |
| 9 | MUST | ✅ found | The MetricReader MUST ensure that data points from OpenTelemetry instruments are output in the configured aggregation temporality for each instrument kind. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:253-265` |  |
| 10 | MUST | ✅ found | For synchronous instruments with Cumulative aggregation temporality, MetricReader.Collect MUST receive data points exposed in previous collections regardless of whether new measurements have been recorded. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:250-256` |  |
| 11 | MUST | ✅ found | For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:250-256` |  |
| 12 | MUST | ✅ found | For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:250-256` |  |
| 13 | MUST | ✅ found | For instruments with Cumulative aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST repeat the same starting timestamps. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:262-265` |  |
| 14 | MUST | ✅ found | For instruments with Delta aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST advance the starting timestamp. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:262-265` |  |
| 15 | MUST | ✅ found | The ending timestamp (i.e. TimeUnixNano) MUST always be equal to time the metric data point took effect, which is equal to when MetricReader.Collect was invoked. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:130` |  |
| 16 | MUST | ✅ found | The SDK MUST support multiple MetricReader instances to be registered on the same MeterProvider. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:42-45` |  |
| 17 | SHOULD NOT | ✅ found | The MetricReader.Collect invocation on one MetricReader instance SHOULD NOT introduce side-effects to other MetricReader instances. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:101` |  |
| 18 | MUST NOT | ✅ found | The SDK MUST NOT allow a MetricReader instance to be registered on more than one MeterProvider instance. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:153-159` |  |
| 19 | SHOULD | ✅ found | The SDK SHOULD provide a way to allow MetricReader to respond to MeterProvider.ForceFlush and MeterProvider.Shutdown. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94-96,138-139` |  |

#### Produce batch

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#produce-batch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Produce MUST return a batch of Metric Points, filtered by the optional metricFilter parameter. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13` |  |
| 2 | SHOULD | ⚠️ partial | Implementation SHOULD use the filter as early as possible to gain as much performance gain possible (memory allocation, internal metric fetching, etc). | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13` | The interface accepts ФильтрМетрик as an optional parameter and the reader passes it to producers (line 366 of ОтелПериодическийЧитательМетрик.os), but the default interface implementation returns an empty array without using the filter. |
| 3 | SHOULD | ❌ not_found | If the batch of Metric Points includes resource information, Produce SHOULD require a resource as a parameter. | - | Произвести(ФильтрМетрик) has no Resource parameter. The interface only accepts ФильтрМетрик. |
| 4 | SHOULD | ❌ not_found | Produce SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Произвести() returns Массив (array of ОтелДанныеМетрики). There is no mechanism to communicate success/failure/timeout status to the caller, only exceptions. |
| 5 | SHOULD | ❌ not_found | Produce SHOULD include a single InstrumentationScope which identifies the MetricProducer. | - | ИнтерфейсПродюсерМетрик has no mechanism to associate an InstrumentationScope with the MetricProducer itself. The default implementation returns an empty array. |

## Условные требования (Conditional)

Требования из условных секций. Применяются только при реализации соответствующей опциональной фичи.

### Сводка условных секций

| Раздел | Секция | Scope | Stability | Keywords | Ссылка |
|---|---|---|---|---|---|
| Resource Sdk | Resource detector name | conditional:Resource Detector Naming (conditional) | Development | 6 | [spec](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-detector-name) |

## Ограничения платформы OneScript

| Ограничение | Влияние на спецификацию | Решение |
|---|---|---|
| Нет наносекундной точности | Временные метки с точностью до миллисекунд | Используется миллисекундная точность |
| Нет TLS/mTLS из SDK | Сертификаты конфигурируются вне SDK | Делегировано системе/прокси |
| Нет opaque-объектов | Ключи контекста - строки | Строковые константы как ключи |
| Нет thread-local | ФоновыеЗадания вместо goroutines | Передача контекста через параметры |
| Число = System.Decimal (не IEEE 754) | NaN, Infinity, отрицательный ноль невозможны | Операции, порождающие NaN/Inf, выбрасывают исключение - требования к обработке NaN/Inf неприменимы |

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
| Conditional секций | 1 |
| Всего keywords | 824 |
| Stable universal keywords | 701 |

