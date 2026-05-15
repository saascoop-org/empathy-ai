# Implementation Backlog

Checklist de pendencias de implementacao em ordem de precedencia. A ordem considera dependencias tecnicas, risco de seguranca/privacidade e impacto na manutencao.

## P0 - Contratos, Configuracao E Base De Qualidade

- [x] Criar schemas Pydantic para entrada do usuario, metadados de idioma, saida de cada agente, resultado final do workflow e registros persistidos.
- [x] Substituir `dict`s soltos entre agentes por contratos tipados.
- [x] Definir uma camada de configuracao central para variaveis de ambiente:
  - [x] `OLLAMA_BASE_URL`.
  - [x] `GEMMA_MODEL`.
  - [x] `INTERACTION_DB_PATH`.
  - [x] `DEFAULT_UI_LANGUAGE`.
  - [x] `PROCESSING_LANGUAGE`.
- [x] Validar configuracoes na inicializacao e expor erros claros para ambiente invalido.
- [x] Fixar versoes das dependencias ou migrar para `pyproject.toml`.
- [x] Criar specs de prompts versionadas para cada chamada LLM.

## P1 - Seguranca, Safety E Privacidade

- [x] Transformar regras de safety em uma politica explicita versionada.
- [x] Expandir `BiasSafetyAgent` para cobrir:
  - [x] diagnostico ou rotulo clinico.
  - [x] culpabilizacao.
  - [x] normalizacao comportamental.
  - [x] linguagem patologizante.
  - [x] assedio, abuso ou risco emocional.
  - [x] pedidos fora do escopo da ferramenta.
- [x] Criar testes negativos para respostas que nao devem ser emitidas.
- [x] Melhorar anonimização para reduzir falsos positivos e falsos negativos.
- [x] Separar anonimização para processamento de anonimização para persistência, caso os requisitos diverjam.
- [x] Documentar limites da anonimização atual como risco conhecido.
- [x] Garantir logging estruturado sem texto bruto do usuário.
- [x] Adicionar política de retenção e exclusão de dados locais.

## P2 - Arquitetura De Aplicacao

- [x] Separar responsabilidades hoje concentradas na UI:
  - [x] caso de uso de análise de interação.
  - [x] presenter/localizer de saída.
  - [x] repositório de persistência.
  - [x] gateway de LLM.
- [x] Criar uma camada `services/` ou `use_cases/` para coordenar workflow, localização e persistência.
- [x] Manter `app/streamlit_app.py` apenas como camada de apresentação.
- [x] Criar interfaces/portas para LLM e storage para facilitar testes.
- [x] Padronizar tratamento de erros de workflow, LLM, storage e configuração.
- [x] Remover duplicação entre localização da UI e localização dos resultados.

## P3 - Multilingue E Saida Localizada

- [x] Separar traduções da UI em arquivos por idioma.
- [x] Criar validação automática de cobertura das chaves de tradução.
- [x] Implementar fallback de chave ausente para EN.
- [x] Criar uma etapa explícita de tradução/pós-processamento da saída do LLM.
- [x] Validar que a resposta final do LLM está no idioma selecionado.
- [x] Melhorar detecção de idioma com estratégia mais confiável ou modelo local leve.
- [x] Registrar idioma detectado, idioma de processamento e idioma de saída em todos os resultados.

## P4 - Persistência E Dados Locais

- [x] Adicionar métodos de leitura, listagem e exclusão ao `InteractionStore`.
- [x] Implementar exclusão de registros pelo usuário.
- [x] Implementar limpeza total dos dados locais pela interface.
- [x] Adicionar migrações ou controle de versão do schema SQLite.
- [x] Adicionar testes para leitura, exclusão e migração.
- [x] Definir se feedback deve ser normalizado em enum.
- [x] Garantir que nenhum dado bruto seja persistido em `result_json`.

## P5 - Testes E Validação

- [x] Separar testes por domínio:
  - [x] `tests/test_workflow.py`.
  - [x] `tests/test_i18n.py`.
  - [x] `tests/test_safety.py`.
  - [x] `tests/test_privacy.py`.
  - [x] `tests/test_storage.py`.
  - [x] `tests/test_llm_runtime.py`.
- [x] Adicionar testes de integração da UI ou smoke test de renderização Streamlit.
- [x] Adicionar testes para consentimento ligado/desligado.
- [x] Adicionar testes de idioma de saída para PT-BR, EN e ES.
- [x] Adicionar testes de timeout, modelo ausente e resposta vazia do Ollama.
- [x] Adicionar fixtures realistas sem dados pessoais reais.
- [x] Criar matriz de cenários de aceitação baseada nas specs.

## P6 - Observabilidade E Operação

- [x] Adicionar logging estruturado com redacao de dados sensíveis.
- [x] Medir tempo de execução por etapa do workflow.
- [x] Registrar quando fallback do LLM for usado.
- [x] Adicionar tela ou seção de status local:
  - [x] modelo configurado.
  - [x] status do Ollama.
  - [x] idioma de processamento.
  - [x] caminho do banco local.
- [x] Criar scripts operacionais:
  - [x] verificar ambiente.
  - [x] rodar smoke test.
  - [x] limpar banco local.

## P7 - CI, Empacotamento E Higiene Do Repositorio

- [ ] Criar `pyproject.toml` com metadata, dependências e ferramentas.
- [ ] Adicionar formatador e linter.
- [ ] Adicionar GitHub Actions para:
  - [ ] instalar dependências.
  - [ ] rodar testes.
  - [ ] rodar smoke test sem LLM.
  - [ ] validar specs/documentação mínima.
- [ ] Adicionar política de branches/PRs no README ou docs.
- [ ] Decidir destino de `Empathy_description.pdf`:
  - [ ] versionar se for documento oficial necessário.
  - [ ] mover para storage externo se for artefato grande.
  - [ ] ignorar se for apenas referência local.

## P8 - Funcionalidades Pós-Demo

- [ ] Reavaliar integração com ChromaDB somente com caso de uso claro de recuperação semântica.
- [ ] Definir política de privacidade específica para embeddings antes de ativar ChromaDB.
- [ ] Considerar LangGraph se o workflow passar a ter branches, retries ou estados condicionais.
- [ ] Adicionar painel de histórico consentido com busca e exclusão.
- [ ] Adicionar exportação local de registros anonimizados, se houver necessidade real.

## Critério De Pronto Para Próxima Fase

- [x] Workflow tipado com Pydantic.
- [x] Safety policy versionada e testada.
- [x] UI desacoplada da orquestração de caso de uso.
- [x] Persistência com leitura e exclusão consentida.
- [x] Saída localizada validada automaticamente.
- [x] Testes organizados por domínio.
- [ ] CI mínimo rodando em PR.
