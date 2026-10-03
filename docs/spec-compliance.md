# Анализ соответствия спецификации OpenTelemetry v1.61.0

> **Версия спецификации**: [v1.61.0](https://opentelemetry.io/docs/specs/otel/)
> **Дата анализа**: 2026-10-03
> **Методология**: spec-first - извлечены все MUST/SHOULD требования стабильных разделов спецификации, затем каждое прослежено до кода

## Сводка (Stable)

Учитываются только требования из стабильных разделов спецификации с универсальной областью применения.

| Показатель | Значение |
|---|---|
| Всего Stable-требований | 868 |
| Stable + universal | 828 |
| Stable + conditional | 40 |
| Найдено требований (Stable universal) | 781 |
| ✅ Реализовано (found) | 774 (99.1%) |
| ⚠️ Частично (partial) | 6 (0.8%) |
| ❌ Не реализовано (not_found) | 1 (0.1%) |
| ➖ Неприменимо (n_a) | 47 |
| **MUST/MUST NOT found** | 476/478 (99.6%) |
| **SHOULD/SHOULD NOT found** | 298/303 (98.3%) |

## Соответствие по разделам (Stable)

| Раздел | ✅ | ⚠️ | ❌ | ➖ | Всего | % found |
|---|---|---|---|---|---|---|
| Context | 14 | 0 | 0 | 1 | 14 | 100.0% |
| Baggage Api | 17 | 0 | 0 | 0 | 17 | 100.0% |
| Resource Sdk | 21 | 0 | 0 | 0 | 21 | 100.0% |
| Trace Api | 109 | 1 | 0 | 16 | 110 | 99.1% |
| Trace Sdk | 85 | 0 | 0 | 4 | 85 | 100.0% |
| Logs Api | 22 | 0 | 0 | 0 | 22 | 100.0% |
| Logs Sdk | 73 | 0 | 0 | 3 | 73 | 100.0% |
| Metrics Api | 93 | 0 | 0 | 8 | 93 | 100.0% |
| Metrics Sdk | 203 | 2 | 0 | 4 | 205 | 99.0% |
| Otlp Exporter | 22 | 3 | 0 | 0 | 25 | 88.0% |
| Propagators | 25 | 0 | 0 | 11 | 25 | 100.0% |
| Env Vars | 24 | 0 | 0 | 0 | 24 | 100.0% |
| Prometheus Compatibility | 54 | 0 | 0 | 0 | 54 | 100.0% |
| Prometheus Exporter | 12 | 0 | 1 | 0 | 13 | 92.3% |

## Ключевые несоответствия (Stable)

### MUST/MUST NOT нарушения

- ⚠️ **[Metrics Sdk]** [MUST] The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection.  
  В штатном режиме выполняется: сборы одного читателя сериализованы (БлокировкаСбора в ОтелПериодическийЧитательМетрик и ОтелПрометеусЧитательМетрик), callback-и инструмента вызываются внутри сбора синхронно (inline при таймауте 0 или с ожиданием ОжидатьЗавершения). Но при срабатывании soft-timeout фоновое задание callback продолжает выполняться (OneScript не может прервать ФоновоеЗадание, issue #1672), и следующий раунд сбора начинается до завершения этого callback - это прямо зафиксировано тестом ТестМетр.ЗависшийОбратныйВызовНеЗапускаетсяПовторно («второй сбор начинается, пока задание первого еще выполняется»). SDK лишь пропускает повторный вызов такого callback и отбрасывает его результат, но не гарантирует завершение его выполнения до начала следующего сбора. (`src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:399-417 (БлокировкаСбора сериализует сборы); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:159-169 (БлокировкаСбора); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:394-414 (ВызватьCallbackи - синхронный цикл); src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:121-165`)

- ⚠️ **[Otlp Exporter]** [MUST] The following configuration options MUST be available to configure the OTLP exporter.  
  Опции Endpoint, Insecure, Headers, Timeout, Protocol и Max Request Size доступны (env-переменные с per-signal вариантами и параметры конструкторов транспортов). Но часть опций доступна лишь номинально: Client key file и Client certificate file (mTLS) читаются в ОтелНастройкиTls, но не применяются ни ОтелHttpТранспорт (HTTP-клиент OneScript/1connector, предупреждение в ОтелHttpТранспорт.os:379-383), ни ОтелGrpcТранспорт (OPI_GRPC не поддерживает mTLS, ОтелGrpcТранспорт.os:542-552); Certificate File применяется только gRPC-транспортом, HTTP-транспорт его игнорирует (ограничения TLS платформы и библиотек); Compression для grpc не применяется: у ОтелGrpcТранспорт нет параметра сжатия, ОтелАвтоконфигурация.ПредупредитьОСжатииGrpc (стр. 1061-1067) только логирует предупреждение; Max Response Size настраивается только в ОтелHttpТранспорт (УстановитьМаксРазмерОтвета, стр. 106-121), в ОтелGrpcТранспорт такой опции нет (есть лишь МаксРазмерЗапроса). (`src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-647 (СоздатьТранспортДляСигнала), 1357-1377 (СоздатьНастройкиTlsДляСигнала); src/Экспорт/Классы/ОтелHttpТранспорт.os:325-388; src/Экспорт/Классы/ОтелGrpcТранспорт.os:239-277`)

### SHOULD/SHOULD NOT несоответствия

- ⚠️ **[Trace Api]** [SHOULD NOT] If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type).  
  Рекомендуемый спекой способ реализован: ОтелСпаны.Обернуть()/Невалидный() (аналоги Java Span.wrap()/getInvalid()) возвращают объект с интерфейсом Span, комментарий класса (ОтелНезаписывающийСпан.os:266-267) не рекомендует прямое создание. Но сам тип ОтелНезаписывающийСпан открыт публично: он зарегистрирован в lib.config:36 как обычный класс, Новый ОтелНезаписывающийСпан(...) доступен любому коду (комментарий модуля ОтелСпаны.os:12-13 называет такое создание «допустимым», так делают тесты), библиотека сверяет тип по имени (ОтелТрассировщик.os:168), а справочник docs/api называет ОтелНезаписывающийСпан возвращаемым типом НачатьСпан/НачатьКорневойСпан/НачатьДочернийСпан (ОтелТрассировщик.md:55,71,88) и построителя спана (ОтелПостроительСпана.md:104-106). В lib.config OneScript нет internal/package-private классов, поэтому тип скрыт только рекомендациями в комментариях, а не технически. (`src/Трассировка/Модули/ОтелСпаны.os:1-13,36-59; lib.config:36; src/Трассировка/Классы/ОтелТрассировщик.os:168; docs/api/Трассировка/ОтелТрассировщик.md:55,71,88`)

- ⚠️ **[Metrics Sdk]** [SHOULD] The implementation SHOULD use a timeout to prevent indefinite callback execution.  
  Таймаут реализован как soft-timeout: ОтелИсполнительОбратныхВызовов.ВызватьСТаймаутом запускает callback через ФоновыеЗадания.Выполнить и ждет Задание.ОжидатьЗавершения(ТаймаутМс) (по умолчанию 30000 мс у ОтелМетр/ОтелПровайдерМетрик); по истечении сбор перестает ждать, измерения отбрасываются с предупреждением в лог и таймаутом в результате сбора. Само выполнение callback не прерывается: у ФоновоеЗадание в OneScript нет Прервать()/ОтменитьЗадание() (https://github.com/EvilBeaver/OneScript/issues/1672), задание продолжает работу в фоне; SDK лишь не вызывает этот callback повторно до завершения задания. Предотвращается неограниченное ожидание сбора, но не неограниченное выполнение callback. (`src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:121-165 (ВызватьСТаймаутом: ФоновыеЗадания.Выполнить + ОжидатьЗавершения(ТаймаутМс)), 182-192 (ЗаданиеВыполняется); src/Метрики/Классы/ОтелМетр.os:406-416,1035 (таймаут callback-ов, по умолчанию 30000 мс)`)

- ⚠️ **[Otlp Exporter]** [SHOULD] OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter.  
  HTTP-транспорт отправляет заголовок User-Agent: OTel-OTLP-Exporter-OneScript/<версия> (экспортер, язык и версия; подтверждено перехватом запроса). gRPC-транспорт кладет user-agent только в метаданные вызова (СформироватьМетаданные), а tonic внутри OPI_GRPC вырезает зарезервированный заголовок user-agent из метаданных и подставляет собственный: перехват запроса ОтелGrpcТранспорт показал user-agent: tonic/0.13.1, хотя пользовательская метаданная x-custom дошла. Для OTLP/gRPC экспортер себя в User-Agent не идентифицирует; юнит-тесты ТестGrpcТранспорт проверяют только содержимое Соответствия метаданных, а не отправляемый заголовок. (`src/Ядро/Модули/ОтелУтилиты.os:487-498 (UserAgentЭкспортераOtlp: OTel-OTLP-Exporter-OneScript/<версия>); src/Экспорт/Классы/ОтелHttpТранспорт.os:356-368; src/Экспорт/Классы/ОтелGrpcТранспорт.os:288-302`)

- ⚠️ **[Otlp Exporter]** [SHOULD] The resulting User-Agent SHOULD include the exporter’s default User-Agent string.  
  Для HTTP итоговый заголовок содержит стандартную строку после идентификатора продукта (перехвачено: MyDistribution/1.2.3 OTel-OTLP-Exporter-OneScript/1.1.0). Для gRPC идентификатор продукта и стандартная строка собираются только в метаданных, а на проводе tonic (OPI_GRPC) заменяет user-agent на tonic/0.13.1: итоговый User-Agent gRPC-запроса не содержит стандартной строки экспортера. (`src/Ядро/Модули/ОтелУтилиты.os:487-498 (ИдентификаторПродукта + пробел + СтандартныйUserAgent); src/Экспорт/Классы/ОтелHttpТранспорт.os:356-368; src/Экспорт/Классы/ОтелGrpcТранспорт.os:288-302`)

- ❌ **[Prometheus Exporter]** [SHOULD NOT] A Prometheus Exporter SHOULD use an official Prometheus client library when one exists for the implementation language and it is practical to do so (e.g., dependency concerns) for serving Prometheus m...  
  Экспортер использует неофициальную клиентскую библиотеку Prometheus: пакет prometheus 1.0.6 (yellow-hammer/prometheus, автор Ivan Karlo) - стороннюю библиотеку для OneScript с реестром коллекторов, типами метрик и сериализацией в text format/OpenMetrics. В списке официальных клиентских библиотек Prometheus (Go, Java/Scala, Python, Ruby, Rust) ее нет; официальной библиотеки для OneScript не существует. Зависимость времени выполнения объявлена в packagedef:32 и opm-metadata.xml:22 (dev=false). Выдачу метрик целиком формирует эта библиотека: ОтелПрометеусЧитательМетрик подключает ее (#Использовать prometheus, стр. 4), текст text format 0.0.4 строит Prometheus.СериализоватьВТекст (стр. 107), Content-Type берется из Prometheus.ContentTypeМетрик (стр. 116), выдача OpenMetrics (exemplars, _created, UNIT) возможна только через CollectorRegistry библиотеки, куда читатель отдает семейства методом Collect() (стр. 208-210). Собственного сериализатора формата экспозиции без библиотеки нет (документация Prometheus допускает реализовать формат экспозиции самостоятельно, если клиентской библиотеки для языка нет), поэтому SHOULD NOT не соблюдено. (`src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:4,107,116,208-210; packagedef:32; opm-metadata.xml:22`)

## Детальный анализ по разделам (Stable)

### Context

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:7,58-64,245-252,383` |  |
| 2 | MUST | ✅ found | A `Context` MUST be immutable, and its write operations MUST result in the creation of a new `Context` containing the original values and the specified values updated. | `src/Ядро/Модули/ОтелКонтекст.os:125-129,170-174,185-189,201-205,368-374` |  |
| 3 | MUST | ✅ found | In the cases where an extremely clear, pre-existing option is not available, OpenTelemetry MUST provide its own `Context` implementation. | `src/Ядро/Модули/ОтелКонтекст.os:3-14; src/Ядро/Классы/ОтелКлючКонтекста.os:1-4; src/Ядро/Классы/ОтелТокенКонтекста.os:50-56` |  |

#### Create a key

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#create-a-key)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The API MUST accept the following parameter: | `src/Ядро/Модули/ОтелКонтекст.os:42-44` |  |
| 5 | SHOULD NOT | ✅ found | Multiple calls to `CreateKey` with the same name SHOULD NOT return the same value unless language constraints dictate otherwise. | `src/Ядро/Модули/ОтелКонтекст.os:33-34,42-44; src/Ядро/Классы/ОтелКлючКонтекста.os:3-4,38-40` |  |
| 6 | MUST | ✅ found | The API MUST return an opaque object representing the newly created key. | `src/Ядро/Модули/ОтелКонтекст.os:42-44; src/Ядро/Классы/ОтелКлючКонтекста.os:1-42` |  |

#### Get value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Ядро/Модули/ОтелКонтекст.os:108-113` |  |
| 8 | MUST | ✅ found | The API MUST return the value in the `Context` for the specified key. | `src/Ядро/Модули/ОтелКонтекст.os:108-113` |  |

#### Set value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Ядро/Модули/ОтелКонтекст.os:125-129` |  |
| 10 | MUST | ✅ found | The API MUST return a new `Context` containing the new value. | `src/Ядро/Модули/ОтелКонтекст.os:125-129,368-374` |  |

#### Optional Global operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#optional-global-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ➖ n_a | These operations SHOULD only be used to implement automatic scope switching and define higher level APIs by SDK components and OpenTelemetry instrumentation libraries. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Оно адресовано авторам SDK-компонентов и instrumentation libraries (в каких случаях использовать глобальные операции Get current Context / Attach / Detach), а не реализации самого Context API: в OneScript нет разграничения SDK-only/пользовательского кода, все Экспорт-функции модуля ОтелКонтекст одинаково доступны любому вызывающему. Аналогично паттерну «ForceFlush SHOULD only be called in cases where it is absolutely necessary». Для справки: собственные компоненты SDK используют глобальные операции только для построения высокоуровневых API (ОтелСпан.СделатьТекущим, ОтелBaggage.СделатьТекущим/Текущий, неявный родитель в ОтелТрассировщик.os:74,99, неявный контекст в ОтелЛоггер.os:72,105,176). |

#### Get current Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#get-current-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST return the `Context` associated with the caller’s current execution unit. | `src/Ядро/Модули/ОтелКонтекст.os:58-64,324-334` |  |

#### Attach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#attach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | The API MUST accept the following parameters: * The `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:245` |  |
| 14 | MUST | ✅ found | The API MUST return a value that can be used as a `Token` to restore the previous `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:251,353-358` |  |

#### Detach Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/#detach-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The API MUST accept the following parameters: * A `Token` that was returned by a previous call to attach a `Context`. | `src/Ядро/Модули/ОтелКонтекст.os:267` |  |

### Baggage Api

#### Overview

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#overview)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Each name in `Baggage` MUST be associated with exactly one value. | `src/Ядро/Классы/ОтелПостроительBaggage.os:23-27` |  |
| 2 | SHOULD NOT | ✅ found | Language API SHOULD NOT restrict which strings are used as baggage names. | `src/Ядро/Классы/ОтелПостроительBaggage.os:23-27, src/Ядро/Классы/ОтелBaggage.os:67-71` |  |
| 3 | MUST | ✅ found | Language API MUST accept any valid UTF-8 string as baggage value in `Set` and return the same value from `Get`. | `src/Ядро/Классы/ОтелBaggage.os:37-39,67-71` |  |
| 4 | MUST | ✅ found | Language API MUST treat both baggage names and values as case sensitive. | `src/Ядро/Классы/ОтелBaggage.os:37-39, src/Ядро/Классы/ОтелПостроительBaggage.os:24` |  |
| 5 | MUST | ✅ found | The Baggage API MUST be fully functional in the absence of an installed SDK. | `src/Ядро/Классы/ОтелBaggage.os:16-27, src/Ядро/Модули/ОтелГлобальный.os:196-204` |  |
| 6 | MUST | ✅ found | The `Baggage` container MUST be immutable, so that the containing `Context` also remains immutable. | `src/Ядро/Классы/ОтелBaggage.os:151-162` |  |

#### Get Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#get-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | To access the value for a name/value pair set by a prior event, the Baggage API MUST provide a function that takes the name as input, and returns a value associated with the given name, or null if the... | `src/Ядро/Классы/ОтелBaggage.os:37-39` |  |

#### Get All Values

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#get-all-values)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST NOT | ✅ found | The order of name/value pairs MUST NOT be significant. | `src/Ядро/Классы/ОтелBaggage.os:102-104` |  |

#### Set Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#set-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | MUST | ✅ found | To record the value for a name/value pair, the Baggage API MUST provide a function which takes a name, and a value as input. | `src/Ядро/Классы/ОтелBaggage.os:67-71` |  |

#### Remove Value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#remove-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | To delete a name/value pair, the Baggage API MUST provide a function which takes a name as input. | `src/Ядро/Классы/ОтелBaggage.os:81-85 (Удалить(Ключ) - возвращает новый иммутабельный Baggage без ключа через ТоПостроитель().Удалить(Ключ).Построить()); src/Ядро/Классы/ОтелПостроительBaggage.os:37-41 (Builder.Удалить(Ключ))` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | If an implementation of this API does not operate directly on the `Context`, it MUST provide the following functionality to interact with a `Context` instance: | `src/Ядро/Модули/ОтелКонтекст.os:154-159 (BaggageИзКонтекста(КонтекстОбъект) = Extract Baggage from Context); src/Ядро/Модули/ОтелКонтекст.os:185-189 (КонтекстСBaggage(Контекст, Багаж) = Insert Baggage to Context, возвращает новый иммутабельный контекст)` |  |
| 12 | SHOULD NOT | ✅ found | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Baggage API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:23,46-50,382 (КлючBaggage - не-Экспорт переменная модуля, экспортные геттеры ключей удалены); src/Ядро/Классы/ОтелКлючКонтекста.os:1-4 (ключи сравниваются по ссылке - воссоздать ключ по имени нельзя)` |  |
| 13 | SHOULD | ✅ found | If the language has support for implicitly propagated `Context` (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Модули/ОтелКонтекст.os:95-97 (ТекущийBaggage() = Get active Baggage), src/Ядро/Модули/ОтелКонтекст.os:229-231 (СделатьBaggageТекущим(Багаж) = Set active Baggage, возвращает токен); src/Ядро/Классы/ОтелBaggage.os:16-18,25-27 (Текущий(), СделатьТекущим())` |  |
| 14 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:95-97,154-159,185-189,229-231; src/Ядро/Классы/ОтелBaggage.os:16-27 (полностью реализовано в ядре API поверх контекста, без зависимости от SDK-провайдеров)` |  |

#### Clear Baggage in the Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#clear-baggage-in-the-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | To avoid sending any name/value pairs to an untrusted process, the Baggage API MUST provide a way to remove all baggage entries from a context. | `src/Ядро/Классы/ОтелBaggage.os:93-95 (Очистить() - новый пустой Baggage); src/Ядро/Модули/ОтелКонтекст.os:185-189,229-231 (КонтекстСBaggage / СделатьBaggageТекущим - установка пустого Baggage в контекст); src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:37-40 (пустой Baggage не внедряется)` |  |

#### Propagation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#propagation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The API layer or an extension package MUST include the following `Propagator`s: | `src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:31 (Внедрить/Inject), :97 (Извлечь/Extract), :157 (Поля/Fields) - TextMapPropagator по W3C Baggage (заголовок baggage, percent-encoding, метаданные после ';', лимит 8192); lib.config:134` |  |

#### Conflict Resolution

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/baggage/api/#conflict-resolution)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | If a new name/value pair is added and its name is the same as an existing name, then the new pair MUST take precedence. | `src/Ядро/Классы/ОтелПостроительBaggage.os:23-27 (Установить: Значения.Вставить/Метаданные.Вставить заменяют существующую запись); src/Ядро/Классы/ОтелBaggage.os:67-71 (Установить через построитель); src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:137-138 (при извлечении от удалённого пира - тот же построитель, последняя пара побеждает)` |  |

### Resource Sdk

#### Resource SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#resource-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | The SDK MUST allow for creation of `Resources` and for associating them with telemetry. | `src/Ядро/Классы/ОтелРесурс.os:102-108; src/Ядро/Классы/ОтелПостроительРесурса.os:77-83; src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:30-33; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:28-31; src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:22-25` |  |
| 2 | MUST | ✅ found | When associated with a `TracerProvider`, all `Span`s produced by any `Tracer` from the provider MUST be associated with this `Resource`. | `src/Трассировка/Классы/ОтелТрассировщик.os:246-251; src/Трассировка/Классы/ОтелСпан.os:815-830; src/Трассировка/Классы/ОтелПровайдерТрассировки.os:123-125` |  |

#### SDK-provided resource attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#sdk-provided-resource-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The SDK MUST provide access to a Resource with at least the attributes listed at Semantic Attributes with SDK-provided Default Value. | `src/Ядро/Классы/ОтелРесурс.os:110-114` |  |
| 4 | MUST | ✅ found | This resource MUST be associated with a `TracerProvider`, `MeterProvider`, or `LoggerProvider` if another resource was not explicitly specified. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:413-417; src/Метрики/Классы/ОтелПровайдерМетрик.os:431-435; src/Логирование/Классы/ОтелПровайдерЛогирования.os:264-268` |  |

#### Create

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#create)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The interface MUST provide a way to create a new resource. | `src/Ядро/Классы/ОтелРесурс.os:102-108; src/Ядро/Классы/ОтелПостроительРесурса.os:22-83` |  |

#### Merge

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#merge)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | The interface MUST provide a way for an old resource and an updating resource to be merged into a new resource. | `src/Ядро/Классы/ОтелРесурс.os:41-66` |  |
| 7 | MUST | ✅ found | If either resource contains `Entities` then merge behavior with Entities MUST be used, otherwise merge behavior without Entities MUST be used. | `src/Ядро/Классы/ОтелРесурс.os:41-66` |  |

#### Merge behavior without Entities

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#merge-behavior-without-entities)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The resulting resource MUST have all attributes that are on any of the two input resources. | `src/Ядро/Классы/ОтелРесурс.os:58-64` |  |
| 9 | MUST | ✅ found | If a key exists on both the old and updating resource, the value of the updating resource MUST be picked (even if the updated value is empty). | `src/Ядро/Классы/ОтелРесурс.os:62-64; src/Ядро/Классы/ОтелАтрибуты.os:19-21` |  |

#### Detecting resource information from the environment

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#detecting-resource-information-from-the-environment)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific environments (e.g. EKS, AKS, GKE) MUST be implemented as packages separate from the SDK. | `src/Ядро/Классы/ОтелРесурс.os:116-119` |  |
| 11 | MUST | ✅ found | Resource detector packages MUST provide a method that returns a resource. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:17-31; src/Ядро/Классы/ОтелДетекторРесурсаПроцесса.os:17-27; src/Ядро/Классы/ОтелДетекторРесурсаПроцессора.os:22-38` |  |
| 12 | MUST NOT | ✅ found | Note the failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаПроцессора.os:26-31; src/Ядро/Модули/ОтелУтилиты.os:541-544` |  |
| 13 | SHOULD | ✅ found | Note the failure to detect any resource information MUST NOT be considered an error, whereas an error that occurs during an attempt to detect resource information SHOULD be considered an error. | `src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:23-27; src/Ядро/Классы/ОтелДетекторРесурсаПроцесса.os:21-23; src/Ядро/Классы/ОтелДетекторРесурсаПроцессора.os:32-34` |  |
| 14 | MUST | ✅ found | Resource detectors that populate resource attributes according to OpenTelemetry semantic conventions MUST ensure that the resource has a Schema URL set to a value that matches the semantic conventions... | `src/Ядро/Модули/ОтелУтилиты.os:541-550; src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:30; src/Ядро/Классы/ОтелДетекторРесурсаПроцесса.os:26; src/Ядро/Классы/ОтелДетекторРесурсаПроцессора.os:37` |  |
| 15 | SHOULD | ✅ found | Empty Schema URL SHOULD be used if the detector does not populate the resource with any known attributes that have a semantic convention or if the detector does not know what attributes it will popula... | `src/Ядро/Модули/ОтелУтилиты.os:541-544; src/Ядро/Классы/ОтелРесурс.os:143-158` |  |
| 16 | MUST | ✅ found | If multiple detectors are combined and the detectors use different non-empty Schema URL it MUST be an error since it is impossible to merge such resources. | `src/Ядро/Классы/ОтелРесурс.os:42-51; src/Ядро/Классы/ОтелРесурс.os:121-125` |  |

#### Specifying resource information via an environment variable

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/resource/sdk/#specifying-resource-information-via-an-environment-variable)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge this, as the secondary resource, with any resource information provided by the user, i.e. the user p... | `src/Ядро/Классы/ОтелРесурс.os:138-158; src/Ядро/Классы/ОтелПостроительРесурса.os:77-83; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:173-210` |  |
| 18 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Ядро/Классы/ОтелРесурс.os:171-200; src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:832-861` |  |
| 19 | MUST | ✅ found | The `,` and `=` characters in keys and values MUST be percent encoded. | `src/Ядро/Классы/ОтелРесурс.os:174-189; src/Ядро/Модули/ОтелУтилиты.os:302-322` |  |
| 20 | SHOULD | ✅ found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | `src/Ядро/Классы/ОтелРесурс.os:146-151,192-198; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:184-194` |  |
| 21 | SHOULD | ✅ found | In case of any error, e.g. failure during the decoding process, the entire environment variable value SHOULD be discarded and an error SHOULD be reported following the Error Handling principles. | `src/Ядро/Классы/ОтелРесурс.os:193-196; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:191-192` |  |

### Trace Api

#### TracerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `TracerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:119-121,129-138` |  |
| 2 | SHOULD | ✅ found | Thus, implementations of `TracerProvider` SHOULD allow creating an arbitrary number of `TracerProvider` instances. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:402-437; src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:105-113` |  |

#### TracerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The `TracerProvider` MUST provide the following functions: * Get a `Tracer` | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:51-53,67-107` |  |

#### Get a Tracer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-a-tracer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:67-71; src/Трассировка/Классы/ОтелПостроительТрассировщика.os:26-64` |  |
| 5 | SHOULD | ✅ found | This name SHOULD uniquely identify the instrumentation scope, such as the instrumentation library (e.g. `io.opentelemetry.contrib.mongodb`), package, module or class name. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:59,80-81,88; src/Ядро/Классы/ОтелОбластьИнструментирования.os:61-79,164-169` |  |
| 6 | MUST | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHO... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:72-106` |  |
| 7 | SHOULD | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHO... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:76-78,80-81` |  |
| 8 | SHOULD | ✅ found | In case an invalid name (null or empty string) is specified, a working Tracer implementation MUST be returned as a fallback rather than returning null or throwing an exception, its `name` property SHO... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:72-75` |  |
| 9 | MUST NOT | ✅ found | Implementations MUST NOT require users to repeatedly obtain a `Tracer` again with the same identity to pick up configuration changes. | `src/Трассировка/Классы/ОтелТрассировщик.os:8-9,50-52,216-254,362-379; src/Трассировка/Классы/ОтелПровайдерТрассировки.os:114-116,204-206; src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:62-73` |  |

#### Context Interaction

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#context-interaction)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The API MUST provide the following functionality to interact with a `Context` instance: * Extract the `Span` from a `Context` instance * Combine the `Span` with a `Context` instance, creating a new `C... | `src/Ядро/Модули/ОтелКонтекст.os:139-144,170-174` |  |
| 11 | SHOULD NOT | ✅ found | The functionality listed above is necessary because API users SHOULD NOT have access to the Context Key used by the Tracing API implementation. | `src/Ядро/Модули/ОтелКонтекст.os:20-21,46-50,381` |  |
| 12 | SHOULD | ✅ found | If the language has support for implicitly propagated `Context` (see here), the API SHOULD also provide the following functionality: | `src/Ядро/Модули/ОтелКонтекст.os:85-87,216-218` |  |
| 13 | SHOULD | ✅ found | This functionality SHOULD be fully implemented in the API when possible. | `src/Ядро/Модули/ОтелКонтекст.os:85-87,139-144,170-174,216-218` |  |

#### Tracer operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracer-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | The `Tracer` MUST provide functions to: * Create a new `Span` (see the section on `Span`) | `src/Трассировка/Классы/ОтелТрассировщик.os:25-27,71-76,93-101,121-126` |  |
| 15 | SHOULD | ✅ found | The `Tracer` SHOULD provide functions to: * Report if `Tracer` is `Enabled` | `src/Трассировка/Классы/ОтелТрассировщик.os:50-52` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when creating `Span`s, a `Tracer` SHOULD provide this `Enabled` API. | `src/Трассировка/Классы/ОтелТрассировщик.os:29-52` |  |
| 17 | MUST | ✅ found | Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Трассировка/Классы/ОтелТрассировщик.os:50` |  |
| 18 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Трассировка/Классы/ОтелТрассировщик.os:47-52,191-193; src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:51-53` |  |
| 19 | SHOULD | ✅ found | The API SHOULD be documented that instrumentation authors needs to call this API each time they create a new `Span` to ensure they have the most up-to-date response. | `src/Трассировка/Классы/ОтелТрассировщик.os:29-33` |  |

#### SpanContext

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spancontext)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | The API MUST implement methods to create a `SpanContext`. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:252-272` |  |
| 21 | SHOULD | ✅ found | These methods SHOULD be the only way to create a `SpanContext`. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:230-236,252-272` |  |
| 22 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:16-95,252-272` |  |
| 23 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:230-236,252-272` |  |

#### Retrieving the TraceId and SpanId

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#retrieving-the-traceid-and-spanid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | The API MUST allow retrieving the `TraceId` and `SpanId` in the following forms: | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23-34 (ИдТрассировки/ИдСпана - hex),84-95 (ИдТрассировкиВДвоичномВиде/ИдСпанаВДвоичномВиде - binary)` |  |
| 25 | MUST | ✅ found | Hex - returns the lowercase hex encoded `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` (result MUST be a 16-hex-character lowercase string). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23-25,176-194 (ДвоичныеВHex, алфавит 0123456789abcdef),257-259` |  |
| 26 | MUST | ✅ found | Hex - returns the lowercase hex encoded `TraceId` (result MUST be a 32-hex-character lowercase string) or `SpanId` (result MUST be a 16-hex-character lowercase string). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:32-34,176-194 (ДвоичныеВHex, алфавит 0123456789abcdef),258-260` |  |
| 27 | MUST | ✅ found | Binary - returns the binary representation of the `TraceId` (result MUST be a 16-byte array) or `SpanId` (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:84-86,136-164 (HexВДвоичные),259` |  |
| 28 | MUST | ✅ found | Binary - returns the binary representation of the `TraceId` (result MUST be a 16-byte array) or `SpanId` (result MUST be an 8-byte array). | `src/Трассировка/Классы/ОтелКонтекстСпана.os:93-95,136-164 (HexВДвоичные),260` |  |
| 29 | SHOULD NOT | ✅ found | The API SHOULD NOT expose details about how they are internally stored. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:3-6 (хранилище - неэкспортные переменные),23-34,84-95` |  |

#### IsValid

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isvalid)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | An API called `IsValid`, that returns a boolean value, which is `true` if the SpanContext has a non-zero TraceID and a non-zero SpanID, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:70-77 (Валиден),109-123 (ВсеНулевыеБайты)` |  |

#### IsRemote

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isremote)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 31 | MUST | ✅ found | An API called `IsRemote`, that returns a boolean value, which is `true` if the SpanContext was propagated from a remote parent, MUST be provided. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:60-62 (Удаленный)` |  |
| 32 | MUST | ✅ found | When extracting a `SpanContext` through the Propagators API, `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:163 (Новый ОтелКонтекстСпана(..., Истина) в Извлечь)` |  |
| 33 | MUST | ✅ found | When extracting a `SpanContext` through the Propagators API, `IsRemote` MUST return true, whereas for the SpanContext of any child spans it MUST return false. | `src/Трассировка/Классы/ОтелКонтекстСпана.os:256 (Удаленный = Ложь по умолчанию); src/Трассировка/Классы/ОтелСпан.os:846-847; src/Трассировка/Классы/ОтелТрассировщик.os:292` |  |

#### TraceState

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#tracestate)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | MUST | ✅ found | Tracing API MUST provide at least the following operations on `TraceState`: | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:50-57 (Получить),73-112 (Установить - add/update),122-140 (Удалить)` |  |
| 35 | MUST | ✅ found | These operations MUST follow the rules described in the W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:88-106 (новый/измененный ключ в начало, вытеснение крайней правой записи при 32),296-316 (усечение до 512),339-392 (валидация ключа и значения по W3C)` |  |
| 36 | MUST | ✅ found | All mutating operations MUST return a new `TraceState` with the modifications applied. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:108-111,136-139` |  |
| 37 | MUST | ✅ found | `TraceState` MUST at all times be valid according to rules specified in W3C Trace Context specification. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:74-86,238-291 (Разобрать: отброс невалидных, дубликатов и записей сверх 32),296-316,339-392` |  |
| 38 | MUST | ✅ found | Every mutating operations MUST validate input parameters. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:74-86 (Установить: КлючВалиден/ЗначениеВалидно),123-128 (Удалить: КлючВалиден)` |  |
| 39 | MUST NOT | ✅ found | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data and MUST follow the general error handling guidelines. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:74-86,123-128 (при невалидном вводе возвращается неизмененный ЭтотОбъект)` |  |
| 40 | MUST | ✅ found | If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data and MUST follow the general error handling guidelines. | `src/Трассировка/Классы/ОтелСостояниеТрассировки.os:75-78,81-85,124-127 (Лог.Предупреждение без исключения, возврат исходного состояния)` |  |

#### Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 41 | SHOULD | ➖ n_a | The span name SHOULD be the most general string that identifies a (statistically) interesting class of Spans, rather than individual Span instances while still being human-readable. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Имя спана выбирает вызывающий код при вызове ОтелТрассировщик.ПостроительСпана()/НачатьСпан(), SDK принимает любую переданную строку. Собственных Instrumentation Libraries, формирующих имена спанов, пакет не содержит (src/Интеграции содержит только ОтелАппендерLogos для логов). |
| 42 | SHOULD | ➖ n_a | Generality SHOULD be prioritized over human-readability. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Это продолжение рекомендации по выбору имени спана: имя задает вызывающий код, SDK не может оценить общность имени и приоритизировать ее над читаемостью. |
| 43 | SHOULD | ✅ found | A `Span`’s start time SHOULD be set to the current time on span creation. | `src/Трассировка/Классы/ОтелСпан.os:851-856` |  |
| 44 | SHOULD | ✅ found | After the `Span` is created, it SHOULD be possible to change its name, set its `Attribute`s, add `Event`s, and set the `Status`. | `src/Трассировка/Классы/ОтелСпан.os:307-314 (ИзменитьИмя),328-343 (УстановитьАтрибут),358-373 (ДобавитьСобытие),496-515 (УстановитьСтатус)` |  |
| 45 | MUST NOT | ✅ found | These MUST NOT be changed after the `Span`’s end time has been set. | `src/Трассировка/Классы/ОтелСпан.os:309,329,359,498,504,557,575 (проверки Завершен.Получить()),526-544 (Завершить устанавливает Завершен под блокировкой)` |  |
| 46 | SHOULD NOT | ➖ n_a | To prevent misuse, implementations SHOULD NOT provide access to a `Span`’s attributes besides its `SpanContext`. | `src/Трассировка/Классы/ОтелСпан.os:5-14,168-201` | OneScript не поддерживает internal/package-private модификаторы; SDK-геттеры (Атрибуты(), События(), Линки() и т.п.) обязаны быть Экспорт, иначе процессоры/экспортёры не смогут читать данные спана. Аналогично приватным конструкторам. Ограничение явно задокументировано в шапке класса ОтелСпан.os:5-14 со ссылкой на это требование; геттеры возвращают копии коллекций (ОтелСпан.os:168-201), изменить спан через них нельзя. |
| 47 | MUST NOT | ➖ n_a | However, alternative implementations MUST NOT allow callers to create `Span`s directly. | `src/Трассировка/Классы/ОтелСпан.os:786-791` | OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. ПриСозданииОбъекта всегда публичен, поэтому Новый ОтелСпан(...) технически вызываем из пользовательского кода; комментарий класса (ОтелСпан.os:786-791) запрещает прямой вызов, внутри SDK единственная точка создания - ОтелТрассировщик.НачатьСпанSdk() (ОтелТрассировщик.os:246). |
| 48 | MUST | ✅ found | All `Span`s MUST be created via a `Tracer`. | `src/Трассировка/Классы/ОтелТрассировщик.os:25-27 (ПостроительСпана),71-76 (НачатьСпан),93-101 (НачатьКорневойСпан),121-126 (НачатьДочернийСпан),216-254 (НачатьСпанSdk - единственный вызов Новый ОтелСпан, строка 246)` |  |

#### Span Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 49 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating a `Span` other than with a `Tracer`. | `src/Трассировка/Классы/ОтелСпан.os:786-791` | OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Помимо платформенно-неустранимого публичного конструктора ОтелСпан других API создания спана нет: единственный вызов Новый ОтелСпан(...) в src - ОтелТрассировщик.НачатьСпанSdk() (ОтелТрассировщик.os:246); ОтелСпаны.Обернуть()/Невалидный() лишь оборачивают существующий SpanContext в незаписывающий спан - это отдельная операция, которую требует сама спецификация (Wrapping a SpanContext in a Span). |
| 50 | MUST NOT | ✅ found | In languages with implicit `Context` propagation, `Span` creation MUST NOT set the newly created `Span` as the active `Span` in the current `Context` by default, but this functionality MAY be offered ... | `src/Трассировка/Классы/ОтелТрассировщик.os:71-76,158-179,216-254 (создание не помещает спан в контекст); src/Трассировка/Классы/ОтелСпан.os:480-482 (СделатьТекущим - отдельная операция)` |  |
| 51 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Трассировка/Классы/ОтелТрассировщик.os:25-27,71-76,93-101,121-126; src/Трассировка/Классы/ОтелПостроительСпана.os:37-117; src/Трассировка/Классы/ОтелСпан.os:772-778 (SpanKind по умолчанию Внутренний),851-858 (время начала по умолчанию текущее, пустые атрибуты)` |  |
| 52 | MUST NOT | ✅ found | This API MUST NOT accept a `Span` or `SpanContext` as parent, only a full `Context`. | `src/Трассировка/Классы/ОтелПостроительСпана.os:37-41 (УстановитьРодителя(Context)); src/Трассировка/Классы/ОтелТрассировщик.os:121-126,158-166; src/Ядро/Модули/ОтелКонтекст.os:139-144` |  |
| 53 | MUST | ✅ found | The semantic parent of the Span MUST be determined according to the rules described in Determining the Parent Span from a Context. | `src/Трассировка/Классы/ОтелТрассировщик.os:158-179 (НачатьСпанВКонтексте: ОтелКонтекст.СпанИзКонтекста),216-234 (невалидный родитель - корневой спан)` |  |
| 54 | MUST | ✅ found | The API documentation MUST state that adding attributes at span creation is preferred to calling `SetAttribute` later, as samplers can only consider information already present during span creation. | `src/Трассировка/Классы/ОтелПостроительСпана.os:69-71; src/Трассировка/Классы/ОтелТрассировщик.os:61-62; docs/api/Трассировка/ОтелПостроительСпана.md:63` |  |
| 55 | SHOULD | ➖ n_a | This argument SHOULD only be set when span creation time has already passed. | `src/Трассировка/Классы/ОтелПостроительСпана.os:101-117` | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение - он не может определить, совпадает ли момент вызова API с логическим стартом операции. Рекомендация отражена в документирующем комментарии УстановитьВремяНачала() (ОтелПостроительСпана.os:104-106); если аргумент не задан, используется текущее время (ОтелСпан.os:851-856). |
| 56 | MUST NOT | ➖ n_a | If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument. | `src/Трассировка/Классы/ОтелПостроительСпана.os:101-117` | Требование является рекомендацией по использованию для вызывающих кода (caller guidance): субъект - «API user», SDK не может программно обеспечить это ограничение и запретить вызов УстановитьВремяНачала(). Комментарий метода (ОтелПостроительСпана.os:104-106) указывает задавать время явно ТОЛЬКО если вызов API не совпадает с логическим стартом операции. |
| 57 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span, and MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:93-101 (НачатьКорневойСпан); src/Трассировка/Классы/ОтелПостроительСпана.os:49-53 (БезРодителя)` |  |
| 58 | MUST | ✅ found | Implementations MUST provide an option to create a `Span` as a root span, and MUST generate a new `TraceId` for each root span created. | `src/Трассировка/Классы/ОтелТрассировщик.os:229-230 (Провайдер.СгенерироватьИдТрассировки() без валидного родителя); src/Трассировка/Классы/ОтелПровайдерТрассировки.os:291-304; src/Ядро/Модули/ОтелУтилиты.os:96-116` |  |
| 59 | MUST | ✅ found | For a Span with a parent, the `TraceId` MUST be the same as the parent. | `src/Трассировка/Классы/ОтелТрассировщик.os:224-225 (ИдТрассировки = ВалидныйРодитель.ИдТрассировки()),241,246-251` |  |
| 60 | MUST | ✅ found | Also, the child span MUST inherit all `TraceState` values of its parent by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:228,245,284-285,417-426 (ОпределитьСостояниеТрассировки); src/Трассировка/Модули/ОтелСэмплер.os:184 (сэмплер возвращает TraceState родителя)` |  |
| 61 | MUST | ➖ n_a | Any span that is created MUST also be ended. | `src/Трассировка/Классы/ОтелСпан.os:526-544` | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Спецификация прямо указывает: «This is the responsibility of the user» и допускает утечку ресурсов при незавершенных спанах. Для завершения SDK предоставляет ОтелСпан.Завершить() (ОтелСпан.os:526-544). |

#### Specifying links

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#specifying-links)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 62 | MUST | ✅ found | During `Span` creation, a user MUST have the ability to record links to other `Span`s. | `src/Трассировка/Классы/ОтелПостроительСпана.os:96-99 (ДобавитьЛинк); src/Трассировка/Классы/ОтелТрассировщик.os:71-76 (параметр Линки); src/Трассировка/Классы/ОтелСпан.os:897-901 (линки применяются до OnStart)` |  |

#### Get Context

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#get-context)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 63 | MUST | ✅ found | The Span interface MUST provide: An API that returns the `SpanContext` for the given `Span`. | `src/Трассировка/Классы/ОтелСпан.os:97-99 (КонтекстСпана() возвращает ОтелКонтекстСпана, без проверки Завершен - доступен и после завершения спана); src/Трассировка/Классы/ОтелНезаписывающийСпан.os:29-31` |  |
| 64 | MUST | ✅ found | The returned value MUST be the same for the entire Span lifetime. | `src/Трассировка/Классы/ОтелСпан.os:846-847 (КонтекстСпана присваивается только в конструкторе, сеттера нет), 97-99; src/Трассировка/Классы/ОтелКонтекстСпана.os:230-236 (сеттеры не Экспорт - контекст неизменяем); src/Трассировка/Классы/ОтелНезаписывающийСпан.os:275-284` |  |

#### IsRecording

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#isrecording)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:526-544 (Завершить устанавливает Завершен), 154-160, 307-314, 328-331, 358-361, 386-389, 430-433, 496-500 (все мутаторы игнорируются после завершения), 556-559, 574-577, 594-597 (повторная проверка под блокировкой)` |  |
| 66 | SHOULD | ✅ found | After a `Span` is ended, it SHOULD become non-recording and `IsRecording` SHOULD always return `false`. | `src/Трассировка/Классы/ОтелСпан.os:294-296 (ЗаписьАктивна() = НЕ Завершен.Получить()), 538-540 (Завершен устанавливается в Завершить); src/Трассировка/Классы/ОтелНезаписывающийСпан.os:155-157` |  |
| 67 | SHOULD NOT | ✅ found | `IsRecording` SHOULD NOT take any parameters. | `src/Трассировка/Классы/ОтелСпан.os:294 (Функция ЗаписьАктивна() Экспорт - без параметров); src/Трассировка/Классы/ОтелНезаписывающийСпан.os:155` |  |
| 68 | SHOULD | ➖ n_a | This flag SHOULD be used to avoid expensive computations of a Span attributes or events in case when a Span is definitely not recorded. | `src/Трассировка/Классы/ОтелСпан.os:294-296; src/Трассировка/Классы/ОтелНезаписывающийСпан.os:155-157` | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Оно адресовано авторам инструментирования (секция продолжает: «Users of the API should only access the IsRecording property when instrumenting code»): проверять флаг перед дорогими вычислениями атрибутов/событий. Сам флаг реализован и доступен для такой проверки: ОтелСпан.ЗаписьАктивна(), ОтелНезаписывающийСпан.ЗаписьАктивна() = Ложь. |

#### Set Attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | MUST | ✅ found | A `Span` MUST have the ability to set `Attributes` associated with it. | `src/Трассировка/Классы/ОтелСпан.os:328-343 (УстановитьАтрибут), 556-567 (ЗаписатьАтрибут)` |  |
| 70 | MUST | ✅ found | The Span interface MUST provide: An API to set a single `Attribute` where the attribute properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:328 (Функция УстановитьАтрибут(Ключ, Значение) Экспорт); src/Трассировка/Классы/ОтелНезаписывающийСпан.os:180-182` |  |
| 71 | SHOULD | ✅ found | Setting an attribute with the same key as an existing attribute SHOULD overwrite the existing attribute’s value. | `src/Трассировка/Классы/ОтелСпан.os:556-567 (существующий ключ минует проверку лимита и перезаписывается); src/Ядро/Классы/ОтелАтрибуты.os:19-22 (Соответствие.Вставить заменяет значение по ключу)` |  |

#### Add Events

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-events)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | MUST | ✅ found | A `Span` MUST have the ability to add events. | `src/Трассировка/Классы/ОтелСпан.os:358-373 (ДобавитьСобытие), 574-587 (ЗаписатьСобытие)` |  |
| 73 | MUST | ✅ found | The Span interface MUST provide: An API to record a single `Event` where the `Event` properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:358 (ДобавитьСобытие(НовоеИмя, НовыеАтрибуты = Неопределено, МеткаВремени = Неопределено) - имя, необязательные атрибуты и метка времени отдельными параметрами); src/Трассировка/Классы/ОтелСобытиеСпана.os:94-98 (без метки - текущее время вызова)` |  |
| 74 | SHOULD | ✅ found | Events SHOULD preserve the order in which they are recorded. | `src/Трассировка/Классы/ОтелСпан.os:574-587 (События.Добавить в конец массива под блокировкой), 189-191, 643-656 (копия в том же порядке); src/Экспорт/Классы/ОтелЭкспортерСпанов.os:238-242 (экспорт в порядке записи)` |  |

#### Add Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#add-link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | MUST | ✅ found | A `Span` MUST have the ability to add `Link`s associated with it after its creation - see Links. | `src/Трассировка/Классы/ОтелСпан.os:430-460 (ДобавитьЛинк(НовыйКонтекстСпана, НовыеАтрибуты = Неопределено) на созданном спане), 594-609 (ЗаписатьЛинк)` |  |

#### Set Status

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#set-status)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 76 | MUST | ✅ found | `Description` MUST only be used with the `Error` `StatusCode` value. | `src/Трассировка/Классы/ОтелСпан.os:506-510 (СообщениеСтатуса сохраняется только для Ошибка, иначе пустая строка); src/Экспорт/Классы/ОтелЭкспортерСпанов.os:268-273 (message экспортируется только непустым)` |  |
| 77 | MUST | ✅ found | The Span interface MUST provide: An API to set the `Status`. | `src/Трассировка/Классы/ОтелСпан.os:496-515 (УстановитьСтатус(Значение, Сообщение = '') - StatusCode и необязательный Description отдельными параметрами); src/Трассировка/Модули/ОтелКодСтатуса.os:14-34; src/Трассировка/Классы/ОтелНезаписывающийСпан.os:243-245` |  |
| 78 | SHOULD | ✅ found | This SHOULD be called `SetStatus`. | `src/Трассировка/Классы/ОтелСпан.os:496 (УстановитьСтатус - точный перевод SetStatus)` |  |
| 79 | MUST | ✅ found | `Description` MUST be IGNORED for `StatusCode` `Ok` & `Unset` values. | `src/Трассировка/Классы/ОтелСпан.os:497-500 (вызов с Unset игнорируется целиком), 508-509 (для Ok сообщение сбрасывается в пустую строку)` |  |
| 80 | SHOULD | ✅ found | The status code SHOULD remain unset, except for the following circumstances: | `src/Трассировка/Классы/ОтелСпан.os:861 (КодСтатуса = НеУстановлен по умолчанию; SDK сам статус спана не выставляет - УстановитьСтатус вызывается только пользователем, ЗаписатьИсключение статус не меняет), 497-500` |  |
| 81 | SHOULD | ✅ found | An attempt to set value `Unset` SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:497-500 (Значение = ОтелКодСтатуса.НеУстановлен() - возврат без изменений)` |  |
| 82 | SHOULD | ➖ n_a | When the status is set to `Error` by Instrumentation Libraries, the `Description` SHOULD be documented and predictable. | - | Требование адресовано Instrumentation Libraries (политика их поведения: документирование Description при статусе Error); данный пакет реализует только API+SDK, IL не включены (src/Интеграции содержит лишь мост логов ОтелАппендерLogos, статус спанов он не выставляет). |
| 83 | SHOULD | ➖ n_a | For operations not covered by the semantic conventions, Instrumentation Libraries SHOULD publish their own conventions, including possible values of `Description` and what they mean. | - | Требование адресовано Instrumentation Libraries (политика их поведения: публикация собственных конвенций и значений Description); данный пакет реализует только API+SDK, IL не включены. |
| 84 | SHOULD NOT | ➖ n_a | Generally, Instrumentation Libraries SHOULD NOT set the status code to `Ok`, unless explicitly configured to do so. | - | Требование адресовано Instrumentation Libraries (политика их поведения); данный пакет реализует только API+SDK, IL не включены. Сам SDK статус Ok не выставляет. |
| 85 | SHOULD | ➖ n_a | Instrumentation Libraries SHOULD leave the status code as `Unset` unless there is an error, as described above. | - | Требование адресовано Instrumentation Libraries (политика их поведения); данный пакет реализует только API+SDK, IL не включены. |
| 86 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:503-504 (статус меняется только при КодСтатуса <> Ок - Ok финален)` |  |
| 87 | SHOULD | ✅ found | When span status is set to `Ok` it SHOULD be considered final and any further attempts to change it SHOULD be ignored. | `src/Трассировка/Классы/ОтелСпан.os:497-511 (после Ok любые вызовы УстановитьСтатус, включая Error и Unset, не меняют код и сообщение)` |  |
| 88 | SHOULD | ➖ n_a | Analysis tools SHOULD respond to an `Ok` status by suppressing any errors they would otherwise generate. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:268-273` | Требование адресовано внешним Analysis tools (бэкендам/системам анализа, потребляющим телеметрию), а не Trace API/SDK - по тому же принципу, что и требования к Instrumentation Libraries и OpenTelemetry Organization (субъект требования - не реализация SDK). Данный пакет только генерирует и экспортирует телеметрию; со стороны SDK статус Ok корректно передается потребителям (status.code в OTLP, ОтелЭкспортерСпанов.os:268-273), поведение сторонних систем анализа в этом коде не реализуется и не может быть верифицировано. |

#### End

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#end)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | SHOULD | ✅ found | Implementations SHOULD ignore all subsequent calls to `End` and any other Span methods, i.e. the Span becomes non-recording by being ended (there might be exceptions when Tracer is streaming events an... | `src/Трассировка/Классы/ОтелСпан.os:527-530 (CAS-guard ЗавершаетсяСейчас: повторный Завершить - no-op), 154-160, 307-314, 328-331, 358-361, 386-389, 430-433, 496-500 (мутаторы игнорируются после завершения), 294-296 (ЗаписьАктивна = Ложь)` |  |
| 90 | MUST | ✅ found | However, all API implementations of such methods MUST internally call the `End` method and be documented to do so. | `src/Трассировка/Классы/ОтелСпан.os:526-544 (Завершить - единственный метод, завершающий спан; альтернативных методов завершения в API нет); src/Ядро/Классы/ОтелТокенКонтекста.os:35-44 (Закрыть() только отсоединяет контекст и спан не завершает - задокументировано в ОтелСпан.os:466-469, 520-521)` |  |
| 91 | MUST NOT | ✅ found | `End` MUST NOT have any effects on child spans. | `src/Трассировка/Классы/ОтелСпан.os:526-544 (меняет только собственное состояние: ВремяОкончания, Завершен, затем ПриЗавершении процессора для этого спана; ссылок на дочерние спаны у спана нет)` |  |
| 92 | MUST NOT | ✅ found | `End` MUST NOT inactivate the `Span` in any `Context` it is active in. | `src/Трассировка/Классы/ОтелСпан.os:517-544 (Завершить не обращается к ОтелКонтекст и не закрывает область - задокументировано в 520-521); src/Ядро/Модули/ОтелКонтекст.os:267-306 (снятие спана из контекста только через ОтсоединитьКонтекст по токену)` |  |
| 93 | MUST | ✅ found | It MUST still be possible to use an ended span as parent via a Context it is contained in. | `src/Трассировка/Классы/ОтелТрассировщик.os:158-166 (родитель берется из контекста через КонтекстСпана() без проверки завершенности), 216-235; src/Трассировка/Классы/ОтелСпан.os:97-99` |  |
| 94 | MUST | ✅ found | Also, any mechanisms for putting the Span into a Context MUST still work after the Span was ended. | `src/Трассировка/Классы/ОтелСпан.os:480-482 (СделатьТекущим без проверки Завершен); src/Ядро/Модули/ОтелКонтекст.os:170-174 (КонтекстСоСпаном), 216-218 (СделатьСпанТекущим)` |  |
| 95 | MUST | ✅ found | If omitted, this MUST be treated equivalent to passing the current time. | `src/Трассировка/Классы/ОтелСпан.os:526, 531-535 (НовоеВремяОкончания = Неопределено -> ОтелУтилиты.ТекущееВремяВНаносекундах())` |  |
| 96 | MUST NOT | ✅ found | This operation itself MUST NOT perform blocking I/O on the calling thread. | `src/Трассировка/Классы/ОтелСпан.os:526-544 (без ввода-вывода); src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:32-37; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-69 (OnEnd только кладет спан в буфер, экспорт выполняет фоновое задание); src/Конфигурация/Модули/ОтелАвтоконфигурация.os:740-794 (по умолчанию пакетный процессор); синхронный ОтелПростойПроцессорСпанов предназначен для отладки (ОтелПростойПроцессорСпанов.os:135-136) и по тексту спеки вне области требования` |  |
| 97 | SHOULD | ✅ found | Any locking used needs be minimized and SHOULD be removed entirely if possible. | `src/Трассировка/Классы/ОтелСпан.os:527-530 (lock-free CAS на АтомарноеБулево), 536-540 (БлокировкаРесурса удерживается только на установку флага Завершен, чтобы дождаться начатых записей; вызов процессора вне блокировки); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:53-64 (блокировка буфера только на добавление элемента)` |  |

#### Record Exception

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#record-exception)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | SHOULD | ✅ found | To facilitate recording an exception languages SHOULD provide a `RecordException` method if the language uses exceptions. | `src/Трассировка/Классы/ОтелСпан.os:375-418 (ЗаписатьИсключение); src/Трассировка/Классы/ОтелНезаписывающийСпан.os:198-209` |  |
| 99 | MUST | ✅ found | The method MUST record an exception as an `Event` with the conventions outlined in the exceptions document. | `src/Трассировка/Классы/ОтелСпан.os:391-407 (атрибуты exception.message, exception.type, exception.stacktrace), 415 (событие с именем exception через ДобавитьСобытие)` |  |
| 100 | SHOULD | ✅ found | The minimum required argument SHOULD be no more than only an exception object. | `src/Трассировка/Классы/ОтелСпан.os:386 (единственный обязательный параметр - ИнформацияОбОшибке)` |  |
| 101 | MUST | ✅ found | If `RecordException` is provided, the method MUST accept an optional parameter to provide any additional event attributes (this SHOULD be done in the same way as for the `AddEvent` method). | `src/Трассировка/Классы/ОтелСпан.os:386 (ДополнительныеАтрибуты = Неопределено), 409-413 (дополнительные атрибуты записываются после сгенерированных и имеют приоритет)` |  |
| 102 | SHOULD | ✅ found | If `RecordException` is provided, the method MUST accept an optional parameter to provide any additional event attributes (this SHOULD be done in the same way as for the `AddEvent` method). | `src/Трассировка/Классы/ОтелСпан.os:358 (ДобавитьСобытие: НовыеАтрибуты - необязательный ОтелАтрибуты), 386 (ЗаписатьИсключение: ДополнительныеАтрибуты - необязательный ОтелАтрибуты), 415 (атрибуты проходят через ДобавитьСобытие с теми же лимитами)` |  |

#### Span lifetime

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#span-lifetime)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 103 | MUST | ✅ found | Start and end time as well as Event’s timestamps MUST be recorded at a time of a calling of corresponding API. | `src/Трассировка/Классы/ОтелСпан.os:854-859 (время начала фиксируется при создании спана в НачатьСпан), 534-538 (время окончания - при вызове Завершить); src/Трассировка/Классы/ОтелСобытиеСпана.os:94-98 (метка события - при вызове ДобавитьСобытие, ОтелСпан.os:363)` |  |

#### Wrapping a SpanContext in a Span

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#wrapping-a-spancontext-in-a-span)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 104 | MUST | ✅ found | The API MUST provide an operation for wrapping a `SpanContext` with an object implementing the `Span` interface. | `src/Трассировка/Модули/ОтелСпаны.os:24-44 (Обернуть); src/Трассировка/Классы/ОтелНезаписывающийСпан.os:13-256 (интерфейс Span: КонтекстСпана, ЗаписьАктивна, УстановитьАтрибут, ДобавитьСобытие, ДобавитьЛинк, УстановитьСтатус, ИзменитьИмя, Завершить, ЗаписатьИсключение)` |  |
| 105 | SHOULD NOT | ⚠️ partial | If a new type is required for supporting this operation, it SHOULD NOT be exposed publicly if possible (e.g. by only exposing a function that returns something with the Span interface type). | `src/Трассировка/Модули/ОтелСпаны.os:1-13,36-59; lib.config:36; src/Трассировка/Классы/ОтелТрассировщик.os:168; docs/api/Трассировка/ОтелТрассировщик.md:55,71,88` | Рекомендуемый спекой способ реализован: ОтелСпаны.Обернуть()/Невалидный() (аналоги Java Span.wrap()/getInvalid()) возвращают объект с интерфейсом Span, комментарий класса (ОтелНезаписывающийСпан.os:266-267) не рекомендует прямое создание. Но сам тип ОтелНезаписывающийСпан открыт публично: он зарегистрирован в lib.config:36 как обычный класс, Новый ОтелНезаписывающийСпан(...) доступен любому коду (комментарий модуля ОтелСпаны.os:12-13 называет такое создание «допустимым», так делают тесты), библиотека сверяет тип по имени (ОтелТрассировщик.os:168), а справочник docs/api называет ОтелНезаписывающийСпан возвращаемым типом НачатьСпан/НачатьКорневойСпан/НачатьДочернийСпан (ОтелТрассировщик.md:55,71,88) и построителя спана (ОтелПостроительСпана.md:104-106). В lib.config OneScript нет internal/package-private классов, поэтому тип скрыт только рекомендациями в комментариях, а не технически. |
| 106 | SHOULD | ✅ found | If a new type is required to be publicly exposed, it SHOULD be named `NonRecordingSpan`. | `lib.config:36; src/Трассировка/Классы/ОтелНезаписывающийСпан.os:260-267 (ОтелНезаписывающийСпан = NonRecordingSpan с обязательным префиксом Отел)` |  |
| 107 | MUST | ✅ found | `GetContext` MUST return the wrapped `SpanContext`. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:29-31,277-278; src/Трассировка/Модули/ОтелСпаны.os:43` |  |
| 108 | MUST | ✅ found | `IsRecording` MUST return `false` to signal that events, attributes and other elements are not being recorded, i.e. they are being dropped. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:155-157` |  |
| 109 | MUST | ✅ found | The remaining functionality of `Span` MUST be defined as no-op operations. | `src/Трассировка/Классы/ОтелНезаписывающийСпан.os:69-76,159-222,234-254` |  |
| 110 | MUST | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Модули/ОтелСпаны.os:36-59; src/Трассировка/Классы/ОтелНезаписывающийСпан.os:275-284 (без зависимостей от провайдера/процессоров SDK); src/Трассировка/Классы/ОтелТрассировщик.os:268-270 (используется в API-режиме без SDK); src/Пропагация/Классы/ОтелW3CПропагатор.os:165` |  |
| 111 | SHOULD NOT | ✅ found | This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable. | `src/Трассировка/Модули/ОтелСпаны.os:15-20 (кэш НевалидныйСпан не экспортируется), 36-59 (функции модуля без точек расширения и регистрации реализаций)` |  |

#### SpanKind

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#spankind)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 112 | SHOULD | ➖ n_a | In order for `SpanKind` to be meaningful, callers SHOULD arrange that a single Span does not serve more than one purpose. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Субъект требования - callers: не совмещать в одном Span несколько ролей. Со своей стороны SDK дает все пять видов SpanKind (ОтелВидСпана.os:9-52: Внутренний, Сервер, Клиент, Производитель, Потребитель; по умолчанию Внутренний - ОтелСпан.os:775-781), чтобы вызывающий код мог следовать рекомендации. |
| 113 | SHOULD NOT | ➖ n_a | For example, a server-side span SHOULD NOT be used to describe outgoing remote procedure call. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Это пример к предыдущей рекомендации для инструментирующего кода: для исходящего RPC создается отдельный CLIENT-спан (ОтелВидСпана.Клиент()); SDK не может запретить описывать исходящий вызов SERVER-спаном. |

#### Link

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#link)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 114 | MUST | ✅ found | A user MUST have the ability to record links to other `SpanContext`s. | `src/Трассировка/Классы/ОтелСпан.os:433-463 (ДобавитьЛинк); src/Трассировка/Классы/ОтелПостроительСпана.os:97-100; src/Трассировка/Классы/ОтелТрассировщик.os:71-76 (параметр Линки при создании спана)` |  |
| 115 | MUST | ✅ found | The API MUST provide: An API to record a single `Link` where the `Link` properties are passed as arguments. | `src/Трассировка/Классы/ОтелСпан.os:420-433 (ДобавитьЛинк(НовыйКонтекстСпана, НовыеАтрибуты = Неопределено))` |  |
| 116 | SHOULD | ✅ found | Implementations SHOULD record links containing `SpanContext` with empty `TraceId` or `SpanId` (all zeros) as long as either the attribute set or `TraceState` is non-empty. | `src/Трассировка/Классы/ОтелСпан.os:438-452,597-612,623-626,669-671` |  |
| 117 | SHOULD | ✅ found | Span SHOULD preserve the order in which `Link`s are set. | `src/Трассировка/Классы/ОтелСпан.os:199-201,597-612 (Линки.Добавить в конец массива),900-904; src/Трассировка/Классы/ОтелПостроительСпана.os:97-100` |  |
| 118 | MUST | ✅ found | The API documentation MUST state that adding links at span creation is preferred to calling `AddLink` later, for contexts that are available during span creation, because head sampling decisions can o... | `src/Трассировка/Классы/ОтелСпан.os:420-424; src/Трассировка/Классы/ОтелПостроительСпана.os:85-88; docs/api/Трассировка/ОтелСпан.md:171-176; docs/api/Трассировка/ОтелПостроительСпана.md:74-78` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 119 | MUST | ✅ found | TracerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:7,13-19,93-105` |  |
| 120 | MUST | ✅ found | Tracer - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелТрассировщик.os:3-4; docs/api/Трассировка/ОтелТрассировщик.md:7,11` |  |
| 121 | MUST | ✅ found | Span - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСпан.os:5-6,38-44` |  |
| 122 | MUST | ✅ found | Event - Events are immutable and MUST be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелСобытиеСпана.os:3,18-66,72-74,90-118; src/Трассировка/Классы/ОтелСпан.os:362-363 (событие получает собственную копию атрибутов)` |  |
| 123 | SHOULD | ✅ found | Link - Links are immutable and SHOULD be safe for concurrent use by default. | `src/Трассировка/Классы/ОтелЛинк.os:1-13,28-54,67-71; src/Трассировка/Классы/ОтелСпан.os:447-451 (линк спана получает собственную копию атрибутов)` |  |

#### Behavior of the API in the absence of an installed SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/api/#behavior-of-the-api-in-the-absence-of-an-installed-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 124 | MUST | ✅ found | The API MUST return a non-recording `Span` with the `SpanContext` in the parent `Context` (whether explicitly given or implicit current). | `src/Трассировка/Классы/ОтелТрассировщик.os:71-76,121-126,158-172,268-270; src/Ядро/Модули/ОтелГлобальный.os:129-138,254-261; src/Трассировка/Модули/ОтелСпаны.os:36-44` |  |
| 125 | SHOULD | ✅ found | If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly without instantiating a new `Span`. | `src/Трассировка/Классы/ОтелТрассировщик.os:167-170` |  |
| 126 | MUST | ✅ found | If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.e., having a `SpanContext` with all-zero Span and Trace IDs, empty Tracestate, and unsampled TraceFl... | `src/Трассировка/Классы/ОтелТрассировщик.os:161-171,268-270; src/Трассировка/Модули/ОтелСпаны.os:36-39,54-59; src/Трассировка/Классы/ОтелНезаписывающийСпан.os:279-282` |  |

### Trace Sdk

#### Tracer Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#tracer-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ➖ n_a | It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` (see API). | `src/Трассировка/Классы/ОтелТрассировщик.os:337-341; src/Трассировка/Классы/ОтелПровайдерТрассировки.os:51-53,67-107` | OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os:786-791) и docs/spec-compliance.md. ПриСозданииОбъекта класса ОтелТрассировщик (ОтелТрассировщик.os:337-341) всегда публичен, поэтому запретить прямой вызов «Новый ОтелТрассировщик(...)» средствами языка невозможно. Внутри SDK трассировщики создаются только в ОтелПровайдерТрассировки.ПолучитьТрассировщик() (ОтелПровайдерТрассировки.os:67-107) и через ПостроительТрассировщика().Построить(), который делегирует в ПолучитьТрассировщик() (ОтелПостроительТрассировщика.os:62-64). |
| 2 | MUST | ✅ found | The `TracerProvider` MUST implement the Get a Tracer API. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:51-53,67-107; src/Трассировка/Классы/ОтелПостроительТрассировщика.os:26-64` |  |
| 3 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Tracer`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:80-81,86,98; src/Трассировка/Классы/ОтелТрассировщик.os:137-139,337-341; src/Ядро/Классы/ОтелОбластьИнструментирования.os:164-169` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | Configuration ( i.e., SpanProcessors, IdGenerator, SpanLimits, `Sampler`, and (Development) TracerConfigurator) MUST be owned by the `TracerProvider`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:9-37,204-251,291-326,402-437; src/Трассировка/Классы/ОтелТрассировщик.os:6-11,230-251,369-374` |  |
| 5 | MUST | ✅ found | If configuration is updated (e.g., adding a `SpanProcessor`), the updated configuration MUST also apply to all already returned `Tracers` (i.e. it MUST NOT matter whether a `Tracer` was obtained from ... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:114-116,204-206; src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:62-73; src/Трассировка/Классы/ОтелТрассировщик.os:50-52,230-251,369-374` |  |
| 6 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `SpanProcessor`), the updated configuration MUST also apply to all already returned `Tracers` (i.e. it MUST NOT matter whether a `Tracer` was obtained from ... | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:88-106,114-116; src/Трассировка/Классы/ОтелТрассировщик.os:6-11,50-52,191-193,246-251; tests/unit/Трассировка/ТестПровайдерТрассировки.os:351-371` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | `Shutdown` MUST be called only once for each `TracerProvider` instance. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:150-157; tests/unit/Трассировка/ТестПровайдерТрассировки.os:453-466` |  |
| 8 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op Tracer for these calls, if possible. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:82-87; src/Трассировка/Классы/ОтелТрассировщик.os:50-52,96-98,167-172,191-193,268-270` |  |
| 9 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:150-157,190-193; src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-40; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:215-236` |  |
| 10 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:150-157; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:52-76,159-177,192-202; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114; src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:96-104` |  |
| 11 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` within all internal processors. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:156,338-340; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:52-76,192-202` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:137-139,167-172,179-183; src/Ядро/Модули/ОтелРезультатыЭкспорта.os:84-92; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:215-236` |  |
| 13 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:137-139,167-172,350-352; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:69-76,159-177; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-252; src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120` |  |
| 14 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered `SpanProcessors`. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:338-340,350-352; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:69-76,192-202` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | `Enabled` MUST return `false` when either: | `src/Трассировка/Классы/ОтелТрассировщик.os:50-52; src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:51-53; tests/unit/Трассировка/ТестПровайдерТрассировки.os:351-371` |  |
| 16 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:50-52,191-193; src/Трассировка/Классы/ОтелПровайдерТрассировки.os:270-272` |  |

#### Additional Span Interfaces

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#additional-span-interfaces)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 17 | MUST | ✅ found | Readable span: A function receiving this as argument MUST be able to access all information that was added to the span, as listed in the API spec for Span. | `src/Трассировка/Классы/ОтелСпан.os:88-259,294-296; src/Трассировка/Классы/ОтелСобытиеСпана.os:23-50; src/Трассировка/Классы/ОтелЛинк.os:33-52` |  |
| 18 | MUST | ✅ found | A function receiving this as argument MUST be able to access the `InstrumentationScope` [since 1.10.0] and `Resource` information (implicitly) associated with the span. | `src/Трассировка/Классы/ОтелСпан.os:208-210,217-219` |  |
| 19 | MUST | ✅ found | For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated since 1.10.0] having the same name and version values as the `InstrumentationScope`. | `src/Трассировка/Классы/ОтелСпан.os:230-232; src/Ядро/Классы/ОтелОбластьИнструментирования.os:88-90` |  |
| 20 | MUST | ✅ found | A function receiving this as argument MUST be able to reliably determine whether the Span has ended (some languages might implement this by having an end timestamp of `null`, others might have an expl... | `src/Трассировка/Классы/ОтелСпан.os:257-259,526-544` |  |
| 21 | MUST | ✅ found | Counts for attributes, events and links dropped due to collection limits MUST be available for exporters to report as described in the exporters specification. | `src/Трассировка/Классы/ОтелСпан.os:266-286; src/Трассировка/Классы/ОтелСобытиеСпана.os:50; src/Трассировка/Классы/ОтелЛинк.os:52; src/Экспорт/Классы/ОтелЭкспортерСпанов.os:235,243,261,265` |  |
| 22 | MUST | ✅ found | As an exception to the authoritative set of span properties defined in the API spec, implementations MAY choose not to expose (and store) the full parent Context of the Span but they MUST expose at le... | `src/Трассировка/Классы/ОтелСпан.os:106-120` |  |
| 23 | MUST | ✅ found | It MUST be possible for functions being called with this to somehow obtain the same `Span` instance and type that the span creation API returned (or will return) to the user (for example, the `Span` c... | `src/Трассировка/Классы/ОтелСпан.os:541-543,903-905; src/Трассировка/Классы/ОтелТрассировщик.os:246-253; src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11-20` |  |

#### Sampling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | Span Processor MUST receive only those spans which have this field set to `true`. | `src/Трассировка/Классы/ОтелТрассировщик.os:167-172,237-242,283-294; src/Трассировка/Классы/ОтелСпан.os:294-296,903-905; src/Трассировка/Классы/ОтелНезаписывающийСпан.os:155-157,252-254` |  |
| 25 | SHOULD NOT | ✅ found | However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:51-53,123-131; src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:32-37,43-51` |  |
| 26 | MUST | ✅ found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:47-66; src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:32-37; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-69,263-279; src/Трассировка/Классы/ОтелТрассировщик.os:393-405` |  |
| 27 | SHOULD NOT | ✅ found | Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT receive the ones that do not. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:51-53,123-131; src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:32-37,43-51` |  |
| 28 | MUST NOT | ✅ found | The flag combination `SampledFlag == true` and `IsRecording == false` could cause gaps in the distributed trace, and because of this the OpenTelemetry SDK MUST NOT allow this combination. | `src/Трассировка/Классы/ОтелТрассировщик.os:240-252,283-294,393-405; src/Трассировка/Классы/ОтелНезаписывающийСпан.os:155-157` |  |

#### SDK Span creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#sdk-span-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | MUST | ✅ found | When asked to create a Span, the SDK MUST act as if doing the following in order: | `src/Трассировка/Классы/ОтелТрассировщик.os:216-254,283-294,362-379,393-405; src/Трассировка/Классы/ОтелСпан.os:545,907` |  |

#### ShouldSample

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shouldsample)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | If the parent `SpanContext` contains a valid `TraceId`, they MUST always match. | `src/Трассировка/Классы/ОтелТрассировщик.os:218-225,237-239,369-374` |  |
| 31 | MUST NOT | ✅ found | `RECORD_ONLY` - `IsRecording` will be `true`, but the `Sampled` flag MUST NOT be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:244-252,393-405; src/Трассировка/Классы/ОтелСпан.os:294-296` |  |
| 32 | MUST | ✅ found | `RECORD_AND_SAMPLE` - `IsRecording` will be `true` and the `Sampled` flag MUST be set. | `src/Трассировка/Классы/ОтелТрассировщик.os:244-252,395-398; src/Трассировка/Классы/ОтелСпан.os:294-296` |  |
| 33 | SHOULD | ✅ found | If the sampler returns an empty `Tracestate` here, the `Tracestate` will be cleared, so samplers SHOULD normally return the passed-in `Tracestate` if they do not intend to change it. | `src/Трассировка/Модули/ОтелСэмплер.os:163-185; src/Трассировка/Классы/ОтелТрассировщик.os:228,237-239` |  |

#### GetDescription

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#getdescription)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | SHOULD NOT | ➖ n_a | Callers SHOULD NOT cache the returned value. | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. Внутри самого SDK кеширования нет: ОтелСэмплер.Описание (src/Трассировка/Модули/ОтелСэмплер.os:119-140) формирует строку при каждом вызове, в том числе описание делегата для ParentBased/AlwaysRecord (строки 131, 136); других вызовов Описание сэмплера в src нет. |

#### AlwaysOn

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwayson)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | MUST | ✅ found | Description MUST be `AlwaysOnSampler`. | `src/Трассировка/Модули/ОтелСэмплер.os:119-122` |  |

#### AlwaysOff

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwaysoff)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | Description MUST be `AlwaysOffSampler`. | `src/Трассировка/Модули/ОтелСэмплер.os:119,123-124` |  |

#### TraceIdRatioBased

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#traceidratiobased)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 37 | MUST | ✅ found | The `TraceIdRatioBased` MUST ignore the parent `SampledFlag`. | `src/Трассировка/Модули/ОтелСэмплер.os:283-284,372-391` |  |
| 38 | MUST | ✅ found | Description MUST return a string of the form `"TraceIdRatioBased{RATIO}"` with `RATIO` replaced with the Sampler instance’s trace sampling ratio represented as a decimal number. | `src/Трассировка/Модули/ОтелСэмплер.os:119,125-126,245-250` |  |
| 39 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:245-250` |  |
| 40 | SHOULD | ✅ found | The precision of the number SHOULD follow implementation language standards and SHOULD be high enough to identify when Samplers have different ratios. | `src/Трассировка/Модули/ОтелСэмплер.os:245-250` |  |

#### Requirements for `TraceIdRatioBased` sampler algorithm

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#requirements-for-traceidratiobased-sampler-algorithm)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 41 | MUST | ✅ found | The sampling algorithm MUST be deterministic. | `src/Трассировка/Модули/ОтелСэмплер.os:372-391,404-410` |  |
| 42 | MUST | ✅ found | To achieve this, implementations MUST use a deterministic hash of the `TraceId` when computing the sampling decision. | `src/Трассировка/Модули/ОтелСэмплер.os:385-386,464-465; src/Ядро/Модули/ОтелУтилиты.os:212-231` |  |
| 43 | MUST | ✅ found | A `TraceIdRatioBased` sampler with a given sampling probability MUST also sample all traces that any `TraceIdRatioBased` sampler with a lower sampling probability would sample. | `src/Трассировка/Модули/ОтелСэмплер.os:372-379,393-410` |  |

#### AlwaysRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#alwaysrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 44 | MUST | ✅ found | Based on the decision from the wrapped root sampler, `AlwaysRecord` MUST behave as follows: | `src/Трассировка/Модули/ОтелСэмплер.os:105-107,285-290,310-327` |  |

#### Span Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST | ✅ found | Span attributes MUST adhere to the common rules of attribute limits. | `src/Трассировка/Классы/ОтелСпан.os:328-343 (УстановитьАтрибут: лимиты длины и глубины значения через ОтелУтилиты.ОграничитьЗначениеАтрибута), 556-567 (ЗаписатьАтрибут: новый ключ сверх МаксАтрибутов отбрасывается со счетчиком, перезапись существующего ключа разрешена); src/Ядро/Модули/ОтелУтилиты.os:385-387,556-603 (усечение строк по символам, двоичных данных по байтам, рекурсивно для элементов массивов; прочие значения не усекаются); src/Трассировка/Классы/ОтелЛимитыСпана.os:269-277 (AttributeCountLimit=128, AttributeValueLengthLimit=без ограничения); src/Конфигурация/Модули/ОтелАвтоконфигурация.os:509-519 (OTEL_SPAN_ATTRIBUTE_* перекрывают общие OTEL_ATTRIBUTE_*)` |  |
| 46 | MUST | ✅ found | If the SDK implements the limits above it MUST provide a way to change these limits, via a configuration to the TracerProvider, by allowing users to configure individual limits like in the Java exampl... | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:76-79 (УстановитьЛимитыСпана, аналог SdkTracerProviderBuilder.setSpanLimits); src/Трассировка/Классы/ОтелПровайдерТрассировки.os:408,434 (параметр ЛимитыСпана конструктора провайдера); src/Трассировка/Классы/ОтелЛимитыСпана.os:125-245 (отдельный fluent-сеттер для каждого лимита); src/Трассировка/Классы/ОтелТрассировщик.os:249 (лимиты провайдера передаются каждому создаваемому спану)` |  |
| 47 | SHOULD | ✅ found | The name of the configuration options SHOULD be `EventCountLimit` and `LinkCountLimit`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:103-105,113-115 (КоличествоСобытийЛимит = EventCountLimit, КоличествоСсылокЛимит = LinkCountLimit), 138-141,151-154 (УстановитьКоличествоСобытийЛимит / УстановитьКоличествоСсылокЛимит); src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:244,249 (event_count_limit, link_count_limit); src/Конфигурация/Модули/ОтелАвтоконфигурация.os:521-528 (otel.span.event.count.limit, otel.span.link.count.limit)` |  |
| 48 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `SpanLimits`. | `src/Трассировка/Классы/ОтелЛимитыСпана.os:251-277 (класс ОтелЛимитыСпана = SpanLimits, аналог io.opentelemetry.sdk.trace.SpanLimits); lib.config:31` |  |
| 49 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK’s log to indicate to the user that an attribute, event, or link was discarded due to such a limit. | `src/Трассировка/Классы/ОтелСпан.os:628-633 (ВывестиПредупреждениеОбОтброшенныхДанных: Лог.Предупреждение о данных, отброшенных из-за лимитов); вызовы при отбрасывании атрибута :563, события :585, линка :600, атрибутов события/линка :581,606` |  |
| 50 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per span (i.e., not per discarded attribute, event, or link). | `src/Трассировка/Классы/ОтелСпан.os:74-75,869 (флаг ПредупреждениеОтброшенныхВыведено на каждый спан), 628-633 (сообщение выводится только при флаге Ложь, после чего флаг взводится; вызов идет под Блокировка спана)` |  |

#### ID Generators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#id-generators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 51 | MUST | ✅ found | The SDK MUST by default randomly generate both the `TraceId` and the `SpanId`. | `src/Ядро/Модули/ОтелУтилиты.os:96-116,126-147 (по умолчанию TraceId и SpanId берутся из случайного UUIDv4 - Новый УникальныйИдентификатор, с повтором при нулевом значении); src/Трассировка/Классы/ОтелПровайдерТрассировки.os:291-326 (без пользовательского генератора делегирует в ОтелУтилиты); src/Трассировка/Классы/ОтелТрассировщик.os:230,235` |  |
| 52 | MUST | ✅ found | The SDK MUST provide a mechanism for customizing the way IDs are generated for both the `TraceId` and the `SpanId`. | `src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:81-98 (УстановитьГенераторИд, аналог SdkTracerProviderBuilder.setIdGenerator); src/Трассировка/Классы/ОтелПровайдерТрассировки.os:291-326,402-410 (ГенераторИд провайдера генерирует TraceId и SpanId, некорректный результат заменяется генератором по умолчанию); src/Ядро/Модули/ОтелУтилиты.os:74-76 (глобальный УстановитьГенераторИд)` |  |
| 53 | MUST | ✅ found | The SDK MAY provide this functionality by allowing custom implementations of an interface like the Java example below (name of the interface MAY be `IdGenerator`, name of the methods MUST be consisten... | `src/Трассировка/Классы/ОтелКонтекстСпана.os:23,32 (SpanContext: ИдТрассировки()/ИдСпана()); src/Трассировка/Классы/ОтелПровайдерТрассировки.os:295,317 (методы генератора СгенерироватьИдТрассировки()/СгенерироватьИдСпана() согласованы с именами SpanContext); src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:81-87` |  |
| 54 | MUST NOT | ✅ found | Additional `IdGenerator` implementing vendor-specific protocols such as AWS X-Ray trace ID generator MUST NOT be maintained or distributed as part of the OpenTelemetry Core packages. | `src/Ядро/Модули/ОтелУтилиты.os:96-147 (в пакете есть только генератор по умолчанию на основе UUID); lib.config (нет классов vendor-specific генераторов; AWS X-Ray и подобные в src/ отсутствуют)` |  |

#### Span processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | MUST | ✅ found | SDK MUST allow to end each pipeline with individual exporter. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:143-148 (каждый процессор получает собственный Экспортер); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:429-438; src/Трассировка/Классы/ОтелПровайдерТрассировки.os:114-116, src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:44-47 (регистрация нескольких конвейеров процессор+экспортер)` |  |
| 56 | MUST | ✅ found | SDK MUST allow users to implement and configure custom processors. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:1-55 (&Интерфейс для пользовательских процессоров); src/Трассировка/Классы/ОтелПровайдерТрассировки.os:114-116; src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:44-47 (ДобавитьПроцессор принимает любой объект-процессор); src/Ядро/Модули/ОтелРезультатыЗакрытия.os:135-147 (Закрыть/СброситьБуфер пользовательского процессора вызываются с учетом числа его параметров)` |  |

#### Interface definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 57 | MUST | ✅ found | The `SpanProcessor` interface MUST declare the following methods: | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:11 (ПриНачале = OnStart), 19 (ПриЗавершении = OnEnd), 30 (СброситьБуфер = ForceFlush), 43 (Закрыть = Shutdown)` |  |

#### OnStart

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onstart)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 58 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ОтелСпан.os:903-905 (в ПриНачале передается сам изменяемый объект спана ЭтотОбъект по ссылке - процессор может сохранить ссылку); src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:5-12` |  |
| 59 | SHOULD | ✅ found | It SHOULD be possible to keep a reference to this span object and updates to the span SHOULD be reflected in it. | `src/Трассировка/Классы/ОтелСпан.os:307-343,358-373,496-515 (изменения имени, атрибутов, событий, статуса пишутся в тот же объект), 88-90,168-181,239-250 (геттеры читают текущее состояние спана)` |  |

#### OnEnd(Span)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#onendspan)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | MUST | ✅ found | This method MUST be called synchronously within the `Span.End()` API, therefore it should not block or throw an exception. | `src/Трассировка/Классы/ОтелСпан.os:526-544 (Завершить устанавливает ВремяОкончания и синхронно вызывает Процессор.ПриЗавершении(ЭтотОбъект) на строках 541-543); src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:36-44 (исключения процессоров перехватываются); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-69 (пакетный процессор только кладет спан в буфер)` |  |

#### Shutdown()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `SpanProcessor` instance. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:150-157 (CAS по Закрыт: Закрыть процессоров вызывается только при первом Shutdown провайдера); src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:96-99; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-100 (повторный Закрыть не выполняет закрытие повторно)` |  |
| 62 | SHOULD | ✅ found | SDKs SHOULD ignore these calls gracefully, if possible. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:25-27 (ПриНачале - no-op), 47-50 (ПриЗавершении после Закрыть игнорируется); src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:20-22; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-51 (Обработать после Закрыть игнорируется), 124-127 (ПринудительноВыгрузитьСРезультатом после закрытия возвращает результат без исключения); СброситьБуфер после закрытия работает с пустым буфером без исключений` |  |
| 63 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:34-45; src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:86-104; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:83-114 (Закрыть возвращает ОтелРезультатЗакрытия); src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-38 (Успешно/ИстекТаймаут/Описание)` |  |
| 64 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:103 -> src/Ядро/Модули/ОтелРезультатыЗакрытия.os:110-121,89-95 (дождаться текущего экспорта, СброситьБуфер экспортера, затем Закрыть); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:104-106 (тот же ЭкспортироватьВсеПакеты, что и СброситьБуфер на строке 80), 110-112 (затем Экспортер.Закрыть)` |  |
| 65 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114 (Закрыть(ТаймаутМс = 30000): ОставшеесяВремя/СрокИстек ограничивают ожидание фонового задания, финальный экспорт и закрытие экспортера, итог - Таймаут); src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:96-104 -> src/Ядро/Модули/ОтелРезультатыЗакрытия.os:110-121; src/Ядро/Классы/ОтелБлокировкаСТаймаутом.os:20-30 (ожидание блокировки экспорта ограничено сроком)` |  |

#### ForceFlush()

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 66 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `Spans` for which the `SpanProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as possible, pre... | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217 (экспорт буфера до опустошения до возврата), 231-252 (ожидание экспорта, начатого фоновым заданием, через БлокировкаЭкспорта); src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:79-84 -> src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120 (дожидается экспорта в другом потоке)` |  |
| 67 | SHOULD | ✅ found | In particular, if any `SpanProcessor` has any associated exporter, it SHOULD try to call the exporter’s `Export` with all spans for which this was not already done and then invoke `ForceFlush` on it. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-217 (Export для всех неэкспортированных спанов, затем Экспортер.СброситьБуфер на строках 211-214); src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120 (простой процессор после текущего экспорта вызывает Экспортер.СброситьБуфер)` |  |
| 68 | MUST | ✅ found | The built-in SpanProcessors MUST do so. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:79-84; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217` |  |
| 69 | MUST | ✅ found | If a timeout is specified (see below), the SpanProcessor MUST prioritize honoring the timeout over finishing all calls. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-252 (срок проверяется перед каждым пакетом, оставшиеся пакеты пропускаются с результатом Таймаут; остаток срока передается в захват блокировки, Export и СброситьБуфер экспортера); src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120; src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:93-112` |  |
| 70 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Трассировка/Классы/ИнтерфейсПроцессорСпанов.os:22-32; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71-81,191-217 (СброситьБуфер возвращает ОтелРезультатЭкспорта); src/Ядро/Классы/ОтелРезультатЭкспорта.os:17-36 (Успешно/ИстекТаймаут/Статус); src/Ядро/Модули/ОтелРезультатыЭкспорта.os:18-39` |  |
| 71 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `SpanProcessor` ex... | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение |
| 72 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81,191-217 (СброситьБуфер(ТаймаутМс) прерывается с результатом Таймаут при истечении срока); src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120; src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:93-112` |  |

#### Built-in span processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#built-in-span-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:143-148 (SimpleSpanProcessor, &Реализует ИнтерфейсПроцессорСпанов); src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:60-63 (BatchSpanProcessor, &Расширяет ОтелБазовыйПакетныйПроцессор); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:429-450` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 74 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:57-64 (БлокировкаЭкспорта.Захватить()/Освободить() вокруг Экспортер.Экспортировать), 146 (Новый ОтелБлокировкаСТаймаутом); src/Ядро/Классы/ОтелБлокировкаСТаймаутом.os:20-36 (взаимоисключение через АтомарноеБулево.СравнитьИУстановить)` |  |

#### Batching processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#batching-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 75 | MUST | ✅ found | The processor MUST synchronize calls to `Span Exporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:231-252 (ЭкспортироватьПакет: извлечение пакета и Export под БлокировкаЭкспорта, стр. 234/250), 263-279 (единственный вызов Экспортер.Экспортировать, стр. 273), 445; src/Трассировка/Классы/ОтелПакетныйПроцессорСпанов.os:36,60-61 (использует базовый процессор через extends)` |  |
| 76 | SHOULD | ✅ found | The processor SHOULD export a batch when any of the following happens AND the previous export call has returned: | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:66-68 (фоновый экспорт стартует с первым спаном), 168-174 (интервал scheduledDelayMillis отсчитывается заново после каждого экспорта), 351-368 (триггер по истечении интервала или при maxExportBatchSize спанов в очереди), 79-81 (триггер ForceFlush), 234 (БлокировкаЭкспорта - новый экспорт только после возврата предыдущего), 431-434 (умолчания 2048/512/5000/30000); src/Конфигурация/Модули/ОтелАвтоконфигурация.os:792 (ЗапуститьФоновыйЭкспорт сразу после создания)` |  |

#### Span Exporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-exporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 77 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:7-8 (Export и Shutdown/ForceFlush могут вызываться конкурентно, реализация MUST быть безопасна для параллельного вызова); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:12-13 и src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:8 (Export не вызывается конкурентно); docs/architecture.md:298; docs/api/Экспорт/ОтелЭкспортерСпанов.md:16-18` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | MUST | ✅ found | The exporter MUST support three functions: Export, Shutdown, and ForceFlush. | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:14,26,35 (Экспортировать, СброситьБуфер, Закрыть); src/Экспорт/Классы/ОтелЭкспортерСпанов.os:33,63,73,121` |  |

#### `Export(batch)`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 79 | MUST NOT | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:33-52 (отправка в Обещании, ожидание Обещание.Получить(ТаймаутОперацииМс)), 122,126 (таймаут по умолчанию 10000 мс); src/Экспорт/Классы/ОтелHttpТранспорт.os:171 и src/Экспорт/Классы/ОтелGrpcТранспорт.os:169 (сетевой таймаут каждой попытки)` |  |
| 80 | MUST | ✅ found | Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:42,47-51 (по истечении ТаймаутОперацииМс возвращается Ложь = Failure), 122,126 (верхний предел по умолчанию 10000 мс); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:272-277 (передает exportTimeoutMillis в Export, Ложь трактуется как Failure)` |  |
| 81 | SHOULD NOT | ✅ found | The default SDK’s Span Processors SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the spans are being sent to. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:47-66 (однократный вызов Export без повтора); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:263-279 (неудачный пакет логируется и отбрасывается, в буфер не возвращается); повтор реализован в протокол-специфичных транспортах: src/Экспорт/Классы/ОтелHttpТранспорт.os:124,182,351-354; src/Экспорт/Классы/ОтелGrpcТранспорт.os:119,257` |  |

#### `ForceFlush()`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 82 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Spans` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this metho... | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:33-52 (Export синхронный, без внутреннего буфера: полученные спаны отправлены до возврата Export), 63-66 (СброситьБуфер - нечего досылать, немедленный успех); src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120 и src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-217 (процессоры вызывают ForceFlush экспортера после завершения текущего Export)` |  |
| 83 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:18-28 (СброситьБуфер возвращает ОтелРезультатЭкспорта); src/Экспорт/Классы/ОтелЭкспортерСпанов.os:63-66; src/Ядро/Классы/ОтелРезультатЭкспорта.os:17-38 (Успешно, ИстекТаймаут, Статус: 0 успех / 1 ошибка / 2 таймаут)` |  |
| 84 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports t... | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение. |
| 85 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ИнтерфейсЭкспортерСпанов.os:26 (СброситьБуфер(ТаймаутМс = 0)); src/Экспорт/Классы/ОтелЭкспортерСпанов.os:63-66 (принимает таймаут, завершается немедленно); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:211-214 и src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120 (процессоры передают оставшееся время срока)` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/trace/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 86 | MUST | ✅ found | Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПровайдерТрассировки.os:67-107 (ПолучитьТрассировщик: СинхронизированнаяКарта + двойная проверка под БлокировкаРесурса), 137-139,338-352 (СброситьБуфер по снимку-копии списка процессоров), 150-157 (Закрыть: АтомарноеБулево.СравнитьИУстановить), 423-425; src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:62-82 (копирование при записи); tests/unit/Трассировка/ТестПровайдерТрассировкиКонкурентность.os:17` |  |
| 87 | MUST | ✅ found | Sampler - `ShouldSample` and `GetDescription` MUST be safe to be called concurrently. | `src/Трассировка/Модули/ОтелСэмплер.os:163-185 (ДолженСэмплировать - чистая функция от аргументов), 119-140 (Описание - чистая функция), 443-452 (переменные модуля - константы, задаются один раз при загрузке и далее только читаются)` |  |
| 88 | MUST | ✅ found | Span processor - all methods MUST be safe to be called concurrently. | `src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:47-104 (АтомарноеБулево Закрыт, ОтелБлокировкаСТаймаутом вокруг Export/ForceFlush/Shutdown); src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-69 (буфер под БлокировкаРесурса), 95-114 (CAS при Закрыть), 154-161 (CAS запуска фонового экспорта), 231-252, 297-328; src/Трассировка/Классы/ОтелКомпозитныйПроцессорСпанов.os:3-5,62-82; tests/unit/Экспорт/ТестБазовыйПакетныйПроцессор.os:17,266,288,492` |  |
| 89 | MUST | ✅ found | Span Exporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерСпанов.os:7-8,12-13 (признак Закрыт - АтомарноеБулево), 63-66 (СброситьБуфер без состояния), 73-76 (Закрыть - атомарная запись АтомарноеБулево.Установить)` |  |

### Logs Api

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `LoggerProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:147,157` |  |

#### LoggerProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#loggerprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `LoggerProvider` MUST provide the following functions: | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:58` |  |

#### Get a Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#get-a-logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following instrumentation scope parameters: | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:58-62; src/Логирование/Классы/ОтелПостроительЛоггера.os:26,39,52` |  |
| 4 | MUST | ✅ found | This API MUST be structured to accept a variable number of attributes, including none. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:61; src/Ядро/Классы/ОтелАтрибуты.os:19` |  |

#### Logger

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#logger)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | The `Logger` MUST provide a function to: | `src/Логирование/Классы/ОтелЛоггер.os:98` |  |
| 6 | SHOULD | ✅ found | The `Logger` SHOULD provide functions to: | `src/Логирование/Классы/ОтелЛоггер.os:57` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | The API MUST accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:19,98; src/Логирование/Классы/ОтелЗаписьЛога.os:186,203,220,237,313,329,345` |  |
| 8 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:98` |  |
| 9 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:103-106,123` |  |
| 10 | SHOULD | ✅ found | When only explicit Context is supported, this parameter SHOULD be required. | `src/Логирование/Классы/ОтелЛоггер.os:98,103-106; src/Ядро/Модули/ОтелКонтекст.os:58` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when generating a `LogRecord`, a `Logger` SHOULD provide this `Enabled` API. | `src/Логирование/Классы/ОтелЛоггер.os:57-84` |  |
| 12 | SHOULD | ✅ found | The API SHOULD accept the following parameters: | `src/Логирование/Классы/ОтелЛоггер.os:57-61` |  |
| 13 | SHOULD | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:58` |  |
| 14 | MUST | ✅ found | When implicit Context is supported, then this parameter SHOULD be optional and if unspecified then MUST use current Context. | `src/Логирование/Классы/ОтелЛоггер.os:72,82-83` |  |
| 15 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Логирование/Классы/ОтелЛоггер.os:53-54,63-83; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:84-101` |  |
| 16 | SHOULD | ✅ found | The API documentation SHOULD state that calling `Enabled` is optional and is not required before emitting a `LogRecord`. | `src/Логирование/Классы/ОтелЛоггер.os:27-31` |  |
| 17 | SHOULD | ✅ found | The documentation SHOULD also state that the returned value is not static and can change over time, so a cached value can become stale. | `src/Логирование/Классы/ОтелЛоггер.os:34-35` |  |

#### Optional and required parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#optional-and-required-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 18 | MUST | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:58-62; src/Логирование/Классы/ОтелЛоггер.os:57-61,98; src/Логирование/Классы/ОтелЗаписьЛога.os:186-368` |  |
| 19 | MUST NOT | ✅ found | For each optional parameter, the API MUST be structured to accept it, but MUST NOT obligate a user to provide it. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:60-62; src/Логирование/Классы/ОтелЛоггер.os:58-61,98; src/Логирование/Классы/ОтелЗаписьЛога.os:423-449` |  |
| 20 | MUST | ✅ found | For each required parameter, the API MUST be structured to obligate a user to provide it. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:38,59; src/Ядро/Модули/ОтелГлобальный.os:95` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | LoggerProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:7` |  |
| 22 | MUST | ✅ found | Logger - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Логирование/Классы/ОтелЛоггер.os:245,32,89` |  |

### Logs Sdk

#### Logs SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logs-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:259-278; src/Логирование/Классы/ОтелЛоггер.os:98-128; lib.config:51-62` |  |

#### LoggerProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A `LoggerProvider` MUST provide a way to allow a Resource to be specified. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:259-268; src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:22-25,60-66` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the `LogRecord`s produced by any `Logger` from the `LoggerProvider`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:68-72,85; src/Логирование/Классы/ОтелЛоггер.os:98-100,254-258` |  |

#### LoggerProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `LoggerProviders`s. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:9-23,259-278` |  |

#### Logger Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logger-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | SHOULD | ➖ n_a | It SHOULD only be possible to create `Logger` instances through a `LoggerProvider` (see API). | `src/Логирование/Классы/ОтелЛоггер.os:241-258; src/Логирование/Классы/ОтелПровайдерЛогирования.os:38-40,58-94; src/Логирование/Классы/ОтелПостроительЛоггера.os:62-64` | OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. ПриСозданииОбъекта класса ОтелЛоггер (ОтелЛоггер.os:254-258) всегда публичен, поэтому прямой вызов Новый ОтелЛоггер(...) в обход LoggerProvider запретить средствами языка невозможно. Штатный и документированный путь создания логгера - ОтелПровайдерЛогирования.ПолучитьЛоггер() и ПостроительЛоггера().Построить(), который делегирует в ПолучитьЛоггер(); класс задокументирован комментарием «Получается из ОтелПровайдерЛогирования» (ОтелЛоггер.os:241-245). |
| 6 | MUST | ✅ found | The `LoggerProvider` MUST implement the Get a Logger API. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:29-40,42-94; src/Логирование/Классы/ОтелПостроительЛоггера.os:18-64` |  |
| 7 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Logger`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:73-74,85; src/Логирование/Классы/ОтелЛоггер.os:139-141,229-231,254-258; src/Ядро/Классы/ОтелОбластьИнструментирования.os:164-169; tests/unit/Логирование/ТестПровайдерЛогирования.os:74-94` |  |
| 8 | MUST | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep t... | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:63-67,73-93; src/Ядро/Классы/ОтелОбластьИнструментирования.os:61-79; tests/unit/Логирование/ТестПровайдерЛогирования.os:322-338,375-391` |  |
| 9 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep t... | `src/Ядро/Классы/ОтелОбластьИнструментирования.os:53-56,164-169; src/Логирование/Классы/ОтелПровайдерЛогирования.os:73-74` |  |
| 10 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working `Logger` MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep t... | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:63-67` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | Configuration ( i.e. LogRecordProcessors and (Development) LoggerConfigurator) MUST be owned by the `LoggerProvider`. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:11-12,20-21,96-103,269-273; src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:36-39,60-66` |  |
| 12 | MUST | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained ... | `src/Логирование/Классы/ОтелЛоггер.os:7-8,19-24,76-83,122-124; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:40-58; tests/unit/Логирование/ТестЛоггер.os:240-268` |  |
| 13 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated configuration MUST also apply to all already returned `Logger`s (i.e. it MUST NOT matter whether a `Logger` was obtained ... | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:75-93,191-198; src/Логирование/Классы/ОтелЛоггер.os:63-83,122-124; tests/unit/Логирование/ТестЛоггер.os:240-268; tests/unit/Логирование/ТестПровайдерЛогирования.os:51-71` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | `Shutdown` MUST be called only once for each `LoggerProvider` instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:138-141; tests/unit/Логирование/ТестПровайдерЛогирования.os:341-372` |  |
| 15 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op `Logger` for these calls, if possible. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:42-47,68-72; src/Логирование/Классы/ОтелЛоггер.os:63-68,122-124; tests/unit/Логирование/ТестПровайдерЛогирования.os:155-173` |  |
| 16 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:128-146,182-185; src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-40; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:215-236; tests/unit/Логирование/ТестПровайдерЛогирования.os:554-567` |  |
| 17 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:138-146; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:69-76,159-177,192-202; tests/unit/Логирование/ТестПровайдерЛогирования.os:500-515,570-584` |  |
| 18 | MUST | ✅ found | `Shutdown` MUST be implemented by invoking `Shutdown` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:142-145,227-229; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:52-54,69-76,192-202; tests/unit/Логирование/ТестПровайдерЛогирования.os:587-606` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:114-126,148-162,170-174; src/Ядро/Классы/ОтелРезультатЭкспорта.os:17-38; src/Ядро/Модули/ОтелРезультатыЭкспорта.os:84-92` |  |
| 20 | SHOULD | ✅ found | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model... | `src/Ядро/Модули/ОтелРезультатыЭкспорта.os:27-29,84-92; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:215-231; tests/unit/Логирование/ТестПровайдерЛогирования.os:484-497,535-548` |  |
| 21 | SHOULD | ✅ found | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it SHOULD return some NO ERROR status, language implementations MAY decide how to model... | `src/Ядро/Модули/ОтелРезультатыЭкспорта.os:18-20,84-87; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:232-235; tests/unit/Логирование/ТестПровайдерЛогирования.os:518-532` |  |
| 22 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:124-126,157-162,239-241; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:69-76,159-177; tests/unit/Логирование/ТестПровайдерЛогирования.os:634-645` |  |
| 23 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered LogRecordProcessors. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:124-126,239-241; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:69-76,192-202; tests/unit/Логирование/ТестПровайдерЛогирования.os:612-631` |  |

#### Emit a LogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#emit-a-logrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | SHOULD | ✅ found | If Observed Timestamp is unspecified, the implementation SHOULD set it equal to the current time. | `src/Логирование/Классы/ОтелЛоггер.os:117-120 (Записать: если ПустаяСтрока(ЗаписьЛога.ВремяНаблюдения()) - УстановитьВремяНаблюдения(ОтелУтилиты.ТекущееВремяВНаносекундах()), явно заданное значение не перезаписывается); подтверждено tests/unit/Логирование/ТестЛоггер.os:149-196 (ЗаписатьУстанавливаетObservedTimestamp, ЗаписатьСохраняетЯвноУстановленныйObservedTimestamp)` |  |
| 25 | MUST | ✅ found | If an Exception is provided, the SDK MUST by default set attributes from the exception on the `LogRecord` with the conventions outlined in the exception semantic conventions. | `src/Логирование/Классы/ОтелЛоггер.os:115,189-227 (Записать всегда вызывает ПрименитьАтрибутыИсключения: exception.message = Описание, exception.type = ИмяМодуля либо RuntimeError, exception.stacktrace = ПодробноеОписаниеОшибки(); тот же подход, что в ОтелСпан.ЗаписатьИсключение); src/Логирование/Классы/ОтелЗаписьЛога.os:362-377 (УстановитьИсключение / ИнформацияОбИсключении); подтверждено tests/unit/Логирование/ТестЛоггер.os:374-401,652-684` |  |
| 26 | MUST | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:194-206 (УстановитьАтрибутИсключенияЕслиНеЗадан: атрибут из исключения пишется только если ключ еще не задан пользователем); подтверждено tests/unit/Логирование/ТестЛоггер.os:403-432 (ЗаписатьАтрибутыПользователяПриоритетнееИсключения)` |  |
| 27 | MUST NOT | ✅ found | User-provided attributes MUST take precedence and MUST NOT be overwritten by exception-derived attributes. | `src/Логирование/Классы/ОтелЛоггер.os:202-206 (проверка ЗаписьЛога.Атрибуты().Получить(Ключ) = Неопределено перед установкой exception.*: пользовательское значение не перезаписывается); подтверждено tests/unit/Логирование/ТестЛоггер.os:403-432 (exception.message пользователя сохранен)` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | `Enabled` MUST return `false` when either: | `src/Логирование/Классы/ОтелЛоггер.os:57-84 (Включен: Ложь при отсутствии зарегистрированных процессоров - строки 76-78 через ЕстьПроцессоры(), иначе делегирует композиту - строки 82-83); src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:84-101 (Ложь только если все процессоры реализуют Включен и каждый вернул Ложь; процессор без Включен считается включенным); пункты Status: Development (LoggerConfig) не реализованы и в Stable-оценку не входят; подтверждено tests/unit/Логирование/ТестЛоггер.os:221-236, tests/unit/Логирование/ТестКомпозитныйПроцессорЛогов.os:121-131,150-164` |  |
| 29 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:90-98 (Истина, если хотя бы один процессор вернул Истина или не реализует Включен); встроенные процессоры возвращают Истина: src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:33-41, ОтелПростойПроцессорЛогов.os:72-80, ОтелПакетныйПроцессорЛогов.os:48-56; Ложь после закрытия провайдера (ОтелЛоггер.os:66-68) допускается MAY; подтверждено tests/unit/Логирование/ТестЛоггер.os:331-348,481-527, tests/unit/Логирование/ТестКомпозитныйПроцессорЛогов.os:106-119` |  |

#### ReadableLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readablelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 30 | MUST | ✅ found | A function receiving this as an argument MUST be able to access all the information added to the LogRecord. | `src/Логирование/Классы/ОтелЗаписьЛога.os:53-168,375-377 (Экспорт-геттеры Время, ВремяНаблюдения, НомерСерьезности, ТекстСерьезности, Тело, Атрибуты, ИдТрассировки, ИдСпана, ФлагиТрассировки, ИмяСобытия, КоличествоОтброшенныхАтрибутов, ИнформацияОбИсключении); читаются экспортером src/Экспорт/Классы/ОтелЭкспортерЛогов.os:250-269` |  |
| 31 | MUST | ✅ found | It MUST also be able to access the Instrumentation Scope and Resource information (implicitly) associated with the `LogRecord`. | `src/Логирование/Классы/ОтелЗаписьЛога.os:139-150 (Ресурс(), ОбластьИнструментирования()); заполняются логгером при emit - src/Логирование/Классы/ОтелЛоггер.os:99-100; подтверждено tests/unit/Логирование/ТестЛоггер.os:118-147 (ScopeИResourceНаЗаписиПослеЗаписать)` |  |
| 32 | MUST | ✅ found | The trace context fields MUST be populated from the resolved `Context` (either the explicitly passed `Context` or the current `Context`) when emitted. | `src/Логирование/Классы/ОтелЛоггер.os:98-112,173-187 (Записать(ЗаписьЛога, Контекст = Неопределено): явный контекст либо ОтелКонтекст.Текущий(); ВалидныйКонтекстСпана -> УстановитьКонтекстТрассировки и УстановитьФлагиТрассировки в момент emit); подтверждено tests/unit/Логирование/ТестЛоггер.os:63-91,270-329 (АвтокорреляцияСТекущимСпаном, ЗаписатьСЯвнымКонтекстом, КонтекстРазрешаетсяПриEmitАНеПриСозданииЗаписи)` |  |
| 33 | MUST | ✅ found | Counts for attributes due to collection limits MUST be available for exporters to report as described in the transformation to non-OTLP formats specification. | `src/Логирование/Классы/ОтелЗаписьЛога.os:152-159,241-246 (КоличествоОтброшенныхАтрибутов(); счетчик ОтброшенныхАтрибутов растет при отбрасывании по лимиту); используется src/Экспорт/Классы/ОтелЭкспортерЛогов.os:260 (droppedAttributesCount) и src/Экспорт/Классы/ОтелПротоКодировщикLogs.os:157-158; подтверждено tests/unit/Логирование/ТестЗаписьЛога.os:326-345` |  |

#### ReadWriteLogRecord

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#readwritelogrecord)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 34 | MUST | ✅ found | A function receiving this as an argument MUST additionally be able to modify the following information added to the LogRecord: | `src/Логирование/Классы/ОтелЗаписьЛога.os:186-351 (УстановитьСерьезность, УстановитьТекстСерьезности, УстановитьТело, УстановитьАтрибут - добавление/изменение, УдалитьАтрибут - удаление, УстановитьКонтекстТрассировки - TraceId и SpanId, УстановитьФлагиТрассировки, УстановитьИмяСобытия, УстановитьВремя, УстановитьВремяНаблюдения); запись изменяема в OnEmit: src/Логирование/Классы/ОтелЛоггер.os:122-127 (Зафиксировать() вызывается только после ПриПоявлении процессоров); подтверждено tests/unit/Логирование/ТестЗаписьЛога.os:84-99 (УдалениеАтрибута)` |  |

#### LogRecord Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecord-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 35 | MUST | ✅ found | `LogRecord` attributes MUST adhere to the common rules of attribute limits. | `src/Логирование/Классы/ОтелЗаписьЛога.os:237-251 (лимит количества: новый ключ сверх МаксАтрибутов отбрасывается и учитывается в счетчике, перезапись существующего ключа не считается; значение ограничивается ОтелУтилиты.ОграничитьЗначениеАтрибута); src/Ядро/Модули/ОтелУтилиты.os:385-387,556-603 (усечение строк и двоичных данных, поэлементно для массивов и отображений, лимит глубины); значения по умолчанию src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:97-101 (128 атрибутов, длина без ограничения); подтверждено tests/unit/Логирование/ТестЗаписьЛога.os:134-202` |  |
| 36 | MUST | ✅ found | If the SDK implements attribute limits it MUST provide a way to change these limits, via a configuration to the `LoggerProvider`, by allowing users to configure individual limits like in the Java exam... | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:259-277 (параметр конструктора ЛимитыЗаписейЛога), src/Логирование/Классы/ОтелПостроительПровайдераЛогирования.os:50-53 (УстановитьЛимитыЗаписейЛога); отдельные лимиты src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:51-80 (УстановитьМаксАтрибутов, УстановитьМаксДлинаЗначенияАтрибута, УстановитьМаксГлубинаЗначенияАтрибута); применяются при создании записи src/Логирование/Классы/ОтелЛоггер.os:19-24; OTEL_LOGRECORD_ATTRIBUTE_* - src/Конфигурация/Модули/ОтелАвтоконфигурация.os:661-676; подтверждено tests/unit/Логирование/ТестПровайдерЛогирования.os:96-120` |  |
| 37 | SHOULD | ✅ found | The options MAY be bundled in a class, which then SHOULD be called `LogRecordLimits`. | `src/Логирование/Классы/ОтелЛимитыЗаписейЛога.os:1-103 (класс ОтелЛимитыЗаписейЛога - дословно LogRecordLimits, «лимиты записей лога»; зарегистрирован в lib.config:54)` |  |
| 38 | SHOULD | ✅ found | There SHOULD be a message printed in the SDK’s log to indicate to the user that an attribute was discarded due to such a limit. | `src/Логирование/Классы/ОтелЗаписьЛога.os:242-245,405-410 (при отбрасывании атрибута по лимиту ВывестиПредупреждениеОбОтброшенныхДанных -> Лог.Предупреждение «Запись лога: атрибуты отброшены из-за лимитов»)` |  |
| 39 | MUST | ✅ found | To prevent excessive logging, the message MUST be printed at most once per `LogRecord` (i.e., not per discarded attribute). | `src/Логирование/Классы/ОтелЗаписьЛога.os:35-36,405-410,433 (флаг ПредупреждениеОтброшенныхВыведено на экземпляре записи, инициализируется Ложь в конструкторе: предупреждение выводится не более одного раза на запись)` |  |

#### LogRecordProcessor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordprocessor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 40 | MUST | ✅ found | The SDK MUST allow each pipeline to end with an individual exporter. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:165-171 (конструктор принимает собственный Экспортер); src/Логирование/Классы/ОтелПакетныйПроцессорЛогов.os:65-68 + src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:429-438 (пакетный процессор со своим Экспортер); src/Логирование/Классы/ОтелПровайдерЛогирования.os:101-103 и ОтелКомпозитныйПроцессорЛогов.os:21-29,47-58 (несколько независимых конвейеров процессор + экспортер)` |  |
| 41 | MUST | ✅ found | The SDK MUST allow users to implement and configure custom processors and decorate built-in processors for advanced scenarios such as enriching with attributes. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:1-77 (&Интерфейс для пользовательских процессоров: ПриПоявлении, Включен, СброситьБуфер, Закрыть); src/Логирование/Классы/ОтелПровайдерЛогирования.os:101-103, ОтелПостроительПровайдераЛогирования.os:36-39 (ДобавитьПроцессор принимает произвольный процессор без проверки типа, встроенный процессор можно обернуть); запись изменяема в ПриПоявлении (ОтелЛоггер.os:122-127) - обогащение атрибутами; подтверждено tests/unit/Логирование/ТестПровайдерЛогирования.os:50-71, tests/unit/Логирование/ТестЛоггер.os:481-527 (пользовательские процессоры из сценариев)` |  |

#### OnEmit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#onemit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 42 | SHOULD NOT | ✅ found | This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD NOT block or throw exceptions. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:5-16; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:21-29; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:41-69; src/Логирование/Классы/ОтелПакетныйПроцессорЛогов.os:29-31; src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:23-56` |  |
| 43 | MUST | ✅ found | For a `LogRecordProcessor` registered directly on SDK `LoggerProvider`, the `logRecord` mutations MUST be visible in next registered processors. | `src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:21-29; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:40-58; src/Логирование/Классы/ОтелПровайдерЛогирования.os:101-103; src/Логирование/Классы/ОтелЛоггер.os:123-128` |  |
| 44 | SHOULD | ✅ found | To avoid such race conditions, implementations SHOULD recommended to users that a clone of `logRecord` be used for any concurrent processing, such as in a batching processor. | `src/Логирование/Классы/ОтелПакетныйПроцессорЛогов.os:13-25; docs/api/Логирование/ОтелПакетныйПроцессорЛогов.md:16-19` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST NOT | ✅ found | Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller. | `src/Логирование/Классы/ОтелЛоггер.os:58-85; src/Логирование/Классы/ОтелЛоггер.os:148-162; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:85-106; src/Ядро/Классы/ОтелОбластьИнструментирования.os:40-42` |  |

#### ShutDown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 46 | SHOULD | ✅ found | `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:138-146; src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:110-113; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-100` |  |
| 47 | SHOULD | ✅ found | SDKs SHOULD ignore these calls gracefully, if possible. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:39-42; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:48-51; src/Логирование/Классы/ОтелЛоггер.os:123-125` |  |
| 48 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:55-66; src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:100-118; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:83-114; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:138-154; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:9-37` |  |
| 49 | MUST | ✅ found | `Shutdown` MUST include the effects of `ForceFlush`. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-217; src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:110-118; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:89-121` |  |
| 50 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:330-339; src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:110-118; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:110-121; src/Ядро/Классы/ОтелБлокировкаСТаймаутом.os:20-30` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 51 | SHOULD | ✅ found | This is a hint to ensure that any tasks associated with `LogRecord`s for which the `LogRecordProcessor` had already received events prior to the call to `ForceFlush` SHOULD be completed as soon as pos... | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:180-217; src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:82-98; src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120` |  |
| 52 | SHOULD | ✅ found | In particular, if any `LogRecordProcessor` has any associated exporter, it SHOULD try to call the exporter’s `Export` with all `LogRecord`s for which this was not already done and then invoke `ForceFl... | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-217; src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:93-98; src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120` |  |
| 53 | MUST | ✅ found | The built-in LogRecordProcessors MUST do so. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:93-98; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-217` |  |
| 54 | MUST | ✅ found | If a timeout is specified (see below), the `LogRecordProcessor` MUST prioritize honoring the timeout over finishing all calls. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-252; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:272-273; src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120; src/Ядро/Классы/ОтелБлокировкаСТаймаутом.os:20-30` |  |
| 55 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:43-53; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71-81; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:116-140; src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:82-98; src/Ядро/Модули/ОтелРезультатыЭкспорта.os:13-39` |  |
| 56 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the `LogRecordProcesso... | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance) о том, в каких случаях следует вызывать ForceFlush; SDK не может программно обеспечить это ограничение. |
| 57 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:79-81; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-205; src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:93-98; src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120` |  |

#### Built-in processors

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#built-in-processors)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 58 | MUST | ✅ found | The standard OpenTelemetry SDK MUST implement both simple and batch processors, as described below. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:155-171; src/Логирование/Классы/ОтелПакетныйПроцессорЛогов.os:62-68; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:416-450; lib.config:58-59` |  |
| 59 | SHOULD | ✅ found | Other common processing scenarios SHOULD be first considered for implementation out-of-process in OpenTelemetry Collector. | `lib.config:58-61; src/Логирование/Классы/` |  |

#### Simple processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#simple-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:46-54; src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:168; src/Ядро/Классы/ОтелБлокировкаСТаймаутом.os:20-36` |  |

#### Batching processor

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#batching-processor)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | MUST | ✅ found | The processor MUST synchronize calls to `LogRecordExporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:219-279; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:445; src/Логирование/Классы/ОтелПакетныйПроцессорЛогов.os:29-31` |  |

#### LogRecordExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 62 | MUST | ✅ found | Each implementation MUST document the concurrency characteristics the SDK requires of the exporter. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:6-7; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:219-222; docs/architecture.md:298; docs/api/Экспорт/ОтелЭкспортерЛогов.md:17` |  |

#### LogRecordExporter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 63 | MUST | ✅ found | A `LogRecordExporter` MUST support the following functions: | `src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:14,26,35; src/Экспорт/Классы/ОтелЭкспортерЛогов.os:34,64,74,122` |  |

#### Export

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#export)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 64 | MUST NOT | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:34-53,123-127` |  |
| 65 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (`Failure`). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:43-52,123-127; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:628-630,817-818` |  |
| 66 | SHOULD NOT | ✅ found | The default SDK’s `LogRecordProcessors` SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the logs are being sent to. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:39-56; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:263-279; src/Экспорт/Классы/ОтелHttpТранспорт.os:182,351-354; src/Экспорт/Классы/ОтелGrpcТранспорт.os:119,257` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | SHOULD | ✅ found | This is a hint to ensure that the export of any `ReadableLogRecords` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning fr... | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:34-53,64-67; src/Ядро/Модули/ОтелРезультатыЭкспорта.os:107-120; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:191-217` |  |
| 68 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:64-67; src/Экспорт/Классы/ИнтерфейсЭкспортерЛогов.os:18-28; src/Ядро/Классы/ОтелРезультатЭкспорта.os:17-38` |  |
| 69 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports t... | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance); SDK не может программно обеспечить это ограничение (решение, когда вызывать ForceFlush, принимает пользователь или инструментированное приложение). |
| 70 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:64-67` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each `LogRecordExporter` instance. | `src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:110-118; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:110-121; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:95-114` |  |
| 72 | SHOULD | ✅ found | After the call to `Shutdown` subsequent calls to `Export` are not allowed and SHOULD return a Failure result. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:35-37,74-77` |  |
| 73 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:74-77` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/logs/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 74 | MUST | ✅ found | LoggerProvider - Logger creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелПровайдерЛогирования.os:7,58-94,124-126,138-146,227-241,274-276; src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:3-5,47-58` |  |
| 75 | MUST | ✅ found | Logger - all methods MUST be safe to be called concurrently. | `src/Логирование/Классы/ОтелЛоггер.os:32,57-84,89,98-128,245,254-258` |  |
| 76 | MUST | ✅ found | LogRecordExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерЛогов.os:1,6-7,12,64-77,128` |  |

### Metrics Api

#### MeterProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | Thus, the API SHOULD provide a way to set/register and access a global default `MeterProvider`. | `src/Ядро/Модули/ОтелГлобальный.os:175-177,185-194` |  |

#### MeterProvider operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meterprovider-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | The `MeterProvider` MUST provide the following functions: | `src/Метрики/Классы/ОтелПровайдерМетрик.os:59-61,74-125` |  |

#### Get a Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#get-a-meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | This API MUST accept the following parameters: | `src/Метрики/Классы/ОтелПровайдерМетрик.os:74-78,84-85; src/Метрики/Классы/ОтелПостроительМетра.os:26-64` |  |
| 4 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:76; src/Метрики/Классы/ОтелПостроительМетра.os:26,92` |  |
| 5 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:78; src/Метрики/Классы/ОтелПостроительМетра.os:39,93` |  |
| 6 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:77; src/Метрики/Классы/ОтелПостроительМетра.os:52-55,94; src/Ядро/Классы/ОтелОбластьИнструментирования.os:164-169; src/Ядро/Классы/ОтелАтрибуты.os:19` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | SHOULD NOT | ✅ found | Note: `Meter` SHOULD NOT be responsible for the configuration. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:103-110,266-339; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:28-90; src/Метрики/Классы/ОтелМетр.os:56-257` |  |

#### Meter operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#meter-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | The `Meter` MUST provide functions to create new Instruments: | `src/Метрики/Классы/ОтелМетр.os:80-82,180-184,96-98,146-148,251-255,131-133,216-220` |  |

#### Instrument

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ➖ n_a | Language-level features such as the distinction between integer and floating point numbers SHOULD be considered as identifying. | `src/Метрики/Модули/ОтелАгрегация.os:419-423; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:591-611; src/Метрики/Классы/ОтелМетр.os:1143-1154,1279-1287` | Ограничение платформы OneScript (Число = System.Decimal): единственный числовой тип - Число, языкового различия integer/floating point не существует. API не предоставляет типизированных вариантов инструментов (нет аналога Java LongCounter/DoubleCounter): СоздатьСчетчик/СоздатьГистограмму/СоздатьДатчик и т.д. не принимают числовой тип, поэтому такому признаку идентичности неоткуда взяться. Внутренний тип значения int/double выводится из вида инструмента (ОтелАгрегация.ТипЗначенияДляВида), а вид уже входит в идентичность инструмента (НайтиЗарегистрированныйИнструмент/ЗарегистрироватьДескриптор: имя, вид, единица, описание); экспортер явно документирует, что Число OneScript одно для целых и дробных значений (ОтелЭкспортерМетрик.os:591-592). |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | SHOULD | ✅ found | The API SHOULD treat it as an opaque string. | `src/Метрики/Классы/ОтелМетр.os:627,666,1040-1045; src/Метрики/Модули/ОтелПотокиМетрик.os:60; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:421` |  |
| 11 | MUST | ✅ found | It MUST be case-sensitive (e.g. `kb` and `kB` are different units), ASCII string. | `src/Метрики/Классы/ОтелМетр.os:1275-1277,1330,1477; src/Метрики/Классы/ОтелСелекторИнструментов.os:52` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | The API MUST treat it as an opaque string. | `src/Метрики/Классы/ОтелМетр.os:626,665,1040-1045 (Описание = НормализоватьСтроку(Описание): только Неопределено -> "", без разбора и преобразования); src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:10,50-52; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:10,62-64 (хранится и возвращается как есть, сравнивается только на равенство)` |  |
| 13 | MUST | ✅ found | It MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or `utf8mb3`). | `src/Метрики/Классы/ОтелМетр.os:80,626 (Описание - Строка = .NET System.String, полный Unicode - платформенная гарантия); src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:50-52` |  |
| 14 | MUST | ✅ found | It MUST support at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:80,626 (Описание - Строка длиной до 2^31 символов - платформенная гарантия; усечения нигде нет); src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:50-52` |  |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | OpenTelemetry SDKs MUST handle `advisory` parameters as described here. | `src/Метрики/Классы/ОтелМетр.os:635,675,1542-1573 (ПроверитьСовет: advisory принимаются для всех видов инструментов, невалидные ГраницыГистограммы игнорируются с предупреждением); src/Метрики/Модули/ОтелПотокиМетрик.os:366-374,391-399 (ГраницыПотока: advisory ГраницыГистограммы (ExplicitBucketBoundaries) применяются к агрегации explicit_bucket_histogram по умолчанию, настройки View приоритетнее)` |  |

#### Synchronous Instrument API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#synchronous-instrument-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | The API to construct synchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:80-82,96-98,131-133,146-148 (СоздатьСчетчик/СоздатьГистограмму/СоздатьРеверсивныйСчетчик/СоздатьДатчик: Имя, Описание, ЕдиницаИзмерения, Совет)` |  |
| 17 | SHOULD | ✅ found | If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:80,96,131,146 (Имя - обязательный позиционный параметр без значения по умолчанию)` |  |
| 18 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:80,96,131,146 (обязательность Имя обеспечена структурно), 71-72 (doc-комментарий параметра Имя); docs/api/Метрики/ОтелМетр.md:35,50,65,80 (Имя без значения по умолчанию)` |  |
| 19 | SHOULD | ✅ found | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `src/Метрики/Классы/ОтелМетр.os:62-69 (doc-комментарий: regex [A-Za-z][A-Za-z0-9_./-]{0,254}, длина, допустимые символы); docs/api/Метрики/ОтелМетр.md:25 (паттерн имени для всех инструментов метра)` |  |
| 20 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`; that is left to implementations of the API, like the SDK. | `src/Метрики/Классы/ОтелМетр.os:625,1061-1070 (ВалидироватьИмяИнструмента - SDK-уровневая мягкая проверка объединенного API+SDK: предупреждение в лог, инструмент создается)` |  |
| 21 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:80,96,131,146 (ЕдиницаИзмерения = "" по умолчанию)` |  |
| 22 | MUST | ✅ found | Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелМетр.os:80,627 (ЕдиницаИзмерения - Строка без приведения регистра и ограничения длины), 1275-1277,1472-1478 (единица сравнивается регистрозависимо)` |  |
| 23 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:627,1040-1045 (НормализоватьСтроку - только Неопределено -> "", содержимое единицы не проверяется)` |  |
| 24 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:80,96,131,146 (Описание = "" по умолчанию)` |  |
| 25 | MUST | ✅ found | Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:80,626 (Описание - Строка: полный Unicode и длина до 2^31 символов - платформенная гарантия)` |  |
| 26 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:80,96,131,146 (Совет = Неопределено по умолчанию)` |  |
| 27 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:635,1542-1573 (ПроверитьСовет - SDK-уровневая мягкая проверка объединенного API+SDK: предупреждение и игнорирование невалидного поля, регистрация не отклоняется)` |  |

#### Asynchronous Instrument API

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-instrument-api)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | The API to construct asynchronous instruments MUST accept the following parameters: | `src/Метрики/Классы/ОтелМетр.os:180-184,216-220,251-255 (СоздатьНаблюдаемыйСчетчик/СоздатьНаблюдаемыйРеверсивныйСчетчик/СоздатьНаблюдаемыйДатчик: Имя, Callback, Описание, ЕдиницаИзмерения, Совет)` |  |
| 29 | SHOULD | ✅ found | If possible, the API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелМетр.os:180,216,251 (Имя - обязательный позиционный параметр без значения по умолчанию)` |  |
| 30 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, the API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелМетр.os:180,216,251 (обязательность Имя обеспечена структурно), 153,189,225 (doc-комментарий параметра Имя); docs/api/Метрики/ОтелМетр.md:111,127,143 (Имя без значения по умолчанию)` |  |
| 31 | SHOULD | ✅ found | The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to conform to the instrument name syntax. | `docs/api/Метрики/ОтелМетр.md:25 (паттерн имени для всех инструментов метра, включая наблюдаемые); src/Метрики/Классы/ОтелМетр.os:62-69 (doc-комментарий с regex имени инструмента)` |  |
| 32 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `name`, that is left to implementations of the API. | `src/Метрики/Классы/ОтелМетр.os:664,1061-1070 (ВалидироватьИмяИнструмента - SDK-уровневая мягкая проверка: предупреждение в лог, инструмент создается)` |  |
| 33 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:180,216,251 (ЕдиницаИзмерения = "" по умолчанию)` |  |
| 34 | MUST | ✅ found | Meaning, the API MUST accept a case-sensitive string that supports ASCII character encoding and can hold at least 63 characters. | `src/Метрики/Классы/ОтелМетр.os:180,666 (ЕдиницаИзмерения - Строка без приведения регистра и ограничения длины), 1472-1478 (регистрозависимое сравнение единиц)` |  |
| 35 | SHOULD NOT | ✅ found | The API SHOULD NOT validate the `unit`. | `src/Метрики/Классы/ОтелМетр.os:666,1040-1045 (НормализоватьСтроку - только Неопределено -> "", содержимое не проверяется)` |  |
| 36 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелМетр.os:180,216,251 (Описание = "" по умолчанию)` |  |
| 37 | MUST | ✅ found | Meaning, the API MUST accept a string that supports at least BMP (Unicode Plane 0) encoded characters and hold at least 1023 characters. | `src/Метрики/Классы/ОтелМетр.os:180,665 (Описание - Строка: полный Unicode и длина до 2^31 символов - платформенная гарантия)` |  |
| 38 | MUST NOT | ✅ found | Therefore, this API needs to be structured to accept `advisory` parameters, but MUST NOT obligate the user to provide it. | `src/Метрики/Классы/ОтелМетр.os:180,216,251 (Совет = Неопределено по умолчанию)` |  |
| 39 | SHOULD NOT | ✅ found | The API SHOULD NOT validate `advisory` parameters. | `src/Метрики/Классы/ОтелМетр.os:675,1542-1573 (ПроверитьСовет - та же мягкая SDK-уровневая проверка, что и для синхронных инструментов)` |  |
| 40 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of `callback` functions, including none. | `src/Метрики/Классы/ОтелМетр.os:180,216,251 (Callback = Неопределено: нет callback-ов / одиночный Действие / Массив из Действие); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:516-527` |  |
| 41 | MUST | ✅ found | The API MUST support creation of asynchronous instruments by passing zero or more `callback` functions to be permanently registered to the newly created instrument. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:516-527 (callback-и создания регистрируются в Действия инструмента на все время его жизни); src/Метрики/Классы/ОтелМетр.os:670-672,972-983 (callback-и повторного создания идентичного инструмента добавляются к возвращаемому экземпляру)` |  |
| 42 | SHOULD | ✅ found | The API SHOULD support registration of `callback` functions associated with asynchronous instruments after they are created. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:127-143 (ДобавитьCallback); src/Метрики/Классы/ОтелМетр.os:532-563 (ЗарегистрироватьОбратныйВызов для нескольких инструментов)` |  |
| 43 | MUST | ✅ found | Where the API supports registration of `callback` functions after asynchronous instrumentation creation, the user MUST be able to undo registration of the specific callback after its registration by s... | `src/Метрики/Классы/ОтелРегистрацияНаблюдателя.os:14-20 (Закрыть); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:142,151-163 (ДобавитьCallback возвращает регистрацию, УдалитьCallback); src/Метрики/Классы/ОтелМетр.os:562,570-572,944-962 (отмена мульти-callback)` |  |
| 44 | MUST | ✅ found | Every currently registered Callback associated with a set of instruments MUST be evaluated exactly once during collection prior to reading data for that instrument set. | `src/Метрики/Классы/ОтелМетр.os:440-471 (СобратьДляЧитателя: мульти-callback-и вызываются один раз до сбора инструментов); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:257-279,394-414 (ВызватьCallbackи: каждый callback снимка вызывается ровно один раз перед Хранилище.Собрать)` |  |
| 45 | MUST | ✅ found | Callback functions MUST be documented as follows for the end user: | `src/Метрики/Классы/ОтелМетр.os:157-170,193-206,228-241,515-523; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:110-118; docs/api/Метрики/ОтелМетр.md:201-212 (раздел «Требования к callback»: реентерабельность, ограниченное время, отсутствие дублирующих наблюдений)` |  |
| 46 | SHOULD | ✅ found | Callback functions SHOULD be reentrant safe. | `src/Метрики/Классы/ОтелМетр.os:158-159; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:111-112; docs/api/Метрики/ОтелМетр.md:205-206 (рекомендация задокументирована для пользователя)` |  |
| 47 | SHOULD NOT | ✅ found | Callback functions SHOULD NOT take an indefinite amount of time. | `src/Метрики/Классы/ОтелМетр.os:160-161; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:113-114; docs/api/Метрики/ОтелМетр.md:207-209 (рекомендация задокументирована для пользователя); src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:121-165 (дополнительно SDK ограничивает ожидание callback-а таймаутом)` |  |
| 48 | SHOULD NOT | ✅ found | Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same `attributes`) across all registered callbacks. | `src/Метрики/Классы/ОтелМетр.os:162-164; docs/api/Метрики/ОтелМетр.md:210-211 (рекомендация задокументирована для пользователя); src/Метрики/Классы/ОтелХранилищеНаблюдений.os:299-322 (дублирующие наблюдения агрегируются в одну серию без сбоя сбора)` |  |
| 49 | MUST | ✅ found | Callbacks registered at the time of instrument creation MUST apply to the single instruments which is under construction. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:516-527 (callback-и создания - только в Действия создаваемого инструмента); src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:56-64 (callback получает ОтелНаблюдениеМетрики только этого инструмента)` |  |
| 50 | MUST | ✅ found | Idiomatic APIs for multiple-instrument Callbacks MUST distinguish the instrument associated with each observed `Measurement` value. | `src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:77-93 (ВызватьМультиCallback: Соответствие инструмент -> ОтелНаблюдениеМетрики, дополнительно по имени инструмента); src/Метрики/Классы/ОтелМетр.os:757-771 (наблюдения распределяются по своим инструментам)` |  |
| 51 | MUST | ✅ found | Multiple-instrument Callbacks MUST be associated at the time of registration with a declared set of asynchronous instruments from the same `Meter` instance. | `src/Метрики/Классы/ОтелМетр.os:532-563 (ЗарегистрироватьОбратныйВызов: набор инструментов задается при регистрации, проверки ПринадлежитМетру и ЭтоАсинхронныйИнструмент), 929-936,993-1003` |  |
| 52 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical times... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:394-414 (одно ВремяНаблюдения на все записи вызова callback-а, при сборе читателем - время сбора); src/Метрики/Классы/ОтелМетр.os:738-771,778-798 (мульти-callback: одно время для всех инструментов вызова)` |  |
| 53 | MUST | ✅ found | The API MUST treat observations from a single Callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical times... | `src/Метрики/Классы/ОтелХранилищеНаблюдений.os:279-297,299-322 (время точки данных = время группы наблюдений вызова); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:402-405; src/Метрики/Классы/ОтелМетр.os:768,787` |  |
| 54 | SHOULD | ✅ found | The API SHOULD provide some way to pass `state` to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:127 (ДобавитьCallback(Callback, Состояние)); src/Метрики/Классы/ОтелМетр.os:532 (ЗарегистрироватьОбратныйВызов(Callback, НовыеИнструменты, Состояние)); src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:58-62,87-91 (Состояние передается вторым аргументом callback-а)` |  |

#### General operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#general-operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 55 | SHOULD | ✅ found | All synchronous instruments SHOULD provide functions to: * Report if instrument is `Enabled` | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:250-253 (Функция Включен); наследуется ОтелСчетчик/ОтелРеверсивныйСчетчик/ОтелГистограмма/ОтелДатчик/ОтелЭкспоненциальнаяГистограмма через &Расширяет (src/Метрики/Классы/ОтелСчетчик.os:70)` |  |

#### Enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 56 | SHOULD | ✅ found | To help users avoid performing computationally expensive operations when recording measurements, synchronous instruments SHOULD provide this `Enabled` API. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:232-253 (Функция Включен(Атрибуты = Неопределено) у всех синхронных инструментов)` |  |
| 57 | MUST | ✅ found | Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters to be added. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:235,250 (необязательный параметр Атрибуты зарезервирован для расширяемости; новые необязательные параметры добавляются без нарушения совместимости)` |  |
| 58 | MUST | ✅ found | This API MUST return a language idiomatic boolean type. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:246-247,250-253 (возвращает Булево)` |  |
| 59 | SHOULD | ✅ found | The API SHOULD be documented that instrumentation authors needs to call this API each time they record a measurement to ensure they have the most up-to-date response. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:237-241 (doc-комментарий: вызывать перед каждым Add()/Record(), значение может меняться со временем, не кэшировать)` |  |

#### Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 60 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating a `Counter` other than with a `Meter`. | `src/Метрики/Классы/ОтелСчетчик.os:70-73; src/Метрики/Классы/ОтелМетр.os:80-82,643` | OneScript не поддерживает приватные конструкторы: ПриСозданииОбъекта всегда публичен, а классы ОтелСчетчик и ОтелБазовыйСинхронныйИнструмент зарегистрированы в lib.config, поэтому Новый ОтелСчетчик() технически вызываем из пользовательского кода. Такой объект нефункционален: поле &Родитель (библиотека extends) заполняет только ПостроительНаследника(...).Построить(), который вызывается в ОтелМетр.СоздатьСинхронныйИнструмент (ОтелМетр.os:643); при прямом создании Родитель = Неопределено и запись значения завершается исключением. Единственный документированный способ создания Counter - ОтелМетр.СоздатьСчетчик() (ОтелМетр.os:80-82). Ограничение аналогично приватным конструкторам ОтелСпан (документировано в ОтелСпан.os:786-791 и docs/spec-compliance.md). |

#### Add

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#add)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 61 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелСчетчик.os:34` |  |
| 62 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелСчетчик.os:30,34` |  |
| 63 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелСчетчик.os:34` |  |
| 64 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелСчетчик.os:29-34` |  |
| 65 | SHOULD | ✅ found | This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелСчетчик.os:17-30` |  |
| 66 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелСчетчик.os:19-27,35-41` |  |
| 67 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелСчетчик.os:31,34; src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:76; src/Метрики/Классы/ОтелХранилищеМетрики.os:507-512` |  |
| 68 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелСчетчик.os:34; src/Метрики/Классы/ОтелМетр.os:80-82` |  |

#### Asynchronous Counter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-counter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating an Asynchronous Counter other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:180-184,682; src/Метрики/Классы/ОтелНаблюдаемыйСчетчик.os:22-24` | OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Единственная фабрика ObservableCounter в SDK - ОтелМетр.СоздатьНаблюдаемыйСчетчик() (ОтелМетр.os:180-184); других API создания асинхронных инструментов (в ОтелПровайдерМетрик, ОтелГлобальный и др.) нет, связывание фасада с базовым инструментом через ПостроительНаследника выполняется только в ОтелМетр (ОтелМетр.os:682). Классы ОтелНаблюдаемыйСчетчик (lib.config:80) и ОтелБазовыйНаблюдаемыйИнструмент (lib.config:105) имеют публичный ПриСозданииОбъекта (платформенное ограничение): голый Новый ОтелНаблюдаемыйСчетчик() нефункционален (поле &Родитель задает только ПостроительНаследника), а сборка в обход Meter через Новый ОтелБазовыйНаблюдаемыйИнструмент(..., Агрегатор) возможна лишь из-за отсутствия приватных конструкторов (так делают тесты, напр. tests/unit/Метрики/ТестБазовыйНаблюдаемыйИнструмент.os:24). |
| 70 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical times... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:394-414; src/Метрики/Классы/ОтелМетр.os:445-448,757-771,778-798; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:284-287` |  |
| 71 | MUST | ✅ found | The API MUST treat observations from a single callback as logically taking place at a single instant, such that when recorded, observations from a single callback MUST be reported with identical times... | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:402-405; src/Метрики/Классы/ОтелМетр.os:768,787-790; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:284-287` |  |
| 72 | SHOULD | ✅ found | The API SHOULD provide some way to pass `state` to the callback. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:127; src/Метрики/Классы/ОтелМетр.os:532; src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:56-64,87-91` |  |

#### Histogram creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#histogram-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating a `Histogram` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:96-98,113-118,643; src/Метрики/Классы/ОтелГистограмма.os:51-53` | OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Единственные фабрики Histogram в SDK - ОтелМетр.СоздатьГистограмму() (ОтелМетр.os:96-98) и ОтелМетр.СоздатьЭкспоненциальнуюГистограмму() (ОтелМетр.os:113-118); других API создания гистограмм (в ОтелПровайдерМетрик, ОтелГлобальный и др.) нет, связывание фасада через ПостроительНаследника выполняется только в ОтелМетр (ОтелМетр.os:643). Классы ОтелГистограмма (lib.config:71) и ОтелБазовыйСинхронныйИнструмент (lib.config:104) имеют публичный ПриСозданииОбъекта (платформенное ограничение): голый Новый ОтелГистограмма() нефункционален (поле &Родитель задает только ПостроительНаследника), а сборка в обход Meter через Новый ОтелБазовыйСинхронныйИнструмент(..., Агрегатор) возможна лишь из-за отсутствия приватных конструкторов (так делают тесты, напр. tests/unit/Метрики/ТестВременнаяАгрегация.os:273). |

#### Record

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#record)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 74 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелГистограмма.os:31` |  |
| 75 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелГистограмма.os:27,31` |  |
| 76 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелГистограмма.os:31` |  |
| 77 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелГистограмма.os:26-31` |  |
| 78 | SHOULD | ✅ found | This API SHOULD be documented in a way to communicate to users that this value is expected to be non-negative. | `src/Метрики/Классы/ОтелГистограмма.os:15-18,27` |  |
| 79 | SHOULD NOT | ✅ found | This API SHOULD NOT validate this value, that is left to implementations of the API. | `src/Метрики/Классы/ОтелГистограмма.os:17-18,31-33` |  |
| 80 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелГистограмма.os:28,31; src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:76; src/Метрики/Классы/ОтелХранилищеМетрики.os:507-512` |  |

#### Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 81 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating a `Gauge` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:146-148,643; src/Метрики/Классы/ОтелДатчик.os:41-43` | OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Единственная фабрика Gauge в SDK - ОтелМетр.СоздатьДатчик() (ОтелМетр.os:146-148); других API создания датчиков (в ОтелПровайдерМетрик, ОтелГлобальный и др.) нет, связывание фасада через ПостроительНаследника выполняется только в ОтелМетр (ОтелМетр.os:643). Классы ОтелДатчик (lib.config:79) и ОтелБазовыйСинхронныйИнструмент (lib.config:104) имеют публичный ПриСозданииОбъекта (платформенное ограничение): голый Новый ОтелДатчик() нефункционален (поле &Родитель задает только ПостроительНаследника), а сборка в обход Meter через Новый ОтелБазовыйСинхронныйИнструмент(..., Агрегатор) возможна лишь из-за отсутствия приватных конструкторов. |

#### Record

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#record)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 82 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 83 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелДатчик.os:17,21` |  |
| 84 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелДатчик.os:21` |  |
| 85 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелДатчик.os:16-21` |  |
| 86 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелДатчик.os:18,21; src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:76; src/Метрики/Классы/ОтелХранилищеМетрики.os:507-512` |  |
| 87 | MUST | ✅ found | The API MUST allow callers to provide flexible attributes at invocation time rather than having to register all the possible attribute names during the instrument creation. | `src/Метрики/Классы/ОтелДатчик.os:21; src/Метрики/Классы/ОтелМетр.os:146-148` |  |

#### Asynchronous Gauge creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-gauge-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 88 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating an Asynchronous Gauge other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:251-255,682; src/Метрики/Классы/ОтелНаблюдаемыйДатчик.os:22-24` | OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Единственная фабрика ObservableGauge в SDK - ОтелМетр.СоздатьНаблюдаемыйДатчик() (ОтелМетр.os:251-255); других API создания асинхронных инструментов (в ОтелПровайдерМетрик, ОтелГлобальный и др.) нет, связывание фасада через ПостроительНаследника выполняется только в ОтелМетр (ОтелМетр.os:682). Классы ОтелНаблюдаемыйДатчик (lib.config:83) и ОтелБазовыйНаблюдаемыйИнструмент (lib.config:105) имеют публичный ПриСозданииОбъекта (платформенное ограничение): голый Новый ОтелНаблюдаемыйДатчик() нефункционален (поле &Родитель задает только ПостроительНаследника), а сборка в обход Meter через Новый ОтелБазовыйНаблюдаемыйИнструмент(..., Агрегатор) возможна лишь из-за отсутствия приватных конструкторов (так делают тесты, напр. tests/unit/Метрики/ТестБазовыйНаблюдаемыйИнструмент.os:24). |

#### UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating an `UpDownCounter` other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:131` | OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен); ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Единственная фабрика UpDownCounter в SDK - ОтелМетр.СоздатьРеверсивныйСчетчик() (ОтелМетр.os:131-133 -> СоздатьСинхронныйИнструмент/НовыйФасад, ОтелМетр.os:622-645, 691); в ОтелПровайдерМетрик, ОтелГлобальный и остальных модулях src/ других фабрик UpDownCounter нет (grep по src/). Классы ОтелРеверсивныйСчетчик (lib.config:70) и ОтелБазовыйСинхронныйИнструмент (lib.config:104) зарегистрированы с публичным ПриСозданииОбъекта, поэтому технически инструмент можно собрать в обход Meter через Новый ОтелБазовыйСинхронныйИнструмент(...) + ПостроительНаследника (так делают тесты, напр. tests/unit/Метрики/ТестВременнаяАгрегация.os:273); голый Новый ОтелРеверсивныйСчетчик() без связывания через ПостроительНаследника нефункционален - поле &Родитель не установлено. |

#### Add

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#add)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | SHOULD NOT | ✅ found | This API SHOULD NOT return a value (it MAY return a dummy value if required by certain programming languages or systems, for example `null`, `undefined`). | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 91 | MUST | ✅ found | This API MUST accept the following parameter: | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 92 | SHOULD | ✅ found | If possible, this API SHOULD be structured so a user is obligated to provide this parameter. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21` |  |
| 93 | MUST | ✅ found | If it is not possible to structurally enforce this obligation, this API MUST be documented in a way to communicate to users that this parameter is needed. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:13-20; docs/api/Метрики/ОтелРеверсивныйСчетчик.md:26` |  |
| 94 | MUST | ✅ found | Therefore, this API MUST be structured to accept a variable number of attributes, including none. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21; src/Метрики/Классы/ОтелХранилищеМетрики.os:54-58` |  |

#### Asynchronous UpDownCounter creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#asynchronous-updowncounter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 95 | MUST NOT | ➖ n_a | There MUST NOT be any API for creating an Asynchronous UpDownCounter other than with a `Meter`. | `src/Метрики/Классы/ОтелМетр.os:216` | OneScript не поддерживает приватные конструкторы (ПриСозданииОбъекта всегда публичен); ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. Единственная фабрика ObservableUpDownCounter в SDK - ОтелМетр.СоздатьНаблюдаемыйРеверсивныйСчетчик() (ОтелМетр.os:216-220 -> СоздатьАсинхронныйИнструмент/НовыйФасад, ОтелМетр.os:662-685, 701); в ОтелПровайдерМетрик, ОтелГлобальный и остальных модулях src/ других фабрик нет (grep по src/). Классы ОтелНаблюдаемыйРеверсивныйСчетчик (lib.config:82) и ОтелБазовыйНаблюдаемыйИнструмент (lib.config:105) зарегистрированы с публичным ПриСозданииОбъекта, поэтому технически инструмент можно собрать в обход Meter через Новый ОтелБазовыйНаблюдаемыйИнструмент(...) + ПостроительНаследника (тесты создают базовый инструмент напрямую, напр. tests/unit/Метрики/ТестБазовыйНаблюдаемыйИнструмент.os:24); голый Новый ОтелНаблюдаемыйРеверсивныйСчетчик() без связывания через ПостроительНаследника нефункционален. |

#### Multiple-instrument callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#multiple-instrument-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 96 | SHOULD | ✅ found | The API to register a new Callback SHOULD accept: | `src/Метрики/Классы/ОтелМетр.os:532; src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:77-93` |  |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | SHOULD | ✅ found | All the metrics components SHOULD allow new APIs to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:186-210; src/Метрики/Классы/ОтелПровайдерМетрик.os:136-163; packagedef:7` |  |
| 98 | SHOULD | ✅ found | All the metrics APIs SHOULD allow optional parameter(s) to be added to existing APIs without introducing breaking changes, if possible. | `src/Метрики/Классы/ОтелРеверсивныйСчетчик.os:21; src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:250; src/Метрики/Классы/ОтелМетр.os:131` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/api/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 99 | MUST | ✅ found | MeterProvider - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:39-48; docs/api/Метрики/ОтелПровайдерМетрик.md:21` |  |
| 100 | MUST | ✅ found | Meter - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелМетр.os:58-59; docs/api/Метрики/ОтелМетр.md:23` |  |
| 101 | MUST | ✅ found | Instrument - all methods MUST be documented that implementations need to be safe for concurrent use by default. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:33-34; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:43-46; docs/api/Метрики/ОтелРеверсивныйСчетчик.md:14; docs/api/Метрики/ОтелНаблюдаемыйРеверсивныйСчетчик.md:13` |  |

### Metrics Sdk

#### Metrics SDK

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metrics-sdk)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | All language implementations of OpenTelemetry MUST provide an SDK. | `lib.config:64-110 (классы и модули SDK метрик); src/Метрики/Классы/ОтелПровайдерМетрик.os:417-464 (SDK MeterProvider); src/Ядро/Классы/ОтелSdk.os:9-10,45-47 (ПровайдерМетрик в составе SDK)` |  |

#### MeterProvider

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 2 | MUST | ✅ found | A `MeterProvider` MUST provide a way to allow a Resource to be specified. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:429-435 (ПриСозданииОбъекта(Ресурс = Неопределено, ...); без ресурса - Новый ОтелРесурс()), 132-134 (Ресурс()); src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:28-31 (УстановитьРесурс), 84-85 (Построить передает Ресурс)` |  |
| 3 | SHOULD | ✅ found | If a `Resource` is specified, it SHOULD be associated with all the metrics produced by any `Meter` from the `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:103-106,406 (ресурс провайдера передается каждому метру, включая no-op), 411-415 (ресурс передается читателю для продюсеров); src/Метрики/Классы/ОтелМетр.os:1101 (УстановитьРесурс), 463-468 (Ресурс передается в СобратьДляЧитателя инструментов); src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:127-137; src/Метрики/Классы/ОтелБазовыйАгрегатор.os:28-34 (ОтелДанныеМетрики с ресурсом); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:354-363,694,743-748 (ресурс провайдера для MetricProducer)` |  |

#### MeterProvider Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meterprovider-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | SHOULD | ✅ found | The SDK SHOULD allow the creation of multiple independent `MeterProvider`s. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:5-33,429-464 (все состояние - переменные экземпляра, синглтона нет; модули src/Метрики/Модули/ не имеют переменных модуля); src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:84-90 (каждый Построить создает новый провайдер); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:354-363 (читатель привязывается только к одному провайдеру)` |  |

#### Meter Creation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter-creation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | SHOULD | ➖ n_a | It SHOULD only be possible to create `Meter` instances through a `MeterProvider` (see API). | `src/Метрики/Классы/ОтелМетр.os:1097-1123 (публичный ПриСозданииОбъекта); src/Метрики/Классы/ОтелПровайдерМетрик.os:103,406 (единственные места создания ОтелМетр в src); src/Метрики/Классы/ОтелПостроительМетра.os:62-64 (делегирует в ПолучитьМетр)` | OneScript не поддерживает приватные конструкторы; ограничение документировано в коде (ОтелСпан.os) и docs/spec-compliance.md. ПриСозданииОбъекта класса ОтелМетр (ОтелМетр.os:1097-1123) всегда публичен, поэтому прямой вызов Новый ОтелМетр(...) в обход MeterProvider запретить средствами языка невозможно. Внутри SDK ОтелМетр создается только провайдером: ОтелПровайдерМетрик.ПолучитьМетр (ОтелПровайдерМетрик.os:103) и НоопМетр (ОтелПровайдерМетрик.os:406); ОтелПостроительМетра.Построить делегирует в ПолучитьМетр (ОтелПостроительМетра.os:62-64). |
| 6 | MUST | ✅ found | The `MeterProvider` MUST implement the Get a Meter API. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:74-125 (ПолучитьМетр(ИмяБиблиотеки, ВерсияБиблиотеки = "", АтрибутыОбласти = Неопределено, АдресСхемы = "")), 59-61 (ПостроительМетра); src/Метрики/Классы/ОтелПостроительМетра.os:26-64 (УстановитьВерсию, УстановитьАдресСхемы, УстановитьАтрибутыОбласти, Построить)` |  |
| 7 | MUST | ✅ found | The input provided by the user MUST be used to create an `InstrumentationScope` instance which is stored on the created `Meter`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:84-85 (Новый ОтелОбластьИнструментирования(ИмяБиблиотеки, ВерсияБиблиотеки, АтрибутыОбласти, АдресСхемы)), 103-106 (область передается в новый метр); src/Ядро/Классы/ОтелОбластьИнструментирования.os:164-169; src/Метрики/Классы/ОтелМетр.os:1100 (УстановитьОбластьИнструментирования), 362-364 (ОбластьИнструментирования()); tests/unit/Метрики/ТестПровайдерМетрик.os:63-88` |  |
| 8 | MUST | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the ... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:79-125 (невалидное имя не прерывает создание - возвращается рабочий ОтелМетр); src/Ядро/Классы/ОтелОбластьИнструментирования.os:61-79 (Ключ безопасен к Неопределено); src/Экспорт/Классы/ОтелЭкспортерМетрик.os:370-375 (экспорт области с невалидным именем без ошибки); tests/unit/Метрики/ТестПровайдерМетрик.os:475-504,653-663` |  |
| 9 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the ... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:84-85 (ИмяБиблиотеки передается в область без замены); src/Ядро/Классы/ОтелОбластьИнструментирования.os:164-165 (УстановитьИмя(Имя) - имя сохраняется как передано, включая Неопределено и ""), 53-79 (Ключ() не перезаписывает поля)` |  |
| 10 | SHOULD | ✅ found | In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be returned as a fallback rather than returning null or throwing an exception, its `name` SHOULD keep the ... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:79-83 (Лог.Предупреждение о невалидном имени инструментирующей библиотеки)` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | Configuration (i.e. MetricExporters, MetricReaders, Views, and (Development) MeterConfigurator and (Development) view_matching_mode) MUST be owned by the `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:20-31 (Представления, ФильтрЭкземпляров, ЧитательМетрик/ЧитателиМетрик, АгрегацияГистограммПоУмолчанию, ТаймаутОбратныхВызововМс - поля провайдера), 429-464 (читатели регистрируются при создании провайдера), 103-114 (метры получают конфигурацию от провайдера); src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:42-45,57-63,84-90; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:7-8,754-756 (экспортер принадлежит читателю провайдера), 354-363 (читатель регистрируется только у одного провайдера)` |  |
| 12 | MUST | ✅ found | If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:266-288 (ЗарегистрироватьПредставление), 306-318 (УстановитьАгрегациюГистограммПоУмолчанию), 327-339 (УстановитьТаймаутОбратныхВызововМс) - обход Метрики.Значения() под БлокировкаМетрик; src/Метрики/Классы/ОтелМетр.os:301-317,325-328,406-416,489-514 (повторное разрешение потоков созданных инструментов); tests/unit/Метрики/ТестКонвейерМетрик.os:123-143; tests/unit/Метрики/ТестПровайдерМетрик.os:1007-1021` |  |
| 13 | MUST NOT | ✅ found | If configuration is updated (e.g., adding a `MetricReader`), the updated configuration MUST also apply to all already returned `Meters` (i.e. it MUST NOT matter whether a `Meter` was obtained from the... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:99-120 (новый метр получает текущую конфигурацию под БлокировкаМетрик), 272-287,307-317,328-338 (ранее выданные метры обновляются под той же блокировкой); tests/unit/Метрики/ТестПровайдерМетрик.os:1007-1021 (ранее выданный и новый метр получают одинаковую конфигурацию); tests/unit/Метрики/ТестКонвейерМетрик.os:123-143` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MeterProvider` instance. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:188-191 (Закрыт.СравнитьИУстановить: повторный вызов не выполняет Shutdown повторно); tests/unit/Метрики/ТестПровайдерМетрик.os:426-443,521-534` |  |
| 15 | SHOULD | ✅ found | SDKs SHOULD return a valid no-op Meter for these calls, if possible. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:86-88,121-123,405-409 (НоопМетр - выключенный ОтелМетр, не регистрируется в читателях); src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:76-79 (запись игнорируется у выключенного метра); src/Метрики/Классы/ОтелМетр.os:446-450 (выключенный метр не дает данных); tests/unit/Метрики/ТестПровайдерМетрик.os:640-650,910-924` |  |
| 16 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:188-219 (Закрыть возвращает ОтелРезультатЗакрытия), 254-257 (ЗакрытьАсинхронно возвращает Обещание); src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-40 (Успешно/ИстекТаймаут/Описание); src/Ядро/Модули/ОтелРезультатыЗакрытия.os:239-260 (Свести: ошибка/таймаут/успех); tests/unit/Метрики/ТестПровайдерМетрик.os:703-718,850-863,888-907` |  |
| 17 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:188-219 (Закрыть(ТаймаутМс = 30000): каждому читателю передается оставшееся время, после срока - 1 мс, при истечении срока возвращается Таймаут); src/Ядро/Модули/ОтелРезультатыЗакрытия.os:159-177 (ОставшеесяВремя, СрокИстек); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:149-175 (ожидание фонового задания, финальный сбор и Закрыть экспортера в пределах срока), 399-417 (БлокировкаСбора.Захватить(срок)), 429-469 (callback-и и продюсеры в пределах срока), 484-503 (экспорт в пределах срока); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:412-432 (ТаймаутДоСрока для callback-ов); tests/unit/Метрики/ТестПровайдерМетрик.os:866-907` |  |
| 18 | MUST | ✅ found | `Shutdown` MUST be implemented at least by invoking `Shutdown` on all registered MetricReader and MetricExporter instances. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:200-217 (Закрыть у каждого читателя, в т.ч. после исключения и истечения срока); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:171-173 (читатель закрывает свой экспортер); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:240-253 (pull-читатель Prometheus); tests/unit/Метрики/ТестПровайдерМетрик.os:178-197,446-472,888-907` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 19 | MUST | ✅ found | `ForceFlush` MUST invoke `ForceFlush` on all registered MetricReader instances that implement `ForceFlush`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:176-178,229-234,354-365 (СброситьЧитателей: ПринудительноВыгрузитьСРезультатом или СброситьБуфер у каждого читателя, в т.ч. после исключения и истечения срока); src/Ядро/Модули/ОтелРезультатыЗакрытия.os:216-226; tests/unit/Метрики/ТестПровайдерМетрик.os:151-175,930-1004` |  |
| 20 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:176-178 (СброситьБуфер возвращает ОтелРезультатЭкспорта), 229-234 (ПринудительноВыгрузитьСРезультатом возвращает ОтелРезультатЗакрытия), 242-246 (СброситьБуферАсинхронно возвращает Обещание); src/Ядро/Классы/ОтелРезультатЭкспорта.os:17-36 (Успешно/ИстекТаймаут/Статус); src/Ядро/Модули/ОтелРезультатыЭкспорта.os:84-92 (успех/таймаут/ошибка); tests/unit/Метрики/ТестПровайдерМетрик.os:975-986` |  |
| 21 | SHOULD | ✅ found | `ForceFlush` SHOULD return some ERROR status if there is an error condition; and if there is no error condition, it should return some NO ERROR status, language implementations MAY decide how to model... | `src/Ядро/Модули/ОтелРезультатыЗакрытия.os:216-226 (исключение читателя возвращается ошибкой), 239-260 (Свести: ошибка при сбое любого читателя, иначе таймаут или успех); src/Ядро/Модули/ОтелРезультатыЭкспорта.os:18-39,84-92; src/Метрики/Классы/ОтелПровайдерМетрик.os:176-178,229-234; tests/unit/Метрики/ТестПровайдерМетрик.os:787-844` |  |
| 22 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:176-178,229-234 (ТаймаутМс; у ПринудительноВыгрузитьСРезультатом по умолчанию 30000 мс), 354-365 (ВызватьВПределахСрока с оставшимся временем, Таймаут при истечении срока); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:187-205 (ForceFlush читателя и экспортера в пределах срока, по умолчанию 30000 мс), 399-417, 429-469, 484-503, 827-832; src/Ядро/Классы/ОтелБлокировкаСТаймаутом.os:20-30; tests/unit/Метрики/ТестПровайдерМетрик.os:930-986` |  |

#### View

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#view)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | MUST | ✅ found | The SDK MUST provide functionality for a user to create Views for a `MeterProvider`. | `src/Метрики/Классы/ОтелПредставление.os:132-181 (View - конфигурация потока: НовоеИмя, НовоеОписание, ключи атрибутов, ГраницыГистограммы, Агрегация, РезервуарЭкземпляров, ЛимитМощностиАгрегации); src/Метрики/Классы/ОтелСелекторИнструментов.os:145-174 (критерии выбора инструментов); src/Метрики/Классы/ОтелПровайдерМетрик.os:266-288 (ЗарегистрироватьПредставление)` |  |
| 24 | MUST | ✅ found | This functionality MUST accept as inputs the Instrument selection criteria and the resulting stream configuration. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:266-269 (ЗарегистрироватьПредставление(Селектор, Представление)); src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:57-63; src/Метрики/Классы/ОтелСелекторИнструментов.os:37-65,164-174 (имя, вид, единица инструмента, имя/версия/адрес схемы метра); src/Метрики/Классы/ОтелПредставление.os:162-181; src/Метрики/Модули/ОтелПотокиМетрик.os:190-205,246-256 (селектор выбирает инструменты, конфигурация View применяется к потоку)` |  |
| 25 | MUST | ✅ found | The SDK MUST provide the means to register Views with a `MeterProvider`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:266-288 (ЗарегистрироватьПредставление); src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:57-63,84-90; tests/unit/Метрики/ТестПровайдерМетрик.os:275-290` |  |

#### Instrument selection criteria

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-selection-criteria)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | SHOULD | ✅ found | Criteria SHOULD be treated as additive. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:37-65 (Совпадает: любой заданный и несовпавший критерий возвращает Ложь - логическое И всех критериев)` |  |
| 27 | MUST | ✅ found | The SDK MUST accept the following criteria: | `src/Метрики/Классы/ОтелСелекторИнструментов.os:164-174 (ПриСозданииОбъекта(Имя, ТипИнструмента, ИмяМетра, Единица, ВерсияМетра, АдресСхемыМетра) - name, type, meter_name, unit, meter_version, meter_schema_url), 37-65 (Совпадает: сравнение по каждому критерию); src/Метрики/Модули/ОтелПотокиМетрик.os:190-205 (СовпавшиеПредставления передает селектору имя/вид/единицу инструмента и имя/версию/адрес схемы метра)` |  |
| 28 | MUST | ✅ found | If the SDK does not support wildcards in general, it MUST still recognize the special single asterisk (`*`) character as matching all Instruments. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:40-42 (Имя = "*" пропускает проверку имени - совпадение со всеми инструментами)` |  |
| 29 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:164 (Имя = Неопределено), 40 (критерий проверяется только если задан)` |  |
| 30 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `type`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:164 (ТипИнструмента = Неопределено), 44 (критерий проверяется только если задан)` |  |
| 31 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `unit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:165 (Единица = Неопределено), 52 (критерий проверяется только если задан)` |  |
| 32 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:165 (ИмяМетра = Неопределено), 48 (критерий проверяется только если задан)` |  |
| 33 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_version`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:166 (ВерсияМетра = Неопределено), 56 (критерий проверяется только если задан)` |  |
| 34 | MUST NOT | ✅ found | Therefore, the instrument selection criteria parameter needs to be structured to accept a `meter_schema_url`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:166 (АдресСхемыМетра = Неопределено), 60 (критерий проверяется только если задан)` |  |
| 35 | MUST NOT | ✅ found | Therefore, the instrument selection criteria can be structured to accept the criteria, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелСелекторИнструментов.os:164-166 (все параметры селектора необязательны, по умолчанию Неопределено; обязательных дополнительных критериев нет)` |  |

#### Stream configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#stream-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | The SDK MUST accept the following stream configuration parameters: | `src/Метрики/Классы/ОтелПредставление.os:162-181 (ПриСозданииОбъекта: НовоеИмя, НовоеОписание, РазрешенныеКлючиАтрибутов, ИсключенныеКлючиАтрибутов, Агрегация, РезервуарЭкземпляров (фабрика), ЛимитМощностиАгрегации); src/Метрики/Модули/ОтелПотокиМетрик.os:246-256,288-354 (применение параметров View к потоку)` |  |
| 37 | SHOULD | ✅ found | `name`: The metric stream name that SHOULD be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:328-331 (Поток.Имя = Представление.НовоеИмя()), 470-474 (хранилище потока создается с Поток.Имя)` |  |
| 38 | SHOULD | ✅ found | In order to avoid conflicts, if a `name` is provided the View SHOULD have an instrument selector that selects at most one instrument. | `src/Метрики/Классы/ОтелМетр.os:301-317 (УстановитьПредставления проверяет селектор каждого View), 838-853 (ПроверитьУзостьСелектораView: предупреждение для View с НовоеИмя и селектором без точного Имя / с "*"), 866-898 (предупреждение о конфликте имен потоков)` |  |
| 39 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept a `name`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:163 (НовоеИмя = Неопределено)` |  |
| 40 | MUST | ✅ found | If the user does not provide a `name` value, name from the Instrument the View matches MUST be used by default. | `src/Метрики/Модули/ОтелПотокиМетрик.os:258-261 (НачальныйПоток: Имя = Дескриптор.Имя), 328-331 (переопределяется только при НовоеИмя <> Неопределено)` |  |
| 41 | MUST NOT | ✅ found | The `name` provided via stream configuration is NOT REQUIRED to conform to the instrument name syntax, and the SDK MUST NOT validate it against that syntax. | `src/Метрики/Модули/ОтелПотокиМетрик.os:328-331 (НовоеИмя присваивается потоку без проверки синтаксиса); src/Метрики/Классы/ОтелМетр.os:625,664,1061-1070 (ВалидироватьИмяИнструмента применяется только к имени инструмента при создании, не к НовоеИмя View)` |  |
| 42 | SHOULD | ✅ found | `description`: The metric stream description that SHOULD be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:332-334 (Поток.Описание = Представление.НовоеОписание()), 470-474` |  |
| 43 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept a `description`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:164 (НовоеОписание = Неопределено)` |  |
| 44 | MUST | ✅ found | If the user does not provide a `description` value, the description from the Instrument a View matches MUST be used by default. | `src/Метрики/Модули/ОтелПотокиМетрик.os:258-261 (НачальныйПоток: Описание = Дескриптор.Описание), 332-334 (переопределяется только при НовоеОписание <> Неопределено)` |  |
| 45 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:22-36,51-56 (Обработать/КлючСохраняется: ключи из allow-list сохраняются); src/Метрики/Модули/ОтелПотокиМетрик.os:252,477 (allow-list View передается хранилищу); src/Метрики/Классы/ОтелХранилищеМетрики.os:58; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:301 (фильтр применяется до агрегации)` |  |
| 46 | MUST | ✅ found | The allow-list contains attribute keys that identify the attributes that MUST be kept, and all other attributes MUST be ignored. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:51-54 (КлючСохраняется: ключ вне allow-list отбрасывается); src/Метрики/Классы/ОтелХранилищеМетрики.os:58-59 (серия строится по отфильтрованным атрибутам)` |  |
| 47 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept `attribute_keys`, but MUST NOT obligate a user to provide them. | `src/Метрики/Классы/ОтелПредставление.os:165 (РазрешенныеКлючиАтрибутов = Неопределено), 168 (ИсключенныеКлючиАтрибутов = Неопределено)` |  |
| 48 | MUST | ✅ found | If the `Attributes` advisory parameter is absent, all attributes MUST be kept. | `src/Метрики/Модули/ОтелПотокиМетрик.os:266-267 (Разрешенные/Исключенные = Неопределено по умолчанию); src/Метрики/Классы/ОтелОбработчикАтрибутов.os:26-28 (без allow/exclude-list возвращаются все атрибуты измерения)` |  |
| 49 | SHOULD | ✅ found | Additionally, implementations SHOULD support configuring an exclude-list of attribute keys. | `src/Метрики/Классы/ОтелПредставление.os:56-58,168 (ИсключенныеКлючиАтрибутов); src/Метрики/Модули/ОтелПотокиМетрик.os:253,477 (exclude-list передается хранилищу потока)` |  |
| 50 | MUST | ✅ found | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:55 (КлючСохраняется: ключ из exclude-list отбрасывается), 22-36 (Обработать)` |  |
| 51 | MUST | ✅ found | The exclude-list contains attribute keys that identify the attributes that MUST be excluded, all other attributes MUST be kept. | `src/Метрики/Классы/ОтелОбработчикАтрибутов.os:51-56 (КлючСохраняется: при отсутствии allow-list все ключи вне exclude-list сохраняются), 29-35` |  |
| 52 | SHOULD | ✅ found | SDK documentation SHOULD inform users that attributes excluded from a metric stream by View configuration may still be exported on Exemplars as filtered attributes, and describe how to disable or othe... | `src/Метрики/Классы/ОтелПредставление.os:142-145 (документирующий комментарий класса View: filteredAttributes и отключение через ОтелФильтрЭкземпляров.ВсегдаВыключен() / OTEL_METRICS_EXEMPLAR_FILTER=always_off / ОтелФабрикаNoopРезервуаров); docs/product/050-metrics.md:255-261; docs/api/Метрики/ОтелПредставление.md:34-38` |  |
| 53 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept an `aggregation`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:167 (Агрегация = Неопределено)` |  |
| 54 | MUST | ✅ found | If the user does not provide an `aggregation` value, the `MeterProvider` MUST apply a default aggregation configurable on the basis of instrument type according to the MetricReader instance. | `src/Метрики/Модули/ОтелПотокиМетрик.os:289-292 (без агрегации View поток не меняется), 366-370 (ЗавершитьПоток), 412-440 (АгрегацияЧитателя: Читатель.АгрегацияПоУмолчанию(Дескриптор.Вид)); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:302-314,322-324,759-777 (агрегация по умолчанию по виду инструмента, настраиваемая УстановитьАгрегациюПоУмолчанию); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:307-320` |  |
| 55 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept an `exemplar_reservoir`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:169 (РезервуарЭкземпляров = Неопределено)` |  |
| 56 | MUST | ✅ found | If the user does not provide an `exemplar_reservoir` value, the `MeterProvider` MUST apply a default exemplar reservoir. | `src/Метрики/Модули/ОтелПотокиМетрик.os:479-483 (СоздатьХранилище: без фабрики View - ФабрикаРезервуаровПоУмолчанию); src/Метрики/Модули/ОтелАгрегация.os:254-266 (ФабрикаРезервуаровПоУмолчанию: выровненный по бакетам для явной гистограммы, простой min(20, МаксБакетов) для экспоненциальной, простой размера 1 для остальных)` |  |
| 57 | MUST NOT | ✅ found | Therefore, the stream configuration parameter needs to be structured to accept an `aggregation_cardinality_limit`, but MUST NOT obligate a user to provide one. | `src/Метрики/Классы/ОтелПредставление.os:170 (ЛимитМощностиАгрегации = Неопределено)` |  |
| 58 | MUST | ✅ found | If the user does not provide an `aggregation_cardinality_limit` value, the `MeterProvider` MUST apply the default aggregation cardinality limit the `MetricReader` is configured with. | `src/Метрики/Модули/ОтелПотокиМетрик.os:375-377 (ЗавершитьПоток), 452-465 (ЛимитМощностиЧитателя: Читатель.ЛимитМощностиДляВида / ЛимитМощности); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:255-257,267-270,278-280; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:260-262,272-275` |  |

#### Measurement processing

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#measurement-processing)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 59 | SHOULD | ✅ found | The SDK SHOULD use the following logic to determine how to process Measurements made with an Instrument: | `src/Метрики/Модули/ОтелПотокиМетрик.os:111-125 (СоздатьХранилища: потоки для каждого читателя провайдера), 190-205 (СовпавшиеПредставления), 218-232 (ПотокиЧитателя: поток на каждый совпавший View, иначе поток по умолчанию); src/Метрики/Классы/ОтелМетр.os:477-502 (ОбновитьПотоки)` |  |
| 60 | MUST | ✅ found | Instrument advisory parameters, if any, MUST be honored. | `src/Метрики/Модули/ОтелПотокиМетрик.os:366-374 (ЗавершитьПоток), 391-399 (ГраницыПотока: advisory ГраницыГистограммы = ExplicitBucketBoundaries для агрегации по умолчанию), 538-546 (ЗначениеСовета); src/Метрики/Классы/ОтелМетр.os:1542-1573 (ПроверитьСовет)` |  |
| 61 | SHOULD | ✅ found | If applying the View results in conflicting metric identities the implementation SHOULD apply the View and emit a warning. | `src/Метрики/Модули/ОтелПотокиМетрик.os:218-225 (каждый совпавший View применяется и дает свой поток); src/Метрики/Классы/ОтелМетр.os:866-888 (ЗарегистрироватьИменаПотоков: обнаружение одноименных потоков одного читателя), 890-898 (ПредупредитьОКонфликтеПотоков: предупреждение, оба потока экспортируются)` |  |
| 62 | SHOULD | ✅ found | If applying the View would produce semantic errors (for example, configuring an asynchronous instrument to use the Explicit bucket histogram aggregation), the implementation SHOULD emit a warning and ... | `src/Метрики/Модули/ОтелПотокиМетрик.os:288-314 (ПрименитьАгрегацию: предупреждение для неизвестной/несовместимой агрегации), 246-250 (ПотокПредставления: View пропускается целиком), 226-230 (без применимых View - поток по умолчанию); src/Метрики/Модули/ОтелАгрегация.os:199-202 (СовместимаСВидом: гистограммы недопустимы для асинхронных инструментов)` |  |
| 63 | MUST | ✅ found | If both the View and Instrument advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Модули/ОтелПотокиМетрик.os:391-399 (ГраницыПотока: границы View приоритетнее, при агрегации из View advisory-границы не используются), 309-312 (АгрегацияИзПредставления), 335-337 (ГраницыГистограммы View)` |  |
| 64 | SHOULD | ✅ found | If the Instrument could not match with any of the registered `View`(s), the SDK SHOULD enable the instrument using the default aggregation and temporality. | `src/Метрики/Модули/ОтелПотокиМетрик.os:226-230 (ПотокиЧитателя: без совпавших View - поток по умолчанию), 412-440 (АгрегацияЧитателя), 162-175 (ВременнаяАгрегацияЧитателя); src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:129-131 (сбор с временной агрегацией читателя)` |  |

#### Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 65 | MUST | ✅ found | The SDK MUST provide the following `Aggregation` to support the Metric Points in the Metrics Data Model. | `src/Метрики/Модули/ОтелАгрегация.os:15-17 (ПоУмолчанию - Default), 25-27 (Сумма - Sum), 35-37 (ПоследнееЗначение - Last Value), 45-47 (Отбросить - Drop), 58-65 (ГистограммаСЯвнымиГраницами - Explicit Bucket Histogram), 180-187,406-417 (Default по виду инструмента), 215-240 (СоздатьАгрегаторПотока); агрегаторы src/Метрики/Классы/ОтелАгрегаторDrop.os, ОтелАгрегаторСуммы.os, ОтелАгрегаторПоследнегоЗначения.os, ОтелАгрегаторГистограммы.os` |  |
| 66 | SHOULD | ✅ found | The SDK SHOULD provide the following `Aggregation`: | `src/Метрики/Модули/ОтелАгрегация.os:76-81 (ГистограммаЭкспоненциальная - Base2 Exponential Bucket Histogram), 232-237 (СоздатьАгрегаторПотока); src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:1-431` |  |

#### Histogram Aggregations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#histogram-aggregations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 67 | SHOULD NOT | ✅ found | This SHOULD NOT be collected when used with instruments that record negative measurements (e.g. `UpDownCounter` or `ObservableGauge`). | `src/Метрики/Модули/ОтелАгрегация.os:218 (СобиратьSum = НЕ ЗаписываетОтрицательные(Вид)), 276-279 (ЗаписываетОтрицательные: UpDownCounter, Gauge, ObservableUpDownCounter, ObservableGauge), 229,234-235 (флаг передается агрегаторам гистограмм); src/Метрики/Классы/ОтелАгрегаторГистограммы.os:66-68,142-144; src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:78-80,106-108 (sum не накапливается и не попадает в точку данных)` |  |

#### Explicit Bucket Histogram Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#explicit-bucket-histogram-aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 68 | SHOULD | ✅ found | SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good reasons to use something different (e.g. for backward compatibility reasons in a stable SDK release... | `src/Метрики/Классы/ОтелАгрегаторГистограммы.os:172-190 (СтандартныеГраницы: [0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000]), 262-263 (используются, если границы не заданы); src/Метрики/Модули/ОтелПотокиМетрик.os:371-374,391-399 (без границ View/advisory границы остаются Неопределено)` |  |

#### Handle all normal values

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#handle-all-normal-values)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 69 | SHOULD NOT | ➖ n_a | Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the `sum`, `min`, and `max` fields, because these values do not map into a valid bucket. | - | Ограничение платформы OneScript: Число = System.Decimal (не IEEE 754) - значения NaN, +Inf, -Inf непредставимы в типе Число, а операции, которые в IEEE 754 дали бы такие значения, выбрасывают исключение. Такие значения не могут попасть в аккумуляторы sum/min/max гистограмм (ОтелАгрегаторЭкспоненциальнойГистограммы.Записать), поэтому требование неприменимо на этой платформе. |

#### Support a minimum and maximum scale

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#support-a-minimum-and-maximum-scale)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 70 | MUST | ✅ found | The implementation MUST maintain reasonable minimum and maximum scale parameters that the automatic scale parameter will not exceed. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:313-324 (ПонизитьШкалуНа1: МинимальнаяШкала = -10, ниже не понижается), 240-244 (на минимальной шкале понижение прекращается), 44,125-127,414-427 (шкала начинается и сбрасывается к НачальнаяШкала = MaxScale, по умолчанию 20, автоматически только понижается); src/Метрики/Модули/ОтелАгрегация.os:322-330 (МаксШкала = 20 по умолчанию), 352 (МаксШкала >= -10), 234-235 (MaxScale передается агрегатору)` |  |

#### Use the maximum scale for single measurements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#use-the-maximum-scale-for-single-measurements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 71 | SHOULD | ✅ found | When the histogram contains not more than one value in either of the positive or negative ranges, the implementation SHOULD use the maximum scale. | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:44 (СоздатьАккумулятор: scale = НачальнаяШкала = MaxScale, по умолчанию 20), 213-216 (ДобавитьВБакеты: первое значение диапазона - один бакет без понижения шкалы), 123-127 (СформироватьТочкуДанных: count<=1 -> scale = НачальнаяШкала); src/Метрики/Модули/ОтелАгрегация.os:232-236 (МаксШкала передается агрегатору как начальная шкала)` |  |

#### Maintain the ideal scale

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#maintain-the-ideal-scale)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 72 | SHOULD | ✅ found | Implementations SHOULD adjust the histogram scale as necessary to maintain the best resolution possible, within the constraint of maximum size (max number of buckets). | `src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:231-262 (ПонизитьШкалуПриНеобходимости: шкала понижается на 1 только пока диапазон бакетов не помещается в МаксБакетов), 313-324 (ПонизитьШкалуНа1), 326-353 (ПонизитьБакеты)` |  |

#### Observations inside asynchronous callbacks

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#observations-inside-asynchronous-callbacks)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 73 | MUST | ✅ found | Callback functions MUST be invoked for the specific `MetricReader` performing collection, such that observations made or produced by executing callbacks only apply to the intended `MetricReader` durin... | `src/Метрики/Классы/ОтелМетр.os:440-471 (СобратьДляЧитателя: мульти-callback-и вызываются в сборе конкретного читателя), 738-747 (НаблюденияМультиОбратныхВызовов); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:257-279 (СобратьДляЧитателя: callback-и вызываются для читателя, наблюдения применяются только к ХранилищаЧитателя); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:628-632; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:375` |  |
| 74 | SHOULD | ✅ found | The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered callbacks. | `src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:180-200 (ДобавитьВнешниеНаблюдения: вне callback-контекста наблюдения игнорируются с предупреждением), 394-414 (ВызватьCallbackи: флаг ВыполняетсяCallback); src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:56-64 (новый ОтелНаблюдениеМетрики на каждый вызов callback)` |  |
| 75 | SHOULD | ⚠️ partial | The implementation SHOULD use a timeout to prevent indefinite callback execution. | `src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:121-165 (ВызватьСТаймаутом: ФоновыеЗадания.Выполнить + ОжидатьЗавершения(ТаймаутМс)), 182-192 (ЗаданиеВыполняется); src/Метрики/Классы/ОтелМетр.os:406-416,1035 (таймаут callback-ов, по умолчанию 30000 мс)` | Таймаут реализован как soft-timeout: ОтелИсполнительОбратныхВызовов.ВызватьСТаймаутом запускает callback через ФоновыеЗадания.Выполнить и ждет Задание.ОжидатьЗавершения(ТаймаутМс) (по умолчанию 30000 мс у ОтелМетр/ОтелПровайдерМетрик); по истечении сбор перестает ждать, измерения отбрасываются с предупреждением в лог и таймаутом в результате сбора. Само выполнение callback не прерывается: у ФоновоеЗадание в OneScript нет Прервать()/ОтменитьЗадание() (https://github.com/EvilBeaver/OneScript/issues/1672), задание продолжает работу в фоне; SDK лишь не вызывает этот callback повторно до завершения задания. Предотвращается неограниченное ожидание сбора, но не неограниченное выполнение callback. |
| 76 | MUST | ⚠️ partial | The implementation MUST complete the execution of all callbacks for a given instrument before starting a subsequent round of collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:399-417 (БлокировкаСбора сериализует сборы); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:159-169 (БлокировкаСбора); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:394-414 (ВызватьCallbackи - синхронный цикл); src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:121-165` | В штатном режиме выполняется: сборы одного читателя сериализованы (БлокировкаСбора в ОтелПериодическийЧитательМетрик и ОтелПрометеусЧитательМетрик), callback-и инструмента вызываются внутри сбора синхронно (inline при таймауте 0 или с ожиданием ОжидатьЗавершения). Но при срабатывании soft-timeout фоновое задание callback продолжает выполняться (OneScript не может прервать ФоновоеЗадание, issue #1672), и следующий раунд сбора начинается до завершения этого callback - это прямо зафиксировано тестом ТестМетр.ЗависшийОбратныйВызовНеЗапускаетсяПовторно («второй сбор начинается, пока задание первого еще выполняется»). SDK лишь пропускает повторный вызов такого callback и отбрасывает его результат, но не гарантирует завершение его выполнения до начала следующего сбора. |
| 77 | SHOULD NOT | ✅ found | The implementation SHOULD NOT produce aggregated metric data for a previously-observed attribute set which is not observed during a successful callback. | `src/Метрики/Классы/ОтелХранилищеНаблюдений.os:222-266 (СобратьТочки/СгруппироватьНаблюдения: серии строятся заново только из наблюдений текущего сбора); src/Метрики/Классы/ОтелИсполнительОбратныхВызовов.os:121-165 (наблюдения упавшего или просроченного callback отбрасываются)` |  |

#### Cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 78 | SHOULD | ✅ found | SDKs SHOULD support being configured with a cardinality limit. | `src/Метрики/Классы/ОтелПредставление.os:92-94,170,180 (ЛимитМощностиАгрегации View); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:255-280,739,750 (лимит читателя и лимит по виду инструмента); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:260-285; src/Метрики/Классы/ОтелМетр.os:382-384` |  |
| 79 | SHOULD | ✅ found | Cardinality limit enforcement SHOULD occur after attribute filtering, if any. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:58-65 (ОбработчикАтрибутов.Обработать до выбора серии), 315-329 (СерияДляЗаписи: лимит проверяется по ключу отфильтрованных атрибутов); src/Метрики/Классы/ОтелХранилищеНаблюдений.os:299-315 (ДобавитьНаблюдение)` |  |

#### Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 80 | SHOULD | ✅ found | A view with criteria matching the instrument an aggregation is created for has an `aggregation_cardinality_limit` value defined for the stream, that value SHOULD be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:338-340 (ПрименитьНастройкиПредставления: ЛимитМощностиАгрегации View), 476 (СоздатьХранилище: УстановитьЛимитМощности); src/Метрики/Классы/ОтелПредставление.os:92-94` |  |
| 81 | SHOULD | ✅ found | If there is no matching view, but the `MetricReader` defines a default cardinality limit value based on the instrument an aggregation is created for, that value SHOULD be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:375-377 (ЗавершитьПоток), 452-465 (ЛимитМощностиЧитателя: Читатель.ЛимитМощностиДляВида(Вид)); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:267-280; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:272-285` |  |
| 82 | SHOULD | ✅ found | If none of the previous values are defined, the default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:739,750 (НовыйЛимитМощности = 2000); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1869; src/Метрики/Модули/ОтелПотокиМетрик.os:26,31; src/Метрики/Классы/ОтелХранилищеМетрики.os:560,568; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:441,449` |  |

#### Overflow attribute

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#overflow-attribute)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 83 | MUST | ✅ found | The SDK MUST create an Aggregator with the overflow attribute set prior to reaching the cardinality limit and use it to aggregate Measurements for which the correct Aggregator could not be created. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:315-329 (СерияДляЗаписи: серия переполнения агрегирует измерения наборов сверх лимита), 539-547 (КлючПереполнения, АтрибутыПереполнения: otel.metric.overflow=true); src/Метрики/Классы/ОтелХранилищеНаблюдений.os:303-315,420-428` |  |
| 84 | MUST | ✅ found | The SDK MUST provide the guarantee that overflow would not happen if the maximum number of distinct, non-overflow attribute sets is less than or equal to the limit. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:315-329 (переполнение только для нового набора при Серии.Количество() >= ЛимитМощности, серия переполнения в Серии не входит); src/Метрики/Классы/ОтелХранилищеНаблюдений.os:303-315` |  |

#### Synchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#synchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 85 | MUST | ✅ found | Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attribute sets that were observed prior to the beginning of overflow. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:315-319 (СерияДляЗаписи: существующая серия выбирается до проверки лимита), 360-388 (СнимокИнтервала: кумулятивный сбор сохраняет серии), 139-153 (ОчиститьТочкиДанных: для кумулятивной серии не сбрасываются)` |  |
| 86 | MUST | ✅ found | Regardless of aggregation temporality, the SDK MUST ensure that every Measurement is reflected in exactly one Aggregator, which is either an Aggregator associated with the correct attribute set or an ... | `src/Метрики/Классы/ОтелХранилищеМетрики.os:54-75 (Записать: выбор серии и агрегация под одной блокировкой), 315-329 (СерияДляЗаписи: ровно одна серия - своего набора или переполнения)` |  |
| 87 | MUST NOT | ✅ found | Measurements MUST NOT be double-counted or dropped during an overflow. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:54-75,315-329,360-388 (запись и смена дельта-интервала под одной блокировкой: каждое измерение попадает ровно в одну серию одного интервала)` |  |

#### Asynchronous instrument cardinality limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#asynchronous-instrument-cardinality-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 88 | SHOULD | ✅ found | Aggregators of asynchronous instruments SHOULD prefer the first-observed attributes in the callback when limiting cardinality, regardless of temporality. | `src/Метрики/Классы/ОтелХранилищеНаблюдений.os:251-266 (СгруппироватьНаблюдения: наблюдения в порядке callback-ов и записей), 299-315 (ДобавитьНаблюдение: свои серии получают первые ЛимитМощности наборов, остальные - серия переполнения, независимо от временности)` |  |

#### Meter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#meter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 89 | MUST | ✅ found | Distinct meters MUST be treated as separate namespaces for the purposes of detecting duplicate instrument registrations. | `src/Метрики/Классы/ОтелМетр.os:1019-1021 (реестры ИнструментыПоИмени/ДескрипторыИнструментов/ИнструментыПроходНасквозь - поля экземпляра метра), 1143-1154 (НайтиЗарегистрированныйИнструмент ищет только в реестре своего метра); src/Метрики/Классы/ОтелПровайдерМетрик.os:89-115 (отдельный ОтелМетр на ключ области); src/Ядро/Классы/ОтелОбластьИнструментирования.os:61-79 (Ключ: имя, версия, schema_url, атрибуты)` |  |

#### Duplicate instrument registration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#duplicate-instrument-registration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 90 | MUST | ✅ found | This means that the Meter MUST return a functional instrument that can be expected to export data even if this will cause semantic error in the data model. | `src/Метрики/Классы/ОтелМетр.os:1143-1154 (НайтиЗарегистрированныйИнструмент: при конфликте описания/advisory - первый инструмент, при конфликте вида/единицы - pass-through), 1237-1273 (ЗарегистрироватьПодБлокировкой: инструмент запрошенного вида с собственными потоками добавляется в Инструменты и собирается читателями), 622-645, 662-685` |  |
| 91 | SHOULD | ✅ found | Therefore, when a duplicate instrument registration occurs, and it is not corrected with a View, a warning SHOULD be emitted. | `src/Метрики/Классы/ОтелМетр.os:1312-1366 (ПроверитьКонфликтДескриптора: Лог.Предупреждение; пропуск предупреждения при исправлении через View - 1337-1348), 1435-1439 (КонфликтИсправленПереименованием)` |  |
| 92 | SHOULD | ✅ found | The emitted warning SHOULD include information for the user on how to resolve the conflict, if possible. | `src/Метрики/Классы/ОтелМетр.os:1360-1365 (рецепт включается в текст предупреждения), 1667-1693 (ПостроитьРецептРазрешенияКонфликта)` |  |
| 93 | SHOULD | ✅ found | If the potential conflict involves multiple `description` properties, setting the `description` through a configured View SHOULD avoid the warning. | `src/Метрики/Классы/ОтелМетр.os:1343-1348 (ТолькоКонфликтОписания + ОписаниеЗаданоЧерезView - предупреждение не выдается), 1633-1648 (ОписаниеЗаданоЧерезView: View с НовоеОписание, селектор по имени без учета регистра, виду и единице)` |  |
| 94 | SHOULD | ✅ found | If the potential conflict involves instruments that can be distinguished by a supported View selector (e.g. name, instrument kind) a renaming View recipe SHOULD be included in the warning. | `src/Метрики/Классы/ОтелМетр.os:1667-1680 (ПостроитьРецептРазрешенияКонфликта: View с селектором Имя+ТипИнструмента или Имя+Единица и НовоеИмя='<уникальное_имя>')` |  |
| 95 | SHOULD | ✅ found | Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Metric` objects and emit a generic warning describing the duplicate instrument registration. | `src/Метрики/Классы/ОтелМетр.os:1149-1153, 1244-1250 (pass-through инструмент по ключу имя|вид|единица), 1472-1478 (ЕстьНесовместимыйКонфликт), 1350-1365 (предупреждение с различиями регистраций), 1378-1400 (РазличияРегистраций)` |  |
| 96 | MUST | ✅ found | To accommodate the recommendations from the data model, the SDK MUST aggregate data from identical Instruments together in its export pipeline. | `src/Метрики/Классы/ОтелМетр.os:1143-1154, 1238-1243 (идентичная регистрация возвращает тот же экземпляр с теми же хранилищами), 671, 972-983 (ДобавитьCallbackСуществующему: callback-и повторного асинхронного инструмента регистрируются у первого экземпляра); src/Метрики/Классы/ОтелПровайдерМетрик.os:92-95 (идентичный метр - тот же экземпляр)` |  |

#### Name conflict

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#name-conflict)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 97 | MUST | ✅ found | When this happens, the Meter MUST return an instrument using the first-seen instrument name and log an appropriate error as described above. | `src/Метрики/Классы/ОтелМетр.os:628,667 (имя нормализуется НРег для поиска), 1149-1150 (возврат первого инструмента), 1167-1173 (ИмяПервойРегистрации - первое встреченное имя и для pass-through), 1318-1326 (Лог.Предупреждение 'Instrument name conflict (case-only)' с обоими именами)` |  |

#### Instrument name

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-name)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 98 | SHOULD | ✅ found | When a Meter creates an instrument, it SHOULD validate the instrument name conforms to the instrument name syntax | `src/Метрики/Классы/ОтелМетр.os:625,664 (вызов при создании синхронных и асинхронных инструментов), 1061-1070 (ВалидироватьИмяИнструмента), 1081-1119 (ИмяИнструментаВалидно: [A-Za-z][A-Za-z0-9_./-]{0,254})` |  |
| 99 | SHOULD | ✅ found | If the instrument name does not conform to this syntax, the Meter SHOULD emit an error notifying the user about the invalid name. | `src/Метрики/Классы/ОтелМетр.os:1065-1069 (Лог.Предупреждение с невалидным именем и требуемым синтаксисом)` |  |

#### Instrument unit

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-unit)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 100 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument unit. | `src/Метрики/Классы/ОтелМетр.os:627,666,1040-1045 (НормализоватьСтроку - только замена Неопределено на пустую строку, без проверки формата/длины единицы)` |  |
| 101 | MUST | ✅ found | If a unit is not provided or the unit is null, the Meter MUST treat it the same as an empty unit string. | `src/Метрики/Классы/ОтелМетр.os:80,96,113,131,146,180,216,251 (ЕдиницаИзмерения = "" по умолчанию), 627,666,1040-1045 (НормализоватьСтроку: Неопределено -> "")` |  |

#### Instrument description

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-description)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 102 | SHOULD NOT | ✅ found | When a Meter creates an instrument, it SHOULD NOT validate the instrument description. | `src/Метрики/Классы/ОтелМетр.os:626,665,1040-1045 (НормализоватьСтроку - без проверки содержимого/длины описания)` |  |
| 103 | MUST | ✅ found | If a description is not provided or the description is null, the Meter MUST treat it the same as an empty description string. | `src/Метрики/Классы/ОтелМетр.os:80,96,113,131,146,180,216,251 (Описание = "" по умолчанию), 626,665,1040-1045 (НормализоватьСтроку: Неопределено -> "")` |  |

#### Instrument advisory parameters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameters)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 104 | SHOULD | ✅ found | When a Meter creates an instrument, it SHOULD validate the instrument advisory parameters. | `src/Метрики/Классы/ОтелМетр.os:635,675 (вызов при создании инструмента), 1542-1573 (ПроверитьСовет), 1575-1587 (ГраницыВозрастают)` |  |
| 105 | SHOULD | ✅ found | If an advisory parameter is not valid, the Meter SHOULD emit an error notifying the user and proceed as if the parameter was not provided. | `src/Метрики/Классы/ОтелМетр.os:1547-1567 (Лог.Предупреждение и сброс невалидного поля/Совета в Неопределено); src/Метрики/Модули/ОтелПотокиМетрик.os:538-546 (ЗначениеСовета - без валидных границ применяются границы по умолчанию)` |  |
| 106 | MUST | ✅ found | If multiple identical Instruments are created with different advisory parameters, the Meter MUST return an instrument using the first-seen advisory parameters and log an appropriate error as described... | `src/Метрики/Классы/ОтелМетр.os:1143-1154 (возврат первого инструмента), 1472-1478 (ЕстьНесовместимыйКонфликт: advisory не делает конфликт несовместимым), 1328-1332,1350-1365 (Конфликт.Совета -> предупреждение с различием advisory и рецептом), 1480-1492 (СоветыРавны)` |  |
| 107 | MUST | ✅ found | If both a View and advisory parameters specify the same aspect of the Stream configuration, the setting defined by the View MUST take precedence over the advisory parameters. | `src/Метрики/Модули/ОтелПотокиМетрик.os:326-337 (ПрименитьНастройкиПредставления - границы View), 366-379 (ЗавершитьПоток), 391-399 (ГраницыПотока: границы View, затем агрегация View без advisory, затем advisory)` |  |

#### Instrument advisory parameter: `ExplicitBucketBoundaries`

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-advisory-parameter-explicitbucketboundaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 108 | MUST | ✅ found | If no View matches, or if a matching View selects the default aggregation, the `ExplicitBucketBoundaries` advisory parameter MUST be used. | `src/Метрики/Модули/ОтелПотокиМетрик.os:218-232 (без совпавших View - поток по умолчанию), 309-312 (View с default-агрегацией не выставляет АгрегацияИзПредставления), 366-379 (ЗавершитьПоток), 391-399 (ГраницыПотока - advisory-границы), 538-546 (ЗначениеСовета); src/Метрики/Классы/ОтелАгрегаторГистограммы.os:262-263 (без границ - границы по умолчанию)` |  |

#### Instrument enabled

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#instrument-enabled)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 109 | MUST | ✅ found | The synchronous instrument `Enabled` MUST return `false` when either: * Status: Development - The MeterConfig of the `Meter` used to create the instrument has parameter `enabled=false`.* All resolved ... | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:250-253,322-333; src/Метрики/Классы/ОтелАгрегаторDrop.os:76-78; src/Метрики/Классы/ОтелМетр.os:477-502` |  |
| 110 | SHOULD | ✅ found | Otherwise, it SHOULD return `true`. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:250-253,358-359; src/Метрики/Модули/ОтелПотокиМетрик.os:226-230` |  |

#### Exemplar

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 111 | MUST | ✅ found | A Metric SDK MUST provide a mechanism to sample `Exemplar`s from measurements via the `ExemplarFilter` and `ExemplarReservoir` hooks. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:68-88; src/Метрики/Классы/ОтелХранилищеМетрики.os:54-75,420-434,482-493; src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:52-120` |  |
| 112 | SHOULD | ✅ found | `Exemplar` sampling SHOULD be turned on by default. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:440-444; src/Метрики/Модули/ОтелПотокиМетрик.os:32,478-483; src/Метрики/Модули/ОтелАгрегация.os:254-266` |  |
| 113 | MUST NOT | ✅ found | If `Exemplar` sampling is off, the SDK MUST NOT have overhead related to exemplar sampling. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:54-61,259-269,450-471; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:357-382` |  |
| 114 | MUST | ✅ found | A Metric SDK MUST allow exemplar sampling to leverage the configuration of metric aggregation. | `src/Метрики/Модули/ОтелАгрегация.os:254-266; src/Метрики/Модули/ОтелПотокиМетрик.os:467-485; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:163-170` |  |
| 115 | SHOULD | ✅ found | A Metric SDK SHOULD provide configuration for Exemplar sampling, specifically: * `ExemplarFilter`: filter which measurements can become exemplars.* `ExemplarReservoir`: storage and sampling of exempla... | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:74-77,114-129; src/Метрики/Классы/ОтелПровайдерМетрик.os:429-444; src/Метрики/Классы/ОтелПредставление.os:83-85,156-157,169; src/Метрики/Модули/ОтелПотокиМетрик.os:341-353` |  |

#### ExemplarFilter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarfilter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 116 | MUST | ✅ found | The `ExemplarFilter` configuration MUST allow users to select between one of the built-in ExemplarFilters. | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14-55; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:74-77; src/Метрики/Классы/ОтелПровайдерМетрик.os:429-444` |  |
| 117 | SHOULD | ✅ found | The ExemplarFilter SHOULD be a configuration parameter of a `MeterProvider` for an SDK. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:103-106,151-153,429-444; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:74-77,84-85` |  |
| 118 | SHOULD | ✅ found | The default value SHOULD be `TraceBased`. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:440-441; src/Метрики/Классы/ОтелМетр.os:1022-1023; src/Конфигурация/Классы/ОтелКонфигурацияПровайдераМетрик.os:22` |  |
| 119 | SHOULD | ✅ found | The filter configuration SHOULD follow the environment variable specification. | `src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114-129; src/Метрики/Модули/ОтелФильтрЭкземпляров.os:46-55; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:380,922-932; docs/env-variables.md:174` |  |
| 120 | MUST | ✅ found | An OpenTelemetry SDK MUST support the following filters: * AlwaysOn* AlwaysOff* TraceBased | `src/Метрики/Модули/ОтелФильтрЭкземпляров.os:14-35,68-88` |  |

#### ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 121 | MUST | ✅ found | The `ExemplarReservoir` interface MUST provide a method to offer measurements to the reservoir and another to collect accumulated Exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:52-120; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50-102; src/Метрики/Классы/ОтелНоопРезервуарЭкземпляров.os:20-39` |  |
| 122 | MUST | ✅ found | A new `ExemplarReservoir` MUST be created for every known timeseries data point, as determined by aggregation and view configuration. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:315-338,450-455; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:357-369` |  |
| 123 | SHOULD | ✅ found | The “offer” method SHOULD accept measurements, including: * The `value` of the measurement.* The complete set of `Attributes` of the measurement.* The Context of the measurement, which covers the Bagg... | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39-54; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:37-52; src/Метрики/Классы/ОтелХранилищеМетрики.os:482-493` |  |
| 124 | SHOULD | ✅ found | The “offer” method SHOULD have the ability to pull associated trace and span information without needing to record full context. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:176-224; src/Метрики/Классы/ОтелХранилищеМетрики.os:495-505` |  |
| 125 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additional sampling performed by the res... | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:39-50; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:37-48; src/Метрики/Классы/ОтелНоопРезервуарЭкземпляров.os:9-16` |  |
| 126 | MUST | ✅ found | This MUST be clearly documented in the API and the reservoir MUST be given the `Attributes` associated with its timeseries point either at construction so that additional sampling performed by the res... | `src/Метрики/Классы/ОтелХранилищеМетрики.os:482-493; src/Метрики/Классы/ОтелХранилищеНаблюдений.os:371-382; src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:226-249` |  |
| 127 | MUST | ✅ found | The “collect” method MUST return accumulated `Exemplar`s. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:104-120; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:84-102` |  |
| 128 | SHOULD | ✅ found | In other words, Exemplars reported against a metric data point SHOULD have occurred within the start/stop timestamps of that point. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:92-111,139-153,360-400` |  |
| 129 | MUST | ✅ found | `Exemplar`s MUST retain any attributes available in the measurement that are not preserved by aggregation or view configuration for the associated timeseries. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:226-249; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:246-269; src/Метрики/Классы/ОтелХранилищеМетрики.os:473-493` |  |
| 130 | SHOULD | ✅ found | The `ExemplarReservoir` SHOULD avoid allocations when sampling exemplars. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:34-37,61-86; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:61-67,132-143` |  |

#### Exemplar defaults

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exemplar-defaults)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 131 | MUST | ✅ found | The SDK MUST include two types of built-in exemplar reservoirs: * `SimpleFixedSizeExemplarReservoir`* `AlignedHistogramBucketExemplarReservoir` | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:255-271; src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:1-3,275-287; lib.config:73-77` |  |
| 132 | SHOULD | ✅ found | Explicit bucket histogram aggregation with more than 1 bucket SHOULD use `AlignedHistogramBucketExemplarReservoir`. | `src/Метрики/Модули/ОтелАгрегация.os:259-261` |  |
| 133 | SHOULD | ✅ found | Base2 Exponential Histogram Aggregation SHOULD use a `SimpleFixedSizeExemplarReservoir` with a reservoir equal to the smaller of the maximum number of buckets configured on the aggregation or twenty (... | `src/Метрики/Модули/ОтелАгрегация.os:255,262-264` |  |
| 134 | SHOULD | ✅ found | All other aggregations SHOULD use `SimpleFixedSizeExemplarReservoir`. | `src/Метрики/Модули/ОтелАгрегация.os:265` |  |

#### SimpleFixedSizeExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#simplefixedsizeexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 135 | MUST | ✅ found | This reservoir MUST use a uniformly-weighted sampling algorithm based on the number of samples the reservoir has seen so far to determine if the offered measurements should be sampled. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:61-86` |  |
| 136 | SHOULD | ✅ found | Any stateful portion of sampling computation SHOULD be reset every collection cycle. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:139-153,360-400,438-448; src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:124-134` |  |
| 137 | SHOULD | ✅ found | Otherwise, a default size of `1` SHOULD be used. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:265; src/Метрики/Классы/ОтелФабрикаПростыхРезервуаров.os:46; src/Метрики/Модули/ОтелАгрегация.os:265; src/Метрики/Классы/ОтелХранилищеМетрики.os:570` |  |

#### AlignedHistogramBucketExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#alignedhistogrambucketexemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 138 | MUST | ✅ found | This Exemplar reservoir MUST take a configuration parameter that is the configuration of a Histogram. | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:281-287; src/Метрики/Классы/ОтелФабрикаВыровненныхРезервуаровГистограммы.os:20-22,46-48; src/Метрики/Модули/ОтелАгрегация.os:259-261` |  |
| 139 | MUST | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has s... | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:63-66,154-179` |  |
| 140 | SHOULD | ✅ found | This implementation MUST store at most one measurement that falls within a histogram bucket, and SHOULD use a uniformly-weighted sampling algorithm based on the number of measurements the bucket has s... | `src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:132-143` |  |
| 141 | SHOULD | ✅ found | This configuration parameter SHOULD have the same format as specifying bucket boundaries to Explicit Bucket Histogram Aggregation. | `src/Метрики/Модули/ОтелАгрегация.os:58-65,259-261; src/Метрики/Классы/ОтелАгрегаторГистограммы.os:158-160` |  |

#### Custom ExemplarReservoir

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#custom-exemplarreservoir)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 142 | MUST | ✅ found | The SDK MUST provide a mechanism for SDK users to provide their own ExemplarReservoir implementation. | `src/Метрики/Классы/ОтелПредставление.os:83-85,156-157,169,179; src/Метрики/Модули/ОтелПотокиМетрик.os:341-353,556-563` |  |
| 143 | MUST | ✅ found | This extension MUST be configurable on a metric View, although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reservoir - Paragraph 2). | `src/Метрики/Классы/ОтелПредставление.os:156-157,169,179; src/Метрики/Модули/ОтелПотокиМетрик.os:341-353,479-483` |  |
| 144 | MUST | ✅ found | This extension MUST be configurable on a metric View, although individual reservoirs MUST still be instantiated per metric-timeseries (see Exemplar Reservoir - Paragraph 2). | `src/Метрики/Классы/ОтелХранилищеМетрики.os:276-287,331-338,450-455; src/Метрики/Модули/ОтелПотокиМетрик.os:345-353` |  |

#### MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 145 | SHOULD | ✅ found | To construct a `MetricReader` when setting up an SDK, at least the following SHOULD be provided: | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:771-792 (конструктор: Экспортер - обязательный позиционный параметр, НовыйЛимитМощности = 2000, НоваяАгрегацияГистограмм), 302-324 (агрегация по умолчанию как функция вида инструмента: АгрегацияПоУмолчанию/УстановитьАгрегациюПоУмолчанию, иначе агрегация экспортера), 335-342 (временная агрегация по виду инструмента - у экспортера), 267-280 (лимит мощности по виду инструмента), 73-81 (ДобавитьПродюсер - MetricProducers); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:79-88,272-320; tests/unit/Метрики/ТестКонвейерМетрик.os:45,71` |  |
| 146 | SHOULD | ✅ found | This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:302-314 (АгрегацияПоУмолчанию: без агрегации, заданной читателю, вызывается Экспортер.АгрегацияПоУмолчанию(ВидИнструмента)), 799-800 (ЭкспортерЗадаетАгрегацию - наличие метода у экспортера); src/Экспорт/Классы/ОтелЭкспортерМетрик.os:154-159 (АгрегацияПоУмолчанию OTLP-экспортера); src/Метрики/Модули/ОтелПотокиМетрик.os:412-440 (поток берет агрегацию читателя по виду инструмента); tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:1589` |  |
| 147 | SHOULD | ✅ found | If not configured, the default aggregation SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:307-313 (без агрегации читателя и экспортера - агрегация вида по умолчанию или default), 801-811 (АгрегацииВидов: sum, last_value, explicit_bucket_histogram по спецификации); src/Метрики/Модули/ОтелПотокиМетрик.os:370,431-439 (незаданная или неприменимая агрегация - агрегация по умолчанию); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:307-310` |  |
| 148 | SHOULD | ✅ found | This function SHOULD be obtained from the `exporter`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:335-342 (ВременнаяАгрегацияДляВида вызывает Экспортер.ПолучитьВременнуюАгрегацию(ТипИнструмента)); src/Экспорт/Классы/ОтелЭкспортерМетрик.os:140-142 (селектор временной агрегации экспортера); src/Метрики/Модули/ОтелСелекторВременнойАгрегации.os:24-84; src/Метрики/Модули/ОтелПотокиМетрик.os:162-175` |  |
| 149 | SHOULD | ✅ found | If not configured, the Cumulative temporality SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:337-341 (экспортер без ПолучитьВременнуюАгрегацию - Кумулятивная); src/Экспорт/Классы/ОтелЭкспортерМетрик.os:280-284 (селектор по умолчанию ВсегдаКумулятивная); src/Метрики/Модули/ОтелПотокиМетрик.os:162-175 (читатель без временной агрегации или не Дельта - Кумулятивная)` |  |
| 150 | SHOULD | ✅ found | If not configured, a default value of 2000 SHOULD be used. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:774 (НовыйЛимитМощности = 2000), 267-270 (ЛимитМощностиДляВида: заданный для вида или общий лимит); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1869; src/Метрики/Модули/ОтелПотокиМетрик.os:26,452-465` |  |
| 151 | SHOULD | ✅ found | A common implementation of `MetricReader`, the periodic exporting `MetricReader` SHOULD be provided to be used typically with push-based metrics collection. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:85-101 (Запустить: фоновое задание ПериодическийСбор), 374-385 (ДождатьсяИнтервалаСбора), 756-792 (класс PeriodicMetricReader, интервал по умолчанию 60000 мс); lib.config (класс ОтелПериодическийЧитательМетрик)` |  |
| 152 | MUST | ✅ found | The `MetricReader` MUST ensure that data points from OpenTelemetry instruments are output in the configured aggregation temporality for each instrument kind. | `src/Метрики/Модули/ОтелПотокиМетрик.os:162-175 (ВременнаяАгрегацияЧитателя по виду инструмента); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:335-342; src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:127-137 и src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:259-281 (поток собирается с временной агрегацией читателя); src/Метрики/Классы/ОтелХранилищеМетрики.os:92-111,360-388 (синхронные: дельта-сбор начинает новый интервал, кумулятивный накапливает - Delta в Cumulative); src/Метрики/Классы/ОтелХранилищеНаблюдений.os:279-297,348-355 (асинхронные суммы: Cumulative в Delta вычитанием прошлого значения); tests/unit/Метрики/ТестКонвейерМетрик.os:13` |  |
| 153 | MUST | ✅ found | For synchronous instruments with Cumulative aggregation temporality, MetricReader.Collect MUST receive data points exposed in previous collections regardless of whether new measurements have been reco... | `src/Метрики/Классы/ОтелХранилищеМетрики.os:360-388 (кумулятивный снимок не начинает новый интервал: серии прошлых сборов сохраняются и выводятся без новых измерений), 315-329 (серии интервала); src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:127-137; tests/unit/Метрики/ТестКонвейерМетрик.os:13` |  |
| 154 | MUST | ✅ found | For synchronous instruments with Delta aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелХранилищеМетрики.os:92-111,366-368 (дельта-сбор атомарно начинает новый интервал без серий: Интервал = НовыйИнтервал(ВремяСбора)); tests/unit/Метрики/ТестКонвейерМетрик.os:13` |  |
| 155 | MUST | ✅ found | For asynchronous instruments with Delta or Cumulative aggregation temporality, MetricReader.Collect MUST only receive data points with measurements recorded since the previous collection. | `src/Метрики/Классы/ОтелХранилищеНаблюдений.os:43-62,222-266 (серии строятся только из наблюдений callback-ов текущего сбора, не наблюдавшиеся серии не выводятся - для Delta и Cumulative); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:259-281,397-425 (callback-и вызываются на каждый сбор читателя)` |  |
| 156 | MUST | ✅ found | For instruments with Cumulative aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST repeat the same starting timestamps (e.g. `(T0, T1], (T0, T2],... | `src/Метрики/Классы/ОтелХранилищеМетрики.os:360-369 (кумулятивный снимок сохраняет ВремяСтарта интервала), 574 (интервал начинается при создании потока); src/Метрики/Классы/ОтелХранилищеНаблюдений.os:281,452 (кумулятивные точки - ВремяСоздания потока)` |  |
| 157 | MUST | ✅ found | For instruments with Delta aggregation temporality, successive data points received by successive calls to MetricReader.Collect MUST advance the starting timestamp ( e.g. `(T0, T1], (T1, T2], (T2, T3]... | `src/Метрики/Классы/ОтелХранилищеМетрики.os:364-369 (дельта-сбор начинает новый интервал с ВремяСтарта = время сбора); src/Метрики/Классы/ОтелХранилищеНаблюдений.os:235-238,281 (ВремяПрошлогоСбора - начало следующего дельта-интервала)` |  |
| 158 | MUST | ✅ found | The ending timestamp (i.e. `TimeUnixNano`) MUST always be equal to time the metric data point took effect, which is equal to when MetricReader.Collect was invoked. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:446-449 (одно ВремяСбора на вызов сбора передается всем метрам); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:368-375; src/Метрики/Классы/ОтелМетр.os:443-458,780 (время сбора у наблюдений мульти-callback-ов); src/Метрики/Классы/ОтелХранилищеМетрики.os:364,402-408 (timeUnixNano точки = время сбора); src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:413 (наблюдения callback-ов получают время сбора); src/Метрики/Классы/ОтелХранилищеНаблюдений.os:279-287` |  |
| 159 | MUST | ✅ found | The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`, and the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NOT introduce side-ef... | `src/Метрики/Классы/ОтелПровайдерМетрик.os:26-27,161-163 (ЧитателиМетрик - массив), 446-455 (регистрация массива читателей), 107,112-114 (метр получает всех читателей и регистрируется в каждом); src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:42-45,84-85; src/Метрики/Модули/ОтелПотокиМетрик.os:111-125 (потоки на каждого читателя); tests/unit/Метрики/ТестПровайдерМетрик.os:369` |  |
| 160 | SHOULD NOT | ✅ found | The SDK MUST support multiple `MetricReader` instances to be registered on the same `MeterProvider`, and the MetricReader.Collect invocation on one `MetricReader` instance SHOULD NOT introduce side-ef... | `src/Метрики/Модули/ОтелПотокиМетрик.os:111-125,137-150 (у каждого читателя свои хранилища потоков; сбор берет только хранилища своего читателя); src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:127-137; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:259-281 (наблюдения callback-ов применяются только к потокам собирающего читателя); src/Метрики/Классы/ОтелМетр.os:742-759 (мульти-callback-и вызываются на сбор каждого читателя); tests/unit/Метрики/ТестКонвейерМетрик.os:13 (дельта-сбор одного читателя не меняет данные кумулятивного)` |  |
| 161 | MUST NOT | ✅ found | The SDK MUST NOT allow a `MetricReader` instance to be registered on more than one `MeterProvider` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:354-363 (ЗарегистрироватьУПровайдера: CAS АтомарноеБулево Зарегистрирован, повторная регистрация отклоняется с ошибкой в логе); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:343-352; src/Метрики/Классы/ОтелПровайдерМетрик.os:411-415 (читатель добавляется только при успешной регистрации); tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:342` |  |
| 162 | SHOULD | ✅ found | The SDK SHOULD provide a way to allow `MetricReader` to respond to MeterProvider.ForceFlush and MeterProvider.Shutdown. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:176-178,229-234,354-365 (ForceFlush провайдера вызывает ПринудительноВыгрузитьСРезультатом или СброситьБуфер каждого читателя), 188-219 (Shutdown провайдера вызывает Закрыть каждого читателя); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:149-175,187-205; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:185-199,240-253` |  |

#### Collect

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#collect)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 163 | SHOULD | ✅ found | `Collect` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:456-466 (РезультатСбора по сбоям и таймаутам callback-ов, метров и продюсеров), 112-136 (СброситьБуфер/СброситьБуферБезОчистки - сбор с передачей экспортеру - возвращают ОтелРезультатЭкспорта: успех, ошибка или таймаут); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:102-108,154-170,389 (СобратьВТексте/СобратьСемейства: выходной параметр РезультатСбора); src/Ядро/Модули/ОтелРезультатыЭкспорта.os:52-62 (РезультатСбора); tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:229` |  |
| 164 | SHOULD | ✅ found | `Collect` SHOULD invoke Produce on registered MetricProducers. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:456,660-714 (СобратьДанныеПродюсеров: Продюсер.Произвести(РесурсДляПродюсеров()) у каждого продюсера при каждом сборе), 73-81 (ДобавитьПродюсер); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:383-387,403-427; src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:26-28` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 165 | MUST | ✅ found | `Shutdown` MUST be called only once for each `MetricReader` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:149-153 (Закрыть: CAS Закрыт.СравнитьИУстановить - Shutdown выполняется один раз, повторный вызов возвращает ошибку «Reader закрыт»); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:240-243; src/Метрики/Классы/ОтелПровайдерМетрик.os:188-191,204-217 (провайдер вызывает Закрыть каждого читателя один раз); tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:434; tests/unit/Метрики/ТестПровайдерМетрик.os:426` |  |
| 166 | SHOULD | ✅ found | SDKs SHOULD return some failure for these calls, if possible. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:112-116,130-134,187-190 (после Закрыть сбор не выполняется, возвращается ошибка), 374-385 (фоновый периодический сбор завершается); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:154-158 (СобратьСемейства/СобратьВТексте: РезультатСбора = Ошибка, метрик нет); tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:467,485` |  |
| 167 | SHOULD | ✅ found | `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:138-175 (Закрыть возвращает ОтелРезультатЗакрытия: сведенный результат финального экспорта и закрытия экспортера с признаком истечения срока); src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-38 (Успешно/ИстекТаймаут/Описание); src/Ядро/Модули/ОтелРезультатыЗакрытия.os:239-260 (Свести: ошибка, таймаут или успех); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:240-253` |  |
| 168 | SHOULD | ✅ found | `Shutdown` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:149-175 (Закрыть(ТаймаутМс = 30000): Обещание.Получить(ОставшеесяВремя), финальный сбор с оставшимся временем, Закрыть экспортера в пределах срока, Таймаут по истечении срока), 399-417 (БлокировкаСбора.Захватить(срок)), 429-469 (callback-и получают таймаут не больше времени до срока, после срока callback-и и продюсеры не вызываются, данные не экспортируются), 484-503 (экспорт получает время, оставшееся после сбора); src/Метрики/Классы/ОтелМетр.os:742-759; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:405-412; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:189-201 (ТаймаутДоСрока); tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:164,1638,1684,1719` |  |

#### Periodic exporting MetricReader

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#periodic-exporting-metricreader)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 169 | MUST | ✅ found | When `maxExportBatchSize` is configured, the reader MUST ensure no batch provided to `Export` exceeds the `maxExportBatchSize` by splitting the batch of metric data points into smaller batches. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:576-607 (РазбитьНаПакеты: в пакете не больше МаксРазмерПакетаЭкспорта точек данных), 619-633 (ЧастьДанных), 226-244 (maxExportBatchSize: МаксРазмерПакетаЭкспорта/УстановитьМаксРазмерПакетаЭкспорта, 0 - без ограничения), 493-501; tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:1441,1455,1483` |  |
| 170 | MUST | ✅ found | The initial batch of metric data MUST be split into as many “full” batches of size `maxExportBatchSize` as possible – even if this splits up data points that belong to the same metric into different b... | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:584-601 (пакет заполняется ровно до МаксРазмерПакетаЭкспорта точек; точки одной метрики делятся между пакетами через ЧастьДанных), 619-633; tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:1455 (6 точек при размере 4: полный пакет из 4 точек счетчика, затем 1 точка счетчика и датчик)` |  |
| 171 | MUST | ✅ found | The reader MUST ensure all batches produced from a single `Collect()` are provided to `Export` serially and in-order before metric data points from a subsequent `Collect()` are provided. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:484-503 (пакеты одного сбора экспортируются последовательно в порядке РазбитьНаПакеты), 399-417 (сбор и экспорт всех его пакетов выполняются под БлокировкаСбора: следующий сбор начинается после экспорта всех пакетов текущего); tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:1455` |  |
| 172 | MUST NOT | ✅ found | The reader MUST NOT combine metrics from different `Collect()` calls into the same batch provided to `Export`. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:444-468 (МассивДанных локален для одного сбора), 576-607 (пакеты строятся только из данных этого сбора; буфера между сборами нет), 494-497 (после истечения срока оставшиеся пакеты отбрасываются, а не переносятся в следующий сбор)` |  |
| 173 | MUST | ✅ found | The reader MUST synchronize calls to `MetricExporter`’s `Export` to make sure that they are not invoked concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:514-528 (Экспортер.Экспортировать вызывается под БлокировкаРесурса Блокировка), 399-417 (сбор и экспорт сериализованы ОтелБлокировкаСТаймаутом БлокировкаСбора для фонового задания, ForceFlush и Shutdown); src/Ядро/Классы/ОтелБлокировкаСТаймаутом.os:20-36` |  |
| 174 | MUST | ✅ found | If an export is still in progress when the next scheduled interval occurs, the reader MUST either delay the subsequent collection and export until the in-progress export finishes, or skip the schedule... | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:97-101 (фоновый цикл: следующий интервал отсчитывается после завершения предыдущего сбора и экспорта), 374-385 (ДождатьсяИнтервалаСбора), 399-407 (фоновый сбор с ТаймаутМс = 0 ждет завершения сбора и экспорта, идущего в другом потоке: последующий сбор задерживается)` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 175 | SHOULD | ✅ found | `ForceFlush` SHOULD collect metrics, split into batches if necessary, call `Export(batch)` on each batch serially, and call `ForceFlush()` on the configured Push Metric Exporter. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:187-205 (ПринудительноВыгрузитьСРезультатом: СброситьБуфер - сбор и экспорт, затем ForceFlush экспортера), 429-469 (сбор), 484-503,576-607 (разбиение на пакеты и последовательный Export каждого пакета), 825-830 (СброситьБуферЭкспортера: ПринудительноВыгрузитьСРезультатом или СброситьБуфер экспортера); src/Метрики/Классы/ОтелПровайдерМетрик.os:354-365` |  |
| 176 | SHOULD | ✅ found | `ForceFlush` MAY skip `Export(batch)` calls if the timeout is already expired, but SHOULD still call `ForceFlush()` on the configured Push Metric Exporter even if the timeout has passed. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:199-203 (ForceFlush экспортера вызывается независимо от исхода и срока СброситьБуфер), 494-497 (после истечения срока оставшиеся Export(batch) пропускаются), 825-830; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:159-164,216-226 (после срока экспортер получает 1 мс); tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:1344` |  |
| 177 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:177-205 (ПринудительноВыгрузитьСРезультатом возвращает ОтелРезультатЗакрытия: ошибка, таймаут или успех); src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-38; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:239-260` |  |
| 178 | SHOULD | ✅ found | If any `Export(batch)` call fails or times out, or if the configured exporter’s `ForceFlush()` fails or times out, `ForceFlush` SHOULD return some ERROR status. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:192-204 (результаты сбора, экспорта и ForceFlush экспортера сводятся Свести; исключение - ошибка), 514-537 (ЭкспортироватьПакет: сбой - Ошибка, превышение таймаута - Таймаут), 484-503; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:239-260 (Свести: ошибка или таймаут - Успешно() = Ложь); tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:1407,1424` |  |
| 179 | SHOULD | ✅ found | If all calls succeed, `ForceFlush` SHOULD return some NO ERROR status. | `src/Ядро/Модули/ОтелРезультатыЗакрытия.os:239-260 (без ошибок и таймаутов Свести возвращает Успех); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:204,529-531` |  |
| 180 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:187-205 (ПринудительноВыгрузитьСРезультатом(ТаймаутМс = 30000)), 399-417 (БлокировкаСбора.Захватить(срок)), 429-469 (callback-и в пределах срока, после срока продюсеры не вызываются и данные не экспортируются), 484-503 (экспорт пакетов в пределах оставшегося срока), 825-830 (ForceFlush экспортера с оставшимся временем); src/Ядро/Модули/ОтелРезультатыЗакрытия.os:189-201; tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:1344,1684,1703,1719` |  |

#### MetricExporter

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricexporter)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 181 | MUST | ✅ found | `MetricExporter` defines the interface that protocol-specific exporters MUST implement so that they can be plugged into OpenTelemetry SDK and support sending of telemetry data. | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:5-45 (интерфейс с аннотацией &Интерфейс: Экспортировать, СброситьБуфер, Закрыть); src/Экспорт/Классы/ОтелЭкспортерМетрик.os:265-285 (OTLP-экспортер реализует ИнтерфейсЭкспортерМетрик через аннотацию &Реализует, транспорт HTTP/gRPC/InMemory); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:514-519,825-830 (читатель работает с любым экспортером интерфейса)` |  |
| 182 | SHOULD | ✅ found | Metric Exporters SHOULD report an error condition for data output by the `MetricReader` with unsupported Aggregation or Aggregation Temporality, as this condition can be corrected by a change of `Metr... | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:60-62,183-234 (ВалидироватьСовместимостьДанных: неподдерживаемый тип агрегации или неуказанная временная агрегация - предупреждение в логе и результат Ложь/Failure), 436-446; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:637-655 (экспоненциальная гистограмма - предупреждение), 657-681 (дельта-суммы и гистограммы - предупреждение)` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 183 | MUST | ✅ found | A Push Metric Exporter MUST support the following functions: | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:14-16 (Export: Экспортировать), 26-28 (ForceFlush: СброситьБуфер), 35-37 (Shutdown: Закрыть); src/Экспорт/Классы/ОтелЭкспортерМетрик.os:51-74,87-90,104-112,124-130` |  |

#### Export(batch)

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#exportbatch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 184 | MUST | ✅ found | The SDK MUST provide a way for the exporter to get the Meter information (e.g. name, version, etc.) associated with each `Metric Point`. | `src/Метрики/Классы/ОтелДанныеМетрики.os:48-50 (ОбластьИнструментирования() у каждой метрики батча); src/Ядро/Классы/ОтелОбластьИнструментирования.os:21-51 (Имя, Версия, Атрибуты, АдресСхемы); src/Экспорт/Классы/ОтелЭкспортерМетрик.os:302,370-384 (экспортер группирует точки по области и выводит name/version/attributes/schemaUrl); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:628-630 (часть метрики при разбиении на пакеты сохраняет область)` |  |
| 185 | MUST NOT | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:51-74 (Экспортировать: отправка в Обещании, ожидание Обещание.Получить(ТаймаутОперацииМс), по таймауту - Ложь), 270,276 (таймаут по умолчанию 10000 мс); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:498,557-565,789 (Export получает меньший из exportTimeoutMillis = 30000 и срока); tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:1368,1385` |  |
| 186 | MUST | ✅ found | `Export` MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call must time out with an error result (Failure). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:64-73 (верхний предел ТаймаутОперацииМс: по истечении Обещание.Получить бросает исключение - возвращается Ложь = Failure), 270 (10000 мс по умолчанию); src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:514-537 (Ложь после истечения таймаута трактуется как Таймаут, исключение - Ошибка), 789 (exportTimeoutMillis = 30000); tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:1407` |  |
| 187 | SHOULD NOT | ✅ found | The default SDK SHOULD NOT implement retry logic, as the required logic is likely to depend heavily on the specific protocol and backend the metrics are being sent to. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:514-537 (Export вызывается однократно, сбой возвращается результатом, пакет не повторяется и не возвращается в буфер), 484-503; повтор реализован только в протокол-специфичных транспортах экспортера: src/Экспорт/Классы/ОтелHttpТранспорт.os:124,182,351-354; src/Экспорт/Классы/ОтелGrpcТранспорт.os:119,257` |  |

#### ForceFlush

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#forceflush)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 188 | SHOULD | ✅ found | This is a hint to ensure that the export of any `Metrics` the exporter has received prior to the call to `ForceFlush` SHOULD be completed as soon as possible, preferably before returning from this met... | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:51-74,87-90,124-130; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:187-205,399-417` |  |
| 189 | SHOULD | ✅ found | `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:18-28; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:87-90,124-130; src/Ядро/Классы/ОтелРезультатЭкспорта.os:17-38; src/Ядро/Классы/ОтелРезультатЗакрытия.os:20-40` |  |
| 190 | SHOULD | ➖ n_a | `ForceFlush` SHOULD only be called in cases where it is absolutely necessary, such as when using some FaaS providers that may suspend the process after an invocation, but before the exporter exports t... | - | Требование является рекомендацией по использованию для вызывающих кода (caller guidance): оно описывает, в каких случаях вызывающему следует вызывать ForceFlush экспортера (например, в FaaS-окружениях перед приостановкой процесса); SDK не может программно обеспечить это ограничение. |
| 191 | SHOULD | ✅ found | `ForceFlush` SHOULD complete or abort within some timeout. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:87-90,124-130; src/Экспорт/Классы/ИнтерфейсЭкспортерМетрик.os:26-28; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:790-795` |  |

#### Shutdown

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#shutdown)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 192 | SHOULD | ✅ found | Shutdown SHOULD be called only once for each `MetricExporter` instance. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:149-153,171-173; src/Метрики/Классы/ОтелПровайдерМетрик.os:188-191; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:92-112` |  |
| 193 | SHOULD NOT | ✅ found | `Shutdown` SHOULD NOT block indefinitely (e.g. if it attempts to flush the data and the destination is unavailable). | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:104-112; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:171-174; src/Ядро/Модули/ОтелРезультатыЗакрытия.os:192-202` |  |

#### MetricProducer

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#metricproducer)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 194 | MUST | ✅ found | `MetricProducer` defines the interface which bridges to third-party metric sources MUST implement, so they can be plugged into an OpenTelemetry MetricReader as a source of aggregated metric data. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:1-38; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:73-81,641-679; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:79-88,383-427` |  |
| 195 | SHOULD | ✅ found | `MetricProducer` implementations SHOULD accept configuration for the `AggregationTemporality` of produced metrics. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:14-15; src/Метрики/Классы/ОтелДанныеМетрики.os:115-131; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:398-415; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:71-74` |  |

#### Interface Definition

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#interface-definition)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 196 | MUST | ✅ found | A `MetricProducer` MUST support the following functions: | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:26-28,34-36` |  |

#### Produce batch

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#produce-batch)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 197 | MUST | ✅ found | `Produce` MUST return a batch of Metric Points, filtered by the optional `metricFilter` parameter. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:23-28; src/Метрики/Классы/ОтелРезультатПроизводстваМетрик.os:4-9,72-81; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:654-673` |  |
| 198 | SHOULD | ✅ found | If the batch of Metric Points includes resource information, `Produce` SHOULD require a resource as a parameter. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:18-26; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:354-363,656,706-711; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:405,435-440` |  |
| 199 | SHOULD | ✅ found | `Produce` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out. | `src/Метрики/Классы/ОтелРезультатПроизводстваМетрик.os:4-49; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:659-668,690-698; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:410-421` |  |
| 200 | SHOULD | ✅ found | If a batch of Metric Points can include `InstrumentationScope` information, `Produce` SHOULD include a single InstrumentationScope which identifies the `MetricProducer`. | `src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:15-16; src/Метрики/Классы/ОтелДанныеМетрики.os:43-50,208-218; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:449-461` |  |

#### Defaults and configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#defaults-and-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 201 | MUST | ✅ found | The SDK MUST provide configuration according to the SDK environment variables specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:6-45,149-155,376-442,922-932,1233-1242; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114-129` |  |

#### Numerical limits handling

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#numerical-limits-handling)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 202 | MUST | ✅ found | The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry. | `src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:76-93; src/Метрики/Классы/ОтелНаблюдениеМетрики.os:19-22; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:435-442; src/Метрики/Классы/ОтелАгрегаторЭкспоненциальнойГистограммы.os:177-207` |  |
| 203 | MUST | ➖ n_a | If the SDK receives float/double values from Instruments, it MUST handle all the possible values. | - | OneScript Число = System.Decimal (не IEEE 754): типов float/double в рантайме нет, инструменты (ОтелСчетчик.Добавить, ОтелГистограмма.Записать, ОтелДатчик.Записать и др.) принимают только Число-Decimal, поэтому NaN, Infinity и отрицательный ноль как значения невозможны - операции, которые в IEEE 754 дали бы их, в Decimal выбрасывают исключение (оно перехватывается и логируется в ОтелБазовыйСинхронныйИнструмент.Записать, стр. 86-92). Весь диапазон Decimal SDK обрабатывает: min/max гистограмм инициализируются Decimal.MaxValue (ОтелАгрегаторГистограммы.os:258-260, ОтелАгрегаторЭкспоненциальнойГистограммы.os:421-423), ноль и значения в пределах порога нуля учитываются в zeroCount до вычисления логарифма (ОтелАгрегаторЭкспоненциальнойГистограммы.os:177-188). |

#### Compatibility requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#compatibility-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 204 | SHOULD | ✅ found | All the metrics components SHOULD allow new methods to be added to existing components without introducing breaking changes. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:335-342,764-765,790-795; src/Метрики/Классы/ОтелПровайдерМетрик.os:354-365; packagedef:7` |  |
| 205 | SHOULD | ✅ found | All the metrics SDK methods SHOULD allow optional parameter(s) to be added to existing methods without introducing breaking changes, if possible. | `src/Ядро/Модули/ОтелРезультатыЗакрытия.os:123-147; src/Метрики/Классы/ОтелПровайдерМетрик.os:210-213; src/Экспорт/Классы/ОтелЭкспортерМетрик.os:104; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:149` |  |

#### Concurrency requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#concurrency-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 206 | MUST | ✅ found | MeterProvider - Meter creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПровайдерМетрик.os:39-48 (потокобезопасность документирована), 74-125 (ПолучитьМетр: fast-path через СинхронизированнаяКарта, slow-path с двойной проверкой и повторной проверкой Закрыт под БлокировкаМетрик), 59-61 (ПостроительМетра; src/Метрики/Классы/ОтелПостроительМетра.os:62-63 Построить вызывает ПолучитьМетр), 176-178,229-234,354-365 (ForceFlush: СброситьБуфер/ПринудительноВыгрузитьСРезультатом обходят массив читателей, неизменяемый после конструктора), 188-219 (Shutdown: Закрыть идемпотентен через Закрыт.СравнитьИУстановить, снимок метров под БлокировкаМетрик 381-394), 436-438 (СинхронизированнаяКарта, АтомарноеБулево, БлокировкаРесурса); tests/unit/Метрики/ТестПровайдерМетрикКонкурентность.os:16` |  |
| 207 | MUST | ✅ found | ExemplarReservoir - all methods MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:52-93 (Предложить под Блокировка), 104-120 (Собрать возвращает копию под Блокировка), 124-134 (Очистить под Блокировка), 26-28 (МаксРазмер - неизменяемое поле), 270 (БлокировкаРесурса); src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:50-73,84-102,106-116,286 (Предложить/Собрать/Очистить под БлокировкаРесурса); src/Метрики/Классы/ОтелНоопРезервуарЭкземпляров.os:20-44 (без состояния); tests/unit/Метрики/ТестРезервуарыКонкурентность.os:18` |  |
| 208 | MUST | ✅ found | MetricReader - `Collect`, `ForceFlush` (for periodic exporting MetricReader) and `Shutdown` MUST be safe to be called concurrently. | `src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:399-417 (сбор СобратьИЭкспортировать сериализован через БлокировкаСбора; вызывается фоновым заданием, ForceFlush и Shutdown), 419-430,641-652 (снимки метров и продюсеров под Блокировка), 112-118,187-205 (ForceFlush: СброситьБуфер/ПринудительноВыгрузитьСРезультатом с атомарной проверкой Закрыт), 149-175 (Shutdown: Закрыт.СравнитьИУстановить), 747-753 (инициализация блокировок); src/Ядро/Классы/ОтелБлокировкаСТаймаутом.os:20-36 (взаимоисключающая блокировка на CAS АтомарноеБулево); src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:102-108,154-170,208-210 (Collect под БлокировкаСбора), 185-187,1161-1166 (ForceFlush - атомарная проверка Закрыт), 240-253 (Shutdown: CAS и очистка списков под Блокировка), 1858-1859; tests/unit/Метрики/ТестПериодическийЧитательМетрик.os:253; tests/unit/Метрики/ТестПрометеусЧитательМетрик.os:302` |  |
| 209 | MUST | ✅ found | MetricExporter - `ForceFlush` and `Shutdown` MUST be safe to be called concurrently. | `src/Экспорт/Классы/ОтелЭкспортерМетрик.os:7-19 (потокобезопасность документирована), 87-90 (СброситьБуфер - no-op без состояния), 124-130 (ПринудительноВыгрузитьСРезультатом - атомарное чтение Закрыт), 104-112 (Закрыть - атомарная запись АтомарноеБулево, идемпотентно), 51-54 (Экспортировать атомарно проверяет Закрыт), 278 (Закрыт = АтомарноеБулево)` |  |

### Otlp Exporter

#### Configuration Options

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#configuration-options)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ⚠️ partial | The following configuration options MUST be available to configure the OTLP exporter. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-647 (СоздатьТранспортДляСигнала), 1357-1377 (СоздатьНастройкиTlsДляСигнала); src/Экспорт/Классы/ОтелHttpТранспорт.os:325-388; src/Экспорт/Классы/ОтелGrpcТранспорт.os:239-277` | Опции Endpoint, Insecure, Headers, Timeout, Protocol и Max Request Size доступны (env-переменные с per-signal вариантами и параметры конструкторов транспортов). Но часть опций доступна лишь номинально: Client key file и Client certificate file (mTLS) читаются в ОтелНастройкиTls, но не применяются ни ОтелHttpТранспорт (HTTP-клиент OneScript/1connector, предупреждение в ОтелHttpТранспорт.os:379-383), ни ОтелGrpcТранспорт (OPI_GRPC не поддерживает mTLS, ОтелGrpcТранспорт.os:542-552); Certificate File применяется только gRPC-транспортом, HTTP-транспорт его игнорирует (ограничения TLS платформы и библиотек); Compression для grpc не применяется: у ОтелGrpcТранспорт нет параметра сжатия, ОтелАвтоконфигурация.ПредупредитьОСжатииGrpc (стр. 1061-1067) только логирует предупреждение; Max Response Size настраивается только в ОтелHttpТранспорт (УстановитьМаксРазмерОтвета, стр. 106-121), в ОтелGrpcТранспорт такой опции нет (есть лишь МаксРазмерЗапроса). |
| 2 | MUST | ✅ found | Each configuration option MUST be overridable by a signal specific option. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:562-647 (СоздатьТранспортДляСигнала: protocol 568-574, headers 576-582, compression 584-588, endpoint 590-617, timeout 627-632), 1307-1315 (ПараметрСигналаИлиОбщий), 1155-1158 (ЧислоСОткатом), 1357-1377 (certificate, client.key, client.certificate, insecure per-signal)` |  |
| 3 | MUST | ✅ found | The implementation MUST honor the following URL components: | `src/Экспорт/Классы/ОтелHttpТранспорт.os:204-210 (ВыполнитьОднуПопытку: ПолныйURL = БазовыйURL + Путь передается в КоннекторHTTP.Post со схемой, хостом, портом и путем); src/Конфигурация/Модули/ОтелАвтоконфигурация.os:707-722 (РазобратьСхемуURL: http/https)` |  |
| 4 | MUST | ✅ found | When using `OTEL_EXPORTER_OTLP_ENDPOINT`, exporters MUST construct per-signal URLs as described below. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:606-617 (generic endpoint: базовый URL + /v1/{signal}); src/Экспорт/Классы/ОтелHttpТранспорт.os:205-209 (склейка без двойного слеша)` |  |
| 5 | SHOULD | ✅ found | The option SHOULD accept any form allowed by the underlying gRPC client implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:310-339 (ОткрытьСоединение, комментарий: OPI_GRPC на tonic принимает адрес только со схемой http/https); src/Конфигурация/Модули/ОтелАвтоконфигурация.os:691-722 (РазобратьСхемуURL, примечание о возможностях OPI_GRPC)` |  |
| 6 | MUST | ✅ found | Additionally, the option MUST accept a URL with a scheme of either `http` or `https`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:707-722 (РазобратьСхемуURL принимает http и https), 634-637 (адрес передается в ОтелGrpcТранспорт); src/Экспорт/Классы/ОтелGrpcТранспорт.os:310-320` |  |
| 7 | SHOULD | ✅ found | If the gRPC client implementation does not support an endpoint with a scheme of `http` or `https` then the endpoint SHOULD be transformed to the most sensible format for that implementation. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:310-320 (OPI_GRPC/tonic поддерживает http/https, поэтому адрес передается без трансформации)` |  |
| 8 | MUST | ✅ found | Options MUST be one of: `grpc`, `http/protobuf`, `http/json`. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:980-992 (РаспознатьПротоколOtlp: только grpc, http/protobuf, http/json, остальное игнорируется с предупреждением), 965-968 (НормализоватьПротоколOtlp)` |  |
| 9 | SHOULD | ✅ found | SDKs SHOULD default endpoint variables to use `http` scheme unless they have good reasons to choose `https` scheme for the default (e.g., for backward compatibility reasons in a stable SDK release). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:607-612 (АдресПоУмолчанию = http://localhost:4317 / http://localhost:4318), 251, 261` |  |
| 10 | SHOULD | ✅ found | However, if they are already implemented, they SHOULD continue to be supported as they were part of a stable release of the specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1365-1370 (поддерживаются актуальные OTEL_EXPORTER_OTLP_[<SIGNAL>_]INSECURE; устаревшие OTEL_EXPORTER_OTLP_SPAN_INSECURE и OTEL_EXPORTER_OTLP_METRIC_INSECURE в истории src/ никогда не реализовывались, поэтому сохранять нечего)` |  |
| 11 | SHOULD | ✅ found | The default protocol SHOULD be `http/protobuf`, unless there are strong reasons for SDKs to select `grpc` as the default. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:570-574 (ПараметрИлиУмолчание(..., otel.exporter.otlp.protocol, http/protobuf)), 237-238; src/Экспорт/Классы/ОтелHttpТранспорт.os:332 (НовыйПротокол = http/protobuf)` |  |

#### Endpoint URLs for OTLP/HTTP

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#endpoint-urls-for-otlphttp)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 12 | MUST | ✅ found | Based on the environment variables above, the OTLP/HTTP exporter MUST construct URLs for each signal as follow: | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:590-617 (СоздатьТранспортДляСигнала: per-signal URL как есть либо базовый URL + /v1/{signal}); src/Экспорт/Классы/ОтелHttpТранспорт.os:204-210` |  |
| 13 | MUST | ✅ found | For the per-signal variables (`OTEL_EXPORTER_OTLP_<signal>_ENDPOINT`), the URL MUST be used as-is without any modification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:602-605 (ветка ЕстьАдресСигнала: ПутьСигнала = пустая строка), 1326-1340 (НормализоватьURLДляPerSignal)` |  |
| 14 | MUST | ✅ found | The only exception is that if an URL contains no path part, the root path `/` MUST be used (see Example 2). | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1326-1340 (НормализоватьURLДляPerSignal: добавляет / при отсутствии пути)` |  |
| 15 | MUST NOT | ✅ found | An SDK MUST NOT modify the URL in ways other than specified above. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:204-210 (ПолныйURL = БазовыйURL + Путь, на стыке убирается только дублирующийся слеш); src/Конфигурация/Модули/ОтелАвтоконфигурация.os:602-617, 1326-1340 (порт не подставляется, умолчания 80/443 по схеме - в 1connector)` |  |

#### Specify Protocol

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specify-protocol)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | SHOULD | ✅ found | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:95-124, 239-277 (grpc); src/Экспорт/Классы/ОтелHttpТранспорт.os:134-187 (http/protobuf через ОтелПротоКодировщик*, а также http/json); src/Конфигурация/Модули/ОтелАвтоконфигурация.os:634-643` |  |
| 17 | MUST | ✅ found | SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them. | `src/Экспорт/Классы/ОтелGrpcТранспорт.os:95-124, 239-277 (grpc); src/Экспорт/Классы/ОтелHttpТранспорт.os:134-187 (http/protobuf, http/json); src/Конфигурация/Модули/ОтелАвтоконфигурация.os:634-643` |  |
| 18 | SHOULD | ✅ found | If they support only one, it SHOULD be `http/protobuf`. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:137-139 (http/protobuf), 332; поддерживаются оба транспорта` |  |
| 19 | SHOULD | ✅ found | If no configuration is provided the default transport SHOULD be `http/protobuf` unless SDKs have good reasons to choose `grpc` as the default (e.g. for backward compatibility reasons when `grpc` was a... | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:570-574, 237-238 (умолчание http/protobuf); src/Экспорт/Классы/ОтелHttpТранспорт.os:332; src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:380-381` |  |

#### Specifying headers via environment variables

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#specifying-headers-via-environment-variables)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | All attribute values MUST be considered strings. | `src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:809-813 (РазобратьПарыКлючЗначение), 832-861 (РазобратьПары: значения остаются строками, без приведения типов); src/Конфигурация/Модули/ОтелАвтоконфигурация.os:576-582` |  |

#### Retry

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#retry)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | MUST | ✅ found | Transient errors MUST be handled with a retry strategy. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:182, 204-232 (HTTP 429/502/503/504 и сетевые ошибки бросают исключение, которое повторяет СтратегияПовтора; Retry-After учитывается), 350-354; src/Экспорт/Классы/ОтелGrpcТранспорт.os:119, 158-209 (ОшибкаПовторяемая, недоступность коллектора), 256-259` |  |
| 22 | MUST | ✅ found | This retry strategy MUST implement an exponential back-off with jitter to avoid overwhelming the destination until the network is restored or the destination has recovered. | `src/Экспорт/Классы/ОтелHttpТранспорт.os:350-354 (СтратегияПовтора: ТипыРасчетаЗадержки.Экспоненциальная + ИспользоватьРазбросЗадержки(Истина), задержка 1000*2^n с разбросом 0.75-1.25); src/Экспорт/Классы/ОтелGrpcТранспорт.os:256-259 (аналогично)` |  |

#### User Agent

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/protocol/exporter/#user-agent)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 23 | SHOULD | ⚠️ partial | OpenTelemetry protocol exporters SHOULD emit a User-Agent header to at a minimum identify the exporter, the language of its implementation, and the version of the exporter. | `src/Ядро/Модули/ОтелУтилиты.os:487-498 (UserAgentЭкспортераOtlp: OTel-OTLP-Exporter-OneScript/<версия>); src/Экспорт/Классы/ОтелHttpТранспорт.os:356-368; src/Экспорт/Классы/ОтелGrpcТранспорт.os:288-302` | HTTP-транспорт отправляет заголовок User-Agent: OTel-OTLP-Exporter-OneScript/<версия> (экспортер, язык и версия; подтверждено перехватом запроса). gRPC-транспорт кладет user-agent только в метаданные вызова (СформироватьМетаданные), а tonic внутри OPI_GRPC вырезает зарезервированный заголовок user-agent из метаданных и подставляет собственный: перехват запроса ОтелGrpcТранспорт показал user-agent: tonic/0.13.1, хотя пользовательская метаданная x-custom дошла. Для OTLP/gRPC экспортер себя в User-Agent не идентифицирует; юнит-тесты ТестGrpcТранспорт проверяют только содержимое Соответствия метаданных, а не отправляемый заголовок. |
| 24 | SHOULD | ✅ found | The format of the header SHOULD follow RFC 7231. | `src/Ядро/Модули/ОтелУтилиты.os:487-498 (product/version-токены OTel-OTLP-Exporter-OneScript/<версия>, идентификатор продукта отделяется пробелом)` |  |
| 25 | SHOULD | ⚠️ partial | The resulting User-Agent SHOULD include the exporter’s default User-Agent string. | `src/Ядро/Модули/ОтелУтилиты.os:487-498 (ИдентификаторПродукта + пробел + СтандартныйUserAgent); src/Экспорт/Классы/ОтелHttpТранспорт.os:356-368; src/Экспорт/Классы/ОтелGrpcТранспорт.os:288-302` | Для HTTP итоговый заголовок содержит стандартную строку после идентификатора продукта (перехвачено: MyDistribution/1.2.3 OTel-OTLP-Exporter-OneScript/1.1.0). Для gRPC идентификатор продукта и стандартная строка собираются только в метаданных, а на проводе tonic (OPI_GRPC) заменяет user-agent на tonic/0.13.1: итоговый User-Agent gRPC-запроса не содержит стандартной строки экспортера. |

### Propagators

#### Operations

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#operations)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | `Propagator`s MUST define `Inject` and `Extract` operations, in order to write values to and read values from carriers respectively. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:63 (Внедрить), 99 (Извлечь); src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:31, 97; src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:20, 41; src/Пропагация/Классы/ОтелНоопПропагатор.os:15, 29 (все пропагаторы: Внедрить(Контекст, Носитель, Сеттер) / Извлечь(Контекст, Носитель, Геттер))` |  |
| 2 | MUST | ✅ found | Each `Propagator` type MUST define the specific carrier type and MAY define additional parameters. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:55-63, 88-99 (TextMap-носитель: Носитель - носитель заголовков, доступ через ОтелСеттерТекстовойКарты/ОтелГеттерТекстовойКарты, по умолчанию Соответствие; дополнительные параметры Сеттер/Геттер); src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:14-20; src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:29-33 (Носитель - Соответствие - коллекция заголовков, строковые ключ/значение)` |  |

#### Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The Propagator MUST retrieve the appropriate value from the `Context` first, such as `SpanContext`, `Baggage` or another cross-cutting concern context. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:64-72 (Спан = ОтелКонтекст.СпанИзКонтекста(Контекст), затем КонтекстСпана(); выход при отсутствии/невалидности); src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:32-40 (ОбъектBaggage = ОтелКонтекст.BaggageИзКонтекста(Контекст); выход при отсутствии/пустом)` |  |

#### Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any pre... | `src/Пропагация/Классы/ОтелW3CПропагатор.os:107-158 (все ветки невалидного traceparent: Лог.Предупреждение + Возврат Контекст, без ВызватьИсключение); src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:110-147 (невалидные list-member пропускаются, декодирование через РаскодироватьСтроку не бросает исключений); src/Трассировка/Классы/ОтелСостояниеТрассировки.os:238-291 (невалидные записи tracestate отбрасываются с предупреждением); src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:44-48 (Попытка/Исключение вокруг Извлечь каждого пропагатора)` |  |
| 5 | MUST NOT | ✅ found | If a value can not be parsed from the carrier, for a cross-cutting concern, the implementation MUST NOT throw an exception and MUST NOT store a new value in the `Context`, in order to preserve any pre... | `src/Пропагация/Классы/ОтелW3CПропагатор.os:108, 114, 125, 131, 141, 151, 157 (Возврат Контекст - исходный контекст без нового значения); src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:106-108, 143-147 (без разобранных записей возвращается исходный Контекст, существующий baggage сохраняется); src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:44-48 (при исключении ТекущийКонтекст не переприсваивается); подтверждено tests/unit/Пропагация/ТестW3CПропагатор.os:51-65, 371-542 и tests/unit/Пропагация/ТестW3CBaggageПропагатор.os:121-141` |  |

#### TextMap Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#textmap-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 6 | MUST | ✅ found | In order to increase compatibility, the key-value pairs MUST only consist of US-ASCII characters that make up valid HTTP header fields as per RFC 9110. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:33-41 (Установить пропускает невалидные пары с предупреждением), 57-69 (КлючВалиден - RFC 9110 token), 82-103 (ЗначениеВалидно - VCHAR/SP/HTAB без краевых пробелов); src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:48-67, 232-248 (ключи-token, percent-encoding значений, валидация метаданных); src/Трассировка/Классы/ОтелСостояниеТрассировки.os:339-392 (ключи/значения tracestate - печатный ASCII)` |  |
| 7 | MUST | ✅ found | `Getter` and `Setter` MUST be stateless and allowed to be saved as constants, in order to effectively avoid runtime allocations. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:1-6, 73-75 (нет полей состояния); src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:11-16 (единственное поле - логгер, данных носителя не хранит); создаются один раз и переиспользуются как константы: src/Пропагация/Классы/ОтелW3CПропагатор.os:224-225, src/Пропагация/Классы/ОтелW3CBaggageПропагатор.os:352-353` |  |

#### Set

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#set)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | SHOULD | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:40 (Носитель.Вставить(Ключ, Значение) - ключ без изменения регистра); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:146-159 (СеттерСохраняетРегистрКлюча: Content-Type)` |  |
| 9 | MUST | ✅ found | The implementation SHOULD preserve casing (e.g. it should not transform `Content-Type` to `content-type`) if the used protocol is case insensitive, otherwise it MUST preserve casing. | `src/Пропагация/Классы/ОтелСеттерТекстовойКарты.os:33-41 (регистр ключа сохраняется безусловно, независимо от регистрозависимости протокола)` |  |

#### Keys

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#keys)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 10 | MUST | ✅ found | The `Keys` function MUST return the list of all the keys in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:59-65 (Функция Ключи(Носитель) - Массив всех ключей носителя); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:111-127` |  |

#### Get

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#get)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST | ✅ found | The Get function MUST return the first value of the given propagation key or return null if the key doesn’t exist. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:20-28 (Функция Получить(Носитель, Ключ): возвращает первое совпавшее значение в порядке обхода носителя, иначе Неопределено); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:46-75` |  |
| 12 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:21-23 (Получить: сравнение НРег(КлючИЗначение.Ключ) = НРег(Ключ)); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:29-43` |  |

#### Composite Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#composite-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | Implementations MUST offer a facility to group multiple `Propagator`s from different cross-cutting concerns in order to leverage them as a single entity. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:1-94 (отдельный класс ОтелКомпозитныйПропагатор; конструктор ПриСозданииОбъекта(Пропагаторы) на строке 89 принимает массив пропагаторов, вызов в порядке задания); используется для tracecontext+baggage в src/Конфигурация/Модули/ОтелАвтоконфигурация.os:495` |  |
| 14 | MUST | ✅ found | There MUST be functions to accomplish the following operations. | `src/Пропагация/Классы/ОтелКомпозитныйПропагатор.os:89-92 (Create - Новый ОтелКомпозитныйПропагатор(Массив)), 20-28 (Inject - Процедура Внедрить(Контекст, Носитель, Сеттер)), 41-51 (Extract - Функция Извлечь(Контекст, Носитель, Геттер)); подтверждено tests/unit/Пропагация/ТестКомпозитныйПропагатор.os:11,34` |  |

#### Global Propagators

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#global-propagators)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 15 | MUST | ✅ found | The OpenTelemetry API MUST provide a way to obtain a propagator for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:215-227 (Функция ПолучитьПропагаторы - единственный поддерживаемый тип TextMapPropagator); также src/Ядро/Классы/ОтелSdk.os:54-56 (Функция Пропагаторы)` |  |
| 16 | SHOULD | ➖ n_a | Instrumentation libraries SHOULD call propagators to extract and inject the context on all remote calls. | - | Требование адресовано Instrumentation Libraries (политика их поведения); данный пакет реализует только API+SDK, IL не включены (единственная интеграция src/Интеграции/Классы/ОтелАппендерLogos.os - мост логов logos, удалённых вызовов не выполняет). |
| 17 | MUST | ✅ found | The OpenTelemetry API MUST use no-op propagators unless explicitly configured otherwise. | `src/Ядро/Модули/ОтелГлобальный.os:215-227 (ПолучитьПропагаторы: явно установленные -> пропагаторы SDK -> иначе no-op), 279-287 (ПолучитьИлиСоздатьПропагаторыПоУмолчанию возвращает Новый ОтелНоопПропагатор()); src/Пропагация/Классы/ОтелНоопПропагатор.os:1-52; подтверждено tests/unit/Ядро/ТестГлобальный.os:235-258` |  |
| 18 | SHOULD | ✅ found | If pre-configured, `Propagator`s SHOULD default to a composite `Propagator` containing the W3C Trace Context Propagator and the Baggage `Propagator` specified in the Baggage API. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:456-496 (СоздатьПропагаторы: по умолчанию "tracecontext,baggage" (стр. 460-462) -> Новый ОтелКомпозитныйПропагатор), 1434-1438 (ДобавитьПропагатор: ОтелW3CПропагатор + ОтелW3CBaggageПропагатор); аналогично src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:204-211` |  |
| 19 | MUST | ✅ found | These platforms MUST also allow pre-configured propagators to be disabled or overridden. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:466-482 (otel.propagators=none отключает - ОтелНоопПропагатор; иные значения переопределяют состав); src/Ядро/Модули/ОтелГлобальный.os:202-204, 216-219 (УстановитьПропагаторы - программное переопределение, приоритетнее пропагаторов SDK); src/Ядро/Классы/ОтелПостроительSdk.os:65-68` |  |

#### Get Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#get-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | This method SHOULD exist for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:215-227 (Функция ПолучитьПропагаторы - глобальный TextMap-пропагатор, обычно ОтелКомпозитныйПропагатор); подтверждено tests/unit/Ядро/ТестГлобальный.os:216-228` |  |

#### Set Global Propagator

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#set-global-propagator)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | SHOULD | ✅ found | This method SHOULD exist for each supported `Propagator` type. | `src/Ядро/Модули/ОтелГлобальный.os:202-204 (Процедура УстановитьПропагаторы(Пропагаторы) - отдельный глобальный сеттер, независимый от SDK); подтверждено tests/unit/Ядро/ТестГлобальный.os:262-273` |  |

#### Propagators Distribution

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#propagators-distribution)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 22 | MUST | ➖ n_a | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry Core packages: | - | Требование адресовано OpenTelemetry Organization (официальный реестр пропагаторов); данный пакет является независимой SDK-реализацией, не официальным дистрибутивом OTel. Для справки: W3C TraceContext и W3C Baggage входят в основной пакет (lib.config:133-134), B3 вынесен в отдельный пакет opentelemetry-propagator-b3 и подгружается рефлексивно (src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1406-1425). |
| 23 | MUST | ➖ n_a | The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST be distributed as OpenTelemetry Core packages: | - | Требование адресовано OpenTelemetry Organization (официальный реестр пропагаторов); данный пакет является независимой SDK-реализацией, не официальным дистрибутивом OTel. Порядок распространения официальных OpenTelemetry Core packages к независимому opm-пакету opentelemetry как к субъекту требования не применим. |
| 24 | MUST NOT | ➖ n_a | It MUST NOT use `OpenTracing` in the resulting propagator name as it is not widely adopted format in the OpenTracing ecosystem. | - | Требование адресовано OpenTelemetry Organization (официальный реестр пропагаторов); данный пакет является независимой SDK-реализацией, не официальным дистрибутивом OTel. Правило именования относится к пропагатору OT Trace из списка дополнительных пропагаторов, которые организация OTel MAY сопровождать как Core packages; в этом репозитории OT Trace не реализован (поиск opentracing / ottrace / ot-tracer по src/ - совпадений нет), а ни один из имеющихся пропагаторов (lib.config:131-137; имена tracecontext, baggage, b3, b3multi, none в src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1434-1447) не использует OpenTracing в имени. |
| 25 | MUST NOT | ✅ found | Additional `Propagator`s implementing vendor-specific protocols such as AWS X-Ray trace header protocol MUST NOT be maintained or distributed as part of the OpenTelemetry Core packages. | `lib.config:131-137; src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1434-1447; src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:766-778` |  |

#### W3C Trace Context Requirements

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#w3c-trace-context-requirements)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 26 | MUST | ✅ found | A W3C Trace Context propagator MUST parse and validate the `traceparent` and `tracestate` HTTP headers as specified in W3C Trace Context Level 2. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:99-167,196-210; src/Трассировка/Классы/ОтелСостояниеТрассировки.os:238-392` |  |
| 27 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid `traceparent` value using the same header. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:69-81` |  |
| 28 | MUST | ✅ found | A W3C Trace Context propagator MUST propagate a valid `tracestate` unless the value is empty, in which case the `tracestate` header may be omitted. | `src/Пропагация/Классы/ОтелW3CПропагатор.os:83-85` |  |

#### B3 Extract

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-extract)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 29 | MUST | ➖ n_a | MUST attempt to extract B3 encoded using single and multi-header formats. | - | B3-пропагатор в репозитории отсутствует: grep -r B3 src/ находит только комментарии и рефлексивную загрузку класса ОтелB3Пропагатор по имени (src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1396-1442), самого класса нет ни в src/Пропагация/Классы/, ни в lib.config:131-137. Он намеренно поставляется отдельным пакетом opentelemetry-propagator-b3 (docs/architecture.md:258-262), поэтому извлечение single/multi-header форматов с приоритетом single-header реализуется во внешнем пакете и не проверяемо по коду данного репозитория. |
| 30 | MUST | ➖ n_a | MUST preserve a debug trace flag, if received, and propagate it with subsequent requests. | - | Класс ОтелB3Пропагатор в репозитории отсутствует (отдельный пакет opentelemetry-propagator-b3, рефлексивная загрузка в src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1406-1425). Сохранение debug-флага (X-B3-Flags / 'd' в single-header) и его пропагация в последующих запросах - логика этого внешнего класса, не проверяемая по коду данного репозитория. |
| 31 | MUST | ➖ n_a | Additionally, an OpenTelemetry implementation MUST set the sampled trace flag when the debug flag is set. | - | Класс ОтелB3Пропагатор в репозитории отсутствует (отдельный пакет opentelemetry-propagator-b3, рефлексивная загрузка в src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1406-1425). Установка sampled trace flag при наличии debug-флага выполняется при извлечении во внешнем классе и не проверяема по коду данного репозитория. |
| 32 | MUST NOT | ➖ n_a | MUST NOT reuse `X-B3-SpanId` as the ID for the server-side span. | - | Класс ОтелB3Пропагатор в репозитории отсутствует (отдельный пакет opentelemetry-propagator-b3, рефлексивная загрузка в src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1406-1425); интерпретация X-B3-SpanId при извлечении - ответственность внешнего класса. Со стороны SDK: трассировщик всегда генерирует новый SpanId для создаваемого спана, а извлечённый удалённый контекст используется только как родитель (src/Трассировка/Классы/ОтелТрассировщик.os:235). |

#### B3 Inject

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#b3-inject)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 33 | MUST | ➖ n_a | MUST default to injecting B3 using the single-header format | - | Класс ОтелB3Пропагатор (отдельный пакет opentelemetry-propagator-b3) в репозитории отсутствует; его собственный формат внедрения по умолчанию и фактически записываемые заголовки определяются внешним пакетом и не проверяемы здесь. Для справки: автоконфигурация SDK для значения b3 явно передаёт конструктору формат 'single' (src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1409-1412), что согласуется с опцией B3 Single из таблицы Configuration спецификации. |
| 34 | MUST | ✅ found | MUST provide configuration to change the default injection format to B3 multi-header | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1406-1414,1439-1443` |  |
| 35 | MUST NOT | ➖ n_a | MUST NOT propagate `X-B3-ParentSpanId` as OpenTelemetry does not support reusing the same ID for both sides of a request. | - | Класс ОтелB3Пропагатор в репозитории отсутствует (отдельный пакет opentelemetry-propagator-b3, рефлексивная загрузка в src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1406-1425); набор внедряемых B3-заголовков (в т.ч. отказ от X-B3-ParentSpanId) определяется внешним классом. В коде данного репозитория заголовок X-B3-ParentSpanId нигде не формируется (поиск по src/ - совпадений нет). |

#### Fields

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#fields)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ➖ n_a | Fields MUST return the header names that correspond to the configured format, i.e., the headers used for the inject operation. | - | Требование относится к методу Поля() B3-пропагатора, которого нет в репозитории: grep -r B3 src/ находит только рефлексивную загрузку класса ОтелB3Пропагатор по имени (src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1396-1442), а не сам класс; в src/Пропагация/Классы/ и lib.config:131-137 его нет. Поля() для B3 реализуется в отдельном пакете opentelemetry-propagator-b3. Для справки: в пропагаторах этого репозитория Поля() возвращает именно заголовки, используемые при Внедрить (src/Пропагация/Классы/ОтелW3CПропагатор.os:174-179). |

### Env Vars

#### Environment Variable Specification

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#environment-variable-specification)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | If they do, they SHOULD use the names and value parsing behavior specified in this document. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:6-74,149-155,291-337,456-495,948-954,980-992,1006-1015,1079-1089,1102-1108,1122-1140,1233-1242,1277-1293; src/Ядро/Классы/ОтелРесурс.os:143-158; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:114-129` |  |
| 2 | SHOULD | ✅ found | They SHOULD also follow the common configuration specification. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:459-495,980-992,1006-1015,1079-1089,1122-1140,1155-1158,1191-1200,1233-1242; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:272; src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:541-549` |  |

#### Implementation guidelines

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#implementation-guidelines)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 3 | MUST | ✅ found | The environment-based configuration MUST have a direct code configuration equivalent. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:135-141,342-345,417-440,538-544,637-642,789-792; src/Ядро/Классы/ОтелПостроительSdk.os:26-99; src/Трассировка/Классы/ОтелПостроительПровайдераТрассировки.os:30-105; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:28-84; src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:429; src/Экспорт/Классы/ОтелНастройкиTls.os:16-23; src/Ядро/Модули/ОтелГлобальный.os:241-254` |  |

#### Parsing empty value

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#parsing-empty-value)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | The SDK MUST interpret an empty value of an environment variable the same way as when the variable is unset. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:110-118,184,199,228,292,460-462,595-596,924,950-951,981,1080,1102-1108,1123-1125,1310,1366; src/Ядро/Классы/ОтелРесурс.os:145,155; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:117; src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:248` |  |

#### Boolean

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#boolean)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST | ✅ found | Any value that represents a Boolean MUST be set to true only by the case-insensitive string `"true"`, meaning `"True"` or `"TRUE"` are also accepted, as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:948-954,1277-1293,1365-1370` |  |
| 6 | MUST NOT | ✅ found | An implementation MUST NOT extend this definition and define additional values that are interpreted as true. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1282-1292` |  |
| 7 | MUST | ✅ found | Any value not explicitly defined here as a true value, including unset and empty values, MUST be interpreted as false. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:948-954,1277-1293,1365-1370; src/Экспорт/Классы/ОтелНастройкиTls.os:49` |  |
| 8 | SHOULD | ✅ found | If any value other than a true value, case-insensitive string `"false"`, empty, or unset is used, a warning SHOULD be logged to inform users about the fallback to false being applied. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1285-1291` |  |
| 9 | SHOULD | ✅ found | All Boolean environment variables SHOULD be named and defined such that false is the expected safe default behavior. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:7,65,948-954,1365-1370; src/Экспорт/Классы/ОтелНастройкиTls.os:49` |  |
| 10 | MUST NOT | ✅ found | Renaming or changing the default value MUST NOT happen without a major version upgrade. | `packagedef:7` |  |

#### Numeric

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#numeric)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | SHOULD | ✅ found | The following paragraph was added after stabilization and the requirements are thus qualified as “SHOULD” to allow implementations to avoid breaking changes. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1122-1140,1155-1158` |  |
| 12 | MUST | ✅ found | For new implementations, these should be treated as MUST requirements. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1122-1140,1155-1158,1191-1200` |  |
| 13 | SHOULD | ✅ found | For variables accepting a numeric value, if the user provides a value the implementation cannot parse, the implementation SHOULD generate a warning and gracefully ignore the setting, i.e., treat them ... | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1006-1015,1122-1140,1155-1158,1168-1177` |  |

#### Enum

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#enum)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 14 | SHOULD | ✅ found | Enum values SHOULD be interpreted in a case-insensitive manner. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:297,397,468,487,984,1028,1083,1234; src/Метрики/Модули/ОтелФильтрЭкземпляров.os:54` |  |
| 15 | MUST | ✅ found | For sources accepting an enum value, if the user provides a value the implementation does not recognize, the implementation MUST generate a warning and gracefully ignore the setting. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:321-334,402-409,928-930,990-991,1033-1037,1087-1088,1233-1242,1415-1423,1444-1445; src/Метрики/Классы/ОтелПостроительПровайдераМетрик.os:121-126` |  |

#### General SDK Configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#general-sdk-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 16 | MUST | ✅ found | Values MUST be deduplicated in order to register a `Propagator` only once. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:485-493` |  |
| 17 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1006-1011,1128-1138,1252-1262` |  |
| 18 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:1008,1012,1139,1254-1262` |  |
| 19 | MUST | ✅ found | Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e. the implementation MUST behave as if OTEL_TRACES_SAMPLER_ARG is not set. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:299,308-309,319-320,1007-1008,1012` |  |

#### Attribute Limits

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#attribute-limits)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | SHOULD | ✅ found | Implementations SHOULD only offer environment variables for the types of attributes, for which that SDK implements truncation mechanism. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:509-545,661-676; src/Трассировка/Классы/ОтелСпан.os:332-333,362-363,444,561-565,690-708,718-730; src/Трассировка/Классы/ОтелСобытиеСпана.os:104-117; src/Логирование/Классы/ОтелЗаписьЛога.os:242-249; src/Ядро/Модули/ОтелУтилиты.os:385-387,556-580` |  |

#### Exporter Selection

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#exporter-selection)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 21 | SHOULD NOT | ✅ found | It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:741-742,1233-1242` |  |
| 22 | SHOULD NOT | ✅ found | It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:382-383,1233-1242` |  |
| 23 | SHOULD NOT | ✅ found | It SHOULD NOT be supported by new implementations. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:807-808,1233-1242` |  |

#### Declarative configuration

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#declarative-configuration)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 24 | MUST | ✅ found | When `OTEL_CONFIG_FILE` is set, all other environment variables besides those referenced in the configuration file for environment variable substitution MUST be ignored. | `src/Конфигурация/Модули/ОтелАвтоконфигурация.os:104-126; src/Конфигурация/Модули/ОтелКонфигурационнаяФабрика.os:72-73,784; src/Ядро/Классы/ОтелРесурс.os:102-107,138-140; src/Конфигурация/Модули/ОтелФайловаяКонфигурация.os:32; src/Конфигурация/Модули/ОтелПодстановкаПеременных.os:246` |  |

### Prometheus Compatibility

#### Differences between Prometheus formats

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#differences-between-prometheus-formats)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | Exemplars MUST be dropped if they are not supported. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:720-748,761-782,795-806; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:581-584,692-694` |  |
| 2 | MUST | ✅ found | If the specification below requires producing a Prometheus Info-typed metric, a Prometheus Gauge with an additional `_info` name suffix MUST be produced if Info-typed metrics are not supported. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:504-516,563-567,739-740; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:615-626,638-648,659-671` |  |
| 3 | MUST | ✅ found | If the specification below requires producing a Prometheus StateSet-typed metric, a Prometheus Gauge MUST be produced instead if StateSet-typed metrics are not supported. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:563-570,745-746; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:659-671` |  |
| 4 | SHOULD | ✅ found | Exponential (Native) Histograms SHOULD be dropped if they are not supported, or MAY be converted to fixed-bucket histograms. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:596-598,637-644` |  |

#### Metric Metadata

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#metric-metadata)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 5 | MUST NOT | ✅ found | Prometheus Pull exporters for OpenTelemetry metric data MUST NOT allow duplicate UNIT, HELP, or TYPE comments for the same metric name to be returned in a single scrape of the Prometheus endpoint. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:604-606,698-718,1148-1154,1184-1201; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:497-519,527-556` |  |
| 6 | MUST | ✅ found | Exporters MUST drop entire metrics to prevent conflicting TYPE comments, but SHOULD NOT drop metric points as a result of conflicting UNIT or HELP comments. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:604-606,1184-1201` |  |
| 7 | SHOULD NOT | ✅ found | Exporters MUST drop entire metrics to prevent conflicting TYPE comments, but SHOULD NOT drop metric points as a result of conflicting UNIT or HELP comments. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:622-625,698-718,1043-1064` |  |
| 8 | SHOULD | ✅ found | Instead, all but one of the conflicting UNIT and HELP comments (but not metric points) SHOULD be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:698-718,1043-1064` |  |
| 9 | SHOULD | ✅ found | If dropping a comment or metric points, the exporter SHOULD warn the user through error logging. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:608-617,640-653,677-679,1043-1064,1120-1121,1198-1199` |  |
| 10 | MUST | ✅ found | The Name of an OTLP metric MUST be added as the Prometheus Metric Name. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:504-540,600-603,1279-1291` |  |
| 11 | SHOULD | ✅ found | Discouraged characters in the metric name SHOULD be replaced with the `_` character by default, aiming for compatibility with Prometheus conventions. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1810-1828,1861` |  |
| 12 | SHOULD | ✅ found | Multiple consecutive `_` characters SHOULD be replaced with a single `_` character. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1816,1862` |  |
| 13 | MUST | ✅ found | The Unit of an OTLP metric point MUST be converted from the UCUM unit to the equivalent unit word in Prometheus if it is included in the table in Metric Metadata above. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1304-1324,1353-1359,1772-1798` |  |
| 14 | MUST | ✅ found | Portions of the Unit within brackets (e.g. {packet}) MUST be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1308,1865` |  |
| 15 | MUST | ✅ found | Units defined as rates over time (e.g. “m/s”) MUST be converted to words (e.g. “meters_per_second”). | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1309-1316,1335-1341,1800-1807` |  |
| 16 | SHOULD | ✅ found | The resulting unit SHOULD be added to the metric as UNIT metadata. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:699,713; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:553-556` |  |
| 17 | SHOULD | ✅ found | A suffix to the metric name SHOULD be added unless the metric name already ends with the unit (before type-specific suffixes). | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1279-1291` |  |
| 18 | MUST | ✅ found | The description of an OTLP metrics point MUST be added as HELP metadata. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:712; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:439-452,549` |  |
| 19 | MUST | ✅ found | The data point type of an OTLP metric MUST be added as TYPE metadata. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:552-571,711; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:550,659-671` |  |

#### Instrumentation Scope

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#instrumentation-scope)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 20 | MUST | ✅ found | Prometheus exporters MUST by default add the scope name as the `otel_scope_name` label, the scope version as the `otel_scope_version` label, the scope schema URL as the `otel_scope_schema_url` label, ... | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:373-374,453-454,1376-1381,1482-1505,1537-1548` |  |
| 21 | MUST | ✅ found | Scope attributes that, after adding the `otel_scope_` prefix and applying the label-name conversion described in `Metric Attributes`, would conflict with `otel_scope_name`, `otel_scope_version`, or `o... | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1483-1497` |  |

#### Gauges

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#gauges)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 22 | MUST | ✅ found | An OpenTelemetry Gauge MUST be converted following a hint present in metric.metadata: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:552-571; src/Метрики/Классы/ОтелДанныеМетрики.os:139-150` |  |
| 23 | MUST | ✅ found | If the `prometheus.type` key is absent, or its value is equal to `gauge`, the datapoint MUST be transformed to a Prometheus Gauge. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:563,568-569` |  |
| 24 | MUST | ✅ found | If the `prometheus.type` key has value equal to `unkown`, the datapoint MUST be transformed to a Prometheus Unknown. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:563-565; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:659-671` |  |
| 25 | SHOULD | ✅ found | If the `prometheus.type` key has value equal to `info`, the datapoint SHOULD be transformed to a Prometheus Info. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:504-512,566-567,739-740` |  |
| 26 | SHOULD | ✅ found | If the `prometheus.type` key has value equal to `stateset`, the datapoint SHOULD be transformed to a Prometheus Stateset. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:566-567,745-746` |  |
| 27 | SHOULD | ✅ found | Exemplars on OpenTelemetry Gauges SHOULD be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:733-748; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:692-694` |  |

#### Sums

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#sums)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 28 | MUST | ✅ found | An OpenTelemetry Sum MUST be converted following the rules below: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:552-571,595-626,669-681,733-748` |  |
| 29 | MUST | ✅ found | If the aggregation temporality is cumulative and the sum is monotonic, it MUST be converted to a Prometheus Counter. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:330-332,560-562,669-681` |  |
| 30 | SHOULD | ✅ found | If the metric name for monotonic Sum metric points does not end in a suffix of `_total` a suffix of `_total` SHOULD be added by default, otherwise the name MUST remain unchanged. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:504-516,1279-1291` |  |
| 31 | MUST | ✅ found | If the metric name for monotonic Sum metric points does not end in a suffix of `_total` a suffix of `_total` SHOULD be added by default, otherwise the name MUST remain unchanged. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:505-506,515,1281-1285` |  |
| 32 | SHOULD | ✅ found | Monotonic Sum metric points with `StartTimeUnixNano` SHOULD transform `StartTimeUnixNano` into Prometheus `StartTime`, following the appropriate format used by each Prometheus protocol. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:741-744,816-821; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:595-599,705-711` |  |
| 33 | MUST | ✅ found | If Sum is converted to a Prometheus Counter, then `Exemplars` MUST be converted as described in the Exemplar Conversion section. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:741-744,829-833,909-935; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:589-592,692-694,721-731` |  |
| 34 | SHOULD | ✅ found | Otherwise, `Exemplars` SHOULD be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:733-748` |  |
| 35 | SHOULD | ✅ found | If the Prometheus protocol only supports a single exemplar on the Counter sample, the latest exemplar SHOULD be converted. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:743,843-845,858-874` |  |

#### Histograms

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#histograms)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 36 | MUST | ✅ found | An OpenTelemetry Histogram with a cumulative aggregation temporality MUST be converted to a Prometheus Histogram by default. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:330-332,554-556,761-782` |  |
| 37 | MUST | ✅ found | OpenTelemetry Histograms with Delta aggregation temporality MAY be aggregated into a Cumulative aggregation temporality and follow the logic below, or MUST be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:330-332,596-599,669-681` |  |

#### Histograms as Prometheus Histograms

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#histograms-as-prometheus-histograms)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 38 | MUST | ✅ found | When converting to a Prometheus Histogram, an OpenTelemetry Histogram MUST be converted following the rules below: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:761-782; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:325-372` |  |
| 39 | SHOULD | ✅ found | If set, `StartTimeUnixNano` SHOULD be transformed into Prometheus `StartTime`, following the appropriate format used by each Prometheus protocol. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:780-781,816-821; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:595-599,705-711` |  |
| 40 | SHOULD | ✅ found | If the Prometheus protocol only supports a single exemplar per-bucket, the latest exemplar that falls into each bucket SHOULD be converted. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:768-776,858-887` |  |

#### Summaries

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#summaries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 41 | MUST | ✅ found | An OpenTelemetry Summary MUST be converted to a Prometheus Summary as follows: | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:557-559,733-738,795-806` |  |
| 42 | MUST | ✅ found | The `quantile` label value MUST be the stringified floating point value of each quantile (between 0.0 and 1.0), starting from lowest to highest, and all being non-negative. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:796-802,988-1002; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:392-437,747-778` |  |
| 43 | SHOULD NOT | ✅ found | Explicit timestamps SHOULD NOT be used for pull protocols, such as the Prometheus text exposition format, where Prometheus assigns the scrape timestamp. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1015-1022; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:126-140` |  |
| 44 | SHOULD | ✅ found | Exemplars on OpenTelemetry Summaries SHOULD be dropped. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:795-806; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:692-694` |  |

#### Metric Attributes

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#metric-attributes)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 45 | MUST | ✅ found | OpenTelemetry Metric Attributes MUST be converted to Prometheus labels. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1376-1381,1537-1548,1591-1601` |  |
| 46 | MUST | ✅ found | String Attribute values are converted directly to Metric Attributes, and non-string Attribute values MUST be converted to string attributes following the attribute specification. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1652-1669,1680-1766` |  |
| 47 | SHOULD | ✅ found | Discouraged characters SHOULD be replaced with the `_` character. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1810-1828,1839-1841,1861` |  |
| 48 | SHOULD | ✅ found | Multiple consecutive `_` characters SHOULD be replaced with a single `_` character. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1816,1839-1841,1862` |  |
| 49 | MUST | ✅ found | In such cases, the values MUST be concatenated together, separated by `;`, and ordered by the lexicographical order of the original keys. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1376-1381,1537-1548,1559-1601,1609-1639` |  |

#### Exemplar Conversion

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#exemplar-conversion)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 50 | MUST | ✅ found | When an exemplar is converted per the metric-type-specific sections above, the OpenTelemetry Exemplar MUST be converted to a Prometheus exemplar if the Prometheus (push or pull) protocol being used su... | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:743,776,829-833,909-935; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:581-592,692-694,721-731` |  |
| 51 | MUST | ✅ found | If present, the OpenTelemetry Exemplar’s Trace ID and Span ID MUST be added as Exemplar labels using the `trace_id` and `span_id` keys, respectively. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:912-920,924-926` |  |
| 52 | MUST | ✅ found | These labels MUST take precedence over labels from `filtered_attributes` in cases where there is a key collision. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:911,918,924-926` |  |
| 53 | MUST | ✅ found | Timestamps MUST be added as timestamps on the Prometheus exemplar. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:930-933,976-978; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:725-728` |  |
| 54 | MUST | ✅ found | `filtered_attributes` MUST be added as labels on the Prometheus exemplar, unless they would exceed the Prometheus protocol’s exemplar limits. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:910-911,921-923,945-974` |  |

### Prometheus Exporter

#### Client Libraries

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#client-libraries)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | SHOULD | ✅ found | A Prometheus Exporter SHOULD use an official Prometheus client library when one exists for the implementation language and it is practical to do so (e.g., dependency concerns) for serving Prometheus m... | `packagedef:32; src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:4` |  |
| 2 | SHOULD NOT | ❌ not_found | A Prometheus Exporter SHOULD use an official Prometheus client library when one exists for the implementation language and it is practical to do so (e.g., dependency concerns) for serving Prometheus m... | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:4,107,116,208-210; packagedef:32; opm-metadata.xml:22` | Экспортер использует неофициальную клиентскую библиотеку Prometheus: пакет prometheus 1.0.6 (yellow-hammer/prometheus, автор Ivan Karlo) - стороннюю библиотеку для OneScript с реестром коллекторов, типами метрик и сериализацией в text format/OpenMetrics. В списке официальных клиентских библиотек Prometheus (Go, Java/Scala, Python, Ruby, Rust) ее нет; официальной библиотеки для OneScript не существует. Зависимость времени выполнения объявлена в packagedef:32 и opm-metadata.xml:22 (dev=false). Выдачу метрик целиком формирует эта библиотека: ОтелПрометеусЧитательМетрик подключает ее (#Использовать prometheus, стр. 4), текст text format 0.0.4 строит Prometheus.СериализоватьВТекст (стр. 107), Content-Type берется из Prometheus.ContentTypeМетрик (стр. 116), выдача OpenMetrics (exemplars, _created, UNIT) возможна только через CollectorRegistry библиотеки, куда читатель отдает семейства методом Collect() (стр. 208-210). Собственного сериализатора формата экспозиции без библиотеки нет (документация Prometheus допускает реализовать формат экспозиции самостоятельно, если клиентской библиотеки для языка нет), поэтому SHOULD NOT не соблюдено. |
| 3 | SHOULD | ✅ found | If a Prometheus client library is used, the OpenTelemetry Prometheus Exporter SHOULD be modeled as a custom Collector so it can be used in conjunction with existing Prometheus instrumentation. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:201-210; oscript_modules/prometheus/src/Классы/CollectorRegistry.os:23-39,64-87` |  |

#### Version and Format

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#version-and-format)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 4 | MUST | ✅ found | Regardless of whether a Prometheus client library is used, the Prometheus Exporter MUST support version `0.0.4` of the Text-based format. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:90-117; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:15-17,56-62,463-488` |  |
| 5 | MUST NOT | ✅ found | A Prometheus Exporter for an OpenTelemetry metrics SDK MUST NOT use Prometheus Remote Write format or OpenMetrics protobuf format. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:102-117,208-210; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:33-47,929-949` |  |
| 6 | SHOULD NOT | ✅ found | A Prometheus Exporter for an OpenTelemetry metrics SDK SHOULD NOT add explicit timestamps on Metric points. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1015-1022; oscript_modules/prometheus/src/Модули/PrometheusTextFormat.os:126-140,571-600` |  |

#### Target

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#target)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 7 | MUST | ✅ found | There MUST be at most one `target` info metric exposed by an SDK Prometheus exporter. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:366-391,1184-1201,1392-1410; tests/unit/Метрики/ТестПрометеусЧитательМетрик.os:1664-1682` |  |

#### Temporality

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#temporality)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 8 | MUST | ✅ found | A Prometheus Exporter MUST set the MetricReader `temporality` as a function of instrument kind to be `cumulative` for all instrument kinds. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:119-131,322-332; src/Метрики/Модули/ОтелПотокиМетрик.os:152-175; src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:127-131; src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:271-273` |  |

#### Default Aggregation

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#default-aggregation)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 9 | SHOULD | ✅ found | A Prometheus Exporter SHOULD support a configuration option to set the MetricReader default `aggregation` as a function of instrument kind. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:298-320; src/Метрики/Модули/ОтелПотокиМетрик.os:412-440` |  |
| 10 | MUST | ✅ found | This option MAY be named `default_aggregation`, and MUST use the default aggregation by default. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:307-310,1871; src/Метрики/Модули/ОтелАгрегация.os:15-17,153-167,180-187,406-417` |  |

#### Resource Attributes as Metric Labels

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#resource-attributes-as-metric-labels)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 11 | MUST NOT | ✅ found | By default, it MUST NOT add any resource attributes as metric labels. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:40-43,1392-1396,1868` |  |
| 12 | SHOULD | ✅ found | The configuration SHOULD allow the user to select resource attributes to include or exclude. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:212-228,1392-1468` |  |

#### Scope Info

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/metrics/sdk_exporters/prometheus/#scope-info)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 13 | MUST | ✅ found | The option MAY be named `scope_info_enabled`, and MUST be `true` by default. | `src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:370-381,1136-1138,1376-1381,1482-1505` |  |

## Условные требования (Conditional)

Требования из условных секций. Применяются только при реализации соответствующей опциональной фичи.

### Propagators

#### GetAll

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#getall) | Scope: conditional:GetAll Getter (post-stable extension)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ✅ found | If explicitly implemented, the `GetAll` function MUST return all values of the given propagation key. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:40-49 (Функция ПолучитьВсе(Носитель, Ключ): собирает все совпавшие значения в Массив); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:78-94; обратная совместимость для геттеров без ПолучитьВсе - src/Пропагация/Классы/ОтелW3CПропагатор.os:196-210 (Рефлектор.МетодСуществует)` |  |
| 2 | SHOULD | ✅ found | It SHOULD return them in the same order as they appear in the carrier. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:43-47 (ПолучитьВсе: Для Каждого по носителю, Результат.Добавить в порядке обхода); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:78-94 (Результат[0]="первое", Результат[1]="второе")` |  |
| 3 | SHOULD | ✅ found | If the key doesn’t exist, it SHOULD return an empty collection. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:41,48 (Результат = Новый Массив() возвращается пустым при отсутствии совпадений); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:97-109` |  |
| 4 | MUST | ✅ found | If the getter is intended to work with an HTTP request object, the getter MUST be case insensitive. | `src/Пропагация/Классы/ОтелГеттерТекстовойКарты.os:42-44 (ПолучитьВсе: сравнение НРег(КлючИЗначение.Ключ) = НРег(Ключ)); подтверждено tests/unit/Пропагация/ТестГеттерСеттер.os:78-94 (ключи traceparent/Traceparent)` |  |

### Prometheus Compatibility

#### Metric Metadata

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#metric-metadata) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | The Prometheus Metric Name MUST be added as the Name of the OTLP metric. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus 1.0.6 (только реестр и сериализация: CollectorRegistry, PrometheusTextFormat.Сериализовать) нет scrape и разбора экспозиции (# TYPE/# HELP/# UNIT, сэмплы), у ИнтерфейсПродюсерМетрик нет реализации-моста из Prometheus. Имя Prometheus-метрики в имя OTLP-метрики не переносится: принимаемых Prometheus-метрик нет. |
| 2 | SHOULD NOT | ➖ n_a | The name SHOULD NOT be altered. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Имена Prometheus-метрик в OTLP не переносятся, поэтому требование не применимо. Нормализация имени в ОтелПрометеусЧитательМетрик (БазовоеИмя/НормализоватьИмя) относится к обратному направлению OTLP → Prometheus и к этому требованию не относится. |
| 3 | MUST | ➖ n_a | Prometheus UNIT metadata, if present, MUST be converted to the unit of the OTLP metric. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus 1.0.6 (только сериализация) нет разбора экспозиции, строки # UNIT Prometheus не читаются, переводить единицу в OTLP не из чего. |
| 4 | MUST | ➖ n_a | The unit MUST be translated from words to the UCUM abbreviation if it is in the following set of commonly-used units: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Таблица ЗаполнитьСловаЕдиниц читателя переводит в обратную сторону (UCUM → слова Prometheus) для экспорта; перевода слов единиц Prometheus в UCUM при приеме нет, так как приема нет. |
| 5 | MUST | ➖ n_a | Prometheus HELP metadata, if present, MUST be added as the description of the OTLP metric. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus 1.0.6 (только сериализация) нет разбора экспозиции, строки # HELP не читаются; описание OTel-метрики пишется в HELP только при экспорте (СемействоМетрики). |
| 6 | MUST | ➖ n_a | Prometheus TYPE metadata, if present, MUST be used to determine the OTLP data type, and dictates type-specific conversion rules listed below. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Строки # TYPE не разбираются; ВидPrometheus выбирает тип Prometheus по типу OTel-метрики (обратное направление). |
| 7 | MUST | ➖ n_a | The TYPE metadata MUST also be added to the OTLP metric.metadata under the `prometheus.type` key (e.g. `prometheus.type="unknown"`). | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. ОтелДанныеМетрики хранит metadata, а читатель только читает подсказку prometheus.type при экспорте (ВидPrometheus); записи TYPE принятой Prometheus-метрики в metadata нет, так как приема нет. |

#### Timestamps

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#timestamps) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | If present, the Prometheus Metric Sample’s Start timestamp (also referred to as the Created timestamp) MUST be converted to the Start timestamp of the OTLP data point. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Реализовано только обратное направление: УстановитьВремяСоздания переводит startTimeUnixNano в сэмпл _created при экспорте; разбора _created/Created timestamp принятых сэмплов нет. |
| 2 | SHOULD | ➖ n_a | If no start timestamp is present, the start time of the OTLP data point SHOULD be left unset. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Точки данных OTLP из Prometheus-сэмплов не строятся, поэтому оставлять время старта незаполненным не для чего. |
| 3 | MUST | ➖ n_a | If present, the Prometheus Metric Sample’s Timestamp MUST be converted to the Timestamp of the OTLP data point. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus 1.0.6 (только сериализация) нет разбора сэмплов экспозиции, временные метки Prometheus-сэмплов не читаются. |
| 4 | MUST | ➖ n_a | For metrics scraped from a Prometheus endpoint without an explicit timestamp, the timestamp of the OTLP data point MUST be set to the time of the scrape. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. SDK не скрейпит Prometheus-эндпоинты (scrape нет ни в src/, ни в зависимости prometheus 1.0.6), поэтому времени скрейпа нет. |

#### Counters

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#counters) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | A Prometheus Counter MUST be converted to an OTLP Sum with `is_monotonic` equal to `true`. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Prometheus Counter не принимается; реализовано только обратное направление (монотонная Sum → counter в ВидPrometheus). |
| 2 | MUST | ➖ n_a | Exemplars on the Prometheus Counter Sample MUST be converted to OpenTelemetry Exemplars on the OpenTelemetry Sum data point following the rules in Exemplars. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Exemplars Prometheus-сэмплов не разбираются; ЭкземплярPrometheus переводит exemplars только в обратном направлении (OTLP → Prometheus). |

#### Gauges

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#gauges) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | A Prometheus Gauge MUST be converted to an OTLP Gauge. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus 1.0.6 (только сериализация) нет разбора экспозиции; Prometheus Gauge не принимается и в OTLP Gauge не переводится. |

#### Histograms

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#histograms) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | A Prometheus Histogram MUST be converted to an OTLP Histogram. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Prometheus Histogram не принимается; реализовано только обратное направление (OTLP Histogram → _bucket/_sum/_count в ДобавитьСэмплыГистограммы). |
| 2 | MUST | ➖ n_a | In the text format, Prometheus histograms buckets, count and sum are sent as separate samples and they MUST be merged together when forming an OTLP Histogram. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Сэмплы text format (_bucket, _count, _sum) не разбираются и не объединяются; ДобавитьСэмплыГистограммы выполняет обратную операцию - расщепляет OTLP-гистограмму на отдельные сэмплы. |
| 3 | MUST | ➖ n_a | If `_count` is not present, the metric MUST be dropped. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Принимаемых Prometheus-гистограмм нет, проверять наличие _count и отбрасывать нечего. |
| 4 | MUST | ➖ n_a | If `_sum` is not present, the histogram’s sum MUST be unset. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. OTLP-гистограммы из Prometheus-сэмплов не строятся, поэтому оставлять sum незаполненным при отсутствии _sum не для чего. |
| 5 | MUST | ➖ n_a | Exemplars on the Prometheus Histogram Sample MUST be converted to OpenTelemetry Exemplars on the OpenTelemetry Histogram data point following the rules in Exemplars. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Exemplars Prometheus-гистограмм не разбираются; ЭкземплярPrometheus/ПоследниеЭкземплярыБакетов работают только в обратном направлении (OTLP → Prometheus). |

#### Native Histograms

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#native-histograms) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | A Prometheus Native Histogram with standard (exponential) schema (i.e. schemas -4 to 8) and which are of the integer and counter flavor MUST be converted to an OTLP Exponential Histogram as follows: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Native histograms (protobuf/Remote Write) не принимаются: ни в src/, ни в зависимости prometheus 1.0.6 нет их разбора. При экспорте читатель, наоборот, отбрасывает OTLP экспоненциальные гистограммы (ТипМетрикиПоддерживается). |
| 2 | MUST | ➖ n_a | Overflow buckets MUST be dropped and not counted in the overall `Count`. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Native histograms Prometheus не принимаются, поэтому overflow-бакетов, которые нужно было бы отбрасывать, нет. |
| 3 | MUST | ➖ n_a | A Native histogram with custom buckets (NHCB) schema (i.e. schema -53) and which are of the integer and counter flavor MUST be converted to an OTLP Histogram as follows: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. NHCB (schema -53) не принимаются и в OTLP Histogram не переводятся: разбора native histograms нет. |
| 4 | MUST | ➖ n_a | Native histograms of the float or gauge flavors MUST be dropped. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Native histograms Prometheus (в том числе float и gauge flavors) не принимаются, отбрасывать нечего. |
| 5 | MUST | ➖ n_a | Native Histograms with `Schema` outside of the range [-4, 8] and not equal to -53 MUST be dropped. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Проверка Schema (вне [-4, 8] и не равна -53) относится к разбору native histogram Prometheus, которого в SDK нет. |
| 6 | MUST | ➖ n_a | Exemplars on the Prometheus Native Histogram Sample MUST be converted to OpenTelemetry Exemplars on the OpenTelemetry Exponential Histogram data point following the rules in Exemplars. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик, OTLP → Prometheus), приема Prometheus-метрик и их перевода в OTLP нет. Native histograms и их exemplars не принимаются; перевод exemplars реализован только в обратном направлении (ЭкземплярPrometheus, OTLP → Prometheus). |

#### Summaries

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#summaries) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | Prometheus Summary MUST be converted to an OTLP Summary. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. Ни в src/, ни в зависимости prometheus (она только сериализует семейства в text format/OpenMetrics) нет разбора экспозиции Prometheus. Перевода Prometheus Summary в OTLP Summary нет; есть только обратное направление OTLP Summary → Prometheus summary (ДобавитьСэмплыСводки, src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:795-806). |
| 2 | MUST | ➖ n_a | In text formats where Prometheus Summaries are represented by multiple samples, samples with same metric family name MUST be merged together into a single OTLP Summary. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. Слияния сэмплов quantile, _count и _sum одного семейства в один OTLP Summary нет: text format Prometheus в SDK не разбирается (ни в src/, ни в зависимости prometheus нет парсера экспозиции). |
| 3 | MUST | ➖ n_a | If `_count` is not present, the metric MUST be dropped. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. Входящие Prometheus-сводки не принимаются, поэтому обработки сводки без _count (отбрасывание метрики) нет. |
| 4 | MUST | ➖ n_a | If `_sum` is not present, the summary’s sum MUST be set to zero. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. Входящие Prometheus-сводки не принимаются, поэтому установки нулевой суммы для сводки без _sum нет. |

#### Dropped Types

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#dropped-types) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | The following Prometheus types MUST be dropped: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. Prometheus GaugeHistogram и Native GaugeHistogram на вход не принимаются (разбора экспозиции Prometheus нет ни в src/, ни в зависимости prometheus), отбрасывать нечего. |

#### Exemplars

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#exemplars) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | Prometheus Exemplars MUST be converted to OpenTelemetry Exemplars as follows: | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. Перевода Prometheus Exemplar → OpenTelemetry Exemplar нет; есть только обратное направление OTel Exemplar → Prometheus exemplar (ЭкземплярPrometheus, src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:909-935). |
| 2 | MUST | ➖ n_a | If present, the timestamp MUST be used as the OpenTelemetry exemplar’s timestamp. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. Exemplars Prometheus не принимаются, перенос их времени в OTel Exemplar отсутствует. |
| 3 | MUST | ➖ n_a | If present, and if the values are valid Trace and Span IDs, the `trace_id` and `span_id` labels MUST be converted to the OpenTelemetry Exemplar’s Trace ID and Span ID, respectively. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. Перевода лейблов trace_id/span_id exemplar Prometheus в Trace ID/Span ID OTel Exemplar нет. |
| 4 | MUST | ➖ n_a | All labels other than `trace_id` and `span_id` MUST be added to the OpenTelemetry exemplar as filtered attributes. | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. Перевода прочих лейблов exemplar Prometheus в filtered attributes OTel Exemplar нет. |

#### Instrumentation Scope

[Ссылка на спецификацию](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#instrumentation-scope) | Scope: conditional:Prometheus Receiver (Prometheus → OTLP)

| # | Уровень | Статус | Требование | Расположение в коде | Пояснение |
|---|---|---|---|---|---|
| 1 | MUST | ➖ n_a | Labels with `otel_scope_` prefix MUST be dropped from all metric points and used as the Instrumentation Scope name (`otel_scope_name`), version (`otel_scope_version`), schema URL (`otel_scope_schema_u... | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. Разбора входящих лейблов otel_scope_* (отбрасывание с точек, заполнение имени, версии, schema URL и атрибутов области) нет; есть только обратное направление: ЛейблыОбласти (src/Метрики/Классы/ОтелПрометеусЧитательМетрик.os:1482-1505) добавляет лейблы otel_scope_* при выдаче OTLP → Prometheus. |
| 2 | MUST | ➖ n_a | Metrics which do not have any label with `otel_scope_` prefix MUST be assigned an instrumentation scope identifying the entity performing the translation from Prometheus to OpenTelemetry (e.g. the col... | - | Условная фича Prometheus Receiver (Prometheus → OTLP) не реализована: SDK только экспортирует метрики в Prometheus (ОтелПрометеусЧитательМетрик), приема Prometheus-метрик и их перевода в OTLP нет. Назначения области инструментирования транслятора Prometheus → OpenTelemetry метрикам без лейблов otel_scope_* нет: Prometheus-метрики в SDK не принимаются. |

### Сводка условных секций

| Раздел | Секция | Scope | Keywords | Ссылка |
|---|---|---|---|---|
| Propagators | GetAll | conditional:GetAll Getter (post-stable extension) | 4 | [spec](https://opentelemetry.io/docs/specs/otel/context/api-propagators/#getall) |
| Prometheus Compatibility | Metric Metadata | conditional:Prometheus Receiver (Prometheus → OTLP) | 7 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#metric-metadata) |
| Prometheus Compatibility | Timestamps | conditional:Prometheus Receiver (Prometheus → OTLP) | 4 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#timestamps) |
| Prometheus Compatibility | Counters | conditional:Prometheus Receiver (Prometheus → OTLP) | 2 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#counters) |
| Prometheus Compatibility | Gauges | conditional:Prometheus Receiver (Prometheus → OTLP) | 1 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#gauges) |
| Prometheus Compatibility | Histograms | conditional:Prometheus Receiver (Prometheus → OTLP) | 5 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#histograms) |
| Prometheus Compatibility | Native Histograms | conditional:Prometheus Receiver (Prometheus → OTLP) | 6 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#native-histograms) |
| Prometheus Compatibility | Summaries | conditional:Prometheus Receiver (Prometheus → OTLP) | 4 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#summaries) |
| Prometheus Compatibility | Dropped Types | conditional:Prometheus Receiver (Prometheus → OTLP) | 1 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#dropped-types) |
| Prometheus Compatibility | Exemplars | conditional:Prometheus Receiver (Prometheus → OTLP) | 4 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#exemplars) |
| Prometheus Compatibility | Instrumentation Scope | conditional:Prometheus Receiver (Prometheus → OTLP) | 2 | [spec](https://opentelemetry.io/docs/specs/otel/compatibility/prometheus_and_openmetrics/#instrumentation-scope) |

## Ограничения платформы OneScript

| Ограничение | Влияние на спецификацию | Решение |
|---|---|---|
| Нет наносекундной точности | Временные метки с точностью до миллисекунд | Используется миллисекундная точность |
| Нет opaque-объектов | Ключи контекста - строки | Строковые константы как ключи |
| Нет thread-local | ФоновыеЗадания вместо goroutines | Передача контекста через параметры |
| Число = System.Decimal (не IEEE 754) | NaN, Infinity, отрицательный ноль невозможны | Операции, порождающие NaN/Inf, выбрасывают исключение - требования к обработке NaN/Inf неприменимы |
| Нет varargs (переменного числа параметров) | Спека требует "variable number of attributes" (metrics) и "zero or more callbacks" | Используется контейнерный объект: `ОтелАтрибуты` для атрибутов, один полиморфный параметр `Callback = Неопределено \| Действие \| Массив` для callback-ов. Семантически эквивалентно. |
| Модель распространения opm-пакета | Спека OTel описывает пропагаторы как отдельные extension-packages (Java/JS) | Пропагаторы (W3C TraceContext, W3C Baggage, B3, Jaeger и др.) поставляются в составе основного opm-пакета `opentelemetry`. Функциональность полностью соответствует спеке; отличие только в модели распространения. |

## Методология

### Процесс анализа

1. **Извлечение требований** (`extract_requirements.py`): загрузка 14 страниц спецификации, разбиение на секции, подсчёт MUST/SHOULD keywords; в отчёт входят только требования разделов со статусом Stable
2. **Генерация промптов** (`generate_prompts.py`): группировка секций по доменам, генерация промптов с JSON-схемой вывода для агентов
3. **Верификация** (general-purpose агенты): каждый агент анализирует 5-8 секций, записывает результат в JSON
4. **Сборка отчёта** (`assemble_report.py`): детерминированная сборка markdown из JSON-результатов

### Статусы

| Статус | Значение |
|---|---|
| ✅ found | Требование полностью реализовано с корректной семантикой |
| ⚠️ partial | Код существует, но не полностью соответствует спецификации |
| ❌ not_found | Реализация отсутствует |
| ➖ n_a | Неприменимо: ограничение платформы или не выполнено условие требования |

### Статистика извлечения

| Метрика | Значение |
|---|---|
| Страниц спецификации | 14 |
| Stable секций | 264 |
| Из них условных | 11 |
| Stable-требований | 868 |
| Из них universal | 828 |

