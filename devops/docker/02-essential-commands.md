# 2. Essential Docker Commands

## 1. Build an image

```bash
docker build -t my-api .
```

```text
docker build   = build an image
-t my-api      = name it "my-api"
.              = find the Dockerfile in the current folder
```

```text
Dockerfile + code -> my-api image
```

## 2. Run a container

```bash
docker run --name my-api-container -p 8000:8000 my-api
```

```text
docker run                = start a new container
--name my-api-container   = container name
-p 8000:8000              = laptop port : container port
my-api                    = image to run
```

```text
my-api image -> my-api-container -> running app
```

The image and container can have different names.

## 3. Run in the background

```bash
docker run -d --name my-api-container -p 8000:8000 my-api
```

`-d` means run in the background so you can continue using the terminal.

## 4. See containers

```bash
docker ps
```

Shows only running containers.

```bash
docker ps -a
```

`-a` means all. It also shows stopped containers.

## 5. See logs

```bash
docker logs -f my-api-container
```

```text
logs                    = show application output
-f                      = keep showing new logs
my-api-container        = container to read
```

Press `Ctrl + C` to stop watching. The container continues running.

## 6. Stop and delete a container

```bash
docker stop my-api-container
docker rm my-api-container
```

```text
stop -> stops the running app
rm   -> removes the stopped container
```

The original `my-api` image is not deleted.

## 7. See images

```bash
docker image ls
```

```text
image = work with images
ls    = list them
```

## 8. Open a shell inside a container

```bash
docker exec -it my-api-container sh
```

```text
exec               = run a command inside a running container
-it                = let you type and see the output
my-api-container   = container name
sh                 = open its terminal
```

Use this for checking problems. Do not manually change production code inside the container.

## Complete flow

```text
docker build -> image
docker run   -> running container
docker logs  -> view its output
docker stop  -> stop it
docker rm    -> remove it
```
