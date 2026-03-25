---
skill_name: ux
domain: usabilidade digital e acessibilidade sênior
keywords:
  - whatsapp
  - interface
  - acessibilidade
  - fonte
  - botão
  - tela
  - áudio
  - vídeo
  - aplicativo
  - app
  - celular
  - smartphone
  - digital
  - navegação
  - clique
  - menu
  - ícone
  - tutorial
  - ajuda
  - dificuldade
  - usabilidade
  - design
prompt_template: >
  Atue como um Designer de UX especializado em Acessibilidade para
  o público sênior (60+ anos). Use o CONHECIMENTO PRÉVIO abaixo
  para fundamentar sua resposta. Aplique princípios de design universal,
  considere limitações motoras e cognitivas típicas da idade, e priorize
  a jornada via WhatsApp como canal principal. Use Chain-of-Thought
  para detalhar cada etapa quando propor fluxos de interação.
---

# Conteúdos Digitais e Usabilidade — UX Sênior

## Consumo de Conteúdo Digital

### WhatsApp como Porta de Entrada
- **Canal #1** para o público 60+: 93% dos idosos com smartphone usam WhatsApp (TIC Domicílios 2023).
- Prefere **áudios** a texto (gravação por voz é mais natural que digitar).
- Recebe informações via **grupos familiares** — principal filtro de conteúdo.
- Vulnerável a desinformação: dificuldade em distinguir notícia falsa de verdadeira.

### Preferências de Formato
1. **Áudio** (>60 seg avaliado como "longo") — ideal para explicações simples.
2. **Vídeo curto** (<2 min) — excelente para tutoriais passo-a-passo.
3. **Imagens com texto grande** — cards informativos com contraste alto.
4. **Texto** — apenas para informações curtas, listas ou confirmações. Evitar parágrafos longos.
5. **PDFs / documentos** — apenas quando necessário (comprovantes, contratos). Dificuldade em abrir e navegar.

### Horários de Pico
- Manhã (7-10h): verificação de mensagens noturnas, notícias.
- Início da tarde (13-15h): após almoço, período de maior engajamento.
- Noite (19-21h): WhatsApp com família.

## Barreiras de Usabilidade

### Limitações Físicas
- **Visual**: presbiopia (dificuldade de foco próximo), sensibilidade a brilho, menor percepção de contraste.
- **Motora**: menor precisão no toque (tremor, artrite), dificuldade com gestos complexos (pinça, swipe, long press).
- **Auditiva**: perda auditiva parcial — áudios precisam de boa qualidade e opção de transcrição.
- **Cognitiva**: processamento mais lento, menor memória de trabalho — excesso de opções gera paralisia.

### Problemas Comuns em Interfaces
- **Fontes pequenas**: padrão de 14px é insuficiente. Mínimo recomendado: **18sp** (Android) / **18pt** (iOS).
- **Ícones abstratos**: hamburger menu (≡), seta de compartilhar, nuvem. Preferem **ícone + texto**.
- **Muitos cliques**: cada tela adicional aumenta abandono em ~15% para 65+.
- **Timeout curto**: sessões expiram antes do usuário completar a tarefa.
- **Feedback insuficiente**: ação realizada sem confirmação visual clara gera ansiedade ("será que deu certo?").
- **Linguagem técnica**: "token", "autenticação", "biometria", "QR code" — barreiras linguísticas reais.

## Facilitadores e Boas Práticas

### Princípios de Design para 60+
1. **Menos é mais**: telas com 1-3 ações claras. Sem menus aninhados.
2. **Texto legível**: 18px+, contraste mínimo 4.5:1 (WCAG AA), sans-serif.
3. **Áreas de toque grandes**: mínimo 48x48dp (recomendado 56x56dp para o público sênior).
4. **Confirmação explícita**: "Você está enviando R$ 50,00 para Maria. Confirmar?" com botão verde grande.
5. **Ícone + texto sempre**: nunca ícone sozinho. "🏠 Início", "💰 Saldo", "📞 Ajuda".
6. **Caminho de volta claro**: botão "Voltar" visível em todas as telas. Sem gestos ocultos.
7. **Feedback imediato**: animação suave + mensagem "✅ Pagamento realizado com sucesso!".
8. **Ajuda acessível**: botão de ajuda fixo. Opção de ligar para atendimento humano sempre visível.

### Padrões para WhatsApp
- **Mensagens curtas**: máximo 3 linhas por mensagem. Se precisar de mais, dividir em mensagens sequenciais.
- **Emojis como marcadores**: ✅ para confirmação, ⚠️ para alerta, 📌 para informação importante.
- **Botões de resposta rápida**: usar listas de opções numeradas ("Digite 1 para Saldo, 2 para Extrato").
- **Sem links encurtados**: links curtos parecem golpe. Usar domínios reconhecíveis ou evitar links.
- **Horário de envio**: respeitar o horário do público. Não enviar após 20h.

### Fluxo de Conversa Ideal (WhatsApp)
```
[Bot] Olá, Maria! 👋 Sou o assistente do [Banco].
[Bot] Como posso ajudar hoje?

1️⃣ Ver meu saldo
2️⃣ Consultar empréstimo
3️⃣ Falar com atendente
4️⃣ Outra dúvida

[User] 1

[Bot] ✅ Seu saldo em 24/03/2026:
💰 Conta Corrente: R$ 1.234,56

Deseja mais alguma coisa?
1️⃣ Sim, outra consulta
2️⃣ Não, obrigado(a)
```

## Métricas de Sucesso
- **Taxa de completamento**: % de usuários que completam a tarefa sem abandonar.
- **Tempo por tarefa**: idosos levam 2-3x mais tempo que adultos jovens. Design deve acomodar.
- **Chamadas ao suporte**: redução indica melhoria de autoatendimento.
- **NPS por faixa etária**: 60+ tende a dar notas extremas (muito satisfeito ou muito insatisfeito).

## Fontes Esperadas
- NIC.br / TIC Domicílios (acesso à internet por faixa etária)
- W3C / WCAG 2.1+ (diretrizes de acessibilidade web)
- Google Material Design (guidelines de acessibilidade)
- Apple Human Interface Guidelines (acessibilidade iOS)
- Nielsen Norman Group (UX research para idosos)
- Febraban (pesquisas de uso de canais digitais por idade)
