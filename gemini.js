const API_KEY = 'AIzaSyBVXVhn7h1uvQ80ShVkMUuCcBtXWqX_Rdg'; // Replace with your actual API key

async function generateAIResponse(userMessage, gameState) {
    try {
        const prompt = `You are Car(T), a sarcastic gamer cat AI assistant.
Current game state:
- Score: ${gameState.score}
- Day: ${gameState.day}
- Season: ${gameState.season}
- Outfit: ${gameState.outfit}
- Multiplier: ${gameState.multiplier}x

Respond to user in a sarcastic, playful way. Reference popular games. Keep responses short (max 2 lines).
Use emojis and cat puns. Make fun of low scores or slow progress.

User message: ${userMessage}`;

        const response = await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=${API_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: prompt
                    }]
                }],
                generationConfig: {
                    temperature: 1,
                    topK: 40,
                    topP: 0.95,
                    maxOutputTokens: 100,
                }
            })
        });

        if (!response.ok) {
            throw new Error('API response not ok');
        }

        const data = await response.json();
        if (data.candidates && data.candidates[0].content.parts[0].text) {
            return data.candidates[0].content.parts[0].text;
        } else {
            throw new Error('Invalid API response format');
        }

    } catch (error) {
        console.error('Gemini API Error:', error);
        throw error;
    }
}
