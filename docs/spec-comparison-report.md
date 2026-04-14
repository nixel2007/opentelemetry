# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             649    664 +   15 ✅
  partial           105     82   -23
  not_found          56     63 +    7 ⚠️  РЕГРЕССИЯ
  n_a                14     15 +    1
  Всего             824    824 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (23) - требует перепроверки:

     [Logs Sdk / ForceFlush]
       partial → not_found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:107-111 → -
       Пояснение: СброситьБуфер (ForceFlush) is implemented as Процедура (void) with no return value in all processor implementations (ИнтерфейсПроцессорЛогов.os:28, От
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Logger]
       found → partial
       Текст: If the `LoggerProvider` supports updating the LoggerConfigurator, then upon update the `Logger` MUST
       Пояснение: Logger has УстановитьКонфигурацию setter method, but LoggerProvider does not have a public method to update the configurator and propagate new LoggerC
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ShutDown]
       partial → not_found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:116-123 → -
       Пояснение: Закрыть (Shutdown) is implemented as Процедура (void) with no return value in all processor implementations (ИнтерфейсПроцессорЛогов.os:36, ОтелПросто
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Instrument]
       found → n_a
       Текст: Language-level features such as the distinction between integer and floating point numbers SHOULD be
       Расположение: src/Метрики/Классы/ОтелМетр.os:562 → -
       Пояснение: OneScript has a single numeric type (Число) with no language-level distinction between integer and floating point. There is no type information to use
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ExemplarReservoir]
       found → partial
       Текст: The "offer" method SHOULD accept measurements, including: The value of the measurement, the complete
       Расположение: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39 → src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:41
       Пояснение: Метод Предложить() принимает Значение и АтрибутыИзмерения, но вместо полного Context (с Baggage) принимает только КонтекстСпана (SpanContext). Timesta
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       partial → not_found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88 → -
       Пояснение: СброситьБуфер() является процедурой (void) и не возвращает информацию об успехе, ошибке или таймауте.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       partial → not_found
       Текст: `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no erro
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88 → -
       Пояснение: СброситьБуфер() является процедурой (void) и не возвращает статус ERROR/NO ERROR.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       found → not_found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88 → -
       Пояснение: СброситьБуфер() вызывает СобратьИЭкспортировать() синхронно без механизма таймаута.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Interface Definition]
       partial → not_found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47 → -
       Пояснение: Метод СброситьБуфер() экспортера является процедурой (void) и не возвращает информацию об успехе, ошибке или таймауте.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Periodic exporting MetricReader]
       found → partial
       Текст: The reader MUST synchronize calls to `MetricExporter`'s `Export` to make sure that they are not invo
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:141 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:166
       Пояснение: Периодический экспорт выполняется последовательно в фоновом задании, но вызов СброситьБуфер() из основного потока может привести к конкурентному вызов
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       found → partial
       Текст: `Produce` MUST return a batch of Metric Points, filtered by the optional `metricFilter` parameter.
       Пояснение: Метод Произвести() возвращает массив (batch), но не принимает параметр metricFilter. Фильтрация применяется только к данным из Meter, а не из внешних 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       partial → not_found
       Текст: Implementation SHOULD use the filter as early as possible to gain as much performance gain possible 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:259 → -
       Пояснение: Метод Произвести() не принимает параметр фильтра, поэтому ранняя фильтрация невозможна.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       partial → not_found
       Текст: SDKs SHOULD return some failure for these calls, if possible.
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:88 → -
       Пояснение: СброситьБуфер() (Collect) является процедурой (void) без возвращаемого значения. После вызова Закрыть() повторный вызов СброситьБуфер() не возвращает 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       partial → not_found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:105 → -
       Пояснение: Метод Закрыть() является процедурой (void) и не возвращает информацию об успехе, ошибке или таймауте.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Propagators Distribution]
       found → partial
       Текст: The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST 
       Пояснение: W3C TraceContext and W3C Baggage propagators are maintained, but B3 propagator is not implemented in this codebase
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Propagators Distribution]
       found → partial
       Текст: The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST 
       Расположение: src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:1 → src/Пропагация/Классы/ОтелW3CПропагатор.os:1
       Пояснение: W3C TraceContext and W3C Baggage are distributed as part of core package (allowed by MAY clause), but B3 propagator is not distributed at all
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / ForceFlush()]
       found → partial
       Текст: The built-in SpanProcessors MUST do so.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:72 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:157
       Пояснение: Пакетный процессор корректно вызывает Экспортер.Экспортировать() и Экспортер.СброситьБуфер() при ForceFlush. Однако простой процессор (ОтелПростойПроц
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / OnEnding]
       partial → n_a
       Текст: The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking `
       Расположение: src/Трассировка/Классы/ОтелСпан.os:447 → -
       Пояснение: Ограничение платформы OneScript: нет механизма thread-local storage или goroutine-подобных гарантий изоляции. OneScript использует ФоновыеЗадания, кот
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Sampling]
       partial → not_found
       Текст: However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set.
       Расположение: src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37 → -
       Пояснение: SimpleSpanProcessor and BatchSpanProcessor export all spans received from the processor chain without checking the Sampled flag. RECORD_ONLY spans (Is
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Sampling]
       partial → not_found
       Текст: Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT re
       Расположение: src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:37 → -
       Пояснение: No filtering of non-sampled spans (Sampled=false, IsRecording=true) before the exporter. The processors pass all received spans to the exporter regard
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Tracer]
       found → not_found
       Текст: the `Tracer` MUST be updated to behave according to the new `TracerConfig`.
       Расположение: src/Трассировка/Классы/ОтелТрассировщик.os:178 → -
       Пояснение: Нет механизма обновления TracerConfigurator на провайдере после создания. Конфигуратор устанавливается только в конструкторе. Нет кода, который пересч
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / TracerConfig]
       found → partial
       Текст: However, the changes MUST be eventually visible.
       Расположение: src/Трассировка/Классы/ОтелТрассировщик.os:13 → src/Трассировка/Классы/ОтелТрассировщик.os:204
       Пояснение: Трассировщик читает Конфигурация.Включен() по ссылке, поэтому мутация объекта TracerConfig была бы видна. Но нет публичного механизма обновления Trace
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / `ForceFlush()`]
       found → partial
       Текст: `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using som
       Пояснение: Метод СброситьБуфер() существует, но в SDK отсутствует документация, рекомендующая вызывать ForceFlush только в необходимых случаях (FaaS и т.п.).
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (30) - требует перепроверки:

     [Baggage Api / Overview]
       not_found → found
       Текст: Language API MUST treat both baggage names and values as case sensitive.
       Код: src/Ядро/Классы/ОтелBaggage.os:3
       Было: ОтелBaggage stores entries in a plain Соответствие (Map) which in OneScript/1C is case-insensitive f
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Context / Attach Context]
       partial → found
       Текст: The API MUST accept the following parameters: * The `Context`.
       Код: src/Ядро/Модули/ОтелКонтекст.os:246
       Было: There is no generic Attach(Context) method accepting a Context object. Attach is implemented via spe
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Boolean]
       partial → found
       Текст: All Boolean environment variables SHOULD be named and defined such that false is the expected safe d
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:762
       Было: Единственная булева переменная OTEL_ENABLED имеет значение по умолчанию "true". По спецификации безо
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Api / Emit a LogRecord]
       n_a → found
       Текст: When only explicit Context is supported, this parameter SHOULD be required.
       Код: src/Логирование/Классы/ОтелЛоггер.os:76
       Было: The implementation supports implicit Context via ОтелКонтекст.Текущий(), so the condition 'When only
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Logger Creation]
       partial → found
       Текст: It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` (see API).
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:54
       Было: OneScript не поддерживает ограничение видимости конструкторов; Logger может быть создан напрямую чер
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Concurrency requirements]
       partial → found
       Текст: MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent u
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:29
       Было: Thread-safety IS implemented via СинхронизированнаяКарта for the meters cache, but the class/method 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Concurrency requirements]
       partial → found
       Текст: Meter - all methods MUST be documented that implementations need to be safe for concurrent use by de
       Код: src/Метрики/Классы/ОтелМетр.os:37
       Было: Thread-safety IS implemented via СинхронизированнаяКарта for instruments cache and descriptors, but 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Concurrency requirements]
       partial → found
       Текст: Instrument - all methods MUST be documented that implementations need to be safe for concurrent use 
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:45
       Было: Thread-safety IS implemented via СинхронизированнаяКарта for accumulators and attributes, but the cl
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Histogram operations]
       not_found → partial
       Текст: This API SHOULD be documented in a way to communicate to users that this value is expected to be non
       Код: src/Метрики/Классы/ОтелГистограмма.os:13
       Было: Документация метода Записать в ОтелГистограмма.os не упоминает, что значение должно быть неотрицател
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / AlignedHistogramBucketExemplarReservoir]
       partial → found
       Текст: and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucke
       Код: src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50
       Было: The implementation uses a last-seen strategy (replaces the exemplar on each measurement) instead of 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Concurrency requirements]
       partial → found
       Текст: MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:273
       Было: Meter creation uses СинхронизированнаяКарта (thread-safe map) for caching meters. However, the Закры
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Concurrency requirements]
       partial → found
       Текст: ExemplarReservoir - all methods MUST be safe to be called concurrently.
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:176
       Было: Uses СинхронизированнаяКарта for bucket storage and АтомарноеЧисло for measurement counters. However
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument advisory parameters]
       partial → found
       Текст: If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed
       Код: src/Метрики/Классы/ОтелМетр.os:693
       Было: Метод ПроверитьСовет выводит предупреждение через Лог.Предупреждение при невалидных типах advisory-п
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument description]
       partial → found
       Текст: If a description is not provided or the description is null, the Meter MUST treat it the same as an 
       Код: src/Метрики/Классы/ОтелМетр.os:52
       Было: Параметр Описание имеет значение по умолчанию "" (пустая строка), что корректно обрабатывает случай 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument enabled]
       partial → found
       Текст: The synchronous instrument `Enabled` MUST return `false` when either: The MeterConfig of the `Meter`
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:226
       Было: Метод Включен() корректно возвращает Ложь при MeterConfig.enabled=false (через разделяемый Атомарное
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument unit]
       partial → found
       Текст: If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit str
       Код: src/Метрики/Классы/ОтелМетр.os:53
       Было: Параметр ЕдиницаИзмерения имеет значение по умолчанию "" (пустая строка), что корректно обрабатывает
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       partial → found
       Текст: `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Код: src/Экспорт/Классы/ОтелHttpТранспорт.os:69
       Было: Export delegates to Транспорт.Отправить() which uses HTTP with default timeouts, but there is no exp
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       partial → found
       Текст: `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Код: src/Экспорт/Классы/ОтелHttpТранспорт.os:149
       Было: Export relies on HTTP transport timeouts implicitly, no explicit timeout limit with error result (Fa
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       partial → found
       Текст: Shutdown SHOULD be called only once for each `MetricExporter` instance.
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:53
       Было: Закрыть() uses АтомарноеБулево so multiple calls are safe, but subsequent Export calls return Ложь w
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter Creation]
       partial → found
       Текст: In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be ret
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:66
       Было: A working Meter is returned for empty string names, but null (Неопределено) would cause a type error
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: To construct a `MetricReader` when setting up an SDK, at least the following SHOULD be provided:
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:348
       Было: Constructor accepts exporter and interval, but does not directly accept optional aggregation functio
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       not_found → partial
       Текст: This function SHOULD be obtained from the `exporter`.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:352
       Было: The default output aggregation function is not obtained from the exporter. Aggregation is determined
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       not_found → partial
       Текст: If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include
       Код: src/Метрики/Классы/ОтелДанныеМетрики.os:42
       Было: ИнтерфейсПродюсерМетрик has no InstrumentationScope - the interface is a minimal stub with just Прои
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Specify Protocol]
       partial → found
       Текст: If they support only one, it SHOULD be `http/protobuf`.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563
       Было: SDK supports grpc and http/json but not true http/protobuf transport. The HTTP transport always send
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Detecting resource information from the environment]
       partial → found
       Текст: If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be a
       Код: src/Ядро/Классы/ОтелРесурс.os:43
       Было: Merge detects schema URL conflict and returns an empty resource (line 43), but does not report an er
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Span]
       partial → found
       Текст: However, alternative implementations MUST NOT allow callers to create `Span`s directly.
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:56
       Было: В OneScript конструкторы всегда публичные - нет механизма сокрытия конструктора (private/package-pri
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Span Creation]
       partial → found
       Текст: There MUST NOT be any API for creating a `Span` other than with a `Tracer`.
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:56
       Было: В OneScript конструкторы классов всегда публичные. Конструктор ОтелСпан доступен для вызова напрямую
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Additional Span Interfaces]
       partial → found
       Текст: implementations MAY choose not to expose (and store) the full parent Context of the Span but they MU
       Код: src/Трассировка/Классы/ОтелСпан.os:101
       Было: Only parent span ID is stored and exposed via ИдРодительскогоСпана(). The full parent SpanContext (t
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Configuration]
       partial → found
       Текст: Configuration (i.e., SpanProcessors, IdGenerator, SpanLimits, `Sampler`, and (Development) TracerCon
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:9
       Было: SpanProcessors, SpanLimits, Sampler и TracerConfigurator принадлежат TracerProvider, но IdGenerator 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Explicit randomness]
       not_found → found
       Текст: SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value.
       Код: src/Трассировка/Модули/ОтелСэмплер.os:157
       Было: The sampler module (ОтелСэмплер.os) does not handle the `rv` sub-key of OpenTelemetry TraceState at 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (17) - агент нашёл дополнительные:

     [Metrics Api] SHOULD found: The `unit` is an optional string provided by the author of the Instrument. The A
     [Trace Api] MUST found: The Span interface MUST provide:
     [Trace Api] SHOULD found: To help users avoid performing computationally expensive operations when creatin
     [Trace Api] MUST found: The Span interface MUST provide:
     [Trace Api] SHOULD partial: its `name` property SHOULD be set to an empty string,
     [Trace Api] SHOULD not_found: and a message reporting that the specified value is invalid SHOULD be logged.
     [Trace Api] MUST found: (result MUST be a 16-hex-character lowercase string).
     [Trace Api] MUST found: (result MUST be an 8-byte array).
     [Trace Api] MUST found: The Span interface MUST provide:
     [Trace Api] MUST found: The Span interface MUST provide:
     [Trace Api] SHOULD NOT found: and SHOULD NOT be overridable.
     [Trace Api] MUST found: and MUST follow the general error handling guidelines.
     [Trace Sdk] MUST not_found: and that the explicit randomness values MUST not be modified.
     [Trace Sdk] MUST found: name of the methods MUST be consistent with SpanContext
     [Trace Sdk] SHOULD partial: After the call to `Shutdown`, subsequent attempts to get a `Tracer` are not allo
     [Trace Sdk] SHOULD partial: SDKs SHOULD ignore these calls gracefully, if possible.
     [Trace Sdk] SHOULD partial: `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be i

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (17) - были раньше, теперь нет:

     [Metrics Api] SHOULD found: The API SHOULD treat it as an opaque string.
     [Trace Api] MUST found: The Span interface MUST provide: An API to record a single `Event` where the `Ev
     [Trace Api] SHOULD found: a `Tracer` SHOULD provide this `Enabled` API.
     [Trace Api] MUST found: The Span interface MUST provide: An API that returns the `SpanContext` for the g
     [Trace Api] SHOULD partial: In case an invalid name (null or empty string) is specified, a working Tracer im
     [Trace Api] SHOULD not_found: In case an invalid name (null or empty string) is specified, a working Tracer im
     [Trace Api] MUST found: Binary - returns the binary representation of the `TraceId` (result MUST be a 16
     [Trace Api] MUST found: Binary - returns the binary representation of the `TraceId` (result MUST be a 16
     [Trace Api] MUST found: The Span interface MUST provide: An API to set a single `Attribute` where the at
     [Trace Api] MUST found: The Span interface MUST provide: An API to set the `Status`.
     [Trace Api] SHOULD NOT found: This functionality MUST be fully implemented in the API, and SHOULD NOT be overr
     [Trace Api] MUST found: If invalid value is passed the operation MUST NOT return `TraceState` containing
     [Trace Sdk] MUST not_found: The calling CompositeSampler SHOULD update the threshold of the outgoing TraceSt
     [Trace Sdk] MUST partial: The SDK MAY provide this functionality by allowing custom implementations of an 
     [Trace Sdk] SHOULD partial: SDKs SHOULD return a valid no-op Tracer for these calls, if possible.
     [Trace Sdk] SHOULD partial: After the call to `Shutdown`, subsequent calls to `OnStart`, `OnEnd`, or `ForceF
     [Trace Sdk] SHOULD found: `ForceFlush` SHOULD complete or abort within some timeout.

  Итого изменений: 87
    Понижений: 23, Повышений: 30, Боковых: 0
    Новых req: 17, Пропущенных req: 17
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
