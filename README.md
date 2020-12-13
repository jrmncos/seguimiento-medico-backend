# Software de seguimiento medico

Descripcion: El proyecto requiere tener Docker y Docker-Compose instalado en su sistema Operativo.
Docker: https://docs.docker.com/engine/install/
Docker-compose: https://docs.docker.com/compose/install/
## Instalacion
- git clone https://github.com/jrmncos/seguimiento-medico-backend.git
- cd seguimiento-medico-backend
- docker-compose up

## Puesta en marcha
- Para crear un superusuario: *`docker exec -it CONTAINER_ID python3 manage.py createsuperuser`*
	-- Docker ps y ver el container id de *seguimientomedico_web* 
- Para inicializar el servidor de autenticacion: Ir a la url `locahost:8080/o/applications/`
	-- Logearse con la cuenta de superusuario
	--  New application
	-- Name: react-native ; Client Type: Public; Authorization grant type: Resource owner passsword-based
	-- Save (**No olvidarse guardar el Client Secret**)