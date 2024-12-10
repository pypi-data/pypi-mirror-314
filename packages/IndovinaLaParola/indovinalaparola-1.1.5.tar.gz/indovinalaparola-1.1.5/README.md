# Processo e Sviluppo del Software
Assignment 2 - DevOps - Gruppo Gasa
Realizzato da:Bishara Giovanni, Mocellin Andrea






## L’Applicazione

Indovina la Parola è un gioco interattivo in cui l'obiettivo è indovinare una parola segreta scegliendo lettere una per volta. Ogni volta che l'utente inserisce una lettera corretta, la parola si aggiorna mostrando la lettera nella posizione giusta, mentre le lettere sbagliate fanno diminuire i tentativi disponibili. Il gioco termina quando l'utente indovina la parola o esaurisce i tentativi a disposizione.
[Link alla Repository](https://gitlab.com/gasa9965349/gasa)



## Il Codice
Il codice sorgente dell’applicazione è organizzato nei seguenti file:
IndovinaLaParola.py: Il file principale dell’applicazione 


## La Pipeline
``` 
image: python:latest

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

before_script:
  - python -V
  - pip install virtualenv
  - virtualenv venv
  - source venv/bin/activate  #Attiva l'ambiente virtuale per il resto della pipeline

stages:
  - build
  - verify
  - test
  - package
  - release
  - docs

build:
  stage: build
  script:
    - echo "Fase di build installazione delle dipendenze."
    - pip install prospector bandit
    - pip install pytest
    - pip install setuptools
    - pip install wheel
    - pip install --upgrade build
    - pip install twine
    - pip install mkdocs
    - echo "Dependencies installed."

verify:
  stage: verify
  script:
    - bandit -r ./IndovinaLaParola.py
    - prospector ./IndovinaLaParola.py --no-autodetect 

test:
  stage: test
  script:
    - echo "Fase di test esecuzione dei test automatici."
    - pytest  

package:
  stage: package
  script:
    - python -m build
  artifacts:
    paths:
      - dist/*  

release:
  stage: release
  script:
   - twine upload dist/* -u __token__ -p $PYPI_TOKEN  
  

docs:
  stage: docs
  script:
    - mkdocs build
    - cp -r ./site ../public
  artifacts:
    paths:
      - public 
 
```
## Build
In questa fase, vengono installate le dipendenze necessarie per il progetto, come prospector e bandit per la verifica del codice, setuptools e wheel per la creazione del pacchetto, e strumenti come twine (per il rilascio su PyPI) e mkdocs (per la documentazione).
## Verify
In questa fase, vengono eseguite delle verifiche di sicurezza e qualità sul codice con bandit (analisi di vulnerabilità) e prospector (analisi di qualità del codice).
## Test
In questa fase, vengono eseguiti i test automatici usando pytest. Prima di eseguire i test, pytest viene installato nell'ambiente virtuale.
## Package
La fase di pacchettizzazione crea il pacchetto del progetto (usando il modulo build di Python). I file generati vengono poi salvati come artefatti (nella directory dist/), che saranno usati nelle fasi successive.
## Release
Qui, il pacchetto creato viene caricato su PyPI usando twine. Il token di autenticazione necessario per il caricamento è fornito come variabile d'ambiente $PYPI_TOKEN.
## Docs 
In questa fase, viene costruita la documentazione con mkdocs e quindi copiata nella directory public/, che viene registrata come artefatto, consentendo di consultare la documentazione generata.


