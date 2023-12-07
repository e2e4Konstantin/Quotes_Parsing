-- Таблица 4.8-288. Трубы гофрированные поливинилхлоридные открыто по стенам и потолкам с установкой соединительных коробок
select c.ID_tblCatalog, c.* from tblCatalogs c
where c.FK_tblCatalogs_tblDirectoryItems = (
        select di.ID_tblDirectoryItem from tblDirectoryItems di where di.name = 'Таблица'
    )   and c.code REGEXP '^4\.8-\d+-\d+-0-288';
-- 4830

-- получить все Уникальные значения атрибутов с названием "Способ" a.name = 'Способ' and
select a.* from tblAttributes a where a.FK_tblAttributes_tblQuotes in
    (select q.ID_tblQuote from tblQuotes q where q.FK_tblQuotes_tblCatalogs = 4830);

select distinct a.name from tblAttributes a where a.FK_tblAttributes_tblQuotes in (select q.ID_tblQuote from tblQuotes q where q.FK_tblQuotes_tblCatalogs = 4830);
-- Материал, Способ, Тип, Элемент


select distinct a.value from tblAttributes a where a.name = 'Способ' and a.FK_tblAttributes_tblQuotes in (select q.ID_tblQuote from tblQuotes q where q.FK_tblQuotes_tblCatalogs = 4830);

select count(distinct a.value) from tblAttributes a where a.name = 'Способ' and a.FK_tblAttributes_tblQuotes in (select q.ID_tblQuote from tblQuotes q where q.FK_tblQuotes_tblCatalogs = 4830);