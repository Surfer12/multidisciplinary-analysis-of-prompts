const http = require('http');
const WebTool = require('../tools/web/web_tool');
const AITool = require('../tools/ai/ai_tool');

const webTool = new WebTool();
const aiTool = new AITool();

const server = http.createServer(async (req, res) => {
  if (req.method === 'POST') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });

    req.on('end', async () => {
      try {
        const { prompt, context = {}, url, code } = JSON.parse(body);
        let response;

        switch (req.url) {
          case '/v1/tools/llm_code_generate':
            response = await aiTool.generateResponse({
              prompt,
              context,
              provider: 'openai'
            });
            break;

          case '/v1/tools/web_request':
            response = await webTool.makeRequest(url, context);
            break;

          case '/v1/tools/web_scrape':
            response = await webTool.scrapeWebpage(url, context);
            break;

          case '/v1/tools/code_analyze':
            response = await aiTool.analyzeCode({
              code,
              ...context
            });
            break;

          case '/v1/tools/code_document':
            response = await aiTool.enhanceDocumentation({
              code,
              ...context
            });
            break;

          case '/v1/tools/code_improve':
            response = await aiTool.suggestImprovements({
              code,
              ...context
            });
            break;

          default:
            res.writeHead(404);
            res.end(JSON.stringify({ error: 'Tool not found' }));
            return;
        }

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(response));
      } catch (error) {
        console.error("Error:", error);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: "error", message: error.message }));
      }
    });
  } else {
    res.writeHead(404);
    res.end();
  }
});

const PORT = process.env.MCP_PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log('Available endpoints:');
  console.log('- POST /v1/tools/llm_code_generate');
  console.log('- POST /v1/tools/web_request');
  console.log('- POST /v1/tools/web_scrape');
  console.log('- POST /v1/tools/code_analyze');
  console.log('- POST /v1/tools/code_document');
  console.log('- POST /v1/tools/code_improve');
});