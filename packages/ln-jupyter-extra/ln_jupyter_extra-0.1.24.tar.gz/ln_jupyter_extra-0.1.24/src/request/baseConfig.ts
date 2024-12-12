/**
 * axios 基础配置
 */
import type { AxiosRequestConfig } from 'axios';
const domain = window.location.origin;

export const baseConfig: AxiosRequestConfig = {
  baseURL: domain, // baseUrl
  timeout: 60000 // 超时时间
};
