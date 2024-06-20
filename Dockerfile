FROM ubuntu:noble
RUN mkdir app
COPY . /app
CMD ["uname -a"]
