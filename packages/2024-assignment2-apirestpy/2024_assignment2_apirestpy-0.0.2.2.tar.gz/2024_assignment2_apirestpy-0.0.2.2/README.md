# CI/CD PIPELINE

## Runner
L'immagine docker in cui sarà testa la pipeline.
``` yml
image: python:3.9-slim
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
Consiste nela creazione dell'ambiente virtuale python e dell'installazione delle dipendenze.
``` yml
# codice
```

### Verify 
È la fase di controllo statico e dinamico del codice.
L'analisi statica avviene tramite gli strumenti python Prospector e Bandit.

``` yml
# codice
```
### Test 
In questa fase vengono svolti dei test di unità e performance tramite lo strumento pytest.
#### Test di unità
``` yml
# codice
```
#### Test di performance
``` yml
# codice
```
#### Reports
Si ottiene l'output in formato standard xml JUNIT.
``` yml
# codice
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
      - ./dist/ # Posizione dei packages whl e .tg.gz
```

### Release
La fase di release svolge il release sul repository PyPi.
``` yml
  script:
    - TWINE_PASSWORD=${PYPI_TOKEN} TWINE_USERNAME=__token__ python -m twine upload dist/*
```
Questo viene svolto solamente se una commit viene taggata come release 'vx.x.x'
``` yml
  rules: 
    # TODO
```
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




