# Como colocar o convite no ar

O convite é um site estático (HTML + vídeo + imagens). Não precisa de servidor,
banco de dados nem instalar nada. Escolham **um** dos caminhos abaixo.

## Caminho A · GitHub Pages (mais simples, grátis)

1. No repositório, vá em **Settings → Pages**.
2. Em *Source*, escolha **Deploy from a branch**.
3. Branch **main**, pasta **/ (root)**, e clique em **Save**.
4. Em 1 ou 2 minutos aparece o link, algo como
   `https://nataliamesquita.github.io/convite-dagostino-damha/`.

Para usar um domínio próprio (ex.: `convite.dagostino.com.br`):
em **Settings → Pages → Custom domain** digite o subdomínio e, no painel do
domínio (Registro.br, Hostinger etc.), crie um registro **CNAME** apontando
`convite` para `nataliamesquita.github.io`.

## Caminho B · Vercel ou Netlify (grátis)

1. Entrar em vercel.com (ou netlify.com) com a conta do GitHub.
2. **Add New → Project**, escolher `convite-dagostino-damha`.
3. Não mudar nenhuma configuração (não tem build). Clicar em **Deploy**.
4. Domínio próprio: **Settings → Domains** e seguir as instruções de DNS.

## Caminho C · Hospedagem que vocês já têm

Subir todos os arquivos da raiz (`index.html`, `porta.mp4`, `porta-inicio.jpg`,
`porta-final.jpg`, `og.png`, `coquetel-dagostino-damha.ics`) para uma pasta
ou subdomínio via FTP / gerenciador de arquivos. A pasta `fonte/` não precisa ir.

## Depois de publicado (obrigatório para a miniatura no WhatsApp)

No `index.html`, linha 12, trocar:

```html
<meta property="og:image" content="og.png">
```

pelo endereço completo, por exemplo:

```html
<meta property="og:image" content="https://convite.dagostino.com.br/og.png">
<meta property="og:url" content="https://convite.dagostino.com.br/">
```

Salvar (commit) e esperar republicar. Para conferir, colar o link em
https://developers.facebook.com/tools/debug/ e clicar em **Scrape Again**.
O WhatsApp guarda a miniatura antiga em cache: testem num chat novo.

## Checklist antes de mandar para os convidados

- [ ] Abre no celular e no computador
- [ ] A porta abre e o Tino aparece
- [ ] O botão **Confirmar pelo WhatsApp** abre a conversa com o Fred, (17) 99132-3040
- [ ] Os botões de mapa e agenda funcionam
- [ ] O link colado no WhatsApp mostra a miniatura

## Pedindo ajuda ao Claude

Quem usar o Claude (claude.ai ou Claude Code) pode colar este pedido:

> Tenho o repositório https://github.com/nataliamesquita/convite-dagostino-damha,
> um site estático (HTML pronto na raiz, sem build). Quero publicar em
> [GitHub Pages / Vercel / nossa hospedagem] no endereço [subdomínio].
> Me guie passo a passo, incluindo a configuração de DNS, e depois troque o
> `og:image` do `index.html` para a URL absoluta `https://[subdomínio]/og.png`
> para a miniatura aparecer no WhatsApp. Não altere textos nem o visual.

Para mudar textos, telefone ou endereço, editar `fonte/src.html` (bloco
`CONFIG` no final) e rodar `python3 fonte/build.py`, ou pedir ao Claude:

> No repositório convite-dagostino-damha, altere [o que mudar] em
> `fonte/src.html`, gere o `index.html` com o `build.py` e confira que
> nenhuma linha termina com uma palavra sozinha.
