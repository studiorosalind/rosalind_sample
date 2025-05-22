import React, { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import { useQuery } from 'react-query'
import { NextPage } from 'next'
import Head from 'next/head'
import {
  Box,
  Container,
  Heading,
  Text,
  Button,
  Flex,
  Stack,
  Badge,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Spinner,
  Alert,
  AlertIcon,
  Divider,
  useColorModeValue,
  Code,
} from '@chakra-ui/react'
import { format } from 'date-fns'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { atomDark } from 'react-syntax-highlighter/dist/cjs/styles/prism'

// API client functions - would be in a separate file in a real app
const fetchIssue = async (id: string) => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/issues/${id}`)
  if (!response.ok) {
    throw new Error('Failed to fetch issue')
  }
  return response.json()
}

// WebSocket connection for real-time updates
const useIssueWebSocket = (issueId: string) => {
  const [messages, setMessages] = useState<any[]>([])
  const [status, setStatus] = useState<string | null>(null)
  const [solution, setSolution] = useState<any | null>(null)
  const [isConnected, setIsConnected] = useState(false)

  useEffect(() => {
    if (!issueId) return
    
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const wsUrl = `${apiUrl.replace('http://', 'ws://').replace('https://', 'wss://')}/api/issues/ws/${issueId}`
    const socket = new WebSocket(wsUrl)

    socket.onopen = () => {
      setIsConnected(true)
      console.log('WebSocket connected')
    }

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      console.log('WebSocket message:', data)

      if (data.type === 'message') {
        setMessages((prev) => [...prev, data])
      } else if (data.type === 'status') {
        setStatus(data.status)
      } else if (data.type === 'solution') {
        setSolution(data.solution)
      }
    }

    socket.onclose = () => {
      setIsConnected(false)
      console.log('WebSocket disconnected')
    }

    return () => {
      socket.close()
    }
  }, [issueId])

  return { messages, status, solution, isConnected }
}

// Status badge component
const StatusBadge = ({ status }: { status: string }) => {
  let color = 'gray'
  
  switch (status) {
    case 'new':
      color = 'blue'
      break
    case 'analyzing':
      color = 'orange'
      break
    case 'resolved':
      color = 'green'
      break
    case 'failed':
      color = 'red'
      break
  }
  
  return <Badge colorScheme={color}>{status}</Badge>
}

// Solution component
const Solution = ({ solution }: { solution: any }) => {
  if (!solution) return null;
  
  return (
    <Box mt={4} p={4} borderWidth={1} borderRadius="md">
      <Heading size="md" mb={2}>Solution</Heading>
      
      {solution.root_cause && (
        <Box mb={4}>
          <Heading size="sm" mb={2}>Root Cause</Heading>
          <Text>{solution.root_cause}</Text>
        </Box>
      )}
      
      {solution.explanation && (
        <Box mb={4}>
          <Heading size="sm" mb={2}>Explanation</Heading>
          <Text whiteSpace="pre-wrap">{solution.explanation}</Text>
        </Box>
      )}
      
      {solution.steps && solution.steps.length > 0 && (
        <Box mb={4}>
          <Heading size="sm" mb={2}>Steps</Heading>
          {solution.steps.map((step: any, index: number) => (
            <Box key={index} mt={4} p={3} borderWidth={1} borderRadius="md">
              <Heading size="xs" mb={2}>Step {step.step_number}: {step.description}</Heading>
              
              {step.code_changes && Object.entries(step.code_changes).map(([file, code]: [string, any], idx: number) => (
                <Box key={idx} mt={2}>
                  <Text fontWeight="bold" fontSize="sm" mb={1}>{file}</Text>
                  <SyntaxHighlighter language="java" style={atomDark}>
                    {code}
                  </SyntaxHighlighter>
                </Box>
              ))}
              
              {step.commands && step.commands.length > 0 && (
                <Box mt={2}>
                  <Text fontWeight="bold" fontSize="sm" mb={1}>Commands</Text>
                  <Code p={2} borderRadius="md" display="block" whiteSpace="pre">
                    {step.commands.join('\n')}
                  </Code>
                </Box>
              )}
            </Box>
          ))}
        </Box>
      )}
      
      {solution.references && solution.references.length > 0 && (
        <Box mt={4}>
          <Heading size="sm" mb={2}>References</Heading>
          <ul>
            {solution.references.map((ref: string, index: number) => (
              <li key={index}>{ref}</li>
            ))}
          </ul>
        </Box>
      )}
    </Box>
  );
};

const IssueDetailPage: NextPage = () => {
  const router = useRouter()
  const { id } = router.query
  const bgColor = useColorModeValue('gray.50', 'gray.900')
  
  const { data: issue, error, isLoading } = useQuery(
    ['issue', id],
    () => fetchIssue(id as string),
    {
      enabled: !!id,
    }
  )
  
  const { messages, status: wsStatus, solution, isConnected } = useIssueWebSocket(id as string)
  
  // Combine API status with WebSocket status
  const currentStatus = wsStatus || (issue?.status || 'unknown')
  
  if (isLoading) {
    return (
      <Container maxW="container.xl" py={10}>
        <Flex justify="center" align="center" h="50vh">
          <Spinner size="xl" />
        </Flex>
      </Container>
    )
  }
  
  if (error) {
    return (
      <Container maxW="container.xl" py={10}>
        <Alert status="error">
          <AlertIcon />
          Error loading issue. Please try again later.
        </Alert>
      </Container>
    )
  }
  
  return (
    <>
      <Head>
        <title>{issue?.title || 'Issue Detail'} - SAHUR</title>
        <meta name="description" content="Issue detail and tracking" />
      </Head>
      
      <Box as="main" bg={bgColor} minH="100vh">
        <Container maxW="container.xl" py={10}>
          {/* Header */}
          <Flex justify="space-between" align="center" mb={6}>
            <Box>
              <Button 
                variant="link" 
                mb={2} 
                onClick={() => router.push('/issues')}
              >
                &larr; Back to issues
              </Button>
              <Heading as="h1" size="xl">{issue?.title}</Heading>
              <Flex mt={2} align="center">
                <Text mr={2}>Status:</Text>
                <StatusBadge status={currentStatus} />
                {isConnected && (
                  <Badge ml={2} colorScheme="green">Live</Badge>
                )}
              </Flex>
            </Box>
            <Box>
              <Text fontSize="sm">Created: {issue?.created_at ? format(new Date(issue.created_at), 'PPP') : 'N/A'}</Text>
              <Text fontSize="sm">Last Updated: {issue?.updated_at ? format(new Date(issue.updated_at), 'PPP') : 'N/A'}</Text>
            </Box>
          </Flex>
          
          <Divider my={6} />
          
          {/* Content */}
          <Tabs>
            <TabList>
              <Tab>Details</Tab>
              <Tab>Analysis Log</Tab>
              <Tab>Solution</Tab>
            </TabList>
            
            <TabPanels>
              {/* Details Tab */}
              <TabPanel>
                <Stack spacing={6}>
                  <Box>
                    <Heading size="md" mb={2}>Description</Heading>
                    <Text>{issue?.description}</Text>
                  </Box>
                  
                  {issue?.error_message && (
                    <Box>
                      <Heading size="md" mb={2}>Error Message</Heading>
                      <Code p={3} borderRadius="md" display="block" whiteSpace="pre">
                        {issue.error_message}
                      </Code>
                    </Box>
                  )}
                  
                  {issue?.stack_trace && (
                    <Box>
                      <Heading size="md" mb={2}>Stack Trace</Heading>
                      <SyntaxHighlighter language="java" style={atomDark}>
                        {issue.stack_trace}
                      </SyntaxHighlighter>
                    </Box>
                  )}
                </Stack>
              </TabPanel>
              
              {/* Analysis Log Tab */}
              <TabPanel>
                <Stack spacing={4}>
                  {messages.length === 0 ? (
                    <Text>No analysis logs available yet.</Text>
                  ) : (
                    messages.map((message, index) => (
                      <Box key={index} p={3} borderWidth={1} borderRadius="md"
                           bg={message.role === 'user' ? 'blue.50' : message.role === 'system' ? 'gray.50' : 'green.50'}>
                        <Text fontWeight="bold" mb={1} color={message.role === 'user' ? 'blue.600' : 
                                                            message.role === 'system' ? 'gray.600' : 'green.600'}>
                          {message.role === 'user' ? 'User' : 
                           message.role === 'system' ? 'System' : 'Assistant'}
                        </Text>
                        <Text whiteSpace="pre-wrap">{message.content}</Text>
                      </Box>
                    ))
                  )}
                </Stack>
              </TabPanel>
              
              {/* Solution Tab */}
              <TabPanel>
                {solution ? (
                  <Solution solution={solution} />
                ) : issue?.solution ? (
                  <Solution solution={issue.solution} />
                ) : (
                  <Text>No solution available yet.</Text>
                )}
              </TabPanel>
            </TabPanels>
          </Tabs>
        </Container>
      </Box>
    </>
  )
}

export default IssueDetailPage 

// This function gets called at build time on server-side.
// It may be called again, on a serverless function, if
// revalidation is enabled and a new request comes in
export async function getStaticProps({ params }: { params: { id: string } }) {
  return {
    props: {
      // We don't need to pass any props since we'll fetch the data on the client
      id: params.id,
    },
    // Re-generate the post at most once per 10 seconds
    // if a request comes in
    revalidate: 10, // seconds
  }
}

// This function gets called at build time on server-side.
// It defines which paths will be pre-rendered.
export async function getStaticPaths() {
  return {
    // Only pre-render the homepage at build time
    // All other pages will be generated at runtime
    paths: [],
    // { fallback: false } means other routes should 404.
    // { fallback: true } means it will generate on-demand.
    // { fallback: 'blocking' } means it will generate server-side
    // on first request and then cache it.
    fallback: 'blocking',
  }
} 