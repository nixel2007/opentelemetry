# Отчёт сравнения spec-compliance

```

======================================================================
📊 СРАВНЕНИЕ С ПРЕДЫДУЩИМ АНАЛИЗОМ
======================================================================

  Статус           Было  Стало      Δ
  --------------------------------------
  found             697    670   -27 ⚠️  РЕГРЕССИЯ
  partial            63    100 +   37
  not_found          56     44   -12
  n_a                 8     10 +    2
  Всего             824    824 +    0

  🔴 ПОНИЖЕНИЕ СТАТУСА (73) - требует перепроверки:

     [Env Vars / Boolean]
       found → partial
       Текст: Any value not explicitly defined here as a true value, including unset and empty values, MUST be int
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:764 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:777-780
       Пояснение: Функция Включено() использует инвертированную семантику: при unset/empty применяется default "true" (SDK включён). Семантически эквивалентно OTEL_SDK_
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Env Vars / Boolean]
       found → partial
       Текст: All Boolean environment variables SHOULD be named and defined such that false is the expected safe d
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:763 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:778
       Пояснение: Используется OTEL_ENABLED с дефолтом "true" вместо стандартного OTEL_SDK_DISABLED (дефолт false). Семантика сохранена (SDK активен по умолчанию), но п
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Api / Enabled]
       found → partial
       Текст: The API SHOULD be documented that instrumentation authors needs to call this API each time they emit
       Расположение: src/Логирование/Классы/ОтелЛоггер.os:28-31 → src/Логирование/Классы/ОтелЛоггер.os:28
       Пояснение: Метод Включен имеет документирующий комментарий с описанием назначения, но в нём отсутствует явное указание инструментирующим авторам вызывать API каж
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Enabled]
       found → partial
       Текст: Any modifications to parameters inside `Enabled` MUST NOT be propagated to the caller.
       Расположение: src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:14 → src/Логирование/Классы/ИнтерфейсПроцессорЛогов.os:19
       Пояснение: Включен() в интерфейсе процессора не принимает параметров (Context, InstrumentationScope, SeverityNumber, EventName) - требование о невидимости модифи
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ForceFlush]
       found → not_found
       Текст: ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:137 → -
       Пояснение: СброситьБуфер объявлена как Процедура (void) - нет возвращаемого статуса/Обещания, таймаут неотличим от успеха.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD complete or abort within some timeout.
       Расположение: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:64-67 → src/Логирование/Классы/ОтелПровайдерЛогирования.os:113
       Пояснение: Провайдер.СброситьБуфер() не принимает таймаут и вызывает Процессор.СброситьБуфер() без аргументов. Композитный процессор поддерживает таймаут, но про
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ForceFlush]
       found → partial
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71 → src/Экспорт/Классы/ОтелЭкспортерЛогов.os:45
       Пояснение: СброситьБуфер у экспортера - Процедура (не возвращает статус). Нет способа для вызывающего узнать, успех/неудача/таймаут. У провайдера есть СброситьБу
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / Logger Creation]
       found → partial
       Текст: It SHOULD only be possible to create Logger instances through a LoggerProvider (see API).
       Расположение: src/Логирование/Классы/ОтелПровайдерЛогирования.os:54 → src/Логирование/Классы/ОтелЛоггер.os:249
       Пояснение: Логгер создаётся через Провайдер.ПолучитьЛоггер() и ОтелПостроительЛоггера.Построить(), но класс ОтелЛоггер технически инстанцируем напрямую через Нов
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / OnEmit]
       found → partial
       Текст: This method is called synchronously on the thread that emitted the `LogRecord`, therefore it SHOULD 
       Расположение: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:19-23 → src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:18
       Пояснение: ОтелПростойПроцессорЛогов.ПриПоявлении вызывает Экспортер.Экспортировать синхронно под блокировкой - блокирует поток эмиттера; исключения из Экспортир
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / OnEmit]
       found → not_found
       Текст: Therefore, any concurrent modifications and reads of `logRecord` may result in race conditions. To a
       Расположение: src/Логирование/Классы/ОтелЛоггер.os:111 → -
       Пояснение: Нет документированной рекомендации пользователям клонировать запись лога при конкурентной обработке, нет API для клонирования ОтелЗаписьЛога.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ShutDown]
       found → partial
       Текст: `Shutdown` SHOULD be called only once for each `LogRecordProcessor` instance.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:81 → src/Логирование/Классы/ОтелПростойПроцессорЛогов.os:57
       Пояснение: Нет идемпотентной защиты от повторного вызова Закрыть() - ни в ОтелПростойПроцессорЛогов, ни в базовом пакетном (Закрыт=Истина ставится, но повторный 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ShutDown]
       found → partial
       Текст: After the call to `Shutdown`, subsequent calls to `OnEmit` are not allowed. SDKs SHOULD ignore these
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:42-45 → src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:43
       Пояснение: Базовый пакетный процессор игнорирует Обработать при Закрыт=Истина. В ОтелПростойПроцессорЛогов.ПриПоявлении нет проверки закрытия - вызов Экспортер.Э
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Logs Sdk / ShutDown]
       found → not_found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Логирование/Классы/ОтелКомпозитныйПроцессорЛогов.os:81-95 → -
       Пояснение: Закрыть объявлена как Процедура (void) во всех реализациях - нет возвращаемого статуса/Обещания, таймаут неотличим от успеха.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Counter operations]
       found → partial
       Текст: This API SHOULD NOT validate this value, that is left to implementations of the API.
       Расположение: src/Метрики/Классы/ОтелСчетчик.os:22-24 → src/Метрики/Классы/ОтелСчетчик.os:22
       Пояснение: API Добавить валидирует значение: отрицательные значения молча отбрасываются (Если Значение < 0 Тогда Возврат), что нарушает SHOULD NOT validate на ур
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Enabled]
       found → partial
       Текст: The API SHOULD be documented that instrumentation authors needs to call this API each time they reco
       Расположение: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:83-86 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:224
       Пояснение: Метод задокументирован (назначение, возврат), но без явного указания пользователю вызывать Enabled перед каждой записью измерения.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Get a Meter]
       found → partial
       Текст: Therefore, this API MUST be structured to accept a variable number of attributes, including none.
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:53 → src/Метрики/Классы/ОтелПровайдерМетрик.os:62
       Пояснение: Параметр АтрибутыОбласти принимает ОтелАтрибуты (контейнер), а не variable number of attributes (varargs) - пользователь обязан сначала создать ОтелАт
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Instrument]
       found → partial
       Текст: Language-level features such as the distinction between integer and floating point numbers SHOULD be
       Расположение: - → src/Метрики/Классы/ОтелМетр.os:607
       Пояснение: В OneScript тип Число единый (System.Decimal), различия integer/float на уровне языка нет. Идентификация инструментов ведётся по имени, виду, единице,
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to con
       Расположение: src/Метрики/Классы/ОтелМетр.os:43-44 → src/Метрики/Классы/ОтелМетр.os:43
       Пояснение: Документация метода есть, но не упоминает instrument name syntax.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API SHOULD NOT validate `advisory` parameters.
       Расположение: src/Метрики/Классы/ОтелМетр.os:687-706 → src/Метрики/Классы/ОтелМетр.os:687
       Пояснение: ПроверитьСовет() валидирует структуру advisory (пишет предупреждения при неверных типах), что частично нарушает SHOULD NOT validate.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API SHOULD be documented in a way to communicate to users that the `name` parameter needs to con
       Расположение: src/Метрики/Классы/ОтелМетр.os:230-231 → src/Метрики/Классы/ОтелМетр.os:231
       Пояснение: Документация метода есть, но не упоминает instrument name syntax.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API SHOULD NOT validate `advisory` parameters.
       Расположение: src/Метрики/Классы/ОтелМетр.os:687-706 → src/Метрики/Классы/ОтелМетр.os:687
       Пояснение: ПроверитьСовет() валидирует структуру advisory (пишет предупреждения при неверных типах), что частично нарушает SHOULD NOT validate.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: this API MUST be structured to accept a variable number of `callback` functions, including none.
       Пояснение: СоздатьНаблюдаемыйСчетчик принимает один опциональный Callback (включая none), но не переменное число callback-ов в сигнатуре конструктора.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: The API MUST support creation of asynchronous instruments by passing zero or more `callback` functio
       Расположение: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:147-156 → src/Метрики/Классы/ОтелМетр.os:242
       Пояснение: В конструкторе можно передать zero или один callback; дополнительные callback добавляются через ДобавитьCallback после создания, а не при создании.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Callback functions MUST be documented as follows for the end user:
       Расположение: src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69 → src/Метрики/Классы/ОтелМетр.os:232
       Пояснение: Параметр Callback задокументирован как "callback для наблюдения", но явно не документирует требования (reentrancy, отсутствие длительной работы, отсут
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Callback functions SHOULD be reentrant safe.
       Расположение: src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69 → src/Метрики/Классы/ОтелМетр.os:232
       Пояснение: Требование относится к пользовательской документации callback; явного указания на reentrancy в doc-комментарии нет.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Callback functions SHOULD NOT take an indefinite amount of time.
       Расположение: src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69 → src/Метрики/Классы/ОтелМетр.os:232
       Пояснение: В doc-комментарии нет указания на ограничение по времени выполнения callback.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Api / Synchronous and Asynchronous instruments]
       found → partial
       Текст: Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same
       Расположение: src/Метрики/Классы/ОтелНаблюдениеМетрики.os:62-69 → src/Метрики/Классы/ОтелМетр.os:232
       Пояснение: В doc-комментарии нет указания на запрет дублирующих observations.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Duplicate instrument registration]
       found → partial
       Текст: The emitted warning SHOULD include information for the user on how to resolve the conflict, if possi
       Расположение: src/Метрики/Классы/ОтелМетр.os:619-622 → src/Метрики/Классы/ОтелМетр.os:618
       Пояснение: Предупреждение сообщает имя/вид/единицы существующего и запрошенного инструмента, но не предлагает конкретный рецепт View для разрешения конфликта.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / ExemplarReservoir]
       found → partial
       Текст: The offer method SHOULD have the ability to pull associated trace and span information without needi
       Расположение: src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:125-129 → src/Метрики/Классы/ОтелРезервуарЭкземпляров.os:41
       Пояснение: Метод Предложить принимает КонтекстСпана (trace/span info), но Baggage и полный Context не доступны - extract trace/span из контекста выполняется на у
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       found → not_found
       Текст: Arithmetic sum of Measurement values in population. This SHOULD NOT be collected when used with inst
       Расположение: src/Метрики/Классы/ОтелАгрегаторГистограммы.os:51 → -
       Пояснение: sum всегда собирается в ОтелАгрегаторГистограммы/ОтелАгрегаторЭкспоненциальнойГистограммы независимо от типа инструмента; условие отключения sum при о
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       found → n_a
       Текст: Implementations SHOULD NOT incorporate non-normal values (i.e., +Inf, -Inf, and NaNs) into the sum, 
       Пояснение: Платформа OneScript использует System.Decimal вместо IEEE 754; значения +Inf/-Inf/NaN невозможны (операции выбрасывают исключение), поэтому требование
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Histogram Aggregations]
       found → partial
       Текст: SDKs SHOULD use the default value when boundaries are not explicitly provided, unless they have good
       Расположение: src/Метрики/Классы/ОтелАгрегаторГистограммы.os:185-202 → src/Метрики/Классы/ОтелАгрегаторГистограммы.os:118
       Пояснение: Дефолтные границы применяются, но массив СтандартныеГраницы() пропускает границу 7500 из спецификации: [0, 5, 10, 25, 50, 75, 100, 250, 500, 750, 1000
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Instrument enabled]
       found → partial
       Текст: The synchronous instrument `Enabled` MUST return `false` when either:
       Расположение: /home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:231 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:235-237
       Пояснение: Метод Включен() возвращает Ложь при отключённом MeterConfig (МетрВключен) и при явном Отключить(), но не проверяет условие 'все резолвленные Views исп
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Interface Definition]
       found → partial
       Текст: This is a hint to ensure that the export of any Metrics the exporter has received prior to the call 
       Пояснение: СброситьБуфер() экспортёра - пустая процедура (нет буферизации, синхронный экспорт). Требование формально выполнено (нечего флашить), но это не явная 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Interface Definition]
       found → partial
       Текст: ForceFlush SHOULD complete or abort within some timeout.
       Пояснение: СброситьБуфер() экспортёра - пустая процедура (синхронный экспорт без буфера), явного таймаута нет, но и блокировки нет.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Measurement processing]
       found → not_found
       Текст: If applying the View results in conflicting metric identities the implementation SHOULD apply the Vi
       Пояснение: SDK не детектирует конфликтующие metric identities между несколькими Views и не эмитит предупреждение
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Measurement processing]
       found → not_found
       Текст: If it is not possible to apply the View without producing semantic errors the implementation SHOULD 
       Пояснение: Нет проверки семантических ошибок View (например, async инструмент + histogram aggregation) и соответствующего предупреждения
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Meter Creation]
       found → partial
       Текст: In the case where an invalid `name` (null or empty string) is specified, a working Meter MUST be ret
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:65 → src/Метрики/Классы/ОтелПровайдерМетрик.os:66
       Пояснение: При Неопределено имя принудительно заменяется на пустую строку ('') - оригинальное невалидное значение не сохраняется (Неопределено → ""). Пустая стро
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MeterConfig]
       found → partial
       Текст: If a `Meter` is disabled, it MUST behave equivalently to No-op Meter.
       Расположение: src/Метрики/Классы/ОтелМетр.os:428 → src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:83
       Пояснение: ПрименитьКонфигурацию устанавливает МетрВключен, Instrument.Включен() учитывает его (строки 235-237), однако Записать() проверяет только собственный ф
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / MetricReader]
       found → partial
       Текст: The MetricReader.Collect invocation on one MetricReader instance SHOULD NOT introduce side-effects t
       Расположение: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:101 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:250
       Пояснение: При delta-временности ОчиститьТочкиДанных обнуляет состояние инструмента, разделяемое между читателями; Collect одного reader'а влияет на данные други
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Name conflict]
       found → partial
       Текст: the Meter MUST return an instrument using the first-seen instrument name and log an appropriate erro
       Расположение: /home/nfedkin/git_tree/github/nixel2007/opentelemetry/src/Метрики/Классы/ОтелМетр.os:54 → src/Метрики/Классы/ОтелМетр.os:56-60
       Пояснение: Первый найденный инструмент возвращается (ИнструментыПоИмени по НРег(Имя)), но ПроверитьКонфликтДескриптора логирует только при отличии вида/единицы/о
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → not_found
       Текст: The implementation SHOULD disregard the use of asynchronous instrument APIs outside of registered ca
       Пояснение: Нет кода, игнорирующего использование async API вне зарегистрированных callback-ов; внешние наблюдения от мульти-callback применяются при сборе
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Observations inside asynchronous callbacks]
       partial → not_found
       Текст: The implementation SHOULD use a timeout to prevent indefinite callback execution.
       Пояснение: ВызватьМультиОбратныеВызовы и ВызватьCallbackИСобрать вызывают callback синхронно без ограничения по времени; таймаут отсутствует
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       found → partial
       Текст: `Shutdown` MUST be called only once for each `MeterProvider` instance.
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:144 → src/Метрики/Классы/ОтелПровайдерМетрик.os:143
       Пояснение: Флаг Закрыт устанавливается, но Закрыть() не имеет явной защиты от повторного вызова (нет СравнитьИУстановить как у читателя). Повторный вызов попытае
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Shutdown]
       found → partial
       Текст: After the call to `Shutdown`, subsequent attempts to get a `Meter` are not allowed. SDKs SHOULD retu
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:70 → src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94
       Пояснение: СброситьБуфер() (Collect) - Процедура без возвращаемого значения. После Закрыть() данные экспортёра не принимаются (Экспортер.Закрыт=Истина → Экспорти
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Start timestamps]
       partial → not_found
       Текст: For asynchronous instrument, the start timestamp SHOULD be the creation time of the instrument, if t
       Расположение: - → src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:184
       Пояснение: Для async инструментов startTimeUnixNano устанавливается равным текущему времени сбора (ВремяСейчас), а не времени создания инструмента или границы пр
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: The SDK MUST accept the following stream configuration parameters: name, description, attribute_keys
       Расположение: src/Метрики/Классы/ОтелПредставление.os:156-164 → src/Метрики/Классы/ОтелПредставление.os:156
       Пояснение: ОтелПредставление принимает все параметры (name, description, attribute_keys, aggregation, exemplar_reservoir, cardinality_limit), но параметр Агрегац
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → not_found
       Текст: In order to avoid conflicts, if a name is provided the View SHOULD have an instrument selector that 
       Пояснение: SDK не валидирует, что при заданном name селектор сужен до одного инструмента, и не применяет fail-fast
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Metrics Sdk / Stream configuration]
       found → partial
       Текст: If the user does not provide an aggregation_cardinality_limit value, the MeterProvider MUST apply th
       Расположение: src/Метрики/Классы/ОтелПровайдерМетрик.os:249-255 → src/Метрики/Классы/ОтелПровайдерМетрик.os:248
       Пояснение: Дефолт из MetricReader применяется ко всем инструментам через ПрименитьНастройкиЧитателяКМетру, но View.ЛимитМощностиАгрегации не применяется per-view
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → partial
       Текст: The following configuration options MUST be available to configure the OTLP exporter.
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:148-186 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:569
       Пояснение: Реализованы Endpoint, Headers, Compression, Timeout, Protocol (общие и per-signal). Отсутствуют Insecure, Certificate File, Client key file, Client ce
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Configuration Options]
       found → partial
       Текст: Additionally, the option MUST accept a URL with a scheme of either `http` or `https`.
       Расположение: src/Экспорт/Классы/ОтелGrpcТранспорт.os:174-175 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:632
       Пояснение: Адрес передаётся в ОтелGrpcТранспорт как есть; явной обработки http/https схемы и её приоритета над insecure нет.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Otlp Exporter / Specify Protocol]
       found → partial
       Текст: SDKs SHOULD support both `grpc` and `http/protobuf` transports and MUST support at least one of them
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:563-571 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:578
       Пояснение: Поддерживаются grpc и http/json; http/protobuf распознаётся, но ОтелHttpТранспорт всегда отправляет JSON (src/Экспорт/Классы/ОтелHttpТранспорт.os:56-5
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Propagators Distribution]
       found → partial
       Текст: The official list of propagators that MUST be maintained by the OpenTelemetry organization and MUST 
       Расположение: src/Пропагация/Классы/ОтелB3Пропагатор.os:1 → src/Пропагация/Классы/
       Пояснение: Пропагаторы W3C TraceContext, W3C Baggage и B3 реализованы, но входят в состав основного opm-пакета opentelemetry, а не распространяются как отдельные
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / Propagators Distribution]
       found → n_a
       Текст: It MUST NOT use OpenTracing in the resulting propagator name as it is not widely adopted format in t
       Пояснение: Пропагатор OT Trace не реализован в SDK, требование об именовании к нему неприменимо.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Propagators / W3C Trace Context Requirements]
       found → partial
       Текст: A W3C Trace Context propagator MUST parse and validate the traceparent and tracestate HTTP headers a
       Пояснение: Парсинг и базовая валидация traceparent (длины, version != ff, all-zeros) выполняются, tracestate передаётся строкой в ОтелСостояниеТрассировки; однак
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Detecting resource information from the environment]
       found → partial
       Текст: whereas an error that occurs during an attempt to detect resource information SHOULD be considered a
       Расположение: src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:24 → src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:25
       Пояснение: Ошибки детекции логируются как Отладка (debug), а не как ошибка - не отличаются от штатного отсутствия информации.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Resource Sdk / Specifying resource information via an environment variable]
       found → partial
       Текст: The SDK MUST extract information from the `OTEL_RESOURCE_ATTRIBUTES` environment variable and merge 
       Расположение: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:122 → src/Конфигурация/Модули/ОтелАвтоконфигурация.os:137
       Пояснение: OTEL_RESOURCE_ATTRIBUTES извлекается в СоздатьРесурс, но автоматического merge с user-provided ресурсом (переданным напрямую в провайдер минуя автокон
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Behavior of the API in the absence of an installed SDK]
       found → partial
       Текст: The API MUST return a non-recording `Span` with the `SpanContext` in the parent `Context` (whether e
       Расположение: src/Трассировка/Классы/ОтелТрассировщик.os:82 → src/Ядро/Модули/ОтелГлобальный.os:71
       Пояснение: В проекте API и SDK не разделены. При отсутствии установленного SDK ОтелГлобальный.ПолучитьТрассировщик() вызывает исключение через ПроверитьИнициализ
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Behavior of the API in the absence of an installed SDK]
       found → partial
       Текст: If the parent `Context` contains no `Span`, an empty non-recording Span MUST be returned instead (i.
       Расположение: src/Трассировка/Классы/ОтелНоопСпан.os:277 → src/Трассировка/Классы/ОтелНоопСпан.os:267
       Пояснение: ОтелНоопСпан без аргумента создаёт невалидный контекст all-zero, что корректно. Однако это поведение относится к SDK-уровню (при DROP-семплировании). 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Set Status]
       found → partial
       Текст: An attempt to set value `Unset` SHOULD be ignored.
       Пояснение: Явная проверка Значение = НеУстановлен → Возврат отсутствует. Error→Unset блокируется на строке 436, Ok блокирует любые изменения (431). В состоянии U
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Span Creation]
       found → partial
       Текст: If API is called at a moment of a Span logical start, API user MUST NOT explicitly set this argument
       Пояснение: Параметр доступен через УстановитьВремяНачала без явного документирующего предупреждения о логическом старте; по умолчанию используется текущее время
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / TraceState]
       found → partial
       Текст: If invalid value is passed the operation MUST NOT return `TraceState` containing invalid data and MU
       Расположение: src/Трассировка/Классы/ОтелСостояниеТрассировки.os:68 → src/Трассировка/Классы/ОтелСостояниеТрассировки.os:67
       Пояснение: Невалидные параметры молча игнорируются (возврат ЭтотОбъект без изменений); отсутствует явное логирование/обработка ошибок согласно общим guidelines
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Api / Wrapping a SpanContext in a Span]
       found → n_a
       Текст: This functionality MUST be fully implemented in the API, and SHOULD NOT be overridable.
       Пояснение: В OneScript нет языковых механизмов наследования/переопределения классов. Платформенное ограничение - переопределение методов класса невозможно.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Concurrency requirements]
       found → partial
       Текст: Tracer Provider - Tracer creation, `ForceFlush` and `Shutdown` MUST be safe to be called concurrentl
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:336 → src/Трассировка/Классы/ОтелПровайдерТрассировки.os:63
       Пояснение: Закрыт - АтомарноеБулево, но доступ к кэшу Трассировщики (Соответствие) и списку Процессоры не защищён блокировкой; конкурентный ПолучитьТрассировщик/
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Enabled]
       found → partial
       Текст: `Enabled` MUST return `false` when either: there are no registered `SpanProcessors`, `Tracer` is dis
       Пояснение: Функция Включен() возвращает Конфигурация.Включен() когда конфигурация задана, игнорируя наличие процессоров; комбинированная проверка (нет процессоро
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Enabled]
       found → partial
       Текст: Otherwise, it SHOULD return `true`.
       Расположение: src/Трассировка/Классы/ОтелТрассировщик.os:42 → src/Трассировка/Классы/ОтелТрассировщик.os:38
       Пояснение: Возврат Истина корректен для случая без конфигурации при наличии процессоров, но поведение при заданной конфигурации не учитывает процессоры, поэтому 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / ForceFlush()]
       found → not_found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:72 → -
       Пояснение: Процедура СброситьБуфер(ТаймаутМс) не возвращает статус, поэтому вызывающий не может отличить успех, неудачу и таймаут.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / OnEnding]
       found → partial
       Текст: The SDK MUST guarantee that the span can no longer be modified by any other thread before invoking `
       Расположение: src/Трассировка/Классы/ОтелСпан.os:467 → src/Трассировка/Классы/ОтелСпан.os:459
       Пояснение: Завершить() вызывает ПередЗавершением синхронно, но нет явной блокировки, запрещающей другим ФоновымЗаданиям модифицировать спан перед вызовом OnEndin
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / SDK Span creation]
       found → partial
       Текст: When asked to create a Span, the SDK MUST act as if doing the following in order:
       Пояснение: Порядок TraceId-resolve → ShouldSample → создание спана соблюдён, но spanId генерируется только для реальных спанов (строка 91); при DROP возвращается
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Shutdown()]
       found → not_found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Расположение: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80 → -
       Пояснение: Процедура Закрыть(ТаймаутМс) не возвращает статус - нельзя отличить успех, неудачу и таймаут; логирование таймаута не возвращается вызывающему.
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / Tracer Creation]
       found → partial
       Текст: It SHOULD only be possible to create `Tracer` instances through a `TracerProvider` (see API).
       Расположение: src/Трассировка/Классы/ОтелПровайдерТрассировки.os:47 → src/Трассировка/Классы/ОтелПровайдерТрассировки.os:63
       Пояснение: TracerProvider.ПолучитьТрассировщик и ПостроительТрассировщика - штатный путь, но в OneScript нельзя скрыть конструктор - клиент может напрямую вызват
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / `Export(batch)`]
       found → partial
       Текст: Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Расположение: src/Экспорт/Классы/ОтелHttpТранспорт.os:69 → src/Экспорт/Классы/ОтелЭкспортерСпанов.os:28
       Пояснение: Экспортировать делегирует в Транспорт.Отправить; явного таймаута в самом экспортере нет — верхний предел зависит от настроек транспорта (HTTPConnectio
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

     [Trace Sdk / `Export(batch)`]
       found → partial
       Текст: Export() MUST NOT block indefinitely, there MUST be a reasonable upper limit after which the call mu
       Расположение: src/Экспорт/Классы/ОтелHttpТранспорт.os:149 → src/Экспорт/Классы/ОтелЭкспортерСпанов.os:28
       Пояснение: В Экспортировать нет параметра таймаута и нет явной логики отсечения с возвратом Failure по таймауту; контракт Failure=Ложь при истечении таймаута не 
       ⚠️  Возможные причины: 1) регрессия в коде; 2) агент строже оценил; 3) ложное срабатывание

  🟢 ПОВЫШЕНИЕ СТАТУСА (54) - требует перепроверки:

     [Env Vars / Exporter Selection]
       not_found → found
       Текст: It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new impleme
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:216
       Было: Код не поддерживает deprecated значение "logging" для экспортеров - только "otlp", "console" и "none
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Exporter Selection]
       not_found → found
       Текст: It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new impleme
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:401
       Было: Код не поддерживает deprecated значение "logging" для метрик экспортера - только "otlp" и "none". Эт
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / Exporter Selection]
       not_found → found
       Текст: It is a deprecated value left for backwards compatibility. It SHOULD NOT be supported by new impleme
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:337
       Было: Код не поддерживает deprecated значение "logging" для логов экспортера - только "otlp" и "none". Это
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Env Vars / General SDK Configuration]
       partial → found
       Текст: Values MUST be deduplicated in order to register a Propagator only once.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:483
       Было: Правильная дедупликация пропагаторов реализована через Соответствие как Set, но используется неправи
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Logs Sdk / ForceFlush]
       partial → found
       Текст: ForceFlush SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:71
       Было: Timeout is supported at processor level but not exposed at LoggerProvider.СброситьБуфер() level - on
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Asynchronous Counter creation]
       partial → found
       Текст: The API SHOULD provide some way to pass `state` to the callback.
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:163
       Было: Callbacks are created as lambda functions that can capture closure variables, but there's no explici
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Counter operations]
       partial → found
       Текст: If possible, this API SHOULD be structured so a user is obligated to provide this parameter.
       Код: src/Метрики/Классы/ОтелСчетчик.os:21
       Было: Параметр Значение обязательный, но может быть 0 или отрицательным (игнорируется).
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Enabled]
       partial → found
       Текст: Parameters can be added in the future, therefore, the API MUST be structured in a way for parameters
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:235
       Было: Метод Включен() не принимает параметры, но можно добавить перегрузку в будущем.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Instrument description]
       not_found → found
       Текст: It MUST support BMP (Unicode Plane 0), which is basically only the first three bytes of UTF-8 (or `u
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:11
       Было: Нет явной проверки или ограничения на BMP Unicode. Строки обрабатываются как есть через Нормализоват
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Instrument description]
       not_found → found
       Текст: It MUST support at least 1023 characters.
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:11
       Было: Нет ограничений на длину строки описания. Строка принимается без проверки длины.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: If possible, the API SHOULD be structured so a user is obligated to provide this parameter.
       Код: src/Метрики/Классы/ОтелМетр.os:51
       Было: Имя обязательный первый параметр, но технически можно передать пустую строку без проверки.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: If possible, the API SHOULD be structured so a user is obligated to provide this parameter.
       Код: src/Метрики/Классы/ОтелМетр.os:242
       Было: Имя обязательный первый параметр, но технически можно передать пустую строку без проверки.
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Api / Synchronous and Asynchronous instruments]
       partial → found
       Текст: Every currently registered Callback associated with a set of instruments MUST be evaluated exactly o
       Код: src/Метрики/Классы/ОтелБазовыйНаблюдаемыйИнструмент.os:160
       Было: Callbacks выполняются при сборе, но нет явного механизма предотвращения двойного вызова в течение од
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / AlignedHistogramBucketExemplarReservoir]
       partial → found
       Текст: This implementation MUST store at most one measurement that falls within a histogram bucket, and SHO
       Код: src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:76
       Было: Uses simple replacement (last measurement wins) instead of uniformly-weighted sampling algorithm
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / AlignedHistogramBucketExemplarReservoir]
       partial → found
       Текст: This implementation MUST store at most one measurement that falls within a histogram bucket, and SHO
       Код: src/Метрики/Классы/ОтелВыровненныйРезервуарГистограммы.os:55
       Было: Uses simple replacement (last measurement wins) instead of uniformly-weighted sampling algorithm
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Collect]
       not_found → partial
       Текст: Collect SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:209
       Было: Collect methods do not provide failure/timeout return values - they handle errors internally with lo
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Configuration]
       partial → found
       Текст: If there is no matching view, but the `MetricReader` defines a default cardinality limit value based
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:251
       Было: MetricReader has ЛимитМощности method returning default 2000, but this is not applied to instruments
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Duplicate instrument registration]
       not_found → partial
       Текст: Otherwise (e.g., use of multiple units), the SDK SHOULD pass through the data by reporting both `Met
       Код: src/Метрики/Классы/ОтелМетр.os:57
       Было: SDK returns the first registered instrument, not both Metric objects. No data pass-through for confl
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Exemplar]
       partial → found
       Текст: the SDK MUST NOT have overhead related to exemplar sampling
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:381-385
       Было: Filter check is implemented to skip sampling when disabled, but complete overhead elimination when s
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Exemplar defaults]
       not_found → found
       Текст: Explicit bucket histogram aggregation with more than 1 bucket SHOULD use AlignedHistogramBucketExemp
       Код: src/Метрики/Классы/ОтелМетр.os:106
       Было: No automatic assignment of reservoir type based on aggregation configuration found
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Exemplar defaults]
       not_found → found
       Текст: Base2 Exponential Histogram Aggregation SHOULD use a SimpleFixedSizeExemplarReservoir with a reservo
       Код: src/Метрики/Классы/ОтелМетр.os:147
       Было: No automatic assignment of reservoir type for exponential histograms found
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Exemplar defaults]
       not_found → found
       Текст: All other aggregations SHOULD use SimpleFixedSizeExemplarReservoir.
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:299
       Было: No automatic assignment of reservoir type based on aggregation type found
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       partial → found
       Текст: `ForceFlush` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:165
       Было: Асинхронная версия возвращает Обещание, но синхронная версия не возвращает статус
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / ForceFlush]
       not_found → partial
       Текст: ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:94
       Было: СброситьБуфер() is a void procedure (Процедура). There is no return value or mechanism to communicat
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Interface Definition]
       not_found → partial
       Текст: ForceFlush SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Экспорт/Классы/ОтелЭкспортерМетрик.os:47
       Было: СброситьБуфер() on the exporter is a void procedure (Процедура). No return value or mechanism to com
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Meter]
       not_found → found
       Текст: If the `MeterProvider` supports updating the MeterConfigurator, then upon update the `Meter` MUST be
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:221
       Было: MeterProvider does not support updating MeterConfigurator. The конфигураторМетров callback is only c
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / MetricReader]
       partial → found
       Текст: This function SHOULD be obtained from the exporter.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:265
       Было: Temporality is not obtained from exporter - it is hardcoded in SDK
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Numerical limits handling]
       n_a → found
       Текст: The SDK MUST handle numerical limits in a graceful way according to Error handling in OpenTelemetry.
       Код: src/Метрики/Классы/ОтелАгрегаторСуммы.os:1
       Было: OneScript uses System.Decimal instead of IEEE 754, so NaN and Infinity are not possible - operations
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       partial → found
       Текст: Implementation SHOULD use the filter as early as possible to gain as much performance gain possible 
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:366
       Было: The interface accepts ФильтрМетрик as an optional parameter and the reader passes it to producers (l
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Produce batch]
       not_found → partial
       Текст: Produce SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ИнтерфейсПродюсерМетрик.os:13
       Было: Произвести() returns Массив (array of ОтелДанныеМетрики). There is no mechanism to communicate succe
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       partial → found
       Текст: `Shutdown` SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:177
       Было: Асинхронная версия возвращает Обещание, но синхронная версия не возвращает статус
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       not_found → found
       Текст: SDKs SHOULD return some failure for these calls, if possible.
       Код: src/Метрики/Классы/ОтелПровайдерМетрик.os:70
       Было: СброситьБуфер() (Collect) is a void procedure with no guard checking Закрыт flag after shutdown. No 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Shutdown]
       not_found → partial
       Текст: Shutdown SHOULD provide a way to let the caller know whether it succeeded, failed or timed out.
       Код: src/Метрики/Классы/ОтелПериодическийЧитательМетрик.os:111
       Было: Закрыть() is a void procedure. All exceptions (timeout, exporter close errors) are caught internally
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       partial → found
       Текст: For delta aggregations, the start timestamp MUST equal the previous collection interval's timestamp,
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:166
       Было: Start timestamp handling for delta aggregations not fully implemented according to spec
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       partial → found
       Текст: This implies that all data points with delta temporality aggregation for an instrument MUST share th
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:297
       Было: Delta temporality start timestamp consistency not enforced
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Start timestamps]
       partial → found
       Текст: Cumulative timeseries MUST use a consistent start timestamp for all collection intervals.
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:162
       Было: Cumulative start timestamp consistency not fully implemented
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Metrics Sdk / Synchronous instrument cardinality limits]
       not_found → found
       Текст: Aggregators for synchronous instruments with cumulative temporality MUST continue to export all attr
       Код: src/Метрики/Классы/ОтелБазовыйСинхронныйИнструмент.os:159
       Было: Implementation does not distinguish between cumulative and delta temporality for overflow handling. 
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       not_found → partial
       Текст: If the gRPC client implementation does not support an endpoint with a scheme of `http` or `https` th
       Код: src/Экспорт/Классы/ОтелGrpcТранспорт.os:37
       Было: gRPC transport uses OPI_GRPC library which handles URL formats internally, but no explicit transform
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Configuration Options]
       not_found → found
       Текст: they SHOULD continue to be supported as they were part of a stable release of the specification.
       Было: Obsolete environment variables OTEL_EXPORTER_OTLP_SPAN_INSECURE and OTEL_EXPORTER_OTLP_METRIC_INSECU
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Otlp Exporter / Specify Protocol]
       partial → found
       Текст: If they support only one, it SHOULD be `http/protobuf`.
       Код: src/Конфигурация/Модули/ОтелАвтоконфигурация.os:572
       Было: SDK supports grpc and http/json, but not http/protobuf specifically
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Extract]
       partial → found
       Текст: MUST preserve a debug trace flag, if received, and propagate it with subsequent requests.
       Код: src/Пропагация/Классы/ОтелB3Пропагатор.os:184
       Было: Debug flag is detected during extract ("d" in single-header, X-B3-Flags=1 in multi-header) and cause
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / B3 Inject]
       partial → found
       Текст: MUST default to injecting B3 using the single-header format
       Код: src/Пропагация/Классы/ОтелB3Пропагатор.os:240
       Было: Constructor defaults to ОтелФорматB3.Мульти() (multi-header) when no format is provided. The spec re
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Propagators / Fields]
       partial → found
       Текст: Fields MUST return the header names that correspond to the configured format, i.e., the headers used
       Код: src/Пропагация/Классы/ОтелB3Пропагатор.os:86
       Было: For single-header format, Fields correctly returns ["b3"]. For multi-header format, Fields returns [
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Resource Sdk / Detecting resource information from the environment]
       partial → found
       Текст: Custom resource detectors related to generic platforms (e.g. Docker, Kubernetes) or vendor specific 
       Код: src/Ядро/Классы/ОтелДетекторРесурсаХоста.os:1
       Было: Детекторы реализованы как отдельные классы (ОтелДетекторРесурсаХоста, ОтелДетекторРесурсаПроцесса, О
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Behavior of the API in the absence of an installed SDK]
       not_found → partial
       Текст: If the `Span` in the parent `Context` is already non-recording, it SHOULD be returned directly witho
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:81
       Было: ОтелТрассировщик.НачатьСпан always creates a new ОтелНоопСпан(КонтекстРодителяСпана) when sampling f
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / End]
       partial → found
       Текст: This operation itself MUST NOT perform blocking I/O on the calling thread.
       Код: src/Трассировка/Классы/ОтелСпан.os:459
       Было: End() вызывает Процессор.ПриЗавершении(), а SimpleSpanProcessor синхронно вызывает Экспортер.Экспорт
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Api / Retrieving the TraceId and SpanId]
       partial → found
       Текст: The API SHOULD NOT expose details about how they are internally stored.
       Код: src/Трассировка/Классы/ОтелКонтекстСпана.os:23
       Было: Binary getters (ИдТрассировкиВДвоичномВиде, ИдСпанаВДвоичномВиде) return the internal ДвоичныеДанные
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Additional Span Interfaces]
       partial → found
       Текст: For backwards compatibility it MUST also be able to access the `InstrumentationLibrary` [deprecated 
       Код: src/Ядро/Классы/ОтелОбластьИнструментирования.os:68
       Было: InstrumentationScope is accessible via ОбластьИнструментирования() and contains the same name/versio
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Explicit randomness]
       not_found → partial
       Текст: SDKs and Samplers MUST NOT overwrite explicit randomness in an OpenTelemetry TraceState value.
       Код: src/Трассировка/Модули/ОтелСэмплер.os:157
       Было: В коде нет проверки подключа 'rv' в TraceState и предотвращения его перезаписи. ОтелСостояниеТрассир
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Sampling]
       not_found → partial
       Текст: However, Span Exporter SHOULD NOT receive them unless the `Sampled` flag was also set.
       Код: src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:42
       Было: Процессоры (ОтелПростойПроцессорСпанов, ОтелПакетныйПроцессорСпанов) передают экспортеру все заверше
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Sampling]
       not_found → partial
       Текст: Span Exporters MUST receive those spans which have `Sampled` flag set to true and they SHOULD NOT re
       Код: src/Трассировка/Классы/ОтелПростойПроцессорСпанов.os:42
       Было: Процессоры передают экспортеру все завершенные спаны без фильтрации по флагу Sampled. Нет механизма,
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / Shutdown()]
       partial → found
       Текст: `Shutdown` SHOULD complete or abort within some timeout.
       Код: src/Экспорт/Классы/ОтелБазовыйПакетныйПроцессор.os:80
       Было: Параметр ТаймаутМс принимается, но простой процессор не использует его - вызов Экспортер.Закрыть() н
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / TraceID randomness]
       partial → found
       Текст: For root span contexts, the SDK SHOULD implement the TraceID randomness requirements of the W3C Trac
       Код: src/Ядро/Модули/ОтелУтилиты.os:78
       Было: TraceIDs are generated using UUID v4 (Новый УникальныйИдентификатор()), which provides 122 random bi
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

     [Trace Sdk / TracerConfig]
       partial → found
       Текст: The value of `enabled` MUST be used to resolve whether a `Tracer` is Enabled. If `enabled` is `false
       Код: src/Трассировка/Классы/ОтелТрассировщик.os:38
       Было: When enabled is false, Включен() correctly returns false. However, when enabled is true (or no confi
       ⚠️  Возможные причины: 1) код добавлен/исправлен; 2) агент мягче оценил; 3) ложное повышение

  ➕ НОВЫЕ ТРЕБОВАНИЯ (40) - агент нашёл дополнительные:

     [Context] MUST found: The API MUST accept the following parameters:
     [Env Vars] MUST found: Invalid or unrecognized input MUST be logged and MUST be otherwise ignored, i.e.
     [Env Vars] SHOULD found: The following paragraph was added after stabilization and the requirements are t
     [Logs Api] MUST found: The API MUST accept the following parameters: Timestamp (optional), Observed Tim
     [Logs Sdk] MUST found: If configuration is updated (e.g., adding a `LogRecordProcessor`), the updated c
     [Logs Sdk] SHOULD partial: `ForceFlush` SHOULD return some ERROR status if there is an error condition; and
     [Logs Sdk] SHOULD found: `ForceFlush` SHOULD return some ERROR status if there is an error condition; and
     [Logs Sdk] SHOULD partial: In the case where an invalid `name` (null or empty string) is specified, a worki
     [Logs Sdk] SHOULD found: In the case where an invalid `name` (null or empty string) is specified, a worki
     [Logs Sdk] SHOULD found: SDKs SHOULD return a valid no-op `Logger` for these calls, if possible.
     [Metrics Api] MUST found: The API MUST treat observations from a single callback as logically taking place
     [Metrics Api] MUST found: Therefore, this API needs to be structured to accept a `schema_url`, but MUST NO
     [Metrics Api] SHOULD found: The API to register a new Callback SHOULD accept:
     [Metrics Api] MUST found: The API MUST treat observations from a single Callback as logically taking place
     [Metrics Sdk] MUST partial: although individual reservoirs MUST still be instantiated per metric-timeseries 
     [Metrics Sdk] MUST found: The "offer" method MAY accept a filtered subset of `Attributes` which diverge fr
     [Metrics Sdk] MUST found: The implementation MUST maintain reasonable minimum and maximum scale parameters
     [Metrics Sdk] MUST found: If no View matches, or if a matching View selects the default aggregation, the `
     [Metrics Sdk] SHOULD found: When a Meter creates an instrument, it SHOULD validate the instrument advisory p
     [Metrics Sdk] MUST found: If both a View and advisory parameters specify the same aspect of the Stream con
     ... и ещё 20

  ➖ ПРОПУЩЕННЫЕ ТРЕБОВАНИЯ (40) - были раньше, теперь нет:

     [Context] MUST found: The API MUST accept the following parameters: * A `Token` that was returned by a
     [Env Vars] MUST found: Invalid or unrecognized input MUST be logged
     [Env Vars] SHOULD found: For new implementations, these should be treated as MUST requirements.
     [Logs Api] MUST found: The API MUST accept the following parameters:
     [Logs Sdk] MUST found: it MUST NOT matter whether a Logger was obtained from the LoggerProvider before 
     [Logs Sdk] SHOULD partial: ForceFlush SHOULD return some ERROR status if there is an error condition
     [Logs Sdk] SHOULD partial: and if there is no error condition, it SHOULD return some NO ERROR status
     [Logs Sdk] SHOULD found: its name SHOULD keep the original invalid value
     [Logs Sdk] SHOULD found: and a message reporting that the specified value is invalid SHOULD be logged.
     [Logs Sdk] SHOULD found: After the call to Shutdown, subsequent attempts to get a Logger are not allowed.
     [Metrics Api] MUST found: observations from a single callback MUST be reported with identical timestamps
     [Metrics Api] MUST NOT found: Therefore, this API needs to be structured to accept a schema_url, but MUST NOT 
     [Metrics Api] SHOULD found: The API to register a new Callback SHOULD accept: A `callback` function* A list 
     [Metrics Api] MUST found: observations from a single callback MUST be reported with identical timestamps.
     [Metrics Sdk] MUST found: Individual reservoirs MUST still be instantiated per metric-timeseries.
     [Metrics Sdk] MUST found: The reservoir MUST be given the Attributes associated with its timeseries point 
     [Metrics Sdk] MUST found: Implementations are REQUIRED to accept the entire normal range of IEEE floating 
     [Metrics Sdk] MUST found: the `ExplicitBucketBoundaries` advisory parameter MUST be used
     [Metrics Sdk] SHOULD found: it SHOULD validate the instrument advisory parameters
     [Metrics Sdk] MUST found: MUST take precedence over the advisory parameters
     ... и ещё 20

  Итого изменений: 207
    Понижений: 73, Повышений: 54, Боковых: 0
    Новых req: 40, Пропущенных req: 40
    Новых секций: 0, Исчезнувших секций: 0

  ⚠️  РЕКОМЕНДАЦИЯ: перепроверьте понижения и пропущенные требования вручную, чтобы отличить реальные регрессии от вариативности агентов.

======================================================================
```
