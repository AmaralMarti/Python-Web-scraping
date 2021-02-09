# Python-Web-scraping

## Preparação do ambiente

Os passos a seguir são para um ambiente Linux com o Python 3.8 instalado;
#### IMPORTANTE: **_Se vc está usando Windows esses passos serão diferentes, mas não é difícil adequar se você entendê-los._**

### A - O Virtual Environment

O ambiente virtual é um ambiente Python isolado para o seu projeto, ele é independente do ambiente Python global do seu computador. As dependências que 
você instalar com o "pip" ficarão restritas ao seu projeto. Mais detalhes você pode encontrar na documentação: https://docs.python.org/pt-br/3/library/venv.html

**1. Criar o ambiente virtual**

Abra o terminal e vá até o diretório do repositório, então digite o comando abaixo. Depois da execução você vai reparar que um novo diretório chamado "venv" vai
aparecer dentro do diretório do seu projeto, esse é o diretório onde fica o seu venv.

```
python -m venv ./venv
```

**2. Ativar o ambiente virtual**

Depois que criar o ambiente virtual é preciso ativá-lo, isso vai fazer com que você passe a usar o seu ambiente virtual Python em vez de usar o ambiente global 
Python do seu computador.

Ainda no terminal, na raiz do seu projeto, digite o comando abaixo. Depois da execução do comando você vai reparar que o seu terminal vai mudar indicando que você
agora está com o "venv" ativado

```
source ./venv/bin/activate
```

**3. Instalando as dependências**

Agora que você tem um ambiente virtual e já está com ele ativado, vamos instalar as dependências do projeto nele. Essas dependências estão no arquivo
"requirements.txt".

Novamente no terminal, na raiz do projeto, digite o comando:

```
pip install -r requirements.txt
```

### B - Rodando o teste

Depois do amviente preparado nós vamos rodar o teste.

**1. Teste no modo síncrono (modo normal)**

O modo síncrono é aquele em que cada uma das instruções é executada por vez, ou seja, a aplicação só vai para a instrução seguinte depois que a instrução atual
estiver concluida. Esse é o modo normal, mas para esse teste isso pode ser lento já que cada requisição pro site do Github é um pouco lenta. Para repositórios
grandes isso pode ser muito demorado, chegando a mais de 1 hora de execução.

No terminal, estando na raiz do projeto execute:

```
python teste.py
```

**2. Teste no modo assíncrono (é uma tentativa e está longe de estar pronto)**

O modo assíncrono vai criar uma thread para cada requisição, o que vai permitir que várias requisições ao Github sejam feitas ao mesmo tempo. Claro que isso vai
agilizar a execução, mas vai trazer alguns contratempos que precisam ser resolvidos, tais como:

- O Github permite até 5000 requisições por hora (o que dá mais ou mento 0,83 requisições por segundo), depois disso ele vai retornar 429 (too many requests)
  e seu código vai quebrar. É preciso tratar isso de forma adequada, eu fiz uma grambiarra pra ficar reenviando a request, mas não está muito eficiente e o 
  correto é controlar o número de requisições que são enviados por segundo.
  
- Com muitas threads ao mesmo tempo a aplicação se perde as vezes. É preciso tratar isso e talvez esse tratamento tenha ligação com o tratamento do problema 
  anterior.
  

No terminal, estando na raiz do projeto execute:

```
python teste-thread.py
```
