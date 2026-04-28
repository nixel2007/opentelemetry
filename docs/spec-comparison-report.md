# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             686    718 +   32 ✅
  partial            86     66   -20
  not_found          54     53    -1
  n_a                14      3   -11
  Всего             840    840 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (19) - требует перепроверки:

     [Metrics Api / Asynchronous Counter creation]
       found → partial
       Текст: The API SHOULD provide some way to pass `state` to the callback.
       Расположение: src/Метрики/Классы/ОтелМетр.os:291 → src/Метрики/Классы/ОтелМетр.os:567
       Пояснение: Callback вызывается через Действие.Выполнить(Наблюдения) - явного параметра state нет, состояние может быть захвачено только через объект-владелец мет
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Histogram operations]
       partial → not_found
       Текст: This API SHOULD be documented in a way to communicate to users that this value is expected to be non
       Пояснение: Документирующий комментарий перед Записать описывает параметр как 'измеренное значение', но не упоминает, что значение должно быть неотрицательным.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Instrument]
       found → n_a
       Текст: Language-level features such as the distinction between integer and floating point numbers SHOULD be
       Расположение: src/Метрики/Классы/ОтелБазовыйАгрегатор.os:8 → -
       Пояснение: OneScript использует единый числовой тип System.Decimal — различие между integer и floating point на уровне языка отсутствует, поэтому требование непр
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Callback functions MUST be documented as follows for the end user:
       Расположение: src/Метрики/Классы/ОтелМетр.os:269 → src/Метрики/Классы/ОтелМетр.os:271
       Пояснение: Документирующие комментарии для СоздатьНаблюдаемыйСчетчик описывают часть требований к callback (потокобезопасность, отсутствие дублей), но не дословн
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Callback functions SHOULD be reentrant safe.
       Расположение: src/Метрики/Классы/ОтелМетр.os:277 → src/Метрики/Классы/ОтелМетр.os:344
       Пояснение: Комментарии для СоздатьНаблюдаемыйРеверсивныйСчетчик и СоздатьНаблюдаемыйДатчик упоминают 'потокобезопасность и реентерабельность', но в комментарии д
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       found → partial
       Текст: When the histogram contains not more than one value in either of the positive or negative ranges, th
       Расположение: src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:307 → src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:306
       Пояснение: НачальнаяШкала = 20 (= MaxScale по умолчанию) используется при первом измерении, но нет специальной логики «при ≤1 значении использовать максимальную 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricExporter]
       partial → not_found
       Текст: Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsuppo
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:250 → -
       Пояснение: В ОтелЭкспортерМетрик нет проверок поддерживаемых типов Aggregation/Temporality перед экспортом — все типы принимаются без диагностики.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       found → partial
       Текст: Implementation SHOULD use the filter as early as possible to gain as much performance gain possible 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:366 → src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13
       Пояснение: Параметр ФильтрМетрик принят интерфейсом, но раннее применение фильтра — обязанность реализации; в самом интерфейсе/SDK нет паттерна, гарантирующего р
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       partial → not_found
       Текст: `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13 → -
       Пояснение: Произвести возвращает только Массив данных, без статуса успех/ошибка/таймаут; в СобратьДанныеПродюсеров ошибки лишь логируются.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       partial → not_found
       Текст: `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`.
       Расположение: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13 → -
       Пояснение: Интерфейс продюсера не определяет/не возвращает InstrumentationScope, идентифицирующий MetricProducer; в результирующих данных используется область вы
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       found → partial
       Текст: For delta aggregations, the start timestamp MUST equal the previous collection interval’s timestamp,
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:171 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:174
       Пояснение: Для синхронных инструментов ВремяСтарта корректно сбрасывается на ТекущееВремя при delta-сборе. Для асинхронных инструментов startTimeUnixNano = Время
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       found → partial
       Текст: This implies that all data points with delta temporality aggregation for an instrument MUST share th
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:21 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:174
       Пояснение: Синхронные инструменты используют общий ВремяСтарта для всех точек. Асинхронные в ПреобразоватьЗаписиВТочки задают startTimeUnixNano индивидуально по 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       found → partial
       Текст: Cumulative timeseries MUST use a consistent start timestamp for all collection intervals.
       Пояснение: Синхронные сохраняют ВремяСтарта при кумулятивной временности. Асинхронные при каждом callback заново выставляют startTimeUnixNano = ВремяСейчас, что 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       partial → not_found
       Текст: For asynchronous instrument, the start timestamp SHOULD be:
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:188 → -
       Пояснение: Для асинхронных инструментов startTimeUnixNano выставляется в текущее время наблюдения (ПреобразоватьЗаписиВТочки), а не время создания инструмента ил
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → partial
       Текст: The option SHOULD accept any form allowed by the underlying gRPC client implementation.
       Расположение: src/Экспорт/Классы/ОтелGrpcТранспорт.os:184 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:796
       Пояснение: РазобратьСхемуURL принимает только http/https/без схемы; иные формы (DNS-имена, unix:, dns:) отклоняются как 'неподдерживаемая схема'.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Global Propagators]
       found → partial
       Текст: If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace
       Расположение: src/Ядро/Модули/ОтелГлобальный.os:121 → src/Ядро/Модули/ОтелГлобальный.os:132
       Пояснение: Дефолт ОтелГлобальный.ПолучитьПропагаторы() возвращает ОтелНоопПропагатор, а не композит W3C TraceContext + W3C Baggage. Платформенной пред-конфигурац
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / TextMap Propagator]
       found → partial
       Текст: In order to increase compatibility, the key-value pairs MUST only consist of US-ASCII characters tha
       Расположение: src/Пропагация/Классы/ОтелW3CПропагатор.os:63 → src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:18
       Пояснение: Сеттер просто записывает ключ/значение в Соответствие через Носитель.Вставить без явной валидации US-ASCII / RFC 9110. Используемые имена заголовков (
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Specifying resource information via an environment variable]
       partial → not_found
       Текст: In case of any error, e.g. failure during the decoding process, the entire environment variable valu
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:742 → -
       Пояснение: В ПрименитьАтрибутыИзОкружения нет блока Попытка/Исключение вокруг парсинга OTEL_RESOURCE_ATTRIBUTES и РаскодироватьСтроку; при ошибке декодирования з
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / TraceIdRatioBased]
       found → partial
       Текст: The precision of the number SHOULD follow implementation language standards and SHOULD be high enoug
       Пояснение: Используется фиксированный формат 'ЧДЦ=6' (6 знаков после точки). Этого достаточно для типичных коэффициентов (включая пример 0.000100 из спецификации
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (55) - требует перепроверки:

     [Logs Api / Emit a LogRecord]
       n_a → found
       Текст: When only explicit Context is supported, this parameter SHOULD be required.
       Код: src/Логирование/Классы/ОтелЛоггер.os:94
       Было: Альтернативная ветка спецификации: SDK поддерживает неявный контекст (ОтелКонтекст.Текущий()), поэто
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD return some ERROR status if there is an error condition;
       Код: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:85
       Было: СброситьБуферАсинхронно возвращает Обещание, ошибки могут проявиться через rejected Promise, но синх
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: and if there is no error condition, it SHOULD return some NO ERROR status, language implementations 
       Код: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:72
       Было: Только асинхронный вариант возвращает Обещание; синхронный СброситьБуфер - процедура (void), без явн
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:74
       Было: Метод СброситьБуфер провайдера не принимает параметр таймаута и не передаёт его процессорам. Async-в
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелЭкспортерЛогов.os:64
       Было: СброситьБуфер() — процедура без возврата; СброситьБуферАсинхронно() возвращает Обещание, но не разли
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:74
       Было: СброситьБуфер реализован как Процедура без возвращаемого значения; статус успеха/таймаута не возвращ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:129
       Было: СброситьБуфер у экспортера не принимает параметра таймаута и не имеет механизма прерывания; синхронн
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Logger Creation]
       partial → found
       Текст: In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be 
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:67
       Было: При ИмяБиблиотеки = Неопределено код заменяет на пустую строку (Неопределено → ''), не сохраняя исхо
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ShutDown]
       partial → found
       Текст: After the call to `Shutdown`, subsequent calls to `OnEmit` are not allowed. SDKs SHOULD ignore these
       Код: src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:26
       Было: ОтелБазовыйПакетныйПроцессор.Обработать проверяет флаг Закрыт и игнорирует вызовы; в ОтелПростойПроц
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Multiple-instrument callbacks]
       not_found → found
       Текст: The API to register a new Callback SHOULD accept: * A `callback` function* A list (or tuple, etc.) o
       Код: src/Метрики/Классы/ОтелМетр.os:530
       Было: Multiple-instrument callbacks являются опциональной фичей (MAY support); SDK не предоставляет API ре
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of 
       Код: src/Метрики/Классы/ОтелМетр.os:530
       Было: ЗарегистрироватьОбратныйВызов(Callback, НовыеИнструменты) принимает явный набор инструментов, но не 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Collect]
       partial → found
       Текст: `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:224
       Было: СброситьБуфер - процедура без возврата статуса; ошибки экспорта только логируются. Нет способа вызыв
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Concurrency requirements]
       partial → found
       Текст: MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:100
       Было: Закрыт реализован через АтомарноеБулево с CAS (СравнитьИУстановить) - Закрыть идемпотентен и безопас
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Concurrency requirements]
       partial → found
       Текст: MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently.
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:71
       Было: Методы СброситьБуфер и Закрыть в ОтелЭкспортерМетрик существуют как простые делегирующие процедуры, 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Configuration]
       partial → found
       Текст: If there is no matching view, but the `MetricReader` defines a default cardinality limit value based
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:290
       Было: MetricReader предоставляет один общий ЛимитМощности (по умолчанию 2000), не дифференцированный по ти
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarReservoir]
       partial → found
       Текст: The “offer” method SHOULD accept measurements, including:
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:41
       Было: Предложить принимает Значение, АтрибутыИзмерения и КонтекстСпана, но timestamp генерируется внутри (
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarReservoir]
       partial → found
       Текст: This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associat
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:42
       Было: АтрибутыСерии передаются в каждом вызове Предложить(), а не на конструировании резервуара; функциона
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no erro
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:173
       Было: СброситьБуфер - процедура без возвращаемого статуса; ошибки/успех модулируются только через Обещание
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:163
       Было: СброситьБуфер/СброситьБуферАсинхронно не принимают параметр таймаута и не имеют механизма прерывания
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       not_found → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:107
       Было: СброситьБуфер - Процедура без возвращаемого значения; невозможно отличить успех от неудачи/таймаута.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       not_found → found
       Текст: `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no erro
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:235
       Было: СброситьБуфер не возвращает значение; статус ошибки/успеха недоступен.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       not_found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:106
       Было: СброситьБуфер не принимает таймаут и не прерывает операцию по таймауту.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument selection criteria]
       n_a → found
       Текст: Therefore, the instrument selection criteria can be structured to accept the criteria, but MUST NOT 
       Код: src/Метрики/Классы/ОтелСелекторИнструментов.os:159
       Было: Дополнительные (не из списка спецификации) критерии селектором не поддерживаются - SDK принимает тол
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       not_found → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:68
       Было: Экспортер.СброситьБуфер - Процедура без возвращаемого значения; статус succeed/failed/timed out не с
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       partial → found
       Текст: If applying the View results in conflicting metric identities the implementation SHOULD apply the Vi
       Код: src/Метрики/Классы/ОтелМетр.os:902
       Было: Конфликт дескрипторов инструмента (одинаковое имя, разные параметры) логируется через Лог.Предупрежд
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Measurement processing]
       not_found → partial
       Текст: If it is not possible to apply the View without producing semantic errors (e.g. the View sets an asy
       Код: src/Метрики/Классы/ОтелМетр.os:671
       Было: Нет валидации семантической совместимости View с инструментом (например, Explicit bucket histogram д
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter Creation]
       partial → found
       Текст: In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be ret
       Код: src/Ядро/Классы/ОтелОбластьИнструментирования.os:108
       Было: При передаче Неопределено имя нормализуется в пустую строку (стр. 67), исходное Неопределено не сохр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: The `MetricReader` MUST ensure that data points from OpenTelemetry instruments are output in the con
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:355
       Было: Для синхронных инструментов конверсия Delta→Cumulative реализована через сохранение аккумуляторов пр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect 
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:355
       Было: Для асинхронных инструментов ВнешниеНаблюдения очищаются после сбора, но Cumulative-вариант не вычит
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       not_found → found
       Текст: In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector tha
       Код: src/Метрики/Классы/ОтелМетр.os:878
       Было: Нет проверки, что при заданном имени потока селектор отбирает не более одного инструмента; первый на
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: If the user does not provide a `name` value, name from the Instrument the View matches MUST be used 
       Код: src/Метрики/Классы/ОтелМетр.os:677
       Было: ОтелПредставление поддерживает поле НовоеИмя, но в коде применения View (ПрименитьПредставлениеКИнст
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: If the user does not provide a `description` value, the description from the Instrument a View match
       Код: src/Метрики/Классы/ОтелПредставление.os:38
       Было: Поле НовоеОписание есть в ОтелПредставление, но применение НовоеОписание() в выходные данные метрики
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       not_found → found
       Текст: However, if they are already implemented, they SHOULD continue to be supported as they were part of 
       Было: Устаревшие переменные OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE не обраб
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → partial
       Текст: Resource detectors SHOULD have a unique name for reference in configuration.
       Код: src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1
       Было: Условная фича Resource Detector Naming не реализована: классы детекторов (ОтелДетекторРесурсаХоста, 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: Names SHOULD be snake case and consist of lowercase alphanumeric and `_` characters, which ensures t
       Было: Условная фича Resource Detector Naming не реализована: у детекторов нет имён, к которым применимо тр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → partial
       Текст: Resource detector names SHOULD reflect the root namespace of attributes they populate.
       Код: src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:22
       Было: Условная фича Resource Detector Naming не реализована: у детекторов нет имён, которые могли бы отраж
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → partial
       Текст: Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name whic
       Код: src/Ядро/Классы/ОтелДетекторРесурсаПроцессора.os:23
       Было: Условная фича Resource Detector Naming не реализована: имена детекторам не присваиваются.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: An SDK which identifies multiple resource detectors with the same name SHOULD report an error.
       Было: Условная фича Resource Detector Naming не реализована: SDK не идентифицирует детекторы по имени, поэ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → partial
       Текст: In order to limit collisions, resource detectors SHOULD document their name in a manner which is eas
       Код: src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:12
       Было: Условная фича Resource Detector Naming не реализована: имена детекторам не присваиваются и не докуме
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Specifying resource information via an environment variable]
       partial → found
       Текст: The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge 
       Код: src/Ядро/Классы/ОтелРесурс.os:138
       Было: OTEL_RESOURCE_ATTRIBUTES извлекается и применяется к ресурсу, но логика приоритета 'user-provided re
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / End]
       partial → found
       Текст: This operation itself MUST NOT perform blocking I/O on the calling thread.
       Код: src/Трассировка/Классы/ОтелСпан.os:484
       Было: Завершить() сам по себе не делает I/O, но синхронно вызывает Процессор.ПриЗавершении. ОтелПростойПро
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / End]
       n_a → found
       Текст: Any locking used needs be minimized and SHOULD be removed entirely if possible.
       Код: src/Трассировка/Классы/ОтелСпан.os:484
       Было: В OneScript однопоточная модель выполнения в рамках сеанса; явных блокировок (locks/mutex) нет
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Link]
       partial → found
       Текст: Implementations SHOULD record links containing `SpanContext` with empty `TraceId` or `SpanId` (all z
       Код: src/Трассировка/Классы/ОтелСпан.os:400
       Было: ДобавитьЛинк не отвергает контексты с нулевыми ID, но и не реализует явное условие 'attribute set ил
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Set Status]
       partial → found
       Текст: An attempt to set value Unset SHOULD be ignored.
       Код: src/Трассировка/Классы/ОтелСпан.os:461
       Было: Нет явной проверки 'если входное Значение = НеУстановлен то выйти'. Из ERROR попытка установить UNSE
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Set Status]
       partial → found
       Текст: When the status is set to Error by Instrumentation Libraries, the Description SHOULD be documented a
       Код: src/Трассировка/Классы/ОтелСпан.os:450
       Было: Это требование к документации Instrumentation Libraries, а не к самому SDK. SDK API позволяет переда
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Set Status]
       partial → found
       Текст: For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish the
       Код: src/Трассировка/Классы/ОтелСпан.os:450
       Было: Это процессное требование к авторам Instrumentation Libraries, а не к коду SDK. В данном репозитории
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Set Status]
       n_a → found
       Текст: Generally, Instrumentation Libraries SHOULD NOT set the status code to Ok, unless explicitly configu
       Код: src/Трассировка/Классы/ОтелСпан.os:678
       Было: Требование к Instrumentation Libraries, а не к Trace API SDK. В репозитории нет Instrumentation Libr
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Set Status]
       n_a → found
       Текст: Instrumentation Libraries SHOULD leave the status code as Unset unless there is an error, as describ
       Код: src/Трассировка/Классы/ОтелСпан.os:678
       Было: Требование к Instrumentation Libraries, а не к Trace API SDK. В репозитории нет Instrumentation Libr
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Set Status]
       n_a → found
       Текст: Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generat
       Код: src/Трассировка/Классы/ОтелСпан.os:450
       Было: Требование относится к инструментам анализа (бэкендам), а не к SDK
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Wrapping a SpanContext in a Span]
       not_found → partial
       Текст: If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possib
       Код: src/Трассировка/Классы/ОтелНоопСпан.os:272
       Было: Класс ОтелНоопСпан публично экспонирован и используется напрямую через `Новый ОтелНоопСпан(...)` в п
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Additional Span Interfaces]
       partial → found
       Текст: For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated 
       Код: src/Трассировка/Классы/ОтелСпан.os:195
       Было: Spand экспонирует ОбластьИнструментирования (InstrumentationScope), но не имеет отдельного устаревше
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:128
       Было: Метод СброситьБуфер() — Процедура, ничего не возвращает; ошибки только через исключения, таймаут не 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:128
       Было: Provider.СброситьБуфер() не принимает таймаут. На уровне КомпозитныйПроцессор.СброситьБуфер(ТаймаутМ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush()]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:74-76
       Было: СброситьБуфер реализована как Процедура (void), не возвращает статус. Таймаут логируется, но caller 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / `ForceFlush()`]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелЭкспортерСпанов.os:65
       Было: СброситьБуфер реализована как Процедура без возвращаемого значения; ошибки/таймауты логируются, но в
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (16) - агент нашёл дополнительные:

     [Env Vars] SHOULD found: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD found: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD found: It SHOULD NOT be supported by new implementations.
     [Logs Api] MUST found: The API MUST accept the following parameters: Timestamp (optional), Observed Tim
     [Metrics Api] SHOULD found: The `unit` is an optional string provided by the author of the Instrument. The A
     [Metrics Sdk] MUST found: This extension MUST be configurable on a metric View,
     [Metrics Sdk] SHOULD partial: After the call to `Shutdown`, subsequent invocations to `Collect` are not allowe
     [Trace Api] MUST found: This API MUST accept the following parameters: `name` (required), `version` (opt
     [Trace Api] MUST found: The API MUST provide: * An API to record a single `Link` where the `Link` proper
     [Trace Api] MUST found: The API MUST allow retrieving the TraceId and SpanId in the following forms: Hex
     [Trace Api] SHOULD found: This SHOULD be called SetStatus.
     [Trace Api] MUST NOT partial: Vendors may implement the Span interface to effect vendor-specific logic. Howeve
     [Trace Api] MUST found: The API MUST accept the following parameters: span name, parent Context (or root
     [Trace Sdk] MUST NOT not_found: The calling CompositeSampler SHOULD update the threshold of the outgoing TraceSt
     [Trace Sdk] MUST NOT found: i.e. it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvider
     [Trace Sdk] SHOULD partial: SDKs SHOULD ignore these calls gracefully, if possible.

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (16) - были раньше, теперь нет:

     [Env Vars] SHOULD found: "logging": Standard Output. It is a deprecated value left for backwards compatib
     [Env Vars] SHOULD found: "logging": Standard Output. It is a deprecated value left for backwards compatib
     [Env Vars] SHOULD found: "logging": Standard Output. It is a deprecated value left for backwards compatib
     [Logs Api] MUST found: The API MUST accept the following parameters:
     [Metrics Api] SHOULD found: The API SHOULD treat it as an opaque string.
     [Metrics Sdk] MUST found: This extension MUST be configurable on a metric View, although individual reserv
     [Metrics Sdk] SHOULD partial: SDKs SHOULD return some failure for these calls, if possible.
     [Trace Api] MUST found: This API MUST accept the following parameters:
     [Trace Api] MUST found: An API to record a single `Link` where the `Link` properties are passed as argum
     [Trace Api] MUST found: The API MUST allow retrieving the `TraceId` and `SpanId` in the following forms:
     [Trace Api] SHOULD found: An API to set the Status. This SHOULD be called SetStatus.
     [Trace Api] MUST NOT partial: However, alternative implementations MUST NOT allow callers to create `Span`s di
     [Trace Api] MUST found: The API MUST accept the following parameters:
     [Trace Sdk] MUST not_found: The calling CompositeSampler SHOULD update the threshold of the outgoing TraceSt
     [Trace Sdk] MUST NOT found: If configuration is updated (e.g., adding a `SpanProcessor`), the updated config
     [Trace Sdk] SHOULD found: After the call to `Shutdown`, subsequent calls to `OnStart`, `OnEnd`, or `ForceF

  Итого изменений: 106
    Понижений: 19, Повышений: 55, Боковых: 0
    Новых req: 16, Пропущенных req: 16
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
