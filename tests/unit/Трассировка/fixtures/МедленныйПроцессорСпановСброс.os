// Fixture: медленный процессор спанов — засыпает в СброситьБуфер для тестирования таймаута.
// BSLLS:PublicMethodsDescription-off
// BSLLS:MissingParameterDescription-off
// BSLLS:MissingReturnedValueDescription-off
// BSLLS:MissingVariablesDescription-off
// BSLLS:MagicNumber-off

Процедура ПриНачале(Спан, РодительскийКонтекст = Неопределено) Экспорт // BSLLS:UnusedParameters-off
КонецПроцедуры

Процедура ПередЗавершением(Спан) Экспорт // BSLLS:UnusedParameters-off
КонецПроцедуры

Процедура ПриЗавершении(Спан) Экспорт // BSLLS:UnusedParameters-off
КонецПроцедуры

Функция СброситьБуфер(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
    Приостановить(200);
    Возврат ОтелРезультатыЭкспорта.Успех();
КонецФункции

Процедура Закрыть(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
КонецПроцедуры
