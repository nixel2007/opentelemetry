# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             688    686    -2 ⚠️  РЕГРЕССИЯ
  partial            85     86 +    1
  not_found          41     54 +   13 ⚠️  РЕГРЕССИЯ
  n_a                10     14 +    4
  Всего             824    840 +   16

  🔴 ПОНИЖЕНИЕ СТАТУСА (31) - требует перепроверки:

     [Logs Api / Emit a LogRecord]
       found → n_a
       Текст: When only explicit Context is supported, this parameter SHOULD be required.
       Расположение: src/Логирование/Классы/ОтелЛоггер.os:94 → -
       Пояснение: Альтернативная ветка спецификации: SDK поддерживает неявный контекст (ОтелКонтекст.Текущий()), поэтому требование 'only explicit Context' не применимо
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Logger Creation]
       found → partial
       Текст: In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be 
       Пояснение: При ИмяБиблиотеки = Неопределено код заменяет на пустую строку (Неопределено → ''), не сохраняя исходное значение Неопределено. Для пустой строки ориг
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ShutDown]
       found → partial
       Текст: After the call to `Shutdown`, subsequent calls to `OnEmit` are not allowed. SDKs SHOULD ignore these
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:67 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43
       Пояснение: ОтелБазовыйПакетныйПроцессор.Обработать проверяет флаг Закрыт и игнорирует вызовы; в ОтелПростойПроцессорЛогов нет проверки состояния после Закрыть(),
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of 
       Пояснение: ЗарегистрироватьОбратныйВызов(Callback, НовыеИнструменты) принимает явный набор инструментов, но не валидирует, что все инструменты принадлежат тому ж
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API SHOULD provide some way to pass `state` to the callback.
       Пояснение: Callback получает только объект ОтелНаблюдениеМетрики. Отдельного механизма передачи user state нет; пользователь может использовать замыкание lambda.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → partial
       Текст: MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:308 → src/Метрики/Классы/ОтелПровайдерМетрик.os:59
       Пояснение: Закрыт реализован через АтомарноеБулево с CAS (СравнитьИУстановить) - Закрыть идемпотентен и безопасен. Однако ПолучитьМетр (Meter creation) и Сбросит
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → partial
       Текст: MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:64 → src/Экспорт/Классы/ОтелЭкспортерМетрик.os:58
       Пояснение: Методы СброситьБуфер и Закрыть в ОтелЭкспортерМетрик существуют как простые делегирующие процедуры, но не имеют явной БлокировкиРесурса для защиты от 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Configuration]
       found → partial
       Текст: If there is no matching view, but the `MetricReader` defines a default cardinality limit value based
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:253 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:151
       Пояснение: MetricReader предоставляет один общий ЛимитМощности (по умолчанию 2000), не дифференцированный по типу инструмента. Метр применяет его ко всем инструм
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       partial → not_found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94 → -
       Пояснение: СброситьБуфер - Процедура без возвращаемого значения; невозможно отличить успех от неудачи/таймаута.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       partial → not_found
       Текст: `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no erro
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94 → -
       Пояснение: СброситьБуфер не возвращает значение; статус ошибки/успеха недоступен.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       partial → not_found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94 → -
       Пояснение: СброситьБуфер не принимает таймаут и не прерывает операцию по таймауту.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Interface Definition]
       partial → not_found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:58 → -
       Пояснение: Экспортер.СброситьБуфер - Процедура без возвращаемого значения; статус succeed/failed/timed out не сообщается.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter Creation]
       found → partial
       Текст: In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be ret
       Пояснение: При передаче Неопределено имя нормализуется в пустую строку (стр. 67), исходное Неопределено не сохраняется. Пустая строка сохраняется. Полное соответ
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: The output `temporality` (optional), a function of instrument kind. This function SHOULD be obtained
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:265 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:419
       Пояснение: Селектор агрегации задаётся внутренней инициализацией ИнициализироватьСелекторАгрегации, не получается из экспортёра. По умолчанию SDK использует фикс
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: The `MetricReader` MUST ensure that data points from OpenTelemetry instruments are output in the con
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:250 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:163
       Пояснение: Для синхронных инструментов конверсия Delta→Cumulative реализована через сохранение аккумуляторов при Кумулятивной. Для асинхронных инструментов конве
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:228 → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:114
       Пояснение: Для асинхронных инструментов ВнешниеНаблюдения очищаются после сбора, но Cumulative-вариант не вычитает предыдущие значения - всегда выдаются последни
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`,
       Пояснение: СброситьБуферБезОчистки используется для всех читателей кроме последнего, последний выполняет ОчиститьТочкиДанных. Это уменьшает побочные эффекты, но 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       found → partial
       Текст: SDKs SHOULD return a valid no-op Meter for these calls, if possible.
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:70 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94
       Пояснение: СброситьБуфер - Процедура без возвращаемого значения; после Закрыть подкласс Экспортер вернёт Ложь, но читатель не пробрасывает результат вызывающей с
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       partial → not_found
       Текст: In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector tha
       Пояснение: Нет проверки, что при заданном имени потока селектор отбирает не более одного инструмента; первый найденный View применяется без проверки конфликта.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: If the user does not provide a `name` value, name from the Instrument the View matches MUST be used 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:283 → src/Метрики/Классы/ОтелМетр.os:635
       Пояснение: ОтелПредставление поддерживает поле НовоеИмя, но в коде применения View (ПрименитьПредставлениеКИнструменту) переименование инструмента по View не при
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: If the user does not provide a `description` value, the description from the Instrument a View match
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:284 → src/Метрики/Классы/ОтелМетр.os:635
       Пояснение: Поле НовоеОписание есть в ОтелПредставление, но применение НовоеОписание() в выходные данные метрики не реализовано (используется описание инструмента
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Specifying resource information via an environment variable]
       found → partial
       Текст: The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge 
       Пояснение: OTEL_RESOURCE_ATTRIBUTES извлекается и применяется к ресурсу, но логика приоритета 'user-provided resource > env' отсутствует: автоконфигурация просто
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / End]
       found → n_a
       Текст: Any locking used needs be minimized and SHOULD be removed entirely if possible.
       Расположение: src/Трассировка/Классы/ОтелСпан.os:459 → -
       Пояснение: В OneScript однопоточная модель выполнения в рамках сеанса; явных блокировок (locks/mutex) нет
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Link]
       found → partial
       Текст: Implementations SHOULD record links containing `SpanContext` with empty `TraceId` or `SpanId` (all z
       Расположение: src/Трассировка/Классы/ОтелСпан.os:373-391 → src/Трассировка/Классы/ОтелСпан.os:373
       Пояснение: ДобавитьЛинк не отвергает контексты с нулевыми ID, но и не реализует явное условие 'attribute set или TraceState non-empty' - принимает любой контекст
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → partial
       Текст: When the status is set to `Error` by Instrumentation Libraries, the `Description` SHOULD be document
       Пояснение: Это требование к документации Instrumentation Libraries, а не к самому SDK. SDK API позволяет передавать Сообщение, но конвенций по документации Descr
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → partial
       Текст: For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish the
       Пояснение: Это процессное требование к авторам Instrumentation Libraries, а не к коду SDK. В данном репозитории Instrumentation Libraries отсутствуют
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → n_a
       Текст: Generally, Instrumentation Libraries SHOULD NOT set the status code to `Ok`, unless explicitly confi
       Пояснение: Требование к Instrumentation Libraries, а не к Trace API SDK. В репозитории нет Instrumentation Libraries
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → n_a
       Текст: Instrumentation Libraries SHOULD leave the status code as `Unset` unless there is an error, as descr
       Пояснение: Требование к Instrumentation Libraries, а не к Trace API SDK. В репозитории нет Instrumentation Libraries
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → n_a
       Текст: Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they would otherwise gener
       Пояснение: Требование относится к инструментам анализа (бэкендам), а не к SDK
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Additional Span Interfaces]
       found → partial
       Текст: For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated 
       Расположение: src/Ядро/Классы/ОтелОбластьИнструментирования.os:68 → src/Трассировка/Классы/ОтелСпан.os:182
       Пояснение: Spand экспонирует ОбластьИнструментирования (InstrumentationScope), но не имеет отдельного устаревшего геттера InstrumentationLibrary - доступ к данны
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Presumption of TraceID randomness]
       found → partial
       Текст: For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Contex
       Расположение: src/Трассировка/Модули/ОтелСэмплер.os:139 → src/Трассировка/Модули/ОтелСэмплер.os:277
       Пояснение: TraceIdRatioBased сэмплер (СэмплироватьПоДоле) использует первые 8 hex-символов TraceID как источник случайности (presumption of randomness), но не уч
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (25) - требует перепроверки:

     [Env Vars / Enum]
       partial → found
       Текст: For sources accepting an enum value, if the user provides a value the implementation does not recogn
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:292
       Было: Предупреждение и безопасное игнорирование реализовано для otel.traces.sampler (строка 293) и otel.pr
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Api / Enabled]
       partial → found
       Текст: When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then M
       Код: src/Логирование/Классы/ОтелЛоггер.os:194
       Было: Контекст = Неопределено разрешается в текущий контекст только внутри ТрассировкаНеСэмплирована (ветк
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Concurrency requirements]
       partial → found
       Текст: Instrument - all methods MUST be documented that implementations need to be safe for concurrent use 
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:49
       Было: Потокобезопасность документирована только для синхронных инструментов (ОтелБазовыйСинхронныйИнструме
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Get a Meter]
       partial → found
       Текст: Therefore, this API MUST be structured to accept a variable number of attributes, including none.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:62
       Было: Параметр АтрибутыОбласти принимает ОтелАтрибуты-контейнер (или Неопределено) - т.е. 'переменное числ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Instrument]
       n_a → found
       Текст: Language-level features such as the distinction between integer and floating point numbers SHOULD be
       Код: src/Метрики/Классы/ОтелБазовыйАгрегатор.os:8
       Было: В OneScript единый числовой тип System.Decimal - различия integer/floating point на уровне языка отс
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / MeterProvider]
       partial → found
       Текст: Thus, the API SHOULD provide a way to set/register and access a global default `MeterProvider`.
       Код: src/Ядро/Модули/ОтелГлобальный.os:33
       Было: Глобальный доступ к Meter осуществляется через ОтелГлобальный.ПолучитьМетр(), установка провайдера м
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarReservoir]
       partial → found
       Текст: This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associat
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:30
       Было: Параметр АтрибутыСерии передаётся в Предложить(), но в документирующем комментарии не подчёркнуто, ч
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       partial → found
       Текст: This is a hint to ensure that the export of any `Metrics` the exporter has received prior to the cal
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:58
       Было: СброситьБуфер экспортёра - пустая реализация (no-op), потому что экспортёр синхронный и не буферизуе
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:58
       Было: СброситьБуфер - пустая процедура без параметра таймаута; прерывание по таймауту не реализовано явно,
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       partial → found
       Текст: Shutdown SHOULD be called only once for each `MetricExporter` instance.
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:64
       Было: Закрыть() идемпотентен (Закрыт.Установить(Истина) можно вызывать повторно без побочных эффектов), но
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       not_found → partial
       Текст: If applying the View results in conflicting metric identities the implementation SHOULD apply the Vi
       Код: src/Метрики/Классы/ОтелМетр.os:707
       Было: View применяется, но нет диагностики 'conflicting metric identities' (когда несколько View дают один
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricExporter]
       not_found → partial
       Текст: Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsuppo
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:250
       Было: ОтелЭкспортерМетрик не проверяет совместимость агрегации/временности данных и не сообщает об ошибке 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: If not configured, the Cumulative temporality SHOULD be used.
       Код: src/Метрики/Модули/ОтелСелекторВременнойАгрегации.os:24
       Было: Временность делегируется экспортеру через Экспортер.ПолучитьВременнуюАгрегацию; явного fallback на C
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → found
       Текст: Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that 
       Код: src/Метрики/Классы/ОтелМетр.os:536
       Было: Callback вызывается при сборе конкретным reader, но состояние инструмента общее для всех reader'ов —
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → found
       Текст: The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered ca
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:168
       Было: Есть ДобавитьВнешниеНаблюдения, разрешающая наблюдения вне зарегистрированного callback, что противо
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       partial → found
       Текст: Implementation SHOULD use the filter as early as possible to gain as much performance gain possible 
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:366
       Было: Фильтр принимается в интерфейсе, но применение зависит от реализации продюсера. Никакой внутренней р
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       not_found → partial
       Текст: If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include
       Код: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13
       Было: Интерфейс продюсера не требует и не документирует привязку InstrumentationScope, идентифицирующего с
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       not_found → partial
       Текст: For asynchronous instrument, the start timestamp SHOULD be:
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:188
       Было: Для async-инструментов startTimeUnixNano = ВремяСейчас на каждый collect, что не соответствует требо
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       partial → found
       Текст: The option SHOULD accept any form allowed by the underlying gRPC client implementation.
       Код: src/Экспорт/Классы/ОтелGrpcТранспорт.os:184
       Было: gRPC транспорт принимает адрес и передаёт его в oint/api/grpc клиент, но специальная обработка форм 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       not_found → found
       Текст: If the gRPC client implementation does not support an endpoint with a scheme of http or https then t
       Код: src/Экспорт/Классы/ОтелGrpcТранспорт.os:184
       Было: Преобразование URL http/https в альтернативную форму для gRPC-клиента не реализовано — адрес передаё
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Specify Protocol]
       partial → found
       Текст: If they support only one, it SHOULD be http/protobuf.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:612
       Было: SDK поддерживает более одного транспорта (grpc и http/json), поэтому условие «если поддерживается то
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Global Propagators]
       partial → found
       Текст: If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace
       Код: src/Ядро/Модули/ОтелГлобальный.os:121
       Было: В SDK нет pre-configured пропагаторов: если пользователь не задал, ПолучитьПропагаторы возвращает От
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Behavior of the API in the absence of an installed SDK]
       not_found → partial
       Текст: If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly witho
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:226
       Было: Нет проверки ЗаписьАктивна()/IsRecording у родительского спана в ОтелТрассировщик.НачатьСпан - всегд
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Wrapping a SpanContext in a Span]
       partial → found
       Текст: The API MUST provide an operation for wrapping a `SpanContext` with an object implementing the `Span
       Код: src/Трассировка/Классы/ОтелНоопСпан.os:272
       Было: Операция реализована через конструктор Новый ОтелНоопСпан(КонтекстСпана), но отдельного метода API (
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / `ForceFlush()`]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:126
       Было: СброситьБуфер() экспортера не принимает параметр таймаута. Для синхронного экспортера это no-op (зав
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  📋 Новые секции (2):
     + [Logs Sdk] Event to span event bridge (9 req)
     + [Trace Sdk] ID Generators (4 req)

  📋 Исчезнувшие секции (1):
     - [Trace Sdk] Id Generators (4 req)

  ➕ НОВЫЕ ТРЕБОВАНИЯ (20) - агент нашёл дополнительные:

     [Logs Api] MUST found: The API MUST accept the following parameters:
     [Logs Sdk] SHOULD not_found: Additional processors defined in this document SHOULD be provided by SDK package
     [Logs Sdk] MUST found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Logs Sdk] MUST NOT found: If trace_based is false, log records MUST NOT be affected because of this parame
     [Metrics Api] SHOULD found: To help users avoid performing computationally expensive operations when recordi
     [Metrics Api] SHOULD not_found: The API to register a new Callback SHOULD accept: * A `callback` function* A lis
     [Metrics Sdk] SHOULD partial: The “offer” method SHOULD accept measurements, including:
     [Metrics Sdk] SHOULD not_found: `ForceFlush` MAY skip `Export(batch)` calls if the timeout is already expired, b
     [Metrics Sdk] SHOULD found: This function SHOULD be obtained from the `exporter`.
     [Metrics Sdk] MUST not_found: Status: Development - When `maxExportBatchSize` is configured, the reader MUST e
     [Metrics Sdk] MUST not_found: The initial batch of metric data MUST be split into as many "full" batches of si
     [Metrics Sdk] MUST found: The reader MUST ensure all metric data points from a single `Collect()` are prov
     [Metrics Sdk] MUST NOT found: The reader MUST NOT combine metrics from different `Collect()` calls into the sa
     [Metrics Sdk] SHOULD found: After the call to `Shutdown`, subsequent attempts to get a `Meter` are not allow
     [Otlp Exporter] MUST found: Protocol: The transport protocol. Options MUST be one of: `grpc`, `http/protobuf
     [Trace Api] MUST found: This API MUST accept the following parameters:
     [Trace Api] SHOULD found: In case an invalid name (null or empty string) is specified, a working Tracer im
     [Trace Api] SHOULD found: In case an invalid name (null or empty string) is specified, a working Tracer im
     [Trace Api] SHOULD found: An API to set the Status. This SHOULD be called SetStatus.
     [Trace Sdk] SHOULD found: After the call to `Shutdown`, subsequent calls to `OnStart`, `OnEnd`, or `ForceF

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (13) - были раньше, теперь нет:

     [Logs Api] MUST found: The API MUST accept the following parameters: Timestamp (optional), Observed Tim
     [Logs Sdk] MUST NOT found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Metrics Api] SHOULD found: synchronous instruments SHOULD provide this `Enabled` API.
     [Metrics Api] SHOULD found: The API to register a new Callback SHOULD accept:
     [Metrics Sdk] SHOULD found: The "offer" method SHOULD accept measurements, including: The `value` of the mea
     [Metrics Sdk] SHOULD partial: The default output `aggregation` (optional), a function of instrument kind. This
     [Metrics Sdk] SHOULD partial: SDKs SHOULD return some failure for these calls, if possible.
     [Otlp Exporter] MUST partial: Options MUST be one of: grpc, http/protobuf, http/json.
     [Trace Api] MUST found: This API MUST accept the following parameters: `name` (required), `version` (opt
     [Trace Api] SHOULD found: its `name` property SHOULD be set to an empty string.
     [Trace Api] SHOULD found: a message reporting that the specified value is invalid SHOULD be logged.
     [Trace Api] SHOULD found: This SHOULD be called `SetStatus`.
     [Trace Sdk] SHOULD found: SDKs SHOULD ignore these calls gracefully, if possible.

  Итого изменений: 89
    Понижений: 31, Повышений: 25, Боковых: 0
    Новых req: 20, Пропущенных req: 13
    Новых секций: 2, Исчезнувших секций: 1

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
