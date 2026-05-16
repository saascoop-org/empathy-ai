# Issue Draft: Preparar demo publica controlada com UX Streamlit e Gemma4

## Contexto

Queremos disponibilizar uma demo para teste em URL publica controlada, mantendo a arquitetura atual no curto prazo: VM protegida + Ollama/Gemma4 + Streamlit, com diario efemero.

Branch local de registro: `ux-demo-readiness-streamlit`

Commits locais:

- `4fd7bdc` - `Prepare Streamlit UX demo readiness`
- `a58b9f1` - `Add public demo issue draft`

Observacao: a branch foi criada localmente. O `gh` local esta com token invalido e o conector GitHub retornou 403 ao criar issue, entao o push da branch e a abertura da issue ainda precisam de autenticacao GitHub valida.

## Como criar a issue no GitHub

Depois de reautenticar o GitHub CLI:

```powershell
gh auth login -h github.com
gh issue create --repo HackathonBrTeam/Empathy-Interactional-Expertise --title "Preparar demo publica controlada com UX Streamlit e Gemma4" --body-file docs/issue_demo_publica_controlada.md
```

Opcionalmente, publique a branch antes:

```powershell
git push -u origin ux-demo-readiness-streamlit
```

## Implementacoes registradas

- Front-end Streamlit reorganizado para fluxo vertical e menor carga cognitiva.
- Mapa de Alteridade com rotulos persistentes e exemplos em placeholders.
- Cenarios de demo pre-preenchidos para acelerar apresentacao.
- Diario de aprendizado mutuo com busca, titulos amigaveis, data/hora local, exclusao e exibicao localizada.
- Correcoes de idioma para reduzir mistura EN/PT-BR/ES na interface e no diario.
- Ponte sugerida destacada como resultado principal, com botao de copiar.
- Entrada opcional de audio com `st.audio_input`, sinalizada como recurso de demo sem transcricao automatica.
- Melhorias de acessibilidade: contraste, foco visivel, feedback nao dependente apenas de cor e script de checagem.
- Documentacao criada para backlog UX, validacao de acessibilidade, contratos HTTP futuros, privacidade de audio, roteiro de demo e decisao de evolucao do front-end.

## Validacoes executadas

- `python -m pytest`: 50 passed.
- `python scripts/smoke_test.py`: 3 cenarios ok.
- `python scripts/check_ux_accessibility.py`: ok.
- `python scripts/check_streamlit.py`: ok em `http://localhost:8501`.

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

## Pendencias para implantacao da demo publica controlada

- [ ] Definir provedor/tamanho da VM compativel com Gemma4.
- [ ] Validar `gemma4:e2b` com memoria suficiente no servidor.
- [ ] Configurar Streamlit para host publico atras de proxy/HTTPS.
- [ ] Proteger acesso com autenticacao ou senha.
- [ ] Implementar politica de diario efemero ou desativar persistencia entre usuarios.
- [ ] Confirmar que nenhum dado cru e persistido.
- [ ] Definir limpeza automatica de `data/interactions.sqlite3` ou storage temporario.
- [ ] Documentar operacao de start/stop da demo.
- [ ] Executar checklist de validacao antes de liberar a URL.

## Riscos conhecidos

- Streamlit ainda nao e o front ideal para teste publico multiusuario.
- SQLite local precisa isolamento ou uso efemero para multiplos testers.
- Gemma4 pode apresentar latencia alta e fila se houver concorrencia.
- A anonimizacao atual e baseline de demo, nao garantia produtiva.
- Audio exige HTTPS e ainda nao possui transcricao automatica nesta versao.
