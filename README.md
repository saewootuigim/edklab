# Kim Lab Website

This repository contains the Django-based website for the **Kim Lab** at Syracuse University, led by **Eun-Deok Kim**.

The website provides information about the lab's research, members, publications, research opportunities, and contact information.

## About Kim Lab

Kim Lab is a plant molecular and cell biology research laboratory focused on understanding how genetic and epigenetic mechanisms establish cell fate and enable plants to adapt to changing environmental conditions.

The lab uses **stomata as a model system** to investigate:

* Chromatin regulatory dynamics involved in stem cell fate programming
* Cellular mechanisms involved in environmental adaptation
* Genetic and epigenetic regulation of cell fate

Research approaches include genomics and epigenomics, confocal microscopy, CRISPR genome editing, and traditional genetic, molecular biology, and biochemical methods.

## Website

Production website:

[https://www.ekimlab.com/](https://www.ekimlab.com/)

## Website Features

The site currently includes the following sections:

* **Home** — Introduction to Kim Lab and its research focus
* **People** — Current lab members and alumni
* **Publications** — Publications by Eun-Deok Kim and collaborators
* **Opportunities** — Information about available research positions
* **Contact** — Lab location and contact information

## Technology

The website is built using:

* **Python**
* **Django**
* **Bootstrap**
* HTML/CSS/JavaScript

The website uses Django's administration interface for managing site content.

## Deployment

The production website is hosted on **PythonAnywhere**.

Static files are collected using Django's `collectstatic` command and served separately from the Django application.

Typical deployment steps include:

```bash
python manage.py collectstatic
```

After updating the application code, the production web application should be reloaded on PythonAnywhere.

## Local Development

Clone the repository and create a Python virtual environment:

```bash
git clone <repository-url>
cd edklab
python -m venv django
```

Activate the virtual environment on Windows:

```bash
django\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

The development site should then be available at:

```text
http://127.0.0.1:8000/
```

## Static Files

For local development, Django's development server can serve static files automatically when configured appropriately.

For production, static files should be collected into the configured `STATIC_ROOT` directory:

```bash
python manage.py collectstatic
```

The generated static files should not normally be committed to Git.

## Repository Notes

Generated files and local development settings should not be committed to the repository. For example:

```gitignore
staticfiles/
.vscode/
__pycache__/
*.py[cod]
```

Keep production credentials, secret keys, and other sensitive configuration outside the repository.

## Research and Content

The website's content includes information about current lab members, publications related to plant development and gene regulation, and opportunities for postdoctoral fellows, graduate students, lab technicians, and undergraduate researchers.

For current information about the laboratory, please visit:

[https://www.ekimlab.com/](https://www.ekimlab.com/)

## Contact

**Kim Lab**<br>
456 Life Sciences Complex<br>
107 College Place<br>
Syracuse, NY 13244<br>

Email: [ekim112@syr.edu](mailto:ekim112@syr.edu)

The website's public contact information and research description are maintained by Kim Lab. ([KimLab][1])

---

© Eun-Deok Kim's Lab

[1]: https://www.ekimlab.com/ "KimLab | home"
