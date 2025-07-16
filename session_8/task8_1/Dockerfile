# Use a minimal image
FROM busybox:latest

RUN mkdir /www

# ASCII art touch
RUN echo -e "\
   (\_/)\n\
  ( •_•)\n\
 / >🌮 Looking forward to lunch?\n" > /www/index.html

# Start HTTP server on port 8080
CMD ["httpd", "-f", "-p", "8080", "-h", "/www"]
