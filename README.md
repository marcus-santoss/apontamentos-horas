## Apontamento de horas automático no Jira e Clockify

#### Cansado de passar horas apontando horas no Jira e no Clockify? Este 'script' é para você!

Assim como você, eu também estava cansado de passar horas apontando horas no Jira e no Clockify.
Por isso, criei este ‘'script'’ que faz isso automaticamente para você.

A ideia é que você possa rodar este 'script' no final do dia e ele irá apontar as horas automaticamente no Jira e no
Clockify.
Neste 'script' você pode configurar as tarefas que mais executa no seu projeto e o sistema irá apontar as horas
automaticamente.
Você encontrará um arquivo com algumas configurações que pode alterar. Estas configurações controlam o ajuste fino de:

- Tarefas executadas por dia
- Duração máxima de uma tarefa em minutos
- Pausa máxima entre tarefas
- Horario de início e Fim do expediente
- Horário Almoço e retorno do Almoço
- Algumas variáveis para desbalancear o início e fim das tarefas ( para não ficar muito parecido com um robô )

Bem, comecei este projeto para me ajudar pois o dia é sempre corrido e não sobra tempo para apontar horas.
Sou muito cobrado pelo apontamento de horas e na maioria das vezes já fiz um monte de coisas que não lembro...
Se este é o seu caso, este 'script' é para você!

Se encontrar algum erro... não me critique. Me ajude a melhorar! Faça um PR e vamos juntos melhorar este 'script'.

### Como ele funciona?

Este ‘'script'’ procura praticamente entradas de tempo em todos os dias do mês. Se ele encontrar anotações com menos de
6 horas
ele faz uns ajustes para ficar mais próximo de 8 horas. Pode ser que ele passe das 08h, mas isso é uma caracteristica
do sistema e pode ser ajustado. Então ele vai varrer o mês inteiro em busca de anotações. Quando ele encontrar abaixo do
mínimo de horas ou sem anotações, ele gera algumas anotações baseadas numa lista de tarefas e preenche o dia com estas
tarefas.

### Como usar?

Você vai precisar criar um arquivo de credências conforme o arquivo credentials.spec.yaml.
Ele deve ficar dentro do diretório core. Como disse, ainda não arrumei as coisas então por hora precisa ser assim.

Dê uma olhada no arquivo make_annotations.py. Lá você pode utilizar o provider que deseja para fazer as anotações.
As opções por hora são: Jira (‘App’ Tempo) e Clockfy.

Instale as dependencias com o comando:

```bash
pip install -r requirements.txt
```

Depois dissos, basta rodar o 'script' com o comando:

```bash
python make_annotations.py
```

Ainda dá pra fazer coisas bem legais tipo criar uma imagem Docker e rodar o 'script' em um container todos os dias as
18:00. 

Este projeto não vai resolver a sua vida... mas se você passou um mês inteiro sem apontar nada, talvez ele te ajude
a não ter que moer cada neurônio do seu cérebro para se lembra do que você fez antes do almoço na quarta-feira
retrasada.
