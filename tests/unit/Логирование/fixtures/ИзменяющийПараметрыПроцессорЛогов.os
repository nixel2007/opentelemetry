// Fixture: процессор, который в Включен() изменяет переданные параметры.
// BSLLS:PublicMethodsDescription-off
// BSLLS:MissingParameterDescription-off
// BSLLS:MissingReturnedValueDescription-off

// BSLLS:NumberOfOptionalParams-off
// BSLLS:UnusedParameters-off
Функция Включен(
        Контекст = Неопределено,
        ОбластьИнструментирования = Неопределено,
        СтепеньСерьезности = 0,
        ИмяСобытия = "") Экспорт
// BSLLS:UnusedParameters-on
// BSLLS:NumberOfOptionalParams-on
    Если ТипЗнч(Контекст) = Тип("Соответствие") Тогда
        Контекст.Вставить("изменено процессором", Истина);
    КонецЕсли;
    СтепеньСерьезности = 99;
    ИмяСобытия = "ИЗМЕНЕНО";
    Возврат Истина;
КонецФункции

Процедура ПриПоявлении(ЗаписьЛога, Контекст = Неопределено) Экспорт // BSLLS:UnusedParameters-off
КонецПроцедуры

Функция СброситьБуфер(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
    Возврат ОтелРезультатыЭкспорта.Успех();
КонецФункции

Функция Закрыть(ТаймаутМс = 0) Экспорт // BSLLS:UnusedParameters-off
    Возврат ОтелРезультатыЗакрытия.Успех();
КонецФункции
