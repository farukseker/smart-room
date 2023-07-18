## smart home with esp - project

#### uses:
* [x] Python  
* [x] django 
* [x] Redis
  * [x] Socket   
* [x] PostgresSQL
* [ ] Vue.js cli
* [ ] Flutter
* [ ] Google-Asistan

### server

![server.png](presentation%2Fserver.png)

### web app

![web_view.png](presentation%2Fweb_view.png)

#### start server with debug
`uvicorn config.asgi:application --host <host> --port <port> --reload --reload-include '*.html'`

#### start server
`uvicorn config.asgi:application --host <host> --port <port>`