# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             717    748 +   31 ✅
  partial            65     44   -21
  not_found          43     30   -13
  n_a                15     18 +    3
  Всего             840    840 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (19) - требует перепроверки:

     [Context / Detach Context]
       found → partial
       Текст: The API MUST accept the following parameters: * A `Token` that was returned by a previous call to at
       Расположение: src/Ядро/Классы/ОтелОбласть.os:23 → src/Ядро/Модули/ОтелКонтекст.os:271
       Пояснение: ВосстановитьПредыдущийКонтекст() реализует detach (снимает верхний элемент стека контекстов), но НЕ принимает Token-параметр. Восстановление выполняет
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Api / Emit a LogRecord]
       found → n_a
       Текст: When only explicit Context is supported, this parameter SHOULD be required.
       Расположение: src/Логирование/Классы/ОтелЛоггер.os:94 → -
       Пояснение: Условное требование: применимо только к SDK, поддерживающим ИСКЛЮЧИТЕЛЬНО explicit Context. Данная реализация поддерживает implicit Context (ОтелКонте
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ReadWriteLogRecord]
       found → partial
       Текст: A function receiving this as an argument MUST additionally be able to modify the following informati
       Пояснение: Сеттеры есть для Timestamp/ObservedTimestamp/SeverityText/SeverityNumber/Body/TraceId/SpanId/TraceFlags/EventName и для добавления/изменения атрибутов
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       found → partial
       Текст: SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good
       Расположение: src/Метрики/Классы/ОтелАгрегаторГистограммы.os:154 → src/Метрики/Классы/ОтелАгрегаторГистограммы.os:128
       Пояснение: Дефолтные границы в СтандартныеГраницы() содержат 14 значений (отсутствует 7500), тогда как спецификация требует 15: [0, 5, 10, 25, 50, 75, 100, 250, 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument unit]
       found → partial
       Текст: When a Meter creates an instrument, it SHOULD NOT validate the instrument unit.
       Расположение: src/Метрики/Классы/ОтелМетр.os:53 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:282
       Пояснение: УстановитьЕдиницаИзмерения проверяет ASCII-печатность через ОтелУтилиты.СтрокаПечатнаяASCII и заменяет невалидное значение на пустую строку с предупре
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Numerical limits handling]
       found → n_a
       Текст: If the SDK receives float/double values from Instruments, it MUST handle all the possible values.
       Расположение: src/Метрики/Классы/ОтелСчетчик.os:1 → -
       Пояснение: OneScript Число = System.Decimal (не IEEE 754). NaN, Infinity и денормализованные значения на платформе невозможны - такие литералы не существуют, опе
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       found → partial
       Текст: The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered ca
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:196 → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:226
       Пояснение: ВызватьCallbackИСобрать вызывает только зарегистрированные через ДобавитьCallback функции, но ВнешниеНаблюдения позволяют записывать наблюдения вне ca
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       partial → not_found
       Текст: `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13 → -
       Пояснение: Функция Произвести возвращает только Массив данных метрик, без статуса успех/ошибка/таймаут; механизм оповещения о неуспехе/таймауте отсутствует.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector tha
       Расположение: src/Метрики/Классы/ОтелМетр.os:892 → src/Метрики/Классы/ОтелМетр.os:1020
       Пояснение: ПроверитьКонфликтИменView только логирует предупреждение при множественных совпадениях, но не валидирует селектор на этапе регистрации View.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → partial
       Текст: The option SHOULD accept any form allowed by the underlying gRPC client implementation.
       Расположение: src/Экспорт/Классы/ОтелGrpcТранспорт.os:48 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:691
       Пояснение: РазобратьСхемуURL принимает только http/https и (без схемы → http://). Произвольные формы, разрешённые gRPC-клиентом (например, dns:///, unix://), не 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → partial
       Текст: If the gRPC client implementation does not support an endpoint with a scheme of http or https then t
       Расположение: src/Экспорт/Классы/ОтелGrpcТранспорт.os:48 → src/Экспорт/Классы/ОтелGrpcТранспорт.os:209
       Пояснение: URL с http(s):// передаётся в OPI_GRPC.ПолучитьПараметрыСоединения как есть, без явной трансформации в host:port-форму, ожидаемую gRPC-клиентами.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / User Agent]
       not_found → n_a
       Текст: The resulting User-Agent SHOULD include the exporter's default User-Agent string.
       Пояснение: Условное требование: применимо только если экспортер реализует MAY-опцию для добавления пользовательского product identifier. SDK не предоставляет так
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Global Propagators]
       found → partial
       Текст: If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace
       Пояснение: OneScript SDK не выполняет pre-configure пропагаторов (платформа не относится к ASP.NET-подобным). По умолчанию ПолучитьПропагаторы() возвращает ОтелН
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Propagators Distribution]
       found → partial
       Текст: The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST 
       Расположение: src/Пропагация/Классы/ОтелB3Пропагатор.os:1 → src/Пропагация/
       Пояснение: Пропагаторы (W3C TraceContext, W3C Baggage, B3) реализованы и поддерживаются, но распространяются как часть единого SDK-пакета (lib.config), а не как 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Detecting resource information from the environment]
       found → partial
       Текст: Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions
       Расположение: src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18 → src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:20
       Пояснение: Host-детектор устанавливает host.name и os.type (атрибуты семантических соглашений), но Schema URL пустой; должен быть https://opentelemetry.io/schema
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Context Interaction]
       found → partial
       Текст: The functionality listed above is necessary because API users SHOULD NOT have access to the Context 
       Расположение: src/Ядро/Модули/ОтелКонтекст.os:141 → src/Ядро/Модули/ОтелКонтекст.os:51
       Пояснение: Ключи КлючСпан/КлючBaggage инкапсулированы как переменные модуля, но также экспортируются через функции КлючСпана()/КлючBaggage(), что даёт пользовате
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / End]
       found → partial
       Текст: This operation itself MUST NOT perform blocking I/O on the calling thread.
       Расположение: src/Трассировка/Классы/ОтелСпан.os:484 → src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:45
       Пояснение: Завершить() синхронно вызывает Процессор.ПриЗавершении(). У ОтелПакетныйПроцессорСпанов это неблокирующая постановка в очередь (соответствует требован
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Wrapping a SpanContext in a Span]
       found → n_a
       Текст: This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable.
       Расположение: src/Трассировка/Классы/ОтелНоопСпан.os:1 → -
       Пояснение: OneScript не поддерживает sealed-классы / final-методы; механизм запрета переопределения отсутствует на уровне платформы. Класс расположен в API-слое 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / OnEnding]
       found → n_a
       Текст: The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking `
       Расположение: src/Трассировка/Классы/ОтелСпан.os:484 → -
       Пояснение: OneScript использует ФоновыеЗадания вместо потоков; межпоточная безопасность спана на уровне goroutine/thread-local не применима к платформе. Спан-объ
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (51) - требует перепроверки:

     [Env Vars / Boolean]
       not_found → found
       Текст: If any value other than a true value, case-insensitive string "false", empty, or unset is used, a wa
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:947
       Было: Boolean-парсинг (НРег(Значение) = "true") молча трактует любое не-"true" значение как false без логи
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Api / Enabled]
       partial → found
       Текст: The API SHOULD be documented that instrumentation authors needs to call this API each time they emit
       Код: src/Логирование/Классы/ОтелЛоггер.os:28
       Было: Документирующий комментарий есть и поясняет назначение API (пропустить создание LogRecord), но не ук
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / OnEmit]
       partial → found
       Текст: This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD 
       Код: src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:32
       Было: ПриПоявлении выполняется синхронно. ОтелКомпозитныйПроцессорЛогов.ПриПоявлении ловит исключения проц
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ShutDown]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:103
       Было: Закрыть реализован как Процедура (void) и не возвращает статус успеха/ошибки/таймаута. Асинхронный в
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:158
       Было: Закрыть() - процедура без возвращаемого значения; ЗакрытьАсинхронно() возвращает Обещание, но статус
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:166
       Было: ОтелПровайдерЛогирования.Закрыть() не принимает параметр таймаута и вызывает Процессор.Закрыть() без
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Asynchronous Counter creation]
       partial → found
       Текст: The API SHOULD provide some way to pass `state` to the callback.
       Код: src/Метрики/Классы/ОтелМетр.os:313
       Было: Явного параметра state у callback нет; передача состояния возможна только через захват замыкания лям
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Enabled]
       partial → found
       Текст: The API SHOULD be documented that instrumentation authors needs to call this API each time they reco
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253
       Было: Doc-комментарий описывает семантику Включен(), но не содержит явного указания вызывать API перед каж
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Histogram operations]
       partial → found
       Текст: This API SHOULD be documented in a way to communicate to users that this value is expected to be non
       Код: src/Метрики/Классы/ОтелГистограмма.os:14
       Было: Документирующий комментарий процедуры Записать описывает параметр Значение как «измеренное значение»
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to con
       Код: src/Метрики/Классы/ОтелМетр.os:42
       Было: Doc-комментарий метода СоздатьСчетчик описывает имя как 'имя счетчика', но не упоминает требования к
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to con
       Код: src/Метрики/Классы/ОтелМетр.os:285
       Было: Doc-комментарий метода СоздатьНаблюдаемыйСчетчик описывает имя как 'имя инструмента', но не упоминае
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Asynchronous instrument cardinality limits]
       not_found → found
       Текст: Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback 
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:255
       Было: В ОтелБазовыйНаблюдаемыйИнструмент.ВызватьCallbackИСобрать() лимит мощности для асинхронных инструме
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Configuration]
       partial → found
       Текст: If there is no matching view, but the `MetricReader` defines a default cardinality limit value based
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:343
       Было: MetricReader.ЛимитМощности() применяется ко всем инструментам Meter единым числом; нет дифференциаци
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       not_found → partial
       Текст: Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Met
       Код: src/Метрики/Классы/ОтелМетр.os:886
       Было: При повторной регистрации возвращается ранее зарегистрированный инструмент (Возврат Существующий), в
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarReservoir]
       partial → found
       Текст: This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associat
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:36
       Было: Документирующий комментарий метода Предложить упоминает АтрибутыИзмерения и АтрибутыСерии, но не опи
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarReservoir]
       partial → found
       Текст: This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associat
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:42
       Было: АтрибутыСерии передаются в каждый вызов Предложить(), а не сохраняются в резервуаре при конструирова
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` MAY skip `Export(batch)` calls if the timeout is already expired, but SHOULD still call
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:201
       Было: Не реализована логика таймаута и отдельного вызова ForceFlush() на экспортёре по истечении таймаута.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       partial → found
       Текст: Arithmetic sum of `Measurement` values in population. This SHOULD NOT be collected when used with in
       Код: src/Метрики/Классы/ОтелАгрегаторГистограммы.os:59
       Было: Sum собирается безусловно. Нет проверки типа инструмента и пропуска sum при UpDownCounter/Observable
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       partial → found
       Текст: The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic 
       Код: src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:218
       Было: Минимальная шкала захардкожена (-10), максимальная ограничена параметром НачальнаяШкала (default 20)
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument name]
       not_found → found
       Текст: When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrumen
       Код: src/Метрики/Классы/ОтелМетр.os:726
       Было: ОтелМетр.СоздатьСчетчик/СоздатьГистограмму/etc. не выполняют валидацию имени инструмента (нет провер
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument name]
       not_found → found
       Текст: If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the
       Код: src/Метрики/Классы/ОтелМетр.os:730
       Было: Поскольку валидация имени отсутствует, ошибка о невалидном имени не эмитируется.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:106
       Было: СброситьБуфер() возвращает ОтелРезультатыЭкспорта.Успех() безусловно (no-op), статус таймаута/ошибки
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:106
       Было: Параметр ТаймаутМс есть, но помечен UnusedParameters — таймаут не учитывается; реализация — синхронн
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MeterConfig]
       partial → found
       Текст: If a `Meter` is disabled, it MUST behave equivalently to No-op Meter.
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:93
       Было: Синхронные инструменты при МетрВключен=Ложь возвращают управление без записи; но ВызватьCallbackИСоб
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MeterConfig]
       partial → found
       Текст: The value of `enabled` MUST be used to resolve whether an instrument is Enabled.
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:265
       Было: Включен(Атрибуты) = МетрВключен.Получить() И Включен.Получить() реализован для синхронных инструмент
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricProducer]
       not_found → partial
       Текст: `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of pro
       Код: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:23
       Было: Интерфейс ИнтерфейсПродюсерМетрик.Произвести(ФильтрМетрик) не принимает и нет конфигурации Aggregati
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: To construct a `MetricReader` when setting up an SDK, at least the following SHOULD be provided: * T
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:570
       Было: Конструктор принимает Экспортер, ИнтервалЭкспортаМс, ЛимитМощности, агрегацию гистограмм. MetricFilt
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → found
       Текст: Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that 
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:382
       Было: Перед вызовом мульти-callback инструменты очищаются, но изоляция per-MetricReader не строгая: если н
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       not_found → partial
       Текст: The implementation SHOULD use a timeout to prevent indefinite callback execution.
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:230
       Было: Callback'и async-инструментов выполняются синхронно без таймаута: ВызватьМультиОбратныеВызовы и Вызв
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:205
       Было: Метод Закрыть() не принимает параметр таймаута. Есть асинхронная обертка ЗакрытьАсинхронно(), но без
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: SDKs SHOULD return some failure for these calls, if possible.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:84
       Было: После Закрыть() флаг Закрыт=Истина, но СброситьБуфер()/СобратьИЭкспортировать() не проверяют этот фл
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:149
       Было: Закрыть() — Процедура (void), не возвращает статус успеха/ошибки/таймаута.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       not_found → found
       Текст: The default protocol SHOULD be http/protobuf, unless there are strong reasons for SDKs to select grp
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:222
       Было: Дефолт протокола в коде - 'http/json' (см. ПротоколHttpJson = "http/json" и default параметра 'proto
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Specify Protocol]
       not_found → found
       Текст: If no configuration is provided the default transport SHOULD be http/protobuf unless SDKs have good 
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:636
       Было: Default protocol установлен в 'http/json' (ПараметрСигналаИлиОбщий(... 'protocol', ПротоколHttpJson)
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / User Agent]
       not_found → found
       Текст: OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the export
       Код: src/Экспорт/Классы/ОтелHttpТранспорт.os:200
       Было: В коде HTTP/gRPC транспортов (ОтелHttpТранспорт, ОтелGrpcТранспорт) не задаётся заголовок User-Agent
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / User Agent]
       not_found → found
       Текст: The format of the header SHOULD follow RFC 7231.
       Код: src/Экспорт/Классы/ОтелHttpТранспорт.os:200
       Было: User-Agent заголовок не формируется, формат RFC 7231 не применяется.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Detecting resource information from the environment]
       partial → found
       Текст: Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attrib
       Код: src/Ядро/Классы/ОтелРесурс.os:138
       Было: Все встроенные детекторы (host, process, processor) безусловно устанавливают непустой Schema URL '1.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Specifying resource information via an environment variable]
       partial → found
       Текст: The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge 
       Код: src/Ядро/Классы/ОтелРесурс.os:137
       Было: OTEL_RESOURCE_ATTRIBUTES читается и применяется только в составе дефолтной инициализации ресурса (За
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Concurrency requirements]
       partial → found
       Текст: Link - Links are immutable and SHOULD be safe for concurrent use by default.
       Код: src/Трассировка/Классы/ОтелСпан.os:166
       Было: Link реализован inline как `Новый Соответствие()` (не отдельный класс), нет документирующего коммент
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Set Status]
       n_a → found
       Текст: Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generat
       Код: src/Трассировка/Классы/ОтелСпан.os:466
       Было: Требование адресовано инструментам анализа/визуализации (downstream-системы), а не SDK/API. Вне обла
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / IdGenerator randomness]
       not_found → partial
       Текст: If the SDK uses an `IdGenerator` extension point, the SDK SHOULD allow the extension to determine wh
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:335
       Было: Интерфейс IdGenerator (УстановитьГенераторИд) поддерживает только генерацию ID, но не предоставляет 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Presumption of TraceID randomness]
       partial → found
       Текст: For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Contex
       Код: src/Трассировка/Модули/ОтелСэмплер.os:356
       Было: Сэмплер TraceIdRatioBased презюмирует случайность, используя TraceId для решения. Однако нет логики 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Random trace flag]
       not_found → found
       Текст: For root span contexts, the SDK SHOULD set the `Random` flag in the trace flags when it generates Tr
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:344
       Было: ВычислитьФлагиТрассировки в ОтелТрассировщик.os:303 устанавливает только бит 0 (sampled=1) для корне
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Sampling]
       partial → found
       Текст: However, Span Exporter SHOULD NOT receive them unless the Sampled flag was also set.
       Код: src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:49
       Было: ОтелПростойПроцессорСпанов и ОтелПакетныйПроцессорСпанов передают экспортеру все завершённые спаны (
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Sampling]
       partial → found
       Текст: Span Exporters MUST receive those spans which have Sampled flag set to true and they SHOULD NOT rece
       Код: src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:41
       Было: Процессоры спанов передают экспортёру и спаны с RECORD_ONLY (Sampled=false), нет отдельного шага фил
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:159
       Было: Закрыть — Процедура (void), не возвращает статус; ошибки внутренних процессоров проглатываются (Лог.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:159
       Было: Метод Закрыть() на TracerProvider не принимает параметр таймаута; внутренний ОтелКомпозитныйПроцессо
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Span Limits]
       partial → found
       Текст: The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`.
       Код: src/Трассировка/Классы/ОтелЛимитыСпана.os:91
       Было: Поля называются МаксСобытий (MaxEvents) и МаксЛинков (MaxLinks), что семантически близко, но не точн
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / TraceIdRatioBased]
       partial → found
       Текст: The precision of the number SHOULD follow implementation language standards and SHOULD be high enoug
       Код: src/Трассировка/Модули/ОтелСэмплер.os:125
       Было: Precision жёстко ограничена 6 знаками после запятой (Формат с ЧДЦ=6) вместо использования стандартно
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / TraceIdRatioBased]
       partial → found
       Текст: The precision of the number SHOULD follow implementation language standards and SHOULD be high enoug
       Код: src/Трассировка/Модули/ОтелСэмплер.os:125
       Было: При фиксированной precision=6 два сэмплера с долями, отличающимися менее чем на 1e-6, дадут одинаков
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Tracer Creation]
       n_a → found
       Текст: It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` (see API).
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:69
       Было: OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен). Конвенциональ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (5) - агент нашёл дополнительные:

     [Metrics Sdk] MUST found: The SDK MUST accept the following criteria: name, type, unit, meter_name, meter_
     [Trace Api] SHOULD found: its `name` property SHOULD be set to an empty string, and a message reporting th
     [Trace Sdk] MUST NOT found: If configuration is updated (e.g., adding a `SpanProcessor`), the updated config
     [Trace Sdk] SHOULD found: SDKs SHOULD return a valid no-op Tracer for these calls, if possible.
     [Trace Sdk] SHOULD found: SDKs SHOULD ignore these calls gracefully, if possible.

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (5) - были раньше, теперь нет:

     [Metrics Sdk] MUST found: The SDK MUST accept the following criteria:
     [Trace Api] SHOULD found: its `name` property SHOULD be set to an empty string.
     [Trace Sdk] MUST NOT found: (i.e. it MUST NOT matter whether a `Tracer` was obtained from the `TracerProvide
     [Trace Sdk] SHOULD partial: After the call to `Shutdown`, subsequent attempts to get a `Tracer` are not allo
     [Trace Sdk] SHOULD found: After the call to `Shutdown`, subsequent calls to `OnStart`, `OnEnd`, or `ForceF

  Итого изменений: 80
    Понижений: 19, Повышений: 51, Боковых: 0
    Новых req: 5, Пропущенных req: 5
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
