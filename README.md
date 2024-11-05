# Projeto de Recomendação de Filmes e Séries via gRPC

Este projeto implementa um sistema de recomendação de filmes e séries utilizando gRPC para comunicação entre cliente e servidor. O servidor consulta a API do The Movie Database (TMDB) para fornecer recomendações com base nos critérios especificados pelo usuário.

## Pré-requisitos

- **Python 3.7** ou superior
- **Pip** (gerenciador de pacotes do Python)
- **Conta na [TMDB](https://www.themoviedb.org/)** para obter uma chave de API
- **Conexão com a internet** para acessar a API TMDB

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. **Crie um ambiente virtual** (opcional, mas recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use venv\Scripts\activate

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt


4. **Configuração da API TMDB**

   - **Obtenha uma chave de API:**
     - Crie uma conta em TMDB.
     - Navegue até as configurações da conta e obtenha uma chave de API.

   - **Configure a chave de API no projeto:**
     - No arquivo `servidor.py`, localize a linha:
       ```python
       TMDB_API_KEY = '88a14d3ae04de73aab3f3e8f1695c3b3'
       ```
     - Substitua o valor pela sua chave de API obtida no passo anterior.
     - **Importante:** Não compartilhe sua chave de API publicamente.

## Executando o Servidor

- **Inicie o servidor gRPC:**

   ```bash
   python servidor.py

   O servidor estará escutando na porta 50051. Certifique-se de que essa porta está disponível e não está bloqueada por firewall.

## Executando o Cliente

- **Configure o endereço do servidor (se necessário):**
  - No arquivo `cliente.py`, verifique a linha:
    ```python
    with grpc.insecure_channel('192.168.207.102:50051') as channel:
    ```
  - Substitua `'192.168.207.102'` pelo endereço IP onde o servidor está sendo executado. Se estiver executando localmente, use `'localhost'` ou `'127.0.0.1'`.

- **Execute o cliente:**

   ```bash
   python cliente.py
   O cliente solicitará informações para a recomendação:
   - Tipo: `'filme'` ou `'série'`
   - Gênero: ex. `'Ação'`, `'Comédia'`, `'Drama'`
   - Ano de lançamento: ex. `2022`
   - Nota mínima: de `0.0` a `10.0`

   Após inserir os dados, o cliente exibirá uma lista de até 5 recomendações com base nos critérios fornecidos.

## Funcionamento

- **Servidor (`servidor.py`):**
  - Implementa um serviço gRPC que recebe solicitações de recomendação.
  - Consulta a API TMDB para obter filmes ou séries que correspondam aos critérios.
  - Retorna uma lista de títulos recomendados.

- **Cliente (`cliente.py`):**
  - Solicita ao usuário os critérios para a recomendação.
  - Envia uma requisição ao servidor gRPC com os dados fornecidos.
  - Recebe e exibe as recomendações ao usuário.

## Possíveis Erros e Soluções

- **Erro:** "A chave da API TMDB não foi definida no ambiente."
  - Verifique se a chave da API TMDB foi configurada corretamente no `servidor.py`.

- **Erro de conexão:**
  - Certifique-se de que o servidor está em execução e o endereço IP e porta no `cliente.py` estão corretos.
  - Verifique se não há firewall bloqueando a porta 50051.

- **Nenhuma recomendação encontrada:**
  - Pode ocorrer se não houver filmes ou séries que correspondam exatamente aos critérios especificados.
  - Tente ajustar os critérios (por exemplo, usar um ano diferente ou uma nota mínima menor).

- **Gênero não encontrado:**
  - Verifique se o gênero digitado é válido e corresponde aos gêneros disponíveis na TMDB.
  - Alguns gêneros comuns:
    - Ação
    - Comédia
    - Drama
    - Ficção científica
