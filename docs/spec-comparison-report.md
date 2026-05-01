# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             755    772 +   17 ✅
  partial            43     34    -9
  not_found          28     15   -13
  n_a                14     19 +    5
  Всего             840    840 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (29) - требует перепроверки:

     [Logs Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Пояснение: Таймаут передаётся в каждый Процессор.СброситьБуфер(ТаймаутМс) и агрегируется через ОтелРезультатыЭкспорта.ОжидатьВсе(...,ТаймаутМс), но это soft-time
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Пояснение: СброситьБуфер принимает параметр ТаймаутМс, но не использует его - синхронный экспортёр сразу возвращает Успех; для пакетных процессоров (ОтелПровайде
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:167 → src/Логирование/Классы/ОтелПровайдерЛогирования.os:165
       Пояснение: Soft-timeout: цикл по процессорам прерывается при превышении таймаута, но активный Процессор.Закрыть() не прерывается жёстко. OneScript ФоновоеЗадание
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Counter operations]
       found → partial
       Текст: This API SHOULD NOT validate this value, that is left to implementations of the API.
       Пояснение: Метод Добавить выполняет валидацию: при отрицательном значении логирует предупреждение и игнорирует измерение (`Если Значение < 0 Тогда ... Возврат`).
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API SHOULD NOT validate `advisory` parameters.
       Расположение: src/Метрики/Классы/ОтелМетр.os:1026 → src/Метрики/Классы/ОтелМетр.os:1072
       Пояснение: ПроверитьСовет проверяет тип Совета (Структура) и тип значений ГраницыГистограммы/КлючиАтрибутов (Массив), логируя предупреждения. Это лёгкая структур
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API SHOULD NOT validate `advisory` parameters.
       Расположение: src/Метрики/Классы/ОтелМетр.os:1026 → src/Метрики/Классы/ОтелМетр.os:1072
       Пояснение: ПроверитьСовет проверяет тип Совета и тип внутренних полей advisory, логируя предупреждения. Лёгкая валидация advisory нарушает SHOULD NOT validate, х
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Callback functions SHOULD NOT take an indefinite amount of time.
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:75 → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:336
       Пояснение: Документировано требование к callback (комментарий о времени выполнения) и реализован soft-timeout через ВыполнитьCallbackСУчётомТаймаута + ОжидатьЗав
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API SHOULD provide some way to pass `state` to the callback.
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:264 → -
       Пояснение: Отдельный параметр state для callback не предусмотрен. Передача состояния возможна только через лексические замыкания (closure capture) Действий OneSc
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ExemplarReservoir]
       found → partial
       Текст: The "offer" method SHOULD accept measurements, including: The `value` of the measurement, the comple
       Расположение: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:42-49 → src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:46
       Пояснение: Предложить принимает Значение, АтрибутыИзмерения и КонтекстСпана, но отдельный параметр timestamp не принимается (генерируется внутри СоздатьЭкземпляр
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       found → partial
       Текст: Arithmetic sum of `Measurement` values in population. This SHOULD NOT be collected when used with in
       Расположение: src/Метрики/Классы/ОтелАгрегаторГистограммы.os:59 → src/Метрики/Классы/ОтелАгрегаторГистограммы.os:42
       Пояснение: Sum накапливается всегда без условия пропуска при отрицательных измерениях. Гистограмма обычно не используется с UpDownCounter/ObservableGauge, но явн
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       found → partial
       Текст: When the histogram contains not more than one value in either of the positive or negative ranges, th
       Пояснение: Шкала инициализируется НачальнаяШкала=20 (макс) и понижается при необходимости — для одиночного значения используется max scale. Однако нет явного пер
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument advisory parameters]
       found → partial
       Текст: If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed
       Расположение: src/Метрики/Классы/ОтелМетр.os:1032 → src/Метрики/Классы/ОтелМетр.os:1078
       Пояснение: ПроверитьСовет логирует предупреждение при невалидной структуре/типе, но не сбрасывает Совет в Неопределено - последующая логика всё равно может попыт
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter Creation]
       found → n_a
       Текст: It SHOULD only be possible to create `Meter` instances through a `MeterProvider` (see API).
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:74 → src/Метрики/Классы/ОтелМетр.os:733
       Пояснение: OneScript не поддерживает приватные/internal конструкторы (ПриСозданииОбъекта всегда публичен). Meter создаётся через ОтелПровайдерМетрик.ПолучитьМетр
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MeterConfig]
       found → partial
       Текст: If a `Meter` is disabled, it MUST behave equivalently to No-op Meter.
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:369 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:93
       Пояснение: Записать() в синхронных инструментах short-circuit-ит только по локальному флагу Включен (instrument-level), но не проверяет МетрВключен (meter-level)
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Numerical limits handling]
       found → n_a
       Текст: If the SDK receives float/double values from Instruments, it MUST handle all the possible values.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:98 → -
       Пояснение: OneScript использует System.Decimal вместо IEEE 754 float/double. NaN, Infinity и отрицательный ноль невозможны на уровне платформы — арифметические о
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Specify Protocol]
       found → partial
       Текст: SDKs SHOULD support both grpc and http/protobuf transports and MUST support at least one of them.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:639-654 → src/Экспорт/Классы/ОтелHttpТранспорт.os:199
       Пояснение: grpc-транспорт реализован полностью (ОтелGrpcТранспорт). HTTP-транспорт принимает значение протокола 'http/protobuf', но фактически отправляет данные 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Specify Protocol]
       found → partial
       Текст: If no configuration is provided the default transport SHOULD be http/protobuf unless SDKs have good 
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:644 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:234
       Пояснение: Дефолтное значение протокола = 'http/protobuf' (строка), но HTTP-транспорт всегда отправляет JSON (Content-Type: application/json), т.е. фактический w
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Detecting resource information from the environment]
       found → partial
       Текст: Note the failure to detect any resource information MUST NOT be considered an error, whereas an erro
       Пояснение: Ошибки при детектировании логируются на уровне Предупреждение, а не Ошибка - спека требует считать это ошибкой.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → partial
       Текст: The status code SHOULD remain unset, except for the following circumstances:
       Расположение: src/Трассировка/Классы/ОтелСпан.os:467 → src/Трассировка/Классы/ОтелСпан.os:474
       Пояснение: Это требование к Instrumentation Libraries (политическое поведение пользовательского кода), а не к API. SDK обеспечивает дефолт Unset (НЕ устанавливае
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → not_found
       Текст: An attempt to set value Unset SHOULD be ignored.
       Расположение: src/Трассировка/Классы/ОтелСпан.os:478 → -
       Пояснение: В УстановитьСтатус нет проверки на Unset: вызов с Значение=ОтелКодСтатуса.НеУстановлен() допускается и при текущем КодСтатуса=НеУстановлен фактически 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → n_a
       Текст: When the status is set to Error by Instrumentation Libraries, the Description SHOULD be documented a
       Расположение: src/Трассировка/Классы/ОтелСпан.os:456 → -
       Пояснение: Это требование к авторам Instrumentation Libraries (документировать Description), а не к SDK. Проверяется в самих библиотеках инструментирования, а не
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → n_a
       Текст: For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish the
       Расположение: src/Трассировка/Классы/ОтелСпан.os:467 → -
       Пояснение: Это требование к Instrumentation Libraries (политика публикации конвенций), а не к коду SDK.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → n_a
       Текст: Generally, Instrumentation Libraries SHOULD NOT set the status code to Ok, unless explicitly configu
       Расположение: src/Трассировка/Классы/ОтелСпан.os:467 → -
       Пояснение: Это требование к авторам Instrumentation Libraries (не вызывать УстановитьСтатус(Ok) без явной конфигурации), а не к SDK. SDK предоставляет API, огран
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → n_a
       Текст: Instrumentation Libraries SHOULD leave the status code as Unset unless there is an error, as describ
       Расположение: src/Трассировка/Классы/ОтелСпан.os:467 → -
       Пояснение: Это требование к Instrumentation Libraries (политика их поведения), а не к коду SDK.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → n_a
       Текст: Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generat
       Пояснение: Требование к Analysis tools (бэкендам/UI анализа трейсов), а не к SDK инструментирования. Вне области ответственности кода данного проекта.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span]
       partial → n_a
       Текст: To prevent misuse, implementations SHOULD NOT provide access to a `Span`'s attributes besides its `S
       Расположение: src/Трассировка/Классы/ОтелСпан.os:150 → src/Трассировка/Классы/ОтелСпан.os:6
       Пояснение: OneScript не поддерживает internal/package-private модификаторы; SDK-геттеры (Атрибуты(), События(), Линки() и т.п.) обязаны быть Экспорт, иначе проце
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / OnEnding]
       found → partial
       Текст: The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking `
       Расположение: src/Трассировка/Классы/ОтелСпан.os:501 → src/Трассировка/Классы/ОтелСпан.os:508
       Пояснение: Завершить() вызывает ПередЗавершением синхронно, но в ОтелСпан нет явной блокировки/lock-а, защищающего от модификации спана из других ФоновыеЗадания 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Shutdown()]
       found → partial
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:96 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:103
       Пояснение: Закрыть/ЗакрытьСРезультатом принимает ТаймаутМс и ЭкспортироватьВсеПакеты соблюдает его (soft-timeout); однако OneScript не поддерживает hard-cancel Ф
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Tracer Creation]
       found → n_a
       Текст: It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` (see API).
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:69 → src/Трассировка/Классы/ОтелТрассировщик.os:312
       Пояснение: OneScript не поддерживает приватные/internal конструкторы — ПриСозданииОбъекта всегда публичен. Документированный путь создания — ОтелПровайдерТрассир
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (49) - требует перепроверки:

     [Env Vars / Boolean]
       partial → found
       Текст: Any value not explicitly defined here as a true value, including unset and empty values, MUST be int
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1010
       Было: БезопасноеБулево возвращает значение по умолчанию (Умолчание), а не жёстко false, при невалидном зна
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Declarative configuration]
       partial → found
       Текст: When `OTEL_CONFIG_FILE` is set, all other environment variables besides those referenced in the conf
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:99
       Было: Когда OTEL_CONFIG_FILE задана, выполняется ОтелФайловаяКонфигурация.Разобрать + ОтелКонфигурационная
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Enum]
       partial → found
       Текст: For sources accepting an enum value, if the user provides a value the implementation does not recogn
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:332
       Было: Предупреждение для нераспознанных значений выводится для otel.traces.sampler (стр. 320) и otel.propa
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / General SDK Configuration]
       partial → found
       Текст: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation 
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:947
       Было: БезопасноеЧисло логирует и применяет значение по умолчанию (1.0) при невалидном otel.traces.sampler.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / General SDK Configuration]
       partial → found
       Текст: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation 
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:949
       Было: Невалидный otel.traces.sampler.arg для traceidratio/parentbased_traceidratio логируется и заменяется
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / General SDK Configuration]
       partial → found
       Текст: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation 
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:983
       Было: БезопасноеЧисло возвращает значение по умолчанию (1.0) при невалидном arg, что соответствует «as if 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Numeric]
       n_a → found
       Текст: The following paragraph was added after stabilization and the requirements are thus qualified as "SH
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:943
       Было: Мета-требование о статусе требований в спецификации (квалификация SHOULD vs MUST), а не функциональн
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Api / Emit a LogRecord]
       n_a → found
       Текст: When only explicit Context is supported, this parameter SHOULD be required.
       Код: src/Логирование/Классы/ОтелЛоггер.os:112
       Было: Условная альтернатива: применима, только если SDK поддерживает исключительно explicit Context. ОтелЛ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Api / Enabled]
       partial → found
       Текст: The API SHOULD be documented that instrumentation authors needs to call this API each time they emit
       Код: src/Логирование/Классы/ОтелЛоггер.os:36
       Было: Документирующий комментарий описывает назначение Включен() как hot-path оптимизацию и упоминает, что
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Built-in processors]
       partial → found
       Текст: Additional processors defined in this document SHOULD be provided by SDK packages.
       Код: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:1
       Было: Реализованы Simple и Batch процессоры, но дополнительный процессор Event-to-span event bridge (опред
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Event to span event bridge]
       not_found → found
       Текст: This processor SHOULD be provided by SDK.
       Код: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:1
       Было: Процессор Event-to-span event bridge не реализован: в src/Логирование/Классы/ нет соответствующего к
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Event to span event bridge]
       not_found → partial
       Текст: The processor MUST bridge a LogRecord to a span event if and only if all of the following conditions
       Код: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:44
       Было: Процессор Event-to-span event bridge не реализован.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Event to span event bridge]
       not_found → partial
       Текст: If any of these conditions is not met, the processor MUST do nothing.
       Код: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:54
       Было: Процессор Event-to-span event bridge не реализован.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Event to span event bridge]
       not_found → found
       Текст: When a LogRecord is bridged, the processor MUST add exactly one span event with the following mappin
       Код: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:74
       Было: Процессор Event-to-span event bridge не реализован.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Event to span event bridge]
       not_found → found
       Текст: the span event name MUST be the LogRecord's Event Name.
       Код: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:53
       Было: Процессор Event-to-span event bridge не реализован.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Event to span event bridge]
       not_found → partial
       Текст: if the LogRecord has a Timestamp set, it MUST be used as the span event timestamp.
       Код: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:73
       Было: Процессор Event-to-span event bridge не реализован.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Event to span event bridge]
       not_found → found
       Текст: all LogRecord Attributes MUST be copied to the span event as span event attributes.
       Код: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:72
       Было: Процессор Event-to-span event bridge не реализован.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Event to span event bridge]
       not_found → found
       Текст: Note that bridging a LogRecord to a span event MUST NOT prevent that LogRecord from continuing throu
       Код: src/Логирование/Классы/ОтелПроцессорСобытийВSpanEvents.os:1
       Было: Процессор Event-to-span event bridge не реализован.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / OnEmit]
       not_found → found
       Текст: To avoid such race conditions, implementations SHOULD recommended to users that a clone of logRecord
       Код: src/Логирование/Классы/ОтелПакетныйПроцессорЛогов.os:14
       Было: Нет ни документации (комментариев), ни рекомендаций пользователю о клонировании ЗаписьЛога для парал
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Counter creation]
       n_a → found
       Текст: There MUST NOT be any API for creating a `Counter` other than with a `Meter`.
       Код: src/Метрики/Классы/ОтелМетр.os:59
       Было: OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен), поэтому невоз
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Enabled]
       partial → found
       Текст: The API SHOULD be documented that instrumentation authors needs to call this API each time they reco
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:258
       Было: Метод Включен() имеет документирующий комментарий, но в нём не указано явно, что нужно вызывать этот
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Concurrency requirements]
       partial → found
       Текст: MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:264
       Было: ОтелЭкспортерМетрик использует АтомарноеБулево только для флага Закрыт (идемпотентный shutdown через
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       partial → found
       Текст: The emitted warning SHOULD include information for the user on how to resolve the conflict, if possi
       Код: src/Метрики/Классы/ОтелМетр.os:1194
       Было: Предупреждение содержит общую информацию о конфликте (имя, тип, единицы), но не предлагает конкретно
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       partial → found
       Текст: If the potential conflict involves multiple `description` properties, setting the `description` thro
       Код: src/Метрики/Классы/ОтелМетр.os:991
       Было: ПроверитьКонфликтДескриптора сравнивает Описание напрямую и не учитывает, что описание могло быть пе
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       partial → found
       Текст: If the potential conflict involves instruments that can be distinguished by a supported View selecto
       Код: src/Метрики/Классы/ОтелМетр.os:1194
       Было: Предупреждение не включает конкретный рецепт View для переименования инструмента; даётся только обще
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Exemplar defaults]
       partial → found
       Текст: All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`.
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:337
       Было: По умолчанию у синхронного инструмента ставится ОтелФабрикаПростыхРезервуаров(1), но не для всех вид
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarReservoir]
       partial → found
       Текст: The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars.
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:64
       Было: СоздатьЭкземпляр() аллоцирует новое Соответствие при каждом offer (включая массив filteredAttributes
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` MAY skip `Export(batch)` calls if the timeout is already expired, but SHOULD still call
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:209
       Было: При неудаче СброситьБуфер (включая таймаут) функция возвращается раньше (строки 194-199) и не вызыва
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:194
       Было: Параметр ТаймаутМс принимается и передаётся экспортёру, но в локальной операции СброситьБуфер не исп
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       n_a → partial
       Текст: Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`
       Было: OneScript Number = System.Decimal: значения +Inf, -Inf, NaN на платформе невозможны (любая попытка в
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:121
       Было: ПринудительноВыгрузитьСРезультатом принимает ТаймаутМс, но в синхронном экспортёре параметр помечен 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       partial → found
       Текст: If applying the View results in conflicting metric identities the implementation SHOULD apply the Vi
       Код: src/Метрики/Классы/ОтелМетр.os:1115
       Было: ПроверитьКонфликтИменView эмитит предупреждение и применяет View только для случая 'wide selector + 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       not_found → found
       Текст: If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asy
       Код: src/Метрики/Классы/ОтелМетр.os:1247
       Было: Нет проверки совместимости агрегации с типом инструмента: ОпределитьАгрегаторИзПредставления возвращ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricExporter]
       not_found → found
       Текст: Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsuppo
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:54
       Было: ОтелЭкспортерМетрик.Экспортировать не проверяет совместимость агрегации/темпоральности данных и не в
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricProducer]
       partial → found
       Текст: `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of pro
       Код: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:32
       Было: Интерфейс Произвести принимает ФильтрМетрик, в котором может содержаться предпочтительная темпоральн
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: If not configured, the Cumulative temporality SHOULD be used.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:379
       Было: Reader не имеет собственного хранения temporality селектора с дефолтом Cumulative; всегда обращается
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       not_found → partial
       Текст: The implementation SHOULD use a timeout to prevent indefinite callback execution.
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:336
       Было: Вызов Callback.Выполнить() в ВызватьМультиОбратныеВызовы и ВызватьCallbackИСобрать выполняется синхр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       partial → found
       Текст: `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`.
       Код: src/Метрики/Классы/ОтелДанныеМетрики.os:42
       Было: Каждый ОтелДанныеМетрики содержит ОбластьИнструментирования, но интерфейс Произвести возвращает Масс
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:153
       Было: ЗакрытьСРезультатом принимает параметр ТаймаутМс, но фактически использует ИнтервалЭкспортаМс*Множит
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       partial → found
       Текст: If the gRPC client implementation does not support an endpoint with a scheme of http or https then t
       Код: src/Экспорт/Классы/ОтелGrpcТранспорт.os:208
       Было: Endpoint передаётся в OPI_GRPC как есть. Базовая нормализация (добавление http://, если схема отсутс
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / User Agent]
       not_found → found
       Текст: The resulting User-Agent SHOULD include the exporter's default User-Agent string.
       Код: src/Экспорт/Классы/ОтелHttpТранспорт.os:200
       Было: Нет API/конфигурации для добавления product identifier к User-Agent. Поскольку MAY-фича (добавление 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Specifying resource information via an environment variable]
       partial → found
       Текст: In case of any error, e.g. failure during the decoding process, the entire environment variable valu
       Код: src/Ядро/Классы/ОтелРесурс.os:185
       Было: Парсинг OTEL_RESOURCE_ATTRIBUTES не обёрнут в Попытка/Исключение: пары без '=' молча пропускаются (э
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Specifying resource information via an environment variable]
       partial → found
       Текст: In case of any error, e.g. failure during the decoding process, the entire environment variable valu
       Код: src/Ядро/Классы/ОтелРесурс.os:181
       Было: Нет логирования ошибки декодирования OTEL_RESOURCE_ATTRIBUTES: при сбое РаскодироватьСтроку выбрасыв
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Behavior of the API in the absence of an installed SDK]
       partial → found
       Текст: If the Span in the parent Context is already non-recording, it SHOULD be returned directly without i
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:77
       Было: В функции СоздатьНоопСпанВAPIРежиме всегда создаётся новый ОтелНоопСпан с контекстом родителя - пров
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Concurrency requirements]
       partial → found
       Текст: Link - Links are immutable and SHOULD be safe for concurrent use by default.
       Код: src/Трассировка/Классы/ОтелЛинк.os:5
       Было: Линк хранится как Соответствие внутри массива Линки спана, иммутабельность гарантируется только тем,
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Wrapping a SpanContext in a Span]
       partial → found
       Текст: If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possib
       Код: src/Трассировка/Модули/ОтелСпаны.os:36
       Было: Класс ОтелНоопСпан публично экспонируется (используется в коде через 'Новый ОтелНоопСпан(...)'), а н
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Wrapping a SpanContext in a Span]
       partial → found
       Текст: If a new type is required to be publicly exposed, it SHOULD be named NonRecordingSpan.
       Код: src/Трассировка/Классы/ОтелНезаписывающийСпан.os:1
       Было: Класс назван ОтелНоопСпан (NoopSpan), а не NonRecordingSpan. Модуль-обёртка ОтелNonRecordingSpan сущ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / IdGenerator randomness]
       partial → found
       Текст: If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine wh
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:364
       Было: Для корневых спанов всегда выставляется ФлагRandom() (хардкод), без запроса к пользовательскому гене
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / IdGenerator randomness]
       partial → found
       Текст: Custom implementations of the `IdGenerator` SHOULD identify themselves appropriately when all genera
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:364
       Было: Нет marker-интерфейса/механизма для пользовательского IdGenerator идентифицировать себя как источник
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (11) - агент нашёл дополнительные:

     [Env Vars] MUST found: For new implementations, these should be treated as MUST requirements.
     [Logs Sdk] MUST NOT found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Metrics Api] MUST NOT found: Therefore, this API needs to be structured to accept a `schema_url`, but MUST NO
     [Metrics Api] SHOULD found: The `unit` is an optional string provided by the author of the Instrument. The A
     [Metrics Api] SHOULD found: The API to register a new Callback SHOULD accept: A `callback` function. A list 
     [Metrics Sdk] SHOULD found: This function SHOULD be obtained from the `exporter`.
     [Metrics Sdk] SHOULD found: After the call to `Shutdown`, subsequent attempts to get a `Meter` are not allow
     [Metrics Sdk] SHOULD partial: For asynchronous instrument, the start timestamp SHOULD be: - The creation time 
     [Trace Sdk] MUST NOT found: (i.e. it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvide
     [Trace Sdk] SHOULD found: After the call to `Shutdown`, subsequent calls to `OnStart`, `OnEnd`, or `ForceF
     [Trace Sdk] MUST found: Each processor registered on `TracerProvider` is a start of pipeline that consis

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (11) - были раньше, теперь нет:

     [Env Vars] SHOULD found: For new implementations, these should be treated as MUST requirements.
     [Logs Sdk] MUST found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Metrics Api] MUST found: Therefore, this API MUST be structured to accept a variable number of attributes
     [Metrics Api] SHOULD found: The API SHOULD treat it as an opaque string.
     [Metrics Api] SHOULD found: The API to register a new Callback SHOULD accept:
     [Metrics Sdk] SHOULD partial: The default output `aggregation` (optional), a function of instrument kind. This
     [Metrics Sdk] SHOULD found: SDKs SHOULD return some failure for these calls, if possible.
     [Metrics Sdk] SHOULD not_found: For asynchronous instrument, the start timestamp SHOULD be:
     [Trace Sdk] MUST NOT found: If configuration is updated (e.g., adding a `SpanProcessor`), the updated config
     [Trace Sdk] SHOULD found: SDKs SHOULD ignore these calls gracefully, if possible.
     [Trace Sdk] MUST found: SDK MUST allow to end each pipeline with individual exporter.

  Итого изменений: 100
    Понижений: 29, Повышений: 49, Боковых: 0
    Новых req: 11, Пропущенных req: 11
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
