# web fonts api
自托管 Webfont 字体生成接口

docker build -t web-fonts-api .

## window
docker run -d --restart=always --name web-fonts-api -p 8000:80 -v /d/www/web-fonts-api:/app web-fonts-api

## linux
docker run -d --restart=always --name web-fonts-api -p 8000:80 -v /home/docker/web-fonts-api/app:/app web-fonts-api

浏览器访问 http://ip:8000/fonts

```
// POST JSON
{
  "dirname": "AlibabaPuHui",
  "content": "你好"
}
```