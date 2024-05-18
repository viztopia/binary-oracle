module.exports = {
    apps: [
      {
        name: "bot_api",
        script: "./bot_api.py",
        interpreter: ".venv/bin/python", // path to python binary in venv
        autorestart: true,
        watch: true,
        max_memory_restart: "500M" // optional, restart if exceeds 500MB memory
      }
    ]
  }