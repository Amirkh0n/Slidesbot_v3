// ==================== DOM bilan ishlash funksiyalari ====================
function getElement(id) {
    return document.getElementById(id);
}

function scrollToBottom() {
    const chatArea = document.querySelector('.chat-area-main');
    chatArea.scrollTop = chatArea.scrollHeight;
}

// ==================== Xabarlarni qo‘shish funksiyasi ====================
function addMessageToChat(message) {
    const chatArea = document.querySelector('.chat-area-main');
    const newMessageDiv = document.createElement('div');
    newMessageDiv.className = message.from_chat === 'user' ? 'chat-msg' : 'chat-msg owner';

    let content = '';
    if (message.message_type === 'photo') {
        content = `
            <div class="chat-msg-text">
                <img src="${message.get_file_url}" loading="lazy" /><br>
                ${message.message_text || ''}
            </div>
        `;
    } else if (message.message_type === 'file') {
        content = `
            <div class="chat-msg-text">
                <h3><a href="${message.get_file_url}">Document</a></h3><br>
                ${message.message_text || ''}
            </div>
        `;
    } else {
        content = `<div class="chat-msg-text">${message.message_text || ''}</div>`;
    }

    newMessageDiv.innerHTML = `
        <div class="chat-msg-profile">
            <div class="chat-msg-date">${message.created_at}</div>
        </div>
        <div class="chat-msg-content">${content}</div>
    `;
    chatArea.appendChild(newMessageDiv);
    scrollToBottom();
}

// ==================== API bilan ishlash funksiyalari ====================
async function fetchNewMessages(lenMsg) {
    const userId = getElement('send-message-btn').getAttribute('data-user-id');

    try {
        const response = await fetch(`/get_new_messages/?len_msg=${lenMsg}&user_id=${userId}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        });
        if (!response.ok) throw new Error('Serverdan noto‘g‘ri javob keldi');

        const data = await response.json();
        if (data.have_new) {
            
            // const messages = JSON.parse(data.messages);
            
            // alert("noArray:"+ typeof messages.fields+typeof data);
            data.messages.forEach(message => addMessageToChat(message.fields));
            //alert('Yangi xabarlar keldi: ' + JSON.stringify(data)); // Yangi xabarlar uchun alert
            
            return lenMsg + data.messages.length;
        }
    } catch (error) {
        console.error('Xato:', error);
    }
    return lenMsg;
}

async function sendMessage(csrfToken, userId) {
    const messageText = getElement('message-textarea').value.trim();
    if (!messageText) return;

    try {
        const response = await fetch('/send_message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ message_text: messageText, user_id: userId }),
        });
        const data = await response.json();
        if (!data.error) {
            getElement('message-textarea').value = '';
            // addMessageToChat(data);
        } else {
            console.error('Xato:', data.error);
        }
    } catch (error) {
        console.error('Xatolik:', error);
    }
}

async function uploadFile(inputElement, apiUrl, chatId, callback) {
    const file = inputElement.files[0];
    if (!file) {
        alert('Iltimos, faylni tanlang!');
        return;
    }

    const formData = new FormData();
    formData.append('chat_id', chatId);
    formData.append('document', file);

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            body: formData,
        });
        const result = await response.json();
        if (result.ok && callback) callback(result);
    } catch (error) {
        console.error('Fayl yuklashda xatolik:', error);
        alert('Xatolik yuz berdi, qayta urinib ko‘ring.');
    }
}

// ==================== Hodisalar boshqaruvi ====================
document.addEventListener('DOMContentLoaded', () => {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const userId = getElement('send-message-btn').getAttribute('data-user-id');
    let lenMsg = Number(getElement('send-message-btn').getAttribute('data-len_msg'));

    // Xabar yuborish hodisasi
    getElement('send-message-btn').addEventListener('click', () => {
        sendMessage(csrfToken, userId);
    });

    // Fayl yuklash hodisasi
    const fileInput = getElement('fileInput');
    getElement('fileInputDiv').addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (event) => {
        const token = '5901209945:AAGQqHQmo5xOk-zlWYZJrNQOH48N8FmGoKU';
        const apiUrl = `https://api.telegram.org/bot${token}/sendDocument`;

        uploadFile(event.target, apiUrl, userId, (result) => {
            postToServer(result.result.message_id, result.result.document.file_id, userId);
        });
    });

    // Rasm yuklash hodisasi
    const imageInput = getElement('imageInput');
    getElement('imageInputDiv').addEventListener('click', () => imageInput.click());
    imageInput.addEventListener('change', (event) => {
        console.log('Yuklangan rasm:', event.target.files[0]);
    });

    // Yangi xabarlarni yuklash
    (async function pollNewMessages() {
        lenMsg = await fetchNewMessages(lenMsg);
        setTimeout(pollNewMessages, 1000);
    })();

    // Sahifa yuklanganda avtomatik scroll
    scrollToBottom();
});

// ==================== Serverga yuborish funksiyasi ====================
async function postToServer(messageId, fileId, userId) {
    const data = { message_id: messageId, file_id: fileId, user_id: userId };

    try {
        const response = await fetch('/send_file/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        if (response.ok) {
            console.log('Server javobi:', result);
        } else {
            console.error('Xato:', result);
        }
    } catch (error) {
        console.error('Xatolik yuz berdi:', error);
    }
}