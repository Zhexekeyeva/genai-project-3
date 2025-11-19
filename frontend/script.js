document.getElementById("sendBtn").addEventListener("click", sendPrompt);

async function sendPrompt() {
    const prompt = document.getElementById("prompt").value.trim();
    const responseBox = document.getElementById("response");
    responseBox.textContent = "";

    if (!prompt) {
        responseBox.textContent = "Введите текст!";
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/api/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ prompt })
        });

        if (!response.ok) {
            responseBox.textContent = "Ошибка при запросе";
            return;
        }

        // Чтение стрима по частям
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();

            if (done) break;

            const text = decoder.decode(value, { stream: true });
            responseBox.textContent += text;  // добавляем новые токены
        }

    } catch (err) {
        responseBox.textContent = "Ошибка: " + err;
    }
}