# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             762    829 +   67 ✅
  partial            22      4   -18
  not_found           1      0    -1
  n_a                83     76    -7
  Всего             868    909 +   41

  🔴 ПОНИЖЕНИЕ СТАТУСА (2) - требует перепроверки:

     [Logs Sdk / Built-in processors]
       found → n_a
       Текст: Other common processing scenarios SHOULD be first considered for implementation out-of-process in Op
       Расположение: lib.config:58-61 (в SDK только встроенные Simple/Batch процессоры, внутренний композитный процессор для цепочки и интерфейс; прочие сценарии обработки - фильтрация, обогащение, маршрутизация - в SDK in-process не реализуются); src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:1-76 (пользовательские процессоры подключаются через интерфейс) → -
       Пояснение: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / B3 Inject]
       found → n_a
       Текст: MUST provide configuration to change the default injection format to B3 multi-header
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:458-498,1437-1442; src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:781-827 (otel.propagators / OTEL_PROPAGATORS и propagator в файле конфигурации: значение b3 задаёт формат single, значение b3multi - формат multi; формат передаётся конструктору ОтелB3Пропагатор из пакета opentelemetry-propagator-b3); подтверждено tests/unit/Конфигурация/ТестКонфигурационнаяФабрика.os:1292-1314 → src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:1608
       Пояснение: B3 пропагатор отсутствует в репозитории (отдельный пакет opentelemetry-propagator-b3); SDK передаёт режим multi через имя b3multi. Реализация конфигур
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (29) - требует перепроверки:

     [Logs Sdk / Export]
       partial → found
       Текст: `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Код: src/Экспорт/Классы/ОтелЭкспортерЛогов.os:37
       Было: Для OTLP/HTTP (протокол по умолчанию http/protobuf) выполняется полностью: срок экспорта - меньший и
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Export]
       partial → found
       Текст: `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Код: src/Экспорт/Классы/ОтелЭкспортерЛогов.os:47
       Было: Предел существует: срок экспорта - меньший из таймаута вызова и таймаута экспортера (по умолчанию 10
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:124
       Было: Таймаут поддержан: СброситьБуфер(ТаймаутМс = 0) и ПринудительноВыгрузитьСРезультатом(ТаймаутМс = 300
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79
       Было: Срок соблюдается на уровне процессоров: СброситьБуфер(ТаймаутМс) принимает таймаут, срок проверяется
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ShutDown]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95
       Было: Срок соблюдается на уровне процессоров: Закрыть(ТаймаутМс = 30000) принимает таймаут, ожидание блоки
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Логирование/Классы/ОтелПровайдерЛогирования.os:138
       Было: Таймаут поддержан: Закрыть(ТаймаутМс = 30000) передает каждому процессору оставшееся время, вызывает
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Asynchronous UpDownCounter creation]
       n_a → found
       Текст: There MUST NOT be any API for creating an Asynchronous UpDownCounter other than with a `Meter`.
       Код: src/Метрики/Классы/ОтелМетр.os:199
       Было: OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Instrument]
       n_a → found
       Текст: Language-level features such as the distinction between integer and floating point numbers SHOULD be
       Код: src/Метрики/Классы/ОтелМетр.os:1243
       Было: Ограничение платформы OneScript (Число = System.Decimal, не IEEE 754): в языке один числовой тип Чис
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / UpDownCounter creation]
       n_a → found
       Текст: There MUST NOT be any API for creating an `UpDownCounter` other than with a `Meter`.
       Код: src/Метрики/Классы/ОтелМетр.os:114
       Было: OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Export(batch)]
       partial → found
       Текст: `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47
       Было: Для OTLP/HTTP выполняется полностью: срок экспорта - меньший из таймаута вызова и таймаута экспортер
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Export(batch)]
       partial → found
       Текст: `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47
       Было: Верхний предел есть: меньший из таймаута вызова и таймаута экспортера (по умолчанию 10000 мс), у чит
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:182
       Было: Срок соблюдается в штатных случаях (СброситьБуфер и ПринудительноВыгрузитьСРезультатом принимают Тай
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:187
       Было: Срок поддержан: ПринудительноВыгрузитьСРезультатом(ТаймаутМс = 30000) и СброситьБуфер(ТаймаутМс = 0)
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Numerical limits handling]
       n_a → found
       Текст: If the SDK receives float/double values from Instruments, it MUST handle all the possible values.
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:81
       Было: Ограничение платформы OneScript: Число = System.Decimal (не IEEE 754), значений NaN, Infinity и отри
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:194
       Было: Срок соблюдается в штатных случаях (Закрыть принимает ТаймаутМс, передает читателям оставшееся время
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:149
       Было: Срок поддержан и передается по шагам: Закрыть(ТаймаутМс = 30000) ждет фоновое задание периодического
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / User Agent]
       partial → found
       Текст: The resulting User-Agent SHOULD include the exporter’s default User-Agent string.
       Код: src/Ядро/Модули/ОтелУтилиты.os:485
       Было: HTTP: идентификатор продукта из заголовка user-agent (в любом регистре) ставится перед стандартной с
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Prometheus Exporter / Client Libraries]
       not_found → partial
       Текст: A Prometheus Exporter SHOULD use an official Prometheus client library when one exists for the imple
       Код: src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:4
       Было: Экспортер использует неофициальную клиентскую библиотеку Prometheus: пакет prometheus 1.0.6 (yellow-
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Propagators Distribution]
       n_a → found
       Текст: It MUST NOT use `OpenTracing` in the resulting propagator name as it is not widely adopted format in
       Код: src/Пропагация/Классы/
       Было: Требование адресовано OpenTelemetry Organization (официальный реестр пропагаторов); данный пакет явл
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Span Creation]
       n_a → found
       Текст: This argument SHOULD only be set when span creation time has already passed.
       Код: src/Трассировка/Классы/ОтелПостроительСпана.os:110
       Было: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не мож
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Span Creation]
       n_a → found
       Текст: If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument
       Код: src/Трассировка/Классы/ОтелПостроительСпана.os:110
       Было: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не мож
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Span Creation]
       n_a → found
       Текст: Any span that is created MUST also be ended.
       Код: src/Трассировка/Классы/ОтелСпан.os:529
       Было: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не мож
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:130
       Было: СброситьБуфер принимает таймаут, передает каждому процессору оставшееся время и сообщает истечение с
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / ForceFlush()]
       partial → found
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79
       Было: СброситьБуфер(ТаймаутМс) принимает срок и возвращает Таймаут по его истечении: ожидание блокировки э
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / GetDescription]
       n_a → found
       Текст: Callers SHOULD NOT cache the returned value.
       Код: src/Трассировка/Классы/ИнтерфейсСэмплер.os:36
       Было: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не мож
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:143
       Было: Закрыть принимает таймаут (по умолчанию 30000 мс), передает каждому процессору оставшееся время и со
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown()]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95
       Было: Закрыть(ТаймаутМс) принимает срок и возвращает Таймаут по его истечении: ожидание фонового экспорта 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / `Export(batch)`]
       partial → found
       Текст: Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Код: src/Экспорт/Классы/ОтелЭкспортерСпанов.os:36-54 (таймаут по умолчанию 10000 мс, оставшееся время передается транспорту; Ложь при сбое)
       Было: Для HTTP срок соблюдается полностью (таймаут запроса не больше времени до срока, повторы и паузы в п
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / `Export(batch)`]
       partial → found
       Текст: Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Код: src/Экспорт/Классы/ОтелЭкспортерСпанов.os:36-54,112
       Было: Верхний предел есть (по умолчанию 10000 мс, меньший из таймаута вызова и таймаута экспортера), по ис
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  📋 Новые секции (12):
     + [Configuration Api] ConfigProperties (5 req)
     + [Configuration Data Model] Environment variable substitution (8 req)
     + [Configuration Data Model] File-based configuration model (1 req)
     + [Configuration Data Model] YAML file format (3 req)
     + [Configuration Sdk] Create (7 req)
     + [Configuration Sdk] Create Component (2 req)
     + [Configuration Sdk] In-Memory configuration model (2 req)
     + [Configuration Sdk] Parse (6 req)
     + [Configuration Sdk] PluginComponentProvider operations (1 req)
     + [Configuration Sdk] Register PluginComponentProvider (3 req)
     + [Configuration Sdk] SDK extension components (2 req)
     + [Configuration Sdk] SDK operations (1 req)

  ➕ НОВЫЕ ТРЕБОВАНИЯ (14) - агент нашёл дополнительные:

     [Context] MUST found: The API MUST accept the following parameters:
     [Env Vars] SHOULD NOT found: It is a deprecated value left for backwards compatibility. It SHOULD NOT be supp
     [Env Vars] SHOULD NOT found: It is a deprecated value left for backwards compatibility. It SHOULD NOT be supp
     [Env Vars] SHOULD NOT found: It is a deprecated value left for backwards compatibility. It SHOULD NOT be supp
     [Logs Sdk] SHOULD found: Additional processors defined in this document SHOULD be provided by SDK package
     [Metrics Sdk] SHOULD found: The “offer” method SHOULD accept measurements, including: * The `value` of the m
     [Trace Api] MUST found: The Span interface MUST provide:
     [Trace Api] MUST found: The Span interface MUST provide:
     [Trace Api] SHOULD found: its `name` property SHOULD be set to an empty string, and a message reporting th
     [Trace Api] SHOULD found: its `name` property SHOULD be set to an empty string, and a message reporting th
     [Trace Api] MUST found: The API MUST provide:
     [Trace Api] MUST found: The Span interface MUST provide:
     [Trace Api] MUST found: The Span interface MUST provide:
     [Trace Sdk] MUST found: `Enabled` MUST return `false` when either: * there are no registered `SpanProces

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (14) - были раньше, теперь нет:

     [Context] MUST found: The API MUST accept the following parameters: * A `Token` that was returned by a
     [Env Vars] SHOULD NOT found: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD NOT found: It SHOULD NOT be supported by new implementations.
     [Env Vars] SHOULD NOT found: It SHOULD NOT be supported by new implementations.
     [Metrics Sdk] SHOULD found: The “offer” method SHOULD accept measurements, including:
     [Metrics Sdk] MUST found: `Produce` MUST return a batch of Metric Points, filtered by the optional `metric
     [Trace Api] MUST found: The Span interface MUST provide: An API to record a single `Event` where the `Ev
     [Trace Api] MUST found: The Span interface MUST provide: An API that returns the `SpanContext` for the g
     [Trace Api] SHOULD found: In case an invalid name (null or empty string) is specified, a working Tracer im
     [Trace Api] SHOULD found: In case an invalid name (null or empty string) is specified, a working Tracer im
     [Trace Api] MUST found: The API MUST provide: An API to record a single `Link` where the `Link` properti
     [Trace Api] MUST found: The Span interface MUST provide: An API to set a single `Attribute` where the at
     [Trace Api] MUST found: The Span interface MUST provide: An API to set the `Status`.
     [Trace Sdk] MUST found: `Enabled` MUST return `false` when either:

  Итого изменений: 59
    Понижений: 2, Повышений: 29, Боковых: 0
    Новых req: 14, Пропущенных req: 14
    Новых секций: 12, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
