# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             829    837 +    8 ✅
  partial             4      4     0
  not_found           0      0     0
  n_a                76     68    -8
  Всего             909    909 +    0

  🟢 ПОВЫШЕНИЕ СТАТУСА (8) - требует перепроверки:

     [Propagators / B3 Extract]
       n_a → found
       Текст: When extracting B3, propagators: * MUST attempt to extract B3 encoded using single and multi-header 
       Код: opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:65
       Было: B3 пропагатор распространяется отдельным пакетом opentelemetry-propagator-b3 (намеренно, по спеке) и
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Extract]
       n_a → found
       Текст: MUST preserve a debug trace flag, if received, and propagate it with subsequent requests.
       Код: opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:137
       Было: B3 пропагатор отсутствует в репозитории (отдельный пакет opentelemetry-propagator-b3); поведение B3 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Extract]
       n_a → found
       Текст: Additionally, an OpenTelemetry implementation MUST set the sampled trace flag when the debug flag is
       Код: opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:137
       Было: B3 пропагатор отсутствует в репозитории (отдельный пакет opentelemetry-propagator-b3); поведение B3 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Extract]
       n_a → found
       Текст: MUST NOT reuse `X-B3-SpanId` as the ID for the server-side span.
       Код: opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:201
       Было: B3 пропагатор отсутствует в репозитории (отдельный пакет opentelemetry-propagator-b3); поведение B3 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Inject]
       n_a → found
       Текст: When injecting B3, propagators: * MUST default to injecting B3 using the single-header format
       Код: opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:259
       Было: B3 пропагатор отсутствует в репозитории (отдельный пакет opentelemetry-propagator-b3); SDK лишь созд
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Inject]
       n_a → found
       Текст: MUST provide configuration to change the default injection format to B3 multi-header
       Код: opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:259
       Было: B3 пропагатор отсутствует в репозитории (отдельный пакет opentelemetry-propagator-b3); SDK передаёт 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Inject]
       n_a → found
       Текст: MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support reusing the same ID for bot
       Код: opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:113
       Было: B3 пропагатор отсутствует в репозитории (отдельный пакет opentelemetry-propagator-b3); поведение B3 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Fields]
       n_a → found
       Текст: Fields MUST return the header names that correspond to the configured format, i.e., the headers used
       Код: opentelemetry-propagator-b3/src/Классы/ОтелB3Пропагатор.os:86
       Было: B3 пропагатор отсутствует в репозитории (grep B3 в src/Пропагация пуст); поставляется отдельным паке
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  Итого изменений: 8
    Понижений: 0, Повышений: 8, Боковых: 0
    Новых req: 0, Пропущенных req: 0
    Новых секций: 0, Исчезнувших секций: 0

======================================================================
```
