# Анализ соответствия спецификации OpenTelemetry v1.55.0

> **Версия спецификации**: [v1.55.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-04-08
> **Методология**: spec-first - извлечены все MUST/SHOULD требования из спецификации, затем каждое прослежено до кода

## Сводка (Stable)

Учитываются только требования из стабильных разделов спецификации с универсальной областью применения.

| Показатель | Значение |
|---|---|
| Всего keywords в спецификации | 824 |
| Stable + universal keywords | 660 |
| Conditional keywords | 23 |
| Development keywords | 156 |
| Найдено требований (Stable universal) | 625 |
| ✅ Реализовано (found) | 449 (71.8%) |
| ⚠️ Частично (partial) | 90 (14.4%) |
| ❌ Не реализовано (not_found) | 84 (13.4%) |
| ➖ Неприменимо (n_a) | 2 |
| **MUST/MUST NOT found** | 313/370 (84.6%) |
| **SHOULD/SHOULD NOT found** | 136/253 (53.8%) |

## Соответствие по разделам (Stable)

| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |
|---|---|---|---|---|---|---|
| Context | 7 | 1 | 0 | 0 | 8 | 87.5% |
| Baggage Api | 17 | 0 | 0 | 0 | 17 | 100.0% |
| Resource Sdk | 12 | 3 | 0 | 0 | 15 | 80.0% |
| Trace Api | 105 | 11 | 4 | 0 | 120 | 87.5% |
| Trace Sdk | 52 | 15 | 8 | 0 | 75 | 69.3% |
| Logs Api | 19 | 1 | 1 | 0 | 21 | 90.5% |
| Logs Sdk | 40 | 10 | 5 | 0 | 55 | 72.7% |
| Metrics Api | 61 | 5 | 8 | 0 | 74 | 82.4% |
| Metrics Sdk | 95 | 29 | 43 | 1 | 168 | 56.5% |
| Otlp Exporter | 14 | 5 | 5 | 1 | 25 | 56.0% |
| Propagators | 19 | 7 | 6 | 0 | 32 | 59.4% |
| Env Vars | 8 | 3 | 4 | 0 | 15 | 53.3% |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ✅ **[Context]** [MUST] A Context MUST be immutable  
  Контекст реализован как ФиксированноеСоответствие (иммутабельный). Все операции создают новую копию. (`src/Ядро/Модули/ОтелКонтекст.os`)

- ✅ **[Context]** [MUST] The API MUST accept the following parameter: The key name. The key name exists for debugging purposes and does not uniquely identify the key.  
  ОтелКонтекст.СоздатьКлюч(Имя) - создает ОтелКлючКонтекста с именем для отладки. (`src/Ядро/Модули/ОтелКонтекст.os:35`)

- ✅ **[Context]** [MUST] The API MUST return an opaque object representing the newly created key  
  Возвращает ОтелКлючКонтекста - непрозрачный объект, сравнение по ссылке. (`src/Ядро/Классы/ОтелКлючКонтекста.os`)

- ✅ **[Context]** [MUST] The API MUST accept the following parameters: The Context. The key.  
  ПолучитьИзКонтекста(Контекст, Ключ) - generic get с явным контекстом и ОтелКлючКонтекста. (`src/Ядро/Модули/ОтелКонтекст.os`)

- ✅ **[Context]** [MUST] The API MUST accept the following parameters: The Context. The key. The value to be set.  
  КонтекстСоЗначением(Контекст, Ключ, Значение) - generic set с явным контекстом. (`src/Ядро/Модули/ОтелКонтекст.os`)

- ✅ **[Context]** [MUST] The API MUST return a new Context containing the new value  
  КонтекстСоЗначением() возвращает новый ФиксированноеСоответствие. (`src/Ядро/Модули/ОтелКонтекст.os`)

- ⚠️ **[Context]** [MUST] The API MUST accept the following parameters: The Context.  
  There is no generic Attach(Context) method that accepts a Context (Соответствие) as a single parameter. Instead, the code provides specialized methods: УстановитьЗначение(Ключ, Значение) at line 147, СделатьСпанТекущим(Спан) at line 163, and СделатьBaggageТекущим(Багаж) at line 176 — none of which accept a whole Context object as the spec requires. (`src/Ядро/Модули/ОтелКонтекст.os:147`)

- ✅ **[Resource Sdk]** [MUST] Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK.  
  Три отдельных класса-детектора: ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, ОтелДетекторРесурсаПроцессора. (`src/Ядро/Классы/`)

- ✅ **[Resource Sdk]** [MUST] Resource detector packages MUST provide a method that returns a resource. This can then be associated with TracerProvider or MeterProvider instances.  
  Каждый детектор имеет метод Обнаружить(), возвращающий ОтелРесурс. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17`)

- ⚠️ **[Resource Sdk]** [MUST] Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions.  
  Детекторы вынесены в отдельные классы, но Schema URL пока не устанавливается. (`src/Ядро/Классы/ОтелДетекторРесурсаХоста.os`)

- ✅ **[Resource Sdk]** [MUST] If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources.  
  Используется ОтелРесурс.Слить(), который обрабатывает конфликт Schema URL (возвращает пустой ресурс при различных непустых URL). (`src/Ядро/Классы/ОтелРесурс.os:45`)

- ⚠️ **[Trace Api]** [MUST] In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception  
  ПолучитьТрассировщик принимает пустую строку и создает рабочий трассировщик, но нет явной проверки на пустое/null имя и нет логирования предупреждения (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52`)

- ✅ **[Trace Api]** [MUST] Binary - returns the binary representation of the TraceId (result MUST be a 16-byte array)  
  Метод ИдТрассировкиВДвоичномВиде() добавлен в ОтелКонтекстСпана, возвращает бинарное представление TraceId как 16-байтовый массив. (`src/Трассировка/Классы/ОтелКонтекстСпана.os`)

- ✅ **[Trace Api]** [MUST] Binary - returns the binary representation of the SpanId (result MUST be an 8-byte array)  
  Метод ИдСпанаВДвоичномВиде() добавлен в ОтелКонтекстСпана, возвращает бинарное представление SpanId как 8-байтовый массив. (`src/Трассировка/Классы/ОтелКонтекстСпана.os`)

- ⚠️ **[Trace Api]** [MUST NOT] alternative implementations MUST NOT allow callers to create Spans directly  
  OneScript не поддерживает модификаторы доступа - все конструкторы публичны. Пользователь технически может вызвать Новый ОтелСпан(...) напрямую, хотя дизайн API направляет через Трассировщик (`src/Трассировка/Классы/ОтелТрассировщик.os:48`)

- ⚠️ **[Trace Api]** [MUST] All Spans MUST be created via a Tracer  
  Дизайн API направляет через Трассировщик (НачатьСпан, НачатьДочернийСпан, НачатьКорневойСпан, ПостроительСпана), но OneScript не может запретить прямое создание через конструктор из-за отсутствия модификаторов доступа (`src/Трассировка/Классы/ОтелТрассировщик.os:48`)

- ⚠️ **[Trace Api]** [MUST NOT] There MUST NOT be any API for creating a Span other than with a Tracer  
  Все штатные API создания спана идут через Трассировщик, но конструктор ОтелСпан публичен из-за ограничений OneScript (нет модификаторов доступа) (`src/Трассировка/Классы/ОтелТрассировщик.os:48`)

- ⚠️ **[Trace Api]** [MUST NOT] This API MUST NOT accept a Span or SpanContext as parent, only a full Context  
  SpanBuilder.УстановитьРодителя() принимает ОтелСпан или ОтелКонтекстСпана напрямую, а не полный Context (Соответствие). Также Трассировщик.НачатьДочернийСпан() принимает Span/SpanContext. Неявное использование контекста в НачатьСпан() работает корректно (`src/Трассировка/Классы/ОтелПостроительСпана.os:33`)

- ✅ **[Trace Api]** [MUST] The API documentation MUST state that adding attributes at span creation is preferred to calling SetAttribute later, as samplers can only consider information already present during span creation  
  Документация добавлена в ОтелПостроительСпана - указано, что установка атрибутов при создании спана предпочтительнее вызова SetAttribute позже, т.к. семплеры учитывают только данные, доступные при создании. (`src/Трассировка/Классы/ОтелПостроительСпана.os`)

- ✅ **[Trace Api]** [MUST] Also, the child span MUST inherit all TraceState values of its parent by default  
  Дочерние спаны теперь наследуют TraceState родителя. ОтелТрассировщик.ОпределитьСостояниеТрассировки() разрешает TraceState из результата семплирования или родителя и передает в конструктор ОтелСпан → ОтелКонтекстСпана. (`src/Трассировка/Классы/ОтелТрассировщик.os`)

- ✅ **[Trace Api]** [MUST] The API documentation MUST state that adding links at span creation is preferred to calling AddLink later, for contexts that are available during span creation, because head sampling decisions can only consider information present during span creation.  
  Документация добавлена в ОтелПостроительСпана - указано, что добавление линков при создании спана предпочтительнее вызова AddLink позже, т.к. решения head sampling учитывают только данные, доступные при создании. (`src/Трассировка/Классы/ОтелПостроительСпана.os`)

- ✅ **[Trace Api]** [MUST] TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  Добавлена документация потокобезопасности в ОтелПровайдерТрассировки. Используется СинхронизированнаяКарта для кэша трассировщиков, АтомарноеБулево для флага закрытия. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os`)

- ✅ **[Trace Api]** [MUST] Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  Добавлена документация потокобезопасности в ОтелТрассировщик. Трассировщик делегирует вызовы в потокобезопасный провайдер. (`src/Трассировка/Классы/ОтелТрассировщик.os`)

- ✅ **[Trace Api]** [MUST] Span - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  Добавлена документация потокобезопасности в ОтелСпан. Документация описывает гарантии конкурентного доступа к методам спана. (`src/Трассировка/Классы/ОтелСпан.os`)

- ✅ **[Trace Api]** [MUST] Event - Events are immutable and MUST be safe for concurrent use by default.  
  Добавлена документация в ОтелСобытиеСпана о неизменяемости и потокобезопасности. Объект фактически неизменяем после создания (нет методов-мутаторов). (`src/Трассировка/Классы/ОтелСобытиеСпана.os`)

- ✅ **[Trace Api]** [MUST] The API MUST return a non-recording Span with the SpanContext in the parent Context (whether explicitly given or implicit current).  
  При отклонении семплером возвращается NoopSpan с traceId родителя. ОтелГлобальный.ПроверитьИнициализацию() теперь лениво создаёт noop SDK (с пустыми провайдерами) вместо исключения, поэтому без настроенного SDK также возвращается non-recording span. (`src/Трассировка/Классы/ОтелТрассировщик.os:63`, `src/Ядро/Модули/ОтелГлобальный.os`)

- ⚠️ **[Trace Sdk]** [MUST] For backwards compatibility it MUST also be able to access the InstrumentationLibrary [deprecated since 1.10.0] having the same name and version values as the InstrumentationScope.  
  Нет отдельного InstrumentationLibrary (deprecated alias). Есть только ОбластьИнструментирования, что по сути то же самое, но без явного deprecated alias. (`src/Трассировка/Классы/ОтелСпан.os:162`)

- ✅ **[Trace Sdk]** [MUST NOT] RECORD_ONLY - IsRecording will be true, but the Sampled flag MUST NOT be set.  
  ОтелТрассировщик.ВычислитьФлагиТрассировки() теперь возвращает 0 для RECORD_ONLY и 1 только для RECORD_AND_SAMPLED. Флаги передаются в конструктор ОтелСпан → ОтелКонтекстСпана. (`src/Трассировка/Классы/ОтелТрассировщик.os`)

- ✅ **[Trace Sdk]** [MUST NOT] SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value (the rv sub-key).  
  SDK не перезаписывает подключ rv в TraceState. Дочерние спаны теперь наследуют TraceState родителя через ОтелТрассировщик.ОпределитьСостояниеТрассировки(), что сохраняет rv. (`src/Трассировка/Классы/ОтелТрассировщик.os`)

- ✅ **[Trace Sdk]** [MUST] To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per discarded attribute, event, or link).  
  Добавлен флаг ПредупреждениеОтброшенныхВыведено и логгер Лог. При отбрасывании атрибутов, событий или линков выводится одно предупреждение на спан через ВывестиПредупреждениеОбОтброшенныхДанных(). (`src/Трассировка/Классы/ОтелСпан.os`)

- ✅ **[Trace Sdk]** [MUST] The SpanProcessor interface MUST declare the following methods: OnStart, OnEnd, Shutdown, ForceFlush.  
  ИнтерфейсПроцессорСпанов определяет все 4 метода через &Интерфейс из extends. (`src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os`)

- ❌ **[Trace Sdk]** [MUST] If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls.  
  СброситьБуфер() (ForceFlush) does not accept a timeout parameter. It calls ЭкспортироватьВсеПакеты() which loops until the buffer is empty with no timeout mechanism. (-)

- ✅ **[Trace Sdk]** [MUST] The processor MUST synchronize calls to Span Exporter's Export to make sure that they are not invoked concurrently. (Simple processor)  
  Добавлена БлокировкаЭкспорта (БлокировкаРесурса) вокруг вызова Экспортер.Экспортировать() в ОтелПростойПроцессорСпанов.ПриЗавершении. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os`)

- ✅ **[Trace Sdk]** [MUST] The processor MUST synchronize calls to Span Exporter's Export to make sure that they are not invoked concurrently. (Batching processor)  
  Добавлена БлокировкаЭкспорта (БлокировкаРесурса) вокруг вызова Экспортер.Экспортировать() в ОтелБазовыйПакетныйПроцессор. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os`)

- ❌ **[Trace Sdk]** [MUST] Each implementation MUST document the concurrency characteristics the SDK requires of the exporter.  
  В коде ОтелЭкспортерСпанов и транспортов нет документации о требованиях к конкурентности, которые SDK предъявляет к экспортеру. (-)

- ✅ **[Trace Sdk]** [MUST] Tracer Provider - Tracer creation, ForceFlush and Shutdown MUST be safe to be called concurrently.  
  Создание трассировщиков потокобезопасно через СинхронизированнаяКарта. Закрыть() использует АтомарноеБулево с СравнитьИУстановить(Ложь, Истина) для однократного выполнения. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os`)

- ⚠️ **[Trace Sdk]** [MUST] Span processor - all methods MUST be safe to be called concurrently.  
  Вызовы Export синхронизированы через БлокировкаЭкспорта в обоих процессорах. Однако другие методы (ПриНачале, СброситьБуфер, Закрыть) не имеют полной синхронизации. Добавлена документация потокобезопасности. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os`, `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os`)

- ⚠️ **[Trace Sdk]** [MUST] Span Exporter - ForceFlush and Shutdown MUST be safe to be called concurrently.  
  Добавлена документация потокобезопасности в ОтелЭкспортерСпанов. СброситьБуфер - no-op, безопасен. Однако Закрыть() использует обычный флаг Закрыт без атомарной операции - конкурентный вызов может привести к гонке. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os`)

- ✅ **[Logs Api]** [MUST] LoggerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default.  
  Добавлена документация потокобезопасности в ОтелПровайдерЛогирования. Кэш логгеров использует СинхронизированнаяКарта, флаг закрытия - АтомарноеБулево. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os`)

- ✅ **[Logs Sdk]** [MUST] Configuration (i.e. LogRecordProcessors and (Development) LoggerConfigurator) MUST be owned by the LoggerProvider.  
  Конфигуратор (Действие callback) добавлен как поле ОтелПровайдерЛогирования. Создан класс ОтелКонфигурацияЛоггера. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os:21`)

- ✅ **[Logs Sdk]** [MUST] A function receiving this as an argument MUST additionally be able to modify the following information added to the LogRecord: Timestamp, ObservedTimestamp, SeverityText, SeverityNumber, Body, Attributes (addition, modification, removal), TraceId, SpanId, TraceFlags, EventName.  
  Все поля модифицируемы, включая SeverityText - добавлен отдельный метод УстановитьТекстСерьезности() для независимой установки SeverityText от SeverityNumber. (`src/Логирование/Классы/ОтелЗаписьЛога.os`)

- ✅ **[Logs Sdk]** [MUST] To prevent excessive logging, the message MUST be printed at most once per LogRecord (i.e., not per discarded attribute).  
  Добавлен флаг ПредупреждениеОтброшенныхВыведено и логгер Лог. При отбрасывании атрибутов выводится одно предупреждение на запись лога через ВывестиПредупреждениеОбОтброшенныхДанных(). (`src/Логирование/Классы/ОтелЗаписьЛога.os`)

- ⚠️ **[Logs Sdk]** [MUST NOT] Any modifications to parameters inside Enabled MUST NOT be propagated to the caller. Parameters are immutable or passed by value.  
  Logger.Включен не модифицирует параметры, но у LogRecordProcessor нет собственного метода Enabled. Logger.Включен не делегирует вызов в процессор - вместо этого проверяет только ЕстьПроцессоры(). Отдельный интерфейс Enabled на уровне LogRecordProcessor отсутствует. (`src/Логирование/Классы/ОтелЛоггер.os:41`)

- ✅ **[Logs Sdk]** [MUST] The Simple processor MUST synchronize calls to LogRecordExporter's Export to make sure that they are not invoked concurrently.  
  Добавлена БлокировкаЭкспорта (БлокировкаРесурса) вокруг вызова Экспортер.Экспортировать() в ОтелПростойПроцессорЛогов.ПриПоявлении. (`src/Логирование/Классы/ОтелПростойПроцессорЛогов.os`)

- ✅ **[Logs Sdk]** [MUST] The Batching processor MUST synchronize calls to LogRecordExporter's Export to make sure that they are not invoked concurrently.  
  Добавлена БлокировкаЭкспорта (БлокировкаРесурса) вокруг вызова Экспортер.Экспортировать() в ОтелБазовыйПакетныйПроцессор. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os`)

- ❌ **[Logs Sdk]** [MUST] Each LogRecordExporter implementation MUST document the concurrency characteristics the SDK requires of the exporter.  
  ОтелЭкспортерЛогов не содержит документации о требованиях конкурентности SDK к экспортеру. (-)

- ✅ **[Logs Sdk]** [MUST] LoggerProvider - Logger creation, ForceFlush and Shutdown MUST be safe to be called concurrently.  
  Кэш логгеров использует СинхронизированнаяКарта (потокобезопасно). Закрыть() использует АтомарноеБулево с СравнитьИУстановить(Ложь, Истина) для однократного выполнения. (`src/Логирование/Классы/ОтелПровайдерЛогирования.os`)

- ⚠️ **[Logs Sdk]** [MUST] LogRecordExporter - ForceFlush and Shutdown MUST be safe to be called concurrently.  
  Добавлена документация потокобезопасности в ОтелЭкспортерЛогов. СброситьБуфер() - no-op, безопасен тривиально. Однако Закрыть() использует обычный флаг Закрыт без атомарной операции - конкурентный вызов может привести к гонке. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os`)

- ✅ **[Metrics Api]** [MUST] This API MUST be structured to accept a variable number of callback functions, including none.  
  Конструктор принимает 0 или 1 callback, метод ДобавитьCallback() для добавления дополнительных. (`src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os`)

- ✅ **[Metrics Api]** [MUST] The API MUST support creation of asynchronous instruments by passing zero or more callback functions to be permanently registered to the newly created instrument.  
  Фабричные методы принимают необязательный Действие. ДобавитьCallback() для дополнительных. (`src/Метрики/Классы/ОтелМетр.os`)

- ✅ **[Metrics Api]** [MUST] Where the API supports registration of callback functions after asynchronous instrumentation creation, the user MUST be able to undo registration of the specific callback after its registration by some means.  
  ОтелРегистрацияНаблюдателя.Закрыть() отменяет регистрацию callback. (`src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os`)

- ✅ **[Metrics Sdk]** [MUST] The SDK MUST accept the following criteria: name, type, unit, meter_name, meter_version, meter_schema_url  
  Selector принимает все 6 критериев: ИмяИнструмента, ТипИнструмента, Единица, ИмяМетра, ВерсияМетра, АдресСхемыМетра. (`src/Метрики/Классы/ОтелСелекторИнструментов.os`)

- ❌ **[Metrics Sdk]** [MUST NOT] The instrument selection criteria parameter needs to be structured to accept a unit, but MUST NOT obligate a user to provide one.  
  Unit criterion is not implemented in ОтелСелекторИнструментов at all (-)

- ✅ **[Metrics Sdk]** [MUST NOT] The instrument selection criteria parameter needs to be structured to accept a meter_version, but MUST NOT obligate a user to provide one.  
  meter_version - необязательный параметр конструктора ОтелСелекторИнструментов. (`src/Метрики/Классы/ОтелСелекторИнструментов.os`)

- ✅ **[Metrics Sdk]** [MUST NOT] The instrument selection criteria parameter needs to be structured to accept a meter_schema_url, but MUST NOT obligate a user to provide one.  
  meter_schema_url - необязательный параметр конструктора ОтелСелекторИнструментов. (`src/Метрики/Классы/ОтелСелекторИнструментов.os`)

- ✅ **[Metrics Sdk]** [MUST] The SDK MUST accept the following stream configuration parameters: name, description, attribute_keys, aggregation, exemplar_reservoir, aggregation_cardinality_limit  
  ОтелПредставление принимает все параметры: Имя, Описание, РазрешенныеКлючиАтрибутов, ИсключенныеКлючиАтрибутов, Агрегация, ГраницыГистограммы, РезервуарЭкземпляров, ЛимитМощностиАгрегации. (`src/Метрики/Классы/ОтелПредставление.os`)

- ✅ **[Metrics Sdk]** [MUST] The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept.  
  Добавлено поле ИсключенныеКлючиАтрибутов в ОтелПредставление. (`src/Метрики/Классы/ОтелПредставление.os`)  
  Exclude-list is not implemented (-)

- ✅ **[Metrics Sdk]** [MUST] All other attributes MUST be kept (in exclude-list mode).  
  Поле ИсключенныеКлючиАтрибутов добавлено в ОтелПредставление. (`src/Метрики/Классы/ОтелПредставление.os`)  
  Exclude-list is not implemented (-)

- ✅ **[Metrics Sdk]** [MUST NOT] The stream configuration parameter needs to be structured to accept an exemplar_reservoir, but MUST NOT obligate a user to provide one.  
  exemplar_reservoir - необязательный параметр конструктора ОтелПредставление. (`src/Метрики/Классы/ОтелПредставление.os`)

- ✅ **[Metrics Sdk]** [MUST] If the user does not provide an exemplar_reservoir value, the MeterProvider MUST apply a default exemplar reservoir.  
  Резервуар по умолчанию создается в ОтелБазовыйСинхронныйИнструмент. Гистограммы используют ОтелВыровненныйРезервуарГистограммы, экспоненциальные - ОтелРезервуарЭкземпляров(min(20, max_buckets)), остальные - ОтелРезервуарЭкземпляров(1). View может переопределить. (`src/Метрики/Классы/ОтелМетр.os`)

- ✅ **[Metrics Sdk]** [MUST NOT] The stream configuration parameter needs to be structured to accept an aggregation_cardinality_limit, but MUST NOT obligate a user to provide one.  
  aggregation_cardinality_limit - необязательный параметр конструктора ОтелПредставление. (`src/Метрики/Классы/ОтелПредставление.os`)

- ⚠️ **[Metrics Sdk]** [MUST] If the user does not provide an aggregation_cardinality_limit value, the MeterProvider MUST apply the default aggregation cardinality limit the MetricReader is configured with.  
  Default cardinality limit (2000) is set in ОтелМетр constructor but it's not configurable per-View and not sourced from MetricReader (`src/Метрики/Классы/ОтелМетр.os:412`)

- ⚠️ **[Metrics Sdk]** [MUST] If the MeterProvider has no View registered, take the Instrument and apply the default Aggregation on the basis of instrument kind according to the MetricReader instance's aggregation property. Instrument advisory parameters, if any, MUST be honored.  
  Default aggregation is applied when no View matches, but instrument advisory parameters are not implemented (`src/Метрики/Классы/ОтелМетр.os:51-59`)

- ⚠️ **[Metrics Sdk]** [MUST] Callback functions MUST be invoked for the specific MetricReader performing collection, such that observations made or produced by executing callbacks only apply to the intended MetricReader during collection.  
  Callbacks are invoked during collection (ВызватьМультиОбратныеВызовы + individual instrument callbacks via Собрать), but observations are not scoped per-MetricReader - all readers share the same instrument data (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:126-133`)

- ⚠️ **[Metrics Sdk]** [MUST] Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow.  
  Реализация перенаправляет новые наборы атрибутов в overflow при достижении лимита, но при вызове ОчиститьТочкиДанных() (строка 131-136) полностью сбрасываются все аккумуляторы, включая ранее наблюдённые. Cumulative temporality не поддерживается явно - SDK реализует reset-based (delta-like) поведение. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:89`)

- ❌ **[Metrics Sdk]** [MUST] If multiple identical Instruments are created with different advisory parameters, the Meter MUST return an instrument using the first-seen advisory parameters and log an appropriate error as described in duplicate instrument registrations.  
  Advisory parameters are not implemented. Duplicate instrument registration checks exist (ПроверитьКонфликтДескриптора in ОтелМетр.os:441), but only for name/kind/unit/description - not for advisory parameters. (-)

- ❌ **[Metrics Sdk]** [MUST] If both a View and advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters.  
  Advisory parameters are not implemented. Views are implemented (ОтелПредставление.os), but since there are no advisory parameters, there is no precedence logic between Views and advisory params. (-)

- ❌ **[Metrics Sdk]** [MUST] If no View matches, or if a matching View selects the default aggregation, the ExplicitBucketBoundaries advisory parameter MUST be used. If neither is provided, the default bucket boundaries apply.  
  The ExplicitBucketBoundaries advisory parameter is not implemented. Instrument creation methods (e.g., СоздатьГистограмму in ОтелМетр.os:72) do not accept an advisory boundaries parameter. The histogram aggregator uses standard boundaries by default (ОтелАгрегаторГистограммы.os:118-135) or View-provided boundaries, but there is no advisory parameter path. (-)

- ✅ **[Metrics Sdk]** [MUST] A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation. For example, Exemplar sampling of histograms should be able to leverage bucket boundaries.  
  Гистограммы используют ОтелВыровненныйРезервуарГистограммы с привязкой к границам бакетов. (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os`, `src/Метрики/Классы/ОтелМетр.os`)

- ✅ **[Metrics Sdk]** [MUST] The ExemplarReservoir interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars.  
  Предложить() принимает сырые данные измерения (Значение, АтрибутыИзмерения, АтрибутыСерии, КонтекстСпана) и строит экземпляр внутри. Собрать() возвращает массив экземпляров. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os`)

- ⚠️ **[Metrics Sdk]** [MUST] A new ExemplarReservoir MUST be created for every known timeseries data point, as determined by aggregation and view configuration.  
  A single ОтелРезервуарЭкземпляров is created per instrument (line 217), not per timeseries. The reservoir internally uses a СинхронизированнаяКарта keyed by attribute key to separate timeseries, but it is one reservoir instance shared across all series, not a separate reservoir per series. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:217`)

- ✅ **[Metrics Sdk]** [MUST] The 'offer' method MAY accept a filtered subset of Attributes which diverge from the timeseries the reservoir is associated with. This MUST be clearly documented in the API and the reservoir MUST be given the Attributes associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the 'offer' method.  
  Предложить() принимает АтрибутыИзмерения и АтрибутыСерии, внутри вычисляет filteredAttributes. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os`)

- ✅ **[Metrics Sdk]** [MUST] Exemplars MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries.  
  Резервуар вычисляет filteredAttributes как разницу АтрибутыИзмерения - АтрибутыСерии и сохраняет в экземпляре. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os`)

- ✅ **[Metrics Sdk]** [MUST] This MUST be clearly documented in the API and the reservoir MUST be given the Attributes associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes.  
  Предложить() получает полные АтрибутыИзмерения и АтрибутыСерии для вычисления filteredAttributes. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os`)

- ✅ **[Metrics Sdk]** [MUST] The SDK MUST include two types of built-in exemplar reservoirs: SimpleFixedSizeExemplarReservoir and AlignedHistogramBucketExemplarReservoir.  
  ОтелРезервуарЭкземпляров (Algorithm R) и ОтелВыровненныйРезервуарГистограммы (по бакетам). (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os`, `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os`)

- ✅ **[Metrics Sdk]** [MUST] This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram.  
  ОтелВыровненныйРезервуарГистограммы принимает массив Границы в конструкторе. (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os`)

- ✅ **[Metrics Sdk]** [MUST] This implementation MUST store at most one measurement that falls within a histogram bucket.  
  Каждый бакет хранит ровно один слот, последнее измерение заменяет предыдущее. (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os`)

- ✅ **[Metrics Sdk]** [MUST] The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation.  
  View (ОтелПредставление) принимает кастомный РезервуарЭкземпляров, который применяется к инструменту. (`src/Метрики/Классы/ОтелПредставление.os`, `src/Метрики/Классы/ОтелМетр.os`)

- ✅ **[Metrics Sdk]** [MUST] This extension MUST be configurable on a metric View.  
  ОтелПредставление.РезервуарЭкземпляров() применяется при настройке инструмента в ОтелМетр.ПрименитьПредставлениеКИнструменту(). (`src/Метрики/Классы/ОтелМетр.os`)

- ❌ **[Metrics Sdk]** [MUST] Individual reservoirs MUST still be instantiated per metric-timeseries.  
  Нет механизма кастомных резервуаров, поэтому нет и создания отдельных экземпляров на каждую метрику-таймсерию через кастомный резервуар. (-)

- ✅ **[Metrics Sdk]** [MUST] Shutdown MUST be called only once for each MetricReader instance. After the call to Shutdown, subsequent invocations to Collect are not allowed.  
  Закрыт конвертирован в АтомарноеБулево. Закрыть() использует СравнитьИУстановить(Ложь, Истина) для однократного выполнения. Повторные вызовы игнорируются. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os`)

- ✅ **[Metrics Sdk]** [MUST] The reader MUST synchronize calls to MetricExporter's Export to make sure that they are not invoked concurrently.  
  Добавлена БлокировкаЭкспорта (БлокировкаРесурса) вокруг вызова Экспортер.Экспортировать() в ОтелБазовыйПакетныйПроцессор, используемом читателем метрик. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os`)

- ⚠️ **[Metrics Sdk]** [MUST NOT] Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure).  
  Метод Экспортировать() вызывает Транспорт.Отправить() синхронно. Таймаут задан на уровне HTTP-транспорта (ТаймаутСекунд), но в самом экспортере нет явного ограничения. Не всегда гарантируется error result при timeout. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:19`)

- ❌ **[Metrics Sdk]** [MUST] A MetricFilter MUST support the following functions (TestMetric, TestAttributes).  
  No MetricFilter interface or class exists in the codebase. No TestMetric or TestAttributes operations are implemented. (-)

- ❌ **[Metrics Sdk]** [MUST] A MetricFilter MUST support the following functions (TestMetric, TestAttributes).  
  No MetricFilter interface or class exists in the codebase. No TestMetric or TestAttributes operations are implemented. (-)

- ❌ **[Metrics Sdk]** [MUST] The SDK MUST provide configuration according to the SDK environment variables specification.  
  The SDK does provide environment variable configuration through ОтелАвтоконфигурация module, supporting OTEL_METRICS_EXPORTER, OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE, OTEL_EXPORTER_OTLP_METRICS_DEFAULT_HISTOGRAM_AGGREGATION and other OTEL_ variables. However, several metrics-specific SDK env variables from the spec (like OTEL_METRIC_EXPORT_INTERVAL, OTEL_METRIC_EXPORT_TIMEOUT) are not implemented - only a subset is covered. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1`)

- ❌ **[Metrics Sdk]** [MUST] The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry.  
  No explicit numerical limits handling is implemented in the metrics SDK. There are no checks for overflow, underflow, or error handling for extreme numerical values in aggregators (ОтелАгрегаторСуммы, ОтелАгрегаторГистограммы, etc.). (-)

- ⚠️ **[Metrics Sdk]** [MUST] MeterProvider - Meter creation, ForceFlush and Shutdown MUST be safe to be called concurrently.  
  Meter creation (ПолучитьМетр) uses СинхронизированнаяКарта for thread-safe access to the meters cache. However, ForceFlush (СброситьБуфер) and Shutdown (Закрыть) iterate over ЧитателиМетрик array without synchronization - these methods are not explicitly thread-safe. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:221`)

- ❌ **[Metrics Sdk]** [MUST] MetricExporter - ForceFlush and Shutdown MUST be safe to be called concurrently.  
  ОтелЭкспортерМетрик does not use any synchronization (no БлокировкаРесурса, no СинхронизированнаяКарта). The СброситьБуфер and Закрыть methods are not thread-safe - concurrent calls to Закрыть and Экспортировать could race on the Закрыт flag. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:40`)

- ❌ **[Otlp Exporter]** [MUST] Each configuration option MUST be overridable by a signal specific option.  
  Нет поддержки сигнал-специфичных переменных окружения (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_HEADERS и т.д.). Используется только общий набор otel.exporter.otlp.* для всех сигналов. (-)

- ✅ **[Otlp Exporter]** [MUST] The implementation MUST honor the following URL components: scheme (http or https), host, port, path.  
  URL обрабатывается через КоннекторHTTP. Trailing slash в base URL нормализуется в ВыполнитьОднуПопытку(). (`src/Экспорт/Классы/ОтелHttpТранспорт.os`)

- ✅ **[Otlp Exporter]** [MUST] When using OTEL_EXPORTER_OTLP_ENDPOINT, exporters MUST construct per-signal URLs by appending signal paths (v1/traces, v1/metrics, v1/logs) relative to the base URL.  
  Trailing slash нормализуется перед конкатенацией пути сигнала. (`src/Экспорт/Классы/ОтелHttpТранспорт.os`)

- ⚠️ **[Otlp Exporter]** [MUST] For the per-signal variables (OTEL_EXPORTER_OTLP_<signal>_ENDPOINT), the URL MUST be used as-is without any modification.  
  Per-signal endpoint переменные (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT и т.д.) не поддерживаются, поэтому невозможно использовать URL as-is для конкретного сигнала. (-)

- ⚠️ **[Otlp Exporter]** [MUST] If a per-signal URL contains no path part, the root path / MUST be used (see Example 2).  
  Per-signal endpoint переменные не поддерживаются, поэтому логика обработки пустого пути для per-signal URL отсутствует. (-)

- ⚠️ **[Otlp Exporter]** [MUST NOT] An SDK MUST NOT modify the URL in ways other than specified above.  
  URL не модифицируется сверх конкатенации БазовыйURL + Путь. Однако per-signal endpoints не поддерживаются, что ограничивает полноту оценки. (`src/Экспорт/Классы/ОтелHttpТранспорт.os:74`)

- ✅ **[Otlp Exporter]** [MUST] This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered.  
  Реализована экспоненциальная задержка Pow(2, НомерПопытки - 1) с jitter-фактором (0.5 + случайное/2000) в HTTP и gRPC транспортах. (`src/Экспорт/Классы/ОтелHttpТранспорт.os`, `src/Экспорт/Классы/ОтелGrpcТранспорт.os`)

- ⚠️ **[Propagators]** [MUST] Getter and Setter MUST be stateless and allowed to be saved as constants, in order to effectively avoid runtime allocations.  
  There are no separate Getter or Setter objects/interfaces in the codebase. Propagators directly work with Соответствие (Map) as carriers - reading via iteration (Для Каждого КлючИЗначение Из Заголовки) and writing via Заголовки.Вставить(). The Getter/Setter abstraction as separate stateless objects does not exist. (-)

- ⚠️ **[Propagators]** [MUST] The implementation MUST preserve casing if the used protocol is not case insensitive.  
  Casing is preserved in practice (keys written as literal strings), but there is no Setter interface that formally guarantees casing preservation as a contract. (`src/Пропагация/Модули/ОтелW3CПропагатор.os:51`)

- ❌ **[Propagators]** [MUST] The Keys function MUST return the list of all the keys in the carrier.  
  There is no Getter interface or Keys function. Propagators iterate over the carrier (Соответствие) directly using Для Каждого instead of using a Getter.Keys() abstraction. (-)

- ❌ **[Propagators]** [MUST] The Get function MUST return the first value of the given propagation key or return null if the key doesn't exist.  
  There is no Getter.Get() function. The propagators iterate over all headers manually (Для Каждого КлючИЗначение Из Заголовки) checking НРег(КлючИЗначение.Ключ) to find keys, instead of using a Get function. (-)

- ⚠️ **[Propagators]** [MUST] The Get function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive.  
  Case-insensitive lookup IS implemented inline (НРег(КлючИЗначение.Ключ) = 'traceparent'), but it is not in a separate Getter.Get() function - it's inline in each propagator's Extract method. (`src/Пропагация/Модули/ОтелW3CПропагатор.os:71`)

- ❌ **[Propagators]** [MUST] If explicitly implemented, the GetAll function MUST return all values of the given propagation key.  
  There is no GetAll function or Getter interface. The inline iteration in propagators only finds the last matching header value (overwriting on each match), not all values. (-)

- ⚠️ **[Propagators]** [MUST] The GetAll function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive.  
  Case-insensitive lookup is implemented inline via НРег() in each propagator's Extract, but there is no separate GetAll function or Getter interface. (`src/Пропагация/Модули/ОтелW3CПропагатор.os:71`)

- ✅ **[Propagators]** [MUST] The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise.  
  Создан класс ОтелНоопПропагатор с методами Внедрить/Извлечь/Поля. ОтелГлобальный.ПолучитьПропагаторы() возвращает ОтелНоопПропагатор, если пропагаторы не сконфигурированы. (`src/Пропагация/Классы/ОтелНоопПропагатор.os`, `src/Ядро/Модули/ОтелГлобальный.os`)

- ✅ **[Propagators]** [MUST] This method MUST exist for each supported Propagator type. Returns a global Propagator.  
  Метод ОтелГлобальный.ПолучитьПропагаторы() существует и делегирует в глобальный SDK. ОтелГлобальный.ПроверитьИнициализацию() теперь лениво создаёт noop SDK, поэтому ПолучитьПропагаторы() больше не выбрасывает исключение без настроенного SDK. (`src/Ядро/Модули/ОтелГлобальный.os`)

- ⚠️ **[Propagators]** [MUST] This method MUST exist for each supported Propagator type. Sets the global Propagator instance.  
  Добавлен метод ОтелГлобальный.УстановитьПропагаторы() для независимой от SDK установки глобальных пропагаторов. Хранение через АтомарнаяСсылка. (`src/Ядро/Модули/ОтелГлобальный.os`)

- ⚠️ **[Propagators]** [MUST] The official list of propagators that MUST be maintained by the OpenTelemetry organization: W3C TraceContext, W3C Baggage, B3.  
  W3C TraceContext и W3C Baggage реализованы. B3 Propagator отсутствует (не реализован как extension package). (`src/Пропагация/Модули/ОтелW3CПропагатор.os:1`)

- ⚠️ **[Propagators]** [MUST] The official list of propagators MUST be distributed as OpenTelemetry extension packages: W3C TraceContext (MAY alternatively be in API), W3C Baggage (MAY alternatively be in API), B3.  
  W3C TraceContext и Baggage распространяются как часть API (допускается по MAY-оговорке). B3 не реализован ни как extension, ни inline. (`src/Пропагация/Модули/ОтелW3CПропагатор.os:1`)

- ❌ **[Propagators]** [MUST NOT] OT Trace propagator MUST NOT use OpenTracing in the resulting propagator name as it is not widely adopted format in the OpenTracing ecosystem.  
  OT Trace пропагатор не реализован в данном SDK. Требование к именованию неприменимо без реализации, но OT Trace не входит в список разрешённых n_a. (-)

- ⚠️ **[Env Vars]** [MUST] For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting.  
  Для OTEL_TRACES_SAMPLER нераспознанное значение обрабатывается gracefully - фолбэк на parentbased_always_on (строки 216-218), но без логирования предупреждения. Для OTEL_PROPAGATORS нераспознанное значение теперь логирует предупреждение через Сообщить() и пропускается. Для OTEL_TRACES_EXPORTER/OTEL_LOGS_EXPORTER/OTEL_METRICS_EXPORTER нераспознанные значения не обрабатываются - передаются дальше как есть. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os`)

### SHOULD/SHOULD NOT несоответствия

- ✅ **[Context]** [SHOULD NOT] Multiple calls to CreateKey with the same name SHOULD NOT return the same value unless language constraints dictate otherwise  
  Каждый вызов СоздатьКлюч() создает новый объект ОтелКлючКонтекста, сравнение по ссылке. (`src/Ядро/Модули/ОтелКонтекст.os:35`)

- ⚠️ **[Resource Sdk]** [SHOULD] An error that occurs during an attempt to detect resource information SHOULD be considered an error.  
  Errors during resource detection are caught via Попытка/Исключение but logged at Лог.Отладка (debug) level instead of error level. Per spec, detection errors SHOULD be treated as errors, but they are silently suppressed to debug log. (`src/Ядро/Классы/ОтелРесурс.os:121`)

- ⚠️ **[Resource Sdk]** [SHOULD] Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate.  
  The resource uses empty Schema URL (АдресСхемы defaults to ''), but the inline detection DOES populate known semantic convention attributes (host.name, os.type, process.pid). Per spec, empty URL is for detectors that don't know what they populate - this detector knows exactly what it populates, so it should set a schema URL per the previous MUST requirement. (`src/Ядро/Классы/ОтелРесурс.os:98`)

- ⚠️ **[Trace Api]** [SHOULD] Its name property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged  
  Имя сохраняется как есть (в том числе пустая строка), но предупреждение о невалидном имени не логируется (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52`)

- ⚠️ **[Trace Api]** [SHOULD] A message reporting that the specified value is invalid SHOULD be logged when an invalid name is specified  
  Нет логирования предупреждения при пустом/невалидном имени (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52`)

- ⚠️ **[Trace Api]** [SHOULD NOT] implementations SHOULD NOT provide access to a Span's attributes besides its SpanContext  
  ОтелСпан публично предоставляет Атрибуты(), События(), Линки() и другие свойства. OneScript не поддерживает интерфейсы, поэтому один класс обслуживает и API, и SDK (процессорам нужен доступ к данным для экспорта) (`src/Трассировка/Классы/ОтелСпан.os:126`)

- ⚠️ **[Trace Api]** [SHOULD] This SHOULD be called SetStatus.  
  Method is named УстановитьСтатус (Russian translation), not SetStatus, but the naming convention uses Russian throughout. (`src/Трассировка/Классы/ОтелСпан.os:402`)

- ❌ **[Trace Api]** [SHOULD] When the status is set to Error by Instrumentation Libraries, the Description SHOULD be documented and predictable.  
  No documentation or conventions for standard error descriptions in instrumentation libraries are provided. (-)

- ❌ **[Trace Api]** [SHOULD] Instrumentation Libraries SHOULD publish their own conventions for Description values, including possible values and what they mean.  
  No published conventions for Description values found in the codebase. (-)

- ❌ **[Trace Api]** [SHOULD] Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generate.  
  This is a requirement for analysis/visualization tools, not directly verifiable in the SDK code itself. No analysis tool behavior is implemented. (-)

- ⚠️ **[Trace Api]** [SHOULD] If a new type is required to be publicly exposed, it SHOULD be named NonRecordingSpan.  
  The type is named ОтелНоопСпан (NoopSpan), not NonRecordingSpan. While functional behavior matches, the naming convention differs from the spec recommendation. (`src/Трассировка/Классы/ОтелНоопСпан.os:1`)

- ⚠️ **[Trace Api]** [SHOULD] Link - Links are immutable and SHOULD be safe for concurrent use by default.  
  Links are stored as Соответствие (Map) objects in an array. They are effectively immutable after creation, but not documented as such. No explicit concurrency safety documentation. (`src/Трассировка/Классы/ОтелСпан.os:361`)

- ❌ **[Trace Api]** [SHOULD] If the Span in the parent Context is already non-recording, it SHOULD be returned directly without instantiating a new Span.  
  The Tracer always creates a new ОтелНоопСпан even when the parent is already non-recording. There is no check in НачатьСпан to detect and directly return an existing non-recording parent span. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() - процедура без возвращаемого значения, не сообщает вызывающему об успехе/неудаче/таймауте. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:91-95`)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() не имеет механизма таймаута - блокирующий вызов без ограничения времени. (`src/Трассировка/Классы/ОтелПровайдерТрассировки.os:91-95`)

- ⚠️ **[Trace Sdk]** [SHOULD NOT] Span Exporter SHOULD NOT receive them unless the Sampled flag was also set.  
  Процессор передает все завершённые спаны экспортеру без проверки флага Sampled. Если семплер вернёт RECORD_ONLY (решение=1), спан всё равно будет экспортирован. Встроенные семплеры никогда не возвращают RECORD_ONLY, но архитектурно проверка отсутствует. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-31`)

- ⚠️ **[Trace Sdk]** [SHOULD NOT] Span Exporters SHOULD NOT receive the ones that do not have Sampled flag set.  
  Нет фильтрации по флагу Sampled в цепочке процессор→экспортер. Все спаны, прошедшие семплирование (RECORD_ONLY или RECORD_AND_SAMPLE), передаются экспортеру без различия. (`src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-31`)

- ❌ **[Trace Sdk]** [SHOULD] If the sampler returns an empty Tracestate here, the Tracestate will be cleared, so samplers SHOULD normally return the passed-in Tracestate if they do not intend to change it.  
  Семплер ОтелСэмплер.ДолженСэмплировать() не принимает TraceState родителя как параметр и не передаёт его в ОтелРезультатСэмплирования. Вместо этого создаётся новый пустой ОтелСостояниеТрассировки, что приводит к потере родительского TraceState. (-)

- ✅ **[Trace Sdk]** [SHOULD NOT] Description MAY change over time. Callers SHOULD NOT cache the returned value of GetDescription.  
  Реализована функция ОтелСэмплер.Описание(Стратегия, Доля, КорневаяСтратегия), возвращающая строковое описание семплера. (`src/Трассировка/Модули/ОтелСэмплер.os`)

- ⚠️ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values.  
  TraceID генерируется через UUID v4 (Новый УникальныйИдентификатор), что обеспечивает достаточную случайность (122 бита). Однако специфические требования W3C Trace Context Level 2 (например, флаг Random) не реализованы. TraceID случайный, но SDK не сигнализирует об этом через флаг. (`src/Ядро/Модули/ОтелУтилиты.os:78-92`)

- ❌ **[Trace Sdk]** [SHOULD] For root span contexts, the SDK SHOULD set the Random flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements.  
  Флаг Random (бит W3C Trace Context Level 2) не устанавливается. ОтелКонтекстСпана создаётся с флагами=1 (только бит Sampled). Нет логики установки флага Random при генерации случайного TraceID. (-)

- ❌ **[Trace Sdk]** [SHOULD] Custom implementations of the IdGenerator SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace random flag will be set in the associated Trace contexts.  
  The custom IdGenerator mechanism (УстановитьГенераторИд) has no way for implementations to declare W3C Level 2 randomness compliance. There is no marker interface, flag property, or any mechanism to indicate randomness support and set the random trace flag. (-)

- ❌ **[Trace Sdk]** [SHOULD] There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute, event, or link was discarded due to such a limit.  
  ОтелСпан tracks dropped counts (ОтброшенныхАтрибутов, ОтброшенныхСобытий, ОтброшенныхЛинков) but does not log any warning message when items are discarded. There is no Лог variable or log call in ОтелСпан.os. (-)

- ❌ **[Trace Sdk]** [SHOULD] The SpanProcessor interface SHOULD declare the following methods: OnEnding method.  
  No OnEnding method exists in any span processor. The processors only have ПриНачале (OnStart) and ПриЗавершении (OnEnd). There is no intermediate step between span End() being called and OnEnd being invoked. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] Shutdown SHOULD be called only once for each SpanProcessor instance. After the call to Shutdown, subsequent calls to OnStart, OnEnd, or ForceFlush are not allowed. SDKs SHOULD ignore these calls gracefully, if possible.  
  BatchSpanProcessor (via ОтелБазовыйПакетныйПроцессор) checks Закрыт flag in Обработать() and returns early, which prevents OnEnd from processing. However SimpleSpanProcessor has no such guard - after Закрыть() it can still receive ПриЗавершении() calls (it just won't have an exporter if it was closed). Also no protection against double Shutdown calls. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:42-44`)

- ❌ **[Trace Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Закрыть() (Shutdown) in both ОтелПростойПроцессорСпанов and ОтелБазовыйПакетныйПроцессор is a Процедура (void), not a Функция. It returns nothing - no success/failure/timeout indication. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] Shutdown SHOULD complete or abort within some timeout.  
  BatchSpanProcessor's ОстановитьФоновыйЭкспорт() uses a timeout when waiting for the background export promise (ТаймаутЭкспортаМс). However the ЭкспортироватьВсеПакеты() call in Закрыть() has no timeout - it loops until the buffer is empty, potentially blocking indefinitely. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:184-193`)

- ⚠️ **[Trace Sdk]** [SHOULD] Shutdown SHOULD be called only once for each SpanProcessor instance.  
  Закрыть() sets Закрыт=Истина but does not guard against being called multiple times. If called twice, it will attempt to stop background export and flush again, and close the exporter again. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:73-74`)

- ❌ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() is a Процедура (void) - it returns nothing to indicate success, failure or timeout. (-)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() (ForceFlush) has no timeout parameter and no internal timeout. It calls ЭкспортироватьВсеПакеты() which loops synchronously until buffer is empty, potentially blocking indefinitely if exports are slow. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:67-69`)

- ⚠️ **[Trace Sdk]** [SHOULD] The processor SHOULD export a batch when any of the following happens AND the previous export call has returned: scheduledDelayMillis after the processor is constructed OR the first span is received; the queue contains maxExportBatchSize or more spans; ForceFlush is called.  
  Все три условия экспорта реализованы: периодический таймер (ПериодическийЭкспорт, строка 105), порог размера пакета (строка 53, 60), ForceFlush (СброситьБуфер, строка 67). Однако нет явной проверки, что предыдущий вызов Export завершился перед началом нового (AND the previous export call has returned). (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:41`)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер реализован как Процедура (void) без возвращаемого значения. Вызывающий код не может узнать, был ли ForceFlush успешным, неудачным или прерванным по таймауту. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38`)

- ⚠️ **[Trace Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout. ForceFlush can be implemented as a blocking API or an asynchronous API which notifies the caller via a callback or an event.  
  СброситьБуфер экспортера не имеет механизма таймаута. Для синхронного экспортера это не критично (нет буфера), но у ОтелБазовыйПакетныйПроцессор.СброситьБуфер также нет таймаута - он вызывает ЭкспортироватьВсеПакеты(), который может выполняться неограниченно долго при большом буфере. (`src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38`)

- ❌ **[Logs Api]** [SHOULD] The Enabled API SHOULD be documented that instrumentation authors need to call this API each time they emit a LogRecord to ensure they have the most up-to-date response.  
  The Включен() method documentation does not mention that it should be called each time before emitting. The doc only describes parameters and return value. (-)

- ⚠️ **[Logs Api]** [SHOULD] When only explicit Context is supported for Emit, this parameter SHOULD be required.  
  The implementation supports implicit Context (falls back to ОтелКонтекст.Текущий()), so Context is optional. This requirement applies to explicit-only Context SDKs, which this is not, but the spec sentence still contains a SHOULD. The implementation is correct for its design choice (implicit context). (`src/Логирование/Классы/ОтелЛоггер.os:64`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() объявлен как Процедура (void) без возвращаемого значения - вызывающий код не может узнать об успехе, ошибке или таймауте. На уровне провайдера есть СброситьБуферАсинхронно() с Обещанием, но сам экспортер не предоставляет обратной связи. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  ForceFlush экспортера - no-op (завершается мгновенно). Но ForceFlush пакетного процессора (ЭкспортироватьВсеПакеты) зацикливается до исчерпания буфера без собственного таймаута - полагается только на таймаут транспорта для каждого отдельного пакета, но общий таймаут ForceFlush не конфигурируется. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:67`)

- ❌ **[Logs Sdk]** [SHOULD] There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute was discarded due to such a limit.  
  When an attribute is discarded (ОтелЗаписьЛога.os:214), only the counter ОтброшенныхАтрибутов is incremented. No log message is printed to alert the user. (-)

- ❌ **[Logs Sdk]** [SHOULD] To avoid race conditions, implementations SHOULD recommended to users that a clone of logRecord be used for any concurrent processing, such as in a batching processor.  
  Нет механизма клонирования ОтелЗаписьЛога и нет документации, рекомендующей пользователям клонировать запись для конкурентной обработки. (-)

- ❌ **[Logs Sdk]** [SHOULD] Shutdown SHOULD be called only once for each LogRecordProcessor instance.  
  Нет защиты от повторного вызова Закрыть(). В ОтелПростойПроцессорЛогов нет флага Закрыт, повторный вызов приводит к повторному вызову Экспортер.Закрыть(). В ОтелБазовыйПакетныйПроцессор Закрыт устанавливается в Истина, но Закрыть() не проверяет этот флаг перед выполнением. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] After the call to Shutdown, subsequent calls to OnEmit are not allowed. SDKs SHOULD ignore these calls gracefully, if possible.  
  ОтелБазовыйПакетныйПроцессор.Обработать проверяет флаг Закрыт и делает Возврат (строка 42-43). Однако ОтелПростойПроцессорЛогов.ПриПоявлении не проверяет закрытие процессора - вызовы после Shutdown делегируются экспортеру (который проверяет Закрыт). (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:42`)

- ❌ **[Logs Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Закрыть() объявлена как Процедура (void) во всех процессорах. Нет возвращаемого значения для информирования вызывающего кода об успехе, ошибке или таймауте. (-)

- ⚠️ **[Logs Sdk]** [SHOULD] Shutdown SHOULD complete or abort within some timeout.  
  В пакетном процессоре ОстановитьФоновыйЭкспорт() использует таймаут при ожидании фонового задания (строка 187), но сама процедура ЭкспортироватьВсеПакеты() не ограничена по времени - если экспортер зависнет, Shutdown заблокируется бесконечно. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:187`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() объявлен как Процедура (void) без возвращаемого значения - вызывающий код не может узнать об успехе, ошибке или таймауте. На уровне провайдера есть СброситьБуферАсинхронно() с Обещанием, но сам экспортер не предоставляет обратной связи. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  ForceFlush экспортера - no-op (завершается мгновенно). Но ForceFlush пакетного процессора (ЭкспортироватьВсеПакеты) зацикливается до исчерпания буфера без собственного таймаута - полагается только на таймаут транспорта для каждого отдельного пакета, но общий таймаут ForceFlush не конфигурируется. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:67`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() объявлен как Процедура (void) без возвращаемого значения - вызывающий код не может узнать об успехе, ошибке или таймауте. На уровне провайдера есть СброситьБуферАсинхронно() с Обещанием, но сам экспортер не предоставляет обратной связи. (`src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38`)

- ⚠️ **[Logs Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  ForceFlush экспортера - no-op (завершается мгновенно). Но ForceFlush пакетного процессора (ЭкспортироватьВсеПакеты) зацикливается до исчерпания буфера без собственного таймаута - полагается только на таймаут транспорта для каждого отдельного пакета, но общий таймаут ForceFlush не конфигурируется. (`src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:67`)

- ⚠️ **[Metrics Api]** [SHOULD] Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying.  
  OneScript не различает int/float на уровне типа Число. Дескриптор инструмента регистрируется с Вид, ЕдиницаИзмерения и Описание, но не с числовым типом. Агрегатор использует строковые маркеры 'int'/'double', но они не являются частью идентификации инструмента при проверке конфликтов. (`src/Метрики/Классы/ОтелМетр.os:436`)

- ❌ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (sync).  
  Документация методов СоздатьСчетчик и аналогов не упоминает синтаксис имен инструментов (правила ABNF). (-)

- ❌ **[Metrics Api]** [SHOULD NOT] The API SHOULD NOT validate advisory parameters (sync).  
  Advisory-параметры не реализованы в API синхронных инструментов, поэтому невозможно оценить валидацию. (-)

- ❌ **[Metrics Api]** [SHOULD] The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (async).  
  Документация методов СоздатьНаблюдаемыйСчетчик и аналогов не упоминает синтаксис имен инструментов. (-)

- ❌ **[Metrics Api]** [SHOULD NOT] The API SHOULD NOT validate advisory parameters (async).  
  Advisory-параметры не реализованы в API асинхронных инструментов. (-)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD support registration of callback functions associated with asynchronous instruments after they are created.  
  Мульти-callback регистрация через ЗарегистрироватьОбратныйВызов поддерживается на уровне Метра, но нет метода регистрации дополнительного callback на отдельном наблюдаемом инструменте после его создания. (`src/Метрики/Классы/ОтелМетр.os:348`)

- ❌ **[Metrics Api]** [SHOULD] Callback functions SHOULD be reentrant safe. The SDK expects to evaluate callbacks for each MetricReader independently.  
  Нет документации для пользователей о том, что callback-функции должны быть реентерабельными. (-)

- ❌ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT take an indefinite amount of time.  
  Нет документации для пользователей о том, что callback-функции не должны занимать неопределённо долгое время. (-)

- ❌ **[Metrics Api]** [SHOULD NOT] Callback functions SHOULD NOT make duplicate observations (more than one Measurement with the same attributes) across all registered callbacks.  
  Нет документации для пользователей о недопустимости дублирующих наблюдений. (-)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD provide some way to pass state to the callback.  
  Callback передаётся как Действие (lambda). OneScript Действие может захватывать контекст через замыкание, но нет явного механизма передачи состояния (дополнительного параметра state) в callback. Передача состояния возможна только через замыкание lambda. (`src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:108`)

- ❌ **[Metrics Api]** [SHOULD] The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response.  
  Метод Включен() существует, но в документации (комментариях) к нему нет указания на то, что авторы инструментирования должны вызывать его каждый раз перед записью измерения. (-)

- ⚠️ **[Metrics Api]** [SHOULD] The increment value is expected to be non-negative. This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative.  
  Документация (комментарий на строке 14) говорит 'Отрицательные значения игнорируются' и параметр описан как 'положительное значение'. Однако формулировка не строго совпадает со spec-требованием 'communicate that value is expected to be non-negative'. По факту поведение корректное. (`src/Метрики/Классы/ОтелСчетчик.os:14`)

- ⚠️ **[Metrics Api]** [SHOULD] The API SHOULD provide some way to pass state to the callback.  
  Callback передаётся как Действие (lambda) и может захватывать состояние через замыкание, но нет явного дополнительного параметра state в сигнатуре callback. (`src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:108`)

- ❌ **[Metrics Sdk]** [SHOULD] A view with criteria matching the instrument an aggregation is created for has an aggregation_cardinality_limit value defined for the stream, that value SHOULD be used.  
  Поле ЛимитМощностиАгрегации добавлено в ОтелПредставление. (`src/Метрики/Классы/ОтелПредставление.os`)

- ❌ **[Metrics Sdk]** [SHOULD] If there is no matching view, but the MetricReader defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used.  
  ОтелПериодическийЧитательМетрик не имеет настройки default cardinality limit. Лимит задаётся только на уровне Meter (2000) и инструмента. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() - процедура без возвращаемого значения. Не возвращает статус успеха/ошибки/таймаута. СброситьБуферАсинхронно() возвращает Обещание, но синхронный вариант не информирует о результате. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:112`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status.  
  СброситьБуфер() не возвращает никакого статуса (ERROR/NO ERROR). Это процедура (void), а не функция. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:112`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() не принимает параметр таймаута и не имеет механизма прерывания по тайм-ауту. (`src/Метрики/Классы/ОтелПровайдерМетрик.os:112`)

- ❌ **[Metrics Sdk]** [SHOULD] If the user does not provide any value, the SDK SHOULD use the Attributes advisory parameter configured on the instrument instead.  
  No advisory parameter support implemented; when no attribute_keys are set, all attributes are kept without checking instrument advisory (-)

- ✅ **[Metrics Sdk]** [SHOULD] Additionally, implementations SHOULD support configuring an exclude-list of attribute keys.  
  Поле ИсключенныеКлючиАтрибутов добавлено в ОтелПредставление. (`src/Метрики/Классы/ОтелПредставление.os`)

- ⚠️ **[Metrics Sdk]** [SHOULD] If it is not possible to apply the View without producing semantic errors the implementation SHOULD emit a warning and proceed as if the View did not exist.  
  Warning is emitted for conflict, but no check for semantic errors like assigning histogram aggregation to async instrument (`src/Метрики/Классы/ОтелМетр.os:441-454`)

- ❌ **[Metrics Sdk]** [SHOULD NOT] Histogram Aggregations: Arithmetic sum of Measurement values in population. This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. UpDownCounter or ObservableGauge).  
  The histogram aggregator always collects sum regardless of instrument type - no conditional logic to skip sum for negative-value instruments (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the sum, min, and max fields, because these values do not map into a valid bucket.  
  No explicit handling of Inf/NaN values in the exponential histogram aggregator (-)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks.  
  No mechanism to detect or disregard observations made outside callback context (-)

- ❌ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback execution.  
  No timeout mechanism for callbacks; they execute without time limits (-)

- ❌ **[Metrics Sdk]** [SHOULD NOT] The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback.  
  Asynchronous instruments (ОтелБазовыйНаблюдаемыйИнструмент) clear external observations after each collect, but individual callback observations are freshly generated each time, so stale attribute sets from prior callbacks may persist within external observations if not properly cleared (-)

- ❌ **[Metrics Sdk]** [SHOULD] A view with criteria matching the instrument an aggregation is created for has an aggregation_cardinality_limit value defined for the stream, that value SHOULD be used.  
  ОтелПредставление (View) не имеет поля aggregation_cardinality_limit. View поддерживает имя, описание, атрибуты, границы гистограммы, агрегацию, но не лимит кардинальности per-stream. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If there is no matching view, but the MetricReader defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used.  
  ОтелПериодическийЧитательМетрик не имеет настройки default cardinality limit. Лимит задаётся только на уровне Meter (2000) и инструмента. (-)

- ❌ **[Metrics Sdk]** [SHOULD] Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality.  
  ОтелБазовыйНаблюдаемыйИнструмент не реализует ни лимита кардинальности, ни overflow-логики. В отличие от синхронных инструментов, наблюдаемые инструменты не имеют ЛимитМощности, КлючПереполнения или ПеренаправитьВПереполнение(). Все записи из callback принимаются без ограничений. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible.  
  Предупреждение содержит информацию о конфликтующих параметрах (вид, единица измерения), но не включает рекомендацию по разрешению конфликта (например, использовать View для переименования). (`src/Метрики/Классы/ОтелМетр.os:449`)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves multiple description properties, setting the description through a configured View SHOULD avoid the warning.  
  Проверка конфликта (ПроверитьКонфликтДескриптора) не учитывает наличие View, который мог бы задать описание. Предупреждение выдаётся всегда при различии description, независимо от настроенных View. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning.  
  Предупреждение (строка 449) не содержит рецепта по использованию View для переименования или разрешения конфликта. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both Metric objects and emit a generic warning describing the duplicate instrument registration.  
  При дубликате возвращается первый зарегистрированный инструмент (строка 48), а не оба объекта Metric. Предупреждение выдаётся (строка 449), но данные второго инструмента не экспортируются отдельно. (`src/Метрики/Классы/ОтелМетр.os:48`)

- ❌ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax.  
  Методы создания инструментов (СоздатьСчетчик и др.) не выполняют валидацию имени инструмента. Имя нормализуется через НРег() (lower case), но не проверяется на соответствие синтаксису (regex паттерн спецификации). (-)

- ❌ **[Metrics Sdk]** [SHOULD] If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name.  
  Нет проверки синтаксиса имени инструмента и соответствующего предупреждения/ошибки при невалидном имени. (-)

- ❌ **[Metrics Sdk]** [SHOULD] When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters.  
  Advisory parameters are not implemented in the SDK. The instrument creation methods (СоздатьСчетчик, СоздатьГистограмму, etc.) do not accept advisory parameters and there is no validation logic for them. (-)

- ❌ **[Metrics Sdk]** [SHOULD] If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided.  
  Advisory parameters are not implemented, so there is no validation or error emission for invalid advisory parameters. (-)

- ✅ **[Metrics Sdk]** [SHOULD] A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: ExemplarFilter: filter which measurements can become exemplars; ExemplarReservoir: storage and sampling of exemplars.  
  ExemplarFilter конфигурируется через ОтелПостроительПровайдераМетрик.УстановитьФильтрЭкземпляров(). ExemplarReservoir конфигурируется через View. (`src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os`, `src/Метрики/Классы/ОтелПредставление.os`)

- ✅ **[Metrics Sdk]** [SHOULD] The filter configuration SHOULD follow the environment variable specification.  
  OTEL_METRICS_EXEMPLAR_FILTER читается в конструкторе ОтелПостроительПровайдераМетрик. Поддерживаются always_on, always_off, trace_based. (`src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os`)

- ✅ **[Metrics Sdk]** [SHOULD] The 'offer' method SHOULD accept measurements, including: the value of the measurement, the complete set of Attributes, the Context (Baggage and active Span), and a timestamp.  
  Предложить() принимает Значение, АтрибутыИзмерения, АтрибутыСерии, КонтекстСпана. Временная метка генерируется внутри. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os`)

- ✅ **[Metrics Sdk]** [SHOULD] The 'offer' method SHOULD have the ability to pull associated trace and span information without needing to record full context.  
  КонтекстСпана передается в Предложить(), из него извлекаются traceId/spanId. (`src/Метрики/Классы/ОтелРезервуарЭкземпляров.os`)

- ⚠️ **[Metrics Sdk]** [SHOULD] Exemplars are expected to abide by the AggregationTemporality of any metric point they are recorded with. Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point.  
  ОчиститьТочкиДанных (line 131-136) clears the reservoir after collection, which partially supports delta temporality. However, there is no explicit check or guarantee that exemplars fall within the start/stop timestamps of the metric point. The reservoir simply accumulates and is cleared on export. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:134`)

- ❌ **[Metrics Sdk]** [SHOULD] The ExemplarReservoir SHOULD avoid allocations when sampling exemplars.  
  The reservoir creates new Массив instances and uses СинхронизированнаяКарта with dynamic insertions. Each exemplar creates a new Соответствие (Map) in ЗахватитьЭкземпляр. There is no evidence of allocation avoidance strategies like pre-allocated slots or object pooling. (-)

- ✅ **[Metrics Sdk]** [SHOULD] Explicit bucket histogram aggregation with more than 1 bucket SHOULD use AlignedHistogramBucketExemplarReservoir.  
  Гистограммы используют ОтелВыровненныйРезервуарГистограммы с границами бакетов. (`src/Метрики/Классы/ОтелМетр.os`)

- ✅ **[Metrics Sdk]** [SHOULD] Base2 Exponential Histogram Aggregation SHOULD use a SimpleFixedSizeExemplarReservoir with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty (e.g. min(20, max_buckets)).  
  Экспоненциальные гистограммы используют ОтелРезервуарЭкземпляров(Мин(20, МаксБакетов)). (`src/Метрики/Классы/ОтелМетр.os`)

- ✅ **[Metrics Sdk]** [SHOULD] All other aggregations SHOULD use SimpleFixedSizeExemplarReservoir.  
  Счетчики, датчики и реверсивные счетчики используют ОтелРезервуарЭкземпляров. (`src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os`)

- ❌ **[Metrics Sdk]** [SHOULD] Any stateful portion of sampling computation SHOULD be reset every collection cycle.  
  Метод Собрать() возвращает данные, но не сбрасывает счетчик num_measurements_seen (Счетчики). Метод Очистить() очищает все данные, но не вызывается автоматически при каждом цикле сбора. Нет автоматического сброса счетчиков при collection. (-)

- ✅ **[Metrics Sdk]** [SHOULD] This implementation SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled.  
  ОтелВыровненныйРезервуарГистограммы заменяет экземпляр в бакете последним измерением. (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os`)

- ✅ **[Metrics Sdk]** [SHOULD] This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation.  
  ОтелВыровненныйРезервуарГистограммы принимает тот же формат массива границ, что и агрегатор гистограммы. (`src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os`)

- ⚠️ **[Metrics Sdk]** [SHOULD] Collect SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() (аналог Collect) является Процедурой, а не Функцией - не возвращает результат (успех/ошибка/таймаут). Ошибки логируются, но вызывающий код не получает информацию о результате. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:68`)

- ❌ **[Metrics Sdk]** [SHOULD] Collect SHOULD invoke Produce on registered MetricProducers.  
  Нет реализации MetricProducer и метода Produce. Collect собирает данные только из зарегистрированных Meter, но не из внешних MetricProducer. (-)

- ❌ **[Metrics Sdk]** [SHOULD] SDKs SHOULD return some failure for calls to Collect after Shutdown, if possible.  
  Нет проверки флага Закрыт в методах СброситьБуфер() и СобратьИЭкспортировать(). После Shutdown эти методы продолжают работать нормально, не возвращая ошибку. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод Закрыть() - Процедура, а не Функция, не возвращает результат. Таймаут обрабатывается при ожидании фонового задания, но результат не передается вызывающему коду. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:85`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  Метод СброситьБуфер() является Процедурой и не возвращает результат. Ошибки логируются, но вызывающий код не информируется об успехе или неудаче. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:68`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status.  
  СброситьБуфер() - Процедура без возвращаемого значения. Нет статусов ERROR/NO ERROR для возврата вызывающему коду. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:68`)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  Метод СброситьБуфер() вызывает СобратьИЭкспортировать() синхронно без таймаута. Нет механизма ограничения времени выполнения ForceFlush. (-)

- ❌ **[Metrics Sdk]** [SHOULD] Metric Exporters SHOULD report an error condition for data output by the MetricReader with unsupported Aggregation or Aggregation Temporality.  
  Экспортер не проверяет, соответствует ли Aggregation или Temporality его возможностям. Данные экспортируются без валидации типа агрегации. (-)

- ⚠️ **[Metrics Sdk]** [SHOULD] This is a hint to ensure that the export of any Metrics the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method.  
  Метод СброситьБуфер() экспортера пуст (нет буферизации - синхронный экспорт), что формально корректно, но нет явного указания что все данные экспортированы. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43`)

- ⚠️ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.  
  СброситьБуфер() экспортера - Процедура без возвращаемого значения, не информирует о результате. (`src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43`)

- ❌ **[Metrics Sdk]** [SHOULD] ForceFlush SHOULD complete or abort within some timeout.  
  СброситьБуфер() экспортера - пустой метод без таймаута. Для синхронного экспорта это неактуально, но при буферизации будет проблемой. (-)

- ❌ **[Metrics Sdk]** [SHOULD] MetricProducer implementations SHOULD accept configuration for the AggregationTemporality of produced metrics.  
  No MetricProducer interface exists. The Prometheus reader (ОтелПрометеусЧитательМетрик) does not accept AggregationTemporality configuration - it always outputs cumulative data per Prometheus convention. No separate MetricProducer with temporality config. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The obsolete OTEL_EXPORTER_OTLP_SPAN_INSECURE and OTEL_EXPORTER_OTLP_METRIC_INSECURE SHOULD continue to be supported as they were part of a stable release of the specification.  
  Устаревшие переменные OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE не реализованы. Требование условно (SHOULD continue to be supported if already implemented), но никогда не были реализованы. (-)

- ⚠️ **[Otlp Exporter]** [SHOULD] The default protocol SHOULD be http/protobuf unless SDKs have good reasons to choose grpc as the default.  
  Дефолтный протокол установлен как http/json (строка 150), а не http/protobuf. OneScript не поддерживает protobuf нативно для HTTP, поэтому используется JSON. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ⚠️ **[Otlp Exporter]** [SHOULD] If no configuration is provided the default transport SHOULD be http/protobuf unless SDKs have good reasons to choose grpc as the default.  
  Дефолтный протокол - http/json (строка 150), а не http/protobuf. HTTP-транспорт отправляет JSON, не protobuf. Это осознанный выбор из-за отсутствия нативной поддержки protobuf для HTTP в OneScript. (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150`)

- ❌ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter.  
  Нет User-Agent заголовка ни в HTTP-транспорте (ОтелHttpТранспорт.os), ни в gRPC-транспорте (ОтелGrpcТранспорт.os). HTTP-транспорт устанавливает только Content-Type и пользовательские заголовки. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The format of the User-Agent header SHOULD follow RFC 7231.  
  User-Agent заголовок не реализован, поэтому формат RFC 7231 также не может быть соблюден. (-)

- ❌ **[Otlp Exporter]** [SHOULD] The resulting User-Agent SHOULD include the exporter's default User-Agent string when a product identifier configuration option is used.  
  User-Agent заголовок не реализован вообще, конфигурация product identifier также отсутствует. (-)

- ⚠️ **[Propagators]** [SHOULD] The implementation SHOULD preserve casing (e.g. it should not transform Content-Type to content-type) if the used protocol is case insensitive, otherwise it MUST preserve casing.  
  Casing is preserved for injected keys (e.g. 'traceparent', 'tracestate', 'baggage' are lowercase constants). However, there is no explicit Setter interface - values are written directly via Заголовки.Вставить(), which preserves the key as-is. The implementation effectively preserves casing but lacks the Setter abstraction. (`src/Пропагация/Модули/ОтелW3CПропагатор.os:51`)

- ❌ **[Propagators]** [SHOULD] GetAll SHOULD return values in the same order as they appear in the carrier.  
  No GetAll function exists. See above - no Getter interface is implemented. (-)

- ❌ **[Propagators]** [SHOULD] If the key doesn't exist, GetAll SHOULD return an empty collection.  
  No GetAll function exists. No Getter interface is implemented. (-)

- ⚠️ **[Env Vars]** [SHOULD] They SHOULD also follow the common configuration specification.  
  Автоконфигурация использует configor (МенеджерПараметров) для чтения переменных окружения, что соответствует общему подходу конфигурации. Однако не все аспекты common configuration specification реализованы (например, нет поддержки OTEL_CONFIG_FILE). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:59`)

- ❌ **[Env Vars]** [SHOULD] If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied.  
  Функция Включено() в строке 561-564 просто сравнивает НРег(Значение) = "true" и возвращает Ложь для всех остальных значений. Нет логирования предупреждения при получении нестандартного значения (не "true", не "false", не пустое). (-)

- ❌ **[Env Vars]** [SHOULD] For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them as not set.  
  Числовые значения парсятся через Число() (например строка 224: Число(Менеджер.Параметр("otel.bsp.max.queue.size", "2048"))). При невалидном значении Число() выбросит исключение, а не сгенерирует предупреждение и проигнорирует настройку. Нет try/catch обёртки и нет логирования предупреждения. (-)

- ❌ **[Env Vars]** [SHOULD] For new implementations, these should be treated as MUST requirements (generate a warning and gracefully ignore unparseable numeric values).  
  То же что и предыдущее - нет graceful обработки невалидных числовых значений. Число() при невалидном вводе вызовет исключение вместо предупреждения и фолбэка на значение по умолчанию. (-)

- ❌ **[Env Vars]** [SHOULD] The following paragraph was added after stabilization and the requirements are thus qualified as "SHOULD" to allow implementations to avoid breaking changes.  
  Это контекстное предложение, уточняющее уровень SHOULD для предыдущих требований. Реализация не обрабатывает невалидные числовые значения gracefully - отсутствует try/catch и предупреждение. (-)

- ⚠️ **[Env Vars]** [SHOULD] Enum values SHOULD be interpreted in a case-insensitive manner.  
  Пропагаторы (otel.propagators) сравниваются case-insensitive через НРег() в строке 344. Однако другие enum-значения (otel.traces.sampler, otel.traces.exporter, otel.logs.exporter, otel.metrics.exporter) сравниваются case-sensitive (строки 177-178, 190-219, 255-256, 291-292). Например, ИмяСэмплера = "always_on" - сравнение без НРег(). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:344`)

## Детальный анализ по разделам (Stable)

### Context

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ ok | A Context MUST be immutable | `src/Ядро/Модули/ОтелКонтекст.os` | Контекст реализован как ФиксированноеСоответствие (иммутабельный). Все операции создают новую копию. |
| 2 | MUST | ✅ found | its write operations MUST result in the creation of a new Context containing the original values and the specified values updated | `src/Ядро/Модули/ОтелКонтекст.os:114` |  |
| 3 | MUST | ✅ found | OpenTelemetry MUST provide its own Context implementation | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### Create a key

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#create-a-key)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ ok | The API MUST accept the following parameter: The key name. The key name exists for debugging purposes and does not uniquely identify the key. | `src/Ядро/Модули/ОтелКонтекст.os:35` | ОтелКонтекст.СоздатьКлюч(Имя) создает ОтелКлючКонтекста с именем для отладки. |
| 5 | SHOULD NOT | ✅ ok | Multiple calls to CreateKey with the same name SHOULD NOT return the same value unless language constraints dictate otherwise | `src/Ядро/Модули/ОтелКонтекст.os:35` | Каждый вызов СоздатьКлюч() создает новый объект, сравнение по ссылке. |
| 6 | MUST | ✅ ok | The API MUST return an opaque object representing the newly created key | `src/Ядро/Классы/ОтелКлючКонтекста.os` | Возвращает ОтелКлючКонтекста - непрозрачный объект. |

#### Get value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ ok | The API MUST accept the following parameters: The Context. The key. | `src/Ядро/Модули/ОтелКонтекст.os` | ПолучитьИзКонтекста(Контекст, Ключ) - generic get с явным контекстом и ОтелКлючКонтекста. |
| 8 | MUST | ✅ found | The API MUST return the value in the Context for the specified key | `src/Ядро/Модули/ОтелКонтекст.os:47` |  |

#### Set value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ ok | The API MUST accept the following parameters: The Context. The key. The value to be set. | `src/Ядро/Модули/ОтелКонтекст.os` | КонтекстСоЗначением(Контекст, Ключ, Значение) - generic set с явным контекстом. |
| 10 | MUST | ✅ ok | The API MUST return a new Context containing the new value | `src/Ядро/Модули/ОтелКонтекст.os` | КонтекстСоЗначением() возвращает новый ФиксированноеСоответствие. |

#### Optional Global operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#optional-global-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | These operations SHOULD only be used to implement automatic scope switching and define higher level APIs by SDK components and OpenTelemetry instrumentation libraries | `src/Ядро/Модули/ОтелКонтекст.os:163` |  |

#### Get current Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-current-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST return the Context associated with the caller's current execution unit | `src/Ядро/Модули/ОтелКонтекст.os:29` |  |

#### Attach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#attach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ⚠️ partial | The API MUST accept the following parameters: The Context. | `src/Ядро/Модули/ОтелКонтекст.os:147` | There is no generic Attach(Context) method that accepts a Context (Соответствие) as a single parameter. Instead, the code provides specialized methods: УстановитьЗначение(Ключ, Значение) at line 147, СделатьСпанТекущим(Спан) at line 163, and СделатьBaggageТекущим(Багаж) at line 176 — none of which accept a whole Context object as the spec requires. |
| 14 | MUST | ✅ found | The API MUST return a value that can be used as a Token to restore the previous Context. | `src/Ядро/Модули/ОтелКонтекст.os:151` |  |

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
| 4 | MUST | ✅ found | Language API MUST treat both baggage names and values as case sensitive. | `src/Ядро/Классы/ОтелBaggage.os:156` |  |
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
| 11 | MUST | ✅ found | If an implementation of this API does not operate directly on the Context, it MUST provide the following functionality to interact with a Context instance: Extract the Baggage from a Context instance; Insert the Baggage to a Context instance. | `src/Ядро/Модули/ОтелКонтекст.os:97` |  |
| 12 | SHOULD NOT | ✅ found | API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:17` |  |
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
| 16 | MUST | ✅ found | The API layer or an extension package MUST include the following Propagators: A TextMapPropagator implementing the W3C Baggage Specification. | `src/Пропагация/Модули/ОтелW3CBaggageПропагатор.os:17` |  |

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
| 1 | MUST | ✅ found | The SDK MUST allow for creation of Resources and for associating them with telemetry. | `src/Ядро/Классы/ОтелРесурс.os:95` |  |
| 2 | MUST | ✅ found | When associated with a TracerProvider, all Spans produced by any Tracer from the provider MUST be associated with this Resource. | `src/Трассировка/Классы/ОтелТрассировщик.os:70` |  |

#### SDK-provided resource attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#sdk-provided-resource-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The SDK MUST provide access to a Resource with at least the attributes listed at Semantic Attributes with SDK-provided Default Value. | `src/Ядро/Классы/ОтелРесурс.os:104` |  |
| 4 | MUST | ✅ found | This resource MUST be associated with a TracerProvider or MeterProvider if another resource was not explicitly specified. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:214` |  |

#### Create

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#create)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The interface MUST provide a way to create a new resource, from Attributes. | `src/Ядро/Классы/ОтелПостроительРесурса.os:61` |  |
| 6 | MUST | ✅ found | The interface MUST provide a way for an old resource and an updating resource to be merged into a new resource. | `src/Ядро/Классы/ОтелРесурс.os:44` |  |
| 7 | MUST | ✅ found | The resulting resource MUST have all attributes that are on any of the two input resources. | `src/Ядро/Классы/ОтелРесурс.os:58` |  |
| 8 | MUST | ✅ found | If a key exists on both the old and updating resource, the value of the updating resource MUST be picked (even if the updated value is empty). | `src/Ядро/Классы/ОтелРесурс.os:61` |  |

#### Detecting resource information from the environment

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#detecting-resource-information-from-the-environment)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os` |  |
| 10 | MUST | ✅ found | Resource detector packages MUST provide a method that returns a resource. This can then be associated with TracerProvider or MeterProvider instances. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17` |  |
| 11 | MUST NOT | ✅ found | The failure to detect any resource information MUST NOT be considered an error. | `src/Ядро/Классы/ОтелРесурс.os:120` |  |
| 12 | SHOULD | ⚠️ partial | An error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелРесурс.os:121` | Errors during resource detection are caught via Попытка/Исключение but logged at Лог.Отладка (debug) level instead of error level. Per spec, detection errors SHOULD be treated as errors, but they are silently suppressed to debug log. |
| 13 | MUST | ⚠️ partial | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os` | Детекторы вынесены в отдельные классы, но Schema URL пока не устанавливается. |
| 14 | SHOULD | ⚠️ partial | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will populate. | `src/Ядро/Классы/ОтелРесурс.os:98` | The resource uses empty Schema URL (АдресСхемы defaults to ''), but the inline detection DOES populate known semantic convention attributes (host.name, os.type, process.pid). Per spec, empty URL is for detectors that don't know what they populate - this detector knows exactly what it populates, so it should set a schema URL per the previous MUST requirement. |
| 15 | MUST | ✅ found | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources. | `src/Ядро/Классы/ОтелРесурс.os:45` |  |

### Trace Api

#### Timestamp

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#timestamp)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD provide a way to set/register and access a global default TracerProvider. | `src/Ядро/Модули/ОтелГлобальный.os:30` |  |
| 2 | SHOULD | ✅ found | Implementations of TracerProvider SHOULD allow creating an arbitrary number of TracerProvider instances. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:207` |  |

#### TracerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The TracerProvider MUST provide the following functions: Get a Tracer | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52` |  |
| 4 | MUST | ✅ found | This API MUST accept the following parameters: name (required) | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:53` |  |
| 5 | SHOULD | ✅ found | This name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:57` |  |
| 6 | MUST | ⚠️ partial | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52` | ПолучитьТрассировщик принимает пустую строку и создает рабочий трассировщик, но нет явной проверки на пустое/null имя и нет логирования предупреждения |
| 7 | SHOULD | ⚠️ partial | Its name property SHOULD be set to an empty string, and a message reporting that the specified value is invalid SHOULD be logged | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52` | Имя сохраняется как есть (в том числе пустая строка), но предупреждение о невалидном имени не логируется |
| 8 | SHOULD | ⚠️ partial | A message reporting that the specified value is invalid SHOULD be logged when an invalid name is specified | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52` | Нет логирования предупреждения при пустом/невалидном имени |
| 9 | MUST NOT | ✅ found | Implementations MUST NOT require users to repeatedly obtain a Tracer again with the same identity to pick up configuration changes | `src/Трассировка/Классы/ОтелТрассировщик.os:160` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API MUST provide the following functionality to interact with a Context instance: Extract the Span from a Context instance; Combine the Span with a Context instance, creating a new Context instance | `src/Ядро/Модули/ОтелКонтекст.os:82` |  |
| 11 | SHOULD NOT | ✅ found | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation | `src/Ядро/Модули/ОтелКонтекст.os:312` |  |
| 12 | SHOULD | ✅ found | If the language has support for implicitly propagated Context, the API SHOULD also provide the following functionality: Get the currently active span from the implicit context; Set the currently active span into a new context, and make that the implicit context | `src/Ядро/Модули/ОтелКонтекст.os:56` |  |
| 13 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible | `src/Ядро/Модули/ОтелКонтекст.os:1` |  |

#### SpanContext

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spancontext)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The API MUST implement methods to create a SpanContext | `src/Трассировка/Классы/ОтелКонтекстСпана.os:124` |  |
| 15 | SHOULD | ✅ found | These methods SHOULD be the only way to create a SpanContext | `src/Трассировка/Классы/ОтелКонтекстСпана.os:124` |  |
| 16 | MUST | ✅ found | This functionality MUST be fully implemented in the API | `src/Трассировка/Классы/ОтелКонтекстСпана.os:1` |  |
| 17 | SHOULD NOT | ✅ found | This functionality SHOULD NOT be overridable | `src/Трассировка/Классы/ОтелКонтекстСпана.os:1` |  |

#### Retrieving the TraceId and SpanId

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#retrieving-the-traceid-and-spanid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | The API MUST allow retrieving the TraceId and SpanId in the following forms: Hex | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 19 | MUST | ✅ found | Hex - returns the lowercase hex encoded TraceId (result MUST be a 32-hex-character lowercase string) | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |
| 20 | MUST | ✅ found | Hex - returns the lowercase hex encoded SpanId (result MUST be a 16-hex-character lowercase string) | `src/Трассировка/Классы/ОтелКонтекстСпана.os:32` |  |
| 21 | MUST | ✅ found | Binary - returns the binary representation of the TraceId (result MUST be a 16-byte array) | `src/Трассировка/Классы/ОтелКонтекстСпана.os` | Метод ИдТрассировкиВДвоичномВиде() возвращает бинарное представление TraceId |
| 22 | MUST | ✅ found | Binary - returns the binary representation of the SpanId (result MUST be an 8-byte array) | `src/Трассировка/Классы/ОтелКонтекстСпана.os` | Метод ИдСпанаВДвоичномВиде() возвращает бинарное представление SpanId |
| 23 | SHOULD NOT | ✅ found | The API SHOULD NOT expose details about how they are internally stored | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23` |  |

#### IsValid

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isvalid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | An API called IsValid, that returns a boolean value, which is true if the SpanContext has a non-zero TraceID and a non-zero SpanID, MUST be provided | `src/Трассировка/Классы/ОтелКонтекстСпана.os:70` |  |

#### IsRemote

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isremote)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | An API called IsRemote, that returns a boolean value, which is true if the SpanContext was propagated from a remote parent, MUST be provided | `src/Трассировка/Классы/ОтелКонтекстСпана.os:60` |  |
| 26 | MUST | ✅ found | When extracting a SpanContext through the Propagators API, IsRemote MUST return true | `src/Пропагация/Модули/ОтелW3CПропагатор.os:115` |  |
| 27 | MUST | ✅ found | For the SpanContext of any child spans it MUST return false | `src/Трассировка/Классы/ОтелКонтекстСпана.os:128` |  |

#### TraceState

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracestate)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | Tracing API MUST provide at least the following operations on TraceState: Get value for a given key, Add a new key/value pair, Update an existing value for a given key, Delete a key/value pair | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:44,66,105` |  |
| 29 | MUST | ✅ found | These operations MUST follow the rules described in the W3C Trace Context specification | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:227` |  |
| 30 | MUST | ✅ found | All mutating operations MUST return a new TraceState with the modifications applied | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:92` |  |
| 31 | MUST | ✅ found | TraceState MUST at all times be valid according to rules specified in W3C Trace Context specification | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:220` |  |
| 32 | MUST | ✅ found | Every mutating operations MUST validate input parameters | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67` |  |
| 33 | MUST NOT | ✅ found | If invalid value is passed the operation MUST NOT return TraceState containing invalid data | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:68` |  |
| 34 | MUST | ✅ found | If invalid value is passed the operation MUST follow the general error handling guidelines | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:68` |  |

#### Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | SHOULD | ✅ found | The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable | `src/Трассировка/Классы/ОтелСпан.os:4` |  |
| 36 | SHOULD | ✅ found | Generality SHOULD be prioritized over human-readability | `src/Трассировка/Классы/ОтелСпан.os:4` |  |
| 37 | SHOULD | ✅ found | A Span's start time SHOULD be set to the current time on span creation | `src/Трассировка/Классы/ОтелСпан.os:563` |  |
| 38 | SHOULD | ✅ found | After the Span is created, it SHOULD be possible to change its name, set its Attributes, add Events, and set the Status | `src/Трассировка/Классы/ОтелСпан.os:239,255,284,402` |  |
| 39 | MUST NOT | ✅ found | These (name, Attributes, Events, Status) MUST NOT be changed after the Span's end time has been set | `src/Трассировка/Классы/ОтелСпан.os:240` |  |
| 40 | SHOULD NOT | ⚠️ partial | implementations SHOULD NOT provide access to a Span's attributes besides its SpanContext | `src/Трассировка/Классы/ОтелСпан.os:126` | ОтелСпан публично предоставляет Атрибуты(), События(), Линки() и другие свойства. OneScript не поддерживает интерфейсы, поэтому один класс обслуживает и API, и SDK (процессорам нужен доступ к данным для экспорта) |
| 41 | MUST NOT | ⚠️ partial | alternative implementations MUST NOT allow callers to create Spans directly | `src/Трассировка/Классы/ОтелТрассировщик.os:48` | OneScript не поддерживает модификаторы доступа - все конструкторы публичны. Пользователь технически может вызвать Новый ОтелСпан(...) напрямую, хотя дизайн API направляет через Трассировщик |
| 42 | MUST | ⚠️ partial | All Spans MUST be created via a Tracer | `src/Трассировка/Классы/ОтелТрассировщик.os:48` | Дизайн API направляет через Трассировщик (НачатьСпан, НачатьДочернийСпан, НачатьКорневойСпан, ПостроительСпана), но OneScript не может запретить прямое создание через конструктор из-за отсутствия модификаторов доступа |

#### Span Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST NOT | ⚠️ partial | There MUST NOT be any API for creating a Span other than with a Tracer | `src/Трассировка/Классы/ОтелТрассировщик.os:48` | Все штатные API создания спана идут через Трассировщик, но конструктор ОтелСпан публичен из-за ограничений OneScript (нет модификаторов доступа) |
| 44 | MUST NOT | ✅ found | Span creation MUST NOT set the newly created Span as the active Span in the current Context by default | `src/Трассировка/Классы/ОтелТрассировщик.os:48` |  |
| 45 | MUST | ✅ found | The API MUST accept the following parameters: span name (required), parent Context, SpanKind, Attributes, Links, Start timestamp | `src/Трассировка/Классы/ОтелПостроительСпана.os:22` |  |
| 46 | MUST NOT | ⚠️ partial | This API MUST NOT accept a Span or SpanContext as parent, only a full Context | `src/Трассировка/Классы/ОтелПостроительСпана.os:33` | SpanBuilder.УстановитьРодителя() принимает ОтелСпан или ОтелКонтекстСпана напрямую, а не полный Context (Соответствие). Также Трассировщик.НачатьДочернийСпан() принимает Span/SpanContext. Неявное использование контекста в НачатьСпан() работает корректно |
| 47 | MUST | ✅ found | The semantic parent of the Span MUST be determined according to the rules described in Determining the Parent Span from a Context | `src/Трассировка/Классы/ОтелТрассировщик.os:49` |  |
| 48 | MUST | ✅ found | The API documentation MUST state that adding attributes at span creation is preferred to calling SetAttribute later, as samplers can only consider information already present during span creation | `src/Трассировка/Классы/ОтелПостроительСпана.os` | Документация добавлена в ОтелПостроительСпана |
| 49 | SHOULD | ✅ found | Start timestamp argument SHOULD only be set when span creation time has already passed | `src/Трассировка/Классы/ОтелПостроительСпана.os:107` |  |
| 50 | MUST NOT | ✅ found | If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument (start timestamp) | `src/Трассировка/Классы/ОтелПостроительСпана.os:107` |  |
| 51 | MUST | ✅ found | Implementations MUST provide an option to create a Span as a root span | `src/Трассировка/Классы/ОтелТрассировщик.os:91` |  |
| 52 | MUST | ✅ found | Implementations MUST generate a new TraceId for each root span created | `src/Трассировка/Классы/ОтелТрассировщик.os:92` |  |
| 53 | MUST | ✅ found | For a Span with a parent, the TraceId MUST be the same as the parent | `src/Трассировка/Классы/ОтелТрассировщик.os:52` |  |
| 54 | MUST | ✅ found | Also, the child span MUST inherit all TraceState values of its parent by default | `src/Трассировка/Классы/ОтелТрассировщик.os` | ОтелТрассировщик.ОпределитьСостояниеТрассировки() наследует TraceState из родителя или результата семплирования |
| 55 | MUST | ✅ found | Any span that is created MUST also be ended. This is the responsibility of the user | `src/Трассировка/Классы/ОтелСпан.os:436` |  |

#### Specifying links

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#specifying-links)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 56 | MUST | ✅ found | During Span creation, a user MUST have the ability to record links to other Spans | `src/Трассировка/Классы/ОтелПостроительСпана.os:90` |  |

#### Get Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 57 | MUST | ✅ found | The Span interface MUST provide: An API that returns the SpanContext for the given Span. This MAY be called GetContext | `src/Трассировка/Классы/ОтелСпан.os:72` |  |
| 58 | MUST | ✅ found | The returned value MUST be the same for the entire Span lifetime | `src/Трассировка/Классы/ОтелСпан.os:555` |  |
| 59 | SHOULD | ✅ found | After a Span is ended, it SHOULD become non-recording | `src/Трассировка/Классы/ОтелСпан.os:227` |  |
| 60 | SHOULD | ✅ found | After a Span is ended, IsRecording SHOULD always return false | `src/Трассировка/Классы/ОтелСпан.os:227` |  |
| 61 | SHOULD NOT | ✅ found | IsRecording SHOULD NOT take any parameters | `src/Трассировка/Классы/ОтелСпан.os:226` |  |
| 62 | SHOULD | ✅ found | This flag (IsRecording) SHOULD be used to avoid expensive computations of a Span attributes or events in case when a Span is definitely not recorded | `src/Трассировка/Классы/ОтелПостроительСпана.os:127` |  |

#### Set Attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 63 | MUST | ✅ found | A Span MUST have the ability to set Attributes associated with it | `src/Трассировка/Классы/ОтелСпан.os:255` |  |
| 64 | MUST | ✅ found | The Span interface MUST provide: An API to set a single Attribute where the attribute properties are passed as arguments. This MAY be called SetAttribute | `src/Трассировка/Классы/ОтелСпан.os:255` |  |
| 65 | SHOULD | ✅ found | Setting an attribute with the same key as an existing attribute SHOULD overwrite the existing attribute's value | `src/Трассировка/Классы/ОтелСпан.os:269` |  |

#### Add Events

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-events)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | MUST | ✅ found | A Span MUST have the ability to add events. Events have a time associated with the moment when they are added to the Span | `src/Трассировка/Классы/ОтелСпан.os:284` |  |
| 67 | MUST | ✅ found | The Span interface MUST provide: An API to record a single Event where the Event properties are passed as arguments. This MAY be called AddEvent | `src/Трассировка/Классы/ОтелСпан.os:284` |  |
| 68 | SHOULD | ✅ found | Events SHOULD preserve the order in which they are recorded | `src/Трассировка/Классы/ОтелСпан.os:288` |  |

#### Add Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | MUST | ✅ found | A Span MUST have the ability to add Links associated with it after its creation | `src/Трассировка/Классы/ОтелСпан.os:351` |  |

#### Set Status

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-status)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 70 | MUST | ✅ found | Description MUST only be used with the Error StatusCode value. | `src/Трассировка/Классы/ОтелСпан.os:418` |  |
| 71 | MUST | ✅ found | The Span interface MUST provide: An API to set the Status. | `src/Трассировка/Классы/ОтелСпан.os:402` |  |
| 72 | SHOULD | ⚠️ partial | This SHOULD be called SetStatus. | `src/Трассировка/Классы/ОтелСпан.os:402` | Method is named УстановитьСтатус (Russian translation), not SetStatus, but the naming convention uses Russian throughout. |
| 73 | MUST | ✅ found | Description MUST be IGNORED for StatusCode Ok & Unset values. | `src/Трассировка/Классы/ОтелСпан.os:418` |  |
| 74 | SHOULD | ✅ found | The status code SHOULD remain unset, except for the following circumstances. | `src/Трассировка/Классы/ОтелСпан.os:568` |  |
| 75 | SHOULD | ✅ found | An attempt to set value Unset SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:413` |  |
| 76 | SHOULD | ❌ not_found | When the status is set to Error by Instrumentation Libraries, the Description SHOULD be documented and predictable. | - | No documentation or conventions for standard error descriptions in instrumentation libraries are provided. |
| 77 | SHOULD | ❌ not_found | Instrumentation Libraries SHOULD publish their own conventions for Description values, including possible values and what they mean. | - | No published conventions for Description values found in the codebase. |
| 78 | SHOULD NOT | ✅ found | Generally, Instrumentation Libraries SHOULD NOT set the status code to Ok, unless explicitly configured to do so. | `src/Трассировка/Классы/ОтелСпан.os:402` |  |
| 79 | SHOULD | ✅ found | Instrumentation Libraries SHOULD leave the status code as Unset unless there is an error. | `src/Трассировка/Классы/ОтелСпан.os:568` |  |
| 80 | SHOULD | ✅ found | When span status is set to Ok it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:408` |  |
| 81 | SHOULD | ✅ found | Any further attempts to change Ok status SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:408` |  |
| 82 | SHOULD | ❌ not_found | Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generate. | - | This is a requirement for analysis/visualization tools, not directly verifiable in the SDK code itself. No analysis tool behavior is implemented. |

#### UpdateName

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#updatename)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 83 | SHOULD | ✅ found | Implementations SHOULD ignore all subsequent calls to End and any other Span methods, i.e. the Span becomes non-recording by being ended. | `src/Трассировка/Классы/ОтелСпан.os:437` |  |
| 84 | MUST | ✅ found | However, all API implementations of such methods MUST internally call the End method and be documented to do so. | `src/Трассировка/Классы/ОтелСпан.os:436` |  |
| 85 | MUST NOT | ✅ found | End MUST NOT have any effects on child spans. Those may still be running and can be ended later. | `src/Трассировка/Классы/ОтелСпан.os:436` |  |
| 86 | MUST NOT | ✅ found | End MUST NOT inactivate the Span in any Context it is active in. | `src/Трассировка/Классы/ОтелСпан.os:436` |  |
| 87 | MUST | ✅ found | It MUST still be possible to use an ended span as parent via a Context it is contained in. | `src/Ядро/Модули/ОтелКонтекст.os:163` |  |
| 88 | MUST | ✅ found | Also, any mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:387` |  |
| 89 | MUST | ✅ found | If omitted, this MUST be treated equivalent to passing the current time (end timestamp parameter). | `src/Трассировка/Классы/ОтелСпан.os:438` |  |
| 90 | MUST NOT | ✅ found | This operation itself MUST NOT perform blocking I/O on the calling thread. | `src/Трассировка/Классы/ОтелСпан.os:444` |  |
| 91 | SHOULD | ✅ found | Any locking used needs be minimized and SHOULD be removed entirely if possible. | `src/Трассировка/Классы/ОтелСпан.os:436` |  |

#### Record Exception

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#record-exception)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 92 | SHOULD | ✅ found | To facilitate recording an exception languages SHOULD provide a RecordException method if the language uses exceptions. | `src/Трассировка/Классы/ОтелСпан.os:307` |  |
| 93 | MUST | ✅ found | The method MUST record an exception as an Event with the conventions outlined in the exceptions document. | `src/Трассировка/Классы/ОтелСпан.os:312` |  |
| 94 | SHOULD | ✅ found | The minimum required argument SHOULD be no more than only an exception object. | `src/Трассировка/Классы/ОтелСпан.os:307` |  |
| 95 | MUST | ✅ found | If RecordException is provided, the method MUST accept an optional parameter to provide any additional event attributes. | `src/Трассировка/Классы/ОтелСпан.os:307` |  |
| 96 | SHOULD | ✅ found | This SHOULD be done in the same way as for the AddEvent method (additional attributes parameter). | `src/Трассировка/Классы/ОтелСпан.os:307` |  |

#### Span lifetime

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-lifetime)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | MUST | ✅ found | Start and end time as well as Event's timestamps MUST be recorded at a time of a calling of corresponding API. | `src/Трассировка/Классы/ОтелСпан.os:563` |  |

#### Wrapping a SpanContext in a Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#wrapping-a-spancontext-in-a-span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | MUST | ✅ found | The API MUST provide an operation for wrapping a SpanContext with an object implementing the Span interface. | `src/Трассировка/Классы/ОтелНоопСпан.os:272` |  |
| 99 | SHOULD NOT | ✅ found | If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |
| 100 | SHOULD | ⚠️ partial | If a new type is required to be publicly exposed, it SHOULD be named NonRecordingSpan. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` | The type is named ОтелНоопСпан (NoopSpan), not NonRecordingSpan. While functional behavior matches, the naming convention differs from the spec recommendation. |
| 101 | MUST | ✅ found | GetContext MUST return the wrapped SpanContext. | `src/Трассировка/Классы/ОтелНоопСпан.os:29` |  |
| 102 | MUST | ✅ found | IsRecording MUST return false to signal that events, attributes and other elements are not being recorded. | `src/Трассировка/Классы/ОтелНоопСпан.os:155` |  |
| 103 | MUST | ✅ found | The remaining functionality of Span MUST be defined as no-op operations. | `src/Трассировка/Классы/ОтелНоопСпан.os:167` |  |
| 104 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |
| 105 | SHOULD NOT | ✅ found | This functionality SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелНоопСпан.os:1` |  |

#### SpanKind

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 106 | SHOULD | ✅ found | In order for SpanKind to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose. | `src/Трассировка/Модули/ОтелВидСпана.os:1` |  |
| 107 | SHOULD NOT | ✅ found | For example, a server-side span SHOULD NOT be used to describe outgoing remote procedure call. | `src/Трассировка/Модули/ОтелВидСпана.os:1` |  |
| 108 | MUST | ✅ found | A user MUST have the ability to record links to other SpanContexts. | `src/Трассировка/Классы/ОтелСпан.os:351` |  |
| 109 | MUST | ✅ found | The API MUST provide: An API to record a single Link where the Link properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:351` |  |
| 110 | SHOULD | ✅ found | Implementations SHOULD record links containing SpanContext with empty TraceId or SpanId (all zeros) as long as either the attribute set or TraceState is non-empty. | `src/Трассировка/Классы/ОтелСпан.os:351` |  |
| 111 | SHOULD | ✅ found | Span SHOULD preserve the order in which Links are set. | `src/Трассировка/Классы/ОтелСпан.os:567` |  |
| 112 | MUST | ✅ found | The API documentation MUST state that adding links at span creation is preferred to calling AddLink later, for contexts that are available during span creation, because head sampling decisions can only consider information present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os` | Документация добавлена в ОтелПостроительСпана |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 113 | MUST | ✅ found | TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os` | Документация потокобезопасности добавлена |
| 114 | MUST | ✅ found | Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелТрассировщик.os` | Документация потокобезопасности добавлена |
| 115 | MUST | ✅ found | Span - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os` | Документация потокобезопасности добавлена |
| 116 | MUST | ✅ found | Event - Events are immutable and MUST be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСобытиеСпана.os` | Документация неизменяемости и потокобезопасности добавлена |
| 117 | SHOULD | ⚠️ partial | Link - Links are immutable and SHOULD be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:361` | Links are stored as Соответствие (Map) objects in an array. They are effectively immutable after creation, but not documented as such. No explicit concurrency safety documentation. |

#### Behavior of the API in the absence of an installed SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#behavior-of-the-api-in-the-absence-of-an-installed-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 118 | MUST | ✅ found | The API MUST return a non-recording Span with the SpanContext in the parent Context (whether explicitly given or implicit current). | `src/Трассировка/Классы/ОтелТрассировщик.os:63` | При отклонении семплером возвращается NoopSpan. ОтелГлобальный лениво создаёт noop SDK - без настроенного SDK также возвращается non-recording span. |
| 119 | SHOULD | ❌ not_found | If the Span in the parent Context is already non-recording, it SHOULD be returned directly without instantiating a new Span. | - | The Tracer always creates a new ОтелНоопСпан even when the parent is already non-recording. There is no check in НачатьСпан to detect and directly return an existing non-recording parent span. |
| 120 | MUST | ✅ found | If the parent Context contains no Span, an empty non-recording Span MUST be returned instead (i.e., having a SpanContext with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFlags). | `src/Трассировка/Классы/ОтелНоопСпан.os:277` |  |

### Trace Sdk

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, Sampler, and TracerConfigurator) MUST be owned by the TracerProvider. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:6-22` |  |
| 2 | MUST | ✅ found | The updated configuration MUST also apply to all already returned Tracers (i.e. it MUST NOT matter whether a Tracer was obtained from the TracerProvider before or after the configuration change). | `src/Трассировка/Классы/ОтелТрассировщик.os:5-6` |  |
| 3 | MUST NOT | ✅ found | It MUST NOT matter whether a Tracer was obtained from the TracerProvider before or after the configuration change. | `src/Трассировка/Классы/ОтелТрассировщик.os:67` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:91-95` | СброситьБуфер() - процедура без возвращаемого значения, не сообщает вызывающему об успехе/неудаче/таймауте. |
| 5 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:91-95` | СброситьБуфер() не имеет механизма таймаута - блокирующий вызов без ограничения времени. |
| 6 | MUST | ✅ found | ForceFlush MUST invoke ForceFlush on all registered SpanProcessors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:92-94` |  |

#### Additional Span Interfaces

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#additional-span-interfaces)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | Readable span: A function receiving this as argument MUST be able to access all information that was added to the span, as listed in the API spec for Span. | `src/Трассировка/Классы/ОтелСпан.os:63-218` |  |
| 8 | MUST | ✅ found | A function receiving this as argument MUST be able to access the InstrumentationScope and Resource information (implicitly) associated with the span. | `src/Трассировка/Классы/ОтелСпан.os:153-163` |  |
| 9 | MUST | ⚠️ partial | For backwards compatibility it MUST also be able to access the InstrumentationLibrary [deprecated since 1.10.0] having the same name and version values as the InstrumentationScope. | `src/Трассировка/Классы/ОтелСпан.os:162` | Нет отдельного InstrumentationLibrary (deprecated alias). Есть только ОбластьИнструментирования, что по сути то же самое, но без явного deprecated alias. |
| 10 | MUST | ✅ found | A function receiving this as argument MUST be able to reliably determine whether the Span has ended. | `src/Трассировка/Классы/ОтелСпан.os:189-191` |  |
| 11 | MUST | ✅ found | Counts for attributes, events and links dropped due to collection limits MUST be available for exporters to report as described in the exporters specification. | `src/Трассировка/Классы/ОтелСпан.os:198-217` |  |
| 12 | MUST | ✅ found | Implementations MAY choose not to expose the full parent Context of the Span but they MUST expose at least the full parent SpanContext. | `src/Трассировка/Классы/ОтелСпан.os:81-83` |  |
| 13 | MUST | ✅ found | Read/write span: It MUST be possible for functions being called with this to somehow obtain the same Span instance and type that the span creation API returned (or will return) to the user. | `src/Трассировка/Классы/ОтелСпан.os:535-594` |  |

#### Sampling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | Span Processor MUST receive only those spans which have this field [IsRecording] set to true. | `src/Трассировка/Классы/ОтелТрассировщик.os:61-79` |  |
| 15 | SHOULD NOT | ⚠️ partial | Span Exporter SHOULD NOT receive them unless the Sampled flag was also set. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-31` | Процессор передает все завершённые спаны экспортеру без проверки флага Sampled. Если семплер вернёт RECORD_ONLY (решение=1), спан всё равно будет экспортирован. Встроенные семплеры никогда не возвращают RECORD_ONLY, но архитектурно проверка отсутствует. |
| 16 | MUST | ✅ found | Span Exporters MUST receive those spans which have Sampled flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-31` |  |
| 17 | SHOULD NOT | ⚠️ partial | Span Exporters SHOULD NOT receive the ones that do not have Sampled flag set. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26-31` | Нет фильтрации по флагу Sampled в цепочке процессор→экспортер. Все спаны, прошедшие семплирование (RECORD_ONLY или RECORD_AND_SAMPLE), передаются экспортеру без различия. |
| 18 | MUST NOT | ✅ found | The flag combination SampledFlag == true and IsRecording == false could cause gaps in the distributed trace, and because of this the OpenTelemetry SDK MUST NOT allow this combination. | `src/Трассировка/Классы/ОтелТрассировщик.os:62-64` |  |

#### SDK Span creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sdk-span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | When asked to create a Span, the SDK MUST act as if doing the following in order: use valid parent trace ID or generate new (before ShouldSample), query Sampler's ShouldSample, generate new span ID independently of sampling decision, create span depending on ShouldSample decision. | `src/Трассировка/Классы/ОтелТрассировщик.os:48-79` |  |

#### ShouldSample

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shouldsample)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | TraceId of the Span to be created. If the parent SpanContext contains a valid TraceId, they MUST always match. | `src/Трассировка/Классы/ОтелТрассировщик.os:52-61` |  |
| 21 | MUST NOT | ✅ found | RECORD_ONLY - IsRecording will be true, but the Sampled flag MUST NOT be set. | `src/Трассировка/Классы/ОтелТрассировщик.os` | ВычислитьФлагиТрассировки() возвращает 0 для RECORD_ONLY и 1 для RECORD_AND_SAMPLED |
| 22 | MUST | ✅ found | RECORD_AND_SAMPLE - IsRecording will be true and the Sampled flag MUST be set. | `src/Трассировка/Классы/ОтелСпан.os:555` |  |
| 23 | SHOULD | ❌ not_found | If the sampler returns an empty Tracestate here, the Tracestate will be cleared, so samplers SHOULD normally return the passed-in Tracestate if they do not intend to change it. | - | Семплер ОтелСэмплер.ДолженСэмплировать() не принимает TraceState родителя как параметр и не передаёт его в ОтелРезультатСэмплирования. Вместо этого создаётся новый пустой ОтелСостояниеТрассировки, что приводит к потере родительского TraceState. |
| 24 | SHOULD NOT | ✅ found | Description MAY change over time. Callers SHOULD NOT cache the returned value of GetDescription. | `src/Трассировка/Модули/ОтелСэмплер.os` | Реализована функция Описание(). |

#### TraceID randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#traceid-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | SHOULD | ⚠️ partial | For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trace Context Level 2 Candidate Recommendation when generating TraceID values. | `src/Ядро/Модули/ОтелУтилиты.os:78-92` | TraceID генерируется через UUID v4 (Новый УникальныйИдентификатор), что обеспечивает достаточную случайность (122 бита). Однако специфические требования W3C Trace Context Level 2 (например, флаг Random) не реализованы. TraceID случайный, но SDK не сигнализирует об этом через флаг. |

#### Random trace flag

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#random-trace-flag)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | SHOULD | ❌ not_found | For root span contexts, the SDK SHOULD set the Random flag in the trace flags when it generates TraceIDs that meet the W3C Trace Context Level 2 randomness requirements. | - | Флаг Random (бит W3C Trace Context Level 2) не устанавливается. ОтелКонтекстСпана создаётся с флагами=1 (только бит Sampled). Нет логики установки флага Random при генерации случайного TraceID. |

#### Explicit randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#explicit-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 27 | MUST NOT | ✅ found | SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value (the rv sub-key). | `src/Трассировка/Классы/ОтелТрассировщик.os` | TraceState наследуется от родителя, rv сохраняется |
| 28 | SHOULD | ✅ found | For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Context Level 2 randomness requirements, unless an explicit randomness value is present in the rv sub-key of the OpenTelemetry TraceState. | `src/Трассировка/Модули/ОтелСэмплер.os:260-262` |  |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | SHOULD | ❌ not_found | Custom implementations of the IdGenerator SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace random flag will be set in the associated Trace contexts. | - | The custom IdGenerator mechanism (УстановитьГенераторИд) has no way for implementations to declare W3C Level 2 randomness compliance. There is no marker interface, flag property, or any mechanism to indicate randomness support and set the random trace flag. |

#### Span Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | Span attributes MUST adhere to the common rules of attribute limits. | `src/Трассировка/Классы/ОтелСпан.os:255-271` |  |
| 31 | MUST | ✅ found | If the SDK implements the limits above it MUST provide a way to change these limits, via a configuration to the TracerProvider, by allowing users to configure individual limits. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:83-152` |  |
| 32 | SHOULD | ✅ found | The name of the configuration options SHOULD be EventCountLimit and LinkCountLimit. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:34-43` |  |
| 33 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called SpanLimits. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:1` |  |
| 34 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute, event, or link was discarded due to such a limit. | `src/Трассировка/Классы/ОтелСпан.os` | ВывестиПредупреждениеОбОтброшенныхДанных() выводит предупреждение через логгер. |
| 35 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per discarded attribute, event, or link). | `src/Трассировка/Классы/ОтелСпан.os` | Флаг ПредупреждениеОтброшенныхВыведено гарантирует однократный вывод. |

#### Id Generators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#id-generators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | The SDK MUST by default randomly generate both the TraceId and the SpanId. | `src/Ядро/Модули/ОтелУтилиты.os:78-114` |  |
| 37 | MUST | ✅ found | The SDK MUST provide a mechanism for customizing the way IDs are generated for both the TraceId and the SpanId. | `src/Ядро/Модули/ОтелУтилиты.os:63-65` |  |
| 38 | MUST | ✅ found | Name of the methods MUST be consistent with SpanContext (one to generate a SpanId and one for TraceId). | `src/Ядро/Модули/ОтелУтилиты.os:78-114` |  |
| 39 | MUST NOT | ✅ found | Additional IdGenerator implementing vendor-specific protocols such as AWS X-Ray trace id generator MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | `src/Ядро/Модули/ОтелУтилиты.os:78` |  |

#### Span processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 40 | MUST | ✅ found | SDK MUST allow to end each pipeline with individual exporter. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:63-65` |  |
| 41 | MUST | ✅ found | SDK MUST allow users to implement and configure custom processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:76-78` |  |
| 42 | MUST | ✅ found | The SpanProcessor interface MUST declare the following methods: OnStart, OnEnd, Shutdown, ForceFlush. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os` |  |
| 43 | SHOULD | ❌ not_found | The SpanProcessor interface SHOULD declare the following methods: OnEnding method. | - | No OnEnding method exists in any span processor. The processors only have ПриНачале (OnStart) and ПриЗавершении (OnEnd). There is no intermediate step between span End() being called and OnEnd being invoked. |
| 44 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ОтелСпан.os:592` |  |
| 45 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it (OnStart span parameter is read/write). | `src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:18-26` |  |

#### OnEnd(Span)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onendspan)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | MUST | ✅ found | This method MUST be called synchronously within the Span.End() API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:443-446` |  |

#### Shutdown()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 47 | SHOULD | ⚠️ partial | Shutdown SHOULD be called only once for each SpanProcessor instance. After the call to Shutdown, subsequent calls to OnStart, OnEnd, or ForceFlush are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:42-44` | BatchSpanProcessor (via ОтелБазовыйПакетныйПроцессор) checks Закрыт flag in Обработать() and returns early, which prevents OnEnd from processing. However SimpleSpanProcessor has no such guard - after Закрыть() it can still receive ПриЗавершении() calls (it just won't have an exporter if it was closed). Also no protection against double Shutdown calls. |
| 48 | SHOULD | ❌ not_found | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Закрыть() (Shutdown) in both ОтелПростойПроцессорСпанов and ОтелБазовыйПакетныйПроцессор is a Процедура (void), not a Функция. It returns nothing - no success/failure/timeout indication. |
| 49 | MUST | ✅ found | Shutdown MUST include the effects of ForceFlush. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:73-80` |  |
| 50 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:184-193` | BatchSpanProcessor's ОстановитьФоновыйЭкспорт() uses a timeout when waiting for the background export promise (ТаймаутЭкспортаМс). However the ЭкспортироватьВсеПакеты() call in Закрыть() has no timeout - it loops until the buffer is empty, potentially blocking indefinitely. |
| 51 | SHOULD | ⚠️ partial | Shutdown SHOULD be called only once for each SpanProcessor instance. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:73-74` | Закрыть() sets Закрыт=Истина but does not guard against being called multiple times. If called twice, it will attempt to stop background export and flush again, and close the exporter again. |

#### ForceFlush()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 52 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with Spans for which the SpanProcessor had already received events prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:67-69` |  |
| 53 | SHOULD | ✅ found | In particular, if any SpanProcessor has any associated exporter, it SHOULD try to call the exporter's Export with all spans for which this was not already done and then invoke ForceFlush on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:119-134` |  |
| 54 | MUST | ✅ found | The built-in SpanProcessors MUST do so (call Export and then ForceFlush on exporter). | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:67-69` |  |
| 55 | MUST | ❌ not_found | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. | - | СброситьБуфер() (ForceFlush) does not accept a timeout parameter. It calls ЭкспортироватьВсеПакеты() which loops until the buffer is empty with no timeout mechanism. |
| 56 | SHOULD | ❌ not_found | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | СброситьБуфер() is a Процедура (void) - it returns nothing to indicate success, failure or timeout. |
| 57 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the SpanProcessor exports the completed spans. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:91-95` |  |
| 58 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:67-69` | СброситьБуфер() (ForceFlush) has no timeout parameter and no internal timeout. It calls ЭкспортироватьВсеПакеты() which loops synchronously until buffer is empty, potentially blocking indefinitely if exports are slow. |

#### Built-in span processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#built-in-span-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:1, src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:1` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | MUST | ✅ found | The processor MUST synchronize calls to Span Exporter's Export to make sure that they are not invoked concurrently. (Simple processor) | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os` | Добавлена БлокировкаЭкспорта вокруг вызова Экспортировать() |
| 61 | MUST | ✅ found | The processor MUST synchronize calls to Span Exporter's Export to make sure that they are not invoked concurrently. (Batching processor) | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os` | Добавлена БлокировкаЭкспорта вокруг вызова Экспортировать() |
| 62 | SHOULD | ⚠️ partial | The processor SHOULD export a batch when any of the following happens AND the previous export call has returned: scheduledDelayMillis after the processor is constructed OR the first span is received; the queue contains maxExportBatchSize or more spans; ForceFlush is called. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:41` | Все три условия экспорта реализованы: периодический таймер (ПериодическийЭкспорт, строка 105), порог размера пакета (строка 53, 60), ForceFlush (СброситьБуфер, строка 67). Однако нет явной проверки, что предыдущий вызов Export завершился перед началом нового (AND the previous export call has returned). |
| 63 | MUST | ❌ not_found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | - | В коде ОтелЭкспортерСпанов и транспортов нет документации о требованиях к конкурентности, которые SDK предъявляет к экспортеру. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 64 | MUST | ✅ found | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:22, src/Экспорт/Классы/ОтелЭкспортерСпанов.os:44, src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38` |  |

#### `Export(batch)`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | MUST NOT | ✅ found | Export() MUST NOT block indefinitely. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:71` |  |
| 66 | MUST | ✅ found | There MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:129` |  |
| 67 | SHOULD NOT | ✅ found | The default SDK's Span Processors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the spans are being sent to. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:26, src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:136` |  |

#### `ForceFlush()`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | This is a hint to ensure that the export of any Spans the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38` |  |
| 69 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38` | СброситьБуфер реализован как Процедура (void) без возвращаемого значения. Вызывающий код не может узнать, был ли ForceFlush успешным, неудачным или прерванным по таймауту. |
| 70 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the completed spans. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38` |  |
| 71 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. ForceFlush can be implemented as a blocking API or an asynchronous API which notifies the caller via a callback or an event. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:38` | СброситьБуфер экспортера не имеет механизма таймаута. Для синхронного экспортера это не критично (нет буфера), но у ОтелБазовыйПакетныйПроцессор.СброситьБуфер также нет таймаута - он вызывает ЭкспортироватьВсеПакеты(), который может выполняться неограниченно долго при большом буфере. |

#### Examples

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#examples)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST | ✅ found | Tracer Provider - Tracer creation, ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os` | СинхронизированнаяКарта для кэша, АтомарноеБулево для однократного Shutdown |
| 73 | MUST | ✅ found | Sampler - ShouldSample and GetDescription MUST be safe to be called concurrently. | `src/Трассировка/Модули/ОтелСэмплер.os:112` |  |
| 74 | MUST | ⚠️ partial | Span processor - all methods MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os`, `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os` | Вызовы Export синхронизированы через БлокировкаЭкспорта. Другие методы не имеют полной синхронизации. Документация потокобезопасности добавлена. |
| 75 | MUST | ⚠️ partial | Span Exporter - ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os` | Документация потокобезопасности добавлена. СброситьБуфер - no-op, безопасен. Закрыть() использует обычный флаг Закрыт без атомарной операции. |

### Logs Api

#### Logs API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logs-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD provide a way to set/register and access a global default LoggerProvider. | `src/Ядро/Модули/ОтелГлобальный.os:30` |  |

#### LoggerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The LoggerProvider MUST provide the following functions: Get a Logger. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:46` |  |
| 3 | MUST | ✅ found | This API MUST accept the following instrumentation scope parameters: name, version (optional), schema_url (optional), attributes (optional). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:46` |  |
| 4 | MUST | ✅ found | The attributes parameter: This API MUST be structured to accept a variable number of attributes, including none. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:49` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The Logger MUST provide a function to: Emit a LogRecord. | `src/Логирование/Классы/ОтелЛоггер.os:64` |  |
| 6 | SHOULD | ✅ found | The Logger SHOULD provide functions to: Report if Logger is Enabled. | `src/Логирование/Классы/ОтелЛоггер.os:41` |  |
| 7 | MUST | ✅ found | The Emit API MUST accept the following parameters: Timestamp (optional), Observed Timestamp (optional), Context, Severity Number (optional), Severity Text (optional), Body (optional), Attributes (optional), Event Name (optional). | `src/Логирование/Классы/ОтелЛоггер.os:64` |  |
| 8 | SHOULD | ✅ found | When implicit Context is supported, then the Context parameter SHOULD be optional for Emit. | `src/Логирование/Классы/ОтелЛоггер.os:64` |  |
| 9 | MUST | ✅ found | When implicit Context is supported and Context parameter is unspecified for Emit, then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:70` |  |
| 10 | SHOULD | ✅ found | A Logger SHOULD provide the Enabled API to help users avoid performing computationally expensive operations when generating a LogRecord. | `src/Логирование/Классы/ОтелЛоггер.os:41` |  |
| 11 | SHOULD | ✅ found | The Enabled API SHOULD accept the following parameters: Context, Severity Number (optional), Event Name (optional). | `src/Логирование/Классы/ОтелЛоггер.os:41` |  |
| 12 | SHOULD | ✅ found | When implicit Context is supported, then the Context parameter for Enabled SHOULD be optional. | `src/Логирование/Классы/ОтелЛоггер.os:41` |  |
| 13 | MUST | ✅ found | When implicit Context is supported and Context parameter for Enabled is unspecified, then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:41` |  |
| 14 | MUST | ✅ found | The Enabled API MUST return a language idiomatic boolean type. | `src/Логирование/Классы/ОтелЛоггер.os:41` |  |
| 15 | SHOULD | ❌ not_found | The Enabled API SHOULD be documented that instrumentation authors need to call this API each time they emit a LogRecord to ensure they have the most up-to-date response. | - | The Включен() method documentation does not mention that it should be called each time before emitting. The doc only describes parameters and return value. |
| 16 | SHOULD | ⚠️ partial | When only explicit Context is supported for Emit, this parameter SHOULD be required. | `src/Логирование/Классы/ОтелЛоггер.os:64` | The implementation supports implicit Context (falls back to ОтелКонтекст.Текущий()), so Context is optional. This requirement applies to explicit-only Context SDKs, which this is not, but the spec sentence still contains a SHOULD. The implementation is correct for its design choice (implicit context). |

#### Optional and required parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#optional-and-required-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | For each optional parameter, the API MUST be structured to accept it. | `src/Логирование/Классы/ОтелЗаписьЛога.os:173` |  |
| 18 | MUST NOT | ✅ found | For each optional parameter, the API MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелЗаписьЛога.os:173` |  |
| 19 | MUST | ✅ found | For each required parameter, the API MUST be structured to obligate a user to provide it. | `src/Логирование/Классы/ОтелЛоггер.os:64` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | LoggerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os` | Документация потокобезопасности добавлена |
| 21 | MUST | ✅ found | Logger - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелЛоггер.os:102` |  |

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
| 2 | MUST | ✅ found | A LoggerProvider MUST provide a way to allow a Resource to be specified. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:22` |  |
| 3 | SHOULD | ✅ found | If a Resource is specified, it SHOULD be associated with all the LogRecords produced by any Logger from the LoggerProvider. | `src/Логирование/Классы/ОтелЛоггер.os:66` |  |

#### LoggerProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent LoggerProviders. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:60` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Configuration (i.e. LogRecordProcessors and (Development) LoggerConfigurator) MUST be owned by the LoggerProvider. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:21` |  |
| 6 | MUST | ✅ found | If configuration is updated (e.g., adding a LogRecordProcessor), the updated configuration MUST also apply to all already returned Loggers. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:75` |  |
| 7 | MUST NOT | ✅ found | It MUST NOT matter whether a Logger was obtained from the LoggerProvider before or after the configuration change. | `src/Логирование/Классы/ОтелЛоггер.os:87` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ✅ found | The export of any ReadableLogRecords the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38` |  |
| 9 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38` | СброситьБуфер() объявлен как Процедура (void) без возвращаемого значения - вызывающий код не может узнать об успехе, ошибке или таймауте. На уровне провайдера есть СброситьБуферАсинхронно() с Обещанием, но сам экспортер не предоставляет обратной связи. |
| 10 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the ReadableLogRecords. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38` |  |
| 11 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:67` | ForceFlush экспортера - no-op (завершается мгновенно). Но ForceFlush пакетного процессора (ЭкспортироватьВсеПакеты) зацикливается до исчерпания буфера без собственного таймаута - полагается только на таймаут транспорта для каждого отдельного пакета, но общий таймаут ForceFlush не конфигурируется. |

#### ReadableLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readablelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | A function receiving this as an argument MUST be able to access all the information added to the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:45` |  |
| 13 | MUST | ✅ found | It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) associated with the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:126` |  |
| 14 | MUST | ✅ found | The trace context fields MUST be populated from the resolved Context (either the explicitly passed Context or the current Context) when emitted. | `src/Логирование/Классы/ОтелЛоггер.os:69` |  |
| 15 | MUST | ✅ found | Counts for attributes due to collection limits MUST be available for exporters to report as described in the transformation to non-OTLP formats specification. | `src/Логирование/Классы/ОтелЗаписьЛога.os:144` |  |

#### ReadWriteLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readwritelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | A function receiving this as an argument MUST additionally be able to modify the following information added to the LogRecord: Timestamp, ObservedTimestamp, SeverityText, SeverityNumber, Body, Attributes (addition, modification, removal), TraceId, SpanId, TraceFlags, EventName. | `src/Логирование/Классы/ОтелЗаписьЛога.os` | Все поля модифицируемы, включая SeverityText через отдельный метод УстановитьТекстСерьезности() |

#### LogRecord Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecord-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | LogRecord attributes MUST adhere to the common rules of attribute limits. | `src/Логирование/Классы/ОтелЗаписьЛога.os:213` |  |
| 18 | MUST | ✅ found | If the SDK implements attribute limits it MUST provide a way to change these limits, via a configuration to the LoggerProvider, by allowing users to configure individual limits. | `src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:50` |  |
| 19 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called LogRecordLimits. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:1` |  |
| 20 | SHOULD | ❌ not_found | There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute was discarded due to such a limit. | - | When an attribute is discarded (ОтелЗаписьЛога.os:214), only the counter ОтброшенныхАтрибутов is incremented. No log message is printed to alert the user. |
| 21 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per LogRecord (i.e., not per discarded attribute). | `src/Логирование/Классы/ОтелЗаписьЛога.os` | Флаг ПредупреждениеОтброшенныхВыведено гарантирует однократный вывод. |

#### LogRecordProcessor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 22 | MUST | ✅ found | The SDK MUST allow each pipeline to end with an individual exporter. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:52` |  |
| 23 | MUST | ✅ found | The SDK MUST allow users to implement and configure custom processors and decorate built-in processors for advanced scenarios such as enriching with attributes. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:75` |  |

#### LogRecordProcessor operations#### OnEmit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor-operations-onemit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | SHOULD NOT | ✅ found | OnEmit is called when a LogRecord is emitted. This method is called synchronously on the thread that emitted the LogRecord, therefore it SHOULD NOT block or throw exceptions. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17` |  |
| 25 | MUST | ✅ found | For a LogRecordProcessor registered directly on SDK LoggerProvider, the logRecord mutations MUST be visible in next registered processors. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:18` |  |
| 26 | SHOULD | ❌ not_found | To avoid race conditions, implementations SHOULD recommended to users that a clone of logRecord be used for any concurrent processing, such as in a batching processor. | - | Нет механизма клонирования ОтелЗаписьЛога и нет документации, рекомендующей пользователям клонировать запись для конкурентной обработки. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 27 | MUST NOT | ⚠️ partial | Any modifications to parameters inside Enabled MUST NOT be propagated to the caller. Parameters are immutable or passed by value. | `src/Логирование/Классы/ОтелЛоггер.os:41` | Logger.Включен не модифицирует параметры, но у LogRecordProcessor нет собственного метода Enabled. Logger.Включен не делегирует вызов в процессор - вместо этого проверяет только ЕстьПроцессоры(). Отдельный интерфейс Enabled на уровне LogRecordProcessor отсутствует. |

#### ShutDown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | SHOULD | ❌ not_found | Shutdown SHOULD be called only once for each LogRecordProcessor instance. | - | Нет защиты от повторного вызова Закрыть(). В ОтелПростойПроцессорЛогов нет флага Закрыт, повторный вызов приводит к повторному вызову Экспортер.Закрыть(). В ОтелБазовыйПакетныйПроцессор Закрыт устанавливается в Истина, но Закрыть() не проверяет этот флаг перед выполнением. |
| 29 | SHOULD | ⚠️ partial | After the call to Shutdown, subsequent calls to OnEmit are not allowed. SDKs SHOULD ignore these calls gracefully, if possible. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:42` | ОтелБазовыйПакетныйПроцессор.Обработать проверяет флаг Закрыт и делает Возврат (строка 42-43). Однако ОтелПростойПроцессорЛогов.ПриПоявлении не проверяет закрытие процессора - вызовы после Shutdown делегируются экспортеру (который проверяет Закрыт). |
| 30 | SHOULD | ❌ not_found | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | Закрыть() объявлена как Процедура (void) во всех процессорах. Нет возвращаемого значения для информирования вызывающего кода об успехе, ошибке или таймауте. |
| 31 | MUST | ✅ found | Shutdown MUST include the effects of ForceFlush. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:73` |  |
| 32 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:187` | В пакетном процессоре ОстановитьФоновыйЭкспорт() использует таймаут при ожидании фонового задания (строка 187), но сама процедура ЭкспортироватьВсеПакеты() не ограничена по времени - если экспортер зависнет, Shutdown заблокируется бесконечно. |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | SHOULD | ✅ found | The export of any ReadableLogRecords the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38` |  |
| 34 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38` | СброситьБуфер() объявлен как Процедура (void) без возвращаемого значения - вызывающий код не может узнать об успехе, ошибке или таймауте. На уровне провайдера есть СброситьБуферАсинхронно() с Обещанием, но сам экспортер не предоставляет обратной связи. |
| 35 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the ReadableLogRecords. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38` |  |
| 36 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:67` | ForceFlush экспортера - no-op (завершается мгновенно). Но ForceFlush пакетного процессора (ЭкспортироватьВсеПакеты) зацикливается до исчерпания буфера без собственного таймаута - полагается только на таймаут транспорта для каждого отдельного пакета, но общий таймаут ForceFlush не конфигурируется. |

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
| 39 | MUST | ✅ found | The Simple processor MUST synchronize calls to LogRecordExporter's Export to make sure that they are not invoked concurrently. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os` | Добавлена БлокировкаЭкспорта вокруг вызова Экспортировать() |
| 40 | MUST | ✅ found | The Batching processor MUST synchronize calls to LogRecordExporter's Export to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os` | Добавлена БлокировкаЭкспорта вокруг вызова Экспортировать() |
| 41 | MUST | ❌ not_found | Each LogRecordExporter implementation MUST document the concurrency characteristics the SDK requires of the exporter. | - | ОтелЭкспортерЛогов не содержит документации о требованиях конкурентности SDK к экспортеру. |

#### LogRecordExporter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 42 | MUST | ✅ found | A LogRecordExporter MUST support the following functions: Export, ForceFlush, Shutdown | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:22,38,44` |  |

#### Export

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#export)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 43 | MUST NOT | ✅ found | Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:71` |  |
| 44 | MUST | ✅ found | There MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелHttpТранспорт.os:129` |  |
| 45 | SHOULD NOT | ✅ found | The default SDK's LogRecordProcessors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the logs are being sent to. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:15` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | SHOULD | ✅ found | The export of any ReadableLogRecords the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38` |  |
| 47 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38` | СброситьБуфер() объявлен как Процедура (void) без возвращаемого значения - вызывающий код не может узнать об успехе, ошибке или таймауте. На уровне провайдера есть СброситьБуферАсинхронно() с Обещанием, но сам экспортер не предоставляет обратной связи. |
| 48 | SHOULD | ✅ found | ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports the ReadableLogRecords. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:38` |  |
| 49 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:67` | ForceFlush экспортера - no-op (завершается мгновенно). Но ForceFlush пакетного процессора (ЭкспортироватьВсеПакеты) зацикливается до исчерпания буфера без собственного таймаута - полагается только на таймаут транспорта для каждого отдельного пакета, но общий таймаут ForceFlush не конфигурируется. |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 50 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each LogRecordExporter instance. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:44` |  |
| 51 | SHOULD | ✅ found | After the call to Shutdown subsequent calls to Export are not allowed and SHOULD return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:23` |  |
| 52 | SHOULD NOT | ✅ found | Shutdown SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:44` |  |
| 53 | MUST | ✅ found | LoggerProvider - Logger creation, ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os` | СинхронизированнаяКарта для кэша, АтомарноеБулево для однократного Shutdown |
| 54 | MUST | ✅ found | Logger - all methods MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелЛоггер.os:64` |  |
| 55 | MUST | ⚠️ partial | LogRecordExporter - ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os` | Документация потокобезопасности добавлена. СброситьБуфер() - no-op, безопасен. Закрыть() использует обычный флаг Закрыт без атомарной операции. |

### Metrics Api

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD provide a way to set/register and access a global default MeterProvider. | `src/Ядро/Модули/ОтелГлобальный.os:30` |  |

#### MeterProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The MeterProvider MUST provide the following functions: Get a Meter | `src/Метрики/Классы/ОтелПровайдерМетрик.os:50` |  |
| 3 | MUST | ✅ found | This API MUST accept the following parameters: name, version, schema_url, attributes | `src/Метрики/Классы/ОтелПровайдерМетрик.os:50` |  |
| 4 | MUST NOT | ✅ found | Users can provide a version, but it is up to their discretion. Therefore, this API needs to be structured to accept a version, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:52` |  |
| 5 | MUST NOT | ✅ found | Users can provide a schema_url, but it is up to their discretion. Therefore, this API needs to be structured to accept a schema_url, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:54` |  |
| 6 | MUST | ✅ found | This API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:53` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ found | Meter SHOULD NOT be responsible for the configuration. This should be the responsibility of the MeterProvider instead. | `src/Метрики/Классы/ОтелМетр.os:1` |  |

#### Meter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The Meter MUST provide functions to create new Instruments: Counter, Asynchronous Counter, Histogram, Gauge, Asynchronous Gauge, UpDownCounter, Asynchronous UpDownCounter | `src/Метрики/Классы/ОтелМетр.os:43` |  |

#### Instrument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ⚠️ partial | Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying. | `src/Метрики/Классы/ОтелМетр.os:436` | OneScript не различает int/float на уровне типа Число. Дескриптор инструмента регистрируется с Вид, ЕдиницаИзмерения и Описание, но не с числовым типом. Агрегатор использует строковые маркеры 'int'/'double', но они не являются частью идентификации инструмента при проверке конфликтов. |

#### Synchronous and Asynchronous instruments

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#synchronous-and-asynchronous-instruments)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API to construct synchronous instruments MUST accept the following parameters: A name of the Instrument. | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 11 | SHOULD | ✅ found | The name needs to be provided by a user. If possible, the API SHOULD be structured so a user is obligated to provide this parameter (sync). | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 12 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed (sync name). | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 13 | SHOULD | ❌ not_found | The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (sync). | - | Документация методов СоздатьСчетчик и аналогов не упоминает синтаксис имен инструментов (правила ABNF). |
| 14 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the name; that is left to implementations of the API, like the SDK (sync). | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 15 | MUST NOT | ✅ found | Users can provide a unit, but it is up to their discretion. Therefore, this API needs to be structured to accept a unit, but MUST NOT obligate a user to provide one (sync). | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 16 | MUST | ✅ found | The unit parameter needs to support the instrument unit rule. Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters (sync). | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 17 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the unit (sync). | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 18 | MUST NOT | ✅ found | Users can provide a description, but it is up to their discretion. Therefore, this API needs to be structured to accept a description, but MUST NOT obligate a user to provide one (sync). | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 19 | MUST | ✅ found | The description needs to support the instrument description rule. Meaning, the API MUST accept a string that supports at least BMP encoded characters and hold at least 1023 characters (sync). | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 20 | MUST NOT | ✅ found | Users can provide advisory parameters, but its up to their discretion. Therefore, this API needs to be structured to accept advisory parameters, but MUST NOT obligate the user to provide it (sync). | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 21 | SHOULD NOT | ❌ not_found | The API SHOULD NOT validate advisory parameters (sync). | - | Advisory-параметры не реализованы в API синхронных инструментов, поэтому невозможно оценить валидацию. |
| 22 | MUST | ✅ found | The API to construct asynchronous instruments MUST accept the following parameters: A name of the Instrument. | `src/Метрики/Классы/ОтелМетр.os:198` |  |
| 23 | SHOULD | ✅ found | The name needs to be provided by a user. If possible, the API SHOULD be structured so a user is obligated to provide this parameter (async). | `src/Метрики/Классы/ОтелМетр.os:198` |  |
| 24 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed (async name). | `src/Метрики/Классы/ОтелМетр.os:198` |  |
| 25 | SHOULD | ❌ not_found | The API SHOULD be documented in a way to communicate to users that the name parameter needs to conform to the instrument name syntax (async). | - | Документация методов СоздатьНаблюдаемыйСчетчик и аналогов не упоминает синтаксис имен инструментов. |
| 26 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the name, that is left to implementations of the API (async). | `src/Метрики/Классы/ОтелМетр.os:198` |  |
| 27 | MUST NOT | ✅ found | Users can provide a unit, but it is up to their discretion. Therefore, this API needs to be structured to accept a unit, but MUST NOT obligate a user to provide one (async). | `src/Метрики/Классы/ОтелМетр.os:198` |  |
| 28 | MUST | ✅ found | The unit parameter needs to support the instrument unit rule. Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters (async). | `src/Метрики/Классы/ОтелМетр.os:198` |  |
| 29 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the unit (async). | `src/Метрики/Классы/ОтелМетр.os:198` |  |
| 30 | MUST NOT | ✅ found | Users can provide a description, but it is up to their discretion. Therefore, this API needs to be structured to accept a description, but MUST NOT obligate a user to provide one (async). | `src/Метрики/Классы/ОтелМетр.os:198` |  |
| 31 | MUST | ✅ found | The description needs to support the instrument description rule. Meaning, the API MUST accept a string that supports at least BMP encoded characters and hold at least 1023 characters (async). | `src/Метрики/Классы/ОтелМетр.os:198` |  |
| 32 | MUST NOT | ✅ found | Users can provide advisory parameters, but its up to their discretion. Therefore, this API needs to be structured to accept advisory parameters, but MUST NOT obligate the user to provide it (async). | `src/Метрики/Классы/ОтелМетр.os:198` |  |
| 33 | SHOULD NOT | ❌ not_found | The API SHOULD NOT validate advisory parameters (async). | - | Advisory-параметры не реализованы в API асинхронных инструментов. |
| 34 | MUST | ✅ found | This API MUST be structured to accept a variable number of callback functions, including none. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os` |  |
| 35 | MUST | ✅ found | The API MUST support creation of asynchronous instruments by passing zero or more callback functions to be permanently registered to the newly created instrument. | `src/Метрики/Классы/ОтелМетр.os` |  |
| 36 | SHOULD | ⚠️ partial | The API SHOULD support registration of callback functions associated with asynchronous instruments after they are created. | `src/Метрики/Классы/ОтелМетр.os:348` | Мульти-callback регистрация через ЗарегистрироватьОбратныйВызов поддерживается на уровне Метра, но нет метода регистрации дополнительного callback на отдельном наблюдаемом инструменте после его создания. |
| 37 | MUST | ✅ found | Where the API supports registration of callback functions after asynchronous instrumentation creation, the user MUST be able to undo registration of the specific callback after its registration by some means. | `src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os` |  |
| 38 | MUST | ✅ found | Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set. | `src/Метрики/Классы/ОтелМетр.os:355` |  |
| 39 | MUST | ✅ found | Callback functions MUST be documented as follows for the end user. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:97` |  |
| 40 | SHOULD | ❌ not_found | Callback functions SHOULD be reentrant safe. The SDK expects to evaluate callbacks for each MetricReader independently. | - | Нет документации для пользователей о том, что callback-функции должны быть реентерабельными. |
| 41 | SHOULD NOT | ❌ not_found | Callback functions SHOULD NOT take an indefinite amount of time. | - | Нет документации для пользователей о том, что callback-функции не должны занимать неопределённо долгое время. |
| 42 | SHOULD NOT | ❌ not_found | Callback functions SHOULD NOT make duplicate observations (more than one Measurement with the same attributes) across all registered callbacks. | - | Нет документации для пользователей о недопустимости дублирующих наблюдений. |
| 43 | MUST | ✅ found | Callbacks registered at the time of instrument creation MUST apply to the single instruments which is under construction. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:108` |  |
| 44 | MUST | ✅ found | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the instrument associated with each observed Measurement value. | `src/Метрики/Классы/ОтелМетр.os:358` |  |
| 45 | MUST | ✅ found | Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of asynchronous instruments from the same Meter instance. | `src/Метрики/Классы/ОтелМетр.os:348` |  |
| 46 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:138` |  |
| 47 | MUST | ✅ found | When recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:138` |  |
| 48 | SHOULD | ⚠️ partial | The API SHOULD provide some way to pass state to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:108` | Callback передаётся как Действие (lambda). OneScript Действие может захватывать контекст через замыкание, но нет явного механизма передачи состояния (дополнительного параметра state) в callback. Передача состояния возможна только через замыкание lambda. |

#### General operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | SHOULD | ✅ found | All synchronous instruments SHOULD provide functions to: Report if instrument is Enabled | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179` |  |
| 50 | SHOULD | ✅ found | synchronous instruments SHOULD provide this Enabled API | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179` |  |
| 51 | MUST | ✅ found | the API MUST be structured in a way for parameters to be added | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179` |  |
| 52 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. A returned value of true means the instrument is enabled for the provided arguments, and a returned value of false means the instrument is disabled for the provided arguments. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179-181` |  |
| 53 | SHOULD | ❌ not_found | The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response. | - | Метод Включен() существует, но в документации (комментариях) к нему нет указания на то, что авторы инструментирования должны вызывать его каждый раз перед записью измерения. |

#### Counter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 54 | MUST NOT | ✅ found | There MUST NOT be any API for creating a Counter other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 55 | SHOULD NOT | ✅ found | Counter Add API SHOULD NOT return a value | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 56 | MUST | ✅ found | Counter Add API MUST accept the following parameter: A numeric increment value. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 57 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter (the increment value). | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 58 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелСчетчик.os:17` |  |
| 59 | SHOULD | ⚠️ partial | The increment value is expected to be non-negative. This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелСчетчик.os:14` | Документация (комментарий на строке 14) говорит 'Отрицательные значения игнорируются' и параметр описан как 'положительное значение'. Однако формулировка не строго совпадает со spec-требованием 'communicate that value is expected to be non-negative'. По факту поведение корректное. |
| 60 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value (the increment value), that is left to implementations of the API. | `src/Метрики/Классы/ОтелСчетчик.os:22-24` |  |
| 61 | MUST | ✅ found | this API MUST be structured to accept a variable number of attributes, including none (for Counter Add). | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 62 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation (for Counter Add). | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |
| 63 | MUST NOT | ✅ found | There MUST NOT be any API for creating an Asynchronous Counter other than with a Meter. | `src/Метрики/Классы/ОтелМетр.os:198` |  |
| 64 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:138` |  |
| 65 | MUST | ✅ found | observations from a single callback MUST be reported with identical timestamps. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:138-143` |  |
| 66 | SHOULD | ⚠️ partial | The API SHOULD provide some way to pass state to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:108` | Callback передаётся как Действие (lambda) и может захватывать состояние через замыкание, но нет явного дополнительного параметра state в сигнатуре callback. |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: A callback function; A list (or tuple, etc.) of Instruments used in the callback function. | `src/Метрики/Классы/ОтелМетр.os:348` |  |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: A callback function; A list (or tuple, etc.) of Instruments used in the callback function. | `src/Метрики/Классы/ОтелМетр.os:348` |  |

#### Note: in the real world these would be retrieved from the operating system

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-in-the-real-world-these-would-be-retrieved-from-the-operating-system)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: A callback function; A list (or tuple, etc.) of Instruments used in the callback function. | `src/Метрики/Классы/ОтелМетр.os:348` |  |

#### Note the two associated instruments are passed to the callback.

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#note-the-two-associated-instruments-are-passed-to-the-callback)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 70 | SHOULD | ✅ found | All the metrics components SHOULD allow new APIs to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:1` |  |
| 71 | SHOULD | ✅ found | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелСчетчик.os:21` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST | ✅ found | MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:221` |  |
| 73 | MUST | ✅ found | Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелМетр.os:405` |  |
| 74 | MUST | ✅ found | Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:16` |  |

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
| 2 | MUST | ✅ found | A MeterProvider MUST provide a way to allow a Resource to be specified. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:206` |  |
| 3 | SHOULD | ✅ found | If a Resource is specified, it SHOULD be associated with all the metrics produced by any Meter from the MeterProvider. | `src/Метрики/Классы/ОтелМетр.os:420` |  |

#### MeterProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent MeterProviders. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:206` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | SHOULD | ✅ found | A view with criteria matching the instrument an aggregation is created for has an aggregation_cardinality_limit value defined for the stream, that value SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os` | Поле ЛимитМощностиАгрегации добавлено в ОтелПредставление. |
| 6 | SHOULD | ❌ not_found | If there is no matching view, but the MetricReader defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | - | ОтелПериодическийЧитательМетрик не имеет настройки default cardinality limit. Лимит задаётся только на уровне Meter (2000) и инструмента. |
| 7 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:205` |  |
| 8 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:276` |  |
| 9 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:89` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | ForceFlush MUST invoke ForceFlush on all registered MetricReader instances that implement ForceFlush. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:112` |  |
| 11 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:112` | СброситьБуфер() - процедура без возвращаемого значения. Не возвращает статус успеха/ошибки/таймаута. СброситьБуферАсинхронно() возвращает Обещание, но синхронный вариант не информирует о результате. |
| 12 | SHOULD | ⚠️ partial | ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:112` | СброситьБуфер() не возвращает никакого статуса (ERROR/NO ERROR). Это процедура (void), а не функция. |
| 13 | SHOULD | ⚠️ partial | ForceFlush SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:112` | СброситьБуфер() не принимает параметр таймаута и не имеет механизма прерывания по тайм-ауту. |

#### View

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The SDK MUST provide functionality for a user to create Views for a MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:173` |  |
| 15 | MUST | ✅ found | This functionality MUST accept as inputs the Instrument selection criteria. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:1` |  |
| 16 | MUST | ✅ found | This functionality MUST accept as inputs the resulting stream configuration. | `src/Метрики/Классы/ОтелПредставление.os:1` |  |

#### Instrument selection criteria

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-selection-criteria)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | SHOULD | ✅ found | Criteria SHOULD be treated as additive. This means an Instrument has to match all the provided criteria for the View to be applied. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:24-43` |  |
| 18 | MUST | ✅ found | The SDK MUST accept the following criteria: name, type, unit, meter_name, meter_version, meter_schema_url | `src/Метрики/Классы/ОтелСелекторИнструментов.os` | Все 6 критериев реализованы. |
| 19 | MUST | ✅ found | If the SDK does not support wildcards in general, it MUST still recognize the special single asterisk (*) character as matching all Instruments. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:25` |  |
| 20 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:90` |  |
| 21 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a type, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:90` |  |
| 22 | MUST NOT | ❌ not_found | The instrument selection criteria parameter needs to be structured to accept a unit, but MUST NOT obligate a user to provide one. | - | Unit criterion is not implemented in ОтелСелекторИнструментов at all |
| 23 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a meter_name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:90` |  |
| 24 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a meter_version, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os` | Необязательный параметр конструктора. |
| 25 | MUST NOT | ✅ found | The instrument selection criteria parameter needs to be structured to accept a meter_schema_url, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os` | Необязательный параметр конструктора. |
| 26 | MUST NOT | ✅ found | The instrument selection criteria can be structured to accept additional criteria the SDK accepts, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:90` |  |

#### Stream configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#stream-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 27 | MUST | ✅ found | The SDK MUST accept the following stream configuration parameters: name, description, attribute_keys, aggregation, exemplar_reservoir, aggregation_cardinality_limit | `src/Метрики/Классы/ОтелПредставление.os` | Все параметры реализованы. |
| 28 | SHOULD | ✅ found | name: The metric stream name that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:23-25` |  |
| 29 | SHOULD | ✅ found | In order to avoid conflicts, if a name is provided the View SHOULD have an instrument selector that selects at most one instrument. | `src/Метрики/Классы/ОтелПредставление.os:23-25` |  |
| 30 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept a name, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:89` |  |
| 31 | MUST | ✅ found | If the user does not provide a name value, name from the Instrument the View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:185-187` |  |
| 32 | SHOULD | ✅ found | description: The metric stream description that SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os:32-34` |  |
| 33 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept a description, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:90` |  |
| 34 | MUST | ✅ found | If the user does not provide a description value, the description from the Instrument a View matches MUST be used by default. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:188-190` |  |
| 35 | MUST | ✅ found | attribute_keys: This is, at a minimum, an allow-list of attribute keys for measurements captured in the metric stream. The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:242-251` |  |
| 36 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored (second MUST - ignored). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:242-251` |  |
| 37 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept attribute_keys, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелПредставление.os:91` |  |
| 38 | SHOULD | ❌ not_found | If the user does not provide any value, the SDK SHOULD use the Attributes advisory parameter configured on the instrument instead. | - | No advisory parameter support implemented; when no attribute_keys are set, all attributes are kept without checking instrument advisory |
| 39 | MUST | ✅ found | If the Attributes advisory parameter is absent, all attributes MUST be kept. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:81-83` |  |
| 40 | SHOULD | ✅ found | Additionally, implementations SHOULD support configuring an exclude-list of attribute keys. | `src/Метрики/Классы/ОтелПредставление.os` | Поле ИсключенныеКлючиАтрибутов добавлено. |
| 41 | MUST | ✅ found | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелПредставление.os` | ИсключенныеКлючиАтрибутов реализовано. |
| 42 | MUST | ✅ found | All other attributes MUST be kept (in exclude-list mode). | `src/Метрики/Классы/ОтелПредставление.os` | Исключаются только указанные ключи. |
| 43 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept an aggregation, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:93` |  |
| 44 | MUST | ✅ found | If the user does not provide an aggregation value, the MeterProvider MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance. | `src/Метрики/Классы/ОтелМетр.os:51-59` |  |
| 45 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept an exemplar_reservoir, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os` | Необязательный параметр конструктора. |
| 46 | MUST | ✅ found | If the user does not provide an exemplar_reservoir value, the MeterProvider MUST apply a default exemplar reservoir. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:217` | Резервуар по умолчанию создаётся, теперь также конфигурируем per-view. |
| 47 | MUST NOT | ✅ found | The stream configuration parameter needs to be structured to accept an aggregation_cardinality_limit, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os` | Необязательный параметр конструктора. |
| 48 | MUST | ⚠️ partial | If the user does not provide an aggregation_cardinality_limit value, the MeterProvider MUST apply the default aggregation cardinality limit the MetricReader is configured with. | `src/Метрики/Классы/ОтелМетр.os:412` | Default cardinality limit (2000) is set in ОтелМетр constructor but it's not configurable per-View and not sourced from MetricReader |

#### Measurement processing

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#measurement-processing)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | SHOULD | ✅ found | The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument: Determine the MeterProvider which owns the Instrument. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:151-174` |  |
| 50 | MUST | ⚠️ partial | If the MeterProvider has no View registered, take the Instrument and apply the default Aggregation on the basis of instrument kind according to the MetricReader instance's aggregation property. Instrument advisory parameters, if any, MUST be honored. | `src/Метрики/Классы/ОтелМетр.os:51-59` | Default aggregation is applied when no View matches, but instrument advisory parameters are not implemented |
| 51 | SHOULD | ✅ found | If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning. | `src/Метрики/Классы/ОтелМетр.os:441-454` |  |
| 52 | SHOULD | ⚠️ partial | If it is not possible to apply the View without producing semantic errors the implementation SHOULD emit a warning and proceed as if the View did not exist. | `src/Метрики/Классы/ОтелМетр.os:441-454` | Warning is emitted for conflict, but no check for semantic errors like assigning histogram aggregation to async instrument |
| 53 | MUST | ✅ found | If both a View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:425-434` |  |
| 54 | SHOULD | ✅ found | If the Instrument could not match with any of the registered View(s), the SDK SHOULD enable the instrument using the default aggregation and temporality. | `src/Метрики/Классы/ОтелМетр.os:457-465` |  |

#### conflicting metric identities)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#conflicting-metric-identities)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | MUST | ✅ found | The SDK MUST provide the following Aggregation to support the Metric Points in the Metrics Data Model: Drop, Default, Sum, Last Value, Explicit Bucket Histogram. | `src/Метрики/Модули/ОтелАгрегация.os:1-65` |  |
| 56 | SHOULD | ✅ found | The SDK SHOULD provide the following Aggregation: Base2 Exponential Bucket Histogram. | `src/Метрики/Модули/ОтелАгрегация.os:76-81` |  |

#### Sum Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#sum-aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 57 | SHOULD NOT | ❌ not_found | Histogram Aggregations: Arithmetic sum of Measurement values in population. This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. UpDownCounter or ObservableGauge). | - | The histogram aggregator always collects sum regardless of instrument type - no conditional logic to skip sum for negative-value instruments |
| 58 | SHOULD | ✅ found | SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different. | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:118-135` |  |
| 59 | MUST | ✅ found | The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic scale parameter will not exceed. The maximum scale is defined by the MaxScale configuration parameter. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:290-301` |  |
| 60 | SHOULD | ✅ found | When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:41` |  |
| 61 | SHOULD | ✅ found | Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possible, within the constraint of maximum size. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:157-185` |  |
| 62 | SHOULD NOT | ❌ not_found | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the sum, min, and max fields, because these values do not map into a valid bucket. | - | No explicit handling of Inf/NaN values in the exponential histogram aggregator |

#### Observations inside asynchronous callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#observations-inside-asynchronous-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 63 | MUST | ⚠️ partial | Callback functions MUST be invoked for the specific MetricReader performing collection, such that observations made or produced by executing callbacks only apply to the intended MetricReader during collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:126-133` | Callbacks are invoked during collection (ВызватьМультиОбратныеВызовы + individual instrument callbacks via Собрать), but observations are not scoped per-MetricReader - all readers share the same instrument data |
| 64 | SHOULD | ❌ not_found | The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks. | - | No mechanism to detect or disregard observations made outside callback context |
| 65 | SHOULD | ❌ not_found | The implementation SHOULD use a timeout to prevent indefinite callback execution. | - | No timeout mechanism for callbacks; they execute without time limits |
| 66 | MUST | ✅ found | The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:126-133` |  |
| 67 | SHOULD NOT | ❌ not_found | The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback. | - | Asynchronous instruments (ОтелБазовыйНаблюдаемыйИнструмент) clear external observations after each collect, but individual callback observations are freshly generated each time, so stale attribute sets from prior callbacks may persist within external observations if not properly cleared |

#### Cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | SDKs SHOULD support being configured with a cardinality limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:152-154` |  |
| 69 | SHOULD | ✅ found | Cardinality limit enforcement SHOULD occur after attribute filtering, if any. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:76-104` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 70 | SHOULD | ✅ found | A view with criteria matching the instrument an aggregation is created for has an aggregation_cardinality_limit value defined for the stream, that value SHOULD be used. | `src/Метрики/Классы/ОтелПредставление.os` | Поле ЛимитМощностиАгрегации добавлено. |
| 71 | SHOULD | ❌ not_found | If there is no matching view, but the MetricReader defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | - | ОтелПериодическийЧитательМетрик не имеет настройки default cardinality limit. Лимит задаётся только на уровне Meter (2000) и инструмента. |
| 72 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:205` |  |
| 73 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:276` |  |
| 74 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:89` |  |

#### Synchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#synchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | MUST | ⚠️ partial | Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:89` | Реализация перенаправляет новые наборы атрибутов в overflow при достижении лимита, но при вызове ОчиститьТочкиДанных() (строка 131-136) полностью сбрасываются все аккумуляторы, включая ранее наблюдённые. Cumulative temporality не поддерживается явно - SDK реализует reset-based (delta-like) поведение. |
| 76 | MUST | ✅ found | Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in exactly one Aggregator, which is either an Aggregator associated with the correct attribute set or an aggregator associated with the overflow attribute set. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:87` |  |
| 77 | MUST NOT | ✅ found | Measurements MUST NOT be double-counted or dropped during an overflow. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:87` |  |

#### Asynchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#asynchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | SHOULD | ❌ not_found | Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality. | - | ОтелБазовыйНаблюдаемыйИнструмент не реализует ни лимита кардинальности, ни overflow-логики. В отличие от синхронных инструментов, наблюдаемые инструменты не имеют ЛимитМощности, КлючПереполнения или ПеренаправитьВПереполнение(). Все записи из callback принимаются без ограничений. |

#### Duplicate instrument registration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#duplicate-instrument-registration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 79 | MUST | ✅ found | The Meter MUST return a functional instrument that can be expected to export data even if this will cause semantic error in the data model. | `src/Метрики/Классы/ОтелМетр.os:48` |  |
| 80 | SHOULD | ✅ found | When a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted. | `src/Метрики/Классы/ОтелМетр.os:449` |  |
| 81 | SHOULD | ⚠️ partial | The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible. | `src/Метрики/Классы/ОтелМетр.os:449` | Предупреждение содержит информацию о конфликтующих параметрах (вид, единица измерения), но не включает рекомендацию по разрешению конфликта (например, использовать View для переименования). |
| 82 | SHOULD | ❌ not_found | If the potential conflict involves multiple description properties, setting the description through a configured View SHOULD avoid the warning. | - | Проверка конфликта (ПроверитьКонфликтДескриптора) не учитывает наличие View, который мог бы задать описание. Предупреждение выдаётся всегда при различии description, независимо от настроенных View. |
| 83 | SHOULD | ❌ not_found | If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning. | - | Предупреждение (строка 449) не содержит рецепта по использованию View для переименования или разрешения конфликта. |
| 84 | SHOULD | ⚠️ partial | Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both Metric objects and emit a generic warning describing the duplicate instrument registration. | `src/Метрики/Классы/ОтелМетр.os:48` | При дубликате возвращается первый зарегистрированный инструмент (строка 48), а не оба объекта Metric. Предупреждение выдаётся (строка 449), но данные второго инструмента не экспортируются отдельно. |
| 85 | MUST | ✅ found | The SDK MUST aggregate data from identical Instruments together in its export pipeline. | `src/Метрики/Классы/ОтелМетр.os:45` |  |

#### Name conflict

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#name-conflict)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 86 | MUST | ✅ found | When this happens, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above. | `src/Метрики/Классы/ОтелМетр.os:44` |  |

#### Instrument name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 87 | SHOULD | ❌ not_found | When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax. | - | Методы создания инструментов (СоздатьСчетчик и др.) не выполняют валидацию имени инструмента. Имя нормализуется через НРег() (lower case), но не проверяется на соответствие синтаксису (regex паттерн спецификации). |
| 88 | SHOULD | ❌ not_found | If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name. | - | Нет проверки синтаксиса имени инструмента и соответствующего предупреждения/ошибки при невалидном имени. |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 90 | MUST | ✅ found | If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit string. | `src/Метрики/Классы/ОтелМетр.os:43` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 91 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument description. | `src/Метрики/Классы/ОтелМетр.os:43` |  |
| 92 | MUST | ✅ found | If a description is not provided or the description is null, the Meter MUST treat it the same as an empty description string. | `src/Метрики/Классы/ОтелМетр.os:43` |  |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 93 | SHOULD | ❌ not_found | When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters. | - | Advisory parameters are not implemented in the SDK. The instrument creation methods (СоздатьСчетчик, СоздатьГистограмму, etc.) do not accept advisory parameters and there is no validation logic for them. |
| 94 | SHOULD | ❌ not_found | If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided. | - | Advisory parameters are not implemented, so there is no validation or error emission for invalid advisory parameters. |
| 95 | MUST | ❌ not_found | If multiple identical Instruments are created with different advisory parameters, the Meter MUST return an instrument using the first-seen advisory parameters and log an appropriate error as described in duplicate instrument registrations. | - | Advisory parameters are not implemented. Duplicate instrument registration checks exist (ПроверитьКонфликтДескриптора in ОтелМетр.os:441), but only for name/kind/unit/description - not for advisory parameters. |
| 96 | MUST | ❌ not_found | If both a View and advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | - | Advisory parameters are not implemented. Views are implemented (ОтелПредставление.os), but since there are no advisory parameters, there is no precedence logic between Views and advisory params. |

#### Instrument advisory parameter: `ExplicitBucketBoundaries`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameter-explicitbucketboundaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | MUST | ❌ not_found | If no View matches, or if a matching View selects the default aggregation, the ExplicitBucketBoundaries advisory parameter MUST be used. If neither is provided, the default bucket boundaries apply. | - | The ExplicitBucketBoundaries advisory parameter is not implemented. Instrument creation methods (e.g., СоздатьГистограмму in ОтелМетр.os:72) do not accept an advisory boundaries parameter. The histogram aggregator uses standard boundaries by default (ОтелАгрегаторГистограммы.os:118-135) or View-provided boundaries, but there is no advisory parameter path. |

#### Exemplar

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | MUST | ✅ found | A Metric SDK MUST provide a mechanism to sample Exemplars from measurements via the ExemplarFilter and ExemplarReservoir hooks. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:284` |  |
| 99 | SHOULD | ✅ found | Exemplar sampling SHOULD be turned on by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:216` |  |
| 100 | MUST NOT | ✅ found | If Exemplar sampling is off, the SDK MUST NOT have overhead related to exemplar sampling. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:285` |  |
| 101 | MUST | ✅ found | A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation. For example, Exemplar sampling of histograms should be able to leverage bucket boundaries. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os` | Гистограммы используют ОтелВыровненныйРезервуарГистограммы с привязкой к бакетам. |
| 102 | SHOULD | ✅ found | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: ExemplarFilter: filter which measurements can become exemplars; ExemplarReservoir: storage and sampling of exemplars. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os` | ExemplarFilter через построитель и env var, ExemplarReservoir через View. |
| 103 | MUST | ✅ found | The ExemplarFilter configuration MUST allow users to select between one of the built-in ExemplarFilters. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 104 | SHOULD | ✅ found | The ExemplarFilter SHOULD be a configuration parameter of a MeterProvider for an SDK. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:70` |  |
| 105 | SHOULD | ✅ found | The default value SHOULD be TraceBased. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:225` |  |
| 106 | SHOULD | ✅ found | The filter configuration SHOULD follow the environment variable specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os` | OTEL_METRICS_EXEMPLAR_FILTER читается в конструкторе построителя. |
| 107 | MUST | ✅ found | An OpenTelemetry SDK MUST support the following filters: AlwaysOn, AlwaysOff, TraceBased. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14` |  |
| 107 | SHOULD | ✅ found | The 'offer' method SHOULD accept measurements, including: the value of the measurement, the complete set of Attributes, the Context (Baggage and active Span), and a timestamp. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os` | Предложить() принимает Значение, Атрибуты, КонтекстСпана. Временная метка внутри. |
#### ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 108 | MUST | ✅ found | The ExemplarReservoir interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os` | Предложить() принимает сырые данные (Значение, Атрибуты, Контекст), Собрать() возвращает экземпляры. |
| 109 | MUST | ⚠️ partial | A new ExemplarReservoir MUST be created for every known timeseries data point, as determined by aggregation and view configuration. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os` | Один резервуар на инструмент, но внутри СинхронизированнаяКарта разделяет данные по ключу серии. Не отдельный экземпляр на серию. |
| 110 | SHOULD | ✅ found | The 'offer' method SHOULD accept measurements, including: the value of the measurement, the complete set of Attributes, the Context (Baggage and active Span), and a timestamp. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os` | Предложить() принимает Значение, Атрибуты, КонтекстСпана. Временная метка внутри. |
| 111 | SHOULD | ✅ found | The 'offer' method SHOULD have the ability to pull associated trace and span information without needing to record full context. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os` | КонтекстСпана передается в Предложить(), оттуда извлекаются traceId/spanId. |
| 112 | MUST | ✅ found | The 'offer' method MAY accept a filtered subset of Attributes which diverge from the timeseries the reservoir is associated with. This MUST be clearly documented in the API and the reservoir MUST be given the Attributes associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes from a measurement in the 'offer' method. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os` | Предложить() получает АтрибутыИзмерения и АтрибутыСерии, вычисляет filteredAttributes. |
| 113 | MUST | ✅ found | The 'collect' method MUST return accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:71` |  |
| 114 | SHOULD | ⚠️ partial | Exemplars are expected to abide by the AggregationTemporality of any metric point they are recorded with. Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:134` | ОчиститьТочкиДанных (line 131-136) clears the reservoir after collection, which partially supports delta temporality. However, there is no explicit check or guarantee that exemplars fall within the start/stop timestamps of the metric point. The reservoir simply accumulates and is cleared on export. |
| 115 | MUST | ✅ found | Exemplars MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os` | filteredAttributes вычисляется как разница АтрибутыИзмерения - АтрибутыСерии. |
| 116 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the Attributes associated with its timeseries point either at construction so that additional sampling performed by the reservoir has access to all attributes. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os` | Предложить() получает полные АтрибутыИзмерения и АтрибутыСерии. |
| 117 | SHOULD | ❌ not_found | The ExemplarReservoir SHOULD avoid allocations when sampling exemplars. | - | The reservoir creates new Массив instances and uses СинхронизированнаяКарта with dynamic insertions. Each exemplar creates a new Соответствие (Map) in ЗахватитьЭкземпляр. There is no evidence of allocation avoidance strategies like pre-allocated slots or object pooling. |

#### Exemplar defaults

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar-defaults)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 118 | MUST | ✅ found | The SDK MUST include two types of built-in exemplar reservoirs: SimpleFixedSizeExemplarReservoir and AlignedHistogramBucketExemplarReservoir. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os`, `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os` | ОтелРезервуарЭкземпляров и ОтелВыровненныйРезервуарГистограммы. |
| 119 | SHOULD | ✅ found | Explicit bucket histogram aggregation with more than 1 bucket SHOULD use AlignedHistogramBucketExemplarReservoir. | `src/Метрики/Классы/ОтелМетр.os` | Гистограммы используют ОтелВыровненныйРезервуарГистограммы. |
| 120 | SHOULD | ✅ found | Base2 Exponential Histogram Aggregation SHOULD use a SimpleFixedSizeExemplarReservoir with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty (e.g. min(20, max_buckets)). | `src/Метрики/Классы/ОтелМетр.os` | Экспоненциальные гистограммы: ОтелРезервуарЭкземпляров(Мин(20, МаксБакетов)). |
| 121 | SHOULD | ✅ found | All other aggregations SHOULD use SimpleFixedSizeExemplarReservoir. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os` | Счетчики, датчики и реверсивные счетчики используют ОтелРезервуарЭкземпляров. |

#### SimpleFixedSizeExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#simplefixedsizeexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 122 | MUST | ✅ found | This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the reservoir has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:46` |  |
| 123 | SHOULD | ❌ not_found | Any stateful portion of sampling computation SHOULD be reset every collection cycle. | - | Метод Собрать() возвращает данные, но не сбрасывает счетчик num_measurements_seen (Счетчики). Метод Очистить() очищает все данные, но не вызывается автоматически при каждом цикле сбора. Нет автоматического сброса счетчиков при collection. |
| 124 | SHOULD | ✅ found | If no size configuration is provided, a default size of 1 SHOULD be used. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:100` |  |

#### AlignedHistogramBucketExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#alignedhistogrambucketexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 125 | MUST | ✅ found | This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os` | Конструктор принимает массив Границы. |
| 126 | MUST | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os` | Один слот на бакет, последнее заменяет предыдущее. |
| 127 | SHOULD | ✅ found | This implementation SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os` | Последнее измерение заменяет предыдущее в бакете. |
| 128 | SHOULD | ✅ found | This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os` | Тот же формат Массив границ. |

#### Custom ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#custom-exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 129 | MUST | ✅ found | The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation. | `src/Метрики/Классы/ОтелПредставление.os`, `src/Метрики/Классы/ОтелМетр.os` | View принимает кастомный резервуар, применяется к инструменту. |
| 130 | MUST | ✅ found | This extension MUST be configurable on a metric View. | `src/Метрики/Классы/ОтелМетр.os` | ОтелПредставление.РезервуарЭкземпляров() применяется в ПрименитьПредставлениеКИнструменту(). |
| 131 | MUST | ⚠️ partial | Individual reservoirs MUST still be instantiated per metric-timeseries. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os` | Один резервуар на инструмент с внутренним разделением по ключу серии, а не отдельный экземпляр на серию. |

#### MetricReader operations#### Collect

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader-operations-collect)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 132 | SHOULD | ⚠️ partial | Collect SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:68` | Метод СброситьБуфер() (аналог Collect) является Процедурой, а не Функцией - не возвращает результат (успех/ошибка/таймаут). Ошибки логируются, но вызывающий код не получает информацию о результате. |
| 133 | SHOULD | ❌ not_found | Collect SHOULD invoke Produce on registered MetricProducers. | - | Нет реализации MetricProducer и метода Produce. Collect собирает данные только из зарегистрированных Meter, но не из внешних MetricProducer. |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 134 | MUST | ✅ found | Shutdown MUST be called only once for each MetricReader instance. After the call to Shutdown, subsequent invocations to Collect are not allowed. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os` | АтомарноеБулево с СравнитьИУстановить для однократного Shutdown |
| 135 | SHOULD | ❌ not_found | SDKs SHOULD return some failure for calls to Collect after Shutdown, if possible. | - | Нет проверки флага Закрыт в методах СброситьБуфер() и СобратьИЭкспортировать(). После Shutdown эти методы продолжают работать нормально, не возвращая ошибку. |
| 136 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:85` | Метод Закрыть() - Процедура, а не Функция, не возвращает результат. Таймаут обрабатывается при ожидании фонового задания, но результат не передается вызывающему коду. |
| 137 | SHOULD | ✅ found | Shutdown SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:89` |  |

#### Periodic exporting MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 138 | MUST | ✅ found | The reader MUST synchronize calls to MetricExporter's Export to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os` | Добавлена БлокировкаЭкспорта вокруг вызова Экспортировать() |
| 139 | SHOULD | ✅ found | ForceFlush SHOULD collect metrics, call Export(batch) and ForceFlush() on the configured Push Metric Exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:68` |  |
| 140 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:68` | Метод СброситьБуфер() является Процедурой и не возвращает результат. Ошибки логируются, но вызывающий код не информируется об успехе или неудаче. |
| 141 | SHOULD | ⚠️ partial | ForceFlush SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:68` | СброситьБуфер() - Процедура без возвращаемого значения. Нет статусов ERROR/NO ERROR для возврата вызывающему коду. |
| 142 | SHOULD | ❌ not_found | ForceFlush SHOULD complete or abort within some timeout. | - | Метод СброситьБуфер() вызывает СобратьИЭкспортировать() синхронно без таймаута. Нет механизма ограничения времени выполнения ForceFlush. |

#### MetricExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 143 | MUST | ✅ found | MetricExporter defines the interface that protocol-specific exporters MUST implement so that they can be plugged into OpenTelemetry SDK and support sending of telemetry data. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:19` |  |
| 144 | SHOULD | ❌ not_found | Metric Exporters SHOULD report an error condition for data output by the MetricReader with unsupported Aggregation or Aggregation Temporality. | - | Экспортер не проверяет, соответствует ли Aggregation или Temporality его возможностям. Данные экспортируются без валидации типа агрегации. |
| 145 | MUST | ✅ found | A Push Metric Exporter MUST support the following functions: Export(batch). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:19` |  |
| 146 | MUST | ✅ found | The SDK MUST provide a way for the exporter to get the Meter information (e.g. name, version, etc.) associated with each Metric Point. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:91` |  |
| 147 | MUST NOT | ⚠️ partial | Export MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:19` | Метод Экспортировать() вызывает Транспорт.Отправить() синхронно. Таймаут задан на уровне HTTP-транспорта (ТаймаутСекунд), но в самом экспортере нет явного ограничения. Не всегда гарантируется error result при timeout. |
| 148 | SHOULD NOT | ✅ found | The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the metrics are being sent to. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:19` |  |
| 149 | SHOULD | ⚠️ partial | This is a hint to ensure that the export of any Metrics the exporter has received prior to the call to ForceFlush SHOULD be completed as soon as possible, preferably before returning from this method. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` | Метод СброситьБуфер() экспортера пуст (нет буферизации - синхронный экспорт), что формально корректно, но нет явного указания что все данные экспортированы. |
| 150 | SHOULD | ⚠️ partial | ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` | СброситьБуфер() экспортера - Процедура без возвращаемого значения, не информирует о результате. |
| 151 | SHOULD | ❌ not_found | ForceFlush SHOULD complete or abort within some timeout. | - | СброситьБуфер() экспортера - пустой метод без таймаута. Для синхронного экспорта это неактуально, но при буферизации будет проблемой. |
| 152 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each MetricExporter instance. After the call to Shutdown subsequent calls to Export are not allowed and should return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` |  |
| 153 | SHOULD NOT | ✅ found | Shutdown SHOULD NOT block indefinitely. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` |  |
| 154 | MUST | ✅ found | A Push Metric Exporter MUST support the ForceFlush function. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:43` |  |
| 155 | MUST | ✅ found | A Push Metric Exporter MUST support the Shutdown function. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:49` |  |

#### Pull Metric Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#pull-metric-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 156 | MUST | ✅ found | MetricProducer defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data. | - | There is no separate MetricProducer interface. The SDK collects metrics directly from Meter objects registered in MetricReader, not through a MetricProducer interface. However, the pull exporter (ОтелПрометеусЧитательМетрик) is modeled as a MetricReader which is one of the allowed approaches per the spec ("they could model the pull exporter as MetricReader"). The MUST here applies to third-party metric sources implementing MetricProducer - since no third-party bridging is present, the MetricProducer interface itself is not implemented as a separate entity. |
| 157 | SHOULD | ❌ not_found | MetricProducer implementations SHOULD accept configuration for the AggregationTemporality of produced metrics. | - | No MetricProducer interface exists. The Prometheus reader (ОтелПрометеусЧитательМетрик) does not accept AggregationTemporality configuration - it always outputs cumulative data per Prometheus convention. No separate MetricProducer with temporality config. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 158 | MUST | ❌ not_found | A MetricFilter MUST support the following functions (TestMetric, TestAttributes). | - | No MetricFilter interface or class exists in the codebase. No TestMetric or TestAttributes operations are implemented. |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 159 | MUST | ❌ not_found | A MetricFilter MUST support the following functions (TestMetric, TestAttributes). | - | No MetricFilter interface or class exists in the codebase. No TestMetric or TestAttributes operations are implemented. |

#### TestMetric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#testmetric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 160 | MUST | ❌ not_found | The SDK MUST provide configuration according to the SDK environment variables specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1` | The SDK does provide environment variable configuration through ОтелАвтоконфигурация module, supporting OTEL_METRICS_EXPORTER, OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE, OTEL_EXPORTER_OTLP_METRICS_DEFAULT_HISTOGRAM_AGGREGATION and other OTEL_ variables. However, several metrics-specific SDK env variables from the spec (like OTEL_METRIC_EXPORT_INTERVAL, OTEL_METRIC_EXPORT_TIMEOUT) are not implemented - only a subset is covered. |

#### Numerical limits handling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#numerical-limits-handling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 161 | MUST | ❌ not_found | The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry. | - | No explicit numerical limits handling is implemented in the metrics SDK. There are no checks for overflow, underflow, or error handling for extreme numerical values in aggregators (ОтелАгрегаторСуммы, ОтелАгрегаторГистограммы, etc.). |
| 162 | MUST | ➖ n_a | If the SDK receives float/double values from Instruments, it MUST handle all the possible values (e.g. NaN and Infinities for IEEE 754). | - | OneScript does not have IEEE 754 float/double types with NaN/Infinity values. OneScript's Число (Number) type is a decimal/arbitrary precision number that does not produce NaN or Infinity values, so this requirement is not applicable to the OneScript platform. |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 163 | SHOULD | ✅ found | All the metrics components SHOULD allow new methods to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:1` |  |
| 164 | SHOULD | ✅ found | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to existing methods without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:50` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 165 | MUST | ⚠️ partial | MeterProvider - Meter creation, ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:221` | Meter creation (ПолучитьМетр) uses СинхронизированнаяКарта for thread-safe access to the meters cache. However, ForceFlush (СброситьБуфер) and Shutdown (Закрыть) iterate over ЧитателиМетрик array without synchronization - these methods are not explicitly thread-safe. |
| 166 | MUST | ✅ found | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:101` |  |
| 167 | MUST | ✅ found | MetricReader - Collect, ForceFlush (for periodic exporting MetricReader) and Shutdown MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:11` |  |
| 168 | MUST | ❌ not_found | MetricExporter - ForceFlush and Shutdown MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:40` | ОтелЭкспортерМетрик does not use any synchronization (no БлокировкаРесурса, no СинхронизированнаяКарта). The СброситьБуфер and Закрыть methods are not thread-safe - concurrent calls to Закрыть and Экспортировать could race on the Закрыт flag. |

### Otlp Exporter

#### Configuration Options

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#configuration-options)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The following configuration options MUST be available to configure the OTLP exporter. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:130` |  |
| 2 | MUST | ❌ not_found | Each configuration option MUST be overridable by a signal specific option. | - | Нет поддержки сигнал-специфичных переменных окружения (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT, OTEL_EXPORTER_OTLP_METRICS_HEADERS и т.д.). Используется только общий набор otel.exporter.otlp.* для всех сигналов. |
| 3 | MUST | ✅ found | The implementation MUST honor the following URL components: scheme (http or https), host, port, path. | `src/Экспорт/Классы/ОтелHttpТранспорт.os` | URL обрабатывается через КоннекторHTTP. Trailing slash в base URL нормализуется в ВыполнитьОднуПопытку(). |
| 4 | MUST | ✅ found | When using OTEL_EXPORTER_OTLP_ENDPOINT, exporters MUST construct per-signal URLs by appending signal paths (v1/traces, v1/metrics, v1/logs) relative to the base URL. | `src/Экспорт/Классы/ОтелHttpТранспорт.os` | Trailing slash нормализуется перед конкатенацией пути сигнала. |
| 5 | SHOULD | ➖ n_a | The gRPC endpoint option SHOULD accept any form allowed by the underlying gRPC client implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:129` | gRPC реализован через OPI_GRPC (oint) - обёртку над HTTP/2, а не нативный gRPC-клиент. Формат адреса определяется внешней библиотекой. |
| 6 | MUST | ✅ found | Additionally, the gRPC endpoint option MUST accept a URL with a scheme of either http or https. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:153` |  |
| 7 | SHOULD | ✅ found | If the gRPC client implementation does not support an endpoint with a scheme of http or https then the endpoint SHOULD be transformed to the most sensible format. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:153` |  |
| 8 | MUST | ✅ found | Protocol options MUST be one of: grpc, http/protobuf, http/json. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` |  |
| 9 | SHOULD | ✅ found | SDKs SHOULD default endpoint variables to use http scheme unless they have good reasons to choose https scheme for the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:158` |  |
| 10 | SHOULD | ❌ not_found | The obsolete OTEL_EXPORTER_OTLP_SPAN_INSECURE and OTEL_EXPORTER_OTLP_METRIC_INSECURE SHOULD continue to be supported as they were part of a stable release of the specification. | - | Устаревшие переменные OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE не реализованы. Требование условно (SHOULD continue to be supported if already implemented), но никогда не были реализованы. |
| 11 | MUST | ⚠️ partial | For the per-signal variables (OTEL_EXPORTER_OTLP_<signal>_ENDPOINT), the URL MUST be used as-is without any modification. | - | Per-signal endpoint переменные (OTEL_EXPORTER_OTLP_TRACES_ENDPOINT и т.д.) не поддерживаются, поэтому невозможно использовать URL as-is для конкретного сигнала. |
| 12 | MUST | ⚠️ partial | If a per-signal URL contains no path part, the root path / MUST be used (see Example 2). | - | Per-signal endpoint переменные не поддерживаются, поэтому логика обработки пустого пути для per-signal URL отсутствует. |
| 13 | MUST NOT | ⚠️ partial | An SDK MUST NOT modify the URL in ways other than specified above. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:74` | URL не модифицируется сверх конкатенации БазовыйURL + Путь. Однако per-signal endpoints не поддерживаются, что ограничивает полноту оценки. |
| 14 | SHOULD | ⚠️ partial | The default protocol SHOULD be http/protobuf unless SDKs have good reasons to choose grpc as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Дефолтный протокол установлен как http/json (строка 150), а не http/protobuf. OneScript не поддерживает protobuf нативно для HTTP, поэтому используется JSON. |
| 15 | MUST | ✅ found | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal by appending v1/traces, v1/metrics, v1/logs to the base OTEL_EXPORTER_OTLP_ENDPOINT. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:32` |  |

#### Specify Protocol

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specify-protocol)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ✅ found | SDKs SHOULD support both grpc and http/protobuf transports. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:1` |  |
| 17 | MUST | ✅ found | SDKs MUST support at least one of grpc or http/protobuf transports. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:1` |  |
| 18 | SHOULD | ✅ found | If SDKs support only one transport, it SHOULD be http/protobuf. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:1` |  |
| 19 | SHOULD | ⚠️ partial | If no configuration is provided the default transport SHOULD be http/protobuf unless SDKs have good reasons to choose grpc as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:150` | Дефолтный протокол - http/json (строка 150), а не http/protobuf. HTTP-транспорт отправляет JSON, не protobuf. Это осознанный выбор из-за отсутствия нативной поддержки protobuf для HTTP в OneScript. |

#### Specifying headers via environment variables

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | All attribute values MUST be considered strings (in OTEL_EXPORTER_OTLP_HEADERS environment variable key-value pairs). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:467` |  |

#### Retry

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#retry)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | Transient errors MUST be handled with a retry strategy. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:82` |  |
| 22 | MUST | ✅ found | This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered. | `src/Экспорт/Классы/ОтелHttpТранспорт.os`, `src/Экспорт/Классы/ОтелGrpcТранспорт.os` | Экспоненциальная задержка с jitter-фактором (0.5 + случайное/2000) |

#### Transient errors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#transient-errors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | SHOULD | ❌ not_found | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter. | - | Нет User-Agent заголовка ни в HTTP-транспорте (ОтелHttpТранспорт.os), ни в gRPC-транспорте (ОтелGrpcТранспорт.os). HTTP-транспорт устанавливает только Content-Type и пользовательские заголовки. |
| 24 | SHOULD | ❌ not_found | The format of the User-Agent header SHOULD follow RFC 7231. | - | User-Agent заголовок не реализован, поэтому формат RFC 7231 также не может быть соблюден. |
| 25 | SHOULD | ❌ not_found | The resulting User-Agent SHOULD include the exporter's default User-Agent string when a product identifier configuration option is used. | - | User-Agent заголовок не реализован вообще, конфигурация product identifier также отсутствует. |

### Propagators

#### Operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Propagators MUST define Inject and Extract operations, in order to write values to and read values from carriers respectively. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:38,68` |  |
| 2 | MUST | ✅ found | Each Propagator type MUST define the specific carrier type and MAY define additional parameters. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:38` |  |

#### Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The Propagator MUST retrieve the appropriate value from the Context first, such as SpanContext, Baggage or another cross-cutting concern context. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:39` |  |
| 4 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:76-102` |  |
| 5 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT store a new value in the Context, in order to preserve any previously existing valid value. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:77,82,87,97,101` |  |

#### TextMap Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | In order to increase compatibility, the key/value pairs MUST only consist of US-ASCII characters that make up valid HTTP header fields as per RFC 9110. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:50-51` |  |
| 7 | MUST | ⚠️ partial | Getter and Setter MUST be stateless and allowed to be saved as constants, in order to effectively avoid runtime allocations. | - | There are no separate Getter or Setter objects/interfaces in the codebase. Propagators directly work with Соответствие (Map) as carriers - reading via iteration (Для Каждого КлючИЗначение Из Заголовки) and writing via Заголовки.Вставить(). The Getter/Setter abstraction as separate stateless objects does not exist. |

#### TextMap Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ⚠️ partial | The implementation SHOULD preserve casing (e.g. it should not transform Content-Type to content-type) if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:51` | Casing is preserved for injected keys (e.g. 'traceparent', 'tracestate', 'baggage' are lowercase constants). However, there is no explicit Setter interface - values are written directly via Заголовки.Вставить(), which preserves the key as-is. The implementation effectively preserves casing but lacks the Setter abstraction. |
| 9 | MUST | ⚠️ partial | The implementation MUST preserve casing if the used protocol is not case insensitive. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:51` | Casing is preserved in practice (keys written as literal strings), but there is no Setter interface that formally guarantees casing preservation as a contract. |

#### Getter argument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#getter-argument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ❌ not_found | The Keys function MUST return the list of all the keys in the carrier. | - | There is no Getter interface or Keys function. Propagators iterate over the carrier (Соответствие) directly using Для Каждого instead of using a Getter.Keys() abstraction. |
| 11 | MUST | ❌ not_found | The Get function MUST return the first value of the given propagation key or return null if the key doesn't exist. | - | There is no Getter.Get() function. The propagators iterate over all headers manually (Для Каждого КлючИЗначение Из Заголовки) checking НРег(КлючИЗначение.Ключ) to find keys, instead of using a Get function. |
| 12 | MUST | ⚠️ partial | The Get function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:71` | Case-insensitive lookup IS implemented inline (НРег(КлючИЗначение.Ключ) = 'traceparent'), but it is not in a separate Getter.Get() function - it's inline in each propagator's Extract method. |
| 13 | MUST | ❌ not_found | If explicitly implemented, the GetAll function MUST return all values of the given propagation key. | - | There is no GetAll function or Getter interface. The inline iteration in propagators only finds the last matching header value (overwriting on each match), not all values. |
| 14 | SHOULD | ❌ not_found | GetAll SHOULD return values in the same order as they appear in the carrier. | - | No GetAll function exists. See above - no Getter interface is implemented. |
| 15 | SHOULD | ❌ not_found | If the key doesn't exist, GetAll SHOULD return an empty collection. | - | No GetAll function exists. No Getter interface is implemented. |
| 16 | MUST | ⚠️ partial | The GetAll function is responsible for handling case sensitivity. If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:71` | Case-insensitive lookup is implemented inline via НРег() in each propagator's Extract, but there is no separate GetAll function or Getter interface. |

#### Composite Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | Implementations MUST offer a facility to group multiple Propagators from different cross-cutting concerns in order to leverage them as a single entity. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:1-77` |  |
| 18 | MUST | ✅ found | There MUST be functions to accomplish the following operations: Create a composite propagator, Extract from a composite propagator, Inject into a composite propagator. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:17,33,73` |  |

#### Composite Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | The OpenTelemetry API MUST provide a way to obtain a propagator for each supported Propagator type. | `src/Ядро/Модули/ОтелГлобальный.os:108` |  |
| 20 | SHOULD | ✅ found | Instrumentation libraries SHOULD call propagators to extract and inject the context on all remote calls. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:17` |  |
| 21 | MUST | ✅ found | The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise. | `src/Пропагация/Классы/ОтелНоопПропагатор.os`, `src/Ядро/Модули/ОтелГлобальный.os` | Создан класс ОтелНоопПропагатор. ОтелГлобальный.ПолучитьПропагаторы() возвращает его по умолчанию. |
| 22 | SHOULD | ✅ found | If pre-configured, Propagators SHOULD default to a composite Propagator containing the W3C Trace Context Propagator and the Baggage Propagator specified in the Baggage API. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:341` |  |
| 23 | MUST | ✅ found | These platforms MUST also allow pre-configured propagators to be disabled or overridden. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:339` |  |

#### Get Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#get-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | This method MUST exist for each supported Propagator type. Returns a global Propagator. | `src/Ядро/Модули/ОтелГлобальный.os` | ОтелГлобальный.ПолучитьПропагаторы() существует и больше не выбрасывает исключение без настроенного SDK |

#### Set Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#set-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 25 | MUST | ✅ found | This method MUST exist for each supported Propagator type. Sets the global Propagator instance. | `src/Ядро/Модули/ОтелГлобальный.os` | Добавлен метод ОтелГлобальный.УстановитьПропагаторы() с хранением через АтомарнаяСсылка, независимо от SDK. |
| 26 | MUST | ⚠️ partial | The official list of propagators that MUST be maintained by the OpenTelemetry organization: W3C TraceContext, W3C Baggage, B3. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:1` | W3C TraceContext и W3C Baggage реализованы. B3 Propagator отсутствует (не реализован как extension package). |
| 27 | MUST | ⚠️ partial | The official list of propagators MUST be distributed as OpenTelemetry extension packages: W3C TraceContext (MAY alternatively be in API), W3C Baggage (MAY alternatively be in API), B3. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:1` | W3C TraceContext и Baggage распространяются как часть API (допускается по MAY-оговорке). B3 не реализован ни как extension, ни inline. |
| 28 | MUST NOT | ❌ not_found | OT Trace propagator MUST NOT use OpenTracing in the resulting propagator name as it is not widely adopted format in the OpenTracing ecosystem. | - | OT Trace пропагатор не реализован в данном SDK. Требование к именованию неприменимо без реализации, но OT Trace не входит в список разрешённых n_a. |
| 29 | MUST NOT | ✅ found | Additional Propagators implementing vendor-specific protocols such as AWS X-Ray trace header protocol MUST NOT be maintained or distributed as part of the Core OpenTelemetry repositories. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:1` |  |

#### W3C Trace Context Requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#w3c-trace-context-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | A W3C Trace Context propagator MUST parse and validate the traceparent and tracestate HTTP headers as specified in W3C Trace Context Level 2. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:68` |  |
| 31 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid traceparent value using the same header. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:51` |  |
| 32 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid tracestate unless the value is empty, in which case the tracestate header may be omitted. | `src/Пропагация/Модули/ОтелW3CПропагатор.os:53` |  |

### Env Vars

#### Environment Variable Specification

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#environment-variable-specification)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If they do, they SHOULD use the names and value parsing behavior specified in this document. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:6-34` |  |
| 2 | SHOULD | ⚠️ partial | They SHOULD also follow the common configuration specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:59` | Автоконфигурация использует configor (МенеджерПараметров) для чтения переменных окружения, что соответствует общему подходу конфигурации. Однако не все аспекты common configuration specification реализованы (например, нет поддержки OTEL_CONFIG_FILE). |

#### Implementation guidelines

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#implementation-guidelines)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The environment-based configuration MUST have a direct code configuration equivalent. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:59` |  |

#### Parsing empty value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#parsing-empty-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:105` |  |

#### Type-specific guidance### Boolean

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#type-specific-guidance-boolean)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Any value that represents a Boolean MUST be set to true only by the case-insensitive string "true", meaning "True" or "TRUE" are also accepted, as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 6 | MUST NOT | ✅ found | An implementation MUST NOT extend this definition and define additional values that are interpreted as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563` |  |
| 7 | MUST | ✅ found | Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-563` |  |
| 8 | SHOULD | ❌ not_found | If any value other than a true value, case-insensitive string "false", empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied. | - | Функция Включено() в строке 561-564 просто сравнивает НРег(Значение) = "true" и возвращает Ложь для всех остальных значений. Нет логирования предупреждения при получении нестандартного значения (не "true", не "false", не пустое). |
| 9 | SHOULD | ✅ found | All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562` |  |
| 10 | MUST NOT | ✅ found | Renaming or changing the default value MUST NOT happen without a major version upgrade. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:7` |  |

#### Numeric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#numeric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ❌ not_found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them as not set. | - | Числовые значения парсятся через Число() (например строка 224: Число(Менеджер.Параметр("otel.bsp.max.queue.size", "2048"))). При невалидном значении Число() выбросит исключение, а не сгенерирует предупреждение и проигнорирует настройку. Нет try/catch обёртки и нет логирования предупреждения. |
| 12 | SHOULD | ❌ not_found | For new implementations, these should be treated as MUST requirements (generate a warning and gracefully ignore unparseable numeric values). | - | То же что и предыдущее - нет graceful обработки невалидных числовых значений. Число() при невалидном вводе вызовет исключение вместо предупреждения и фолбэка на значение по умолчанию. |
| 13 | SHOULD | ❌ not_found | The following paragraph was added after stabilization and the requirements are thus qualified as "SHOULD" to allow implementations to avoid breaking changes. | - | Это контекстное предложение, уточняющее уровень SHOULD для предыдущих требований. Реализация не обрабатывает невалидные числовые значения gracefully - отсутствует try/catch и предупреждение. |

#### String

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#string)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | SHOULD | ⚠️ partial | Enum values SHOULD be interpreted in a case-insensitive manner. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:344` | Пропагаторы (otel.propagators) сравниваются case-insensitive через НРег() в строке 344. Однако другие enum-значения (otel.traces.sampler, otel.traces.exporter, otel.logs.exporter, otel.metrics.exporter) сравниваются case-sensitive (строки 177-178, 190-219, 255-256, 291-292). Например, ИмяСэмплера = "always_on" - сравнение без НРег(). |
| 15 | MUST | ⚠️ partial | For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os` | OTEL_TRACES_SAMPLER - graceful fallback без предупреждения. OTEL_PROPAGATORS - логирует предупреждение и пропускает. OTEL_*_EXPORTER - не обрабатываются. |

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
| 1 | SHOULD | ➖ n_a | Resource detectors SHOULD have a unique name for reference in configuration. | - | Resource detectors are not implemented as separate entities in this SDK. This is a conditional feature (Resource Detector Naming) that is not realized. |
| 2 | SHOULD | ➖ n_a | Names SHOULD be snake case and consist of lowercase alphanumeric and _ characters, which ensures they conform to declarative configuration property name requirements. | - | Resource detectors are not implemented as separate entities. Conditional feature not realized. |
| 3 | SHOULD | ➖ n_a | Resource detector names SHOULD reflect the root namespace of attributes they populate. | - | Resource detectors are not implemented as separate entities. Conditional feature not realized. |
| 4 | SHOULD | ➖ n_a | Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name which appropriately conveys their purpose. | - | Resource detectors are not implemented as separate entities. Conditional feature not realized. |
| 5 | SHOULD | ➖ n_a | An SDK which identifies multiple resource detectors with the same name SHOULD report an error. | - | Resource detectors are not implemented as separate entities. Conditional feature not realized. |
| 6 | SHOULD | ➖ n_a | Resource detectors SHOULD document their name in a manner which is easily discoverable. | - | Resource detectors are not implemented as separate entities. Conditional feature not realized. |
| 7 | MUST | ✅ found | The SDK MUST extract information from the OTEL_RESOURCE_ATTRIBUTES environment variable and merge this, as the secondary resource, with any resource information provided by the user, i.e. the user provided resource information has higher priority. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:96` |  |
| 8 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:108` |  |
| 9 | MUST | ❌ not_found | The , and = characters in keys and values MUST be percent encoded. Other characters MAY be percent-encoded. | - | The parsing function РазобратьПарыКлючЗначение() (line 467) splits by comma and equals but does NOT perform percent-decoding of keys or values. Percent-encoded values like %2C or %3D will be stored literally instead of being decoded to , and =. |
| 10 | SHOULD | ❌ not_found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded. | - | The parsing function РазобратьПарыКлючЗначение() silently ignores malformed entries (pairs without '=') but does not discard the entire value on error. Individual bad entries are skipped while valid entries are kept. |
| 11 | SHOULD | ❌ not_found | In case of any error an error SHOULD be reported following the Error Handling principles. | - | No error reporting mechanism exists in the OTEL_RESOURCE_ATTRIBUTES parsing. Malformed entries are silently ignored without logging any error or warning. |

### Trace Api

#### Tracer operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracer-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The Tracer MUST provide functions to: Create a new Span | `src/Трассировка/Классы/ОтелТрассировщик.os:48` |  |
| 2 | SHOULD | ✅ found | The Tracer SHOULD provide functions to: Report if Tracer is Enabled | `src/Трассировка/Классы/ОтелТрассировщик.os:33` |  |
| 3 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when creating Spans, a Tracer SHOULD provide this Enabled API | `src/Трассировка/Классы/ОтелТрассировщик.os:33` |  |
| 4 | MUST | ✅ found | There are currently no required parameters for this API. Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added | `src/Трассировка/Классы/ОтелТрассировщик.os:33` |  |
| 5 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. A returned value of true means the Tracer is enabled for the provided arguments, and a returned value of false means the Tracer is disabled | `src/Трассировка/Классы/ОтелТрассировщик.os:33` |  |
| 6 | SHOULD | ❌ not_found | The API SHOULD be documented that instrumentation authors needs to call this API each time they create a new Span to ensure they have the most up-to-date response | - | Документация метода Включен() не содержит рекомендации вызывать его перед каждым созданием спана |

### Trace Sdk

#### Tracer Provider### Tracer Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer-provider-tracer-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create Tracer instances through a TracerProvider (see API). | `src/Трассировка/Классы/ОтелТрассировщик.os:160` |  |
| 2 | MUST | ✅ found | The TracerProvider MUST implement the Get a Tracer API. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:52` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Tracer. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:57-58` |  |
| 4 | MUST | ❌ not_found | The TracerProvider MUST compute the relevant TracerConfig using the configured TracerConfigurator, and create a Tracer whose behavior conforms to that TracerConfig. | - | Нет TracerConfigurator и TracerConfig. TracerProvider создаёт Tracer напрямую без вычисления TracerConfig через конфигуратор. |

#### TracerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | The function MUST accept the following parameter: tracer_scope: The InstrumentationScope of the Tracer. | - | TracerConfigurator не реализован. Нет функции/класса, принимающего InstrumentationScope для вычисления конфигурации трассировщика. |
| 2 | MUST | ❌ not_found | The function MUST return the relevant TracerConfig, or some signal indicating that the default TracerConfig should be used. | - | TracerConfigurator не реализован. Нет функции, возвращающей TracerConfig. |
| 3 | MUST | ✅ found | Shutdown MUST be called only once for each TracerProvider instance. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:100-105` |  |
| 4 | SHOULD | ⚠️ partial | After the call to Shutdown, subsequent attempts to get a Tracer are not allowed. SDKs SHOULD return a valid no-op Tracer for these calls, if possible. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:59-61` | После Закрыть() ПолучитьТрассировщик() возвращает новый ОтелТрассировщик, а не NoOp-трассировщик. Трассировщик создаётся обычный, но не кешируется. |
| 5 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:100-105` | Закрыть() - процедура без возвращаемого значения, не сообщает вызывающему об успехе/неудаче/таймауте. |
| 6 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:100-105` | Закрыть() не имеет механизма таймаута - блокирующий вызов без ограничения времени. |
| 7 | MUST | ✅ found | Shutdown MUST be implemented at least by invoking Shutdown within all internal processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:101-103` |  |

#### Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | Tracer MUST behave according to the TracerConfig computed during Tracer creation. | - | TracerConfig не реализован. Tracer не имеет ссылки на TracerConfig и не использует его для определения поведения. |
| 2 | MUST | ❌ not_found | If the TracerProvider supports updating the TracerConfigurator, then upon update the Tracer MUST be updated to behave according to the new TracerConfig. | - | TracerConfigurator и TracerConfig не реализованы. Нет механизма обновления конфигурации отдельного трассировщика через TracerConfig. |

#### TracerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | If not explicitly set, the enabled parameter SHOULD default to true (i.e. Tracers are enabled by default). | - | TracerConfig не реализован как отдельная сущность с параметром enabled. Включённость трассировщика определяется наличием процессоров, а не явным параметром enabled в TracerConfig. |
| 2 | MUST | ⚠️ partial | If a Tracer is disabled, it MUST behave equivalently to a No-op Tracer. | `src/Трассировка/Классы/ОтелТрассировщик.os:33-35` | Метод Включен() проверяет наличие процессоров, но при Включен()=Ложь трассировщик всё равно создаёт обычные спаны - нет перехода к NoOp-поведению на уровне Tracer. |
| 3 | MUST | ❌ not_found | The value of enabled MUST be used to resolve whether a Tracer is Enabled. If enabled is false, Enabled returns false. If enabled is true, Enabled returns true. | - | TracerConfig.enabled не реализован. Метод Включен() проверяет наличие процессоров, а не значение enabled из TracerConfig. |
| 4 | MUST | ❌ not_found | The changes MUST be eventually visible. | - | TracerConfig не реализован, поэтому нет механизма отслеживания изменений параметров конфигурации трассировщика. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | Enabled MUST return false when either: there are no registered SpanProcessors, or Tracer is disabled (TracerConfig.enabled is false). | `src/Трассировка/Классы/ОтелТрассировщик.os:33-35` | Включен() проверяет наличие процессоров (первое условие), но не проверяет TracerConfig.enabled (второе условие), так как TracerConfig не реализован. |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return true. | `src/Трассировка/Классы/ОтелТрассировщик.os:33-35` |  |

#### AlwaysOn* Returns `RECORD_AND_SAMPLE` always.* Description MUST be `AlwaysOnSampler`.#### AlwaysOff* Returns `DROP` always.* Description MUST be `AlwaysOffSampler`.#### TraceIdRatioBased

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwayson-returns-recordandsample-always-description-must-be-alwaysonsampler-alwaysoff-returns-drop-always-description-must-be-alwaysoffsampler-traceidratiobased)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | AlwaysOn: Description MUST be AlwaysOnSampler. | `src/Трассировка/Модули/ОтелСэмплер.os` | Описание() возвращает "AlwaysOnSampler" для стратегии ВсегдаВключен. |
| 2 | MUST | ✅ found | AlwaysOff: Description MUST be AlwaysOffSampler. | `src/Трассировка/Модули/ОтелСэмплер.os` | Описание() возвращает "AlwaysOffSampler" для стратегии ВсегдаВыключен. |
| 3 | MUST NOT | ✅ found | OpenTelemetry SDK implementors SHALL NOT remove or modify the behavior of the original TraceIdRatioBased sampler until at least January 1, 2027. | `src/Трассировка/Модули/ОтелСэмплер.os:81-83` |  |
| 4 | MUST | ✅ found | The TraceIdRatioBased MUST ignore the parent SampledFlag. | `src/Трассировка/Модули/ОтелСэмплер.os:247-268` |  |
| 5 | MUST | ✅ found | Description MUST return a string of the form TraceIdRatioBased{RATIO} with RATIO replaced with the Sampler instance's trace sampling ratio represented as a decimal number. | `src/Трассировка/Модули/ОтелСэмплер.os` | Описание() возвращает "TraceIdRatioBased{X}" с текущим ratio. |
| 6 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards. | `src/Трассировка/Модули/ОтелСэмплер.os` | Используется стандартное преобразование Строка(Доля). |
| 7 | SHOULD | ✅ found | The precision SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os` | Используется полная точность Строка(Доля). |
| 8 | MUST | ✅ found | The sampling algorithm MUST be deterministic. A trace identified by a given TraceId is sampled or not independent of language, time, etc. | `src/Трассировка/Модули/ОтелСэмплер.os:247-268` |  |
| 9 | MUST | ✅ found | Implementations MUST use a deterministic hash of the TraceId when computing the sampling decision. | `src/Трассировка/Модули/ОтелСэмплер.os:260-262` |  |
| 10 | MUST | ✅ found | A TraceIdRatioBased sampler with a given sampling probability MUST also sample all traces that any TraceIdRatioBased sampler with a lower sampling probability would sample. | `src/Трассировка/Модули/ОтелСэмплер.os:262-268` |  |
| 11 | SHOULD | ❌ not_found | When this sampler observes a non-empty parent span context, meaning when it is used not as a root sampler, the SDK SHOULD emit a warning. | - | TraceIdRatioBased семплер (СэмплироватьПоДоле) не проверяет наличие родительского контекста и не выдаёт предупреждение при использовании не как корневой семплер. |
| 12 | MUST | ❌ not_found | The ProbabilitySampler sampler MUST ignore the parent SampledFlag. | - | ProbabilitySampler не реализован. В SDK есть только TraceIdRatioBased (ПоДолеТрассировок), AlwaysOn/Off и ParentBased. |
| 13 | SHOULD | ❌ not_found | When (R >= T), the OpenTelemetry TraceState SHOULD be modified to include the key-value th:T for rejection threshold value (T). | - | ProbabilitySampler не реализован. Нет логики работы с пороговыми значениями и подключами ot в TraceState. |
| 14 | SHOULD | ❌ not_found | When a ProbabilitySampler Sampler makes a decision for a non-root Span using TraceID randomness when the Trace random flag was not set, the SDK SHOULD issue a warning statement. | - | ProbabilitySampler не реализован. |
| 15 | MUST | ❌ not_found | Based on the decision from the wrapped root sampler, AlwaysRecord MUST behave as follows: DROP becomes RECORD_ONLY, RECORD_ONLY stays RECORD_ONLY, RECORD_AND_SAMPLE stays RECORD_AND_SAMPLE. | - | AlwaysRecord декоратор семплера не реализован. |
| 16 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the parameters passed to delegate GetSamplingIntent methods, as they are considered read-only state. | - | CompositeSampler и ComposableSampler не реализованы. |
| 17 | MUST NOT | ❌ not_found | ComposableSamplers MUST NOT modify the OpenTelemetry TraceState (i.e., the ot sub-key of TraceState). | - | CompositeSampler и ComposableSampler не реализованы. |
| 18 | MUST NOT | ❌ not_found | The explicit randomness values MUST not be modified by ComposableSamplers. | - | CompositeSampler и ComposableSampler не реализованы. |
| 19 | SHOULD | ❌ not_found | The calling CompositeSampler SHOULD update the threshold of the outgoing TraceState (unless !threshold_reliable). | - | CompositeSampler не реализован. |

#### IdGenerator randomness

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#idgenerator-randomness)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | Custom implementations of the IdGenerator SHOULD identify themselves appropriately when all generated TraceID values meet the W3C Trace Context Level 2 randomness requirements, so that the Trace random flag will be set in the associated Trace contexts. | - | The custom IdGenerator mechanism (УстановитьГенераторИд) has no way for implementations to declare W3C Level 2 randomness compliance. There is no marker interface, flag property, or any mechanism to indicate randomness support and set the random trace flag. |

#### OnEnding

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onending)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | The end timestamp MUST have been computed (the OnEnding method duration is not included in the span duration). | - | OnEnding is not implemented. In ОтелСпан.Завершить(), the end timestamp is set and then Завершен=Истина is immediately set before calling Процессор.ПриЗавершении (OnEnd). There is no intermediate OnEnding callback. |
| 2 | MUST | ❌ not_found | The Span object MUST still be mutable (i.e., SetAttribute, AddLink, AddEvent can be called) while OnEnding is called. | - | OnEnding is not implemented. By the time ПриЗавершении (OnEnd) is called, Завершен is already Истина, making the span immutable. |
| 3 | MUST | ❌ not_found | This method MUST be called synchronously within the Span.End() API, therefore it should not block or throw an exception. | - | OnEnding method does not exist in any processor implementation. |
| 4 | MUST | ❌ not_found | The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking OnEnding of the first SpanProcessor. | - | OnEnding is not implemented. The span uses a simple Завершен flag without thread-safety guarantees for the transition from mutable to OnEnding state. |

### Logs Api

#### Ergonomic API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#ergonomic-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | The ergonomic API SHOULD make it more convenient to emit event records following the event semantics. | - | No ergonomic/convenience logging API exists. There is no separate higher-level API for event-oriented logging beyond the base Logger.Записать() method. |
| 2 | SHOULD | ❌ not_found | The design of the ergonomic API SHOULD be idiomatic for its language. | - | No ergonomic API is implemented, so there is no language-idiomatic design to evaluate. |

### Logs Sdk

#### Logger Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create Logger instances through a LoggerProvider (see API). | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:46` |  |
| 2 | MUST | ✅ found | The LoggerProvider MUST implement the Get a Logger API. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:46` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Logger. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:56` |  |
| 4 | MUST | ✅ found | In the case where an invalid name (null or empty string) is specified, a working Logger MUST be returned as a fallback rather than returning null or throwing an exception. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:46` |  |
| 5 | SHOULD | ✅ found | Its name SHOULD keep the original invalid value. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:57` |  |
| 6 | SHOULD | ❌ not_found | A message reporting that the specified value is invalid SHOULD be logged. | - | ПолучитьЛоггер() не проверяет ИмяБиблиотеки на пустую строку/null и не логирует предупреждение при невалидном имени. |
| 7 | MUST | ✅ found | The LoggerProvider MUST compute the relevant LoggerConfig using the configured LoggerConfigurator, and create a Logger whose behavior conforms to that LoggerConfig. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:66` | Конфигуратор (callback) вызывается в ПолучитьЛоггер(), результат передается в конструктор ОтелЛоггер. |

#### LoggerConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The LoggerConfigurator function MUST accept the following parameter: logger_scope - the InstrumentationScope of the Logger. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:69` | Конфигуратор - Действие (callback), вызывается с ОбластьИнструментирования как параметром. |
| 2 | MUST | ✅ found | The LoggerConfigurator function MUST return the relevant LoggerConfig, or some signal indicating that the default LoggerConfig should be used. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:69` | Конфигуратор возвращает ОтелКонфигурацияЛоггера или Неопределено (default). |
| 3 | MUST | ⚠️ partial | Shutdown MUST be called only once for each LoggerProvider instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:99` | Метод Закрыть() существует, но не содержит защиты от повторного вызова (нет проверки 'Если Закрыт Тогда Возврат'). При повторном вызове Процессор.Закрыть() будет вызван повторно на всех процессорах. |
| 4 | SHOULD | ✅ found | After the call to Shutdown, subsequent attempts to get a Logger are not allowed. SDKs SHOULD return a valid no-op Logger for these calls, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:51` |  |
| 5 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:99` | Синхронный Закрыть() - Процедура (void), не возвращает статус. ЗакрытьАсинхронно() возвращает Обещание, но основной синхронный метод не сигнализирует об успехе/ошибке/таймауте. |
| 6 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:124` | ЗакрытьАсинхронно() возвращает Обещание с возможностью таймаута через Обещание.Получить(таймаут). Но синхронный Закрыть() не имеет механизма таймаута, может блокировать бесконечно. |
| 7 | MUST | ✅ found | Shutdown MUST be implemented by invoking Shutdown on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:100` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Logger MUST behave according to the LoggerConfig computed during logger creation. | `src/Логирование/Классы/ОтелЛоггер.os:49` | Включен() проверяет Конфигурация.Включен() и МинимальнаяСтепеньСерьезности(). |
| 2 | MUST | ✅ found | If the LoggerProvider supports updating the LoggerConfigurator, then upon update the Logger MUST be updated to behave according to the new LoggerConfig. | `src/Логирование/Классы/ОтелЛоггер.os:112` | УстановитьКонфигурацию() обновляет конфигурацию логгера. |

#### LoggerConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If not explicitly set, the enabled parameter SHOULD default to true (i.e. Loggers are enabled by default). | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:42` | Конструктор по умолчанию: НовыйВключен = Истина. |
| 2 | MUST | ✅ found | If a Logger is disabled, it MUST behave equivalently to No-op Logger. | `src/Логирование/Классы/ОтелЛоггер.os:50` | Включен() возвращает Ложь если Конфигурация.Включен() = Ложь. |
| 3 | MUST | ✅ found | If not explicitly set, the minimum_severity parameter MUST default to 0. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os:42` | Конструктор по умолчанию: НоваяМинимальнаяСтепеньСерьезности = 0. |
| 4 | MUST | ✅ found | If a log record's SeverityNumber is specified (i.e. not 0) and is less than the configured minimum_severity, the log record MUST be dropped by the Logger. | `src/Логирование/Классы/ОтелЛоггер.os:53` | Включен() проверяет НомерСерьезности < МинимальнаяСтепеньСерьезности(). |
| 5 | MUST | ⚠️ partial | If not explicitly set, the trace_based parameter MUST default to false. | `src/Логирование/Классы/ОтелКонфигурацияЛоггера.os` | ОтелКонфигурацияЛоггера не содержит параметра trace_based. |
| 6 | MUST | ❌ not_found | If trace_based is true, log records associated with unsampled traces MUST be dropped by the Logger. | - | Фильтрация trace_based не реализована. |
| 7 | MUST | ✅ found | It is not necessary for implementations to ensure that changes to any of these parameters are immediately visible to callers of Enabled. However, the changes MUST be eventually visible. | `src/Логирование/Классы/ОтелЛоггер.os:112` | УстановитьКонфигурацию() обновляет поле Конфигурация напрямую, изменения видны при следующем вызове Включен(). |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If Observed Timestamp is unspecified, the implementation SHOULD set it equal to the current time. | `src/Логирование/Классы/ОтелЛоггер.os:82` |  |
| 2 | MUST | ❌ not_found | If an Exception is provided, the SDK MUST by default set attributes from the exception on the LogRecord with the conventions outlined in the exception semantic conventions. | - | The Записать (emit) method has no exception handling logic. No exception semantic convention attributes (exception.type, exception.message, exception.stacktrace) are set automatically. |
| 3 | MUST | ❌ not_found | User-provided attributes MUST take precedence over exception-derived attributes. | - | No exception-derived attribute logic exists, so precedence rules are not applicable but also not implemented. |
| 4 | MUST NOT | ❌ not_found | User-provided attributes MUST NOT be overwritten by exception-derived attributes. | - | No exception-derived attribute logic exists, so the protection against overwriting is not implemented. |
| 5 | MUST | ⚠️ partial | Before processing a log record, the implementation MUST apply the filtering rules defined by the LoggerConfig (in case Enabled was not called prior to emitting the record). | `src/Логирование/Классы/ОтелЛоггер.os:53` | Фильтрация реализована в Включен(), но не дублируется в Записать(). Если вызвать Записать() без предварительного Включен(), фильтрация не применяется. |
| 6 | MUST | ⚠️ partial | Minimum severity: If the log record's SeverityNumber is specified (i.e. not 0) and is less than the configured minimum_severity, the log record MUST be dropped. | `src/Логирование/Классы/ОтелЛоггер.os:53` | Фильтрация по minimum_severity реализована в Включен(), но не в Записать(). |
| 7 | MUST | ❌ not_found | Trace-based: If trace_based is true, and if the log record has a SpanId and the TraceFlags SAMPLED flag is unset, the log record MUST be dropped. | - | No trace_based filtering in the emit path. Log records are never dropped based on trace sampling status. |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST NOT | ⚠️ partial | Any modifications to parameters inside Enabled MUST NOT be propagated to the caller. Parameters are immutable or passed by value. | `src/Логирование/Классы/ОтелЛоггер.os:41` | Logger.Включен не модифицирует параметры, но у LogRecordProcessor нет собственного метода Enabled. Logger.Включен не делегирует вызов в процессор - вместо этого проверяет только ЕстьПроцессоры(). Отдельный интерфейс Enabled на уровне LogRecordProcessor отсутствует. |

### Metrics Api

#### General characteristics#### Instrument name syntax

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-characteristics-instrument-name-syntax)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | The API SHOULD treat it (unit) as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:209` |  |
| 2 | MUST | ✅ found | It (unit) MUST be case-sensitive (e.g. kb and kB are different units), ASCII string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:209` |  |
| 3 | MUST | ✅ found | The API MUST treat it (description) as an opaque string. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:208` |  |
| 4 | MUST | ✅ found | It (description) MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or utf8mb3). | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:208` |  |
| 5 | MUST | ✅ found | It (description) MUST support at least 1023 characters. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:208` |  |
| 6 | MUST | ❌ not_found | OpenTelemetry SDKs MUST handle advisory parameters as described here. | - | Нет реализации advisory-параметров (ExplicitBucketBoundaries, Attributes) в API инструментов. Методы создания инструментов (СоздатьСчетчик, СоздатьГистограмму и т.д.) не принимают параметр advisory. |

### Metrics Sdk

#### Meter Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | It SHOULD only be possible to create Meter instances through a MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:49` |  |
| 2 | MUST | ✅ found | The MeterProvider MUST implement the Get a Meter API. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:49` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an InstrumentationScope instance which is stored on the created Meter. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:62` |  |
| 4 | MUST | ⚠️ partial | In the case where an invalid name (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:49` | ПолучитьМетр принимает любое имя и возвращает рабочий Meter, но нет явной проверки на пустую строку или null с сохранением оригинального невалидного значения и логированием предупреждения. |
| 5 | SHOULD | ⚠️ partial | Its name SHOULD keep the original invalid value. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:62` | Имя передаётся как есть в InstrumentationScope, но нет явной логики обработки невалидных имён - имя сохраняется, но это побочный эффект, а не явное поведение. |
| 6 | SHOULD | ❌ not_found | A message reporting that the specified value is invalid SHOULD be logged. | - | Нет проверки на невалидное имя (пустая строка или null) и нет логирования предупреждения в ПолучитьМетр. |
| 7 | MUST | ❌ not_found | The MeterProvider MUST compute the relevant MeterConfig using the configured MeterConfigurator, and create a Meter whose behavior conforms to that MeterConfig. | - | MeterConfigurator и MeterConfig не реализованы. Meter создаётся напрямую без вычисления конфигурации через конфигуратор. |

#### MeterConfigurator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfigurator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | The function MUST accept the following parameter: meter_scope - the InstrumentationScope of the Meter. | - | MeterConfigurator как отдельная функция/класс не реализован. Нет сущности, принимающей InstrumentationScope и возвращающей MeterConfig. |
| 2 | MUST | ❌ not_found | The function MUST return the relevant MeterConfig, or some signal indicating that the default MeterConfig should be used. | - | MeterConfigurator не реализован, возврат MeterConfig отсутствует. |
| 3 | MUST | ✅ found | Shutdown MUST be called only once for each MeterProvider instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:127` |  |
| 4 | SHOULD | ✅ found | After the call to Shutdown, subsequent attempts to get a Meter are not allowed. SDKs SHOULD return a valid no-op Meter for these calls, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:55` |  |
| 5 | SHOULD | ⚠️ partial | Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:127` | Метод Закрыть() - процедура без возвращаемого значения. Нет способа узнать результат (успех/ошибка/таймаут). ЗакрытьАсинхронно() возвращает Обещание, но синхронный вариант не возвращает статус. |
| 6 | SHOULD | ⚠️ partial | Shutdown SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:127` | Закрыть() вызывает Закрыть() на читателях, которые ждут фоновое задание с таймаутом, но сам MeterProvider.Закрыть() не имеет параметра таймаута. |
| 7 | MUST | ✅ found | Shutdown MUST be implemented at least by invoking Shutdown on all registered MetricReader and MetricExporter instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:133` |  |

#### Start timestamps

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#start-timestamps)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp, or the creation time of the instrument if this is the first collection interval for the instrument. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:215` | ВремяСтарта is initialized at instrument creation and reset after ОчиститьТочкиДанных(), which partially matches delta semantics, but this is always set regardless of aggregation temporality |
| 2 | MUST | ⚠️ partial | This implies that all data points with delta temporality aggregation for an instrument MUST share the same start timestamp. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:226-237` | All data points from ПолучитьТочкиДанных share the same ВремяСтарта, but there's no explicit delta vs cumulative distinction |
| 3 | MUST | ⚠️ partial | Cumulative timeseries MUST use a consistent start timestamp for all collection intervals. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:215` | ВремяСтарта is always reset after each export (ОчиститьТочкиДанных), which is correct for delta but breaks cumulative requirement of a consistent start timestamp |
| 4 | SHOULD | ❌ not_found | For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the series. | - | Start timestamp is set at instrument creation, not at the time of the first measurement for each series |
| 5 | SHOULD | ❌ not_found | For asynchronous instruments, the start timestamp SHOULD be: the creation time of the instrument if the first series measurement occurred in the first collection interval, otherwise the timestamp of the collection interval prior to the first series measurement. | - | Asynchronous instruments (ОтелБазовыйНаблюдаемыйИнструмент) set startTimeUnixNano to current time in ПреобразоватьЗаписиВТочки, not implementing the specified logic |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instrument registrations. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:62` |  |
| 2 | MUST | ⚠️ partial | Meter MUST behave according to the MeterConfig computed during Meter creation. | `src/Метрики/Классы/ОтелМетр.os:399` | Meter получает конфигурацию при создании (Представления, ФильтрЭкземпляров, ЛимитМощности), но отдельная сущность MeterConfig отсутствует. Конфигурация задаётся через отдельные параметры конструктора и сеттеры, а не через единый объект MeterConfig. |
| 3 | MUST | ❌ not_found | If the MeterProvider supports updating the MeterConfigurator, then upon update the Meter MUST be updated to behave according to the new MeterConfig. | - | MeterConfigurator не реализован. MeterProvider не поддерживает динамическое обновление конфигурации метров после создания. Нет механизма MeterConfigurator update. |

#### MeterConfig

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterconfig)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ❌ not_found | If not explicitly set, the enabled parameter SHOULD default to true (i.e. Meters are enabled by default). | - | MeterConfig как отдельная сущность не существует. Параметр enabled реализован на уровне инструментов (ОтелБазовыйСинхронныйИнструмент.Включен, строка 219, по умолчанию Истина), но не на уровне Meter. Нет MeterConfig.enabled. |
| 2 | MUST | ⚠️ partial | If a Meter is disabled, it MUST behave equivalently to No-op Meter. | `src/Метрики/Классы/ОтелМетр.os:379` | Meter можно отключить через ОтключитьИнструменты(), что отключает все инструменты (они перестают записывать). Но это не полноценный no-op: Meter по-прежнему создаёт новые инструменты, и нет MeterConfig.enabled для контроля на уровне метра. |
| 3 | MUST | ⚠️ partial | The value of enabled MUST be used to resolve whether an instrument is Enabled. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179` | Инструменты имеют метод Включен() (строка 179) и Отключить() (строка 185), но это прямое свойство инструмента, а не производное от MeterConfig.enabled. Связь Meter.enabled → Instrument.Enabled отсутствует как спецификационный механизм. |
| 4 | MUST | ❌ not_found | The changes MUST be eventually visible. | - | Нет механизма динамического обновления конфигурации MeterConfig. MeterConfigurator не реализован, поэтому требование eventual visibility изменений неприменимо в текущей архитектуре - но сама причина в отсутствии MeterConfig. |

#### Instrument enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | The synchronous instrument Enabled MUST return false when either: the MeterConfig of the Meter used to create the instrument has parameter enabled=false, or all resolved views for the instrument are configured with the Drop Aggregation. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:179` | Enabled() method exists and returns an AtomicBoolean value (line 179-181). Instruments can be disabled via Отключить() (line 185-187), which is called when the provider is closed (ОтелМетр.os:379-386). However, there is no MeterConfig with enabled=false parameter, and there is no logic to check if all resolved views use Drop Aggregation. The Enabled flag is only toggled by explicit Отключить() calls on provider shutdown. |
| 2 | SHOULD | ✅ found | Otherwise, it SHOULD return true. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:219` |  |

#### MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | To construct a MetricReader when setting up an SDK, at least the exporter to use, which is a MetricExporter instance, SHOULD be provided. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:208` |  |
| 2 | SHOULD | ⚠️ partial | The default output aggregation (optional), a function of instrument kind, SHOULD be obtained from the exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:208` | Читатель не запрашивает агрегацию у экспортера. Агрегация задается на уровне MeterProvider/View, а не читателя. |
| 3 | SHOULD | ⚠️ partial | If not configured, the default aggregation SHOULD be used. | `src/Метрики/Модули/ОтелАгрегация.os:9` | Дефолтная агрегация существует (ОтелАгрегация.ПоУмолчанию()), но она не интегрирована через MetricReader - она применяется на уровне инструментов. |
| 4 | SHOULD | ⚠️ partial | The output temporality (optional), a function of instrument kind, SHOULD be obtained from the exporter. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:62` | Экспортер имеет СелекторВременнойАгрегации, но MetricReader не запрашивает его и не использует для конвертации. Селектор используется только при формировании OTLP данных в экспортере. |
| 5 | SHOULD | ⚠️ partial | If not configured, the Cumulative temporality SHOULD be used. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:65` | Дефолт Cumulative есть в конструкторе экспортера (ОтелСелекторВременнойАгрегации.ВсегдаКумулятивная()), но это в экспортере, а не в читателе. |
| 6 | SHOULD | ✅ found | The default aggregation cardinality limit (optional) to use, a function of instrument kind. If not configured, a default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелМетр.os:412` |  |
| 7 | SHOULD | ❌ not_found | A MetricReader SHOULD provide the MetricFilter to the SDK or registered MetricProducer(s) when calling the Produce operation. | - | Нет реализации MetricFilter. Нет реализации MetricProducer. Нет метода Produce. |
| 8 | SHOULD | ✅ found | A common implementation of MetricReader, the periodic exporting MetricReader SHOULD be provided to be used typically with push-based metrics collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:1` |  |
| 9 | MUST | ⚠️ partial | The MetricReader MUST ensure that data points from OpenTelemetry instruments are output in the configured aggregation temporality for each instrument kind. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:62` | Временная агрегация поддерживается на уровне экспортера (СелекторВременнойАгрегации), но MetricReader не выполняет конвертацию Delta<->Cumulative. Нет логики конвертации между типами агрегации. |
| 10 | MUST | ❌ not_found | For synchronous instruments with Cumulative aggregation temporality, MetricReader.Collect MUST receive data points exposed in previous collections regardless of whether new measurements have been recorded. | - | Нет логики управления кумулятивной/дельта семантикой в MetricReader. Данные очищаются после каждого экспорта (ОчиститьТочкиДанных), что является Delta-поведением, не Cumulative. |
| 11 | MUST | ⚠️ partial | For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:140` | Фактически реализовано Delta-поведение - после экспорта данные очищаются (ОчиститьТочкиДанных). Но это не управляется конфигурацией temporality, а является поведением по умолчанию. |
| 12 | MUST | ⚠️ partial | For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:127` | Callback-вызовы для асинхронных инструментов выполняются при каждом сборе (ВызватьМультиОбратныеВызовы), данные собираются свежие, но управление через temporality отсутствует. |
| 13 | MUST | ❌ not_found | For instruments with Cumulative aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST repeat the same starting timestamps. | - | Нет управления StartTimeUnixNano для кумулятивной временной агрегации. Нет логики, которая бы хранила и повторяла начальный timestamp. |
| 14 | MUST | ❌ not_found | For instruments with Delta aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST advance the starting timestamp. | - | Нет управления StartTimeUnixNano для дельта временной агрегации. Нет логики продвижения начального timestamp. |
| 15 | MUST | ❌ not_found | The ending timestamp (i.e. TimeUnixNano) MUST always be equal to time the metric data point took effect, which is equal to when MetricReader.Collect was invoked. | - | Нет явной установки TimeUnixNano = время вызова Collect в MetricReader. Timestamps управляются на уровне инструментов/агрегаторов, но не централизованно при Collect. |
| 16 | MUST | ✅ found | The SDK MUST support multiple MetricReader instances to be registered on the same MeterProvider. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:97` |  |
| 17 | SHOULD NOT | ⚠️ partial | The MetricReader.Collect invocation on one MetricReader instance SHOULD NOT introduce side-effects to other MetricReader instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:112` | Реализована попытка изоляции: при нескольких читателях все кроме последнего вызывают СброситьБуферБезОчистки(). Однако вызов последнего читателя с очисткой данных влияет на все инструменты, что является side-effect для других читателей. |
| 18 | MUST NOT | ❌ not_found | The SDK MUST NOT allow a MetricReader instance to be registered on more than one MeterProvider instance. | - | Нет проверки при регистрации MetricReader, что он не зарегистрирован в другом MeterProvider. MetricReader не хранит ссылку на свой MeterProvider. |
| 19 | SHOULD | ✅ found | The SDK SHOULD provide a way to allow MetricReader to respond to MeterProvider.ForceFlush and MeterProvider.Shutdown. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:112` |  |

#### Produce batch

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#produce-batch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ❌ not_found | Produce MUST return a batch of Metric Points, filtered by the optional metricFilter parameter. | - | No Produce method exists as a separate MetricProducer interface. The MetricReader classes collect data internally but do not expose a Produce method with metricFilter parameter. |
| 2 | SHOULD | ❌ not_found | Implementation SHOULD use the filter as early as possible to gain as much performance gain possible (memory allocation, internal metric fetching, etc). | - | No MetricFilter or metricFilter parameter is implemented. No filtering mechanism exists in the collection pipeline. |
| 3 | SHOULD | ❌ not_found | If the batch of Metric Points includes resource information, Produce SHOULD require a resource as a parameter. | - | No Produce method exists. Resource is passed indirectly through Meter objects, not as a Produce parameter. |
| 4 | SHOULD | ❌ not_found | Produce SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | - | No Produce method exists. The internal collection in MetricReader does not return success/failure status to the caller - errors are logged but not propagated. |
| 5 | SHOULD | ❌ not_found | If a batch of Metric Points can include InstrumentationScope information, Produce SHOULD include a single InstrumentationScope which identifies the MetricProducer. | - | No Produce method or MetricProducer exists. InstrumentationScope is included per-instrument via Meter, not per-MetricProducer. |

### Env Vars

#### Prometheus Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#prometheus-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD NOT | ✅ found | "logging": Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations (OTEL_TRACES_EXPORTER). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:177-178` |  |
| 2 | SHOULD NOT | ✅ found | "logging": Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations (OTEL_METRICS_EXPORTER). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:291-292` |  |
| 3 | SHOULD NOT | ✅ found | "logging": Standard Output. It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new implementations (OTEL_LOGS_EXPORTER). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:255-256` |  |
| 4 | MUST | ➖ n_a | OTEL_EXPORTER_PROMETHEUS_HOST and OTEL_EXPORTER_PROMETHEUS_PORT environment variables for Prometheus exporter configuration. | - | Prometheus Exporter реализован как pull-based reader (ОтелПрометеусЧитательМетрик), но не использует собственный HTTP-сервер - метрики экспортируются через внешний HTTP-handler. Переменные OTEL_EXPORTER_PROMETHEUS_HOST/PORT не применимы, так как Prometheus exporter не управляет собственным слушателем. Scope: conditional:Prometheus Exporter (extension) - конфигурация хоста/порта не реализована. |

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
| Нет нативного protobuf | HTTP/JSON вместо HTTP/protobuf | Полная поддержка через JSON-сериализацию |
| Нет gRPC | Только HTTP транспорт | HTTP/JSON как основной протокол |
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

