// Cửa trung gian gọi Claude (Anthropic) API — chạy phía máy chủ Netlify để tránh CORS trình duyệt.
// App gọi /api/claude/message -> (redirect) -> hàm này -> Anthropic.
exports.handler = async (event) => {
  const JSON_HEADERS = { 'content-type': 'application/json; charset=utf-8' };
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers: JSON_HEADERS, body: JSON.stringify({ error: 'Chỉ chấp nhận POST' }) };
  }
  try {
    const { prompt, maxTokens, apiKey, model } = JSON.parse(event.body || '{}');
    const key = (apiKey || process.env.ANTHROPIC_API_KEY || process.env.CLAUDE_API_KEY || '').trim();
    if (!key) {
      return { statusCode: 400, headers: JSON_HEADERS, body: JSON.stringify({ error: 'Chưa có Claude API Key (nhập trong Cài đặt AI)' }) };
    }
    const resp = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-api-key': key,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: model || 'claude-opus-4-8',
        max_tokens: parseInt(maxTokens || 1024, 10),
        messages: [{ role: 'user', content: prompt || '' }],
      }),
    });
    const data = await resp.json();
    if (!resp.ok) {
      const msg = (data && data.error && data.error.message) || ('HTTP ' + resp.status);
      return { statusCode: 502, headers: JSON_HEADERS, body: JSON.stringify({ error: 'Claude API lỗi: ' + msg }) };
    }
    const text = (data.content || [])
      .filter((b) => b.type === 'text')
      .map((b) => b.text)
      .join('')
      .trim();
    return { statusCode: 200, headers: JSON_HEADERS, body: JSON.stringify({ text: text || '(Claude không trả về nội dung)' }) };
  } catch (e) {
    return { statusCode: 502, headers: JSON_HEADERS, body: JSON.stringify({ error: 'Lỗi kết nối Claude: ' + (e && e.message ? e.message : String(e)) }) };
  }
};
