declare module 'react-syntax-highlighter' {
  import { ReactNode } from 'react';
  
  export const Prism: React.ComponentType<{
    children: ReactNode;
    language?: string;
    style?: any;
    [key: string]: any;
  }>;
}

declare module 'react-syntax-highlighter/dist/cjs/styles/prism' {
  export const atomDark: any;
  export const materialLight: any;
  export const materialDark: any;
  export const prism: any;
  export const okaidia: any;
  export const tomorrow: any;
  export const solarizedlight: any;
  export const vs: any;
} 