# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             784    744   -40 ⚠️  РЕГРЕССИЯ
  partial            21     37 +   16
  not_found          14     23 +    9 ⚠️  РЕГРЕССИЯ
  n_a                21     36 +   15
  Всего             840    840 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (53) - требует перепроверки:

     [Logs Api / Emit a LogRecord]
       found → n_a
       Текст: When only explicit Context is supported, this parameter SHOULD be required.
       Расположение: src/Логирование/Классы/ОтелЛоггер.os:112 → -
       Пояснение: Реализация поддерживает implicit Context (ОтелКонтекст.Текущий() при Контекст=Неопределено в ОтелЛоггер.Записать), поэтому требование к режиму "only e
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Batching processor]
       found → partial
       Текст: The processor MUST synchronize calls to LogRecordExporter's Export to make sure that they are not in
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:222 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:213
       Пояснение: Извлечение элементов из буфера выполняется под БлокировкаРесурса, но сам вызов Экспортер.Экспортировать намеренно вне блокировки (комментарий в коде, 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Concurrency requirements]
       found → partial
       Текст: LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:13 → src/Логирование/Классы/ОтелПровайдерЛогирования.os:61
       Пояснение: ForceFlush и Shutdown защищены БлокировкаПроцессоров и АтомарноеБулево Закрыт; однако создание логгеров (ПолучитьЛоггер) использует кэш Логгеры (Соотв
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ForceFlush]
       found → n_a
       Текст: ForceFlush SHOULD only be called in cases where it is absolutely necessary, such as when using some 
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:192 → -
       Пояснение: Это рекомендация для вызывающей стороны (caller), а не требование к реализации LogRecordExporter. SDK не может ограничивать когда пользователь вызывае
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Counter creation]
       found → n_a
       Текст: There MUST NOT be any API for creating a `Counter` other than with a `Meter`.
       Расположение: src/Метрики/Классы/ОтелМетр.os:59 → src/Метрики/Классы/ОтелСчетчик.os:60
       Пояснение: OneScript не поддерживает приватные/internal-конструкторы: ПриСозданииОбъекта всегда публичен. Каноничный путь создания — Meter.СоздатьСчетчик(); прям
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Get a Meter]
       found → partial
       Текст: Therefore, this API MUST be structured to accept a variable number of attributes, including none.
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:77 → src/Метрики/Классы/ОтелПровайдерМетрик.os:76
       Пояснение: Параметр АтрибутыОбласти принимает один объект ОтелАтрибуты (или Неопределено), а не переменное число атрибутов. Атрибуты передаются как коллекция, а 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Instrument unit]
       found → partial
       Текст: It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII string.
       Расположение: src/Метрики/Классы/ОтелМетр.os:62 → src/Метрики/Классы/ОтелМетр.os:842
       Пояснение: Case-sensitivity обеспечивается платформой: оператор `=` в OneScript для строк регистрозависим, поэтому 'kb' и 'kB' различаются автоматически. Однако 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API SHOULD NOT validate the `name`; that is left to implementations of the API, like the SDK.
       Расположение: src/Метрики/Классы/ОтелМетр.os:775 → src/Метрики/Классы/ОтелМетр.os:863
       Пояснение: API и SDK объединены в одном пакете. ВалидироватьИмяИнструмента вызывается на API-точке входа СоздатьСчетчик, но это SDK-уровневая мягкая проверка (то
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API SHOULD NOT validate the `name`, that is left to implementations of the API.
       Расположение: src/Метрики/Классы/ОтелМетр.os:775 → src/Метрики/Классы/ОтелМетр.os:863
       Пояснение: ВалидироватьИмяИнструмента вызывается и для async-методов СоздатьНаблюдаемый*. SDK-уровневая мягкая проверка (warning, инструмент всё равно создаётся)
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → n_a
       Текст: MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:100 → -
       Пояснение: OneScript - однопоточная среда (концепция параллельного исполнения отсутствует, ФоновоеЗадание имеет ограниченные возможности). Раздел Concurrency req
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → n_a
       Текст: ExemplarReservoir - all methods MUST be safe to be called concurrently.
       Расположение: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:62 → -
       Пояснение: OneScript однопоточен; пред-условие "For languages which support concurrent execution" не выполняется. Реализации ОтелРезервуарЭкземпляров/ОтелВыровне
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → n_a
       Текст: MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:314 → -
       Пояснение: OneScript не поддерживает параллельное исполнение. Методы Собрать/СброситьБуфер/Закрыть в ОтелПериодическийЧитательМетрик и ОтелПрометеусЧитательМетри
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → n_a
       Текст: MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:264 → -
       Пояснение: OneScript - однопоточная среда; пред-условие раздела не выполняется. Методы СброситьБуфер/Закрыть у экспортёров метрик существуют и однопоточно безопа
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD collect metrics, split into batches if necessary, call `Export(batch)` on each b
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:190 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:179
       Пояснение: ПринудительноВыгрузитьСРезультатом вызывает СброситьБуфер (Collect+Export) и затем ВызватьФорсФлашЭкспортера, но разбиение на батчи не реализовано (ma
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument selection criteria]
       found → partial
       Текст: If the SDK does not support wildcards in general, it MUST still recognize the special single asteris
       Расположение: src/Метрики/Классы/ОтелСелекторИнструментов.os:37 → src/Метрики/Классы/ОтелСелекторИнструментов.os:38
       Пояснение: Only special asterisk (*) is supported for matching all instruments. General wildcard patterns (?, *) are not implemented.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MeterConfig]
       found → partial
       Текст: The value of `enabled` MUST be used to resolve whether an instrument is Enabled.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:271 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:275
       Пояснение: Функция Включен() инструмента возвращает МетрВключен.Получить() И Включен.Получить(), то есть значение MeterConfig.enabled действительно участвует в р
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       found → partial
       Текст: Implementation SHOULD use the filter as early as possible to gain as much performance gain possible 
       Расположение: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:32 → src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:33
       Пояснение: Интерфейс ИнтерфейсПродюсерМетрик принимает параметр ФильтрМетрик и документирует его передачу, но реализация по умолчанию (Возврат Новый ОтелРезульта
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       partial → not_found
       Текст: If the batch of Metric Points includes resource information, `Produce` SHOULD require a resource as 
       Расположение: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:32 → -
       Пояснение: Сигнатура Произвести(ФильтрМетрик = Неопределено) не принимает параметр Ресурс; в интерфейсе ресурс не передаётся.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       found → partial
       Текст: `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`.
       Расположение: src/Метрики/Классы/ОтелДанныеМетрики.os:42 → src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:33
       Пояснение: Интерфейс не запрещает включение InstrumentationScope (ОтелДанныеМетрики имеет область инструментирования), но интерфейс/документация не требует от ре
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → not_found
       Текст: In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector tha
       Расположение: src/Метрики/Классы/ОтелМетр.os:1115 → -
       Пояснение: No validation to ensure selector matches at most one instrument when name is provided. MeterProvider doesn't check for name conflicts during View regi
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: If the user does not provide any value, the SDK SHOULD use the `Attributes` advisory parameter confi
       Расположение: src/Метрики/Классы/ОтелМетр.os:856 → -
       Пояснение: Attributes advisory parameter is not implemented in OneScript SDK. All attributes are kept by default when no filter is provided.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / User Agent]
       found → n_a
       Текст: The resulting User-Agent SHOULD include the exporter's default User-Agent string.
       Расположение: src/Экспорт/Классы/ОтелHttpТранспорт.os:200 → -
       Пояснение: Условное требование: применимо только если экспортер реализует MAY-фичу — конфигурационную опцию для добавления product identifier к User-Agent. Эта о
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Extract]
       found → not_found
       Текст: MUST attempt to extract B3 encoded using single and multi-header formats.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1133 → -
       Пояснение: B3 пропагатор не реализован: в src/Пропагация/Классы есть только W3C TraceContext, W3C Baggage, Composite и Noop пропагаторы.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Extract]
       found → not_found
       Текст: MUST preserve a debug trace flag, if received, and propagate it with subsequent requests.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1133 → -
       Пояснение: B3 пропагатор не реализован, обработка debug-флага B3 отсутствует.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Extract]
       found → not_found
       Текст: Additionally, an OpenTelemetry implementation MUST set the sampled trace flag when the debug flag is
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1133 → -
       Пояснение: B3 пропагатор не реализован, логика установки sampled при debug отсутствует.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Extract]
       found → not_found
       Текст: MUST NOT reuse `X-B3-SpanId` as the ID for the server-side span.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1133 → -
       Пояснение: B3 пропагатор не реализован, логика обработки заголовка X-B3-SpanId отсутствует.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Inject]
       found → not_found
       Текст: MUST default to injecting B3 using the single-header format
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1136 → -
       Пояснение: B3 пропагатор не реализован: в src/Пропагация/Классы отсутствует класс B3-пропагатора и логика инжекта single-header.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Inject]
       found → not_found
       Текст: MUST provide configuration to change the default injection format to B3 multi-header
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1136 → -
       Пояснение: B3 пропагатор не реализован, конфигурация переключения формата (single/multi-header) отсутствует.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Inject]
       found → not_found
       Текст: MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support reusing the same ID for bot
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1133 → -
       Пояснение: B3 пропагатор не реализован, логика инжекта B3-заголовков отсутствует.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Fields]
       found → not_found
       Текст: Fields MUST return the header names that correspond to the configured format, i.e., the headers used
       Расположение: src/Пропагация/Классы/ОтелW3CПропагатор.os:144 → -
       Пояснение: Требование относится к B3 пропагатору (раздел B3 Requirements/Fields). B3 пропагатор не реализован, поэтому метод Поля() для B3 отсутствует. Метод Пол
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Global Propagators]
       found → n_a
       Текст: Instrumentation libraries SHOULD call propagators to extract and inject the context on all remote ca
       Расположение: src/Ядро/Модули/ОтелГлобальный.os:128 → -
       Пояснение: Требование адресовано Instrumentation Libraries (политика их поведения); данный пакет реализует только API+SDK, IL не включены.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Propagators Distribution]
       found → partial
       Текст: The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST 
       Пояснение: В составе пакета поддерживаются W3C TraceContext (ОтелW3CПропагатор) и W3C Baggage (ОтелW3CBaggageПропагатор), но пропагатор B3 из обязательного списк
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Propagators Distribution]
       found → partial
       Текст: The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST 
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1133 → src/Пропагация/Классы/ОтелW3CПропагатор.os:1
       Пояснение: W3C TraceContext и W3C Baggage распространяются как часть API/SDK (см. src/Пропагация/Классы), однако B3 пропагатор отсутствует, поэтому полный официа
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Propagators Distribution]
       found → n_a
       Текст: It MUST NOT use `OpenTracing` in the resulting propagator name as it is not widely adopted format in
       Расположение: src/Пропагация/Классы/ → -
       Пояснение: Требование адресовано реализациям OT Trace propagator (deprecated). В данном пакете OT Trace propagator не реализован, поэтому требование к именованию
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Setter argument]
       found → partial
       Текст: The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-t
       Пояснение: Установить() безусловно приводит ключ к нижнему регистру через НРег(Ключ) (HTTP/2-конвенция), нарушая требование SHOULD не трансформировать Content-Ty
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Setter argument]
       found → partial
       Текст: The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-t
       Пояснение: Сеттер не различает протокол - всегда применяет НРег(Ключ); для case-sensitive протоколов casing не сохраняется. Реализация работает только для case-i
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Detecting resource information from the environment]
       found → partial
       Текст: If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be a
       Расположение: src/Ядро/Классы/ОтелРесурс.os:43 → src/Ядро/Классы/ОтелРесурс.os:46
       Пояснение: Конфликт Schema URL логируется как Предупреждение (warning), не как ошибка; результирующий ресурс получает пустой Schema URL вместо того чтобы считать
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / End]
       found → n_a
       Текст: However, all API implementations of such methods MUST internally call the `End` method and be docume
       Расположение: src/Трассировка/Классы/ОтелСпан.os:508 → -
       Пояснение: В OneScript нет языковых конструкций вроде Python with-statement, требующих альтернативных End-методов; единственный метод завершения — Завершить().
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span]
       found → n_a
       Текст: The span name SHOULD be the most general string that identifies a (statistically) interesting class 
       Расположение: src/Трассировка/Классы/ОтелПостроительСпана.os:193 → -
       Пояснение: Требование адресовано Instrumentation Libraries (политика именования спанов вызывающим кодом); данный пакет реализует только API+SDK, IL не включены.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span]
       found → n_a
       Текст: Generality SHOULD be prioritized over human-readability.
       Расположение: src/Трассировка/Классы/ОтелПостроительСпана.os:193 → -
       Пояснение: Требование адресовано Instrumentation Libraries (политика именования спанов вызывающим кодом); данный пакет реализует только API+SDK, IL не включены.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span]
       found → n_a
       Текст: All Spans MUST be created via a Tracer.
       Расположение: src/Трассировка/Классы/ОтелТрассировщик.os:68 → -
       Пояснение: OneScript не поддерживает приватные конструкторы; Tracer (ОтелТрассировщик) - единственный задокументированный способ создания Span, но язык не позвол
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / SpanKind]
       found → n_a
       Текст: In order for `SpanKind` to be meaningful, callers SHOULD arrange that a single Span does not serve m
       Расположение: src/Трассировка/Модули/ОтелВидСпана.os:1 → -
       Пояснение: Требование адресовано вызывающим коду (callers/Instrumentation Libraries) — это политика их поведения; данный пакет реализует только API+SDK, IL не вк
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / SpanKind]
       found → n_a
       Текст: For example, a server-side span SHOULD NOT be used to describe outgoing remote procedure call.
       Расположение: src/Трассировка/Модули/ОтелВидСпана.os:1 → -
       Пояснение: Требование адресовано вызывающим коду (callers/Instrumentation Libraries); данный пакет реализует только API+SDK и не навязывает семантику использован
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Wrapping a SpanContext in a Span]
       found → partial
       Текст: If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possib
       Расположение: src/Трассировка/Модули/ОтелСпаны.os:36 → src/Трассировка/Классы/ОтелНезаписывающийСпан.os:1; src/Трассировка/Модули/ОтелСпаны.os:36
       Пояснение: Предоставлен публичный модуль-функция ОтелСпаны.Обернуть(), как рекомендует спека, но сам класс ОтелНезаписывающийСпан также публично экспортируется в
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Wrapping a SpanContext in a Span]
       found → n_a
       Текст: This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable.
       Расположение: src/Трассировка/Классы/ОтелНезаписывающийСпан.os:1 → -
       Пояснение: OneScript не поддерживает запрет наследования/sealed-классы; контроль 'не должно быть переопределяемо' невозможно выразить средствами языка. Документи
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Batching processor]
       found → partial
       Текст: The processor MUST synchronize calls to `Span Exporter`'s `Export` to make sure that they are not in
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:222 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:213
       Пояснение: ИзвлечьЭлементыИзБуфера выполняется под Блокировкой, но сам вызов Экспортер.Экспортировать в ЭкспортироватьПакет вызывается ВНЕ блокировки (комментари
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Concurrency requirements]
       found → partial
       Текст: Span processor - all methods MUST be safe to be called concurrently.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:47 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:328
       Пояснение: ОтелПростойПроцессорСпанов использует БлокировкаРесурса и АтомарноеБулево корректно. Однако ОтелБазовыйПакетныйПроцессор хранит флаг Закрыт как обычны
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / ForceFlush()]
       found → partial
       Текст: `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using som
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:74 → src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:39
       Пояснение: Это требование к вызывающему коду (рекомендация по использованию API), а не к реализации. В документирующих комментариях метода СброситьБуфер нет явно
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / IdGenerator randomness]
       found → partial
       Текст: Custom implementations of the `IdGenerator` SHOULD identify themselves appropriately when all genera
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:364 → src/Трассировка/Классы/ОтелПровайдерТрассировки.os:386
       Пояснение: SDK поддерживает опциональный метод ФлагRandomДляНовыхИд() у пользовательского ГенераторИд (duck typing), но в OneScript нет marker-интерфейсов/наслед
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:168 → src/Трассировка/Классы/ОтелПровайдерТрассировки.os:165
       Пояснение: Закрыть(ТаймаутМс) принимает таймаут и прерывает цикл между итерациями процессоров (ИстекТаймаут → возврат ОтелРезультатыЗакрытия.Таймаут()), однако в
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / TraceIdRatioBased]
       found → partial
       Текст: The precision of the number SHOULD follow implementation language standards and SHOULD be high enoug
       Пояснение: Точность жёстко задана как ЧДЦ=6 (6 знаков после запятой) в Формат(); это не вытекает из «language standards» OneScript (Decimal поддерживает 28 знача
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / `ForceFlush()`]
       found → partial
       Текст: `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using som
       Расположение: src/Экспорт/Классы/ОтелЭкспортерСпанов.os:63 → src/Экспорт/Классы/ОтелЭкспортерСпанов.os:54
       Пояснение: Это рекомендация по использованию для вызывающего, SDK не может её обеспечить программно. В документирующем комментарии СброситьБуфер не указано, что 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / `ForceFlush()`]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Расположение: src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:26 → src/Экспорт/Классы/ОтелЭкспортерСпанов.os:63
       Пояснение: Метод СброситьБуфер принимает параметр ТаймаутМс, но игнорирует его (синхронный экспортер без буфера сразу возвращает Успех). Параметр не используется
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (15) - требует перепроверки:

     [Logs Sdk / Event to span event bridge]
       partial → found
       Текст: if the LogRecord has a Timestamp set, it MUST be used as the span event timestamp.
       Код: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:78
       Было: Используется ЗаписьЛога.Время() как timestamp события, но нет явной проверки 'если Timestamp установ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Event to span event bridge]
       not_found → found
       Текст: Otherwise, if the LogRecord has an ObservedTimestamp set, it MUST be used as the span event timestam
       Код: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:80
       Было: Fallback на ObservedTimestamp (ВремяНаблюдения) при отсутствии Time не реализован - используется тол
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:138
       Было: Таймаут передаётся в каждый Процессор.СброситьБуфер(ТаймаутМс) и агрегируется через ОтелРезультатыЭк
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелЭкспортерЛогов.os:64
       Было: СброситьБуфер принимает параметр ТаймаутМс, но не использует его - синхронный экспортёр сразу возвра
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:160
       Было: Soft-timeout: цикл по процессорам прерывается при превышении таймаута, но активный Процессор.Закрыть
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Counter operations]
       partial → found
       Текст: This API SHOULD NOT validate this value, that is left to implementations of the API.
       Код: src/Метрики/Классы/ОтелСчетчик.os:35
       Было: Метод Добавить выполняет валидацию: при отрицательном значении логирует предупреждение и игнорирует 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions SHOULD NOT take an indefinite amount of time.
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:78
       Было: Документировано требование к callback (комментарий о времени выполнения) и реализован soft-timeout ч
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       n_a → found
       Текст: Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`
       Код: src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:70
       Было: OneScript использует System.Decimal: NaN/+Inf/-Inf невозможно представить в платформе (операции брос
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: This function SHOULD be obtained from the `exporter`.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:368
       Было: Селектор агрегации по умолчанию задаётся в конструкторе MetricReader жёстко (sum, last_value, ...), 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Numerical limits handling]
       n_a → found
       Текст: If the SDK receives float/double values from Instruments, it MUST handle all the possible values.
       Код: src/Метрики/Классы/ОтелАгрегаторСуммы.os:1
       Было: OneScript использует System.Decimal вместо IEEE 754 float/double. NaN, Infinity и отрицательный ноль
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → found
       Текст: The implementation SHOULD use a timeout to prevent indefinite callback execution.
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:238
       Было: Soft-timeout через ФоновыеЗадания.ОжидатьЗавершения: SDK перестаёт ждать, но фоновое задание продолж
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       partial → found
       Текст: Cumulative timeseries MUST use a consistent start timestamp for all collection intervals.
       Код: src/Метрики/Классы/ОтелСинхронныйИнструмент.os:127
       Было: Для синхронных инструментов ВремяСтарта при cumulative не сбрасывается — консистентно. Для асинхронн
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       partial → found
       Текст: For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the
       Код: src/Метрики/Классы/ОтелСинхронныйИнструмент.os:127
       Было: ВремяСтарта инициализируется в ПриСозданииОбъекта (время создания инструмента), а не на момент перво
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Set Status]
       n_a → found
       Текст: The status code SHOULD remain unset, except for the following circumstances:
       Код: src/Трассировка/Классы/ОтелСпан.os:227
       Было: Требование адресовано Instrumentation Libraries (политика их поведения), а не API/SDK. Данный проект
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown()]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:87
       Было: Закрыть/ЗакрытьСРезультатом принимает ТаймаутМс и ЭкспортироватьВсеПакеты соблюдает его (soft-timeou
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (26) - агент нашёл дополнительные:

     [Logs Api] MUST found: For each optional parameter, the API MUST be structured to accept it, but MUST N
     [Logs Sdk] MUST NOT found: ... (i.e. it MUST NOT matter whether a `Logger` was obtained from the `LoggerPro
     [Logs Sdk] SHOULD found: ... its `name` SHOULD keep the original invalid value, ...
     [Logs Sdk] SHOULD found: ... and a message reporting that the specified value is invalid SHOULD be logged
     [Metrics Api] SHOULD found: The API SHOULD treat it as an opaque string.
     [Metrics Api] MUST found: The Meter MUST provide functions to create new Instruments:
     [Metrics Api] SHOULD found: The API to register a new Callback SHOULD accept:
     [Metrics Sdk] MUST found: This extension MUST be configurable on a metric View,
     [Metrics Sdk] MUST partial: The "offer" method MAY accept a filtered subset of `Attributes` which diverge fr
     [Metrics Sdk] MUST found: Implementations are REQUIRED to accept the entire normal range of IEEE floating 
     [Metrics Sdk] MUST found: If a `View` is registered to a `MeterProvider` and an Instrument is registered t
     [Metrics Sdk] MUST found: If a `View` matches an Instrument, MUST support the `attribute_keys` field as an
     [Metrics Sdk] SHOULD found: The `View`s applying to an Instrument SHOULD be applied in the order they were r
     [Metrics Sdk] SHOULD found: The `View` SHOULD NOT be used to filter attributes in case where its `attribute_
     [Metrics Sdk] SHOULD found: The Instrument `unit` SHOULD be used if it is not overridden by a `View`.
     [Metrics Sdk] SHOULD found: The Instrument `description` SHOULD be used if it is not overridden by a `View`.
     [Metrics Sdk] SHOULD partial: The default output `aggregation` (optional), a function of instrument kind. This
     [Metrics Sdk] SHOULD partial: SDKs SHOULD return a valid no-op Meter for these calls, if possible.
     [Metrics Sdk] SHOULD found: For asynchronous instrument, the start timestamp SHOULD be:
     [Otlp Exporter] SHOULD n_a: [2]: The environment variables `OTEL_EXPORTER_OTLP_SPAN_INSECURE` and `OTEL_EXPO
     ... и ещё 6

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (26) - были раньше, теперь нет:

     [Logs Api] MUST NOT found: For each optional parameter, the API MUST be structured to accept it, but MUST N
     [Logs Sdk] MUST NOT found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Logs Sdk] SHOULD found: In the case where an invalid `name` (null or empty string) is specified, a worki
     [Logs Sdk] SHOULD found: In the case where an invalid `name` (null or empty string) is specified, a worki
     [Metrics Api] SHOULD found: The `unit` is an optional string provided by the author of the Instrument. The A
     [Metrics Api] MUST found: The `Meter` MUST provide functions to create new Instruments: Create a new Count
     [Metrics Api] SHOULD found: The API to register a new Callback SHOULD accept: A `callback` function. A list 
     [Metrics Sdk] MUST found: This extension MUST be configurable on a metric View, although individual reserv
     [Metrics Sdk] MUST found: This MUST be clearly documented in the API and the reservoir MUST be given the `
     [Metrics Sdk] MUST found: The implementation MUST maintain reasonable minimum and maximum scale parameters
     [Metrics Sdk] SHOULD found: The SDK SHOULD use the following logic to determine how to process Measurements 
     [Metrics Sdk] MUST found: Instrument advisory parameters, if any, MUST be honored.
     [Metrics Sdk] SHOULD found: If applying the View results in conflicting metric identities the implementation
     [Metrics Sdk] SHOULD found: If it is not possible to apply the View without producing semantic errors (e.g. 
     [Metrics Sdk] MUST found: If both a View and Instrument advisory parameters specify the same aspect of the
     [Metrics Sdk] SHOULD found: If the Instrument could not match with any of the registered `View`(s), the SDK 
     [Metrics Sdk] SHOULD found: This function SHOULD be obtained from the `exporter`.
     [Metrics Sdk] SHOULD found: After the call to `Shutdown`, subsequent attempts to get a `Meter` are not allow
     [Metrics Sdk] SHOULD partial: For asynchronous instrument, the start timestamp SHOULD be: - The creation time 
     [Otlp Exporter] SHOULD found: However, if they are already implemented, they SHOULD continue to be supported a
     ... и ещё 6

  Итого изменений: 120
    Понижений: 53, Повышений: 15, Боковых: 0
    Новых req: 26, Пропущенных req: 26
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
