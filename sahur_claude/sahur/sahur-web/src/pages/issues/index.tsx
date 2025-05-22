import React, { useState } from 'react'
import { useQuery } from 'react-query'
import { NextPage } from 'next'
import Head from 'next/head'
import { useRouter } from 'next/router'
import {
  Box,
  Container,
  Heading,
  Text,
  Button,
  Flex,
  Stack,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  useColorModeValue,
  Spinner,
  Alert,
  AlertIcon,
} from '@chakra-ui/react'
import { format } from 'date-fns'

// API client - would be in a separate file in a real app
const fetchIssues = async () => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/issues`)
  if (!response.ok) {
    throw new Error('Failed to fetch issues')
  }
  return response.json()
}

type IssueStatus = 'new' | 'analyzing' | 'resolved' | 'failed'

interface Issue {
  id: string
  title: string
  status: IssueStatus
  created_at: string
  updated_at: string
}

const getStatusColor = (status: IssueStatus) => {
  switch (status) {
    case 'new':
      return 'blue'
    case 'analyzing':
      return 'orange'
    case 'resolved':
      return 'green'
    case 'failed':
      return 'red'
    default:
      return 'gray'
  }
}

const IssuesPage: NextPage = () => {
  const router = useRouter()
  const { data, error, isLoading } = useQuery<Issue[]>('issues', fetchIssues)
  const bgColor = useColorModeValue('gray.50', 'gray.900')
  
  return (
    <>
      <Head>
        <title>Issues - SAHUR</title>
        <meta name="description" content="View and manage your issues" />
      </Head>
      
      <Box as="main" bg={bgColor} minH="100vh">
        <Container maxW="container.xl" py={10}>
          <Flex justify="space-between" align="center" mb={6}>
            <Heading as="h1" size="xl">Issues</Heading>
            <Button 
              colorScheme="brand" 
              onClick={() => router.push('/new-issue')}
            >
              Create New Issue
            </Button>
          </Flex>
          
          {isLoading ? (
            <Flex justify="center" p={10}>
              <Spinner size="xl" />
            </Flex>
          ) : error ? (
            <Alert status="error">
              <AlertIcon />
              Error loading issues. Please try again later.
            </Alert>
          ) : !data || data.length === 0 ? (
            <Box textAlign="center" p={10} borderWidth={1} borderRadius="lg">
              <Text mb={4}>No issues found.</Text>
              <Button 
                colorScheme="brand" 
                onClick={() => router.push('/new-issue')}
              >
                Create Your First Issue
              </Button>
            </Box>
          ) : (
            <Box overflowX="auto">
              <Table variant="simple">
                <Thead>
                  <Tr>
                    <Th>ID</Th>
                    <Th>Title</Th>
                    <Th>Status</Th>
                    <Th>Created</Th>
                    <Th>Last Updated</Th>
                    <Th>Actions</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {data.map((issue) => (
                    <Tr key={issue.id}>
                      <Td>{issue.id.substring(0, 8)}</Td>
                      <Td>{issue.title}</Td>
                      <Td>
                        <Badge colorScheme={getStatusColor(issue.status)}>
                          {issue.status}
                        </Badge>
                      </Td>
                      <Td>{format(new Date(issue.created_at), 'MMM d, yyyy')}</Td>
                      <Td>{format(new Date(issue.updated_at), 'MMM d, yyyy')}</Td>
                      <Td>
                        <Button
                          size="sm"
                          onClick={() => router.push(`/issues/${issue.id}`)}
                        >
                          View
                        </Button>
                      </Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            </Box>
          )}
        </Container>
      </Box>
    </>
  )
}

export default IssuesPage 