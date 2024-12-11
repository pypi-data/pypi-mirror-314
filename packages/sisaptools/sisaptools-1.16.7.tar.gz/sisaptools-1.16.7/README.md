Overview
--------
[Package](https://pypi.python.org/pypi/sisaptools) amb eines comunes utilitzades en els processos de càlcul de [SISAP](https://github.com/sisap-ics/sisap) i de [SIDIAP](https://bitbucket.org/sisapICS/sidiap/overview).

Requisites
----------
* les dependències s'instalen automàticament, però cal tenir instantclient d'Oracle i client mariaDB (per exemple amb contenidor [pydb](https://hub.docker.com/r/sisap/pydb/))
* definir les variables d'entorn (environment)
  * APP_CHARSET (default `utf8`)
  * TMP_FOLDER (default `/tmp`)
  * AES_KEY ('path/to/.aes') no hi ha ruta per default, i faria servir la clau 'testkey' 

Packaging
---------
* canviar versió a setup.py
* publish.sh

A note on character encoding
----------------------------
### MySQLdb / PyMySQL
* Consideracions prèvies:
  * El paràmetre `CHARSET` de la connexió serveix per codificar i decodificar en cas que s'utilitzi `unicode` per entrada o sortida. Hi ha una diferència important entre els dos paquets:
    * A `MySQLdb` executa un `SET NAMES` (almenys a `1.3.7`), i per tant estableix `character_set_client` per l'entrada i `character_set_results` per la sortida
    * A `PyMySQL` no ho fa (almenys a `0.7.9`), i per tant cal fer-ho específicament (`INIT_COMMAND` o manualment després de connectar). És imprescindible que coincideixin
    * Per ordre, primer s'executa `INIT_COMMAND`, després `CHARSET` (a `MySQLdb`) i després el que es faci manualment després de connectar
* L'entrada depèn del que s'envia:
  * `bytes`: han de ser en la mateixa codificació que `character_set_client` (establert per qualsevol mètode, veure Consideracions prèvies)
  * `unicode`: guardarà sempre bé (internament utilitza `CHARSET` per fer encode a `python`, i el servidor utilitza `character_set_client` per interpretar-ho)
* La sortida depèn del paràmetre `USE_UNICODE` de la connexió (default `python2`: depèn de si s'especifica `CHARSET` o no; default `python3`: `True`):
  * Si és False: retorna `bytes` segons el valor de `character_set_results` (establert per qualsevol mètode, veure Consideracions prèvies)
  * Si és True: retorna `unicode` (internament el servidor utilitza `character_set_results` per retornar, i després `python` utilitza `CHARSET` per decodificar)

### Redis
* Entrada depèn del que s'envia:
  * `bytes`: guarda sense modificació
  * `unicode`: guarda codificat segons el paràmetre `ENCODING` de la connexió (default: `utf8`)
* Sortida depèn del paràmetre `DECODE_RESPONSES` de la connexió (default: `False`):
  * `False`: retorna `bytes` (sense modificació)
  * `True`: retorna `unicode` segons el paràmetre `ENCODING` de la connexió (default: `utf8`)

### cx_Oracle
Es comporta diferent segons la versió de l'intèrpret, sense possibilitat de configuració:
* En `python2` treballa sempre en `bytes` amb la codificació especificada a `NLS_LANG`, tant per l'entrada com per la sortida
* En `python3` treballa sempre en `unicode`, tant per l'entrada com per la sortida (internament el servidor retorna segons `NLS_LANG`, i després `python` decodifica segons el mateix paràmetre)

### pymongo
MongoDB guarda sempre en `utf8`
* Entrada: Es pot enviar tant `unicode` com `utf8`, però no altres encodings
* Sortida: Torna sempre `unicode` excepte si l'entrada s'ha fet amb `bytes` de `python3`; en aquest cas torna `Binary` en python2 i `bytes` en python3
