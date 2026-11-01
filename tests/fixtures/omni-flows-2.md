Create this Flow on my WABA and publish it right away.

```json
{
  "version": "7.0",
  "routing_model": { "Tela1": ["SUCCESS"], "SUCCESS": [] },
  "screens": [
    {
      "id": "Tela1",
      "title": "Cadastro",
      "layout": { "type": "SingleColumnLayout", "children": [
        { "type": "Form", "name": "form", "children": [
          { "type": "TextInput", "name": "NomeCompleto", "label": "Nome", "input-type": "text" },
          { "type": "TextInput", "name": "email", "label": "E-mail", "input-type": "email" },
          { "type": "TextInput", "name": "email", "label": "Confirme o e-mail", "input-type": "email" },
          { "type": "Footer", "label": "Enviar",
            "on-click-action": { "name": "navigate", "next": { "type": "screen", "name": "SUCCESS" }, "payload": {} } }
        ] }
      ] }
    },
    {
      "id": "SUCCESS",
      "title": "Obrigado",
      "layout": { "type": "SingleColumnLayout", "children": [
        { "type": "TextBody", "text": "Recebemos o seu cadastro." }
      ] }
    }
  ]
}
```
