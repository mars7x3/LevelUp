FROM node:22.9.0-alpine as builder

WORKDIR /frontend

RUN npm install npm@latest -g

COPY ./frontend/package*.json ./

RUN npm install --legacy-peer-deps

COPY frontend .

RUN tsc --noUnusedLocals false && vite build

FROM nginx:alpine

COPY --from=builder /frontend/build /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]
