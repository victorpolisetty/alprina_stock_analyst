## Run you own agent

### Get the code

1. Clone this repo:

    ```
    git clone https://github.com/victorpolisetty/alprina_stock_analyst.git
    ```

2. Create the virtual environment:

    ```
    cd alprina_stock_analyst
    poetry shell
    poetry install
    ```

3. Sync packages:

    ```
    autonomy packages sync --update-packages
    ```

### Prepare the data

1. Prepare a `keys.json` file containing wallet address and the private key for each of the four agents.

    ```
    autonomy generate-key ethereum -n 4
    ```

2. Prepare a `ethereum_private_key.txt` file containing one of the private keys from `keys.json`. Ensure that there is no newline at the end.

3. Deploy a [Safe on Gnosis](https://app.safe.global/welcome) (it's free) and set your agent addresses as signers. Set the signature threshold to 3 out of 4.

4. Fund your agents and Safe with a small amount of xDAI, i.e. $0.02 each.

5. Create an empty .env file:

6. Fill in the required environment variables in .env. These variables are: `ALL_PARTICIPANTS`, `SAFE_CONTRACT_ADDRESS`
