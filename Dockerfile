FROM node:18-alpine
RUN apk add --no-cache python3 py3-pip
WORKDIR /app
COPY package.json ./
RUN npm install
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["npm", "start"]  // 或自定义启动脚本
