module.exports = {
    apps: [
      {
        name: "bot_api",
        script: ".venv/bin/python", // path to python binary in venv
        args: "bot_api.py", // your script name
        interpreter: ".venv/bin/python", // path to python binary in venv
        virtualenv: ".venv", // path to virtualenv directory
        autorestart: true,
        watch: true,
        max_memory_restart: "500M" // optional, restart if exceeds 500MB memory
      }
    ]
  }