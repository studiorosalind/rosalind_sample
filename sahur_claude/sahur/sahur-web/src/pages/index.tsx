import { Box, Container, Heading, Text, Button, Stack, useColorModeValue } from '@chakra-ui/react'
import { NextPage } from 'next'
import Head from 'next/head'
import { useRouter } from 'next/router'

const Home: NextPage = () => {
  const router = useRouter()
  const bgColor = useColorModeValue('gray.50', 'gray.900')
  
  return (
    <>
      <Head>
        <title>SAHUR - Smart AI-powered Help for Understanding and Resolving</title>
        <meta name="description" content="SAHUR - Smart AI-powered Help for Understanding and Resolving" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <Box as="main" bg={bgColor} minH="100vh">
        <Container maxW="container.xl" py={10}>
          <Stack spacing={8} direction="column" align="center" textAlign="center">
            <Heading as="h1" size="2xl">
              SAHUR
            </Heading>
            <Text fontSize="xl">
              Smart AI-powered Help for Understanding and Resolving
            </Text>
            <Box maxW="container.md">
              <Text>
                SAHUR is an intelligent system that helps developers understand and resolve
                technical issues by analyzing error messages, logs, and code snippets using
                AI-powered contextual understanding.
              </Text>
            </Box>
            <Stack direction="row" spacing={4}>
              <Button 
                colorScheme="brand" 
                size="lg"
                onClick={() => router.push('/issues')}
              >
                View Issues
              </Button>
              <Button 
                variant="outline" 
                colorScheme="brand" 
                size="lg"
                onClick={() => router.push('/new-issue')}
              >
                Create New Issue
              </Button>
            </Stack>
          </Stack>
        </Container>
      </Box>
    </>
  )
}

export default Home 