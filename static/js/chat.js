// Xabarni chat maydoniga qo'shish funksiyasi
function addMessageToChat(message) {
    const chatArea = document.querySelector('.chat-area-main');

    // Yangi xabar divi yaratish
    const newMessageDiv = document.createElement('div');
    newMessageDiv.className = message.from_chat === 'user' ? 'chat-msg' : 'chat-msg owner';

    newMessageDiv.innerHTML = `
            <div class="chat-msg-profile">
                <div class="chat-msg-date">${ message.created_at }</div>
            </div>
            <div class="chat-msg-content">
                <div class="chat-msg-text">${ message.message_text }</div>
            </div>
    `;

    // Chat maydoniga xabarni qo'shish
    chatArea.appendChild(newMessageDiv);

    // Avtomatik scroll qilish
    chatArea.scrollTop = chatArea.scrollHeight;
}

// Xabarni yuborish funksiyasi
function sendMessage(csrfToken, userId) {
    const messageText = document.getElementById('message-textarea').value;

    // Xabar bo'sh emasligini tekshirish
    if (!messageText.trim()) {
        return;
    }

    // AJAX so'rovi orqali serverga yuborish
    fetch('/send_message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            message_text: messageText,
            user_id: userId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Xato:', data.error);
        } else {
            // Matn maydonini tozalash va xabarni qo'shish
            document.getElementById('message-textarea').value = '';
            addMessageToChat(data);
        }
    })
    .catch(error => {
        console.error('Xato:', error);
    });
}

// Sahifa yuklanganda avtomatik scroll
function scrollToBottom() {
    window.scrollTo(0, document.body.scrollHeight);
}

// Yangi xabarlarni olish funksiyasi
function fetchNewMessages(lastMessageId) {
    fetch(`/get_new_messages/?last_message_id=${lastMessageId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.messages && data.messages.length > 0) {
            data.messages.forEach(message => {
                addMessageToChat(message);
            });

            // Oxirgi xabar ID sini yangilash
            lastMessageId = data.messages[data.messages.length - 1].id;
        }
    })
    .catch(error => {
        console.error('Xato:', error);
    });

    // Har 5 soniyada yana yangi xabarlarni tekshirish
    setTimeout(() => fetchNewMessages(lastMessageId), 5000);
}

// Sahifa yuklanganda funksiyalarni ulash
document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const userId = document.getElementById('send-message-btn').getAttribute('data-user-id');
    let lastMessageId = 0; // Oxirgi ko'rilgan xabar ID si

    // Xabar yuborish tugmasiga voqea biriktirish
    document.getElementById('send-message-btn').addEventListener('click', function () {
        sendMessage(csrfToken, userId);
    });

    // Sahifa yuklanganda avtomatik scroll
    scrollToBottom();

    // Yangi xabarlarni tekshirishni boshlash
    fetchNewMessages(lastMessageId);
});