# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             744    755 +   11 ✅
  partial            37     29    -8
  not_found          23     15    -8
  n_a                36     41 +    5
  Всего             840    840 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (13) - требует перепроверки:

     [Metrics Api / Counter operations]
       found → partial
       Текст: This API SHOULD NOT validate this value, that is left to implementations of the API.
       Пояснение: Метод Counter.Add (точка входа API) выполняет валидацию — отклоняет отрицательные значения и логирует предупреждение, что прямо противоречит SHOULD NO
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       found → n_a
       Текст: Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`
       Пояснение: OneScript Число = System.Decimal: значения +Inf/-Inf/NaN физически непредставимы, поэтому требование к sum о non-normal values неприменимо к платформе
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Numerical limits handling]
       found → n_a
       Текст: If the SDK receives float/double values from Instruments, it MUST handle all the possible values.
       Пояснение: Платформенный тип Число = System.Decimal не имеет понятий float/double, NaN, ±Inf и -0; предусловие требования (получение float/double от инструментов
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       found → partial
       Текст: Cumulative timeseries MUST use a consistent start timestamp for all collection intervals.
       Расположение: src/Метрики/Классы/ОтелСинхронныйИнструмент.os:127 → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:435
       Пояснение: Для синхронных инструментов ВремяСтарта корректно сохраняется при cumulative (ОтелБазовыйСинхронныйИнструмент.os:177-182), но для async-инструментов s
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       found → partial
       Текст: For synchronous instruments, the start timestamp SHOULD be the time of the first measurement for the
       Расположение: src/Метрики/Классы/ОтелСинхронныйИнструмент.os:127 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:344
       Пояснение: ВремяСтарта инициализируется в ПриСозданииОбъекта (момент создания инструмента), а не на момент первого измерения, как рекомендует SHOULD; сам новый а
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Extract]
       not_found → n_a
       Текст: MUST attempt to extract B3 encoded using single and multi-header formats.
       Пояснение: B3-пропагатор поставляется как отдельный опциональный пакет opentelemetry-propagator-b3 (см. ОтелАвтоконфигурация.os:1149-1178), в данном репозитории 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Extract]
       not_found → n_a
       Текст: MUST preserve a debug trace flag, if received, and propagate it with subsequent requests.
       Пояснение: Логика debug-флага B3 относится к классу ОтелB3Пропагатор из отдельного опционального пакета opentelemetry-propagator-b3, в данном SDK-репозитории не 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Extract]
       not_found → n_a
       Текст: Additionally, an OpenTelemetry implementation MUST set the sampled trace flag when the debug flag is
       Пояснение: Установка sampled при debug — часть B3-пропагатора, который в этом репозитории отсутствует и поставляется отдельным пакетом opentelemetry-propagator-b
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Extract]
       not_found → n_a
       Текст: MUST NOT reuse `X-B3-SpanId` as the ID for the server-side span.
       Пояснение: Обработка X-B3-SpanId — часть B3-пропагатора (отдельный пакет opentelemetry-propagator-b3), не реализуется в данном SDK-репозитории.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Inject]
       not_found → n_a
       Текст: MUST default to injecting B3 using the single-header format
       Пояснение: Инжект B3 single-header — функция отдельного пакета opentelemetry-propagator-b3 (см. ОтелАвтоконфигурация.os:1159-1178), в этом репозитории отсутствуе
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Inject]
       not_found → n_a
       Текст: MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support reusing the same ID for bot
       Пояснение: Логика инжекта B3-заголовков (в т.ч. отказ от X-B3-ParentSpanId) — внутренняя ответственность класса ОтелB3Пропагатор из отдельного пакета opentelemet
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → n_a
       Текст: The status code SHOULD remain unset, except for the following circumstances:
       Пояснение: Требование адресовано instrumentation-библиотекам/вызывающему коду (политика, когда ставить статус); SDK лишь обеспечивает дефолт UNSET (ОтелСпан.os:7
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / ForceFlush()]
       partial → n_a
       Текст: `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using som
       Пояснение: SHOULD-рекомендация адресована вызывающему коду (когда вызывать ForceFlush), а не реализации; СброситьБуфер реализован корректно, отсутствие комментар
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (17) - требует перепроверки:

     [Logs Sdk / Concurrency requirements]
       partial → found
       Текст: LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:79
       Было: ForceFlush и Shutdown защищены БлокировкаПроцессоров и АтомарноеБулево Закрыт; однако создание логге
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Get a Meter]
       partial → found
       Текст: Therefore, this API MUST be structured to accept a variable number of attributes, including none.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:74
       Было: Параметр АтрибутыОбласти принимает один объект ОтелАтрибуты (или Неопределено), а не переменное числ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API SHOULD NOT validate the `name`; that is left to implementations of the API, like the SDK.
       Код: src/Метрики/Классы/ОтелМетр.os:863
       Было: API и SDK объединены в одном пакете. ВалидироватьИмяИнструмента вызывается на API-точке входа Создат
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API SHOULD NOT validate the `name`, that is left to implementations of the API.
       Код: src/Метрики/Классы/ОтелМетр.os:863
       Было: ВалидироватьИмяИнструмента вызывается и для async-методов СоздатьНаблюдаемый*. SDK-уровневая мягкая 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Concurrency requirements]
       n_a → found
       Текст: MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:94
       Было: OneScript - однопоточная среда (концепция параллельного исполнения отсутствует, ФоновоеЗадание имеет
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Concurrency requirements]
       n_a → found
       Текст: ExemplarReservoir - all methods MUST be safe to be called concurrently.
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:72
       Было: OneScript однопоточен; пред-условие "For languages which support concurrent execution" не выполняетс
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Concurrency requirements]
       n_a → found
       Текст: MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be 
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:289
       Было: OneScript не поддерживает параллельное исполнение. Методы Собрать/СброситьБуфер/Закрыть в ОтелПериод
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Concurrency requirements]
       n_a → found
       Текст: MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:268
       Было: OneScript - однопоточная среда; пред-условие раздела не выполняется. Методы СброситьБуфер/Закрыть у 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD collect metrics, split into batches if necessary, call `Export(batch)` on each b
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:179
       Было: ПринудительноВыгрузитьСРезультатом вызывает СброситьБуфер (Collect+Export) и затем ВызватьФорсФлашЭк
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument selection criteria]
       partial → found
       Текст: If the SDK does not support wildcards in general, it MUST still recognize the special single asteris
       Код: src/Метрики/Классы/ОтелСелекторИнструментов.os:38
       Было: Only special asterisk (*) is supported for matching all instruments. General wildcard patterns (?, *
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MeterConfig]
       partial → found
       Текст: The value of `enabled` MUST be used to resolve whether an instrument is Enabled.
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:275
       Было: Функция Включен() инструмента возвращает МетрВключен.Получить() И Включен.Получить(), то есть значен
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       not_found → found
       Текст: In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector tha
       Код: src/Метрики/Классы/ОтелМетр.os:1275
       Было: No validation to ensure selector matches at most one instrument when name is provided. MeterProvider
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: If the user does not provide any value, the SDK SHOULD use the `Attributes` advisory parameter confi
       Код: src/Метрики/Классы/ОтелМетр.os:952-960
       Было: Attributes advisory parameter is not implemented in OneScript SDK. All attributes are kept by defaul
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Inject]
       not_found → found
       Текст: MUST provide configuration to change the default injection format to B3 multi-header
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1159-1178
       Было: B3 пропагатор не реализован, конфигурация переключения формата (single/multi-header) отсутствует.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Span]
       n_a → found
       Текст: All Spans MUST be created via a Tracer.
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:74
       Было: OneScript не поддерживает приватные конструкторы; Tracer (ОтелТрассировщик) - единственный задокумен
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / IdGenerator randomness]
       partial → found
       Текст: Custom implementations of the `IdGenerator` SHOULD identify themselves appropriately when all genera
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:386
       Было: SDK поддерживает опциональный метод ФлагRandomДляНовыхИд() у пользовательского ГенераторИд (duck typ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / `ForceFlush()`]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелЭкспортерСпанов.os:63
       Было: Метод СброситьБуфер принимает параметр ТаймаутМс, но игнорирует его (синхронный экспортер без буфера
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  Итого изменений: 30
    Понижений: 13, Повышений: 17, Боковых: 0
    Новых req: 0, Пропущенных req: 0
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
