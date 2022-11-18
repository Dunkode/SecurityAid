# SecurityAid


**Informações:**  

**Repositório criado para a Atividade Avaliativa - Projeto Computer Vision Full.**  
**Universidade:** Atitus Educação – Passo Fundo/RS  
**Disciplina:** Computação Gráfica  
**Professor:** Marcos Roberto dos Santos  
**Alunos:** Éderson Vidal Junior e Vitalino Pitt  


**Descrição:**  
A internação em hospital é um momento delicado para o paciente apresentando-se como um momento delicado em sua vida.  Isolado dos seus vínculos sociais, o paciente torna-se “dependente” dos cuidados da equipe hospitalar.  
É comprovado e pode verificar a importância do acompanhante e da visita para o paciente internado no hospital, sendo elas, estratégias relacionadas à promoção da sua saúde.  
Acompanhantes e visitantes apresentam-se como a rede de apoio familiar e social ao paciente, porém, é comum em grandes hospitais que estes perdem-se no labirinto de corredores e setores.  Juntando-se a isso encontram-se casos de pessoas mal “intencionadas” que podem estar ali para pequenos furtos ou outras práticas maliciosas. 
Frente a essa realidade, buscou-se através desse projeto, evitar que pessoas circulem por setores sem autorização.  Através deste a equipe hospitalar pode auxiliar e monitorar as pessoas, facilitando o acesso rápido aos pacientes e evitando que elas circulem desnecessariamente pelo hospital.  


**Projeto:**  
O projeto tem como finalidade automatizar o monitoramento de visitantes e acompanhantes através do cadastro de reconhecimento facial, cor do crachá e identificar se este está ou não no setor autorizado durante a visita.  Caso não esteja, será enviada uma notificação via Telegram, com o nome, foto da pessoa, data e hora do registro.   


**Requisitos:**  
* Técnicas de processamento de imagens como redimensionamento, recorte e mudança de cores:  Ao cadastrar o visitante / acompanhante é salvo uma imagem com o nome deste para posterior técnica de reconhecimento facial.  
* HaarCascade: Utilizado no reconhecimento do visitante/acompanhante e na identificação da cor crachá. É usado o HaarCascade disponibilizado pela biblioteca face_recognition.
* Log: Serão geradas informações (nome do visitante, foto, data, hora do registro e permissão no local do registro) e arquivadas para posterior encaminhamento via Telegram.  
* Identificação facial: Utilizado na hora do cadastro de visitantes/acompanhantes e na hora de identificar se os mesmos estão ou não no setor autorizado para visita.  
* Aplicado técnicas de binarização e detecção de bordas, aplicando correção morfológica nas imagens: Essas técnicas são utilizadas para descobrir qual a cor do crachá que o visitante está usando, onde é selecionado um Ponto de Interesse logo abaixo de seu rosto, e são aplicadas técnicas de detecção de bordas e binarização para identificar a cor usada.
* Incluído skill referente a seleção de objetos por cores, o qual determina se o visitante está no setor autorizado.


**Imagens:**  
Na pasta “prints” será possível encontrar as imagens citadas abaixo, comprovando algumas funcionalidades do projeto.  
* Análise das cores - Amarelo;  
* Análise das cores - Azul;  
* Análise das cores - Verde;  
* Análise das cores - Vermelho;  
* Área de interesse;  
* Identificação do rosto e seleção da área de interesse;  
* Mensagem de alerta de pessoa não autorizada;  
* Pessoa reconhecida e autorizada;  
* Pessoa reconhecida e com cor não autorizada;  
* Pessoa reconhecida e não autorizada;  


**Bibliotecas Utilizadas:**  
anyio==3.6.2  
APScheduler==3.9.1  
asyncio==3.4.3  
cachetools==5.2.0  
certifi==2022.9.24  
charset-normalizer==2.1.1  
click==8.1.3  
cmake==3.24.1.1  
cmake-build-extension==0.5.1  
colorama==0.4.6  
dlib==19.24.0  
face-recognition==1.3.0  
face-recognition-models==0.3.0  
gitdb==4.0.9  
GitPython==3.1.29  
h11==0.12.0  
httpcore==0.15.0  
httpx==0.23.0  
idna==3.4  
ninja==1.10.2.4  
numpy==1.23.4
opencv-python==4.6.0.66  
packaging==21.3  
Pillow==9.2.0  
pyparsing==3.0.9  
pytz==2022.5  
pytz-deprecation-shim==0.1.0.post0  
requests==2.28.1  
rfc3986==1.5.0  
schedule==1.1.0  
setuptools-scm==7.0.5  
six==1.16.0  
smmap==5.0.0  
sniffio==1.3.0  
tomli==2.0.1  
tornado==6.2  
typing_extensions==4.4.0  
tzdata==2022.6  
tzlocal==4.2  
urllib3==1.26.12  
