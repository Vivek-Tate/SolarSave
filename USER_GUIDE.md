# User Guide

Solar Save is a desktop-centered web application powered by the Python Flask framework. It allows UK users to donate funds for constructing solar panels to listed organizations worldwide in order to offset their household's carbon footprint and make a positive impact on the environment.

The web application caters towards three different user types:
- __Householders__ form the largest part of the user base. These are users with a household in the UK that wish to offset their carbon footprint by donating funds for constructing solar panels towards organizations in other parts of the world.
- __Staff__ are concerned with analysing the donations made by householders. Anyone can register to apply to be a staff user, but their account needs to be approved by an administrator before it can be used.
- __Administrators__ (admins) are responsible for user management. Admins can view all registered users and have the power to suspend or delete their accounts.

## Administrator Pages

- __Admin Dashboard__ - Gives admins an overview of current page statistics along with a dynamic interactive table of all user accounts registered on Solar Save. Each user account can be suspended or deleted.


## Staff Pages

- __Staff Reports__ - Gives staff informative graphs about the donations made along with a dynamic interactive table of donations that allows searching and filtering. Aggregated donation data can be exported in table format to be processed further.


## Householder Pages

- __My Profile__ - Gives a householder an overview of their account information, along with a summary interesting facts about their donations, a call to invite friends to join Solar Save, badges relative to how much a householder has donated, highlighting the reduced carbon footprint through donating, and a complete list of all donations made by this user.
- __Home Page__ - This is the landing page of the website, aimed at introducing the user to Solar Save and using our interactive features to gain interest and engagement.
- __Browse Countries Page__ - Allows householders to browse and compare countries based relevant statistics such as potential carbon offset per donated solar panel, solar panel price, carbon emissions, etc. The list of countries is searchable and sort-able by the aforementioned statistics. A traffic light indicator shows how "good" a given country is for offsetting your carbon footprint.
- __Country Page__ - Each country offers a general description of the country and offers users a list of organisations that can be donated towards.
- __Donation Gateway__ - Householders must be logged in to be able to donate. Householders can decide how many solar panels to donate towards an organization in a given country. Payment is currently facilitated via PayPal.


## Authentication

- __Householder Registration & Login__ - Householders can either register through traditional e-mail and password authentication or use Google SSO.
- __Staff Registration__ - Anyone can register to apply to a staff account. This account will be suspended until reviewed and approved by an administrator.
- __Admin Registration__ - Administrator accounts need to be added manually to the database. This is in the interest of security.
