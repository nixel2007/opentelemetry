# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             718    717    -1 ⚠️  РЕГРЕССИЯ
  partial            66     65    -1
  not_found          53     43   -10
  n_a                 3     15 +   12
  Всего             840    840 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (30) - требует перепроверки:

     [Logs Api / Enabled]
       found → partial
       Текст: When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then M
       Расположение: src/Логирование/Классы/ОтелЛоггер.os:194 → src/Логирование/Классы/ОтелЛоггер.os:49
       Пояснение: Параметр Контекст опциональный (Неопределено по умолчанию), но в методе Включен текущий контекст разрешается только в ветке TraceBased (через Трассиро
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Logger Creation]
       found → n_a
       Текст: It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` (see API).
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:56 → -
       Пояснение: OneScript не поддерживает приватные/internal конструкторы (`ПриСозданииОбъекта` всегда публичен). Идиоматическая модель создания логгеров - через Отел
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / OnEmit]
       found → partial
       Текст: This method is called synchronously on the thread that emitted the LogRecord, therefore it SHOULD NO
       Расположение: src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:25 → src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:23
       Пояснение: ПриПоявлении выполняется синхронно. ОтелКомпозитныйПроцессорЛогов.ПриПоявлении ловит исключения процессоров, но сам ОтелПростойПроцессорЛогов.ПриПоявл
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:167 → src/Логирование/Классы/ОтелПровайдерЛогирования.os:139
       Пояснение: Закрыть() - процедура без возвращаемого значения; ЗакрытьАсинхронно() возвращает Обещание, но статус успех/ошибка/таймаут на уровне провайдера не разл
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API SHOULD NOT validate the `unit`.
       Расположение: src/Метрики/Классы/ОтелМетр.os:51 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:277
       Пояснение: УстановитьЕдиницаИзмерения проверяет, что строка содержит только печатные ASCII-символы; не-ASCII значения сбрасываются в пустую строку с предупрежден
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API SHOULD NOT validate the `unit`.
       Расположение: src/Метрики/Классы/ОтелМетр.os:291 → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:142
       Пояснение: УстановитьЕдиницаИзмерения проверяет ASCII-печатность и сбрасывает не-ASCII в пустую строку с предупреждением — это валидация, противоречащая SHOULD N
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Configuration]
       found → partial
       Текст: If there is no matching view, but the `MetricReader` defines a default cardinality limit value based
       Пояснение: MetricReader.ЛимитМощности() применяется ко всем инструментам Meter единым числом; нет дифференциации лимита по типу инструмента (per-instrument-type 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ExemplarReservoir]
       found → partial
       Текст: This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associat
       Пояснение: Документирующий комментарий метода Предложить упоминает АтрибутыИзмерения и АтрибутыСерии, но не описывает явно семантику фильтрованного подмножества 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ExemplarReservoir]
       found → partial
       Текст: This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associat
       Расположение: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:42 → src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:41
       Пояснение: АтрибутыСерии передаются в каждый вызов Предложить(), а не сохраняются в резервуаре при конструировании; функционально эквивалентно, но архитектура от
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       found → partial
       Текст: The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic 
       Пояснение: Минимальная шкала захардкожена (-10), максимальная ограничена параметром НачальнаяШкала (default 20), но MaxScale как отдельный конфигурируемый параме
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Interface Definition]
       found → partial
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:68 → src/Экспорт/Классы/ОтелЭкспортерМетрик.os:66
       Пояснение: СброситьБуфер() возвращает ОтелРезультатыЭкспорта.Успех() безусловно (no-op), статус таймаута/ошибки не дифференцируется.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Interface Definition]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Пояснение: Параметр ТаймаутМс есть, но помечен UnusedParameters — таймаут не учитывается; реализация — синхронный no-op (тривиально завершается).
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter Creation]
       found → n_a
       Текст: It SHOULD only be possible to create `Meter` instances through a `MeterProvider` (see API).
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:74 → src/Метрики/Классы/ОтелМетр.os:650
       Пояснение: OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен). Документированный путь создания — через ОтелПровайдерМетрик.Пол
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MeterConfig]
       found → partial
       Текст: The value of `enabled` MUST be used to resolve whether an instrument is Enabled.
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:260 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:259
       Пояснение: Включен(Атрибуты) = МетрВключен.Получить() И Включен.Получить() реализован для синхронных инструментов; для наблюдаемых (ОтелБазовыйНаблюдаемыйИнструм
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: To construct a `MetricReader` when setting up an SDK, at least the following SHOULD be provided:
       Пояснение: Конструктор принимает Экспортер, ИнтервалЭкспортаМс, ЛимитМощности, агрегацию гистограмм. MetricFilter и MetricProducer добавляются отдельными методам
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       found → partial
       Текст: Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that 
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:244 → src/Метрики/Классы/ОтелМетр.os:565
       Пояснение: Перед вызовом мульти-callback инструменты очищаются, но изоляция per-MetricReader не строгая: если несколько reader-ов конкурентно собирают метрики, н
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → n_a
       Текст: However, if they are already implemented, they SHOULD continue to be supported as they were part of 
       Пояснение: Условное требование: применимо только если obsolete env vars (OTEL_EXPORTER_OTLP_SPAN_INSECURE, OTEL_EXPORTER_OTLP_METRIC_INSECURE) уже были реализова
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Detecting resource information from the environment]
       found → partial
       Текст: Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attrib
       Расположение: src/Ядро/Классы/ОтелРесурс.os:137 → src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:18
       Пояснение: Все встроенные детекторы (host, process, processor) безусловно устанавливают непустой Schema URL '1.29.0'. ПрименитьАтрибутыИзОкружения (env-источник)
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       partial → n_a
       Текст: Resource detectors SHOULD have a unique name for reference in configuration.
       Расположение: src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1 → -
       Пояснение: Условная фича 'Resource Detector Naming' не реализована: детекторы (ОтелДетекторРесурсаХоста/Процесса/Процессора) не имеют отдельной строки-имени для 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: Names SHOULD be snake case and consist of lowercase alphanumeric and `_` characters, which ensures t
       Пояснение: Условная фича именования детекторов не реализована — формат имён не определён.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       partial → n_a
       Текст: Resource detector names SHOULD reflect the root namespace of attributes they populate.
       Расположение: src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:22 → -
       Пояснение: Условная фича именования детекторов не реализована.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       partial → n_a
       Текст: Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name whic
       Расположение: src/Ядро/Классы/ОтелДетекторРесурсаПроцессора.os:23 → -
       Пояснение: Условная фича именования детекторов не реализована.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       not_found → n_a
       Текст: An SDK which identifies multiple resource detectors with the same name SHOULD report an error.
       Пояснение: Условная фича именования детекторов не реализована — нет ни имён, ни проверки коллизий.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Resource detector name]
       partial → n_a
       Текст: In order to limit collisions, resource detectors SHOULD document their name in a manner which is eas
       Расположение: src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:12 → -
       Пояснение: Условная фича именования детекторов не реализована — документировать нечего.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Specifying resource information via an environment variable]
       found → partial
       Текст: The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge 
       Пояснение: OTEL_RESOURCE_ATTRIBUTES читается и применяется только в составе дефолтной инициализации ресурса (ЗаполнитьАтрибутыПоУмолчанию). Если пользователь пер
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → partial
       Текст: An attempt to set value Unset SHOULD be ignored.
       Расположение: src/Трассировка/Классы/ОтелСпан.os:461 → src/Трассировка/Классы/ОтелСпан.os:450
       Пояснение: Установка Unset явно не игнорируется отдельной проверкой; работает корректно только потому, что Unset->Unset идемпотентно, а Error->Unset и Ok->Unset 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → n_a
       Текст: Analysis tools SHOULD respond to an Ok status by suppressing any errors they would otherwise generat
       Расположение: src/Трассировка/Классы/ОтелСпан.os:450 → -
       Пояснение: Требование адресовано инструментам анализа/визуализации (downstream-системы), а не SDK/API. Вне области реализации OpenTelemetry SDK для OneScript.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       partial → n_a
       Текст: There MUST NOT be any API for creating a Span other than with a Tracer.
       Расположение: src/Трассировка/Классы/ОтелСпан.os:640 → src/Трассировка/Классы/ОтелСпан.os:622
       Пояснение: OneScript не поддерживает приватные конструкторы; ПриСозданииОбъекта класса ОтелСпан всегда публичен. Ограничение задокументировано в комментарии клас
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / TraceIdRatioBased]
       found → partial
       Текст: The precision of the number SHOULD follow implementation language standards and SHOULD be high enoug
       Расположение: src/Трассировка/Модули/ОтелСэмплер.os:113 → src/Трассировка/Модули/ОтелСэмплер.os:125
       Пояснение: Precision жёстко ограничена 6 знаками после запятой (Формат с ЧДЦ=6) вместо использования стандартного для платформы представления Decimal — для очень
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Tracer Creation]
       found → n_a
       Текст: It SHOULD only be possible to create `Tracer` instances through a `TracerProvider`.
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:69 → src/Трассировка/Классы/ОтелТрассировщик.os:282
       Пояснение: OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен). Конвенциональный путь создания — через ОтелПровайдерТрассировки
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (25) - требует перепроверки:

     [Logs Sdk / Built-in processors]
       not_found → found
       Текст: Additional processors defined in this document SHOULD be provided by SDK packages.
       Было: Дополнительный процессор, описанный в спецификации (Event to span event bridge), не реализован в SDK
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Histogram operations]
       not_found → partial
       Текст: This API SHOULD be documented in a way to communicate to users that this value is expected to be non
       Код: src/Метрики/Классы/ОтелГистограмма.os:13
       Было: Документирующий комментарий перед Записать описывает параметр как 'измеренное значение', но не упоми
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Instrument unit]
       partial → found
       Текст: It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII string.
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:277
       Было: Case-sensitive обеспечен нативно (оператор = в OneScript регистрозависим), однако валидация ASCII не
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions MUST be documented as follows for the end user:
       Код: src/Метрики/Классы/ОтелМетр.os:271
       Было: Документирующие комментарии для СоздатьНаблюдаемыйСчетчик описывают часть требований к callback (пот
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Callback functions SHOULD be reentrant safe.
       Код: src/Метрики/Классы/ОтелМетр.os:276
       Было: Комментарии для СоздатьНаблюдаемыйРеверсивныйСчетчик и СоздатьНаблюдаемыйДатчик упоминают 'потокобез
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: The API SHOULD provide some way to pass `state` to the callback.
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:199
       Было: В callback передаётся только Observable Result (ОтелНаблюдениеМетрики). Отдельного механизма state н
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       not_found → partial
       Текст: `ForceFlush` MAY skip `Export(batch)` calls if the timeout is already expired, but SHOULD still call
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:106
       Было: В коде reader.СброситьБуфер нет вызова Экспортер.СброситьБуфер ни при нормальном выполнении, ни посл
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Histogram Aggregations]
       partial → found
       Текст: When the histogram contains not more than one value in either of the positive or negative ranges, th
       Код: src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:307
       Было: НачальнаяШкала = 20 (= MaxScale по умолчанию) используется при первом измерении, но нет специальной 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Instrument advisory parameters]
       partial → found
       Текст: If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed
       Код: src/Метрики/Классы/ОтелМетр.os:858
       Было: ПроверитьСовет логирует предупреждение при некорректном типе advisory-полей, но не сбрасывает невали
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Numerical limits handling]
       n_a → found
       Текст: If the SDK receives float/double values from Instruments, it MUST handle all the possible values.
       Код: src/Метрики/Классы/ОтелСчетчик.os:1
       Было: OneScript использует System.Decimal вместо IEEE 754: NaN, Infinity, отрицательный ноль невозможны на
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       partial → found
       Текст: Implementation SHOULD use the filter as early as possible to gain as much performance gain possible 
       Код: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13
       Было: Параметр ФильтрМетрик принят интерфейсом, но раннее применение фильтра — обязанность реализации; в с
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       not_found → partial
       Текст: If the batch of Metric Points includes resource information, `Produce` SHOULD require a resource as 
       Код: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13
       Было: Метод Произвести не принимает параметр Resource; ресурс не передаётся продюсеру.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       not_found → partial
       Текст: `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13
       Было: Произвести возвращает только Массив данных, без статуса успех/ошибка/таймаут; в СобратьДанныеПродюсе
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       not_found → found
       Текст: If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include
       Код: src/Метрики/Классы/ОтелДанныеМетрики.os:1
       Было: Интерфейс продюсера не определяет/не возвращает InstrumentationScope, идентифицирующий MetricProduce
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       partial → found
       Текст: For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp,
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:174
       Было: Для синхронных инструментов ВремяСтарта корректно сбрасывается на ТекущееВремя при delta-сборе. Для 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       partial → found
       Текст: This implies that all data points with delta temporality aggregation for an instrument MUST share th
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:356
       Было: Синхронные инструменты используют общий ВремяСтарта для всех точек. Асинхронные в ПреобразоватьЗапис
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       partial → found
       Текст: Cumulative timeseries MUST use a consistent start timestamp for all collection intervals.
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:170
       Было: Синхронные сохраняют ВремяСтарта при кумулятивной временности. Асинхронные при каждом callback занов
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       partial → found
       Текст: The option SHOULD accept any form allowed by the underlying gRPC client implementation.
       Код: src/Экспорт/Классы/ОтелGrpcТранспорт.os:48
       Было: РазобратьСхемуURL принимает только http/https/без схемы; иные формы (DNS-имена, unix:, dns:) отклоня
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Specify Protocol]
       partial → found
       Текст: SDKs SHOULD support both grpc and http/protobuf transports and MUST support at least one of them.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:632
       Было: Конфигурация принимает значения 'grpc' и 'http/protobuf', однако HTTP-транспорт всегда отправляет JS
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Global Propagators]
       partial → found
       Текст: If pre-configured, Propagators SHOULD default to a composite Propagator containing the W3C Trace Con
       Код: src/Ядро/Модули/ОтелГлобальный.os:132
       Было: Дефолт ОтелГлобальный.ПолучитьПропагаторы() возвращает ОтелНоопПропагатор, а не композит W3C TraceCo
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / TextMap Propagator]
       partial → found
       Текст: In order to increase compatibility, the key-value pairs MUST only consist of US-ASCII characters tha
       Код: src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:32
       Было: Сеттер просто записывает ключ/значение в Соответствие через Носитель.Вставить без явной валидации US
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / W3C Trace Context Requirements]
       partial → found
       Текст: A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP heade
       Код: src/Пропагация/Классы/ОтелW3CПропагатор.os:88
       Было: traceparent парсится и валидируется (длина, версия 'ff', all-zeros), но комментарий в коде явно указ
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Context Interaction]
       partial → found
       Текст: The functionality listed above is necessary because API users SHOULD NOT have access to the Context 
       Код: src/Ядро/Модули/ОтелКонтекст.os:141
       Было: Функции Extract/Combine (СпанИзКонтекста, КонтекстСоСпаном) предоставлены, и пользователи могут не р
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / AlwaysRecord]
       not_found → found
       Текст: Based on the decision from the wrapped root sampler, `AlwaysRecord` MUST behave as follows: ...
       Код: src/Трассировка/Модули/ОтелСэмплер.os:284
       Было: Sampler-декоратор AlwaysRecord, который переводит DROP-решение обёрнутого сэмплера в RECORD_ONLY, в 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / OnEnding]
       partial → found
       Текст: The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking `
       Код: src/Трассировка/Классы/ОтелСпан.os:484
       Было: Метод Завершить() выполняется синхронно, и флаг Завершен защищает от повторного входа, но нет явной 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (17) - агент нашёл дополнительные:

     [Env Vars] SHOULD found: "logging": Standard Output. It is a deprecated value left for backwards compatib
     [Env Vars] SHOULD found: "logging": Standard Output. It is a deprecated value left for backwards compatib
     [Env Vars] SHOULD found: "logging": Standard Output. It is a deprecated value left for backwards compatib
     [Logs Api] MUST found: The API MUST accept the following parameters:
     [Metrics Api] SHOULD found: The API SHOULD treat it as an opaque string.
     [Metrics Sdk] MUST found: This extension MUST be configurable on a metric View, although individual reserv
     [Metrics Sdk] SHOULD found: The "offer" method SHOULD accept measurements, including: * The `value` of the m
     [Metrics Sdk] SHOULD partial: SDKs SHOULD return some failure for these calls, if possible.
     [Metrics Sdk] SHOULD partial: For asynchronous instrument, the start timestamp SHOULD be: - The creation time 
     [Trace Api] SHOULD found: its `name` property SHOULD be set to an empty string.
     [Trace Api] SHOULD found: and a message reporting that the specified value is invalid SHOULD be logged.
     [Trace Api] MUST found: The API MUST allow retrieving the `TraceId` and `SpanId` in the following forms:
     [Trace Api] MUST NOT n_a: However, alternative implementations MUST NOT allow callers to create `Span`s di
     [Trace Api] MUST found: The API MUST accept the following parameters:
     [Trace Sdk] MUST not_found: The calling CompositeSampler SHOULD update the threshold of the outgoing TraceSt
     [Trace Sdk] SHOULD partial: After the call to `Shutdown`, subsequent attempts to get a `Tracer` are not allo
     [Trace Sdk] SHOULD found: After the call to `Shutdown`, subsequent calls to `OnStart`, `OnEnd`, or `ForceF

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (17) - были раньше, теперь нет:

     [Env Vars] SHOULD found: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD found: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD found: It SHOULD NOT be supported by new implementations.
     [Logs Api] MUST found: The API MUST accept the following parameters: Timestamp (optional), Observed Tim
     [Metrics Api] SHOULD found: The `unit` is an optional string provided by the author of the Instrument. The A
     [Metrics Sdk] MUST found: This extension MUST be configurable on a metric View,
     [Metrics Sdk] SHOULD found: The "offer" method SHOULD accept measurements, including:
     [Metrics Sdk] SHOULD partial: After the call to `Shutdown`, subsequent invocations to `Collect` are not allowe
     [Metrics Sdk] SHOULD not_found: For asynchronous instrument, the start timestamp SHOULD be:
     [Trace Api] SHOULD found: In case an invalid name (null or empty string) is specified, a working Tracer im
     [Trace Api] SHOULD found: In case an invalid name (null or empty string) is specified, a working Tracer im
     [Trace Api] MUST found: The API MUST allow retrieving the TraceId and SpanId in the following forms: Hex
     [Trace Api] MUST NOT partial: Vendors may implement the Span interface to effect vendor-specific logic. Howeve
     [Trace Api] MUST found: The API MUST accept the following parameters: span name, parent Context (or root
     [Trace Sdk] MUST NOT not_found: The calling CompositeSampler SHOULD update the threshold of the outgoing TraceSt
     [Trace Sdk] SHOULD partial: SDKs SHOULD return a valid no-op Tracer for these calls, if possible.
     [Trace Sdk] SHOULD partial: SDKs SHOULD ignore these calls gracefully, if possible.

  Итого изменений: 89
    Понижений: 30, Повышений: 25, Боковых: 0
    Новых req: 17, Пропущенных req: 17
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
