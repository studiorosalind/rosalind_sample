#!/bin/bash

# SAHUR Demonstration Script
# This script demonstrates how to use the SAHUR system

# Set colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print section headers
print_header() {
  echo -e "\n${BLUE}==== $1 ====${NC}\n"
}

# Function to print success messages
print_success() {
  echo -e "${GREEN}✓ $1${NC}"
}

# Function to print info messages
print_info() {
  echo -e "${YELLOW}ℹ $1${NC}"
}

# Function to print error messages
print_error() {
  echo -e "${RED}✗ $1${NC}"
}

# Check if Docker and Docker Compose are installed
check_prerequisites() {
  print_header "Checking Prerequisites"
  
  if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
  else
    print_success "Docker is installed."
  fi
  
  if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
  else
    print_success "Docker Compose is installed."
  fi
}

# Set up environment
setup_environment() {
  print_header "Setting Up Environment"
  
  if [ ! -f .env ]; then
    print_info "Creating .env file from .env.example"
    cp .env.example .env
    print_success "Created .env file."
  else
    print_info ".env file already exists."
  fi
}

# Build and start the services
start_services() {
  print_header "Starting Services"
  
  print_info "Building and starting Docker containers..."
  docker-compose up -d --build
  
  if [ $? -eq 0 ]; then
    print_success "Services started successfully."
  else
    print_error "Failed to start services."
    exit 1
  fi
  
  # Wait for services to be ready
  print_info "Waiting for services to be ready..."
  sleep 10
}

# Simulate a Slack event
simulate_slack_event() {
  print_header "Simulating Slack Event"
  
  print_info "Sending a simulated Slack event to the server..."
  
  # Create a sample event
  EVENT_DATA='{
    "type": "event_callback",
    "event": {
      "type": "app_mention",
      "text": "@sahur analyze NullPointerException in UserService.processUserRequest",
      "user": "U12345678",
      "channel": "C12345678",
      "event_ts": "1621234567.123456",
      "ts": "1621234567.123456"
    },
    "team_id": "T12345678",
    "api_app_id": "A12345678",
    "event_id": "Ev12345678",
    "event_time": 1621234567
  }'
  
  # Send the event to the server
  RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d "$EVENT_DATA" http://localhost:8000/api/slack/events)
  
  # Extract the issue ID from the response
  ISSUE_ID=$(echo $RESPONSE | grep -o '"issue_id":"[^"]*"' | cut -d'"' -f4)
  
  if [ -n "$ISSUE_ID" ]; then
    print_success "Slack event processed successfully. Issue ID: $ISSUE_ID"
    echo $ISSUE_ID > .issue_id
  else
    print_error "Failed to process Slack event."
    exit 1
  fi
}

# Check the issue status
check_issue_status() {
  print_header "Checking Issue Status"
  
  if [ ! -f .issue_id ]; then
    print_error "Issue ID not found. Please run the simulate_slack_event step first."
    exit 1
  fi
  
  ISSUE_ID=$(cat .issue_id)
  print_info "Checking status of issue $ISSUE_ID..."
  
  # Get the issue status from the server
  RESPONSE=$(curl -s -X GET http://localhost:8000/api/issues/$ISSUE_ID)
  
  # Extract the status from the response
  STATUS=$(echo $RESPONSE | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
  
  if [ -n "$STATUS" ]; then
    print_success "Issue status: $STATUS"
  else
    print_error "Failed to get issue status."
    exit 1
  fi
}

# Open the web UI
open_web_ui() {
  print_header "Opening Web UI"
  
  if [ ! -f .issue_id ]; then
    print_error "Issue ID not found. Please run the simulate_slack_event step first."
    exit 1
  fi
  
  ISSUE_ID=$(cat .issue_id)
  URL="http://localhost:3000/issue/tracking/$ISSUE_ID"
  
  print_info "Opening web UI at $URL..."
  
  # Open the URL in the default browser
  if command -v xdg-open &> /dev/null; then
    xdg-open $URL
  elif command -v open &> /dev/null; then
    open $URL
  else
    print_info "Please open the following URL in your browser: $URL"
  fi
  
  print_success "Web UI opened."
}

# Clean up
cleanup() {
  print_header "Cleaning Up"
  
  print_info "Stopping Docker containers..."
  docker-compose down
  
  if [ $? -eq 0 ]; then
    print_success "Docker containers stopped successfully."
  else
    print_error "Failed to stop Docker containers."
  fi
  
  if [ -f .issue_id ]; then
    rm .issue_id
    print_success "Removed temporary files."
  fi
}

# Main function
main() {
  print_header "SAHUR Demonstration"
  
  check_prerequisites
  setup_environment
  start_services
  simulate_slack_event
  check_issue_status
  open_web_ui
  
  print_info "Press Enter to clean up and exit..."
  read
  
  cleanup
  
  print_header "Demonstration Completed"
  print_success "Thank you for trying SAHUR!"
}

# Run the main function
main
