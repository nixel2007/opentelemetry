# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             669    638   -31 ⚠️  РЕГРЕССИЯ
  partial            80     93 +   13
  not_found          73     88 +   15 ⚠️  РЕГРЕССИЯ
  n_a                 2      5 +    3
  Всего             824    824 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (70) - требует перепроверки:

     [Env Vars / Boolean]
       found → partial
       Текст: Any value that represents a Boolean MUST be set to true only by the case-insensitive string "true", 
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:764 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:763-764
       Пояснение: The implementation uses НРег(Значение) = "true" which only accepts lowercase 'true', not case-insensitive as required by spec
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Boolean]
       found → not_found
       Текст: An implementation MUST NOT extend this definition and define additional values that are interpreted 
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:764 → -
       Пояснение: No explicit validation exists to prevent extension of true values - the current implementation accepts any non-'true' as false but doesn't enforce the
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Boolean]
       found → partial
       Текст: Any value not explicitly defined here as a true value, including unset and empty values, MUST be int
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:764 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:763-764
       Пояснение: Implementation treats non-'true' values as false but doesn't handle case-insensitive 'false' values correctly
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Boolean]
       found → not_found
       Текст: All Boolean environment variables SHOULD be named and defined such that false is the expected safe d
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:762 → -
       Пояснение: While OTEL_ENABLED defaults to true (safe behavior), there's no systematic approach to ensure all boolean variables follow this pattern
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Boolean]
       found → not_found
       Текст: Renaming or changing the default value MUST NOT happen without a major version upgrade.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:762 → -
       Пояснение: No versioning policy or protection mechanism exists to prevent breaking changes to environment variable names or defaults
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Environment Variable Specification]
       found → partial
       Текст: They SHOULD also follow the common configuration specification.
       Расположение: src/Ядро/Классы/ОтелПостроительSdk.os:73 → -
       Пояснение: The implementation reads environment variables through configor but doesn't implement all aspects of common configuration specification like programma
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / General SDK Configuration]
       found → not_found
       Текст: Values MUST be deduplicated in order to register a `Propagator` only once.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:468 → -
       Пояснение: Код для OTEL_PROPAGATORS есть в строке 446, но нет явной дедупликации пропагаторов - они просто добавляются в список без проверки дубликатов.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / General SDK Configuration]
       found → not_found
       Текст: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation 
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:800 → -
       Пояснение: Нет обработки OTEL_TRACES_SAMPLER_ARG в коде - переменная упоминается только в комментариях строка 18, но не читается и не валидируется.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / General SDK Configuration]
       found → not_found
       Текст: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation 
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:803 → -
       Пояснение: Нет обработки OTEL_TRACES_SAMPLER_ARG в коде - переменная упоминается только в комментариях строка 18, но не читается и не валидируется.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Numeric]
       found → not_found
       Текст: For new implementations, these should be treated as MUST requirements.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:797 → -
       Пояснение: This is a meta-requirement about treating SHOULD as MUST for new implementations - there's no explicit handling to enforce this distinction
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ReadWriteLogRecord]
       found → partial
       Текст: A function receiving this as an argument MUST additionally be able to modify the following informati
       Расположение: src/Логирование/Классы/ОтелЗаписьЛога.os:179 → src/Логирование/Классы/ОтелЗаписьЛога.os:179-347
       Пояснение: ОтелЗаписьЛога provides modification capabilities but there's no separate ReadWriteLogRecord interface as specified
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ReadableLogRecord]
       found → partial
       Текст: A function receiving this as an argument MUST be able to access all the information added to the Log
       Расположение: src/Логирование/Классы/ОтелЗаписьЛога.os:44 → src/Логирование/Классы/ОтелЗаписьЛога.os:45-153
       Пояснение: ОтелЗаписьЛога provides access to all information but there's no separate ReadableLogRecord interface as specified
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ReadableLogRecord]
       found → partial
       Текст: It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) assoc
       Расположение: src/Логирование/Классы/ОтелЗаписьЛога.os:141 → src/Логирование/Классы/ОтелЗаписьЛога.os:131-143
       Пояснение: ОтелЗаписьЛога provides access to scope and resource but there's no separate ReadableLogRecord interface as specified
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Compatibility requirements]
       found → not_found
       Текст: All the metrics components SHOULD allow new APIs to be added to existing components without introduc
       Расположение: src/Метрики/Классы/ОтелМетр.os:37 → -
       Пояснение: No explicit design or documentation found regarding adding new APIs without breaking changes. The current implementation doesn't show extensibility pa
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Compatibility requirements]
       found → partial
       Текст: All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introdu
       Расположение: src/Метрики/Классы/ОтелМетр.os:51 → src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21
       Пояснение: Some methods use optional parameters (e.g., Атрибуты = Неопределено, Контекст = Неопределено), but there's no systematic design to ensure all APIs can
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Histogram operations]
       found → partial
       Текст: This API SHOULD NOT validate this value, that is left to implementations of the API.
       Расположение: src/Метрики/Классы/ОтелГистограмма.os:21 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:88-91
       Пояснение: The API validates that the value is a number type but doesn't validate non-negative values as required by spec
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Instrument unit]
       found → partial
       Текст: It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII string.
       Пояснение: Unit string is stored as-is without modification, but descriptor conflict comparison at line 613 uses OneScript's `<>` operator which is case-insensit
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Therefore, this API MUST be structured to accept a variable number of `callback` functions, includin
       Расположение: src/Метрики/Классы/ОтелМетр.os:232 → src/Метрики/Классы/ОтелМетр.os:242
       Пояснение: API принимает только 0 или 1 callback при создании (Callback = Неопределено), а не произвольное число. Добавление дополнительных callback возможно чер
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API MUST support creation of asynchronous instruments by passing zero or more `callback` functio
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:155 → src/Метрики/Классы/ОтелМетр.os:242
       Пояснение: API создания принимает максимум один callback. Передача нескольких callback при создании не поддерживается - только через ДобавитьCallback после созда
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Callback functions MUST be documented as follows for the end user:
       Расположение: src/Метрики/Классы/ОтелНаблюдениеМетрики.os:46 → src/Метрики/Классы/ОтелНаблюдениеМетрики.os:59
       Пояснение: Есть базовая документация использования callback в комментариях ОтелНаблюдениеМетрики, но не задокументированы конкретные требования спецификации: рее
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / AlignedHistogramBucketExemplarReservoir]
       found → partial
       Текст: and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucke
       Пояснение: Implementation uses last-seen strategy (replaces previous exemplar) instead of uniformly-weighted sampling algorithm for bucket sampling.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Defaults and configuration]
       found → partial
       Текст: The SDK MUST provide configuration according to the SDK environment variables specification.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:77 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:16
       Пояснение: SDK читает OTEL_METRICS_EXPORTER, OTEL_METRICS_EXEMPLAR_FILTER и OTEL_EXPORTER_OTLP_METRICS_* переменные окружения, но OTEL_METRIC_EXPORT_INTERVAL и O
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Exemplar]
       found → not_found
       Текст: If `Exemplar` sampling is off, the SDK MUST NOT have overhead related to exemplar sampling.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:374 → -
       Пояснение: No conditional exemplar sampling logic found that avoids overhead when sampling is disabled.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Exemplar]
       found → partial
       Текст: A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation.
       Расположение: src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:1 → src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:41-47
       Пояснение: ExemplarReservoir exists but no clear integration with aggregation configuration (e.g., histogram bucket boundaries) is visible.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Exemplar defaults]
       found → partial
       Текст: All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:290 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:188
       Пояснение: SimpleFixedSizeExemplarReservoir is created by default for synchronous instruments, but not all aggregation types are explicitly configured to use it 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ExemplarFilter]
       found → partial
       Текст: The filter configuration SHOULD follow the environment variable specification.
       Расположение: src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114 → src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:104
       Пояснение: OTEL_METRICS_EXEMPLAR_FILTER is read but only in MeterProviderBuilder, not in auto-configuration module. Full environment variable specification suppo
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       found → n_a
       Текст: Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`
       Расположение: src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:63 → -
       Пояснение: OneScript uses System.Decimal, not IEEE 754, so non-normal values like NaN and Infinity are not possible
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       partial → n_a
       Текст: The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic 
       Расположение: src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:302 → -
       Пояснение: This requirement is specific to exponential histograms, which may not be implemented in the basic metrics SDK
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       found → partial
       Текст: Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possi
       Расположение: src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:157 → src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:1
       Пояснение: Exponential histogram aggregator exists but dynamic scale adjustment logic is not fully implemented
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument advisory parameter: `ExplicitBucketBoundaries`]
       found → partial
       Текст: If no View matches, or if a matching View selects the default aggregation, the `ExplicitBucketBounda
       Расположение: src/Метрики/Классы/ОтелМетр.os:584 → src/Метрики/Классы/ОтелМетр.os:697-700,554-584
       Пояснение: Advisory parameters including boundaries are validated and stored, but specific logic for using ExplicitBucketBoundaries when no view matches or defau
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument advisory parameters]
       found → partial
       Текст: If both a View and advisory parameters specify the same aspect of the Stream configuration, the sett
       Расположение: src/Метрики/Классы/ОтелМетр.os:565 → src/Метрики/Классы/ОтелМетр.os:554-584
       Пояснение: Views are applied to instruments but the precedence logic for advisory parameters vs views is not explicitly implemented - views simply override throu
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument enabled]
       found → partial
       Текст: The synchronous instrument `Enabled` MUST return `false` when either: The MeterConfig of the `Meter`
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:226 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:231-232
       Пояснение: Enabled method exists and considers both meter enabled state and instrument enabled state, but specific logic for drop aggregation views is not implem
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument selection criteria]
       found → partial
       Текст: If the SDK does not support wildcards in general, it MUST still recognize the special single asteris
       Пояснение: Only single asterisk '*' is supported for matching all instruments, but no general wildcard pattern matching with '?' or other patterns is implemented
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Interface Definition]
       found → not_found
       Текст: The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily 
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:29 → -
       Пояснение: SDK реализует retry-логику в транспортном слое: ОтелHttpТранспорт и ОтелGrpcТранспорт используют СтратегияПовтора с экспоненциальной задержкой, что пр
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Measurement processing]
       found → not_found
       Текст: Instrument advisory parameters, if any, MUST be honored.
       Расположение: src/Метрики/Классы/ОтелМетр.os:527 → -
       Пояснение: Advisory parameters from instruments are partially used but no systematic honoring of all advisory parameters
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Measurement processing]
       found → not_found
       Текст: If both a View and Instrument advisory parameters specify the same aspect of the Stream configuratio
       Расположение: src/Метрики/Классы/ОтелМетр.os:524 → -
       Пояснение: No systematic precedence logic found between View settings and instrument advisory parameters
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Measurement processing]
       found → not_found
       Текст: If the Instrument could not match with any of the registered `View`(s), the SDK SHOULD enable the in
       Расположение: src/Метрики/Классы/ОтелМетр.os:48 → -
       Пояснение: No explicit handling found for instruments that don't match any registered Views
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter Creation]
       found → partial
       Текст: It SHOULD only be possible to create `Meter` instances through a `MeterProvider` (see API).
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:56 → src/Метрики/Классы/ОтелПостроительМетра.os:63
       Пояснение: Meter creation is implemented through MeterProvider.ПолучитьМетр() and MeterBuilder.Построить(), but the Meter class constructor is public allowing di
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → not_found
       Текст: The SDK SHOULD provide a way to allow `MetricReader` to respond to MeterProvider.ForceFlush and Mete
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:92 → -
       Пояснение: No explicit ForceFlush/Shutdown callbacks or interfaces found in MetricReader implementations for MeterProvider events.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Numerical limits handling]
       not_found → n_a
       Текст: If the SDK receives float/double values from Instruments, it MUST handle all the possible values.
       Пояснение: OneScript использует System.Decimal (не IEEE 754): NaN, Infinity, отрицательный ноль невозможны - операции выбрасывают исключение. Платформа не поддер
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → not_found
       Текст: Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:157 → -
       Пояснение: Callbacks are invoked globally, not specific to individual MetricReaders during collection
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → not_found
       Текст: The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered ca
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:58 → -
       Пояснение: No validation found to disregard asynchronous instrument API usage outside callbacks
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       found → not_found
       Текст: The implementation MUST complete the execution of all callbacks for a given instrument before starti
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:157 → -
       Пояснение: No synchronization logic found to ensure all callbacks complete before next collection
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       partial → not_found
       Текст: `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`.
       Расположение: src/Метрики/Классы/ОтелДанныеМетрики.os:42 → -
       Пояснение: Интерфейс продюсера не включает InstrumentationScope для идентификации самого MetricProducer - возвращаемые данные метрик содержат scope от Meter, а н
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       found → not_found
       Текст: For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp,
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:145 → -
       Пояснение: No delta aggregation start timestamp management found according to collection intervals
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       found → not_found
       Текст: This implies that all data points with delta temporality aggregation for an instrument MUST share th
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:283 → -
       Пояснение: No logic found to ensure consistent start timestamps for delta temporality data points
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       found → not_found
       Текст: Cumulative timeseries MUST use a consistent start timestamp for all collection intervals.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141 → -
       Пояснение: No consistent start timestamp management found for cumulative timeseries
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       partial → not_found
       Текст: For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:263 → -
       Пояснение: Start timestamps use current time, not the time of first measurement
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       partial → not_found
       Текст: For asynchronous instrument, the start timestamp SHOULD be:
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:184 → -
       Пояснение: Asynchronous instruments use current time for start timestamp, not the logic described in the specification
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → not_found
       Текст: `name`: The metric stream name that SHOULD be used.
       Расположение: src/Метрики/Классы/ОтелПредставление.os:29 → -
       Пояснение: ОтелПредставление has НовоеИмя field but no usage documentation or validation for stream naming
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → not_found
       Текст: In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector tha
       Расположение: src/Метрики/Классы/ОтелСелекторИнструментов.os:159 → -
       Пояснение: No validation logic found to ensure single instrument selection when name is provided
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → not_found
       Текст: If the user does not provide a `name` value, name from the Instrument the View matches MUST be used 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:230 → -
       Пояснение: No logic found to apply instrument name as default when view name is not provided
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → not_found
       Текст: `description`: The metric stream description that SHOULD be used.
       Расположение: src/Метрики/Классы/ОтелПредставление.os:38 → -
       Пояснение: ОтелПредставление has НовоеОписание field but no usage documentation for stream description
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → not_found
       Текст: If the user does not provide a `description` value, the description from the Instrument a View match
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:233 → -
       Пояснение: No logic found to apply instrument description as default when view description is not provided
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       partial → not_found
       Текст: If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggreg
       Расположение: src/Метрики/Классы/ОтелМетр.os:48 → -
       Пояснение: Default aggregation is handled by instrument type, but not configurable per MetricReader instance
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Synchronous instrument cardinality limits]
       found → not_found
       Текст: Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attr
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:141 → -
       Пояснение: Implementation does not distinguish between cumulative and delta temporality for cardinality overflow handling - uses generic overflow behavior for al
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → partial
       Текст: The option SHOULD accept any form allowed by the underlying gRPC client implementation.
       Расположение: src/Экспорт/Классы/ОтелGrpcТранспорт.os:146 → src/Экспорт/Классы/ОтелGrpcТранспорт.os:137
       Пояснение: gRPC transport accepts address as string but doesnt expose all underlying gRPC client configuration options
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → not_found
       Текст: If the gRPC client implementation does not support an endpoint with a scheme of `http` or `https` th
       Расположение: src/Экспорт/Классы/ОтелGrpcТранспорт.os:174 → -
       Пояснение: No URL scheme transformation logic found in gRPC transport
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Specify Protocol]
       found → not_found
       Текст: If they support only one, it SHOULD be `http/protobuf`.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563 → -
       Пояснение: SDK supports grpc and http/json, not http/protobuf as preferred
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Detecting resource information from the environment]
       found → partial
       Текст: Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attrib
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:117 → src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:19
       Пояснение: Detectors set schema URL before attempting attribute detection. If detection fails (exception), the resource still has a non-empty schema URL despite 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Retrieving the TraceId and SpanId]
       found → partial
       Текст: The API SHOULD NOT expose details about how they are internally stored.
       Расположение: src/Трассировка/Классы/ОтелКонтекстСпана.os:4 → src/Трассировка/Классы/ОтелКонтекстСпана.os:84
       Пояснение: Binary getters (ИдТрассировкиВДвоичномВиде, ИдСпанаВДвоичномВиде) return the internal ДвоичныеДанные directly, exposing the internal storage format. H
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Explicit randomness]
       found → not_found
       Текст: SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value.
       Расположение: src/Трассировка/Модули/ОтелСэмплер.os:157 → -
       Пояснение: The codebase does not implement explicit randomness handling. The TraceState implementation in ОтелСостояниеТрассировки.os does not check for or prese
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Id Generators]
       found → partial
       Текст: name of the methods MUST be consistent with SpanContext
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:214 → src/Ядро/Модули/ОтелУтилиты.os:57
       Пояснение: The IdGenerator interface uses Russian method names СгенерироватьИдТрассировки() and СгенерироватьИдСпана() instead of generateTraceIdBytes() and gene
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Presumption of TraceID randomness]
       partial → not_found
       Текст: For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Contex
       Расположение: src/Трассировка/Модули/ОтелСэмплер.os:290 → -
       Пояснение: The sampler implementation in ОтелСэмплер.os does not check for explicit randomness values in the 'rv' sub-key of TraceState. It operates assuming all
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Span Limits]
       found → partial
       Текст: The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`.
       Пояснение: The class has МаксСобытий() and МаксЛинков() methods but uses Russian names instead of the specified English names EventCountLimit and LinkCountLimit.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Span Limits]
       found → partial
       Текст: The options MAY be bundled in a class, which then SHOULD be called `SpanLimits`.
       Пояснение: The class exists as ОтелЛимитыСпана but uses Russian naming instead of the specified English name SpanLimits.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Span Limits]
       found → not_found
       Текст: There SHOULD be a message printed in the SDK's log to indicate to the user that an attribute, event,
       Расположение: src/Трассировка/Классы/ОтелСпан.os:480 → -
       Пояснение: No logging implementation found for when limits are exceeded and items are discarded. The ОтелЛимитыСпана class only provides configuration but no enf
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Span Limits]
       found → not_found
       Текст: To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per disca
       Расположение: src/Трассировка/Классы/ОтелСпан.os:481 → -
       Пояснение: No logging implementation found for limit violations. There's no code to log when attributes, events, or links are discarded due to limits, and no mec
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / TraceID randomness]
       found → partial
       Текст: For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trac
       Расположение: src/Ядро/Модули/ОтелУтилиты.os:78 → src/Ядро/Модули/ОтелУтилиты.os:78-92
       Пояснение: TraceIDs are generated using UUID v4 (Новый УникальныйИдентификатор()), which provides 122 random bits out of 128. However, UUID v4 has fixed version 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / TracerConfig]
       found → partial
       Текст: The value of `enabled` MUST be used to resolve whether a `Tracer` is Enabled. If `enabled` is `false
       Пояснение: When enabled is false, Включен() correctly returns false. However, when enabled is true (or no config), Включен() returns Провайдер.Процессор().ЕстьПр
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (48) - требует перепроверки:

     [Logs Api / Enabled]
       partial → found
       Текст: The API SHOULD be documented that instrumentation authors needs to call this API each time they emit
       Код: src/Логирование/Классы/ОтелЛоггер.os:28
       Было: Метод Включен() задокументирован, но документация не упоминает, что результат может меняться со врем
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Enabled]
       partial → found
       Текст: `Enabled` MUST return `false` when either: there are no registered `LogRecordProcessors`; `Logger` i
       Код: src/Логирование/Классы/ОтелЛоггер.os:42-62
       Было: Включен() handles most conditions (no processors, disabled config, severity filtering, trace-based f
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       not_found → partial
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71
       Было: СброситьБуфер (ForceFlush) is implemented as Процедура (void) with no return value in all processor 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Logger]
       partial → found
       Текст: If the `LoggerProvider` supports updating the LoggerConfigurator, then upon update the `Logger` MUST
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:213-217
       Было: Logger has УстановитьКонфигурацию setter method, but LoggerProvider does not have a public method to
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Logger Creation]
       not_found → found
       Текст: In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be 
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:60
       Было: Код не проверяет пустое или null имя логгера и не логирует диагностическое предупреждение о невалидн
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ShutDown]
       not_found → partial
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:57
       Было: Закрыть (Shutdown) is implemented as Процедура (void) with no return value in all processor implemen
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Counter operations]
       partial → found
       Текст: The increment value is expected to be non-negative. This API SHOULD be documented in a way to commun
       Код: src/Метрики/Классы/ОтелСчетчик.os:17
       Было: The method comment mentions 'положительное значение для добавления' but does not explicitly phrase i
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Histogram operations]
       partial → found
       Текст: This API SHOULD be documented in a way to communicate to users that this value is expected to be non
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:88-91
       Было: Documentation comment says 'измеренное значение' but does not mention non-negative expectation
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Instrument]
       n_a → found
       Текст: Language-level features such as the distinction between integer and floating point numbers SHOULD be
       Код: src/Метрики/Классы/ОтелМетр.os:63
       Было: OneScript has a single numeric type (Число) with no language-level distinction between integer and f
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       not_found → partial
       Текст: The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to con
       Код: src/Метрики/Классы/ОтелМетр.os:43
       Было: API documentation for sync instrument creation methods does not explicitly mention that the name mus
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       not_found → partial
       Текст: The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to con
       Код: src/Метрики/Классы/ОтелМетр.os:231
       Было: API documentation for async instrument creation methods does not explicitly mention that the name mu
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Collect]
       not_found → partial
       Текст: `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:240-259
       Было: Метод СобратьИЭкспортировать() - это Процедура (void), не возвращает результата вызывающему коду. Пу
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Configuration]
       partial → found
       Текст: A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardi
       Код: src/Метрики/Классы/ОтелПредставление.os:93
       Было: ОтелПредставление has ЛимитМощностиАгрегации field, but ПрименитьПредставлениеКИнструменту in ОтелМе
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Configuration]
       not_found → partial
       Текст: If there is no matching view, but the `MetricReader` defines a default cardinality limit value based
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:251
       Было: ОтелПериодическийЧитательМетрик does not define a per-instrument-type default cardinality limit; the
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Custom ExemplarReservoir]
       partial → found
       Текст: although individual reservoirs MUST still be instantiated per metric-timeseries
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:188
       Было: Кастомный резервуар из View применяется к инструменту целиком (src/Метрики/Классы/ОтелМетр.os:579-58
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       partial → found
       Текст: The emitted warning SHOULD include information for the user on how to resolve the conflict, if possi
       Код: src/Метрики/Классы/ОтелМетр.os:1000
       Было: Warning message reports the conflicting parameters but does not include specific instructions on how
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       partial → found
       Текст: Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Met
       Код: src/Метрики/Классы/ОтелМетр.os:1000
       Было: A warning is emitted, but the code returns the existing instrument instance rather than reporting bo
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarReservoir]
       partial → found
       Текст: A new `ExemplarReservoir` MUST be created for every known timeseries data point, as determined by ag
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:188
       Было: Один резервуар создается на инструмент, а не на каждую серию (timeseries). Внутри резервуар ключует 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarReservoir]
       partial → found
       Текст: The "offer" method SHOULD accept measurements, including: The `value` of the measurement, the comple
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:34-40
       Было: Метод Предложить() принимает Значение и АтрибутыИзмерения, но вместо полного Context (с Baggage) при
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarReservoir]
       partial → found
       Текст: The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars.
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:1-2
       Было: Метод СоздатьЭкземпляр() создает новый объект Соответствие для каждого экземпляра при каждом вызове 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       not_found → found
       Текст: This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpD
       Код: src/Метрики/Классы/ОтелАгрегаторГистограммы.os:1
       Было: The histogram aggregator always collects the sum field (ОтелАгрегаторГистограммы.Записать line 51). 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       partial → found
       Текст: SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good
       Код: src/Метрики/Классы/ОтелАгрегаторГистограммы.os:1
       Было: Default boundaries are used when none provided, but the values [0, 5, 10, 25, 50, 75, 100, 250, 500,
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter]
       not_found → found
       Текст: If the `MeterProvider` supports updating the MeterConfigurator, then upon update the `Meter` MUST be
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:221
       Было: ОтелПровайдерМетрик does not support updating the MeterConfigurator after creation; the Конфигуратор
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: This function SHOULD be obtained from the `exporter`.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:262-266
       Было: Агрегация по умолчанию задается как параметр конструктора читателя (НоваяАгрегацияГистограмм), а не 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NOT introduce side-effects
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:250-256
       Было: При ручном flush (СброситьБуфер) побочные эффекты минимизируются - все кроме последнего читателя экс
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       not_found → found
       Текст: The SDK MUST NOT allow a `MetricReader` instance to be registered on more than one `MeterProvider` i
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:197-200
       Было: Нет валидации при регистрации читателя. Метод ЗарегистрироватьЧитатель() в построителе просто добавл
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Numerical limits handling]
       not_found → partial
       Текст: The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry.
       Было: В коде SDK метрик нет явной обработки числовых пределов (переполнение, граничные значения). Агрегато
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Periodic exporting MetricReader]
       partial → found
       Текст: The reader MUST synchronize calls to `MetricExporter`'s `Export` to make sure that they are not invo
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:242
       Было: Периодический экспорт выполняется последовательно в фоновом задании, но вызов СброситьБуфер() из осн
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       partial → found
       Текст: `Produce` MUST return a batch of Metric Points, filtered by the optional `metricFilter` parameter.
       Код: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13
       Было: Метод Произвести() возвращает массив (batch), но не принимает параметр metricFilter. Фильтрация прим
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       not_found → partial
       Текст: Implementation SHOULD use the filter as early as possible to gain as much performance gain possible 
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:366
       Было: Метод Произвести() не принимает параметр фильтра, поэтому ранняя фильтрация невозможна.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       not_found → partial
       Текст: `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:370
       Было: Метод Произвести() возвращает массив и не предоставляет структурированного способа сообщить об успех
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: Additionally, implementations SHOULD support configuring an exclude-list of attribute keys.
       Код: src/Метрики/Классы/ОтелПредставление.os:9
       Было: ОтелПредставление has ИсключенныеКлючиАтрибутов field defined in the constructor and getter, but the
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all oth
       Код: src/Метрики/Классы/ОтелМетр.os:575
       Было: ОтелПредставление defines ИсключенныеКлючиАтрибутов but ОтелМетр.ПрименитьПредставлениеКИнструменту 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all oth
       Код: src/Метрики/Классы/ОтелМетр.os:575
       Было: Same as above - the exclude-list is defined in ОтелПредставление but never applied, so the 'keep all
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST appl
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:251
       Было: Default cardinality limit of 2000 is hardcoded in ОтелБазовыйСинхронныйИнструмент and ОтелМетр. The 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Inject]
       not_found → found
       Текст: MUST provide configuration to change the default injection format to B3 multi-header
       Код: src/Пропагация/Классы/ОтелB3Пропагатор.os:198
       Было: Класс ОтелB3Пропагатор не предоставляет конфигурации для переключения между single-header и multi-he
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Enabled]
       not_found → partial
       Текст: The API SHOULD be documented that instrumentation authors needs to call this API each time they crea
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:31
       Было: Документация метода Включен() не содержит указания о том, что авторы инструментирования должны вызыв
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Get a Tracer]
       partial → found
       Текст: In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:68
       Было: ПолучитьТрассировщик принимает ИмяБиблиотеки и вернёт рабочий трассировщик даже с пустым именем (не 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Get a Tracer]
       not_found → found
       Текст: In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:70
       Было: Нет явной проверки на невалидное имя и принудительной установки его в пустую строку - ОбластьИнструм
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Get a Tracer]
       not_found → found
       Текст: In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:69
       Было: Нет логирования сообщения о невалидном имени - в коде ПолучитьТрассировщик отсутствует вызов логгера
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Span]
       partial → found
       Текст: alternative implementations MUST NOT allow callers to create `Span`s directly.
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:56
       Было: OneScript does not support private constructors or access modifiers. ОтелСпан constructor is technic
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Span Creation]
       partial → found
       Текст: There MUST NOT be any API for creating a `Span` other than with a `Tracer`.
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:56
       Было: OneScript does not support private constructors or access modifiers. ОтелСпан constructor is technic
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Span Creation]
       partial → found
       Текст: This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`.
       Код: src/Трассировка/Классы/ОтелПостроительСпана.os:33
       Было: ОтелПостроительСпана.УстановитьРодителя() correctly accepts only Context (Соответствие) and rejects 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush()]
       not_found → partial
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:66
       Было: Методы СброситьБуфер являются процедурами (void) без возвращаемого значения - нет способа сообщить в
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown()]
       not_found → partial
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:77
       Было: Методы Закрыть являются процедурами (void) без возвращаемого значения - нет способа сообщить вызываю
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Tracer]
       not_found → found
       Текст: If the `TracerProvider` supports updating the TracerConfigurator, then upon update the `Tracer` MUST
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:154
       Было: Нет механизма обновления TracerConfigurator на провайдере после создания. Конфигуратор устанавливает
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / TracerConfig]
       partial → found
       Текст: If a `Tracer` is disabled, it MUST behave equivalently to a No-op Tracer.
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:57
       Было: Метод Включен() возвращает Ложь при отключённом трассировщике, но методы создания спанов (НачатьСпан
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / TracerConfig]
       partial → found
       Текст: However, the changes MUST be eventually visible.
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:191
       Было: Трассировщик читает Конфигурация.Включен() по ссылке, поэтому мутация объекта TracerConfig была бы в
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (27) - агент нашёл дополнительные:

     [Env Vars] SHOULD partial: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD partial: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD partial: It SHOULD NOT be supported by new implementations.
     [Env Vars] MUST not_found: Invalid or unrecognized input MUST be logged
     [Env Vars] SHOULD found: For variables accepting a numeric value, if the user provides a value the implem
     [Logs Api] SHOULD found: a Logger SHOULD provide this Enabled API.
     [Metrics Api] MAY found: This MAY be called CreateObservableCounter.
     [Metrics Api] SHOULD found: synchronous instruments SHOULD provide this `Enabled` API.
     [Metrics Api] MUST NOT found: this API needs to be structured to accept a `schema_url`, but MUST NOT obligate 
     [Metrics Api] SHOULD found: The API SHOULD treat it as an opaque string.
     [Metrics Api] SHOULD partial: The API to register a new Callback SHOULD accept: A list (or tuple, etc.) of Ins
     [Metrics Sdk] MUST found: This extension MUST be configurable on a metric View, although individual reserv
     [Metrics Sdk] MAY found: The "offer" method MAY accept a filtered subset of `Attributes` which diverge fr
     [Metrics Sdk] MUST n_a: Implementations are REQUIRED to accept the entire normal range of IEEE floating 
     [Metrics Sdk] SHOULD found: its `name` SHOULD keep the original invalid value
     [Metrics Sdk] SHOULD found: a message reporting that the specified value is invalid SHOULD be logged.
     [Metrics Sdk] SHOULD found: The default output `aggregation` (optional), a function of instrument kind. This
     [Metrics Sdk] SHOULD partial: If no size configuration is provided, the default size MAY be the number of poss
     [Otlp Exporter] MUST found: The implementation MUST honor the following URL components: scheme (`http` or `h
     [Propagators] MUST NOT found: the implementation MUST NOT throw an exception
     ... и ещё 7

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (27) - были раньше, теперь нет:

     [Env Vars] SHOULD NOT found: It is a deprecated value left for backwards compatibility. It SHOULD NOT be supp
     [Env Vars] SHOULD NOT found: It is a deprecated value left for backwards compatibility. It SHOULD NOT be supp
     [Env Vars] SHOULD NOT found: It is a deprecated value left for backwards compatibility. It SHOULD NOT be supp
     [Env Vars] MUST found: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e.
     [Env Vars] SHOULD found: The following paragraph was added after stabilization and the requirements are t
     [Logs Api] SHOULD found: To help users avoid performing computationally expensive operations when generat
     [Metrics Api] MUST found: The API MUST treat observations from a single callback as logically taking place
     [Metrics Api] SHOULD found: To help users avoid performing computationally expensive operations when recordi
     [Metrics Api] MUST found: Users can provide a `schema_url`, but it is up to their discretion. Therefore, t
     [Metrics Api] SHOULD found: The `unit` is an optional string provided by the author of the Instrument. The A
     [Metrics Api] SHOULD found: The API to register a new Callback SHOULD accept:
     [Metrics Sdk] MUST found: This extension MUST be configurable on a metric View
     [Metrics Sdk] MUST found: This MUST be clearly documented in the API and the reservoir MUST be given the `
     [Metrics Sdk] SHOULD found: When the histogram contains not more than one value in either of the positive or
     [Metrics Sdk] SHOULD found: In the case where an invalid `name` (null or empty string) is specified, a worki
     [Metrics Sdk] SHOULD not_found: In the case where an invalid `name` (null or empty string) is specified, a worki
     [Metrics Sdk] SHOULD found: This function SHOULD be obtained from the `exporter`.
     [Metrics Sdk] SHOULD found: Otherwise, a default size of `1` SHOULD be used.
     [Otlp Exporter] MUST found: The implementation MUST honor the following URL components:
     [Propagators] MUST NOT found: the implementation MUST NOT throw an exception and MUST NOT store a new value in
     ... и ещё 7

  Итого изменений: 172
    Понижений: 70, Повышений: 48, Боковых: 0
    Новых req: 27, Пропущенных req: 27
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
