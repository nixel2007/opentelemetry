# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             670    686 +   16 ✅
  partial           100     87   -13
  not_found          44     41    -3
  n_a                10     10     0
  Всего             824    824 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (29) - требует перепроверки:

     [Env Vars / Enum]
       found → partial
       Текст: For sources accepting an enum value, if the user provides a value the implementation does not recogn
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:267 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:293
       Пояснение: Предупреждение и безопасное игнорирование реализовано для otel.traces.sampler (строка 293) и otel.propagators (строка 529), но для otel.traces.exporte
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Api / Enabled]
       found → partial
       Текст: When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then M
       Расположение: src/Логирование/Классы/ОтелЛоггер.os:158 → src/Логирование/Классы/ОтелЛоггер.os:68
       Пояснение: Контекст = Неопределено разрешается в текущий контекст только внутри ТрассировкаНеСэмплирована (ветка trace-based фильтрации), но в процессор Включен 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no erro
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:137 → src/Логирование/Классы/ОтелПровайдерЛогирования.os:122
       Пояснение: Синхронный СброситьБуфер() ничего не возвращает (NO ERROR/успех неотличим). Статус доступен только через СброситьБуферАсинхронно().
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Расположение: src/Экспорт/Классы/ОтелЭкспортерЛогов.os:45 → src/Экспорт/Классы/ОтелЭкспортерЛогов.os:62
       Пояснение: ОтелЭкспортерЛогов.СброситьБуфер() не принимает параметр таймаута и не имеет механизма прерывания по таймауту (синхронный экспортер, сам экспорт уже о
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Concurrency requirements]
       found → partial
       Текст: Instrument - all methods MUST be documented that implementations need to be safe for concurrent use 
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:45 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:49
       Пояснение: Потокобезопасность документирована только для синхронных инструментов (ОтелБазовыйСинхронныйИнструмент:49-50). Базовый класс наблюдаемых инструментов 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Instrument]
       partial → n_a
       Текст: Language-level features such as the distinction between integer and floating point numbers SHOULD be
       Расположение: src/Метрики/Классы/ОтелМетр.os:607 → -
       Пояснение: В OneScript единый числовой тип System.Decimal - различия integer/floating point на уровне языка отсутствуют, поэтому требование неприменимо к платфор
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Instrument unit]
       found → partial
       Текст: It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII string.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:253 → src/Метрики/Классы/ОтелМетр.os:621
       Пояснение: Строки в OneScript регистрозависимы по умолчанию (сравнение '=' case-sensitive), поэтому case-sensitivity обеспечивается платформой. Однако проверки н
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / MeterProvider]
       found → partial
       Текст: Thus, the API SHOULD provide a way to set/register and access a global default `MeterProvider`.
       Расположение: src/Ядро/Модули/ОтелГлобальный.os:31 → src/Ядро/Модули/ОтелГлобальный.os:100
       Пояснение: Глобальный доступ к Meter осуществляется через ОтелГлобальный.ПолучитьМетр(), установка провайдера метрик - через билдер SDK (ОтелПостроительSdk.Устан
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Duplicate instrument registration]
       partial → not_found
       Текст: Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Met
       Расположение: src/Метрики/Классы/ОтелМетр.os:57 → -
       Пояснение: Код возвращает ранее зарегистрированный инструмент (ОтелМетр.os:59), а не регистрирует второй Metric объект с другой единицей. Второй инструмент не со
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ExemplarReservoir]
       found → partial
       Текст: ...and the reservoir MUST be given the `Attributes` associated with its timeseries point either at c
       Пояснение: Параметр АтрибутыСерии передаётся в Предложить(), но в документирующем комментарии не подчёркнуто, что филтрованный набор атрибутов может расходиться 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument advisory parameters]
       found → partial
       Текст: If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed
       Расположение: src/Метрики/Классы/ОтелМетр.os:692-705 → src/Метрики/Классы/ОтелМетр.os:796
       Пояснение: ПроверитьСовет эмитирует предупреждения и при некорректном типе Совет (не Структура) фактически игнорирует его (ПолучитьГраницыИзСовета/ПолучитьКлючиА
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument selection criteria]
       found → n_a
       Текст: Therefore, the instrument selection criteria can be structured to accept the criteria, but MUST NOT 
       Расположение: src/Метрики/Классы/ОтелСелекторИнструментов.os:159 → -
       Пояснение: SDK не принимает дополнительные критерии сверх перечисленных в спецификации, поэтому требование к 'additional criteria' не применимо.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Interface Definition]
       found → partial
       Текст: Shutdown SHOULD be called only once for each `MetricExporter` instance.
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:53 → src/Экспорт/Классы/ОтелЭкспортерМетрик.os:64
       Пояснение: Закрыть() идемпотентен (Закрыт.Установить(Истина) можно вызывать повторно без побочных эффектов), но явной защиты/проверки повторного вызова (как в ри
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: If not configured, the Cumulative temporality SHOULD be used.
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:107 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:262
       Пояснение: Временность делегируется экспортеру через Экспортер.ПолучитьВременнуюАгрегацию; явного fallback на Cumulative в читателе нет - зависит от экспортера.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       found → partial
       Текст: Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:228 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:226
       Пояснение: Callback вызывается при сборе конкретным reader, но состояние инструмента общее для всех reader'ов — нет явной изоляции наблюдений по reader'у.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       found → partial
       Текст: Implementation SHOULD use the filter as early as possible to gain as much performance gain possible 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:366 → src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13
       Пояснение: Фильтр принимается в интерфейсе, но применение зависит от реализации продюсера. Никакой внутренней реализации продюсера в SDK нет - только интерфейс, 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Produce batch]
       partial → not_found
       Текст: If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include
       Расположение: src/Метрики/Классы/ОтелДанныеМетрики.os:42 → -
       Пояснение: Интерфейс продюсера не требует и не документирует привязку InstrumentationScope, идентифицирующего сам MetricProducer. Данные продюсера добавляются в 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → partial
       Текст: The option SHOULD accept any form allowed by the underlying gRPC client implementation.
       Расположение: src/Экспорт/Классы/ОтелGrpcТранспорт.os:37 → src/Экспорт/Классы/ОтелGrpcТранспорт.os:1
       Пояснение: gRPC транспорт принимает адрес и передаёт его в oint/api/grpc клиент, но специальная обработка форм адреса (unix:, dns:, etc.) не реализована — URL ра
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       partial → not_found
       Текст: If the gRPC client implementation does not support an endpoint with a scheme of `http` or `https` th
       Расположение: src/Экспорт/Классы/ОтелGrpcТранспорт.os:37 → -
       Пояснение: Преобразование URL http/https в альтернативную форму для gRPC-клиента не реализовано — адрес передаётся как есть.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → not_found
       Текст: However, if they are already implemented, they SHOULD continue to be supported as they were part of 
       Пояснение: Obsolete-переменные OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE не реализованы и, следовательно, требование о сохранении сов
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Specify Protocol]
       found → partial
       Текст: If they support only one, it SHOULD be `http/protobuf`.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:572 → src/Экспорт/Классы/ОтелHttpТранспорт.os:64
       Пояснение: SDK поддерживает более одного транспорта (grpc и http/json), поэтому условие «если поддерживается только один» формально не активно; однако реального 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Global Propagators]
       found → partial
       Текст: If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:457 → src/Ядро/Модули/ОтелГлобальный.os:132
       Пояснение: В SDK нет pre-configured пропагаторов: если пользователь не задал, ПолучитьПропагаторы возвращает ОтелНоопПропагатор вместо композита W3C Trace Contex
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Behavior of the API in the absence of an installed SDK]
       partial → not_found
       Текст: If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly witho
       Расположение: src/Трассировка/Классы/ОтелТрассировщик.os:81 → -
       Пояснение: Нет проверки ЗаписьАктивна()/IsRecording у родительского спана в ОтелТрассировщик.НачатьСпан - всегда создаётся новый экземпляр (ОтелСпан или ОтелНооп
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / End]
       found → partial
       Текст: This operation itself MUST NOT perform blocking I/O on the calling thread.
       Пояснение: Сам Завершить() не выполняет I/O напрямую, но синхронно вызывает Процессор.ПриЗавершении(), и ОтелПростойПроцессорСпанов экспортирует спан синхронно в
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span]
       found → partial
       Текст: However, alternative implementations MUST NOT allow callers to create `Span`s directly.
       Расположение: src/Трассировка/Классы/ОтелСпан.os:1 → src/Трассировка/Классы/ОтелСпан.os:599
       Пояснение: Конструктор ОтелСпан публичный, OneScript не поддерживает ограничение видимости конструктора. Пользователь может вызвать Новый ОтелСпан(...) напрямую,
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       found → partial
       Текст: There MUST NOT be any API for creating a `Span` other than with a `Tracer`.
       Расположение: src/Трассировка/Классы/ОтелТрассировщик.os:27 → src/Трассировка/Классы/ОтелСпан.os:599
       Пояснение: Публичный конструктор ОтелСпан доступен для прямого вызова (Новый ОтелСпан(...)). Платформа OneScript не позволяет ограничить видимость конструктора. 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Wrapping a SpanContext in a Span]
       found → partial
       Текст: The API MUST provide an operation for wrapping a `SpanContext` with an object implementing the `Span
       Расположение: src/Трассировка/Классы/ОтелНоопСпан.os:273 → src/Трассировка/Классы/ОтелНоопСпан.os:279
       Пояснение: Операция реализована через конструктор Новый ОтелНоопСпан(КонтекстСпана), но отдельного метода API (например, Tracer.WrapSpanContext) не существует. И
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Wrapping a SpanContext in a Span]
       partial → not_found
       Текст: If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possib
       Расположение: src/Трассировка/Классы/ОтелНоопСпан.os:273 → -
       Пояснение: Тип ОтелНоопСпан зарегистрирован как публичный класс в lib.config и напрямую инстанциируется снаружи (пропагаторы, Tracer). Нет скрытой/пакетной видим
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / `ForceFlush()`]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:126 → src/Экспорт/Классы/ОтелЭкспортерСпанов.os:57
       Пояснение: СброситьБуфер() экспортера не принимает параметр таймаута. Для синхронного экспортера это no-op (завершается мгновенно), но механизма прерывания по та
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (50) - требует перепроверки:

     [Env Vars / Boolean]
       partial → found
       Текст: Any value not explicitly defined here as a true value, including unset and empty values, MUST be int
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:851
       Было: Функция Включено() использует инвертированную семантику: при unset/empty применяется default "true" 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Boolean]
       partial → found
       Текст: All Boolean environment variables SHOULD be named and defined such that false is the expected safe d
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:852
       Было: Используется OTEL_ENABLED с дефолтом "true" вместо стандартного OTEL_SDK_DISABLED (дефолт false). Се
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Enabled]
       partial → found
       Текст: Any modifications to parameters inside Enabled MUST NOT be propagated to the caller.
       Код: src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:26
       Было: Включен() в интерфейсе процессора не принимает параметров (Context, InstrumentationScope, SeverityNu
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       not_found → partial
       Текст: ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71
       Было: СброситьБуфер объявлена как Процедура (void) - нет возвращаемого статуса/Обещания, таймаут неотличим
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Logger Creation]
       partial → found
       Текст: It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` (see API).
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:56
       Было: Логгер создаётся через Провайдер.ПолучитьЛоггер() и ОтелПостроительЛоггера.Построить(), но класс Оте
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Logger Creation]
       partial → found
       Текст: In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be 
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:63
       Было: При ИмяБиблиотеки = Неопределено код подменяет значение на пустую строку (строки 61-63) вместо сохра
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / OnEmit]
       partial → found
       Текст: This method is called synchronously on the thread that emitted the LogRecord, therefore it SHOULD NO
       Код: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:17
       Было: ОтелПростойПроцессорЛогов.ПриПоявлении вызывает Экспортер.Экспортировать синхронно под блокировкой -
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ShutDown]
       partial → found
       Текст: Shutdown SHOULD be called only once for each LogRecordProcessor instance.
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:132
       Было: Нет идемпотентной защиты от повторного вызова Закрыть() - ни в ОтелПростойПроцессорЛогов, ни в базов
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ShutDown]
       partial → found
       Текст: After the call to Shutdown, subsequent calls to OnEmit are not allowed. SDKs SHOULD ignore these cal
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:67
       Было: Базовый пакетный процессор игнорирует Обработать при Закрыт=Истина. В ОтелПростойПроцессорЛогов.ПриП
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ShutDown]
       not_found → partial
       Текст: Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:87
       Было: Закрыть объявлена как Процедура (void) во всех реализациях - нет возвращаемого статуса/Обещания, тай
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Therefore, this API MUST be structured to accept a variable number of callback functions, including 
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147
       Было: СоздатьНаблюдаемыйСчетчик принимает один опциональный Callback (включая none), но не переменное числ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API MUST support creation of asynchronous instruments by passing zero or more callback functions
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147
       Было: В конструкторе можно передать zero или один callback; дополнительные callback добавляются через Доба
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions MUST be documented as follows for the end user:
       Код: src/Метрики/Классы/ОтелМетр.os:276
       Было: Параметр Callback задокументирован как "callback для наблюдения", но явно не документирует требовани
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions SHOULD be reentrant safe.
       Код: src/Метрики/Классы/ОтелМетр.os:277
       Было: Требование относится к пользовательской документации callback; явного указания на reentrancy в doc-к
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions SHOULD NOT take an indefinite amount of time.
       Код: src/Метрики/Классы/ОтелМетр.os:279
       Было: В doc-комментарии нет указания на ограничение по времени выполнения callback.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions SHOULD NOT make duplicate observations (more than one Measurement with the same a
       Код: src/Метрики/Классы/ОтелМетр.os:280
       Было: В doc-комментарии нет указания на запрет дублирующих observations.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Configuration]
       partial → found
       Текст: A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardi
       Код: src/Метрики/Классы/ОтелМетр.os:645
       Было: ОтелПредставление хранит ЛимитМощностиАгрегации (getter/setter), но значение нигде не применяется к 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Custom ExemplarReservoir]
       partial → found
       Текст: although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reserv
       Код: src/Метрики/Классы/ОтелПредставление.os:83
       Было: Одна инстанция резервуара используется на уровне инструмента и хранит данные по КлючАтрибутов внутри
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarReservoir]
       partial → found
       Текст: The "offer" method SHOULD have the ability to pull associated trace and span information without nee
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:126
       Было: Метод Предложить принимает КонтекстСпана (trace/span info), но Baggage и полный Context не доступны 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       not_found → partial
       Текст: `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no erro
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94
       Было: СброситьБуфер() объявлена как Процедура - не возвращает ни ERROR, ни NO ERROR статуса.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       not_found → partial
       Текст: Arithmetic sum of `Measurement` values in population. This SHOULD NOT be collected when used with in
       Код: src/Метрики/Классы/ОтелАгрегаторГистограммы.os:51
       Было: sum всегда собирается в ОтелАгрегаторГистограммы/ОтелАгрегаторЭкспоненциальнойГистограммы независимо
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       partial → found
       Текст: SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good
       Код: src/Метрики/Классы/ОтелАгрегаторГистограммы.os:118
       Было: Дефолтные границы применяются, но массив СтандартныеГраницы() пропускает границу 7500 из спецификаци
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       partial → found
       Текст: The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily 
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:34
       Было: Транспорт реализует retry-логику через СтратегияПовтора для кодов 429/502/503/504 с экспоненциальной
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter Creation]
       partial → found
       Текст: In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be ret
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:66
       Было: При Неопределено имя принудительно заменяется на пустую строку ('') - оригинальное невалидное значен
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: This function SHOULD be obtained from the `exporter`.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:265
       Было: Default aggregation задаётся через параметр НоваяАгрегацияГистограмм и фиксированный селектор в Иниц
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Name conflict]
       partial → found
       Текст: When this happens, the Meter MUST return an instrument using the first-seen instrument name and log 
       Код: src/Метрики/Классы/ОтелМетр.os:56
       Было: Первый найденный инструмент возвращается (ИнструментыПоИмени по НРег(Имя)), но ПроверитьКонфликтДеск
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Observations inside asynchronous callbacks]
       not_found → partial
       Текст: The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered ca
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:81
       Было: Нет кода, игнорирующего использование async API вне зарегистрированных callback-ов; внешние наблюден
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` MUST be called only once for each `MeterProvider` instance.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:144
       Было: Флаг Закрыт устанавливается, но Закрыть() не имеет явной защиты от повторного вызова (нет СравнитьИУ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: The SDK MUST accept the following stream configuration parameters:
       Код: src/Метрики/Классы/ОтелПредставление.os:156
       Было: ОтелПредставление принимает все параметры (name, description, attribute_keys, aggregation, exemplar_
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       not_found → partial
       Текст: In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector tha
       Было: SDK не валидирует, что при заданном name селектор сужен до одного инструмента, и не применяет fail-f
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Stream configuration]
       partial → found
       Текст: If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST appl
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:253
       Было: Дефолт из MetricReader применяется ко всем инструментам через ПрименитьНастройкиЧитателяКМетру, но V
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       partial → found
       Текст: The following configuration options MUST be available to configure the OTLP exporter.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:603
       Было: Реализованы Endpoint, Headers, Compression, Timeout, Protocol (общие и per-signal). Отсутствуют Inse
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       partial → found
       Текст: Additionally, the option MUST accept a URL with a scheme of either `http` or `https`.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:665
       Было: Адрес передаётся в ОтелGrpcТранспорт как есть; явной обработки http/https схемы и её приоритета над 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Propagators Distribution]
       partial → found
       Текст: The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST 
       Код: src/Пропагация/Классы/ОтелB3Пропагатор.os:1
       Было: Пропагаторы W3C TraceContext, W3C Baggage и B3 реализованы, но входят в состав основного opm-пакета 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Propagators Distribution]
       n_a → found
       Текст: It MUST NOT use `OpenTracing` in the resulting propagator name as it is not widely adopted format in
       Код: src/Пропагация/Классы/
       Было: Пропагатор OT Trace не реализован в SDK, требование об именовании к нему неприменимо.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Specifying resource information via an environment variable]
       partial → found
       Текст: The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge 
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:151
       Было: OTEL_RESOURCE_ATTRIBUTES извлекается в СоздатьРесурс, но автоматического merge с user-provided ресур
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Specifying resource information via an environment variable]
       not_found → partial
       Текст: In case of any error, e.g. failure during the decoding process, the entire environment variable valu
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:742
       Было: В РазобратьПарыКлючЗначение нет обработки ошибок декодирования: при сбое исключение пробрасывается, 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Span Creation]
       partial → found
       Текст: If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument
       Код: src/Трассировка/Классы/ОтелПостроительСпана.os:108
       Было: Параметр доступен через УстановитьВремяНачала без явного документирующего предупреждения о логическо
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / TraceState]
       partial → found
       Текст: If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data and MU
       Код: src/Трассировка/Классы/ОтелСостояниеТрассировки.os:76
       Было: Невалидные параметры молча игнорируются (возврат ЭтотОбъект без изменений); отсутствует явное логиро
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Wrapping a SpanContext in a Span]
       n_a → found
       Текст: This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable.
       Код: src/Трассировка/Классы/ОтелНоопСпан.os
       Было: В OneScript нет языковых механизмов наследования/переопределения классов. Платформенное ограничение 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Concurrency requirements]
       partial → found
       Текст: Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrentl
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:368
       Было: Закрыт - АтомарноеБулево, но доступ к кэшу Трассировщики (Соответствие) и списку Процессоры не защищ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Enabled]
       partial → found
       Текст: Otherwise, it SHOULD return `true`.
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:38
       Было: Возврат Истина корректен для случая без конфигурации при наличии процессоров, но поведение при задан
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Explicit randomness]
       partial → found
       Текст: SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value.
       Код: src/Трассировка/Классы/ОтелСостояниеТрассировки.os:189
       Было: Сэмплер сохраняет родительский TraceState через параметр РодительскоеСостояниеТрассировки и передаёт
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush()]
       not_found → partial
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71-73
       Было: Процедура СброситьБуфер(ТаймаутМс) не возвращает статус, поэтому вызывающий не может отличить успех,
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Presumption of TraceID randomness]
       partial → found
       Текст: For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Contex
       Код: src/Трассировка/Модули/ОтелСэмплер.os:139
       Было: TraceIdRatioBased сэмплер использует TraceID как источник случайности (презумпция случайности), но н
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / SDK Span creation]
       partial → found
       Текст: When asked to create a Span, the SDK MUST act as if doing the following in order:
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:56
       Было: Порядок TraceId-resolve → ShouldSample → создание спана соблюдён, но spanId генерируется только для 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown()]
       not_found → partial
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:77; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80
       Было: Процедура Закрыть(ТаймаутМс) не возвращает статус - нельзя отличить успех, неудачу и таймаут; логиро
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Tracer Creation]
       partial → found
       Текст: It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` (see API).
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:65
       Было: TracerProvider.ПолучитьТрассировщик и ПостроительТрассировщика - штатный путь, но в OneScript нельзя
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / `Export(batch)`]
       partial → found
       Текст: Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Код: src/Экспорт/Классы/ОтелЭкспортерСпанов.os:48
       Было: Экспортировать делегирует в Транспорт.Отправить; явного таймаута в самом экспортере нет — верхний пр
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / `Export(batch)`]
       partial → found
       Текст: Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Код: src/Экспорт/Классы/ОтелЭкспортерСпанов.os:47
       Было: В Экспортировать нет параметра таймаута и нет явной логики отсечения с возвратом Failure по таймауту
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (16) - агент нашёл дополнительные:

     [Context] MUST found: The API MUST accept the following parameters: * A `Token` that was returned by a
     [Logs Sdk] MUST NOT found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Logs Sdk] MUST found: `Enabled` MUST return `false` when either: there are no registered `LogRecordPro
     [Metrics Api] SHOULD found: synchronous instruments SHOULD provide this `Enabled` API.
     [Metrics Sdk] SHOULD found: This implementation MUST store at most one measurement that falls within a histo
     [Metrics Sdk] MUST found: This extension MUST be configurable on a metric View, although individual reserv
     [Metrics Sdk] MUST partial: This MUST be clearly documented in the API and the reservoir MUST be given the `
     [Metrics Sdk] SHOULD partial: The default output `aggregation` (optional), a function of instrument kind. This
     [Metrics Sdk] SHOULD NOT found: The SDK MUST support multiple `MetricReader` instances to be registered on the s
     [Metrics Sdk] SHOULD partial: SDKs SHOULD return some failure for these calls, if possible.
     [Metrics Sdk] SHOULD not_found: For asynchronous instrument, the start timestamp SHOULD be:
     [Otlp Exporter] MUST found: The implementation MUST honor the following URL components: scheme (http or http
     [Otlp Exporter] MUST partial: Options MUST be one of: grpc, http/protobuf, http/json.
     [Trace Api] MUST found: This API MUST accept the following parameters: `name` (required), `version` (opt
     [Trace Api] SHOULD found: its `name` property SHOULD be set to an empty string.
     [Trace Api] SHOULD found: a message reporting that the specified value is invalid SHOULD be logged.

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (16) - были раньше, теперь нет:

     [Context] MUST found: The API MUST accept the following parameters:
     [Logs Sdk] MUST found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Logs Sdk] MUST found: Enabled MUST return false when either: there are no registered LogRecordProcesso
     [Metrics Api] SHOULD found: To help users avoid performing computationally expensive operations when recordi
     [Metrics Sdk] SHOULD found: and SHOULD use a uniformly-weighted sampling algorithm based on the number of me
     [Metrics Sdk] MUST found: This extension MUST be configurable on a metric View,
     [Metrics Sdk] MUST found: The "offer" method MAY accept a filtered subset of `Attributes` which diverge fr
     [Metrics Sdk] SHOULD found: This function SHOULD be obtained from the `exporter`.
     [Metrics Sdk] SHOULD NOT partial: and the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NO
     [Metrics Sdk] SHOULD partial: After the call to `Shutdown`, subsequent invocations to `Collect` are not allowe
     [Metrics Sdk] SHOULD not_found: For asynchronous instrument, the start timestamp SHOULD be: - The creation time 
     [Otlp Exporter] MUST found: The implementation MUST honor the following URL components:
     [Otlp Exporter] MUST found: Protocol: The transport protocol. Options MUST be one of: `grpc`, `http/protobuf
     [Trace Api] MUST found: This API MUST accept the following parameters:
     [Trace Api] SHOULD found: In case an invalid name (null or empty string) is specified, a working Tracer im
     [Trace Api] SHOULD found: In case an invalid name (null or empty string) is specified, a working Tracer im

  Итого изменений: 111
    Понижений: 29, Повышений: 50, Боковых: 0
    Новых req: 16, Пропущенных req: 16
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
