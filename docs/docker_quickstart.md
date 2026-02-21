# Docker Quick Start Guide

Welcome to Docker! Think of Docker as a magic shipping container for your applications. Instead of saying "it works on my machine," you package everything your app needs (code, tools, system libraries) into a container. Then, it runs *exactly* the same way on any other machine.

## Key Concepts

1. **Image**: The blueprint. It's a read-only template with instructions for creating a container (like a snapshot of an OS + your code).
2. **Container**: The running instance of an image. It's an isolated environment where your app actually runs.
3. **Dockerfile**: The text file containing instructions to build your image.

## Step 1: The Dockerfile

Look at your project's `Dockerfile`. It's essentially a recipe:

```dockerfile
# 1. Start with a base image (like installing an OS)
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy files from your computer into the container
COPY requirements.txt .

# 4. Run commands (like installing dependencies)
RUN pip install -r requirements.txt

# 5. Copy the rest of your app's code
COPY . .

# 6. Specify the command to run when the container starts
CMD ["python", "src/server.py"]
```

## Step 2: Building an Image

To turn that Dockerfile into an Image, you use the `build` command.

Open your terminal in the same folder as your `Dockerfile` and run:

```bash
docker build -t my-first-app .
```

* `-t my-first-app`: This "tags" (names) your image so you can find it later.
* `.`: This tells Docker to look for the Dockerfile in the current directory.

## Step 3: Running a Container

Now that you have your image, let's run it!

```bash
docker run -p 8000:8000 -d --name my-running-app my-first-app
```

* `-p 8000:8000`: This maps port 8000 on your *host machine* (your computer) to port 8000 *inside the container*. Now you can access your app at `http://localhost:8000`.
* `-d`: Runs the container in the background (detached mode), so it doesn't lock up your terminal.
* `--name my-running-app`: Gives your container a friendly name.
* `my-first-app`: The image we built in Step 2.

## Step 4: Managing Containers

Here are the most common commands you'll use everyday:

* **See what's running:**
  ```bash
  docker ps
  ```
  *(Add `-a` to see stopped containers too: `docker ps -a`)*

* **Stop a container:**
  ```bash
  docker stop my-running-app
  ```

* **Start a stopped container:**
  ```bash
  docker start my-running-app
  ```

* **Delete a container:** (Must be stopped first)
  ```bash
  docker rm my-running-app
  ```

* **View the logs of a container:**
  ```bash
  docker logs -f my-running-app
  ```
  *(The `-f` "follows" the logs, showing new output in real-time)*

* **Go inside a running container:** (Like SSHing into a server)
  ```bash
  docker exec -it my-running-app /bin/bash
  ```
  *(Type `exit` to get out)*

## Summary Workflow

1. Write Code
2. Update/Create `Dockerfile`
3. `docker build -t app-name .`
4. `docker run -p local_port:container_port app-name`
