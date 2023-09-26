# eComSync 🛒- Integration of Amazon and eBay for eCommerce Online Retail Websites

## Overview
This REST service offers eCommerce websites to import sales/orders from third-party sellers such as Amazon and eBay to its platform(WooCommerce or Opencart). eCommerce website owners do not have to manually download the reports daily as a CSV file and upload those order details manually. Users with experience in databases can manually import orders through CSV files. Still, those who don't have a technical background might need to learn how to import the orders into MySQL database, which is primarily used in Opencart or WooCommerce.


## Install Dependencies

Before you can run the application, you will need to install the necessary dependencies. Here are the steps to do so:

1. Install Python: Python is a programming language that lets you work more quickly and integrate your systems more effectively. You can install it using the following commands:

```console
sudo apt install python3
mkdir ecommerce && cd ecommerce
```

The first command installs Python 3 on your system. The second command creates a new directory called 'ecommerce' and navigates into it.

2. Install Dependencies: Our application requires certain Python packages to run. These are listed in the `requirements.txt` file. You can install all of these at once using the following command:

```console
pip install -r requirements.txt

```

This command uses pip, the Python package installer, to install the packages listed in the requirements.txt file. These packages are necessary for the application to run correctly.

After following these steps, your environment should be set up with all the necessary dependencies to run the application.

## Instructions how to setup the application  environment and  database

To get your Flask application up and running, please follow these steps:

1. Activate your virtual environment: Use the command source ecomdev/bin/activate to activate the 'ecomdev' virtual environment. Virtual environments help to keep dependencies required by different projects separate. Install the virtualenv package using pip. virtualenv is a tool for creating isolated Python environments. 

```console
pip install virtualenv
virtualenv -p python3 ecomdev
source ecomdev/bin/activate
```
Remember to `deactivate` your virtual environment when you're done working on your project by using the command deactivate.

2. Set the `FLASK_APP` environment variable: The command `export FLASK_APP=ecomsync` tells Flask which application to run.

```console
export FLASK_APP=ecomsync
```

3. Set the `FLASK_ENV` environment variable: By using the command `export FLASK_ENV=ecomdev`, you're specifying the environment in which you are working. This is a good practice as it can enable features like debug mode in a development environment.

```console
export FLASK_ENV=ecomdev
```

4. Start the Flask development server: Finally, use the command `flask run` to start your application.
```console
flask run
```


5. To initialize and populate your database, please execute the following commands:

```console
flask init-db
flask testgen
```

These commands will respectively initialize your database and generate test data for your application.


6. To generate a master key for API access, you will need to use the `flask masterkey` command. This command is a custom command provided by our application for managing master keys.

```console
flask masterkey
```


Running Pylint for Code Quality Checks
---

To run Pylint on your Flask application, use the following commands:

Before running Pylint, you need to ensure it is installed. If it's not, you can install it using pip:

```console
pip install pylint
pylint ecomsync
```

Pylint will now check the ecomsync project or file and output any warnings, errors, or suggestions it has about your code. This is a good way to ensure that your code adheres to Python's best practices and is free of any easily avoidable errors.


How to run and test the API
---

How to setup and run the client
---

To initialize the frontend, execute the subsequent instructions within the frontend directory:

```console
npm install
npm run dev
```

`npm install`: This command is used to install all the dependencies of your project. When you run this command, npm (Node Package Manager) will look at your `package.json` file, locate all the dependencies listed under `dependencies` and `devDependencies`, and install them in your project's `node_modules` folder. This makes sure that your project has all the necessary libraries and tools it needs to run properly.

`npm run dev`: This command starts the Vite development server. In your package.json file, there will be a `scripts` section where dev is defined. In a Vite project, it is typically defined as `"dev": "vite"`. This means when you run npm run dev, it's essentially running the `vite` command. This starts the development server and serves your application at a local URL (usually `localhost:3000` or `localhost:5000`). The development server also enables features like hot module replacement, which means you can make changes to your code and see those changes in your browser without having to manually refresh the page.

The url to the entrypoint
---

You can interact with the frontend of our application by navigating to `http://localhost:5173/`.

To properly configure the application, there's an environment variable `VITE_ACCESS_KEY` that needs to be set in the `.env` file. This key is generated during the setup process when running the `flask masterkey` command.

Additionally, you can directly interact with the backend services via REST API at `http://localhost:5000.` Please note that to successfully make requests to the API, the generated access key must be included in the request headers. This ensures proper authorization and access control for the backend services.


__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__



