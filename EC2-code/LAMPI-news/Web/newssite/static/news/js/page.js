document.addEventListener("DOMContentLoaded", function() {
    const reconnectInterval = 3000;
    const brokerUrl = "34.207.111.28";
    const brokerPort = 50002;
    const clientId = "clientId" + new Date().getTime();
    let client = new Paho.MQTT.Client(brokerUrl, brokerPort, clientId);

    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    function initializeClient() {
        client.connect({
            onSuccess: onConnect,
            onFailure: onConnectFailure,
            useSSL: false,
        });
    }

    function onConnect() {
        console.log("Connected to WebSocket port " + brokerPort);
        client.subscribe("web/news");
    }

    function onConnectFailure(responseObject) {
        console.error("Connection failed: " + responseObject.errorMessage);
        setTimeout(initializeClient, reconnectInterval);
    }

    function onConnectionLost(responseObject) {
        if (responseObject.errorCode !== 0) {
            console.log("Connection lost:", responseObject.errorMessage);
            setTimeout(initializeClient, reconnectInterval);
        }
    }

    function onMessageArrived(message) {
        let newsItem = JSON.parse(message.payloadString);
        addNewsItem(newsItem);
    }

    function addNewsItem(newsItem) {
        if (!document.getElementById(`news-item-${newsItem.id}`)) {
            let li = document.createElement("li");
            li.id = `news-item-${newsItem.id}`;
            li.innerHTML = `<a href="${newsItem.url}" target="_blank">${newsItem.title}</a> <button class="delete-button" data-id="${newsItem.id}">Delete</button>`;
            document.getElementById("newsList").appendChild(li);
        } else {
            console.log('Duplicate message received, ignoring.');
        }
    }
    document.getElementById('newsList').addEventListener('click', function(event) {
        if (event.target.classList.contains('delete-button')) {
            deleteItem(event.target.dataset.id);
        }
    });

    function deleteItem(id) {
        fetch(`/news/delete/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: id })
        }).then(response => response.json())
          .then(data => {
              if (data.status === 'success') {
                  const item = document.getElementById(`news-item-${id}`);
                  if (item) {
                      item.remove();
                  }
              } else {
                  console.error('Delete failed:', data.message);
              }
          }).catch(error => console.error('Error:', error));
    }

    function getCSRFToken() {
        let cookies = document.cookie.split(';');
        let token = cookies.find(c => c.trim().startsWith('csrftoken='));
        return token ? token.split('=')[1] : 'unknown';
    }

    initializeClient();
});
