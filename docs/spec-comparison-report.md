# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             750    750     0
  partial            42     42     0
  not_found          30     28    -2
  n_a                18     20 +    2
  Всего             840    840 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (28) - требует перепроверки:

     [Env Vars / Boolean]
       found → partial
       Текст: Any value not explicitly defined here as a true value, including unset and empty values, MUST be int
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:938 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:952
       Пояснение: БезопасноеБулево возвращает значение по умолчанию (Умолчание), а не жёстко false, при невалидном значении. На практике вызовы (Отключён) передают Ложь
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Declarative configuration]
       found → partial
       Текст: When `OTEL_CONFIG_FILE` is set, all other environment variables besides those referenced in the conf
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:95 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:97
       Пояснение: Когда OTEL_CONFIG_FILE задана, выполняется ОтелФайловаяКонфигурация.Разобрать + ОтелКонфигурационнаяФабрика.Создать без обращения к остальным OTEL_* п
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Enum]
       found → partial
       Текст: For sources accepting an enum value, if the user provides a value the implementation does not recogn
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:318 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:320
       Пояснение: Предупреждение для нераспознанных значений выводится для otel.traces.sampler (стр. 320) и otel.propagators (стр. 562), но в СоздатьПровайдерТрассировк
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / General SDK Configuration]
       found → partial
       Текст: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation 
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:919 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:298
       Пояснение: БезопасноеЧисло логирует и применяет значение по умолчанию (1.0) при невалидном otel.traces.sampler.arg, что эквивалентно поведению как если бы переме
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / General SDK Configuration]
       found → partial
       Текст: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation 
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:919 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:298
       Пояснение: Невалидный otel.traces.sampler.arg для traceidratio/parentbased_traceidratio логируется и заменяется на 1.0 (через БезопасноеЧисло). Но для прочих тип
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / General SDK Configuration]
       found → partial
       Текст: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation 
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:921 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:300
       Пояснение: БезопасноеЧисло возвращает значение по умолчанию (1.0) при невалидном arg, что соответствует «as if not set». Но это применяется только к ratio-сэмпле
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Numeric]
       found → n_a
       Текст: The following paragraph was added after stabilization and the requirements are thus qualified as "SH
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:915 → -
       Пояснение: Мета-требование о статусе требований в спецификации (квалификация SHOULD vs MUST), а не функциональное требование к коду.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Api / Enabled]
       found → partial
       Текст: The API SHOULD be documented that instrumentation authors needs to call this API each time they emit
       Пояснение: Документирующий комментарий описывает назначение Включен() как hot-path оптимизацию и упоминает, что значение может меняться со временем ("По умолчани
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Built-in processors]
       found → partial
       Текст: Additional processors defined in this document SHOULD be provided by SDK packages.
       Расположение: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:1 → src/Логирование/Классы/
       Пояснение: Реализованы Simple и Batch процессоры, но дополнительный процессор Event-to-span event bridge (определённый в этом же документе спецификации) не реали
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Counter creation]
       found → n_a
       Текст: There MUST NOT be any API for creating a `Counter` other than with a `Meter`.
       Расположение: src/Метрики/Классы/ОтелМетр.os:59 → -
       Пояснение: OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен), поэтому невозможно структурно запретить создание ОтелСчетчик на
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Enabled]
       found → partial
       Текст: The API SHOULD be documented that instrumentation authors needs to call this API each time they reco
       Пояснение: Метод Включен() имеет документирующий комментарий, но в нём не указано явно, что нужно вызывать этот API перед каждым измерением для получения самого 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → n_a
       Текст: MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:100 → -
       Пояснение: OneScript использует ФоновыеЗадания (background jobs), а не goroutine/thread-local concurrency. Платформа не поддерживает разделяемую память между пот
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → n_a
       Текст: ExemplarReservoir - all methods MUST be safe to be called concurrently.
       Расположение: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:98 → -
       Пояснение: OneScript использует ФоновыеЗадания (background jobs), без разделяемой памяти между потоками. Concurrency-safety неприменим на уровне платформы.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → n_a
       Текст: MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:50 → -
       Пояснение: OneScript использует ФоновыеЗадания, а не shared-memory многопоточность. Платформенное ограничение - concurrency-safety на уровне goroutine/thread неп
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Concurrency requirements]
       found → n_a
       Текст: MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:14 → -
       Пояснение: OneScript использует ФоновыеЗадания, без разделяемой памяти. Concurrency-safety неприменим на уровне платформы.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Exemplar defaults]
       found → partial
       Текст: All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:335 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:331
       Пояснение: По умолчанию у синхронного инструмента ставится ОтелФабрикаПростыхРезервуаров(1), но не для всех видов агрегации существует автоматическое назначение 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` MAY skip `Export(batch)` calls if the timeout is already expired, but SHOULD still call
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:201 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:194
       Пояснение: При неудаче СброситьБуфер (включая таймаут) функция возвращается раньше (строки 194-199) и не вызывает Экспортер.ПринудительноВыгрузитьСРезультатом, ч
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Interface Definition]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Пояснение: ПринудительноВыгрузитьСРезультатом принимает ТаймаутМс, но в синхронном экспортёре параметр помечен UnusedParameters-off и фактически не применяется (
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Measurement processing]
       found → partial
       Текст: If applying the View results in conflicting metric identities the implementation SHOULD apply the Vi
       Расположение: src/Метрики/Классы/ОтелМетр.os:1044 → src/Метрики/Классы/ОтелМетр.os:1069
       Пояснение: ПроверитьКонфликтИменView эмитит предупреждение и применяет View только для случая 'wide selector + НовоеИмя'. Прочие сценарии конфликта identities (о
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Measurement processing]
       partial → not_found
       Текст: If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asy
       Расположение: src/Метрики/Модули/ОтелАгрегация.os:144 → -
       Пояснение: Нет проверки совместимости агрегации с типом инструмента: ОпределитьАгрегаторИзПредставления возвращает агрегатор как есть (например, ОтелАгрегаторГис
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: If not configured, the Cumulative temporality SHOULD be used.
       Расположение: src/Метрики/Модули/ОтелСелекторВременнойАгрегации.os:24 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:362-366
       Пояснение: Reader не имеет собственного хранения temporality селектора с дефолтом Cumulative; всегда обращается к экспортёру.ПолучитьВременнуюАгрегацию(). Дефолт
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Numerical limits handling]
       found → n_a
       Текст: The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:1 → -
       Пояснение: OneScript использует System.Decimal (28 значащих цифр), а не IEEE 754. NaN, Infinity и отрицательный ноль невозможны - арифметические операции выбрасы
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → not_found
       Текст: The implementation SHOULD use a timeout to prevent indefinite callback execution.
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:230 → -
       Пояснение: Вызов Callback.Выполнить() в ВызватьМультиОбратныеВызовы и ВызватьCallbackИСобрать выполняется синхронно без таймаута; механизма прерывания зависшего 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       found → partial
       Текст: `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`.
       Расположение: src/Метрики/Классы/ОтелДанныеМетрики.os:1 → src/Метрики/Классы/ОтелДанныеМетрики.os:42
       Пояснение: Каждый ОтелДанныеМетрики содержит ОбластьИнструментирования, но интерфейс Произвести возвращает Массив метрик (потенциально с разными scope) и не треб
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Пояснение: ЗакрытьСРезультатом принимает параметр ТаймаутМс, но фактически использует ИнтервалЭкспортаМс*МножительТаймаутаОжидания вместо переданного значения; п
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       found → partial
       Текст: Cumulative timeseries MUST use a consistent start timestamp for all collection intervals.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:175 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:329
       Пояснение: Для синхронных инструментов ВремяСтарта инициализируется в ПриСозданииОбъекта и при cumulative не сбрасывается — start стабилен. Для асинхронных же От
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → partial
       Текст: If the gRPC client implementation does not support an endpoint with a scheme of `http` or `https` th
       Расположение: src/Экспорт/Классы/ОтелGrpcТранспорт.os:207 → src/Экспорт/Классы/ОтелGrpcТранспорт.os:1-317
       Пояснение: Endpoint передаётся в OPI_GRPC как есть. Базовая нормализация (добавление http://, если схема отсутствует) есть в ОтелАвтоконфигурация.os:819-826, но 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Concurrency requirements]
       found → partial
       Текст: Link - Links are immutable and SHOULD be safe for concurrent use by default.
       Расположение: src/Трассировка/Классы/ОтелСпан.os:166 → src/Трассировка/Классы/ОтелСпан.os:423
       Пояснение: Линк хранится как Соответствие внутри массива Линки спана, иммутабельность гарантируется только тем, что после Завершить() коллекция не изменяется. От
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (33) - требует перепроверки:

     [Baggage Api / Context Interaction]
       partial → found
       Текст: The functionality listed above is necessary because API users SHOULD NOT have access to the Context 
       Код: src/Ядро/Модули/ОтелКонтекст.os:20
       Было: Функция КлючBaggage() экспортирована и доступна публично, поскольку OneScript не поддерживает приват
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Context / Detach Context]
       partial → found
       Текст: The API MUST accept the following parameters: * A `Token` that was returned by a previous call to at
       Код: src/Ядро/Модули/ОтелКонтекст.os:263
       Было: ВосстановитьПредыдущийКонтекст() реализует detach (снимает верхний элемент стека контекстов), но НЕ 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Api / Enabled]
       partial → found
       Текст: When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then M
       Код: src/Логирование/Классы/ОтелЛоггер.os:68
       Было: Контекст резолвится в текущий через ОтелКонтекст.Текущий() только в проверке сэмплирования (Трассиро
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ReadWriteLogRecord]
       partial → found
       Текст: A function receiving this as an argument MUST additionally be able to modify the following informati
       Код: src/Логирование/Классы/ОтелЗаписьЛога.os:179
       Было: Сеттеры есть для Timestamp/ObservedTimestamp/SeverityText/SeverityNumber/Body/TraceId/SpanId/TraceFl
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Counter operations]
       partial → found
       Текст: This API SHOULD NOT validate this value, that is left to implementations of the API.
       Код: src/Метрики/Классы/ОтелСчетчик.os:32
       Было: ОтелСчетчик.Добавить проверяет Значение < 0 и игнорирует с логированием. Хотя в данном коде API и SD
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API SHOULD NOT validate the `unit`.
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:282
       Было: УстановитьЕдиницаИзмерения проверяет ASCII через ОтелУтилиты.СтрокаПечатнаяASCII и подменяет non-ASC
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API SHOULD NOT validate `advisory` parameters.
       Код: src/Метрики/Классы/ОтелМетр.os:1026
       Было: ПроверитьСовет проверяет тип Структуры и типы вложенных полей (Границы должны быть Массив, КлючиАтри
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API SHOULD NOT validate the `unit`.
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:193
       Было: УстановитьЕдиницаИзмерения проверяет ASCII через ОтелУтилиты.СтрокаПечатнаяASCII и подменяет non-ASC
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API SHOULD NOT validate `advisory` parameters.
       Код: src/Метрики/Классы/ОтелМетр.os:1026
       Было: ПроверитьСовет проверяет структуру и типы advisory полей с логированием предупреждений - это валидац
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       not_found → partial
       Текст: If the potential conflict involves multiple `description` properties, setting the `description` thro
       Код: src/Метрики/Классы/ОтелМетр.os:935
       Было: ПроверитьКонфликтДескриптора сравнивает Описание независимо от View; нет логики, подавляющей предупр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       not_found → partial
       Текст: If the potential conflict involves instruments that can be distinguished by a supported View selecto
       Код: src/Метрики/Классы/ОтелМетр.os:955
       Было: Текст предупреждения (ОтелМетр.os:906-912) не содержит рецепт переименовывающего View — приводятся т
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD collect metrics, split into batches if necessary, call `Export(batch)` on each b
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:185
       Было: ПринудительноВыгрузитьСРезультатом вызывает СброситьБуфер (collect+Export) и затем Экспортер.Принуди
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       partial → found
       Текст: SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good
       Код: src/Метрики/Классы/ОтелАгрегаторГистограммы.os:165
       Было: Дефолтные границы в СтандартныеГраницы() содержат 14 значений (отсутствует 7500), тогда как специфик
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument unit]
       partial → found
       Текст: When a Meter creates an instrument, it SHOULD NOT validate the instrument unit.
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:285
       Было: УстановитьЕдиницаИзмерения проверяет ASCII-печатность через ОтелУтилиты.СтрокаПечатнаяASCII и заменя
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter Creation]
       n_a → found
       Текст: It SHOULD only be possible to create `Meter` instances through a `MeterProvider` (see API).
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:74
       Было: OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен). Основной путь
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`,
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:33-38, 430-462
       Было: При множественных читателях `СброситьБуфер` корректно вызывает `СброситьБуферБезОчистки` у всех кром
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → found
       Текст: The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered ca
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:121
       Было: ВызватьCallbackИСобрать вызывает только зарегистрированные через ДобавитьCallback функции, но Внешни
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       not_found → found
       Текст: `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелРезультатПроизводстваМетрик.os:1
       Было: Функция Произвести возвращает только Массив данных метрик, без статуса успех/ошибка/таймаут; механиз
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector tha
       Код: src/Метрики/Классы/ОтелМетр.os:522
       Было: ПроверитьКонфликтИменView только логирует предупреждение при множественных совпадениях, но не валиди
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       n_a → found
       Текст: However, if they are already implemented, they SHOULD continue to be supported as they were part of 
       Было: Условное требование к obsolete env-переменным OTEL_EXPORTER_OTLP_SPAN_INSECURE / OTEL_EXPORTER_OTLP_
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / User Agent]
       n_a → not_found
       Текст: The resulting User-Agent SHOULD include the exporter's default User-Agent string.
       Было: Условное требование: применимо только если экспортер реализует MAY-опцию для добавления пользователь
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Global Propagators]
       partial → found
       Текст: If pre-configured, Propagators SHOULD default to a composite Propagator containing the W3C Trace Con
       Код: src/Ядро/Модули/ОтелГлобальный.os:180
       Было: OneScript SDK не выполняет pre-configure пропагаторов (платформа не относится к ASP.NET-подобным). П
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Propagators Distribution]
       partial → found
       Текст: The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST 
       Код: src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:1
       Было: Пропагаторы (W3C TraceContext, W3C Baggage, B3) реализованы и поддерживаются, но распространяются ка
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Detecting resource information from the environment]
       partial → found
       Текст: Note the failure to detect any resource information MUST NOT be considered an error, whereas an erro
       Код: src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:29
       Было: Host-детектор логирует ошибку как Warning, но Process- и CPU-детекторы логируют исключения уровнем D
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Detecting resource information from the environment]
       partial → found
       Текст: Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions
       Код: src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:20
       Было: Host-детектор устанавливает host.name и os.type (атрибуты семантических соглашений), но Schema URL п
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Specifying resource information via an environment variable]
       not_found → partial
       Текст: In case of any error, e.g. failure during the decoding process, the entire environment variable valu
       Код: src/Ядро/Классы/ОтелРесурс.os:137
       Было: ПрименитьАтрибутыИзОкружения не оборачивает декодирование пар в Попытка/Исключение: нет логики 'отбр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Specifying resource information via an environment variable]
       not_found → partial
       Текст: In case of any error, e.g. failure during the decoding process, the entire environment variable valu
       Код: src/Ядро/Классы/ОтелРесурс.os:137
       Было: Нет диагностики ошибки парсинга OTEL_RESOURCE_ATTRIBUTES (нет вызова Лог.Ошибка/Предупреждение в При
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Context Interaction]
       partial → found
       Текст: The functionality listed above is necessary because API users SHOULD NOT have access to the Context 
       Код: src/Ядро/Модули/ОтелКонтекст.os:43
       Было: Ключи КлючСпан/КлючBaggage инкапсулированы как переменные модуля, но также экспортируются через функ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / End]
       partial → found
       Текст: This operation itself MUST NOT perform blocking I/O on the calling thread.
       Код: src/Трассировка/Классы/ОтелСпан.os:501
       Было: Завершить() синхронно вызывает Процессор.ПриЗавершении(). У ОтелПакетныйПроцессорСпанов это неблокир
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Set Status]
       partial → found
       Текст: An attempt to set value Unset SHOULD be ignored.
       Код: src/Трассировка/Классы/ОтелСпан.os:478
       Было: Попытка перейти в Unset из Ok или Error блокируется (Ok финален; Error→Unset запрещён явно), но при 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Wrapping a SpanContext in a Span]
       n_a → found
       Текст: This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable.
       Код: src/Трассировка/Классы/ОтелНоопСпан.os:1
       Было: OneScript не поддерживает sealed-классы / final-методы; механизм запрета переопределения отсутствует
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / IdGenerator randomness]
       not_found → partial
       Текст: Custom implementations of the `IdGenerator` SHOULD identify themselves appropriately when all genera
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:344
       Было: В SDK нет маркер-интерфейса или иного механизма, через который пользовательский IdGenerator мог бы д
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / OnEnding]
       n_a → found
       Текст: The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking `
       Код: src/Трассировка/Классы/ОтелСпан.os:501
       Было: OneScript использует ФоновыеЗадания вместо потоков; межпоточная безопасность спана на уровне gorouti
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (10) - агент нашёл дополнительные:

     [Env Vars] SHOULD found: For new implementations, these should be treated as MUST requirements.
     [Logs Api] MUST found: The API MUST accept the following parameters: Timestamp (optional), Observed Tim
     [Metrics Api] SHOULD found: The API to register a new Callback SHOULD accept:
     [Metrics Sdk] MUST found: The SDK MUST accept the following criteria:
     [Metrics Sdk] SHOULD partial: The default output `aggregation` (optional), a function of instrument kind. This
     [Metrics Sdk] SHOULD found: SDKs SHOULD return some failure for these calls, if possible.
     [Metrics Sdk] SHOULD not_found: For asynchronous instrument, the start timestamp SHOULD be:
     [Trace Api] MUST found: This API MUST accept the following parameters:
     [Trace Api] SHOULD found: In case an invalid name (null or empty string) is specified, a working Tracer im
     [Trace Api] SHOULD found: In case an invalid name (null or empty string) is specified, a working Tracer im

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (10) - были раньше, теперь нет:

     [Env Vars] MUST found: For new implementations, these should be treated as MUST requirements.
     [Logs Api] MUST found: The API MUST accept the following parameters:
     [Metrics Api] SHOULD found: The API to register a new Callback SHOULD accept: A `callback` function, A list 
     [Metrics Sdk] MUST found: The SDK MUST accept the following criteria: name, type, unit, meter_name, meter_
     [Metrics Sdk] SHOULD found: This function SHOULD be obtained from the `exporter`.
     [Metrics Sdk] SHOULD found: After the call to `Shutdown`, subsequent invocations to `Collect` are not allowe
     [Metrics Sdk] SHOULD partial: For asynchronous instrument, the start timestamp SHOULD be: - The creation time 
     [Trace Api] MUST found: This API MUST accept the following parameters: name (required), version (optiona
     [Trace Api] SHOULD found: its `name` property SHOULD be set to an empty string, and a message reporting th
     [Trace Api] SHOULD found: its `name` property SHOULD be set to an empty string, and a message reporting th

  Итого изменений: 81
    Понижений: 28, Повышений: 33, Боковых: 0
    Новых req: 10, Пропущенных req: 10
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
