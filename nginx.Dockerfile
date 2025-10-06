FROM node:22.13.0-alpine as builder

WORKDIR /frontend

COPY ./frontend/package*.json ./
RUN npm install --legacy-peer-deps

COPY frontend .

RUN npm run build

FROM nginx:alpine
COPY --from=builder /frontend/dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]