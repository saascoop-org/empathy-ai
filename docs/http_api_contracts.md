# Contratos HTTP Para Evolucao Pos-Demo

Estes contratos documentam a separacao futura entre interface, API Python e engine de analise. Eles servem como base para uma migracao incremental para FastAPI sem alterar o fluxo demonstrativo atual em Streamlit.

## POST /api/analysis

Executa uma analise de interacao com contexto opcional do Mapa de Alteridade.

### Request

```json
{
  "interaction": "Minha colega esta passando informacoes do projeto de forma confusa.",
  "output_language": "auto",
  "store_consent": true,
  "feedback": "partially_useful",
  "alterity_map": {
    "user_profile": "costumo ser direto e literal quando estou sob pressao",
    "other_profile": "pode esperar mais contexto e validacao",
    "context_factors": "projeto atrasado",
    "repair_supports": "entender a expectativa e combinar proximo passo"
  }
}
```

### Response

```json
{
  "analysis_id": 12,
  "stored_record_id": 7,
  "language": {
    "user_language": "pt-BR",
    "processing_language": "en",
    "output_language": "pt-BR"
  },
  "context": {
    "interaction_summary": "A troca envolve informacoes de projeto percebidas como confusas."
  },
  "translation": {
    "translation_for_user": "A outra pessoa talvez nao perceba quais detalhes estao pouco claros.",
    "translation_for_other_person": "O usuario pode precisar de prioridades e proximos passos."
  },
  "response": {
    "bridge_message": "Voce poderia compartilhar o que esta mais incerto para alinharmos prioridade, prazo e proximo passo?"
  },
  "learning": {
    "reflection_question": "Qual informacao precisa ser esclarecida primeiro?"
  },
  "safety": {
    "safe": true,
    "guidance": "Apoio comunicacional, nao aconselhamento especializado."
  }
}
```

## GET /api/diary

Lista registros locais consentidos.

### Query Params

- `limit`: numero maximo de registros.
- `query`: termo opcional para busca em interacao, ponte ou reflexao.
- `language`: idioma de exibicao.

### Response

```json
{
  "items": [
    {
      "id": 7,
      "created_at": "2026-05-16T16:32:00-03:00",
      "title": "colega esta passando informacoes do projeto - 16/05/2026 16:32",
      "interaction": "colega esta passando informacoes do projeto de forma confusa",
      "bridge": "Voce poderia compartilhar o que esta mais incerto?",
      "reflection_question": "Qual informacao precisa ser esclarecida primeiro?",
      "feedback": "Parcialmente util"
    }
  ]
}
```

## DELETE /api/diary/{record_id}

Remove um registro local consentido.

### Response

```json
{
  "deleted": true,
  "record_id": 7
}
```

## POST /api/audio/transcription

Recebe audio temporario, transcreve e retorna texto para revisao antes da analise.

### Request

`multipart/form-data`

- `audio`: arquivo de audio gravado no navegador.
- `language_hint`: idioma opcional.

### Response

```json
{
  "transcript": "Meu chefe foi direto no chat e eu respondi curto porque o projeto esta atrasado.",
  "detected_language": "pt-BR",
  "retention": "discarded_after_processing"
}
```

## POST /api/audio/extract-alterity-map

Extrai rascunhos editaveis para preencher o Mapa de Alteridade.

### Request

```json
{
  "transcript": "Meu chefe foi direto no chat e eu respondi curto porque o projeto esta atrasado.",
  "output_language": "pt-BR"
}
```

### Response

```json
{
  "interaction": "Meu chefe foi direto no chat e eu respondi curto.",
  "alterity_map": {
    "user_profile": "tende a ser direto quando ha pressao de prazo",
    "other_profile": "pode esperar mais contexto ou alinhamento",
    "context_factors": "projeto atrasado; conversa por chat",
    "repair_supports": "explicar intencao e perguntar qual informacao falta"
  },
  "requires_manual_review": true
}
```
