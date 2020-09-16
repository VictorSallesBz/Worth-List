# Worth-List
Criador de dicionário para ataques de dicionários.

print("Hello World")

# Qual o objetivo?
### Analisar dicionários de senhas, verificando os formatos mais comuns de senhas.
Pegamos dicionários de senhas famosos como o rockyou, ou algum outro de nossa escolha,
e analisamos os formatos de senhas mais utilizados, para criarmos senhas sem que 
percamos tempos com formatos que poucas pessoas usam (e se usarem um ataque de dicionário será pouco efetivo).

### Analisar as redes sociais do alvo através de palavras de referência.
Coletamos os tweets do alvo (quem sabe mais pra frente podemos pegar informações de outras redes sociais também)
em busca de palavras de referências como gosto musical, time, religião, pessoas próximas, datas importantes etc. 
para a criação do dicionário.


Não sei como vou implementar ainda, já fiz alguns testes e estou estudando o melhor modo de implementar.

### Criar dicionário personalizado para o alvo.
Com a ajuda de palavras de referências e uma análise prévia de formatos válidos para senhas,
criamos um dicionário contendo senhas com uma maior probabilidade de sucesso.

# Como funciona?
### Analisador de dicionários
* Coloque o dicionário no arquivo "Files/Wordlist to Analyze.txt" e rode o programa.
* Selecione a opção 1 - Analyze word list.
* Escolha a quantidade de formatos que queira escrever.

Ex.: Quero usar apenas os 100 formatos mais comuns  -> Digite 100
* Escolha o tamanho mínimo que as senhas devem ter.
* Escolha o tamanho máximo que as senhas devem ter.
* Após isso os formatos serão escritos em "Files/Formats.txt" e alguns dados extras em "Files/Data.txt".

Exemplo

#### 5 Senhas mais comuns com tamanho entre 4 e 6:
1. yyyyyy
2. yyyy
3. 9999
4. Xyyyyy
5. Xyyy@

#### Onde 
* y -> Letra minúscula
* X -> Letra maiúscula
* 9 -> Número
* @ -> Caracter Especial

#### Lembrando que isso é um exemplo de saída e dependerá única e exclusivamente do dicionário utilizado para a análise.

### Coletar palavras de referências do twitter.
* Ainda não foi implementado. Estou trabalhando para ver a melhor forma de fazé-lo e se será viável fazé-lo.
* Toda e qualquer sugestão de implementação será muito bem vinda.

### Criação do dicionário.
* É necessário que o arquivo "Files/Formats.txt" contenha formatos válidos para a criação.
* Escreva as palavras de referências em "Files/Words.txt" e rode o programa.

As palavras devem ser escritas linha a linha.

Nomes devem ser escritos em uma única linha.

#### Exemplo

victor hugo santana salles

24

10

1995

fulaninho silveira costa

flamengo

scalene

* Selecione a opção 2 - Generate word list from file.
* Escolha a quantidade de formatos que queira usar Ex.: Quero usar apenas os 100 formatos mais comuns -> Digite 100.
* Escolha o tamanho mínimo que as senhas devem ter.
* Escolha o tamanho máximo que as senhas devem ter.
* Escolha se deseja um dicionário mais leve ou mais pesado.

#### Diferença entre os 2 modos:
1. As listas leves são combinações entre as palavras de referências como por exemplo: ABC -> AB, AC, BC.
2. As listas pesadas são permutações entre as palavras de referências como por exemplo: ABC -> AB, AC, BA, BC, CA, CB.

* Após isso, o dicionário será escrito em "Files/Wordlist.txt".

# Requirements
* Instalar a biblioteca Nltk.
```
pip install nltk
```
* Instalar a biblioteca Tweepy.
```
pip install tweepy
```
* Muita fé em seu Deus/Deuses para que rode sem problemas - Pode ignorar essa etapa caso seja ateu ou agnóstico.

# Próximas atualizações
* Criar uma opção para criar dicionários voltados para força bruta - Leia-se "cópia descarada do Crunch".
* Implementar a coleta de informações pelo Twitter.
* Adicionar pequenas funções como:
1. Adicionar manualmenete formartos.
2. Adicionar manualmente palavras de referências.
3. Adicionar manualmente senhas no dicionário.
* *Talvez* criar um script para instalar todas dependências e rodar o programa automaticamente.


# Observações
* Meu inglês é de Joel Santana, portanto relevem os possíveis muitos erros gramaticais no código.
Escrevi ele em inglês justamente para estudar já que venho estudando por imersão, onde coloco o inglês
em todas as coisas do meu dia a dia como celular e computador configurados em inglês, lendo artigos, livros
em inglês e também vendo e ouvindo tudo em inglês com legenda.

Por enquanto é isso, até a próxima :)
