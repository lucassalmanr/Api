# Documentação da API de Licenciamento (Integração AKASHA)

Esta é uma API desenvolvida em **FastAPI** que atua como uma interface (middleware) de comunicação com a API principal do ecossistema AKASHA. Ela é responsável por simplificar a comunicação com a API externa e fornecer rotas acessíveis para gerenciar empreendimentos, enviar de formulários + documentos, e obter classificações de Inteligência Artificial para licenciamento.

## Sumário
- [Configurações Gerais](#configurações-gerais)
- [Modelos de Dados (Schemas)](#modelos-de-dados-schemas)
- [Endpoints](#endpoints)

---

## Configurações Gerais
- **URL Base Padrão**: As rotas possuem o prefixo fundamental `/api/v1/licenciamento`.
- **CORS**: A API está com o middleware CORS para permitir requisições de qualquer origem (`["*"]`), bem como todos os métodos HTTP e cabeçalhos.
- **Autenticação com a API AKASHA**: Realizada através do envio do cabeçalho `x-api-key`, fornecido na comunicação pelo `LicensingClient`.

---

## Modelos de Dados (Schemas)

A API utiliza a biblioteca Pydantic para validação das estruturas JSON enviadas no corpo das requisições:

### `DevelopmentCreateRequest`
Utilizado para realizar o cadastro e envio na rota principal de criação.
- `name` *(string)*: Nome do empreendimento a ser criado.
- `description` *(string)*: Breve descrição das utilidades/atividades do empreendimento.
- `e_ia` *(boolean)*: Sinaliza a intenção de auxílio via inteligência artificial.

### `Classification`
Utilizado para processar e solicitar a análise de licenciamento pela Inteligência Artificial.
- `development_id` *(int)*: ID numérico com o número do empreendimento já registrado.

### `EmpreendimentoRequest` / `EmpreendimentoResponse`
Modelos exclusivos para realizar rápidos fluxos de teste (mocks) em rotas locais antes da integração ou subida para produção.

---

## Endpoints

### 1. Healthcheck Simplificado
**`GET /api/v1/licenciamento/health`**
Verifica a disponibilidade da infraestrutura do middleware de FastAPI.

- **Resposta de Sucesso (200 OK):**
  ```json
  {
    "status": "ok"
  }
  ```

---

### 2. Criar Empreendimento
**`POST /api/v1/licenciamento/criar-empreendimento`**
Recebe as informações básicas e cadastra um novo empreendimento na API oficial do AKASHA (`/api/licensing/developments`).

- **Corpo da Requisição (JSON):**
  Corresponde ao Payload do Schema `DevelopmentCreateRequest`.
  ```json
  {
      "name": "Meu Empreendimento",
      "description": "Indústria Madeireira Local",
      "e_ia": true
  }
  ```
- **Resposta de Sucesso (Exemplo):**
  Retorna um resumo dos dados registrados em conjunto com seu novo ID externo.
  ```json
  {
      "name": "Meu Empreendimento",
      "description": "Indústria Madeireira Local",
      "id": 169
  }
  ```
- **Tratamento de Erros:** O FastAPI interceptará erros da API do AKASHA como `401 Unauthorized`, `422 Unprocessable Entity` ou `500 Server Error` devolvendo as devidas exceções tratadas de ambiente para o Frontend.

---

### 3. Classificar Empreendimento via Inteligência Artificial
**`POST /api/v1/licenciamento/api/licensing/ai/classify/full`**
Notifica a inteligência artificial do AKASHA a buscar os dados e processar em que estágio de licenciamento a atividade do `development_id` se enquadra. Retorna uma ficha técnica que é salva em diretório.

- **Corpo da Requisição (JSON):**
  ```json
  {
      "development_id": 169
  }
  ```
- **Ações Internas (I/O)**: O objeto resultante da classificação da API é reestruturando e salvo integralmente como backup e base rápida na pasta interna `app/data/data{id}.json`.
- **Resposta de Sucesso (Tratada):** Retorna a tradução da IA indicando dados de enquadramento.
  ```json
  {
      "group": "Exemplo Grupo X",
      "activity": "Exemplo Atividade XYZ",
      "criterios": "Mais de 1000m² - Uso de fornos",
      "porte": "M",
      "modalidade": "Licença Simplificada"
  }
  ```

---

### 4. Recebimento e Envio de Documentos (Forms)
**`POST /api/v1/licenciamento/forms`**
Coleta dados complexos e envio de documentações (Anexos em bytes/pdf) juntamente com parâmetros que complementam as diretrizes do empreendimento.
A requisição é do tipo `multipart/form-data`, diferente dos JSONs de outras rotas.

- **Campos (Form-Data):**
  - **`development_id`** (Número / Texto Simples): Referência ao empreendimento.
  - **`user_input`** (Texto Simples): Informações inseridas em texto complementar pelo usuário.
  - **`e_ai`** (Booleano): Opção se a IA participa também neste formulário.
  - **`document`** (Arquivo / UploadFile): Documento que passará por Upload (Ex: Comprovante .pdf, Imagem).

- **Resposta:**
  Retorna o payload bruto de submissão do documento repassado pela rota do AKASHA.

---

### 5. Mockup / Ambientes de Teste
**`POST /api/v1/licenciamento/empreendimentos-teste`**
Rota dedicada a simular a resposta de um serviço interno com processamentos rápidos puramente processados no `LicensingService`.
Retorna uma mensagem de validações de processamento confirmando a estrutura `EmpreendimentoRequest -> EmpreendimentoResponse`.
