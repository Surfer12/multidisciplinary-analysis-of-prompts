const OpenAI = require('openai');
const Anthropic = require('@anthropic-ai/sdk');

class AITool {
  constructor() {
    this.openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY || 'dummy-key'
    });

    this.anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY || 'dummy-key'
    });

    this.defaultModel = {
      openai: 'gpt-4',
      anthropic: 'claude-3-opus-20240229'
    };
  }

  async generateResponse({
    prompt,
    systemPrompt = null,
    temperature = 0.7,
    maxTokens = null,
    provider = 'anthropic'
  }) {
    try {
      if (provider === 'anthropic') {
        const response = await this.anthropic.messages.create({
          model: this.defaultModel.anthropic,
          max_tokens: maxTokens || 4096,
          temperature,
          messages: [
            ...(systemPrompt ? [{ role: 'system', content: systemPrompt }] : []),
            { role: 'user', content: prompt }
          ]
        });

        return {
          success: true,
          text: response.content[0].text,
          metadata: {
            provider: 'anthropic',
            model: this.defaultModel.anthropic,
            timestamp: new Date().toISOString()
          }
        };
      } else {
        const response = await this.openai.chat.completions.create({
          model: this.defaultModel.openai,
          temperature,
          max_tokens: maxTokens,
          messages: [
            ...(systemPrompt ? [{ role: 'system', content: systemPrompt }] : []),
            { role: 'user', content: prompt }
          ]
        });

        return {
          success: true,
          text: response.choices[0].message.content,
          metadata: {
            provider: 'openai',
            model: this.defaultModel.openai,
            timestamp: new Date().toISOString()
          }
        };
      }
    } catch (error) {
      return {
        success: false,
        error: error.message,
        metadata: {
          provider,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  async analyzeCode({
    code,
    analysisType = 'general',
    context = null,
    provider = 'anthropic'
  }) {
    const prompt = `
      Please analyze the following code${analysisType !== 'general' ? ` focusing on ${analysisType}` : ''}:

      \`\`\`
      ${code}
      \`\`\`

      ${context ? `Additional context: ${JSON.stringify(context)}` : ''}

      Please provide:
      1. A brief overview
      2. Key components and their purposes
      3. Potential improvements or issues
      4. Best practices assessment
    `;

    const systemPrompt = 'You are an expert code analyst. Provide clear, actionable insights.';

    return this.generateResponse({
      prompt,
      systemPrompt,
      temperature: 0.3,
      provider
    });
  }

  async enhanceDocumentation({
    code,
    docStyle = 'jsdoc',
    includeExamples = true,
    provider = 'anthropic'
  }) {
    const prompt = `
      Please enhance the documentation for the following code using ${docStyle} style:

      \`\`\`
      ${code}
      \`\`\`

      ${includeExamples ? 'Include practical examples for key functions.' : ''}
      Focus on:
      1. Function/method descriptions
      2. Parameter documentation
      3. Return value documentation
      4. Type information
      5. Usage examples (if requested)
    `;

    const systemPrompt = 'You are an expert technical writer. Provide clear, comprehensive documentation.';

    return this.generateResponse({
      prompt,
      systemPrompt,
      temperature: 0.2,
      provider
    });
  }

  async suggestImprovements({
    code,
    focusAreas = null,
    provider = 'anthropic'
  }) {
    const prompt = `
      Please suggest improvements for the following code${focusAreas ? ` focusing on: ${focusAreas.join(', ')}` : ''}:

      \`\`\`
      ${code}
      \`\`\`

      For each suggestion, provide:
      1. Description of the improvement
      2. Rationale
      3. Example implementation (if applicable)
      4. Impact assessment
    `;

    const systemPrompt = 'You are an expert code reviewer. Provide specific, actionable improvements.';

    return this.generateResponse({
      prompt,
      systemPrompt,
      temperature: 0.3,
      provider
    });
  }
}

module.exports = AITool;