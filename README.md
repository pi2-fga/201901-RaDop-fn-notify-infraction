# FN-Notify-Infraction

A **Função Notify Infraction** é a função responsável por receber as informações da infração e do veículo e notificar aos usuários do RaDop a informação.

## Parâmetros

Os parâmetros da função fn-notify-infraction seguem o modelo de dados do pacote (_package_) de mensagens da arquitetura do sistema do radar. Eles consistem em um objeto JSON com o seguinte formato:

- **id**: Um UUID para identificar unicamente aquele pacote (tipo `string`).

- **type**: Qual o tipo da chamada de função, para que a função possa identificar se o pacote que ele recebeu é do seu domínio. Para a função Notify Feasible só serão aceitos pacotes com a chave `notify-feasible-call` (tipo `string`).

- **payload**: Será um outro objeto JSON com o conteúdo da mensagem (tipo `dict`).

    - **infraction_id**: Identificador da infração no formato UUID (tipo `string`).

    - **infraction-data**: Objeto JSON com as informações de infração (tipo `dict`).

        - **considered_speed**: Valor da velocidade considerada na infração (tipo `integer`)

        - **id_radar**: Identificador do radar que capturou a infração (tipo `integer`)

        - **infraction**: Domínio que identifica a gravidade da infração (tipo `integer`)

        - **max_allowed_speed**: Valor da velocidade máxima da via (tipo `integer`)

        - **vehicle_speed**: Valor da velocidade capturada do veículo (tipo `integer`)

    - **vehicle-data**: Objeto JSON com as informações do veículo da infração (tipo `dict`).

        - **brand**: Marca do veículo (tipo `string`)

        - **chassis**: Inicial da chassi do veículo (tipo `string`)

        - **city**: Cidade de registro do veículo (tipo `string`)

        - **color**: Cor do veículo (tipo `string`)

        - **date**: Data e hora da verificação do veículo e da infração (tipo `string`)

        - **model**: Modelo do veículo (tipo `string`)

        - **model_year**: Ano do modelo do veículo (tipo `string`)

        - **year**: Ano de fabricação do veículo (tipo `string`)

        - **plate**: Placa do veículo (tipo `string`)

        - **state**: Estado de registro do veículo (tipo `string`)

        - **return_code**: Código de retorno da verificação (tipo `string`)

        - **status_code**: Código da situação veículo (tipo `string`)

        - **status_message**: Mensagem da situação do veículo (tipo `string`)

- **time**: O dia e horário em que essa mensagem foi enviado no formato RFC3339, ou seja, `YYYY-MM-DDTHH:MM:SSZ` (tipo `string`).

__Exemplo__:

```json
{
  "id": "e7a62db3-4b36-4573-b688-23317174b40e",
  "payload": {
    "infraction_id": "34e221bf-1f0a-4439-b9bf-4f5f23e16230",
    "infraction-data": {
      "considered_speed": 77,
      "id_radar": 42,
      "infraction": 2,
      "max_allowed_speed": 60,
      "vehicle_speed": 80
    },
    "vehicle-data": {
      "brand": "FIAT/FIORINO 1.0",
      "chassis": "41647",
      "city": "RIACHAO DO JACUIPE",
      "color": "Branca",
      "date": "15/06/2019 às 14:36:42",
      "model": "FIAT/FIORINO 1.0",
      "model_year": "1994",
      "plate": "JMA1451",
      "return_code": "0",
      "return_message": "Sem erros.",
      "state": "BA",
      "status_code": "0",
      "status_message": "Sem restrição",
      "year": "1994"
    }
  },
  "time": "2019-06-15T17:36:43.702105Z",
  "type": "notify-infraction-call"
}
```

## Tecnologias Utilizadas

- Plataforma OpenFaaS
    - _Self-Hosted_ Function as a Service
- Python 3
- JSON

## Ambiente de Desenvolvimento

Recomendado o uso de OpenFaaS local em Docker Swarm.

O guia para criar o ambiente local está disponível [na seção de _Deployment_ da documentação do OpenFaaS](http://docs.openfaas.com/deployment/docker-swarm/).

Editor de texto de preferência.

## Ambiente de Teste Local

Recomendados a utilização de um ambiente virtual criado pelo módulo `virtualenvwrapper`.
Existe um sítio virtual com instruções em inglês para a instalação que pode ser acessado [aqui](https://virtualenvwrapper.readthedocs.io/en/latest/install.html). Mas você pode também seguir o roteiro abaixo para a instalação do ambiente:

```shell
python3 -m pip install -U pip # Faz a atualização do pip
python3 -m pip install virtualenvwrapper # Caso queira instalar apenas para o usuário use a opt --user
```

Agora configure o seu shell para utilizar o virtualenvwrapper, adicionando essas duas linhas ao arquivo de inicialização do seu shell (`.bashrc`, `.profile`, etc.)

```shell
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

Caso queira adicionar um local específico de projeto basta adicionar uma terceira linha com o seguinte `export`:

```shell
export PROJECT_HOME=/path/to/project
```

Execute o arquivo de inicialização do shell para que as mudanças surtam efeito, por exemplo:

```shell
source ~/.bashrc
```

Agora crie um ambiente virtual com o seguinte comando (colocando o nome que deseja para o ambiente), neste exemplo usarei o nome composta:

```shell
mkvirtualenv fn-notify-infraction
```

Para utilizá-lo:

```shell
workon fn-notify-infraction
pip install -r compiler/requirements.txt # Irá instalar todas as dependências usadas no projeto
```

**OBS**: Caso o sua variável de ambiente *PROJECT_HOME* esteja _setada_ ao executar o `workon` você será levado para o diretório lá configurado.

Para outras configurações e documentação adicional acesse a página do [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).

## Deploy Local para Desenvolvimento

Para deploy da função, basta seguir o roteiro abaixo:

```shell
faas build -f fn-notify-infraction.yml
faas deploy -f fn-notify-infraction.yml
```

Para utilizá-lo, teste pela interface web no endereço definido, chamar pela CLI, ou por requisição HTTP:

FaaS CLI:

```shell
echo $'{\n  "id": "e7a62db3-4b36-4573-b688-23317174b40e",\n  "payload": {\n    "infraction_id": "34e221bf-1f0a-4439-b9bf-4f5f23e16230",\n    "infraction-data": {\n      "considered_speed": 77,\n      "id_radar": 42,\n      "infraction": 2,\n      "max_allowed_speed": 60,\n      "vehicle_speed": 80\n    },\n    "vehicle-data": {\n      "brand": "FIAT/FIORINO 1.0",\n      "chassis": "41647",\n      "city": "RIACHAO DO JACUIPE",\n      "color": "Branca",\n      "date": "15/06/2019 às 14:36:42",\n      "model": "FIAT/FIORINO 1.0",\n      "model_year": "1994",\n      "plate": "JMA1451",\n      "return_code": "0",\n      "return_message": "Sem erros.",\n      "state": "BA",\n      "status_code": "0",\n      "status_message": "Sem restrição",\n      "year": "1994"\n    }\n  },\n  "time": "2019-06-15T17:36:43.702105Z",\n  "type": "notify-infraction-call"\n}' | faas-cli invoke fn-notify-infraction
```

HTTP-Request:

```shell
curl -d $'{\n  "id": "e7a62db3-4b36-4573-b688-23317174b40e",\n  "payload": {\n    "infraction_id": "34e221bf-1f0a-4439-b9bf-4f5f23e16230",\n    "infraction-data": {\n      "considered_speed": 77,\n      "id_radar": 42,\n      "infraction": 2,\n      "max_allowed_speed": 60,\n      "vehicle_speed": 80\n    },\n    "vehicle-data": {\n      "brand": "FIAT/FIORINO 1.0",\n      "chassis": "41647",\n      "city": "RIACHAO DO JACUIPE",\n      "color": "Branca",\n      "date": "15/06/2019 às 14:36:42",\n      "model": "FIAT/FIORINO 1.0",\n      "model_year": "1994",\n      "plate": "JMA1451",\n      "return_code": "0",\n      "return_message": "Sem erros.",\n      "state": "BA",\n      "status_code": "0",\n      "status_message": "Sem restrição",\n      "year": "1994"\n    }\n  },\n  "time": "2019-06-15T17:36:43.702105Z",\n  "type": "notify-infraction-call"\n}' -X POST http://127.0.0.1:8080/function/fn-notify-infraction
```

Exemplo de saída:

```shell
{'status_code': 200, 'message': 'A  infração e7a62db3-4b36-4573-b688-23317174b40e (ID) será notificada. O identificador da notificação é 24f4eef2-0417-48d0-a580-eafedb759b27', 'infraction': {'infraction_identifier': '34e221bf-1f0a-4439-b9bf-4f5f23e16230', 'allowed_track_speed': 60, 'read_speed': 80, 'considered_speed': 77, 'penalty': {'level': 'Gravíssima', 'value': 880.41, 'points': 7}, 'date': '15/06/2019', 'time': '14:36:42', 'vehicle_brand': 'FIAT', 'vehicle_model': 'FIORINO 1.0', 'vehicle_year': '1994', 'vehicle_chassi': '41647', 'vehicle_color': 'Branca', 'vehicle_plate': 'JMA1451', 'vehicle_city': 'RIACHAO DO JACUIPE', 'vehicle_state': 'BA', 'vehicle_status': 'Sem restrição'}}
```

## Execução do Ambiente de Testes

Para executar os testes do fn-notify-infraction siga o roteiro descrito abaixo:

Primeiro assegure-se de que tem todas as dependências necessárias para executar o projeto.

```shell
pip install -r fn-notify-infraction/requirements.txt
# Ou caso não esteja trabalhando com uma virtualenv
python3 -m pip install -r fn-notify-infraction/requirements.txt
```

**OBS**: Caso queria instalar apenas para o usuário e não no sistema use a opt `--user` ao final do comando pip.

Agora que todas as dependências estão instaladas basta rodar o comando do pytest para verificar se o código está de acordo com o teste.

```shell
pytest fn-notify-infraction/ # Executa os testes no pytest
py.test --cov=fn-notify-infraction fn-notify-infraction/ # Executa os testes e avalia a cobertura estática de código
py.test --cov=fn-notify-infraction --cov-report html fn-notify-infraction/ # Faz o mesmo papel que o comando anterior, além de gerar uma pasta htmlcov/ com uma página relatório da cobertura
flake8 fn-notify-infraction/* # Executa o PEP8 linter nos arquivos python
```

Durante o `pytest` e o `py.test`, o terminal lhe apresentará um _output_ com o relatório dos testes e a cobertura de testes da aplicação. Para outras configuraões e documentação complementar acesse o sítio virtual do provedor do [pytest](https://docs.pytest.org/en/latest/) e do [coverage](https://pytest-cov.readthedocs.io/en/latest/).

Durante o `flake8`, o terminal lhe apresentará um relatório com os erros e _warnings_ do guia de estilo PEP8 do python, para demais configurações e documentações você pode acessar o sítio do [flake8](http://flake8.pycqa.org/en/latest/index.html) ou visualizar o estilo do [PEP8](https://www.python.org/dev/peps/pep-0008/).
