# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             762    762     0
  partial            22     22     0
  not_found           1      1     0
  n_a                83     83     0
  Всего             868    868 +    0

  ➕ НОВЫЕ ТРЕБОВАНИЯ (2) - агент нашёл дополнительные:

     [Metrics Sdk] SHOULD found: The “offer” method SHOULD accept measurements, including:
     [Trace Api] MUST found: The `Tracer` MUST provide functions to:

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (2) - были раньше, теперь нет:

     [Metrics Sdk] SHOULD found: The “offer” method SHOULD accept measurements, including: * The `value` of the m
     [Trace Api] MUST found: The `Tracer` MUST provide functions to: * Create a new `Span` (see the section o

  Итого изменений: 4
    Понижений: 0, Повышений: 0, Боковых: 0
    Новых req: 2, Пропущенных req: 2
    Новых секций: 0, Исчезнувших секций: 0

======================================================================
```
