# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             638    696 +   58 ✅
  partial            93     63   -30
  not_found          88     57   -31
  n_a                 5      8 +    3
  Всего             824    824 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (31) - требует перепроверки:

     [Logs Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Расположение: src/Экспорт/Классы/ОтелЭкспортерЛогов.os:45 → src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:61
       Пояснение: Timeout is supported at processor level but not exposed at LoggerProvider.СброситьБуфер() level - only async version supports timeout via Promise
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Asynchronous Counter creation]
       found → partial
       Текст: The API SHOULD provide some way to pass state to the callback.
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147 → -
       Пояснение: Callbacks are created as lambda functions that can capture closure variables, but there's no explicit state parameter mechanism provided by the API
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Counter operations]
       found → partial
       Текст: If possible, this API SHOULD be structured so a user is obligated to provide this parameter.
       Пояснение: Параметр Значение обязательный, но может быть 0 или отрицательным (игнорируется).
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Enabled]
       found → partial
       Текст: the API MUST be structured in a way for parameters to be added.
       Пояснение: Метод Включен() не принимает параметры, но можно добавить перегрузку в будущем.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Histogram operations]
       found → partial
       Текст: This API SHOULD be documented in a way to communicate to users that this value is expected to be non
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:88-91 → -
       Пояснение: Documentation doesn't explicitly state non-negative expectation for histogram values
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Instrument description]
       found → not_found
       Текст: It MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or `u
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:11 → -
       Пояснение: Нет явной проверки или ограничения на BMP Unicode. Строки обрабатываются как есть через НормализоватьСтроку().
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Instrument description]
       found → not_found
       Текст: It MUST support at least 1023 characters.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:11 → -
       Пояснение: Нет ограничений на длину строки описания. Строка принимается без проверки длины.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: If possible, the API SHOULD be structured so a user is obligated to provide this parameter.
       Пояснение: Имя обязательный первый параметр, но технически можно передать пустую строку без проверки.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: If possible, the API SHOULD be structured so a user is obligated to provide this parameter.
       Пояснение: Имя обязательный первый параметр, но технически можно передать пустую строку без проверки.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Every currently registered Callback associated with a set of instruments MUST be evaluated exactly o
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160 → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160-180
       Пояснение: Callbacks выполняются при сборе, но нет явного механизма предотвращения двойного вызова в течение одного цикла сборки.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / AlignedHistogramBucketExemplarReservoir]
       found → partial
       Текст: This implementation MUST store at most one measurement that falls within a histogram bucket, and SHO
       Расположение: src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50 → src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:40-51
       Пояснение: Uses simple replacement (last measurement wins) instead of uniformly-weighted sampling algorithm
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Collect]
       partial → not_found
       Текст: `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:240-259 → -
       Пояснение: Collect methods do not provide failure/timeout return values - they handle errors internally with logging
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Configuration]
       found → partial
       Текст: A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardi
       Расположение: src/Метрики/Классы/ОтелПредставление.os:93 → src/Метрики/Классы/ОтелПредставление.os:92
       Пояснение: ОтелПредставление has ЛимитМощностиАгрегации field but it is not applied to instruments in ПрименитьПредставлениеКИнструменту method
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Duplicate instrument registration]
       found → not_found
       Текст: Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Met
       Расположение: src/Метрики/Классы/ОтелМетр.os:1000 → -
       Пояснение: SDK returns the first registered instrument, not both Metric objects. No data pass-through for conflicting instruments with different units
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Exemplar defaults]
       found → not_found
       Текст: Explicit bucket histogram aggregation with more than 1 bucket SHOULD use `AlignedHistogramBucketExem
       Расположение: src/Метрики/Классы/ОтелМетр.os:106-107 → -
       Пояснение: No automatic assignment of reservoir type based on aggregation configuration found
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Exemplar defaults]
       found → not_found
       Текст: Base2 Exponential Histogram Aggregation SHOULD use a `SimpleFixedSizeExemplarReservoir` with a reser
       Расположение: src/Метрики/Классы/ОтелМетр.os:146-148 → -
       Пояснение: No automatic assignment of reservoir type for exponential histograms found
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Exemplar defaults]
       partial → not_found
       Текст: All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:188 → -
       Пояснение: No automatic assignment of reservoir type based on aggregation type found
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ExemplarReservoir]
       found → partial
       Текст: The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars.
       Расположение: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1-2 → -
       Пояснение: Algorithm R implementation allocates arrays but this is standard practice for reservoir sampling
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter]
       found → not_found
       Текст: If the `MeterProvider` supports updating the MeterConfigurator, then upon update the `Meter` MUST be
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:221 → -
       Пояснение: MeterProvider does not support updating MeterConfigurator. The конфигураторМетров callback is only called once during meter creation, not dynamically 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Numerical limits handling]
       partial → n_a
       Текст: The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry.
       Пояснение: OneScript uses System.Decimal instead of IEEE 754, so NaN and Infinity are not possible - operations throw exceptions instead of returning special val
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       partial → not_found
       Текст: `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:370 → -
       Пояснение: Произвести() returns Массив (array of ОтелДанныеМетрики). There is no mechanism to communicate success/failure/timeout status to the caller, only exce
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       partial → not_found
       Текст: The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `
       Пояснение: Default protocol is set to "http/json" instead of "http/protobuf" as required by spec
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Specify Protocol]
       partial → not_found
       Текст: If no configuration is provided the default transport SHOULD be `http/protobuf` unless SDKs have goo
       Пояснение: Default protocol is "http/json" instead of "http/protobuf" as recommended
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: Resource detectors SHOULD have a unique name for reference in configuration.
       Пояснение: Условная фича Resource Detector Naming не реализована в данном SDK - детекторы не имеют именования для конфигурации.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: Names SHOULD be snake case and consist of lowercase alphanumeric and `_` characters, which ensures t
       Пояснение: Условная фича Resource Detector Naming не реализована в данном SDK.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: Resource detector names SHOULD reflect the root namespace of attributes they populate.
       Пояснение: Условная фича Resource Detector Naming не реализована в данном SDK.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name whic
       Пояснение: Условная фича Resource Detector Naming не реализована в данном SDK.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: An SDK which identifies multiple resource detectors with the same name SHOULD report an error.
       Пояснение: Условная фича Resource Detector Naming не реализована в данном SDK.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: In order to limit collisions, resource detectors SHOULD document their name in a manner which is eas
       Пояснение: Условная фича Resource Detector Naming не реализована в данном SDK.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Context Interaction]
       found → partial
       Текст: The functionality listed above is necessary because API users SHOULD NOT have access to the Context 
       Пояснение: КлючСпана() экспортирована публично и доступна пользователям API. Высокоуровневые API (СпанИзКонтекста, КонтекстСоСпаном) существуют, но ключ контекст
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / End]
       found → partial
       Текст: This operation itself MUST NOT perform blocking I/O on the calling thread.
       Пояснение: End() вызывает Процессор.ПриЗавершении(), а SimpleSpanProcessor синхронно вызывает Экспортер.Экспортировать(), что может выполнять блокирующий HTTP-за
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (88) - требует перепроверки:

     [Env Vars / Boolean]
       partial → found
       Текст: Any value that represents a Boolean MUST be set to true only by the case-insensitive string "true", 
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:764
       Было: The implementation uses НРег(Значение) = "true" which only accepts lowercase 'true', not case-insens
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Boolean]
       not_found → found
       Текст: An implementation MUST NOT extend this definition and define additional values that are interpreted 
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:764
       Было: No explicit validation exists to prevent extension of true values - the current implementation accep
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Boolean]
       partial → found
       Текст: Any value not explicitly defined here as a true value, including unset and empty values, MUST be int
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:764
       Было: Implementation treats non-'true' values as false but doesn't handle case-insensitive 'false' values 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Boolean]
       not_found → found
       Текст: All Boolean environment variables SHOULD be named and defined such that false is the expected safe d
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:763
       Было: While OTEL_ENABLED defaults to true (safe behavior), there's no systematic approach to ensure all bo
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Boolean]
       not_found → found
       Текст: Renaming or changing the default value MUST NOT happen without a major version upgrade.
       Было: No versioning policy or protection mechanism exists to prevent breaking changes to environment varia
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Environment Variable Specification]
       partial → found
       Текст: They SHOULD also follow the common configuration specification.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1-104
       Было: The implementation reads environment variables through configor but doesn't implement all aspects of
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / General SDK Configuration]
       not_found → partial
       Текст: Values MUST be deduplicated in order to register a `Propagator` only once.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:468-474
       Было: Код для OTEL_PROPAGATORS есть в строке 446, но нет явной дедупликации пропагаторов - они просто доба
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / General SDK Configuration]
       not_found → found
       Текст: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation 
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:253-258
       Было: Нет обработки OTEL_TRACES_SAMPLER_ARG в коде - переменная упоминается только в комментариях строка 1
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / General SDK Configuration]
       not_found → found
       Текст: Invalid or unrecognized input MUST be logged
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:253
       Было: Нет обработки OTEL_TRACES_SAMPLER_ARG в коде - переменная упоминается только в комментариях строка 1
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / General SDK Configuration]
       not_found → found
       Текст: MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not 
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:253-258
       Было: Нет обработки OTEL_TRACES_SAMPLER_ARG в коде - переменная упоминается только в комментариях строка 1
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Numeric]
       not_found → found
       Текст: For new implementations, these should be treated as MUST requirements.
       Было: This is a meta-requirement about treating SHOULD as MUST for new implementations - there's no explic
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:61-74
       Было: СброситьБуфер() is a Процедура (void) - does not return explicit status. СброситьБуферАсинхронно() r
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:64-67
       Было: СброситьБуфер() does not accept a timeout parameter. Individual processors support ТаймаутМс but are
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71
       Было: СброситьБуфер() is declared as Процедура (void return); failure propagates via exceptions, but there
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:137
       Было: СброситьБуфер() объявлен как Процедура (void), а не Функция - вызывающий код не получает информацию 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / OnEmit]
       partial → found
       Текст: This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD 
       Код: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:19-23
       Было: Exceptions are caught at composite processor level (try-catch in ПриПоявлении), but ОтелПростойПроце
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / OnEmit]
       not_found → found
       Текст: To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecor
       Код: src/Логирование/Классы/ОтелЛоггер.os:111
       Было: No documentation or mechanism recommending users to clone logRecord for concurrent processing; the b
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ReadWriteLogRecord]
       partial → found
       Текст: A function receiving this as an argument MUST additionally be able to modify the following informati
       Код: src/Логирование/Классы/ОтелЗаписьЛога.os:308-347
       Было: ОтелЗаписьЛога provides modification capabilities but there's no separate ReadWriteLogRecord interfa
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ReadableLogRecord]
       partial → found
       Текст: A function receiving this as an argument MUST be able to access all the information added to the Log
       Код: src/Логирование/Классы/ОтелЗаписьЛога.os:51-125
       Было: ОтелЗаписьЛога provides access to all information but there's no separate ReadableLogRecord interfac
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ReadableLogRecord]
       partial → found
       Текст: It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) assoc
       Код: src/Логирование/Классы/ОтелЗаписьЛога.os:135-145
       Было: ОтелЗаписьЛога provides access to scope and resource but there's no separate ReadableLogRecord inter
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ShutDown]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:81-95
       Было: Закрыть() is declared as Процедура (void return); failure propagates via exceptions, but there is no
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:149
       Было: Закрыть() is a Процедура (void) - does not return explicit status. ЗакрытьАсинхронно() returns Обеща
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Compatibility requirements]
       not_found → found
       Текст: All the metrics components SHOULD allow new APIs to be added to existing components without introduc
       Было: No explicit design or documentation found regarding adding new APIs without breaking changes. The cu
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Compatibility requirements]
       partial → found
       Текст: All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introdu
       Код: src/Метрики/Классы/ОтелМетр.os:171
       Было: Some methods use optional parameters (e.g., Атрибуты = Неопределено, Контекст = Неопределено), but t
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Counter operations]
       partial → found
       Текст: This API SHOULD NOT validate this value, that is left to implementations of the API.
       Код: src/Метрики/Классы/ОтелСчетчик.os:22-24
       Было: Метод Добавить выполняет проверку Значение < 0 и игнорирует отрицательные значения (строка 22-24), х
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Enabled]
       partial → found
       Текст: The API SHOULD be documented that instrumentation authors needs to call this API each time they reco
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:83-86
       Было: Документация метода Включен() описывает возвращаемое значение и условия отключения, но не содержит р
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Histogram operations]
       partial → found
       Текст: This API SHOULD NOT validate this value, that is left to implementations of the API.
       Код: src/Метрики/Классы/ОтелГистограмма.os:20-22
       Было: The API validates that the value is a number type but doesn't validate non-negative values as requir
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Instrument unit]
       partial → found
       Текст: It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII string.
       Код: src/Метрики/Классы/ОтелМетр.os:540
       Было: Unit string is stored as-is without modification, but descriptor conflict comparison at line 613 use
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Multiple-instrument callbacks]
       partial → found
       Текст: The API to register a new Callback SHOULD accept: A list (or tuple, etc.) of Instruments used in the
       Код: src/Метрики/Классы/ОтелМетр.os:388
       Было: Multiple-instrument callbacks are partially implemented through ВнешниеНаблюдения mechanism, but the
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to con
       Код: src/Метрики/Классы/ОтелМетр.os:43-44
       Было: Документация параметра Имя не упоминает требования к синтаксису имени инструмента (допустимые символ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to con
       Код: src/Метрики/Классы/ОтелМетр.os:230-231
       Было: Документация параметра Имя асинхронных инструментов не упоминает требования к синтаксису имени инстр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Therefore, this API MUST be structured to accept a variable number of `callback` functions, includin
       Код: src/Метрики/Классы/ОтелМетр.os:242
       Было: API принимает только 0 или 1 callback при создании (Callback = Неопределено), а не произвольное числ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API MUST support creation of asynchronous instruments by passing zero or more `callback` functio
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147-156
       Было: API создания принимает максимум один callback. Передача нескольких callback при создании не поддержи
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions MUST be documented as follows for the end user:
       Код: src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69
       Было: Есть базовая документация использования callback в комментариях ОтелНаблюдениеМетрики, но не задокум
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions SHOULD be reentrant safe.
       Код: src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69
       Было: В документации API нет указания для пользователей о необходимости реентрантной безопасности callback
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions SHOULD NOT take an indefinite amount of time.
       Код: src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69
       Было: В документации API нет указания для пользователей о недопустимости неограниченного времени выполнени
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same
       Код: src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69
       Было: В документации API нет указания для пользователей о недопустимости дублирования наблюдений с одинако
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Defaults and configuration]
       partial → found
       Текст: The SDK MUST provide configuration according to the SDK environment variables specification.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:3
       Было: SDK читает OTEL_METRICS_EXPORTER, OTEL_METRICS_EXEMPLAR_FILTER и OTEL_EXPORTER_OTLP_METRICS_* переме
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Exemplar]
       not_found → partial
       Текст: If `Exemplar` sampling is off, the SDK MUST NOT have overhead related to exemplar sampling.
       Код: /home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Модули/ОтелФильтрЭкземпляров.os:46
       Было: No conditional exemplar sampling logic found that avoids overhead when sampling is disabled.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Exemplar]
       partial → found
       Текст: A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation.
       Код: /home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:88
       Было: ExemplarReservoir exists but no clear integration with aggregation configuration (e.g., histogram bu
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarFilter]
       partial → found
       Текст: The filter configuration SHOULD follow the environment variable specification.
       Код: src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114-133
       Было: OTEL_METRICS_EXEMPLAR_FILTER is read but only in MeterProviderBuilder, not in auto-configuration mod
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       not_found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94
       Было: СброситьБуфер() вызывает СобратьИЭкспортировать() синхронно без явного таймаута; таймаут зависит тол
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       n_a → found
       Текст: Implementations are REQUIRED to accept the entire normal range of IEEE floating point values (i.e., 
       Было: OneScript uses System.Decimal, not IEEE 754 floating point, so NaN and Infinity handling is not appl
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       n_a → found
       Текст: Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`
       Было: OneScript uses System.Decimal, not IEEE 754, so non-normal values like NaN and Infinity are not poss
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       partial → found
       Текст: Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possi
       Код: src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:296-320
       Было: Exponential histogram aggregator exists but dynamic scale adjustment logic is not fully implemented
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument enabled]
       partial → found
       Текст: The synchronous instrument `Enabled` MUST return `false` when either: * Status: Development - The Me
       Код: /home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:231
       Было: Enabled method exists and considers both meter enabled state and instrument enabled state, but speci
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument selection criteria]
       partial → found
       Текст: If the SDK does not support wildcards in general, it MUST still recognize the special single asteris
       Код: src/Метрики/Классы/ОтелСелекторИнструментов.os:37-38
       Было: Only single asterisk '*' is supported for matching all instruments, but no general wildcard pattern 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       not_found → partial
       Текст: The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily 
       Код: src/Экспорт/Классы/ОтелHttpТранспорт.os:76
       Было: SDK реализует retry-логику в транспортном слое: ОтелHttpТранспорт и ОтелGrpcТранспорт используют Стр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       partial → found
       Текст: The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrum
       Код: src/Метрики/Классы/ОтелМетр.os:754-871
       Было: Basic view processing is implemented but not the complete logic flow described in the specification
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       not_found → found
       Текст: Instrument advisory parameters, if any, MUST be honored.
       Код: src/Метрики/Классы/ОтелМетр.os:792-813
       Было: Advisory parameters from instruments are partially used but no systematic honoring of all advisory p
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       not_found → found
       Текст: If applying the View results in conflicting metric identities the implementation SHOULD apply the Vi
       Было: No conflict detection or warning logic found for conflicting metric identities from Views
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       not_found → found
       Текст: If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asy
       Было: No validation or warning logic found for incompatible View configurations
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       not_found → found
       Текст: If both a View and Instrument advisory parameters specify the same aspect of the Stream configuratio
       Код: src/Метрики/Классы/ОтелМетр.os:792-813
       Было: No systematic precedence logic found between View settings and instrument advisory parameters
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       not_found → found
       Текст: If the Instrument could not match with any of the registered `View`(s), the SDK SHOULD enable the in
       Код: src/Метрики/Классы/ОтелМетр.os:829-871
       Было: No explicit handling found for instruments that don't match any registered Views
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter Creation]
       partial → found
       Текст: It SHOULD only be possible to create `Meter` instances through a `MeterProvider`
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:59
       Было: Meter creation is implemented through MeterProvider.ПолучитьМетр() and MeterBuilder.Построить(), but
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       not_found → found
       Текст: The SDK SHOULD provide a way to allow `MetricReader` to respond to MeterProvider.ForceFlush and Mete
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94-96,138-139
       Было: No explicit ForceFlush/Shutdown callbacks or interfaces found in MetricReader implementations for Me
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       not_found → found
       Текст: Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that 
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:281-305
       Было: Callbacks are invoked globally, not specific to individual MetricReaders during collection
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       not_found → partial
       Текст: The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered ca
       Было: No validation found to disregard asynchronous instrument API usage outside callbacks
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       not_found → partial
       Текст: The implementation SHOULD use a timeout to prevent indefinite callback execution.
       Было: No timeout mechanism found in callback execution code
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       not_found → found
       Текст: The implementation MUST complete the execution of all callbacks for a given instrument before starti
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160-185
       Было: No synchronization logic found to ensure all callbacks complete before next collection
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / SimpleFixedSizeExemplarReservoir]
       partial → found
       Текст: If no size configuration is provided, the default size MAY be the number of possible concurrent thre
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:174
       Было: Default size is hardcoded as 1, but no logic to use CPU count for default sizing when no configurati
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       not_found → partial
       Текст: For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp,
       Было: No delta aggregation start timestamp management found according to collection intervals
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       not_found → partial
       Текст: This implies that all data points with delta temporality aggregation for an instrument MUST share th
       Было: No logic found to ensure consistent start timestamps for delta temporality data points
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       not_found → partial
       Текст: Cumulative timeseries MUST use a consistent start timestamp for all collection intervals.
       Было: No consistent start timestamp management found for cumulative timeseries
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       not_found → partial
       Текст: For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the
       Было: Start timestamps use current time, not the time of first measurement
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       not_found → found
       Текст: `name`: The metric stream name that SHOULD be used.
       Код: src/Метрики/Классы/ОтелПредставление.os:29
       Было: ОтелПредставление has НовоеИмя field but no usage documentation or validation for stream naming
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       not_found → found
       Текст: In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector tha
       Было: No validation logic found to ensure single instrument selection when name is provided
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       not_found → found
       Текст: If the user does not provide a `name` value, name from the Instrument the View matches MUST be used 
       Код: src/Метрики/Классы/ОтелМетр.os:754-760
       Было: No logic found to apply instrument name as default when view name is not provided
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       not_found → found
       Текст: `description`: The metric stream description that SHOULD be used.
       Код: src/Метрики/Классы/ОтелПредставление.os:37
       Было: ОтелПредставление has НовоеОписание field but no usage documentation for stream description
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       not_found → found
       Текст: If the user does not provide a `description` value, the description from the Instrument a View match
       Код: src/Метрики/Классы/ОтелМетр.os:754-760
       Было: No logic found to apply instrument description as default when view description is not provided
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       not_found → found
       Текст: If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggreg
       Код: src/Метрики/Классы/ОтелМетр.os:829-871
       Было: Default aggregation is handled by instrument type, but not configurable per MetricReader instance
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       partial → found
       Текст: The option SHOULD accept any form allowed by the underlying gRPC client implementation.
       Код: src/Экспорт/Классы/ОтелGrpcТранспорт.os:174-175
       Было: gRPC transport accepts address as string but doesnt expose all underlying gRPC client configuration 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Specify Protocol]
       partial → found
       Текст: SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563-571
       Было: SDK supports grpc and http/json but not http/protobuf specifically
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Specify Protocol]
       not_found → partial
       Текст: If they support only one, it SHOULD be `http/protobuf`.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563-571
       Было: SDK supports grpc and http/json, not http/protobuf as preferred
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Global Propagators]
       not_found → found
       Текст: If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:443
       Было: SDK не предоставляет предварительной конфигурации пропагаторов по умолчанию. При отсутствии явной ко
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Propagators Distribution]
       partial → found
       Текст: The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST 
       Код: src/Пропагация/Классы/ОтелB3Пропагатор.os:1
       Было: B3 propagator is distributed within the main package rather than as a separate extension package. W3
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Detecting resource information from the environment]
       partial → found
       Текст: whereas an error that occurs during an attempt to detect resource information SHOULD be considered a
       Код: src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:24
       Было: Errors during detection are caught and logged at Debug level (Лог.Отладка) instead of Error level. T
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Detecting resource information from the environment]
       partial → found
       Текст: Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attrib
       Код: src/Ядро/Классы/ОтелРесурс.os:99
       Было: Detectors set schema URL before attempting attribute detection. If detection fails (exception), the 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush()]
       partial → found
       Текст: If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over f
       Код: src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:75
       Было: Пакетный процессор корректно проверяет таймаут в ЭкспортироватьВсеПакеты. Простой процессор принимае
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush()]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:72
       Было: Метод СброситьБуфер возвращает void (Процедура). Ошибки передаются через исключения, но нет явного в
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush()]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:75
       Было: Пакетный процессор поддерживает таймаут через ЭкспортироватьВсеПакеты. Простой процессор принимает п
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / OnEnding]
       n_a → found
       Текст: The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking `
       Код: src/Трассировка/Классы/ОтелСпан.os:467
       Было: Многопоточная безопасность контекста на уровне goroutine/thread-local - ограничение платформы OneScr
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Presumption of TraceID randomness]
       not_found → partial
       Текст: For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Contex
       Код: src/Трассировка/Модули/ОтелСэмплер.os:290-298
       Было: The sampler implementation in ОтелСэмплер.os does not check for explicit randomness values in the 'r
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown()]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80
       Было: Метод Закрыть возвращает void (Процедура). Ошибки передаются через исключения, но нет явного возврат
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown()]
       partial → found
       Текст: `Shutdown` MUST include the effects of `ForceFlush`.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:83
       Было: Простой процессор: Закрыть вызывает Экспортер.Закрыть(), но НЕ вызывает СброситьБуфер (ForceFlush эк
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Span Limits]
       not_found → found
       Текст: To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per disca
       Код: src/Трассировка/Классы/ОтелСпан.os:481-483
       Было: No logging implementation found for limit violations. There's no code to log when attributes, events
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Span Limits]
       partial → found
       Текст: The options MAY be bundled in a class, which then SHOULD be called `SpanLimits`.
       Код: src/Трассировка/Классы/ОтелЛимитыСпана.os:1
       Было: The class exists as ОтелЛимитыСпана but uses Russian naming instead of the specified English name Sp
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Span Limits]
       not_found → found
       Текст: There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute, event,
       Код: src/Трассировка/Классы/ОтелСпан.os:481-483
       Было: No logging implementation found for when limits are exceeded and items are discarded. The ОтелЛимиты
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (41) - агент нашёл дополнительные:

     [Env Vars] SHOULD not_found: It is a deprecated value left for backwards compatibility. It SHOULD NOT be supp
     [Env Vars] SHOULD not_found: It is a deprecated value left for backwards compatibility. It SHOULD NOT be supp
     [Env Vars] SHOULD not_found: It is a deprecated value left for backwards compatibility. It SHOULD NOT be supp
     [Env Vars] SHOULD found: For new implementations, these should be treated as MUST requirements.
     [Logs Api] SHOULD found: To help users avoid performing computationally expensive operations when generat
     [Logs Sdk] MUST found: If configuration is updated (e.g., adding a LogRecordProcessor), the updated con
     [Logs Sdk] MUST found: it MUST NOT matter whether a Logger was obtained from the LoggerProvider before 
     [Logs Sdk] SHOULD partial: ForceFlush SHOULD return some ERROR status if there is an error condition
     [Logs Sdk] SHOULD partial: and if there is no error condition, it SHOULD return some NO ERROR status
     [Logs Sdk] SHOULD found: its name SHOULD keep the original invalid value
     [Logs Sdk] SHOULD found: and a message reporting that the specified value is invalid SHOULD be logged.
     [Logs Sdk] SHOULD found: After the call to Shutdown, subsequent attempts to get a Logger are not allowed.
     [Metrics Api] MUST found: observations from a single callback MUST be reported with identical timestamps
     [Metrics Api] SHOULD found: To help users avoid performing computationally expensive operations when recordi
     [Metrics Api] SHOULD NOT found: Note: Meter SHOULD NOT be responsible for the configuration. This should be the 
     [Metrics Api] MUST found: The MeterProvider MUST provide the following functions: * Get a Meter
     [Metrics Api] MUST found: observations from a single callback MUST be reported with identical timestamps.
     [Metrics Sdk] SHOULD found: The SDK SHOULD provide the following Aggregation: Base2 Exponential Bucket Histo
     [Metrics Sdk] MUST found: The reservoir MUST be given the Attributes associated with its timeseries point 
     [Metrics Sdk] SHOULD found: When the histogram contains not more than one value in either of the positive or
     ... и ещё 21

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (41) - были раньше, теперь нет:

     [Env Vars] SHOULD partial: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD partial: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD partial: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD found: For variables accepting a numeric value, if the user provides a value the implem
     [Logs Api] SHOULD found: a Logger SHOULD provide this Enabled API.
     [Logs Sdk] MUST found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Logs Sdk] MUST NOT found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Logs Sdk] SHOULD partial: `ForceFlush` SHOULD return some ERROR status if there is an error condition; and
     [Logs Sdk] SHOULD partial: `ForceFlush` SHOULD return some ERROR status if there is an error condition; and
     [Logs Sdk] SHOULD found: In the case where an invalid `name` (null or empty string) is specified, a worki
     [Logs Sdk] SHOULD found: In the case where an invalid `name` (null or empty string) is specified, a worki
     [Logs Sdk] SHOULD found: SDKs SHOULD return a valid no-op `Logger` for these calls, if possible.
     [Metrics Api] MAY found: This MAY be called CreateObservableCounter.
     [Metrics Api] SHOULD found: synchronous instruments SHOULD provide this `Enabled` API.
     [Metrics Api] SHOULD NOT found: `Meter` SHOULD NOT be responsible for the configuration.
     [Metrics Api] MUST found: The `MeterProvider` MUST provide the following functions:
     [Metrics Api] MUST found: The API MUST treat observations from a single Callback as logically taking place
     [Metrics Sdk] SHOULD found: The SDK SHOULD provide the following `Aggregation`:
     [Metrics Sdk] MAY found: The "offer" method MAY accept a filtered subset of `Attributes` which diverge fr
     [Metrics Sdk] MUST n_a: The implementation MUST maintain reasonable minimum and maximum scale parameters
     ... и ещё 21

  Итого изменений: 201
    Понижений: 31, Повышений: 88, Боковых: 0
    Новых req: 41, Пропущенных req: 41
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
