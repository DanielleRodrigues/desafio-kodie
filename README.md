# Classificação e Encaminhamento de Mensagens com IA e n8n

Projeto desenvolvido para o desafio técnico da **KODIE** (módulos de Fundamentos de IA e Automação e Agentes), integrando uma API em [FastAPI](https://fastapi.tiangolo.com/) com Inteligência Artificial ao fluxo de automação `kodie-classificacao-mensagens` no [n8n](https://n8n.io/), exposto localmente via [ngrok](https://ngrok.com/)[cite: 1, 15, 17].

## Apresentação da Ideia

A ideia nasceu da necessidade de tornar o atendimento ao cliente mais ágil e organizado em empresas que recebem mensagens de texto variadas diariamente[cite: 1]. Em vez de exigir triagem manual mensagem a mensagem para entender o assunto, a urgência e o setor responsável, o projeto combina uma API com modelo de IA e um fluxo no [n8n](https://n8n.io/) para classificar e direcionar cada ocorrência automaticamente[cite: 1, 8, 17].

## Problema Escolhido

O projeto resolve o cenário de **Classificação de Mensagens**[cite: 1]. Uma empresa recebe mensagens de clientes com dúvidas, solicitações e reclamações, mas sem um processo padronizado para identificar o tipo de demanda, a prioridade e a área de destino, o que pode atrasar respostas e desorganizar o atendimento[cite: 1, 8].

## Solução Proposta

A solução é composta por um back-end em [FastAPI](https://fastapi.tiangolo.com/) (`api/main.py`) que recebe a mensagem do cliente, aplica um `prompt` estruturado para classificar o conteúdo e retorna um JSON padronizado com `categoria`, `urgencia`, `setor_destino` (`Financeiro`, `Suporte Técnico` ou `Comercial`) e `resumo`[cite: 1, 8, 20]. Na sequência, o workflow no [n8n](https://n8n.io/) (`kodie-classificacao-mensagens.json`) consome essa resposta e encaminha os dados pelo node **Switch** para os nodes de destino correspondentes[cite: 15, 17].

## Tecnologias Utilizadas

* **Back-end e API:** [Python](https://www.python.org/), [FastAPI](https://fastapi.tiangolo.com/) e [Uvicorn](https://www.uvicorn.org/)[cite: 1, 13]
* **Inteligência Artificial:** modelo de IA integrado via API com `prompt` estruturado e saída em JSON[cite: 1, 8]
* **Automação de Fluxos:** [n8n](https://n8n.io/) (nodes `Webhook`, `HTTP Request` e `Switch`)
* **Túnel e Testes de Endpoint:** [ngrok](https://ngrok.com/) (exposição do endpoint `/classificar` para o `n8n` Cloud) e [httpbin.org](https://httpbin.org/) (recebimento de `POST` nos ramos setoriais)
* **Controle de Versão:** [Git](https://git-scm.com/) e [GitHub](https://github.com)[cite: 1]

## Funcionamento do Sistema

1. **Entrada via Webhook:** o node `Webhook1` recebe uma requisição `POST` em `/classificar-mensagem` contendo `{"mensagem": "..."}`[cite: 15].
2. **Chamada à API de Classificação:** o node `HTTP Request` envia um `POST` para `https://curvy-liver-cider.ngrok-free.dev/classificar` repassando `={{ { "mensagem": $json.body.mensagem } }}`[cite: 15].
3. **Processamento com IA em JSON:** a API em [FastAPI](https://fastapi.tiangolo.com/) interpreta a mensagem conforme as regras do `prompt` e devolve um JSON estruturado com `categoria` (`Dúvida`, `Solicitação` ou `Reclamação`), `urgencia` (`Baixa`, `Média` ou `Alta`), `setor_destino` (`Financeiro`, `Suporte Técnico` ou `Comercial`) e `resumo`[cite: 8, 15].
4. **Roteamento e Envio no n8n:** o node **Switch** avalia `={{ $json.setor_destino.trim() }}` nas regras de `Financeiro`, `Suporte Técnico` e `Comercial` (com saída de `Fallback`) e envia os dados via `POST` para `https://httpbin.org/post` nos nodes `HTTP Request1`, `HTTP Request2` e `HTTP Request3`[cite: 15, 16].

### Documentação Visual do Fluxo de Automação

> Substitua os caminhos abaixo pelas suas capturas de ecrã reais (por exemplo, em `docs/prints/`) e mantenha uma breve descrição para cada imagem[cite: 1].

* **Fluxo completo:** `![Fluxo completo no n8n](docs/prints/fluxo-completo.png)` — Exibe todos os nodes conectados (`Webhook1`, `HTTP Request`, `Switch` e `HTTP Request1/2/3`) no workflow `kodie-classificacao-mensagens`[cite: 1, 15, 17].
* **Execução bem-sucedida:** `![Execução bem-sucedida](docs/prints/execucao-sucesso.png)` — Demonstra execuções concluídas com indicadores verdes ao longo do caminho percorrido[cite: 1, 17, 18].
* **Configuração dos nodes:** `![Configuração do Switch](docs/prints/config-switch.png)` — Mostra as regras configuradas no `Switch` para `Financeiro`, `Suporte Técnico` e `Comercial`, acompanhadas das configurações dos demais nodes[cite: 1, 16].
* **Resultados:** `![Resultados de entrada e saída](docs/prints/resultados-output.png)` — Evidencia os dados recebidos e classificados (`categoria`, `urgencia`, `setor_destino` e `resumo`) no fluxo[cite: 1, 16].

## Como Executar

### 1. Clonar o repositório e configurar variáveis de ambiente

```bash
git clone <URL_DO_SEU_REPOSITORIO_GITHUB>
cd desafio-kodie
