FROM node:20.15.0

# Set the working directory
WORKDIR /app

COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json

# Install dependencies
RUN npm install

# Copy project files
COPY . /app

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
