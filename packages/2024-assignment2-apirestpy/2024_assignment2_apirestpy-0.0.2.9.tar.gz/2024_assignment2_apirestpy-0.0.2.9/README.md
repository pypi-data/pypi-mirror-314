# CI/CD PIPELINE

## Runner
L'immagine docker in cui sarà testa la pipeline.
``` yml
image: python:3.9-slim
```
## Defaults
Di default viene attivato l'enviromment virtuale e viene inserito come cache la cartella contenente l'enviromment con i pacchetti.
```yml
default:
  before_script:
    - source $VENV_PATH/bin/activate
  cache:
    key: pip-cache
    paths:
      - $VENV_DIR/
```
## Stages
Le fasi principali della pipeline sono: 
``` yml
stages:
  - build 
  - verify 
  - test 
  - package 
  - release_step
  - docs 
```
### Build
Consiste nella creazione dell'ambiente virtuale python e dell'installazione delle dipendenze.

#### Crezione dell'ambiente:
``` yml
 before_script:
   # Creazione ambiente virutale
   - python -m venv $VENV_PATH
   - source $VENV_PATH/bin/activate
```
#### Installazione dipendenze APP/Pipeline
``` yml
  script:
    - pip install --upgrade pip
    # installazione dependencies app
    - pip install -r requirements.txt
    # installazione deps pipeline
    - pip install mkdocs prospector bandit pytest setuptools wheel twine locust
```
Ritornando come artifacts l'ambiente virutale per mantenere i pacchetti installati attraverso i vari stages.
``` yml
  artifacts:
    paths:
      - $VENV_PATH # ambiente virtuale salvato come artifact
    expire_in: 1 day
```


### Verify 
È la fase di analisi statica e dinamica del codice.

#### Analisi statica
L'analisi statica avviene tramite gli strumenti python Prospector per la valutazione del codice e Bandit per la valutazione della sicurezza.
``` yml
 script:
    - prospector app.py
 # ...
 script:
    - bandit -r app.py
```


#### Analisi dinamica
L'analisi dinamica avviene tramite lo strumento Locust per la verifica dell'applicazione sotto un carico di utenti.
In questo caso sono settati tramite: 
```--user <numero_di_utenti> ``` 
pari a 5 utenti.
```yml
script:
    - nohup python app.py &
    - locust -f locustfile.py --host=http://127.0.0.1:5000 --headless --users 5 --spawn-rate 5 --run-time 30s --csv=locust_report --html=locust_report.html
```
Questa fase ritorna gli artifact sotto forma di file CSV e una rappresentazione grafica come pagina HTML.

```yml
  artifacts:
    paths:
      - locust_report_stats.csv
      - locust_report_failures.csv
      - locust_report_stats_history.csv
      - locust_report.html
    expire_in: 1 day
```

### Test 
In questa fase vengono svolti dei test di unità e performance tramite lo strumento pytest.
#### Test di unità
Vengono eseguiti i test del file 'test_app.py' e ritornato il risultato come XML nel formato standard JUNIT.
``` yml
  script:
    - pytest test_app.py --junit-xml=unit_test_report.xml
    - echo "Unit tests passed"
```
Il risultato è salvato come artifact e ritornato anche come reports in modo da essere caricato sulla pagina di test di GitLab.
```yml
  artifacts:
    paths:
      - ./unit_test_report.xml
    reports:
       junit: ./unit_test_report.xml
```

#### Test di performance
Vengono eseguiti i test del file 'test_performance.py' e ritornato il risultato come XML nel formato standard JUNIT.
``` yml
  script:
    - pytest test_performance.py --junit-xml=unit_test_report.xml
    - echo "Performance tests passed"
```
Il risultato è salvato come artifact e ritornato anche come reports in modo da essere caricato sulla pagina di test di GitLab.
```yml
  artifacts:
    paths:
      - ./perf_test_report.xml
    reports:
       junit: ./perf_test_report.xml 
```

### Packages
In questa fase si andrà a creare il package python.
``` yml
script:
   - python setup.py sdist bdist_wheel
```
Ritornando come artifacts la posizione del package.
Gli artifacts vengono salvati  solamente se il packaging avviene con successo e durano finchè non vengono sovrascritti.
``` yml
  artifacts:
    when: on_success
    paths:
      - ./dist/ # Posizione dei packages whl e .tar.gz
```

### Release
La fase di release svolge il release sul repository PyPi.
``` yml
  script:
    - TWINE_PASSWORD=${PYPI_TOKEN} TWINE_USERNAME=__token__ python -m twine upload dist/*
```
Questo viene svolto solamente se una commit viene taggata come release 'vx.x.x'

La release deve essere svolta nel seguente modo:
1. Aggiorna manualmente la version number nel file 'setup.py'
2. Tag della commit con il version number
Tag della commit si può fare nel seguente modo: 
``` bash
git tag -a v$(python setup.py --version) -m 'description of version'
git push origin v$(python setup.py --version)
```

### Docs 
Viene generata la documentazione su GitLab Pages della branch master. 
``` yml
  script:
  - mkdocs build --verbose
  - mv site public
```
Compilando i file nella cartella './docs':
- [./docs/api-reference.md](./docs/api-reference.md)
- [./docs/getting-started.md](./docs/getting-started.md)
- [./docs/index.md](./docs/index.md)

Fornendo in output la path dove trovare le pagine web solo in caso di successo dello stage. 
``` yml
  artifacts:
    paths:
    - public
    when: on_success
```

## Documentazione App
Il README dell'applicazione si può trovare: [./README_APP.md](./README_APP.md)




