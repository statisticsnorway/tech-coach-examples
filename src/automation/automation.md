# Automatisk kjøring av flere notebooks

Å dele opp Jupyter notebooks i funksjoner er nyttig av minst to grunner:

1. Det muliggjør testing av koden.
2. Du kan automatisere kjøring av mange notebooks etter hverandre ved å kalle
   funksjoner. Dette er 10-100 ganger raskere enn å bruke Papermill og gir bedre
   programstruktur. **Automatisere ved å bruke funksjoner er den anbefalte måten
   å kjøre flere notebooks etter hverandre på.**

## Eksempel

GitHub-repoet [tech-coach-examples] inneholder både eksempel på automatisering med
papermill og automatisering ved å bruke pythonfunksjoner.
Begge eksemplene automatiserer den samme koden som består av to notebooks,
`child1.py` og `child2.py`.

Kort om hva eksempelnotebookene gjør:

- `child1.py` leser inn valutakurser, gjør dataminimering og lagrer resultatet til fil.
  Typisk det som gjøres fra kildedata til inndata.
- `child2.py` leser opp filen, beregner gjennomsnittlig valutakurs per måned for hver
  valuta og lagrer til fil.

I begge eksemplene lages det en overordnet notebook, `parent`, som kjører
child-notebookene. Papermill-katalogen viser hvordan dette gjøres for Papermill,
mens pythonfunctions-katalogen viser hvordan det gjøres med funksjoner.

Vi har beskrevet hvordan man kommer fra papermill og over til eksemplet på
automatisering ved hjelp av pythonfunksjoner. Se beskrivelse på [Confluence].

[tech-coach-examples]: https://github.com/statisticsnorway/tech-coach-examples/
[confluence]: https://statistics-norway.atlassian.net/wiki/spaces/KOD/pages/3925147685/Hvordan+automatisere+Jupyter+notebooks+ved+bruk+av+funksjoner#Konverter-en-notebook-til-funksjoner
