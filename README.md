# Classificação e Encaminhamento de Mensagens com IA e n8n

Projeto desenvolvido para o desafio técnico da **KODIE** (módulos de Fundamentos de IA e Automação e Agentes), integrando uma API em [FastAPI](https://fastapi.tiangolo.com/) com Inteligência Artificial ao fluxo de automação `kodie-classificacao-mensagens` no [n8n](https://n8n.io/), exposto localmente via [ngrok](https://ngrok.com/).

## Apresentação da Ideia

A ideia nasceu da necessidade de tornar o atendimento ao cliente mais ágil e organizado em empresas que recebem mensagens de texto variadas diariamente. Em vez de exigir triagem manual mensagem a mensagem para entender o assunto, a urgência e o setor responsável, o projeto combina uma API com modelo de IA e um fluxo no [n8n](https://n8n.io/) para classificar e direcionar cada ocorrência automaticamente.

## Problema Escolhido

O projeto resolve o cenário de **Classificação de Mensagens**. Uma empresa recebe mensagens de clientes com dúvidas, solicitações e reclamações, mas sem um processo padronizado para identificar o tipo de demanda, a prioridade e a área de destino, o que pode atrasar respostas e desorganizar o atendimento.

## Solução Proposta

A solução é composta por um back-end em [FastAPI](https://fastapi.tiangolo.com/) (`api/main.py`) que recebe a mensagem do cliente, aplica um `prompt` estruturado para classificar o conteúdo e retorna um JSON padronizado com `categoria`, `urgencia`, `setor_destino` (`Financeiro`, `Suporte Técnico` ou `Comercial`) e `resumo`. Na sequência, o workflow no [n8n](https://n8n.io/) (`kodie-classificacao-mensagens.json`) consome essa resposta e encaminha os dados pelo node **Switch** para os nodes de destino correspondentes.

## Tecnologias Utilizadas

* **Back-end e API:** [Python](https://www.python.org/), [FastAPI](https://fastapi.tiangolo.com/) e [Uvicorn](https://www.uvicorn.org/)
* **Inteligência Artificial:** modelo de IA integrado via API com `prompt` estruturado e resposta em formato JSON
* **Automação de Fluxos:** [n8n](https://n8n.io/) (nodes `Webhook`, `HTTP Request` e `Switch`)
* **Túnel e Testes de Endpoint:** [ngrok](https://ngrok.com/) (exposição do endpoint `/classificar` para o n8n Cloud) e [httpbin.org](https://httpbin.org/) (recebimento de `POST` nos ramos setoriais)
* **Controle de Versão:** [Git](https://git-scm.com/) e [GitHub](https://github.com)

## Funcionamento do Sistema

1. **Entrada via Webhook:** o node `Webhook1` recebe uma requisição `POST` em `/classificar-mensagem` contendo `{"mensagem": "..."}`.
2. **Chamada à API de Classificação:** o node `HTTP Request` envia um `POST` para o endpoint `/classificar` da API FastAPI repassando `={{ { "mensagem": $json.body.mensagem } }}`.
3. **Processamento com IA em JSON:** a API em [FastAPI](https://fastapi.tiangolo.com/) interpreta a mensagem conforme as regras do `prompt` e devolve um JSON estruturado com `categoria` (`Dúvida`, `Solicitação` ou `Reclamação`), `urgencia` (`Baixa`, `Média` ou `Alta`), `setor_destino` (`Financeiro`, `Suporte Técnico` ou `Comercial`) e `resumo`.
4. **Roteamento e Envio no n8n:** o node **Switch** avalia `={{ $json.setor_destino.trim() }}` nas regras de `Financeiro`, `Suporte Técnico` e `Comercial` (mantendo saída de `Fallback`) e envia os dados via `POST` para `https://httpbin.org/post` nos nodes `HTTP Request1`, `HTTP Request2` e `HTTP Request3`.

### Documentação Visual do Fluxo de Automação

A documentação visual detalhada — contendo os prints do fluxo completo, execuções bem-sucedidas nos três setores, configuração interna dos nodes e resultados de entrada (`INPUT`) e saída (`OUTPUT`) — está disponível no documento complementar:

* 📄 **[Documentação Visual do Fluxo (PDF)](docs/documentacao-fluxo.pdf)**

## Como Executar

### 1. Clonar o repositório e configurar variáveis de ambiente

```bash
git clone [https://github.com/DanielleRodrigues/desafio-kodie.git](https://github.com/DanielleRodrigues/desafio-kodie.git)
cd desafio-kodie
