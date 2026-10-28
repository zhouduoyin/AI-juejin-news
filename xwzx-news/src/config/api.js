/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // API地址 (Anthropic Messages API)
  apiEndpoint: 'http://192.168.0.55/v1/messages',

  // API Key 通过环境变量注入（VITE_AI_API_KEY），不要提交真实 Key
  apiKey: import.meta.env.VITE_AI_API_KEY ?? 'your-api-key-here',

  // 使用的模型
  model: 'deepseek-v4-pro',

  // 最大输出token数
  maxTokens: 4096
}
