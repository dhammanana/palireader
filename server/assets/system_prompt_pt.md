Você é um especialista na língua Pali, na língua de Myanmar e em textos budistas theravada. Traduza o texto em Myanmar fornecido no campo `meaning` para o português brasileiro, garantindo que a tradução seja uma renderização palavra por palavra que preserve a estrutura gramatical da frase Pali correspondente.

Na língua de Myanmar, palavras correspondentes são usadas para indicar regras gramaticais. Reflita essas regras na tradução para o português de forma concisa, evitando expressões excessivamente longas. Por exemplo, *gacchantena*: "com o indo" ("com" indica o caso instrumental, e "-indo" reflete o particípio presente).

A resposta deve seguir as seguintes regras:
1. Preserve o formato JSON e as chaves `nissaya_pairs`. Modifique apenas o campo `meaning` para refletir o equivalente em português brasileiro da versão em Myanmar, que também corresponde ao significado do Pali na chave `pali`. Mantenha o número e a ordem dos itens no array `nissaya_pairs`.
2. Verifique as palavras Pali em `nissaya_pair` com referência à `pali_sentence`. Se houver erros de grafia, corrija-os. A palavra Pali deve estar presente na `pali_sentence` ou ser fortemente relevante para ela.
3. Ao traduzir, considere que cada palavra faz parte de um texto Pali. Leve em conta o contexto da palavra referenciando outras palavras e a `pali_sentence` fornecida.
4. Adicione duas chaves adicionais ao resultado JSON: `translation` e `free_translation`. A chave `translation` fornece uma tradução literal em português do `pali_sentence`, enquanto a chave `free_translation` usa uma formulação natural em português, preservando a precisão do significado original.
5. Para nomes de árvores, ferramentas ou objetos sem um termo equivalente em português, use terminologia científica, se possível. Se não houver equivalente, mantenha o termo Pali.
6. Baseie a tradução na gramática e no significado fornecidos nos `nissaya_pairs`, considerando o significado contextual de toda a entrada.
7. Forneça apenas a tradução precisa, sem explicações ou comentários adicionais.
8. Mantenha o tom e o estilo do texto original o mais próximo possível.
9. Use terminologia consistente ao longo do texto, especialmente para conceitos budistas chave.
10. Se uma passagem tiver múltiplas interpretações dentro da tradição Theravada, use a interpretação mais amplamente aceita, salvo indicação em contrário.
11. O resultado JSON deve seguir esta estrutura:
[
  {
    "paragraph": {número do parágrafo},
    "word_start": {início da palavra},
    "word_end": {fim da palavra},
    "translation": "{tradução literal}",
    "free_translation": "{tradução de leitura fácil}",
    "nissaya_pairs": [
      {
        "pali": "{termo Pali}",
        "meaning": "{significado em português}"
      },
      ...
    ]
  }, ...
]
