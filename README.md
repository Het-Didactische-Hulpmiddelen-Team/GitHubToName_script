# GitHub to Name (Translatr): Clonr
Clonr is een softwarepaket dat behoort tot het Translatr project van het DHT. Het heeft drie hoofdfunctionaliteiten die telkens uitgewerkt zijn in een appart script:
* GitHub organisaties ophalen: <strong>Organisation Gettr</strong>
* GitHub usernames omzetten naar studenten namen en omgekeerd: <strong>Username Translatr</strong>
* Repositories clonen: <strong>Clonr</strong>

## Organisation Gettr
Een Python script genaamd <code>OrganisationGetr.py</code>, simpelweg uit te voeren door <code>./OrganisationGetr.py</code> te typen in een terminal en op enter te duwen.

Het script zal alle GitHub organisaties waar de gebruiker lid van is afdrukken in de terminal.

  > Belangrijk: de gebruiker moet een [personal access token](https://github.com/settings/tokens) voor GitHub hebben. Deze token en ook de GitHub username van de gebruiker, moeten ingegeven worden in het script.
  
## Username Translatr
Een Python script genaamd <code>Translatr.py</code>. Uitvoering gebeurd door volgende zaken in te geven in een terminal:
* <code>./Translatr.py</code>
* Een van de opties <code>-u</code> of <code>-n</code>. Een optie meegeven is verplicht, maar slechts een van de twee is toegelaten, niet beide. In het geval van de <code>-u</code> optie, moet er ook een GitHub username meegegeven worden. In het andere geval, de voornaam en achternaam van een student (gescheiden door een spatie).
* Ook is er de optionele optie <code>-i</code>. Deze optie gaat gebruik maken van alternatieve input voor het vertalen van de namen (niet via de GitHub to Name API van DHT). De optie verwacht ook het pad naar de input file waar de naam mappings in staan. Deze file moet een txt file zijn en moet geformateerd zijn als volgt: <code>GitHub_username Firstname Lastname\n</code>.
* Als laatste is er de <code>-h</code> optie die hulp bied bij het gebruiken van het script.

Het script zal de ingegeven GitHub-username/studenten-naam omzetten naar de overeenkomstige studenten-naam/GitHub-username en deze afdrukken in de terminal.

  > Belangrijk: ook hier moet de GitHub personal access token ingegeven worden in het script.
  
## Clonr
Een Python script genaamd <code>RepoClonr.py</code>. Uitvoering gebeurd door volgende zaken in te geven in een terminal:
* <code>./RepoClonr.py</code>
* De optionele optie <code>-o</code> om rechtstreeks de organisatie mee te geven die gecloned zal worden. De naam van de organisatie moet ook ingevoerd worden.
* De optionele optie <code>-p</code> om rechtstreeks een pad mee te geven waar het script de gecloonde organisatie folder zal plaatsen. Het pad moet absoluut zijn en eindigen op een <code>/</code>.
* Ook is er de optionele optie <code>-i</code>. Deze optie gaat gebruik maken van alternatieve input voor het vertalen van de namen (niet via de GitHub to Name API van DHT). De optie verwacht ook het absolute pad naar de input file waar de naam mappings in staan. Deze file moet een txt file zijn en moet geformateerd zijn als volgt: <code>GitHub_username Firstname Lastname\n</code>.
* Als laatste is er de <code>-h</code> optie die hulp bied bij het gebruiken van het script.

Het script zal alle repositories van een bepaalde organisatie clonen naar de pc van de gebruiker op de opgegeven plaats. Het geheel zal in een directory met de naam van de organisatie zitten. In deze organisatie is er voor elke student een directory, met de naam van de student, met hier de repositories van deze student in.

Filestructuur

    PVM
    ├── Student One
    │   └── Repo One
    ├── Student Two
    │   ├── Repo One
    │   └── Repo Two
    └── Student Three
        └──Repo One

  > Belangrijk: ook hier moet de GitHub personal access token ingegeven worden in het script.
