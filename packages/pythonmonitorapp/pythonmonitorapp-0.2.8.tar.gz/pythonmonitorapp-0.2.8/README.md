# Costruzione di una Pipeline CD/CI - il caso “Python monitor app”

**Assignment 2** svolto dal gruppo FPV:
- Marco Ferioli, 879277
- Luca Pinciroli, 885969
- Giulia Raffaella Vitale, 885938

## Report del lavoro svolto

### 1. Progetto selezionato ed operazioni di modifica
Il progetto selezionato è una semplice web application realizzata in python, che permette di monitorare in real time il funzionamento della CPU e dei processi in esecuzione sul proprio computer.

Al fine di costruire la pipeline CI / CD sono state effettuate delle modifiche preliminari sul progetto.
In particolare sono state aggiornate e aggiunte diverse dipendenze presenti all’interno del file `requirements.txt` e sono stati introdotti i file `setup.py` e `mkdocs.yml` per effettuare alcune delle operazioni della pipeline.

### 2. Cache
Al fine di rendere efficiente l’uso delle risorse ed evitare che le operazioni siano ridondanti, è stata predisposta una cache nel quale è stato salvato l’ambiente virtuale usato dalla pipeline:

```yaml
default:
    cache:
        paths:
            - src/.venv
```

Nei successivi stage, come è possibile notare anche dal codice, il contenuto della cache viene recuperato nel `before_script` ed utilizzato al fine di velocizzare le operazioni svolte.

### 3. Definizione degli stages
L’implementazione della pipeline CI/CD per un applicativo python prevede anzitutto la costituzione di un file di configurazione Yaml, di norma denominato `.gitlab-ci.yml`: tale file contiene le istruzioni che GitLab deve utilizzare al fine di eseguire automaticamente i task della pipeline.

La pipeline è strutturata in sei stages: build, verify, test, package, release, docs; ciascuno degli stage è specificato all’interno di `stages`:

```yaml
stages:
    - build
    - verify
    - test
    - package
    - release
    - docs
```

Per ciascuno degli stages, vengono riportati di seguito i relativi jobs.

### 4. Build
Build è lo stage nel quale si verifica che il codice dell’applicazione compili correttamente.

In quanto linguaggio interpretato, Python non richiede una fase di compilazione; di conseguenza, questo stage si limita all'installazione e alla risoluzione delle dipendenze del progetto.

```yaml
build_app:
    stage: build
    before_script: 
        - . src/.venv/bin/activate
    script:
        - apt-get update && apt-get install -y python3-venv
        - python3 -m venv src/.venv 
        - pip install -r src/requirements.txt 
```

All’interno del job vengono eseguiti tre differenti step: il primo si occupa dell'installazione degli strumenti necessari all’esecuzione del progetto, il secondo crea l’ambiente virtuale utilizzato per il task, mentre il terzo effettua l’installazione delle dipendenze necessarie.

### 5. Verify
Verify è lo stage utilizzato per il controllo di stile e sicurezza, al fine di assicurare che il codice segua standard di qualità uniformi.

Nell’esecuzione di tale stage sono state effettuate due tipologie di **analisi statica** (senza esecuzione del codice), ossia l’analisi della qualità del codice e l’analisi della sicurezza.

L’analisi della qualità del codice utilizza **Prospector**, un tool che informa riguardo la presenza di possibili errori, potenziali problemi e violazioni di convenzioni:

```yaml
code_quality: 
    stage: verify
    before_script: 
        - . src/.venv/bin/activate
    script:
        - prospector src --output-format json > prospector-report.json
    artifacts:
        paths:
            - prospector-report.json
        when: on_failure
    allow_failure: true
```

L’analisi sulla sicurezza usa invece **Bandit**, un tool progettato per trovare problemi comuni di sicurezza nel codice Python:

```yaml
security_scan:
    stage: verify
    before_script: 
        - . src/.venv/bin/activate
    script:
        - bandit -r src --severity-level low -f json -o bandit-report.json
    artifacts:
        paths:
            - bandit-report.json
        when: on_failure
    allow_failure: true
```

In entrambi i casi, viene usato il comando `allow_failure: true`, il quale consente di segnalare errori di stile del codice senza bloccare l’intero processo della pipeline.
Nel caso siano presenti errori, questi verranno salvati in un file json come artefatto, al fine di poterli consultare.

Per quanto riguarda l’**analisi dinamica** del codice, all’interno della pipeline vengono effettuate due operazioni: un controllo sul test-coverage ed uno sulla vulnerabilità delle dipendenze installate.

Per la prima operazione è stato utilizzato il seguente frammento di codice:

```yaml
coverage_dynamic_analysis:
    stage: verify
    before_script: 
        - . src/.venv/bin/activate
    script:
        - pytest --cov=src --cov-report=xml:coverage.xml --cov-fail-under=80
    artifacts:
        paths:
            - coverage.xml
```

L’obiettivo è verificare che il codice dei file all’interno della cartella `src` sia ben coperto dai test; viene inoltre stabilita una soglia minima di coverage tramite il tag `cov-fail-under`. 
Viene infine prodotto l’artifact `coverage.xml`, contenente il livello di copertura.

Per mettere in atto la seconda operazione, è stato invece utilizzato il seguente frammento di codice:

```yaml
dependency_check:
    stage: verify
    script:
        - apt-get update && apt-get install -y openjdk-11-jre curl unzip  
        - curl -sSL https://github.com/jeremylong/DependencyCheck/releases/download/v8.3.1/dependency-check-8.3.1-release.zip -o dependency-check.zip
        - ls -lh dependency-check.zip 
        - unzip dependency-check.zip -d dependency-check
        - ls -lh dependency-check/dependency-check/bin 
        - dependency-check/dependency-check/bin/dependency-check.sh --project FlaskApp --scan src --out dependency-check-report.html
    artifacts:
        paths:
            - dependency-check-report.html
        when: always
```
L'obiettivo del codice eseguito è quello di identificare eventuali vulnerabilità all’interno delle dipendenze installate, contribuendo a migliorare la sicurezza del progetto.

Il funzionamento del job si basa sull’utilizzo dei seguenti componenti:
- `openjdk-11-jre`\
Rappresenta il Java Runtime Environment necessario per eseguire il tool OWASP dependency-check.
- `curl` e `unzip`\
Sono pacchetti utili per scaricare e decomprimere la release del tool.

Tramite `curl` ed `unzip` viene scaricato lo strumento di analisi delle dipendenze, che viene successivamente de-compresso dal formato `.zip`.
A questo punto è possibile eseguire `dependency-check`, che successivamente produce un artefatto contenente le vulnerabilità individuate.

### 6. Test
Lo stage `test` consente di avviare automaticamente i test presenti nel progetto, in modo tale da verificare che l’applicazione superi i test prima di effettuare la release, assicurandosi così che ogni componente operi come previsto.

Per eseguire i test è stato utilizzato il comando `pytest`:

```yaml
unit_tests:
    stage: test
    before_script: 
        - . src/.venv/bin/activate
    script:
        - pytest -v src/app/tests/test_api.py
        - pytest -v src/app/tests/test_views.py

performance_tests:
    stage: test
    needs: [unit_tests]
    before_script: 
        - . src/.venv/bin/activate
    script:
        - pytest -v src/app/tests/test_performance.py
```

L’esecuzione dei test è stata predisposta per fare in modo che i test di performance vengano eseguiti solo nel caso in cui i test di unità vadano a buon fine.
Per effettuare tale operazione viene utilizzata la parola chiave `needs`; i due job sono quindi eseguiti in sequenza.

### 7. Package
Tale stage consente la costruzione del pacchetto dell’applicazione, salvato come artefatto, in modo tale da renderlo disponibile negli stage successivi della pipeline.

```yaml
package:
    stage: package
    before_script: 
        - . src/.venv/bin/activate
    script:
        - python setup.py sdist bdist_wheel  
    artifacts:
        paths:
            - dist/*.whl
            - dist/*.tar.gz 
```

### 8. Release
Il job release nella pipeline CI/CD è progettato per rilasciare il codice come pacchetto Python su **PyPI** (Python Package Index).

```yaml
release:
    stage: release
    before_script: 
        - . src/.venv/bin/activate
    script:
        - pip install twine
        - twine upload dist/* -u "__token__" -p "$PYPI_TOKEN"
    only:
        - main
    dependencies:
        - package
```

Al fine di effettuare tale operazione è stato utilizzato **Twine**.
Lo strumento viene installato e successivamente viene utilizzato per caricare la release su PyPI sfruttando un token.
Le variabili sono state definite in settings -> CI/CD. 

Questo job dipende dal risultato del job package, in quanto quest’ultimo deve andare a buon fine per poter rilasciare il prodotto.
Inoltre viene eseguito solamente se il branch attivo è main, in modo tale da evitare rilasci accidentali su branch secondari.

Al fine di effettuare correttamente la release, è importante aggiornare il numero di versione dell’applicativo prima di far eseguire la pipeline.

### 9. Docs
La documentazione del progetto consiste in un file in markdown che si trova all’interno della cartella `doc` nella root del progetto. 
L’ultima fase della pipeline si occupa della pubblicazione di tale documentazione su GitLab Pages.
Al fine di eseguire questa operazione sono stati predisposti i seguenti job:

```yaml
documentation:
    stage: docs
    before_script: 
        - . src/.venv/bin/activate
    script:
        - pip install -r src/requirements.txt
        - mkdocs build --site-dir public 
    artifacts:
        paths:
            - public  
pages:
    stage: docs
    needs: [documentation]
    script:
        - echo "Sito generato in public, pronto per GitLab Pages"
    artifacts:
        paths:
            - public
```

Il job `documentation` utilizza **MkDocs** per generare il sito statico sul quale verrà visualizzata la documentazione del progetto, mentre il job `pages` si occupa della pubblicazione del sito su **GitLab** **Pages**.

### 10. Risultato finale
Ecco come appaiono gli stage con i rispettivi job all’interno dell’ambiente GitLab:

![pipeline](https://i.ibb.co/09dWj7x/pipeline.png)

Come è possibile notare, tutti i job predisposti vengono completati con successo, ad eccezione di `security_scan` che produce un warning.