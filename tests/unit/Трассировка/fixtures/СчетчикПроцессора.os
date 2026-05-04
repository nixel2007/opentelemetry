// Fixture: считает количество вызовов ПриЗавершении.
// Используется для проверки однократного вызова процессора при повторном завершении спана.
// BSLLS:PublicMethodsDescription-off
// BSLLS:MissingParameterDescription-off
// BSLLS:MissingReturnedValueDescription-off
// BSLLS:MissingVariablesDescription-off
// BSLLS:ExportVariables-off

Перем КоличествоВызовов Экспорт;

Процедура ПриНачале(Спан, РодительскийКонтекст = Неопределено) Экспорт // BSLLS:UnusedParameters-off
КонецПроцедуры

Процедура ПередЗавершением(Спан) Экспорт // BSLLS:UnusedParameters-off
КонецПроцедуры

Процедура ПриЗавершении(Спан) Экспорт // BSLLS:UnusedParameters-off
    КоличествоВызовов = КоличествоВызовов + 1;
КонецПроцедуры

Функция СброситьБуфер(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
    Возврат Истина;
КонецФункции

Процедура Закрыть() Экспорт
КонецПроцедуры

КоличествоВызовов = 0;
