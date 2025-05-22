# Use Node.js LTS as the base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Disable Next.js telemetry
ENV NEXT_TELEMETRY_DISABLED=1

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of the application code
COPY . .

# Ensure public directory exists
RUN mkdir -p public

# Expose the port the app will run on
EXPOSE 3000

# Start the application
CMD ["npm", "run", "dev"] 