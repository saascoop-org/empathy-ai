# Issue Draft: Preparar demo publica controlada com VM, Ollama/Gemma4 e Streamlit

## Contexto

Queremos disponibilizar o EmpathyAI para teste em uma URL publica controlada, mantendo a arquitetura atual no curto prazo: VM protegida + Ollama/Gemma4 + Streamlit, com diario efemero.

Esta issue trata do proximo passo de implantacao. O pacote de UX ja implementado na branch `ux-demo-readiness-streamlit` deve ser registrado separadamente em `docs/issue_ux_demo_readiness_streamlit.md`.

## Decisao recomendada para a URL publica

Publicar apenas como demo controlada, nao como demo aberta:

- VM com RAM/VRAM suficiente para Gemma4.
- Ollama e Streamlit no mesmo servidor ou rede privada.
- HTTPS obrigatorio.
- Autenticacao simples ou link protegido.
- Porta do Ollama nao exposta publicamente.
- Diario efemero por sessao ou desativado para evitar mistura de dados entre testers.
- Limite de concorrencia/rate limit.
- Rotina de limpeza de dados apos testes.

## Escopo da demo publica controlada

- Expor a interface Streamlit por uma URL publica protegida.
- Executar o modelo Gemma4 via Ollama no servidor da demo.
- Manter a experiencia de UX implementada na branch `ux-demo-readiness-streamlit`.
- Usar persistencia efemera para o diario de aprendizado mutuo.
- Garantir que a demo seja adequada para teste limitado, nao para producao aberta.

## Pendencias para implantacao

- [ ] Definir provedor/tamanho da VM compativel com Gemma4.
- [ ] Validar `gemma4:e2b` com memoria suficiente no servidor.
- [ ] Configurar Ollama no servidor e baixar o modelo definido em `GEMMA_MODEL`.
- [ ] Configurar Streamlit para host publico atras de proxy/HTTPS.
- [ ] Proteger acesso com autenticacao ou senha.
- [ ] Garantir que a porta do Ollama nao fique exposta publicamente.
- [ ] Implementar politica de diario efemero ou desativar persistencia entre usuarios.
- [ ] Confirmar que nenhum dado cru e persistido.
- [ ] Definir limpeza automatica de `data/interactions.sqlite3` ou storage temporario.
- [ ] Documentar operacao de start/stop da demo.
- [ ] Executar checklist de validacao antes de liberar a URL.

## Checklist de validacao antes da URL

- [ ] `python -m pytest`
- [ ] `python scripts/smoke_test.py`
- [ ] `python scripts/check_ux_accessibility.py`
- [ ] `python scripts/check_streamlit.py`
- [ ] Teste manual de idioma PT-BR.
- [ ] Teste manual do diario efemero.
- [ ] Teste manual de concorrencia minima.
- [ ] Teste manual de acesso HTTPS.
- [ ] Teste manual de bloqueio da porta do Ollama.

## Riscos conhecidos

- Streamlit ainda nao e o front ideal para teste publico multiusuario.
- SQLite local precisa isolamento ou uso efemero para multiplos testers.
- Gemma4 pode apresentar latencia alta e fila se houver concorrencia.
- A anonimizacao atual e baseline de demo, nao garantia produtiva.
- Audio exige HTTPS e ainda nao possui transcricao automatica nesta versao.

## Como criar esta issue no GitHub

Depois de reautenticar o GitHub CLI:

```powershell
gh auth login -h github.com
gh issue create --repo HackathonBrTeam/Empathy-Interactional-Expertise --title "Preparar demo publica controlada com VM, Ollama/Gemma4 e Streamlit" --body-file docs/issue_demo_publica_controlada.md
```

