# binary-oracle


# Installation on Linux server with virtual environment

### Download the repository and navigate to the directory

git clone https://github.com/viztopia/binary-oracle.git
cd binary-oracle

### Create a virtual environment (use python3.10 or above)

python3.10 -m venv .venv

### Activate the virtual environment

source .venv/bin/activate

### Install the requirements

pip install -r requirements.txt

### copy the example environment file to a local .env file and update values as needed
cp example.env .env

### Put bot personas in the `bot_personas` directory if needed

### Serve the bot api endpoint
python3.10 bot_api.py
