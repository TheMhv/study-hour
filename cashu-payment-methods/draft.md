# Cashu onchain payments

### O que é?

São uma nova forma de fazer operações de mint e melt utilizando pagamentos Bitcoin onchain.

- Já não era assim?

Não, o Cashu foi, inicialmente, criado sob o protocolo Lightning, utilizando pagamentos via bolt11. Mais tarde foi implementado pagamentos via Bolt12.

Pagamentos onchain estão em discussão e devem ser implementados em breve.

...

Antes de continuar, precisamos entender como funciona as operações de Mint e Melt do Cashu.

## Como funciona o Cashu

Como sabemos, Cashu é uma implementação de Ecash Chaumian, que utiliza **Blind Diffie-Hellmann Key Exchange** para criar uma assinatura válida de um segredo ofuscado.

Para explicar os passos do protocolo, vamos definir três indivíduos, *Alice*, *Bob* e *Carol*.
*Alice* e *Carol* são usuários comuns enquanto **Bob é a Mint**.

* Operação de Mint

A operação de "cunhagem" de novos tokens é feito através de um protocolo simples:

1. *Bob* expõe sua chave pública `A` derivada de uma chave privada `a`.
2. *Alice* cria um segredo `x` e encontra um ponto válido na curva para seu hash `Y = hash_to_curve(x)`.
3. Com o ponto válido `Y` para seu segredo, *Alice* o ofusca utilizando um nonce `r` para que *Bob* não tenha informação: `B' = Y + r*G`
4. *Alice* então envia o segredo ofuscado `B'` juntamente com os fundos para que *Bob* o assine `C' = a*B'`.
5. *Alice* terá então uma assinatura válida de *Bob* para `x`, derivando através de: `C = C' - r*A`.

* Operação de Melt

*Alice* possue um segredo `x` e uma assinatura `C` de *Bob* válida para este valor. Dado que *Bob* não conhece `x`, o processo de dissolver os tokens se baseia simplesmente da exposição do segredo e a validação da assinatura.

6. *Alice* expõe para *Bob* seu segredo `x` e a assinatura `C`.
7. Com a informação do segredo `x`, *Bob* pode chegar ao mesmo ponto válido na curva de seu hash `Y = hash_to_curve(x)`
8. *Bob* valida a assinatura recebida de *Alice* com sua chave privada `C == a*Y`.
  - Se válido, *Bob* envia os fundos para *Alice* e "queima" o segredo `x`, salvando-o para que não possa ser gasto novamente.

### Como funciona na prática (Lightning)

* Mint, pagar invoice

1. A carteira faz uma requisição de cota de cunhagem, especificando o método de pagamento e a unidade para a Mint.
2. A Mint responde com uma cota válida e o invoice do pagamento.
3. O usuário paga o invoice utilizando o mesmo método de pagamento
4. A carteira requisita a cunhagem dos novos tokens para a Mint, utilizando o id da cota e o segredo ofuscado `B'`.
5. A Mint verifica o pagamento da cota, assina o segredo ofuscado `C' = a*B'` e retorna a assinatura ofuscada `C'`.

* Melt, receber pagamento

1. A carteira requisita uma cota de dissolução dos tokens, especificando o método de pagamento e a unidade para a Mint.
2. A Mint responde com uma cota e o valor pago na unidade especificada.
3. A carteira envia uma requisição de dissolução incluindo a cota e provê o segredo.
4. A Mint executa o pagamento e responde com o estado e a prova de pagamento no método especificado

## Pagamentos On-chain

* Mint process

O pagamento onchain segue o mesmo princípio.

1. A carteira faz uma requisição de cota de cunhagem, especificando o método de pagamento e a unidade para a Mint. No pagamento onchain, a carteira deve especificar uma pubkey.
2. A Mint responde com uma cota válida e o endereço que deve receber os fundos.
3. O usuário envia os fundos para o endereço e aguarda o número de confirmação necessária especificada pela Mint.
4. Com a cota confirmada, a carteira requisita a cunhagem dos novos tokens para a Mint, utilizando o id da cota e o segredo ofuscado `B'`.
5. A Mint verifica o pagamento da cota, assina o segredo ofuscado `C' = a*B'` e retorna a assinatura ofuscada `C'`.
