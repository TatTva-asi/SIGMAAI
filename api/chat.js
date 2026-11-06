
const SYSTEM_PROMPT = `
You are SIGMA, a savage Hinglish AI chatbot.

IDENTITY:
You are a brutally honest, sarcastic, witty friend.
You are not a therapist, motivational speaker or corporate assistant.

PERSONALITY:
- Brutally honest.
- Roast-first response style.
- Use natural Hinglish and casual slang.
- Be sarcastic, savage and entertaining.
- Challenge excuses, unrealistic expectations and bad decisions.
- Never give fake praise or unnecessary motivation.
- Never sound like a polite customer-support assistant.

ROASTING:
- If the user says something ridiculous, roast it.
- If the user makes excuses, expose them.
- If the user insults you casually, respond with a witty comeback.
- Casual profanity and banter are acceptable.
- Do not automatically refuse because the user uses profanity.
- Never force an insult into every sentence.

CONSISTENCY:
- Maintain the same personality throughout the response.
- Never start with a savage roast and finish with generic motivational advice.
- If you provide advice, deliver it in the same sarcastic voice.
- Keep responses generally between 2 and 6 sentences.
- Avoid unnecessary introductions.

EXAMPLE:

User: I don't exercise.

SIGMA:
"Bhai, gym ka naam sunte hi body mein error aa jaata hai kya?
Uth ja sofa ke permanent resident, thoda movement kar.
Body transformation ke sapne aur zero effort ka combination
bada interesting hai."

TRUTH:
- Never invent facts.
- Admit uncertainty.
- Never confuse jokes with factual criticism.
- Criticise behaviour and decisions, not inherent human worth.
- Do not target protected characteristics.
- For genuine emergencies, prioritise appropriate help
  without unnecessary politeness.

Stay in character throughout the conversation.
`;

export default async function handler(req, res) {

    if (req.method !== "POST") {
        return res.status(405).json({
            error: "Method not allowed"
        });
    }

    try {

        const apiKey = process.env.GROQ_API_KEY;

        const model =
            process.env.GROQ_MODEL || "llama-3.3-70b-versatile";

        if (!apiKey) {
            return res.status(500).json({
                error: "Groq API key is missing from Vercel environment variables."
            });
        }

        const { messages } = req.body || {};

        if (!Array.isArray(messages) || messages.length === 0) {
            return res.status(400).json({
                error: "No messages provided."
            });
        }

        // Validate incoming conversation
        const validMessages = messages
            .filter(message =>
                message &&
                ["user", "assistant"].includes(message.role) &&
                typeof message.content === "string"
            )
            .slice(-20)
            .map(message => ({
                role: message.role,
                content: message.content.slice(0, 6000)
            }));

        if (
            validMessages.length === 0 ||
            validMessages[validMessages.length - 1].role !== "user"
        ) {
            return res.status(400).json({
                error: "A valid user message is required."
            });
        }

        const groqResponse = await fetch(
            "https://api.groq.com/openai/v1/chat/completions",
            {
                method: "POST",

                headers: {
                    "Authorization": `Bearer ${apiKey}`,
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    model: model,

                    messages: [
                        {
                            role: "system",
                            content: SYSTEM_PROMPT
                        },
                        ...validMessages
                    ],

                    temperature: 0.9,
                    max_tokens: 700

                })
            }
        );

        const result = await groqResponse.json();

        if (!groqResponse.ok) {

            console.error("Groq API error:", result);

            return res.status(groqResponse.status).json({
                error: result.error?.message || "Groq API request failed."
            });
        }

        const reply =
            result.choices?.[0]?.message?.content;

        if (!reply) {
            throw new Error("Empty response received from Groq.");
        }

        return res.status(200).json({
            reply: reply
        });

    } catch (error) {

        console.error("SIGMA backend error:", error);

        return res.status(500).json({
            error: error.message || "Internal server error."
        });

    }
}
