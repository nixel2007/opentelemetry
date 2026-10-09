# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             837    834    -3 ⚠️  РЕГРЕССИЯ
  partial             4      5 +    1
  not_found           0      0     0
  n_a                68     71 +    3
  Всего             909    910 +    1

  🔴 ПОНИЖЕНИЕ СТАТУСА (5) - требует перепроверки:

     [Configuration Data Model / YAML file format]
       found → partial
       Текст: YAML configuration files SHOULD be parsed using v1.2 YAML core schema.
       Расположение: src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:502 → src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:39
       Пояснение: Разбор выполняет библиотека oscript-yaml (YAML 1.2), но в версии 0.3.0 скаляр в кавычках ("true", "123") разрешается не в строку, как требует core sch
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span]
       found → n_a
       Текст: All `Span`s MUST be created via a `Tracer`.
       Расположение: src/Трассировка/Классы/ОтелТрассировщик.os:226 → /home/user/opentelemetry/src/Трассировка/Классы/ОтелСпан.os:811
       Пояснение: OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен); ограничение документировано в коде (ОтелСпан.os) и docs/spec-co
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       found → n_a
       Текст: This argument SHOULD only be set when span creation time has already passed.
       Расположение: src/Трассировка/Классы/ОтелПостроительСпана.os:110 → /home/user/opentelemetry/src/Трассировка/Классы/ОтелПостроительСпана.os:115
       Пояснение: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Рекоменд
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       found → n_a
       Текст: If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument
       Расположение: src/Трассировка/Классы/ОтелПостроительСпана.os:110 → /home/user/opentelemetry/src/Трассировка/Классы/ОтелПостроительСпана.os:115
       Пояснение: Требование адресовано пользователю API (caller guidance); SDK не может программно определить момент логического старта операции.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       found → n_a
       Текст: Any span that is created MUST also be ended.
       Расположение: src/Трассировка/Классы/ОтелСпан.os:529 → -
       Пояснение: Требование является рекомендацией по использованию для вызывающих кода (caller guidance): спецификация прямо указывает «This is the responsibility of 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (1) - требует перепроверки:

     [Logs Sdk / Built-in processors]
       n_a → found
       Текст: Other common processing scenarios SHOULD be first considered for implementation out-of-process in Op
       Код: /home/user/opentelemetry/src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:173
       Было: Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не мож
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (5) - агент нашёл дополнительные:

     [Logs Sdk] SHOULD found: After the call to `Shutdown`, subsequent calls to `OnEmit` are not allowed. SDKs
     [Metrics Api] MUST found: observations from a single callback MUST be reported with identical timestamps.
     [Metrics Sdk] SHOULD found: The “offer” method SHOULD accept measurements, including:
     [Trace Api] SHOULD found: An API to set the `Status`. This SHOULD be called `SetStatus`.
     [Trace Sdk] SHOULD found: The `SpanProcessor` interface SHOULD declare the following methods:

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (4) - были раньше, теперь нет:

     [Logs Sdk] SHOULD found: SDKs SHOULD ignore these calls gracefully, if possible.
     [Metrics Api] MUST found: The API MUST treat observations from a single callback as logically taking place
     [Metrics Sdk] SHOULD found: The “offer” method SHOULD accept measurements, including: * The `value` of the m
     [Trace Api] SHOULD found: This SHOULD be called `SetStatus`.

  Итого изменений: 15
    Понижений: 5, Повышений: 1, Боковых: 0
    Новых req: 5, Пропущенных req: 4
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
