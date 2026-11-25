import os
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "Variável GEMINI_API_KEY não encontrada. Configure seu arquivo .env antes de iniciar a API."
    )

# Inicializa o cliente usando a chave carregada do ambiente (.env ou variável do sistema)
client = genai.Client(api_key=api_key)

app = FastAPI(
    title="KODIE - API de Classificação de Mensagens",
    description="API em FastAPI integrada ao Gemini para classificar mensagens e direcionar para setores.",
    version="1.0.0",
)


class MensagemRequest(BaseModel):
    mensagem: str = Field(
        ...,
        min_length=1,
        description="Texto enviado pelo cliente para classificação.",
    )


class ClassificacaoResponse(BaseModel):
    categoria: Literal["Dúvida", "Solicitação", "Reclamação"]
    urgencia: Literal["Baixa", "Média", "Alta"]
    setor_destino: Literal["Suporte Técnico", "Financeiro", "Comercial"]
    resumo: str = Field(
        ...,
        description="Resumo objetivo da mensagem em até uma frase.",
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/classificar", response_model=ClassificacaoResponse)
def classificar_mensagem(payload: MensagemRequest):
    prompt = f"""
Você é um assistente de triagem de atendimento para uma empresa.
Analise a mensagem do cliente e devolva exclusivamente o JSON estruturado conforme o schema solicitado.

Regras de classificação:
- categoria:
  * "Dúvida": perguntas sobre funcionamento, prazos, regras ou informações gerais.
  * "Solicitação": pedidos de ação, alteração, envio, liberação ou atualização.
  * "Reclamação": relatos de problema, insatisfação, falha, cobrança indevida ou bloqueio.
- urgencia:
  * "Baixa": dúvida comum ou solicitação sem impacto imediato.
  * "Média": necessidade operacional importante mas sem bloqueio crítico ou perda financeira imediata.
  * "Alta": conta bloqueada, pagamento não reconhecido após cobrança, falha crítica ou risco alto de cancelamento.
- setor_destino:
  * "Financeiro": boletos, pagamentos, faturas, cobranças, reembolsos, planos/cobrança.
  * "Suporte Técnico": login, acesso, bugs, erros no sistema, integrações, falhas técnicas.
  * "Comercial": contratação, upgrades, descontos, propostas, informações de venda.
- resumo: escreva uma frase curta e objetiva resumindo o pedido ou problema.

Mensagem do cliente:
\"\"\"{payload.mensagem}\"\"\"
"""

    try:
        response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ClassificacaoResponse,
    ),
)

        if not response.text:
            raise ValueError("A resposta da API Gemini veio vazia.")

        return ClassificacaoResponse.model_validate_json(response.text)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Falha ao processar a classificação com a Gemini API: {exc}",
        ) from exc