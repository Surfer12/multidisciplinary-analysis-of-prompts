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

    this.models = {
      openai: {
        default: 'o1-2024-12-17',
        fallback: ['o3-mini-2025-01-31', 'gpt-4o-2024-05-13']
      },
      anthropic: {
        default: 'claude-3-5-sonnet-20241022',
        fallback: 'claude-3-5-haiku-20241022'
      }
    };

    this.reasoningTypes = {
      default: 'auto',
      types: [
        'auto',              // Let the model choose
        'step_by_step',      // Break down complex problems
        'tree_of_thought',   // Consider multiple paths
        'chain_of_thought',  // Show reasoning process
        'fast',              // Quick, direct responses
        'analytical',        // Detailed analysis
        'creative'           // Creative problem-solving
      ]
    };

    this.reasoningStrength = {
      openai: {
        default: 'high',
        levels: {
          high: {
            temperature: 0.7,
            top_p: 0.95,
            presence_penalty: 0.5,
            frequency_penalty: 0.5,
            best_of: 1
          },
          medium: {
            temperature: 0.5,
            top_p: 0.8,
            presence_penalty: 0.3,
            frequency_penalty: 0.3,
            best_of: 1
          },
          low: {
            temperature: 0.3,
            top_p: 0.6,
            presence_penalty: 0.1,
            frequency_penalty: 0.1,
            best_of: 1
          }
        }
      },
      anthropic: {
        default: 'medium',
        levels: {
          high: { temperature: 0.7 },
          medium: { temperature: 0.5 },
          low: { temperature: 0.3 }
        }
      }
    };

    this.responseFormats = {
      default: 'text',
      types: [
        'text',             // Plain text
        'json',             // JSON structure
        'markdown',         // Markdown formatting
        'code',             // Code-focused
        'structured'        // Custom structured format
      ]
    };
  }

  async generateResponse({
    prompt,
    systemPrompt = null,
    temperature = null,
    maxTokens = null,
    provider = 'anthropic',
    model = null,
    reasoningType = 'auto',
    responseFormat = 'text',
    reasoningStrength = null,
    extraParams = {}
  }) {
    try {
      // Validate and prepare reasoning type
      const validReasoningType = this.reasoningTypes.types.includes(reasoningType)
        ? reasoningType
        : this.reasoningTypes.default;

      // Validate and prepare response format
      const validResponseFormat = this.responseFormats.types.includes(responseFormat)
        ? responseFormat
        : this.responseFormats.default;

      // Get reasoning strength parameters
      const strength = reasoningStrength || this.reasoningStrength[provider].default;
      const strengthParams = this.reasoningStrength[provider].levels[strength];

      // Prepare system prompt with reasoning and format instructions
      const enhancedSystemPrompt = this._buildEnhancedSystemPrompt(
        systemPrompt,
        validReasoningType,
        validResponseFormat
      );

      if (provider === 'anthropic') {
        try {
          const response = await this.anthropic.messages.create({
            model: model || this.models.anthropic.default,
            max_tokens: maxTokens || 4096,
            temperature: temperature || strengthParams.temperature,
            messages: [
              ...(enhancedSystemPrompt ? [{ role: 'system', content: enhancedSystemPrompt }] : []),
              { role: 'user', content: prompt }
            ],
            ...extraParams
          });

          return {
            success: true,
            text: response.content[0].text,
            metadata: {
              provider: 'anthropic',
              model: model || this.models.anthropic.default,
              reasoningType: validReasoningType,
              responseFormat: validResponseFormat,
              reasoningStrength: strength,
              timestamp: new Date().toISOString()
            }
          };
        } catch (error) {
          if (!model && error.message.includes('model')) {
            console.log('Falling back to alternative Anthropic model...');
            return this.generateResponse({
              prompt,
              systemPrompt,
              temperature,
              maxTokens,
              provider,
              model: this.models.anthropic.fallback,
              reasoningType,
              responseFormat,
              reasoningStrength,
              extraParams
            });
          }
          throw error;
        }
      } else {
        let lastError;
        const modelsToTry = [
          model || this.models.openai.default,
          ...(!model ? this.models.openai.fallback : [])
        ];

        for (const currentModel of modelsToTry) {
          try {
            const response = await this.openai.chat.completions.create({
              model: currentModel,
              temperature: temperature || strengthParams.temperature,
              max_tokens: maxTokens,
              messages: [
                ...(enhancedSystemPrompt ? [{ role: 'system', content: enhancedSystemPrompt }] : []),
                { role: 'user', content: prompt }
              ],
              ...strengthParams,  // Apply all reasoning strength parameters
              ...extraParams     // Allow overriding with extra parameters
            });

            return {
              success: true,
              text: response.choices[0].message.content,
              metadata: {
                provider: 'openai',
                model: currentModel,
                reasoningType: validReasoningType,
                responseFormat: validResponseFormat,
                reasoningStrength: strength,
                timestamp: new Date().toISOString()
              }
            };
          } catch (error) {
            lastError = error;
            if (!error.message.includes('model')) {
              throw error;
            }
            console.log(`Model ${currentModel} failed, trying next model...`);
          }
        }
        throw lastError;
      }
    } catch (error) {
      return {
        success: false,
        error: error.message,
        metadata: {
          provider,
          model: model || (provider === 'anthropic' ? this.models.anthropic.default : this.models.openai.default),
          reasoningType,
          responseFormat,
          reasoningStrength,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  _buildEnhancedSystemPrompt(baseSystemPrompt, reasoningType, responseFormat) {
    const reasoningInstructions = {
      auto: '',
      step_by_step: 'Break down your reasoning into clear, sequential steps.',
      tree_of_thought: 'Consider multiple possible approaches and explore their implications before choosing the best path.',
      chain_of_thought: 'Show your complete reasoning process, explaining each logical connection.',
      fast: 'Provide direct, concise responses without detailed explanations.',
      analytical: 'Analyze the problem thoroughly, considering all relevant factors and potential implications.',
      creative: 'Approach the problem creatively, considering novel or unconventional solutions.'
    };

    const formatInstructions = {
      text: 'Provide your response in plain text.',
      json: 'Structure your response as a valid JSON object.',
      markdown: 'Format your response using Markdown syntax.',
      code: 'Focus on providing clean, well-commented code.',
      structured: 'Organize your response in a clear, structured format with sections and subsections.'
    };

    const instructions = [
      baseSystemPrompt,
      reasoningType !== 'auto' && reasoningInstructions[reasoningType],
      formatInstructions[responseFormat]
    ].filter(Boolean).join('\n\n');

    return instructions || null;
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