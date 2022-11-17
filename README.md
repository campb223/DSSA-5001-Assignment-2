# DSSA-5001-Assignment-2

## Overview
For assignment 2, you are tasked with creating an email extrapolation program in Python. <br>
Email extrapolation is identifying the pattern of an email username for a specific company, <br>
then applying this pattern for other people who work for the same company to extrapolate their email <br>
<br>
Your dataset will consist of the following data fields and contain approximately 1000 records: <br>
    - Company Name<br>
    - Company Website<br>
    - Contact (Full Name)<br>
    - First Name<br>
    - Last Name<br>
    - Email (From third party provider)<br>

### Example
Say you have the following data for a contact at AG Monitoring: <br>
    + First Name: Cameron<br>
    + Last Name: Richter<br>
    + Email: crichter@agmonitoring.com<br>
<br>
The program should identify that the email pattern for the above username as first initial, last name.<br>
<br>
This pattern can then be applied to AG Monitoring employees that do not have a provided email.<br>

    + First Name: Matthew
    + Last Name: Nunes
<br>
The extrapolated email for Matthew Nunes would be <b>mnunes@agmonitoring.com</b><br>

## Deliverables 
Your deliverable is an additional column in the dataset, called Email Extrapolated, that contains the <br>
extrapolated email for each contact in the dataset, along with the Python code that executes the task. <br>
<br>
Keep in mind, you may need to clean the data. <br>
<br>
    + First Name: Cliff<br>
    + Last Name: Baldwin, PhD<br>
<br>
If a company has more than one email pattern from our third-party email source, do not extrapolate any emails for that company. 
