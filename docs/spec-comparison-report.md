# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             648    683 +   35 ✅
  partial           138    173 +   35
  not_found          38     99 +   61 ⚠️  РЕГРЕССИЯ
  n_a                52     92 +   40
  Всего             876   1047 +  171

  🔴 ПОНИЖЕНИЕ СТАТУСА (36) - требует перепроверки:

     [Baggage Api / Propagation]
       found → partial
       Текст: The API layer or an extension package MUST include the following `Propagator`s:
       Расположение: src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:1 → src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:166
       Пояснение: TextMapPropagator ОтелW3CBaggageПропагатор (Внедрить/Извлечь/Поля, заголовок baggage, key=value;properties, лимит 8192) входит в основной пакет (lib.c
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Concurrency requirements]
       found → partial
       Текст: LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:79 → src/Логирование/Классы/ОтелПровайдерЛогирования.os:75-90,122,141,327-328
       Пояснение: ForceFlush и Shutdown безопасны: Закрыть() использует CAS на АтомарноеБулево (стр. 141; покрыто тестом конкурентного ЗакрытьАсинхронно), СброситьБуфер
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Concurrency requirements]
       found → partial
       Текст: Logger - all methods MUST be safe to be called concurrently.
       Расположение: src/Логирование/Классы/ОтелЛоггер.os:114 → src/Логирование/Классы/ОтелЛоггер.os:80-88,171-173,196-207,316
       Пояснение: Записать()/Включен() не мутируют разделяемое состояние логгера (запись принадлежит вызывающему, scope и resource неизменяемы, цепочка процессоров copy
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Enabled]
       found → partial
       Текст: Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller.
       Расположение: src/Логирование/Классы/ОтелЛоггер.os:97 → src/Логирование/Классы/ОтелЛоггер.os:98
       Пояснение: ОтелЛоггер.Включен передаёт процессорам защищённую копию InstrumentationScope (ЗащищеннаяКопияОбласти, стр. 97, 179-193), а неявный текущий Context - 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Event to span event bridge]
       found → partial
       Текст: all `LogRecord` Attributes MUST be copied to the span event as span event attributes.
       Пояснение: Все атрибуты записи попадают в span event, но не копируются: мост передаёт в Спан.ДобавитьСобытие сам объект ЗаписьЛога.Атрибуты() (стр. 76, 82), а От
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ForceFlush]
       found → partial
       Текст: This is a hint to ensure that any tasks associated with `LogRecord`s for which the `LogRecordProcess
       Пояснение: Записи, находящиеся в буфере, экспортируются синхронно до возврата (СброситьБуфер → ЭкспортироватьВсеПакеты, стр. 76-77, 176-202). Но записи, уже извл
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Пояснение: СброситьБуфер возвращает ОтелРезультатЭкспорта (Успех/Ошибка/Таймаут), ПринудительноВыгрузитьСРезультатом - ОтелРезультатЗакрытия; простой процессор в
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ShutDown]
       found → partial
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Пояснение: Закрыть возвращает ОтелРезультатЗакрытия (Успех/Ошибка/Таймаут) в пакетном (ОтелБазовыйПакетныйПроцессор, стр. 89-111) и простом (ОтелПростойПроцессор
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:151 → src/Логирование/Классы/ОтелПровайдерЛогирования.os:140-163,210-213
       Пояснение: Закрыть() возвращает ОтелРезультатЗакрытия (Успех/Ошибка/Таймаут), ЗакрытьАсинхронно() - Обещание, однако результат закрытия самих процессоров отбрасы
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:160 → src/Логирование/Классы/ОтелПровайдерЛогирования.os:140,148-155
       Пояснение: Закрыть(ТаймаутМс = 30000) принимает таймаут, но проверяет его только между процессорами (стр. 149-153) и не передает оставшееся время в Процессор.Зак
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Asynchronous Counter creation]
       found → partial
       Текст: The API MUST treat observations from a single callback as logically taking place at a single instant
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:420 → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:433
       Пояснение: Для callback-ов отдельного инструмента (переданных в СоздатьНаблюдаемыйСчетчик или через ДобавитьCallback) требование в основном выполнено: ВызватьCal
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Asynchronous Counter creation]
       found → partial
       Текст: The API MUST treat observations from a single callback as logically taking place at a single instant
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:436 → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:450
       Пояснение: Идентичные startTimeUnixNano/timeUnixNano (ОтелБазовыйНаблюдаемыйИнструмент.os:450-451) гарантируются только в пределах одного вызова ПреобразоватьЗап
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API MUST support creation of asynchronous instruments by passing zero or more `callback` functio
       Пояснение: Callback-и, переданные в СоздатьНаблюдаемыйСчетчик/СоздатьНаблюдаемыйРеверсивныйСчетчик/СоздатьНаблюдаемыйДатчик (Неопределено, Действие или Массив из
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Callback functions MUST be documented as follows for the end user:
       Расположение: src/Метрики/Классы/ОтелМетр.os:321 → src/Метрики/Классы/ОтелМетр.os:292
       Пояснение: Рекомендации для callback-ов задокументированы в комментариях СоздатьНаблюдаемыйСчетчик/СоздатьНаблюдаемыйРеверсивныйСчетчик/СоздатьНаблюдаемыйДатчик 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of 
       Расположение: src/Метрики/Классы/ОтелМетр.os:656 → src/Метрики/Классы/ОтелМетр.os:603
       Пояснение: Мульти-callback ассоциируется при регистрации с объявленным набором инструментов (ОтелМетр.ЗарегистрироватьОбратныйВызов(Callback, НовыеИнструменты, С
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Duplicate instrument registration]
       found → partial
       Текст: To accommodate the recommendations from the data model, the SDK MUST aggregate data from identical I
       Расположение: src/Метрики/Классы/ОтелМетр.os:65 → src/Метрики/Классы/ОтелМетр.os:1016,1087,324,385,447
       Пояснение: Для синхронных инструментов идентичные регистрации (имя без учёта регистра, вид, единица, описание) получают один и тот же экземпляр (НайтиЗарегистрир
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument advisory parameters]
       found → partial
       Текст: When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters.
       Расположение: src/Метрики/Классы/ОтелМетр.os:1222 → src/Метрики/Классы/ОтелМетр.os:1330
       Пояснение: ПроверитьСовет (стр. 1330-1362, вызывается во всех СоздатьXxx с Совет) проверяет только форму: Совет — Структура, ГраницыГистограммы и КлючиАтрибутов 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument advisory parameters]
       found → partial
       Текст: If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed
       Расположение: src/Метрики/Классы/ОтелМетр.os:1238 → src/Метрики/Классы/ОтелМетр.os:1335,1346,1354; src/Метрики/Классы/ОтелАгрегаторГистограммы.os:203
       Пояснение: Для ошибок формы, которые обнаруживает ПроверитьСовет, поведение соответствует спеке: Лог.Предупреждение и параметр отбрасывается (Совет не Структура 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Interface Definition]
       found → partial
       Текст: `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:67 → src/Экспорт/Классы/ОтелЭкспортерМетрик.os:61,67; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:87,153,288,342; src/Экспорт/Классы/ОтелHttpТранспорт.os:195-205,219-228
       Пояснение: ОтелЭкспортерМетрик.Экспортировать ограничивает ожидание отправки (Обещание.Получить) таймаутом - по умолчанию ТаймаутМс = 10000 - и при превышении во
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Interface Definition]
       found → partial
       Текст: `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:61 → src/Экспорт/Классы/ОтелЭкспортерМетрик.os:61,67; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:87,153,288,342
       Пояснение: Верхний предел у экспортера есть (ТаймаутМс, по умолчанию 10000; при превышении - Ложь), но он действует только при положительном или неуказанном тайм
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricExporter]
       found → partial
       Текст: Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsuppo
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:179 → src/Экспорт/Классы/ОтелЭкспортерМетрик.os:179-228; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:318-323
       Пояснение: ОтелЭкспортерМетрик.ВалидироватьСовместимостьДанных сообщает (предупреждение + Ложь) о неподдерживаемом типе метрики, но проверка темпоральности нераб
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: The SDK SHOULD provide a way to allow `MetricReader` to respond to MeterProvider.ForceFlush and Mete
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:163 → src/Метрики/Классы/ОтелПровайдерМетрик.os:163-174,184-215; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:165,180
       Пояснение: Провайдер делегирует ForceFlush/Shutdown читателям, но формального интерфейса читателя нет, и ОтелПрометеусЧитательМетрик этому контракту не соответст
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Overflow attribute]
       found → partial
       Текст: The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct,
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:117 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:115-127; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:438-439
       Пояснение: В последовательном случае гарантия обеспечена: переполнение наступает только для нового набора при Аккумуляторы.Количество() >= ЛимитМощности (стр. 11
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Пояснение: Закрыть(ТаймаутМс) возвращает ОтелРезультатЗакрытия (Успех/Ошибка/Таймаут), ЗакрытьАсинхронно() - Обещание, однако результат Закрыть() каждого читател
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:184,193-209; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:138-166 → src/Метрики/Классы/ОтелПровайдерМетрик.os:184,193-207; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:138-168
       Пояснение: Закрыть(ТаймаутМс = 30000) принимает таймаут, но проверяет его только между читателями (стр. 197-201) и не передает оставшееся время читателям: не-пос
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / User Agent]
       found → partial
       Текст: OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the export
       Расположение: src/Экспорт/Классы/ОтелHttpТранспорт.os:285 → src/Экспорт/Классы/ОтелHttpТранспорт.os:285; src/Экспорт/Классы/ОтелGrpcТранспорт.os:203; src/Ядро/Модули/ОтелУтилиты.os:423-437
       Пояснение: HTTP и gRPC транспорты отправляют User-Agent «OTel-OTLP-Exporter-OneScript/<версия>» (экспортер и язык указаны), но версия берется из ОтелУтилиты.Верс
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / TextMap Propagator]
       found → partial
       Текст: In order to increase compatibility, the key-value pairs MUST only consist of US-ASCII characters tha
       Пояснение: Проверка US-ASCII по RFC 9110 реализована только в сеттере по умолчанию: ОтелСеттерТекстовойКарты.Установить (строки 33-41) пропускает запись с предуп
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / SDK-provided resource attributes]
       found → partial
       Текст: The SDK MUST provide access to a Resource with at least the attributes listed at Semantic Attributes
       Пояснение: Ресурс по умолчанию (Новый ОтелРесурс() -> ЗаполнитьАтрибутыПоУмолчанию(), ОтелРесурс.os:108-112) содержит все ключи из списка: service.name (unknown_
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Concurrency requirements]
       found → partial
       Текст: Span - all methods MUST be documented that implementations need to be safe for concurrent use by def
       Расположение: src/Трассировка/Классы/ОтелСпан.os:5-6 → src/Трассировка/Классы/ОтелСпан.os:5-6,314-509,522
       Пояснение: Doc-комментарий класса (ОтелСпан.os:5-6) заявляет, что все публичные методы Span безопасны для параллельного вызова, но реализация (API и SDK объедине
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Concurrency requirements]
       found → partial
       Текст: Event - Events are immutable and MUST be safe for concurrent use by default.
       Расположение: src/Трассировка/Классы/ОтелСобытиеСпана.os:3,89-116 → src/Трассировка/Классы/ОтелСобытиеСпана.os:3,41-43,97-101; src/Трассировка/Классы/ОтелСпан.os:350-351,615-616
       Пояснение: ОтелСобытиеСпана не имеет экспортных сеттеров (поверхностная иммутабельность, комментарий ОтелСобытиеСпана.os:3), но коллекция атрибутов не защищена: 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Concurrency requirements]
       found → partial
       Текст: Link - Links are immutable and SHOULD be safe for concurrent use by default.
       Расположение: src/Трассировка/Классы/ОтелЛинк.os:1-12,67-71 → src/Трассировка/Классы/ОтелЛинк.os:6-12,42-44,67-71; src/Трассировка/Классы/ОтелПостроительСпана.os:99; src/Трассировка/Классы/ОтелСпан.os:441-447
       Пояснение: ОтелЛинк имеет только геттеры, но атрибуты хранит по ссылке на изменяемый ОтелАтрибуты вызывающего: ОтелПостроительСпана.ДобавитьЛинк (строка 99) не к
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Concurrency requirements]
       found → partial
       Текст: Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrentl
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:517 → src/Трассировка/Классы/ОтелПровайдерТрассировки.os:93-97,128-135,147,453-458,503
       Пояснение: ForceFlush и Shutdown безопасны: Закрыть() использует CAS на АтомарноеБулево (стр. 147), СброситьБуфер() работает по снимку процессоров (стр. 128-135)
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / ForceFlush()]
       found → partial
       Текст: This is a hint to ensure that any tasks associated with `Spans` for which the `SpanProcessor` had al
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:175 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:76,193-195
       Пояснение: Спаны, находящиеся в буфере, экспортируются синхронно до возврата (СброситьБуфер → ЭкспортироватьВсеПакеты, стр. 76-77, 176-202). Но спаны, уже извлеч
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / ForceFlush()]
       found → partial
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Пояснение: СброситьБуфер возвращает ОтелРезультатЭкспорта (Успех/Ошибка/Таймаут; Успешно()/ИстекТаймаут()/Статус()); пакетный процессор сообщает об истечении соб
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:157 → src/Трассировка/Классы/ОтелПровайдерТрассировки.os:146-173
       Пояснение: Закрыть(ТаймаутМс) возвращает ОтелРезультатЗакрытия (Успешно()/ИстекТаймаут()/Описание()), ЗакрытьАсинхронно() - Обещание, но результаты, которые возв
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Shutdown()]
       found → partial
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Пояснение: Закрыть возвращает ОтелРезультатЗакрытия (Успешно()/ИстекТаймаут()/Описание()); пакетный процессор различает Таймаут (стр. 104-105) и Ошибку при исклю
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (23) - требует перепроверки:

     [Env Vars / Enum]
       partial → found
       Текст: Enum values SHOULD be interpreted in a case-insensitive manner.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:305; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:495; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:555; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:932; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:979; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1005; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1119; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:120
       Было: Большинство enum-переменных нормализуются через НРег: OTEL_TRACES_SAMPLER (стр. 305), OTEL_PROPAGATO
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Enum]
       partial → found
       Текст: For sources accepting an enum value, if the user provides a value the implementation does not recogn
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:336-342; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:501-506; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:936-940; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:984-988; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1009-1011; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1123-1126; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1326; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:127-131
       Было: Предупреждение + graceful fallback реализованы для OTEL_TRACES_SAMPLER (стр. 345-350 -> parentbased_
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Logger Creation]
       partial → found
       Текст: The input provided by the user MUST be used to create an `InstrumentationScope` instance which is st
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:72-90; src/Ядро/Классы/ОтелОбластьИнструментирования.os:61-79,164-169; src/Логирование/Классы/ОтелЛоггер.os:162-164,326-334
       Было: InstrumentationScope строится из всех входных параметров (Новый ОтелОбластьИнструментирования(ИмяБиб
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       partial → found
       Текст: Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Met
       Код: src/Метрики/Классы/ОтелМетр.os:1248,1089,1189; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:419
       Было: При конфликте единиц или вида (ЕстьНесовместимыйКонфликт) создаётся второй инструмент, он добавляетс
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ExemplarFilter]
       partial → found
       Текст: An OpenTelemetry SDK MUST support the following filters:
       Код: src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14-68
       Было: AlwaysOn (ВсегдаВключен) и AlwaysOff (ВсегдаВыключен) реализованы корректно. TraceBased (ПоТрассиров
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter]
       partial → found
       Текст: Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instr
       Код: src/Метрики/Классы/ОтелМетр.os:11-22,770-774,1016-1027; src/Метрики/Классы/ОтелПровайдерМетрик.os:89-114; src/Ядро/Классы/ОтелОбластьИнструментирования.os:61-79
       Было: Каждый ОтелМетр имеет собственные ИнструментыПоИмени и ДескрипторыИнструментов (стр. 830-831), поэто
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter Creation]
       partial → found
       Текст: The `MeterProvider` MUST implement the Get a Meter API.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:59-61,74-122; src/Метрики/Классы/ОтелПостроительМетра.os:26-64
       Было: ПолучитьМетр(ИмяБиблиотеки, ВерсияБиблиотеки, АтрибутыОбласти, АдресСхемы) (все параметры, кроме име
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter Creation]
       partial → found
       Текст: The input provided by the user MUST be used to create an `InstrumentationScope` instance which is st
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:89-91,104-111; src/Ядро/Классы/ОтелОбластьИнструментирования.os:61-79,164-169; src/Метрики/Классы/ОтелМетр.os:553-555,768
       Было: InstrumentationScope создаётся из всех входных параметров (Новый ОтелОбластьИнструментирования(ИмяБи
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter Creation]
       partial → found
       Текст: In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be ret
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:79-90,104-111; src/Ядро/Классы/ОтелОбластьИнструментирования.os:61-79; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:292
       Было: ПолучитьМетр для Неопределено или пустого имени не бросает исключение и не возвращает Неопределено: 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Overflow attribute]
       partial → found
       Текст: The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality 
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:115-128,430-436; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:363-369,438-445
       Было: Синхронные инструменты: при Аккумуляторы.Количество() >= ЛимитМощности (стр. 117) создаётся единый o
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / SimpleFixedSizeExemplarReservoir]
       partial → found
       Текст: This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the r
       Код: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:65-95
       Было: Реализован Algorithm R по числу увиденных измерений, но с ошибкой на единицу: АтомарноеЧисло.Получит
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Extract]
       partial → found
       Текст: If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST 
       Код: src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:129
       Было: ОтелW3CПропагатор.Извлечь при любой ошибке разбора traceparent (строки 103-149) возвращает входной К
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: Resource detectors SHOULD have a unique name for reference in configuration.
       Было: Условная фича Resource Detector Naming не реализована: встроенные детекторы (ОтелДетекторРесурсаХост
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: Names SHOULD be snake case and consist of lowercase alphanumeric and `_` characters, which ensures t
       Было: Условная фича Resource Detector Naming не реализована: у детекторов нет имён, поэтому требование к ф
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: Resource detector names SHOULD reflect the root namespace of attributes they populate.
       Было: Условная фича Resource Detector Naming не реализована: у детекторов нет имён, поэтому требование соо
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name whic
       Было: Условная фича Resource Detector Naming не реализована: у детекторов нет имён (в т.ч. у ОтелДетекторР
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: An SDK which identifies multiple resource detectors with the same name SHOULD report an error.
       Было: Условная фича Resource Detector Naming не реализована: нет реестра детекторов по имени, SDK не идент
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: In order to limit collisions, resource detectors SHOULD document their name in a manner which is eas
       Было: Условная фича Resource Detector Naming не реализована: у детекторов нет имён, документировать нечего
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: Populates `service.name` from the OTEL_SERVICE_NAME environment variable and SHOULD fall back to lan
       Было: Условная фича Resource Detector Naming не реализована: встроенного именованного детектора `service` 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Specifying resource information via an environment variable]
       partial → found
       Текст: In case of any error, e.g. failure during the decoding process, the entire environment variable valu
       Код: src/Ядро/Классы/ОтелРесурс.os:193
       Было: Механизм отбрасывания есть: РазобратьСтрокуАтрибутовРесурса обёрнута в Попытка/Исключение и при искл
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Specifying resource information via an environment variable]
       partial → found
       Текст: In case of any error, e.g. failure during the decoding process, the entire environment variable valu
       Код: src/Ядро/Классы/ОтелРесурс.os:190
       Было: Лог.Ошибка вызывается только в ветке Исключение (ОтелРесурс.os:182-185), которая для некорректного в
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Presumption of TraceID randomness]
       partial → found
       Текст: For all span contexts, OpenTelemetry samplers SHOULD presume that TraceIDs meet the W3C Trace Contex
       Код: src/Трассировка/Модули/ОтелСэмплер.os:370
       Было: Приоритет rv реализован: СэмплироватьПоДоле() при наличии валидного rv в ot-подключе использует его 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Tracer Creation]
       partial → found
       Текст: The input provided by the user MUST be used to create an `InstrumentationScope` instance which is st
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:81-82,92-97
       Было: InstrumentationScope строится из всех входных параметров (Новый ОтелОбластьИнструментирования(ИмяБиб
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  📋 Новые секции (36):
     + [Prometheus Compatibility] Counters (2 req)
     + [Prometheus Compatibility] Differences between Prometheus formats (4 req)
     + [Prometheus Compatibility] Dropped Types (1 req)
     + [Prometheus Compatibility] Exemplar Conversion (5 req)
     + [Prometheus Compatibility] Exemplars (4 req)
     + [Prometheus Compatibility] Exponential Histograms (15 req)
     + [Prometheus Compatibility] Gauges (7 req)
     + [Prometheus Compatibility] Histograms (7 req)
     + [Prometheus Compatibility] Histograms as Prometheus Histograms (3 req)
     + [Prometheus Compatibility] Histograms as Prometheus NHCB (12 req)
     + [Prometheus Compatibility] Info (1 req)
     + [Prometheus Compatibility] Instrumentation Scope (4 req)
     + [Prometheus Compatibility] Metric Attributes (5 req)
     + [Prometheus Compatibility] Metric Metadata (22 req)
     + [Prometheus Compatibility] Native Histograms (6 req)
     + [Prometheus Compatibility] Resource Attributes (22 req)
     + [Prometheus Compatibility] StateSet (1 req)
     + [Prometheus Compatibility] Summaries (8 req)
     + [Prometheus Compatibility] Sums (8 req)
     + [Prometheus Compatibility] Timestamps (4 req)
     + [Prometheus Compatibility] Unknown-typed (1 req)
     + [Prometheus Exporter] Client Libraries (3 req)
     + [Prometheus Exporter] Content Negotiation (3 req)
     + [Prometheus Exporter] Default Aggregation (2 req)
     + [Prometheus Exporter] Host (2 req)
     + [Prometheus Exporter] Interaction with Translation Strategy (3 req)
     + [Prometheus Exporter] Metric Conversion (1 req)
     + [Prometheus Exporter] Port (2 req)
     + [Prometheus Exporter] Pull Metric Exporter (1 req)
     + [Prometheus Exporter] Resource Attributes as Metric Labels (3 req)
     + [Prometheus Exporter] Scope Info (1 req)
     + [Prometheus Exporter] Target (1 req)
     + [Prometheus Exporter] Target Info (1 req)
     + [Prometheus Exporter] Temporality (1 req)
     + [Prometheus Exporter] Translation Strategy (2 req)
     + [Prometheus Exporter] Version and Format (3 req)

  Итого изменений: 59
    Понижений: 36, Повышений: 23, Боковых: 0
    Новых req: 0, Пропущенных req: 0
    Новых секций: 36, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
