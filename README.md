# AppTelecom

Aplicação para o departamento de telecomunicações. 

Aplicação web em Django. Módulos necessários se encontram em requirements.txt

# Versão 0.2.1
#### atualizado em 27/03/2023


## Solicitações feitas: 
- Campos da frequência com valor 0 ficam com valor **None** automaticamente ao entrarem em foco. 
  - Foi pensado em utilizar placeholder.
  - Dificultava exclusão de fracção e divisão.
  - Melhorado com um javascript na opção onfocus.
- Novo valor padrão a cada fracção.
  - Toda nova fracção começa com divisões padrões pré definidas
  - Consequentemente, toda nova inspeção também.
- Campos do formulário passam a ficar todos na mesma linha também em telemóveis
em modo de visualização em retrato.
  - Essa mudança foi desaconselhada.
  - Agora existe uma barra de scroll inferior nos PCs.
  - Botões de nova_insp.html foram para a direita nos telemóveis.

## Mudanças de desenvolvimento
- Corrigir erro de refresh na primeira página da nova_insp.
  - Com as mudanças da última versão a primeira vez que se carregava
a página nova_insp.html perdia o valor no index de inspeção ao ser 
recarregada
  - A exclusão do valor da memória cash passa a só ocorrer com novos
POSTs.
- Javascript antigo para tratar o out foi retirado.
  - Não era ultilizado.
- Ajustar o nome da fração no modal.
  - Foi criado um javascript para que o modal de exclusão de fracção 
tenha nele inserido o nome da fracção atual, mesmo que ele não 
esteja na cache.
  - JQuery source passou a ser chamada no Script em base.html.
- Nos templates de Inspeção todos os scripts se encontram em base.
- Ajuste no layout dos botões em input_in.html, nova_insp.html e select_id.
  - Passam a estar separados por duas margens de *0.5.  


# Versão 0.2.0
#### atualizado em 20/03/2023


## Solicitações feitas: 

- Colocar os campos de cada divisão na mesma linha
  - Foi alterado no .forms. 
  - Antiga formatação segue comentada no ficheiro

- Trocar o nome secção para fracção
  - Feito somente para o front-end

- O número do processo passa a aparecer no seguinte padrão 000/2023	 
  - Feito somente para o front-end
  - Views, base de dados e todo o back-end consideram ainda como inteiro.

- Na introdução dos dados só deve aceitar valores com virgulas
  - O programa já aceita números com vírgula ou com pontos (Isso não foi alterado)
  - Os dados agora saem com vírgula no excel exportado pelo utilizador

- Na designação da Divisão deve aceitar mais texto Exº Sala [ZAP 1], Sala de Jantar
  - Foi mudada a quantidade de carácteres para 100 no nome das divisões

- Criar uma caixa Out na primeira linha de cada fração
  - Não estava no acordo inicial. 
  - Todas as novas Secções (agora fracções) tem sua primeira divisão chamada de 'Out'

- Criar uma caixa IN na primeira linha de cada inspeção
  - Não estava no acordo inicial. 
  - Foi criado um novo template para ser exibido no inicio de cada inspeção
  - Essas medidas são salvas com o sec_id igual a 0, já que esse não era utilizado anteriormente
  - Foi adicionada mais uma view para tratar essa nova entrada. 

- Na exportação para Exel o ficheiro deverá criar uma tabela cujo resultado deverá ser de acordo com o ficheiro anexo
  - Não estava no acordo inicial. 
  - A exportação passou de .csv para .xlsx.
  - Na view para o download do ficheiro foi acrescentada a operação desejada (diferença entre a linha e a IN recém adicionada)
  - Além disso o nome das colunas foi editado para o padrão utilizado e a nova tabela acrescentada com um intervalo de uma coluna entre as duas tabelas

- Possibilidade de se editar o nome da Secção pelo utilizador
  - Foio adicionado no template nova_insp um form só para se alterar o nome da secção (agora fracção). 
  - Essa entrada passa a ser salva no fim da cache, com isso todas as views que fazem o uso da cache foram alteradas para processar essa entrada.
  - Nome da secção também é exportada do ficheiro .xlsx

## Ficheiros alterados:

### Inspecao:
- .views
- .models
- .form
- .urls

#### Templates:
- nova_insp.html
- input_in.html
- select_id.html
- base.html

### Pages:

#### Templates:
- select_edit.html
- id_input.html
