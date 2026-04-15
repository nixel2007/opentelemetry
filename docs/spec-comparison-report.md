# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             675    669    -6 ⚠️  РЕГРЕССИЯ
  partial            71     80 +    9
  not_found          61     73 +   12 ⚠️  РЕГРЕССИЯ
  n_a                17      2   -15
  Всего             824    824 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (16) - требует перепроверки:

     [Metrics Sdk / Periodic exporting MetricReader]
       found → partial
       Текст: The reader MUST synchronize calls to `MetricExporter`'s `Export` to make sure that they are not invo
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:199 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:166
       Пояснение: Периодический экспорт выполняется последовательно в фоновом задании, но вызов СброситьБуфер() из основного потока может привести к конкурентному вызов
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggreg
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:85 → src/Метрики/Классы/ОтелМетр.os:48
       Пояснение: Default aggregation per instrument type exists (Counter→Sum, Histogram→ExplicitBucketHistogram, Gauge→LastValue), but it is hardcoded in ОтелМетр, not
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Fields]
       found → partial
       Текст: Fields MUST return the header names that correspond to the configured format, i.e., the headers used
       Расположение: src/Пропагация/Классы/ОтелW3CПропагатор.os:137 → src/Пропагация/Классы/ОтелB3Пропагатор.os:83
       Пояснение: Метод Поля() возвращает 5 заголовков (X-B3-TraceId, X-B3-SpanId, X-B3-Sampled, X-B3-ParentSpanId, X-B3-Flags), но inject использует только 3 (X-B3-Tra
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Global Propagators]
       found → not_found
       Текст: If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:443 → -
       Пояснение: SDK не предоставляет предварительно сконфигурированных пропагаторов. ОтелГлобальный.ПолучитьПропагаторы() возвращает ОтелНоопПропагатор по умолчанию, 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Propagators Distribution]
       found → partial
       Текст: The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST 
       Расположение: src/Пропагация/Классы/ОтелB3Пропагатор.os:1 → lib.config:115
       Пояснение: W3C TraceContext, W3C Baggage и B3 все находятся в основном пакете, а не в отдельных extension-пакетах. W3C MAY быть частью API, но B3 по спеке должен
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Detecting resource information from the environment]
       found → partial
       Текст: Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific 
       Пояснение: Detectors (host, process, processor) are implemented as separate classes but are bundled within the SDK package (src/Ядро/Классы/), not as separate pa
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Enabled]
       partial → not_found
       Текст: The API SHOULD be documented that instrumentation authors needs to call this API each time they crea
       Расположение: src/Трассировка/Классы/ОтелТрассировщик.os:31 → -
       Пояснение: Документация метода Включен() не содержит указания о том, что авторы инструментирования должны вызывать этот API каждый раз при создании нового спана 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Get a Tracer]
       found → partial
       Текст: In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be
       Пояснение: ПолучитьТрассировщик принимает ИмяБиблиотеки и вернёт рабочий трассировщик даже с пустым именем (не бросает исключение), но нет явной проверки на нева
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span]
       found → partial
       Текст: However, alternative implementations MUST NOT allow callers to create `Span`s directly.
       Расположение: src/Трассировка/Классы/ОтелТрассировщик.os:56 → src/Трассировка/Классы/ОтелСпан.os:599
       Пояснение: OneScript does not support private constructors or access modifiers. ОтелСпан constructor is technically accessible via Новый ОтелСпан(...), though th
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       found → partial
       Текст: There MUST NOT be any API for creating a `Span` other than with a `Tracer`.
       Расположение: src/Трассировка/Классы/ОтелТрассировщик.os:56 → src/Трассировка/Классы/ОтелСпан.os:599
       Пояснение: OneScript does not support private constructors or access modifiers. ОтелСпан constructor is technically accessible via Новый ОтелСпан(...), though th
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       found → partial
       Текст: This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`.
       Пояснение: ОтелПостроительСпана.УстановитьРодителя() correctly accepts only Context (Соответствие) and rejects Span/SpanContext. However, ОтелТрассировщик.Начать
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Additional Span Interfaces]
       found → partial
       Текст: For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated 
       Расположение: src/Ядро/Классы/ОтелОбластьИнструментирования.os:57 → src/Трассировка/Классы/ОтелСпан.os:182
       Пояснение: There is no separate InstrumentationLibrary class or accessor. Only InstrumentationScope (ОтелОбластьИнструментирования) is available, which contains 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / ForceFlush()]
       found → partial
       Текст: If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over f
       Пояснение: ОтелПакетныйПроцессорСпанов проверяет таймаут в цикле экспорта (ЭкспортироватьВсеПакеты), но ОтелПростойПроцессорСпанов полностью игнорирует параметр 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / ForceFlush()]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:129
       Пояснение: ОтелПакетныйПроцессорСпанов проверяет таймаут в цикле, но ОтелПростойПроцессорСпанов игнорирует параметр ТаймаутМс в СброситьБуфер
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Shutdown()]
       found → partial
       Текст: `Shutdown` MUST include the effects of `ForceFlush`.
       Пояснение: ОтелПакетныйПроцессорСпанов включает эффект ForceFlush (вызывает ЭкспортироватьВсеПакеты в Закрыть), но ОтелПростойПроцессорСпанов не вызывает Экспорт
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Shutdown()]
       found → partial
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:83
       Пояснение: ОтелПакетныйПроцессорСпанов учитывает таймаут через ЭкспортироватьВсеПакеты, но ОтелПростойПроцессорСпанов игнорирует параметр ТаймаутМс (помечен BSLL
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (19) - требует перепроверки:

     [Metrics Sdk / Numerical limits handling]
       n_a → not_found
       Текст: The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry.
       Было: OneScript использует System.Decimal (не IEEE 754) - NaN, Infinity, отрицательный ноль невозможны. Пе
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Numerical limits handling]
       n_a → not_found
       Текст: If the SDK receives float/double values from Instruments, it MUST handle all the possible values.
       Было: OneScript использует System.Decimal (не IEEE 754) - NaN, Infinity и другие специальные значения IEEE
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Extract]
       n_a → found
       Текст: MUST attempt to extract B3 encoded using single and multi-header formats.
       Код: src/Пропагация/Классы/ОтелB3Пропагатор.os:63
       Было: B3 Propagator is not implemented in this codebase; scope is conditional
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Extract]
       n_a → partial
       Текст: MUST preserve a debug trace flag, if received, and propagate it with subsequent requests.
       Код: src/Пропагация/Классы/ОтелB3Пропагатор.os:139
       Было: B3 Propagator is not implemented in this codebase; scope is conditional
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Extract]
       n_a → found
       Текст: Additionally, an OpenTelemetry implementation MUST set the sampled trace flag when the debug flag is
       Код: src/Пропагация/Классы/ОтелB3Пропагатор.os:140
       Было: B3 Propagator is not implemented in this codebase; scope is conditional
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Extract]
       n_a → found
       Текст: MUST NOT reuse `X-B3-SpanId` as the id for the server-side span.
       Код: src/Пропагация/Классы/ОтелB3Пропагатор.os:167
       Было: B3 Propagator is not implemented in this codebase; scope is conditional
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Inject]
       n_a → partial
       Текст: MUST default to injecting B3 using the single-header format
       Код: src/Пропагация/Классы/ОтелB3Пропагатор.os:27
       Было: B3 Propagator is not implemented in this codebase; scope is conditional
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Inject]
       n_a → not_found
       Текст: MUST provide configuration to change the default injection format to B3 multi-header
       Было: B3 Propagator is not implemented in this codebase; scope is conditional
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Inject]
       n_a → found
       Текст: MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support reusing the same id for bot
       Код: src/Пропагация/Классы/ОтелB3Пропагатор.os:27
       Было: B3 Propagator is not implemented in this codebase; scope is conditional
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: Resource detectors SHOULD have a unique name for reference in configuration.
       Было: Resource Detector Naming is a conditional feature that is not implemented. Detectors have no name pr
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: Names SHOULD be snake case and consist of lowercase alphanumeric and `_` characters, which ensures t
       Было: Resource Detector Naming is a conditional feature that is not implemented.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: Resource detector names SHOULD reflect the root namespace of attributes they populate.
       Было: Resource Detector Naming is a conditional feature that is not implemented.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: Resource detectors which populate attributes from multiple root namespaces SHOULD choose a name whic
       Было: Resource Detector Naming is a conditional feature that is not implemented.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: An SDK which identifies multiple resource detectors with the same name SHOULD report an error.
       Было: Resource Detector Naming is a conditional feature that is not implemented.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Resource detector name]
       n_a → not_found
       Текст: In order to limit collisions, resource detectors SHOULD document their name in a manner which is eas
       Было: Resource Detector Naming is a conditional feature that is not implemented.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Context Interaction]
       partial → found
       Текст: The functionality listed above is necessary because API users SHOULD NOT have access to the Context 
       Код: src/Ядро/Модули/ОтелКонтекст.os:44
       Было: Ключ контекста спана (КлючСпана) доступен через экспортную функцию ОтелКонтекст.КлючСпана(). Хотя по
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Span Limits]
       partial → found
       Текст: The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`.
       Код: src/Трассировка/Классы/ОтелЛимитыСпана.os:34
       Было: The limits exist as МаксСобытий/МаксЛинков (УстановитьМаксСобытий/УстановитьМаксЛинков) rather than 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / TraceID randomness]
       partial → found
       Текст: For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trac
       Код: src/Ядро/Модули/ОтелУтилиты.os:78
       Было: TraceIDs are generated using УникальныйИдентификатор (UUID v4), which provides pseudo-random values 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / `ForceFlush()`]
       partial → found
       Текст: `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using som
       Код: src/Экспорт/Классы/ОтелЭкспортерСпанов.os:44
       Было: Метод СброситьБуфер() существует, но в SDK отсутствует документация, рекомендующая вызывать ForceFlu
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (4) - агент нашёл дополнительные:

     [Trace Api] SHOULD not_found: In case an invalid name (null or empty string) is specified, a working Tracer im
     [Trace Api] SHOULD not_found: In case an invalid name (null or empty string) is specified, a working Tracer im
     [Trace Api] SHOULD NOT found: This functionality MUST be fully implemented in the API, and SHOULD NOT be overr
     [Trace Sdk] SHOULD found: `ForceFlush` SHOULD complete or abort within some timeout.

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (4) - были раньше, теперь нет:

     [Trace Api] SHOULD partial: its `name` property SHOULD be set to an empty string,
     [Trace Api] SHOULD not_found: and a message reporting that the specified value is invalid SHOULD be logged.
     [Trace Api] SHOULD NOT found: and SHOULD NOT be overridable.
     [Trace Sdk] SHOULD partial: `ForceFlush` SHOULD complete or abort within some timeout. `ForceFlush` can be i

  Итого изменений: 43
    Понижений: 16, Повышений: 19, Боковых: 0
    Новых req: 4, Пропущенных req: 4
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
