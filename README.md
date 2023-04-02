# Congresso em Texto

Ferramental para extração de discursos oriundos do Congresso Nacional brasileiro.

## Como rodar esse projeto

### Dependências
- Docker (veja como instalá-lo por [aqui](https://docs.docker.com/get-docker/)) 

### Comandos
1. Build da imagem do Docker

    ```sh
    docker build -t congresso-em-texto:latest .
    ```

2. Iniciar o container
    ```sh
    docker run -d --name congresso-container -v /data/:/app/data/* congresso-em-texto
    ```
    - Aqui, além do container, nós criamos um volume do Docker. Os dados extraídos ficarão salvos
    no host na pasta /data, na raiz do projeto.
 
Se tudo ocorrer bem, um container com nome `congresso-container` será criado. Você pode checar isso executando: 

 ```sh
 docker ps | grep congresso-container
 ```

