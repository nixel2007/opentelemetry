// Fixture: процессор, который при завершении спана добавляет в провайдер другой процессор.
// Детерминированная модель конкурентного ДобавитьПроцессор во время обработки спана.
// BSLLS:PublicMethodsDescription-off
// BSLLS:MissingParameterDescription-off
// BSLLS:MissingReturnedValueDescription-off
// BSLLS:MissingVariablesDescription-off
// BSLLS:ExportVariables-off

Перем Провайдер Экспорт;
Перем ДобавляемыйПроцессор Экспорт;

Процедура ПриНачале(Спан, РодительскийКонтекст = Неопределено) Экспорт // BSLLS:UnusedParameters-off
КонецПроцедуры

Процедура ПередЗавершением(Спан) Экспорт // BSLLS:UnusedParameters-off
КонецПроцедуры

Процедура ПриЗавершении(Спан) Экспорт // BSLLS:UnusedParameters-off
    Провайдер.ДобавитьПроцессор(ДобавляемыйПроцессор);
КонецПроцедуры

Функция СброситьБуфер(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
    Возврат Истина;
КонецФункции

Процедура Закрыть() Экспорт
КонецПроцедуры
