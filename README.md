<h2 align="center">Emergency Department Simulation 2.0</h2>

<!-- <div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/vbarrosos/nhs_ed_simulation/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/vbarrosos/nhs_ed_simulation/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div> -->

---

<p align="center"> This project builds up on the <a href="https://github.com/nottmhospitals/ed_simulation">Emergency Department Simulation</a>, by Ziad Ahmed & Shivam Missar, publicly available on the GitHub of Nottingham University Hospitals NHS Trust.
    <br> 
</p>

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [TODO](../TODO.md)
- [Contributing](../CONTRIBUTING.md)
- [Authors](#authors)
- [Acknowledgments](#acknowledgement)

## About <a name = "about"></a>

More details on this project can be found on the GitHub Repository hosting this project: <a href="https://github.com/nottmhospitals/ed_simulation">https://github.com/nottmhospitals/ed_simulation</a>. As the authors state, the goal is to "create a simulation that highlights resource optimization strategies to reduce patient wait times and improve efficiency within the ED."

Here, I use the original simulation code to build a web app that can be run on a browser, allowing the user to interactively set parameters for the simulation and run it using them. This is entirely developed in Python, and, in the future, I plan on including a version of the simulation written in R. 

### Project Structure <a name = "struct"></a>
```
├── R
├── README.md
├── data
│   └── simulation_report.pdf
└── python
    ├── ED Resource Reneged.ipynb
    ├── dash_app
    │   ├── app.py
    │   ├── assets
    │   │   ├── scripts.js
    │   │   └── stylesheet.css
    │   ├── callbacks.py
    │   ├── layout.py
    │   ├── models
    │   │   ├── simulation.py
    │   │   └── simulation_app.py
    │   ├── utils
    │   │   └── ref_parameters.py
    │   └── views
    │       ├── simulation_view.py
    │       └── table_view.py
    ├── requirements.txt
    ├── simulation_base.py
    └── test_simulation.ipynb
```
## Getting Started <a name = "getting_started"></a>

To get started with this project, follow the steps below to set up your environment and run the Dash app.

### Prerequisites

Ensure you have Python installed on your system. It is recommended to use Python 3.7 or higher. Additionally, it is highly recommended to use a virtual environment to manage dependencies and ensure compatibility across packages.

### Setting Up the Environment

1. **Clone the Repository**  
    Clone this repository to your local machine:
    ```bash
    git clone https://github.com/vbarrosos/nhs_ed_simulation.git
    cd nhs_ed_simulation/python
    ```

2. **Create a Virtual Environment**  
    Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**  
    Install the required Python packages listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Dash App

Once the dependencies are installed, you can run the Dash app:

1. Navigate to the `dash_app` directory:
    ```bash
    cd dash_app
    ```

2. Run the app:
    ```bash
    python app.py
    ```

3. Open your browser and go to `http://127.0.0.1:8050/` to interact with the simulation.

That's it! You now have the Dash app up and running. Make sure to keep your virtual environment activated while working on this project.

### Running the Test Simulation

You can also run the test simulation using the provided Jupyter notebook:

1. Navigate to the `python` directory:
    ```bash
    cd python
    ```

2. Open the `test_simulation.ipynb` notebook:
    ```bash
    jupyter notebook test_simulation.ipynb
    ```

3. Follow the instructions within the notebook to execute the test simulation and analyse the results.

This notebook provides a quick way to validate the simulation logic and experiment with different parameters interactively.

## Usage <a name="usage"></a>

The Dash app provides an interactive interface for running and analysing the Emergency Department simulation. 

Users can set various parameters, such as patient arrival rates, resource availability, and service times, directly through the web interface. Once the parameters are configured, the simulation can be executed, and the results, including visualisations and performance metrics, are displayed in real-time. This allows users to experiment with different scenarios and evaluate the impact of changes on ED efficiency and patient wait times. 

Once you are happy with your parameter choices, you can download a pdf with the compiled results of up to three simulations.

## Results <a name = "results"></a>

You can view the detailed simulation report, which includes analysis and results, directly below:

![Simulation Report](./data/simulation_report.pdf)

## Built Using <a name = "built_using"></a>

### Python
- SimPy - Discrete-event simulations
- Pandas - Data manipulation and analysis
- NumPy - Numerical and random generation
- Matplotlib - Plotting and data visualisation
- Dash - Dashboard creation

### R
- In preparation

## Authors <a name = "authors"></a>

- [@vbarrosos](https://github.com/vbarrosos) - Improvements & further analysis
- [Ziad Ahmed](ziad.ahmed@nhs.net) & [Shivam Missar](shivam.missar@nuh.nhs.uk) - Idea & Initial work
