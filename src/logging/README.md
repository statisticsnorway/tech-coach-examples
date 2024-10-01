# Logging i python

Filene i denne mappen viser hvordan du kan bruke logging i python til å skrive ut
informasjon fra koden din, både til skjerm og til fil.

> [!NOTE]
> Merk: Med *logging* mener vi her informasjon som er nyttig ved utvikling av kode, men
> *ikke* data som skal tas vare på og lagres permanent. Prosessdata,
> kvalitetsindikatorer og tilsvarende ting skal lagres i bøtter i et definert format.

## Fordeler med logging vs bruk print-setninger

* Python sitt loggesystem støtter ulike **loggenivåer**, som lar deg skille mellom
meldinger av ulik viktighet. Noen vanlige nivåer er: `DEBUG`, `INFO`, `WARNING`,
`ERROR` og `CRITICAL`.
* Med logging kan du enkelt logge til filer, konsollen, eller til og med eksterne
loggesystemer, i stedet for å kun skrive til konsollen som med print. Dette er nyttig
for kode i produksjon, der det er viktig å kunne hente fram logger fra filer
for å spore opp problemer.
* Loggesystemet lar deg enkelt tilpasse formatet på loggmeldingene ved å legge til
tidsstempler, loggnivå, filnavn, linjenummer, osv. Dette gjør det mye lettere å finne
ut hvor og når en bestemt hendelse oppstod, spesielt ved feilsøking.

## Om koden

`log_sender.py`: Denne filen viser hvordan du skriver logmeldinger i vanlig kode.
Den bruker kun standard python, ikke noe egenutviklet.

`ssb_logger.py`: Denne definerer en klasse, `SsbLogger`, som setter opp mottak,
formattering og output av loggemeldinger. Output sendes til konsollen og til fil.
Du trenger kun å lage en instans av denne, på toppen der du kjører koden din.
I tillegg inneholder den en dekorator du kan bruke over funksjonene dine for å
få en automatisk logmelding når kjøringen av koden går inn og ut av funksjonen.

`log_demo.py`: Denne filen viser hvordan det hele brukes og settes opp. Dette
er en typisk topp-fil der koden kjøres fra.

## Kjør eksempel

```shell
poetry run src/logging/log_demo.py
```
