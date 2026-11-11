# Convite de inauguração · Dagostino Papelaria e Brinquedo · Damha

Página do convite para o coquetel de inauguração da nova loja no Damha.

- **Quando:** quinta, 26/11/2026, das 19h às 22h
- **Onde:** Rua José Arlindo de Melo Silva, 1486, Parque São Miguel, São José do Rio Preto/SP
- **Confirmação:** o formulário abre o WhatsApp do Frederico Tebar com a mensagem pronta

## Como publicar

É um site estático. Basta subir a raiz deste repositório em qualquer hospedagem
(GitHub Pages, Netlify, Vercel, servidor próprio, subdomínio da loja).

Arquivos publicados:

| Arquivo | O que é |
| --- | --- |
| `index.html` | A página (logo e Tino já embutidos) |
| `porta.mp4`, `porta-inicio.jpg`, `porta-final.jpg` | Animação 3D da porta |
| `og.png` | Miniatura 1200x630 que aparece no WhatsApp |
| `coquetel-dagostino-damha.ics` | Arquivo de agenda |

### Miniatura no WhatsApp (importante)

Depois de definir o domínio, troque no `<head>` do `index.html` o `og:image`
para o endereço completo, por exemplo `https://convite.dagostino.com.br/og.png`.
O WhatsApp só mostra a miniatura com URL absoluta e em domínio público.

Passo a passo completo de publicação: veja [PUBLICAR.md](PUBLICAR.md).

## Editar

O código-fonte está em `fonte/`:

- `src.html`: página editável. No fim do arquivo há o bloco `CONFIG`
  com o telefone do Fred e o endereço.
- `build.py`: gera o `index.html` final, embutindo as imagens.
- `src-v2-telefone-mapa.html`: variante com campo de telefone e mapa
  depois da confirmação (aguardando aprovação).
- `scene3.py`: cena do Blender usada para renderizar a porta.
