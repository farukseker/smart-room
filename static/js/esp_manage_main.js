new Vue({
    el:'#app',
    data:{
        connection: null,
        esp_list: []
    },
    methods: {
        send_key_change_status(key_id, status){
            this.connection.send(JSON.stringify({
                "type":"change_key_status_request",
                "key_id":key_id,
                "status":!status
            }))
        }
    },

    created: function() {
    var vm = this; // Store reference to the Vue instance

    console.log("Starting connection to WebSocket Server")

    var origin = document.location.origin.replace("https","wss").replace("http","ws")

    this.connection = new WebSocket(origin + "/ws/communication/user/")

    this.connection.onmessage = function(event) {
        console.log(event)

        var data = JSON.parse(event.data)
        console.log(data.esp_list)
        vm.esp_list = data.esp_list
        }

    this.connection.onopen = function(event) {
        var loader = document.getElementById('loader')
        loader.style = 'display: none'

        var view = document.getElementById('view')
        view.style = 'display: block'

        console.log(event)
        console.log("Successfully connected to the echo websocket server...")
    }
  }
});