# Movie recommender

## Python setup

<details><summary> MacOS / Linux </summary>

Create a `venv`

```bash
cd server && python3 -m venv venv
```

Activate the `venv`

```bash
source venv/bin/activate
```

Install the required packages

```bash
pip install -r requirements.txt
```

Start the server by running `main.py`

```bash
python3 ./main.py
```

</details>

<details><summary> Windows </summary>

Create a `venv`

```bash
cd server && py -m venv venv
```

Activate the `venv`

```bash
venv\Scripts\activate
```

Install the required packages

```bash
pip install -r requirements.txt
```

Start the server by running `main.py`

```bash
python ./main.py
```

Server will run on `http://localhost:8080`

</details>

## Next.js setup

Install the required packages

```bash
cd client && npm install
```

Start the frontend

```bash
npm run dev
```

Frontend will run on `http://localhost:3000` or any available ports
