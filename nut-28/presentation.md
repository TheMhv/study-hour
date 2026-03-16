---
title: NUT-28 Pay-to-Blinded-Key (P2BK)
author: TheMhv
theme:
  name: catppuccin-macchiato
---

NUT-28: Pay to Blinded Key (P2BK)
---

# O que é?

O NUT-28 descreve um Spending Condition (NUT-10) que estende o NUT-11 (P2PK).

Para entender o NUT-28, precisamos antes entender o básico do NUT-11 (P2PK).

<!-- end_slide -->
<!-- alignment: center -->
<!-- jump_to_middle -->
NUT-11: Pay to Public Key (P2PK)
---
<!-- end_slide -->

NUT-11: Pay to Public Key (P2PK)
---

O NUT-11 descreve um método de Spending Condition (NUT-10), o Pay to Public Key (P2PK).

Ele é usado para 'travar' um token ecash para uma chave pública ECC e requer uma assinatura Schnorr válida correspondente à mesma chave privada para desbloqueá-lo. Essa condição de gasto é assegurada pela Mint.

<!-- pause -->

Seguindo as especificações no NUT-10, o NUT-11 descreve o `Secret`:
```json
[
  "P2PK",
  {
    "nonce": "...", // <hex_str>
    "data": "...", // <hex_str>
    "tags": [["sigflag", "SIG_INPUTS"]]
  }
]
```

Este `Secret` contém 2 campos importantes; o campo `data` e a tag `sigflag`:

- O campo `data` é onde vai a chave pública do destinatário
- A tag `sigflag` determina a mensagem que deverá ser assinada e validada.

<!-- end_slide -->
NUT-11: Pay to Public Key (P2PK)
---

O NUT-11 descreve também o uso de tags opcionais, são elas:

- `pubkeys: <hex_str>`: Especifica chaves públicas adicionais (juntamente com a especificada no campo `data`). Ela serve para criar condições de gasto com mais de uma chave pública.
- `n_sigs: <int>`: Especifica o número mínimo de assinaturas válidas.
- `locktime: <int>`: Define um timestamp no formato Unix que expira a condição de 'trava'.
- `refund: <hex_str>`: Define chaves públicas adicionais que podem prover assinaturas válidas após timestamp do campo `locktime` expirar.
- `n_sigs_refund: <int>`: Especifica o número mínimo de assinaturas válidas para as chaves do campo `refund` após o timestamp `locktime` expirar.

Com estes campos, podemos definir condições de gasto mais complexas, como multisig, locktime e condições de reembolso.

<!--pause -->

---
Para destravar um token ecash cashu com uma Spending Condition do tipo NUT-11, precisamos de um `Witness` com uma ou mais assinaturas válidas para as chaves públicas especificadas no `Secret`:
```json
{
  "signatures": ["..."] // Array<[<hex_str>]>
}
```

<!-- end_slide -->
O "problema" do NUT-11
---

O NUT-11 é uma ótima forma de criar uma condição de gasto baseado em assinaturas e chaves públicas. Mas existe um 'problema': A falta de privacidade.

O NUT-11 descreve a chave pública no `Secret`, expondo-a para qualquer terceiro que tenha acesso a ele. A Mint, por exemplo, contém informações de timing + quantia de ecash emitido + chaves públicas utilizadas e etc, podendo desenhar o caminho de pagamentos e realizar ataques de deanonimização.

<!-- pause -->
---
NUT-28: A solução
---

O NUT-28 surge como uma solução para a falta de privacidade do NUT-11. Ele estende o NUT-11, isto é, utiliza a mesma estrutura de `Secret` e `Witness` descrita no NUT-11.

O NUT-28 ofusca cada chave pública destinatária, utilizando um algoritmo de Key Blinding, com uma escalar derivada de um segredo compartilhado utilizando Elliptic-curve Diffie–Hellman (ECDH).

<!-- end_slide -->
<!-- alignment: center -->
<!-- jump_to_middle -->
NUT-28: Como funciona?
---
<!-- end_slide -->

NUT-28: Como funciona?
---

O NUT-28 utiliza o mesmo `Secret` e `Witness` descritos no NUT-11, a única diferença está no campo `Proof` (descrito no NUT-00) onde é adicionado o campo `p2pk_e` que contém uma chave pública efêmera `E`.

Também mudamos o processo de derivação de chaves. A chave pública utilizada nos campos `Secret.data`, `Secret.tags.pubkeys` e `Secret.tags.refund` serão chaves ofuscadas `P'`, derivadas através de um algoritmo explicado à seguir.

<!-- pause -->

---

## Remetente

Para que o NUT-28 funcione, o remetente (pagador) deve seguir um algoritmo:

- Gerar uma chave efêmera aleatória `e` e computar `E = e*G`
- Para cada chave pública destinatária `P`:
  - a. Deve derivar o segredo compartilhado para a chave: `Z = e*P` (e usar somente a coordenada x: `Z.x`)
  - b. Deve especificar o slot `i` no `Secret`
  - c. A partir destes dados, derivar o escalar: `ri = SHA-256(b"Cashu_P2BK_v1" || Z.x || i_byte)`
  - d. Derivar a chave pública ofuscada: `P' = P + ri*G`
- Construir o `Secret` P2PK (NUT-11) com a chave pública ofuscada `P'` no slot `i` especificado.
- Interagir normalmente com a Mint
- Incluir `p2pk_e = E` no objeto `Proof` do token

Com isso, uma terceira parte nunca sabe sobre `P` ou `ri`. Sendo `P'` uma chave pública válida, fica impossível distinguir de uma chave pública normal.

<!-- end_slide -->

NUT-28: Como funciona?
---

## Destinatário

O destinatário (recebedor) também deve seguir um algoritmo para gerar uma assinatura válida para `P'`:

- Ler `E` do campo `p2pk_e` dentro da `Proof`
- Calcular o segredo compartilhado: `Z = p*E` (usar somente a coordenada x: `Z.x`)
- Para cada slot `i`:
  - a. Computar a mesma escalar: `ri = SHA-256(b"Cashu_P2BK_v1" || Z.x || i_byte)`
  - b. Desofuscar a chave pública: `P = P' - ri*G`
  - c. Verificar se: `P == p*G`
    - Se não, essa chave ofuscada `P'` não é sua chave pública, pular.
  - d. Derivar a chave privada de `P'`: `k = (p + ri) mod n`
  - Gerar uma assinatura válida com a chave privada `k` e gastar o token

Uma assinatura feita com a chave privada `k` é válida para `P'`, sendo impossível determinar se `P'` é uma chave ofuscada ou não, garantindo que as chaves públicas não sejam expostas.


<!-- end_slide -->
<!-- alignment: center -->
<!-- jump_to_middle -->
Tá... Mas por que funciona?
---
<!-- end_slide -->

NUT-28: Por que funciona?
---

# Metade da resposta está no ECDH (Elliptic-curve Diffie-Hellman):

Devido ao problema de logaritmo discreto (ECDLP), podemos expor `P` e `E`, porque:

`P = p*G` e `E = e*G`

E devido à característica de comutatividade do ECC:

`ep*G = e*(p*G) = p*(e*G)`

Ambas as partes podem chegar ao mesmo ponto `Z`:

`Z = e*P = p*E`

<!-- pause -->

> Ok... Mas há um problema aí. A chave pública `P` está sendo exposta, a ideia não é ofuscá-la?

<!-- end_slide -->

NUT-28: Por que funciona?
---

# Aí vem a outra parte da resposta: Key blinding:

Precisamos esconder a chave pública original `P`, então usamos um algoritmo de ofuscação:

`P' = P + r*G`

Isso funciona devido à outra característica do ECC, a linearidade:

`(p+r)*G = p*G + r*G`

Ou seja: `P' = P + r*G`

`P'` é um ponto válido na curva; uma chave pública válida, derivada a partir de `p+r`; sua chave privada. Podemos gerar uma assinatura válida para `P'` com `p+r`.

<!-- pause -->

> Mas como as duas partes chegam a `r` sem que um terceiro também consiga?

<!-- end_slide -->
Gran finale... onde a mágica acontece!
---

<!-- alignment: center -->
![](magic.gif)

<!-- end_slide -->

NUT-28: Por que funciona?
---

Se juntarmos os dois métodos **ECDH** e **Key Blinding**, podemos derivar o fator `r` a partir do segredo compartilhado `Z` sem que um terceiro saiba.

Alice:
- `Z  = e*P`
- `r  = Z.x`
- `P' = P + r*G`
- `E  = e*G`

Bob:
- `Z  = p*E`
- `r  = Z.x`
- `P  = P' - r*G` (valida se `P = p*G`)
- `k  = p+r`

---

Traduzindo para o NUT-11, onde podemos ter mais de uma chave pública, precisamos derivar `ri` para cada uma utilizando o algoritmo:

`ri = SHA-256(b"Cashu_P2BK_v1" || Z.x || i_byte)`

Assim, as partes destinatárias não conseguem desofuscar a chave pública que não seja dela mesma.

<!-- end_slide -->
<!-- alignment: center -->
<!-- jump_to_middle -->
Comentários adicionais
---
<!-- end_slide -->

Comentários adicionais
---

## Derivando chaves ofuscadas

O NUT-28 define 11 slots disponíveis na ordem:
- A chave pública no campo `data` tem slot definido 0: `i = 0`
- Os demais slots (1-10) são definidos nos campos das tags `pubkeys` e `refund`.

Se `ri` não for um escalar válido, devemos adicionar um byte extra `0xff` na preimage do hash:

`ri = SHA-256( b"Cashu_P2BK_v1" || Z.x || i_byte || 0xff)`

Se `ri` ainda não for um escalar válido, devemos descartar `e` e recalcular o ponto `Z` usando um novo segredo.

---

O NUT-28 também explicita que podemos derivar a chave privada negativa:

`k = (-p + ri)`

Por esse motivo, se `P != p*G` o destinatário deve validar também se `P == -p*G`.

<!-- end_slide -->

Referências
---

[NUT-28: Pay-to-Blinded-Key \(P2BK\)](https://github.com/cashubtc/nuts/blob/main/28.md)


<!-- end_slide -->
<!-- alignment: center -->
<!-- jump_to_middle -->
Perguntas?
---

<!-- end_slide -->
<!-- alignment: center -->
<!-- jump_to_middle -->
FIM!
---
