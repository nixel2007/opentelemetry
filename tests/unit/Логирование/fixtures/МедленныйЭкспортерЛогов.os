// Fixture: медленный экспортер логов - засыпает при экспорте для тестирования таймаута.
// BSLLS:PublicMethodsDescription-off
// BSLLS:MissingParameterDescription-off
// BSLLS:MissingReturnedValueDescription-off
// BSLLS:MissingVariablesDescription-off
// BSLLS:MagicNumber-off

Функция Экспортировать(МассивЗаписей, Таймаут = Неопределено) Экспорт // BSLLS:UnusedParameters-off
    Приостановить(200);
    Возврат Истина;
КонецФункции

Функция ПолучитьВременнуюАгрегацию(ТипИнструмента) Экспорт // BSLLS:UnusedParameters-off
    Возврат Неопределено;
КонецФункции

Функция СброситьБуфер(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
    Возврат ОтелРезультатыЭкспорта.Успех();
КонецФункции

Процедура Закрыть() Экспорт
КонецПроцедуры
