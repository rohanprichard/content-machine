# Docker Compose Quick Start

While Docker is great for running a *single* container, most modern applications need multiple pieces—like a web server and a database (e.g., your `content-machine` and `mongodb`!). 

Instead of typing out long `docker run` commands for each one and figuring out how to network them together, we use **Docker Compose**. Docker Compose lets you define your entire multi-container application in a single YAML file (`docker-compose.yml`).

## The `docker-compose.yml` File

Look at your project's `docker-compose.yml`. It defines "services":

```yaml
services:
  # Service 1: Your Python App
  content-machine:
    build: .                # Tells Compose to build the Dockerfile in this directory
    ports:
      - 8000:8000           # Maps localhost:8000 to container:8000
    environment:
      - DISCORD_TOKEN=xyz   # Passes environment variables

  # Service 2: The Database
  mongodb:
    image: mongo:latest     # Instead of building, it downloads a pre-made image from Docker Hub
    ports:
      - 27017:27017
    volumes:
      - mongodb_data:/data/db # Creates a persistent volume so data isn't lost when the container stops

volumes:
  mongodb_data:             # Defines the volume referenced above
```

### The Magic of Compose Networking

Notice how `content-machine` can connect to MongoDB using the URI `mongodb://mongodb:27017/`? 

Docker Compose automatically creates an isolated internal network for your services. **Services can talk to each other using their service names as hostnames.** `content-machine` just connects to `mongodb:27017` and Docker routes the traffic perfectly.

---

## Essential Commands

You must run these commands in the directory where your `docker-compose.yml` file is located.

### 1. Start Everything up

```bash
docker compose up
```
* **What it does:** Builds your images (if they aren't built yet), creates networks and volumes, and starts all containers defined in the file.
* **Pro-tip:** The logs of *all* your containers will stream to your terminal. Press `Ctrl+C` to stop everything.

### 2. Run in the Background

```bash
docker compose up -d
```
* **What it does:** The `-d` (detached) flag starts everything in the background, giving you your terminal back.

### 3. Rebuild After Code Changes

If you change your code or Dockerfile, you need to tell Compose to rebuild the image before starting:

```bash
docker compose up --build -d
```

### 4. See What's Running

```bash
docker compose ps
```
* Shows the status of all containers managed by this specific Compose file.

### 5. View Logs

```bash
# View logs for all services
docker compose logs -f

# View logs for just one specific service
docker compose logs -f content-machine
```

### 6. Stop Everything

```bash
docker compose down
```
* **What it does:** This stops and removes all containers and networks created by `up`. 
* *(Note: It does **not** delete your named volumes like `mongodb_data`, so your database data is perfectly safe!)*

## Summary Workflow

1. Define your multi-app setup in `docker-compose.yml`.
2. Start it: `docker compose up -d`
3. Edit your code.
4. Apply changes: `docker compose up --build -d`
5. Shut down when done for the day: `docker compose down`
