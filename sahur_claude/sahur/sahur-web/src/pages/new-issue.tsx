import React, { useState } from 'react'
import { useMutation } from 'react-query'
import { useRouter } from 'next/router'
import { NextPage } from 'next'
import Head from 'next/head'
import {
  Box,
  Container,
  Heading,
  Text,
  Button,
  FormControl,
  FormLabel,
  FormErrorMessage,
  Input,
  Textarea,
  Stack,
  useToast,
  useColorModeValue,
  Alert,
  AlertIcon,
} from '@chakra-ui/react'

interface IssueFormData {
  title: string;
  description: string;
  error_message?: string;
  stack_trace?: string;
}

const createIssue = async (data: IssueFormData) => {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/issues`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  
  if (!response.ok) {
    throw new Error('Failed to create issue')
  }
  
  return response.json()
}

const NewIssuePage: NextPage = () => {
  const router = useRouter()
  const toast = useToast()
  const bgColor = useColorModeValue('gray.50', 'gray.900')
  
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [errorMessage, setErrorMessage] = useState('')
  const [stackTrace, setStackTrace] = useState('')
  
  const createIssueMutation = useMutation(createIssue, {
    onSuccess: (data) => {
      toast({
        title: 'Issue created.',
        description: 'Your issue has been created successfully.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      })
      router.push(`/issues/${data.id}`)
    },
    onError: (error: any) => {
      toast({
        title: 'Error creating issue.',
        description: 'There was an error creating your issue. Please try again.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
    },
  })
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!title || !description) {
      toast({
        title: 'Validation error.',
        description: 'Title and description are required.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
      return
    }
    
    createIssueMutation.mutate({
      title,
      description,
      error_message: errorMessage,
      stack_trace: stackTrace,
    })
  }
  
  return (
    <>
      <Head>
        <title>New Issue - SAHUR</title>
        <meta name="description" content="Submit a new issue for analysis" />
      </Head>
      
      <Box as="main" bg={bgColor} minH="100vh">
        <Container maxW="container.md" py={10}>
          <Box mb={6}>
            <Button 
              variant="link" 
              mb={2} 
              onClick={() => router.push('/issues')}
            >
              &larr; Back to issues
            </Button>
            <Heading as="h1" size="xl">Create New Issue</Heading>
            <Text mt={2}>Submit a technical problem for SAHUR to analyze and resolve.</Text>
          </Box>
          
          <Box as="form" onSubmit={handleSubmit}>
            <Stack spacing={6}>
              <FormControl isRequired>
                <FormLabel>Issue Title</FormLabel>
                <Input 
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="E.g., NullPointerException in UserService.processRequest"
                />
              </FormControl>
              
              <FormControl isRequired>
                <FormLabel>Description</FormLabel>
                <Textarea 
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Describe the issue and when it occurs..."
                  rows={4}
                />
              </FormControl>
              
              <FormControl>
                <FormLabel>Error Message</FormLabel>
                <Textarea 
                  value={errorMessage}
                  onChange={(e) => setErrorMessage(e.target.value)}
                  placeholder="Paste the exact error message..."
                  rows={3}
                />
              </FormControl>
              
              <FormControl>
                <FormLabel>Stack Trace</FormLabel>
                <Textarea 
                  value={stackTrace}
                  onChange={(e) => setStackTrace(e.target.value)}
                  placeholder="Paste the stack trace here..."
                  rows={8}
                  fontFamily="monospace"
                />
              </FormControl>
              
              <Button 
                type="submit" 
                colorScheme="brand" 
                size="lg"
                isLoading={createIssueMutation.isLoading}
                loadingText="Submitting"
              >
                Submit Issue
              </Button>
            </Stack>
          </Box>
        </Container>
      </Box>
    </>
  )
}

export default NewIssuePage 