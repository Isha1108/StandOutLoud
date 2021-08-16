# StandOutLoud

Steps to Run the code:
1.	Create a project folder in VScode. Open the folder and create virtual environment by running the command "python -m venv env" in the terminal.
2.	 Move app.py file, templates folder and static folder in the virtual environment created. 
3.	The Project made by us is “ShoutOutLoud. This is currently a Web Application and can be easily deployed into Android Application in the format of .apk .



Background
Considering the growing number of local businesses on a small scale, especially those which are initiated by women fail to get recognition due to various factors affecting their livelihood and family. There are many skilful women but just fail to find an opportunity in that field.
Introduction to Application
With Standoutloud, our application, we try to bring all the small-scale businesses at one place and do justice to their service and give a recognition to them. With help of Standoutloud, the business owners can post about them, kind of work they do and the service they provide. All this information will be visible to the common users like us, who can reach out to them if they want to and get their work done. This helps in local level recognition of the business and the word spreads out. If anyone wants to enrol for employment in any of the business, he can do that by contacting the owner where vacancies are available.
Moreover, if any professional organization/individual wants to fund/invest in any of the business, they can contact and take the process ahead.

The whole application is divided into 3 logins:
1.	Entrepreneur Login (small business owners)
2.	Customer Login (users who want the service of business)
3.	Investor Login (professional organization/individual)

Features
1.	Entrepreneur Login: 
a.	See Requests: Here the owner can see all the requests made by the customer with all required details. The owner can Accept/Decline the request accordingly.
b.	Feedbacks: Once the request is fulfilled by the owner, the feedback given by all the customers can be seen in the Feedbacks section.
c.	Payment History: All the records of previous transactions between owner and customer can be seen here.

2.	Customer Login:
a.	Make Request: The customer can search all the businesses in his locality and make request to specific owner by contacting. Once the request is completed, the customer can pay the decided amount to the owner.
b.	My Request History: Here the customer can view the status of the ongoing requests made by him and provide his genuine feedback.
c.	Employment Opportunity: Here the user can see all the nearby businesses and their profile along with their vacancies. If the user is interested to apply for the same, he can contact the owner via calling.



3.	Investor Login:
a.	Search Businesses: Here the investor can search any business and can contact them.
b.	Statistics: Here the investor can see the number of current sales of items/services of the business owners and their predicted growth in a month which will help investor to make a decision. 

Tech Stack:
Frontend: HTML/CSS/JavaScript

Backend: Flask (Python)

Database: MySQL

Machine Learning: XGBOOST and lightgbm (for predicting the sales for next month)

Payment: Razorpay Integration


