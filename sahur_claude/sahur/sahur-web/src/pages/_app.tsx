import React from 'react'
import { ChakraProvider, extendTheme } from '@chakra-ui/react'
import { QueryClient, QueryClientProvider } from 'react-query'
import type { AppProps } from 'next/app'

const theme = extendTheme({
  colors: {
    brand: {
      50: '#e5f0ff',
      100: '#b8d3ff',
      200: '#8ab6ff',
      300: '#5c99ff',
      400: '#2e7cff',
      500: '#0063e6',
      600: '#004db4',
      700: '#003782',
      800: '#002252',
      900: '#000d22',
    },
  },
  fonts: {
    heading: 'Inter, system-ui, sans-serif',
    body: 'Inter, system-ui, sans-serif',
  },
})

// Create a client
const queryClient = new QueryClient()

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <QueryClientProvider client={queryClient}>
      <ChakraProvider theme={theme}>
        <Component {...pageProps} />
      </ChakraProvider>
    </QueryClientProvider>
  )
}

export default MyApp 