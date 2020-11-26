# ILC Projekt

## Projektbeschreibung

Das Projekt besteht aus drei Komponenten, der Datenbank der BUW, welche die Excel Tabellen mit allen benötigten Informationen bereitstellt. Dem RWTH Generator, dieser erstellt aus den Informationen in den Excel Tabellen die Model View Definition als XML Datei (mvdXML). Und dem RWTH Validator, der eine Prüfung von IFC Modellen mit den vorher erstellten mvdXML als Prüfdatei, durchführt.
Die hier vorhandene Implementierung ermöglicht zwei Prozessumsetzungen:

1. mvdXML erstellen
2. IFC prüfen

Das Programm funktioniert template basiert, es können einfache mvdXML Dateien für Property Sets erstellt werden. 
Für das Durchführen einer IFC Prüfung werden ebenfalls die Tabellen der BUW benötigt sowie das IFC Modell. 


## Projektstatus

Aktuell gibt es zu allen Abschnitten einen Entwurf. 
Noch in Arbeit sind Applicabilities in mvdXML.
Die generate.py Datei ist wenig optimiert.
Prüfungen beider RWTH Anwendungen (Generator und Validator) mit umfangreichen Dateien.
Die Möglichkeit idmXML muss noch implementiert werden.
Beim Interface fehlen Login Funktionsbeispiel und darstellende Seiten (Demonstrationszweck).
Unabhängige, einfache mvdXML erstellen muss noch implementiert werden (Ordner: dc_interface). 
Ordner müssen aufgeräumt werden.

## Projektaufbau

Das Projekt besteht bisher aus einem __Front-__ und einem __Backend__. 
Backend:

* guid.py
* rules.py
* xml.py
* xml_laden.py
* generate.py

Frontend:

* View.py
* run.py


## Verwendete Technologien

Benutze Entwicklungsumgebung(en):

* JetBrains PyCharm Community Edition 2019.3
* Visual Studio Code

Geschrieben in __Python 3__.

Weitere verwendete Bibliotheken:

* numpy
* flask
* requests
* pandas
* lxml


## Anforderung/ Anleitung

Download der Ordner __ILC Interface__ und __Generator__, Entwicklungsumgebung einrichten, run.py ausführen.

Die Anwendung kann mit den Dateiformaten .xlxs, .csv und .ifc genutzt werden.