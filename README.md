# Project Name

This project automatically retrieves data from a public Excel sheet and provides analytics through a Streamlit app. 

## Getting Started

To get started, clone this repository and install the required dependencies using pip:

```
pip install -r requirements.txt
```

Next, create a .env file in the root directory of the project and add the password for the analytics link (example in .example.env):

```
OPENAI_API_KEY="api_key"
ANALYTICS_PASSWORD="analytics_password"
```

Run the app using the following command:
```
streamlit run app.py
```

This will launch the app in your default web browser. You can access the analytics page by appending /?analytics=on to the URL and entering the password you set in the .env file.

## Deploy to streamlit

After deploying to streamlit, you need to set environment variable by accessing `Manage app` -> Three dots settings -> `Setting` -> `Secrets`.

