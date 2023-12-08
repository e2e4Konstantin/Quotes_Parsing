SELECT c.ID_tblCatalog,  c.*
FROM tblCatalogs c
WHERE
  c.FK_tblCatalogs_tblDirectoryItems = (
      SELECT di.ID_tblDirectoryItem FROM tblDirectoryItems di WHERE di.name = 'Таблица'
    )
  AND c.code REGEXP '^4\.8-\d+-\d+-0-288';

SELECT a.*
FROM  tblAttributes a
WHERE
  a.FK_tblAttributes_tblQuotes IN (SELECT q.ID_tblQuote FROM tblQuotes q WHERE q.FK_tblQuotes_tblCatalogs = 4830);

SELECT DISTINCT a.name
FROM tblAttributes a
WHERE
  a.FK_tblAttributes_tblQuotes IN (
      SELECT q.ID_tblQuote FROM tblQuotes q WHERE q.FK_tblQuotes_tblCatalogs = 4830);


SELECT DISTINCT a.value
FROM tblAttributes a
WHERE
  a.name = 'Способ'
  AND a.FK_tblAttributes_tblQuotes IN (
      SELECT q.ID_tblQuote FROM tblQuotes q WHERE q.FK_tblQuotes_tblCatalogs = 4830);


SELECT COUNT(DISTINCT a.value)
FROM tblAttributes a
WHERE
  a.name = 'Способ'
  AND a.FK_tblAttributes_tblQuotes IN (
      SELECT q.ID_tblQuote FROM tblQuotes q WHERE q.FK_tblQuotes_tblCatalogs = 4830
    );
