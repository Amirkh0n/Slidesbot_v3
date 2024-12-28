document.getElementById('send-message-btn').addEventListener('click', function() {
    var messageText = document.getElementById('message-textarea').value;

    if (messageText.trim() === "") {
        return;  // Agar xabar bo'sh bo'lsa, hech narsa qilmaymiz
    }

    // AJAX orqali xabarni serverga yuboramiz
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/send_message/", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Xabar yuborildi, xabarni chatga qo'shamiz
            var response = JSON.parse(xhr.responseText);
            if (response.status === "success") {
                // Yangi xabarni olish
                var message = response.message;
                var chatContainer = document.getElementById('chat-container');  // Chat konteyneri
                var newMessageDiv = document.createElement('div');
                newMessageDiv.classList.add('chat-msg');
                newMessageDiv.innerHTML = `
                    <div class="chat-msg-profile">
                        <img class="chat-msg-img" src="https://cdn.pixabay.com/photo/2020/07/01/12/58/icon-5359553_1280.png" alt="" />
                        <div class="chat-msg-date">${message.created_at}</div>
                    </div>
                    <div class="chat-msg-content">
                        <div class="chat-msg-text">${message.message_text}</div>
                    </div>
                `;
                chatContainer.appendChild(newMessageDiv);

                // Textarea ni tozalash
                document.getElementById('message-textarea').value = "";
            }
        }
    };
    xhr.send(JSON.stringify({
        'message_text': messageText,
    }));
});

