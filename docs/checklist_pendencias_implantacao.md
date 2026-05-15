# Checklist de Pendencias de Implantacao

Este checklist organiza as pendencias por ordem de precedencia, considerando dependencias tecnicas, seguranca, privacidade e operacao da solucao.

## P0 - Bloqueadores de Implantacao

- [x] Definir o ambiente-alvo de implantacao: local demonstrativo.
- [x] Confirmar a versao do modelo Gemma disponivel no Ollama e alinhar `README.md`, `.env.example` e codigo para o mesmo identificador de modelo: `gemma4:e2b`.
- [x] Validar instalacao e inicializacao do Ollama no ambiente-alvo: `ollama list` respondeu.
- [x] Garantir que o modelo configurado em `GEMMA_MODEL` esteja baixado no Ollama antes da execucao: `gemma4:e2b` esta disponivel localmente.
- [x] Criar arquivo `.env` do ambiente a partir de `.env.example`.
- [x] Definir politica minima de segredos e variaveis de ambiente, mesmo em execucao local: `.env` foi incluido no `.gitignore`.
- [x] Executar instalacao limpa das dependencias de `requirements.txt`: pacotes essenciais validados.
- [x] Rodar a aplicacao Streamlit no ambiente-alvo e confirmar acesso a interface: `http://localhost:8501` respondeu HTTP 200.

Observacao P0: o modelo `gemma4:e2b` esta instalado, mas a chamada real falhou por memoria insuficiente no ambiente atual: o modelo exige 7.2 GiB e havia 5.4 GiB disponivel. Para a demo local, `gemma3:1b` foi baixado, configurado e validado com resposta real do Ollama. A interface possui fallback seguro quando o LLM nao responde.

## P1 - Fluxo Funcional Principal

- [x] Integrar `app/streamlit_app.py` ao `EmpathyWorkflow` em vez de exibir respostas estaticas.
- [x] Conectar o `EmpathyWorkflow` ao cliente Ollama para gerar respostas reais do modelo, com fallback quando indisponivel.
- [x] Incluir todos os agentes previstos na arquitetura dentro do pipeline de orquestracao:
  - [x] Context Decoder.
  - [x] Double Empathy Analyzer.
  - [x] Perspective Translator.
  - [x] Sensory Load Agent.
  - [x] Bias & Safety Agent.
  - [x] Response Composer.
  - [x] Learning Coach.
- [x] Padronizar o contrato de entrada e saida de cada agente no workflow atual.
- [x] Garantir que a resposta final inclua explicabilidade: contexto percebido, possiveis interpretacoes, ponte de empatia e sugestao de comunicacao.
- [x] Tratar erros de modelo indisponivel, timeout ou resposta vazia sem quebrar a interface.

## P2 - Privacidade, Consentimento e Seguranca

- [x] Implementar consentimento explicito antes de qualquer persistencia de interacoes na interface.
- [x] Aplicar anonimizacao antes de salvar ou registrar qualquer texto de usuario no workflow.
- [x] Revisar o `Anonymizer` para cobrir e-mails, telefones, nomes compostos, URLs, locais e identificadores sensiveis.
- [x] Definir quais dados podem ser armazenados, por quanto tempo e com qual finalidade.
- [x] Implementar camada de seguranca para impedir diagnostico, julgamento de certo/errado ou normalizacao comportamental.
- [x] Adicionar verificacoes de vies e linguagem potencialmente patologizante antes da resposta final.
- [x] Incluir aviso visivel de que a solucao nao substitui suporte clinico, juridico, de RH ou educacional especializado.
- [x] Garantir que logs de erro nao contenham texto bruto do usuario.

## P3 - Persistencia e Recuperacao Local

- [x] Implementar armazenamento SQLite apenas apos consentimento.
- [x] Criar esquema de banco para interacoes anonimizadas, metadados de consentimento e feedback do usuario.
- [x] Definir migracoes ou script de inicializacao do banco local.
- [x] Integrar ChromaDB somente para dados anonimizados e com finalidade clara: adiado para pos-demo, com decisao documentada em `docs/chromadb_decision.md`.
- [x] Validar criacao, leitura e limpeza dos dados persistidos.
- [x] Documentar local dos arquivos de banco e procedimentos de exclusao.

## P4 - Qualidade, Testes e Validacao

- [x] Expandir testes unitarios para cada agente do pipeline.
- [x] Adicionar testes de integracao do workflow completo.
- [x] Criar testes para falhas do Ollama: indisponibilidade.
- [x] Criar testes de anonimizacao com exemplos realistas de dados sensiveis.
- [x] Validar que a solucao nunca retorna diagnosticos ou julgamentos de culpa.
- [x] Executar testes em ambiente limpo antes da implantacao: `python -m pytest` passou com 7 testes.
- [x] Registrar criterios de aceitacao para demo e para uso piloto.

## P5 - Experiencia de Usuario

- [x] Substituir textos demonstrativos por resultados reais do workflow.
- [x] Adicionar estado de carregamento enquanto os agentes executam.
- [x] Exibir mensagens claras para erro recuperavel.
- [x] Permitir que o usuario revise o texto antes de enviar para analise.
- [x] Adicionar controle de consentimento para armazenamento local.
- [x] Coletar feedback simples sobre utilidade, clareza e seguranca da resposta.
- [x] Melhorar acessibilidade da interface: contraste, rotulos, navegacao por teclado e texto compreensivel.

## P6 - Documentacao de Implantacao

- [x] Atualizar o `README.md` com pre-requisitos completos: Python, Ollama, modelo Gemma e comandos de execucao.
- [x] Documentar configuracao do `.env`.
- [x] Documentar como baixar o modelo no Ollama.
- [x] Documentar como executar testes.
- [x] Documentar limites conhecidos da solucao.
- [x] Adicionar guia de troubleshooting para problemas comuns: porta ocupada, Ollama fora do ar, modelo ausente e dependencia faltante.
- [x] Revisar docs de arquitetura, privacidade e etica para refletirem o estado real da implementacao.

## P7 - Operacao e Go/No-Go

- [x] Definir responsavel pela operacao durante demo ou piloto: apresentador(a) da demo / operador(a) da maquina local.
- [x] Definir plano de rollback: parar Streamlit, remover dados locais e restaurar configuracao anterior.
- [x] Confirmar que nao ha dados reais sensiveis em exemplos, testes, commits ou logs.
- [x] Realizar teste final ponta a ponta com pelo menos tres cenarios de comunicacao: `python scripts/smoke_test.py` passou com 3 cenarios.
- [x] Fazer revisao final de seguranca e privacidade antes de liberar uso por terceiros.
- [x] Registrar decisao Go/No-Go com data, responsavel e pendencias aceitas.

## Criterio Minimo Para Implantacao Demonstrativa

- [x] Aplicacao abre no ambiente-alvo.
- [x] Ollama responde com o modelo configurado: `gemma3:1b` respondeu `ok`.
- [x] Interface chama o workflow real.
- [x] Resposta final passa pela camada de seguranca.
- [x] Nenhum texto bruto e persistido sem consentimento.
- [x] README contem instrucoes suficientes para reproduzir a execucao.

## Multilingue

- [x] Interface disponivel em PT-BR, EN e ES.
- [x] Idioma padrao de processamento configurado como EN.
- [x] Deteccao heuristica do idioma do usuario com fallback para EN.
- [x] Saida apresentada no idioma selecionado pelo usuario.
