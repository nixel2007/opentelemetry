// Fixture: медленный процессор логов — засыпает в СброситьБуфер для тестирования таймаута.
// BSLLS:PublicMethodsDescription-off
// BSLLS:MissingParameterDescription-off
// BSLLS:MissingReturnedValueDescription-off
// BSLLS:MissingVariablesDescription-off
// BSLLS:MagicNumber-off

Процедура ПриПоявлении(ЗаписьЛога, Контекст = Неопределено) Экспорт // BSLLS:UnusedParameters-off
КонецПроцедуры

Функция Включен(
        Контекст = Неопределено,
        ОбластьИнструментирования = Неопределено,
        СтепеньСерьезности = 0,
        ИмяСобытия = "") Экспорт // BSLLS:UnusedParameters-off
    Возврат Истина;
КонецФункции

Функция СброситьБуфер(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
    Приостановить(200);
    Возврат ОтелРезультатыЭкспорта.Успех();
КонецФункции

Процедура Закрыть(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
КонецПроцедуры
